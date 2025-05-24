import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points

from .utils import are_x_values_unique


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

    try:
        x_values, y_values = enter_points()

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
