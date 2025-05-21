import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import calculate_tolerance, enter_function, graph


def fixed_point(a, b, X0, Tol, type_of_tol, Niter, Fun, Fun_g):
    # Check the G function

    x_sym = sp.symbols("x")
    try:
        g_expr = sp.sympify(Fun_g.replace("^", "**"))
    except (sp.SympifyError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {e}")
    g_func = sp.lambdify(x_sym, g_expr, modules=["math"])

    # Inicialización de listas para la tabla
    iteraciones = []
    xn = []
    fn = []
    errores = []

    # Primera iteración
    x = X0
    f = Fun(x)
    c = 0
    Error = 100  # Error inicial arbitrario

    iteraciones.append(c)
    xn.append(x)
    fn.append(f)
    errores.append(Error)
    while Error > Tol and f != 0 and c < Niter:
        x = g_func(x)  # Nueva aproximación usando g(x)

        # Validar que la nueva aproximación esté en el intervalo [a, b]
        if x < a or x > b:
            print(
                f"Error: La iteración {c} generó un valor fuera del intervalo [{a}, {b}]."
            )
            break

        f = Fun(x)  # Evaluamos f(x)

        c += 1
        if type_of_tol == "D.C":
            Error = abs(x - xn[-1])  # Cálculo del error absoluto
        else:
            Error = abs((x - xn[-1]) / x)  # Cálculo del error relativo

        # Guardar valores en listas
        iteraciones.append(c)
        xn.append(x)
        fn.append(f)
        errores.append(Error)

    # Mostrar resultados finales

    # Crear y mostrar la tabla de iteraciones
    tabla = pd.DataFrame(
        {"Iteración": iteraciones, "Xn": xn, "f(Xn)": fn, "Error": errores}
    )

    if f == 0:
        # print(f"{x} es raíz de f(x)")
        return tabla, x
    elif Error < Tol:
        # print(f"{x} es una aproximación de una raíz con tolerancia {Tol}")
        return tabla, x
    else:
        # print(f"Fracaso en {Niter} iteraciones")
        return None, Niter


def validate_fixed_point_function(x_symbol, f_function, g_function):
    """
    Validate fixed-point iteration requirements.

    Args:
        x_symbol (sympy.Symbol): Variable symbol
        f_function (sympy.Expr): Original function f(x)
        g_function (sympy.Expr): Transformed function g(x)

    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        roots = sp.solve(f_function, x_symbol)
        if not roots:
            return False

        g_derivative = sp.diff(g_function, x_symbol)
        for root in roots:
            if not sp.simplify(g_function.subs(x_symbol, root) - root).is_zero:
                st.error(f"g(x) ≠ x at x = {root} where f(x) = 0.")
                return False

            derivative_value = g_derivative.subs(x_symbol, root)
            if abs(derivative_value) >= 1:
                st.warning(f"|g'(x)| ≥ 1 at x = {root}. Convergence not guaranteed.")

        return True
    except:
        st.error("Validation failed. Invalid input functions.")
        return False


def show_fixed_point():
    explain_method()

    st.header("Fixed-Point Iteration Method")
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            x = st.text_input(
                "Enter a Variable Name",
                value="x",
                help="Enter a variable name to use in the function. Default is 'x'.",
            )
        with col2:
            # Input for original function f(x)
            f_input = st.text_input(
                "Original Function f(x): ",
                value="x**2 - 4",
                help="Enter the function f(x) whose root you want to find.",
            )
        with col3:
            # Input for transformed function g(x)
            g_input = st.text_input(
                "Transformation g(x): ",
                value="2/x",
                help="Enter g(x) such that g(x) = x at the root of f(x).",
            )

        # Initial guess input
        x0 = st.number_input(
            "Initial guess (x₀)",
            format="%.4f",
            value=2.0,
            step=0.0001,
            help="Provide the initial guess for the root.",
        )

        # Tolerance and iteration settings
        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

        # Parse functions and variable
        x_symbol = sp.symbols(f"{x}")

        f_function = sp.sympify(f_input)
        g_function = sp.sympify(g_input)
    except Exception as e:
        st.error(f"Invalid function input: Please check your inputs")
        return

    # Validate the functions
    if not validate_fixed_point_function(x_symbol, f_function, g_function):
        return

    # Display the functions in LaTeX
    st.subheader("Functions")
    st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
    st.latex(f"g({x_symbol}) = {sp.latex(g_function)}")

    # Check convergence condition
    derivative = sp.diff(g_function, x_symbol)

    st.subheader("Derivative of g(x):")
    st.latex(derivative)

    # Lambdify the functions for numerical evaluations
    g = sp.lambdify(x_symbol, g_function, "numpy")
    f = sp.lambdify(x_symbol, f_function, "numpy")

    # Fixed-Point Iteration Algorithm
    st.subheader("Results")
    table_data = {"Iteration": [], "xₙ": [], "f(xₙ)": [], "Error": []}
    x_prev = x0
    converged = False

    try:
        for i in range(1, niter + 1):
            x_next = g(x_prev)
            f_value = f(x_next)
            error = abs(x_next - x_prev)

            # Append iteration data
            table_data["Iteration"].append(i)
            table_data["xₙ"].append(x_next)
            table_data["f(xₙ)"].append(f_value)
            table_data["Error"].append(error)

            # Check for divergence
            if np.isinf(x_next) or np.isnan(x_next) or abs(x_next) > 1e6:
                st.error(
                    "Method diverged. Try a different initial guess or transformation function g(x)."
                )
                break

            # Check for convergence
            if error < tol:
                converged = True
                break

            x_prev = x_next

            print(converged)

        if converged:
            # Display results table
            result_df = pd.DataFrame(table_data)
            decimals = st.slider(
                "Select number of decimals to display on table",
                min_value=1,
                max_value=10,
                value=4,
                help="Adjust the number of decimal places for the result table.",
            )
            result_display = result_df.style.format(f"{{:.{decimals}f}}")
            st.dataframe(result_display, use_container_width=True)

            st.success(
                f"Root found at x = {x_next:.{decimals}f}, f(x) = {f_value:.{decimals}f}"
            )

    except Exception as e:
        st.error(f"Error: Please check your inputs {e}")

    graph(x, f_input)


def explain_method():
    st.markdown(
        "The **Fixed Point Iteration Method** finds roots by transforming $f(x) = 0$ to $x = g(x)$."
    )

    with st.expander("📘 How the Fixed Point Method Works"):
        st.markdown(
            """
            **1. Rewrite the Function:**
            - Express $f(x) = 0$ as $x = g(x)$, where $g(x)$ is chosen to simplify computations and ensure convergence.

            **2. Choose an Initial Guess $x_0$:**
            - Select an initial guess $x_0$ close to the suspected root.

            **3. Apply the Iteration Formula:**

            $$x_{n+1} = g(x_n)$$

            - Compute successive approximations $x_1, x_2, \dots$ by evaluating $g(x)$ at the previous point.

            **4. Check for Convergence:**
            - Stop the iteration when $|x_{n+1} - x_n|$ is less than a specified tolerance.

            **Convergence Conditions:**
            - The method converges if $|g'(x)| < 1$ for all $x$ in the interval of interest.
        """
        )
