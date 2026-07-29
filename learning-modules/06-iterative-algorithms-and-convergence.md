# Module 6: Iterative Algorithms And Convergence

Iterative algorithms do not arrive with a self-evident stopping point. A
defensible termination rule must connect observable quantities to the accuracy
required by the problem.


## Learning outcomes

After this module, you should be able to:

* distinguish error, residual, and update size;
* combine absolute and relative stopping criteria;
* recognize stagnation, divergence, and false convergence;
* define maximum-iteration and failure policies;
* record convergence evidence suitable for later review.


## What can be observed?

The true error is often unavailable during an iteration. Algorithms therefore
monitor proxies such as residual norms, successive updates, constraint
violations, or conserved quantities. Each proxy needs a justified relationship
to the desired result.


## Stopping criteria

Participants compare rules based on:

* absolute residual;
* relative residual;
* scaled update size;
* multiple simultaneous criteria;
* problem-specific invariants or objectives.

A robust algorithm also reports why it stopped.


## Failure to converge

Termination because an update rounded to zero is not the same as convergence.
The module examines oscillation, slow convergence, stagnation, non-finite
values, and exhausted iteration budgets.


## Convergence studies

Changing an iteration tolerance is informative only when other sources of error
are understood. Participants compare solver convergence with discretization
refinement and learn to avoid spending work on accuracy that the model or data
cannot support.


## Experiment

A small root-finding or linear-solver example will compare several stopping
rules and record the iteration count, residual, estimated error, and termination
reason.


## Connection to the next module

Convergence evidence is one part of validation. Module 7 assembles it with
independent checks into a stronger scientific argument.
