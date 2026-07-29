# Scripts

## Build the published training material

Run the complete documentation build from the repository root:

```bash
scripts/build_training_site.sh
```

The script renders the course landing page, builds the MkDocs learning modules,
and renders the Quarto RevealJS deck into one deployable `_site/` directory.
GitHub Actions calls this same script for pull-request validation and Pages
deployment.
