# Learning Module Structure

The course progresses from the arithmetic model to complete numerical
investigations. Later modules assume the vocabulary and diagnostic distinctions
introduced earlier.


## Part I: Foundations

### Module 1: When Correct Code Produces Wrong Answers

Introduces numerical validity as a concern distinct from syntax, memory safety,
and ordinary functional correctness. Participants learn the investigation
workflow used throughout the course.

### Module 2: Understanding Floating-Point Arithmetic

Builds the finite-precision model needed to reason about rounding, special
values, overflow, and underflow.

### Module 3: Measuring And Comparing Numerical Error

Turns the arithmetic model into practical error measures and defensible
tolerances. This module comes before stability because later discussions need a
precise language for comparing results.


## Part II: Diagnosis And Control

### Module 4: Conditioning And Numerical Stability

Separates sensitivity inherent in the mathematical problem from error
introduced by the selected algorithm and its implementation.

### Module 5: Common Numerical Failure Modes

Applies the previous distinctions to cancellation, accumulation, scaling,
overflow, underflow, and order-dependent arithmetic.

### Module 6: Iterative Algorithms And Convergence

Extends error reasoning to algorithms that produce a sequence of approximations.
Participants distinguish error, residual, update size, stagnation, divergence,
and false convergence.


## Part III: Evidence And Reproducibility

### Module 7: Validating Scientific Computations

Combines reference cases, invariants, properties, refinement studies, and
independent methods into a validation strategy.

### Module 8: Reproducibility Across Computing Environments

Examines which differences are expected when compilers, libraries, hardware,
optimization settings, or parallel execution order change.


## Part IV: Scientific Judgment

### Module 9: Communicating Numerical Reliability

Shows how to report tolerance choices, convergence evidence, environmental
variability, and remaining limitations without overstating confidence.

### Module 10: Capstone Investigation

Participants apply the full workflow to a suspicious result, improve the
calculation, assemble validation evidence, and write a concise reliability
report.


## Suggested delivery

For a one-day core course:

| Block | Modules | Emphasis |
|---|---|---|
| 1 | 1–3 | Motivation, arithmetic, and error measures |
| 2 | 4–6 | Conditioning, stability, failure modes, and convergence |
| 3 | 7–8 | Validation and reproducibility |
| 4 | 9–10 | Communication and capstone investigation |

For two half-days, finish the first half after Module 5 and begin the second half
with convergence and validation. Optional advanced topics are best taught after
the complete core path rather than inserted before participants have a
validation workflow.
