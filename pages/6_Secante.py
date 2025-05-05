import streamlit as st
import sympy as sp

from Main import Numerical_Methods, Web_page
from Methods.Secant_method import secant_method


class Secante_page(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, intervalo, X0, X1):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0, self.X1 = X0, X1

    def call_method(self):
        X0, X1 = self.X0, self.X1
        tol = self.tolerance
        max_iter = self.N_iteraciones
        Fun = self.function
        secant_method(X0, X1, tol, max_iter, Fun)


def Main():
    Web_page.intro("Secant")

    with st.form("PF"):
        (
            N_iter,
            tolerancia,
            f_function,
            x_0,
            tipo_tolerancia,
            intervalo,
            x_1,
        ) = Web_page.form_questions("X1")

        button = st.form_submit_button("Ejecutar Metodo")
    if button:
        # Check if the entered values are valid
        try:
            # Check parent values
            intervalo, tolerancia, x_0 = Web_page.check_values(
                intervalo, tolerancia, tipo_tolerancia, x_0
            )
            x_1 = float(x_1)

            # Evaluate leaves the function intact
            x_symbol = sp.symbols(f"x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")

        Secant = Secante_page(
            N_iter, f_function, (tolerancia, tipo_tolerancia), intervalo, x_0, x_1
        )
        table, x = Secant.call_method()  # We can finally call the numerical method.
        if table is None:
            st.write("Fracaso")
            return
        else:
            Secant.display_results(table, x, Secant.tolerance)
            Web_page.create_graph(Secant.function, Secant.intervalo)


if __name__ == "__main__":
    Main()
