# Optional Advanced Topics

These topics extend the core workflow. They should be introduced after
participants can distinguish conditioning, stability, validation, and
reproducibility.


## Future module idea: mixed-precision computation

A future optional module could teach participants to design and validate a
precision policy rather than merely replace one datatype with another. It
should remain after the complete core path because learners first need error
measures, conditioning, stability, validation evidence, reproducibility
contracts, and qualified reporting.

Candidate learning outcomes are to:

* distinguish input, storage, product, accumulator, refinement, and output
  precision;
* choose binary16, bfloat16, binary32, binary64, or a mixed policy from range
  and accuracy requirements rather than storage width alone;
* identify scaling, overflow, underflow, cancellation, and stagnation risks
  introduced by reduced precision;
* evaluate techniques such as wider accumulation, loss scaling, residual
  correction, and iterative refinement without treating them as automatic
  guarantees;
* validate numerical adequacy and performance benefit as separate claims on a
  declared hardware and software environment.

A suitable investigation would compare several precision policies on an
ordinary case and a deliberately revealing case. Participants would predict
failure, establish a binary64 or independently justified reference, record the
complete arithmetic path, measure error against a scientific requirement, and
measure performance only where the named environment supports a fair test.
The durable objective would be reasoning about precision policies; current
accelerator APIs and format catalogues should remain supporting examples rather
than the organizing principle.


## Arbitrary precision and interval arithmetic

Using higher precision as an investigative tool and intervals as bounds, while
understanding their cost and limitations.


## Numerical linear algebra

Condition estimation, rank decisions, pivoting, scaling, iterative refinement,
and residual-based diagnostics.


## Stochastic algorithms

Seeds, ensembles, statistical tests, uncertainty in estimated quantities, and
statistical rather than bitwise reproducibility.


## Accelerator and distributed computing

Reduction order, fused operations, device-specific precision, compiler flags,
communication topology, and scalable reproducibility strategies.


## Domain-specific case studies

The general workflow can be applied to simulation, optimization, data analysis,
signal processing, computational chemistry, machine learning, and other
institute-relevant domains.
