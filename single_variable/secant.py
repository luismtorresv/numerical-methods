import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import (
    calculate_tolerance,
    enter_function,
    graph,
    show_table,
)


def secant(x0, x1, niter, tol, function, tolerance_type):
    table = []

    # Initial setup
    xn = x1 - function(x1) * (x1 - x0) / (function(x1) - function(x0))
    x_prev = x1
    x_prev2 = x0
    err = 100
    iter = 0

    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # First iteration (iteration 0)
    row = {"x_{n-1}": x0, "x_n": x1, "f(x_n)": function(x1), f"{Error}": None}
    table.append(row)

    # Secant method iterations
    while iter < niter and err >= tol:
        # Update xn
        xn = x_prev - function(x_prev) * (x_prev - x_prev2) / (
            function(x_prev) - function(x_prev2)
        )

        # Calculate error based on tolerance type
        if tolerance_type == "Significant Figures":
            # Calculate relative error
            err = abs((xn - x_prev) / xn)
        elif tolerance_type == "Correct Decimals":
            # Calculate absolute error
            err = abs(xn - x_prev)

        # Append row for current iteration
        row = {"x_{n-1}": x_prev, "x_n": xn, "f(x_n)": function(xn), f"{Error}": err}
        table.append(row)

        iter += 1
        x_prev2 = x_prev
        x_prev = xn

    # Convert table to DataFrame and return
    df = pd.DataFrame(table)
    return {"status": "success", "table": df}


def show_secant():
    st.markdown(
        """
    The **Secant Method** is a numerical technique used to approximate the roots of a function  f(x) .
    Unlike the Newton-Raphson Method, it does not require the computation of derivatives. Instead, it approximates
    the derivative using a secant line through two points on the function.

    The method is iterative and converges faster than the Bisection Method but is less robust than Newton-Raphson.
    """
    )

    with st.expander("📘 How the Secant Method Works"):
        st.markdown(
            """
        **1. Choose Two Initial Guesses $x_0$ and $x_1$ close to the suspected root.**

        **2. Apply the Iteration Formula:**
        """
        )
        st.latex(
            r"""
        x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}
        """
        )
        st.markdown(
            """
            - This formula uses the slope of the secant line through $(x_{n-1}, f(x_{n-1}))$ and $(x_n, f(x_n))$
            to compute the next approximation $x_{n+1}$.

            **3. Check for Convergence:**
            - Stop when $|f(x_{n+1})|$ is sufficiently close to zero or $|x_{n+1} - x_n|$ is less than a specified tolerance.

            **4. Repeat:**
            - Use $x_{n+1}$ and $x_n$ as the new points and iterate until convergence.

            **Advantages:**
            - Does not require the computation of derivatives.
            - Typically converges faster than the Bisection Method.

            **Disadvantages:**
            - May fail if $f(x_n) = f(x_{n-1})$ or if the initial guesses are not close to the root.
        """
        )

    st.header("Secant Method")

    try:
        x, function_input = enter_function()

        col3, col4 = st.columns(2)
        with col3:
            x0 = st.number_input(
                "First Point (x_0)",
                format="%.4f",
                value=0.1,
                step=0.0001,
                help="The first initial guess for the root. It is a value where the function is evaluated.",
            )

        with col4:
            x1 = st.number_input(
                "Second Point (x_1)",
                format="%.4f",
                value=0.2,
                step=0.0001,
                help="The second initial guess for the root. It should be close to x0 and the function should have different signs at x0 and x1.",
            )

        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")
        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(sp.sympify(function_input))}")

        x = sp.symbols(f"{x}")
        function = sp.lambdify(x, sp.sympify(function_input), "numpy")
        result = secant(x0, x1, niter, tol, function, tolerance_type)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            result = result["table"]

        mid = result.iloc[-1]["x_n"]

        if function(mid) <= 0 + tol:
            st.subheader("Results")
            decimals = show_table(result)
            st.success(
                f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {function(mid):.{decimals}f}"
            )
        else:
            st.warning(
                f"Method did not converge, potentially because of a discontinuity in the function."
            )

        graph(x, function_input)
    except Exception as e:
        st.error("Error: Check your input")
        print(e)
