# Human–LLM agreement on the structural quality of thesis abstracts — annotation dataset

Released 2026-09-18. Version 1.0.0.

## What this is

Independent annotations of 160 Spanish-language thesis abstracts by two human
annotators and by several open-weight language models, using a single coding
protocol with 12 variables (10 binary, 2 ordinal 1–5) over four dimensions:
IMRaD adherence, organisational coherence, component completeness and
methodological consistency.

The dataset supports the question the study asks: *is the disagreement between a
language model and a human annotator distinguishable from the disagreement that
already exists between two human annotators, and in which variables does that
equivalence break?*

## Files

| File | Rows | Description |
|---|---|---|
| `annotations.csv` | 22899 | Long format: one row per (document, annotator, variable). |
| `documents.csv` | 160 | Document-level metadata. |
| `annotator_notes.csv` | — | Free-text justifications written during annotation. |
| `codebook/PROTOCOLO_ANOTACION.md` | — | The coding manual, verbatim, in Spanish. |
| `data_dictionary.csv` | — | One row per field. |
| `CHECKSUMS.sha256` | — | Integrity of every file above. |

## What is NOT included, and why

**Abstract texts and thesis titles are not redistributed.** They were harvested via
OAI-PMH from four public institutional repositories in Puno, Peru, and their
copyright belongs to the respective authors and institutions; this dataset does not
hold the rights to relicense them. `documents.csv` carries the persistent `handle`
of each record, so anyone can retrieve the exact text from the source repository
and reproduce the analysis.

Annotators are identified only as A1 and A2. Free-text notes were screened for
e-mail addresses, national identity numbers, student codes, phone numbers and
ORCIDs; the scan is reported in the study repository.

## Coding scheme

See `codebook/`. In brief, for each abstract:

| Variable | Type | Levels |
|---|---|---|
| `D1_imryd_objetivo` | binary | [0, 1] |
| `D1_imryd_metodologia` | binary | [0, 1] |
| `D1_imryd_resultados` | binary | [0, 1] |
| `D1_imryd_conclusiones` | binary | [0, 1] |
| `D1_orden_logico` | binary | [0, 1] |
| `D2_coherencia` | ordinal | [1, 2, 3, 4, 5] |
| `D3_contextualizacion` | binary | [0, 1] |
| `D3_metodo_detallado` | binary | [0, 1] |
| `D3_resultados_concretos` | binary | [0, 1] |
| `D3_conclusion_responde` | binary | [0, 1] |
| `D4_consistencia` | ordinal | [1, 2, 3, 4, 5] |
| `no_evaluable` | binary | [0, 1] |

Two rules of the protocol create structural blanks that are **not** missing data:
§9.3 leaves `D4_consistencia` empty when `no_evaluable = 1`, and §10 leaves every
field empty when the text is not an abstract at all.

## Annotators and models

Human annotators: A1, A2. Both applied the same protocol
independently; the second annotator worked from a blinded workbook containing no
labels or notes from the first.

| Name | Exact model id | Provider | Call dates |
|---|---|---|---|
| mistral-7b | `mistral:latest` | ollama | 2026-09-18 |
| qwen3-8b | `qwen3:8b` | ollama | 2026-09-18 |
| gpt-oss-20b | `openai/gpt-oss-20b` | openai_compatible | 2026-09-18 |

The exact model version and the date of the calls are part of the method: models
change over time and results are not reproducible without them.

## Licence

Annotations, notes, metadata and the coding protocol: **CC BY 4.0**
(https://creativecommons.org/licenses/by/4.0/). Attribution as below. The abstract
texts are not part of this release and remain under their original terms.

## Suggested citation

> <AUTORES> (2026). Human-LLM agreement on the structural quality of thesis abstracts [Data set]. Zenodo. https://doi.org/<DOI>

## Reproducing the analysis

The full pipeline — audit, LLM annotation, agreement statistics, figures and error
analysis — is in the study repository, with pinned dependency versions and a fixed
random seed (42). Bootstrap confidence intervals resample **documents**, not
individual annotations.
