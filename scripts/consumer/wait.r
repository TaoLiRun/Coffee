# This script analyzes whether purchases with coupons decrease consumers' tendency to purchase without coupons in the future.
# It examines the relationship between discount usage and subsequent purchase behavior.

library(dplyr)
library(ggplot2)
library(lubridate)
library(data.table)

# set the working directory
setwd("/home/litao/Coffee/")

# ======================================
# PART 1: LOAD AND PREPARE ORDER DATA
# ======================================

# Read the order CSV file with selected columns
order_data <- read.csv("data/data1031/order_result.csv") %>%
  select(member_id, order_id, create_hour, disount_tag,
         coffee_discount, coffee_commodity_num, coffee_top_commodity_num) %>%
  filter(coffee_commodity_num > 0) %>%
  filter(complete.cases(.))

# Convert create_hour to date-time format
order_data$create_hour <- as.POSIXct(order_data$create_hour,
                                     format = "%Y-%m-%d %H")
order_data$date <- as.Date(order_data$create_hour)

# Sort data by member_id and create_hour
order_data <- order_data %>%
  arrange(member_id, create_hour)

# Define high and low discount thresholds
high_discount_threshold <- 0.5  # 50% or more is considered high discount
low_discount_threshold <- 0.4   # Below 50% is considered low discount

# Create indicators for high and low discount purchases
order_data$high_discount <-
  ifelse(!is.na(order_data$coffee_discount) &
           order_data$coffee_discount >= high_discount_threshold, 1, 0)
order_data$low_discount <-
  ifelse(!is.na(order_data$coffee_discount) &
           order_data$coffee_discount <= low_discount_threshold &
           order_data$coffee_discount > 0, 1, 0)

# Sample members from order data
set.seed(123) # For reproducibility
# First find customers with at least 5 purchases
frequent_buyers <- order_data %>%
  group_by(member_id) %>%
  summarise(purchase_count = n()) %>%
  filter(purchase_count >= 5) %>%
  pull(member_id)
# Then sample from those frequent buyers
sampled_members <- sample(frequent_buyers, min(1000, length(frequent_buyers)))


# Filter order data to include only sampled members
order_data_sampled <- order_data %>%
  filter(member_id %in% sampled_members)


# For each customer, create a time series of their purchase history with coupon status # nolint
customer_history <- order_data_sampled %>%
  group_by(member_id) %>%
  arrange(create_hour) %>%
  mutate(
    purchase_num = row_number(),
    days_since_last_purchase =
      as.numeric(difftime(create_hour, lag(create_hour), units = "days")),
    cum_high_discount_purchases = cumsum(high_discount),
    high_discount_ratio = cum_high_discount_purchases / purchase_num,
    had_high_discount_before =
      ifelse(lag(cum_high_discount_purchases, default = 0) > 0, 1, 0)
  ) %>%
  ungroup()

# examine the relationship between high discount ratio and coffee_discount
ggplot(customer_history, aes(x = high_discount_ratio, y = coffee_discount)) +
  geom_point() +
  geom_smooth(method = "lm") +
  labs(title = "Relationship between High Discount Ratio and Coffee Discount",
       x = "High Discount Ratio",
       y = "Coffee Discount")
# save the plot
ggsave("model-free/plots/high_discount_ratio_coffee_discount.png")
