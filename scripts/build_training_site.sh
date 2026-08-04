#!/usr/bin/env bash

set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

if ! command -v quarto >/dev/null 2>&1; then
    echo "Required command not found: quarto" >&2
    exit 127
fi

site_output_dir="$repo_root/_site"
if [[ "$site_output_dir" != "$repo_root/_site" ]]; then
    echo "Refusing to clean unexpected output directory: $site_output_dir" >&2
    exit 1
fi

rm -rf -- "$site_output_dir"
mkdir -p "$site_output_dir"

echo "Building downloadable Jupyter notebooks..."
for notebook_source in notebooks/*.qmd; do
    quarto render "$notebook_source" --to ipynb --execute
    generated_notebook_name=$(basename "${notebook_source%.qmd}.ipynb")
    python scripts/sanitize_generated_notebook.py \
        "$site_output_dir/notebooks/$generated_notebook_name"
done

echo "Building course website and learning modules..."
quarto render --execute --no-clean

echo "Building slide deck..."
quarto render slides-source/trustworthy-numerical-computing.qmd

for entry_point in \
    "$site_output_dir/index.html" \
    "$site_output_dir/learning-modules/index.html" \
    "$site_output_dir/notebooks/01-opening-experiment.html" \
    "$site_output_dir/notebooks/01-opening-experiment.ipynb" \
    "$site_output_dir/notebooks/02-floating-point-landmarks.html" \
    "$site_output_dir/notebooks/02-floating-point-landmarks.ipynb" \
    "$site_output_dir/notebooks/03-comparison-criteria.html" \
    "$site_output_dir/notebooks/03-comparison-criteria.ipynb" \
    "$site_output_dir/notebooks/04-sensitivity-stability-residuals.html" \
    "$site_output_dir/notebooks/04-sensitivity-stability-residuals.ipynb" \
    "$site_output_dir/notebooks/05-failure-mode-lab.html" \
    "$site_output_dir/notebooks/05-failure-mode-lab.ipynb" \
    "$site_output_dir/notebooks/06-convergence-and-stopping.html" \
    "$site_output_dir/notebooks/06-convergence-and-stopping.ipynb" \
    "$site_output_dir/notebooks/07-validation-evidence.html" \
    "$site_output_dir/notebooks/07-validation-evidence.ipynb" \
    "$site_output_dir/notebooks/08-environment-reproducibility.html" \
    "$site_output_dir/notebooks/08-environment-reproducibility.ipynb" \
    "$site_output_dir/notebooks/09-reliability-statement.html" \
    "$site_output_dir/notebooks/09-reliability-statement.ipynb" \
    "$site_output_dir/hands-on/README.html" \
    "$site_output_dir/hands-on/10-sensor-inversion/README.html" \
    "$site_output_dir/hands-on/10-sensor-inversion/starter/capstone.py" \
    "$site_output_dir/hands-on/10-sensor-inversion/starter/test_capstone.py" \
    "$site_output_dir/hands-on/10-sensor-inversion/starter/evidence-record.md" \
    "$site_output_dir/hands-on/10-sensor-inversion/solution/README.html" \
    "$site_output_dir/hands-on/10-sensor-inversion/solution/capstone.py" \
    "$site_output_dir/hands-on/10-sensor-inversion/solution/test_capstone.py" \
    "$site_output_dir/hands-on/10-sensor-inversion/solution/evidence-record.md" \
    "$site_output_dir/slides/trustworthy-numerical-computing.html"; do
    if [[ ! -f "$entry_point" ]]; then
        echo "Expected publication entry point not found: $entry_point" >&2
        exit 1
    fi
done

echo "Generated deployable training site under _site/."
