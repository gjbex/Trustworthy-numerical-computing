# Scripts

## Build the published training material

Run the complete documentation build from the repository root:

```bash
scripts/build_training_site.sh
```

The script renders the Quarto course website, executes the interactive activity
sources, generates runnable Jupyter notebooks, and renders the Quarto RevealJS
deck into the same deployable `_site/` directory. GitHub Actions calls this same
script for pull-request validation and Pages deployment.

`sanitize_generated_notebook.py` removes machine-local kernel paths from the
generated notebooks before they are published.


## Regenerate the binary64-spacing figure

Run the deterministic, standard-library generator from the repository root:

```bash
python scripts/generate_binary64_spacing_figure.py
```

It writes the reviewed course asset to `figures/binary64-spacing.svg`. The
generator validates the highlighted gaps against the Module 2 values before
writing the SVG.
