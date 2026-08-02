# Trustworthy Numerical Computing

These learning modules support the training session *Trustworthy Numerical
Computing*. They develop a practical method for deciding whether a numerical
result deserves scientific trust.

The modules are the course's long-form reading material. The matching files in
`slides-source/` are teaching aids for instructor-led delivery and deliberately
contain less detail.


## Learning path

1. [When Correct Code Produces Wrong Answers](01-when-correct-code-produces-wrong-answers.md)
2. [Understanding Floating-Point Arithmetic](02-understanding-floating-point-arithmetic.md)
3. [Measuring And Comparing Numerical Error](03-measuring-and-comparing-numerical-error.md)
4. [Conditioning And Numerical Stability](04-conditioning-and-numerical-stability.md)
5. [Common Numerical Failure Modes](05-common-numerical-failure-modes.md)
6. [Iterative Algorithms And Convergence](06-iterative-algorithms-and-convergence.md)
7. [Validating Scientific Computations](07-validating-scientific-computations.md)
8. [Reproducibility Across Computing Environments](08-reproducibility-across-computing-environments.md)
9. [Communicating Numerical Reliability](09-communicating-numerical-reliability.md)
10. [Capstone: Investigating A Suspicious Result](10-capstone-investigating-a-suspicious-result.md)

The [module structure](learning-module-structure.md) explains the prerequisite
order and how the modules fit into a one-day course. [Optional advanced
topics](optional-advanced-topics.md) can be used for a longer course or
domain-specific follow-up.


## Course through-line

Each module contributes to the same investigation workflow:

1. State what result is expected and what accuracy is meaningful.
2. Characterize the problem and its sensitivity to inputs.
3. Identify arithmetic and algorithmic failure modes.
4. Establish independent validation evidence.
5. Check whether conclusions survive relevant environment changes.
6. Communicate assumptions, limitations, and evidence.


## Status

The curriculum structure, module boundaries, and slide mapping are established.
Modules 1 and 2 contain detailed reading material and executable Quarto
activities that generate self-paced Jupyter notebooks. Detailed explanations,
computational experiments, and exercises for later modules will be developed
within this structure.
