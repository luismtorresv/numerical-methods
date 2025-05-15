import numpy as np
import sympy as sp


def quadratic_spline_interpolation(x, y, decimals=None, x_sym=sp.symbols("x")):
    """
    Quadratic Spline Interpolation.

    Parameters:
        x (list or array): List of x-coordinates of data points (must be sorted).
        y (list or array): List of y-coordinates of data points.
        decimals (int, optional): Number of decimals to round the coefficients (default: None).
        x_sym (sympy.Symbol, optional): Symbolic variable for the piecewise function (default: sympy.symbols('x')).

    Returns:
        tuple: Unrounded and rounded piecewise quadratic functions as sympy.Piecewise objects.
    """

    n = len(x) - 1  # Number of intervals

    # Symbolic variables for the coefficients
    a = sp.symbols(f"a0:{n}")
    b = sp.symbols(f"b0:{n}")
    c = sp.symbols(f"c0:{n}")

    # Create a list of quadratic polynomials for each interval
    quadratics = [a[i] * x_sym**2 + b[i] * x_sym + c[i] for i in range(n)]

    # System of equations
    equations = []

    # Interpolation constraints (quadratic passes through data points)
    for i in range(n):
        # Each piece must pass through its endpoints
        equations.append(quadratics[i].subs(x_sym, x[i]) - y[i])
        equations.append(quadratics[i].subs(x_sym, x[i + 1]) - y[i + 1])

    # Continuity of first derivatives at interior points
    for i in range(n - 1):
        derivative_left = sp.diff(quadratics[i], x_sym)
        derivative_right = sp.diff(quadratics[i + 1], x_sym)
        equations.append(
            derivative_left.subs(x_sym, x[i + 1])
            - derivative_right.subs(x_sym, x[i + 1])
        )

    # Additional condition: Second derivative is continuous at the second interior point
    # This provides the extra equation needed for a unique solution
    if n > 1:
        second_derivative_left = sp.diff(quadratics[0], x_sym, 2)
        second_derivative_right = sp.diff(quadratics[1], x_sym, 2)
        equations.append(
            second_derivative_left.subs(x_sym, x[1])
            - second_derivative_right.subs(x_sym, x[1])
        )

    # Solve the system of equations
    try:
        solution = sp.solve(equations, a + b + c)
    except sp.SolveFail:
        raise ValueError(
            "Failed to solve the system of equations. The problem might be ill-conditioned."
        )

    # Construct the piecewise quadratic function
    pieces_unrounded = []
    pieces_rounded = []

    for i in range(n):
        # Substitute the coefficients into the quadratic polynomial
        quadratic_unrounded = quadratics[i].subs(solution)
        if decimals is not None:
            quadratic_rounded = sp.simplify(
                sp.nsimplify(quadratic_unrounded, tolerance=10 ** (-decimals))
            )
        else:
            quadratic_rounded = quadratic_unrounded

        # Define the condition for the interval
        # Use strictly less than for all but the last interval to avoid overlap
        if i < n - 1:
            condition = (x_sym >= x[i]) & (x_sym < x[i + 1])
        else:
            condition = (x_sym >= x[i]) & (x_sym <= x[i + 1])

        # Add the interval's polynomial to the piecewise function
        pieces_unrounded.append((quadratic_unrounded, condition))
        pieces_rounded.append((quadratic_rounded, condition))

    piecewise_function_unrounded = sp.Piecewise(*pieces_unrounded)
    piecewise_function_rounded = sp.Piecewise(*pieces_rounded)

    return piecewise_function_unrounded, piecewise_function_rounded
