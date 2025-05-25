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


def spectral_radius(T):
    """
    Computes the spectral radius (largest absolute eigenvalue) of a matrix T.
    """
    eigenvalues = np.linalg.eigvals(T)  # Compute eigenvalues of T
    return np.max(np.abs(eigenvalues))  # Spectral radius is the max absolute eigenvalue


def make_tableMat(x_m_list, errores):
    """
    Creates a DataFrame from a list of values and corresponding errors.
    """
    table = pd.DataFrame(
        x_m_list[1:], columns=x_m_list[0]
    )  # Convert the list to a DataFrame
    table["Error"] = errores  # Add error column to the DataFrame
    return table
