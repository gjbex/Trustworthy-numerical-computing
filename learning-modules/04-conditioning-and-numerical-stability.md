# Module 4: Conditioning And Numerical Stability

Some problems are intrinsically sensitive to small changes in their inputs.
Others admit reliable solutions but are solved poorly by a particular
algorithm. This distinction guides useful remedies.


## Learning outcomes

After this module, you should be able to:

* describe conditioning as input-to-output sensitivity;
* distinguish conditioning from numerical stability;
* interpret forward error, backward error, and residuals;
* avoid blaming finite precision for an ill-conditioned problem;
* choose an investigation based on the type of error observed.


## Problem sensitivity

A well-conditioned problem changes modestly when its inputs change modestly. An
ill-conditioned problem may amplify input uncertainty or rounding so strongly
that the requested accuracy is unattainable.


## Algorithmic stability

A stable algorithm approximately solves a nearby problem. An unstable algorithm
can introduce much larger error than the problem's conditioning predicts.
Comparing mathematically equivalent algorithms reveals why formulation matters.


## Forward error, backward error, and residual

These measures answer different questions:

* forward error compares the computed result with the desired result;
* backward error asks what nearby input would make the computed result exact;
* a residual measures how well the computed result satisfies an equation.

A small residual does not automatically imply a small forward error when a
problem is ill-conditioned.


## Investigation pattern

Participants learn to:

1. perturb inputs deliberately;
2. compare algorithms or precisions;
3. estimate sensitivity;
4. inspect residuals and invariants;
5. decide whether to reformulate the problem, change the algorithm, or revise
   the expected accuracy.


## Connection to the next module

Module 5 applies the conditioning-and-stability distinction to recurring
finite-precision failure modes.
