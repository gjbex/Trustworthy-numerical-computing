# Repository Instructions

## Purpose

This repository contains the training course *Trustworthy Numerical Computing*.
Treat the landing page, learning modules, slides, demonstrations, exercises, and
publication workflow as one connected teaching system.

The course should help scientists and research software engineers:

1. recognize numerical reliability problems;
2. investigate their causes systematically;
3. prevent or mitigate avoidable problems;
4. validate numerical results with appropriate evidence;
5. communicate assumptions, uncertainty, and limitations.

Always distinguish code that runs correctly from a result that is numerically
and scientifically valid. Language safety, memory safety, type safety, and
ordinary functional tests are valuable, but none establishes numerical validity
on its own.


## Audience and prerequisites

Write for scientists, research software engineers, and technical programmers
who can already read and modify small programs in at least one
scientific-computing language.

Participants may use Python, Julia, C, C++, Fortran, R, MATLAB, Rust, or another
language. Keep the conceptual material language-agnostic unless syntax or a
runtime choice is itself the teaching point.

Assume participants understand:

- variables, expressions, functions, loops, and arrays;
- basic algebra and scientific notation;
- how to run a short program or notebook;
- how to interpret a simple table or plot.

Do not assume prior knowledge of IEEE 754, conditioning, numerical stability,
convergence analysis, parallel reductions, or formal numerical analysis. Define
those ideas before relying on them. Do not reteach general programming concepts
that belong to the prerequisites.


## Repository map

- `index.qmd`: source for the course landing page.
- `learning-modules/`: long-form Markdown reading material built with Quarto.
- `learning-modules/learning-module-structure.md`: prerequisite order and
  delivery structure.
- `notebooks/`: authoritative Quarto `.qmd` sources for self-paced tutorial
  activities; the build generates HTML and runnable Jupyter notebooks.
- `_quarto.yml`: website navigation and HTML rendering configuration.
- `slides-source/`: modular Quarto RevealJS sources aligned with the modules.
- `slides-source/trustworthy-numerical-computing.qmd`: complete slide deck and
  include order.
- `source-code/`: demonstrations and small numerical experiments.
- `hands-on/`: participant exercises and the capstone investigation.
- `environment.yml`: portable Python and Jupyter runtime for course activities.
- `requirements-notebooks.txt`: notebook runtime dependencies installed by CI.
- `scripts/build_training_site.sh`: complete local and CI publication build.
- `.github/workflows/pages.yml`: pull-request validation and Pages deployment.
- `_site/`: ignored, generated deployment artifact.


## Core consistency rule

A curriculum change is not complete until all affected teaching surfaces agree.

Every numbered learning module has a matching numbered slide partial:

```text
learning-modules/04-conditioning-and-numerical-stability.md
slides-source/04-conditioning-and-numerical-stability.qmd
```

When adding, removing, renaming, reordering, or substantially changing a
module:

- update `_quarto.yml`;
- update `learning-modules/index.md`;
- update `learning-modules/learning-module-structure.md`;
- update the matching numbered slide source;
- update the includes in
  `slides-source/trustworthy-numerical-computing.qmd`;
- check `index.qmd` learning outcomes and schedule;
- check all named `source-code/` and `hands-on/` paths;
- check `README.md` and `SETUP.md` when setup or navigation changes.

Use the same terminology for a concept across modules, slides, examples, and
exercises. Do not silently redefine terms such as error, residual, uncertainty,
accuracy, precision, stability, or reproducibility.


## Curriculum and prerequisite order

Preserve this teaching dependency chain:

1. **When Correct Code Produces Wrong Answers** introduces numerical validity
   and the investigation workflow.
2. **Understanding Floating-Point Arithmetic** provides the finite-precision
   model.
3. **Measuring And Comparing Numerical Error** introduces error measures and
   defensible tolerances.
4. **Conditioning And Numerical Stability** separates problem sensitivity,
   algorithmic behaviour, and implementation defects.
5. **Common Numerical Failure Modes** applies those distinctions to
   cancellation, accumulation, scaling, overflow, and underflow.
6. **Iterative Algorithms And Convergence** introduces residuals, updates,
   stopping criteria, stagnation, and failure reporting.
7. **Validating Scientific Computations** combines references, invariants,
   properties, refinement, and independent methods.
8. **Reproducibility Across Computing Environments** addresses compiler,
   library, hardware, optimization, and parallel-order variation.
9. **Communicating Numerical Reliability** turns evidence into a qualified
   scientific claim.
10. **Capstone Investigation** integrates the complete workflow.

Do not use a later distinction as if it were already known. In particular:

- introduce scale-aware error measures before judging stability;
- introduce conditioning before attributing all discrepancies to an algorithm;
- distinguish residual from error before teaching stopping criteria;
- establish validation methods before discussing acceptable cross-platform
  variation;
- teach communication after participants have evidence to communicate.

Keep optional advanced topics after the complete core path. Mixed precision,
interval arithmetic, advanced linear algebra, stochastic validation, and
accelerator reproducibility should not displace the core investigation
workflow.


## Numerical evidence standards

Every computational demonstration, worked example, or exercise should make the
following explicit when relevant:

- the numerical or scientific question;
- input values, units, scale, and valid range;
- the expected qualitative behaviour;
- the reference value, independent check, invariant, or expected trend;
- the error measure or diagnostic quantity;
- the tolerance and its rationale;
- the observed result;
- the limitations of the evidence.

Apply these rules:

- Do not use a universal epsilon or a tolerance chosen merely to make a test
  pass.
- Use absolute, relative, or mixed tolerances according to scale and behaviour
  near zero.
- Distinguish an exact value, a high-precision reference, a trusted benchmark,
  an independent estimate, and an expected range.
- Do not present a residual as the true error without a justified relationship.
- Separate problem conditioning, algorithmic stability, implementation error,
  modelling error, discretization error, and input uncertainty.
- Treat `NaN`, infinity, signed zero, overflow, underflow, and subnormal values
  as observable numerical states, not generic exceptions to hide.
- State whether reproducibility means bitwise identity, tolerance-based
  agreement, statistical equivalence, or the same scientific conclusion.
- Use explicit seeds for stochastic examples. Validate distributions or
  summary properties when exact sequences are not the claim.
- Keep correctness and performance claims separate. Do not imply that a faster
  method is sufficiently accurate without evidence.
- Report only digits supported by the calculation and its inputs.

A failure-mode example must fail for the intended numerical reason. Check that a
contrived case is not actually dominated by a programming defect, unit mistake,
invalid reference, accidental integer operation, or unrelated model error.

Reference solutions should be independently justified. Higher precision is a
useful reference only when its own formulation and convergence have been
checked.


## Learning modules

Learning modules are self-contained reading material, not transcripts of the
slides.

Prefer this structure for a numbered module:

1. a short motivation tied to scientific work;
2. explicit learning outcomes;
3. prerequisite connection to earlier modules;
4. concept explanation with units, assumptions, and limitations;
5. one or more small experiments or worked examples;
6. interpretation and validation questions;
7. a transition to the next module.

Write precise technical prose without turning a module into a numerical-analysis
textbook chapter. Introduce equations only when they clarify reasoning or the
implementation. Define symbols, units, norms, and scaling conventions close to
their first use.

Prefer observable questions:

- What changes when the input scale changes?
- Which quantity is being measured?
- What evidence distinguishes two possible causes?
- What would make this result untrustworthy?
- Which conclusion survives a change in precision or execution order?

Avoid presenting implementation recipes without explaining how participants can
judge whether they worked.


## Interactive notebooks

Interactive activities are self-paced tutorials that complement the reading
modules; they do not replace every narrative page.

- Put participant-facing activity sources in `notebooks/` as executable Quarto
  `.qmd` files.
- Treat each `.qmd` file as the authoritative source. Do not edit or commit the
  generated `.ipynb` file.
- Quarto executes activity sources from a clean kernel during the complete site
  build and generates both HTML and a runnable notebook under `_site/notebooks/`.
- Keep each activity deterministic, fast, and runnable from top to bottom.
- Use explicit parameters and repository-relative paths.
- Move reusable logic to `source-code/` rather than copying it between
  notebooks.
- Keep notebook dependencies synchronized between
  `requirements-notebooks.txt` and `environment.yml`.
- Add an **Open in Colab** link only when the generated notebook is reachable by
  the intended learners.


## Slides

Slides are instructor-led teaching aids. They should support discussion,
prediction, short derivations, live experiments, and interpretation rather than
duplicate the reading material.

- Visible slide text is trainee-facing.
- Put trainer-only instructions, transitions, cautions, and timing guidance in
  `::: notes`.
- Each included module file starts with one level-1 heading.
- Use level-2 headings for ordinary slides.
- Keep one main idea per slide and usually three to five bullets.
- Keep code fragments short. Point longer demonstrations to a real path and an
  exact command.
- Use prediction prompts before revealing numerical output.
- Make units, scales, reference values, and tolerance choices visible when they
  are necessary to interpret a figure or table.
- Keep the slide sequence aligned with the matching learning module, but do not
  copy its paragraphs.

When a module changes conceptually, update its slide partial in the same change.
A prose-only clarification need not change slides if the teaching flow and
claims remain unchanged.


## Examples and demonstrations

Put runnable demonstrations in `source-code/`. Organize them by module or
investigation once concrete examples are added.

Each nontrivial example should have a nearby `README.md` that states:

- its purpose and numerical question;
- the files and inputs involved;
- the exact command to run;
- what participants should predict;
- the expected output shape or diagnostic;
- the reference or validation method;
- known limitations and optional variations.

Prefer small experiments that isolate one effect. Avoid long implementations,
network access, hidden data, long runtimes, unusual hardware, or fragile
services unless they are central to the lesson.

Python is the reference implementation language for short runnable examples and
Jupyter tutorial notebooks. Keep the conceptual explanations language-agnostic,
use the standard library where practical, and add third-party numerical
dependencies only when they serve a specific learning goal. Add equivalents in
other languages only when they help the expected participants rather than
multiplying maintenance cost.


## Hands-on exercises and capstone

Put participant work in `hands-on/`. Keep starter material and reference
solutions clearly separated.

Each exercise should include:

- a numerical question and required accuracy;
- a prediction or hypothesis;
- concrete tasks and controlled variations;
- evidence to record;
- completion criteria;
- optional extensions;
- an independently checked reference solution.

The Module 10 capstone must require participants to:

1. reproduce and characterize a suspicious result;
2. establish a meaningful reference or independent check;
3. assess conditioning and identify the dominant failure mode;
4. improve one factor at a time;
5. validate the change with complementary evidence;
6. write a concise reliability statement.

Do not define capstone success as bitwise identity unless the case specifically
requires it. A qualified conclusion that explains an unavoidable limitation can
be a successful outcome.


## Figures, tables, and reported results

- Label axes, units, scales, and compared methods.
- State whether an axis is linear or logarithmic when it is not visually
  obvious.
- Keep enough significant digits to expose the lesson without implying false
  accuracy.
- Include the reference or baseline in comparison tables.
- Use deterministic ordering for generated tables and sampled data.
- Record the command, parameters, environment, and source revision needed to
  reproduce a published figure when figures are added.
- Do not present one machine's timing as a universal performance result.

Generated figures and data belong under an ignored output directory unless they
are intentional, reviewed course assets. If a generated asset is committed,
document its generating command and provenance.


## Dependencies and environments

Keep dependencies conservative and tied to teaching needs.

- `.github/workflows/pages.yml` pins the Python and Quarto toolchains used for
  publication.
- `requirements-notebooks.txt` pins the Jupyter runtime used to execute tutorial
  notebooks in CI.
- `environment.yml` pins the corresponding portable Python and Jupyter runtime
  for participants and local notebook execution.
- Quarto is a separately installed publishing application. Keep the supported
  local version in `SETUP.md` aligned with the version pinned in
  `.github/workflows/pages.yml`.
- `actionlint` is an optional, separately installed maintainer tool; it does not
  belong in the participant environment.
- Do not add a platform-specific application to `environment.yml` without
  checking Linux, macOS, Windows, and relevant CPU architectures.
- When changing a documentation-tool version, update all affected files and run
  the full build.
- When adding an exercise dependency, document why it is needed and how
  participants install it.
- Avoid adding a large framework for one short demonstration.

Prefer one clear environment and setup path. Do not rely on undocumented global
packages, machine-local files, or credentials.


## Publication and generated output

The source repository does not track rendered HTML.

- `scripts/build_training_site.sh` assembles the complete site in `_site/`.
- `_site/`, `.quarto/`, `_freeze/`, and notebook checkpoints remain ignored.
- Do not manually edit generated output.
- Do not add a workflow that commits generated HTML back to `main`.
- Pull requests build the complete artifact without deploying.
- Pushes to `main` upload and deploy the artifact through GitHub Pages.

The complete build must produce:

- `_site/index.html`;
- `_site/learning-modules/index.html`;
- `_site/notebooks/01-opening-experiment.html`;
- `_site/notebooks/01-opening-experiment.ipynb`;
- `_site/slides/trustworthy-numerical-computing.html`.

Keep build logic in `scripts/build_training_site.sh`; the workflow should call
the documented local command rather than duplicate it.


## Validation by change type

For any source or configuration change, first run:

```bash
git diff --check
```

For landing-page, learning-module, or navigation changes:

```bash
quarto render
```

For slide changes:

```bash
quarto render slides-source/trustworthy-numerical-computing.qmd --to revealjs
```

For cross-cutting curriculum, landing-page, dependency, build, or publication
changes:

```bash
scripts/build_training_site.sh
```

For examples and exercises:

- run the exact documented command;
- verify the intended numerical behaviour;
- compare against the stated reference or invariant;
- check both the expected case and at least one revealing edge case;
- run the full publication build when paths or commands appear in modules or
  slides.

For notebook changes:

- run the authoritative `.qmd` source from a clean kernel through the complete
  publication build;
- confirm that Quarto generates both HTML and a runnable `.ipynb` under
  `_site/notebooks/`;
- inspect the generated notebook for expected outputs, execution order,
  machine-local paths, and unnecessary metadata;
- confirm that no generated `.ipynb` remains under the tracked `notebooks/`
  source directory.

For build or workflow changes:

- run `bash -n scripts/build_training_site.sh`;
- run the complete local build;
- validate workflow YAML with `actionlint` when it is available;
- confirm deployment permissions remain isolated from the build job.

After renaming a file, module, example, command, or concept, search all teaching
surfaces with `rg` and verify every reference.


## Repository hygiene

- Preserve existing user changes and avoid unrelated formatting churn.
- Use `git mv` for tracked moves and renames.
- Do not force a package-style `src/` layout onto the training repository.
- Do not commit `_site/`, generated `.ipynb` files, local Quarto state, notebook
  checkpoints, caches, or transient experiment output.
- Keep small input data close to the example that consumes it.
- Keep large or regenerated scientific data out of Git unless it is an
  intentional teaching asset with documented provenance.
- Keep participant-facing navigation simple: landing page, learning modules,
  slides, examples, exercises, and setup.
