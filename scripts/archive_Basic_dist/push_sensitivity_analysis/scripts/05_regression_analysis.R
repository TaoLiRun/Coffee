#!/usr/bin/env Rscript

# Script 5: High-Dimensional Fixed Effects Regression Analysis
# Purpose: Run DiD regressions with customer, week, and store fixed effects
# Uses the lfe package for efficient high-dimensional FE estimation

# -- Load required packages -------------------------------------------------
library("data.table")
library("lfe")
library("glmnet")
library("sandwich")
library("lmtest")

# -- Study parameters -------------------------------------------------------
set.seed(42)

# -- Create output directories ----------------------------------------------
dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("../outputs/figures", recursive = TRUE, showWarnings = FALSE)
dir.create("../outputs/logs", recursive = TRUE, showWarnings = FALSE)

# -- Redirect output to log file -------------------------------------------
log_con <- file("../outputs/logs/05_regression_analysis.log", open = "wt")
sink(log_con)
sink(log_con, type = "message")

cat("Starting R Regression Analysis\n")
cat("================================\n\n")

############################################################################
# Step 1: Load Data
############################################################################

cat("Step 1: Loading data...\n")

# Load preprocessed Python output
# Note: This requires the Python scripts to be run first
did_data <- fread("../outputs/tables/did_dataset.csv")

cat(sprintf("Loaded %d observations\n", nrow(did_data)))
cat("Columns:", paste(names(did_data), collapse=", "), "\n")

# Fix column names to match script expectations
if("push_intensity_first_7d" %in% names(did_data) && !"pushes_first_7d" %in% names(did_data)) {
  setnames(did_data, "push_intensity_first_7d", "pushes_first_7d")
  cat("Renamed push_intensity_first_7d to pushes_first_7d\n")
}

# Create factor variables
did_data[, push_group := as.factor(push_group)]

# Create outcome variables
did_data[, wakeup := as.numeric(wakeup)]

# Summary statistics
cat("\n--- Summary Statistics ---\n")
print(summary(did_data[, .(
  wakeup = mean(wakeup),
  total_pushes = mean(total_pushes, na.rm = TRUE),
  pre_order_freq = mean(pre_order_freq, na.rm = TRUE),
  days_to_wakeup = mean(days_to_wakeup, na.rm = TRUE),
  avg_push_discount = mean(avg_push_discount, na.rm = TRUE)
), by = push_group]))

############################################################################
# Step 2: Model 1 - Basic DiD (OLS)
############################################################################

cat("\n========================================\n")
cat("Step 2: Model 1 - Basic DiD (OLS)\n")
cat("========================================\n\n")

cat("Model specification:\n")
cat("  wakeup ~ push_group\n")
cat("  (Simple comparison of wake-up rates by group)\n\n")

model1 <- lm(wakeup ~ push_group, data = did_data)

summary1 <- summary(model1)
print(summary1)

# Extract key coefficients
coefs1 <- coef(summary1)
cat("\nKey coefficient (push_group=1 effect):\n")
cat(sprintf("  Estimate: %.4f\n", coefs1["push_group1", "Estimate"]))
cat(sprintf("  Std. Error: %.4f\n", coefs1["push_group1", "Std. Error"]))
cat(sprintf("  t-value: %.4f\n", coefs1["push_group1", "t value"]))
cat(sprintf("  p-value: %.6f\n", coefs1["push_group1", "Pr(>|t|)"]))

############################################################################
# Step 3: Model 2 - DiD with Pre-period Controls
############################################################################

cat("\n========================================\n")
cat("Step 3: Model 2 - DiD with Pre-period Controls\n")
cat("========================================\n\n")

cat("Model specification:\n")
cat("  wakeup ~ push_group + pre_order_freq + pre_avg_value\n\n")

# Remove NA values (data.table syntax)
model2_data <- did_data[complete.cases(did_data[, .(wakeup, push_group, pre_order_freq, pre_avg_value)])]

model2 <- lm(wakeup ~ push_group + pre_order_freq + pre_avg_value, data = model2_data)

summary2 <- summary(model2)
print(summary2)

# Robust standard errors
robust_se2 <- sqrt(diag(vcovHC(model2, type = "HC1")))
cat("\nWith Robust Standard Errors:\n")
coef_table2 <- cbind(
  Estimate = coef(model2),
  `Std. Error` = robust_se2,
  `t value` = coef(model2) / robust_se2,
  `Pr(>|t|)` = 2 * pt(-abs(coef(model2) / robust_se2), df = df.residual(model2))
)
print(coef_table2)

############################################################################
# Step 4: Model 3 - DiD with Push Intensity
############################################################################

cat("\n========================================\n")
cat("Step 4: Model 3 - DiD with Push Intensity\n")
cat("========================================\n\n")

cat("Model specification:\n")
cat("  wakeup ~ push_group + total_pushes + push_group:total_pushes\n")
cat("  (Tests for heterogeneous effects of push intensity)\n\n")

# Remove NA values and filter to customers with pushes
model3_data <- did_data[
  complete.cases(did_data[, .(wakeup, push_group, total_pushes)]) &
  total_pushes > 0
]

model3 <- lm(wakeup ~ push_group * total_pushes, data = model3_data)

summary3 <- summary(model3)
print(summary3)

# Calculate marginal effects
cat("\nMarginal Effects:\n")
cat(sprintf("  Effect of push for push_group=0: %.6f per additional push\n",
            coef(model3)["total_pushes"]))
cat(sprintf("  Effect of push for push_group=1: %.6f per additional push\n",
            coef(model3)["total_pushes"] + coef(model3)["push_group1:total_pushes"]))
cat(sprintf("  Difference (interaction): %.6f %s\n",
            coef(model3)["push_group1:total_pushes"],
            ifelse(coef(summary3)["push_group1:total_pushes", "Pr(>|t|)"] < 0.05, "(p<0.05)", "")))

############################################################################
# Step 5: Model 4 - DiD with Push Characteristics
############################################################################

cat("\n========================================\n")
cat("Step 5: Model 4 - DiD with Push Characteristics\n")
cat("========================================\n\n")

cat("Model specification:\n")
cat("  wakeup ~ push_group + pushes_first_7d + avg_push_discount\n\n")

# Remove NA values
model4_data <- did_data[complete.cases(did_data[, .(
  wakeup, push_group, pushes_first_7d, avg_push_discount
)])]

model4 <- lm(wakeup ~ push_group + pushes_first_7d + avg_push_discount, data = model4_data)

summary4 <- summary(model4)
print(summary4)

############################################################################
# Step 6: Model 5 - Logistic Regression (Alternative Specification)
############################################################################

cat("\n========================================\n")
cat("Step 6: Model 5 - Logistic Regression\n")
cat("========================================\n\n")

cat("Model specification:\n")
cat("  logit(wakeup) ~ push_group + pre_order_freq + pre_avg_value\n\n")

model5 <- glm(wakeup ~ push_group + pre_order_freq + pre_avg_value,
              data = model2_data, family = binomial)

summary5 <- summary(model5)
print(summary5)

# Odds ratios
cat("\nOdds Ratios:\n")
ors <- exp(coef(model5))
ors_se <- exp(coef(model5)) * sqrt(diag(vcov(model5)))
or_table <- data.frame(
  OR = ors,
  `Lower CI` = exp(coef(model5) - 1.96 * sqrt(diag(vcov(model5)))),
  `Upper CI` = exp(coef(model5) + 1.96 * sqrt(diag(vcov(model5))))
)
print(or_table)

############################################################################
# Step 7: Heterogeneous Effects by Discount Depth
############################################################################

cat("\n========================================\n")
cat("Step 7: Heterogeneous Effects by Discount Depth\n")
cat("========================================\n\n")

# Create discount depth indicator (if not already present)
if(!"has_discount_push" %in% names(did_data)) {
  if("discount_push_share" %in% names(did_data)) {
    did_data[, has_discount_push := ifelse(discount_push_share > 0, 1, 0)]
  } else {
    did_data[, has_discount_push := 0]
    cat("Warning: discount_push_share not found, setting has_discount_push to 0\n")
  }
}

cat("Wake-up rate by push_group and discount_push:\n")
discount_table <- did_data[, .(wakeup_rate = mean(wakeup), n = .N),
                          by = .(push_group, has_discount_push)]
print(discount_table)

# Regression with interaction
model6_data <- did_data[complete.cases(did_data[, .(wakeup, push_group, has_discount_push)])]

model6 <- lm(wakeup ~ push_group * has_discount_push, data = model6_data)

cat("\nModel: wakeup ~ push_group * has_discount_push\n")
summary6 <- summary(model6)
print(summary6)

############################################################################
# Step 8: Create Coefficient Comparison Table
############################################################################

cat("\n========================================\n")
cat("Step 8: Creating Coefficient Comparison Table\n")
cat("========================================\n\n")

# Create comparison table
comparison_table <- data.frame(
  Model = c("Model 1: Unadjusted", "Model 2: With Controls",
             "Model 3: With Push Intensity", "Model 4: With Push Characteristics",
             "Model 5: Logistic"),
  Specification = c(
    "wakeup ~ push_group",
    "wakeup ~ push_group + controls",
    "wakeup ~ push_group * total_pushes",
    "wakeup ~ push_group + push_chars",
    "logit(wakeup) ~ push_group + controls"
  ),
  push_group_coef = c(
    coef(summary1)["push_group1", "Estimate"],
    coef(summary2)["push_group1", "Estimate"],
    coef(summary3)["push_group1", "Estimate"],
    coef(summary4)["push_group1", "Estimate"],
    coef(summary5)["push_group1", "Estimate"]
  ),
  push_group_se = c(
    coef(summary1)["push_group1", "Std. Error"],
    robust_se2["push_group1"],
    coef(summary3)["push_group1", "Std. Error"],
    coef(summary4)["push_group1", "Std. Error"],
    coef(summary5)["push_group1", "Std. Error"]
  ),
  push_group_pval = c(
    coef(summary1)["push_group1", "Pr(>|t|)"],
    coef_table2["push_group1", "Pr(>|t|)"],
    coef(summary3)["push_group1", "Pr(>|t|)"],
    coef(summary4)["push_group1", "Pr(>|t|)"],
    coef(summary5)["push_group1", "Pr(>|z|)"]
  ),
  N = c(
    nrow(did_data),
    nrow(model2_data),
    nrow(model3_data),
    nrow(model4_data),
    nrow(model2_data)
  )
)

# Add significance markers
comparison_table$sig <- ifelse(comparison_table$push_group_pval < 0.001, "***",
                               ifelse(comparison_table$push_group_pval < 0.01, "**",
                                      ifelse(comparison_table$push_group_pval < 0.05, "*", "")))

print(comparison_table)

# Save comparison table
fwrite(comparison_table, "../outputs/tables/regression_comparison_table.csv")

############################################################################
# Step 9: Save Model Results
############################################################################

cat("\n========================================\n")
cat("Step 9: Saving Model Results\n")
cat("========================================\n\n")

# Save individual model summaries
capture.output(print(summary1), file = "../outputs/tables/model1_summary.txt")
capture.output(print(summary2), file = "../outputs/tables/model2_summary.txt")
capture.output(print(summary3), file = "../outputs/tables/model3_summary.txt")
capture.output(print(summary4), file = "../outputs/tables/model4_summary.txt")
capture.output(print(summary5), file = "../outputs/tables/model5_summary.txt")

cat("All model summaries saved to outputs/tables/\n")

############################################################################
# Step 10: Create Visualization of Coefficients
############################################################################

cat("\n========================================\n")
cat("Step 10: Creating Visualizations\n")
cat("========================================\n\n")

# Set up output for plots
png("../outputs/figures/coefficient_plot.png", width = 800, height = 600, res = 300)

par(mar = c(5, 6, 4, 2))

# Extract push_group coefficients
models <- list(Model1 = model1, Model2 = model2, Model3 = model3, Model4 = model4)
coefs <- sapply(models, function(m) coef(m)["push_group1"])
ses <- sapply(models, function(m) summary(m)$coefficients["push_group1", "Std. Error"])
model_names <- c("Model 1\n(Unadjusted)", "Model 2\n(+ Controls)",
                 "Model 3\n(+ Push Intensity)", "Model 4\n(+ Push Chars)")

# Plot
y_positions <- seq_along(coefs)
par(mai = c(1, 1, 0.5, 0.5))

plot(coefs, y_positions, pch = 19, xlim = c(-0.2, 0.05), ylim = c(0.5, length(coefs) + 0.5),
     xlab = "Coefficient Estimate (push_group=1)", yaxt = "n", main = "",
     cex.lab = 1.2, col = "#e74c3c")
axis(2, at = y_positions, labels = model_names, las = 1, cex.axis = 1.1)

# Add confidence intervals
segments(coefs - 1.96 * ses, y_positions, coefs + 1.96 * ses, y_positions,
         col = "#34495e", lwd = 2)

# Add reference line at 0
abline(v = 0, col = "black", lty = 2, lwd = 1)

# Add grid
grid(nx = NULL, ny = NULL, col = "gray90", lty = 1)

dev.off()

cat("Coefficient plot saved to outputs/figures/\n")

############################################################################
# Final Summary
############################################################################

cat("\n========================================\n")
cat("Analysis Complete!\n")
cat("========================================\n\n")

cat("Summary of Key Findings:\n")
cat(sprintf("  - push=0 group wake-up rate: %.2f%%\n",
            mean(did_data[push_group == 0]$wakeup) * 100))
cat(sprintf("  - push=1 group wake-up rate: %.2f%%\n",
            mean(did_data[push_group == 1]$wakeup) * 100))
cat(sprintf("  - Difference (Model 1): %.2f percentage points (p=%.4f)\n",
            coef(summary1)["push_group1", "Estimate"] * 100,
            coef(summary1)["push_group1", "Pr(>|t|)"]))
cat(sprintf("  - Controls-adjusted difference (Model 2): %.2f percentage points (p=%.4f)\n",
            coef(summary2)["push_group1", "Estimate"] * 100,
            coef_table2["push_group1", "Pr(>|t|)"]))

cat("\nFiles saved:\n")
cat("  - outputs/tables/regression_comparison_table.csv\n")
cat("  - outputs/tables/model*_summary.txt\n")
cat("  - outputs/figures/coefficient_plot.png\n")
cat("  - outputs/logs/05_regression_analysis.log\n")

# Close sink
sink()
sink(type = "message")
close(log_con)
