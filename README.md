# Concordancia humano–LLM en la anotación de resúmenes de tesis

Pipeline reproducible para un estudio de concordancia entre anotadores humanos y
modelos de lenguaje sobre un esquema de calidad estructural de resúmenes de tesis
(protocolo IMRyD, 12 variables: 10 binarias y 2 ordinales 1–5).

**Estado: análisis completo.** Las seis fases están ejecutadas sobre los 160
documentos, con las tres corridas de cada modelo y 2 000 remuestreos a nivel de
documento (semilla 42). Informes en [`outputs/audit_report.md`](outputs/audit_report.md)
y [`outputs/agreement_report.md`](outputs/agreement_report.md).

## Qué contiene y qué no este repositorio público

Este es el **paquete de replicación** del estudio. Incluye el código completo, las
anotaciones de los dos humanos y de los tres modelos, y todos los resultados
derivados.

**No incluye los textos de los resúmenes ni los títulos de las tesis.** Se cosecharon
por OAI-PMH de cuatro repositorios institucionales públicos y su copyright pertenece a
sus autores e instituciones; este estudio no tiene derecho a relicenciarlos.
`outputs/dataset_release/documents.csv` lleva el **handle persistente** de cada
registro, con el que se recupera el texto exacto en el repositorio de origen y se
reproduce cualquier análisis.

Por la misma razón, `data/raw/` está vacío aquí. Para reconstruirlo hacen falta los
cuadernillos de anotación originales; `src/00_stage_raw.py` documenta las rutas y deja
un manifiesto con SHA-256 de cada archivo, de modo que cualquiera puede verificar que
analiza exactamente los mismos bytes.


## Pregunta de investigación

¿El desacuerdo entre un LLM y un anotador humano es distinguible del desacuerdo
que ya existe entre dos anotadores humanos, y en qué variables concretas se rompe
esa equivalencia? Contraste central por variable: Δκ = κ(A1–LLM) − κ(A1–A2), con
IC bootstrap pareado a nivel de documento.

## Reproducir desde cero

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests/ -q          # 18 pruebas: estimadores + blindaje del prompt
python src/00_stage_raw.py          # copia los originales a data/raw + SHA-256
python src/01_audit.py              # ~35 s; escribe outputs/audit_report.md
python src/00b_select_subset.py     # subconjunto de trabajo + cuadernillo ciego para A2 (~1 min)
python src/02_annotate_llm.py --dry-run          # prompts y coste estimado, sin llamadas
python src/02_annotate_llm.py                    # Fase 2 (requiere llm.models en config.yaml)
python src/run_analysis.py                       # Fases 3-6 encadenadas
```

`run_analysis.py` comprueba primero que todas las corridas de LLM estén completas y
**se niega a seguir si falta alguna**: ejecutar la Fase 3 con datos parciales produce
cifras que parecen definitivas y no lo son. `--partial` lo fuerza y marca el informe;
`--quick` usa 200 remuestreos en vez de 2000, solo para pruebas.

`00_stage_raw.py` lee rutas absolutas del disco del investigador (listadas en el
propio script). En otra máquina basta con colocar los mismos archivos en
`data/raw/` y comprobar los hashes contra `data/raw/PROVENANCE.json`.

Python 3.14.0 en Windows 11. Versiones exactas en `requirements.txt`. Semilla 42
en todo lo aleatorio.

## Estructura

```
data/raw/            originales, solo lectura (attrib +R), con PROVENANCE.json
data/interim/        annotations.csv (largo canónico), documents.csv (con texto)
src/00_stage_raw.py  staging + manifiesto de procedencia   [añadido al plan]
src/01_audit.py      Fase 1
src/00b_select_subset.py  Fase 1b: subconjunto estratificado, cuadernillo ciego, simulacion de precision
src/00c_receive_a2.py     Fase 1c: valida el cuadernillo devuelto por A2 (incl. prueba de independencia)
src/02_annotate_llm.py    Fase 2: anotacion LLM (prompt literal, JSON estricto, cache por hash, N corridas)
src/lib/llm/         prompt.py (esquema + blindaje), providers.py (ollama / openai_compatible / google /
                     anthropic), cache.py
outputs/prompts/     el prompt de sistema y el esquema exactos usados, nombrados por su huella SHA-256
src/lib/metrics.py   κ, κ ponderado, AC1/AC2, PABAK, α de Krippendorff, bootstrap, BH
src/lib/io_raw.py    lectores que fallan ruidosamente si la estructura no coincide
tests/               pruebas contra sklearn, statsmodels y ejemplos publicados
outputs/tables/      CSV + LaTeX; las de confusión en outputs/tables/confusion/
outputs/figures/     fig1–3, en PDF vectorial y en PNG a 300 dpi
outputs/dataset_release/  el dataset publicable, con CHECKSUMS.sha256
data/interim/llm_cache/   las 1 443 respuestas crudas de los modelos
config.yaml          todas las decisiones metodológicas, con valor por defecto documentado
```

## Formato largo canónico

`data/interim/annotations.csv`: `doc_id, annotator, category, label`. Solo se
escriben celdas no vacías; una fila ausente significa «no anotado». Nunca se
imputa.

## Decisiones metodológicas (todas en `config.yaml`)

| Decisión | Valor por defecto | Alternativa / nota |
|---|---|---|
| κ para binarias | sin ponderar | — |
| κ para ordinales 1–5 | ponderado cuadrático | protocolo §15.3 |
| α de Krippendorff | por variable, métrica nominal u ordinal según tipo | no se mezcla binarias y ordinales en un α único |
| κ indefinido (p_e = 1) | NaN, marcado como degenerado | nunca se sustituye por 0 |
| Bootstrap | 2000 remuestreos de **documentos**, IC percentil | BCa disponible como opción |
| Faltantes | exclusión por pares; D4 vacío con `no_evaluable = 1` es estructural (§9.3) | listwise |
| Ancla del Δκ | A1, y también A2 con aviso si discrepan | — |
| Corrida LLM en Δκ | una fila por corrida (`per_run`) | voto mayoritario solo como secundario (es un ensemble) |
| Familia BH | todas las variables × modelos | por modelo |
| Equivalencia | no se ejecuta TOST salvo que se fije un margen | `contrast.equivalence_margin` |
| Fase de calibración | excluida del análisis (no independiente) | — |
| `llm_prior.row_offset` | −1 (confirmado por el investigador el 2026-09-17) | 0 = archivo tal cual |
| Subconjunto de trabajo | n = 160 (todo lo anotado por A1), estratificado por área FORD | `subset.n` |

Por qué el IC percentil y no BCa por defecto: es la opción más simple y la más
fácil de auditar; con 160–300 documentos la diferencia es pequeña y, si acaso,
el percentil es ligeramente más conservador en los extremos. BCa queda como
opción configurable.

## Qué encontró la auditoría (Fase 1)

Informe completo en [`outputs/audit_report.md`](outputs/audit_report.md).

1. **La primera entrega de A2 era una copia byte a byte de A1**: 0 de 1 920 celdas
   distintas y 159 de 160 observaciones libres idénticas. Se detuvo el estudio y se
   rehízo la anotación con un cuadernillo ciego. La segunda entrega, la que se analiza
   aquí, **sí es independiente**: A1 y A2 difieren en 147 de 1 898 celdas (7.7 %).
   De ese episodio salió `src/00c_receive_a2.py`, que comprueba la independencia de
   cualquier cuadernillo antes de aceptarlo.
2. **Cobertura 160 de 300** (53 %) en la fase principal; el análisis usa esos 160.
3. **8 tesis doctorales de 300**: el 86 % del corpus es de pregrado.
4. Tres versiones del archivo de A1 que difieren en 22 celdas de `D4_consistencia`;
   `config.yaml` fija cuál se usa.
5. El cuadernillo LLM previo tenía los valores **corridos una fila** (κ medio 0.01 tal
   cual, 0.59 realineado). Aun corregido no es admisible como corrida de Fase 2: se
   hizo por chat, sin temperature fija, sin semilla y sin repeticiones. Entra en las
   tablas solo como anotador exploratorio.
6. `D1_imryd_objetivo` tiene prevalencia 0.994 en humanos y 1.000 en los modelos: κ
   degenerado por construcción, de ahí que se reporten también AC1 y PABAK.

## Tiempo y coste por fase

| Fase | Tiempo | Coste API |
|---|---|---|
| 0 staging | < 5 s | 0 |
| 1 auditoría | ~35 s | 0 |
| 2 anotación LLM | Groq gpt-oss-20b ≈ 1 h; mistral-7b ≈ 5 h; qwen3-8b ≈ 5 h (160 × 3) | 0 USD (local + capa gratuita de Groq) |
| 3 concordancia | ~30 s (--quick) / ~5 min (2000 remuestreos) | 0 |
| 4 figuras | < 30 s | 0 |
| 5 error | < 10 s | 0 |

## Fase 2: anotación con LLMs

**Prompt.** Sistema = envoltorio de dos frases + el manual `PROTOCOLO_ANOTACION.md`
insertado literalmente (33 448 caracteres, huella `53c7ce15…`); usuario = título +
resumen, exactamente lo que vio el anotador humano. El manual incluye sus cuatro
ejemplos resueltos (§12); se verificó que ninguno pertenece al corpus GT ni al
corpus completo de 31 300, así que no hay fuga. `llm.prompt.strip_sections` permite
quitarlos para una condición zero-shot estricta.

**Blindaje.** `02_annotate_llm.py` no abre ningún archivo de anotaciones humanas
(solo `documents.csv` y `subset.csv`); `tests/test_llm_prompt.py` comprueba que
ninguna observación ni etiqueta de A1 aparece en ningún prompt.

**Salida.** JSON con esquema estricto: un campo por variable del manual, con los
mismos nombres; todas admiten `null` salvo `no_evaluable` (§9.3 y §10 del manual lo
exigen); `observaciones` va en último lugar para que se genere después de las
etiquetas. Hasta 3 reintentos por fallo de parseo, cada fallo guardado en el caché.

**Proveedores** (`llm.models` en `config.yaml`; claves solo por variables de entorno):

| provider | Qué cubre | temperature / seed |
|---|---|---|
| `ollama` | modelos de pesos abiertos en local (API nativa, para fijar `num_ctx`) | sí / sí; versión = digest |
| `openai_compatible` | Groq, Together, OpenRouter, Mistral, DeepSeek, OpenAI… | según endpoint |
| `google` | Gemini (`google-genai`) — sin verificar con clave real | sí / sí |
| `anthropic` | Claude (SDK oficial, salida estructurada, caché de prefijo) | **no / no** en Opus 5 y Sonnet 5 (`temperature` devuelve 400) |

**Corridas.** `llm.runs` define N corridas (temperature, seed). Cada llamada se cachea
en `data/interim/llm_cache/<modelo>/<sha256>.json`; relanzar no repite llamadas.

**Prueba de humo (2026-09-18, local, `mistral:latest` 7B Q4_K_M, RTX 2000 Ada 8 GB):**
3/3 llamadas válidas, ~12.8 k tokens de entrada reales por llamada (el tokenizador de
Mistral sobre español rinde ~1.5× la estimación por caracteres), ~30 s por llamada
en régimen ⇒ **≈ 4 h por modelo** para 160 docs × 3 corridas, coste 0.
**Las tres corridas (temperature 0, semillas 42/43/44) fueron idénticas etiqueta por
etiqueta**: en un decodificador determinista la autoconsistencia vale 1 por construcción.
Ver la decisión abierta en `config.yaml` → `llm.runs`.

## Fase 3: estadística de concordancia (`03_agreement.py`)

Para cada par y variable: κ (cuadrático en ordinales) con IC bootstrap a nivel de
documento, AC1/AC2 de Gwet, PABAK, α de Krippendorff, acuerdo bruto y matriz de
confusión (`outputs/tables/confusion/`). Pares: humano–humano, humano–LLM (cada
corrida), corridas del mismo modelo (autoconsistencia) y r1 entre modelos.
Contraste central Δκ = κ(ancla, LLM) − κ(A1, A2) con bootstrap **pareado**, p
bootstrap bilateral (inversión del IC percentil) y BH sobre la familia configurada;
anclas A1 y A2 con aviso si discrepan. **Δκ se omite mientras
`annotators.A2.independent` sea false.** `--quick` usa 200 remuestreos para pruebas.
Salidas: `table2_agreement_long`, `table2_kappa_matrix`, `table3_delta_kappa`,
`table_selfconsistency`, `table_krippendorff` (CSV + LaTeX) y `outputs/agreement_report.md`.

## Fase 4: figuras (`04_figures.py`)

Escala de grises, serif (Times New Roman → DejaVu Serif si falta), sin títulos,
PDF vectorial + PNG 300 dpi en `outputs/figures/`. Identidad de serie por forma de
marcador además del tono de gris; leyenda siempre que haya ≥ 2 series.
Fig. 1 forest plot de Δκ (requiere tabla 3). Fig. 2 matrices de confusión del mejor
modelo (mayor κ medio vs A1 en r1) frente al consenso humano (A1 = A2; solo A1 y así
rotulado mientras no haya A2). Fig. 3 κ y AC1 por variable ordenada por proporción
de la etiqueta mayoritaria: muestra dónde κ colapsa por prevalencia.

## Fase 5: análisis del error (`05_error_analysis.py`)

Casos donde el LLM discrepa y los dos humanos coincidían, con taxonomía preliminar
por reglas verificables (violación de reglas del manual §8.4/§6.5, desplazamiento
ordinal leve/severo, sobre-etiquetado con/sin palabra clave superficial,
sub-etiquetado, resúmenes largos) y 3–5 ejemplos citables por tipo. Sin A2 solo corre
con `--provisional` y todo sale con sufijo `_PROVISIONAL_A1only` (no apto para el
artículo). Columnas `reviewer_verdict` / `reviewer_notes` vacías para la revisión manual.

## Paquete para el segundo anotador

Los dos cuadernillos ciegos — `Anotacion_calibracion_A2_CIEGO.xlsx` (30 resúmenes, el
paso previo de §13.2) y `Anotacion_subset160_A2_CIEGO.xlsx` (los 160 del análisis) —
**no se redistribuyen aquí**: llevan el título y el resumen completo de cada tesis, que
no son nuestros. Se regeneran con `python src/00b_select_subset.py` una vez recuperados
los textos por su handle, como se explica arriba. El manual que los acompaña sí está,
en `outputs/dataset_release/codebook/`.

Ambos se verificaron como ciegos antes de entregarlos: 0 etiquetas y 0 observaciones de
A1, y listas desplegables que impiden valores fuera del esquema.

Al recibirlos, `python src/00c_receive_a2.py <archivo.xlsx>` valida estructura,
completitud, dominio, reglas del protocolo y **independencia** (detecta copia exacta
u observaciones literalmente iguales a las de A1 — el fallo que ya ocurrió una vez).
Con `--install` lo coloca en `data/raw/` y recuerda el único cambio de `config.yaml`.

## Ollama en esta máquina: usar CUDA, no la iGPU

El servidor de Ollama que arranca solo elige **Vulkan sobre la gráfica integrada
Intel**, porque declara ~15 GiB de memoria compartida frente a los 8 GiB dedicados
de la RTX 2000 Ada. El resultado es ~23 tokens/s procesando el prompt y, bajo carga,
`ggml_vulkan: device lost on Vulkan0` → el runner muere y la llamada devuelve
`HTTP 500 ... connection forcibly closed`. Reducir `num_ctx` no lo arregla: falla
igual a 16 384 y a 20 000.

La Fase 2 levanta por eso un servidor aparte, sin Vulkan, que sí usa CUDA:

```powershell
$env:OLLAMA_VULKAN = '0'
$env:OLLAMA_HOST   = '127.0.0.1:11435'
Start-Process "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve -WindowStyle Hidden
```

`config.yaml` apunta los modelos locales a `http://127.0.0.1:11435`. Comprobación:
el log debe decir `load_tensors: CUDA0 model buffer size = ...`, y `nvidia-smi` debe
mostrar la memoria ocupada. En CUDA, el documento que hacía caer a la iGPU se anota
en 64 s con la caché fría.

`num_ctx: 16384` cabe el prompt más largo observado (13 265 tokens) más 1 024 de
salida, y la caché KV entra en los 8 GB reales. Si alguna vez un prompt no cupiera,
el proveedor **falla ruidosamente**: Ollama truncaría el manual en silencio y la
anotación sería inválida sin que nada lo indicase.

Arreglo permanente, si prefieres no usar un servidor aparte: `setx OLLAMA_VULKAN 0`
y reiniciar la aplicación de Ollama.

### Velocidad: forzar todas las capas a la GPU

Con CUDA ya activo, la generación seguía a **8 tokens/s** porque Ollama reserva un
margen conservador y dejaba 2 de las 33 capas en la CPU; cada token generado tenía
que cruzar a la CPU y volver, y eso se comía el 97 % del tiempo por llamada.

Dos medidas, medidas una a una sobre `mistral:latest`:

| Situación | tokens/s | s por llamada |
|---|---:|---:|
| Vulkan, iGPU Intel | ~8, con caídas del driver | 24 (o fallo) |
| CUDA, 31/33 capas, escritorio ocupando 1.1 GB de VRAM | 8 | 24 |
| CUDA, 31/33 capas, navegadores cerrados | 20 | 10 |
| **CUDA, `num_gpu: 99` (33/33 capas)** | **32** | **6** |

`num_gpu: 99` en `config.yaml` fuerza la descarga completa. Requiere que el
escritorio no ocupe VRAM: con navegadores abiertos no cabe y el runner puede morir.
`qwen3:8b` también entra (31 tokens/s, 7.7 s por llamada).

Esto reduce la Fase 2 de ~8 h a ~1 h 45 min para los dos modelos locales.

### Consistencia de la condición de cómputo

El caché de `mistral-7b` llegó a mezclar tres condiciones (iGPU/Vulkan, CUDA con
descarga parcial, CUDA completa). Como el backend de cómputo puede cambiar el
redondeo en coma flotante y, con temperature 0, llegar a alterar algún token, ese
caché se apartó a `data/interim/_cache_condiciones_mezcladas/` (no se borró) y las
480 llamadas se rehicieron bajo una sola condición.

## Fase 6: empaquetado del dataset (`06_package_release.py`)

Genera `outputs/dataset_release/` para Zenodo: anotaciones en formato largo,
metadatos por documento, observaciones libres, el manual literal, diccionario de
datos, README con licencia CC-BY-4.0 y cita sugerida, y `CHECKSUMS.sha256`.

Dos comprobaciones **bloquean** el empaquetado: un escaneo de identificadores
personales (correos, DNI, códigos de estudiante, teléfonos, ORCID) sobre todos los
campos publicados, y la ausencia de título y texto del resumen. Nada se redacta
automáticamente: si algo aparece, se reporta en `outputs/pii_scan.csv` y se aborta.

**Los textos de los resúmenes no se redistribuyen.** Se cosecharon por OAI-PMH de
cuatro repositorios institucionales públicos y su copyright es de sus autores e
instituciones; el estudio no tiene derecho a relicenciarlos bajo CC-BY-4.0. Se
publica el `handle` persistente de cada registro, que permite recuperar el texto
exacto en la fuente y reproducir el análisis. `release.include_text: true` lo
invierte, pero solo debe activarse con permiso explícito.

## Pendiente

- Sustituir el DOI de Zenodo en `CITATION.cff` y en `release.citation` de
  `config.yaml` cuando el depósito esté publicado.

## Licencia

El código está bajo **MIT** (`LICENSE`). Las anotaciones, las justificaciones de los
anotadores, los metadatos por documento y el manual de codificación están bajo
**CC BY 4.0** (`LICENSE-DATA`). Los textos y títulos de las tesis no se redistribuyen
ni se licencian aquí: se cosecharon por OAI-PMH de repositorios institucionales
públicos y su copyright pertenece a sus autores e instituciones.
