import math

import pandas as pd


def incremental_search_method(Xi, DeltaX, Niter, Fun):
    # Inicialización de listas para la tabla
    iteraciones = []
    xn_vals = []
    fn_vals = []

    # Evaluar función en el punto inicial
    x = Xi
    f = eval(Fun)
    c = 0  # Contador de iteraciones

    # Guardar primera iteración
    iteraciones.append(c)
    xn_vals.append(x)
    fn_vals.append(f)

    # Algoritmo de búsquedas incrementales
    while c < Niter:
        x_new = x + DeltaX  # Incrementamos x
        f_new = eval(Fun)  # Evaluamos f(x_new)

        if f * f_new < 0:  # Cambio de signo => hay raíz en el intervalo [x, x_new]
            # print(f"Se detectó un cambio de signo entre {x} y {x_new}")
            break

        # Guardar valores en listas
        c += 1
        iteraciones.append(c)
        xn_vals.append(x_new)
        fn_vals.append(f_new)

        # Actualizar valores
        x = x_new
        f = f_new

    # Mostrar resultados finales
    # Crear y mostrar la tabla de iteraciones
    tabla = pd.DataFrame(
        {
            "Iteración": iteraciones,
            "Xn": xn_vals,
            "f(Xn)": fn_vals,
        }
    )

    if f_new == 0:
        s = x
        texto = "es raiz de f(x)"
        return tabla, s, texto
    elif f * f_new < 0:
        s = x
        texto = f"Existe una raiz de f(x) entre {x} y {x_new}"
        return tabla, s, texto
    else:
        s = x
        texto = f"Fracaso en {Niter} iteraciones "
        return None, s, texto
