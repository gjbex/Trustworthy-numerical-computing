---
title: "Trustworthy Numerical Computing"
format:
  html:
    theme: cosmo
    toc: true
---

Trustworthy numerical results require more than code that compiles, runs, and
passes ordinary tests. Scientific software must also account for finite
precision, problem conditioning, algorithmic stability, convergence,
validation, and variability across computing environments.

This training develops a practical workflow for recognizing, investigating,
preventing, and communicating numerical reliability problems. The concepts are
language-agnostic and apply to scientific work in Python, Julia, C, C++,
Fortran, R, MATLAB, Rust, and similar environments.


## Learning outcomes

When you complete this training you will be able to

* explain how floating-point representation and rounding affect computations;
* choose meaningful error measures and numerical tolerances;
* distinguish an ill-conditioned problem from an unstable algorithm or an
  implementation defect;
* recognize common failure modes such as cancellation, overflow, underflow,
  and accumulated rounding error;
* define defensible convergence and stopping criteria;
* validate computations using references, invariants, properties, refinement,
  and independent methods;
* reason about reproducibility across compilers, hardware, optimizations, and
  parallel execution;
* report numerical assumptions, limitations, and validation evidence clearly.


## Learning path

The [learning modules](learning-modules/) are the self-contained reading
material for the course. They follow a progression from the arithmetic model to
diagnosis, validation, reproducibility, and communication.

The [slide deck](slides/trustworthy-numerical-computing.html) supports
instructor-led delivery. It provides teaching prompts, short examples, and
discussion anchors rather than duplicating the complete reading material.


## Suggested schedule

The modules are designed so that the core material can be delivered as a
one-day course or split over two half-days. The exact timing will be refined
when the computational experiments and capstone are complete.

| Course block | Modules |
|---|---|
| Motivation and arithmetic foundations | 1–3 |
| Diagnosing and controlling numerical error | 4–6 |
| Validation and reproducibility | 7–8 |
| Communication and capstone investigation | 9–10 |


## Target audience

This training is for scientists, research software engineers, and technical
programmers who develop, review, or rely on numerical software and want stronger
evidence that a computed result is scientifically defensible.


## Prerequisites

Participants should already be able to read and modify small programs in at
least one scientific-computing language. This course does not teach programming
from scratch.

You should be comfortable with:

* variables, expressions, functions, loops, and arrays;
* basic algebra and scientific notation;
* running a short program or notebook and inspecting its output;
* interpreting tables and simple plots;
* the idea that measurements and models have limited precision.

Prior knowledge of IEEE 754, numerical analysis, parallel programming, or a
specific implementation language is not required.


### Quick self-assessment

You are likely ready if you can:

* implement or recognize a loop that sums a collection of numbers;
* compare the output of two implementations;
* explain why a calculated result should not report more meaningful digits than
  its inputs support;
* run the same calculation with a changed input or resolution;
* describe what evidence would make you trust a scientific result.


### Software and access requirements

The reading material and slides only require a web browser. Hands-on work will
require a Linux-style terminal and the course environment described in
`SETUP.md`. The primary exercise language will be selected while the detailed
experiments are developed.


## Level of the material

For participants with the prerequisite programming background, the planned
material is approximately:

* Introductory: 25%
* Intermediate: 55%
* Advanced: 20%


## Trainer

Geert Jan Bex
