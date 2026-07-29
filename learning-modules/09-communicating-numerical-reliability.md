# Module 9: Communicating Numerical Reliability

A trustworthy numerical result includes enough context for another person to
understand the claim, the evidence, and the remaining limitations.


## Learning outcomes

After this module, you should be able to:

* separate numerical error from input, modelling, and measurement uncertainty;
* justify reported digits and tolerance choices;
* summarize convergence and validation evidence;
* describe environment-dependent variability;
* write a concise numerical reliability statement.


## What the result claims

Participants begin by stating the quantity of interest, units, relevant scale,
and accuracy needed for the scientific decision. This prevents implementation
details from replacing the actual claim.


## Evidence and assumptions

A useful report records:

* the algorithm and important numerical settings;
* the reference, invariant, or comparison method;
* error measures and tolerance rationale;
* convergence or refinement behaviour;
* sensitivity to important inputs and environments;
* known limitations and failed checks.


## Reporting precision

Displayed digits should reflect meaningful information, not merely the width of
a floating-point type. Participants consider when uncertainty intervals, ranges,
or order-of-magnitude statements are more honest than a long decimal expansion.


## Communicating variability

The report should say whether repeated or cross-platform results are expected to
be bitwise identical, close within a stated tolerance, statistically
equivalent, or only consistent in their scientific interpretation.


## Reliability statement

Participants practice a short structure:

1. State the computational claim.
2. Summarize the strongest validation evidence.
3. Quantify observed error or variability.
4. State the relevant assumptions.
5. Identify the limitations that could change the conclusion.


## Connection to the capstone

Module 10 requires participants to apply this structure after diagnosing and
improving a suspicious computation.
