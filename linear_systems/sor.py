import numpy as np
import pandas as pd
import streamlit as st

from utils.interface_blocks import (
    calculate_tolerance,
    definite_matrix_interface,
    graph_Ab,
    show_matrix,
    show_T_and_C,
)


def calculate_error(X, X_L, norm=2, error_type=None):
    """
    Calculates the error between two arrays (X and X_L) based on specified norm and error format.
    """
    diff = np.abs(X - X_L)
    if norm == 1:
        norm_error = np.sum(diff)
    elif norm == 2:
        norm_error = np.sqrt(np.sum(diff**2))
    elif norm == "inf":
        norm_error = np.max(diff)
    else:
        raise ValueError("Invalid norm value. Must be 1, 2, or 'inf'.")

    if error_type == "Significant Figures":
        relative_error = norm_error / np.abs(X).max()
        return relative_error
    elif error_type == "Correct Decimals":
        return norm_error
    else:
        raise ValueError(
            "Invalid error_type. Must be 'Significant Figures' or 'Correct Decimals'."
        )


def rad_esp(T):
    """
    Computes the spectral radius of a matrix T.
    """
    eig = np.linalg.eigvals(T)
    rsp = np.max(np.abs(eig))
    return rsp


def make_tableMat(x_m_list, errores):
    """
    Creates a DataFrame from a list of values and corresponding errors.
    """
    table = pd.DataFrame(x_m_list[1:], columns=x_m_list[0])
    table["Error"] = errores
    return table


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
        return None, None, None, err, None, None

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
            return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C

    err = f"SOR method did not converge after {niter} iterations."
    return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C


def show_SOR():
    st.header("Successive Over-Relaxation (SOR) Method")
    st.markdown(
        """
    **Successive Over-Relaxation (SOR) Method** is an iterative technique for solving linear systems of equations,
    extending the Gauss-Seidel method by introducing a relaxation factor, $\\omega$, to accelerate convergence.
    """
    )

    with st.expander("📘 Detailed Explanation of the SOR Method"):
        st.markdown(
            """
            **Method Overview:**
            - The SOR method is derived from splitting the matrix $A$ into its diagonal ($D$), lower triangular ($L$),
            and upper triangular ($U$) components, similar to the Gauss-Seidel method, but with an over-relaxation factor $\\omega$.
            - The formula for the iteration is:
            """
        )
        st.latex(
            r"""
        x^{(k+1)} = (D - \omega L)^{-1} \left[ \omega b + \left( (1 - \omega) D + \omega U \right) x^{(k)} \right]
        """
        )
        st.markdown(
            """
            where:
            - $\\omega$ is the relaxation factor ($0 < \\omega < 2$).
            - If $\\omega = 1$, the method reduces to the Gauss-Seidel method.

            **Procedure:**
            1. **Initialization**:
            - Start with an initial guess $X^{(0)}$ and choose a relaxation factor $\\omega$.
            - Decompose $A$ into $D$, $L$, and $U$.

            2. **Iteration**:
            - Compute matrices:
                - $T = (D - \\omega L)^{-1}((1 - \\omega) D + \\omega U)$
                - $C = \\omega (D - \\omega L)^{-1} b$
            - Update the solution using:
                - $X^{(k+1)} = T X^{(k)} + C$

            3. **Stopping Criteria**:
            - Stop if the error norm $||X^{(k+1)} - X^{(k)}||$ is below a given tolerance.

            **Convergence:**
            - The SOR method converges faster than Gauss-Seidel for well-chosen values of $\\omega$.
            - For optimal $\\omega$, the method achieves the fastest convergence.

            **Advantages:**
            - Improves convergence speed over Gauss-Seidel for certain systems.
            - Simple to implement once $\\omega$ is determined.

            **Disadvantages:**
            - Choosing the optimal $\\omega$ is not straightforward.
            - May not converge for poorly conditioned matrices.

            **Key Parameters:**
            - **Relaxation Factor** ($\\omega$):
            - $0 < \\omega < 1$: Under-relaxation (slower convergence but safer).
            - $\\omega = 1$: Equivalent to Gauss-Seidel.
            - $1 < \\omega < 2$: Over-relaxation (faster convergence for diagonally dominant matrices).

            """
        )
    try:
        # Interfaz para definir la matriz, el vector b y otros parámetros iniciales
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        # Parámetros adicionales: tolerancia, iteraciones y tipo de error
        tol, niter, tolerance_type = calculate_tolerance()

        # Factor de relajación ω
        omega = st.number_input(
            "Relaxation Factor (ω):", min_value=0.0, max_value=2.0, step=0.1, value=1.0
        )

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        # Ejecutar el método SOR
        X, table, rad_esp, err, T, C = sor_method(
            matrix_A, vector_b, x_0, tol, niter, omega, norm_value, tolerance_type
        )

        if err is None:
            st.success("The SOR method has converged successfully.")

            # Mostrar los resultados
            st.write(f"**Solution Vector (x)**")
            show_matrix(X, deci=False)

            st.write(f"**Solution Table**")
            show_matrix(table)

            st.write("Spectral Radius: ", rad_esp)
            show_T_and_C(T, C)
        else:
            st.error(err)
    except Exception as e:
        st.error("Error: Please Check The Input")
        print(e)
