import random
import math
import time

# =========================
#  FUNCIÓN DE COSTO
#  Nº de inversiones (pares i<j con v[i] > v[j])
#  Un vector ordenado tiene costo = 0
# =========================
def calcular_conflictos(solucion):
    conflictos = 0
    n = len(solucion)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if solucion[i] > solucion[j]:
                conflictos += 1
    return conflictos

# =========================
#  VECINO
#  Intercambia dos posiciones (swap) al azar
# =========================
def generar_vecino(solucion):
    vecino = solucion.copy()
    n = len(vecino)
    i, j = random.sample(range(n), 2)  # índices distintos
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

# =========================
#  RECOCIDO SIMULADO PARA ORDENAR
# =========================
def recocido_simulado_ordenamiento(vector_base,
                                   max_iter=10000,
                                   temp_inicial=100.0,
                                   temp_min=0.1,
                                   alpha=0.99,
                                   mostrar_iter=True):
    # La solución actual parte como una permutación del vector_base
    solucion_actual = vector_base.copy()
    random.shuffle(solucion_actual)

    costo_actual = calcular_conflictos(solucion_actual)

    mejor_solucion = solucion_actual.copy()
    mejor_conflicto = costo_actual

    temperatura = temp_inicial
    iteraciones = 0

    inicio_tiempo = time.time()

    # Bucle principal
    while temperatura > temp_min and iteraciones < max_iter and mejor_conflicto != 0:
        iteraciones += 1

        vecino = generar_vecino(solucion_actual)
        costo_vecino = calcular_conflictos(vecino)

        delta = costo_vecino - costo_actual

        # Criterio de aceptación (Metropolis)
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            solucion_actual = vecino
            costo_actual = costo_vecino

        # Mejor global
        if costo_actual < mejor_conflicto:
            mejor_solucion = solucion_actual.copy()
            mejor_conflicto = costo_actual

        if mostrar_iter and (iteraciones % 100 == 0 or iteraciones == 1):
            print(f"Iter {iteraciones:5d} | Temp={temperatura:7.4f} | Costo={costo_actual:4d} | Mejor={mejor_conflicto:4d} | Estado={solucion_actual}")

        # Enfriamiento
        temperatura *= alpha

    fin_tiempo = time.time()
    tiempo = fin_tiempo - inicio_tiempo

    return mejor_solucion, mejor_conflicto, iteraciones, tiempo

# =========================
#  MAIN
# =========================
if __name__ == '__main__':
    vector_base = [5, 2, 8, 1, 3, 7, 4, 6, 0]

    solucion, conflictos, iteraciones, tiempo = recocido_simulado_ordenamiento(
        vector_base,
        max_iter=10000,
        temp_inicial=100.0,
        temp_min=0.1,
        alpha=0.99,
        mostrar_iter=True
    )

    print("\n========== RESULTADO ==========")
    print("Vector base:            ", vector_base)
    print("Mejor solución encontrada:", solucion)
    print("Costo (inversiones):     ", conflictos)
    print("Iteraciones:             ", iteraciones)
    print(f"Tiempo transcurrido (s):  {tiempo:.4f}")

    if conflictos == 0:
        print("El vector está ordenado ascendentemente.")
    else:
        print("No se alcanzó costo 0. Ajusta parámetros (T inicial, alpha, max_iter).")
