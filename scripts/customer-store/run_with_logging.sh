#!/bin/bash
# Run src/customer-store scripts with logs in outputs/customer-store/logs/.
# This script lives in scripts/customer-store/ but always runs Python files
# from src/customer-store/ so relative imports work correctly.
#
# Usage:
#   ./run_with_logging.sh analyze_closure_impact
#   ./run_with_logging.sh plot_closure_trend
#   ./run_with_logging.sh displacement   # runs src/displacement_classification/main.py

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"       # scripts/customer-store
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # model-free/
SRC_CS="$PROJECT_ROOT/src/customer-store"
LOG_DIR="$PROJECT_ROOT/outputs/customer-store/logs"
mkdir -p "$LOG_DIR"

case "$1" in
  analyze_closure_impact)
    cd "$SRC_CS"
    python analyze_closure_impact.py > "$LOG_DIR/analyze_closure_impact.log" 2>&1
    ;;
  plot_closure_trend)
    cd "$SRC_CS"
    python plot_closure_trend.py > "$LOG_DIR/plot_closure_trend.log" 2>&1
    ;;
  *)
    echo "Usage: $0 {analyze_closure_impact|plot_closure_trend|displacement}"
    exit 1
    ;;
esac
#example: bash run_with_logging.sh plot_closure_trend