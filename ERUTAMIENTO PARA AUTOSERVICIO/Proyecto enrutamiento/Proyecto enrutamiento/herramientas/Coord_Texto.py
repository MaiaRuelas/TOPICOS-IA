import os
import csv
import re
import sys

DATOS = r"""
Centro de Distribución	Centro de Distribución 1	24.774908	-107.309857
Centro de Distribución	Centro de Distribución 2	24.846399	-107.380268
Centro de Distribución	Centro de Distribución 3	24.731204	-107.468801
Centro de Distribución	Centro de Distribución 4	24.711617	-107.326765
Centro de Distribución	Centro de Distribución 5	24.820223	-107.358385
Centro de Distribución	Centro de Distribución 6	24.704117	-107.306018
Centro de Distribución	Centro de Distribución 7	24.866489	-107.457532
Centro de Distribución	Centro de Distribución 8	24.736365	-107.463319
Centro de Distribución	Centro de Distribución 9	24.760848	-107.395049
Centro de Distribución	Centro de Distribución 10	24.786389	-107.441754
Tienda	Tienda 1	24.822371	-107.472101
Tienda	Tienda 2	24.758429	-107.426728
Tienda	Tienda 3	24.791214	-107.342965
Tienda	Tienda 4	24.739935	-107.397153
Tienda	Tienda 5	24.818483	-107.490710
Tienda	Tienda 6	24.821509	-107.465895
Tienda	Tienda 7	24.713010	-107.310223
Tienda	Tienda 8	24.893126	-107.338321
Tienda	Tienda 9	24.760923	-107.480466
Tienda	Tienda 10	24.836847	-107.411970
Tienda	Tienda 11	24.724408	-107.400965
Tienda	Tienda 12	24.706878	-107.318136
Tienda	Tienda 13	24.751756	-107.367496
Tienda	Tienda 14	24.762342	-107.395986
Tienda	Tienda 15	24.809342	-107.463029
Tienda	Tienda 16	24.893917	-107.344973
Tienda	Tienda 17	24.887900	-107.321035
Tienda	Tienda 18	24.819580	-107.315625
Tienda	Tienda 19	24.717699	-107.460803
Tienda	Tienda 20	24.709045	-107.434934
Tienda	Tienda 21	24.777735	-107.445730
Tienda	Tienda 22	24.865748	-107.428649
Tienda	Tienda 23	24.756187	-107.391461
Tienda	Tienda 24	24.728185	-107.339561
Tienda	Tienda 25	24.714910	-107.302623
Tienda	Tienda 26	24.854449	-107.460257
Tienda	Tienda 27	24.701104	-107.336908
Tienda	Tienda 28	24.841371	-107.354199
Tienda	Tienda 29	24.854254	-107.485191
Tienda	Tienda 30	24.771693	-107.476826
Tienda	Tienda 31	24.872621	-107.375340
Tienda	Tienda 32	24.766180	-107.487288
Tienda	Tienda 33	24.762196	-107.434963
Tienda	Tienda 34	24.845921	-107.372489
Tienda	Tienda 35	24.877443	-107.405557
Tienda	Tienda 36	24.723919	-107.357351
Tienda	Tienda 37	24.852157	-107.387745
Tienda	Tienda 38	24.854193	-107.401241
Tienda	Tienda 39	24.804547	-107.414492
Tienda	Tienda 40	24.705084	-107.478422
Tienda	Tienda 41	24.706286	-107.372718
Tienda	Tienda 42	24.762871	-107.398286
Tienda	Tienda 43	24.881513	-107.450142
Tienda	Tienda 44	24.782077	-107.348890
Tienda	Tienda 45	24.745760	-107.484604
Tienda	Tienda 46	24.757950	-107.467756
Tienda	Tienda 47	24.885940	-107.338376
Tienda	Tienda 48	24.826681	-107.325708
Tienda	Tienda 49	24.860734	-107.462686
Tienda	Tienda 50	24.878512	-107.392132
Tienda	Tienda 51	24.861488	-107.320782
Tienda	Tienda 52	24.763601	-107.477990
Tienda	Tienda 53	24.745587	-107.414578
Tienda	Tienda 54	24.863603	-107.327854
Tienda	Tienda 55	24.701390	-107.397851
Tienda	Tienda 56	24.783482	-107.455578
Tienda	Tienda 57	24.723973	-107.432477
Tienda	Tienda 58	24.888582	-107.435359
Tienda	Tienda 59	24.803758	-107.359396
Tienda	Tienda 60	24.772726	-107.305644
Tienda	Tienda 61	24.892489	-107.449644
Tienda	Tienda 62	24.799450	-107.439824
Tienda	Tienda 63	24.756968	-107.492623
Tienda	Tienda 64	24.821913	-107.399464
Tienda	Tienda 65	24.710296	-107.444271
Tienda	Tienda 66	24.881653	-107.452088
Tienda	Tienda 67	24.728979	-107.402109
Tienda	Tienda 68	24.897130	-107.451589
Tienda	Tienda 69	24.834427	-107.347676
Tienda	Tienda 70	24.747528	-107.354357
Tienda	Tienda 71	24.773557	-107.373539
Tienda	Tienda 72	24.826706	-107.392845
Tienda	Tienda 73	24.718058	-107.332940
Tienda	Tienda 74	24.764156	-107.462696
Tienda	Tienda 75	24.708155	-107.381821
Tienda	Tienda 76	24.835513	-107.496682
Tienda	Tienda 77	24.802419	-107.454701
Tienda	Tienda 78	24.829035	-107.465127
Tienda	Tienda 79	24.838188	-107.422653
Tienda	Tienda 80	24.887346	-107.472496
Tienda	Tienda 81	24.768213	-107.477305
Tienda	Tienda 82	24.884939	-107.324532
Tienda	Tienda 83	24.751588	-107.368003
Tienda	Tienda 84	24.863444	-107.388960
Tienda	Tienda 85	24.805930	-107.451630
Tienda	Tienda 86	24.718621	-107.320557
Tienda	Tienda 87	24.880084	-107.373380
Tienda	Tienda 88	24.767806	-107.430158
Tienda	Tienda 89	24.845191	-107.320578
Tienda	Tienda 90	24.877417	-107.344025
"""

def a_float(numero_str):
    # Para cambiar comas por puntos y quitar cosas raras 
    s = numero_str.strip().replace(",", ".")
    s = re.sub(r"[^0-9\.\-]", "", s)
    return float(s)

def separar_lineas(texto):
    lineas = [ln for ln in texto.strip().splitlines() if ln.strip()]
    centros = []
    tiendas = []
    for ln in lineas:
        # Primero intento separar por tabulador, si no, por espacios múltiples
        partes = re.split(r"\t+", ln.strip())
        if len(partes) < 4:
            partes = re.split(r"\s{2,}", ln.strip())
        if len(partes) < 4:
            # línea incompleta, la salto
            continue
        tipo = partes[0].strip()
        nombre = partes[1].strip()
        lat = a_float(partes[2])
        lon = a_float(partes[3])
        item = {"tipo": tipo, "nombre": nombre, "lat": lat, "lon": lon}
        if tipo.lower().startswith("centro"):
            centros.append(item)
        else:
            tiendas.append(item)
    return centros, tiendas

def main():
    os.makedirs("data", exist_ok=True)

    centros, tiendas = separar_lineas(DATOS)

    if not centros:
        print("No encontré centros de distribución. Revisa tu bloque de texto.", file=sys.stderr)
        sys.exit(1)

    # Tomamos "Centro de Distribución 1" como depot si existe, si no el primero
    depot = next((c for c in centros if c["nombre"].endswith("1")), centros[0])

    filas = []
    # id=0 será siempre el depot
    filas.append({"id": 0, "nombre": depot["nombre"], "lat": depot["lat"], "lon": depot["lon"]})

    # Tiendas id 1..N
    for i, t in enumerate(tiendas, start=1):
        filas.append({"id": i, "nombre": t["nombre"], "lat": t["lat"], "lon": t["lon"]})

    # Guardar CSV
    ruta_csv = "data/coords.csv"
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "nombre", "lat", "lon"])
        w.writeheader()
        w.writerows(filas)

    print(f"[OK] Guardado {ruta_csv} con {len(filas)} puntos (0 = depot).")

if __name__ == "__main__":
    main()
