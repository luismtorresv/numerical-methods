import pandas as pd
import streamlit as st
import sympy as sp

from utils.generate_report import generate_report
from utils.interface_blocks import calculate_tolerance, enter_function, graph


def regula_falsi(a, b, niter, tol, tolerance_type, function):
    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # Initialize dictionary for table
    table = {
        "Iteration": [],
        "Xm": [],
        "f(Xm)": [],
        "Error": [],
    }

    # Calculate initial function values
    f_a = function(a)
    f_b = function(b)

    if (f_b * f_a) >= 0:
        return {
            "status": "error",
            "message": "Invalid Arguments, the function does not change sign in the interval.",
        }

    else:
        c = 0
        Error = 100
        x_intersect = (a * f_b - b * f_a) / (f_b - f_a)
        fx = function(x_intersect)

        # Store initial iteration
        table["Iteration"].append(c)
        table["Xm"].append(x_intersect)
        table["f(Xm)"].append(fx)
        table["Error"].append(Error)

        # Iterate
        while Error > tol != 0 and c < niter:
            if f_a * fx < 0:
                b = x_intersect
                f_b = fx
            else:
                a = x_intersect
                f_a = fx

            old_intersect = x_intersect
            x_intersect = (a * f_b - b * f_a) / (f_b - f_a)
            fx = function(x_intersect)

            if Error == "Relative Error":
                Error = abs((x_intersect - old_intersect) / x_intersect)
            else:
                Error = abs(x_intersect - old_intersect)

            c += 1
            table["Iteration"].append(c)
            table["Xm"].append(x_intersect)
            table["f(Xm)"].append(fx)
            table["Error"].append(Error)


        df = pd.DataFrame(table)
        if fx == 0:
            #print(f"{result} es raiz de f(x)")
            return {"status": "success", "table": df}
        elif Error < tol:
            # print(f"{x} es una aproximación de una raíz con tolerancia {Tol}")
            return {"status": "success", "table": df}
        else:
            #print(f"Fracaso en {niter} iteraciones")
            return {"status": "error", "message": f"Fracaso en {niter} iteraciones"}


def show_regula_falsi():
    explain_method()
    st.header("False Position Method")
    try:
        x, function_input = enter_function(
            placeholder_function="x**2 - 4", placeholder_variable="x"
        )

        col3, col4 = st.columns(2)
        with col3:
            a = st.number_input(
                "Initial point of search interval (a)",
                format="%.4f",
                value=0.1,
                step=0.0001,
                help="The infimum of the desired search interval [a, b].",
            )
        with col4:
            b = st.number_input(
                "End point of search interval (b)",
                format="%.4f",
                value=3.0,
                step=0.0001,
                help="The supremum of the desired search interval [a, b].",
            )

        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

        x = sp.symbols(f"{x}")
        function_sp = sp.sympify(function_input)
        first_derivative = sp.diff(function_sp, x)
        second_derivative = sp.diff(first_derivative, x)

        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(function_sp)}")

        lambda_function = sp.lambdify(x, function_sp, "numpy")

        # DO CHECKS ON INPUT INTEGRITY
        # check if derivative is continuous in general

        result = regula_falsi(a, b, niter, tol, tolerance_type, lambda_function)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            result = result["table"]

        # Add a slider to choose the number of decimals to display
        decimals = st.slider(
            "Select number of decimals to display on table",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
        # Format the dataframe to display the selected number of decimals
        result_display = result.style.format(
            f"{{:.{decimals}f}}"
        )  # Use f-string to format dynamically

        mid = result.iloc[-1]["Xm"]
        if lambda_function(mid) < 0 + tol:
            st.success(
                f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {lambda_function(mid):.{decimals}f}"
            )
            st.subheader("Results")
            st.dataframe(result_display, use_container_width=True)
        else:
            st.warning(
                f"Method did not converge, potentially because of a discontinuity in the function."
            )

        graph(x, function_input)
        generate_report(
            niter,
            lambda_function,
            tol,
            tolerance_type,
            x,
            first_derivative,
            second_derivative,
        )
    except Exception as ep:
        st.error("Error: Check inputs")
        print(ep)
        return


def explain_method():
    st.markdown(
        """
    The **False Position Method**, also called the **False Position Method**, is a root-finding algorithm used to
    approximate the solution of the equation  f(x) = 0  for a continuous function  f(x) .
    It is based on the Intermediate Value Theorem and linear interpolation.
    """
    )

    with st.expander("📘 How the False Position Method Works"):
        st.markdown(
            """
            **1. Interval Selection:**
            - Start with an interval $[a, b]$ such that $f(a) \cdot f(b) < 0$.
            This ensures there is at least one root in the interval.

            **2. Compute the Next Approximation:**
            - Use the formula for linear interpolation to find the root approximation $x_r$:
        """
        )
        st.latex(
            r"""
        x_r = b - \frac{f(b)(b - a)}{f(b) - f(a)}
        """
        )
        st.markdown(
            """
            - This formula determines the $x$-coordinate of the intersection between the secant line connecting
            $(a, f(a))$ and $(b, f(b))$ and the $x$-axis.

            **3. Update the Interval:**
            - Evaluate $f(x_r)$:
            - If $f(a) \cdot f(x_r) < 0$, the root lies in $[a, x_r]$, so update $b = x_r$.
            - If $f(b) \cdot f(x_r) < 0$, the root lies in $[x_r, b]$, so update $a = x_r$.
            - If $f(x_r) = 0$, the method has found an exact root.

            **4. Convergence Criteria:**
            - Stop the iteration when:
            - The absolute error is below a tolerance:
        """
        )
        st.latex(
            r"""
        \text{Error} = |x_r^{(i+1)} - x_r^{(i)}|
        """
        )
        st.markdown(
            """
            - Or, the function value at $x_r$ is sufficiently close to zero:
        """
        )
        st.latex(
            r"""
        |f(x_r)| < \text{tol}.
        """
        )
        st.markdown(
            """
            **Advantages:**
            - The method combines the accuracy of the Bisection Method and the speed of linear interpolation.
            - It always converges for continuous functions satisfying $f(a) \cdot f(b) < 0$.

            **Limitations:**
            - Convergence may be slow if the function is highly non-linear or one side of the interval dominates.
        """
        )
