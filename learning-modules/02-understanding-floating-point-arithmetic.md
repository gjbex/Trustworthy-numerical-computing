# Module 2: Understanding Floating-Point Arithmetic

Floating-point numbers approximate a wide dynamic range with finite storage.
Their behaviour is systematic, but it differs from arithmetic over real
numbers.


## Learning outcomes

After this module, you should be able to:

* explain sign, significand, exponent, and finite precision conceptually;
* predict when rounding occurs;
* recognize `NaN`, infinity, signed zero, and subnormal values;
* explain the causes of overflow and underflow;
* demonstrate why algebraically equivalent expressions may compute differently.


## A finite set of numbers

The module introduces representable numbers, spacing, rounding modes, and
machine epsilon without requiring participants to memorize an encoding table.
The emphasis is on consequences for scientific calculations.


## Rounding is local

Every elementary operation produces a representable result. Small local
rounding effects can cancel, accumulate, or be amplified by later operations.
Printing more decimal digits reveals a stored approximation; it does not make
the calculation more accurate.


## Exceptional values

Participants investigate:

* positive and negative infinity;
* quiet `NaN` values and their propagation;
* positive and negative zero;
* normal and subnormal numbers;
* overflow and gradual underflow.


## Algebra under finite precision

The module demonstrates that floating-point addition is not generally
associative and that distributive rearrangements may change a computed result.
These observations will later explain order-dependent sums and parallel
reproducibility.


## Experiments

Short experiments should include:

* finding the next representable value at different scales;
* observing when adding a small value has no effect;
* creating and classifying special values;
* comparing different evaluation orders.


## Connection to the next module

Knowing that two computations can differ is not enough. Module 3 establishes
ways to measure whether that difference matters.
