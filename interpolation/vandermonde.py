import numpy as np
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points

from .utils import are_x_values_unique
from .report import generate_report


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

        coeffs, rounded_coefficients, poly, poly_rounded = vandermonde(
            x_values, y_values, decimals
        )

        st.subheader("Results")
        st.write("**Vandermonde Polynomial**")
        st.write(f"$P(x) = {sp.latex(poly_rounded)}$")

        st.subheader("Graph of Vandermonde Interpolation")
        graph_with_points(x_values, y_values, poly)

        generate_report()
    except:
        st.warning("Error: Please check your inputs.")
