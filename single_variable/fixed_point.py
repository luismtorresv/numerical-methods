import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import calculate_tolerance, graph, ui_input_function

from .common import Result, Table, calculate_error, determine_error_type
from .report import generate_report


def fixed_point(
    x_0, tolerance, type_of_tolerance, niter, f_function, g_function
) -> Result:
    result = Result()
    table = Table()
    error_type = determine_error_type(type_of_tolerance)

    # First iteration
    x = x_prev = x_0
    f_x = f_function(x)
    i = 0
    error = 100  # Arbitrary initial error

    table.add_row(x, f_x, error)

    while error > tolerance and f_x != 0 and i < niter:
        x = g_function(x_prev)
        f_x = f_function(x)

        i += 1
        error = calculate_error(x, x_prev, error_type)
        x_prev = x
        table.add_row(x, f_x, error)

    df = table.as_dataframe()
    result.table = df
    print(len(table.x))
    if f_x == 0 or error < tolerance:
        result.set_success_status()
        return result
    result.error_message = "**Error**: Took too many iterations."
    return result


def validate_fixed_point_function(x_symbol, f_function, g_function):
    """
    Validate fixed-point iteration requirements.

    Args:
        x_symbol (sympy.Symbol): Variable symbol
        f_function (sympy.Expr): Original function f(x)
        g_function (sympy.Expr): Transformed function g(x)

    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        roots = sp.solve(f_function, x_symbol)
        if not roots:
            return False

        g_derivative = sp.diff(g_function, x_symbol)
        for root in roots:
            if not sp.simplify(g_function.subs(x_symbol, root) - root).is_zero:
                st.error(f"g(x) ≠ x at x = {root} where f(x) = 0.")
                return False

            derivative_value = g_derivative.subs(x_symbol, root)
            if abs(derivative_value) >= 1:
                st.warning(f"|g'(x)| ≥ 1 at x = {root}. Convergence not guaranteed.")

        return True
    except:
        st.error("Validation failed. Invalid input functions.")
        return False


def show_fixed_point():
    st.header("Fixed-Point Iteration Method")

    col1, col2, col3 = st.columns(3)
    with col1:
        x = st.text_input(
            "Variable name",
            value="x",
            help="Enter a variable name to use in the function. Default is $x$.",
        )
    with col2:
        # Input for original function f(x)
        f_input = st.text_input(
            "Function $f(x)$",
            value="x**2 - 4",
            help="Enter the function $f(x)$ whose root you want to find.",
        )
    with col3:
        # Input for transformed function g(x)
        g_input = st.text_input(
            "Transformation $g(x)$",
            value="2/x",
            help="Enter $g(x)$ such that $g(x) = x$ at the root of $f(x)$.",
        )

    # Initial guess input
    x0 = st.number_input(
        "Initial guess ($x_0$)",
        format="%.4f",
        value=2.0,
        step=0.0001,
        help="Provide the initial guess for the root.",
    )

    # Tolerance and iteration settings
    tol, niter, tolerance_type = calculate_tolerance()
    st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

    # Parse functions and variable
    x_symbol = sp.symbols(f"{x}")

    f_function = sp.sympify(f_input)
    first_derivative = sp.diff(f_function, x)
    second_derivative = sp.diff(first_derivative, x)
    g_function = sp.sympify(g_input)

    # Validate the functions
    # if not validate_fixed_point_function(x_symbol, f_function, g_function):
    #     return

    # Display the functions in LaTeX
    st.subheader("Functions")
    st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
    st.latex(f"g({x_symbol}) = {sp.latex(g_function)}")

    # Check convergence condition
    g_first_derivative = sp.diff(g_function, x_symbol)
    st.subheader("Derivative of $g(x)$")
    st.latex(g_first_derivative)

    # Lambdify the functions for numerical evaluations
    g = nm_lambdify(g_function, x_symbol)
    f = nm_lambdify(f_function, x_symbol)

    result = fixed_point(x0, tol, tolerance_type, niter, f, g)
    st.subheader("Results")
    if result.has_failed():
        st.error(result.error_message)
        # return

    result_display = result.table.style.format("{:.15e}")

    st.divider()

    st.header("Result")
    if not result.has_failed():
        last_x = result.table.iloc[-1]["x"]
        st.success(":material/check: Root found.")

        col1, col2 = st.columns(2)
        col1.metric("$x$", f"{last_x:.10e}")
        col2.metric("$f(x)$", f"{f(last_x):.10e}")

    st.subheader("Table")
    st.table(result_display)

    st.divider()

    graph(f_input)

    st.divider()

    generate_report(
        niter,
        f,
        tol,
        tolerance_type,
        x,
        first_derivative,
        second_derivative,
    )
