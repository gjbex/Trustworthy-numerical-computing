# Module 1: When Correct Code Produces Wrong Answers

## Motivation

A program can be free of syntax errors, memory errors, and obvious logic defects
while still producing a scientifically misleading result. This module
introduces numerical reliability as a separate dimension of correctness.

Consider a sensor whose event times are recorded as nanosecond timestamps. A
monitoring system estimates their variance and flags a measurement run when
that variance exceeds $22.25\ \mathrm{ns}^2$. The calculation completes
normally, produces a plausible value, and may even pass ordinary software
tests. Nevertheless, a small numerical discrepancy near the threshold can
determine whether the run is accepted or flagged for investigation.

In this situation, the important question is not merely whether the program ran
or implemented the requested formula. We must determine whether the computed
value is reliable enough to support the resulting scientific decision---and
what evidence would justify that confidence.


## Learning outcomes

After this module, you should be able to:

* distinguish program execution from numerical and scientific validity;
* identify several sources of discrepancy in a computed result;
* explain why plausible-looking output is weak evidence;
* outline a systematic numerical investigation.


## Starting point

This first module assumes only basic algebra and the ability to run a short
program or notebook. You do not need to know how a computer represents real
numbers. The experiment first establishes that a result deserves scrutiny;
Module 2 will explain the relevant arithmetic mechanism.

For the experiment, the four timestamps are treated as exact input values, and
the population variance and monitoring threshold are treated as given. These
choices isolate the computation. They do not imply that measurement uncertainty
or the suitability of the monitoring rule can be ignored in a real study.


## From executable to trustworthy

Correctness is not a single property. A computation can satisfy one requirement
while failing a more demanding one. It is therefore useful to distinguish five
layers, each associated with a different question:

| Layer | Question | Sensor-monitoring example |
|---|---|---|
| Successful execution | Does the program run to completion? | The program reads the four timestamps and returns a number without an exception. |
| Implementation fidelity | Does the code implement the intended algorithm? | The loops, indexing, units, and operations match the chosen population-variance formula. |
| Mathematical suitability | Does the algorithm answer the intended mathematical question? | Population variance, rather than sample variance or another measure of spread, is the quantity used by the monitoring rule. |
| Numerical adequacy | Is the computed value reliable enough for the decision? | The calculation must retain enough accuracy to determine on which side of $22.25\ \mathrm{ns}^2$ the variance lies. |
| Scientific justification | What evidence supports the conclusion? | A reference calculation, a property the result should satisfy, and an account of the assumptions and limitations support the decision to accept or flag the run. |

Compilers, runtime checks, and ordinary functional tests provide strong evidence
about the first two layers. They do not, by themselves, establish mathematical
suitability, numerical adequacy, or scientific justification. A result can also
fail at more than one layer: for example, a correctly implemented variance may
be computed unreliably, while variance itself may be a poor measure for the
scientific purpose.

The opening experiment concentrates on numerical adequacy and the evidence used
to justify a result. It holds the input values and monitoring rule fixed;
measurement uncertainty and the choice of scientific metric remain important,
but are outside the scope of this first investigation.


## Before the opening experiment

The [opening experiment](../notebooks/01-opening-experiment.qmd) asks whether
the population variance of four large-offset event times exceeds a monitoring
threshold. Before running the calculations, record:

1. whether you expect two algebraically equivalent formulas to agree;
2. what degree of disagreement would concern you;
3. what evidence you would trust when choosing between two answers.


## Opening experiment

Work through the notebook from top to bottom before continuing with the
interpretation below. Preview the authoritative Quarto source from the
repository root with:

```bash
quarto preview notebooks/01-opening-experiment.qmd
```

The complete site build also generates a downloadable Jupyter notebook.


## What the experiment establishes

The two algebraically equivalent implementations return
$22.5\ \mathrm{ns}^2$ and $22.0\ \mathrm{ns}^2$. Both programs run normally and
both answers initially look plausible, but they lead to opposite decisions.

The four timestamps can be written as a common offset of
$100{,}000{,}000\ \mathrm{ns}$ plus the relative event times
$[4, 7, 13, 16]\ \mathrm{ns}$. Their exact population variance is
$45/2 = 22.5\ \mathrm{ns}^2$. The centered implementation therefore agrees with
the exact reference and flags the run. The shortcut implementation returns
$22.0\ \mathrm{ns}^2$ and accepts it. The discrepancy is
$0.5\ \mathrm{ns}^2$; more importantly, the two results lie on opposite sides
of the $22.25\ \mathrm{ns}^2$ decision threshold.

| Calculation | Result | Monitoring decision |
|---|---:|---|
| Exact rational reference | $22.5\ \mathrm{ns}^2$ | Flag |
| Centered formula | $22.5\ \mathrm{ns}^2$ | Flag |
| Shortcut formula | $22.0\ \mathrm{ns}^2$ | Accept |

The experiment also changes the common offset while keeping those relative
event times fixed. The spread of the resulting timestamps has not changed, so
their variance should remain $22.5\ \mathrm{ns}^2$. The centered calculation
preserves that behaviour for the tested offsets. The shortcut calculation
changes as the offset grows and eventually returns zero or values larger than
the entire spread would suggest.

This is enough to reject the shortcut calculation for the monitoring decision.
It is not yet an explanation of why the two formulas behave differently on a
computer.


## Evaluating the evidence

Plausibility is a useful prompt for investigation, but it is weak evidence. Both
candidate results are non-negative, have the expected units, and are of a
reasonable magnitude. Those observations would detect a negative variance or
a unit conversion that was wrong by many orders of magnitude, but they cannot
distinguish $22.5\ \mathrm{ns}^2$ from $22.0\ \mathrm{ns}^2$.

The notebook therefore combines checks with different strengths:

| Evidence | What it establishes | Limitation |
|---|---|---|
| Exact rational reference | The mathematical result for these exact, integer-valued inputs is $22.5\ \mathrm{ns}^2$. | Exact arithmetic may be impractical for larger problems, and the reference code and problem definition must still be correct. |
| Shift invariance | Adding a common offset should not alter variance; violating this property disproves expected behaviour without requiring a new reference value for every offset. | Passing the tested property would not prove correct behaviour for every possible input. |
| Controlled offset sweep | Changing only the offset associates the discrepancy with the scale of the timestamps rather than their spread. | It explores a finite set of constructed inputs and does not by itself identify the arithmetic mechanism. |
| Decision threshold | The discrepancy changes the monitoring conclusion and is therefore consequential in this setting. | A discrepancy of the same size might be irrelevant for a different question or threshold. |

An **invariant** is a property that should remain unchanged under a specified
transformation. Here, adding the same value to every timestamp changes their
location but not their spread. An invariant complements a reference value
because it tests behaviour across a family of related inputs.

Agreement is not automatically independent evidence. Two implementations may
share the same formula, library routine, assumptions, or defect. Confidence is
stronger when checks fail in different ways: the exact reference supplies a
known result, while shift invariance tests a mathematical property.

The evidence supports a limited claim: for these exact inputs and the tested
offsets, the centered calculation is defensible for the stated threshold and
the shortcut calculation is not. It does not assess timestamp uncertainty,
justify variance as the best monitoring statistic, or prove that the centered
implementation is reliable for every dataset.


## Sources of discrepancy

When a result is surprising, several explanations are possible. Separating
them helps prevent the first plausible explanation from becoming the conclusion.

| Source | Example | Diagnostic question |
|---|---|---|
| Input and measurement uncertainty | The sensor may have limited time resolution, a calibration offset, or incorrectly labelled units. | Would recalibration, repeated measurement, or corrected metadata change the input values materially? |
| Modelling and discretization | Population variance may not capture the aspect of sensor behaviour that matters; in a simulation, a grid or time step may be too coarse. | Would a different justified model, statistic, or finer approximation change the conclusion? |
| Algorithm and finite-precision arithmetic | Two algebraically equivalent formulas may behave differently when evaluated with a finite set of computer numbers. | Does a reformulation, arithmetic format, or evaluation order change the observed result? |
| Implementation defects | The code may use the wrong divisor, mix units, omit a value, or implement a different formula than intended. | Does the implementation match the specification on small cases with known answers? |

These categories can interact. A program may contain a unit defect while also
using an unreliable calculation, or it may compute a chosen statistic
accurately even though that statistic is unsuitable for the scientific
question. A compiler, test suite, or output with many digits can provide useful
evidence about particular categories, but none validates all of them at once.


## Investigation workflow

The course will repeatedly use the following workflow. It is a disciplined way
to move from suspicion to a qualified conclusion without deciding on the cause
too early.

| Step | Question | Opening experiment |
|---|---|---|
| 1. State the expected behaviour and decision | What should remain true, and what conclusion depends on the result? | Variance should describe the spread, and values above $22.25\ \mathrm{ns}^2$ flag the run. |
| 2. Reproduce and characterize the discrepancy | Can it be repeated, and under which inputs does it appear? | Both formulas are run on the same four timestamps and give different decisions. |
| 3. Establish a reference or independent check | Is there a known result, simpler case, invariant, or other justified comparison? | Exact rational arithmetic supplies a reference, and shift invariance supplies a property check. |
| 4. Judge whether the discrepancy matters | Does it change the quantity or scientific conclusion that matters? | The results fall on opposite sides of the monitoring threshold. |
| 5. Consider competing explanations | Could the inputs, problem definition, algorithm, arithmetic, or implementation be responsible? | The experiment fixes the inputs and definition, then compares implementations and expected behaviour. |
| 6. Change one factor at a time | Which controlled variation reveals when the discrepancy changes? | Only the common offset is varied while the relative event times remain fixed. |
| 7. Record the supported claim and limitations | What can be concluded, under which assumptions, and what remains unknown? | The reliability statement identifies the defensible result, supporting checks, decision context, and excluded questions. |

The steps need not occur only once or in a rigid order. A failed invariant may
suggest a new controlled variation; that variation may reveal that the original
reference cases were too narrow. Later modules add more precise tools for
individual steps, but the overall reasoning pattern remains the same.


## Questions to ask of any numerical result

Before accepting a computed result, ask:

* What physical, statistical, or mathematical quantity does the number
  represent?
* Are its units, sign, magnitude, and valid range plausible?
* Which input assumptions, measurement uncertainties, and modelling choices
  affect it?
* What behaviour or properties should the result preserve?
* Is there a small case with an exact answer, a trusted reference, or a
  complementary check?
* Which changes to the inputs or computational method should matter, and which
  should not?
* Is any observed discrepancy large enough to change the intended conclusion?
* What does the available evidence leave untested?


## Reflection questions

1. Which layers of correctness are established merely by observing that both
   variance functions terminate and return ordinary numbers?
2. Why would agreement between two functions not necessarily prove that either
   answer is correct?
3. What does the shift-invariance check establish, and what does it leave
   unexplained?
4. Why is the $0.5\ \mathrm{ns}^2$ discrepancy consequential here? Give a
   situation in which the same discrepancy might not matter.
5. What additional evidence would be needed before using the centered formula
   as a general-purpose variance implementation?

::: {.callout-note collapse="true"}
## Suggested answers

1. Termination and an ordinary numeric result establish successful execution.
   They provide little evidence about the remaining layers without tests tied
   to the specification and scientific question.
2. The functions could share an assumption, formula, library operation, or
   implementation defect. Agreement is strongest when the methods provide
   genuinely complementary evidence.
3. The check shows that the shortcut calculation violates a required
   mathematical property for the tested offsets. It does not explain the
   finite-precision mechanism or prove that the centered calculation works for
   every input.
4. The discrepancy changes whether the run is accepted or flagged because the
   threshold lies between the results. It might not matter if both results led
   to the same decision and the required accuracy justified treating them as
   equivalent.
5. Test more input scales and patterns, compare with justified references, and
   check additional mathematical properties. Real use would also require
   assessment of measurement uncertainty and whether variance is the right
   statistic.
:::


## Takeaways

* A program that runs and implements its specification can still produce a
  numerically inadequate or scientifically unjustified result.
* Plausibility is a preliminary check, not validation. References, invariants,
  controlled variations, and decision context provide stronger and
  complementary evidence.
* A trustworthy conclusion states what was tested, why the discrepancy matters,
  which result the evidence supports, and which limitations remain.


## Connection to the next module

The workflow requires a model of how arithmetic behaves on a computer.
[Module 2: Understanding Floating-Point Arithmetic](02-understanding-floating-point-arithmetic.md)
develops that finite-precision model and explains why the two variance formulas
can produce different results.
