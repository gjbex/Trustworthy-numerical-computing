# Reference: Vectors, Norms, And Scaling

Modules 3 through 6 and the capstone compare collections of errors, residuals,
updates, and perturbations. A **norm** turns such a vector into one nonnegative
number that represents its size. The choice of norm is part of the numerical
question: different norms emphasize different features of the same vector.

This page is a reference, not an additional prerequisite module. Return to it
when a module uses norm notation or when you need to choose an aggregation rule.


## From components to one size

A vector is an ordered collection of components,

$$
v=(v_1,v_2,\ldots,v_n).
$$

A norm is written $\|v\|$. It must behave like a consistent measure of size:

* $\|v\|\geq0$, and it is zero only when every component is zero;
* multiplying every component by $\alpha$ multiplies the norm by $|\alpha|$;
* $\|u+v\|\leq\|u\|+\|v\|$, so combining vectors cannot create more than the
  sum of their separate sizes.

These properties do not select one unique norm. The scientific or numerical
requirement determines which summary is useful.


## Common vector norms

For a real vector $v$, three common choices are:

| Name | Definition | What it emphasizes |
|---|---|---|
| 1-norm | $\|v\|_1=\sum_i|v_i|$ | Total absolute magnitude across components |
| Euclidean or 2-norm | $\|v\|_2=\sqrt{\sum_i v_i^2}$ | Combined geometric magnitude |
| Maximum or infinity norm | $\|v\|_\infty=\max_i|v_i|$ | The single largest component magnitude |

The subscript names the norm; it is not an exponent. “Max norm” and “infinity
norm” are two names for the same rule.

For $v=(-3,4,1)$ in a common unit $q$,

$$
\|v\|_1=8\,q,
\qquad
\|v\|_2=\sqrt{26}\,q\approx5.10\,q,
\qquad
\|v\|_\infty=4\,q.
$$

The values differ because they answer different questions; none is the
universally correct size.


## Why Module 4 uses the maximum norm

The maximum norm exposes the largest component change. A bound

$$
\|v\|_\infty\leq\tau
$$

is equivalent to requiring $|v_i|\leq\tau$ for every component. It is therefore
a natural choice when no individual error, residual, or perturbation may exceed
a stated limit.

In Module 4's two-equation experiment,

$$
\Delta b=(0,\eta),
\qquad
\Delta x=(-\eta/\delta,\eta/\delta).
$$

Consequently,

$$
\|\Delta b\|_\infty=|\eta|,
\qquad
\|\Delta x\|_\infty=\frac{|\eta|}{|\delta|}.
$$

This makes the component amplification visible without cancellation between
positive and negative changes. Another norm would produce a different numerical
condition measure, so the norm must always be stated.


## Maximum error, 2-norm, and RMS

For an error vector $e=(e_1,\ldots,e_n)$, Module 3's maximum absolute error is
exactly its maximum norm:

$$
E_\max=\max_i|e_i|=\|e\|_\infty.
$$

The root-mean-square error is a scaled 2-norm:

$$
E_\mathrm{RMS}
=\sqrt{\frac{1}{n}\sum_i e_i^2}
=\frac{\|e\|_2}{\sqrt{n}}.
$$

The maximum exposes the worst component. RMS describes a typical component
scale but can dilute a localized failure. The unscaled 2-norm generally grows
with the number of comparable components, whereas RMS compensates for that
count. Comparisons across different vector lengths must therefore state whether
the aggregation itself changes with problem size.


## Units and component scaling

If all components have the same units, the 1-, 2-, maximum, and RMS norms retain
those units. Raw components with different units or scientifically different
scales should not be combined directly. For example, adding a temperature error
in kelvin to a pressure error in pascals has no coherent interpretation.

One option is to define justified component scales $s_i>0$ and form a
dimensionless scaled vector

$$
z_i=\frac{v_i}{s_i}.
$$

Then $\|z\|_\infty\leq1$ means every component is within its declared scale.
The scales might come from units, measurement resolution, acceptance limits, or
a reference magnitude. Choosing them merely to make a test pass would change
the claim rather than justify it. Sometimes separate component-wise checks are
clearer than one aggregate norm.


## Vector norms and matrix condition numbers

A vector norm measures the size of a vector. A compatible induced matrix norm
measures the largest factor by which a matrix can stretch vectors:

$$
\|A\|=\max_{v\ne0}\frac{\|Av\|}{\|v\|}.
$$

For an invertible matrix, the corresponding normwise condition number is

$$
\kappa(A)=\|A\|\,\|A^{-1}\|.
$$

The subscript in names such as “matrix 2-norm condition number” identifies the
underlying vector norm. Different norm choices can give different numerical
condition numbers, although they describe the same underlying question about
input-to-output amplification. A condition number must therefore name its norm,
scaling, perturbation model, and input.


## A practical reporting checklist

When a norm appears in a numerical claim, record:

1. the vector being measured and what its components represent;
2. the norm or aggregation rule;
3. the units and any component scales;
4. why that norm matches the scientific or numerical requirement;
5. the observed value and comparison threshold;
6. consequential component values that an aggregate could hide;
7. the policy for `NaN`, infinity, and missing components.

A statement such as “the residual norm is small” is incomplete until these
choices make “residual,” “norm,” and “small” inspectable.
