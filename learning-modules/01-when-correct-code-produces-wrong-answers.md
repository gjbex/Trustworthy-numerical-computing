# Module 1: When Correct Code Produces Wrong Answers

A program can be free of syntax errors, memory errors, and obvious logic defects
while still producing a scientifically misleading result. This module
introduces numerical reliability as a separate dimension of correctness.


## Learning outcomes

After this module, you should be able to:

* distinguish program execution from numerical and scientific validity;
* identify several sources of discrepancy in a computed result;
* explain why plausible-looking output is weak evidence;
* outline a systematic numerical investigation.


## From executable to trustworthy

The opening case study will contrast several increasingly demanding questions:

1. Does the program run?
2. Does it implement the intended algorithm?
3. Is the algorithm appropriate for the mathematical problem?
4. Is the result accurate enough for the scientific conclusion?
5. What evidence supports that conclusion?


## Sources of discrepancy

The module introduces four categories that recur throughout the course:

* input and measurement uncertainty;
* modelling and discretization error;
* algorithmic and finite-precision error;
* implementation defects.

The categories interact, but separating them prevents a compiler, test suite, or
high-precision output format from being mistaken for complete validation.


## Investigation workflow

Participants will use the following workflow in later modules:

1. State the expected behaviour and required accuracy.
2. Reproduce and characterize the discrepancy.
3. Establish a reference or independent check.
4. Measure error using a scale-appropriate metric.
5. Assess conditioning and likely failure modes.
6. Change one factor at a time.
7. Record the evidence and remaining limitations.


## Opening experiment

The [opening experiment](../notebooks/01-opening-experiment.qmd) asks whether
the population variance of four large-offset event times exceeds a monitoring
threshold. Two algebraically equivalent implementations return
$22.5\ \mathrm{ns}^2$ and $22.0\ \mathrm{ns}^2$. Both programs run normally and
both answers initially look plausible, but they lead to opposite decisions.

Before choosing an answer, participants:

1. predict how the two implementations should behave;
2. compare both results with an exact rational reference;
3. test the invariant that variance is unchanged by a common offset;
4. vary only that offset to characterize the discrepancy;
5. record a conclusion and the limits of the available evidence.

The activity deliberately establishes *which* result is defensible before
explaining *why* the arithmetic differs. Preview the authoritative Quarto
source from the repository root with:

```bash
quarto preview notebooks/01-opening-experiment.qmd
```

The complete site build also generates a downloadable Jupyter notebook.


## Connection to the next module

The workflow requires a model of how arithmetic behaves on a computer. Module 2
develops that finite-precision model.
