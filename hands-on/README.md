# Hands-On Exercises

The hands-on material turns the course investigation workflow into
participant-owned evidence. Each exercise states a numerical question and
accuracy requirement, starts with a prediction, varies one factor at a time,
and ends with a qualified conclusion.


## Module 10 capstone

[The Stable Total And The Unstable Split](10-sensor-inversion/README.md) asks
participants to investigate a two-component sensor calculation whose threshold
decision changes with arithmetic precision.

The exercise includes:

* a runnable starter with explicit TODOs;
* a structured evidence-record template;
* controlled precision, conditioning, and input-bound variations;
* tests that distinguish expected starter failures from completion;
* a separately checked reference implementation and evidence record;
* instructor notes with timing, checkpoints, expected results, and common
  mistakes.

Only Python's standard library is required. Start from the repository root:

```bash
cd hands-on/10-sensor-inversion/starter
python3 capstone.py
```


## Exercise expectations

Every participant investigation should record:

* the numerical question, quantities, units, scale, and valid input range;
* the required accuracy and decision threshold;
* a prediction or competing hypotheses;
* a reference, invariant, or independently motivated expected trend;
* controlled variations and observed diagnostic quantities;
* the improvement made and the limitation that remains;
* completion checks and revealing edge cases;
* a reliability statement with assumptions and limitations.

Reference solutions are aids for comparison, not unquestionable ground truth.
Review their formulation and evidence as critically as the starter calculation.
