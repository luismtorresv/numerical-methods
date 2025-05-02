import pandas as pd
import math


def secant_method(x0, x1, tol, max_iter, Fun):
    datos = []
    for i in range(max_iter):
        x = x0
        fx0 = eval(Fun)
        x = x1
        fx1 = eval(Fun)
        den = abs(fx1 - fx0)
        if den < 1e-10:  # Evitar división por cero
            break

        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x2 - x1)

        datos.append([i + 1, x1, fx1, error])

        if error < tol:
            break

        x0, x1 = x1, x2

    # Crear tabla con pandas
    tabla = pd.DataFrame(datos, columns=["Iteración", "xi", "f(xi)", "Error"])
    print(tabla.to_string(index=False))

    if fx1 == 0:
        s = x1
        texto = f"{s} es raiz de f(x)"
        return tabla, s, texto
    elif den == 0:
        texto = "Hay una posible raiz multiple"
        return tabla, s, texto
    elif error < tol:
        s = x
        texto = f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {tol}, hayada en la iteracion {i}"
        return tabla, s, texto
    else:
        s = x
        print("Fracaso en ", max_iter, " iteraciones ")
