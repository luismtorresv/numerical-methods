import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify


def generate_report(
    n_iterations,
    f_function,
    tolerance,
    type_of_tolerance,
    symbol,
    first_derivative,
    second_derivative,
):
    st.subheader("Method comparison report")
    first_derivative = nm_lambdify(first_derivative, symbol)
    second_derivative = nm_lambdify(second_derivative, symbol)

    try:
        with st.form("Report"):
            # Initial guess input
            x0 = st.number_input(
                "Initial guess ($x_0$)",
                format="%.4f",
                value=2.0,
                step=0.0001,
                help="Provide the initial guess for the root.",
            )

            # Input for transformed function g(x)
            g_input = st.text_input(
                "Transformation g(x): ",
                value="2/x",
                help="Enter g(x) such that g(x) = x at the root of f(x).",
            )
            a = st.number_input(
                "Initial point of search interval (a)",
                format="%.4f",
                value=0.1,
                step=0.0001,
            )
            b = st.number_input(
                "End point of search interval (b)",
                format="%.4f",
                value=3.0,
                step=0.0001,
            )
            submitted = st.form_submit_button("Generate report")
    except Exception as e:
        st.error(f"Invalid function input: Please check your inputs")
        return

    if submitted:
        results = _run_all_methods(
            x0,
            a,
            b,
            n_iterations,
            tolerance,
            type_of_tolerance,
            f_function,
            g_input,
            first_derivative,
            second_derivative,
        )

        table = {"method": [], "iteration": [], "X_solution": [], "Error": []}
        for method in results:
            # TODO: Fixed point is not currently working properly with the rest of the code.
            if method == "fixed_point":
                continue
            method_result = results[method]
            # Append the method.
            table["method"].append(method)

            # Append the last iteration of each method.
            table["iteration"].append(method_result["table"].index[-1])

            # Append the last X value of each method.
            table["X_solution"].append(0)

            # Append the Error of the last iteration.
            error_value = method_result["table"].tail(1)["Error"].iloc[0]
            formatted_error = f"{error_value:.10e}"
            table["Error"].append(formatted_error)

        df = pd.DataFrame(table)
        st.write(df)


def _run_all_methods(
    x_0,
    a,
    b,
    n_iterations,
    tolerance,
    type_of_tolerance,
    f_function,
    g_function,
    first_derivative,
    second_derivative,
):
    from single_variable.bisection import bisection
    from single_variable.false_position import regula_falsi
    from single_variable.fixed_point import fixed_point
    from single_variable.multiple_roots import multiple_roots
    from single_variable.newton_raphson import newton
    from single_variable.secant import secant

    return {
        "bisection": bisection(
            a,
            b,
            n_iterations,
            tolerance,
            type_of_tolerance,
            f_function,
        ),
        "false_position": regula_falsi(
            a,
            b,
            n_iterations,
            tolerance,
            type_of_tolerance,
            f_function,
        ),
        "fixed_point": fixed_point(
            a,
            b,
            x_0,
            tolerance,
            type_of_tolerance,
            n_iterations,
            f_function,
            g_function,
        ),
        "multiple_roots": multiple_roots(
            x_0,
            n_iterations,
            tolerance,
            f_function,
            first_derivative,
            second_derivative,
            type_of_tolerance,
        ),
        "secant": secant(
            a,
            b,
            n_iterations,
            tolerance,
            f_function,
            type_of_tolerance,
        ),
        "newton": newton(
            x_0,
            n_iterations,
            tolerance,
            type_of_tolerance,
            f_function,
            first_derivative,
        ),
    }
