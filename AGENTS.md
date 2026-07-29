# AGENTS.md

This repository is a template for training-material repositories, not a
software package.


## Repository Style

- Keep the classic GitHub Pages layout: `docs/README.md` plus
  `docs/_config.yml`.
- Use Jekyll with `theme: jekyll-theme-slate`.
- Do not replace the classic Pages setup with a custom GitHub Actions Pages
  workflow unless explicitly requested.
- Keep participant-facing navigation simple: root `README.md`, `SETUP.md`,
  `docs/`, `source-code/`, and optional `hands-on/`.
- Do not force package-style layout such as `src/` unless the training actually
  ships a reusable software package.


## Documentation

- `docs/README.md` is the public training landing page.
- Keep these sections when applicable:
  - Learning outcomes
  - Schedule
  - Training materials
  - Target audience
  - Prerequisites
  - Quick self-assessment
  - Software and access requirements
  - Level of the Material
  - Trainer(s)
- Prefer concrete participant-facing setup instructions over vague requirements.
- Keep Markdown plain and compatible with GitHub Pages/Jekyll.


## Examples

- Put examples and demonstrations in `source-code/`.
- Add local `README.md` files for nontrivial examples.
- Keep commands to run examples close to the code.
- Avoid committing generated outputs unless they are part of the teaching
  material.


## Hands-on Material

- Put participant exercises in `hands-on/`.
- Keep starter files and solutions clearly separated.
- If no hands-on material exists, remove the directory rather than keeping an
  empty placeholder.


## Template Placeholders

- Template placeholders use double-brace uppercase names.
- Use `scripts/fill_placeholders.py` and `template-values.yml` to fill them.
- Do not remove placeholder examples from template documentation unless
  replacing them with real training values.


## Editing Rules

- Preserve existing user changes.
- Avoid broad refactors while updating training content.
- Do not normalize unrelated formatting across notebooks, slides, generated
  files, or legacy training material.
- Keep changes focused on the requested training-repository improvement.
