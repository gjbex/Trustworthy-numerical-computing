# Module 7: Validating Scientific Computations

Validation is an argument supported by several kinds of evidence. No single
test can show that every relevant aspect of a scientific computation is
correct.


## Learning outcomes

After this module, you should be able to:

* distinguish verification of an implementation from validation of a model;
* select reference cases, invariants, and properties;
* design refinement and convergence studies;
* use an independent method or higher precision effectively;
* assemble complementary checks instead of relying on one oracle.


## Reference cases

Useful references include exact solutions, analytically tractable limits,
manufactured solutions, published benchmarks, high-precision calculations, and
trusted experimental data. Each establishes a different kind of confidence.


## Invariants and properties

When an exact answer is unavailable, participants can still test conservation
laws, symmetry, bounds, monotonicity, dimensional consistency, reversibility,
and other properties implied by the problem.


## Cross-method validation

Agreement between independent implementations or algorithms is stronger than
agreement between two versions sharing the same assumptions and defects. The
module discusses how to make comparisons genuinely independent.


## Refinement studies

Participants vary resolution, timestep, tolerance, or precision and examine the
observed trend. A convincing study explains what should converge, at what rate,
and over which regime.


## A validation matrix

For a chosen computation, participants map claims to evidence:

| Claim | Evidence |
|---|---|
| implementation follows the equations | focused tests and manufactured cases |
| important properties are preserved | invariants and bounds |
| approximation error is controlled | refinement study |
| result is not method-specific | independent algorithm |
| conclusion is robust | sensitivity analysis |


## Connection to the next module

Module 8 asks whether the validation evidence survives realistic changes in the
computing environment.
