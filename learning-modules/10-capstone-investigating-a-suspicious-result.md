# Module 10: Capstone—Investigating A Suspicious Result

The capstone combines the complete course workflow. Participants receive a
calculation that runs successfully and produces plausible output, but changes
unexpectedly under a controlled variation.


## Learning outcomes

After this module, you should be able to:

* plan a numerical investigation before changing the implementation;
* isolate the dominant source of discrepancy;
* select and justify a more reliable formulation;
* assemble complementary validation evidence;
* communicate the improved result and its limitations.


## The case

The case should be small enough to investigate during the session while still
including several plausible explanations. Suitable domains include reduction,
root finding, fitting, time integration, or a small linear system.

Participants receive:

* the scientific question and required accuracy;
* a baseline implementation;
* representative inputs;
* one suspicious symptom;
* a template for recording evidence.


## Investigation stages

### 1. Reproduce and characterize

Run the baseline, vary one relevant factor, and describe the discrepancy using
an appropriate error measure.

### 2. Establish a reference

Use an analytical case, higher precision, an independent method, an invariant,
or a refinement trend to create a meaningful comparison.

### 3. Diagnose

Assess conditioning and identify whether the dominant issue is arithmetic,
algorithmic, implementation-related, environmental, or a limitation of the
inputs or model.

### 4. Improve

Reformulate the computation, select a more stable method, rescale the problem,
or revise the stopping criterion. Change one factor at a time.

### 5. Validate

Repeat the original comparison and add at least one independent check. Confirm
that the improvement holds for more than one convenient input.

### 6. Report

Write a concise numerical reliability statement containing the claim,
validation evidence, observed error, assumptions, and remaining limitations.


## Completion criteria

A successful capstone does not require a bitwise-identical result. It requires a
well-supported conclusion about which variation is acceptable, which is not,
and why.


## Connection beyond the core modules

This capstone completes the ten-module core sequence. The
[optional advanced topics](optional-advanced-topics.md) extend the same
investigation workflow to mixed precision, interval arithmetic, numerical
linear algebra, stochastic algorithms, and accelerator or distributed
computing.
