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
values, overflow, and underflow. A comparison of binary16, bfloat16, binary32,
and binary64 makes the trade-off between significand precision and exponent
range explicit without requiring learners to memorize encodings.

### Module 3: Measuring And Comparing Numerical Error

Turns the arithmetic model into practical error measures and defensible
tolerances. This module comes before stability because later discussions need a
precise language for comparing results.


## Part II: Diagnosis And Control

### Module 4: Conditioning And Numerical Stability

Separates sensitivity inherent in the mathematical problem from error
introduced by the selected algorithm and its implementation. It then combines
local sensitivity with deterministic input bounds or covariance-based standard
uncertainties, including the limits of first-order propagation.

### Module 5: Common Numerical Failure Modes

Applies the previous distinctions to cancellation, accumulation, scaling,
overflow, underflow, and order-dependent arithmetic. A companion laboratory
compares specialized functions, reduction algorithms, scaled norms, regrouped
products, and log-domain calculations against references and invariants.

### Module 6: Iterative Algorithms And Convergence

Extends error reasoning to algorithms that produce a sequence of approximations.
Participants distinguish error, residual, update size, stagnation, divergence,
and false convergence. A companion activity compares mixed stopping criteria,
classifies controlled relaxation runs, and uses Newton's method to identify an
attainable binary64 accuracy floor.


## Part III: Evidence And Reproducibility

### Module 7: Validating Scientific Computations

Combines reference cases, invariants, properties, refinement studies, and
independent methods into a validation strategy. A companion activity diagnoses
a suspicious quadrature implementation by combining exact cases, observed
orders, convexity bounds, and an independently bounded series.

### Module 8: Reproducibility Across Computing Environments

Defines bitwise, numerical, statistical, and conclusion-level reproducibility
contracts, then examines which differences are expected when compilers,
libraries, hardware, precision, optimization settings, or parallel execution
order change. A companion activity contrasts harmless low-order variation with
a cancellation-sensitive energy balance whose conclusion depends on reduction
order, partition, and accumulator precision. Learners record input, operation,
accumulator, and output formats separately rather than treating a datatype name
as a complete mixed-precision execution policy.


## Part IV: Scientific Judgment

### Module 9: Communicating Numerical Reliability

Shows how to report tolerance choices, convergence evidence, deterministic input
ranges, environmental variability, supported digits, and remaining limitations
without overstating confidence. A companion activity turns a structured
heating-energy evidence record into a concise reliability statement while
keeping numerical error, input range, and unvalidated model assumptions
distinct.

### Module 10: Capstone Investigation

Participants investigate a two-component sensor calculation whose nominal
threshold decision changes between binary32 and binary64. They establish an
exact-decimal nominal reference, distinguish response residual from
concentration error, diagnose an ill-conditioned component split with
controlled sensor-separation cases, propagate deterministic reading bounds,
and improve arithmetic and decision logic separately. The capstone ends with a
validated `indeterminate` component decision, a tightly bounded total, and a
qualified reliability statement.


## Reference material

[Vectors, Norms, And Scaling](reference-vectors-norms-and-scaling.md) is a
just-in-time reference for the vector summaries introduced in Module 3 and the
norm notation used from Module 4 onward. It is not an additional prerequisite
module and does not change the core sequence.


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
