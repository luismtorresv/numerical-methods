import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points, show_table

from .utils import are_x_values_unique
from .report import generate_report


def newton_interpolation(x, y, decimals, x_sym=sp.symbols("x")):
    n = len(x)
    matrix = np.zeros((n, n))  # Create a square matrix of size len(x)

    # Fill the first column with y values
    for i in range(n):
        matrix[i, 0] = y[i]

    # Compute the divided differences
    for col in range(1, n):
        for row in range(col, n):
            matrix[row, col] = (matrix[row, col - 1] - matrix[row - 1, col - 1]) / (
                x[row] - x[row - col]
            )

    # Newton coefficients (diagonal of the matrix)
    coefficients = np.diagonal(matrix)  # Original coefficients
    rounded_coefficients = np.round(coefficients, decimals)  # Rounded coefficients

    newton_poly_unrounded = 0
    newton_poly_rounded = 0

    for i in range(n):
        # Initialize the term as a product of the coefficient and 1
        term_unrounded = sp.Mul(
            coefficients[i], 1
        )  # Use sp.Mul to maintain the product form
        term_rounded = sp.Mul(rounded_coefficients[i], 1)

        # Create the polynomial term without expansion
        for j in range(i):
            term_unrounded = sp.Mul(
                term_unrounded, (x_sym - x[j]), evaluate=False
            )  # Multiply using sp.Mul
            term_rounded = sp.Mul(
                term_rounded, (x_sym - x[j]), evaluate=False
            )  # Multiply using sp.Mul

        # Add to the total polynomial
        newton_poly_unrounded += term_unrounded
        newton_poly_rounded += term_rounded

    # SymPy expressions of the Newton polynomials
    newton_poly_expr_unrounded = sp.expand(newton_poly_unrounded)
    newton_poly_expr_rounded = sp.expand(newton_poly_rounded)

    return (
        matrix,
        coefficients,
        rounded_coefficients,
        newton_poly_unrounded,
        newton_poly_expr_unrounded,
        newton_poly_rounded,
        newton_poly_expr_rounded,
    )


def show_newton_divided_diff():
    st.header("Newton Interpolation Method")
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

        generate_report()
    except:
        st.error("Error: Please check your input")
