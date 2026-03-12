#!/usr/bin/env Rscript

# Customer Behavior Analysis - Simplified Version

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

############################################################################
# Step 1: Customer Data Preparation
############################################################################

# 1.1 Load customer transaction data
cat("Loading transaction data...\n")
orders_filtered <- fread("../../data/processed/order_member_no_push.csv", encoding = "UTF-8")
orders_filtered$dt <- as.Date(orders_filtered$dt)

# 1.2 Find each customer's primary store
cat("Finding primary stores for customers...\n")
order_result <- fread("data1031/order_result.csv", encoding = "UTF-8",
                      select = c("member_id", "order_type", "dept_id"))

# Keep only customers in our filtered orders
customer_ids <- unique(orders_filtered$member_id)
order_result <- order_result[member_id %in% customer_ids]

# Keep only order_type == 0 (regular orders)
order_result <- order_result[order_type == 0]

# Count orders per customer per store
store_counts <- order_result[, list(order_count = .N), 
                             by = list(member_id, dept_id)]

# For each customer, find the store with most orders
# If tie, pick the store with smaller dept_id
setorder(store_counts, member_id, -order_count, dept_id)
primary_stores <- store_counts[, .SD[1], by = member_id]
primary_stores <- primary_stores[, list(member_id, primary_dept_id = dept_id)]

# 1.3 Keep only orders at primary store
cat("Filtering to primary store orders...\n")
orders_filtered <- merge(orders_filtered, primary_stores, 
                         by.x = "member_id", by.y = "member_id")
orders_filtered <- orders_filtered[dept_id == primary_dept_id]
orders_filtered[, primary_dept_id := NULL]

# 1.4 Exclude specified products
cat("Applying product filters...\n")
orders_filtered <- orders_filtered[!(product_id %in% EXCLUDED_PRODUCT_IDS)]

# Add week number (week 1 starts at START_DATE)
orders_filtered[, week_id := as.integer(floor(as.numeric(dt - START_DATE) / 7)) + 1]

# 1.5 Rename for consistency
setnames(orders_filtered, "member_id", "customer_id")
orders_all <- orders_filtered

############################################################################
# Step 2: Create Customer-Week Panel
############################################################################

cat("Creating customer-week panel...\n")

# 2.1 Count orders per customer per week
weekly_orders <- orders_all[, list(orders = .N), 
                            by = list(customer_id, dept_id, week_id)]

# Find first purchase week for each customer (across all departments)
customer_first_week <- orders_all[, list(first_week = min(week_id)), 
                                  by = customer_id]

# Get unique customer-store combinations
customer_store_pairs <- unique(weekly_orders[, list(customer_id, dept_id)])

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

# 2.2 Filter to keep only weeks >= first_week
full_panel <- full_panel[week_id >= first_week]

# Merge with actual orders
customer_panel <- merge(full_panel, weekly_orders, 
                        by = c("customer_id", "dept_id", "week_id"), 
                        all.x = TRUE)

# 2.3 Fill missing orders with 0
customer_panel[is.na(orders), orders := 0]

# Sort for easier calculation
setorder(customer_panel, customer_id, dept_id, week_id)

# 2.4 Calculate weeks without ordering (sleep weeks)
cat("Calculating sleep weeks...\n")

# Create function to calculate consecutive zeros
calculate_sleep_weeks <- function(order_vector) {
  n <- length(order_vector)
  sleep_count <- integer(n)
  
  if (n < 2) return(sleep_count)
  
  # 第一周总是为0
  sleep_count[1] <- 0
  
  # 从第二周开始计算
  current_streak <- if (order_vector[1] == 0) 1 else 0
  
  for (i in 2:n) {
    sleep_count[i] <- current_streak
    # 更新为下一周做准备
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

# 2.5 Create sleep indicators for different thresholds
for (thr in SLEEP_THRESHOLDS) {
  indicator_name <- paste0("sleep_gt_", thr)
  customer_panel[, (indicator_name) := as.integer(weeks_sleep > thr)]
}

# 2.6 Analyze customers with only one week of non-zero orders
cat("Analyzing customers with single purchase week...\n")

# Count non-zero order weeks per customer
customer_active_weeks <- customer_panel[orders > 0, list(
  active_weeks = .N,
  total_orders = sum(orders)
), by = customer_id]

# Identify single-week customers
single_week_customers <- customer_active_weeks[active_weeks == 1]

cat("\n=== Single Purchase Week Analysis ===\n")
cat("Total unique customers in panel:", length(unique(customer_panel$customer_id)), "\n")# 49737
cat("Customers with only one week of non-zero orders:", nrow(single_week_customers), "\n")# 20233
cat("Percentage:", round(nrow(single_week_customers) / length(unique(customer_panel$customer_id)) * 100, 2), "%\n")# 40.68%

# Distribution of orders in that single week
cat("\nDistribution of orders in their single active week:\n")
print(summary(single_week_customers$total_orders))
#   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#  1.000   1.000   2.000   2.359   3.000  64.000 

# Compare with multi-week customers
multi_week_customers <- customer_active_weeks[active_weeks > 1]
cat("\n=== Comparison with Multi-Week Customers ===\n")
cat("Multi-week customers:", nrow(multi_week_customers), "\n")# 29504
cat("Average active weeks (multi-week customers):", round(mean(multi_week_customers$active_weeks), 2), "\n")# 7.77
cat("Average total orders (single-week):", round(mean(single_week_customers$total_orders), 2), "\n")# 2.36
cat("Average total orders (multi-week):", round(mean(multi_week_customers$total_orders), 2), "\n")# 17.98

# 2.7 Filter customers based on purchase patterns
cat("\n=== Filtering Customers ===\n")
original_customers <- length(unique(customer_panel$customer_id))
# Identify customers to remove based on criterion 1: only one week of purchases
customers_to_remove_1 <- single_week_customers$customer_id

# Identify customers to remove based on criterion 2: more than 14 orders in any single week
customers_with_high_weekly_orders <- customer_panel[orders > 14, unique(customer_id)]
cat("Customers with >14 orders in any week:", length(customers_with_high_weekly_orders), "\n")#583

# Combine both removal criteria (union)
customers_to_remove <- unique(c(customers_to_remove_1, customers_with_high_weekly_orders))

# Filter the customer_panel
customer_panel <- customer_panel[!(customer_id %in% customers_to_remove)]

# Calculate remaining customers
remaining_customers <- length(unique(customer_panel$customer_id))
cat("\n=== After Filtering ===\n")
cat("Remaining customers:", remaining_customers, "\n")# 29054
cat("Share of customers remaining:", round(remaining_customers / original_customers * 100, 2), "%\n")# 58.42%
cat("Customers removed:", original_customers - remaining_customers, "\n")# 20683
cat("Share of customers removed:", round((original_customers - remaining_customers) / original_customers * 100, 2), "%\n")# 41.58%

# 2.8 Don't consider the first week of purchasing
customer_panel <- customer_panel[week_id > first_week]
customer_panel[, first_week := NULL]

############################################################################
# Step 3: Store-Product Timeline (using complete order database)
############################################################################

cat("Creating store-product timeline...\n")

# 3.1 Load the complete order database
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
# - All weeks when it was sold
product_lifecycle <- complete_orders[, list(
  first_week = min(week_id),
  last_week = max(week_id)
), by = list(dept_id, product_id)]

# Count total products per store (for reference)
store_product_counts <- product_lifecycle[, list(
  total_products = .N,
  avg_product_lifetime = mean(last_week - first_week + 1)
), by = dept_id]

cat("\nStore product statistics:\n")
print(store_product_counts)

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
cat("- Number of unique stores:", length(unique_stores), "\n")

cat("Loading store-week availability data...\n")
dept_week_data <- fread("data1031/dept_result_week_order.csv", 
                        encoding = "UTF-8",
                        select = c("dept_id", "monday_date"))

dept_week_data$monday_date <- as.Date(dept_week_data$monday_date)
dept_week_data[, week_id := as.integer(floor(as.numeric(monday_date - START_DATE) / 7)) + 1]

store_week_combinations <- unique(dept_week_data[, list(dept_id, week_id)])
cat("- Total store-week combinations:", nrow(store_week_combinations), "\n")

store_week_combinations <- store_week_combinations[
  store_week_combinations[, 
                          .(first_week = min(week_id), 
                            last_week = max(week_id)), 
                          by = dept_id
  ], 
  on = "dept_id"
][week_id >= first_week + 4 & week_id <= last_week - 4, 
  .(dept_id, week_id)  # Select only original columns
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

# 3.7 Calculate cumulative and active product counts
cat("Calculating cumulative product statistics...\n")

# Sort by store and week
setorder(store_panel, dept_id, week_id)

# 3.8 Create lagged values for analysis
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

# 3.9 Save product lifecycle information for later use
cat("Saving product lifecycle data...\n")

# Save detailed product lifecycle
fwrite(product_lifecycle, "outputs/data/product_lifecycle_detailed.csv")

# 3.10 Create summary statistics
cat("\n=== Store-Product Timeline Summary ===\n")
cat("Total weeks analyzed:", TOTAL_WEEKS, "\n")
cat("Total stores analyzed:", length(unique_stores), "\n")

# Overall statistics
overall_stats <- store_panel[, list(
  total_new_products = sum(new_products),
  total_removed = sum(removed),
  avg_new_per_week = mean(new_products),
  avg_removed_per_week = mean(removed),
  weeks_with_new = sum(new_products > 0),
  weeks_with_removed = sum(removed > 0),
  weeks_with_changes = sum(new_products > 0 | removed > 0)
)]

cat("\nOverall statistics:\n")
cat("- Total new products introduced:", overall_stats$total_new_products, "\n")
cat("- Total products removed:", overall_stats$total_removed, "\n")
cat("- Average new products per week:", round(overall_stats$avg_new_per_week, 2), "\n")

# Store-level statistics
store_level_stats <- store_panel[, list(
  total_new = sum(new_products),
  total_removed = sum(removed),
  max_new_in_week = max(new_products),
  max_removed_in_week = max(removed)
), by = dept_id]

cat("\nStore-level statistics (first 5 stores):\n")
print(store_level_stats[1:min(5, nrow(store_level_stats))])

# 3.12 Save the store panel
cat("\nSaving store-week panel...\n")
fwrite(store_panel, "outputs/data/store_week_panel_complete.csv")
cat("Store-product timeline creation complete!\n")

############################################################################
# Step 4: Merge Panels and Add Product Details
############################################################################

cat("Merging customer and store panels...\n")

# 4.1 Merge customer panel with store information
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
# Step 6: Run Regression Models (Simplified)
############################################################################

cat("Running regression models...\n")
# Check for data issues before running regressions
cat("\nChecking data quality before regressions...\n")

# Check 1: Ensure key variables have variation
check_variation <- function(data, var_name) {
  if (var_name %in% names(data)) {
    unique_vals <- unique(data[[var_name]])
    cat(sprintf("%s: %d unique values (min=%s, max=%s)\n", 
                var_name, length(unique_vals), 
                min(unique_vals, na.rm = TRUE), max(unique_vals, na.rm = TRUE)))
  }
}

cat("\nAnalysis panel variable variation:\n")
check_variation(analysis_panel, "orders")
check_variation(analysis_panel, "new_products")
check_variation(analysis_panel, "new_products_lag1")
check_variation(analysis_panel, "removed")
check_variation(analysis_panel, "weeks_sleep")

cat("\nProduct panel variable variation:\n")
check_variation(product_panel, "purchases_existing")
check_variation(product_panel, "bought_existing")

# Check 3: Ensure sufficient observations for fixed effects
cat("\nChecking fixed effects group sizes:\n")

check_fe_groups <- function(data, fe_var) {
  group_counts <- data[, .N, by = get(fe_var)]
  cat(sprintf("%s: %d unique groups, min obs per group: %d, max obs per group: %d\n",
              fe_var, nrow(group_counts), min(group_counts$N), max(group_counts$N)))
}

cat("\nAnalysis panel FE groups:\n")
check_fe_groups(analysis_panel, "customer_id")
check_fe_groups(analysis_panel, "week_id")
check_fe_groups(analysis_panel, "dept_id")

model_descriptions <- list(
  "Model_A" = "orders ~ new_products + new_products_lag1 + removed + customer_id + week_id + dept_id",
  
  "Model_B_threshold_4" = "orders ~ new_products + removed + sleep_gt_4 + new_products:sleep_gt_4 + removed:sleep_gt_4 + customer_id + week_id + dept_id",
  "Model_B_threshold_8" = "orders ~ new_products + removed + sleep_gt_8 + new_products:sleep_gt_8 + removed:sleep_gt_8 + customer_id + week_id + dept_id",
  "Model_B_threshold_12" = "orders ~ new_products + removed + sleep_gt_12 + new_products:sleep_gt_12 + removed:sleep_gt_12 + customer_id + week_id + dept_id",
  
  "Model_B_continuous" = "orders ~ new_products + removed + weeks_sleep + new_products:weeks_sleep + removed:weeks_sleep + customer_id + week_id + dept_id",
  
  "Model_B_active" = "orders ~ new_products + new_products_lag1 + removed + customer_id + week_id + dept_id (only weeks_sleep <= 4)",
  "Model_B_dormant" = "orders ~ new_products + new_products_lag1 + removed + customer_id + week_id + dept_id (only weeks_sleep > 4)",
  
  "Model_C" = "purchases_existing ~ new_products + new_products_lag1 + removed + customer_id + week_id + dept_id",
  
  "Model_D" = "bought_existing ~ new_products + new_products_lag1 + removed + customer_id + week_id + dept_id",
  
  "Model_A_distributed" = "orders ~ new_products_lag0 + new_products_lag1 + new_products_lag2 + new_products_lag3 + removed_lag0 + removed_lag1 + removed_lag2 + removed_lag3 + customer_id + week_id + dept_id",
  
  "Model_C_distributed" = "purchases_existing ~ new_products_lag0 + new_products_lag1 + new_products_lag2 + new_products_lag3 + removed_lag0 + removed_lag1 + removed_lag2 + removed_lag3 + customer_id + week_id + dept_id"
)

# Save model descriptions
model_summary <- data.table(
  model_name = names(model_descriptions),
  formula = unlist(model_descriptions),
  data_source = c(rep("analysis_panel", 8), "product_panel", "product_panel", 
                  "analysis_panel", "product_panel"),
  description = c(
    "Basic model: effect of new/removed products",
    "Interaction with sleep > 4 weeks",
    "Interaction with sleep > 8 weeks",
    "Interaction with sleep > 12 weeks",
    "Continuous interaction with sleep weeks",
    "Active customers only (sleep <= 4)",
    "Dormant customers only (sleep > 4)",
    "Effect on purchases of existing products",
    "Effect on buying any existing product",
    "Distributed lag model for orders",
    "Distributed lag for existing product purchases"
  )
)

fwrite(model_summary, "outputs/results/model_descriptions.csv")



# Create a list to store regression results
regression_results <- list()

# Model A: Basic model
cat("\nRunning Model A...\n")
model_a <- felm(orders ~ new_products + new_products_lag1 + removed | customer_id + week_id + dept_id,
                data = analysis_panel)
regression_results[["Model_A"]] <- model_a

# Model B with sleep thresholds
for (thr in SLEEP_THRESHOLDS) {
  indicator <- paste0("sleep_gt_", thr)
  model_name <- paste0("Model_B_threshold_", thr)
  
  cat(sprintf("\nRunning %s (sleep > %d weeks)...\n", model_name, thr))
  
  formula_str <- sprintf("orders ~ new_products + removed + %s + new_products:%s + removed:%s | customer_id + week_id + dept_id",
                         indicator, indicator, indicator)
  
  regression_results[[model_name]] <- felm(as.formula(formula_str), data = analysis_panel)
}

# Model B continuous
cat("\nRunning Model_B_continuous...\n")
regression_results[["Model_B_continuous"]] <- felm(
  orders ~ new_products + removed + weeks_sleep + new_products:weeks_sleep + removed:weeks_sleep | 
    customer_id + week_id + dept_id,
  data = analysis_panel
)

# Model B active and dormant subsets
cat("\nRunning Model_B_active (sleep <= 4)...\n")
regression_results[["Model_B_active"]] <- felm(
  orders ~ new_products + new_products_lag1 + removed | customer_id + week_id + dept_id,
  data = analysis_panel[weeks_sleep <= 4]
)

cat("\nRunning Model_B_dormant (sleep > 4)...\n")
regression_results[["Model_B_dormant"]] <- felm(
  orders ~ new_products + new_products_lag1 + removed | customer_id + week_id + dept_id,
  data = analysis_panel[weeks_sleep > 4]
)

# Model C: Effect on purchases of existing products
cat("\nRunning Model_C...\n")
regression_results[["Model_C"]] <- felm(
  purchases_existing ~ new_products + new_products_lag1 + removed | customer_id + week_id + dept_id,
  data = product_panel
)

# Model D: Effect on buying any existing product
cat("\nRunning Model_D...\n")
regression_results[["Model_D"]] <- felm(
  bought_existing ~ new_products + new_products_lag1 + removed | customer_id + week_id + dept_id,
  data = product_panel
)

# Model A with distributed lags
cat("\nRunning Model_A_distributed...\n")
regression_results[["Model_A_distributed"]] <- felm(
  orders ~ new_products_lag0 + new_products_lag1 + new_products_lag2 + new_products_lag3 + 
    removed_lag0 + removed_lag1 + removed_lag2 + removed_lag3 | 
    customer_id + week_id + dept_id,
  data = analysis_panel
)

# Model C with distributed lags
cat("\nRunning Model_C_distributed...\n")
regression_results[["Model_C_distributed"]] <- felm(
  purchases_existing ~ new_products_lag0 + new_products_lag1 + new_products_lag2 + new_products_lag3 + 
    removed_lag0 + removed_lag1 + removed_lag2 + removed_lag3 | 
    customer_id + week_id + dept_id,
  data = product_panel
)

# Create summary tables
cat("\nCreating regression summary tables...\n")

# Function to extract regression results
extract_results <- function(model, model_name) {
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
    p_value = coefs[, "Pr(>|t|)"]
  )
  
  # Add model info
  coef_df[, model := model_name]
  coef_df[, n_obs := summ$N]
  coef_df[, r_squared <- summ$r.squared]
  coef_df[, adj_r_squared <- summ$adj.r.squared]
  
  return(coef_df)
}

# Extract all results
all_results <- rbindlist(
  lapply(names(regression_results), function(model_name) {
    extract_results(regression_results[[model_name]], model_name)
  }),
  fill = TRUE
)

# Save results
fwrite(all_results, "outputs/results/regression_results_detailed.csv")

# Create a simplified summary table
cat("\nCreating simplified coefficient summary...\n")
key_vars <- c("new_products", "new_products_lag1", "removed", 
              "new_products:sleep_gt_4", "new_products:sleep_gt_8", "new_products:sleep_gt_12",
              "new_products:weeks_sleep")

coef_summary <- all_results[term %in% key_vars]
fwrite(coef_summary, "outputs/results/regression_coefficients_summary.csv")

# Print key results
cat("\n=== KEY REGRESSION RESULTS ===\n")
cat("\nModel A (Basic model):\n")
print(all_results[model == "Model_A" & term %in% c("new_products", "new_products_lag1", "removed"),
                  .(term, estimate = round(estimate, 4), p_value = round(p_value, 4))])

cat("\nModel B - Active vs Dormant:\n")
print(data.table(
  model = c("Active (sleep <= 4)", "Dormant (sleep > 4)"),
  new_products_coef = c(
    all_results[model == "Model_B_active" & term == "new_products", round(estimate, 4)],
    all_results[model == "Model_B_dormant" & term == "new_products", round(estimate, 4)]
  ),
  n_obs = c(
    all_results[model == "Model_B_active", unique(n_obs)],
    all_results[model == "Model_B_dormant", unique(n_obs)]
  )
))

cat("\nModel C (Purchases of existing products):\n")
print(all_results[model == "Model_C" & term %in% c("new_products", "new_products_lag1", "removed"),
                  .(term, estimate = round(estimate, 4), p_value = round(p_value, 4))])




############################################################################
# Step 7: Create Summary Statistics
############################################################################

cat("Calculating summary statistics...\n")

# Basic statistics (using filtered data)
avg_weekly_orders <- mean(customer_panel$orders)
total_customers <- length(unique(customer_panel$customer_id))
total_stores <- length(unique(customer_panel$dept_id))
total_weeks_in_analysis <- length(unique(customer_panel$week_id))

# Customer sleep patterns
sleep_summary <- customer_panel[, list(
  avg_sleep_weeks = mean(weeks_sleep),
  max_sleep_weeks = max(weeks_sleep),
  percent_active = mean(weeks_sleep == 0) * 100,
  percent_dormant_4 = mean(weeks_sleep > 4) * 100,
  percent_dormant_8 = mean(weeks_sleep > 8) * 100
), by = customer_id]

# Store product changes
store_changes <- store_panel[, list(
  total_new_products = sum(new_products),
  total_removed = sum(removed),
  avg_new_per_week = mean(new_products[new_products > 0]),
  weeks_with_changes = sum(new_products > 0 | removed > 0)
), by = dept_id]

# Save summaries
summary_stats <- list(
  overall = data.table(
    metric = c("Average weekly orders", "Total customers", "Total stores", 
               "Weeks analyzed", "Start week", "End week", "Start date", "End date"),
    value = c(round(avg_weekly_orders, 3), total_customers, total_stores,
              total_weeks_in_analysis, "5", "79",
              format(START_DATE + 7*4, "%Y-%m-%d"),  # Week 5 start date
              format(START_DATE + 7*78, "%Y-%m-%d"))  # Week 79 start date
  ),
  customer_sleep = sleep_summary[, list(
    metric = c("Average sleep weeks", "Max sleep weeks", 
               "Active customers (%)", "Dormant >4w (%)", "Dormant >8w (%)"),
    value = c(round(mean(avg_sleep_weeks), 2), max(max_sleep_weeks),
              round(mean(percent_active), 1), round(mean(percent_dormant_4), 1),
              round(mean(percent_dormant_8), 1))
  )],
  store_changes = store_changes[, list(
    metric = c("Average overall new products", "Average overall removals", 
               "Weeks with changes (%)", "Max new product in store-week"),
    value = c(round(mean(total_new_products), 1), round(mean(total_removed), 1),
              round(mean(weeks_with_changes) / total_weeks_in_analysis * 100, 1),
              max(store_panel$new_products))
  )]
)

# Write summary file
summary_text <- paste(
  "# Customer Behavior Analysis Summary\n",
  paste0("Generated: ", Sys.Date(), "\n\n"),
  "## Analysis Period\n",
  paste("- Weeks analyzed:", total_weeks_in_analysis, "weeks (week_id 5 to 79)\n"),
  paste("- Date range:", format(START_DATE + 7*4, "%b %d, %Y"), "to", 
        format(START_DATE + 7*78, "%b %d, %Y"), "\n\n"),
  "## Overall Statistics\n",
  paste("-", summary_stats$overall$metric, ":", summary_stats$overall$value, collapse = "\n"),
  "\n\n## Customer Activity Patterns\n",
  paste("-", summary_stats$customer_sleep$metric, ":", summary_stats$customer_sleep$value, collapse = "\n"),
  "\n\n## Store Product Changes\n",
  paste("-", summary_stats$store_changes$metric, ":", summary_stats$store_changes$value, collapse = "\n"),
  "\n\n## Analysis Notes\n",
  "1. Analysis focuses on customers' primary stores only",
  "2. Excluded product IDs:", paste(EXCLUDED_PRODUCT_IDS, collapse = ", "),
  "3. Recent products defined as introduced within last", RECENT_WINDOW, "weeks",
  "4. Sleep thresholds analyzed at", paste(SLEEP_THRESHOLDS, collapse = ", "), "weeks",
  "5. Analysis restricted to week_id 5 to 79 (excluding first 4 and last weeks)",
  sep = ""
)

writeLines(summary_text, "outputs/results/analysis_summary.txt")

############################################################################
# Step 8: Create Sample Visualizations (Basic R plots)
############################################################################

cat("Creating visualizations...\n")

# 8.1 Distribution of weekly orders
png("outputs/plots/weekly_orders_distribution.png", width = 800, height = 600)
hist(customer_panel$orders, 
     main = "Distribution of Weekly Orders per Customer\n(Weeks 5-79)",
     xlab = "Number of Orders",
     ylab = "Frequency",
     col = "lightblue",
     breaks = 30)
dev.off()

# 8.2 Customer sleep weeks distribution
png("outputs/plots/sleep_weeks_distribution.png", width = 800, height = 600)
sleep_data <- customer_panel[, max(weeks_sleep), by = customer_id]$V1
hist(sleep_data[sleep_data <= 20],  # Cap at 20 for readability
     main = "Maximum Consecutive Weeks Without Ordering\n(Weeks 5-79)",
     xlab = "Weeks Without Ordering",
     ylab = "Number of Customers",
     col = "lightcoral",
     breaks = 20)
dev.off()

# 8.3 Store product introductions over time
png("outputs/plots/product_introductions.png", width = 1000, height = 600)
store_sample <- store_panel[dept_id %in% sample(unique(dept_id), 5)]  # Sample 5 stores
plot(1, type = "n", 
     xlim = c(5, 79), ylim = c(0, max(store_sample$new_products) + 1),
     main = "New Product Introductions Over Time (Sample Stores)\n(Weeks 5-79)",
     xlab = "Week", ylab = "New Products Introduced")

colors <- rainbow(length(unique(store_sample$dept_id)))
store_ids <- unique(store_sample$dept_id)

for (i in seq_along(store_ids)) {
  store_data <- store_sample[dept_id == store_ids[i]]
  lines(store_data$week_id, store_data$new_products, 
        col = colors[i], lwd = 2, type = "b")
}

legend("topright", legend = paste("Store", store_ids), 
       col = colors, lwd = 2, bty = "n")
dev.off()


############################################################################
# Step 9: Check Multicollinearity for Key Variables
############################################################################

cat("\n\n=== CHECKING MULTICOLLINEARITY ===\n")
library("car")

cat("\n1. Checking multicollinearity between new_products and removed...\n")

simple_model <- lm(orders ~ new_products + removed, 
                   data = analysis_panel)

vif_results <- vif(simple_model)
cat("\nVariance Inflation Factors (VIF):\n")
print(vif_results)# 1.003069

cat("\nVIF Interpretation:\n")
cat("- VIF < 5: Moderate correlation (usually acceptable)\n")
cat("- VIF 5-10: High correlation (potential concern)\n") 
cat("- VIF > 10: Very high correlation (definite multicollinearity problem)\n")

cat("\n2. Correlation coefficient between new_products and removed:\n")
correlation <- cor(store_panel$new_products, 
                   store_panel$removed, 
                   use = "complete.obs")
cat(sprintf("Correlation: %.4f\n", correlation))# 0.0853

cat("\nCorrelation thresholds:\n")
cat("- |cor| < 0.3: Weak correlation\n")
cat("- 0.3 ≤ |cor| < 0.7: Moderate correlation\n")
cat("- |cor| ≥ 0.7: Strong correlation (potential multicollinearity)\n")