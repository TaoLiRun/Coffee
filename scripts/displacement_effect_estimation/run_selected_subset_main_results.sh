#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
UV_ENV_PYTHON="$PROJECT_ROOT/JAX-py/bin/python"

REGISTRY_REL="outputs/customer-store/closure_pair_registry_selected.csv"
FULL_REGISTRY_REL="outputs/customer-store/closure_pair_registry.csv"
REGISTRY_PATH="$PROJECT_ROOT/$REGISTRY_REL"
FULL_REGISTRY_PATH="$PROJECT_ROOT/$FULL_REGISTRY_REL"

OUTPUT_ROOT="$PROJECT_ROOT/outputs/robustness/selected_subset"
PURCHASE_OUTPUT_REL="outputs/robustness/selected_subset/n_purchases"
PURCHASE_BINARY_OUTPUT_REL="outputs/robustness/selected_subset/purchase_incidence_binary"
VARIETY_OUTPUT_REL="outputs/robustness/selected_subset/variety_seeking_unbalanced"
PURCHASE_OUTPUT_DIR="$PROJECT_ROOT/$PURCHASE_OUTPUT_REL"
PURCHASE_BINARY_OUTPUT_DIR="$PROJECT_ROOT/$PURCHASE_BINARY_OUTPUT_REL"
VARIETY_OUTPUT_DIR="$PROJECT_ROOT/$VARIETY_OUTPUT_REL"
METADATA_DIR="$OUTPUT_ROOT/metadata"
SNAPSHOT_REL="outputs/robustness/selected_subset/metadata/closure_pair_registry_selected.csv"
SNAPSHOT_PATH="$PROJECT_ROOT/$SNAPSHOT_REL"
MANIFEST_PATH="$METADATA_DIR/run_manifest.json"
REPORT_BODY_PATH="$PROJECT_ROOT/reports/robustness_selected_subset_body.md"

EXPECTED_SELECTED_CLOSURES=18
EXPECTED_EXCLUDED_CLOSURES=4

if command -v conda >/dev/null 2>&1; then
  PYTHON_CMD=(conda run -n JAX-py python)
  PYTHON_DESC="conda run -n JAX-py python"
elif [ -x "$UV_ENV_PYTHON" ]; then
  PYTHON_CMD=("$UV_ENV_PYTHON")
  PYTHON_DESC="$UV_ENV_PYTHON"
else
  echo "Error: neither \`conda\` nor $UV_ENV_PYTHON is available." >&2
  exit 1
fi

if [ -x "$UV_ENV_PYTHON" ]; then
  PYTHON_EVAL_CMD=("$UV_ENV_PYTHON")
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_EVAL_CMD=("python3")
else
  PYTHON_EVAL_CMD=("${PYTHON_CMD[@]}")
fi

python_eval() {
  "${PYTHON_EVAL_CMD[@]}" - "$@"
}

validate_registry_scope() {
  python_eval "$FULL_REGISTRY_PATH" "$REGISTRY_PATH" "$EXPECTED_SELECTED_CLOSURES" "$EXPECTED_EXCLUDED_CLOSURES" <<'PY'
from pathlib import Path
import sys

import pandas as pd

full_path = Path(sys.argv[1])
selected_path = Path(sys.argv[2])
expected_selected = int(sys.argv[3])
expected_excluded = int(sys.argv[4])

full_df = pd.read_csv(full_path, encoding="utf-8-sig")
selected_df = pd.read_csv(selected_path, encoding="utf-8-sig")

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["dept_id"] = out["dept_id"].astype(str).str.strip()
    out["closure_start"] = pd.to_datetime(out["closure_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    return out[["dept_id", "closure_start"]].dropna().drop_duplicates()

full_keys = normalize(full_df)
selected_keys = normalize(selected_df)
excluded = len(full_keys) - len(selected_keys)

if len(selected_keys) != expected_selected:
    raise SystemExit(
        f"Selected registry has {len(selected_keys)} unique closures; expected {expected_selected}."
    )
if excluded != expected_excluded:
    raise SystemExit(
        f"Selected registry excludes {excluded} closures; expected {expected_excluded}."
    )

merged = selected_keys.merge(full_keys, on=["dept_id", "closure_start"], how="left", indicator=True)
bad = merged[merged["_merge"] != "both"]
if not bad.empty:
    raise SystemExit(
        "Selected registry is not a strict subset of the full closure registry."
    )
PY
}

validate_estimation_bundle() {
  local output_dir="$1"

  python_eval "$output_dir" "$REGISTRY_PATH" "$EXPECTED_SELECTED_CLOSURES" <<'PY'
from pathlib import Path
import sys

import pandas as pd

output_dir = Path(sys.argv[1])
registry_path = Path(sys.argv[2])
expected_selected = int(sys.argv[3])

required_files = [
    output_dir / "ddd_binary_results.csv",
    output_dir / "summary.md",
    output_dir / "estimation_sample.csv",
]
missing_files = [str(path) for path in required_files if not path.exists()]
if missing_files:
    raise SystemExit(f"Missing required output files: {missing_files}")

sample = pd.read_csv(output_dir / "estimation_sample.csv", encoding="utf-8-sig")
registry = pd.read_csv(registry_path, encoding="utf-8-sig")
binary = pd.read_csv(output_dir / "ddd_binary_results.csv", encoding="utf-8-sig")

def normalize_keys(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["dept_id"] = out["dept_id"].astype(str).str.strip()
    out["closure_start"] = pd.to_datetime(out["closure_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    return out[["dept_id", "closure_start"]].dropna().drop_duplicates()

sample_keys = normalize_keys(sample)
registry_keys = normalize_keys(registry)

if len(sample_keys) != expected_selected:
    raise SystemExit(
        f"{output_dir}: estimation sample has {len(sample_keys)} unique closures; "
        f"expected {expected_selected}."
    )

merged = sample_keys.merge(registry_keys, on=["dept_id", "closure_start"], how="left", indicator=True)
bad = merged[merged["_merge"] != "both"]
if not bad.empty:
    raise SystemExit(
        f"{output_dir}: estimation sample includes closures outside the selected registry."
    )

required_terms = {
    "post_X_treated",
    "post_X_disp",
    "post_X_treated_X_disp",
}
terms = set(binary["term"].astype(str))
missing_terms = sorted(required_terms - terms)
if missing_terms:
    raise SystemExit(f"{output_dir}: ddd_binary_results.csv is missing terms {missing_terms}.")
PY
}

mkdir -p "$PURCHASE_OUTPUT_DIR/logs" "$PURCHASE_BINARY_OUTPUT_DIR/logs" "$VARIETY_OUTPUT_DIR/logs" "$METADATA_DIR"

validate_registry_scope
cp "$REGISTRY_PATH" "$SNAPSHOT_PATH"

BRANCH="$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
COMMIT="$(git -C "$PROJECT_ROOT" rev-parse HEAD 2>/dev/null || true)"

PURCHASE_COMMAND="DISPLACEMENT_EFFECT_CLOSURE_REGISTRY=$REGISTRY_REL $PYTHON_DESC src/displacement_effect_estimation/run.py --output-dir $PURCHASE_OUTPUT_REL --log-file $PURCHASE_OUTPUT_REL/logs/run.log"
PURCHASE_BINARY_COMMAND="DISPLACEMENT_EFFECT_CLOSURE_REGISTRY=$REGISTRY_REL $PYTHON_DESC src/displacement_effect_estimation/run.py --outcome purchase_incidence_binary --output-dir $PURCHASE_BINARY_OUTPUT_REL --log-file $PURCHASE_BINARY_OUTPUT_REL/logs/run.log"
VARIETY_COMMAND="DISPLACEMENT_EFFECT_CLOSURE_REGISTRY=$REGISTRY_REL $PYTHON_DESC src/displacement_effect_estimation/run.py --outcome variety_seeking --no-balanced-panel --output-dir $VARIETY_OUTPUT_REL --log-file $VARIETY_OUTPUT_REL/logs/run.log"

echo "Running selected-subset purchase-frequency robustness result..."
(
  cd "$PROJECT_ROOT"
  DISPLACEMENT_EFFECT_CLOSURE_REGISTRY="$REGISTRY_REL" \
    "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --output-dir "$PURCHASE_OUTPUT_REL" \
    --log-file "$PURCHASE_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$PURCHASE_OUTPUT_DIR"

echo "Running selected-subset purchase-incidence robustness result..."
(
  cd "$PROJECT_ROOT"
  DISPLACEMENT_EFFECT_CLOSURE_REGISTRY="$REGISTRY_REL" \
    "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --outcome purchase_incidence_binary \
    --output-dir "$PURCHASE_BINARY_OUTPUT_REL" \
    --log-file "$PURCHASE_BINARY_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$PURCHASE_BINARY_OUTPUT_DIR"

echo "Running selected-subset novelty-seeking robustness result..."
(
  cd "$PROJECT_ROOT"
  DISPLACEMENT_EFFECT_CLOSURE_REGISTRY="$REGISTRY_REL" \
    "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --outcome variety_seeking \
    --no-balanced-panel \
    --output-dir "$VARIETY_OUTPUT_REL" \
    --log-file "$VARIETY_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$VARIETY_OUTPUT_DIR"

"${PYTHON_CMD[@]}" -c 'from datetime import datetime, timezone; import json, sys; from pathlib import Path; manifest_path = Path(sys.argv[1]); branch = sys.argv[4].strip() or None; commit = sys.argv[5].strip() or None; expected_selected = int(sys.argv[9]); expected_excluded = int(sys.argv[10]); manifest = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "source_registry_path": sys.argv[2], "registry_snapshot_path": sys.argv[3], "baseline_purchase_result_path": "outputs/displacement_effect_estimation", "baseline_purchase_binary_result_path": "outputs/displacement_effect_estimation/purchase_incidence_binary", "baseline_novelty_result_path": "outputs/displacement_effect_estimation/variety_seeking_unbalanced", "expected_selected_closure_count": expected_selected, "excluded_closure_count": expected_excluded, "executed_commands": [sys.argv[6], sys.argv[7], sys.argv[8]], "git_branch": branch, "git_commit": commit}; manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")' \
  "$MANIFEST_PATH" "$REGISTRY_REL" "$SNAPSHOT_REL" "$BRANCH" "$COMMIT" "$PURCHASE_COMMAND" "$PURCHASE_BINARY_COMMAND" "$VARIETY_COMMAND" "$EXPECTED_SELECTED_CLOSURES" "$EXPECTED_EXCLUDED_CLOSURES"

python_eval "$PROJECT_ROOT" "$REPORT_BODY_PATH" <<'PY'
from pathlib import Path
import sys

import pandas as pd

project_root = Path(sys.argv[1])
report_body_path = Path(sys.argv[2])

term_labels = {
    "post_X_treated": "post x treated",
    "post_X_disp": "post x blocked",
    "post_X_treated_X_disp": "post x treated x blocked",
}


def load_terms(output_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(output_dir / "ddd_binary_results.csv", encoding="utf-8-sig")
    return df.loc[:, ["term", "coef", "se", "pvalue"]].copy()


def load_sample(output_dir: Path) -> pd.DataFrame:
    return pd.read_csv(output_dir / "estimation_sample.csv", encoding="utf-8-sig")


def closure_count(df: pd.DataFrame) -> int:
    tmp = df.copy()
    tmp["dept_id"] = tmp["dept_id"].astype(str).str.strip()
    tmp["closure_start"] = pd.to_datetime(tmp["closure_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    return tmp[["dept_id", "closure_start"]].dropna().drop_duplicates().shape[0]


def format_num(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}"


def format_pvalue(value: float) -> str:
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def sample_summary_row(label: str, sample: pd.DataFrame) -> dict:
    return {
        "Run": label,
        "Unique closures": closure_count(sample),
        "Unique members": int(sample["member_id"].nunique()),
        "Rows": int(len(sample)),
    }


def comparison_table(baseline_terms: pd.DataFrame, subset_terms: pd.DataFrame) -> pd.DataFrame:
    merged = baseline_terms.merge(
        subset_terms,
        on="term",
        suffixes=("_baseline", "_subset"),
        validate="one_to_one",
    )
    merged["delta_coef"] = merged["coef_subset"] - merged["coef_baseline"]
    return pd.DataFrame(
        {
            "Term": merged["term"].map(term_labels).fillna(merged["term"]),
            "Baseline coef": merged["coef_baseline"].map(format_num),
            "Baseline SE": merged["se_baseline"].map(format_num),
            "Baseline p": merged["pvalue_baseline"].map(format_pvalue),
            "Subset coef": merged["coef_subset"].map(format_num),
            "Subset SE": merged["se_subset"].map(format_num),
            "Subset p": merged["pvalue_subset"].map(format_pvalue),
            "Subset - baseline": merged["delta_coef"].map(format_num),
        }
    )


selected_registry = pd.read_csv(
    project_root / "outputs/customer-store/closure_pair_registry_selected.csv",
    encoding="utf-8-sig",
)
full_registry = pd.read_csv(
    project_root / "outputs/customer-store/closure_pair_registry.csv",
    encoding="utf-8-sig",
)
selected_closure_count = closure_count(selected_registry)
excluded_closure_count = closure_count(full_registry) - selected_closure_count

purchase_baseline_dir = project_root / "outputs/displacement_effect_estimation"
purchase_subset_dir = project_root / "outputs/robustness/selected_subset/n_purchases"
variety_baseline_dir = project_root / "outputs/displacement_effect_estimation/variety_seeking_unbalanced"
variety_subset_dir = project_root / "outputs/robustness/selected_subset/variety_seeking_unbalanced"

purchase_baseline_terms = load_terms(purchase_baseline_dir)
purchase_subset_terms = load_terms(purchase_subset_dir)
variety_baseline_terms = load_terms(variety_baseline_dir)
variety_subset_terms = load_terms(variety_subset_dir)

purchase_baseline_sample = load_sample(purchase_baseline_dir)
purchase_subset_sample = load_sample(purchase_subset_dir)
variety_baseline_sample = load_sample(variety_baseline_dir)
variety_subset_sample = load_sample(variety_subset_dir)

purchase_supported = (
    purchase_subset_terms.loc[
        purchase_subset_terms["term"] == "post_X_treated_X_disp", "coef"
    ].iloc[0]
    >= 0
)
variety_treated = variety_subset_terms.loc[
    variety_subset_terms["term"] == "post_X_treated", "coef"
].iloc[0]
variety_triple = variety_subset_terms.loc[
    variety_subset_terms["term"] == "post_X_treated_X_disp", "coef"
].iloc[0]
variety_supported = variety_treated > 0 and variety_triple < 0

purchase_triple_row = purchase_subset_terms.loc[
    purchase_subset_terms["term"] == "post_X_treated_X_disp"
].iloc[0]
variety_treated_row = variety_subset_terms.loc[
    variety_subset_terms["term"] == "post_X_treated"
].iloc[0]
variety_triple_row = variety_subset_terms.loc[
    variety_subset_terms["term"] == "post_X_treated_X_disp"
].iloc[0]

sample_comp = pd.DataFrame(
    [
        sample_summary_row("Purchase baseline", purchase_baseline_sample),
        sample_summary_row("Purchase selected subset", purchase_subset_sample),
        sample_summary_row("Novelty baseline", variety_baseline_sample),
        sample_summary_row("Novelty selected subset", variety_subset_sample),
    ]
)
purchase_comp = comparison_table(purchase_baseline_terms, purchase_subset_terms)
variety_comp = comparison_table(variety_baseline_terms, variety_subset_terms)

lines = [
    "# Setup",
    "",
    "This report reruns the two headline pooled DDD results on "
    "`outputs/customer-store/closure_pair_registry_selected.csv`, reusing the existing "
    "displacement scores and feature cache. "
    f"The selected registry keeps **{selected_closure_count} closures** and excludes "
    f"**{excluded_closure_count}** from the original kept sample.",
    "",
    "## Sample Composition",
    "",
    sample_comp.to_markdown(index=False),
    "",
    "# Purchase Frequency",
    "",
    f"The purchase-frequency headline claim is **{'supported' if purchase_supported else 'not supported'}** "
    "under the selected subset. "
    f"The subset blocked-buyer triple interaction is {purchase_triple_row['coef']:.4f} "
    f"(SE {purchase_triple_row['se']:.4f}, p={format_pvalue(purchase_triple_row['pvalue'])}).",
    "",
    purchase_comp.to_markdown(index=False),
    "",
    "# Novelty-Seeking",
    "",
    f"The novelty-seeking headline claim is **{'supported' if variety_supported else 'not supported'}** "
    "under the selected subset. "
    f"The subset baseline treatment effect is {variety_treated_row['coef']:.4f} "
    f"(SE {variety_treated_row['se']:.4f}, p={format_pvalue(variety_treated_row['pvalue'])}), "
    f"and the subset blocked-buyer triple interaction is {variety_triple_row['coef']:.4f} "
    f"(SE {variety_triple_row['se']:.4f}, p={format_pvalue(variety_triple_row['pvalue'])}).",
    "",
    variety_comp.to_markdown(index=False),
    "",
    "# Conclusion",
    "",
    "## Headline Verdicts",
    "",
    f"- Purchase frequency: **{'supported' if purchase_supported else 'not supported'}** on the selected {selected_closure_count}-closure subset.",
    f"- Novelty-seeking: **{'supported' if variety_supported else 'not supported'}** on the selected {selected_closure_count}-closure subset.",
    "",
    "This report is intentionally limited to the pooled headline coefficients. "
    "It does not interpret event-study or heterogeneity outputs in this first robustness pass.",
]

report_body_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "Selected-subset robustness outputs saved under: $OUTPUT_ROOT"
echo "Manifest: $MANIFEST_PATH"
