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

from .common import Result, ResultStatus, Table, calculate_error, determine_error_type
from .report import generate_report


def secant(x_0, x_1, niter, tol, function, tolerance_type) -> Result:
    result = Result()
    table = Table()

    # Initial setup
    try:
        x_n = x_1 - function(x_1) * (x_1 - x_0) / (function(x_1) - function(x_0))
    except ZeroDivisionError:
        result.error_message = "Division by zero."
        return result

    x_prev = x_1
    x_prev_2 = x_0
    err = 100
    iteration_counter = 0

    error_type = determine_error_type(tolerance_type)

    # 0-th iteration
    table.add_row(x_1, function(x_1), None)

    # Secant method iterations
    while iteration_counter < niter and err >= tol:
        denominator = function(x_prev) - function(x_prev_2)
        try:
            x_n = x_prev - function(x_prev) * (x_prev - x_prev_2) / denominator
        except ZeroDivisionError:
            result.error_message = "Division by zero."
            return result

        err = calculate_error(x_n, x_prev, error_type)
        table.add_row(x_n, function(x_n), err)
        iteration_counter += 1
        x_prev_2 = x_prev
        x_prev = x_n

    df = table.as_dataframe()
    result.set_success_status()
    result.table = df
    return result


def show_secant():
    st.header("Secant Method")

    try:
        function_input = ui_input_function()

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
        function = sp.sympify(function_input)

        x = sp.symbols("x")
        first_derivative = sp.diff(function, x)
        second_derivative = sp.diff(first_derivative, x)

        function = nm_lambdify(function, x)
        result = secant(x0, x1, niter, tol, function, tolerance_type)

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
    except Exception as e:
        st.error("Error: Check your input")
        print(e)
