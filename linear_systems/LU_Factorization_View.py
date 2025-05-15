import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import (LU_result, definite_matrix_interface,
                                    graph_Ab)

from .LU_factorization import LU_factorization, solve_LU


def show_LU_factorization():
    st.header("LU Factorization without pivoting")

    st.markdown(
        """
    **LU Factorization** is a matrix decomposition method that breaks a square matrix $A$ into the product of a lower triangular matrix $L$ and an upper triangular matrix $U$. This is particularly useful for solving systems of linear equations, as it simplifies the process into forward and backward substitution steps.

    **Key Features:**
    - The matrix $A$ is decomposed such that $A = L \cdot U$, where:
      - $L$ is a lower triangular matrix with ones on the diagonal.
      - $U$ is an upper triangular matrix.
    - Allows for efficient computation of solutions for multiple right-hand side vectors $b$ once $L$ and $U$ are determined.
    - Requires the matrix to be non-singular (determinant ≠ 0).

    """
    )

    with st.expander("📘 How LU Factorization Works"):
        st.markdown(
            """
        **Procedure:**
        1. **Initialization**: Start with a square matrix $A$ and create an identity matrix $L$ and a copy of $A$ for $U$.

        2. **Decomposition**:
        - For each column $i$, divide the elements below the diagonal by the pivot element $a_{ii}$ to determine the factors for elimination.
        - Subtract the scaled row $i$ from .each subsequent row to create zeros below the diagonal in $U$.
        - Store the factors in the corresponding positions of $L$.

        3. **Validation**:
        - If a pivot element $a_{ii}$ is zero, the matrix cannot be decomposed without permuting rows, and the algorithm halts.

        **Forward and Backward Substitution**:
        - Once $L$ and $U$ are computed, the solution to $Ax = b$ is obtained in two steps:
        1. Solve $L \cdot y = b$ using forward substitution.
        2. Solve $U \cdot x = y$ using backward substitution.

        **Mathematical Formulas**:
        - Eliminate elements below the pivot:
        """
        )
        st.latex(
            r"""
        A_{j} = A_{j} - \frac{A_{j,i}}{A_{i,i}} A_{i}, \quad \text{for } j > i
        """
        )
        st.markdown(
            """
        - Store the factors in $L$:
        """
        )
        st.latex(
            r"""
        L_{j,i} = \frac{A_{j,i}}{A_{i,i}}, \quad \text{for } j > i
        """
        )

        st.markdown(
            """
        **Advantages**:
        - Efficient for solving multiple systems $Ax = b$ with the same $A$ but different $b$.
        - Reduces computational effort compared to Gaussian elimination for repeated solutions.

        **Disadvantages**:
        - Cannot decompose singular matrices without row permutations.
        - Requires careful handling of numerical precision, particularly for small pivot elements.

        **Use Cases**:
        - Solving large systems of linear equations.
        - Computing determinants (as the product of the diagonal elements of $U$).
        - Matrix inversion and numerical methods in scientific computing.
        """
        )

    matrix_A, vector_b = definite_matrix_interface()
    graph_Ab(matrix_A, vector_b)

    result = LU_factorization(matrix_A)

    if result["status"] == "error":
        st.error(result["message"])
        return
    else:
        L = result["L"]
        U = result["U"]

        vector_x = solve_LU(L, U, vector_b)

    LU_result(L=L, U=U, vector_x=vector_x)
