# This script processes push notification policy data by aggregating push counts by date, policy ID, and trigger tag.

library(dplyr)
library(ggplot2)
library(lubridate)
library(data.table)

# set the working directory
setwd("/home/litao/Coffee/")

policy_dt <- read.csv("model-free/data/processed/policy_dt.csv")

# group and sumup the column "num_push"
policy_dt <- policy_dt %>%
  group_by(dt, policy_id, trigger_tag) %>%
  summarise(num_push = sum(num_push)) %>%
  ungroup() %>%
  distinct()

write.csv(policy_dt, "model-free/data/processed/policy_dt.csv",
          row.names = FALSE)
          
'''
# Find all push data files
push_files <- list.files(path = "data/data1031/",
                         pattern = "^sleep_push_result_.*\\.csv$",
                         full.names = TRUE)

# Read and combine all push data
# drop duplicates, and add a column: num_push
all_push_data <- lapply(push_files, function(file) {
  read.csv(file) %>%
    select(dt, policy_id, trigger_tag)
}) %>%
  bind_rows() %>%
  group_by(dt, policy_id, trigger_tag) %>%
  mutate(num_push = n()) %>%
  ungroup() %>%
  distinct()

# 328 unique policy_id
cat("unique policy_id: ", length(unique(all_push_data$policy_id)))

# select columns: dt, policy_id; drop duplicates
policy_dt <- all_push_data %>%
  arrange(dt) %>%
  distinct()

# save policy_dt to a csv file
write.csv(policy_dt, "model-free/processed_data/policy_dt.csv",
          row.names = FALSE)'''
