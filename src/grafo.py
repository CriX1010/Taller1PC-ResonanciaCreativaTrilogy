from src.articulo import Articulo

class Grafo:
    def __init__(self):
        self.nodos: dict[int, Articulo] = {}  # id -> Articulo
        self.num_aristas: int = 0

    def agregar_nodo(self, articulo):
        if articulo.id not in self.nodos:
            self.nodos[articulo.id] = articulo

    def agregar_arista(self, id_origen: int, id_destino: int):
        if id_origen in self.nodos and id_destino in self.nodos:
            self.nodos[id_origen].agregar_arista_salida(id_destino)
            self.nodos[id_destino].agregar_arista_entrada(id_origen)
            self.num_aristas += 1

    def obtener_nodo(self, id: int):
        return self.nodos.get(id, None)

    def __len__(self):
        return len(self.nodos)

    def __repr__(self):
        return f"Grafo(nodos={len(self.nodos)}, aristas={self.num_aristas})"