import pandas as pd
import streamlit as st

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
            g_input = nm_lambdify(
                st.text_input(
                    "Transformation g(x): ",
                    value="2/x",
                    help="Enter g(x) such that g(x) = x at the root of f(x).",
                ),
                symbol,
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

        table = {
            "Method": [],
            "$n_\\text{iter}$": [],
            "$x_\\text{sol}$": [],
            "$f(x_\\text{sol})$": [],
            "$E$": [],
        }
        failed_methods = []

        for method_name, output in results.items():
            if output.has_failed():
                failed_methods.append(method_name)
                continue

            table["Method"].append(method_name)

            print(f"{output.table.shape[0] + 1}")
            table["$n_\\text{iter}$"].append(output.table.shape[0] + 1)

            # Append the last X value of each method.
            x_n = output.table.tail(1)["x"].iloc[0]
            table["$x_\\text{sol}$"].append(f"{x_n:.10e}")

            # Append the last X value of each method.
            f_x_n = output.table.tail(1)["f_x"].iloc[0]
            table["$f(x_\\text{sol})$"].append(f"{f_x_n:.10e}")

            # Append the Error of the last iteration.
            error_value = output.table.tail(1)["error"].iloc[0]
            formatted_error = f"{error_value:.10e}"
            table["$E$"].append(formatted_error)

        df = pd.DataFrame(table)
        st.table(df)

        # Find the best method
        best_iteration = min(table["$n_\\text{iter}$"])
        best_method_id = table["$n_\\text{iter}$"].index(
            min(table["$n_\\text{iter}$"])
        )  # Position of the lowest iteration
        st.write(
            f'The best method is {table["Method"][best_method_id]}, which took {best_iteration} iterations to converge.'
        )


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
    from single_variable.false_position import false_position
    from single_variable.fixed_point import fixed_point
    from single_variable.multiple_roots import multiple_roots
    from single_variable.newton_raphson import newton
    from single_variable.secant import secant

    return {
        "Bisection": bisection(
            a, b, n_iterations, tolerance, type_of_tolerance, f_function
        ),
        "False position": false_position(
            a, b, n_iterations, tolerance, type_of_tolerance, f_function
        ),
        "Fixed point": fixed_point(
            x_0, tolerance, type_of_tolerance, n_iterations, f_function, g_function
        ),
        "Multiple roots": multiple_roots(
            x_0,
            n_iterations,
            tolerance,
            f_function,
            first_derivative,
            second_derivative,
            type_of_tolerance,
        ),
        "Secant": secant(a, b, n_iterations, tolerance, f_function, type_of_tolerance),
        "Newton–Raphson": newton(
            x_0,
            n_iterations,
            tolerance,
            type_of_tolerance,
            f_function,
            first_derivative,
        ),
    }
