# QG convex functions

In this repository we study first order optimization problem over QG convex functions,
namely convex functions verifying for all $x$, $f(x) - f_\star \leq \frac{L}{2}d(x, \mathcal{X}_\star)^2$.

## Article

The folder `paper` contains the article we wrote.

## Code

The folder `code` contains some code based on the PEPit package allowing to use the Performance estimation problem framework very easily.
Please run `pip install -r requirements` before running any of those files.

Each of these files print the worst case guarantee of a given algorithm,
matching the theoretical bound proven in the associated paper.
`gradient_descent_qg_convex_decreasing.py` create the figure 1 of the paper,
showing evidence of the formulated conjecture.
