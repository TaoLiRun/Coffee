#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
UV_ENV_PYTHON="$PROJECT_ROOT/JAX-py/bin/python"

REGISTRY_REL="outputs/customer-store/closure_pair_registry.csv"
FULL_REGISTRY_REL="outputs/customer-store/closure_pair_registry_full.csv"
REGISTRY_PATH="$PROJECT_ROOT/$REGISTRY_REL"
FULL_REGISTRY_PATH="$PROJECT_ROOT/$FULL_REGISTRY_REL"

OUTPUT_ROOT="$PROJECT_ROOT/outputs/03_main_18_closures"
PURCHASE_OUTPUT_REL="outputs/03_main_18_closures/purchase_frequency_ddd_h4"
PURCHASE_BINARY_OUTPUT_REL="outputs/03_main_18_closures/purchase_incidence_ddd_h4"
VARIETY_OUTPUT_REL="outputs/03_main_18_closures/novelty_member_first_ddd_h4"
PURCHASE_OUTPUT_DIR="$PROJECT_ROOT/$PURCHASE_OUTPUT_REL"
PURCHASE_BINARY_OUTPUT_DIR="$PROJECT_ROOT/$PURCHASE_BINARY_OUTPUT_REL"
VARIETY_OUTPUT_DIR="$PROJECT_ROOT/$VARIETY_OUTPUT_REL"
METADATA_DIR="$OUTPUT_ROOT/metadata"
SNAPSHOT_REL="outputs/03_main_18_closures/metadata/closure_pair_registry.csv"
SNAPSHOT_PATH="$PROJECT_ROOT/$SNAPSHOT_REL"
MANIFEST_PATH="$METADATA_DIR/run_manifest.json"
REPORT_BODY_PATH="$PROJECT_ROOT/reports/main_results_body.md"

EXPECTED_MAIN_CLOSURES=18
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
  python_eval "$FULL_REGISTRY_PATH" "$REGISTRY_PATH" "$EXPECTED_MAIN_CLOSURES" "$EXPECTED_EXCLUDED_CLOSURES" <<'PY'
from pathlib import Path
import sys

import pandas as pd

full_path = Path(sys.argv[1])
main_path = Path(sys.argv[2])
expected_main = int(sys.argv[3])
expected_excluded = int(sys.argv[4])

full_df = pd.read_csv(full_path, encoding="utf-8-sig")
main_df = pd.read_csv(main_path, encoding="utf-8-sig")

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["dept_id"] = out["dept_id"].astype(str).str.strip()
    out["closure_start"] = pd.to_datetime(out["closure_start"], errors="coerce").dt.strftime("%Y-%m-%d")
    return out[["dept_id", "closure_start"]].dropna().drop_duplicates()

full_keys = normalize(full_df)
main_keys = normalize(main_df)
excluded = len(full_keys) - len(main_keys)

if len(main_keys) != expected_main:
    raise SystemExit(
        f"Main registry has {len(main_keys)} unique closures; expected {expected_main}."
    )
if excluded != expected_excluded:
    raise SystemExit(
        f"Main registry excludes {excluded} closures from the full registry; expected {expected_excluded}."
    )

merged = main_keys.merge(full_keys, on=["dept_id", "closure_start"], how="left", indicator=True)
bad = merged[merged["_merge"] != "both"]
if not bad.empty:
    raise SystemExit(
        "Main registry is not a strict subset of the full closure registry."
    )
PY
}

validate_estimation_bundle() {
  local output_dir="$1"

  python_eval "$output_dir" "$REGISTRY_PATH" "$EXPECTED_MAIN_CLOSURES" <<'PY'
from pathlib import Path
import sys

import pandas as pd

output_dir = Path(sys.argv[1])
registry_path = Path(sys.argv[2])
expected_main = int(sys.argv[3])

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

if len(sample_keys) != expected_main:
    raise SystemExit(
        f"{output_dir}: estimation sample has {len(sample_keys)} unique closures; "
        f"expected {expected_main}."
    )

merged = sample_keys.merge(registry_keys, on=["dept_id", "closure_start"], how="left", indicator=True)
bad = merged[merged["_merge"] != "both"]
if not bad.empty:
    raise SystemExit(
        f"{output_dir}: estimation sample includes closures outside the main registry."
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

PURCHASE_COMMAND="$PYTHON_DESC src/displacement_effect_estimation/run.py --output-dir $PURCHASE_OUTPUT_REL --log-file $PURCHASE_OUTPUT_REL/logs/run.log"
PURCHASE_BINARY_COMMAND="$PYTHON_DESC src/displacement_effect_estimation/run.py --outcome purchase_incidence_binary --output-dir $PURCHASE_BINARY_OUTPUT_REL --log-file $PURCHASE_BINARY_OUTPUT_REL/logs/run.log"
VARIETY_COMMAND="$PYTHON_DESC src/displacement_effect_estimation/run.py --outcome variety_seeking --output-dir $VARIETY_OUTPUT_REL --log-file $VARIETY_OUTPUT_REL/logs/run.log"

echo "Running main-sample purchase-frequency result..."
(
  cd "$PROJECT_ROOT"
  "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --output-dir "$PURCHASE_OUTPUT_REL" \
    --log-file "$PURCHASE_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$PURCHASE_OUTPUT_DIR"

echo "Running main-sample purchase-incidence result..."
(
  cd "$PROJECT_ROOT"
  "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --outcome purchase_incidence_binary \
    --output-dir "$PURCHASE_BINARY_OUTPUT_REL" \
    --log-file "$PURCHASE_BINARY_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$PURCHASE_BINARY_OUTPUT_DIR"

echo "Running main-sample novelty-seeking result..."
(
  cd "$PROJECT_ROOT"
  "${PYTHON_CMD[@]}" src/displacement_effect_estimation/run.py \
    --outcome variety_seeking \
    --output-dir "$VARIETY_OUTPUT_REL" \
    --log-file "$VARIETY_OUTPUT_REL/logs/run.log"
)
validate_estimation_bundle "$VARIETY_OUTPUT_DIR"

"${PYTHON_CMD[@]}" -c 'from datetime import datetime, timezone; import json, sys; from pathlib import Path; manifest_path = Path(sys.argv[1]); branch = sys.argv[4].strip() or None; commit = sys.argv[5].strip() or None; expected_main = int(sys.argv[9]); expected_excluded = int(sys.argv[10]); manifest = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "source_registry_path": sys.argv[2], "registry_snapshot_path": sys.argv[3], "full_registry_path": "outputs/customer-store/closure_pair_registry_full.csv", "purchase_result_path": "outputs/03_main_18_closures/purchase_frequency_ddd_h4", "purchase_binary_result_path": "outputs/03_main_18_closures/purchase_incidence_ddd_h4", "novelty_result_path": "outputs/03_main_18_closures/novelty_member_first_ddd_h4", "expected_main_closure_count": expected_main, "excluded_closure_count": expected_excluded, "executed_commands": [sys.argv[6], sys.argv[7], sys.argv[8]], "git_branch": branch, "git_commit": commit}; manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")' \
  "$MANIFEST_PATH" "$REGISTRY_REL" "$SNAPSHOT_REL" "$BRANCH" "$COMMIT" "$PURCHASE_COMMAND" "$PURCHASE_BINARY_COMMAND" "$VARIETY_COMMAND" "$EXPECTED_MAIN_CLOSURES" "$EXPECTED_EXCLUDED_CLOSURES"

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


def comparison_table(full_terms: pd.DataFrame, main_terms: pd.DataFrame) -> pd.DataFrame:
    merged = full_terms.merge(
        main_terms,
        on="term",
        suffixes=("_full", "_main"),
        validate="one_to_one",
    )
    merged["delta_coef"] = merged["coef_main"] - merged["coef_full"]
    return pd.DataFrame(
        {
            "Term": merged["term"].map(term_labels).fillna(merged["term"]),
            "Full-registry coef": merged["coef_full"].map(format_num),
            "Full-registry SE": merged["se_full"].map(format_num),
            "Full-registry p": merged["pvalue_full"].map(format_pvalue),
            "Main-sample coef": merged["coef_main"].map(format_num),
            "Main-sample SE": merged["se_main"].map(format_num),
            "Main-sample p": merged["pvalue_main"].map(format_pvalue),
            "Main - full": merged["delta_coef"].map(format_num),
        }
    )


main_registry = pd.read_csv(
    project_root / "outputs/customer-store/closure_pair_registry.csv",
    encoding="utf-8-sig",
)
full_registry = pd.read_csv(
    project_root / "outputs/customer-store/closure_pair_registry_full.csv",
    encoding="utf-8-sig",
)
main_closure_count = closure_count(main_registry)
excluded_closure_count = closure_count(full_registry) - main_closure_count

purchase_full_dir = project_root / "outputs/05_robustness/full_registry_22/n_purchases"
purchase_main_dir = project_root / "outputs/03_main_18_closures/purchase_frequency_ddd_h4"
variety_full_dir = project_root / "outputs/05_robustness/full_registry_22/variety_seeking_unbalanced"
variety_main_dir = project_root / "outputs/03_main_18_closures/novelty_member_first_ddd_h4"

purchase_full_terms = load_terms(purchase_full_dir)
purchase_main_terms = load_terms(purchase_main_dir)
variety_full_terms = load_terms(variety_full_dir)
variety_main_terms = load_terms(variety_main_dir)

purchase_full_sample = load_sample(purchase_full_dir)
purchase_main_sample = load_sample(purchase_main_dir)
variety_full_sample = load_sample(variety_full_dir)
variety_main_sample = load_sample(variety_main_dir)

purchase_supported = (
    purchase_main_terms.loc[
        purchase_main_terms["term"] == "post_X_treated_X_disp", "coef"
    ].iloc[0]
    >= 0
)
variety_treated = variety_main_terms.loc[
    variety_main_terms["term"] == "post_X_treated", "coef"
].iloc[0]
variety_triple = variety_main_terms.loc[
    variety_main_terms["term"] == "post_X_treated_X_disp", "coef"
].iloc[0]
variety_supported = variety_treated > 0 and variety_triple < 0

purchase_triple_row = purchase_main_terms.loc[
    purchase_main_terms["term"] == "post_X_treated_X_disp"
].iloc[0]
variety_treated_row = variety_main_terms.loc[
    variety_main_terms["term"] == "post_X_treated"
].iloc[0]
variety_triple_row = variety_main_terms.loc[
    variety_main_terms["term"] == "post_X_treated_X_disp"
].iloc[0]

sample_comp = pd.DataFrame(
    [
        sample_summary_row("Purchase full registry", purchase_full_sample),
        sample_summary_row("Purchase main sample", purchase_main_sample),
        sample_summary_row("Novelty full registry", variety_full_sample),
        sample_summary_row("Novelty main sample", variety_main_sample),
    ]
)
purchase_comp = comparison_table(purchase_full_terms, purchase_main_terms)
variety_comp = comparison_table(variety_full_terms, variety_main_terms)

lines = [
    "# Setup",
    "",
    "This report reruns the two headline pooled DDD results on "
    "`outputs/customer-store/closure_pair_registry.csv`, reusing the existing "
    "displacement scores and feature cache. "
    f"The main registry keeps **{main_closure_count} closures** and excludes "
    f"**{excluded_closure_count}** from the original kept sample.",
    "",
    "## Sample Composition",
    "",
    sample_comp.to_markdown(index=False),
    "",
    "# Purchase Frequency",
    "",
    f"The purchase-frequency headline claim is **{'supported' if purchase_supported else 'not supported'}** "
    "under the main sample. "
    f"The main-sample blocked-buyer triple interaction is {purchase_triple_row['coef']:.4f} "
    f"(SE {purchase_triple_row['se']:.4f}, p={format_pvalue(purchase_triple_row['pvalue'])}).",
    "",
    purchase_comp.to_markdown(index=False),
    "",
    "# Novelty-Seeking",
    "",
    f"The novelty-seeking headline claim is **{'supported' if variety_supported else 'not supported'}** "
    "under the main sample. "
    f"The main-sample baseline treatment effect is {variety_treated_row['coef']:.4f} "
    f"(SE {variety_treated_row['se']:.4f}, p={format_pvalue(variety_treated_row['pvalue'])}), "
    f"and the main-sample blocked-buyer triple interaction is {variety_triple_row['coef']:.4f} "
    f"(SE {variety_triple_row['se']:.4f}, p={format_pvalue(variety_triple_row['pvalue'])}).",
    "",
    variety_comp.to_markdown(index=False),
    "",
    "# Conclusion",
    "",
    "## Headline Verdicts",
    "",
    f"- Purchase frequency: **{'supported' if purchase_supported else 'not supported'}** on the main {main_closure_count}-closure sample.",
    f"- Novelty-seeking: **{'supported' if variety_supported else 'not supported'}** on the main {main_closure_count}-closure sample.",
    "",
    "This report is intentionally limited to the pooled headline coefficients. "
    "It does not interpret event-study or heterogeneity outputs in this first main-results pass.",
]

report_body_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "Main-sample outputs saved under: $OUTPUT_ROOT"
echo "Manifest: $MANIFEST_PATH"
