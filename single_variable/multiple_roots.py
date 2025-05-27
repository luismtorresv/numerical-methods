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

from .report import generate_report


def multiple_roots(x0, niter, tol, function, df, d2f, tolerance_type):
    table = []
    xi = x0
    for i in range(niter):
        fx = function(xi)
        dfx = df(xi)
        d2fx = d2f(xi)

        if dfx == 0:
            return {
                "status": "error",
                "message": "The first derivative is equal to 0. The method is not applicable.",
            }

        # Fórmula del método
        xi_next = xi - (fx * dfx) / (dfx**2 - fx * d2fx)
        error = abs(xi_next - xi)

        # Guarda resultados de la iteración
        table.append([i + 1, xi, fx, dfx, d2fx, xi_next, error])

        # Verifica si se cumple la tolerancia
        if tolerance_type == "Significant Figures":
            if error < tol:
                break
        elif tolerance_type == "Correct Decimals":
            if round(error, int(-np.log10(tol))) == 0:
                break

        xi = xi_next

    return {
        "status": "success",
        "table": pd.DataFrame(
            table,
            columns=["Iteration", "x_n", "f(x)", "f'(x)", "f''(x)", "x_(i+1)", "Error"],
        ),
    }


def show_multiple_roots():
    st.header("Multiple Roots Method")

    try:
        function_input = ui_input_function()

        x0 = st.number_input(
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
        function_sp = sp.sympify(function_input)
        st.latex(f"f({x}) = {sp.latex(function_sp)}")

        # Preparar función, derivadas y método
        x = sp.symbols("x")
        function = nm_lambdify(function_sp, x)
        first_derivative = sp.diff(function, x)
        second_derivative = sp.diff(first_derivative, x)

        df_sp = sp.diff(function_sp, x)
        d2f_sp = sp.diff(df_sp, x)

        df = nm_lambdify(df_sp, x)
        d2f = nm_lambdify(d2f_sp, x)

        result = multiple_roots(x0, niter, tol, function, df, d2f, tolerance_type)

        if result["status"] == "error":
            st.error(result["message"])
        else:
            mid = result["table"].iloc[-1]["x_i"]
            if function(mid) < 0 + tol:
                decimals = show_table(result["table"])
                st.success(
                    f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {function(mid):.{decimals}f}"
                )
            else:
                st.warning(
                    f"Method did not converge, potentially because of a discontinuity in the function."
                )

        graph(function_input)
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
        st.error("Error: Check your inputs")
        print(e)
