from loaders.cargador_wikipedia import CargadorWikipedia
from utilidades.reporte_basico import ReporteBasicoWikipedia


def mostrar_camino(grafo, camino):
    if not camino:
        print("No se encontró un camino entre esos artículos.")
        return
    nombres = [grafo.obtener_nombre(id_art) for id_art in camino]
    print(f"Camino encontrado ({len(camino)} pasos):")
    print(" -> ".join(nombres))

def mostrar_articulos_disponibles(grafo):
    print("\nAlgunos artículos disponibles en el grafo:")
    print("-" * 45)
    for i, articulo in enumerate(grafo.articulos.values()):
        if i >= 10:
            break
        print(f"[ID {articulo.id_articulo}] {articulo.nombre}")
    print()

def menu_busqueda(grafo):
    print("\n=== Buscador de conexiones entre artículos ===")
    print("Ingresa los IDs de dos artículos para encontrar su camino.")
    print("Escribe 'ver' para ver artículos disponibles.")
    print("Escribe 'salir' para volver al menú principal.\n")

    while True:
        entrada_origen = input("ID artículo origen: ").strip()

        if entrada_origen.lower() == "salir":
            break
        if entrada_origen.lower() == "ver":
            mostrar_articulos_disponibles(grafo)
            continue

        entrada_destino = input("ID artículo destino: ").strip()
        if entrada_destino.lower() == "salir":
            break
        

        try:
            id_origen = int(entrada_origen)
            id_destino = int(entrada_destino)
        except ValueError:
            print("Por favor ingresa números enteros válidos.\n")
            continue

        if grafo.obtener_articulo(id_origen) is None:
            print(f"El ID {id_origen} no existe en el grafo.\n")
            continue

        if grafo.obtener_articulo(id_destino) is None:
            print(f"El ID {id_destino} no existe en el grafo.\n")
            continue

        print("\n-- BFS (camino más corto) --")
        camino_bfs = grafo.encontrar_camino_simple(id_origen, id_destino)
        mostrar_camino(grafo, camino_bfs)

        print("\n-- DFS (camino por profundidad) --")
        camino_dfs = grafo.encontrar_camino_dfs(id_origen, id_destino)
        mostrar_camino(grafo, camino_dfs)

        print()


def menu_pagerank(grafo, carpeta_resultados):
    print("\n=== PageRank ===")
    print("Calculando PageRank (puede tardar unos segundos)...")

    puntajes = grafo.pagerank()

    ranking = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)

    print("\nTop 10 artículos por PageRank:")
    print("-" * 40)
    for posicion, (id_art, puntaje) in enumerate(ranking[:10], start=1):
        nombre = grafo.obtener_nombre(id_art)
        print(f"{posicion}. {nombre} -> {puntaje:.6f}")

    # Exportar ranking completo a archivo
    ruta_archivo = carpeta_resultados / "reporte_pagerank.txt"
    lineas = ["Ranking PageRank de artículos Wikipedia", ""]
    for posicion, (id_art, puntaje) in enumerate(ranking, start=1):
        nombre = grafo.obtener_nombre(id_art)
        lineas.append(f"{posicion}. {nombre} -> {puntaje:.6f}")

    ruta_archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"\nRanking completo exportado a: {ruta_archivo}")


def menu_principal(grafo, carpeta_resultados):
    while True:
        print("\n=== Menú principal ===")
        print("1. Buscar camino entre artículos (BFS / DFS)")
        print("2. Calcular y ver PageRank")
        print("3. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            menu_busqueda(grafo)
        elif opcion == "2":
            menu_pagerank(grafo, carpeta_resultados)
        elif opcion == "3":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


def main():
    cargador = CargadorWikipedia()
    grafo = cargador.cargar_grafo()

    reporte = ReporteBasicoWikipedia()
    archivos_reporte = reporte.generar(grafo)
    reporte.imprimir_en_consola(grafo)

    print()
    print("Archivos generados:")
    print(archivos_reporte["texto"])

    menu_principal(grafo, reporte.carpeta_resultados)


if __name__ == "__main__":
    main()