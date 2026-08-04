# Capstone: The Stable Total And The Unstable Split

This capstone asks you to decide whether two nearly indistinguishable sensor
responses support a concentration threshold. The supplied program runs, returns
positive concentrations, and has a small residual. A controlled precision
change reverses its decision.

Plan for about 75 minutes. Work from the evidence rather than reading the
reference solution first.


## Scientific question and required accuracy

Two compounds have unknown concentrations $c_A$ and $c_B$, measured in
$\mathrm{mg/L}$. Their calibrated sensor responses are modelled by

$$
\begin{aligned}
y_1 &= c_A+c_B,\\
y_2 &= c_A+(1+\delta)c_B.
\end{aligned}
$$

The readings $y_1$ and $y_2$ are in normalized response units. The response
coefficients therefore have units of normalized response per $\mathrm{mg/L}$.
For this case:

| Item | Declared value |
|---|---:|
| $y_1$ | $1.0000000$ response units |
| $y_2$ | $1.0000004$ response units |
| Sensor separation $\delta$ | $10^{-6}$ |
| Deterministic bound on each reading | $\pm5\times10^{-8}$ response units |
| Decision threshold | $c_A>0.61\ \mathrm{mg/L}$ |
| Required absolute accuracy in $c_A$ | $0.01\ \mathrm{mg/L}$ |

The bounds describe an admissible input range, not a probability distribution
or confidence interval. Treat the linear response model and its calibration as
assumptions: the supplied computation does not validate them physically.


## Files

- [`starter/capstone.py`](starter/capstone.py) contains the supplied binary32
  calculation and six investigation TODOs.
- [`starter/test_capstone.py`](starter/test_capstone.py) contains the completion
  checks. Some pass initially; checks that reach TODOs fail until you implement
  them.
- [`starter/evidence-record.md`](starter/evidence-record.md) is the record to
  complete before writing your conclusion.
- The [reference solution overview](solution/README.md) links a separately
  checked implementation and evidence record. Consult it after completing or
  discussing your investigation.

Only Python's standard library is required.


## Start with a prediction

Before running the program, record answers to these questions:

1. Should a residual much smaller than the required concentration accuracy be
   enough to accept the decision?
2. Would you expect binary32 and binary64 to lie on different sides of the
   threshold?
3. Which quantity seems likely to be better determined: each component or
   their total?
4. What evidence would distinguish input sensitivity from a defective solver?


## Reproduce the suspicious result

From the repository root:

```bash
cd hands-on/10-sensor-inversion/starter
python3 capstone.py
```

Record the two concentrations, decision, residual quantity, units, and
precision. Do not change the implementation yet.

Run the supplied checks:

```bash
python3 -m unittest -v
```

The initial failures caused by `NotImplementedError` are expected starter
state, not evidence about the numerical result. Record which baseline and edge
case checks already pass.


## Stage 1: establish the nominal reference

Implement `solve_binary64` and `decimal_reference`.

- Construct `Decimal` inputs from strings; constructing them directly from
  binary floats would import the representation error you are trying to
  examine.
- Compare binary32 and binary64 with the decimal reference using absolute error
  in $\mathrm{mg/L}$.
- State whether each nominal calculation meets the $0.01\ \mathrm{mg/L}$
  requirement and which threshold decision it makes.

Explain why the decimal result is a reference for the declared nominal algebra,
but not proof that the sensor model represents the physical sample.


## Stage 2: assess conditioning

Implement `condition_number_2`. For

$$
A=\begin{bmatrix}1&1\\1&1+\delta\end{bmatrix},
$$

use the eigenvalues of $A^\mathsf{T}A$. Its determinant is $\delta^2$.
Compute the larger eigenvalue directly and obtain the condition number from the
eigenvalue product; avoid subtracting nearly equal values to form the smaller
eigenvalue.

Then repeat the known synthetic split
$c_A=0.6\ \mathrm{mg/L}$, $c_B=0.4\ \mathrm{mg/L}$ for
$\delta=10^{-1},10^{-2},10^{-4},10^{-6}$.

Record how the condition number and binary32 forward error change. Use the
well-separated case as a control: if the same code performs well there, the
evidence points toward sensitivity of the near-indistinguishable system rather
than a generic implementation defect.


## Stage 3: interpret the residual

The supplied `residual_inf_norm` returns

$$
\lVert r\rVert_\infty
=\max_i\left|(A\widehat{c}-y)_i\right|
$$

in normalized response units. Compare it with forward error in the
concentrations, which has units $\mathrm{mg/L}$.

Explain why these quantities cannot be compared as bare numbers. Use the
condition estimate to explain how a small response residual can coexist with a
concentration error large enough to reverse the decision.


## Stage 4: propagate the declared input bounds

Implement `concentration_envelope` by evaluating all four combinations of the
lower and upper reading bounds with `Decimal` arithmetic. Implement
`classify_interval` so that it returns:

- `yes` only if every admissible $c_A$ is strictly above the threshold;
- `no` only if no admissible $c_A$ is strictly above it;
- `indeterminate` when the interval crosses the threshold.

Record separate ranges for $c_A$, $c_B$, and $c_A+c_B$. Do not label these
deterministic ranges as confidence intervals.


## Stage 5: improve one factor at a time

Make and evaluate these changes separately:

1. retain binary64 rather than storing the system in binary32;
2. report an interval decision rather than a Boolean nominal decision;
3. report the well-determined total separately from the component split.

For each change, state what it improves and what it cannot fix. In particular,
decide whether higher arithmetic precision can remove sensitivity to admissible
sensor-reading variation.


## Stage 6: validate and report

Implement `reliability_statement`, then run:

```bash
python3 capstone.py --report
python3 -m unittest -v
```

Your evidence should include at least two complementary checks, such as:

- exact-decimal agreement for the declared nominal inputs;
- the well-separated synthetic control;
- the condition-number trend as $\delta$ changes;
- exhaustive propagation of the four deterministic input corners;
- the invariant $c_A+c_B=y_1$.

Mechanical test success is not scientific approval. Inspect the evidence record
and write a concise statement containing the claim, nominal result, reference,
metric, accuracy requirement, conditioning evidence, input envelope, supported
decision, and limitations.


## Completion criteria

You are finished when you can show that:

- the suspicious result and precision-dependent decision were reproduced;
- the nominal reference is independently justified;
- residual and forward error are distinguished by meaning and units;
- conditioning is identified as the dominant limitation;
- arithmetic precision and input sensitivity are assessed separately;
- the threshold decision covers the complete declared input range;
- at least two complementary validation checks pass;
- the final reliability statement says what is and is not supported.

A well-supported `indeterminate` result is a successful capstone outcome.


::: {.callout-tip collapse="true"}
## Hints

1. Subtract the two sensor equations to isolate $c_B$.
2. For a $2\times2$ matrix, the product of the eigenvalues of
   $A^\mathsf{T}A$ equals $\det(A)^2$.
3. The extrema of this linear mapping over rectangular input bounds occur at
   corners.
4. Ask whether the final conclusion changes when the calculation is more
   accurate but the admissible input range is retained.
:::


## Optional extensions

- Find the smallest sensor separation for which binary32 stores distinct
  response coefficients.
- Determine what reading bound would be required to decide the threshold with
  the requested $0.01\ \mathrm{mg/L}$ accuracy.
- Add a third sensor with a meaningfully different response signature and state
  how it changes the validation argument.
- Explore a least-squares or regularized estimate, but report the added model
  assumption rather than treating regularization as recovered information.


## After the investigation

Compare your work with the
[`solution/evidence-record.md`](solution/evidence-record.md) and the tested
[`solution/capstone.py`](solution/capstone.py). Differences in wording are
expected; compare the claims, evidence, units, and limitations rather than
matching prose exactly.
