import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points

from .utils import are_x_values_unique


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


def show_spline():
    st.header("Linear Spline Method")

    try:
        x_values, y_values = enter_points(val=2)

        if not are_x_values_unique(x_values):
            return

        decimals = st.slider(
            "Select number of decimals to display",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )

        (
            piecewise_function_unrounded,
            piecewise_function_rounded,
        ) = linear_spline_interpolation(x_values, y_values, decimals)

        # Display results
        st.subheader("Results")
        st.write("**Linear Spline Piecewise Function**")
        st.write(f"$P(x) = {sp.latex(piecewise_function_rounded)}$")

        # Graph the interpolation polynomial
        st.subheader("Graph of Spline Interpolation")
        graph_with_points(x_values, y_values, piecewise_function_unrounded)
    except:
        st.error("Error: Please check your inputs")
