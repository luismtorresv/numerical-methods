import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points, show_table

from .newton_interpolation import newton_interpolation


def show_newton_divided_diff():
    st.header("Newton Interpolation Method")

    st.markdown(
        """
    The **Newton Divided Difference Method** is a numerical technique used to construct an interpolating polynomial for a given set of data points.
    It is particularly advantageous because it can handle unevenly spaced data and allows incremental addition of points without recomputing the entire polynomial.

    This method represents the polynomial in terms of divided differences, leading to a compact and recursive formulation.
    """
    )

    with st.expander("📘 How the Newton Divided Difference Method Works"):
        st.markdown(
            """
        **1. Divided Differences Table:**
        - The divided differences are computed recursively based on the data points $ (x_0, y_0), (x_1, y_1), \dots, (x_n, y_n) $.
        - The formula for the first-order divided difference is:
        """
        )
        st.latex(
            r"""
        f[x_i, x_{i+1}] = \frac{f(x_{i+1}) - f(x_i)}{x_{i+1} - x_i}
        """
        )
        st.markdown(
            """
        - For higher orders, the general formula is:
        """
        )
        st.latex(
            r"""
        f[x_i, x_{i+1}, \dots, x_{i+k}] = \frac{f[x_{i+1}, \dots, x_{i+k}] - f[x_i, \dots, x_{i+k-1}]}{x_{i+k} - x_i}
        """
        )
        st.markdown(
            """
        **2. Form the Interpolating Polynomial:**
        - The interpolating polynomial is constructed incrementally:
        """
        )
        st.latex(
            r"""
        P(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \dots
        """
        )
        st.markdown(
            """
        - Each term involves a higher-order divided difference multiplied by the corresponding factors of $ (x - x_i) $.

        **3. Evaluate the Polynomial:**
        - Once the polynomial is constructed, it can be evaluated at any desired point.

        **Advantages:**
        - Handles unevenly spaced data.
        - Efficient for incremental addition of points.

        **Disadvantages:**
        - Less intuitive compared to methods like Lagrange interpolation.
        """
        )
    try:
        x_values, y_values = enter_points()

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
            matrix,
            coefficients,
            rounded_coefficients,
            newton_poly_unrounded,
            newton_poly_expr_unrounded,
            newton_poly_rounded,
            newton_poly_expr_rounded,
        ) = newton_interpolation(x_values, y_values, decimals)

        # Display results
        st.subheader("Results")
        st.write(
            "**Divided Differences Table** The Coefficients of the Newton Interpolation Polynomial are displayed on the Diagonal."
        )
        show_table(pd.DataFrame(matrix), deci=False, decimals=decimals)

        st.write("**Newton Polynomial**")
        st.write(f"$P(x) = {sp.latex(newton_poly_rounded)}$")

        st.write("**Newton Polynomial Simplified**")
        st.write(f"$P(x) = {sp.latex(newton_poly_expr_rounded)}$")

        # Graph the interpolation polynomial
        st.subheader("Graph of Newton Interpolation")
        graph_with_points(x_values, y_values, newton_poly_expr_unrounded)
    except:
        st.error("Error: Please check your input")
