import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import calculate_tolerance, graph, ui_input_function

from .common import Result, Table, calculate_error, determine_error_type
from .report import generate_report


def bisection(a, b, niter, tol, tolerance_type, function) -> Result:
    result = Result()
    table = Table()
    error_type = determine_error_type(tolerance_type)

    if b < a:
        result.error_message = "Invalid Arguments, b must be greater than a."
        return result

    table.add_row(a, function(a), None)
    error = 100  # Arbitrary initial error

    if function(a) * function(b) > 0:
        result.error_message = (
            "Invalid Arguments, the function does not change sign in the interval."
        )
        return result

    mid = (a + b) / 2
    i = 0
    while i < niter and error > tol:
        if function(a) * function(mid) <= 0:
            b = mid
        else:
            a = mid

        i += 1
        prev_mid = mid
        mid = (a + b) / 2

        error = calculate_error(mid, prev_mid, error_type)
        table.add_row(mid, function(mid), error)

    df = table.as_dataframe()
    result.table = df
    result.set_success_status()
    return result


def show_bisection():
    st.header("Bisection Method")

    function_input = ui_input_function(placeholder_function="x**2 - 4")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input(
            "Initial point of search interval (a)",
            format="%.4f",
            value=0.1,
            step=0.0001,
        )
    with col2:
        b = st.number_input(
            "End point of search interval (b)",
            format="%.4f",
            value=3.0,
            step=0.0001,
        )

    tol, niter, tolerance_type = calculate_tolerance()
    st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

    x = sp.symbols("x")
    function_sp = sp.sympify(function_input)
    first_derivative = sp.diff(function_sp, x)
    second_derivative = sp.diff(first_derivative, x)

    st.subheader("Function")
    st.latex(f"f({x}) = {sp.latex(function_sp)}")

    function = nm_lambdify(function_input, x)

    result = bisection(a, b, niter, tol, tolerance_type, function)

    st.subheader("Results")
    if result.has_failed():
        st.error(result.error_message)

    result_display = result.table.style.format("{:.15e}")

    st.divider()

    st.header("Result")
    if not result.has_failed():
        last_x = result.table.iloc[-1]["x"]
        st.success(":material/check: Root found.")

        col1, col2 = st.columns(2)
        col1.metric("$x$", f"{last_x:.10e}")
        col2.metric("$f(x)$", f"{function(last_x):.10e}")

    st.subheader("Table")
    st.table(result_display)

    st.divider()

    graph(function_input)

    st.divider()
    generate_report(
        niter,
        function,
        tol,
        tolerance_type,
        x,
        first_derivative,
        second_derivative,
    )
