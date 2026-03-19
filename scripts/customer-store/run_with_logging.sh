#!/bin/bash
# Run src/customer-store scripts with logs in outputs/customer-store/logs/.
# This script lives in scripts/customer-store/ but always runs Python files
# from src/customer-store/ so relative imports work correctly.
#
# Usage:
#   ./run_with_logging.sh
#   ./run_with_logging.sh main_customer_store

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"       # scripts/customer-store
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # model-free/
SRC_CS="$PROJECT_ROOT/src/customer-store"
LOG_DIR="$PROJECT_ROOT/outputs/customer-store/logs"
mkdir -p "$LOG_DIR"

if [ -z "$1" ] || [ "$1" = "main_customer_store" ]; then
  cd "$SRC_CS"
  python main_customer_store.py > "$LOG_DIR/main_customer_store.log" 2>&1
else
  echo "Usage: $0 [main_customer_store]"
  exit 1
fi
# example: bash run_with_logging.sh