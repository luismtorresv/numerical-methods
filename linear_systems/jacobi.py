import numpy as np
import streamlit as st
import sympy as sp

from utils.interface_blocks import (
    calculate_tolerance,
    definite_matrix_interface,
    graph_Ab,
    show_matrix,
    show_T_and_C,
)

from .report import generate_report
from .utils import calculate_error, make_tableMat, spectral_radius


def jacobi_method(A, b, X_i, tol, niter, norm=2, error_type="Significant Figures"):
    """
    Performs the Jacobi iteration method for solving the linear system Ax = b.

    Parameters:
    A : numpy array
        The matrix A.
    b : numpy array
        The vector b.
    X_i : numpy array
        The initial guess for X.
    tol : float
        The tolerance for stopping criteria (convergence).
    niter : int
        The maximum number of iterations.
    error_rel : int, optional (default=2)
        The type of norm to use for calculating error (1, 2, or 'inf').

    Returns:
    X : numpy array
        The solution vector after convergence or max iterations.
    table : pandas DataFrame
        A table of X values across iterations with corresponding errors.
    rsp : float
        The spectral radius of the matrix T.

    Raises:
    ValueError: If matrix A is singular (non-invertible) or if the system does not converge within the given iterations.
    """
    err = None
    errores = [100]  # List to track errors
    if error_type == "Significant Figures":
        errores = [0]

    # Initialize the table of X values
    X_val = [list(f"X_{i+1}" for i in range(len(b)))]  # Create labels for X values
    X_val.append(
        list(map(int, X_i))
    )  # Add initial guess to the table as a list of integers

    # Check if A is singular (non-invertible)
    try:
        # Try to compute the inverse of D (the diagonal matrix)
        D = np.diag(np.diagonal(A))
        np.linalg.inv(D)  # If D is singular, this will raise an exception
    except np.linalg.LinAlgError:
        err = "Matrix A is singular (non-invertible). Please check the matrix and try again."
        X = []
        return None, None, None, err, None, None

    # Split matrix A into diagonal, lower, and upper parts
    D = np.diag(np.diagonal(A))
    L = -1 * np.tril(A, -1)
    U = -1 * np.triu(A, 1)

    # Compute T and C matrices for Jacobi method
    T = np.linalg.inv(D) @ (L + U)
    C = np.linalg.inv(D) @ b

    # Check if initial guess already satisfies the tolerance
    E = (A @ X_i) - b  # Residual error
    if np.allclose(E, np.zeros(len(b)), atol=tol):
        return X_i, make_tableMat(X_val, errores), spectral_radius(T), err, T, C

    # Jacobi iteration loop
    X = X_i.copy()  # Initialize X with the initial guess
    for i in range(1, niter):
        X_L = X.copy()  # Save current solution for error calculation
        X = T @ X + C  # Update solution

        # Append the new solution to the table
        X_val.append(np.squeeze(X))

        # Calculate the error
        error = calculate_error(X, X_L, norm, error_type)
        errores.append(error)

        # If error is smaller than tolerance, stop the iterations
        if error < tol:
            return X, make_tableMat(X_val, errores), spectral_radius(T), err, T, C

    # If the method doesn't converge within the given iterations, raise an error
    err = f"Jacobi method did not converge after {niter} iterations. Please check system parameters or increase the number of iterations."

    # Return after reaching max iterations
    return X, make_tableMat(X_val, errores), spectral_radius(T), err, T, C


def show_Jacobi():
    st.header("Jacobi Method")

    try:
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        tol, niter, tolerance_type = calculate_tolerance()

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        X, table, spectral_radius_T, err, T, C = jacobi_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        )

        st.divider()
        st.header("Result")
        if err:
            st.error(err)
            return
        st.success(f":material/check: Method has converged to a solution.")

        st.divider()

        st.subheader("Intermediate results")
        show_T_and_C(T, C)

        st.divider()

        st.subheader("Convergence")
        st.metric("Spectral radius of $T$", spectral_radius_T)
        if spectral_radius_T < 1:
            message = "Since $\\rho(T) < 1$, the method was guaranteed to converge."
        else:
            message = (
                "Since $\\rho(T) \geq 1$, "
                "the method was _not_ guaranteed to converge."
            )
        st.write(message)

        st.divider()

        st.header("Solution")
        X = sp.Matrix(X)
        st.latex("\\vec{x} = " + sp.latex(X))

        st.subheader("Table")
        show_matrix(table, deci=False)

        st.divider()

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
        st.error("Error: Please Check Your Input")
        st.write(e)
