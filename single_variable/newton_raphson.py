import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import calculate_tolerance, graph, ui_input_function

from .common import Result, ResultStatus, Table, calculate_error, determine_error_type
from .report import generate_report


def get_derivative(f):
    x = sp.symbols("x")
    f_prime = sp.diff(f, x)
    return f_prime


def newton(x_0, niter, tol, tolerance_type, function, derivative) -> Result:
    result = Result()
    table = Table()
    error_type = determine_error_type(tolerance_type)

    if derivative(x_0) == 0:
        result.error_message = "Derivative cannot be 0."
        return result

    x_n = x_0 - function(x_0) / derivative(x_0)
    x_prev = x_0
    table.add_row(x_0, function(x_0), None)

    error = 100
    iterations = 0

    while iterations < niter and error > tol:
        iterations += 1
        x_prev = x_n
        x_n = x_n - function(x_n) / derivative(x_n)

        error = calculate_error(x_n, x_prev, error_type)
        table.add_row(x_n, function(x_n), error)

    df = table.as_dataframe()
    result.table = df
    if error < tol:
        result.set_success_status()
        return result
    else:
        result.error_message = "**Error:** Took too many iterations."
        return result


def show_newton():
    st.header("Newton-Raphson Method")

    function_input = ui_input_function()

    if not function_input:
        st.stop()

    x0 = st.number_input(
        "Initial Point (x_0)",
        format="%.4f",
        value=0.1,
        step=0.0001,
        help="The first initial guess for the root. It is a value where the function is evaluated.",
    )

    tol, niter, tolerance_type = calculate_tolerance()
    st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

    x = sp.symbols("x")
    function = sp.sympify(function_input)
    first_derivative = sp.diff(function, x)
    second_derivative = sp.diff(first_derivative, x)

    st.subheader("Function")
    st.latex(f"f({x}) = {sp.latex(function)}")
    st.subheader("Derivative")
    st.latex(f"f({x}) = {sp.latex(first_derivative)}")

    function = nm_lambdify(function, x)
    derivative_lambda = nm_lambdify(first_derivative, x)

    result = newton(x0, niter, tol, tolerance_type, function, derivative_lambda)

    if result.has_failed():
        st.error(result.error_message)
        return

    result_display = result.table.style.format("{:.15e}")

    st.divider()

    st.header("Result")
    mid = result.table.iloc[-1]["x"]
    if function(mid) < 0 + tol:
        st.success(":material/check: Root found.")

        col1, col2 = st.columns(2)
        col1.metric("$x$", f"{mid:.10e}")
        col2.metric("$f(x)$", f"{function(mid):.10e}")

    else:
        st.warning(
            f"Method did not converge, potentially because of a discontinuity in the function."
        )
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
