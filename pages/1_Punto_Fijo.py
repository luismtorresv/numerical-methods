import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
from Main import Numerical_Methods, Web_page
from Methods.Fixed_point import fixed_point


class Punto_fijo_page(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, intervalo, X0, g_function):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0 = X0
        self.g_funtion = g_function

    def punto_fijo(self):
        a, b = self.intervalo
        X0 = self.X0
        Tol = self.tolerance
        Niter = self.N_iteraciones
        Fun = self.function
        Fun_g = self.g_funtion
        return fixed_point(a, b, X0, Tol, self.type_of_tolerance, Niter, Fun, Fun_g)


def Main():
    Web_page.intro("Fixed Point")

    with st.form("PF"):
        # Input data. The data unique to the method is passed as an arg to the method
        N_iter, tolerancia, f_function, x_0, tipo_tolerancia, intervalo, g_function = (
            Web_page.form_questions("Funcion G")
        )
        button = st.form_submit_button("Ejecutar Metodo")
    if button:

        # Check if the entered values are valid
        try:
            # Check parent values
            intervalo, tolerancia, x_0 = Web_page.check_values(
                intervalo, tolerancia, tipo_tolerancia, x_0
            )

            # Check both functions
            x_symbol = sp.symbols("x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
            g_function = f"{sp.parse_expr(g_function,evaluate=False)}"

        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        # If there are no errores with the inputs, create the class.
        pf = Punto_fijo_page(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            intervalo,
            x_0,
            g_function,
        )

        # Display results
        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        st.latex(f"g({x_symbol}) = {sp.latex(g_function)}")

        table, x = pf.punto_fijo()  # We can finally call the numerical method.
        if table is None:
            st.write("Fracaso")
            return
        else:
            pf.display_results(table, x, pf.tolerance)


if __name__ == "__main__":
    Main()
