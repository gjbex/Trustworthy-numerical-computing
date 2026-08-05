# Module 9: Communicating Numerical Reliability

A numerical investigation is incomplete when its strongest evidence remains in
an unlabelled table, a notebook cell, or the investigator's memory. Another
scientist needs to know what quantity was computed, which claim the evidence
supports, how close the result is to a requirement, and what could still change
the conclusion.

Good reporting is neither a declaration that a result is “validated” nor a dump
of every diagnostic. It is a compact, traceable argument. The numerical result,
reference, comparison criterion, observed error, decision margin, assumptions,
and limitations must remain distinguishable.

This module turns a small heating-energy calculation into such an argument. The
case has an analytic reference, a predicted refinement rate, a numerical error
budget, a bounded input range, low-order environment variation, and an
explicitly unvalidated model assumption. Those layers make it possible to show
which digits and conclusions are supported—and which are not.


## Learning outcomes

After this module, you should be able to:

* begin a reliability statement with the scientific quantity, units, intended
  use, and required accuracy;
* distinguish numerical error, discretization error, input range, measurement
  uncertainty, model discrepancy, stochastic variability, and environment
  variation;
* summarize references, convergence, invariants, and reproducibility evidence
  without stretching them beyond their scope;
* choose displayed digits that expose the decision-relevant scale without
  implying unsupported accuracy;
* report tolerances together with their metric, rationale, and observed margin;
* retain failed checks, non-finite states, and unresolved limitations;
* write a concise numerical reliability statement linked to a fuller evidence
  record.


## Prerequisite connection

Module 3 established that a tolerance encodes a requirement rather than a repair
for a failed test. Module 4 separated input sensitivity, algorithmic behaviour,
and implementation defects, then introduced a
[propagation framework](04-conditioning-and-numerical-stability.md#propagation-combines-sensitivity-with-input-information)
for declared deterministic bounds and standard uncertainties. Modules 5 and 6
produced arithmetic and convergence diagnostics. Module 7 connected claims to
complementary validation evidence. Module 8 defined bitwise, numerical,
statistical, and conclusion-level reproducibility contracts.

Module 9 does not introduce another way to make a result trustworthy. It teaches
how to communicate the evidence already produced without blurring those
distinctions or claiming more than the tested scope supports.


## Start with the decision-facing claim

A report should first identify:

* the quantity of interest and its units;
* the input range and operating regime;
* the mathematical or physical model being assumed;
* the decision, comparison, or downstream use;
* the accuracy or uncertainty scale that could change that use.

“The solver converged in eight iterations” is an implementation observation,
not the scientific claim. “The computed accumulated energy exceeds the
$20.0\ \mathrm{kWh}$ requirement over the stated input range” identifies a
decision-facing claim. Iteration counts, residuals, and references then become
evidence for or against that claim.

State conditional claims conditionally. If model validation has not been
performed, write “under the exponential power model,” not “the physical system
delivers.”


## Keep result, evidence, interpretation, and limitation separate

A compact report has four layers:

| Layer | Question | Example |
|---|---|---|
| **Result** | What quantity was obtained? | Nominal accumulated energy is $20.62\ \mathrm{kWh}$ |
| **Numerical evidence** | Why is the computation adequate? | Error is $4.20\times10^{-4}\ \mathrm{kWh}$ against an analytic reference, below a $0.01\ \mathrm{kWh}$ budget |
| **Scientific interpretation** | What decision follows? | The conservative lower bound remains above $20.0\ \mathrm{kWh}$ |
| **Limitation** | What has not been established? | The exponential power model has not been compared with observations |

Combining these layers into “the result is correct” hides the scope of the
evidence. Separating them does not make the prose weak; it makes the supported
claim reviewable.


## Controlled reporting case: accumulated heating energy

Assume the power delivered during one characteristic time follows

$$
P(t)=P_0\exp\left(\frac{t}{\tau}\right),
\qquad 0\le t\le\tau,
$$

where $P_0$ is measured in kilowatts and $\tau=1.00\ \mathrm{h}$ is treated as a
fixed configured duration in this teaching case. With the dimensionless
coordinate $x=t/\tau$, the accumulated energy is

$$
E=P_0\tau\int_0^1 e^x\,\mathrm{d}x
  =P_0\tau(e-1).
$$

The inputs and requirements are:

| Item | Declared value |
|---|---|
| Nominal initial power | $P_0=12.0\ \mathrm{kW}$ |
| Admissible measured-power range | $11.9\le P_0\le12.1\ \mathrm{kW}$ |
| Configured duration | $\tau=1.00\ \mathrm{h}$, treated as exact here |
| Decision threshold | $E>20.0\ \mathrm{kWh}$ |
| Numerical error budget | $0.01\ \mathrm{kWh}$ |
| Candidate method | Composite trapezoidal rule with 64 equal panels |

The $0.01\ \mathrm{kWh}$ numerical budget is small compared with both the input
range and the decision margin. It is fixed before inspecting the computed
result. The admissible $P_0$ range is a deterministic input range; no probability
distribution or confidence level is supplied.


## Report the numerical evidence quantitatively

For the nominal input, the analytic model reference is

$$
E_{\mathrm{ref}}
=12.0\,(e-1)
=20.6193819415085428\ldots\ \mathrm{kWh}.
$$

The 64-panel trapezoidal calculation gives

$$
E_{T,64}=20.619801442201130\ \mathrm{kWh},
$$

with absolute numerical error

$$
|E_{T,64}-E_{\mathrm{ref}}|
=4.20\times10^{-4}\ \mathrm{kWh}.
$$

That is about 24 times smaller than the $0.01\ \mathrm{kWh}$ budget. State the
metric and reference: the phrase “error is small” provides neither.

A refinement study supports the expected second-order behaviour:

| Panels | Trapezoidal energy (kWh) | Absolute error (kWh) | Observed order |
|---:|---:|---:|---:|
| 8 | $20.646223105971622$ | $2.68\times10^{-2}$ | — |
| 16 | $20.626093542959936$ | $6.71\times10^{-3}$ | $2.00$ |
| 32 | $20.621059923795926$ | $1.68\times10^{-3}$ | $2.00$ |
| 64 | $20.619801442201130$ | $4.20\times10^{-4}$ | $2.00$ |

The reported evidence is stronger than “the result stopped changing.” It names
the reference, error measure, tested refinements, predicted rate, and observed
rate. It remains evidence for this smooth integrand and tested regime, not every
power history.


## Distinguish an error from an uncertainty or range

These quantities answer different questions:

| Quantity | Meaning | Appropriate report |
|---|---|---|
| Floating-point error | Difference caused by representing and evaluating in finite precision | Method, precision, order sensitivity, and comparison with a stronger arithmetic reference |
| Discretization error | Difference introduced by replacing a continuous problem with a finite approximation | Refinement, observed order, estimator, or bound |
| Iteration error | Difference remaining when an iterative method terminates | Residual, update, stopping criterion, and relationship to the quantity of interest |
| Input range or measurement uncertainty | What input values are admissible or plausible | Units, provenance, calibration, interval or distribution, and propagation method |
| Model discrepancy | Difference between the mathematical model and the real system | Observational validation over a stated intended-use regime |
| Stochastic variability | Variation caused by sampling or random processes | Replicates, estimator uncertainty, interval, and practical effect size |
| Environment variation | Change under compiler, library, hardware, precision, or execution-order choices | Reproducibility contract, tested matrix, metric, and observed spread |

Do not add these quantities together merely because they share units. A
deterministic interval is not a confidence interval, and a residual is not a
probability distribution. Combining uncertainty sources requires a justified
model of their dependence and interpretation.


## Use bounds to keep the claim honest

For convex $e^x$, the midpoint rule is a lower bound and the trapezoidal rule is
an upper bound. At 64 panels and nominal $P_0$:

$$
20.619172191802360
\le E \le
20.619801442201130\ \mathrm{kWh}.
$$

The numerical bracket width is
$6.29\times10^{-4}\ \mathrm{kWh}$, again below the numerical budget.

Because the integral and $P_0$ are positive, the input range and quadrature
bounds combine monotonically into the deterministic envelope

$$
20.447345756870671
\le E \le
20.791633120886139\ \mathrm{kWh}.
$$

This envelope covers the declared $P_0$ range and the midpoint–trapezoidal
numerical bracket. It is not a confidence interval and does not include model
discrepancy or uncertainty in $\tau$. The lower endpoint remains about
$0.45\ \mathrm{kWh}$ above the decision threshold, so the decision is robust to
the included variations.


## Report digits supported by the evidence

Binary64 can print the candidate as
`20.619801442201130`, but the input range spans about
$0.34\ \mathrm{kWh}$. Displaying every stored digit would emphasize arithmetic
representation while hiding the scale that matters.

For the decision-facing statement, a useful presentation is:

* nominal model result: $20.62\ \mathrm{kWh}$;
* deterministic envelope: $[20.45,20.79]\ \mathrm{kWh}$;
* threshold: $20.0\ \mathrm{kWh}$;
* conservative margin: $0.45\ \mathrm{kWh}$.

There is no universal significant-digit rule that replaces judgment. Preserve
full-precision values in the machine-readable evidence record, then round at the
communication boundary according to the input resolution, uncertainty or range,
numerical error, and decision margin. Round the value and its interval to
compatible decimal places.

Trailing zeros can carry meaning. If a requirement is specified as
$20.0\ \mathrm{kWh}$, silently rewriting it as $20\ \mathrm{kWh}$ may erase the
declared resolution. Conversely, extra digits should not be used to manufacture
authority.


## State tolerance rationale and observed margin together

A useful tolerance sentence contains:

1. the compared quantity and units;
2. the reference or baseline;
3. the metric;
4. the numerical acceptance threshold and its rationale;
5. the observed value and pass/fail outcome.

For this case:

> Against the analytic model reference, the 64-panel trapezoidal energy has an
> absolute error of $4.20\times10^{-4}\ \mathrm{kWh}$, below the predeclared
> $0.01\ \mathrm{kWh}$ numerical budget.

The tolerance does not include input range or model discrepancy. Saying so is
part of the result, not an optional disclaimer.


## Compress evidence without replacing it

The reliability statement should name the strongest complementary evidence,
not reproduce every notebook row:

| Claim | Strongest compact evidence | Limitation retained |
|---|---|---|
| The numerical method is adequate at 64 panels | Analytic-reference error is $4.20\times10^{-4}\ \mathrm{kWh}$ and refinement is second order | One smooth model integrand |
| The numerical value is not specific to one quadrature formula | Midpoint and trapezoidal values bracket the analytic reference | Both implementations share the same runtime and model |
| Input-range variation does not reverse the decision | Conservative envelope is $[20.45,20.79]\ \mathrm{kWh}$, above $20.0\ \mathrm{kWh}$ | Range is deterministic and covers only $P_0$ |
| Tested evaluation-order variation is harmless | Forward, reverse, and accurate reductions differ only in low bits and all pass the budget | One Python runtime; no cross-platform execution |
| The exponential model represents the physical system | No observational evidence was used | Not established |

Keep the full tables, code, source revision, input record, and environment record
available as supporting artifacts. The concise statement is an index into that
evidence, not a replacement for it.


## Communicate environment variation at the required level

The 64-panel trapezoidal interior sum produces slightly different binary64
values when accumulated forward, in reverse, or with a more accurate summation
algorithm:

| Reduction | Energy (kWh) | Binary64 representation |
|---|---:|---|
| Forward serial | $20.619801442201130$ | `0x1.49eab4eac447ap+4` |
| Reverse serial | $20.619801442201123$ | `0x1.49eab4eac4478p+4` |
| Accurate summation | $20.619801442201119$ | `0x1.49eab4eac4477p+4` |

Bitwise identity fails. The maximum spread is about
$1.1\times10^{-14}\ \mathrm{kWh}$, negligible relative to the numerical budget,
the input range, and the decision margin. Report numerical and conclusion
reproducibility for these tested orders—not cross-platform reproducibility,
because no other platform was run.


## Failed checks and non-finite states belong in the report

Do not report only successful evidence. A failed invariant, an unresolved
refinement anomaly, a `NaN`, a different termination reason, or an environment
that crosses the decision boundary can define the limit of the supported claim.

Use explicit language:

* “The $128^3$ case exceeded the memory budget and was not evaluated,” not “all
  resolutions passed.”
* “Two GPU runs returned `NaN` and are excluded from the finite-error summary,”
  not an average computed after silently dropping them.
* “The numerical criterion failed although the qualitative classification was
  unchanged,” not “the results were reproducible.”

Separating failure from success prevents a concise statement from becoming
selective evidence.


## A reliability statement has a stable structure

Use a compact sequence:

1. **Claim and scope:** quantity, units, model, input range, and intended use.
2. **Reported result:** rounded value, range or interval, and decision margin.
3. **Numerical evidence:** reference, error metric, tolerance, convergence,
   invariant, or independent method.
4. **Variability:** tested precision, environment, stochastic, or input changes
   and the required agreement level.
5. **Assumptions and limitations:** unvalidated models, omitted uncertainty
   sources, failed checks, and untested regimes.

For the heating case, a defensible statement is:

> Under the exponential power model with $\tau=1.00\ \mathrm{h}$ and
> $P_0\in[11.9,12.1]\ \mathrm{kW}$, accumulated energy is
> $[20.45,20.79]\ \mathrm{kWh}$; the nominal result is
> $20.62\ \mathrm{kWh}$, and the lower bound remains
> $0.45\ \mathrm{kWh}$ above the $20.0\ \mathrm{kWh}$ requirement. The
> 64-panel trapezoidal result differs from the analytic model reference by
> $4.20\times10^{-4}\ \mathrm{kWh}$, shows the expected second-order
> refinement, and preserves the conclusion under the tested reduction orders.
> This supports the threshold decision for the declared input range in the
> tested runtime; it does not validate the exponential model, assign a
> probability to the input range, include uncertainty in $\tau$, or establish
> portability to untested platforms.

The statement is qualified, but it still makes a useful decision. Limitations
identify what evidence would be needed to broaden it.


## Recognize weak reporting patterns

| Pattern | Example | Why it fails |
|---|---|---|
| Overclaim | “The system delivers exactly $20.619801442201130\ \mathrm{kWh}$.” | Treats model, inputs, and stored digits as exact |
| Verdict flag | “The result was validated.” | Does not identify the claim, evidence, or scope |
| Vague agreement | “All environments gave similar answers.” | Omits environments, metric, tolerance, and observed spread |
| Evidence dump | A full convergence log with no interpretation | Forces the reader to reconstruct the claim and decision |
| Limitation-only prose | “Many factors could affect the result.” | Avoids stating what the existing evidence does support |

Useful scientific caution is specific. Name the limitation and its consequence:
“model validation is absent, so the conclusion is conditional on the exponential
power law.”


## Layer the communication artifact

Different readers need different resolution, but the layers should agree:

1. **Headline result:** the decision-facing value, range, and qualification.
2. **Reliability statement:** claim, strongest evidence, variability,
   assumptions, and limitations.
3. **Evidence table:** parameters, references, errors, tolerances, convergence,
   environment comparisons, and failed checks.
4. **Reproducible artifact:** source revision, inputs, configuration, executable
   code, environment record, and complete outputs.

Do not put a stronger claim in the headline than the evidence table supports.
Do not bury a conclusion-changing failure only in the lowest layer.


## Companion activity: writing a reliability statement

The self-paced
[numerical reliability statement](../notebooks/09-reliability-statement.qmd)
activity asks you to:

1. state the energy quantity, units, model, input range, and threshold;
2. compute an analytic reference and a refinement record;
3. separate numerical error from a deterministic input envelope;
4. compare low-order reduction variation against the declared contract;
5. select presentation digits while preserving full evidence precision;
6. diagnose overconfident, vague, and data-dump statements;
7. assemble and revise a claim-evidence-variability-limitation record.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/09-reliability-statement.qmd
```

The complete site build executes the activity and generates a downloadable
Jupyter notebook.


## Questions for reviewing a reliability statement

Before accepting a reported result, ask:

1. Is the decision-facing quantity named with units and an operating range?
2. Does the statement distinguish a computed value from a physical claim?
3. Are the reference, metric, tolerance, and tolerance rationale explicit?
4. Are numerical error, input uncertainty or range, model discrepancy, and
   stochastic variability kept distinct?
5. Do the displayed digits match the evidence and decision scale?
6. Are convergence, validation, and reproducibility claims limited to what was
   actually tested?
7. Are failed checks, non-finite states, and omitted regimes visible?
8. Can a reader locate the full evidence and reproduce the reported result?


## Reflection questions

1. Why is `20.619801442201130 kWh` a poor decision-facing presentation even
   though it is the computed binary64 value?
2. Why is the deterministic envelope not a confidence interval?
3. Which evidence supports the $20.0\ \mathrm{kWh}$ threshold decision, and
   which evidence would be needed to claim that the exponential model is
   physically valid?
4. Why should a tolerance statement name both its reference and rationale?
5. What information is lost when the complete report says only
   `validated=True`?
6. How can a result be conclusion-reproducible but numerically irreproducible?


::: {.callout-note collapse="true"}
## Suggested answers

1. The declared input range produces about $0.34\ \mathrm{kWh}$ of output
   variation, so fifteen decimal places emphasize storage rather than supported
   scientific resolution. Retain full precision in the evidence record and
   report $20.62\ \mathrm{kWh}$ with the range.
2. The range follows from declared admissible inputs and deterministic
   quadrature bounds. No probability model, coverage probability, or sampling
   interpretation was supplied.
3. The conservative envelope remains above the threshold, the numerical error
   passes its budget, refinement is second order, and tested reduction orders
   preserve the decision. Physical validity requires suitable observations and
   uncertainty over the intended-use regime.
4. A number such as $0.01$ has no meaning without the compared quantity, units,
   metric, and requirement that motivated it. Naming the reference also defines
   what discrepancy is being measured.
5. The flag loses the claim, reference, metric, tolerance, observed margin,
   tested inputs and environments, failed checks, assumptions, and limitations.
6. Several runs may remain on the same side of a decision threshold while their
   differences exceed the numerical accuracy requirement. The scientific
   classification survives, but numerical agreement does not.
:::


## Takeaways

* Lead with the quantity, units, intended use, and conditional scientific claim.
* Keep numerical error, input range or uncertainty, model discrepancy,
  stochastic variability, and environment variation distinct.
* Report the reference, metric, tolerance rationale, observed error, and margin
  together.
* Display only digits supported by the evidence while preserving full precision
  in reproducible artifacts.
* Summarize the strongest complementary evidence and retain failed checks and
  limitations.
* A reliability statement is a concise index into the evidence, not a verdict
  that replaces it.


## Connection to the next module

[Module 10: Capstone—Investigating A Suspicious Result](10-capstone-investigating-a-suspicious-result.md)
requires participants to reproduce a suspicious result, diagnose and improve
it, validate the change, and use this reporting structure to state a qualified
conclusion.
