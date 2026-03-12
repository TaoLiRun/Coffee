#!/bin/bash
# Usage:
#   ./run_with_logging.sh displacement   # runs src/displacement_classification/main.py

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"       # scripts/displacement_classification
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # model-free/
SRC_CS="$PROJECT_ROOT/src/displacement_classification"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_classification/logs"
mkdir -p "$LOG_DIR"

case "$1" in
  displacement)
    cd "$SRC_CS"
    python main.py > "$LOG_DIR/displacement_classification.log" 2>&1
    ;;
  *)
    echo "Usage: $0 {displacement}"
    exit 1
    ;;
esac