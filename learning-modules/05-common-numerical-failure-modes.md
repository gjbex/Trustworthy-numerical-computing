# Module 5: Common Numerical Failure Modes

Numerical failures often follow recognizable patterns. Learning these patterns
makes suspicious results easier to diagnose and robust alternatives easier to
select.


## Learning outcomes

After this module, you should be able to:

* recognize catastrophic cancellation and loss of significance;
* explain how rounding error accumulates in long reductions;
* compare naive, pairwise, and compensated summation;
* reformulate expressions to reduce overflow or underflow risk;
* identify calculations whose result depends strongly on evaluation order.


## Cancellation

Subtracting nearly equal quantities can discard the leading digits that the
operands share. Cancellation is especially damaging when earlier rounding or
measurement uncertainty already affects the remaining digits.


## Accumulation and reduction order

Long sums combine values with different signs and magnitudes. Participants
compare sequential, sorted, pairwise, and compensated approaches and consider
their accuracy, cost, and parallel suitability.


## Scaling and range

Intermediate values can overflow even when the final mathematical result is
representable. Conversely, products of small values can underflow. Scaling,
factoring, and specialized formulations such as log-domain calculations can
keep intermediates in a safer range.


## Stable reformulations

The goal is not to memorize isolated tricks. For each failure, participants
will ask:

1. Which information is being lost?
2. At what scale does the loss occur?
3. Can an equivalent expression avoid the dangerous operation?
4. What independent check shows that the reformulation helped?


## Experiments

Candidate experiments include a quadratic formula near a repeated root, variance
from raw moments, summation with mixed magnitudes, and a norm calculation that
overflows before the square root.


## Connection to the next module

Many scientific algorithms repeat an update until a stopping condition is met.
Module 6 examines how the same failure modes affect convergence decisions.
