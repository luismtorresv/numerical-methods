import pandas as pd
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify


def generate_report(
    n_iterations,
    func,
    tolerance,
    type_of_tolerance,
    x_symbol,
    first_derivative,
    second_derivative,
):
    st.markdown("# Generate Report")
    first_derivative = nm_lambdify(first_derivative, x_symbol)
    second_derivative = nm_lambdify(second_derivative, x_symbol)

    from single_variable.bisection import bisection
    from single_variable.false_position import regula_falsi
    from single_variable.fixed_point import fixed_point
    from single_variable.multiple_roots import multiple_roots
    from single_variable.newton_raphson import newton
    from single_variable.secant import secant

    try:
        with st.form("Report"):
            # Initial guess input
            x0 = st.number_input(
                "Initial guess (x₀)",
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
                help="The infimum of the desired search interval [a, b].",
            )
            b = st.number_input(
                "End point of search interval (b)",
                format="%.4f",
                value=3.0,
                step=0.0001,
                help="The supremum of the desired search interval [a, b].",
            )
            submitted = st.form_submit_button("Generate Report")
    except Exception as e:
        st.error(f"Invalid function input: Please check your inputs")
        return

    if submitted:
        results = {
            "bisection": bisection(
                a, b, n_iterations, tolerance, type_of_tolerance, func
            ),
            "false_position": regula_falsi(
                a, b, n_iterations, tolerance, type_of_tolerance, func
            ),
            "fixed_point": fixed_point(
                a, b, x0, tolerance, type_of_tolerance, n_iterations, func, g_input
            ),
            "multiple_roots": multiple_roots(
                x0,
                n_iterations,
                tolerance,
                func,
                first_derivative,
                second_derivative,
                type_of_tolerance,
            ),
            "secant": secant(a, b, n_iterations, tolerance, func, type_of_tolerance),
            "newton": newton(
                x0, n_iterations, tolerance, type_of_tolerance, func, first_derivative
            ),
        }

        table = {"method": [], "iteration": [], "X_solution": [], "Error": []}
        for methods in results:
            # TODO: Fixed point is not currently working properly with the rest of the code.
            if methods == "fixed_point":
                continue
            dict = results[methods]
            # Append the method.
            table["method"].append(methods)

            # Append the last iteration of each method.
            table["iteration"].append(dict["table"].index[-1])

            # Append the last X value of each method.
            table["X_solution"].append(0)

            # Append the Error of the last iteration.
            error_value = dict["table"].tail(1)["Error"].iloc[0]
            formatted_error = f"{error_value:.10e}"
            table["Error"].append(formatted_error)

        df = pd.DataFrame(table)
        st.latex(
            r"\text{Method} \quad \text{Iteration} \quad X_{\text{solution}} \quad \text{Error}"
        )
        st.write(df)
