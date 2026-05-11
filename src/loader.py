from src.articulo import Articulo
from src.grafo import Grafo


def cargar_nombres(path: str) -> dict[int, str]:
    """Retorna dict {id (base 1) -> nombre}"""
    nombres = {}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, linea in enumerate(f):
            nombres[idx + 1] = linea.strip()  # base 1
    print(f"  Nombres cargados: {len(nombres)}")
    return nombres


def cargar_categorias(path_categorias: str, path_nombres_cat: str) -> dict[str, list[int]]:
    """Retorna dict {nombre_categoria -> [ids de artículos]}"""

    # Primero cargamos los nombres de categorías (índice base 1)
    nombres_cat = {}
    with open(path_nombres_cat, "r", encoding="utf-8", errors="ignore") as f:
        for idx, linea in enumerate(f):
            nombres_cat[idx + 1] = linea.strip()

    # Luego leemos la matriz categoría -> artículos
    categorias = {}
    with open(path_categorias, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if linea.startswith("%"):
                continue
            partes = linea.strip().split()
            if len(partes) != 2:
                continue
            id_articulo, id_categoria = int(partes[0]), int(partes[1])
            nombre_cat = nombres_cat.get(id_categoria, f"cat_{id_categoria}")
            if nombre_cat not in categorias:
                categorias[nombre_cat] = []
            categorias[nombre_cat].append(id_articulo)

    print(f"  Categorías cargadas: {len(categorias)}")
    return categorias


def cargar_grafo_filtrado(
    path_aristas: str,
    nombres: dict[int, str],
    ids_filtro: set[int],
    categoria: str
) -> Grafo:
    """Carga solo los nodos y aristas del subconjunto filtrado"""
    from src.grafo import Grafo

    grafo = Grafo()

    # Agregar nodos del filtro
    for id_nodo in ids_filtro:
        nombre = nombres.get(id_nodo, f"articulo_{id_nodo}")
        grafo.agregar_nodo(Articulo(id_nodo, nombre))

    print(f"  Nodos en subconjunto '{categoria}': {len(grafo)}")

    # Leer aristas — solo las que conectan nodos del filtro
    aristas_leidas = 0
    with open(path_aristas, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if linea.startswith("%"):
                continue
            partes = linea.strip().split()
            if len(partes) != 2:
                continue
            origen, destino = int(partes[0]), int(partes[1])
            if origen in ids_filtro and destino in ids_filtro:
                grafo.agregar_arista(origen, destino)
                aristas_leidas += 1

    print(f"  Aristas en subconjunto: {aristas_leidas}")
    return grafo