import math
import random
from src.Utilidades import costo_ruta

# Para que siempre salgan los mismos aleatorios 
random.seed(42)

def hacer_ruta_inicial(n):
    # n = cantidad de puntos (0 = depot, 1-N = tiendas)
    # Empiezo con ruta simple: 0 -> 1 -> 2 -> ... -> N -> 0
    clientes = list(range(1, n))
    return [0] + clientes + [0]

def movimiento_swap(ruta):
    # Intercambia dos clientes
    r = ruta[1:-1]
    if len(r) < 2:
        return ruta[:]
    i, j = random.sample(range(len(r)), 2)
    r[i], r[j] = r[j], r[i]
    return [0] + r + [0]

def movimiento_2opt(ruta):
    # Inverte un segmento interno de la ruta
    r = ruta[1:-1]
    if len(r) < 2:
        return ruta[:]
    i, j = sorted(random.sample(range(len(r)), 2))
    r[i:j+1] = reversed(r[i:j+1])
    return [0] + r + [0]

def vecino_aleatorio(ruta):
    # Eleccion al azar: 50% swap y 50% 2-opt
    if random.random() < 0.5:
        return movimiento_swap(ruta)
    else:
        return movimiento_2opt(ruta)

def recocido(puntos, T_inicial=100.0, T_min=0.01, alfa=0.995, max_iter=20000, imprimir_cada=1000):
    n = len(puntos)
    ruta_actual = hacer_ruta_inicial(n)
    costo_actual = costo_ruta(puntos, ruta_actual)

    mejor_ruta = ruta_actual[:]
    mejor_costo = costo_actual

    T = T_inicial
    iteracion = 0

    print(f"Inicio | T={T:.2f} | costo=${costo_actual:.2f} | ruta={ruta_actual}")

    while T > T_min and iteracion < max_iter:
        iteracion += 1

        # genera un vecino
        vecino = vecino_aleatorio(ruta_actual)
        costo_vecino = costo_ruta(puntos, vecino)

        # calculamos delta
        delta = costo_vecino - costo_actual

        # criterio de aceptación
        if delta <= 0:
            # mejora: aceptamos siempre
            ruta_actual, costo_actual = vecino, costo_vecino
        else:
            # empeora: aceptamos a veces con probabilidad exp(-delta/T)
            if random.random() < math.exp(-delta / T):
                ruta_actual, costo_actual = vecino, costo_vecino

        # mejor global
        if costo_actual < mejor_costo:
            mejor_ruta, mejor_costo = ruta_actual[:], costo_actual

        # enfriamniento
        T *= alfa

        # imprimimos cada cierto número de iteraciones
        if iteracion == 1 or iteracion % imprimir_cada == 0:
            print(f"Iter {iteracion:6d} | T={T:7.3f} | costo=${costo_actual:10.2f} | mejor=${mejor_costo:10.2f}")

    return mejor_ruta, mejor_costo, iteracion
