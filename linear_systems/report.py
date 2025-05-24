import pandas as pd
import streamlit as st
import sympy as sp

SOR_OMEGA_1 = 1
SOR_OMEGA_2 = 0.5
SOR_OMEGA_3 = 1.5


def generate_report(matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type):
    st.subheader("Method comparison report")

    from linear_systems.gauss_seidel import gauss_seidel_method
    from linear_systems.jacobi import jacobi_method
    from linear_systems.sor import sor_method

    with st.form("report"):
        submitted = st.form_submit_button("Generate report")
    if submitted:
        results = {
            "Jacobi": jacobi_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            ),
            "Gauss-Seidel": gauss_seidel_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 1
            "SOR-1": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_1,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 0.5 (Sub-Relaxation)
            "SOR-2": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_2,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 1.5 (Over-Relaxation)
            "SOR-3": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_3,
                norm_value,
                tolerance_type,
            ),
        }

        table = {
            "method": [],
            "N_iteration": [],
            "X_1": [],
            "X_2": [],
            "X_3": [],
            "Error": [],
        }

        for method in results:
            X, results_table, _, _, _, _ = results[method]

            # Respective method
            table["method"].append(method)

            x1, x2, x3 = X
            table["X_1"].append(x1[0])
            table["X_2"].append(x2[0])
            table["X_3"].append(x3[0])

            # Append the last iteration of each method.
            table["N_iteration"].append(results_table.index[-1])

            # Append the Error of the last iteration.
            error_value = results_table.tail(1)["Error"].iloc[0]
            formatted_error = f"{error_value:.10e}"
            table["Error"].append(formatted_error)

        df = pd.DataFrame(table)
        st.write(df)
