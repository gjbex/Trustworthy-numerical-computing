# Module 6: Iterative Algorithms And Convergence

An iterative algorithm produces a sequence of approximations rather than a
self-evident final answer. Stopping is therefore part of the numerical method:
the implementation must connect quantities it can observe to the accuracy the
application requires, detect known failure patterns, and report why the
iteration ended.

A single Boolean named `converged` hides too much. This module develops a small
termination contract using residual and update criteria, an iteration budget,
and explicit failure reasons. A controlled relaxation iteration and Newton's
method for a square root show why neither a small update nor a tight tolerance
is sufficient evidence by itself.


## Learning outcomes

After this module, you should be able to:

* distinguish forward error, residual, and update size;
* explain which of those quantities an algorithm can normally observe;
* combine absolute and relative stopping tolerances with meaningful scales;
* recognize false convergence, stagnation, oscillation, divergence, and
  non-finite iterates;
* define an iteration budget and return a specific termination reason;
* perform a tolerance study and identify an attainable accuracy floor;
* record convergence evidence suitable for later review.


## Prerequisite connection

Module 3 introduced absolute, relative, and mixed comparison criteria. Module
4 separated forward error from residual and showed that their relationship
depends on the problem's conditioning. Module 5 showed how finite precision can
erase an update or make an intermediate non-finite.

This module brings those ideas inside an iteration. It uses mixed criteria for
observable quantities, refuses to interpret a residual as an error without a
problem-specific argument, and treats an update that rounds to zero as possible
stagnation rather than automatic success.


## An iteration exposes several different quantities

Write the approximation after iteration $k$ as $x_k$ and the desired solution
as $x^*$. Three quantities commonly appear in convergence discussions:

### Forward error

The forward error is

$$
e_k=x_k-x^*,
$$

or its norm for a vector problem. It directly describes the quality of the
answer, but $x^*$ is usually unknown. An algorithm therefore cannot normally
use the true forward error as its stopping test. A known solution may be used
in a constructed experiment or test suite, not silently assumed in production.
The [vectors, norms, and scaling reference](reference-vectors-norms-and-scaling.md)
introduces the norm notation used for vector problems.

### Residual

For an equation $f(x)=0$, the residual is

$$
r_k=f(x_k).
$$

It measures how well the computed approximation satisfies the equation. A
residual often has different units from $x$ and needs its own scale. It is
usually observable, but a small residual implies a small forward error only
when the problem supplies a useful relationship between them. An
ill-conditioned problem can have a tiny residual and a large forward error.

Some applications use a defect, constraint violation, gradient, or change in
objective instead of an equation residual. Name the quantity precisely and
state what it is expected to establish.

### Update

The update is

$$
\Delta x_k=x_{k+1}-x_k.
$$

It measures movement between successive iterates and normally has the same
units as $x$. A small update may mean the method has settled near a solution.
It may also mean the step was damped excessively, the update rounded away, or
the algorithm is stuck far from a solution.

| Quantity | Typical interpretation | Usually observable? | Main limitation |
|---|---|---:|---|
| Forward error $e_k$ | Distance from the desired answer | No | Requires $x^*$ or a justified bound |
| Residual $r_k$ | Equation or constraint satisfaction | Yes | Its relation to error is problem-dependent |
| Update $\Delta x_k$ | Movement of the iterate | Yes | Small movement can be stagnation |

None of these quantities can replace the others. A useful termination policy
combines independent evidence where practical.


## Stopping is a numerical claim

An absolute threshold alone has units and fixes one scale. A relative threshold
alone is undefined or unhelpful when the reference scale is zero or very small.
Use a mixed residual criterion

$$
\lVert r_k\rVert \le a_r+\rho_r R,
$$

where $a_r$ is an absolute residual tolerance, $\rho_r$ is a dimensionless
relative tolerance, and $R$ is a documented residual scale. Similarly, use a
mixed update criterion

$$
\lVert\Delta x_k\rVert \le a_x+\rho_x X_k,
$$

where $X_k$ represents a meaningful solution scale. A common local choice is

$$
X_k=\max(\lVert x_k\rVert,\lVert x_{k+1}\rVert),
$$

but a fixed physical or application scale can be better near zero.

The notation and precise form of these criteria are not universal. Different
texts and solver interfaces use different symbols, terminology, normalization,
and scaling conventions. A production solver may normalize the initial
residual, use componentwise scaling, apply a preconditioned norm, or monitor a
backward-error estimate. The contract must state:

* the quantity being measured and its units;
* the norm or aggregation rule;
* the absolute tolerance and the near-zero scale it represents;
* the relative tolerance and reference scale;
* whether one criterion or several criteria must hold.

In the companion activity, `converged` requires both the residual and update
criteria. That conservative choice makes the two signals easy to compare; it
is not a theorem that every solver must use the same conjunction.


## Absolute residuals cannot be compared across scales blindly

Consider the dimensionless scalar equation $x=b$. The approximations
$0.9\times10^{-12}$ to $b=10^{-12}$ and $0.9\times10^{12}$ to $b=10^{12}$
both have relative forward error and relative residual $0.1$. Their absolute
residuals are $10^{-13}$ and $10^{11}$.

An absolute residual threshold of $10^{-6}$ accepts the small-scale result and
rejects the large-scale result, despite their identical relative quality. A
mixed threshold such as

$$
10^{-15}+10^{-8}|b|
$$

rejects both. The absolute part remains essential for $b=0$; its value should
come from a physical noise floor, required resolution, or other application
scale rather than from habit.


## A controlled relaxation iteration

Use the fixed-point iteration

$$
x_{k+1}=x_k+\omega(b-x_k)
$$

to solve $x=b$. Define the residual as $r_k=b-x_k$. For this deliberately
well-conditioned scalar problem, $r_k=x^*-x_k=-e_k$, so residual magnitude and
forward-error magnitude are equal. That convenient identity belongs to this
example; it must not be generalized to arbitrary systems.

The error recurrence is

$$
e_{k+1}=(1-\omega)e_k.
$$

It predicts the exact-arithmetic behaviour:

* $0<\omega<2$ gives contraction, except that $\omega=1$ solves the equation
  in one update;
* $\omega=2$ alternates between two values when the initial error is nonzero;
* $\omega<0$ or $\omega>2$ increases the error magnitude;
* a very small nonzero $\omega$ can form an update too small to change the
  stored iterate.

With $b=1$, $x_0=0$, a residual and update relative tolerance of $10^{-8}$,
and zero absolute tolerance, representative binary64 outcomes are:

| $\omega$ | Behaviour | Iterations | Final residual | Termination reason |
|---:|---|---:|---:|---|
| $0.5$ | Contracting | 27 | $7.45\times10^{-9}$ | `converged` |
| $2$ | Two-cycle | 2 | $1$ | `oscillating` |
| $3$ | Growing | 3 | $-8$ | `diverging` |

These reasons are produced by declared diagnostic rules, not inferred from an
unbounded history. The tutorial detects an exact two-cycle and three successive
increases in residual magnitude. A real solver may need windowed rates,
problem-specific monotonicity expectations, or more tolerant cycle detection.


## A small update can be false convergence

Set $b=2$, $x_0=1$, and $\omega=10^{-20}$. The mathematical update is
$10^{-20}$, but binary64 spacing near one is about $2.22\times10^{-16}$.
Adding the update therefore leaves the stored value unchanged:

$$
x_1=x_0=1,
\qquad
|r_1|=1.
$$

An update-only rule reports success because the stored update is zero. The
residual test rejects the iterate, and the unchanged value supplies direct
evidence of `stagnated`. This is the iterative counterpart of the lost
low-order contributions from Module 5.

Check the updated iterate rather than only the requested mathematical step.
Also distinguish deliberate constraints from arithmetic stagnation: a
projected or bounded method can produce no movement for a valid algorithmic
reason, but still needs an appropriate optimality or feasibility test.


## Failure is a result, not an exception to reporting

A solver should return a result object even when it does not converge, unless
the API contract requires an exception. Useful termination reasons include:

| Reason | Evidence used in this module | Appropriate response |
|---|---|---|
| `converged` | Required residual and update criteria hold | Report the final diagnostics |
| `stagnated` | The computed update does not change the iterate while criteria fail | Reassess scaling, precision, method, or requested tolerance |
| `oscillating` | A declared cycle detector triggers | Change the method, damping, or model |
| `diverging` | Residual magnitude grows over a declared window | Stop before wasting work; diagnose the iteration |
| `non_finite` | Iterate, residual, or update is NaN or infinite | Diagnose range, domain, or invalid arithmetic |
| `max_iterations` | The budget is exhausted | Preserve the best diagnostics; do not relabel as convergence |

The order of checks matters. After forming a candidate, the tutorial checks
for non-finite values, then satisfied stopping criteria, stagnation, a
two-cycle, sustained growth, and finally the iteration budget. Document a
different order if it changes which reason is returned.

At minimum, retain the final iterate, iteration count, termination reason,
residual and update norms, thresholds, scale definitions, and solver
parameters. A short history or convergence-rate summary makes the diagnosis
auditable without requiring every intermediate in a large production run.


## Newton's method meets a floating-point floor

For a less artificial example, solve $x^2-2=0$ with

$$
x_{k+1}=\frac{1}{2}\left(x_k+\frac{2}{x_k}\right),
$$

starting from $x_0=1$. Use $r_k=x_k^2-2$ and compare with an independently
computed high-precision value of $\sqrt{2}$ only after the run. The reference
measures forward error for this teaching experiment; the solver does not use it
to stop.

For this particular positive-root problem,

$$
x-\sqrt{2}=\frac{x^2-2}{x+\sqrt{2}},
$$

so the residual has a direct, well-scaled relationship to forward error near
the positive root. That identity explains the observed agreement; it does not
make residual and forward error interchangeable in other problems.

With mixed residual and update criteria using relative tolerance
$10^{-14}$, the binary64 iteration converges in six iterations. It returns
$x=1.414213562373095$, residual approximately
$-4.44\times10^{-16}$, and relative forward error approximately
$8.87\times10^{-17}$. Requesting relative tolerance $10^{-16}$ instead returns
`stagnated`: the next Newton update rounds to zero while the residual criterion
remains just beyond the requested threshold.

The stricter request did not produce a more accurate binary64 answer. It
changed the honest termination reason.


## Use a tolerance study to find an attainable region

A tolerance study repeats the same mathematical problem and method while
changing the requested tolerance. For the square-root experiment:

| Relative tolerance | Iterations | Relative residual | Relative forward error | Reason |
|---:|---:|---:|---:|---|
| $10^{-2}$ | 3 | $3.00\times10^{-6}$ | $1.50\times10^{-6}$ | `converged` |
| $10^{-4}$ | 4 | $2.26\times10^{-12}$ | $1.13\times10^{-12}$ | `converged` |
| $10^{-8}$ | 5 | $2.22\times10^{-16}$ | $8.87\times10^{-17}$ | `converged` |
| $10^{-12}$ | 6 | $2.22\times10^{-16}$ | $8.87\times10^{-17}$ | `converged` |
| $10^{-14}$ | 6 | $2.22\times10^{-16}$ | $8.87\times10^{-17}$ | `converged` |
| $10^{-16}$ | 6 | $2.22\times10^{-16}$ | $8.87\times10^{-17}$ | `stagnated` |

The plateau is evidence of an attainable binary64 floor for this formulation
and environment. Iteration count alone is not a quality metric: six iterations
can mean either justified convergence or an unmet tolerance at stagnation.

Keep the conclusion narrow. This study changes a solver tolerance, not the
mesh, time step, model, data quality, or arithmetic precision. There is little
value in driving solver error far below dominant modelling, discretization, or
input uncertainty. Module 7 combines convergence evidence with independent
validation and refinement studies.


## Companion activity: convergence and stopping diagnostics

The self-paced
[convergence and stopping diagnostics](../notebooks/06-convergence-and-stopping.qmd)
activity asks you to:

1. predict how an absolute residual rule treats the same relative error at two
   scales;
2. implement mixed residual and update criteria;
3. classify contraction, oscillation, divergence, and arithmetic stagnation;
4. compare update-only and combined stopping decisions;
5. run Newton's method with practical and unattainable tolerances;
6. retain a compact evidence record and state its limitations.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/06-convergence-and-stopping.qmd
```

The complete site build executes the activity and generates a downloadable
Jupyter notebook.


## Questions for reviewing an iterative result

Before accepting a reported convergence claim, ask:

1. What equation, objective, constraint, or invariant is being monitored?
2. Which quantity is the desired error, and is it actually observable?
3. What are the units, norm, absolute scale, and relative scale?
4. Which criteria must hold simultaneously?
5. How are non-finite values, stagnation, cycles, and growth detected?
6. What happens when the iteration budget is exhausted?
7. Does tightening the tolerance improve an independent quality measure?
8. Which larger sources of scientific error remain outside this experiment?


## Reflection questions

1. Why can a residual of $10^{-9}$ be excellent in one problem and useless in
   another?
2. In the relaxation experiment, why does $\omega=10^{-20}$ satisfy an
   update-only test while remaining far from the solution?
3. Why does the Newton run with tolerance $10^{-16}$ return `stagnated` rather
   than `converged`?
4. What evidence would you add before using the tutorial's cycle or divergence
   detector in a production solver?


::: {.callout-note collapse="true"}
## Suggested answers

1. A residual has units and a problem-dependent relationship to forward error.
   Its meaning requires a scale and a conditioning or error argument.
2. The requested update is smaller than binary64 spacing near one, so the
   stored iterate does not move. The residual remains one and independently
   rejects convergence.
3. The update rounds to zero before the residual satisfies the stricter mixed
   criterion. Reporting convergence would claim evidence the computation did
   not produce.
4. Test representative convergent, slowly convergent, noisy, and cycling
   histories; justify window lengths and thresholds; account for approximate
   rather than exact cycles; and document possible false positives.
:::


## Takeaways

* Error, residual, and update answer different questions.
* Absolute and relative tolerances need named scales and units.
* A small update is not sufficient evidence of convergence.
* Failure modes and exhausted budgets require explicit termination reasons.
* A tolerance study can reveal an attainable floor, but not validate the whole
  scientific calculation.
* Record the criteria, scales, final diagnostics, and reason with the result.


## Connection to the next module

Convergence evidence establishes how an iterative calculation terminated. It
does not by itself show that the equations, discretization, implementation, or
inputs answer the scientific question correctly.
[Module 7: Validating Scientific Computations](07-validating-scientific-computations.md)
combines this record with independent references, invariants, cross-method
comparisons, and refinement evidence to build a stronger validation argument.
