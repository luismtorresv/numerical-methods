import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points


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
    st.markdown(
        """
    The **Linear Spline Interpolation Method** is a piecewise linear approach for interpolating between data points.
        It connects each pair of adjacent data points with a straight line, creating a continuous piecewise function that is linear in each interval.

    """
    )

    with st.expander("📘 How the Linear Spline Method Works"):
        st.markdown(
            """
        - The linear spline between two points $ (x_i, y_i) $ and $ (x_{i+1}, y_{i+1}) $ is:
        """
        )
        st.latex(
            r"""
        S_i(x) = y_i + \frac{(y_{i+1} - y_i)}{(x_{i+1} - x_i)}(x - x_i)
        """
        )
        st.markdown(
            """
        **Steps:**
        - For each pair of adjacent data points, compute the linear spline using the above formula.
        - Combine these splines to form the complete piecewise linear interpolation.

        **Advantages:**
        - Simple and easy to compute.
        - Provides a continuous function without oscillation.

        **Disadvantages:**
        - Does not ensure smoothness of the first derivative between segments (i.e., the slope can change abruptly).
        """
        )

    try:
        x_values, y_values = enter_points(val=2)

        # Check for repeated x values
        if len(x_values) != len(set(x_values)):
            st.error(
                "Error: The points entered have an x-repeated value, which makes it impossible to be represented as a function."
            )
            return  # Stop further execution if there are repeated x values

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
