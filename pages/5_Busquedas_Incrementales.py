import streamlit as st
import sympy as sp
from Main import Numerical_Methods
from Methods.BI import incremental_search


class Incremental_Search(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, intervalo, X0, deltaX):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0 = X0
        self.deltaX = deltaX

    def BI(self):
        Xi = self.X0
        DeltaX = self.deltaX
        Niter = self.N_iteraciones
        Fun = self.function
        return incremental_search(Xi, DeltaX, Niter, Fun)


def Main():
    st.set_page_config(page_title="Incremental Search")
    st.markdown("# Incremental Search")
    st.markdown(
        " ### NOTA: La funcion ingresada debe de ser una funcion valida y continua. Solo ingresar el numero deseado de D.C/C.S en la tolerancia."
    )

    with st.form("BI"):
        N_iter = st.slider("Numero de Iteraciones:", 0, 100)
        tolerancia = st.slider("Tolerancia: ", 0, 100)
        f_function = st.text_input("Funcion:")
        Delta_X = st.text_input("Delta X/Crecimiento")
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
            Delta_X = float(Delta_X)
            x_0 = float(x_0)
            x_symbol = sp.symbols(f"x")

            # Evaluate leaves the function intact
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"

        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        BI = Incremental_Search(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            intervalo,
            x_0,
            Delta_X,
        )
        table, x, texto = BI.BI()
        if table is None:
            st.write(texto)
            return
        else:
            st.write(texto)
            BI.display_results(table, x, BI.tolerance)


if __name__ == "__main__":
    Main()
