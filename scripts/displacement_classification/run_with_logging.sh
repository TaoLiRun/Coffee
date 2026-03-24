#!/bin/bash
# Usage:
#   ./run_with_logging.sh displacement
#   ./run_with_logging.sh displacement --tail-closures 3
#   ./run_with_logging.sh displacement --rebuild-push-cache

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"       # scripts/displacement_classification
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # model-free/
SRC_CS="$PROJECT_ROOT/src/displacement_classification"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_classification/logs"
PYTHON_BIN="/home/litao/anaconda3/bin/python3"
mkdir -p "$LOG_DIR"

case "$1" in
  displacement)
    shift
    cd "$PROJECT_ROOT"
    PYTHONPATH="${PROJECT_ROOT}/src/customer-store:${PROJECT_ROOT}/src/displacement_classification${PYTHONPATH:+:$PYTHONPATH}" \
      "$PYTHON_BIN" "$SRC_CS/main.py" "$@" > "$LOG_DIR/displacement_classification.log" 2>&1
    ;;
  *)
    echo "Usage: $0 displacement [args to main.py, e.g. --tail-closures N --rebuild-push-cache]"
    exit 1
    ;;
esac
