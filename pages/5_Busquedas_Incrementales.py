import streamlit as st
import sympy as sp
from Main import Numerical_Methods, Web_page
from Methods.Incremental_Search_method import incremental_search_method


class Incremental_Search_page(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, intervalo, X0, deltaX):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0 = X0
        self.deltaX = deltaX

    def call_method(self):
        Xi = self.X0
        DeltaX = self.deltaX
        Niter = self.N_iteraciones
        Fun = self.function
        return incremental_search_method(Xi, DeltaX, Niter, Fun)


def Main():
    Web_page.intro("Incremental Search")

    with st.form("BI"):
        # Input data. The data unique to the method is passed as an arg to the method
        N_iter, tolerancia, f_function, x_0, tipo_tolerancia, intervalo, Delta_X = (
            Web_page.form_questions("Delta X/Crecimiento")
        )

        button = st.form_submit_button("Ejecutar Metodo")
    if button:
        # Check if the entered values are valid
        try:
            # Check parent values
            intervalo, tolerancia, x_0 = Web_page.check_values(
                intervalo, tolerancia, tipo_tolerancia, x_0
            )

            Delta_X = float(Delta_X)

            # Evaluate leaves the function intact
            x_symbol = sp.symbols(f"x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"

        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        IS = Incremental_Search_page(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            intervalo,
            x_0,
            Delta_X,
        )
        table, x, texto = IS.call_method()
        if table is None:
            st.write(texto)
            return
        else:
            st.write(texto)
            IS.display_results(table, x, IS.tolerance)
            Web_page.create_graph(IS.function, IS.intervalo)


if __name__ == "__main__":
    Main()
