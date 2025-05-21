import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.generate_report import generate_report
from utils.interface_blocks import (
    calculate_tolerance,
    enter_function,
    graph,
    show_table,
)


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
            columns=["Iteration", "x_i", "f(x)", "f'(x)", "f''(x)", "x_(i+1)", "Error"],
        ),
    }


def show_multiple_roots():
    st.header("Multiple Roots Method")
    explain_methods()

    try:
        # Entrada de función y variable
        x, function_input = enter_function()

        col3 = st.columns(1)[0]
        with col3:
            x0 = st.number_input(
                "Initial Point (x_0)",
                format="%.4f",
                value=1.0,
                step=0.0001,
                help="Initial guess for the root. The method requires an initial value close to the actual root.",
            )

        # Calcular tolerancia
        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")
        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(sp.sympify(function_input))}")

        # Preparar función, derivadas y método
        x = sp.symbols(f"{x}")
        function = sp.lambdify(x, sp.sympify(function_input), "numpy")
        first_derivative = sp.diff(function, x)
        second_derivative = sp.diff(first_derivative, x)

        df = sp.lambdify(x, sp.diff(sp.sympify(function_input), x), "numpy")
        d2f = sp.lambdify(
            x, sp.diff(sp.diff(sp.sympify(function_input), x), x), "numpy"
        )

        result = multiple_roots(x0, niter, tol, function, df, d2f, tolerance_type)

        # Mostrar resultados o errores
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

        # Gráfica de la función
        graph(x, function_input)
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

    graph(x, function_input)


def explain_methods():
    st.markdown(
        """
    The **Newton's Method for Multiple Roots** is a numerical technique used to approximate roots of a function  $f(x)$ ,
    especially when the root has multiplicity greater than one. In such cases, the standard Newton-Raphson Method
    may converge slowly or fail entirely.

    This method modifies the Newton-Raphson formula to account for higher multiplicity using the first and second derivatives.
    """
    )

    with st.expander("📘 How the Newton's Method for Multiple Roots Works"):
        st.markdown(
            """
            **1. Formula for the Iteration:**
        """
        )
        st.latex(
            r"""
        x_{i+1} = x_i - \frac{f(x_i)f'(x_i)}{(f'(x_i))^2 - f(x_i)f''(x_i)}
        """
        )
        st.markdown(
            """
            - $f'(x_i)$: First derivative of $f(x)$ evaluated at $x_i$.
            - $f''(x_i)$: Second derivative of $f(x)$ evaluated at $x_i$.
            - This formula incorporates the second derivative to improve convergence for multiple roots.

            **2. Choose Initial Guess $x_0$:**
            - Start with an initial guess $x_0$ close to the suspected root.

            **3. Iteration Process:**
            - Compute $f(x_i)$, $f'(x_i)$, and $f''(x_i)$.
            - Apply the formula to compute $x_{i+1}$.
            - Repeat until the error is less than a specified tolerance.

            **4. Error Check:**
            - The error is calculated as:
        """
        )
        st.latex(
            r"""
        \text{Error} = |x_{i+1} - x_i|
        """
        )
        st.markdown(
            """
            - The iteration stops when the error is below the tolerance threshold, which can be based on:
            - **Significant Figures:** Error must be less than a given tolerance $\text{tol}$.
            - **Correct Decimals:** The error rounded to the specified precision is zero.

            **5. Special Case:**
            - If $f'(x_i) = 0$, the method fails because the denominator in the formula becomes zero.
        """
        )
