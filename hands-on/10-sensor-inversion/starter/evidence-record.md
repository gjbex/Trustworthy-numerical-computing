# Capstone Evidence Record

## Prediction

- Expected effect of changing precision:
- Is a small residual sufficient? Why or why not?
- Quantity expected to be best determined:
- Evidence that would distinguish sensitivity from a solver defect:


## Declared claim and requirements

- Scientific question:
- Concentration units:
- Sensor-reading units:
- Required absolute accuracy:
- Decision threshold:
- Input-bound interpretation:
- Model assumptions:


## Reproduction

| Precision | $c_A$ (mg/L) | $c_B$ (mg/L) | $c_A$ error (mg/L) | Residual (response units) | Meets $0.01$ mg/L? | Decision |
|---|---:|---:|---:|---:|---|---|
| Binary32 |  |  |  |  |  |  |
| Binary64 |  |  |  |  |  |  |
| Decimal reference |  |  | not applicable | not applicable | not applicable |  |


## Conditioning and controlled variation

| Sensor separation $\delta$ | Condition number | Binary32 $c_A$ error (mg/L) | Interpretation |
|---:|---:|---:|---|
| $10^{-1}$ |  |  |  |
| $10^{-2}$ |  |  |  |
| $10^{-4}$ |  |  |  |
| $10^{-6}$ |  |  |  |

- Dominant failure mode:
- Evidence against a generic implementation defect:
- Relationship between residual and forward error:


## Deterministic input envelope

- $c_A$ range:
- $c_B$ range:
- $c_A+c_B$ range:
- Supported threshold decision:
- Why this is not a confidence interval:


## Improvement record

| Change made alone | Evidence improved | Limitation remaining |
|---|---|---|
| Retain binary64 |  |  |
| Use interval decision |  |  |
| Report total separately |  |  |


## Complementary validation checks

1. Check, expected result, observation, and outcome:
2. Check, expected result, observation, and outcome:
3. Optional additional check:


## Environment and provenance

- Source revision:
- Uncommitted changes present:
- Command used to generate the structured report:
- Python implementation and version:
- Operating system and release:
- Machine architecture:
- Floating-point radix and mantissa bits:


## Reliability statement

Write the claim, result, evidence, supported decision, assumptions, and
limitations in one concise paragraph.
