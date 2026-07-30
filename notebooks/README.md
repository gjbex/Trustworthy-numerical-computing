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
