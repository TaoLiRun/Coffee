#!/bin/bash

# Examples:
# Aggregate effect across all closures/events (default):
#   ./run_with_logging.sh
#
# Separate effect for each closure/event:
#   ./run_with_logging.sh --separate-effect
#
# Separate effect for each closure/event, keeping only consumers with
# a purchase in (closure_start - 10, closure_start):
#   ./run_with_logging.sh --separate-effect --select-recency-consumers 10
#
# Invalid:
#   ./run_with_logging.sh --select-recency-consumers 10
# because --select-recency-consumers is only allowed with --separate-effect.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src/displacement_effect_estimation"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_effect_estimation/logs"
mkdir -p "$LOG_DIR"

cd "$SRC_DIR"
conda run -n JAX-py python run.py "$@" > "$LOG_DIR/run.log" 2>&1
echo "Done. Log: $LOG_DIR/run.log"
