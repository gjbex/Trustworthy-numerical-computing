# Environment Setup

The current environment contains the tools needed to build the learning-module
website and Quarto slide deck. Numerical libraries will be added when the
primary language and exercises are selected.


## Create the environment

From the repository root, create and activate the conda environment:

```bash
mamba env create -f environment.yml
mamba activate trustworthy_numerical_computing
```

Verify the documentation tools:

```bash
mkdocs --version
quarto --version
```


## Build all published material

Run:

```bash
scripts/build_training_site.sh
```

This builds:

* the course landing page at `_site/index.html`;
* the MkDocs learning-module site under `_site/learning-modules/`;
* the RevealJS slide deck under `_site/slides/`.

The `_site/` directory is generated and ignored by Git. Remove it at any time;
the build script recreates it from the tracked sources.


## Preview while editing

Preview the learning modules with:

```bash
mkdocs serve
```

Preview the slides with:

```bash
slides-source/preview.sh
```


## GitHub Pages

The workflow in `.github/workflows/pages.yml`:

* builds the complete site on pull requests to validate the sources;
* uploads `_site/` as a GitHub Pages artifact after changes reach `main`;
* deploys the artifact through the `github-pages` environment.

In the repository settings, configure **Pages → Build and deployment → Source**
to use **GitHub Actions**. Do not configure branch-based deployment from
`docs/`; generated HTML is intentionally not committed.
