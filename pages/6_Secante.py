import streamlit as st
import sympy as sp
from Main import Numerical_Methods
from Methods.Secant import secant


class Secante(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, intervalo):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0, self.X1 = None  # No se si se diferencian del intervalo.

    def SC(self):
        X0, X1 = self.X0, self.X1
        tol = self.tolerance
        max_iter = self.N_iteraciones
        Fun = self.function
        secant(X0, X1, tol, max_iter, Fun)


def Main():
    st.set_page_config(page_title="Secante")
    st.markdown("# Secante")
    st.markdown(
        " ### NOTA: La funcion ingresada debe de ser una funcion valida y continua. Solo ingresar el numero deseado de D.C/C.S en la tolerancia."
    )

    with st.form("PF"):
        N_iter = st.slider("Numero de Iteraciones:", 0, 100)
        tolerancia = st.slider("Tolerancia: ", 0, 100)
        f_function = st.text_input("Funcion:")
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

        button = st.form_submit_button("Ejecutar Metodo")
    if button:

        # Check if the entered values are valid
        try:
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
            x_symbol = sp.symbols(f"x")

            # Evaluate leaves the function intact
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        pf = Secante(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            intervalo,
            x_0,
        )
        table, x = pf.punto_fijo()  # We can finally call the numerical method.
        if table is None:
            st.write("Fracaso")
            return
        else:
            pf.display_results(table, x, pf.tolerance)


if __name__ == "__main__":
    Main()
