from collections import deque

from modelos.articulo import ArticuloWikipedia


class GrafoWikipedia:
    """Representa un grafo dirigido de articulos de Wikipedia y sus enlaces."""

    def __init__(self):
        self.articulos = {}

    def agregar_articulo(self, id_articulo, nombre):
        pass
        # TODO

    def obtener_articulo(self, id_articulo):
        pass
        # TODO

    def agregar_enlace(self, id_origen, id_destino):
        pass
        # TODO

    def cantidad_articulos(self):
        pass        
        # TODO

    def cantidad_enlaces(self):
        pass
        # TODO

    def top_por_grado_entrada(self, cantidad=10):
        lista = list(self.articulos.values())
        #TODO
        return lista[:cantidad]

    def top_por_grado_salida(self, cantidad=10):
        lista = list(self.articulos.values())
        #TODO
        return lista[:cantidad]

    def resumen(self):
        return {
            "articulos": self.cantidad_articulos(),
            "enlaces": self.cantidad_enlaces(),
        }

    def bfs(self, id_inicio):
        """
        TODO:
        Implementar recorrido BFS.

        Sugerencia:
        - usar una cola (`deque`);
        - marcar visitados;
        - retornar el orden de visita.
        """
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
        """
        TODO:
        Completar o reescribir este método usando una pila o recursión.
        """
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
        """
        TODO:
        Mejorar esta búsqueda para encontrar caminos más interesantes.
        Por ahora retorna un camino simple usando BFS.
        """
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

    def pagerank(self, iteraciones=20, damping=0.85):
        """
        TODO:
        Este método puede servir como base para la versión final.
        Puede validarlo, modificarlo o reimplementarlo.
        """
        cantidad_nodos = self.cantidad_articulos()
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
                    #TODO, COMPLETAR LA LINEA FALTANTE

            puntajes = nuevos_puntajes

        return puntajes
