# -*- coding: utf-8 -*-

archivos = [
    "Data/wiki-topcats.mtx",
    "Data/wiki-topcats_pagenames.txt",
    "Data/wiki-topcats_Categories.mtx",
    "Data/wiki-topcats_Category_names.txt"
]

for nombre in archivos:
    print(f"\n{'='*50}")
    print(f"ARCHIVO: {nombre}")
    print('='*50)
    with open(nombre, "r", encoding="utf-8", errors="ignore") as f:
        for i, linea in enumerate(f):
            print(f"  {i}: {linea.strip()}")
            if i >= 12:
                break
            
print("-"*20)
# Ver las primeras líneas DESPUÉS del header del .mtx principal
with open("Data/wiki-topcats.mtx", "r", encoding="utf-8", errors="ignore") as f:
    for i, linea in enumerate(f):
        if not linea.startswith("%"):
            print(f"Línea de dimensiones: {linea.strip()}")
            # Leer las siguientes 5 para ver el formato de aristas
            for j in range(5):
                print(f"  arista ejemplo: {next(f).strip()}")
            break
