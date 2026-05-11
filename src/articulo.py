class Articulo:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre
        self.categorias: list[str] = []
        self.vecinos_salida: list[int] = []   # aristas que salen
        self.vecinos_entrada: list[int] = []  # aristas que entran

    def agregar_categoria(self, categoria: str):
        self.categorias.append(categoria)

    def agregar_arista_salida(self, id_destino: int):
        self.vecinos_salida.append(id_destino)

    def agregar_arista_entrada(self, id_origen: int):
        self.vecinos_entrada.append(id_origen)

    def grado_salida(self) -> int:
        return len(self.vecinos_salida)

    def grado_entrada(self) -> int:
        return len(self.vecinos_entrada)

    def __repr__(self):
        return f"Articulo(id={self.id}, nombre='{self.nombre}', " \
               f"in={self.grado_entrada()}, out={self.grado_salida()})"