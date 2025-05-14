import numpy as np
import pandas as pd


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
        return X_i, make_tableMat(X_val, errores), rad_esp(T), err, T, C

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
            return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C

    # If the method doesn't converge within the given iterations, raise an error
    err = f"Jacobi method did not converge after {niter} iterations. Please check system parameters or increase the number of iterations."

    # Return after reaching max iterations
    return X, make_tableMat(X_val, errores), rad_esp(T), err, T, C
