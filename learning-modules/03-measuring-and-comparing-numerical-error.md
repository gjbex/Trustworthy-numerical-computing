# Module 3: Measuring And Comparing Numerical Error

## Motivation

Module 2 explained why finite-precision computations can disagree. That still
leaves a decision: is the discrepancy small enough for the intended scientific
use?

In the opening variance experiment, $22.0\ \mathrm{ns}^2$ differs from the exact
reference $22.5\ \mathrm{ns}^2$ by $0.5\ \mathrm{ns}^2$, or about $2.2\%$ of
the reference. Neither number alone tells us whether the discrepancy is
acceptable. Its significance comes from the monitoring rule: the two values
fall on opposite sides of $22.25\ \mathrm{ns}^2$ and therefore lead to different
decisions.

A numerical comparison is meaningful only when its reference, scale, units,
and purpose are clear. This module turns “the results are close” into a claim
that another person can inspect and challenge.


## Learning outcomes

After this module, you should be able to:

* identify what kind of reference supports a numerical comparison;
* compute and interpret absolute and relative error;
* choose a mixed tolerance for values that may approach zero or span several
  scales;
* explain why machine epsilon is not a universal validation tolerance;
* distinguish numerical error or discrepancy from measurement uncertainty,
  modelling error, discretization error, and ordinary variability;
* select component-wise, maximum, root-mean-square, or derived-quantity
  comparisons according to the scientific requirement;
* document the rationale and limitations of a numerical acceptance criterion.


## Connection to Module 2

[Module 2](02-understanding-floating-point-arithmetic.md) introduced local
spacing, rounding, and exceptional values. Those concepts explain why a
computed value can differ from its mathematical counterpart. They do not
provide an acceptable-error threshold.

For example, machine epsilon describes binary64 spacing near one. A physical
measurement may be uncertain by far more than that, while a sensitive
downstream decision may require accuracy much tighter than a convenient
software default. The required comparison must come from the quantity and its
use, not solely from the floating-point format.


## Name the reference before naming the error

Let $\hat{x}$ denote a computed approximation and let $x_\mathrm{ref}$ denote
the value used as its reference. Calling their difference an *error* can imply
that $x_\mathrm{ref}$ is the truth. That implication is justified only when the
reference is sufficiently well established.

| Reference | What supports it | Appropriate claim |
|---|---|---|
| Exact value | Analytic result or exact arithmetic for the stated inputs | The difference can be called numerical error relative to the exact result. |
| High-accuracy numerical reference | More accurate arithmetic or refinement whose own formulation and convergence were checked | The difference estimates error to the quality justified for the reference. |
| Trusted benchmark | A documented, validated result for a standard case | The computation agrees or disagrees with the benchmark under stated conditions. |
| Independent estimate | A method with sufficiently different assumptions or failure modes | Agreement is complementary evidence, not proof that either estimate is exact. |
| Expected range | Physical bounds, prior observations, or expert knowledge | The result is consistent or inconsistent with the range; no pointwise error is available. |

When the reference is not exact, **discrepancy** is often the more honest word.
Record the reference's provenance, units, assumptions, and known limitations
alongside the comparison. More digits do not make a reference authoritative.


## Absolute error retains the units

For a scalar quantity, the absolute error relative to the reference is

$$
E_\mathrm{abs} = |\hat{x} - x_\mathrm{ref}|.
$$

$E_\mathrm{abs}$ has the same units as the quantity. If a computed pressure is
$100.4\ \mathrm{Pa}$ and the exact reference is $100.0\ \mathrm{Pa}$, the
absolute error is $0.4\ \mathrm{Pa}$. This directly answers a requirement such
as “the pressure must be within $0.5\ \mathrm{Pa}$.”

Absolute error is easy to interpret near zero. Its limitation is scale: an
error of $0.4\ \mathrm{Pa}$ may be negligible relative to a megapascal value
but unacceptable for a pressure perturbation of $0.1\ \mathrm{Pa}$.


## Relative error compares with a scale

When the reference is nonzero, relative error is

$$
E_\mathrm{rel} =
\frac{|\hat{x} - x_\mathrm{ref}|}{|x_\mathrm{ref}|}.
$$

Relative error is dimensionless. Multiplying it by 100 expresses the
discrepancy as a percentage of the reference magnitude. It is useful when a
roughly constant fractional accuracy is required across several scales.

Relative error is undefined when $x_\mathrm{ref}=0$. It also becomes difficult
to interpret near zero: dividing a small absolute discrepancy by an even
smaller reference can produce a very large relative value although both
quantities are below a meaningful physical resolution. Replacing the zero
denominator with an arbitrary epsilon hides the choice of scale rather than
justifying it.


## Before the companion experiment

The [comparison criteria across scales](../notebooks/03-comparison-criteria.qmd)
notebook uses four constructed pressure values to isolate how each criterion
behaves. The listed binary64 values are designated as the references for the
exercise; they are not measurements or claims about exact decimal conversion.
The stated requirement is:

> Accept a computed pressure when its discrepancy is no greater than an
> absolute allowance of $10^{-5}\ \mathrm{Pa}$ plus a relative allowance of
> $10^{-6}$ times the reference magnitude.

Before running the notebook, predict which criterion will be useful:

1. when the exact reference is zero;
2. near zero, where the absolute allowance represents a meaningful floor;
3. near $10^6\ \mathrm{Pa}$, where a small relative discrepancy may be much
   larger than the absolute allowance;
4. for detecting one unacceptable point in a collection.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/03-comparison-criteria.qmd
```

The complete site build also generates a downloadable Jupyter notebook.


## A mixed criterion covers two regimes

A common reference-anchored acceptance criterion is

$$
|\hat{x} - x_\mathrm{ref}|
\leq a + r|x_\mathrm{ref}|,
$$

where:

* $a\geq0$ is the **absolute tolerance**, with the same units as $x$;
* $r\geq0$ is the dimensionless **relative tolerance**;
* the right-hand side is the allowed discrepancy at the scale of the
  reference.

Near zero, the absolute term $a$ dominates. At large reference magnitudes, the
relative term $r|x_\mathrm{ref}|$ dominates. The transition is explicit rather
than hidden in a special case.

The notebook uses $a=10^{-5}\ \mathrm{Pa}$ and $r=10^{-6}$. Its constructed
cases produce the following decisions:

| Case | Reference | Absolute-only | Relative-only | Mixed |
|---|---:|---|---|---|
| Zero | $0\ \mathrm{Pa}$ | Pass | Undefined | Pass |
| Near zero | $10^{-6}\ \mathrm{Pa}$ | Pass | Fail | Pass |
| Order one | $1\ \mathrm{Pa}$ | Fail | Fail | Fail |
| Large | $10^6\ \mathrm{Pa}$ | Fail | Pass | Pass |

No criterion is universally superior. Each outcome follows from a different
question. The mixed criterion is appropriate here because the requirement
explicitly contains both an absolute floor and a fractional allowance.

This criterion is directional: $x_\mathrm{ref}$ defines the scale. That is
appropriate when one value is a justified reference. When neither value is
privileged, a symmetric scale such as the larger magnitude may be more suitable,
but the convention must be stated rather than silently changed.


## A tolerance is a requirement, not a repair

A tolerance determines which discrepancies a comparison will accept. It does
not improve a calculation, correct an inaccurate reference, or explain the
source of a discrepancy.

A defensible tolerance rationale should answer:

1. Which quantity is being compared, and in which units?
2. What reference supports the comparison?
3. What absolute scale remains meaningful near zero?
4. What fractional accuracy is required away from zero?
5. Which scientific or engineering decision depends on passing?
6. How should `NaN`, infinity, and missing results be handled?
7. Which boundary and failure cases demonstrate that the criterion detects the
   problems it is meant to detect?

Sources for a tolerance may include instrument resolution, input uncertainty,
model or discretization requirements, a downstream decision threshold, or a
validated algorithmic accuracy target. These sources should not be combined by
guesswork: their relationships and assumptions determine whether they add,
compete, or require separate checks.

Choose and document the tolerance before inspecting the result whenever
possible. Widening a tolerance only after a test fails changes the claim being
tested and requires a new rationale.


## Why machine epsilon is not a tolerance policy

For binary64, machine epsilon is approximately $2.22\times10^{-16}$: the gap
between 1 and the next larger representable value. It describes one property of
the format at one scale.

It does not encode:

* the units of the result;
* the magnitude of the reference away from one;
* measurement, modelling, or discretization limitations;
* the number and order of operations;
* the accuracy needed by the scientific decision.

Multiplying machine epsilon by an unexplained large constant does not supply
the missing rationale. Format information can help predict a lower-level
rounding effect, but the acceptance criterion must reflect the numerical and
scientific claim.


## Treat non-finite values deliberately

`NaN` and infinity should not pass an ordinary finite-result comparison by
accident. A robust comparison first states whether finite values are required
and classifies both operands.

For most calculations in this course, the default policy is:

* reject `NaN` because it does not represent an ordered numerical result;
* reject infinity unless infinity is an explicitly expected mathematical
  outcome;
* compare signed zeros according to the scientific quantity—usually as equal,
  but with a separate sign check when direction at zero matters.

The policy belongs in the numerical specification. Relying on the incidental
truth value of an expression involving `NaN` makes the intent difficult to
review.


## Error, uncertainty, and variability are different

Several quantities can explain a mismatch between computation and observation.
They should be named separately.

| Quantity | Question it answers | Example |
|---|---|---|
| Numerical error or discrepancy | How far is the computed approximation from the stated mathematical reference? | Difference between a floating-point result and an exact rational value. |
| Measurement uncertainty | How well is the physical input or observed quantity known? | Sensor calibration and finite timestamp resolution. |
| Modelling error | How well does the mathematical model represent the physical system? | A model omits a process that changes the measured response. |
| Discretization error | How much does replacing a continuous problem by a finite approximation affect the result? | A time step or spatial grid is too coarse. |
| Ordinary variability | How much does the quantity vary across repetitions, samples, or stochastic realizations? | Repeated experimental runs have a distribution of outcomes. |

A computed result can have tiny numerical error while the physical conclusion
remains uncertain, or it can have noticeable numerical error while remaining
irrelevant beside natural variability. A numerical tolerance should not be
presented as a complete uncertainty model.


## Comparing collections requires a scientific target

For reference values $x_i$ and approximations $\hat{x}_i$, define component
errors $e_i=\hat{x}_i-x_i$. Several summaries are useful:

* **Component-wise comparison:** apply a scalar criterion to every $i$. This
  locates failures and enforces a per-component requirement.
* **Maximum absolute error:**
  $E_\max=\max_i|e_i|$. It has the quantity's units and exposes the worst
  component.
* **Root-mean-square error:**
  $E_\mathrm{RMS}=\sqrt{\frac{1}{n}\sum_i e_i^2}$. It has the quantity's units
  and describes a typical error scale, but one local failure can be diluted by
  many accurate components.
* **Derived-quantity comparison:** compare the observable that drives the
  scientific conclusion, such as a total flux, peak value, event time, or
  threshold crossing.

Suppose nine pressure errors are $0.1\ \mathrm{Pa}$ and one is
$1.0\ \mathrm{Pa}$. The root-mean-square error is approximately
$0.33\ \mathrm{Pa}$, while the maximum error is $1.0\ \mathrm{Pa}$. An RMS
requirement of $0.5\ \mathrm{Pa}$ passes; a requirement that every point be
within $0.5\ \mathrm{Pa}$ fails. Neither summary is intrinsically correct—the
scientific requirement determines which claim matters.

Report an aggregate together with enough local information to expose failures
that the aggregate can hide. For heterogeneous quantities or units, do not
combine raw component errors into one norm without a documented scaling.


## A comparison workflow

Use the following sequence when defining a numerical check:

1. State the quantity, units, reference, and decision.
2. Decide whether “error,” “discrepancy,” consistency with a range, or another
   relationship is the justified claim.
3. Choose a metric that reflects the relevant scale and spatial or temporal
   structure.
4. Derive absolute and relative tolerances from stated requirements.
5. Define policies for zero, boundaries, `NaN`, and infinity.
6. Test representative passes, intended failures, near-zero cases, large-scale
   cases, and values exactly on the boundary.
7. Record the criterion, rationale, observed result, and limitations together.

Passing such a comparison supports one specific claim: agreement with the
stated reference under the stated metric and tolerance. It does not prove that
the model is suitable, that the reference is exact, or that the algorithm is
stable.


## Questions to ask about a comparison

* Is the reference exact, approximate, independent, or only an expected range?
* Are the units and scaling conventions explicit?
* What happens when the reference is zero or close to zero?
* Is the criterion anchored to a reference or symmetric between two results?
* Which requirement justifies each tolerance term?
* Are non-finite values handled intentionally?
* Could an aggregate metric hide a consequential local error?
* Does passing preserve the scientific conclusion that actually matters?


## Reflection questions

1. Why is “difference from a benchmark” sometimes more accurate wording than
   “error”?
2. What are the units of absolute error, relative error, absolute tolerance,
   and relative tolerance?
3. Why is relative error unsuitable when the reference is zero?
4. In the pressure experiment, why does the near-zero case fail the
   relative-only criterion but pass the mixed criterion?
5. Why does the large-pressure case fail the absolute-only criterion but pass
   the relative and mixed criteria?
6. When would maximum error be more relevant than root-mean-square error?
7. What does a passed tolerance check leave unproven?

::: {.callout-note collapse="true"}
## Suggested answers

1. A benchmark may itself be approximate or valid only under particular
   assumptions. The observed difference is known; the true error may not be.
2. Absolute error and absolute tolerance have the quantity's units. Relative
   error and relative tolerance are dimensionless.
3. Its denominator is zero. Near zero, the denominator can also make a small
   absolute discrepancy appear arbitrarily large.
4. The $5\times10^{-6}\ \mathrm{Pa}$ discrepancy is below the stated absolute
   floor, while dividing by the $10^{-6}\ \mathrm{Pa}$ reference gives a large
   relative value. The mixed requirement explicitly treats the absolute floor
   as meaningful there.
5. The $0.5\ \mathrm{Pa}$ discrepancy exceeds $10^{-5}\ \mathrm{Pa}$, but it is
   only $5\times10^{-7}$ of the $10^6\ \mathrm{Pa}$ reference and is below the
   stated one-part-per-million allowance.
6. Maximum error is appropriate when every component must satisfy a bound or a
   single local failure is consequential. RMS error is appropriate when a
   typical squared-error scale matches the claim.
7. It does not prove that the reference, model, algorithm, implementation, or
   tolerance rationale is valid beyond the stated comparison.
:::


## Takeaways

* Identify and qualify the reference before calling a discrepancy an error.
* Absolute error preserves units; relative error expresses scale but is
  undefined at zero; a justified mixed criterion can cover both regimes.
* Tolerances encode numerical and scientific requirements. Machine epsilon and
  convenient library defaults do not supply those requirements.
* Collection metrics answer different questions, so choose the metric that
  matches the consequential local or aggregate behaviour.
* A comparison result is only as strong as its reference, metric, tolerance
  rationale, and stated limitations.


## Connection to the next module

Error measures describe the size and structure of a discrepancy; they do not
identify its cause.
[Module 4: Conditioning And Numerical Stability](04-conditioning-and-numerical-stability.md)
separates sensitivity inherent in the mathematical problem from error
introduced by an algorithm or implementation.
