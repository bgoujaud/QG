from PEPit import PEP
from PEPit.primitive_steps import exact_linesearch_step

from code.function_class import ConvexQGFunction


def wc_conjugate_gradient_qg_convex(L, n, verbose=1):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is :math:`L-\\text{QG}^+` and convex.

    This code computes a worst-case guarantee for the **conjugate gradient (CG)** method (with exact span searches).
    That is, it computes the smallest possible :math:`\\tau(n, L)` such that the guarantee

    .. math:: f(x_n) - f_\\star \\leqslant \\tau(n, L) \\|x_0-x_\\star\\|^2

    is valid, where :math:`x_n` is the output of the **conjugate gradient** method,
    and where :math:`x_\\star` is a minimizer of :math:`f`.
    In short, for given values of :math:`n` and :math:`L`,
    :math:`\\tau(n, L)` is computed as the worst-case value of
    :math:`f(x_n)-f_\\star` when :math:`\\|x_0-x_\\star\\|^2 \\leqslant 1`.

    **Algorithm**:

        .. math:: x_{t+1} = x_t - \\sum_{i=0}^t \\gamma_i \\nabla f(x_i)

        with

        .. math:: (\\gamma_i)_{i \\leqslant t} = \\arg\\min_{(\\gamma_i)_{i \\leqslant t}} f \\left(x_t - \\sum_{i=0}^t \\gamma_i \\nabla f(x_i) \\right)

    **Theoretical guarantee**:

        The **tight** guarantee obtained in [2, Theorem 2.3] (lower) and [2, Theorem 2.4] (upper) is

        .. math:: f(x_n) - f_\\star \\leqslant \\frac{L}{2 (n + 1)} \\|x_0-x_\\star\\|^2.

    **References**:
    The detailed approach (based on convex relaxations) is available in [1, Corollary 6],
    and the result provided in [2, Theorem 2.4].

    `[1] Y. Drori and A. Taylor (2020). Efficient first-order methods for convex minimization: a constructive approach.
    Mathematical Programming 184 (1), 183-220.
    <https://arxiv.org/pdf/1803.05676.pdf>`_

    [2] B. Goujaud, A. Taylor, A. Dieuleveut (2022).
    Optimal first-order methods for convex functions with a quadratic upper bound.
    arXiv.

    Args:
        L (float): the quadratic growth parameter.
        n (int): number of iterations.
        verbose (int): Level of information details to print.
                       -1: No verbose at all.
                       0: This example's output.
                       1: This example's output + PEPit information.
                       2: This example's output + PEPit information + CVXPY details.

    Returns:
        pepit_tau (float): worst-case value
        theoretical_tau (float): theoretical value

    Example:
        >>> pepit_tau, theoretical_tau = wc_conjugate_gradient_qg_convex(L=1, n=12, verbose=1)
        (PEP-it) Setting up the problem: size of the main PSD matrix: 27x27
        (PEP-it) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEP-it) Setting up the problem: initial conditions (1 constraint(s) added)
        (PEP-it) Setting up the problem: interpolation conditions for 1 function(s)
                 function 1 : 351 constraint(s) added
        (PEP-it) Compiling SDP
        (PEP-it) Calling SDP solver
        (PEP-it) Solver status: optimal (solver: SCS); optimal value: 0.038461130525391705
        *** Example file: worst-case performance of conjugate gradient method ***
            PEP-it guarantee:		 f(x_n)-f_* <= 0.0384611 ||x_0 - x_*||^2
            Theoretical guarantee:	 f(x_n)-f_* <= 0.0384615 ||x_0 - x_*||^2

    """

    # Instantiate PEP
    problem = PEP()

    # Declare a smooth convex function
    func = problem.declare_function(ConvexQGFunction, param={'L': L})

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func.value(xs)

    # Then define the starting point x0 of the algorithm
    x0 = problem.set_initial_point()

    # Set the initial constraint that is the distance between x0 and x_*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)

    # Run n steps of the Conjugate Gradient method
    x_new = x0
    g0, f0 = func.oracle(x0)
    span = [g0]  # list of search directions
    for i in range(n):
        x_old = x_new
        x_new, gx, fx = exact_linesearch_step(x_new, func, span)
        span.append(gx)
        span.append(x_old - x_new)

    # Set the performance metric to the function value accuracy
    problem.set_performance_metric(fx - fs)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(verbose=pepit_verbose)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = L/(2*(n+1))

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of conjugate gradient method ***')
        print('\tPEP-it guarantee:\t\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(pepit_tau))
        print('\tTheoretical guarantee:\t f(x_n)-f_* <= {:.6} ||x_0 - x_*||^2'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":

    pepit_tau, theoretical_tau = wc_conjugate_gradient_qg_convex(L=1, n=12, verbose=1)
