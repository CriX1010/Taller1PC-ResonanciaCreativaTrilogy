from src.loader import cargar_nombres, cargar_categorias, cargar_grafo_filtrado

DATA = "data/"

print("Cargando nombres...")
nombres = cargar_nombres(DATA + "wiki-topcats_pagenames.txt")

print("Cargando categorías...")
categorias = cargar_categorias(
    DATA + "wiki-topcats_Categories.mtx",
    DATA + "wiki-topcats_Category_names.txt"
)

# Ver las 10 categorías más grandes
top10 = sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True)[:10]
print("\nTop 10 categorías más grandes:")
for i, (nombre, ids) in enumerate(top10, 1):
    print(f"  {i:2}. {nombre:<45} ({len(ids):,} artículos)")