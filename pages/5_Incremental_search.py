import streamlit as st
import sympy as sp

from Main import Numerical_Methods, Web_page
from Methods.Incremental_Search_method import incremental_search_method


class Incremental_Search_page(Numerical_Methods):
    def __init__(self, iterations, function, tolerance, interval, X0, deltaX):
        super().__init__(iterations, function, tolerance, interval)
        self.X0 = X0
        self.deltaX = deltaX

    def call_method(self):
        Xi = self.X0
        DeltaX = self.deltaX
        Niter = self.N_iterations
        Fun = self.function
        return incremental_search_method(Xi, DeltaX, Niter, Fun)


def Main():
    Web_page.intro("Incremental Search")

    with st.form("BI"):
        # Input data. The data unique to the method is passed as an arg to the method
        (
            N_iter,
            tolerance,
            f_function,
            x_0,
            type_of_tolerance,
            interval,
            Delta_X,
        ) = Web_page.form_questions("Delta X (step)")

        button = st.form_submit_button("Run method")
    if button:
        # Check if the entered values are valid
        try:
            # Check parent values
            interval, tolerance, x_0 = Web_page.check_values(
                interval, tolerance, type_of_tolerance, x_0
            )

            Delta_X = float(Delta_X)

            # Evaluate leaves the function intact
            x_symbol = sp.symbols(f"x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"

        except:
            st.write("Input error. Check your inputs.")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        IS = Incremental_Search_page(
            N_iter,
            f_function,
            (tolerance, type_of_tolerance),
            interval,
            x_0,
            Delta_X,
        )
        table, x, text = IS.call_method()
        if table is None:
            st.write(text)
            return
        else:
            st.write(text)
            IS.display_results(table, x, IS.tolerance)
            Web_page.create_graph(IS.function, IS.interval)


if __name__ == "__main__":
    Main()
