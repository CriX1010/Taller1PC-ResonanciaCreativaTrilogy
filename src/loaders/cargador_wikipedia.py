from pathlib import Path

from modelos.grafo import GrafoWikipedia


class CargadorWikipedia:
    """Carga desde el dataset los datos necesarios para construir el grafo."""

    def __init__(self, ruta_dataset=None):
        if ruta_dataset is None:
            self.ruta_dataset = Path(__file__).resolve().parent.parent.parent / "dataset"
        else:
            self.ruta_dataset = Path(ruta_dataset)

    def cargar_nombres_articulos(self):
        ruta = self.ruta_dataset / "wiki-topcats_pagenames.txt"
        nombres = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                nombres[indice] = linea.strip()

        return nombres

    def cargar_nombres_categorias(self):
        ruta = self.ruta_dataset / "wiki-topcats_Category_names.txt"
        categorias = {}

        with open(ruta, "r", encoding="utf-8") as archivo:
            for indice, linea in enumerate(archivo, start=1):
                categorias[indice] = linea.strip()

        return categorias

    def _leer_matriz_market(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue

                if len(partes) >= 2:
                    fila = int(partes[0])
                    columna = int(partes[1])
                    yield fila, columna

    def cargar_grafo(self, categoria_filtro: str = "English-language_films"):
        grafo = GrafoWikipedia()

        print("Cargando nombres de artículos...")
        nombres = self.cargar_nombres_articulos()

        print("Cargando nombres de categorías...")
        nombres_cat = self.cargar_nombres_categorias()

        print("Cargando categorías y filtrando...")
        ruta_cat = self.ruta_dataset / "wiki-topcats_Categories.mtx"
        ids_filtro = set()
        cat_por_articulo = {}  # id_articulo -> nombre_categoria

        for id_articulo, id_categoria in self._leer_matriz_market(ruta_cat):
            nombre_cat = nombres_cat.get(id_categoria, f"cat_{id_categoria}")
            if nombre_cat == categoria_filtro:
                ids_filtro.add(id_articulo)
                cat_por_articulo[id_articulo] = nombre_cat

        print(f"  Artículos en '{categoria_filtro}': {len(ids_filtro)}")

        # Agregar nodos al grafo
        for id_nodo in ids_filtro:
            nombre = nombres.get(id_nodo, f"articulo_{id_nodo}")
            grafo.agregar_articulo(id_nodo, nombre)
            grafo.articulos[id_nodo].agregar_categoria(categoria_filtro)

        # Cargar aristas solo entre nodos del filtro
        print("Cargando aristas...")
        ruta_aristas = self.ruta_dataset / "wiki-topcats.mtx"
        for id_origen, id_destino in self._leer_matriz_market(ruta_aristas):
            if id_origen in ids_filtro and id_destino in ids_filtro:
                grafo.agregar_enlace(id_origen, id_destino)

        print(f"  Aristas cargadas: {grafo.cantidad_enlaces()}")
        return grafo
