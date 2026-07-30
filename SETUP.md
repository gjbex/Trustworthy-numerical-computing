# Environment Setup

The conda environment contains the portable Python and Jupyter runtime used by
the tutorial notebooks. Quarto is installed separately because its conda-forge
package is not available consistently across Linux, macOS, and Windows.
Numerical-library dependencies will be added alongside the activities that
require them.


## Install Quarto

Install Quarto 1.9.38 using the installer for your operating system from the
[official Quarto download page](https://quarto.org/docs/download/). Quarto is a
publishing application rather than a Python dependency, and must be available
on `PATH`.

Verify the installation:

```bash
quarto --version
```


## Create the environment

From the repository root, create and activate the conda environment:

```bash
mamba env create -f environment.yml
mamba activate trustworthy_numerical_computing
```

Verify the notebook runtime:

```bash
python --version
jupyter lab --version
```


## Build all published material

Run:

```bash
scripts/build_training_site.sh
```

This builds:

* the course landing page at `_site/index.html`;
* the Quarto learning modules under `_site/learning-modules/`;
* executed activity pages and runnable notebooks under `_site/notebooks/`;
* the RevealJS slide deck under `_site/slides/`.

The `_site/` directory is generated and ignored by Git. Remove it at any time;
the build script recreates it from the tracked sources.


## Preview while editing

Preview the landing page and learning modules with:

```bash
quarto preview
```

Preview an interactive activity directly from its authoritative Quarto source:

```bash
quarto preview notebooks/01-opening-experiment.qmd
```

After running the complete build, open the generated notebook for an editable
Jupyter session with:

```bash
jupyter lab _site/notebooks/01-opening-experiment.ipynb
```

The `.qmd` activity source is tracked. Generated `.ipynb` files and their
execution output remain under `_site/` and are not committed.

Preview the slides with:

```bash
slides-source/preview.sh
```


## Optional workflow validation

Course maintainers can install `actionlint` 1.7.12 separately to validate GitHub
Actions workflows. It is not required by participants and is intentionally not
part of the conda environment.

For example, with Go installed:

```bash
go install github.com/rhysd/actionlint/cmd/actionlint@v1.7.12
actionlint .github/workflows/pages.yml
```

Prebuilt binaries and other installation methods are documented in the
[actionlint repository](https://github.com/rhysd/actionlint).


## GitHub Pages

The workflow in `.github/workflows/pages.yml`:

* builds the complete site on pull requests to validate the sources;
* uploads `_site/` as a GitHub Pages artifact after changes reach `main`;
* deploys the artifact through the `github-pages` environment.

In the repository settings, configure **Pages → Build and deployment → Source**
to use **GitHub Actions**. Do not configure branch-based deployment from
`docs/`; generated HTML is intentionally not committed.
