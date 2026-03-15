#!/bin/bash
# Usage:
#   ./run_with_logging.sh displacement              # runs main.py
#   ./run_with_logging.sh displacement 3           # runs main.py --tail-closures 3

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"       # scripts/displacement_classification
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # model-free/
SRC_CS="$PROJECT_ROOT/src/displacement_classification"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_classification/logs"
mkdir -p "$LOG_DIR"

EXTRA_ARGS=()
if [[ -n "$2" ]]; then
  EXTRA_ARGS=(--tail-closures "$2")
fi

case "$1" in
  displacement)
    cd "$PROJECT_ROOT"
    PYTHONPATH="${PROJECT_ROOT}/src/customer-store:${PROJECT_ROOT}/src/displacement_classification${PYTHONPATH:+:$PYTHONPATH}" \
      python "$SRC_CS/main.py" "${EXTRA_ARGS[@]}" > "$LOG_DIR/displacement_classification.log" 2>&1
    ;;
  *)
    echo "Usage: $0 {displacement} [tail-closures]"
    exit 1
    ;;
esac