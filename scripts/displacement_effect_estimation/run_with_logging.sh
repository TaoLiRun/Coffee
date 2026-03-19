#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src/displacement_effect_estimation"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_effect_estimation/logs"
mkdir -p "$LOG_DIR"

cd "$SRC_DIR"
conda run -n JAX-py python run.py "$@" > "$LOG_DIR/run.log" 2>&1
echo "Done. Log: $LOG_DIR/run.log"
