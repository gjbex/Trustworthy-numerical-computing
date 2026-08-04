# Reference Evidence Record

## Prediction

- Binary32 may change the component split because both the sensor coefficient
  difference and reading difference are close to its resolution near one.
- A small residual is not sufficient because the inverse problem can amplify a
  small response perturbation into a large concentration change.
- The total $c_A+c_B=y_1$ should be better determined than the split.
- A well-separated synthetic control and a condition-number sweep distinguish
  input sensitivity from a generic solver defect.


## Declared claim and requirements

- Scientific question: is $c_A$ strictly greater than
  $0.61\ \mathrm{mg/L}$?
- Required absolute accuracy: $0.01\ \mathrm{mg/L}$ in $c_A$.
- Sensor readings: normalized response units.
- Each reading has a deterministic bound of
  $\pm5\times10^{-8}$ response units.
- The input bounds are not probabilities.
- The linear response law and calibration are assumed rather than physically
  validated by this exercise.


## Reproduction

| Precision | $c_A$ (mg/L) | $c_B$ (mg/L) | $c_A$ error (mg/L) | Residual (response units) | Meets $0.01$ mg/L? | Nominal decision |
|---|---:|---:|---:|---:|---|---|
| Binary32 | $0.625$ | $0.375$ | $0.025$ | $2.50\times10^{-8}$ | no | yes |
| Binary64 | $0.5999999999885$ | $0.4000000000115$ | $1.15\times10^{-11}$ | $0$ | yes | no |
| Exact-decimal nominal reference | $0.6$ | $0.4$ | not applicable | not applicable | not applicable | no |

Against the exact-decimal nominal reference, the binary64 forward error in
$c_A$ is approximately $1.15\times10^{-11}\ \mathrm{mg/L}$, below the declared
$0.01\ \mathrm{mg/L}$ arithmetic requirement for the nominal inputs. The
binary32 error in $c_A$ is $0.025\ \mathrm{mg/L}$, exceeds the requirement, and
reverses the nominal threshold decision.


## Conditioning and controlled variation

For $A=[[1,1],[1,1+\delta]]$, the 2-norm condition number at
$\delta=10^{-6}$ is approximately $4.00\times10^6$.

| Sensor separation $\delta$ | Condition number | Binary32 $c_A$ error (mg/L) |
|---:|---:|---:|
| $10^{-1}$ | $4.21\times10^1$ | $5.01\times10^{-7}$ |
| $10^{-2}$ | $4.02\times10^2$ | $4.79\times10^{-6}$ |
| $10^{-4}$ | $4.00\times10^4$ | $4.77\times10^{-4}$ |
| $10^{-6}$ | $4.00\times10^6$ | $2.50\times10^{-2}$ |

The same binary32 implementation is accurate for the well-separated control,
and its error grows as the signatures become less distinguishable. This
supports conditioning and finite precision as the intended causes, rather than
a generic algebra or indexing defect.

The residual is measured in response units, whereas forward error is measured
in $\mathrm{mg/L}$. The condition number explains why the small residual does
not establish the required component accuracy.


## Deterministic input envelope

Evaluating all four input-bound corners with exact-decimal arithmetic gives:

| Quantity | Admissible range (mg/L) |
|---|---:|
| $c_A$ | $[0.49999995,0.70000005]$ |
| $c_B$ | $[0.30,0.50]$ |
| $c_A+c_B$ | $[0.99999995,1.00000005]$ |

The $c_A$ range crosses $0.61\ \mathrm{mg/L}$, so the supported threshold
decision is **indeterminate**. The range is deterministic and carries no
probability or coverage interpretation.


## Improvement record

| Change made alone | Evidence improved | Limitation remaining |
|---|---|---|
| Retain binary64 | Nominal arithmetic error passes $0.01\ \mathrm{mg/L}$ | Input sensitivity remains |
| Use interval decision | Prevents an unsupported Boolean claim | Does not narrow the range |
| Report total separately | Preserves the well-determined quantity | Does not identify the split |

Higher arithmetic precision removes the avoidable binary32 decision reversal
for nominal inputs. It cannot create information that the two nearly identical
sensor signatures and bounded readings do not contain.


## Complementary validation checks

1. Exact-decimal algebra recovers the declared synthetic nominal split
   $c_A=0.6$, $c_B=0.4$.
2. The well-separated $\delta=0.1$ control is accurate in binary32, while the
   condition-number sweep predicts increasing sensitivity as $\delta$ shrinks.
3. Exhaustive corner propagation bounds every output admitted by the declared
   rectangular input range and preserves the invariant $c_A+c_B=y_1$.


## Environment and provenance

The structured `python3 capstone.py --report` output captures the source
revision and whether the worktree is dirty, along with the Python
implementation and version, operating system and release, machine architecture,
and floating-point radix and mantissa width. These values are generated at run
time rather than copied into this reference record, where they would quickly
become stale.


## Reliability statement

Under the declared linear two-sensor model, the binary64 nominal estimate is
$c_A=0.600\ \mathrm{mg/L}$ and agrees with the exact-decimal nominal reference
to $1.15\times10^{-11}\ \mathrm{mg/L}$, below the predeclared
$0.01\ \mathrm{mg/L}$ accuracy requirement. The emulated binary32 error in
$c_A$ is $0.025\ \mathrm{mg/L}$, exceeds that requirement, and changes the
nominal decision from `no` in binary64 to `yes`. However, the matrix 2-norm
condition number is approximately $4.00\times10^6$, and the deterministic
sensor-reading bounds imply $c_A\in[0.50,0.70]\ \mathrm{mg/L}$, which crosses
the strict $0.61\ \mathrm{mg/L}$ threshold; the supported decision is therefore
indeterminate. The total concentration remains in
$[0.99999995,1.00000005]\ \mathrm{mg/L}$. This evidence does not validate the
linear sensor model, assign a probability to the input bounds, or establish
behaviour on untested precision and hardware paths.
