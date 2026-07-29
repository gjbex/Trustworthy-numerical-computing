#!/usr/bin/env bash

set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

for command in mkdocs quarto; do
    if ! command -v "$command" >/dev/null 2>&1; then
        echo "Required command not found: $command" >&2
        exit 127
    fi
done

site_output_dir="$repo_root/_site"
if [[ "$site_output_dir" != "$repo_root/_site" ]]; then
    echo "Refusing to clean unexpected output directory: $site_output_dir" >&2
    exit 1
fi

rm -rf -- "$site_output_dir"
mkdir -p "$site_output_dir"

echo "Building course landing page..."
quarto render docs/README.md \
    --to html \
    --output-dir "$site_output_dir"
mv "$site_output_dir/README.html" "$site_output_dir/index.html"

echo "Building learning modules..."
mkdocs build --strict --site-dir "$site_output_dir/learning-modules"

echo "Building slide deck..."
quarto render slides-source/trustworthy-numerical-computing.qmd \
    --to revealjs \
    --output-dir "$site_output_dir/slides"

for entry_point in \
    "$site_output_dir/index.html" \
    "$site_output_dir/learning-modules/index.html" \
    "$site_output_dir/slides/trustworthy-numerical-computing.html"; do
    if [[ ! -f "$entry_point" ]]; then
        echo "Expected publication entry point not found: $entry_point" >&2
        exit 1
    fi
done

echo "Generated deployable training site under _site/."
