import streamlit as st
import sympy as sp


def generate_report(
    n_iterations,
    func,
    tolerance,
    type_of_tolerance,
    x_symbol,
    first_derivative,
    second_derivative,
):
    first_derivative = sp.lambdify(x_symbol, sp.sympify(first_derivative), "numpy")
    second_derivative = sp.lambdify(x_symbol, sp.sympify(second_derivative), "numpy")

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
        pass
