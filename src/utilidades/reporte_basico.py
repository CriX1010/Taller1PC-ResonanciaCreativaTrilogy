from pathlib import Path


class ReporteBasicoWikipedia:
    """Genera un reporte simple del grafo y lo exporta a la carpeta de resultados."""

    def __init__(self, carpeta_resultados=None):
        if carpeta_resultados is None:
            self.carpeta_resultados = Path(__file__).resolve().parent.parent.parent / "results"
        else:
            self.carpeta_resultados = Path(carpeta_resultados)

    def generar(self, grafo):
        self.carpeta_resultados.mkdir(parents=True, exist_ok=True)

        resumen = grafo.resumen()
        top_salida = self._extraer_top(grafo.top_por_grado_salida(5), "salida")
        top_entrada = self._extraer_top(grafo.top_por_grado_entrada(5), "entrada")

        ruta_texto = self.carpeta_resultados / "reporte_basico.txt"
        self._exportar_texto(ruta_texto, resumen, top_entrada, top_salida)

        return {
            "texto": ruta_texto,
        }

    def imprimir_en_consola(self, grafo):
        resumen = grafo.resumen()
        top_entrada = self._extraer_top(grafo.top_por_grado_entrada(10), "entrada")
        top_salida = self._extraer_top(grafo.top_por_grado_salida(10), "salida")

        print("Resumen del grafo")
        print("-----------------")
        print(f"Cantidad de articulos: {resumen['articulos']}")
        print(f"Cantidad de enlaces: {resumen['enlaces']}")

        self._imprimir_top("Top 10 por grado de entrada", top_entrada)
        self._imprimir_top("Top 10 por grado de salida", top_salida)

    def _extraer_top(self, articulos, tipo_grado):
        top = []

        for articulo in articulos:
            if tipo_grado == "entrada":
                valor = articulo.grado_entrada()
            else:
                valor = articulo.grado_salida()

            top.append({
                "nombre": articulo.nombre,
                "valor": valor,
            })

        return top

    def _exportar_texto(self, ruta_salida, resumen, top_entrada, top_salida):
        lineas = [
            "Reporte basico de Wikipedia",
            "",
            f"Cantidad de articulos: {resumen['articulos']}",
            f"Cantidad de enlaces: {resumen['enlaces']}",
            "",
            "Top 5 por grado de entrada:",
        ]

        if top_entrada:
            for indice, item in enumerate(top_entrada, start=1):
                lineas.append(f"{indice}. {item['nombre']} -> {item['valor']}")
        else:
            lineas.append("Sin datos.")

        lineas.append("")
        lineas.append("Top 5 por grado de salida:")

        if top_salida:
            for indice, item in enumerate(top_salida, start=1):
                lineas.append(f"{indice}. {item['nombre']} -> {item['valor']}")
        else:
            lineas.append("Sin datos.")

        ruta_salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def _imprimir_top(self, titulo, items):
        print()
        print(titulo)
        print("-" * len(titulo))

        for posicion, item in enumerate(items, start=1):
            print(f"{posicion}. {item['nombre']} -> {item['valor']}")
