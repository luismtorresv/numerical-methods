import sympy as sp


def linear_spline_interpolation(x, y, decimals=None, x_sym=sp.symbols("x")):
    n = len(x)
    pieces_unrounded = []
    pieces_rounded = []

    for i in range(n - 1):
        # Calculate slope (m) and intercept (b) for each interval
        slope = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        intercept = y[i] - slope * x[i]

        # Unrounded linear segment
        linear_segment = slope * x_sym + intercept

        # Rounded linear segment
        if decimals is not None:
            linear_segment_round = sp.simplify(
                sp.nsimplify(linear_segment, tolerance=10 ** (-decimals))
            )
        else:
            linear_segment_round = linear_segment  # No rounding if decimals is None

        # Define condition for each piece
        condition = (x_sym >= x[i]) & (x_sym <= x[i + 1])

        # Append unrounded and rounded pieces
        pieces_unrounded.append((linear_segment, condition))
        pieces_rounded.append((linear_segment_round, condition))

    # Construct the piecewise functions
    piecewise_function_unrounded = sp.Piecewise(*pieces_unrounded)
    piecewise_function_rounded = sp.Piecewise(*pieces_rounded)

    return piecewise_function_unrounded, piecewise_function_rounded
