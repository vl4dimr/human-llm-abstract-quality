# data/raw/ está intencionadamente vacío

Aquí van los cuadernillos de anotación originales y el corpus, que **no se
redistribuyen**: contienen los textos y los títulos de las tesis, cuyo copyright
pertenece a sus autores e instituciones.

Para reconstruir esta carpeta:

1. Consigue los cuadernillos de anotación originales de los autores del estudio.
2. Ajusta las rutas en `src/00_stage_raw.py`.
3. Ejecuta `python src/00_stage_raw.py`, que los copia aquí en solo lectura y escribe
   `PROVENANCE.json` con el SHA-256 de cada archivo.

Para reconstruir solo los textos de los resúmenes, `outputs/dataset_release/documents.csv`
lleva el handle persistente de cada registro en su repositorio de origen.
