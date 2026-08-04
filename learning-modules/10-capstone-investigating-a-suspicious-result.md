# Module 10: Capstone—Investigating A Suspicious Result

Trustworthy numerical work ends neither with a program that runs nor with one
comparison against a preferred answer. It ends with a claim whose scope matches
the available evidence.

This capstone combines the complete course workflow. A two-component sensor
calculation returns positive concentrations and a small residual, but changing
the storage precision reverses a threshold decision. The investigation must
separate avoidable arithmetic error from sensitivity inherent in the inverse
problem—and then decide whether either nominal answer supports the scientific
claim.


## Learning outcomes

After completing this module, you should be able to:

* state a numerical investigation question with quantities, units, input
  bounds, and a decision-relevant accuracy requirement;
* reproduce and characterize a suspicious result before changing it;
* establish a nominal reference and explain what that reference does not prove;
* use residuals, forward errors, controlled cases, and condition estimates to
  distinguish plausible causes;
* improve arithmetic and decision logic one factor at a time;
* validate the revised calculation with complementary evidence;
* report a useful `indeterminate` result when the evidence cannot support a
  binary decision;
* write a qualified numerical reliability statement.


## Prerequisite connection

The investigation deliberately reuses the complete prerequisite chain:

1. **Numerical validity:** running code and plausible output are insufficient.
2. **Floating point:** binary32 and binary64 store different approximations near
   one.
3. **Error measures:** residual and concentration error are different
   quantities with different units.
4. **Conditioning and stability:** a sensitive problem can amplify small input
   or arithmetic perturbations even when the implementation follows the stated
   equations.
5. **Failure modes:** subtraction of nearly equal readings exposes limited
   precision.
6. **Convergence evidence:** a small diagnostic quantity is meaningful only
   when its relationship to the desired error is justified.
7. **Validation:** exact cases, controlled variations, invariants, and
   independent references provide complementary evidence.
8. **Reproducibility:** a precision-dependent difference matters when it
   changes the scientific conclusion.
9. **Communication:** the final claim must name its evidence and limitations.

The capstone does not require every discrepancy to be eliminated. It requires
the conclusion to reflect what can and cannot be established.


## The scientific case

Two compounds have unknown concentrations $c_A$ and $c_B$, both measured in
$\mathrm{mg/L}$. Two calibrated sensors produce readings $y_1$ and $y_2$ in
normalized response units. The assumed linear response model is

$$
\begin{aligned}
y_1 &= c_A+c_B,\\
y_2 &= c_A+(1+\delta)c_B.
\end{aligned}
$$

The normalized coefficients have units of response per $\mathrm{mg/L}$. The
sensor separation $\delta$ measures how differently the second sensor responds
to compound B. If $\delta$ is small, the two response signatures are nearly
indistinguishable.

For the supplied sample:

| Item | Declared value |
|---|---:|
| First reading $y_1$ | $1.0000000$ response units |
| Second reading $y_2$ | $1.0000004$ response units |
| Sensor separation $\delta$ | $10^{-6}$ |
| Bound on each reading | $\pm5\times10^{-8}$ response units |
| Decision threshold | $c_A>0.61\ \mathrm{mg/L}$ |
| Required absolute accuracy in $c_A$ | $0.01\ \mathrm{mg/L}$ |

The reading bounds are deterministic admissible ranges. No probability model
or coverage interpretation is supplied. The exercise also assumes the linear
response law and calibration; it does not provide physical observations with
which to validate them.


## State the claim before computing

The question is not merely “what values does the solver return?” It is:

> Do the declared sensor model, readings, reading bounds, and numerical method
> support the conclusion that $c_A$ is strictly greater than
> $0.61\ \mathrm{mg/L}$, with a required absolute accuracy of
> $0.01\ \mathrm{mg/L}$?

This wording exposes several ways the claim could fail:

* the program could implement the equations incorrectly;
* finite-precision arithmetic could exceed the numerical accuracy requirement;
* the mathematical inverse problem could be too sensitive to the readings;
* the reading bounds could cross the decision threshold;
* the linear calibration model could be invalid for the sample.

Evidence for one item does not silently resolve the others.


## Begin with predictions

Before running the capstone, predict:

1. whether a response residual below $0.01$ is sufficient evidence for a
   concentration accuracy of $0.01\ \mathrm{mg/L}$;
2. whether binary32 and binary64 should make the same threshold decision;
3. whether $c_A$, $c_B$, or their total is likely to be best determined;
4. which controlled experiment could distinguish poor conditioning from a
   generic solver defect;
5. whether higher precision can remove sensitivity to bounded sensor readings.

Recording these predictions reduces hindsight bias. A useful investigation
tests competing explanations rather than immediately rewriting the code.


## Complete the capstone before the worked debrief

If you are using this module as an exercise, stop here and complete the
[sensor-inversion capstone](../hands-on/10-sensor-inversion/README.md). The
starter provides a runnable suspicious result, focused implementation tasks,
completion checks, and an evidence-record template. Return to the material
below after you have recorded your prediction and attempted the investigation.

```bash
cd hands-on/10-sensor-inversion/starter
python3 capstone.py
python3 -m unittest -v
```

The starter tests intentionally encounter `NotImplementedError` until the
investigation TODOs are completed. The initial baseline and revealing binary32
edge case remain runnable.

::: {.callout-warning}
## Worked solution follows

The remainder of this module reveals the nominal reference, diagnosis,
controlled results, input envelope, and reliability statement. Complete the
hands-on investigation first if you want to preserve its prediction-first
sequence.
:::


## Worked debrief: reproduce the supplied result

The participant starter deliberately stores the readings and response
coefficient in binary32 and rounds each solving operation to binary32. Run it
from the repository root:

```bash
cd hands-on/10-sensor-inversion/starter
python3 capstone.py
```

The supplied result is:

```text
scientific question: is c_A > 0.61 mg/L?
required absolute accuracy: 0.01 mg/L
stored precision: binary32
c_A: 0.625000000 mg/L
c_B: 0.375000000 mg/L
decision: yes
residual infinity norm: 2.500e-08 response units
```

The concentrations are positive, sum to one, and nearly satisfy the nominal
sensor equations. None of these observations yet establishes the required
forward accuracy in $c_A$.


## Do not compare unlike quantities

For an approximate concentration vector $\widehat{c}$, the program reports

$$
\lVert r\rVert_\infty
=\lVert A\widehat{c}-y\rVert_\infty
$$

in normalized response units. The required accuracy concerns

$$
|\widehat{c}_A-c_{A,\mathrm{ref}}|
$$

in $\mathrm{mg/L}$. A statement such as “the residual is below $0.01$” compares
numbers with different meanings and units. A residual becomes evidence about
forward error only through an argument involving the problem, scaling, and
conditioning.

The small residual shows that the binary32 result nearly satisfies the nominal
equations. It does not show that those equations determine the component split
accurately.


## Establish a nominal reference

Subtracting the sensor equations gives

$$
y_2-y_1=\delta c_B,
$$

so

$$
c_B=\frac{y_2-y_1}{\delta},
\qquad
c_A=y_1-c_B.
$$

Interpreting the declared input strings as exact decimal values gives

$$
c_{B,\mathrm{ref}}
=\frac{1.0000004-1.0000000}{10^{-6}}
=0.4\ \mathrm{mg/L},
$$

and therefore

$$
c_{A,\mathrm{ref}}=0.6\ \mathrm{mg/L}.
$$

The reference implementation evaluates this algebra with 50-digit `Decimal`
arithmetic constructed from strings. This is independently useful because its
input conversion and arithmetic differ from the emulated binary32 path.

The reference has a precise scope: it verifies the solution of the declared
nominal algebraic system. It does not make the readings exact measurements or
validate the physical response model.


## Compare precision against the reference

The nominal computations produce:

| Arithmetic | $c_A$ (mg/L) | $c_B$ (mg/L) | Nominal decision |
|---|---:|---:|---|
| Binary32 | $0.625$ | $0.375$ | yes |
| Binary64 | $0.5999999999885$ | $0.4000000000115$ | no |
| Exact-decimal reference | $0.6$ | $0.4$ | no |

The binary32 forward error in $c_A$ is
$0.025\ \mathrm{mg/L}$, larger than the required
$0.01\ \mathrm{mg/L}$. Binary64 differs from the nominal reference by about
$1.15\times10^{-11}\ \mathrm{mg/L}$ and easily passes that arithmetic
requirement.

This establishes that binary32 storage is inadequate for the nominal case. It
does not yet establish that the binary64 threshold decision is supported over
the admissible reading range.


## Diagnose the problem conditioning

Write the system as

$$
A c=y,
\qquad
A=
\begin{bmatrix}
1&1\\
1&1+\delta
\end{bmatrix}.
$$

When $\delta=0$, the sensor rows are identical and the component split cannot
be recovered. A small nonzero $\delta$ makes the system solvable but sensitive.

The squared singular values of $A$ are the eigenvalues of
$A^\mathsf{T}A$. For this matrix,

$$
\operatorname{trace}(A^\mathsf{T}A)=4+2\delta+\delta^2,
\qquad
\det(A^\mathsf{T}A)=\delta^2.
$$

If $\lambda_{\max}$ is the larger eigenvalue, the 2-norm condition number can
be evaluated as

$$
\kappa_2(A)=\frac{\lambda_{\max}}{|\delta|}.
$$

This uses the eigenvalue product instead of forming the smaller eigenvalue by a
subtraction that would itself lose accuracy. At $\delta=10^{-6}$,

$$
\kappa_2(A)\approx4.00\times10^6.
$$

The condition number is a worst-case sensitivity measure, not a prediction that
every input incurs exactly that amplification. Its magnitude nevertheless
warns that small relative perturbations in readings or arithmetic may cause
large relative changes in the recovered component split.


## Use a controlled separation sweep

Keep the known concentrations at
$c_A=0.6\ \mathrm{mg/L}$ and $c_B=0.4\ \mathrm{mg/L}$ while changing
$\delta$. Regenerate $y_2=1+0.4\delta$ for each case.

| $\delta$ | $\kappa_2(A)$ | Binary32 error in $c_A$ (mg/L) |
|---:|---:|---:|
| $10^{-1}$ | $4.21\times10^1$ | $5.01\times10^{-7}$ |
| $10^{-2}$ | $4.02\times10^2$ | $4.79\times10^{-6}$ |
| $10^{-4}$ | $4.00\times10^4$ | $4.77\times10^{-4}$ |
| $10^{-6}$ | $4.00\times10^6$ | $2.50\times10^{-2}$ |

The same implementation is accurate in the well-separated control and degrades
as the signatures become less distinguishable. This is discriminating
evidence: it points to the interaction of conditioning and finite precision,
not a generic algebra or indexing error.

At $\delta=10^{-8}$, the two binary32 response coefficients both store as one.
The program reports that the stored separation is zero rather than dividing by
zero or inventing a component estimate. A categorical failure state is more
trustworthy than a plausible unsupported number.


## Separate avoidable error from unavoidable sensitivity

Two statements can both be true:

1. storing this nominal system in binary32 introduces avoidable arithmetic
   error and reverses the nominal decision;
2. the inverse problem is inherently sensitive, so more precise arithmetic
   cannot make bounded readings identify the components accurately.

Calling everything “floating-point noise” would hide the conditioning problem.
Calling everything “ill-conditioned” would hide the avoidable binary32 choice.
The evidence must assign each limitation to the correct layer.

The direct binary64 calculation accurately solves the stored nominal system.
This exercise does not claim a formal stability proof for all inputs, but its
reference agreement makes algorithmic error negligible relative to the stated
input sensitivity in this case.


## Propagate the declared reading bounds

Each reading may vary independently by
$\pm5\times10^{-8}$ normalized response units. Because the mapping from
$(y_1,y_2)$ to $(c_A,c_B)$ is linear for fixed nonzero $\delta$, extrema over
the rectangular input range occur at its four corners.

Evaluating those corners with exact-decimal arithmetic gives:

| Quantity | Deterministic range (mg/L) |
|---|---:|
| $c_A$ | $[0.49999995,0.70000005]$ |
| $c_B$ | $[0.30,0.50]$ |
| $c_A+c_B$ | $[0.99999995,1.00000005]$ |

The component range is wide even though the reading range is narrow. By
contrast, the total is tied directly to $y_1$ and remains tightly bounded.
This contrast reveals which scientific quantity the sensors actually
determine well.

The $c_A$ interval crosses $0.61\ \mathrm{mg/L}$. Therefore:

* `yes` is unsupported because some admissible inputs lie below the threshold;
* `no` is unsupported because some admissible inputs lie above the threshold;
* the supported decision is `indeterminate`.

This is a successful scientific result. It identifies the missing information
instead of disguising it with a nominal Boolean answer.


## Improve one factor at a time

### Retain binary64 arithmetic

This removes the avoidable nominal decision reversal and makes arithmetic error
negligible relative to the $0.01\ \mathrm{mg/L}$ requirement for the declared
nominal system.

It does not reduce the condition number or narrow the admissible input range.


### Change the decision contract

Replace a nominal Boolean comparison with an interval classification:

* return `yes` only when the complete range is above the threshold;
* return `no` only when the complete range is at or below it;
* otherwise return `indeterminate`.

This prevents overclaiming. It does not create a more informative measurement.


### Report the well-determined quantity

Report the tightly bounded total concentration separately from the poorly
determined component split. This preserves useful information without silently
answering a different question.

If the individual threshold is essential, the scientific workflow must change:
obtain a sensor with a more distinct response, add an independently informative
measurement, or reduce the reading bounds enough to support the required
decision.


## Assemble complementary validation evidence

No single check should carry the entire conclusion. A compact evidence
portfolio is:

| Check | Expected behaviour | Observation | Supported claim |
|---|---|---|---|
| Exact-decimal nominal case | Recover $(0.6,0.4)$ | Exact recovery | Reference algebra is correct |
| Binary64 comparison | Error below $0.01\ \mathrm{mg/L}$ | $1.15\times10^{-11}$ | Nominal arithmetic is adequate |
| Well-separated control | Binary32 accurate when sensitivity is modest | Error $5.01\times10^{-7}$ | No generic solver defect observed |
| Separation sweep | Error grows as conditioning worsens | Observed trend agrees | Conditioning diagnosis is supported |
| Four input corners | Bound all declared readings | $c_A$ crosses threshold | Boolean decision unsupported |
| Total invariant | $c_A+c_B=y_1$ | Tight total range | Total is well determined |

These checks are complementary but not completely independent. They share the
same linear model and declared calibration. Physical model validation would
require suitable experimental standards or observations over the intended-use
regime.


## Keep an evidence record

A reviewable record should retain:

* the question, units, threshold, and required accuracy;
* nominal values and deterministic input bounds;
* arithmetic variants, source revision, runtime, operating system,
  architecture, and floating-point metadata;
* reference type and construction;
* residual and forward-error metrics with units;
* condition estimate and controlled cases;
* supported decision and failed decision variants;
* assumptions, untested regimes, and model-validation status.

The capstone program emits a structured record, while the participant template
requires an interpretation of each item. A JSON object can preserve evidence;
it cannot decide whether a scientific claim is adequate without its context.


## Write the final reliability statement

A defensible statement is:

> Under the declared linear two-sensor model, the binary64 nominal estimate is
> $c_A=0.600\ \mathrm{mg/L}$ and agrees with the exact-decimal nominal
> reference to $1.15\times10^{-11}\ \mathrm{mg/L}$, below the predeclared
> $0.01\ \mathrm{mg/L}$ accuracy requirement. The emulated binary32 error in
> $c_A$ is $0.025\ \mathrm{mg/L}$, exceeds that requirement, and changes the
> nominal decision from `no` in binary64 to `yes`. However, the matrix 2-norm
> condition number is approximately $4.00\times10^6$, and the deterministic
> sensor-reading bounds imply
> $c_A\in[0.50,0.70]\ \mathrm{mg/L}$, which crosses the strict
> $0.61\ \mathrm{mg/L}$ threshold; the supported decision is therefore
> indeterminate. The total concentration remains in
> $[0.99999995,1.00000005]\ \mathrm{mg/L}$. This evidence does not validate
> the linear sensor model, assign a probability to the input bounds, or
> establish behaviour on untested precision and hardware paths.

The statement makes three different outcomes visible:

* binary64 is adequate for the nominal stored algebra;
* the component-specific scientific decision is unsupported over the input
  range;
* the total concentration remains a supported result under the assumed model.

None needs to be weakened or exaggerated to make the conclusion useful.


## Capstone materials and reference

The participant-facing
[sensor-inversion capstone](../hands-on/10-sensor-inversion/README.md) provides:

* a runnable binary32 baseline;
* six focused TODOs for reference, conditioning, bounds, decision logic, and
  reporting;
* a prediction-first evidence template;
* identical verification checks for the starter and reference solution;
* optional extensions involving representability, measurement requirements,
  additional sensors, and regularization;
* separate reference material and instructor notes.

Use the separate solution only after attempting the starter. Its evidence
record is a comparison target for claims, metrics, assumptions, and
limitations rather than prose that must be reproduced word for word.


## Questions for reviewing a capstone investigation

1. Was the scientific claim stated before the implementation was changed?
2. Are residual and forward error named with their quantities and units?
3. Does the reference test the nominal algebra, the physical model, or both?
4. Which controlled result distinguishes conditioning from a generic solver
   defect?
5. Does each improvement state what limitation remains?
6. Does the validation portfolio contain genuinely complementary checks?
7. Is the threshold decision evaluated over the complete declared input range?
8. Are unsupported claims replaced with explicit failure or `indeterminate`
   states?
9. Does the final statement preserve useful results without hiding
   conclusion-changing limitations?


## Reflection questions

1. Why does the binary32 residual not establish the required accuracy in
   $c_A$?
2. What does the exact-decimal reference establish, and what does it leave
   untested?
3. Why is the well-separated sensor case more discriminating than a second
   near-identical implementation?
4. Which problem does retaining binary64 solve, and which problem does it not
   solve?
5. Why is `indeterminate` more scientifically useful than selecting the
   binary64 nominal decision?
6. Why can the total concentration be reliable while the component split is
   not?
7. What additional evidence would be required to claim that the sensor model is
   physically valid?


::: {.callout-note collapse="true"}
## Suggested answers

1. The residual is in response units, whereas the required error is in
   $\mathrm{mg/L}$. The large condition number permits small response
   perturbations to correspond to large component changes.
2. The reference accurately solves the declared nominal decimal equations. It
   does not remove reading bounds, validate calibration, or prove the physical
   response model.
3. The same code performs accurately when $\delta=0.1$ and progressively worse
   as $\delta$ shrinks. This controlled trend changes sensitivity while
   preserving the known solution, helping isolate the intended cause.
4. Binary64 removes the avoidable nominal arithmetic error and agrees with the
   decimal reference. It does not improve the sensor separation or narrow the
   admissible reading range.
5. The input envelope crosses the threshold, so neither Boolean decision holds
   for every admitted input. `Indeterminate` accurately identifies what new
   measurement evidence is needed.
6. The total is directly constrained by $y_1=c_A+c_B$. The split depends on the
   small difference $(y_2-y_1)/\delta$, which amplifies reading perturbations.
7. Suitable standards or observations must test the linear response and
   calibration over the intended compounds, concentrations, instruments, and
   operating conditions, with a declared model-discrepancy treatment.
:::


## Takeaways

* Reproduce and measure a suspicious result before rewriting it.
* A small residual is not a forward-error guarantee without conditioning and
  scaling information.
* Reference agreement can establish nominal arithmetic accuracy while leaving
  input sensitivity and model validity unresolved.
* Use controlled cases that change one explanatory factor at a time.
* Higher precision fixes avoidable arithmetic loss; it cannot recover
  information absent from the measurements.
* Report robust quantities separately and use explicit `indeterminate` states
  when the decision boundary is crossed.
* A successful investigation aligns the scientific claim with complementary
  evidence, assumptions, and limitations.


## Connection beyond the core modules

This capstone completes the ten-module core sequence. The
[optional advanced topics](optional-advanced-topics.md) extend the same
investigation workflow to mixed precision, interval arithmetic, numerical
linear algebra, stochastic algorithms, and accelerator or distributed
computing. The capstone's precision comparison, deterministic bounds, and
ill-conditioned inverse problem provide natural starting points for those
extensions.
