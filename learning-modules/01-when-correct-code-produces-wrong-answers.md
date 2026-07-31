# Module 1: When Correct Code Produces Wrong Answers

## Motivation

<!-- TODO: Add a concrete scientific example showing the consequences of a plausible but unreliable numerical result. -->

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

<!-- TODO: Explain the distinct layers of correctness and how success at one layer does not guarantee success at the next. -->

The opening case study will contrast several increasingly demanding questions:

1. Does the program run?
2. Does it implement the intended algorithm?
3. Is the algorithm appropriate for the mathematical problem?
4. Is the result accurate enough for the scientific conclusion?
5. What evidence supports that conclusion?


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

<!-- TODO: Interpret the observations and explain why the discrepancy is scientifically consequential. -->

The two algebraically equivalent implementations return
$22.5\ \mathrm{ns}^2$ and $22.0\ \mathrm{ns}^2$. Both programs run normally and
both answers initially look plausible, but they lead to opposite decisions.


## Evaluating the evidence

<!-- TODO: Explain what each check contributes, distinguish independent evidence from agreement, and state the limitations of the experiment. -->

The investigation uses several kinds of evidence:

1. comparison with an exact rational reference;
2. the invariant that variance is unchanged by a common offset;
3. controlled variation of only that offset;
4. a recorded conclusion and the limits of the available evidence.

The activity deliberately establishes *which* result is defensible before
explaining *why* the arithmetic differs.


## Sources of discrepancy

<!-- TODO: Explain each category with a short example and a diagnostic question, including how the categories can interact. -->

The module introduces four categories that recur throughout the course:

* input and measurement uncertainty;
* modelling and discretization error;
* algorithmic and finite-precision error;
* implementation defects.

Separating these categories prevents a compiler, test suite, or high-precision
output format from being mistaken for complete validation.


## Investigation workflow

<!-- TODO: Explain each step and map it to the opening experiment without introducing the formal concepts reserved for later modules. -->

Participants will use the following workflow in later modules:

1. State the expected behaviour and the decision that depends on the result.
2. Reproduce and characterize the discrepancy.
3. Establish a reference or independent check.
4. Judge whether the discrepancy matters for the intended conclusion.
5. Consider competing explanations and likely failure modes.
6. Change one factor at a time.
7. Record what the evidence supports and which limitations remain.


## Questions to ask of any numerical result

<!-- TODO: Add a concise, reusable checklist covering meaning, units, scale, assumptions, invariants, reference cases, and scientific consequences. -->


## Reflection questions

<!-- TODO: Add questions that test whether learners can interpret the experiment and distinguish plausible output from validated evidence. -->


## Takeaways

<!-- TODO: Summarize the module in three concise conclusions about layers of correctness, numerical evidence, and systematic investigation. -->


## Connection to the next module

The workflow requires a model of how arithmetic behaves on a computer. Module 2
develops that finite-precision model.
