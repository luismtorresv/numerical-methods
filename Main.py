import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import sympy as sp


class Numerical_Methods:
    def __init__(self, iterations, function, tolerance, interval):
        # The values shared between all the functions: Niter, Tol, Func, Interval
        self.N_iterations = iterations
        self.function = self.check_function(function)

        # Tuple made up of: (amount of tolerance, type of tolerance). ej: (10,DC) where DC = Decimales Correctos
        self.tolerance, self.type_of_tolerance = tolerance
        self.interval = interval

    def check_function(self, function):
        # Safely parse and convert strings into callable functions.
        # This sympy operation was taken from a GPT suggestion:

        x_sym = sp.symbols("x")
        try:
            f_expr = sp.sympify(function.replace("^", "**"))
        except (sp.SympifyError, SyntaxError) as e:
            raise ValueError(f"Invalid expression: {e}")

        f = sp.lambdify(x_sym, f_expr, modules=["numpy"])
        return f

    def display_results(self, table, x, tolerance):
        st.markdown(f"### {x} is an approximation of a root with tolerance {tolerance}")
        st.table(table.style.format("{:7,.16f}"))


class Web_page:
    def Main(self):
        Raices = [
            "Punto_Fijo",
            "Raices_Multiples",
            "Newton",
            "Bisección",
            "Busquedas_Incrementales",
            "Secante",
            "Regla_Falsa",
        ]
        solution_linear_system = [""]
        st.markdown("### Section 1:")
        row1 = st.columns(3)
        row2 = st.columns(4)

        counter = 0
        for col in row1 + row2:
            tile = col.container(height=300)
            tile.title("🔥")
            tile.page_link(
                f"pages/{counter+1}_{Raices[counter]}.py", label=Raices[counter]
            )
            counter += 1

        st.markdown("### Section 2:")

    @staticmethod
    def form_questions(method_input):
        N_iter = st.slider("Maximum number of iterations:", 0, 100)
        tolerance = st.slider("Tolerance: ", 0, 100)
        f_function = st.text_input("Function:")

        # Varies from method to method
        variable_input = st.text_input(f"{method_input}: ")

        x_0 = st.text_input("Initial value x0:")

        type_of_tolerance = st.selectbox(
            "Significant figures or correct decimals?:",
            ["C.S", "D.C"],
        )

        st.write("Interval:")
        interval = (
            st.text_input("Lower limit (a):"),
            st.text_input("Upper limit (b):"),
        )

        return (
            N_iter,
            tolerance,
            f_function,
            x_0,
            type_of_tolerance,
            interval,
            variable_input,
        )

    @staticmethod
    def check_values(interval, tolerance, type_of_tolerance, x_0):
        a, b = interval
        interval = (
            float(a),
            float(b),
        )

        tolerance = (
            float(f"5e-{tolerance}")
            if type_of_tolerance == "C.S"
            else float(f"0.5e-{tolerance}")
        )

        x_0 = float(x_0)

        return interval, tolerance, x_0

    @staticmethod
    def intro(method_type):
        st.set_page_config(page_title=f"{method_type}")
        st.markdown(f"# {method_type}")
        st.markdown(
            " ### NOTE: The input function must be continuous."
            "Please only input the number of D.C/C.S in the tolerance field."
        )

    @staticmethod
    def create_graph(function, interval):
        # Define symbol
        f_np = function
        # Create x and y values. fill the inbetween with 1000 dots.
        x_vals = np.linspace(interval[0], interval[1], 1000)
        try:
            y_vals = f_np(x_vals)
        except Exception as e:
            raise RuntimeError(f"Error evaluating function: {e}")

        Web_page.create_graph(x_vals, y_vals, function=function)
        # Plot (Streamlit-compatible)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, label=f"f(x) = {function}")
        ax.axhline(0, color="gray", linestyle="--")
        ax.axvline(0, color="gray", linestyle="--")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Graph of f(x)")
        ax.legend()
        ax.grid(True)

        # Render in Streamlit
        st.pyplot(fig)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Main",
        page_icon="👋",
    )

    st.sidebar.success("Choose a numerical method.")
    st.markdown("## Numerical Analysis project - 2025-1")
    p = Web_page()
    p.Main()
