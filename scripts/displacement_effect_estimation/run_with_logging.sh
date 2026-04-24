#!/bin/bash

# =============================================================================
# Panel structure and model selection
# =============================================================================
# The estimation supports two panel structures that determine the model:
#
#   BALANCED panel  -> DiD model (no displacement prediction needed)
#     Members who purchased in every period (variety_seeking) or every
#     pre-period (n_purchases) are retained.  A simple DiD is estimated:
#       y = delta * post * treated + FE
#
#   UNBALANCED panel -> DDD model (displacement prediction via classification)
#     All members are kept.  A triple-difference accounts for selection:
#       y = delta^B * post * treated + delta^D * post * treated * D + ...
#
# The model is chosen automatically based on the panel structure:
#   variety_seeking  -> balanced by default (DiD); --no-balanced-panel switches to DDD
#   n_purchases      -> unbalanced by default (DDD); --no-unbalanced-panel switches to DiD
# =============================================================================

# Examples:
# Aggregate DDD effect across all closures/events (default, unbalanced panel):
#   ./run_with_logging.sh
#
# Aggregate DiD effect (balanced panel, only members purchasing in every pre-period):
#   ./run_with_logging.sh --no-unbalanced-panel \
#       --output-dir outputs/displacement_effect_estimation/balanced_did
#
# Separate effect for each closure/event:
#   ./run_with_logging.sh --separate-effect
#
# Separate effect for each closure/event, keeping only consumers with
# a purchase in (closure_start - 10, closure_start):
#   ./run_with_logging.sh --separate-effect --select-recency-consumers 10
#
# Separate effect for 10-day closures only, with recency filter, saved to
# a custom output directory:
#   ./run_with_logging.sh --separate-effect --closure-duration-days 10 \
#       --select-recency-consumers 10 \
#       --output-dir outputs/displacement_effect_estimation/separate_effect_d10_r10
#
# Variety-seeking, distinct mode (balanced panel, DiD by default):
#   ./run_with_logging.sh --outcome variety_seeking \
#       --output-dir outputs/displacement_effect_estimation/variety_seeking
#
# Variety-seeking, instance mode (each purchase row counted separately):
#   ./run_with_logging.sh --outcome variety_seeking --variety-seeking-mode instance \
#       --output-dir outputs/displacement_effect_estimation/variety_seeking_instance
#
# Variety-seeking, instance-only-old mode (share of purchase rows on products
# that existed before rel_t=-4):
#   ./run_with_logging.sh --outcome variety_seeking --variety-seeking-mode instance-only-old \
#       --output-dir outputs/displacement_effect_estimation/variety_seeking_instance_only_old
#
# Variety-seeking, unbalanced panel (switches from DiD to DDD):
#   ./run_with_logging.sh --outcome variety_seeking --no-balanced-panel \
#       --output-dir outputs/displacement_effect_estimation/variety_seeking_unbalanced
#
# Invalid:
#   ./run_with_logging.sh --select-recency-consumers 10
# because --select-recency-consumers is only allowed with --separate-effect.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src/displacement_effect_estimation"
LOG_DIR="$PROJECT_ROOT/outputs/displacement_effect_estimation/logs"
UV_ENV_PYTHON="$PROJECT_ROOT/JAX-py/bin/python"
mkdir -p "$LOG_DIR"

cd "$SRC_DIR"

if command -v conda >/dev/null 2>&1; then
    conda run -n JAX-py python run.py "$@" > "$LOG_DIR/run.log" 2>&1
elif [ -x "$UV_ENV_PYTHON" ]; then
    "$UV_ENV_PYTHON" run.py "$@" > "$LOG_DIR/run.log" 2>&1
else
    echo "Error: neither \`conda\` nor $UV_ENV_PYTHON is available." >&2
    exit 1
fi

echo "Done. Log: $LOG_DIR/run.log"
