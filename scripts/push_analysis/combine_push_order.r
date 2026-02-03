# This script combines push notification data with order data to analyze the relationship between marketing pushes and customer purchases.
# It randomly samples consumers and merges their push history with purchase history for analysis.

library(dplyr)
library(ggplot2)
library(lubridate)
library(data.table)

# set the working directory
setwd("/home/litao/Coffee/")
num_samples <- 1000

read_and_process_data <- function(seed = 123) {
  # Set random seed for reproducibility
  set.seed(seed)

  # Read order data
  selected_columns <- c("member_id", "create_hour", "coffee_commodity_num",
                        "not_coffee_commodity_num", "use_coupon_num",
                        "coffee_discount", "drink_not_coffee_discount") # nolint
  order_data <- read.csv("data/data1031/order_result.csv") %>%
    select(all_of(selected_columns))

  # Randomly select num_samples unique consumers
  selected_consumers <- order_data %>%
    group_by(member_id) %>% # nolint
    summarise(purchase_count = n()) %>%
    filter(purchase_count >= 5) %>% # nolint
    pull(member_id)

  selected_consumers <- sample(selected_consumers,
                               min(num_samples, length(selected_consumers)))

  # Filter order data for selected consumers
  # replace all NA with 0
  filtered_order_data <- order_data %>%
    filter(member_id %in% selected_consumers) %>%# nolint
    mutate(across(where(is.numeric), ~ ifelse(is.na(.), 0, .)))

  filtered_order_data <- filtered_order_data %>%
    group_by(member_id, create_hour) %>% # nolint
    summarise(
      coffee_commodity_num = sum(coffee_commodity_num), # nolint
      not_coffee_commodity_num = sum(not_coffee_commodity_num), # nolint
      use_coupon_num = sum(use_coupon_num), # nolint
      coffee_discount = mean(coffee_discount), # nolint
      drink_not_coffee_discount = mean(drink_not_coffee_discount), # nolint
      .groups = "drop"
    ) %>%
    rename(dt = create_hour)

  # Convert dt to date type
  filtered_order_data$dt <- as.Date(filtered_order_data$dt)

  # combine coffee_discount and drink_not_coffee_discount: take the mean
  filtered_order_data <- filtered_order_data %>%
    mutate(commodity_num = coffee_commodity_num + not_coffee_commodity_num) %>% # nolint
    mutate(purchase_discount = (coffee_discount * coffee_commodity_num + drink_not_coffee_discount * not_coffee_commodity_num) / commodity_num) %>% # nolint
    select(-c(not_coffee_commodity_num, coffee_commodity_num)) %>% # nolint
    select(-c(coffee_discount, drink_not_coffee_discount))

  # Find all push data files
  push_files <- list.files(path = "data/data1031/",
                           pattern = "^sleep_push_result_.*\\.csv$",
                           full.names = TRUE)

  # Read and combine all push data
  all_push_data <- lapply(push_files, function(file) {
    read.csv(file) %>%
      select(dt, member_id, action_type, coupon, discount) %>% # nolint
      filter(member_id %in% selected_consumers, # nolint
             (!is.na(coupon) | !is.na(discount)))
  }) %>%
    bind_rows() %>%
    rename(push_dt = dt)

  list(
    order_data = filtered_order_data,
    push_data = all_push_data,
    selected_consumers = selected_consumers
  )
}

combine_push_order <- function(order_data, push_data) {
  # First, process order data to add basic customer history metrics
  customer_history <- order_data %>%
    group_by(member_id) %>% # nolint
    arrange(dt) %>%
    mutate(
      purchase_index = row_number(),
      days_since_last_purchase =
        as.numeric(difftime(dt, lag(dt), units = "days")),
      # Calculate running averages for discount and coupon usage
      # excluding current order by using lag of cummean
      prev_order_discount_level = lag(cummean(purchase_discount)), # nolint
      prev_order_coupon_usage = lag(cummean(use_coupon_num)) # nolint
    ) %>%
    ungroup()

  # Add push indicator column to order data (push = 0 for purchase data)
  customer_history <- customer_history %>%
    mutate(push = 0)

  # Process push data to calculate action counts and averages between orders
  # First calculate prev_dt for each order
  push_metrics <- customer_history %>%
    select(member_id, dt) %>%  # First select only the columns we need # nolint
    group_by(member_id) %>% # nolint
    arrange(dt) %>%
    mutate(
      prev_dt = lag(dt),
      # For first order,
      # use a date far in the past to capture all previous pushes
      prev_dt = as.Date(ifelse(is.na(prev_dt), "2000-01-01", as.character(prev_dt))) # nolint
    ) %>%
    ungroup() %>%
    # Create a cross join with push data, but only for the same member_id
    # and where push date is between previous order and current order
    left_join(
      push_data,
      by = "member_id",
      relationship = "many-to-many"
    ) %>%
    # Filter pushes that occurred between previous order and current order
    filter(push_dt <= dt & push_dt > prev_dt)  %>% # nolint
    # Add push indicator column (push = 1 for push data)
    mutate(push = 1) %>%
    # Calculate days since last push for each push
    group_by(member_id) %>% # nolint
    arrange(push_dt) %>%
    mutate(
      days_since_last_push =
        as.numeric(difftime(push_dt, lag(push_dt), units = "days"))
    ) %>%
    ungroup()

  # Calculate aggregated metrics for each order (keeping original approach)
  push_aggregated <- push_metrics %>%
    group_by(member_id, dt) %>% # nolint
    summarise(
      difftime_push_num_a1 = sum(action_type == 1, na.rm = TRUE), # nolint
      difftime_push_num_a2 = sum(action_type == 2, na.rm = TRUE), # nolint
      difftime_push_num_a3 = sum(action_type == 3, na.rm = TRUE), # nolint
      difftime_push_coupon_level = ifelse(all(is.na(coupon)), NA, max(coupon, na.rm = TRUE)), # nolint
      difftime_push_discount_level = ifelse(all(is.na(discount)), NA, min(discount, na.rm = TRUE)), # nolint
      .groups = "drop" # nolint
    )

  # Join the aggregated push metrics back to customer history
  customer_history <- customer_history %>%
    left_join(push_aggregated, by = c("member_id", "dt")) %>%
    # Replace NA values with 0 for action counts and means
    mutate(
      difftime_push_num_a1 = ifelse(is.na(difftime_push_num_a1), 0, difftime_push_num_a1), # nolint
      difftime_push_num_a2 = ifelse(is.na(difftime_push_num_a2), 0, difftime_push_num_a2), # nolint
      difftime_push_num_a3 = ifelse(is.na(difftime_push_num_a3), 0, difftime_push_num_a3), # nolint
    )

  # Prepare push data for merging (keep original columns)
  push_data_for_merge <- push_metrics %>%
    select(member_id, push_dt, action_type, coupon, discount, push, days_since_last_push) %>% # nolint
    rename(dt = push_dt) %>% # nolint
    # Ensure dt is converted to Date type to match customer_history
    mutate(dt = as.Date(dt)) # nolint

  # Merge purchase data with push data
  combined_data <- bind_rows(
    customer_history,
    push_data_for_merge
  ) %>%
    arrange(member_id, dt) # nolint

  # Now calculate days_since_last_purchase for push rows
  # For each push row, find the most recent purchase date (last row with push=0)
  combined_data <- combined_data %>%
    group_by(member_id) %>% # nolint
    arrange(dt) %>%
    mutate(
      # For push rows, calculate days since last purchase
      days_since_last_purchase = ifelse(
        push == 1, # nolint
        # Find the most recent purchase date (last row with push=0 before current row) # nolint
        sapply(1:n(), function(i) { # nolint
          if (push[i] == 1) { # nolint
            # Get all purchase dates before this push
            purchase_dates <- dt[push == 0 & dt < dt[i]] # nolint
            if (length(purchase_dates) > 0) {
              # Calculate days since the most recent purchase
              as.numeric(difftime(dt[i], max(purchase_dates), units = "days"))
            } else {
              NA  # No previous purchase found
            }
          } else {
            days_since_last_purchase[i]  # Keep original value for purchase rows # nolint
          }
        }),
        days_since_last_purchase  # Keep original value for purchase rows
      )
    ) %>%
    ungroup() %>%
    arrange(member_id, dt)

  # don't want the rows push =1 and days_since_last_push = 0
  # (satisfied at the same time)
  combined_data <- combined_data %>%
    filter(!(push == 1 & days_since_last_push == 0)) # nolint

  as.data.frame(combined_data)
}

process_data <- function() {
  # Read and process data
  data_list <- read_and_process_data()

  # Print some basic information about the data
  cat("Number of selected consumers:",
      length(data_list$selected_consumers), "\n")
  cat("Number of orders:", nrow(data_list$order_data), "\n")
  cat("Number of push records:", nrow(data_list$push_data), "\n")

  # Print unique coupon and discount values in push data
  cat("\nUnique coupons in push data:",
      unique(data_list$push_data$coupon), "\n")
  cat("Unique discounts in push data:",
      unique(data_list$push_data$discount), "\n")

  # Print first few rows of each dataset
  cat("\nFirst few rows of order data:\n")
  print(head(data_list$order_data))

  cat("\nFirst few rows of push data:\n")
  print(head(data_list$push_data))

  # print the push data of member_id 20187
  #cat("\nPush data of member_id 20187:\n") # nolint
  #print(data_list$push_data[data_list$push_data$member_id == 20187, ]) # nolint

  combined_data <- combine_push_order(data_list$order_data,
                                      data_list$push_data)

  # Print information about the combined dataset
  cat("\nCombined dataset information:\n")
  cat("Total rows:", nrow(combined_data), "\n")
  cat("Purchase rows (push=0):", sum(combined_data$push == 0), "\n")
  cat("Push rows (push=1):", sum(combined_data$push == 1), "\n")

  # column names
  cat("\nColumn names of combined data:\n")
  print(colnames(combined_data))

  cat("\nFirst few rows of purchase data (push=0):\n")
  purchase_data <- combined_data[combined_data$push == 0, ]
  print(head(purchase_data[, c("member_id", "dt", "purchase_index", "purchase_discount", # nolint
                               "days_since_last_purchase", "prev_order_discount_level", # nolint
                               "difftime_push_num_a2", "difftime_push_discount_level", "push")])) # nolint

  cat("\nFirst few rows of push data (push=1):\n")
  push_data_combined <- combined_data[combined_data$push == 1, ]
  print(head(push_data_combined[, c("member_id", "dt", "action_type", "coupon", "discount", # nolint
                                    "days_since_last_push", "push")])) # nolint

  # save to csv
  write.csv(combined_data,
            paste0("model-free/combined_data_", num_samples, ".csv"),
            row.names = FALSE)

}

plot_data1 <- function() {
  # plot the days_since_last_purchase vs prev_order_discount_level
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(prev_order_discount_level), # nolint
           !is.na(days_since_last_purchase)) # nolint
  customer_history <- customer_history %>%
    filter(prev_order_discount_level < 0.8, # nolint
           prev_order_discount_level > 0.2, # nolint
           days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = prev_order_discount_level, # nolint
                  y = days_since_last_purchase, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Previous Order Discount Level",
         y = "Days Since Last Purchase",
         title = "Purchase Patterns by Member") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/member_purchase_patterns.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint

}

plot_data2 <- function() {
  # plot the difftime_push_discount_level vs days_since_last_purchase
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(difftime_push_discount_level), # nolint
           !is.na(days_since_last_purchase)) # nolint
  customer_history <- customer_history %>%
    filter(days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = days_since_last_purchase, # nolint
                  y = difftime_push_discount_level, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Days Since Last Purchase",
         y = "Push Discount Level",
         title = "Days Since Last Purchase vs Push Discount") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/push_discount_patterns.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data3 <- function() {
  # plot the difftime_push_discount_level vs prev_order_discount_level
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(difftime_push_discount_level), # nolint
           !is.na(prev_order_discount_level)) # nolint
  customer_history <- customer_history %>%
    filter(prev_order_discount_level < 0.8, # nolint
           prev_order_discount_level > 0.2) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = prev_order_discount_level, # nolint
                  y = difftime_push_discount_level, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Previous Order Discount Level",
         y = "Push Discount Level",
         title = "Push Discount vs Previous Order Discount") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/discount_comparison.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data4 <- function() {
  # plot the days_since_last_purchase (x) vs coffee_discount (y)
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(coffee_discount), # nolint
           !is.na(days_since_last_purchase)) # nolint
  # delete the rows days_since_last_purchase is more than 365 or negative
  customer_history <- customer_history %>%
    filter(days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = days_since_last_purchase, # nolint
                  y = coffee_discount, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Days Since Last Purchase",
         y = "Current Order Discount",
         title = "Current Order Discount vs Days Since Last Purchase") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/current_discount_patterns.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data5 <- function() {
  # plot the purchase_index vs prev_order_discount_level
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(prev_order_discount_level), # nolint
           !is.na(purchase_index)) # nolint

  # Filter out extreme values
  customer_history <- customer_history %>%
    filter(prev_order_discount_level < 0.8, # nolint
           prev_order_discount_level > 0.2) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = purchase_index, # nolint
                  y = prev_order_discount_level, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Purchase Index",
         y = "Previous Order Discount Level",
         title = "Previous Order Discount Level vs Purchase Index") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/discount_by_purchase_index.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data6 <- function() {
  # plot the purchase_index (x) vs days_since_last_purchase (y)
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(days_since_last_purchase), # nolint
           !is.na(purchase_index)) # nolint

  # Filter out extreme values for days_since_last_purchase
  customer_history <- customer_history %>%
    filter(days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0,
           purchase_index <= 50) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = purchase_index, # nolint
                  y = days_since_last_purchase, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Purchase Index",
         y = "Days Since Last Purchase",
         title = "Days Since Last Purchase vs Purchase Index") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/purchase_timing_patterns.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data7 <- function() {
  # plot the frequency of days_since_last_purchase

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for purchase data only (push=0)
  customer_history <- customer_history %>%
    filter(push == 0)

  # Remove any rows with NA values in the variable we need
  customer_history <- customer_history %>%
    filter(!is.na(days_since_last_purchase)) # nolint

  # Filter out extreme values for days_since_last_purchase
  customer_history <- customer_history %>%
    filter(days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0) # nolint

  # Create the histogram
  p <- ggplot(customer_history,
              aes(x = days_since_last_purchase)) + # nolint
    # Add histogram with frequency
    geom_histogram(binwidth = 1,
                   fill = "#0066CC",
                   color = "#003366",
                   alpha = 0.7) +
    # Add labels and theme
    labs(x = "Days Since Last Purchase",
         y = "Frequency",
         title = "Frequency Distribution of Days Since Last Purchase") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/days_since_last_purchase_frequency.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data8 <- function() {
  # plot the days_since_last_push vs discount for push data
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for push data only (push=1)
  customer_history <- customer_history %>%
    filter(push == 1)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(discount), # nolint
           !is.na(days_since_last_push)) # nolint

  # Filter out extreme values for days_since_last_push
  customer_history <- customer_history %>%
    filter(days_since_last_push <= 90, # nolint
           days_since_last_push >= 0) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = days_since_last_push, # nolint
                  y = discount, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Days Since Last Push",
         y = "Push Discount",
         title = "Push Discount vs Days Since Last Push") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/push_discount_timing.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

plot_data9 <- function() {
  # plot the days_since_last_purchase vs discount for push data
  # This demonstrates the updated days_since_last_purchase for push rows
  # for each member_id, and add a trend line

  # read the customer_history.csv
  customer_history <- read.csv(paste0("model-free/combined_data_",
                                      num_samples, ".csv"),
                               row.names = NULL)

  # Filter for push data only (push=1)
  customer_history <- customer_history %>%
    filter(push == 1)

  # Remove any rows with NA values in the variables we need
  customer_history <- customer_history %>%
    filter(!is.na(discount), # nolint
           !is.na(days_since_last_purchase)) # nolint

  # Filter out extreme values for days_since_last_purchase
  customer_history <- customer_history %>%
    filter(days_since_last_purchase <= 90, # nolint
           days_since_last_purchase >= 0) # nolint

  # Create the line plot
  p <- ggplot(customer_history,
              aes(x = days_since_last_purchase, # nolint
                  y = discount, # nolint
                  group = member_id)) + # nolint
    # Add lines for each member with a single blue color and transparency
    geom_line(color = "#0066CC",
              alpha = 0.3,
              size = 0.5) +
    # Add a trend line to show the overall pattern
    geom_smooth(aes(group = 1),
                color = "#003366",
                size = 1.5,
                se = TRUE,
                method = "loess") +
    # Add labels and theme
    labs(x = "Days Since Last Purchase (for push data)",
         y = "Push Discount",
         title = "Push Discount vs Days Since Last Purchase (Push Data)") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14),
      axis.title = element_text(size = 12),
      axis.text = element_text(size = 10),
      panel.grid.major = element_line(color = "gray90"),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "white", color = NA)
    )

  # Save the plot
  ggsave("model-free/plots/push_discount_vs_purchase_timing.pdf",
         p, width = 6, height = 4, device = "pdf") # nolint
}

# Run the main function if this script is run directly
if (!interactive()) {
  process_data() # nolint
  #plot_data1()
  #plot_data2()
  #plot_data3()
  #plot_data4()
  #plot_data5()
  #plot_data6()
  #plot_data7()
  #plot_data8()
  #plot_data9()
}