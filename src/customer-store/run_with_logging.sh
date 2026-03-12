#!/bin/bash
# Run scripts with logs in outputs/customer-store/logs/. Usage:
#   ./run_with_logging.sh analyze_closure_impact
#   ./run_with_logging.sh plot_closure_trend
#   ./run_with_logging.sh displacement  # runs main.py from displacement_classification/

cd "$(dirname "$0")"
LOG_DIR="../../outputs/customer-store/logs"
mkdir -p "$LOG_DIR"

case "$1" in
  analyze_closure_impact)
    python analyze_closure_impact.py > "$LOG_DIR/analyze_closure_impact.log" 2>&1
    ;;
  plot_closure_trend)
    python plot_closure_trend.py > "$LOG_DIR/plot_closure_trend.log" 2>&1
    ;;
  *)
    echo "Usage: $0 {analyze_closure_impact|plot_closure_trend|displacement}"
    exit 1
    ;;
esac
