# Informe de auditoria de datos (Fase 1)

Generado: 2026-09-18T18:42:11  ·  semilla: 42

## 0. Procedencia de los archivos crudos

14 archivos copiados el 2026-09-18T23:40:10.953676+00:00 (SHA-256 en `data/raw/PROVENANCE.json`).

| path                                                    |   bytes | sha256        |
|:--------------------------------------------------------|--------:|:--------------|
| annotations/Anotacion_principal_A1.xlsx                 |  260814 | 97bf1a6bb4e7… |
| annotations/Anotacion_principal_A1_REV.xlsx             |  259949 | 6c1c197134d1… |
| annotations/Anotacion_principal_A1_v0.xlsx              |  252902 | 78ec617d5cd9… |
| annotations/Anotacion_principal_A2.xlsx                 |  261003 | 04373c17b510… |
| annotations/Anotacion_principal_A2_independiente.xlsx   |  146731 | f01c9d8e6790… |
| annotations/Anotacion_calibracion_A2_independiente.xlsx |   38674 | b99de01e451a… |
| annotations/Anotacion_calibracion_A1.xlsx               |   40631 | 2c3f8944e040… |
| annotations/Anotacion_calibracion_A2.xlsx               |   40834 | 8d1dd49221fb… |
| annotations/Anotacion_principal_A3_template.csv         |    7468 | 42389e1dd9ee… |
| llm_prior/Anotacion_IA_Claude.xlsx                      |  224911 | 721d70d0689b… |
| scheme/PROTOCOLO_ANOTACION.md                           |   34202 | 4a30f7d35e11… |
| corpus/clave_maestra.csv                                |   95632 | 6343a4817349… |
| corpus/cuadernillo_principal.txt                        |  606675 | 3e2fb3958fcc… |
| corpus/CORPUS.md                                        |    1826 | 551e801fba3d… |

## 1. Corpus muestreado (clave maestra)

Filas en la clave maestra: **330**. IDs unicos: True.

Por fase:

| fase        |   n |
|:------------|----:|
| calibracion |  30 |
| principal   | 300 |

Fase de analisis: `principal` -> **300 documentos**. Fases excluidas: ['calibracion'].

Composicion de la fase de analisis (tipo de tesis):

| tipo           |   n |   pct |
|:---------------|----:|------:|
| Thesis         |   3 |   1.0 |
| bachelorThesis | 258 |  86.0 |
| doctoralThesis |   8 |   2.7 |
| masterThesis   |  31 |  10.3 |

Por institucion:

| institucion_cod   |   n |
|:------------------|----:|
| UANCV             |  24 |
| UNAP              | 174 |
| UPEU              |  85 |
| UPSC              |  17 |

Por estrato disciplinar (OCDE/FORD):

| estrato                           |   n |
|:----------------------------------|----:|
| Ciencias Sociales                 |  65 |
| (sin código FORD)                 |  52 |
| Ingeniería y Tecnología           |  43 |
| Ciencias Médicas y de la Salud    |  41 |
| Ciencias Naturales                |  34 |
| Humanidades y Artes               |  33 |
| Ciencias Agrícolas y Veterinarias |  32 |

Anios: 2016–2026. Palabras por resumen (segun clave): media 255, mediana 246, min 93, max 915.

> **Aviso:** solo 8 de 300 documentos de la fase principal son tesis doctorales (2.7 %). El corpus es mayoritariamente de tesis de pregrado (bachelorThesis). La descripcion del estudio como «resumenes de tesis doctorales» no coincide con los datos.

## 2. Cuadernillos de anotacion

| workbook           | file                                      |   rows |   annotated_rows |   coverage_pct | annotated_range   | contiguous   |   duplicate_ids |   ids_not_in_key |   D4_filled |   notes_filled |
|:-------------------|:------------------------------------------|-------:|-----------------:|---------------:|:------------------|:-------------|----------------:|-----------------:|------------:|---------------:|
| A1                 | Anotacion_principal_A1.xlsx               |    300 |              160 |         53.300 | 1–160             | True         |               0 |                0 |         148 |            160 |
| A2                 | Anotacion_principal_A2_independiente.xlsx |    160 |              160 |        100.000 | 1–160             | True         |               0 |                0 |         148 |            160 |
| A3                 | Anotacion_principal_A3_template.csv       |    300 |                0 |          0.000 | —                 | False        |               0 |                0 |           0 |              0 |
| A1[A1_REV]         | Anotacion_principal_A1_REV.xlsx           |    300 |              160 |         53.300 | 1–160             | True         |               0 |                0 |         148 |            160 |
| A1[A1_v0]          | Anotacion_principal_A1_v0.xlsx            |    300 |              120 |         40.000 | 1–120             | True         |               0 |                0 |         109 |            120 |
| A2[original_copia] | Anotacion_principal_A2.xlsx               |    300 |              160 |         53.300 | 1–160             | True         |               0 |                0 |         148 |            160 |
| LLM_prior          | Anotacion_IA_Claude.xlsx                  |    300 |              214 |         71.300 | 2–215             | True         |               0 |                0 |         193 |            214 |

Valores fuera del esquema: **0**.

> A3: plantilla declarada como vacia en config; anotadas = 0. Confirmado: **A3 no anoto nada**.

## 3. Textos de los resumenes

Textos vacios: **0**. Textos < 200 caracteres: **0**. Textos que no terminan en puntuacion (posible truncado): **25**.

IDs sin puntuacion final: GT-012, GT-018, GT-027, GT-029, GT-041, GT-043, GT-046, GT-074, GT-083, GT-088, GT-096, GT-101, GT-104, GT-119, GT-124, GT-125, GT-126, GT-151, GT-162, GT-169, GT-172, GT-209, GT-239, GT-240, GT-247

Documentos cuyo texto difiere >15 % en palabras de lo declarado en la clave: **0**.

¿Los cuadernillos contienen el mismo texto por id?

| workbook           |   ids_common |   texts_differ |
|:-------------------|-------------:|---------------:|
| A2                 |          160 |              0 |
| A1[A1_REV]         |          300 |              0 |
| A1[A1_v0]          |          300 |              0 |
| A2[original_copia] |          300 |              0 |
| LLM_prior          |          300 |              0 |

## 4. Cobertura cruzada (fase principal)

Anotadores humanos activos: ['A1', 'A2']. Documentos con TODOS ellos: **160**; con al menos uno: 160; con uno solo: **0**; sin ningun humano: **140** de 300.

LLM_prior anotado: 214 docs; solapa con los dos humanos en **159** docs.

## 5. Independencia entre cuadernillos (diferencia celda a celda)

Para cada par se comparan las 12 variables en los documentos anotados por ambos, y ademas el texto libre de `observaciones`. Dos anotadores independientes no pueden producir observaciones libres identicas.

| pair                             |   docs_common |   cells |   cells_differ |   pct_differ |   notes_both |   notes_identical | differing_vars                                                                                                                                                                                                                                                                  |
|:---------------------------------|--------------:|--------:|---------------:|-------------:|-------------:|------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A1 vs A2                         |           160 |    1920 |            147 |         7.66 |          160 |                 0 | D1_imryd_metodologia:4, D1_imryd_resultados:3, D1_imryd_conclusiones:8, D1_orden_logico:4, D2_coherencia:46, D3_contextualizacion:7, D3_metodo_detallado:15, D3_resultados_concretos:2, D3_conclusion_responde:12, D4_consistencia:46                                           |
| A1 vs A1[A1_REV]                 |           160 |    1920 |             22 |         1.15 |          160 |               138 | D4_consistencia:22                                                                                                                                                                                                                                                              |
| A1 vs A1[A1_v0]                  |           120 |    1440 |             15 |         1.04 |          120 |               105 | D4_consistencia:15                                                                                                                                                                                                                                                              |
| A1 vs A2[original_copia]         |           160 |    1920 |              0 |         0.00 |          160 |               159 | —                                                                                                                                                                                                                                                                               |
| A1 vs LLM_prior                  |           159 |    1908 |            371 |        19.44 |          159 |                 0 | D1_imryd_objetivo:2, D1_imryd_metodologia:3, D1_imryd_resultados:7, D1_imryd_conclusiones:16, D1_orden_logico:15, D2_coherencia:99, D3_contextualizacion:78, D3_metodo_detallado:14, D3_resultados_concretos:9, D3_conclusion_responde:17, D4_consistencia:109, no_evaluable:2  |
| A2 vs A1[A1_REV]                 |           160 |    1920 |            143 |         7.45 |          160 |                 0 | D1_imryd_metodologia:4, D1_imryd_resultados:3, D1_imryd_conclusiones:8, D1_orden_logico:4, D2_coherencia:46, D3_contextualizacion:7, D3_metodo_detallado:15, D3_resultados_concretos:2, D3_conclusion_responde:12, D4_consistencia:42                                           |
| A2 vs A1[A1_v0]                  |           120 |    1440 |            111 |         7.71 |          120 |                 0 | D1_imryd_metodologia:4, D1_imryd_resultados:3, D1_imryd_conclusiones:7, D1_orden_logico:3, D2_coherencia:34, D3_contextualizacion:6, D3_metodo_detallado:12, D3_resultados_concretos:1, D3_conclusion_responde:8, D4_consistencia:33                                            |
| A2 vs A2[original_copia]         |           160 |    1920 |            147 |         7.66 |          160 |                 0 | D1_imryd_metodologia:4, D1_imryd_resultados:3, D1_imryd_conclusiones:8, D1_orden_logico:4, D2_coherencia:46, D3_contextualizacion:7, D3_metodo_detallado:15, D3_resultados_concretos:2, D3_conclusion_responde:12, D4_consistencia:46                                           |
| A2 vs LLM_prior                  |           159 |    1908 |            370 |        19.39 |          159 |                 0 | D1_imryd_objetivo:2, D1_imryd_metodologia:5, D1_imryd_resultados:10, D1_imryd_conclusiones:17, D1_orden_logico:13, D2_coherencia:90, D3_contextualizacion:80, D3_metodo_detallado:10, D3_resultados_concretos:9, D3_conclusion_responde:20, D4_consistencia:112, no_evaluable:2 |
| A1[A1_REV] vs A1[A1_v0]          |           120 |    1440 |              0 |         0.00 |          120 |               120 | —                                                                                                                                                                                                                                                                               |
| A1[A1_REV] vs A2[original_copia] |           160 |    1920 |             22 |         1.15 |          160 |               137 | D4_consistencia:22                                                                                                                                                                                                                                                              |
| A1[A1_REV] vs LLM_prior          |           159 |    1908 |            380 |        19.92 |          159 |                 0 | D1_imryd_objetivo:2, D1_imryd_metodologia:3, D1_imryd_resultados:7, D1_imryd_conclusiones:16, D1_orden_logico:15, D2_coherencia:99, D3_contextualizacion:78, D3_metodo_detallado:14, D3_resultados_concretos:9, D3_conclusion_responde:17, D4_consistencia:118, no_evaluable:2  |
| A1[A1_v0] vs A2[original_copia]  |           120 |    1440 |             15 |         1.04 |          120 |               104 | D4_consistencia:15                                                                                                                                                                                                                                                              |
| A1[A1_v0] vs LLM_prior           |           119 |    1428 |            294 |        20.59 |          119 |                 0 | D1_imryd_objetivo:1, D1_imryd_metodologia:3, D1_imryd_resultados:5, D1_imryd_conclusiones:15, D1_orden_logico:12, D2_coherencia:76, D3_contextualizacion:61, D3_metodo_detallado:11, D3_resultados_concretos:6, D3_conclusion_responde:14, D4_consistencia:88, no_evaluable:2   |
| A2[original_copia] vs LLM_prior  |           159 |    1908 |            371 |        19.44 |          159 |                 0 | D1_imryd_objetivo:2, D1_imryd_metodologia:3, D1_imryd_resultados:7, D1_imryd_conclusiones:16, D1_orden_logico:15, D2_coherencia:99, D3_contextualizacion:78, D3_metodo_detallado:14, D3_resultados_concretos:9, D3_conclusion_responde:17, D4_consistencia:109, no_evaluable:2  |

> **HALLAZGO CRITICO.** Los siguientes pares son copias exactas (0 celdas distintas y observaciones libres identicas):

> - **A1 vs A2[original_copia]** — 160 documentos, 159/160 observaciones identicas.
>
> Un acuerdo humano-humano calculado sobre un par asi vale 1.0 por construccion y no mide nada. **No existe en estos datos una segunda anotacion humana independiente.**

Fase de calibracion (A1 vs A2): 30 docs, **31** celdas distintas de 360, observaciones identicas 0/30.

Relacion entre las versiones de A1: `A1_v0` (120 docs) ⊂ `A1_REV` (160 docs) celda por celda; `A1` (la mas reciente) difiere de `A1_REV` solo en `D4_consistencia`. Ver seccion 10.

### 5b. Alineacion de filas: LLM_prior vs A1

Se compara A1[k] con LLM_crudo[k + s] para s en −3..+3. Si el maximo no esta en s = 0, los valores del cuadernillo LLM estan corridos respecto a sus textos. Se usa el archivo **crudo** (sin aplicar `row_offset`, que ahora vale -1).

|   shift |   D1_objetivo |   D1_metodologia |   D1_resultados |   D1_conclusione |   D1_orden_logic |   D2_coherencia |   D3_contextuali |   D3_metodo_deta |   D3_resultados_ |   D3_conclusion_ |   D4_consistenci |   no_evaluable |   mean_kappa |
|--------:|--------------:|-----------------:|----------------:|-----------------:|-----------------:|----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|---------------:|-------------:|
|  -3.000 |         0.000 |           -0.062 |          -0.156 |           -0.092 |            0.059 |           0.028 |           -0.048 |            0.035 |           -0.028 |           -0.140 |           -0.012 |          0.088 |       -0.027 |
|  -2.000 |         0.000 |           -0.072 |           0.057 |            0.097 |           -0.060 |          -0.068 |            0.034 |           -0.070 |            0.008 |            0.095 |            0.019 |         -0.089 |       -0.004 |
|  -1.000 |         0.000 |            0.893 |           0.842 |            0.782 |            0.254 |           0.600 |            0.092 |            0.737 |            0.862 |            0.778 |            0.278 |          0.916 |        0.586 |
|   0.000 |         0.000 |           -0.071 |          -0.004 |            0.171 |           -0.065 |          -0.039 |           -0.074 |            0.130 |            0.033 |            0.196 |           -0.018 |         -0.088 |        0.014 |
|   1.000 |         0.000 |           -0.067 |          -0.165 |           -0.053 |           -0.065 |          -0.058 |           -0.001 |           -0.059 |           -0.012 |           -0.073 |           -0.059 |         -0.004 |       -0.051 |
|   2.000 |         0.000 |           -0.071 |           0.050 |           -0.053 |            0.041 |           0.074 |           -0.082 |            0.049 |            0.031 |           -0.100 |           -0.005 |         -0.085 |       -0.013 |
|   3.000 |         0.000 |            0.133 |           0.145 |           -0.053 |            0.041 |          -0.091 |            0.036 |            0.002 |            0.024 |           -0.017 |            0.005 |          0.089 |        0.026 |

Evidencia independiente: citas literales de las `observaciones` de la fila k buscadas en el texto del documento k + offset (un anotador alineado cita el texto de su propia fila):

| workbook          |   offset |   quotes |   found_in_text |
|:------------------|---------:|---------:|----------------:|
| A1                |       -1 |      110 |               0 |
| A1                |        0 |      112 |              66 |
| A1                |        1 |      112 |               0 |
| LLM_prior (crudo) |       -1 |       87 |               0 |
| LLM_prior (crudo) |        0 |       88 |               0 |
| LLM_prior (crudo) |        1 |       88 |              35 |

> **HALLAZGO.** El acuerdo A1–LLM_prior es maximo con desplazamiento **s = -1** (κ medio 0.586) y practicamente nulo con s = 0 (κ medio 0.014). Las citas de A1 caen en su propia fila y las del LLM en la fila k+1: **el cuadernillo del LLM tiene sus valores y observaciones corridos una fila respecto a los textos** (la fila GT-k contiene el juicio del documento GT-(k+1)). Es un error de manipulacion del archivo previo, no un desacuerdo real. Para corregirlo: `llm_prior.row_offset: -1` en config.yaml y volver a ejecutar. No se ha tocado `data/raw/`.

## 6. Consistencia con las reglas del protocolo

| workbook           |   D3=1 con D1=0 (§8.4) |   orden=1 con ≤1 componente (§6.5) |   D4 vacio |   D4 vacio y no_evaluable=1 |   no_evaluable=1 con D4 relleno (§9.3) |   no_evaluable=1 con D4 vacio pero otras rellenas |
|:-------------------|-----------------------:|-----------------------------------:|-----------:|----------------------------:|---------------------------------------:|--------------------------------------------------:|
| A1                 |                      0 |                                  8 |         12 |                          12 |                                      0 |                                                11 |
| A2                 |                      0 |                                  9 |         12 |                          12 |                                      0 |                                                11 |
| A1[A1_REV]         |                      0 |                                  8 |         12 |                          12 |                                      0 |                                                11 |
| A1[A1_v0]          |                      0 |                                  7 |         11 |                          11 |                                      0 |                                                10 |
| A2[original_copia] |                      0 |                                  8 |         12 |                          12 |                                      0 |                                                11 |
| LLM_prior          |                      0 |                                  0 |         21 |                          21 |                                      0 |                                                17 |

> Nota: §8.4 hace que D3 dependa deterministicamente de D1 (si D1=0 entonces D3=0). El acuerdo en D3 hereda parte del acuerdo en D1; las 12 variables no son 12 pruebas independientes.

> Nota: la regla §6.5 (orden = 0 con ≤ 1 componentes) se incumple en 8 documentos por los humanos y en 0 por el LLM. Es un desvio del anotador respecto al manual, no un error de datos; se deja tal cual.

## 7. Normalizacion

- `data\interim\annotations.csv`: 6303 filas (doc_id, annotator, category, label). Solo celdas no vacias; una fila ausente = no anotado.
- `data\interim\documents.csv`: 300 documentos con texto y metadatos. **Contiene titulos: no es la version de deposito.**

| annotator   |   rows |   docs |
|:------------|-------:|-------:|
| A1          |   1898 |    160 |
| A2          |   1898 |    160 |
| LLM_prior   |   2507 |    214 |

## 8. Prevalencia por variable y anotador (fase principal, docs anotados)

| variable                | type    | dimension   |   A1_n |   A1_p1 |   A2_n |   A2_p1 |   LLM_prior_n |   LLM_prior_p1 |   A1_mean |   A2_mean |   LLM_prior_mean |
|:------------------------|:--------|:------------|-------:|--------:|-------:|--------:|--------------:|---------------:|----------:|----------:|-----------------:|
| D1_imryd_objetivo       | binary  | D1          |    159 |   0.994 |    159 |   0.994 |           210 |          1.000 |   nan     |   nan     |          nan     |
| D1_imryd_metodologia    | binary  | D1          |    159 |   0.931 |    159 |   0.906 |           210 |          0.924 |   nan     |   nan     |          nan     |
| D1_imryd_resultados     | binary  | D1          |    159 |   0.868 |    159 |   0.849 |           210 |          0.848 |   nan     |   nan     |          nan     |
| D1_imryd_conclusiones   | binary  | D1          |    159 |   0.704 |    159 |   0.692 |           210 |          0.690 |   nan     |   nan     |          nan     |
| D1_orden_logico         | binary  | D1          |    159 |   0.950 |    159 |   0.962 |           210 |          0.924 |   nan     |   nan     |          nan     |
| D2_coherencia           | ordinal | D2          |    159 | nan     |    159 | nan     |           210 |        nan     |     3.000 |     3.220 |            3.386 |
| D3_contextualizacion    | binary  | D3          |    159 |   0.918 |    159 |   0.925 |           210 |          0.443 |   nan     |   nan     |          nan     |
| D3_metodo_detallado     | binary  | D3          |    159 |   0.774 |    159 |   0.830 |           210 |          0.829 |   nan     |   nan     |          nan     |
| D3_resultados_concretos | binary  | D3          |    159 |   0.730 |    159 |   0.742 |           210 |          0.790 |   nan     |   nan     |          nan     |
| D3_conclusion_responde  | binary  | D3          |    159 |   0.654 |    159 |   0.629 |           210 |          0.676 |   nan     |   nan     |          nan     |
| D4_consistencia         | ordinal | D4          |    148 | nan     |    148 | nan     |           193 |        nan     |     2.304 |     2.399 |            3.642 |
| no_evaluable            | binary  | control     |    160 |   0.075 |    160 |   0.075 |           214 |          0.098 |   nan     |   nan     |          nan     |

Distribucion de las ordinales:

| variable        | A1_dist                | A2_dist                | LLM_prior_dist           |
|:----------------|:-----------------------|:-----------------------|:-------------------------|
| D2_coherencia   | 1:1 2:44 3:73 4:36 5:5 | 1:1 2:28 3:70 4:55 5:5 | 1:12 2:34 3:51 4:87 5:26 |
| D4_consistencia | 1:19 2:81 3:36 4:8 5:4 | 1:8 2:85 3:43 4:12     | 1:10 2:33 3:31 4:61 5:58 |

> Variables con prevalencia extrema (p1 > 0.95 o < 0.05) en humanos: `D1_imryd_objetivo` (0.994). Ahi kappa colapsa por construccion: AC1 y PABAK son imprescindibles.

> `D1_imryd_objetivo`: el LLM_prior asigna 1 a **todos** los documentos (varianza cero). Cualquier kappa contra el es degenerado o inestable.

## 9. Acuerdo entre anotadores, recalculado desde cero

Bootstrap: 2000 remuestreos a nivel de documento, IC percentil 95 %, semilla 42. Exclusion por pares de los faltantes (D4 vacio cuando no_evaluable = 1 es estructural, §9.3).

### 9a. A1 vs A2 (humano-humano)

| variable                | type    |   n |   p_obs |   kappa |   kappa_lo |   kappa_hi |   gwet_ac |   pabak |   kripp_alpha |
|:------------------------|:--------|----:|--------:|--------:|-----------:|-----------:|----------:|--------:|--------------:|
| D1_imryd_objetivo       | binary  | 159 |   1.000 |   1.000 |      1.000 |      1.000 |     1.000 |   1.000 |         1.000 |
| D1_imryd_metodologia    | binary  | 159 |   0.975 |   0.833 |      0.643 |      0.962 |     0.970 |   0.950 |         0.833 |
| D1_imryd_resultados     | binary  | 159 |   0.981 |   0.922 |      0.822 |      1.000 |     0.975 |   0.962 |         0.923 |
| D1_imryd_conclusiones   | binary  | 159 |   0.950 |   0.881 |      0.795 |      0.954 |     0.913 |   0.899 |         0.881 |
| D1_orden_logico         | binary  | 159 |   0.975 |   0.701 |      0.322 |      0.938 |     0.973 |   0.950 |         0.702 |
| D2_coherencia           | ordinal | 159 |   0.981 |   0.768 |      0.686 |      0.834 |     0.949 |   0.638 |         0.745 |
| D3_contextualizacion    | binary  | 159 |   0.956 |   0.696 |      0.441 |      0.886 |     0.949 |   0.912 |         0.697 |
| D3_metodo_detallado     | binary  | 159 |   0.906 |   0.705 |      0.560 |      0.830 |     0.862 |   0.811 |         0.704 |
| D3_resultados_concretos | binary  | 159 |   0.987 |   0.968 |      0.916 |      1.000 |     0.979 |   0.975 |         0.968 |
| D3_conclusion_responde  | binary  | 159 |   0.925 |   0.836 |      0.737 |      0.921 |     0.860 |   0.849 |         0.836 |
| D4_consistencia         | ordinal | 148 |   0.981 |   0.753 |      0.672 |      0.811 |     0.955 |   0.611 |         0.738 |
| no_evaluable            | binary  | 160 |   1.000 |   1.000 |      1.000 |      1.000 |     1.000 |   1.000 |         1.000 |

> No se ha proporcionado el valor de acuerdo humano-humano reportado previamente (`audit.previously_reported_agreement` en config.yaml). Indicalo para contrastarlo.

### 9b. A1 vs LLM_prior (solo contexto; row_offset = -1)

La anotacion LLM previa se hizo por chat (claude.ai), sin temperature fija, sin semilla ni repeticiones y con el protocolo v2.0. **No es admisible como corrida de la fase 2**; se muestra solo para ver que aspecto tiene un acuerdo no trivial en este esquema. Calculado tras realinear con offset -1.

| variable                | type    |   n |   p_obs |   kappa |   kappa_lo |   kappa_hi |   kappa_degenerate_frac |   gwet_ac |   ac_lo |   ac_hi |   pabak |   kripp_alpha |
|:------------------------|:--------|----:|--------:|--------:|-----------:|-----------:|------------------------:|----------:|--------:|--------:|--------:|--------------:|
| D1_imryd_objetivo       | binary  | 157 |   0.994 |   0.000 |      0.000 |      0.000 |                   0.376 |     0.994 |   0.981 |   1.000 |   0.987 |         0.000 |
| D1_imryd_metodologia    | binary  | 157 |   0.987 |   0.893 |      0.696 |      1.000 |                   0.000 |     0.986 |   0.963 |   1.000 |   0.975 |         0.894 |
| D1_imryd_resultados     | binary  | 157 |   0.962 |   0.842 |      0.697 |      0.947 |                   0.000 |     0.950 |   0.905 |   0.984 |   0.924 |         0.842 |
| D1_imryd_conclusiones   | binary  | 157 |   0.904 |   0.782 |      0.675 |      0.872 |                   0.000 |     0.830 |   0.744 |   0.903 |   0.809 |         0.782 |
| D1_orden_logico         | binary  | 157 |   0.911 |   0.254 |     -0.041 |      0.512 |                   0.000 |     0.899 |   0.835 |   0.946 |   0.822 |         0.255 |
| D2_coherencia           | ordinal | 157 |   0.951 |   0.600 |      0.510 |      0.679 |                   0.000 |     0.851 |   0.822 |   0.879 |   0.220 |         0.574 |
| D3_contextualizacion    | binary  | 157 |   0.510 |   0.092 |      0.021 |      0.171 |                   0.000 |     0.137 |  -0.044 |   0.302 |   0.019 |        -0.132 |
| D3_metodo_detallado     | binary  | 157 |   0.917 |   0.737 |      0.586 |      0.859 |                   0.000 |     0.879 |   0.803 |   0.942 |   0.834 |         0.736 |
| D3_resultados_concretos | binary  | 157 |   0.949 |   0.862 |      0.754 |      0.947 |                   0.000 |     0.920 |   0.855 |   0.969 |   0.898 |         0.862 |
| D3_conclusion_responde  | binary  | 157 |   0.898 |   0.778 |      0.673 |      0.868 |                   0.000 |     0.812 |   0.719 |   0.891 |   0.796 |         0.779 |
| D4_consistencia         | ordinal | 145 |   0.818 |   0.278 |      0.190 |      0.364 |                   0.000 |     0.360 |   0.243 |   0.466 |   0.078 |         0.106 |
| no_evaluable            | binary  | 159 |   0.987 |   0.916 |      0.767 |      1.000 |                   0.000 |     0.985 |   0.961 |   1.000 |   0.975 |         0.916 |

> IC de kappa inestable (fraccion de remuestreos degenerados > 0.1): `D1_imryd_objetivo` (0.38).

Matrices de confusion A1 (filas) vs LLM_prior (columnas):

| variable                | matrix                                                           |
|:------------------------|:-----------------------------------------------------------------|
| D1_imryd_objetivo       | 0 1 | 0 156                                                      |
| D1_imryd_metodologia    | 9 1 | 1 146                                                      |
| D1_imryd_resultados     | 19 1 | 5 132                                                     |
| D1_imryd_conclusiones   | 43 3 | 12 99                                                     |
| D1_orden_logico         | 3 5 | 9 140                                                      |
| D2_coherencia           | 1 0 0 0 0 | 5 19 16 3 0 | 1 10 15 43 3 | 0 1 1 21 13 | 0 0 0 2 3 |
| D3_contextualizacion    | 11 2 | 75 69                                                     |
| D3_metodo_detallado     | 24 11 | 2 120                                                    |
| D3_resultados_concretos | 34 8 | 0 115                                                     |
| D3_conclusion_responde  | 48 6 | 10 93                                                     |
| D4_consistencia         | 8 7 1 2 1 | 1 16 13 33 16 | 0 1 8 8 18 | 0 0 0 3 5 | 0 0 0 1 3   |
| no_evaluable            | 145 2 | 0 12                                                     |

## 10. Estado y bloqueos

### Resuelto

- **Segunda anotacion humana independiente disponible.** A1 y A2 difieren en 147/1920 celdas (acuerdo bruto 92.3 %) y ninguna observacion libre coincide. La linea base kappa(A1-A2) y el contraste delta-kappa ya son calculables.
- El A2 **original** era copia exacta de A1 (0 celdas distintas, 159/160 observaciones identicas). Se conserva en `data/raw/` solo como evidencia de esta auditoria; `config.yaml` ya no lo usa.
- **Modelos de la fase 2 definidos**: ['mistral-7b', 'qwen3-8b', 'gpt-oss-20b'], 3 corridas cada uno.

### Pendiente

- **Cobertura:** 160 de 300 documentos de la fase principal tienen anotacion humana doble (53 %). Los 140 restantes quedan fuera del analisis; no se imputa nada.
- **Corpus:** 8 tesis doctorales de 300; el resto son de pregrado y maestria. Hay que corregir la descripcion del estudio o restringir la muestra.
- **Tres versiones de A1** que difieren en 22 celdas de `D4_consistencia` (la '-REV' es sistematicamente un punto mas baja). En uso: `annotations/Anotacion_principal_A1.xlsx`.

