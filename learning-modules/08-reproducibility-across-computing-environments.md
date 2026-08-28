# Module 8: Reproducibility Across Computing Environments

Two executions can use the same source code and input data yet produce different
floating-point results. A compiler may contract two operations into one fused
operation. A library may use another approximation to a transcendental function.
A parallel reduction may combine partial sums in a different tree. A processor
or accelerator may use another precision for an intermediate.

The difference may be one harmless low-order bit, evidence of an unstable or
ill-conditioned calculation, or large enough to reverse the scientific
conclusion. Reproducibility is therefore not a demand that every byte always be
identical. It is a claim about which changes are allowed, what agreement is
required, and which evidence shows that the result remains fit for its intended
use.

This module develops that claim through two controlled energy-aggregation
examples. The first loses bitwise identity while easily satisfying its numerical
and scientific requirements. The second is a cancellation-sensitive balance in
which legal changes of reduction order or precision can change the conclusion.


## Learning outcomes

After this module, you should be able to:

* distinguish repeatability, bitwise reproducibility, numerical agreement,
  statistical equivalence, and conclusion reproducibility;
* identify compiler, library, hardware, precision, and parallel-execution
  choices that can change floating-point evaluation;
* distinguish input storage, elementary-operation, accumulator, and output
  formats in a mixed-precision execution policy;
* predict when a reduction-order change is likely to be harmless or
  consequential;
* define a reproducibility contract with a justified comparison criterion;
* design a controlled environment matrix that changes one relevant factor at a
  time;
* record the source, inputs, environment, algorithm, and execution settings
  needed to interpret a rerun;
* report which conclusions survive the tested changes and which remain
  unverified.


## Prerequisite connection

Module 2 established that floating-point arithmetic is rounded and not
associative. Module 3 introduced scale-aware comparisons and justified
tolerances. Module 4 separated problem conditioning from algorithmic stability,
and Module 5 treated summation order as an algorithmic choice. Module 6 showed
that execution details and tolerances belong in a convergence record. Module 7
assembled complementary evidence into a validation portfolio.

That portfolio was produced in one software and arithmetic environment. Module
8 asks whether its supported claims survive the environment changes that matter
for the intended scientific use. It does not assume that every change must
preserve every bit.


## State the reproducibility claim before comparing runs

Terminology varies between fields, so define the operational claim rather than
relying on one word:

| Reproducibility level | Required agreement | Appropriate evidence | Example use |
|---|---|---|---|
| **Repeatability** | The same setup can rerun the calculation under declared conditions | Recorded inputs, configuration, seed, environment, and repeated execution | Debugging a reported failure |
| **Bitwise identity** | Serialized numerical outputs are identical bit for bit | Exact comparison after controlling formats, order, libraries, and relevant environment state | Checkpoint restart or a strict regression artifact |
| **Numerical agreement** | Quantities agree under a justified metric and tolerance | Absolute, relative, mixed, norm-based, or domain-specific comparison | A deterministic solver result with harmless low-order variation |
| **Statistical equivalence** | Distributions or summary properties agree within a declared statistical criterion | Replicated runs, uncertainty intervals, distributional tests, and power analysis | Monte Carlo or stochastic optimization |
| **Conclusion reproducibility** | The same scientific classification or decision follows | A stable decision margin plus evidence that numerical differences do not cross it | Whether a conservation requirement or safety threshold is met |

These levels are not a ranking from bad to good. Bitwise identity can be required
for an exact restart while statistical equivalence is the meaningful contract
for an ensemble calculation. Conversely, two outputs can support the same
conclusion while differing too much to satisfy the numerical accuracy
requirement.

Choose the weakest contract that fully supports the intended use, then test that
contract directly. A weaker contract must not be used merely because a stricter
and scientifically necessary test failed.


## Environment changes alter arithmetic through identifiable mechanisms

An environment label such as “another machine” is too vague for diagnosis.
Record and control the mechanism that can affect the computation:

| Changed factor | Possible numerical mechanism | Useful controlled comparison |
|---|---|---|
| Compiler and flags | Reassociation, contraction, reciprocal approximations, or treatment of exceptional values | Same source and inputs with one flag set changed |
| CPU or accelerator | Different instruction sets, intermediate precision, subnormal handling, or fused operations | Same executable contract on named hardware targets |
| Math library | Different algorithms and accuracy guarantees for functions such as `exp`, `sin`, or linear algebra kernels | Same stored inputs with library and version recorded |
| Vector width | A different grouping of lanes and partial reductions | Scalar, vectorized, and fixed-tree runs |
| Threads or processes | A different partition and reduction tree | Sweep thread or rank count while holding the global data fixed |
| Precision policy | Different storage, accumulation, or mixed-precision choices | Declare each operand and accumulator precision |
| Random-number implementation | Different generator, stream partition, or consumption order | Record generator family, version, seed, and stream mapping |

Ordinary source-level equivalence does not guarantee identical floating-point
evaluation. For example, a fused multiply-add evaluates $ab+c$ with one final
rounding, whereas separate multiplication and addition normally round twice.
Both can be legitimate implementations of a real-arithmetic expression, yet
their binary results can differ.

Aggressive optimization can also permit transformations that are invalid under
strict IEEE-style expression order. Do not describe a flag as merely “faster”:
record the arithmetic freedoms it enables and revalidate the affected claims.


## A changed bit is evidence, not automatically a defect

When two environments disagree, first classify the observation:

1. Are the inputs, configuration, algorithm, stopping reason, and output quantity
   actually the same?
2. Is the difference a permitted consequence of evaluation order, precision, or
   a declared library contract?
3. Does the difference pass the predeclared numerical comparison?
4. Does it preserve the scientific conclusion and its margin?
5. Is the observed variation consistent across a wider environment matrix, or
   was only one convenient pair tested?

A bitwise difference can be harmless under a tolerance-based contract. A
bitwise-identical result can still be scientifically wrong because every run
uses the same defective method or model. Reproducibility complements the
validation evidence from Module 7; it does not replace it.

Non-finite values require explicit classification. `NaN` and infinity must not
pass a tolerance check because an ordinary subtraction or comparison happened
to return false. Signed zero and `NaN` payloads also need deliberate treatment
when the claim is bitwise identity.


## Controlled case 1: different bits, same supported claim

Suppose a calibration workflow aggregates 10,000 positive energy corrections

$$
b_k=\frac{1}{k}\ \mathrm{J},\qquad k=1,\ldots,10{,}000.
$$

The stored inputs are binary64 approximations to these fractions. The numerical
question is the sum of those stored values, not the exact real harmonic sum. An
exact rational sum of the stored binary64 inputs supplies the arithmetic
reference:

$$
B_{\mathrm{ref}}=9.787606036044382\ \mathrm{J}
$$

when rounded to binary64.

The downstream report rounds energy to the nearest $10^{-9}\ \mathrm{J}$. The
workflow allocates one tenth of that unit to reduction error, so the declared
absolute acceptance criterion is

$$
|B-B_{\mathrm{ref}}|\le 10^{-10}\ \mathrm{J}.
$$

The scientific classification is whether the aggregate exceeds
$9.5\ \mathrm{J}$. Using the same explicit left-to-right binary64 accumulator,
three serial orders produce:

| Order | Computed total (J) | Binary64 representation | Absolute error (J) |
|---|---:|---|---:|
| Original | $9.787606036044348$ | `0x1.39341192de2a6p+3` | $3.40\times10^{-14}$ |
| Reverse | $9.787606036044386$ | `0x1.39341192de2bbp+3` | $3.29\times10^{-15}$ |
| Increasing magnitude | $9.787606036044386$ | `0x1.39341192de2bbp+3` | $3.29\times10^{-15}$ |

Bitwise identity fails, but every result passes the $10^{-10}\ \mathrm{J}$
criterion and remains above $9.5\ \mathrm{J}$. The supported claim is
numerically and scientifically reproducible across these orders. This evidence
does not establish identical results on every compiler, library, or processor.


## Controlled case 2: the conclusion changes

Now consider a dimensionless teaching representation of an energy ledger whose
entries are expressed in joules:

* one source contributes $+2^{53}\ \mathrm{J}$;
* one sink contributes $-2^{53}\ \mathrm{J}$;
* 4,096 smaller sources each contribute $0.5\ \mathrm{J}$.

The exact sum of the stored inputs is

$$
E_{\mathrm{ref}}=2048\ \mathrm{J}.
$$

The operational requirement classifies the balance as acceptable only when
$|E|\le100\ \mathrm{J}$. The audit reserves one percent of that limit for
reduction error, giving the numerical criterion
$|E-E_{\mathrm{ref}}|\le1\ \mathrm{J}$. The exact stored-input reference
therefore says that the imbalance is material.

At $2^{53}$, adjacent binary64 values are $2\ \mathrm{J}$ apart. Adding each
$0.5\ \mathrm{J}$ contribution separately to the large source cannot change
the stored accumulator. Legal evaluation orders then produce:

| Evaluation strategy | Computed net energy (J) | Numerical criterion $|E-E_{\mathrm{ref}}|\le1\ \mathrm{J}$ | Scientific classification |
|---|---:|---|---|
| Large source, small terms, large sink | $0$ | Fails | Acceptable balance—wrong conclusion |
| Large source, large sink, small terms | $2048$ | Passes | Material imbalance |
| Small terms, large source, large sink | $2048$ | Passes | Material imbalance |
| Accurate summation checked against exact rational arithmetic | $2048$ | Passes | Material imbalance |

The first result is finite, deterministic, and plausible. None of those
properties makes it adequate. It fails the numerical criterion and reverses the
scientific classification.

The summation condition indicator

$$
\kappa_{\mathrm{sum}}=
\frac{\sum_i |x_i|}{\left|\sum_i x_i\right|}
\approx 8.80\times10^{12}
$$

warns that small relative perturbations of the terms or arithmetic can be
amplified strongly in the small net result. That sensitivity does not excuse the
wrong conclusion; it explains why reduction design, precision, and an
independent reference matter.


## Parallel reductions are numerical algorithms

A parallel reduction partitions the data, reduces each partition, and combines
the partial results. Thread count, rank count, work scheduling, and accelerator
launch geometry can change both stages. They therefore change the numerical
algorithm even when the source contains one call named `sum`.

For the cancellation-sensitive ledger in its listed order, a simple contiguous
chunk simulation uses the same explicit serial accumulator within and across
chunks and gives:

| Number of chunks | Computed net energy (J) | Absolute error (J) | Classification |
|---:|---:|---:|---|
| 1 | $0$ | $2048$ | Acceptable balance—wrong conclusion |
| 2 | $1024$ | $1024$ | Material imbalance |
| 4 | $1536$ | $512$ | Material imbalance |
| 8 | $1792$ | $256$ | Material imbalance |
| 16 | $1920$ | $128$ | Material imbalance |

The apparent improvement is not guaranteed to continue monotonically for every
partition count or data layout. A different tree can lose a different set of
small contributions.

Common strategies serve different contracts:

| Strategy | Benefit | Limitation |
|---|---|---|
| Fixed partition and reduction tree | Can make one execution configuration deterministic | May still be inaccurate and may not remain identical across compilers or hardware |
| Pairwise or compensated reduction | Usually reduces accumulation error | Does not guarantee bitwise identity or cure ill-conditioned input data |
| Long or exact accumulator | Can provide highly accurate or reproducible sums | Extra memory, communication, implementation complexity, or runtime cost |
| Tolerance-based comparison | Accepts harmless variation tied to the scientific requirement | Unsafe if the tolerance is unjustified or hides a changed conclusion |

Deterministic is not synonymous with accurate. Reproducible algorithms should
be checked against a meaningful reference or invariant, not accepted only
because they return the same bits repeatedly.


## Precision is part of the execution contract

“Using double precision” is incomplete when inputs, products, accumulators, and
library kernels can use different formats. Mixed-precision hardware may store
values in one format, multiply in another, and accumulate in a third. Some
processors retain wider intermediates; others round them earlier.

Likewise, “the processor supports 16-bit floating point” is not a complete
numerical claim. Binary16 and bfloat16 have different range and spacing, as
Module 2 showed. Hardware or a library may support a format only for storage and
conversion, for a specialized dot product or matrix operation, or for a wider
set of arithmetic operations. Even a supported multiplication may feed a wider
accumulator rather than round each partial sum to the input format.

Record the complete arithmetic path:

| Component | Question to answer |
|---|---|
| Input and storage | Which format receives each input conversion and stores intermediate arrays? |
| Elementary operations | In which format are products, sums, fused operations, and library kernels defined? |
| Accumulation | Which format holds partial sums, dot products, and reduction nodes, and when are they rounded? |
| Output conversion | Which format is returned or written, and which conversion and rounding rule is applied? |

The datatype visible in source code may be only one part of this path. A value
can also be held in a wider language container after it has already been rounded
to a narrower arithmetic format. Report the arithmetic value and the container
separately when that distinction matters.

In the companion activity, a small standard-library emulator rounds every
addition to binary32. It is not a performance or hardware model. It isolates the
effect of a narrower accumulator under controlled orders:

| Order | Binary64 serial sum (J) | Binary32-rounded serial sum (J) |
|---|---:|---:|
| Large source, small terms, large sink | $0$ | $0$ |
| Large source, large sink, small terms | $2048$ | $2048$ |
| Small terms, large source, large sink | $2048$ | $0$ |

The third order preserves the small total in binary64 but loses it when the
accumulator is rounded to binary32. Record the precision of each important
operation rather than only the input datatype.

Reduced precision can lower storage and data-movement costs and can provide
higher arithmetic throughput on suitable hardware. It may also require
conversions, scaling, wider accumulation, refinement, or rejected computations
to meet an accuracy requirement. Treat performance and numerical adequacy as
separate measured claims; neither follows from a format name.


## Compiler and library controls have limits

Strict floating-point modes can restrict reassociation, contraction, or
exception handling. Reproducible math libraries and deterministic reduction
implementations can narrow variation further. These controls can be necessary
when a contract requires exact restarts or forensic debugging.

They are not universal certificates:

* a compiler flag can have different scope or meaning across toolchains;
* a strict expression order does not standardize every transcendental function;
* a fixed reduction tree can reproduce an inaccurate answer;
* a bitwise contract can be broken by serialization, endianness, `NaN` payloads,
  or changes outside arithmetic;
* disabling useful transformations can impose performance and scalability
  costs.

Document the tested toolchain and verify the resulting executable behaviour.
Do not infer a cross-platform guarantee from a flag name alone.


## Stochastic computations need a statistical contract

An explicit seed is necessary for rerunning many stochastic examples, but a seed
does not by itself define a portable random sequence. Generator families,
library versions, thread counts, and stream-partition strategies can change
which variates are consumed.

If the exact sequence is part of the claim, record the generator, algorithm,
version, seed, and stream mapping and test the sequence explicitly. If the
scientific claim concerns an estimated distribution or expectation, compare the
relevant statistical properties across replicated runs. State the sample size,
uncertainty interval, test statistic, and power or practical effect size. One
matching seeded run is not evidence of statistical equivalence.


## Design an environment matrix that diagnoses causes

A useful matrix begins with one validated baseline and changes one relevant
factor at a time:

| Run | Source and input | Changed factor | Quantities to record |
|---|---|---|---|
| Baseline | Fixed revision and input fingerprint | None | Result, diagnostics, termination reason, environment |
| Order comparison | Same | Serial order or reduction tree | Result bits, error, decision margin |
| Parallel comparison | Same | Thread/rank count and partition | Result, partial-reduction metadata, runtime configuration |
| Precision comparison | Same | Storage or accumulator precision | Result, error, non-finite states, conclusion |
| Toolchain comparison | Same | Compiler, flags, library, or hardware | Versioned environment plus the same validation evidence |

If several factors change together, the comparison can reveal a portability
problem but not identify its cause. Reduce the difference to a controlled case
before attributing it to a compiler or processor.

Test at least one benign case and one revealing edge case. A matrix containing
only well-conditioned inputs can miss a consequential order sensitivity; a
matrix containing only a contrived failure cannot establish behaviour in the
intended operating range.


## Keep a reproducibility record with the result

Record enough information to recreate the claim and interpret differences:

* source revision, dirty-state status, build recipe, compiler, and flags;
* input identifiers, units, valid range, preprocessing, and content fingerprint;
* algorithm, important numerical options, precision policy, and stopping reason;
* runtime, numerical libraries, and relevant library versions;
* CPU or accelerator type and arithmetic modes that affect the claim;
* thread and process counts, affinity, decomposition, and reduction strategy;
* random generator, seed, and stream partition for stochastic work;
* output quantity, reference provenance, comparison metric, tolerance rationale,
  observed difference, and scientific classification.

A complete package inventory can aid forensics, but it is not a substitute for
identifying the factors that affect the claim. Avoid recording hostnames,
credentials, or machine-local paths in a public artifact.

The record should distinguish “not observed in the tested matrix” from “proved
impossible.” A result reproduced on two machines is evidence about those two
configurations, not every future platform.


## Interpret the matrix against the declared contract

| Observation | Interpretation |
|---|---|
| Bits differ, numerical criterion passes, conclusion is unchanged | Acceptable only when bitwise identity was not required |
| Numerical criterion fails, conclusion is unchanged | Scientific classification survived, but numerical reproducibility did not; investigate before accepting the result |
| Conclusion changes | The scientific claim is not reproducible over the tested change |
| Every tested output is identical | Supports bitwise identity over the tested matrix, not over unspecified environments |
| A run returns `NaN`, infinity, or a different termination reason | Treat as a categorical difference requiring diagnosis, not an ordinary tolerance comparison |

Preserve the individual observations. A single `reproducible=True` flag loses
which contract was tested, which environments were covered, and how close the
result came to changing the conclusion.


## Companion activity: testing a reproducibility contract

The self-paced
[environment variation and reproducibility](../notebooks/08-environment-reproducibility.qmd)
activity asks you to:

1. fingerprint deterministic binary64 inputs and record a portable environment
   summary;
2. compare low-order differences for a well-conditioned positive reduction;
3. test bitwise, numerical, and conclusion-level contracts separately;
4. expose a cancellation-sensitive energy balance with controlled orders;
5. simulate several parallel reduction trees and a binary32 accumulator;
6. change one partition parameter and interpret the result;
7. assemble a claim-environment-observation-limitation record.

Preview the authoritative Quarto source from the repository root with:

```bash
quarto preview notebooks/08-environment-reproducibility.qmd
```

The complete site build executes the activity and generates a downloadable
Jupyter notebook.


## Questions for reviewing a reproducibility claim

Before accepting a cross-environment result, ask:

1. Which output quantity and scientific claim are being compared?
2. Is the required contract bitwise, numerical, statistical, or
   conclusion-level agreement?
3. Which metric, tolerance, or statistical criterion represents the intended
   use, and why?
4. Were source revision, inputs, configuration, and algorithm held fixed?
5. Which compiler, library, hardware, precision, or parallel factor changed?
6. Did every run terminate normally with finite diagnostics?
7. Does the tested matrix include a revealing edge case as well as an ordinary
   case?
8. Which untested environment change could still alter the conclusion?


## Reflection questions

1. Why are the three calibration totals not bitwise reproducible even though
   they are numerically adequate?
2. Why does the zero-valued energy balance look plausible, and which evidence
   rejects it?
3. Why can changing the number of chunks change a parallel reduction result?
4. Why is a fixed reduction tree insufficient evidence of numerical accuracy?
5. What must accompany a seed when exact stochastic sequences matter?
6. Which reproducibility level should be required for a checkpoint restart, and
   which might be appropriate for a Monte Carlo estimate?
7. Why is “bfloat16 inputs” insufficient to reproduce a mixed-precision matrix
   calculation?


::: {.callout-note collapse="true"}
## Suggested answers

1. Floating-point addition is not associative, so the orders group rounding
   differently. Their errors are nevertheless far below the declared
   $10^{-10}\ \mathrm{J}$ budget and all remain above the $9.5\ \mathrm{J}$
   decision threshold.
2. Zero is finite and appears to describe perfect cancellation. The exact sum of
   the stored inputs is $2048\ \mathrm{J}$, the zero result fails the
   $1\ \mathrm{J}$ numerical criterion, and it reverses the $100\ \mathrm{J}$
   balance classification.
3. Each chunk forms a different partial sum, and the partial sums are then
   combined in another order. Changing the partition changes both groupings.
4. A fixed tree can return the same rounded result repeatedly while losing the
   same contributions every time. Accuracy still needs a reference, invariant,
   bound, or independently justified algorithm.
5. Record the generator family and algorithm, library version, seed, and mapping
   of streams or counters to threads, processes, or tasks.
6. A checkpoint restart can require bitwise identity when the exact state must
   continue. A Monte Carlo estimate normally needs a statistical-equivalence
   contract tied to uncertainty and practical effect size rather than an
   identical random sequence.
7. It does not state the operation and accumulator formats, when partial results
   round, whether operations are fused, or the output conversion. Different
   policies can use the same stored inputs yet produce different results.
:::


## Takeaways

* Define reproducibility as a testable contract for an intended use.
* Bitwise differences can be harmless, while repeated identical answers can be
  consistently wrong.
* Parallel partitions, reduction trees, and accumulator precision are numerical
  algorithm choices.
* A format name does not define a mixed-precision execution policy; record
  input, operation, accumulator, and output formats separately.
* Compare finite diagnostics, numerical error, and the scientific decision—not
  only serialized output bits.
* Change one environment factor at a time and include both ordinary and
  revealing cases.
* Record source, input, algorithm, environment, execution settings, observed
  variability, and limitations together.


## Connection to the next module

Reproducibility evidence becomes useful to collaborators and reviewers only when
its claim, comparison criterion, tested environments, and limitations are stated
clearly.
[Module 9: Communicating Numerical Reliability](09-communicating-numerical-reliability.md)
turns that evidence into a concise, qualified scientific statement.
