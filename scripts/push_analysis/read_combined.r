# This script analyzes the combined push and purchase data to understand push timing patterns, 
# specifically how long customers wait without purchase before receiving a push notification.

library(dplyr)
library(ggplot2)
library(lubridate)
library(data.table)

# set the working directory
setwd("/home/litao/Coffee/")

data <- read.csv("model-free/data/processed/combined_data_1000.csv")

#########################################################
# After how long without purchase will there be a push?
#########################################################

# Convert to data.table for efficient row-wise operations
setDT(data)

# Initialize a list to store results
result_list <- list()

for (i in seq_len(nrow(data))) {
  if (data$push[i] == 0) {
    if (i + 1 <= nrow(data) && data$push[i + 1] == 1 &&
          !is.na(data$days_since_last_purchase[i + 1])) {
      result_list[[length(result_list) + 1]] <- data.frame(
        member_id = data$member_id[i + 1],
        days_since_last_purchase = data$days_since_last_purchase[i + 1]
      )
    }
  }
}

# Combine all results
result_df <- do.call(rbind, result_list)

# Now plot as before
p1 <- ggplot(result_df, aes(x = days_since_last_purchase)) +
  geom_histogram(binwidth = 1) +
  labs(x = "Days from last purchase to first push", y = "Frequency") +
  theme_minimal()

ggsave("model-free/plots/days_since_last_purchase_to_first_push.pdf",
       plot = p1, width = 8, height = 6)

data1_filt <- result_df %>%
  filter(days_since_last_purchase <= 50)

p2 <- ggplot(data1_filt, aes(x = days_since_last_purchase)) +
  geom_histogram(binwidth = 1) +
  labs(x = "Days from last purchase to first push", y = "Frequency") +
  theme_minimal()

ggsave("model-free/plots/days_since_last_purchase_to_first_push0-50.pdf",
       plot = p2, width = 8, height = 6)

#########################################################
# time between two pushes
#########################################################
selected_columns2 <- c("push", "days_since_last_push")

data2 <- data %>%
  select(all_of(selected_columns2)) %>%
  filter(push == 1) %>%
  filter(!is.na(days_since_last_push)) %>%
  filter(days_since_last_push <= 20)

p3 <- ggplot(data2, aes(x = days_since_last_push)) +
  geom_histogram(binwidth = 1) +
  labs(x = "Days between two pushes", y = "Frequency") +
  theme_minimal()

ggsave("model-free/plots/days_between_two_pushes.pdf",
       plot = p3, width = 8, height = 6)

#########################################################
# pushed coupon and discount
#########################################################
selected_columns3 <- c("push", "coupon", "discount")

coupon_data <- data %>%
  select(all_of(selected_columns3)) %>%
  filter(push == 1) %>%
  filter(!is.na(coupon))

# unique coupons and counts
print(coupon_data %>%
        group_by(coupon) %>%
        summarise(count = n()) %>%
        arrange(desc(count)))

discount_data <- data %>%
  select(all_of(selected_columns3)) %>%
  filter(push == 1) %>%
  filter(!is.na(discount))

# unique discounts and counts
print(discount_data %>%
        group_by(discount) %>%
        summarise(count = n()) %>%
        arrange(desc(count)))

#########################################################
# pushes whose action_type is 3, extract days_since_last_push
#########################################################
selected_columns4 <- c("push", "action_type", "days_since_last_push")

action_type_3_data <- data %>%
  select(all_of(selected_columns4)) %>%
  filter(push == 1) %>%
  filter(action_type == 3) %>%
  filter(!is.na(days_since_last_push)) %>%
  filter(days_since_last_push <= 20)

p4 <- ggplot(action_type_3_data, aes(x = days_since_last_push)) +
  geom_histogram(binwidth = 1) +
  labs(x = "Days since last push", y = "Frequency") +
  theme_minimal()

ggsave("model-free/plots/days_since_last_push_expiration.pdf",
       plot = p4, width = 8, height = 6)


#########################################################
# purchase_discount
#########################################################
selected_columns5 <- c("push", "purchase_discount")

purchase_discount_data <- data %>%
  select(all_of(selected_columns5)) %>%
  filter(push == 0) %>%
  filter(!is.na(purchase_discount))

print(purchase_discount_data %>%
        group_by(purchase_discount) %>%
        summarise(count = n()) %>%
        arrange(desc(count)))
