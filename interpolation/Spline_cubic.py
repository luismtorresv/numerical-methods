import numpy as np
import sympy as sp


def cubic_spline_interpolation(x, y, decimals=None, x_sym=sp.symbols("x")):
    """
    Cubic Spline Interpolation.

    Parameters:
        x (list or array): List of x-coordinates of data points (must be sorted).
        y (list or array): List of y-coordinates of data points.
        decimals (int, optional): Number of decimals to round the coefficients (default: None).
        x_sym (sympy.Symbol, optional): Symbolic variable for the piecewise function (default: sympy.symbols('x')).

    Returns:
        tuple: Unrounded and rounded piecewise cubic functions as sympy.Piecewise objects.
    """

    n = len(x) - 1  # Number of intervals

    # Symbolic variables for the coefficients
    a = sp.symbols(f"a0:{n}")
    b = sp.symbols(f"b0:{n}")
    c = sp.symbols(f"c0:{n}")
    d = sp.symbols(f"d0:{n}")

    # Create a list of cubic polynomials for each interval
    cubics = [
        a[i] * x_sym**3 + b[i] * x_sym**2 + c[i] * x_sym + d[i] for i in range(n)
    ]

    # System of equations
    equations = []

    # Interpolation constraints (cubic passes through data points)
    for i in range(n):
        # Each piece must pass through its endpoints
        equations.append(cubics[i].subs(x_sym, x[i]) - y[i])
        equations.append(cubics[i].subs(x_sym, x[i + 1]) - y[i + 1])

    # Continuity constraints at interior points
    # First derivative
    for i in range(n - 1):
        first_derivative_left = sp.diff(cubics[i], x_sym)
        first_derivative_right = sp.diff(cubics[i + 1], x_sym)
        equations.append(
            first_derivative_left.subs(x_sym, x[i + 1])
            - first_derivative_right.subs(x_sym, x[i + 1])
        )

    # Second derivative
    for i in range(n - 1):
        second_derivative_left = sp.diff(cubics[i], x_sym, 2)
        second_derivative_right = sp.diff(cubics[i + 1], x_sym, 2)
        equations.append(
            second_derivative_left.subs(x_sym, x[i + 1])
            - second_derivative_right.subs(x_sym, x[i + 1])
        )

    # Natural spline boundary conditions:
    # Second derivatives at the first and last points are zero
    first_second_derivative = sp.diff(cubics[0], x_sym, 2)
    last_second_derivative = sp.diff(cubics[n - 1], x_sym, 2)
    equations.append(first_second_derivative.subs(x_sym, x[0]))
    equations.append(last_second_derivative.subs(x_sym, x[n]))

    # Solve the system of equations
    try:
        solution = sp.solve(equations, a + b + c + d)
    except sp.SolveFail:
        raise ValueError(
            "Failed to solve the system of equations. The problem might be ill-conditioned."
        )

    # Construct the piecewise cubic function
    pieces_unrounded = []
    pieces_rounded = []

    for i in range(n):
        # Substitute the coefficients into the cubic polynomial
        cubic_unrounded = cubics[i].subs(solution)
        if decimals is not None:
            cubic_rounded = sp.simplify(
                sp.nsimplify(cubic_unrounded, tolerance=10 ** (-decimals))
            )
        else:
            cubic_rounded = cubic_unrounded

        # Define the condition for the interval
        # Use strictly less than for all but the last interval to avoid overlap
        if i < n - 1:
            condition = (x_sym >= x[i]) & (x_sym < x[i + 1])
        else:
            condition = (x_sym >= x[i]) & (x_sym <= x[i + 1])

        # Add the interval's polynomial to the piecewise function
        pieces_unrounded.append((cubic_unrounded, condition))
        pieces_rounded.append((cubic_rounded, condition))

    piecewise_function_unrounded = sp.Piecewise(*pieces_unrounded)
    piecewise_function_rounded = sp.Piecewise(*pieces_rounded)

    return piecewise_function_unrounded, piecewise_function_rounded
