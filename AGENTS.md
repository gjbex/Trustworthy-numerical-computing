# Repository Instructions

## Scope

This repository is a connected training system. Treat reading material, slides,
examples, exercises, and generated publication output as related teaching
surfaces.


## Repository map

- `learning-modules/`: long-form Markdown reading material built with MkDocs.
- `slides-source/`: modular Quarto RevealJS sources aligned with the modules.
- `source-code/`: demonstrations and small numerical experiments.
- `hands-on/`: participant exercises, including the capstone.
- `docs/README.md`: source for the course landing page.
- `_site/`: ignored, generated publication artifact.
- `mkdocs.yml`: learning-module navigation.
- `scripts/build_training_site.sh`: complete publication build.
- `.github/workflows/pages.yml`: pull-request validation and Pages deployment.


## Core consistency rule

A curriculum change is not complete until the affected learning module, slide
section, example or exercise, navigation, and participant-facing landing page
remain consistent.


## Module-to-slide mapping

Every numbered learning module has a matching numbered slide partial:

```text
learning-modules/04-conditioning-and-numerical-stability.md
slides-source/04-conditioning-and-numerical-stability.qmd
```

When adding, removing, renaming, or substantially changing a module:

- update `mkdocs.yml`;
- update `learning-modules/index.md`;
- update `learning-modules/learning-module-structure.md`;
- update the matching slide file;
- update the includes in
  `slides-source/trustworthy-numerical-computing.qmd`;
- check any named `source-code/` or `hands-on/` paths.


## Teaching order

Preserve the prerequisite chain:

1. numerical validity and investigation workflow;
2. floating-point arithmetic;
3. error measures and tolerances;
4. conditioning and stability;
5. common failure modes;
6. convergence;
7. validation;
8. reproducibility;
9. communication;
10. capstone investigation.

Do not introduce an advanced technique before the vocabulary or validation
method needed to judge it.


## Learning modules

- Write for scientists and technical programmers who already know how to
  program.
- Keep concepts language-agnostic unless syntax is the teaching point.
- Connect mathematical properties to observable program behaviour.
- State what evidence supports a claim.
- Prefer small experiments over long implementations.
- Do not duplicate declared programming prerequisites.


## Slides

- Slides support oral delivery; they do not replace the reading material.
- Visible text is trainee-facing.
- Put trainer-only guidance in `::: notes`.
- Use one level-1 heading per included module section and level-2 headings for
  ordinary slides.
- Keep code short and move longer work to concrete example paths.


## Examples and exercises

- Keep each example focused on one numerical idea or investigation.
- Include exact run commands and observable checks in a nearby `README.md`.
- Keep starter material and reference solutions clearly separated.
- Prefer deterministic examples unless variability is the lesson.
- When variability is intentional, state what range or relationship is
  expected.


## Generated output

Edit sources in `learning-modules/` and `slides-source/`. Do not manually edit
generated files under `_site/`.

Build all publication output with:

```bash
scripts/build_training_site.sh
```


## Validation

For documentation-only structural changes, run:

```bash
mkdocs build --strict
quarto render slides-source/trustworthy-numerical-computing.qmd --to revealjs
```

For complete publication validation, run:

```bash
scripts/build_training_site.sh
```

The build must produce these artifact entry points:

- `_site/index.html`;
- `_site/learning-modules/index.html`;
- `_site/slides/trustworthy-numerical-computing.html`.

Also check that links in `README.md`, `docs/README.md`, `mkdocs.yml`, and the
top-level Quarto includes resolve to real files.


## Continuous integration and deployment

- Pull requests build the complete site without deploying it.
- Pushes to `main` build, upload, and deploy the `_site/` Pages artifact.
- Keep build logic in `scripts/build_training_site.sh`; do not duplicate it in
  workflow-only commands.
- Keep deployment permissions on the deploy job. The build job should remain
  read-only.
- Do not commit generated HTML or have a workflow commit it back to `main`.


## Repository style

- Publish GitHub Pages through the artifact workflow, not from a branch
  directory.
- Keep participant-facing navigation simple.
- Do not force a package-style `src/` layout onto this training repository.
- Avoid committing transient notebook, Quarto, or local preview output.
- Preserve existing user changes and avoid unrelated formatting churn.
