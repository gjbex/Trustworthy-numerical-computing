# Slide sources

The Quarto RevealJS slide deck is modular and follows the numbered learning
modules.

* `trustworthy-numerical-computing.qmd` owns the presentation metadata and
  includes the section files.
* `00-course-overview.qmd` introduces the learning path.
* `01-...qmd` through `10-...qmd` correspond one-to-one with the numbered
  reading modules.
* `11-wrap-up.qmd` closes the course.

Build the published deck from the repository root with:

```bash
scripts/build_training_site.sh
```

Preview it while editing with:

```bash
slides-source/preview.sh
```

Slides are teaching aids. Detailed explanation belongs in `learning-modules/`;
trainer-only delivery guidance belongs in `::: notes` blocks.
