# Instructor Notes: Sensor-Inversion Capstone

## Teaching intent

This capstone tests whether participants can resist treating a code change or a
small residual as complete validation. The intended diagnosis has two layers:

1. binary32 storage creates an avoidable nominal decision reversal;
2. even accurate binary64 arithmetic cannot support the physical threshold
   decision over the declared input bounds because the inverse problem is
   ill-conditioned.

The successful outcome is a qualified `indeterminate` conclusion, not a forced
yes/no classification.


## Suggested timing

| Time | Activity |
|---:|---|
| 10 min | Read the case, predict, and run the baseline |
| 15 min | Build the binary64 and Decimal references |
| 15 min | Diagnose conditioning and residual behaviour |
| 15 min | Propagate bounds and improve the decision contract |
| 10 min | Run complementary checks |
| 10 min | Write and compare reliability statements |

For a shorter delivery, provide the condition-number function and retain the
reference, interval, and reporting tasks.


## Checkpoints

Pause teams before implementation changes and ask them to record:

1. the quantity and units of the residual;
2. the quantity and units of the required accuracy;
3. at least two candidate explanations for the decision reversal;
4. evidence that would discriminate between those explanations.

After the nominal reference, ask whether binary64 has solved the scientific
problem or only the stored algebraic problem. Return attention to the declared
deterministic reading bounds if participants have overlooked them.


## Expected evidence

- Binary32: $(c_A,c_B)=(0.625,0.375)\ \mathrm{mg/L}$, nominal decision `yes`,
  response residual about $2.5\times10^{-8}$, and $c_A$ error
  $0.025\ \mathrm{mg/L}$, which fails the $0.01\ \mathrm{mg/L}$ requirement.
- Binary64: approximately $(0.6,0.4)\ \mathrm{mg/L}$, nominal decision `no`,
  and $c_A$ error about $1.15\times10^{-11}\ \mathrm{mg/L}$, which passes the
  requirement.
- Exact-decimal reference: exactly $(0.6,0.4)\ \mathrm{mg/L}$ for the declared
  decimal inputs.
- Matrix 2-norm condition number: approximately $4.00\times10^6$.
- Input envelope:
  $c_A\in[0.49999995,0.70000005]\ \mathrm{mg/L}$ and
  $c_A+c_B\in[0.99999995,1.00000005]\ \mathrm{mg/L}$.
- Supported decision over the declared range: `indeterminate`.


## Common mistakes

- **“The residual is below 0.01, so it passes.”** The two values have different
  units and conditioning has not been accounted for.
- **“Decimal gives the truth.”** It gives a strong reference for the declared
  nominal algebra, not for uncertain sensor inputs or physical model validity.
- **“Use binary64 and report no.”** This fixes avoidable arithmetic error but
  ignores the conclusion-changing input envelope.
- **“Average the binary32 and binary64 answers.”** Precision variants are not
  independent observations or samples from a probability distribution.
- **“The model is invalid.”** The exercise establishes that model validation is
  absent, not that the linear model is false.
- **Widening the numerical tolerance.** The $0.01\ \mathrm{mg/L}$ requirement
  comes from the decision context; changing it to accept binary32 would change
  the claim.


## Debrief prompts

1. Which result is code verification, which is solution verification, and what
   would be needed for model validation?
2. Why does the well-separated control help isolate the intended cause?
3. Which change improved arithmetic without improving identifiability?
4. Why is reporting the total not merely avoiding the original question?
5. What new measurement would make the component decision answerable?


## Reference-solution validation

From the repository root:

```bash
cd hands-on/10-sensor-inversion/solution
python3 capstone.py --report
python3 -m unittest -v
```

The tests independently check declared-decimal provenance, the exact synthetic
reference, a well-conditioned control and separation sweep, the condition-number
magnitude, all three interval-classification outcomes, the four-corner envelope,
the supplied edge case in which binary32 cannot store the sensor separation,
accuracy outcomes for both precision paths, provenance fields, configurable
threshold reporting, and minimum reliability-statement qualifications.
