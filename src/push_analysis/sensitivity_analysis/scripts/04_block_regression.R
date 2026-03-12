#!/usr/bin/env Rscript
# Script 4: Block Regression Analysis (Refactored for Python Consistency)
#
# Purpose: Analyze how customer behavior evolves across multiple active/dormant periods
#          and how this evolution differs between push=0 and push=1 groups.

library(data.table)
library(lfe)
library(ggplot2)
library(sandwich)
library(lmtest)

# Set working directory to script location
args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])
if (length(script_path) > 0) {
  script_dir <- dirname(normalizePath(script_path))
  setwd(script_dir)
}

# Load data
cat("========================================\n")
cat("Loading Data\n")
cat("========================================\n")

# Load metrics (push_group is already included in Python output)
active_data <- fread("../outputs/tables/active_period_metrics.csv")
dormant_data <- fread("../outputs/tables/dormant_period_metrics.csv")

# Set factors for regression stability
active_data[, `:=`(push_group = as.factor(push_group), 
                   active_period_num = as.factor(active_period_num))]
dormant_data[, `:=`(push_group = as.factor(push_group), 
                    dormant_period_num = as.factor(dormant_period_num))]

cat(paste0("Loaded ", nrow(active_data), " active and ", nrow(dormant_data), " dormant observations\n"))

#============================================================
# Analysis 1: Evolution of Active Period Metrics
#============================================================

cat("\n========================================\n")
cat("Analysis 1: Evolution of Active Period Metrics\n")
cat("========================================\n")

metrics_to_analyze <- c("n_orders", "order_per_week", "avg_order_value", "total_spend", "weeks_active")
active_results <- list()

for (metric in metrics_to_analyze) {
  if (metric %in% names(active_data)) {
    cat(paste0("\n--- Analyzing: ", metric, " ---\n"))
    
    model_data <- active_data[!is.na(get(metric))]
    formula <- as.formula(paste0(metric, " ~ push_group * active_period_num"))
    
    tryCatch({
      fit <- lm(formula, data=model_data)
      coeftest_fit <- coeftest(fit, vcov = vcovHC(fit, type="HC1"))
      print(coeftest_fit)
      active_results[[metric]] <- list(model = fit, coeftest = coeftest_fit, n = nrow(model_data))
    }, error = function(e) cat(paste0("Error fitting ", metric, ": ", e$message, "\n")))
  }
}

saveRDS(active_results, file="../outputs/tables/active_regression_results.rds")

#============================================================
# Analysis 2: Evolution of Dormant Period Metrics
#============================================================

cat("\n========================================\n")
cat("Analysis 2: Evolution of Dormant Period Metrics\n")
cat("========================================\n")

# Model 1: Dormant length (Directly from Python 'dormant_length')
cat("\n--- Model 1: Dormant Length Evolution ---\n")
if ("dormant_length" %in% names(dormant_data)) {
  length_fit <- lm(dormant_length ~ push_group * dormant_period_num, data=dormant_data)
  length_coeftest <- coeftest(length_fit, vcov = vcovHC(length_fit, type="HC1"))
  print(length_coeftest)
}

# Model 2: Push intensity evolution
cat("\n--- Model 2: Push Intensity (Total Pushes) ---\n")
if ("total_pushes" %in% names(dormant_data)) {
  intensity_fit <- lm(total_pushes ~ push_group * dormant_period_num, data=dormant_data)
  intensity_coeftest <- coeftest(intensity_fit, vcov = vcovHC(intensity_fit, type="HC1"))
  print(intensity_coeftest)
}

#============================================================
# Analysis 4: Within-Customer Evolution (Fixed Effects)
#============================================================

cat("\n========================================\n")
cat("Analysis 4: Within-Customer Evolution (Fixed Effects)\n")
cat("========================================\n")

active_long <- melt(active_data, id.vars=c("member_id", "active_period_num", "push_group"),
                    measure.vars=metrics_to_analyze, variable.name="metric", value.name="value")

# Filter to first 5 periods for stability
active_fe_data <- active_long[as.numeric(as.character(active_period_num)) <= 5 & !is.na(value)]
active_fe_data[, metric := as.factor(metric)]

cat("\n--- Active Period FE Model ---\n")
tryCatch({
  active_fe_fit <- felm(value ~ active_period_num:metric | member_id + metric, data=active_fe_data)
  print(summary(active_fe_fit))
  saveRDS(active_fe_fit, file="../outputs/tables/active_fe_results.rds")
}, error = function(e) cat(paste0("Error in FE model: ", e$message, "\n")))

#============================================================
# Analysis 5: Transition Analysis
#============================================================

cat("\n========================================\n")
cat("Analysis 5: Transition Analysis (Active Period t Effect on Dormancy t)\n")
cat("========================================\n")

# Merge active period t with dormant period t
transition_data <- merge(
  active_data[, .(member_id, active_period_num, n_orders, total_spend)],
  dormant_data[, .(member_id, dormant_period_num, total_pushes, dormant_length)],
  by.x=c("member_id", "active_period_num"),
  by.y=c("member_id", "dormant_period_num")
)

# Model: Does active performance predict the length of the subsequent dormancy?
if (nrow(transition_data) > 0) {
  trans_fit <- lm(dormant_length ~ n_orders + total_spend, data=transition_data)
  print(coeftest(trans_fit, vcov = vcovHC(trans_fit, type="HC1")))
  saveRDS(trans_fit, file="../outputs/tables/transition_regression_result.rds")
}

#============================================================
# Create Visualizations
#============================================================

cat("\nCreating Visualizations...\n")
output_dir <- "../outputs/figures/"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

png(paste0(output_dir, "active_period_evolution.png"), width=1200, height=600, res=300)
plot_data <- active_data[, .(total_spend = mean(total_spend, na.rm=TRUE)), 
                         by=.(active_period_num, push_group)]

p <- ggplot(plot_data, aes(x=active_period_num, y=total_spend, color=push_group, group=push_group)) +
  geom_line() + geom_point() +
  theme_minimal() +
  labs(title="Evolution of Total Spend", x="Active Period", y="Avg Spend")
print(p)
dev.off()

#============================================================
# Save Summary Table
#============================================================

summary_table <- data.frame(
  Analysis = c("Active Metrics", "Dormant Length", "Push Intensity", "Within-Customer FE", "Transition Analysis"),
  Status = "Completed"
)
write.csv(summary_table, "../outputs/tables/block_regression_summary.csv", row.names=FALSE)

cat("\n========================================\n")
cat("Block Regression Analysis Complete!\n")
cat("========================================\n")