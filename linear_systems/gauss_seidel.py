import numpy as np
import pandas as pd
import streamlit as st

from utils.generate_linear_systems_report import generate_report
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

    Parameters:
    X : numpy array or list
        The true values (ground truth).
    X_L : numpy array or list
        The predicted values (from the model).
    norm : int, optional (default=2)
        The type of norm to use:
        1 - L1 norm (sum of absolute differences),
        2 - L2 norm (Euclidean distance),
        'inf' - L∞ norm (maximum difference).
    error_type : str, optional
        The type of error format:
        "Significant Figures" for relative error, or
        "Correct Decimals" for absolute error.
    sig_figs : int, optional
        The number of significant figures to round to (if error_type is "Significant Figures").
    decimal_places : int, optional
        The number of Correct Decimals to round to (if error_type is "Correct Decimals").

    Returns:
    error : float
        The calculated error, possibly rounded.
    """

    # Compute absolute difference between the true and predicted values
    diff = np.abs(X - X_L)

    # Choose norm calculation based on norm
    if norm == 1:  # L1 norm (sum of absolute differences)
        norm_error = np.sum(diff)
    elif norm == 2:  # L2 norm (Euclidean distance)
        norm_error = np.sqrt(np.sum(diff**2))
    elif norm == "inf":  # L∞ norm (maximum difference)
        norm_error = np.max(diff)
    else:
        raise ValueError("Invalid value for error_rel. Must be 1, 2, or 'inf'.")

    # Relative error if "Significant Figures" is selected
    if error_type == "Significant Figures":
        relative_error = norm_error / np.abs(X).max()  # Relative to the max value of X
        error = relative_error

    # Absolute error if "Correct Decimals" is selected
    elif error_type == "Correct Decimals":
        error = norm_error

    else:
        raise ValueError(
            "Invalid value for error_type. Must be 'Significant Figures' or 'Correct Decimals'."
        )

    return error


def rad_esp(T):
    """
    Computes the spectral radius (largest absolute eigenvalue) of a matrix T.
    """
    eig = np.linalg.eigvals(T)  # Compute eigenvalues of T
    rsp = np.max(np.abs(eig))  # Spectral radius is the max absolute eigenvalue
    return rsp


def make_tableMat(x_m_list, errores):
    """
    Creates a DataFrame from a list of values and corresponding errors.
    """
    table = pd.DataFrame(
        x_m_list[1:], columns=x_m_list[0]
    )  # Convert the list to a DataFrame
    table["Error"] = errores  # Add error column to the DataFrame
    return table


def gauss_seidel_method(
    A, b, X_i, tol, niter, norm=2, error_type="Significant Figures"
):
    """
    Performs the Gauss-Seidel iteration method for solving the linear system Ax = b.

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
    norm : int, optional (default=2)
        The type of norm to use for calculating error (1, 2, or 'inf').
    error_type : str, optional
        The type of error format:
        "Significant Figures" for relative error, or
        "Correct Decimals" for absolute error.

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
        list(map(float, X_i))
    )  # Add initial guess to the table as a list of floats

    # Check if A is singular (non-invertible)
    try:
        det = np.linalg.det(A)  # Check the determinant of A
        if det == 0:
            err = "Matrix A is singular (non-invertible). Please check the matrix and try again."
            return None, None, None, err, None, None
    except np.linalg.LinAlgError:
        err = "Matrix A is singular (non-invertible). Please check the matrix and try again."
        return None, None, None, err, None, None

    # Split matrix A into diagonal, lower, and upper parts
    D = np.diag(np.diagonal(A))
    L = -1 * np.tril(A, -1)
    U = -1 * np.triu(A, 1)

    # Compute the matrix T for Gauss-Seidel
    T = np.linalg.inv(D - L) @ U
    C = np.linalg.inv(D - L) @ b

    # Check if initial guess already satisfies the tolerance
    E = (A @ X_i) - b  # Residual error
    if np.allclose(E, np.zeros(len(b)), atol=tol):
        return X_i, make_tableMat(X_val, errores), rad_esp(T), err, T, C

    # Gauss-Seidel iteration loop
    X = X_i.copy()  # Initialize X with the initial guess
    for i in range(1, niter):
        X_L = X.copy()  # Save the current solution for error calculation

        # Update solution in place using the Gauss-Seidel formula
        for j in range(len(b)):
            X[j] = (
                b[j] - np.dot(A[j, :j], X[:j]) - np.dot(A[j, j + 1 :], X_L[j + 1 :])
            ) / A[j, j]

        # Append the new solution to the table
        X_val.append(np.squeeze(X.copy()))

        # Calculate the error
        error = calculate_error(X, X_L, norm, error_type)
        errores.append(error)

        # If error is smaller than tolerance, stop the iterations
        if error < tol:
            return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C

    # If the method doesn't converge within the given iterations, raise an error
    err = f"Gauss-Seidel method did not converge after {niter} iterations. Please check system parameters or increase the number of iterations."

    return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C


def show_gauss_seidel():
    st.header("Gauss Seidel Method")

    try:
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        tol, niter, tolerance_type = calculate_tolerance()

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        X, table, rad_esp, err, T, C = gauss_seidel_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        )

        if err == None:
            st.success("The Gauss Seidel method has converged successfully.")
            # Display the results
            st.write(f"**Solution Vector (x)**")
            show_matrix(X, deci=False)
            st.write(f"**Solution Table**")
            show_matrix(table)
            st.write("Spectral Radius: ", rad_esp)
            show_T_and_C(T, C)

            generate_report(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            )

        else:
            st.write("Spectral Radius: ", rad_esp)
            st.error(f"Error: Please Check Your Input. {err}")
    except Exception as e:
        st.error(f"Error: Please Check Your Input")
