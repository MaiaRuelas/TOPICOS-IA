from src.Recocido import recocido
from src.Utilidades import leer_coords_csv, COSTO_POR_KM
import folium


def main():
    # Carga los puntos (depot + tiendas)
    puntos = leer_coords_csv("data/coords.csv")

    # Ejecuta recocido
    mejor_ruta, mejor_costo, iters = recocido(
        puntos,
        T_inicial=100.0,
        T_min=0.01,
        alfa=0.995,
        max_iter=10000,     
        imprimir_cada=1000  # imprime progreso cada N iteraciones
    )

    km_totales = mejor_costo / COSTO_POR_KM

    # Crear lista detallada con los puntos de la mejor ruta
    ruta_detallada = [
        {"id": i, "lat": puntos[i]["lat"], "lon": puntos[i]["lon"]}
        for i in mejor_ruta
    ]

  
    # Crea mapa con Folium
    # Centra el mapa en el primer punto
    lat_centro = ruta_detallada[0]["lat"]
    lon_centro = ruta_detallada[0]["lon"]

    mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=12)

    # Añade marcadores y líneas
    coordenadas = []
    for punto in ruta_detallada:
        lat, lon, id_ = punto["lat"], punto["lon"], punto["id"]
        coordenadas.append((lat, lon))
        folium.Marker(
            location=(lat, lon),
            popup=f"ID: {id_}",
            tooltip=f"Punto {id_}",
            icon=folium.Icon(color="blue" if id_ != ruta_detallada[0]["id"] else "red")
        ).add_to(mapa)

    # Dibuja la ruta (línea entre puntos)
    folium.PolyLine(
        coordenadas,
        color="blue",
        weight=3,
        opacity=0.8
    ).add_to(mapa)

    # Guarda el mapa como archivo HTML
    mapa.save("ruta.html")
    print("\nMapa generado: ruta.html")

 
    print("\n========== RESULTADO ==========")
    print("Mejor ruta (orden de IDs):", mejor_ruta)
    print(f"Km totales aprox: {km_totales:.2f} km")
    print(f"Costo total aprox: ${mejor_costo:.2f}")
    print(f"Iteraciones usadas: {iters}")

  #  print("\nRuta detallada (orden de visita):")
   # for punto in ruta_detallada:
    #    print(punto) 


if __name__ == "__main__":
    main()
