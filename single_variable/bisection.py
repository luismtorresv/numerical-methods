import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify
from utils.generate_report import generate_report
from utils.interface_blocks import calculate_tolerance, enter_function, graph


def bisection(a, b, niter, tol, tolerance_type, function):
    if b < a:
        return {
            "status": "error",
            "message": "Invalid Arguments, b must be greater than a.",
        }

    table = []
    row = {}
    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # initial call
    row["a"] = a
    row["b"] = b
    row["mid"] = (a + b) / 2
    row["f(a)"] = function(a)
    row["f(mid)"] = function((a + b) / 2)
    row["f(b)"] = function(b)
    row["Error"] = None
    table.append(row)
    err = 100

    if function(a) * function(b) > 0:
        return {
            "status": "error",
            "message": "Invalid Arguments, the function does not change sign in the interval.",
        }
    else:
        mid = (a + b) / 2
        iter = 0
        while iter < niter and err > tol:
            if function(a) * function(mid) <= 0:
                b = mid
            else:
                a = mid
            iter += 1
            prev_mid = mid
            mid = (a + b) / 2

            row = {}
            row["a"] = a
            row["b"] = b
            row["mid"] = mid
            row["f(a)"] = function(a)
            row["f(mid)"] = function(mid)
            row["f(b)"] = function(b)
            if Error == "Relative Error":
                row["Error"] = abs((mid - prev_mid) / mid)
            else:
                row["Error"] = abs(mid - prev_mid)
            err = row["Error"]
            table.append(row)

        df = pd.DataFrame(table)
        return {"status": "success", "table": df}


def show_bisection():
    try:
        st.header("Bisection Method")

        x, function_input = enter_function(
            placeholder_function="x**2 - 4", placeholder_variable="x"
        )

        col3, col4 = st.columns(2)
        with col3:
            a = st.number_input(
                "Initial point of search interval (a)",
                format="%.4f",
                value=0.1,
                step=0.0001,
                help="The infimum of the desired search interval [a, b].",
            )
        with col4:
            b = st.number_input(
                "End point of search interval (b)",
                format="%.4f",
                value=3.0,
                step=0.0001,
                help="The supremum of the desired search interval [a, b].",
            )

        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

        x = sp.symbols(f"{x}")
        function_sp = sp.sympify(function_input)
        first_derivative = sp.diff(function_sp, x)
        second_derivative = sp.diff(first_derivative, x)

        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(function_sp)}")

        function = nm_lambdify(function_input, x)

        # DO CHECKS ON INPUT INTEGRITY
        # check if derivative is continuous in general

        result = bisection(a, b, niter, tol, tolerance_type, function)

        if result["status"] == "error":
            st.error(result["message"])
            graph(x, function_input)
            return
        else:
            result = result["table"]

        # Add a slider to choose the number of decimals to display
        decimals = st.slider(
            "Select number of decimals to display on table",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
        # Format the dataframe to display the selected number of decimals
        result_display = result.style.format(
            f"{{:.{decimals}f}}"
        )  # Use f-string to format dynamically

        st.subheader("Results")
        st.dataframe(result_display, use_container_width=True)

        mid = result.iloc[-1]["mid"]
        if function(mid) < 0 + tol:
            st.success(
                f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {function(mid):.{decimals}f}"
            )
        else:
            st.warning(
                f"Method did not converge, potentially because of a discontinuity in the function."
            )

    except Exception as e:
        st.error("Error: Check your inputs ")

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
