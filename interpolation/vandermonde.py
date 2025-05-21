import numpy as np
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points


def vandermonde(x, y, decimals, x_sym=sp.symbols("x")):
    A = np.vander(x, increasing=False)
    coeffs = np.linalg.solve(A, y)
    rounded_coefficients = np.round(coeffs, decimals)

    poly = 0
    poly_rounded = 0

    degree = len(coeffs) - 1
    for i, coeff in enumerate(coeffs):
        poly += coeff * x_sym ** (degree - i)
        poly_rounded += rounded_coefficients[i] * x_sym ** (degree - i)

    return coeffs, rounded_coefficients, poly, poly_rounded


def show_vandermonde():
    st.header("Vandermonde Method")

    st.markdown(
        """
    The **Vandermonde Interpolation Method** is a technique used to find a polynomial that passes through a given set of points.
    It constructs a system of linear equations based on the Vandermonde matrix, which is a structured matrix often used in polynomial interpolation.

    This method is especially useful for understanding how polynomials of degree $ n-1 $ can interpolate $ n $ data points.
    """
    )

    with st.expander("📘 How the Vandermonde Interpolation Method Works"):
        st.markdown(
            """
        **1. Construct the Vandermonde Matrix:**
        - Given $ n $ data points $ (x_0, y_0), (x_1, y_1), \dots, (x_{n-1}, y_{n-1}) $, construct a matrix $ A $ where:
        """
        )
        st.latex(
            r"""
        A = \begin{bmatrix}
        x_0^{n-1} & x_0^{n-2} & \dots & x_0^0 \\
        x_1^{n-1} & x_1^{n-2} & \dots & x_1^0 \\
        \vdots & \vdots & \ddots & \vdots \\
        x_{n-1}^{n-1} & x_{n-1}^{n-2} & \dots & x_{n-1}^0
        \end{bmatrix}
        """
        )
        st.markdown(
            """
        - Each row of $ A $ corresponds to a data point $ x_i $, with columns representing powers of $ x_i $ from $ n-1 $ to $ 0 $.

        **2. Solve the Linear System:**
        - Solve the system $ A \cdot c = y $, where:
          - $ c $: Coefficients of the polynomial.
          - $ y $: Vector of $ y $-values of the data points.

        **3. Form the Polynomial:**
        - Once the coefficients $ c $ are determined, construct the interpolating polynomial:
        """
        )
        st.latex(
            r"""
        p(x) = c_0 x^{n-1} + c_1 x^{n-2} + \dots + c_{n-1}
        """
        )
        st.markdown(
            """
        **4. Rounding (Optional):**
        - Coefficients can be rounded to a specified number of decimal places for simplicity.

        **5. Evaluate the Polynomial:**
        - Use the polynomial $ p(x) $ to approximate values at intermediate points or to visualize the curve.

        **Advantages:**
        - Provides an explicit polynomial representation.
        - Simple to implement for small datasets.

        **Disadvantages:**
        - Computationally expensive for large datasets due to solving a linear system.
        - Prone to numerical instability if the points are close together or far apart.
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

        coeffs, rounded_coefficients, poly, poly_rounded = vandermonde(
            x_values, y_values, decimals
        )

        st.subheader("Results")
        st.write("**Vandermonde Polynomial**")
        st.write(f"$P(x) = {sp.latex(poly_rounded)}$")

        st.subheader("Graph of Vandermonde Interpolation")
        graph_with_points(x_values, y_values, poly)
    except:
        st.warning("Error: Please check your inputs.")
