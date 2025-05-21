import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points


def lagrange(x, y, decimals, x_sym=sp.symbols("x")):
    n = len(x)
    pol = 0
    pol_rounded = 0

    for i in range(n):
        Li = 1
        den = 1

        for j in range(n):
            if j != i:
                Li *= x_sym - x[j]
                den *= x[i] - x[j]

        # Add to the unrounded polynomial
        pol += y[i] * Li / den

    # Simplifying the rounded polynomial and maintaining decimals
    pol_rounded_decimal = sp.N(pol, decimals)

    # Expand the polynomial expressions
    newton_poly_expr_unrounded = sp.expand(pol)
    newton_poly_expr_rounded = sp.N(sp.expand(pol), decimals)

    return (
        pol,
        pol_rounded_decimal,
        newton_poly_expr_unrounded,
        newton_poly_expr_rounded,
    )


def show_lagrange():
    st.header("Lagrange Method")

    st.markdown(
        """
    The **Lagrange Interpolation Method** is one of the most widely used methods for polynomial interpolation.
    It provides a polynomial that exactly passes through a given set of data points. Unlike Newton's method, which builds the polynomial incrementally, Lagrange's method computes the entire polynomial in one go using Lagrange basis polynomials.

    The method is particularly simple to implement and understand, and it is useful when dealing with small datasets or when you need an explicit polynomial form.
    """
    )

    with st.expander("📘 How the Lagrange Interpolation Method Works"):
        st.markdown(
            """
        **1. Lagrange Basis Polynomials:**
        - The Lagrange interpolating polynomial is given by the following sum:
        """
        )
        st.latex(
            r"""
        P(x) = \sum_{i=0}^{n-1} y_i \cdot L_i(x)
        """
        )
        st.markdown(
            """
        Where $ y_i $ are the given data points and $ L_i(x) $ are the Lagrange basis polynomials.

        - Each Lagrange basis polynomial $ L_i(x) $ is defined as:
        """
        )
        st.latex(
            r"""
        L_i(x) = \prod_{\substack{0 \leq j < n \\ j \neq i}} \frac{x - x_j}{x_i - x_j}
        """
        )
        st.markdown(
            """
        - These basis polynomials have the property that $ L_i(x_j) = 1 $ if $i = j$ and $ L_i(x_j) = 0 $ if $i ≠ j$, ensuring that each term in the sum contributes only at the corresponding $ x_i $.
        - The final polynomial is then:
        """
        )
        st.latex(
            r"""
        P(x) = y_0 \cdot L_0(x) + y_1 \cdot L_1(x) + \dots + y_{n-1} \cdot L_{n-1}(x)
        """
        )
        st.markdown(
            """
        **Advantages:**
        - Simple to implement.
        - Does not require solving a system of equations.
        - Provides a direct expression for the interpolating polynomial.

        **Disadvantages:**
        - Can be computationally expensive for large datasets due to the number of multiplications required.
        - Not as efficient for adding new points as methods like Newton's method.
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
            pol_decimal,
            pol_rounded_decimal,
            newton_poly_expr_unrounded,
            newton_poly_expr_rounded,
        ) = lagrange(x_values, y_values, decimals)

        # Display results
        st.subheader("Results")
        st.write("**Lagrange Polynomial**")
        st.write(f"$P(x) = {sp.latex(pol_rounded_decimal)}$")

        st.write("**Lagrange Polynomial Simplified**")
        st.write(f"$P(x) = {sp.latex(newton_poly_expr_rounded)}$")

        # Graph the interpolation polynomial
        st.subheader("Graph of Lagrange Interpolation")
        graph_with_points(x_values, y_values, pol_decimal)
    except:
        st.error("Error: Please check your inputs")
