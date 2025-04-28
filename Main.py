import streamlit as st
import re


class Numerical_Methods:
    def __init__(self, iteraciones, function, tolerance, intervalo):
        self.N_iteraciones = iteraciones
        self.function = function

        # Tuple made up of: (amount of tolerance, type of tolerance). ej: (10,DC) where DC = Decimales Correctos
        self.tolerance, self.type_of_tolerance = tolerance
        self.intervalo = intervalo
    
    def check_function(function):
        pattern = r'^[\d+-/*()]+$'
    
        if re.match(pattern, function) and eval(function):
            return True
        
        return False
    
    def display_results(table, x, tolerancia):
        st.markdown(f"### {x} es una aproximación de una raíz con tolerancia {tolerancia}")
        st.table(table.style.format("{:7,.16f}"))

def main():
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
        tile.page_link(f"pages/{counter+1}_{Raices[counter]}.py", label=Raices[counter])
        counter += 1

    st.markdown("### Capitulo 2:")


if __name__ == "__main__":
    st.set_page_config(
    page_title="Main",
    page_icon="👋",
    )

    st.sidebar.success("Selecciona el metodo que desees.")
    st.markdown("## PROYECTO ANALISIS NUMERICO 2025-1")

    main()
