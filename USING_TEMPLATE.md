# Using This Template

This repository is intended to be marked as a GitHub template repository.


## Create A New Training Repository

1. Push this repository to GitHub.
1. In the repository settings, enable **Template repository**.
1. Create a new training repository with **Use this template**.
1. Copy `template-values.yml`, fill in the values, and run
   `scripts/fill_placeholders.py`.
1. Configure GitHub Pages:
   * Source: deploy from a branch.
   * Branch: `main` or `master`.
   * Folder: `/docs`.
1. Verify that the published page uses `jekyll-theme-slate`.


## Placeholders To Replace

Search for double-brace placeholder markers and replace all placeholders before
publishing.

You can list unresolved placeholders with:

```bash
scripts/fill_placeholders.py template-values.yml --list
```

To preview replacements without editing files:

```bash
scripts/fill_placeholders.py my-values.yml --dry-run
```

To replace placeholders and fail if any remain:

```bash
scripts/fill_placeholders.py my-values.yml --strict
```

Common placeholders:

* `{{TRAINING_TITLE}}`
* `{{TRAINING_SHORT_DESCRIPTION}}`
* `{{TRAINING_TOPIC}}`
* `{{REPOSITORY_URL}}`
* `{{REPOSITORY_NAME}}`
* `{{SLIDE_DECK_FILE}}`
* `{{TRAINER_NAME}}`
* `{{TRAINER_EMAIL}}`
* `{{CONDA_ENVIRONMENT_NAME}}`


## Keep The Classic Pages Style

The website is intentionally simple:

* `docs/README.md` is the landing page;
* `docs/_config.yml` sets `theme: jekyll-theme-slate`;
* no custom GitHub Actions workflow is required for Pages;
* generated slide HTML, if any, should live under `docs/slides/`.


## Cleanup Checklist

Before publishing a new training repository:

* remove unused directories such as `hands-on/` or `slides-source/`;
* choose and replace `LICENSE`;
* update `environment.yml` or remove it if not used;
* verify all links in `README.md` and `docs/README.md`;
* run at least one setup verification command from `SETUP.md`;
* check that `.ipynb_checkpoints/`, generated build directories, and temporary
  outputs are not tracked.
