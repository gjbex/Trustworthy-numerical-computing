# Trustworthy Numerical Computing

Training material for recognizing, investigating, preventing, and communicating
numerical reliability problems in scientific computing.

The course is language-agnostic at the conceptual level. Short computational
experiments will be used to expose failure modes and compare validation
strategies without tying the material to one programming language.


## What is it?

1. `index.qmd`: source for the course landing page.
1. `learning-modules/`: long-form reading material, published with Quarto.
1. `notebooks/`: authoritative Quarto sources for interactive activities;
   the build generates runnable Jupyter notebooks.
1. `slides-source/`: modular Quarto RevealJS slides aligned with the learning
   modules.
1. `source-code/`: demonstrations and small numerical experiments.
1. `hands-on/`: participant-facing exercises and starter files.
1. `_quarto.yml`: navigation and configuration for the course website.
1. `requirements-notebooks.txt`: Python dependencies used to execute notebooks
   locally and in CI.
1. `scripts/build_training_site.sh`: assembles the deployable website under
   `_site/`.
1. `.github/workflows/pages.yml`: validates the site on pull requests and
   deploys it to GitHub Pages from `main`.
1. `environment.yml`: portable Python and Jupyter environment for notebooks and
   core exercises.
1. `SETUP.md`: setup and publication instructions.


## Training materials

- [Course landing page](index.qmd)
- [Learning modules](learning-modules/index.md)
- [Slide sources](slides-source/trustworthy-numerical-computing.qmd)

After running `scripts/build_training_site.sh`, preview the assembled landing
page at `_site/index.html`, the learning modules under
`_site/learning-modules/`, and the slide deck under `_site/slides/`. Quarto
renders the landing page, reading material, interactive activities, generated
Jupyter notebooks, and RevealJS slides.

Generated HTML is not committed. GitHub Actions builds the same `_site/`
artifact for pull-request validation and deploys it after changes reach `main`.
Quarto is installed separately from the conda environment; see
[SETUP.md](SETUP.md) for the supported version and installation guidance.


## Current status

The overall learning path and publication layout are in place. Modules 1
through 5 include detailed reading and executable self-paced activities; the
remaining module and slide files provide the structure for developing later
reading, experiments, and exercises.


## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before
opening issues or pull requests.
