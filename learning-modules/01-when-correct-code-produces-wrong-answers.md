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
6. change one factor at a time.
7. record the evidence and remaining limitations.


## Opening experiment

The first experiment should produce two reasonable-looking answers to the same
question. Participants predict which result to trust, then identify what
additional evidence is needed before either answer is defensible.


## Connection to the next module

The workflow requires a model of how arithmetic behaves on a computer. Module 2
develops that finite-precision model.
