# Interactive notebooks

This directory contains the authoritative Quarto sources for self-paced
activities that complement the long-form learning modules. The complete build
executes each tracked `.qmd` file and generates both course HTML and a runnable
Jupyter `.ipynb` file under `_site/notebooks/`.

Activities in this directory are tutorial sources:

- keep them small enough to execute from a clean kernel in CI;
- use explicit parameters and deterministic inputs;
- avoid hidden state and machine-local paths;
- move reusable numerical logic to `source-code/` once more than one activity
  needs it;
- document any dependency in both `requirements-notebooks.txt` and
  `environment.yml`.

Do not edit or commit generated `.ipynb` files. Published HTML and Jupyter
notebooks are generated during the Quarto build and remain untracked. Add an
**Open in Colab** link only after the generated notebook is available at a URL
the intended learners can access.


## Activities

1. [Opening experiment: two plausible variances](01-opening-experiment.qmd)
   uses an exact reference and shift invariance to investigate two conflicting
   variance calculations.
2. [Floating-point landmarks](02-floating-point-landmarks.qmd) maps
   representable spacing, exceptional values, and evaluation-order effects,
   then uses that model to explain the opening variance discrepancy.
3. [Comparison criteria across scales](03-comparison-criteria.qmd) compares
   absolute, relative, and mixed criteria near zero and across several scales,
   then contrasts maximum and root-mean-square collection errors.
4. [Sensitivity, stability, and residuals](04-sensitivity-stability-residuals.qmd)
   separates problem conditioning from algorithmic behaviour and demonstrates
   why a small residual need not imply a small forward error.
5. [Failure-mode laboratory](05-failure-mode-lab.qmd) diagnoses cancellation,
   reduction-order error, overflowing norm intermediates, underflowing products,
   and log-domain comparisons using references and invariants.
6. [Convergence and stopping diagnostics](06-convergence-and-stopping.qmd)
   compares mixed residual and update criteria, classifies several termination
   reasons, and uses a tolerance study to expose an attainable binary64 floor.
7. [Validation evidence portfolio](07-validation-evidence.qmd) uses exact
   cases, properties, refinement rates, convexity bounds, and an independently
   bounded series to test distinct claims about one quadrature calculation.
