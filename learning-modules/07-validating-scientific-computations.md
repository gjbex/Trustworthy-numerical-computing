# Module 7: Validating Scientific Computations

A numerical result becomes trustworthy through an argument, not through one
successful test. An exact reference can expose a wrong answer at one input but
say little about other inputs. An invariant can reject impossible behaviour
without measuring the error. A refinement study can reveal the expected trend
while sharing the same modelling assumptions. Agreement between two methods is
stronger only to the extent that their failure modes are independent.

This module assembles those checks into a validation portfolio. A small
quadrature example is intentionally simple enough to have an analytic answer,
method-specific properties, a predicted refinement rate, and a genuinely
different series calculation. One suspicious implementation passes a plausible
test and broad bounds, yet the combined evidence identifies what is wrong.


## Learning outcomes

After this module, you should be able to:

* distinguish code verification, solution verification, and model validation;
* match a numerical or scientific claim to evidence that can test it;
* select exact cases, limiting cases, invariants, and properties;
* design and interpret a refinement study with a predicted convergence rate;
* assess whether a comparison method is sufficiently independent;
* use higher precision without treating it as an unquestionable oracle;
* assemble complementary checks and state what they leave unvalidated.


## Prerequisite connection

Module 3 established error measures, reference quality, and justified
tolerances. Module 4 separated problem conditioning, algorithmic stability, and
implementation correctness. Module 5 supplied recognizable arithmetic failure
modes. Module 6 produced a convergence record containing criteria, scales,
diagnostics, and a termination reason.

That record is one item of evidence. A solver can satisfy its stopping contract
while solving the wrong equations, using an inadequate discretization, or
representing the physical system poorly. Module 7 asks which additional checks
are needed for the claim being made.


## Verification and validation answer different questions

Terminology varies between fields, but the following distinction is useful:

* **Code verification** asks whether the implementation correctly represents
  the intended numerical method or equations: “Are we solving the equations
  right?” Exact cases, manufactured solutions, and method properties are
  especially useful here.
* **Solution verification** asks how much numerical error remains in a
  particular calculation. Iteration histories, mesh or time-step refinement,
  and error estimators contribute to this question.
* **Model validation** asks whether the mathematical model adequately
  represents the real system for the intended use: “Are we solving the right
  equations?” This normally requires experimental observations, trusted field
  data, or domain-specific comparisons.

The title of this module uses *validation* in the broad everyday sense of
building confidence in a scientific computation. When reporting evidence, use
the more precise terms. Passing an analytic quadrature case verifies code and
quantifies numerical error; it cannot establish that a physical rate law is a
valid model of an experiment.


## Begin with the claim, not the available test

A check is relevant only when its pass or failure changes confidence in a
specific claim. Write a small validation matrix before running a large
collection of tests:

| Claim | Candidate evidence | What the evidence cannot establish alone |
|---|---|---|
| The numerical method is implemented as specified | Exact or manufactured cases and method properties | Behaviour over all inputs |
| Iteration error is sufficiently small | Residual, update, and stopping record | Discretization or modelling error |
| Discretization error is controlled | Refinement trend and observed order | Correct equations or input data |
| The result is not an artefact of one method | Independent algorithm or implementation | Independence when assumptions or code are shared |
| The model represents the intended system | Experimental or observational comparison | Validity outside the tested regime |
| The scientific conclusion is robust | Sensitivity analysis around uncertain inputs and choices | Unknown omissions or structural model error |

This prevents evidence from being stretched beyond its scope. Ten variants of
the same unit test do not replace a missing refinement study, and two programs
that call the same flawed library routine are not independent merely because
they have different names.


## Reference cases need a stated authority

Useful references include:

* an exact analytic value;
* a manufactured solution constructed to exercise selected terms;
* a limiting or symmetry case with known qualitative behaviour;
* a high-precision calculation whose formulation and convergence were checked;
* a published benchmark with documented inputs and uncertainty;
* trusted experimental data appropriate to the intended use.

State why the reference is authoritative. A previous program version is a
regression baseline, not automatically ground truth. Higher precision reduces
rounding error but can reproduce the same unstable formula, modelling mistake,
or implementation defect. A published number can be unsuitable if its units,
boundary conditions, or parameter definitions differ.

Manufactured solutions are particularly useful when realistic exact solutions
are unavailable. Choose a smooth solution, substitute it into the equations to
derive the required source terms and boundary data, and test whether the code
recovers it. This verifies the exercised operators and their coupling; it does
not validate the realism of the manufactured case.


## Properties can reject wrong answers without an oracle

An **invariant** is a quantity that should remain unchanged, such as total mass
in a closed conservative system. More general **properties** include:

* positivity or boundedness;
* symmetry and antisymmetry;
* monotonicity;
* dimensional consistency;
* conservation or balance laws;
* reversibility where the model supports it;
* linearity, additivity, or permutation invariance;
* exactness for a specified class of inputs.

A property often applies over many inputs and can detect failures for which no
exact output is available. It is usually a necessary condition rather than a
sufficient one. A non-negative concentration field may still have the wrong
profile, and a conservative solver may conserve the wrong quantity because of
a unit conversion error.

Use the strongest property justified by the method. Broad bounds may be too
weak to distinguish two algorithms; exactness for affine functions may test a
specific quadrature contract directly.


## A controlled quadrature problem

Consider the dimensionless accumulated quantity

$$
I=\int_0^1 e^x\,\mathrm{d}x=e-1.
$$

The interval and exponent are dimensionless. In a physical application, a
time or length scale would be needed to nondimensionalize the exponent and
restore output units.

This example offers several independent predictions:

* $e^x$ is positive and increasing, so $1<I<e$;
* $e^x$ is convex, so the composite midpoint estimate lies below $I$ and the
  composite trapezoidal estimate lies above it;
* both midpoint and trapezoidal errors should decrease proportionally to
  $h^2$ in their asymptotic regime;
* the analytic answer can be checked with high-precision arithmetic and with a
  separately bounded exponential series.

The intended composite trapezoidal rule on $n$ equal subintervals of width
$h=1/n$ is

$$
T_n=h\left[
\frac{f(0)}{2}+\sum_{i=1}^{n-1}f(ih)+\frac{f(1)}{2}
\right].
$$

The suspicious candidate in the activity instead computes

$$
S_n=h\sum_{i=0}^{n-1}f(ih),
$$

which is the left-endpoint rule. It is valid as a first-order quadrature rule,
but it does not implement the claimed trapezoidal method.


## One passing reference case is weak evidence

For $f(x)=1$ on $[0,1]$, both $T_8$ and $S_8$ return the exact value one. The
constant case checks the interval width and basic accumulation, but it cannot
distinguish the endpoint weights because every sample has the same value.

The trapezoidal rule must also integrate every affine function exactly. For
$f(x)=x$, the analytic integral is $1/2$:

| Candidate | Computed value with $n=8$ | Absolute error |
|---|---:|---:|
| Intended trapezoidal rule $T_8$ | $0.5$ | $0$ |
| Suspicious candidate $S_8$ | $0.4375$ | $0.0625$ |

This focused reference case directly tests the claimed method. It identifies
an implementation mismatch more efficiently than comparing many arbitrary
functions.


## Necessary properties can still pass a wrong method

For the positive function $e^x$ on $[0,1]$, any reasonable positive-weight
estimate should remain inside the broad bound

$$
1\le Q_n\le e.
$$

At $n=8$, the trapezoidal, midpoint, and suspicious left-endpoint estimates all
satisfy that bound. The check remains valuable: a negative result or a value
above $e$ would be impossible under the stated assumptions. Its success does
not show that the trapezoidal rule was implemented.

This is why complementary evidence matters. The bound probes plausibility; the
affine case probes method fidelity; refinement probes the leading error; an
independent method probes reliance on one formulation.


## Refinement should test a predicted trend

Suppose the error of a method behaves asymptotically as

$$
E(h)=C h^p+\mathcal{O}(h^{p+1}),
$$

where $p$ is the order of accuracy. Halving $h$ should reduce the leading error
by approximately $2^p$. With errors $E_n$ and $E_{2n}$, estimate the observed
order as

$$
p_{\mathrm{obs}}=log_2\left(\frac{|E_n|}{|E_{2n}|}\right).
$$

For $e^x$ on the tested refinements:

| Method | Error at $n=8$ | Error at $n=64$ | Observed order near $n=64$ |
|---|---:|---:|---:|
| Trapezoidal | $2.24\times10^{-3}$ | $3.50\times10^{-5}$ | approximately $2.00$ |
| Midpoint | $1.12\times10^{-3}$ | $1.75\times10^{-5}$ | approximately $2.00$ |
| Suspicious candidate | $1.05\times10^{-1}$ | $1.34\times10^{-2}$ | approximately $1.00$ |

The suspicious routine converges to the correct integral, but at the rate of a
left-endpoint rule rather than the claimed trapezoidal rate. Convergence to the
right limit is not enough to verify the implementation contract.

A convincing refinement study states:

* which resolution parameter changes and which quantities remain fixed;
* the reference, estimator, or difference used as an error measure;
* the predicted rate and assumptions that support it;
* enough refinement levels to identify an asymptotic regime;
* whether roundoff, iteration error, noisy data, or unresolved scales eventually
  obscure the trend.

Do not select only the refinements that produce the desired slope. Coarse
resolutions may not yet be asymptotic, and very fine resolutions can be
dominated by floating-point error or an inner solver tolerance.


## Independent methods should fail differently

The composite midpoint rule samples the centre of each subinterval rather than
the endpoints. For convex $e^x$,

$$
M_n\le I\le T_n.
$$

At $n=8$, the activity obtains

$$
1.717163664995687
< I <
1.720518592164302.
$$

The bracket supports the result without using the decimal digits of $e-1$.
Both bounds converge at second order, and the bracket width decreases by about
a factor of four when the grid is doubled.

Midpoint and trapezoidal quadrature have different sample locations and leading
errors, but the tutorial implementations share a language, function, interval,
and similar loop structure. Their agreement is algorithmically useful but not
fully independent. A separately written implementation, another library, an
analytic transformation, or a method based on different mathematics provides
stronger cross-checking.


## A bounded series supplies a different calculation

The analytic value also has the expansion

$$
e-1=\sum_{k=1}^{\infty}\frac{1}{k!}.
$$

Let $P_N$ be the exact rational partial sum through $k=N$. Because every ratio
between successive omitted terms is at most $1/(N+2)$,

$$
0<(e-1)-P_N
\le
\frac{1}{(N+1)!}\frac{N+2}{N+1}.
$$

For $N=18$, the exact rational partial sum is below the 100-digit decimal
reference by approximately $8.6522\times10^{-18}$, while the proved remainder
bound is approximately $8.6533\times10^{-18}$. The reference lies inside the
bounded interval.

This check uses factorials, exact rational arithmetic, and a tail bound instead
of spatial samples and quadrature weights. It therefore has substantially
different failure modes from the two quadrature implementations. It still does
not validate a physical model or prove that every input to a general integration
routine is handled correctly.


## Higher precision is evidence only with a checked formulation

The activity evaluates $e-1$ at both 80 and 100 decimal digits and records their
relative change. Agreement between precisions shows that the reported decimal
reference has stabilized for this formulation. The independently bounded
series then checks the result from another direction.

When using higher precision elsewhere:

1. preserve the input information intentionally; converting an already rounded
   binary64 value does not recover its lost digits;
2. choose a formulation that is stable at the reference precision;
3. increase precision again and verify that the digits used as a reference
   remain stable;
4. seek a property, bound, or independent method when the reference calculation
   shares important code or assumptions with the candidate.

“More digits” describes an arithmetic setting, not the authority of a result.


## Assemble an evidence record, not a verdict flag

A useful record connects each claim to an observation and a limitation:

| Claim | Observation in the activity | Interpretation |
|---|---|---|
| Constant case is integrated correctly | Both candidates return $1$ | Basic accumulation passes; endpoint weights remain untested |
| Trapezoidal method is implemented | Suspicious candidate returns $0.4375$ for $\int_0^1x\,dx$ | Claim rejected by affine exactness |
| Correct quadrature error is controlled | Midpoint and trapezoidal errors approach order two | Expected asymptotic behaviour observed on tested grids |
| Integral is not method-specific | Convex bracket and bounded series contain the decimal reference | Complementary algorithms agree within stated bounds |
| A real rate model is scientifically valid | No experimental data are used | Not established by this activity |

Record the input, units, implementation revision, method parameters, reference
provenance, error metric, tolerance or bound, observed results, and unresolved
risks. Avoid collapsing the portfolio to `validated=True`; later reviewers need
to know which claims the evidence supports.


## Companion activity: building a validation portfolio

The self-paced
[validation evidence portfolio](../notebooks/07-validation-evidence.qmd)
asks you to:

1. predict why a constant reference case cannot distinguish two quadrature
   candidates;
2. use affine exactness to test the claimed trapezoidal contract;
3. apply broad bounds and explain why passing them is insufficient;
4. measure the observed refinement order of three methods;
5. bracket the unknown integral with midpoint and trapezoidal estimates;
6. check a high-precision reference with an exact rational series and remainder
   bound;
7. write a claim-evidence-limitation record.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/07-validation-evidence.qmd
```

The complete site build executes the activity and generates a downloadable
Jupyter notebook.


## Questions for reviewing validation evidence

Before accepting a scientific-computing claim, ask:

1. Is the claim about implementation, numerical error, or the model's relation
   to reality?
2. What assumptions, inputs, units, and operating range does the claim cover?
3. Why is each reference authoritative, and what does it share with the
   candidate?
4. Which invariants or properties must hold even without an exact answer?
5. What refinement trend and rate should be observed?
6. Are the compared methods independent enough to fail differently?
7. What plausible defect could pass every current check?
8. Which evidence is still missing for the intended scientific conclusion?


## Reflection questions

1. Why does the constant quadrature case fail to detect the wrong endpoint
   weights?
2. What additional information does the observed convergence order provide
   beyond a decreasing error?
3. Why is agreement between midpoint and trapezoidal quadrature weaker than
   agreement with the bounded factorial series?
4. Which evidence in this module would help validate a physical model?


## Suggested answers

1. Every sampled value is one, so several weighting and sampling schemes return
   the interval width. The case does not exercise the affine-exactness contract.
2. A decreasing error shows improvement; the order tests whether the leading
   error behaves as predicted by the claimed method. The suspicious routine
   decreases at first rather than second order.
3. The quadrature methods share the same integrand, interval, arithmetic, and
   similar loop structure. The series uses exact rational terms and a proved
   tail bound, giving it different failure modes.
4. None of the computational checks alone validates a physical model. That
   claim needs suitable experimental or observational data and a declared
   intended-use regime, possibly supplemented by sensitivity analysis.


## Takeaways

* Match evidence to a stated claim and retain its limitations.
* Separate code verification, solution verification, and model validation.
* Use exact cases and strong method properties rather than arbitrary examples.
* Predict the refinement rate before interpreting a convergence plot or table.
* Prefer comparisons whose methods, implementations, and assumptions fail
  differently.
* Check high-precision references rather than treating extra digits as truth.
* A validation portfolio supports qualified claims; it does not produce a
  universal correctness certificate.


## Connection to the next module

The evidence in this module was produced in one arithmetic and software
environment. Module 8 asks whether the supported conclusions survive changes
in compilers, libraries, hardware, optimization, parallel reduction order, and
precision, and what reproducibility level the scientific claim actually needs.
