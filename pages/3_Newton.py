import streamlit as st
import sympy as sp
from Main import Numerical_Methods, Web_page
from Methods.Newton import Newton


class Newton_page(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance,intervalo, X0, f_derivate):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0 = X0
        self.f_derivate = f_derivate

    def call_newton(self):
        X0 = self.X0
        Tol = self.tolerance
        Niter = self.N_iteraciones
        Fun = self.function
        Fun_derivate = self.f_derivate
        return Newton(X0, Tol, self.type_of_tolerance, Niter, Fun, Fun_derivate)


def Main():
    Web_page.intro("Newton")

    with st.form("NT"):

        N_iter, tolerancia, f_function, x_0, tipo_tolerancia, intervalo, f_derivate = (
            Web_page.form_questions("Derivate of function F")
        )

        button = st.form_submit_button("Ejecutar Metodo")
    if button:

        # Check if the entered values are valid
        try:
            # Check parent values
            intervalo, tolerancia, x_0 = Web_page.check_values(
                intervalo, tolerancia, tipo_tolerancia, x_0
            )
            x_symbol = sp.symbols(f"x")

            # Check both functions
            x_symbol = sp.symbols("x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
            f_derivate = f"{sp.parse_expr(f_derivate,evaluate=False)}"

        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        st.latex(f"f'({x_symbol}) = {sp.latex(f_derivate)}")

        # Check if the functions are valid
        Nt = Newton_page(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            intervalo,
            x_0,
            f_derivate
        )
        table, x = Nt.call_newton()  # We can finally call the numerical method.
        if table is None:
            st.write("Fracaso")
            return
        else:
            Nt.display_results(table, x, Nt.tolerance)


if __name__ == "__main__":
    Main()
