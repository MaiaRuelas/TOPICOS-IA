import csv
import math

# Costo promedio por kilómetro (Culiacán, Sinaloa - 2025)
# Calculado con base en:
# - Precio del diésel ≈ $23.0 MXN/L
# - Rendimiento promedio camión mediano ≈ 4.5 km/L
# - Incluye 60% adicional por mantenimiento, operador y peajes
# Resultado: ~ $8.2 MXN/km

COSTO_POR_KM = 8.2

def leer_coords_csv(ruta_csv):
    puntos = []
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for row in lector:
            puntos.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"])
            })
    # Aseguro que estén ordenados por id 
    puntos.sort(key=lambda x: x["id"])
    return puntos

def haversine_km(lat1, lon1, lat2, lon2):
    # fórmula Haversine
    # distancia aproximada sobre la Tierra (radio ~6371 km)
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def distancia_idx(puntos, i, j):
    a = puntos[i]
    b = puntos[j]
    return haversine_km(a["lat"], a["lon"], b["lat"], b["lon"])

def costo_ruta(puntos, ruta):
    # ruta es una lista de ids 
    km_totales = 0.0
    for k in range(len(ruta) - 1):
        km_totales += distancia_idx(puntos, ruta[k], ruta[k+1])
    return km_totales * COSTO_POR_KM
