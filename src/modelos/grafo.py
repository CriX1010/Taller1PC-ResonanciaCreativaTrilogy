from collections import deque

from modelos.articulo import ArticuloWikipedia


class GrafoWikipedia:
    """Representa un grafo dirigido de articulos de Wikipedia y sus enlaces."""

    def __init__(self):
        self.articulos = {}

    def agregar_articulo(self, id_articulo, nombre):
        if id_articulo not in self.articulos:
            self.articulos[id_articulo] = ArticuloWikipedia(id_articulo, nombre)

    def obtener_articulo(self, id_articulo):
        return self.articulos.get(id_articulo, None)

    def agregar_enlace(self, id_origen, id_destino):
        if id_origen in self.articulos and id_destino in self.articulos:
            self.articulos[id_origen].agregar_enlace_salida(id_destino)
            self.articulos[id_destino].agregar_enlace_entrada(id_origen)

    def cantidad_articulos(self):
        return len(self.articulos)

    def cantidad_enlaces(self):
        return sum(a.grado_salida() for a in self.articulos.values())

    def top_por_grado_entrada(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda a: a.grado_entrada(), reverse=True)
        return lista[:cantidad]

    def top_por_grado_salida(self, cantidad=10):
        lista = list(self.articulos.values())
        lista.sort(key=lambda a: a.grado_salida(), reverse=True)
        return lista[:cantidad]

    def resumen(self):
        return {
            "articulos": self.cantidad_articulos(),
            "enlaces": self.cantidad_enlaces(),
        }

    def bfs(self, id_inicio):
        """Recorre el grafo completo desde id_inicio usando anchura. Retorna el orden de visita."""
        if id_inicio not in self.articulos:
            return []

        visitados = set([id_inicio])
        cola = deque([id_inicio])
        recorrido = []

        while cola:
            actual = cola.popleft()
            recorrido.append(actual)

            for vecino in self.articulos[actual].enlaces_salida:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return recorrido

    def dfs(self, id_inicio):
        """Recorre el grafo completo desde id_inicio usando profundidad. Retorna el orden de visita."""
        if id_inicio not in self.articulos:
            return []

        visitados = set()
        pila = [id_inicio]
        recorrido = []

        while pila:
            actual = pila.pop()

            if actual in visitados:
                continue

            visitados.add(actual)
            recorrido.append(actual)

            vecinos = list(self.articulos[actual].enlaces_salida)
            vecinos.reverse()

            for vecino in vecinos:
                if vecino not in visitados:
                    pila.append(vecino)

        return recorrido

    def encontrar_camino_simple(self, id_origen, id_destino):
        """Encuentra el camino más corto entre dos artículos usando BFS. Retorna lista de IDs."""
        if id_origen not in self.articulos or id_destino not in self.articulos:
            return []

        cola = deque([id_origen])
        padres = {id_origen: None}

        while cola:
            actual = cola.popleft()

            if actual == id_destino:
                break

            for vecino in self.articulos[actual].enlaces_salida:
                if vecino not in padres:
                    padres[vecino] = actual
                    cola.append(vecino)

        if id_destino not in padres:
            return []

        camino = []
        actual = id_destino

        while actual is not None:
            camino.append(actual)
            actual = padres[actual]

        camino.reverse()
        return camino

    def pagerank(self, iteraciones=20):
        """Calcula la relevancia de cada artículo usando el algoritmo Pagerank
        iterativo. Retorna un diccionario id_articulo -> puntaje."""
        cantidad_nodos = self.cantidad_articulos()
        damping=0.85
        if cantidad_nodos == 0:
            return {}

        puntajes = {}
        valor_inicial = 1.0 / cantidad_nodos

        for id_articulo in self.articulos:
            puntajes[id_articulo] = valor_inicial

        for _ in range(iteraciones):
            nuevos_puntajes = {}

            for id_articulo in self.articulos:
                nuevos_puntajes[id_articulo] = (1.0 - damping) / cantidad_nodos

            for id_articulo, articulo in self.articulos.items():
                if articulo.grado_salida() == 0:
                    continue

                aporte = puntajes[id_articulo] / articulo.grado_salida()

                for vecino in articulo.enlaces_salida:
                    nuevos_puntajes[vecino] = nuevos_puntajes.get(vecino, 0) + damping * aporte

            puntajes = nuevos_puntajes

        return puntajes

    def obtener_nombre(self, id_articulo):
        articulo = self.articulos.get(id_articulo)
        if articulo:
            return articulo.nombre
        return f"ID {id_articulo} (desconocido)"