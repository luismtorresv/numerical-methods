import numpy as np
import pandas as pd


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
