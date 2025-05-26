import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.interface_blocks import calculate_tolerance, enter_function, graph

from .common import (
    ErrorType,
    Result,
    ResultStatus,
    calculate_error,
    determine_error_type,
)
from .report import generate_report


def false_position(a, b, niter, tol, tolerance_type, function) -> Result:
    result = Result()

    error_type = determine_error_type(tolerance_type)

    # Initialize dictionary for table
    table = {
        "i": [],
        "x": [],
        "f(x)": [],
        "error": [],
    }

    # Calculate initial function values
    f_a = function(a)
    f_b = function(b)

    if (f_b * f_a) >= 0:
        result.error_message = (
            "Invalid arguments:"
            + " "
            + "The function does not change sign in the interval."
        )
        return result

    iteration_counter = 0
    error = 100
    x_intersect = (a * f_b - b * f_a) / (f_b - f_a)
    f_x = function(x_intersect)

    # Store initial iteration
    table["i"].append(iteration_counter)
    table["x"].append(x_intersect)
    table["f(x)"].append(f_x)
    table["error"].append(error)

    # Iterate
    while error > tol != 0 and iteration_counter < niter:
        if f_a * f_x < 0:
            b = x_intersect
            f_b = f_x
        else:
            a = x_intersect
            f_a = f_x

        old_intersect = x_intersect

        x_intersect = (a * f_b - b * f_a) / (f_b - f_a)
        f_x = function(x_intersect)

        error = calculate_error(x_intersect, old_intersect, error_type)
        iteration_counter += 1
        table["i"].append(iteration_counter)
        table["x"].append(x_intersect)
        table["f(x)"].append(f_x)
        table["error"].append(error)

    df = pd.DataFrame(table)
    if f_x == 0 or error < tol:
        result.status = ResultStatus.SUCCESS
        result.table = df
        return result

    # Too many iterations.
    result.table = df
    return result


def show_false_position():
    st.header("False Position Method")
    try:
        x, function_input = enter_function(
            placeholder_function="x**2 - 4", placeholder_variable="x"
        )

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

        x = sp.symbols(f"{x}")
        function_sp = sp.sympify(function_input)
        first_derivative = sp.diff(function_sp, x)
        second_derivative = sp.diff(first_derivative, x)

        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(function_sp)}")

        lambda_function = nm_lambdify(function_sp, x)

        # DO CHECKS ON INPUT INTEGRITY
        # check if derivative is continuous in general

        result = false_position(a, b, niter, tol, tolerance_type, lambda_function)

        if result.has_failed():
            st.error(result.error_message)
            return

        # Add a slider to choose the number of decimals to display
        decimals = st.slider(
            "Select number of decimals to display on table",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
        # Format the dataframe to display the selected number of decimals
        result_display = result.table.style.format(
            f"{{:.{decimals}f}}"
        )  # Use f-string to format dynamically

        mid = result.table.iloc[-1]["x"]
        if lambda_function(mid) < 0 + tol:
            st.success(
                f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {lambda_function(mid):.{decimals}f}"
            )
            st.subheader("Results")
            st.dataframe(result_display, use_container_width=True)
        else:
            st.warning(
                f"Method did not converge, potentially because of a discontinuity in the function."
            )

        graph(x, function_input)
        generate_report(
            niter,
            lambda_function,
            tol,
            tolerance_type,
            x,
            first_derivative,
            second_derivative,
        )
    except Exception as ep:
        st.error("Error: Check inputs")
        print(ep)
        return
