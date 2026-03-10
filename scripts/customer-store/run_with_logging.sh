#!/bin/bash
# Run scripts with logs in the same directory. Usage:
#   ./run_with_logging.sh analyze_closure_impact
#   ./run_with_logging.sh plot_closure_trend
#   ./run_with_logging.sh displacement  # runs train_displacement_model.py from displacement_classification/

cd "$(dirname "$0")"
case "$1" in
  analyze_closure_impact)
    python analyze_closure_impact.py > analyze_closure_impact.log 2>&1
    ;;
  plot_closure_trend)
    python plot_closure_trend.py > plot_closure_trend.log 2>&1
    ;;
  displacement)
    cd ../displacement_classification
    python train_displacement_model.py  # logs to train_displacement_model.log internally
    ;;
  *)
    echo "Usage: $0 {analyze_closure_impact|plot_closure_trend|displacement}"
    exit 1
    ;;
esac
