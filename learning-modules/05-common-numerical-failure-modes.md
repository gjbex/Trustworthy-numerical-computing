# Module 5: Common Numerical Failure Modes

Two expressions can be equal in real arithmetic yet behave very differently in
finite precision. The difference is often not mysterious: a small result is
formed by subtracting nearby values, low-order contributions are repeatedly
discarded, or an intermediate leaves the representable range before later
operations could bring it back.

These patterns recur in statistics, geometry, simulation, optimization,
probability, and data reduction. Recognizing them helps us replace “floating
point is inaccurate” with a specific diagnosis and a testable remedy.


## Learning outcomes

After this module, you should be able to:

* recognize cancellation and determine when it causes loss of significance;
* explain why reduction order changes accumulated rounding error;
* compare sequential, magnitude-ordered, pairwise, and compensated summation;
* detect overflow or underflow in intermediates even when the final result is
  representable;
* apply scaling, regrouping, specialized functions, or log-domain calculations
  to avoid a diagnosed failure mode;
* validate a reformulation with an exact reference, higher-precision result,
  invariant, or equivalent independent calculation.


## Prerequisite connection

Module 2 established binary64 spacing, rounding, finite range, normal and
subnormal values, and non-associativity. Module 3 supplied scale-aware forward
error and reference-quality distinctions. Module 4 separated problem
conditioning from algorithmic stability and implementation correctness.

This module uses all three layers. It treats a changed evaluation order or
reformulation as an algorithmic intervention, measures the result against a
stated reference, and checks whether problem sensitivity remains a separate
limitation.


## Connect arithmetic symptoms to the Module 4 diagnosis

Module 4 separated three questions:

1. Is the mathematical problem sensitive to its inputs?
2. Does the selected algorithm introduce avoidable error?
3. Does the implementation perform the intended algorithm correctly?

The failure modes in this module mainly concern the second question. A
dangerous-looking operation is not by itself proof of instability, and a stable
reformulation does not cure uncertain data or an ill-conditioned problem. For
each example, hold the mathematical input-output map fixed and compare
algorithms against a justified reference or invariant.

Use the following diagnostic sequence:

1. Predict which intermediate may lose information or leave the usable range.
2. Compute a reference or identify an invariant independently.
3. Measure the unsafe and reformulated results with the same error criterion.
4. Change the scale, order, or precision to test the proposed cause.
5. State what the experiment establishes and what it does not.


## Cancellation exposes errors hidden in nearby operands

**Cancellation** occurs when subtracting values with the same leading digits.
The leading digits disappear because they cancel mathematically. If the
operands were already rounded or uncertain, the remaining small difference may
contain few reliable digits. The subtraction did not necessarily create all of
the error; it exposed errors that were small relative to the operands but large
relative to their difference.

Cancellation is therefore not automatically catastrophic. If both operands
and their difference are represented sufficiently accurately, subtraction can
be harmless. The relevant question is whether the information needed for the
small result survived the earlier calculations.

### Example: a small exponential increment

Consider the dimensionless function

$$
f(x)=e^x-1.
$$

For small $x$, a direct implementation first rounds $e^x$ to a value near one
and then subtracts one. When $x=10^{-16}$ in binary64, the increment is too
small to survive that intermediate rounding on the tested platform:

| Method | Computed value | Relative forward error |
|---|---:|---:|
| Direct `exp(x) - 1` | $0$ | $1$ |
| Specialized `expm1(x)` | $1.0\times10^{-16}$ | approximately $7.09\times10^{-17}$ |

The reference is an 80-digit decimal evaluation of $e^x-1$, checked against a
100-digit evaluation. It is approximately
$1.00000000000000005\times10^{-16}$.

This is not evidence that the mathematical problem is severely conditioned.
Its relative condition number is

$$
\kappa_f(x)
=
\left|\frac{x f'(x)}{f(x)}\right|
=
\left|\frac{x e^x}{e^x-1}\right|,
$$

which tends to one as $x$ tends to zero. The direct algorithm loses the small
increment; the specialized formulation evaluates that increment without first
forming a rounded quantity near one.

The same design principle appears in functions such as `log1p(x)` for
$\log(1+x)$ and in the reformulated quadratic root from Module 4. Prefer a
well-tested specialized function when the language or numerical library
provides one. Otherwise derive an equivalent expression and validate it over
the intended input range. Merely increasing precision may postpone the failure
without removing the unstable structure.


## Summation is an algorithm, not a primitive fact

In real arithmetic,

$$
x_1+x_2+\cdots+x_n
$$

is independent of evaluation order. Floating-point addition is not
associative, so a reduction must choose an algorithm and an order. Every
addition rounds; contributions smaller than the current spacing may disappear,
and later cancellation cannot recover them.

For a nonzero exact sum $s=\sum_i x_i$, the quantity

$$
\kappa_{\mathrm{sum}}
=
\frac{\sum_i |x_i|}{|s|}
$$

describes sensitivity to componentwise relative changes in the inputs. A large
value warns that input uncertainty can affect the sum strongly. It does not
make all summation algorithms equivalent: for fixed representable inputs, some
orders still introduce much less arithmetic error than others.

### A controlled mixed-magnitude sum

Use the exactly representable binary64 values

$$
[10^{16},\underbrace{1,1,\ldots,1}_{10\,000\ \text{times}},-10^{16}].
$$

Their exact sum is the integer $10\,000$. The same values give:

| Method | Result | Relative forward error |
|---|---:|---:|
| Explicit left-to-right loop | $0$ | $1$ |
| Increasing-magnitude order | $10\,000$ | $0$ |
| Recursive pairwise tree | $9\,998$ | $2\times10^{-4}$ |
| Neumaier compensated sum | $10\,000$ | $0$ |
| Python `math.fsum` | $10\,000$ | $0$ |

The table is evidence for this constructed sequence, not a universal ranking.
The pairwise tree loses two units because of where this particular tree splits,
but it retains nearly all the information lost by the sequential order.
Sorting works here because the small same-sign values are combined first; it
can be expensive and is not a general cure for mixed signs.

The main options have different contracts:

* **Sequential summation** uses constant extra storage and is simple, but its
  first-order worst-case error growth is proportional to the number of terms.
* **Magnitude ordering** can help selected inputs, but sorting costs work and
  storage, and no single ordering is best for every sign pattern.
* **Pairwise summation** uses a balanced reduction tree. Its error growth is
  commonly proportional to the tree depth, about $\log_2 n$, and the tree maps
  naturally to parallel reductions.
* **Compensated summation** tracks low-order information discarded by ordinary
  additions. It often gives much better accuracy, although it costs extra
  operations and does not make every ill-conditioned sum accurate.
* **A documented library reduction** may provide stronger accuracy guarantees
  and should generally be preferred to an improvised replacement when its
  contract matches the application.

These are qualitative first-order comparisons under ordinary rounding
assumptions, not unconditional bounds. Overflow, subnormal arithmetic, input
uncertainty, or an extremely ill-conditioned sum can dominate them. For large
parallel calculations, record the reduction structure as part of the numerical
method rather than treating order as an irrelevant implementation detail.


## A representable result can have unrepresentable intermediates

Binary64 has a finite exponent range. Checking only the desired final scale is
not enough: a naive formulation can overflow or underflow before later
operations rescale the result.

### Example: a Euclidean norm

The [vectors, norms, and scaling reference](reference-vectors-norms-and-scaling.md)
defines the Euclidean or 2-norm. For $x=y=10^{308}$,

$$
\sqrt{x^2+y^2}
$$

is approximately $1.4142135623730951\times10^{308}$ and is representable in
binary64. The squares are not. A naive calculation returns infinity because
$x^2$ and $y^2$ overflow.

Scale before squaring. With

$$
m=\max(|x|,|y|),
$$

compute

$$
\sqrt{x^2+y^2}
=
m\sqrt{(x/m)^2+(y/m)^2}.
$$

The scaled formula and Python's `hypot` both return
$1.4142135623730951\times10^{308}$ in the course environment. An independent
100-digit decimal reference gives a relative forward error of approximately
$5.77\times10^{-17}$.

The invariant

$$
m\le \sqrt{x^2+y^2}\le \sqrt{2}\,m
$$

also detects the naive infinity without requiring the exact result. For longer
vectors, use a tested scaled norm implementation rather than extending this
two-component sketch without analysis.


## Underflow can erase a result before later rescaling

Binary64 gradually loses relative precision below its smallest normal positive
value, approximately $2.225\times10^{-308}$, and reaches zero below its
smallest positive subnormal, approximately $4.941\times10^{-324}$. An
intermediate can therefore become inaccurate or zero even when the complete
expression has a normal, representable value.

Consider

$$
10^{-200}\times10^{-200}\times10^{200}=10^{-200}.
$$

The left-associated binary64 expression underflows before the rescaling:

| Evaluation | Binary64 result | Relative forward error |
|---|---:|---:|
| $(10^{-200}\times10^{-200})\times10^{200}$ | $0$ | $1$ |
| $10^{-200}\times(10^{-200}\times10^{200})$ | $1.0\times10^{-200}$ | approximately $1.79\times10^{-17}$ |

Regrouping works for these particular scales, but it can move rather than
remove the range problem. A general product may track mantissas and exponents
separately or rescale in blocks.

For products of positive probabilities or likelihoods, the log domain is often
the natural representation:

$$
\log\left(\prod_i p_i\right)=\sum_i \log p_i.
$$

For example, $10^{-200}\times10^{-200}=10^{-400}$ and
$10^{-200}\times10^{-201}=10^{-401}$ both round to zero in binary64. Their log
values remain finite and differ by $\log(10)$, so the larger likelihood can
still be identified. Exponentiating the log may still underflow; the benefit is
that comparison and normalization can often be performed without doing so.
Zeros, signs, and invalid probabilities need explicit handling.


## Match the remedy to the failed operation

| Observed pattern | Diagnostic experiment | Candidate remedy | Important limitation |
|---|---|---|---|
| Nearby values are subtracted | Sweep the separation and compare with a high-precision reference | Algebraic reformulation or a specialized function | Does not restore uncertainty already present in the operands |
| Small terms vanish in a long sum | Permute a fixed input and compare reduction algorithms | Pairwise, compensated, blocked, or documented library reduction | Input conditioning and parallel order still matter |
| A finite expected result becomes infinity | Inspect intermediate magnitudes and check bounds | Scale before powers, products, or norms | Scaling must cover the full input range |
| A nonzero expected result becomes zero | Inspect normal and subnormal ranges; regroup once | Rescale, separate exponent and mantissa, or use logs | The final requested representation may itself be impossible |
| Equivalent orders disagree | Hold inputs fixed and record each evaluation tree | Select and document a stable order | Algebraic equivalence does not imply bitwise equivalence |

Do not replace all of these diagnoses with “use more precision.” Higher
precision is a useful experiment and sometimes a valid requirement, but a
stable formulation generally uses the available precision more effectively and
makes the numerical intent clearer.


## Companion activity: a failure-mode laboratory

The self-paced
[failure-mode laboratory](../notebooks/05-failure-mode-lab.qmd) asks you to
predict and then measure:

1. when `exp(x) - 1` loses the small increment;
2. how five summation strategies treat the same exact input sequence;
3. why a naive norm overflows while a scaled norm remains finite;
4. how multiplication order changes an underflowing intermediate;
5. how log-domain likelihoods preserve a comparison after direct products
   become zero.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/05-failure-mode-lab.qmd
```

The complete site build executes the activity and generates a downloadable
Jupyter notebook.


## What the evidence establishes

The cancellation reference is recomputed at two precisions, and the integer
sum is exact. The norm is checked against both a high-precision value and an
independent range invariant. These checks support the intended diagnosis for
the selected inputs.

They do not prove that every call to `expm1`, compensated summation, `hypot`, or
a log-domain formulation is accurate over its complete domain. Library
implementations and edge-case handling can differ. The examples also do not
separate arithmetic error from uncertainty in real measurements; their inputs
are controlled numerical data chosen to isolate one effect at a time.


## Questions to ask during diagnosis

* Which intermediate first loses significant information?
* Is the exact mathematical problem well-conditioned at this input?
* Which values and units determine a meaningful error scale?
* Does changing only the evaluation order change the conclusion?
* Can scaling keep every intermediate in the normal finite range?
* Does a specialized operation expose the desired small quantity directly?
* Which reference or invariant is independent of the unsafe formulation?
* Does the remedy work across the complete intended input range?


## Reflection questions

1. Why can subtracting two accurately computed values still produce a result
   with few reliable relative digits?
2. What evidence shows that `exp(x) - 1` fails algorithmically near zero rather
   than because $e^x-1$ is severely conditioned there?
3. Why is pairwise summation attractive for parallel reduction even though it
   does not return the exact result in the constructed example?
4. What does $\kappa_{\mathrm{sum}}$ add to a comparison of summation
   algorithms?
5. Why does the expected scale of a final norm not rule out overflow?
6. Why is regrouping the underflowing product useful evidence but not a general
   product algorithm?
7. What can be learned from two likelihoods whose direct products both
   underflow to zero?
8. When is increasing precision an appropriate remedy, and what can it not
   repair?

::: {.callout-note collapse="true"}
## Suggested answers

1. Their absolute errors may be small relative to the operands but large
   relative to the small difference. Cancellation removes the shared leading
   digits and exposes those errors.
2. The relative condition number tends to one, while a specialized evaluation
   of the same mathematical function agrees with the high-precision reference.
   Holding the problem fixed isolates the direct formulation.
3. A balanced tree reduces error growth and exposes independent branches that
   can be evaluated concurrently. It improved the error from one to
   $2\times10^{-4}$ here; pairwise does not promise exact summation.
4. It quantifies sensitivity of the exact sum to input perturbations. A better
   algorithm can reduce arithmetic error but cannot remove uncertainty implied
   by a large condition number.
5. Squaring occurs before the final square root. The squares can exceed the
   finite range even when the square root of their sum would be representable.
6. It demonstrates that the zero arose from an avoidable intermediate. Other
   exponent combinations can make the alternative grouping overflow or
   underflow, so a general method needs systematic scaling.
7. Their log values preserve their ordering and log-ratio even though the
   original binary64 representation cannot distinguish the products.
8. More precision is appropriate when the accuracy requirement and input
   quality justify it or as a diagnostic comparison. It cannot recover
   measurement information that was never present, cure ill-conditioning, or
   replace a more stable formulation by itself.
:::


## Takeaways

* Cancellation is dangerous when the desired small result depends on digits
  already lost from nearby operands.
* Summation has an evaluation tree; order, compensation, and input conditioning
  all affect what can be claimed about the result.
* Scale intermediate calculations, not just outputs, to avoid preventable
  overflow and underflow.
* Regrouping, specialized functions, compensated reductions, and log-domain
  representations are targeted remedies rather than universal recipes.
* Validate a reformulation with a reference or invariant and state the input
  range over which the evidence applies.


## Connection to the next module

Many scientific algorithms repeat reductions, updates, and residual
calculations until a stopping condition is met. A tiny update may indicate
convergence, or it may mean that rounding has erased further progress.
[Module 6: Iterative Algorithms And Convergence](06-iterative-algorithms-and-convergence.md)
uses the failure modes from this module to distinguish genuine convergence,
stagnation, divergence, and false termination.
