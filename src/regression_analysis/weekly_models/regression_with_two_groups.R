#!/usr/bin/env Rscript

# Customer Behavior Analysis - Two Groups Comparison (push=0 vs push=1)
# This script extends regression_no_push_customers.R to compare both groups

# -- Load required packages -------------------------------------------------
library("data.table")
library("lubridate")
library("lfe")

# -- Study parameters -------------------------------------------------------
set.seed(42)

START_DATE <- as.Date("2020-06-01")
END_DATE <- as.Date("2021-12-31")
TOTAL_WEEKS <- as.integer(floor(as.numeric(END_DATE - START_DATE) / 7)) + 1
EXCLUDED_PRODUCT_IDS <- c(1, 2, 3, 4, 5, 6, 7, 8, 26, 30, 31, 72, 73, 74, 156, 182, 205, 235, 253)
SLEEP_THRESHOLDS <- c(4, 8, 12)
RECENT_WINDOW <- 2

# -- Create output directories ----------------------------------------------
dir.create("outputs/data", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/results", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/plots", recursive = TRUE, showWarnings = FALSE)
dir.create("outputs/logs", recursive = TRUE, showWarnings = FALSE)

# -- Load push preference data ---------------------------------------------
cat("Loading push preference data...\n")
no_push_members <- fread("../../data/processed/no_push_members.csv", encoding = "UTF-8")
no_push_member_ids <- unique(no_push_members$member_id)
cat(sprintf("Loaded %d customers with push=0\n", length(no_push_member_ids)))

############################################################################
# Step 1: Customer Data Preparation
############################################################################

# 1.1 Load customer transaction data
cat("Loading transaction data...\n")
orders_all <- fread("../../data/processed/order_commodity_result_processed.csv", encoding = "UTF-8")
orders_all$dt <- as.Date(orders_all$dt)

# 1.2 Split into two groups based on push preference
cat("Splitting customers into two groups...\n")
orders_all[, push_group := ifelse(member_id %in% no_push_member_ids, 0, 1)]
cat(sprintf("Push=0 group: %d customers\n", length(unique(orders_all[push_group == 0]$member_id))))
cat(sprintf("Push=1 group: %d customers\n", length(unique(orders_all[push_group == 1]$member_id))))

# 1.3 Find each customer's primary store
cat("Finding primary stores for customers...\n")
order_result <- fread("../../data/data1031/order_result.csv", encoding = "UTF-8",
                      select = c("member_id", "order_type", "dept_id"))

# Print percentage of order_type == 0 orders
total_orders <- nrow(order_result)
order_type_0_count <- sum(order_result$order_type == 0)
order_type_0_pct <- (order_type_0_count / total_orders) * 100
cat(sprintf("Total orders: %d\n", total_orders))
cat(sprintf("Order type == 0 orders: %d (%.2f%%)\n", order_type_0_count, order_type_0_pct))


# Keep only order_type == 0 (delivery orders)
order_result <- order_result[order_type == 0]

# Count orders per customer per store
store_counts <- order_result[, list(order_count = .N), 
                             by = list(member_id, dept_id)]

# Calculate total orders per customer (across all stores)
customer_total_orders <- order_result[, list(total_orders = .N), by = member_id]

# For each customer, find the store with most orders
# If tie, pick the store with smaller dept_id
setorder(store_counts, member_id, -order_count, dept_id)
primary_stores <- store_counts[, .SD[1], by = member_id]
primary_stores <- primary_stores[, list(member_id, primary_dept_id = dept_id, primary_store_orders = order_count)]

# Merge with customer total orders to calculate ratio
primary_stores <- merge(primary_stores, customer_total_orders, by = "member_id")
primary_stores[, primary_store_ratio := primary_store_orders / total_orders]

# Print statistics about primary store ratio
cat("\n--- Primary Store Statistics ---\n")
cat(sprintf("Mean ratio of orders from primary store: %.4f\n", mean(primary_stores$primary_store_ratio)))
cat(sprintf("Median ratio of orders from primary store: %.4f\n", median(primary_stores$primary_store_ratio)))
cat(sprintf("Min ratio of orders from primary store: %.4f\n", min(primary_stores$primary_store_ratio)))
cat(sprintf("Max ratio of orders from primary store: %.4f\n", max(primary_stores$primary_store_ratio)))
cat(sprintf("Customers with 100%% orders from primary store: %d (%.2f%%)\n", 
            sum(primary_stores$primary_store_ratio == 1), 
            (sum(primary_stores$primary_store_ratio == 1) / nrow(primary_stores)) * 100))

# Keep only necessary columns
primary_stores <- primary_stores[, list(member_id, primary_dept_id)]

# 1.4 Keep only orders at primary store
cat("Filtering to primary store orders...\n")
orders_all <- merge(orders_all, primary_stores, 
                    by.x = "member_id", by.y = "member_id")
orders_all <- orders_all[dept_id == primary_dept_id]
orders_all[, primary_dept_id := NULL]

# 1.5 Exclude specified products
cat("Applying product filters...\n")
orders_all <- orders_all[!(product_id %in% EXCLUDED_PRODUCT_IDS)]

# Add week number (week 1 starts at START_DATE)
orders_all[, week_id := as.integer(floor(as.numeric(dt - START_DATE) / 7)) + 1]

# 1.6 Rename for consistency
setnames(orders_all, "member_id", "customer_id")

# 1.7 Create Customer-Week Panel
cat("Creating customer-week panel...\n")

# Count orders per customer per week
weekly_orders <- orders_all[, list(orders = .N), 
                            by = list(customer_id, dept_id, week_id, push_group)]

# Find first purchase week for each customer (across all departments)
customer_first_week <- orders_all[, list(first_week = min(week_id)), 
                                  by = customer_id]

# Get unique customer-store combinations
customer_store_pairs <- unique(weekly_orders[, list(customer_id, dept_id, push_group)])

# Add first week to customer-store pairs
customer_store_pairs <- merge(customer_store_pairs, customer_first_week, 
                              by = "customer_id", all.x = TRUE)

# Create all possible week IDs
all_weeks <- data.table(week_id = 1:TOTAL_WEEKS)

# Cross join customer-store pairs with all weeks
customer_store_pairs[, dummy := 1]
all_weeks[, dummy := 1]

# Cross join using the dummy key
full_panel <- merge(customer_store_pairs, all_weeks, by = "dummy", allow.cartesian = TRUE)

# Remove dummy column
full_panel[, dummy := NULL]

# 1.8 Filter to keep only weeks > first_week
full_panel <- full_panel[week_id > first_week]

# Merge with actual orders
customer_panel <- merge(full_panel, weekly_orders, 
                        by = c("customer_id", "dept_id", "week_id", "push_group"), 
                        all.x = TRUE)
customer_panel[, first_week := NULL]

# Fill missing orders with 0
customer_panel[is.na(orders), orders := 0]

# Sort for easier calculation
setorder(customer_panel, customer_id, dept_id, week_id)

# Calculate weeks without ordering (sleep weeks)
cat("Calculating sleep weeks...\n")

# Create function to calculate consecutive zeros
calculate_sleep_weeks <- function(order_vector) {
  n <- length(order_vector)
  sleep_count <- integer(n)
  
  if (n < 2) return(sleep_count)
  
  # First week is always 0
  sleep_count[1] <- 0
  
  # Calculate from second week
  current_streak <- if (order_vector[1] == 0) 1 else 0
  
  for (i in 2:n) {
    sleep_count[i] <- current_streak
    # Update for next week
    if (order_vector[i] == 0) {
      current_streak <- current_streak + 1
    } else {
      current_streak <- 0
    }
  }
  
  return(sleep_count)
}

# Apply the function to each customer-store group
customer_panel[, weeks_sleep := calculate_sleep_weeks(orders), 
               by = list(customer_id, dept_id)]

# Create sleep indicators for different thresholds
for (thr in SLEEP_THRESHOLDS) {
  indicator_name <- paste0("sleep_gt_", thr)
  customer_panel[, (indicator_name) := as.integer(weeks_sleep > thr)]
}

# Filter customers (similar to original script)
cat("Filtering customers...\n")
customer_active_weeks <- customer_panel[orders > 0, list(
  active_weeks = .N,
  total_orders = sum(orders)
), by = customer_id]

single_week_customers <- customer_active_weeks[active_weeks == 1]
customers_with_high_weekly_orders <- customer_panel[orders > 14, unique(customer_id)]
customers_to_remove <- unique(c(single_week_customers$customer_id, customers_with_high_weekly_orders))

customer_panel <- customer_panel[!(customer_id %in% customers_to_remove)]

############################################################################
# Step 2: Create Push Panel
############################################################################

# 2.1 Load push data files
cat("Loading push data...\n")
push_files <- list.files("../../data/data1031", pattern = "sleep_push_result_.*\\.csv", full.names = TRUE)
cat(sprintf("Found %d push files\n", length(push_files)))

all_push_data_list <- list()
for (file in push_files) {
  push_data <- fread(file, encoding = "UTF-8",
                     select = c("dt", "member_id", "trigger_tag", "coupon", "discount"))
  all_push_data_list[[length(all_push_data_list) + 1]] <- push_data
}

all_push_data <- rbindlist(all_push_data_list)
all_push_data$dt <- as.Date(all_push_data$dt)
setnames(all_push_data, "member_id", "customer_id")

# 2.2 Add week_id and push_group to push data
cat("Processing push data...\n")
all_push_data[, week_id := as.integer(floor(as.numeric(dt - START_DATE) / 7)) + 1]
all_push_data[, push_group := ifelse(customer_id %in% no_push_member_ids, 0, 1)]

cat(sprintf("Push=0 group: %d push records\n", nrow(all_push_data[push_group == 0])))
cat(sprintf("Push=1 group: %d push records\n", nrow(all_push_data[push_group == 1])))

# 2.3 Aggregate pushes by customer-week (total pushes)
cat("Aggregating pushes by customer-week...\n")
push_panel_total <- all_push_data[, list(
  total_pushes = .N
), by = list(customer_id, week_id, push_group)]

# 2.4 Aggregate pushes by customer-week and trigger_tag
cat("Aggregating pushes by customer-week and trigger type...\n")
push_panel_by_trigger <- all_push_data[, list(
  push_count = .N
), by = list(customer_id, week_id, push_group, trigger_tag)]

# Reshape to wide format (one column per trigger type)
push_panel_wide <- dcast(push_panel_by_trigger, 
                         customer_id + week_id + push_group ~ trigger_tag,
                         value.var = "push_count",
                         fill = 0)

# Rename columns to have prefix "pushes_trigger_"
trigger_cols <- setdiff(names(push_panel_wide), c("customer_id", "week_id", "push_group"))
for (col in trigger_cols) {
  setnames(push_panel_wide, col, paste0("pushes_trigger_", col))
}

# 2.5 Merge push panel with customer panel
cat("Merging push panel with customer panel...\n")
customer_panel <- merge(customer_panel, push_panel_total,
                       by = c("customer_id", "week_id", "push_group"),
                       all.x = TRUE)

customer_panel <- merge(customer_panel, push_panel_wide,
                       by = c("customer_id", "week_id", "push_group"),
                       all.x = TRUE)

# Fill missing push counts with 0
customer_panel[is.na(total_pushes), total_pushes := 0]
push_cols <- names(customer_panel)[grepl("^pushes_trigger_", names(customer_panel))]
for (col in push_cols) {
  customer_panel[is.na(get(col)), (col) := 0]
}

cat("Push panel creation complete!\n")

############################################################################
# Step 3: Store-Product Timeline (using complete order database)
############################################################################

# 3.1 Load the complete order database
cat("Creating store-product timeline...\n")
complete_orders <- fread("../../data/processed/order_commodity_result_processed.csv", 
                         encoding = "UTF-8",
                         select = c("dept_id", "dt", "product_id"))

# 3.2 Convert date column to Date type and filter by date range
cat("Processing dates...\n")
complete_orders$dt <- as.Date(complete_orders$dt)

# Exclude specified product IDs
complete_orders <- complete_orders[!(product_id %in% EXCLUDED_PRODUCT_IDS)]

# Add week_id based on START_DATE
complete_orders[, week_id := as.integer(floor(as.numeric(dt - START_DATE) / 7)) + 1]

# 3.3 Calculate product lifecycle for each store
cat("Calculating product lifecycle per store...\n")

# For each store-product combination, find:
# - First week sold (introduction)
# - Last week sold (removal)
product_lifecycle <- complete_orders[, list(
  first_week = min(week_id),
  last_week = max(week_id)
), by = list(dept_id, product_id)]

# 3.4 Count new products introduced each week at each store
cat("Counting new product introductions per week...\n")
new_products_count <- product_lifecycle[, list(
  new_products = .N,
  new_product_ids = paste(sort(product_id), collapse = ",")
), by = list(dept_id, week_id = first_week)]

# 3.5 Count products removed each week at each store
cat("Counting product removals per week...\n")
removed_products_count <- product_lifecycle[, list(
  removed = .N,
  removed_product_ids = paste(sort(product_id), collapse = ",")
), by = list(dept_id, week_id = last_week)]

# 3.6 Create store-week panel
cat("Creating store-week panel...\n")

# Get all unique stores from the complete database
unique_stores <- unique(complete_orders$dept_id)
cat(sprintf("- Number of unique stores: %d\n", length(unique_stores)))

cat("Loading store-week availability data...\n")
dept_week_data <- fread("../../data/data1031/dept_result_week_order.csv", 
                        encoding = "UTF-8",
                        select = c("dept_id", "monday_date"))

dept_week_data$monday_date <- as.Date(dept_week_data$monday_date)
dept_week_data[, week_id := as.integer(floor(as.numeric(monday_date - START_DATE) / 7)) + 1]

store_week_combinations <- unique(dept_week_data[, list(dept_id, week_id)])
cat(sprintf("- Total store-week combinations: %d\n", nrow(store_week_combinations)))

store_week_combinations <- store_week_combinations[
  store_week_combinations[, 
                          .(first_week = min(week_id), 
                            last_week = max(week_id)), 
                          by = dept_id
  ], 
  on = "dept_id"
][week_id >= first_week + 4 & week_id <= last_week - 4, 
  .(dept_id, week_id)
]

# Merge with new products count
store_panel <- copy(store_week_combinations)
store_panel <- merge(store_panel, new_products_count, 
                     by = c("dept_id", "week_id"), all.x = TRUE)

# Merge with removed products count
store_panel <- merge(store_panel, removed_products_count, 
                     by = c("dept_id", "week_id"), all.x = TRUE)

# Fill missing values with 0 (for weeks with no new/removed products)
store_panel[is.na(new_products), new_products := 0]
store_panel[is.na(removed), removed := 0]

# 3.7 Create lagged variables
cat("Creating lagged variables...\n")

# Function to create lagged variables
create_lagged_variables <- function(data, var_name, max_lag = 3) {
  # Create lag0 (current week)
  data[, paste0(var_name, "_lag0") := get(var_name)]
  
  # Create lag1 to lagmax
  for (lag_num in 1:max_lag) {
    lag_col_name <- paste0(var_name, "_lag", lag_num)
    
    # For each store, shift the values
    data[, (lag_col_name) := shift(get(var_name), n = lag_num, fill = 0), by = dept_id]
  }
  
  return(data)
}

# Apply to new_products and removed
store_panel <- create_lagged_variables(store_panel, "new_products")
store_panel <- create_lagged_variables(store_panel, "removed")

# 3.8 Save product lifecycle information
cat("Saving product lifecycle data...\n")
fwrite(product_lifecycle, "outputs/data/product_lifecycle_detailed.csv")
fwrite(store_panel, "outputs/data/store_week_panel_complete.csv")
cat("Store-product timeline creation complete!\n")

############################################################################
# Step 4: Merge Panels and Add Product Details
############################################################################

# 4.1 Merge customer panel with store information
cat("Merging customer and store panels...\n")
analysis_panel <- merge(customer_panel, store_panel, 
                        by = c("dept_id", "week_id"), all.x = FALSE, all.y = FALSE)

# 4.2 Identify recent vs existing products
cat("Identifying recent vs existing products...\n")

# Add first_week to each order
orders_with_firstweek <- merge(orders_all[, list(customer_id, dept_id, product_id, week_id)],
                               product_lifecycle[, list(dept_id, product_id, first_week)],
                               by = c("dept_id", "product_id"),
                               all.x = TRUE)

# Calculate week difference
orders_with_firstweek[, week_diff := week_id - first_week]

# Create flags using vectorized ifelse
orders_with_firstweek[, is_new_recent := as.integer(week_diff >= 0 & week_diff <= RECENT_WINDOW)]
orders_with_firstweek[, is_existing := as.integer(week_diff > RECENT_WINDOW)]

# Remove helper column if not needed
orders_with_firstweek[, week_diff := NULL]

# Count purchases by type for each customer-store-week
product_counts <- orders_with_firstweek[, list(
  purchases_new_recent = sum(is_new_recent),
  purchases_existing = sum(is_existing)
), by = list(customer_id, dept_id, week_id)]

# 4.3 Merge product counts with analysis panel
product_panel <- merge(analysis_panel, product_counts,
                       by = c("customer_id", "dept_id", "week_id"), all.x = TRUE)

# Fill missing counts with 0
product_panel[is.na(purchases_new_recent), purchases_new_recent := 0]
product_panel[is.na(purchases_existing), purchases_existing := 0]

# Create indicator for whether customer bought new or existing products
product_panel[, bought_new := as.integer(purchases_new_recent > 0)]
product_panel[, bought_existing := as.integer(purchases_existing > 0)]

############################################################################
# Step 5: Save Intermediate Data
############################################################################

cat("Saving intermediate data files...\n")

fwrite(customer_panel, "outputs/data/customer_week_panel.csv")
fwrite(analysis_panel, "outputs/data/analysis_dataset.csv")
fwrite(product_panel, "outputs/data/product_panel.csv")

cat("Data preparation complete!\n")

############################################################################
# Step 6: Run Regression Models for Both Groups
############################################################################

cat("Running regression models for both groups...\n")

# 6.1 Split data into two groups
cat("Splitting data into two groups...\n")
analysis_panel_push0 <- analysis_panel[push_group == 0]
analysis_panel_push1 <- analysis_panel[push_group == 1]
product_panel_push0 <- product_panel[push_group == 0]
product_panel_push1 <- product_panel[push_group == 1]

cat(sprintf("Push=0 group: %d observations\n", nrow(analysis_panel_push0)))
cat(sprintf("Push=1 group: %d observations\n", nrow(analysis_panel_push1)))

# 6.2 Run Model A (Basic model) for both groups
cat("\nRunning Model A for both groups...\n")

# Model A for push=0
cat("Model A - Push=0 group...\n")
model_a_push0 <- felm(orders ~ new_products_lag1 + removed_lag1 | customer_id + week_id + dept_id + week_id:dept_id,
                      data = analysis_panel_push0)

# Model A for push=1
cat("Model A - Push=1 group...\n")
model_a_push1 <- felm(orders ~ new_products_lag1 + removed_lag1 | customer_id + week_id + dept_id + week_id:dept_id,
                      data = analysis_panel_push1)

# 6.3 Run Model A with push variables (for combined analysis)
cat("\nRunning Model A with push variables (combined analysis)...\n")

# Get push variable names (pushes_trigger_*)
push_vars <- names(analysis_panel)[grepl("^pushes_trigger_", names(analysis_panel))]

# Model A with total pushes
cat("Model A with total_pushes...\n")
model_a_with_pushes <- felm(orders ~ new_products_lag1 + removed_lag1 + total_pushes | 
                             customer_id + week_id + dept_id + week_id:dept_id,
                             data = analysis_panel)

# Model A with push variables by trigger type (if available)
if (length(push_vars) > 0) {
  # Use top trigger types (e.g., trigger 1, 2, 3)
  main_trigger_vars <- c("pushes_trigger_1", "pushes_trigger_2", "pushes_trigger_3")
  available_trigger_vars <- intersect(main_trigger_vars, push_vars)
  
  if (length(available_trigger_vars) > 0) {
    cat(sprintf("Model A with trigger-specific push variables: %s\n", paste(available_trigger_vars, collapse=", ")))
    
    # Build formula with available trigger variables
    push_formula <- paste(available_trigger_vars, collapse = " + ")
    formula_str <- paste("orders ~ new_products_lag1 + removed_lag1 +", push_formula, 
                        "| customer_id + week_id + dept_id + week_id:dept_id")
    
    model_a_with_trigger_pushes <- felm(as.formula(formula_str), data = analysis_panel)
  }
}

# 6.4 Run Model_B_threshold_4 with total_pushes for both groups
cat("\nRunning Model_B_threshold_4 with total_pushes for both groups...\n")

# Model_B_threshold_4 for push=0
cat("Model_B_threshold_4 - Push=0 group...\n")
model_b_thr4_push0 <- felm(orders ~ new_products_lag1 + removed_lag1 + sleep_gt_4 + 
                            new_products:sleep_gt_4 + removed:sleep_gt_4 + total_pushes | 
                            customer_id + week_id + dept_id + week_id:dept_id,
                            data = analysis_panel_push0)

# Model_B_threshold_4 for push=1
cat("Model_B_threshold_4 - Push=1 group...\n")
model_b_thr4_push1 <- felm(orders ~ new_products_lag1 + removed_lag1 + sleep_gt_4 + 
                            new_products:sleep_gt_4 + removed:sleep_gt_4 + total_pushes | 
                            customer_id + week_id + dept_id + week_id:dept_id,
                            data = analysis_panel_push1)

# 6.5 Run Model_C with total_pushes for both groups
cat("\nRunning Model_C with total_pushes for both groups...\n")

# Model_C for push=0
cat("Model_C - Push=0 group...\n")
model_c_push0 <- felm(purchases_existing ~ new_products_lag1 + removed_lag1 + total_pushes | 
                      customer_id + week_id + dept_id + week_id:dept_id,
                      data = product_panel_push0)

# Model_C for push=1
cat("Model_C - Push=1 group...\n")
model_c_push1 <- felm(purchases_existing ~ new_products_lag1 + removed_lag1 + total_pushes | 
                      customer_id + week_id + dept_id + week_id:dept_id,
                      data = product_panel_push1)

# 6.6 Run Model_A_distributed with total_pushes for both groups
cat("\nRunning Model_A_distributed with total_pushes for both groups...\n")

# Model_A_distributed for push=0
cat("Model_A_distributed - Push=0 group...\n")
model_a_dist_push0 <- felm(orders ~ new_products_lag1 + new_products_lag2 + new_products_lag3 + 
                            removed_lag1 + removed_lag2 + removed_lag3 + total_pushes | 
                            customer_id + week_id + dept_id + week_id:dept_id,
                            data = analysis_panel_push0)

# Model_A_distributed for push=1
cat("Model_A_distributed - Push=1 group...\n")
model_a_dist_push1 <- felm(orders ~ new_products_lag1 + new_products_lag2 + new_products_lag3 + 
                            removed_lag1 + removed_lag2 + removed_lag3 + total_pushes | 
                            customer_id + week_id + dept_id + week_id:dept_id,
                            data = analysis_panel_push1)

# 6.7 Extract and compare coefficients
cat("\nExtracting and comparing coefficients...\n")

# Function to extract regression results
extract_results <- function(model, model_name, group_name = "") {
  if (is.null(model)) return(NULL)
  
  # Get summary
  summ <- summary(model)
  
  # Extract coefficients
  coefs <- summ$coefficients
  coef_df <- data.table(
    term = rownames(coefs),
    estimate = coefs[, "Estimate"],
    std_error = coefs[, "Std. Error"],
    t_value = coefs[, "t value"],
    p_value = coefs[, "Pr(>|t|)"],
    model = model_name,
    group = group_name,
    n_obs = summ$N,
    r_squared = summ$r.squared,
    adj_r_squared = summ$adj.r.squared
  )
  
  return(coef_df)
}

# Extract results for all models
all_results_list <- list()

# Model A for both groups
all_results_list[["Model_A_push0"]] <- extract_results(model_a_push0, "Model_A", "push_0")
all_results_list[["Model_A_push1"]] <- extract_results(model_a_push1, "Model_A", "push_1")

# Model A with pushes
if (exists("model_a_with_pushes")) {
  all_results_list[["Model_A_with_pushes"]] <- extract_results(model_a_with_pushes, "Model_A_with_pushes", "combined")
}

if (exists("model_a_with_trigger_pushes")) {
  all_results_list[["Model_A_with_trigger_pushes"]] <- extract_results(model_a_with_trigger_pushes, 
                                                                        "Model_A_with_trigger_pushes", 
                                                                        "combined")
}

# Model_B_threshold_4 with total_pushes for both groups
all_results_list[["Model_B_thr4_push0"]] <- extract_results(model_b_thr4_push0, "Model_B_threshold_4", "push_0")
all_results_list[["Model_B_thr4_push1"]] <- extract_results(model_b_thr4_push1, "Model_B_threshold_4", "push_1")

# Model_C with total_pushes for both groups
all_results_list[["Model_C_push0"]] <- extract_results(model_c_push0, "Model_C", "push_0")
all_results_list[["Model_C_push1"]] <- extract_results(model_c_push1, "Model_C", "push_1")

# Model_A_distributed with total_pushes for both groups
all_results_list[["Model_A_dist_push0"]] <- extract_results(model_a_dist_push0, "Model_A_distributed", "push_0")
all_results_list[["Model_A_dist_push1"]] <- extract_results(model_a_dist_push1, "Model_A_distributed", "push_1")

# Combine all results
all_results <- rbindlist(all_results_list, fill = TRUE)

# 6.5 Create coefficient comparison table
cat("\nCreating coefficient comparison table...\n")

# Key variables to compare
key_vars <- c("new_products_lag1", "removed_lag1", "total_pushes",
              "sleep_gt_4", "new_products:sleep_gt_4", "removed:sleep_gt_4",
              "new_products_lag2", "new_products_lag3",
              "removed_lag2", "removed_lag3")

# Filter results for key variables
coef_comparison <- all_results[term %in% key_vars]

# Filter to only push_0 and push_1 groups
coef_comparison_filtered <- coef_comparison[group %in% c("push_0", "push_1")]

# Check if we have data to reshape
if (nrow(coef_comparison_filtered) > 0 && 
    all(c("term", "group", "estimate", "std_error", "p_value") %in% names(coef_comparison_filtered))) {
  # Reshape to compare push_0 vs push_1
  # First reshape estimate
  coef_estimate <- dcast(coef_comparison_filtered, term ~ group, 
                        value.var = "estimate", fill = NA)
  if ("push_0" %in% names(coef_estimate)) setnames(coef_estimate, "push_0", "estimate_push_0")
  if ("push_1" %in% names(coef_estimate)) setnames(coef_estimate, "push_1", "estimate_push_1")
  
  # Reshape std_error
  coef_std_error <- dcast(coef_comparison_filtered, term ~ group, 
                          value.var = "std_error", fill = NA)
  if ("push_0" %in% names(coef_std_error)) setnames(coef_std_error, "push_0", "std_error_push_0")
  if ("push_1" %in% names(coef_std_error)) setnames(coef_std_error, "push_1", "std_error_push_1")
  
  # Reshape p_value
  coef_p_value <- dcast(coef_comparison_filtered, term ~ group, 
                        value.var = "p_value", fill = NA)
  if ("push_0" %in% names(coef_p_value)) setnames(coef_p_value, "push_0", "p_value_push_0")
  if ("push_1" %in% names(coef_p_value)) setnames(coef_p_value, "push_1", "p_value_push_1")
  
  # Merge all together
  coef_comparison_wide <- coef_estimate
  if (nrow(coef_std_error) > 0 && "term" %in% names(coef_std_error)) {
    coef_comparison_wide <- merge(coef_comparison_wide, coef_std_error, by = "term", all.x = TRUE)
  }
  if (nrow(coef_p_value) > 0 && "term" %in% names(coef_p_value)) {
    coef_comparison_wide <- merge(coef_comparison_wide, coef_p_value, by = "term", all.x = TRUE)
  }
} else {
  # Create empty data.table with expected structure
  coef_comparison_wide <- data.table(term = character(0))
}

# Calculate difference
if ("estimate_push_0" %in% names(coef_comparison_wide) && 
    "estimate_push_1" %in% names(coef_comparison_wide)) {
  coef_comparison_wide[, difference := estimate_push_1 - estimate_push_0]
  coef_comparison_wide[, pct_difference := (difference / estimate_push_0) * 100]
}

# Save comparison table
fwrite(coef_comparison_wide, "outputs/results/coefficient_comparison.csv")
fwrite(all_results, "outputs/results/regression_results_all.csv")

cat("\n=== COEFFICIENT COMPARISON ===\n")
print(coef_comparison_wide)

############################################################################
# Step 7: Summary Statistics
############################################################################

cat("\n\n=== SUMMARY STATISTICS ===\n")

# Overall statistics
cat("\n--- Overall Statistics ---\n")
cat(sprintf("Total customers (push=0): %d\n", length(unique(analysis_panel_push0$customer_id))))
cat(sprintf("Total customers (push=1): %d\n", length(unique(analysis_panel_push1$customer_id))))
cat(sprintf("Total observations (push=0): %d\n", nrow(analysis_panel_push0)))
cat(sprintf("Total observations (push=1): %d\n", nrow(analysis_panel_push1)))

# Push statistics
cat("\n--- Push Statistics ---\n")
cat(sprintf("Average weekly pushes (push=0): %.2f\n", mean(analysis_panel_push0$total_pushes, na.rm=TRUE)))
cat(sprintf("Average weekly pushes (push=1): %.2f\n", mean(analysis_panel_push1$total_pushes, na.rm=TRUE)))

# Order statistics
cat("\n--- Order Statistics ---\n")
cat(sprintf("Average weekly orders (push=0): %.2f\n", mean(analysis_panel_push0$orders)))
cat(sprintf("Average weekly orders (push=1): %.2f\n", mean(analysis_panel_push1$orders)))

# Key coefficient differences
cat("\n--- Key Coefficient Differences ---\n")
if (nrow(coef_comparison_wide) > 0) {
  n_to_show <- min(3, nrow(coef_comparison_wide))
  for (i in seq_len(n_to_show)) {
    var_name <- coef_comparison_wide$term[i]
    if ("difference" %in% names(coef_comparison_wide)) {
      diff_val <- coef_comparison_wide$difference[i]
      cat(sprintf("%s: Difference = %.4f\n", var_name, diff_val))
    }
  }
}

cat("\nAnalysis complete! Results saved to outputs/results/\n")
