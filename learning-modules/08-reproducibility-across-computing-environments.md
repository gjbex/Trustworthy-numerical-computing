# Module 8: Reproducibility Across Computing Environments

Scientific software may produce different low-order bits—or occasionally
different conclusions—when the compiler, library, hardware, optimization
settings, or parallel schedule changes.


## Learning outcomes

After this module, you should be able to:

* explain why floating-point reduction order affects results;
* identify compiler and hardware choices that may change arithmetic;
* distinguish bitwise repeatability from scientific reproducibility;
* design comparisons that tolerate harmless variation without hiding failures;
* record the environment needed to interpret a result.


## Sources of environmental variation

The module considers:

* instruction selection and fused operations;
* math-library implementations;
* vectorization and reassociation;
* aggressive floating-point optimization;
* thread and process reduction order;
* accelerator and mixed-precision execution.


## Levels of reproducibility

Different workflows need different guarantees:

* bitwise-identical output;
* numerically equivalent output within a justified tolerance;
* statistically equivalent output;
* the same qualitative scientific conclusion.

The strictest level is not automatically the most useful or affordable.


## Parallel reductions

Parallel execution often changes the grouping and order of operations. The
module compares deterministic reductions, reproducible algorithms, and
tolerance-based validation, including their cost and scalability trade-offs.


## Reproducibility record

Participants identify the information needed to interpret a rerun:

* source revision and input data;
* compiler, flags, and linked libraries;
* hardware and execution configuration;
* seeds and parallel decomposition;
* algorithmic tolerances and termination reason.


## Experiment

The same reduction or iterative calculation should be run with changed order,
thread count, optimization, or precision. Participants decide which differences
are harmless and what evidence supports that decision.


## Connection to the next module

Reproducibility evidence is useful only when it is reported clearly. Module 9
turns an investigation into a defensible scientific statement.
