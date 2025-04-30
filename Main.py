import streamlit as st
import sympy as sp
import re


class Numerical_Methods:
    def __init__(self, iteraciones, function, tolerance, intervalo):
        # The values shared between all the functions: Niter, Tol, Func, Interval
        self.N_iteraciones = iteraciones
        self.function = function

        # Tuple made up of: (amount of tolerance, type of tolerance). ej: (10,DC) where DC = Decimales Correctos
        self.tolerance, self.type_of_tolerance = tolerance
        self.intervalo = intervalo

    def check_function(function):
        # Safely parse and convert strings into callable functions.
        # This sympy operation was taken from a GPT suggestion:

        x_sym = sp.symbols("x")
        try:
            f_expr = sp.sympify(function.replace("^", "**"))
        except (sp.SympifyError, SyntaxError) as e:
            raise ValueError(f"Invalid expression: {e}")

        f = sp.lambdify(x_sym, f_expr, modules=["math"])
        return f

    def display_results(self, table, x, tolerancia):
        st.markdown(
            f"### {x} es una aproximación de una raíz con tolerancia {tolerancia}"
        )
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
        Sol_Sist_ecuaciones = [""]
        st.markdown("### Capitulo 1:")
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

        st.markdown("### Capitulo 2:")

    @staticmethod
    def form_questions(method_input):
        N_iter = st.slider("Numero de Iteraciones:", 0, 100)
        tolerancia = st.slider("Tolerancia: ", 0, 100)
        f_function = st.text_input("Funcion:")

        # Varies from method to method
        varible_input = st.text_input(
            f"{method_input}: "
        )

        x_0 = st.text_input("Valor inicial X0:")

        tipo_tolerancia = st.selectbox(
            "Escoge un tipo de tolerancia:",
            ["C.S", "D.C"],
        )

        st.write("Intervalo:")
        intervalo = (
            st.text_input("Limite inferior (a):"),
            st.text_input("Limite superior (b):"),
        )

        return (
            N_iter,
            tolerancia,
            f_function,
            x_0,
            tipo_tolerancia,
            intervalo,
            varible_input,
        )

    @staticmethod
    def check_values(intervalo, tolerancia, tipo_tolerancia, x_0):
        a, b = intervalo
        intervalo = (
            float(a),
            float(b),
        )

        tolerancia = (
            float(f"5e-{tolerancia}")
            if tipo_tolerancia == "C.S"
            else float(f"0.5e-{tolerancia}")
        )

        x_0 = float(x_0)

        return intervalo, tolerancia, x_0

    @staticmethod
    def intro(method_type):
        st.set_page_config(page_title=f"{method_type}")
        st.markdown(f"# {method_type}")
        st.markdown(
            " ### NOTA: La funcion ingresada debe de ser una funcion valida y continua. Solo ingresar el numero deseado de D.C/C.S en la tolerancia."
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Main",
        page_icon="👋",
    )

    st.sidebar.success("Selecciona el metodo que desees.")
    st.markdown("## PROYECTO ANALISIS NUMERICO 2025-1")
    p = Web_page()
    p.Main()
