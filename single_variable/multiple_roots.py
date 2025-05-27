import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import (
    calculate_tolerance,
    graph,
    show_table,
    ui_input_function,
)

from .common import Result, Table, calculate_error, determine_error_type
from .report import generate_report


def multiple_roots(x_0, n_iter, tol, function, df, d2f, tolerance_type) -> Result:
    result = Result()
    table = Table()
    error_type = determine_error_type(tolerance_type)

    x = x_0
    for _ in range(n_iter):
        f_x = function(x)
        d_f_x = df(x)
        d2_f_x = d2f(x)

        if d_f_x == 0:
            result.error_message = "**Error**: The first derivative is equal to 0. The method is not applicable."
            return result

        x_next = x - (f_x * d_f_x) / (d_f_x**2 - f_x * d2_f_x)

        error = calculate_error(x_next, x, error_type)
        table.add_row(x, f_x, error)

        x = x_next

        if error < tol:
            result.table = table.as_dataframe()
            result.set_success_status()
            return result

    result.error_message = "**Error:** Took too many iterations."
    return result


def show_multiple_roots():
    st.header("Multiple Roots Method")

    original_function_input = ui_input_function()

    x_0 = st.number_input(
        "Initial Point ($x_0$)",
        format="%.4f",
        value=1.0,
        step=0.0001,
        help="Initial guess for the root. The method requires an initial value close to the actual root.",
    )

    # Calcular tolerancia
    tol, niter, tolerance_type = calculate_tolerance()
    st.markdown(f"**Calculated Tolerance:** {tol:.10f}")
    st.subheader("Function")
    function_sp = sp.sympify(original_function_input)
    st.latex(f"f(x) = {sp.latex(function_sp)}")

    # Preparar función, derivadas y método
    x = sp.symbols("x")
    function = nm_lambdify(function_sp, x)
    first_derivative = sp.diff(function_sp, x)
    second_derivative = sp.diff(first_derivative, x)

    df_sp = sp.diff(function_sp, x)
    d2f_sp = sp.diff(df_sp, x)

    df = nm_lambdify(df_sp, x)
    d2f = nm_lambdify(d2f_sp, x)

    result = multiple_roots(x_0, niter, tol, function, df, d2f, tolerance_type)

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

    graph(original_function_input)

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
