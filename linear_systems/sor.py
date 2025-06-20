import numpy as np
import streamlit as st

from utils.interface_blocks import (
    calculate_tolerance,
    definite_matrix_interface,
    graph_Ab,
)

from .report import generate_report
from .ui import ui_matrix_flow
from .utils import MatrixMethodOutput, calculate_error, make_tableMat, spectral_radius


def sor_method(A, b, X_i, tol, niter, omega, norm=2, error_type="Significant Figures"):
    """
    Performs the Successive Over-Relaxation (SOR) method for solving Ax = b.
    """
    err = None
    errores = [100] if error_type == "Significant Figures" else [0]

    X_val = [list(f"X_{i+1}" for i in range(len(b)))]
    X_val.append(list(map(float, X_i)))

    # Check if A is singular
    try:
        D = np.diag(np.diagonal(A))
        np.linalg.inv(D)
    except np.linalg.LinAlgError:
        err = "Matrix A is singular (non-invertible)."
        return MatrixMethodOutput(None, None, None, err, None, None)

    D = np.diag(np.diagonal(A))
    L = -1 * np.tril(A, -1)
    U = -1 * np.triu(A, 1)

    # Compute matrices for SOR
    T = np.linalg.inv(D - omega * L) @ ((1 - omega) * D + omega * U)
    C = omega * np.linalg.inv(D - omega * L) @ b

    X = X_i.copy()
    for i in range(1, niter):
        X_L = X.copy()
        X = T @ X + C

        X_val.append(np.squeeze(X))
        error = calculate_error(X, X_L, norm, error_type)
        errores.append(error)

        if error < tol:
            return MatrixMethodOutput(
                X, make_tableMat(X_val, errores), spectral_radius(T), err, T, C
            )

    err = f"SOR method did not converge after {niter} iterations."
    return MatrixMethodOutput(
        X, make_tableMat(X_val, errores), spectral_radius(T), err, T, C
    )


def show_SOR():
    st.header("Successive Over-Relaxation (SOR) Method")
    try:
        # Interfaz para definir la matriz, el vector b y otros parámetros iniciales
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface()

        # Parámetros adicionales: tolerancia, iteraciones y tipo de error
        tol, niter, tolerance_type = calculate_tolerance()

        # Factor de relajación ω
        omega = st.number_input(
            "Relaxation Factor (ω):", min_value=0.0, max_value=2.0, step=0.1, value=1.0
        )

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        # Ejecutar el método SOR
        matrix_method_output = sor_method(
            matrix_A, vector_b, x_0, tol, niter, omega, norm_value, tolerance_type
        )

        if ui_matrix_flow(matrix_method_output):
            generate_report(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            )
    except Exception as e:
        st.error("Error: Please Check The Input")
        print(e)
