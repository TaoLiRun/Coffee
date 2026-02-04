#!/usr/bin/env Rscript
# Script 4: Block Regression Analysis
#
# Purpose: Analyze how customer behavior evolves across multiple active/dormant periods
#          and how this evolution differs between push=0 and push=1 groups.
#
# Research Questions:
# 1. How do active period metrics (orders, spend, frequency) evolve across periods?
# 2. How do dormant period metrics (length, push effectiveness) evolve across periods?
# 3. Does the evolution differ between push=0 and push=1 groups?
# 4. What predicts wake-up in each dormant period?
# 5. How does push sensitivity change across periods?

library(data.table)
library(lfe)
library(ggplot2)
library(sandwich)
library(lmtest)

# Set working directory to script location
script_dir <- dirname(sys.frame(1)$ofile)
setwd(script_dir)

# Load data
cat("========================================\n")
cat("Loading Data\n")
cat("========================================\n")

# Load active period metrics
active_data <- fread("../../outputs/tables/active_period_metrics.csv")
cat(paste0("Loaded ", nrow(active_data), " active period observations\n"))

# Load dormant period metrics
dormant_data <- fread("../../outputs/tables/dormant_period_metrics.csv")
cat(paste0("Loaded ", nrow(dormant_data), " dormant period observations\n"))

# Get push_group for merging (from first period of each customer)
push_groups <- unique(active_data[, .(member_id, push_group)])

# Merge push_group into dormant_data
dormant_data <- merge(dormant_data, push_groups, by="member_id", all.x=TRUE)

#============================================================
# Analysis 1: Evolution of Active Period Metrics
#============================================================

cat("\n========================================\n")
cat("Analysis 1: Evolution of Active Period Metrics\n")
cat("========================================\n")

# Hypothesis 1: Engagement declines across periods (fatigue)
# Hypothesis 2: push=0 shows slower decline than push=1 (more loyal)

# Model: metric ~ period_number * push_group + member_FE
metrics_to_analyze <- c("n_orders", "order_freq", "avg_order_value", "total_spend", "weeks_active")

active_results <- list()

for (metric in metrics_to_analyze) {
  cat(paste0("\n--- Analyzing: ", metric, " ---\n"))

  # Prepare data
  model_data <- active_data[!is.na(get(metric))]
  model_data$push_group <- as.factor(model_data$push_group)
  model_data$active_period_num <- as.factor(model_data$active_period_num)

  # Simple OLS: metric ~ push_group * active_period_num
  formula <- as.formula(paste0(metric, " ~ push_group * factor(active_period_num)"))

  tryCatch({
    fit <- lm(formula, data=model_data)
    coeftest_fit <- coeftest(fit, vcov = vcovHC(fit, type="HC1"))

    cat("\nCoefficient estimates:\n")
    print(coeftest_fit)

    active_results[[metric]] <- list(
      model = fit,
      coeftest = coeftest_fit,
      n = nrow(model_data)
    )
  }, error = function(e) {
    cat(paste0("Error fitting model for ", metric, ": ", e$message, "\n"))
  })
}

# Save active period results
saveRDS(active_results, file="../../outputs/tables/active_regression_results.rds")
cat("\nSaved active period regression results\n")

#============================================================
# Analysis 2: Evolution of Dormant Period Metrics
#============================================================

cat("\n========================================\n")
cat("Analysis 2: Evolution of Dormant Period Metrics\n")
cat("========================================\n")

# Hypothesis 1: Dormant length increases across periods (harder to wake up)
# Hypothesis 2: Wake-up rate declines across periods (fatigue)
# Hypothesis 3: Push effectiveness changes across periods
# Hypothesis 4: push=0 maintains higher wake-up rates across periods

# Model 1: Wake-up probability ~ period_number * push_group
cat("\n--- Model 1: Wake-up Probability ---\n")

wakeup_model_data <- dormant_data[!is.na(wakeup)]
wakeup_model_data$push_group <- as.factor(wakeup_model_data$push_group)
wakeup_model_data$dormant_period_num <- as.factor(wakeup_model_data$dormant_period_num)

wakeup_formula <- wakeup ~ push_group * factor(dormant_period_num)
wakeup_fit <- lm(wakeup_formula, data=wakeup_model_data)
wakeup_coeftest <- coeftest(wakeup_fit, vcov = vcovHC(wakeup_fit, type="HC1"))

cat("\nWakeup probability model:\n")
print(wakeup_coeftest)

# Model 2: Dormant length (conditional on wakeup) ~ period_number * push_group
cat("\n--- Model 2: Dormant Length (Conditional on Wakeup) ---\n")

length_model_data <- dormant_data[wakeup == 1 & !is.na(days_to_wakeup)]
length_model_data$push_group <- as.factor(length_model_data$push_group)
length_model_data$dormant_period_num <- as.factor(length_model_data$dormant_period_num)

length_formula <- days_to_wakeup ~ push_group * factor(dormant_period_num)
length_fit <- lm(length_formula, data=length_model_data)
length_coeftest <- coeftest(length_fit, vcov = vcovHC(length_fit, type="HC1"))

cat("\nDormant length model:\n")
print(length_coeftest)

# Model 3: Push intensity effect ~ period_number * push_group
cat("\n--- Model 3: Push Intensity Effect ---\n")

intensity_model_data <- dormant_data[!is.na(pushes_per_day) & wakeup == 1]
intensity_model_data$push_group <- as.factor(intensity_model_data$push_group)
intensity_model_data$dormant_period_num <- as.factor(intensity_model_data$dormant_period_num)

intensity_formula <- days_to_wakeup ~ pushes_per_day * push_group * factor(dormant_period_num)
intensity_fit <- lm(intensity_formula, data=intensity_model_data)
intensity_coeftest <- coeftest(intensity_fit, vcov = vcovHC(intensity_fit, type="HC1"))

cat("\nPush intensity model:\n")
print(intensity_coeftest)

# Save dormant period results
dormant_results <- list(
  wakeup = list(model=wakeup_fit, coeftest=wakeup_coeftest),
  length = list(model=length_fit, coeftest=length_coeftest),
  intensity = list(model=intensity_fit, coeftest=intensity_coeftest)
)
saveRDS(dormant_results, file="../../outputs/tables/dormant_regression_results.rds")
cat("\nSaved dormant period regression results\n")

#============================================================
# Analysis 3: Last Push Characteristics Effect on Wake-up
#============================================================

cat("\n========================================\n")
cat("Analysis 3: Last Push Characteristics\n")
cat("========================================\n")

# Hypothesis: Last push before wake-up has stronger effect for push=0
# Metrics: days_from_last_push_to_wakeup, last_push_discount, last_push_has_coupon

lastpush_model_data <- dormant_data[wakeup == 1 & !is.na(days_from_last_push_to_wakeup)]
lastpush_model_data$push_group <- as.factor(lastpush_model_data$push_group)

# Model: days_from_last_push_to_wakeup ~ push_group + last_push_discount + last_push_has_coupon
lastpush_formula <- days_from_last_push_to_wakeup ~ push_group + last_push_discount + last_push_has_coupon
lastpush_fit <- lm(lastpush_formula, data=lastpush_model_data)
lastpush_coeftest <- coeftest(lastpush_fit, vcov = vcovHC(lastpush_fit, type="HC1"))

cat("\nLast push characteristics model:\n")
print(lastpush_coeftest)

# Save last push results
saveRDS(lastpush_fit, file="../../outputs/tables/lastpush_regression_result.rds")

#============================================================
# Analysis 4: Customer-Level Fixed Effects (within-customer evolution)
#============================================================

cat("\n========================================\n")
cat("Analysis 4: Within-Customer Evolution (Fixed Effects)\n")
cat("========================================\n")

# Reshape to long format for FE estimation
active_long <- melt(active_data,
                    id.vars=c("member_id", "active_period_num", "push_group"),
                    measure.vars=metrics_to_analyze,
                    variable.name="metric",
                    value.name="value")

active_long$period <- active_long$active_period_num

# FE model: value ~ period + metric, with member FE
# This estimates how each metric changes across periods, holding customer constant

cat("\n--- Active Period FE Model ---\n")

# Filter to first 5 periods for stability
active_fe_data <- active_long[active_period_num <= 5 & !is.na(value)]
active_fe_data$period <- as.factor(active_fe_data$period)
active_fe_data$metric <- as.factor(active_fe_data$metric)

# Use felm for high-dimensional FE
active_fe_formula <- value ~ period:metric | member_id + metric

tryCatch({
  active_fe_fit <- felm(active_fe_formula, data=active_fe_data)
  summary(active_fe_fit)

  # Save FE results
  saveRDS(active_fe_fit, file="../../outputs/tables/active_fe_results.rds")
  cat("\nSaved active period FE results\n")
}, error = function(e) {
  cat(paste0("Error fitting FE model: ", e$message, "\n"))
})

# Dormant period FE model
dormant_fe_data <- dormant_data[dormant_period_num <= 5 & wakeup == 1]
dormant_fe_data$period <- as.factor(dormant_fe_data$dormant_period_num)

cat("\n--- Dormant Period FE Model ---\n")

# FE model: days_to_wakeup ~ period, with member FE
dormant_fe_formula <- days_to_wakeup ~ period | member_id

tryCatch({
  dormant_fe_fit <- felm(dormant_fe_formula, data=dormant_fe_data)
  summary(dormant_fe_fit)

  # Save FE results
  saveRDS(dormant_fe_fit, file="../../outputs/tables/dormant_fe_results.rds")
  cat("\nSaved dormant period FE results\n")
}, error = function(e) {
  cat(paste0("Error fitting dormant FE model: ", e$message, "\n"))
})

#============================================================
# Analysis 5: Transition Analysis (Period → Next Period)
#============================================================

cat("\n========================================\n")
cat("Analysis 5: Transition Analysis\n")
cat("========================================\n")

# Does performance in period t predict behavior in period t+1?
# Create lagged variables

active_with_lag <- active_data[order(member_id, active_period_num)]
active_with_lag[, lag_n_orders := shift(n_orders), by=member_id]
active_with_lag[, lag_total_spend := shift(total_spend), by=member_id]

dormant_with_lag <- dormant_data[order(member_id, dormant_period_num)]
dormant_with_lag[, lag_wakeup := shift(wakeup), by=member_id]
dormant_with_lag[, lag_days_to_wakeup := shift(days_to_wakeup), by=member_id]

# Model: Does previous active period predict next dormant period?
# Merge active t with dormant t
transition_data <- merge(
  active_with_lag[, .(member_id, active_period_num, n_orders, total_spend)],
  dormant_with_lag[, .(member_id, dormant_period_num, wakeup, days_to_wakeup)],
  by.x=c("member_id", "active_period_num"),
  by.y=c("member_id", "dormant_period_num"),
  all.x=TRUE
)

# Model: wakeup ~ n_orders + total_spend
transition_formula <- wakeup ~ n_orders + total_spend
transition_fit <- lm(transition_formula, data=transition_data[!is.na(wakeup)])
transition_coeftest <- coeftest(transition_fit, vcov = vcovHC(transition_fit, type="HC1"))

cat("\nTransition model (active → dormant):\n")
print(transition_coeftest)

# Save transition results
saveRDS(transition_fit, file="../../outputs/tables/transition_regression_result.rds")

#============================================================
# Create Visualizations
#============================================================

cat("\n========================================\n")
cat("Creating Visualizations\n")
cat("========================================\n")

output_dir <- "../../outputs/figures/"

# Plot 1: Active period evolution by group
png(paste0(output_dir, "active_period_evolution.png"), width=1200, height=800, res=300)

plot_data <- active_data[, .(
  n_orders = mean(n_orders, na.rm=TRUE),
  order_freq = mean(order_freq, na.rm=TRUE),
  total_spend = mean(total_spend, na.rm=TRUE),
  push_group
), by=.(active_period_num, push_group)]

par(mfrow=c(2, 2))

for (metric in c("n_orders", "order_freq", "total_spend")) {
  plot(plot_data$active_period_num, plot_data[[metric]],
       type="b", pch=19,
       col=ifelse(plot_data$push_group==0, "blue", "red"),
       xlab="Active Period Number",
       ylab=metric,
       main=paste("Evolution of", metric),
       lty=1)
  legend("topright", legend=c("push=0", "push=1"),
         col=c("blue", "red"), lty=1, pch=19)
}

dev.off()
cat(paste0("Saved: ", output_dir, "active_period_evolution.png\n"))

# Plot 2: Dormant period evolution by group
png(paste0(output_dir, "dormant_period_evolution.png"), width=1200, height=800, res=300)

dormant_plot_data <- dormant_data[, .(
  wakeup_rate = mean(wakeup, na.rm=TRUE),
  days_to_wakeup = mean(days_to_wakeup, na.rm=TRUE),
  pushes_per_day = mean(pushes_per_day, na.rm=TRUE),
  push_group
), by=.(dormant_period_num, push_group)]

par(mfrow=c(2, 2))

plot(dormant_plot_data$dormant_period_num, dormant_plot_data$wakeup_rate,
     type="b", pch=19,
     col=ifelse(dormant_plot_data$push_group==0, "blue", "red"),
     xlab="Dormant Period Number",
     ylab="Wake-up Rate",
     main="Evolution of Wake-up Rate",
     lty=1)
legend("topright", legend=c("push=0", "push=1"),
       col=c("blue", "red"), lty=1, pch=19)

plot(dormant_plot_data$dormant_period_num, dormant_plot_data$days_to_wakeup,
     type="b", pch=19,
     col=ifelse(dormant_plot_data$push_group==0, "blue", "red"),
     xlab="Dormant Period Number",
     ylab="Days to Wake-up",
     main="Evolution of Days to Wake-up",
     lty=1)

plot(dormant_plot_data$dormant_period_num, dormant_plot_data$pushes_per_day,
     type="b", pch=19,
     col=ifelse(dormant_plot_data$push_group==0, "blue", "red"),
     xlab="Dormant Period Number",
     ylab="Pushes Per Day",
     main="Evolution of Push Intensity",
     lty=1)

dev.off()
cat(paste0("Saved: ", output_dir, "dormant_period_evolution.png\n"))

#============================================================
# Save Summary Table
#============================================================

cat("\n========================================\n")
cat("Creating Summary Table\n")
cat("========================================\n")

# Create coefficient comparison table
summary_table <- data.frame(
  Analysis = c("Active: Orders ~ Period", "Active: Frequency ~ Period",
               "Dormant: Wakeup ~ Period", "Dormant: Length ~ Period",
               "Push Intensity Effect", "Last Push Effect",
               "Active FE (Within)", "Dormant FE (Within)",
               "Transition Effect"),
  N = c(
    active_results$n_orders$n,
    active_results$order_freq$n,
    nrow(wakeup_model_data),
    nrow(length_model_data),
    nrow(intensity_model_data),
    nrow(lastpush_model_data),
    nrow(active_fe_data),
    nrow(dormant_fe_data),
    nrow(transition_data)
  ),
  Status = c("Completed", "Completed", "Completed", "Completed",
              "Completed", "Completed", "Completed", "Completed",
              "Completed")
)

write.csv(summary_table, "../../outputs/tables/block_regression_summary.csv", row.names=FALSE)
cat("\nSaved summary table\n")

cat("\n========================================\n")
cat("Block Regression Analysis Complete!\n")
cat("========================================\n")
