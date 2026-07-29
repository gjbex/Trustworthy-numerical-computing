# Module 3: Measuring And Comparing Numerical Error

A numerical comparison is meaningful only when its scale and purpose are clear.
This module develops the error measures and tolerance choices used throughout
the rest of the course.


## Learning outcomes

After this module, you should be able to:

* compute absolute and relative error;
* choose a mixed tolerance for values that may approach zero;
* distinguish error from uncertainty and ordinary variability;
* explain why a universal epsilon is not a validation policy;
* relate tolerance choices to units and scientific requirements.


## Reference and approximation

Participants distinguish an exact value, a high-quality reference, an
independent estimate, and an expected range. The strength of a claim depends on
which kind of comparison is available.


## Absolute and relative error

Absolute error is expressed in the units of the quantity. Relative error
normalizes by a scale, but becomes unsuitable when the reference is zero or very
small. Mixed criteria combine both ideas:

```text
|computed - reference| <= absolute_tolerance
                       + relative_tolerance * |reference|
```


## Tolerances as requirements

A tolerance should follow from the scientific question, input quality,
discretization, algorithm, and downstream use. It should not be chosen merely
to make an existing test pass.


## Comparisons across collections

The module introduces component-wise, norm-based, and summary comparisons.
Participants consider whether the largest local error, a global norm, or a
derived observable is the relevant quantity.


## Experiment

Participants compare the same set of computed values using absolute-only,
relative-only, and mixed criteria, then identify which choices give misleading
results near zero or across several scales.


## Connection to the next module

Error measures describe a discrepancy. Module 4 asks whether its cause lies in
the mathematical problem, the algorithm, or the implementation.
