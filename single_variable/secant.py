import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import (
    calculate_tolerance,
    enter_function,
    graph,
    show_table,
)

from .report import generate_report


def secant(x0, x1, niter, tol, function, tolerance_type):
    table = []

    # Initial setup
    xn = x1 - function(x1) * (x1 - x0) / (function(x1) - function(x0))
    x_prev = x1
    x_prev2 = x0
    err = 100
    iterations = 0

    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # First iteration (iteration 0)
    row = {"x_{n-1}": x0, "x_n": x1, "f(x_n)": function(x1), "Error": None}
    table.append(row)

    # Secant method iterations
    while iterations < niter and err >= tol:
        # Update xn
        xn = x_prev - function(x_prev) * (x_prev - x_prev2) / (
            function(x_prev) - function(x_prev2)
        )

        # Calculate error based on tolerance type
        if tolerance_type == "Significant Figures":
            # Calculate relative error
            err = abs((xn - x_prev) / xn)
        elif tolerance_type == "Correct Decimals":
            # Calculate absolute error
            err = abs(xn - x_prev)

        # Append row for current iteration
        row = {"x_{n-1}": x_prev, "x_n": xn, "f(x_n)": function(xn), "Error": err}
        table.append(row)

        iterations += 1
        x_prev2 = x_prev
        x_prev = xn

    # Convert table to DataFrame and return
    df = pd.DataFrame(table)
    return {"status": "success", "table": df}


def show_secant():
    st.header("Secant Method")

    try:
        x, function_input = enter_function()

        col3, col4 = st.columns(2)
        with col3:
            x0 = st.number_input(
                "First Point (x_0)",
                format="%.4f",
                value=0.1,
                step=0.0001,
                help="The first initial guess for the root. It is a value where the function is evaluated.",
            )

        with col4:
            x1 = st.number_input(
                "Second Point (x_1)",
                format="%.4f",
                value=0.2,
                step=0.0001,
                help="The second initial guess for the root. It should be close to x0 and the function should have different signs at x0 and x1.",
            )

        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")
        st.subheader("Function")
        function = sp.sympify(function_input)
        st.latex(f"f({x}) = {sp.latex(function)}")

        x = sp.symbols(f"{x}")
        first_derivative = sp.diff(function, x)
        second_derivative = sp.diff(first_derivative, x)

        function = nm_lambdify(function, x)
        result = secant(x0, x1, niter, tol, function, tolerance_type)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            result = result["table"]

        mid = result.iloc[-1]["x_n"]

        if function(mid) <= 0 + tol:
            st.subheader("Results")
            decimals = show_table(result)
            st.success(
                f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {function(mid):.{decimals}f}"
            )
        else:
            st.warning(
                f"Method did not converge, potentially because of a discontinuity in the function."
            )

        graph(x, function_input)
        generate_report(
            niter,
            function,
            tol,
            tolerance_type,
            x,
            first_derivative,
            second_derivative,
        )
    except Exception as e:
        st.error("Error: Check your input")
        print(e)
