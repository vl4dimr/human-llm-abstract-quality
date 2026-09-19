# Informe de concordancia (Fase 3)

Generado: 2026-09-18T21:46:39 · universo: 160 documentos · bootstrap: 2000 remuestreos a nivel de documento, IC percentil 95 %, semilla 42

Anotadores humanos: ['A1', 'A2'] (A2 independiente: **True**). Modelos: {"gpt-oss-20b": ["gpt-oss-20b#r1", "gpt-oss-20b#r2", "gpt-oss-20b#r3"], "mistral-7b": ["mistral-7b#r1", "mistral-7b#r2", "mistral-7b#r3"], "qwen3-8b": ["qwen3-8b#r1", "qwen3-8b#r2", "qwen3-8b#r3"]}. Exploratorio: ['LLM_prior'].

Cobertura (docs con etiqueta en D1_imryd_objetivo): gpt-oss-20b#r1=159, gpt-oss-20b#r2=160, gpt-oss-20b#r3=159, mistral-7b#r1=160, mistral-7b#r2=160, mistral-7b#r3=160, qwen3-8b#r1=160, qwen3-8b#r2=160, qwen3-8b#r3=160, LLM_prior=157

## 1. Todos contra todos: 36 pares x 12 variables

| type             | pair                             | D1_imryd_objetivo   | D1_imryd_metodologia   | D1_imryd_resultados   | D1_imryd_conclusiones   | D1_orden_logico     | D2_coherencia     | D3_contextualizacion   | D3_metodo_detallado   | D3_resultados_concretos   | D3_conclusion_responde   | D4_consistencia     | no_evaluable      |
|:-----------------|:---------------------------------|:--------------------|:-----------------------|:----------------------|:------------------------|:--------------------|:------------------|:-----------------------|:----------------------|:--------------------------|:-------------------------|:--------------------|:------------------|
| human-human      | A1 vs A2                         | 1.00 [1.00, 1.00]   | 0.83 [0.65, 0.97]      | 0.92 [0.82, 1.00]     | 0.88 [0.79, 0.95]       | 0.70 [0.29, 0.94]   | 0.77 [0.69, 0.84] | 0.70 [0.44, 0.89]      | 0.70 [0.55, 0.83]     | 0.97 [0.92, 1.00]         | 0.84 [0.74, 0.92]        | 0.75 [0.67, 0.81]   | 1.00 [1.00, 1.00] |
| human-llm        | A1 vs LLM_prior                  | 0.00 [0.00, 0.00]   | 0.89 [0.70, 1.00]      | 0.84 [0.70, 0.95]     | 0.78 [0.67, 0.88]       | 0.25 [-0.04, 0.52]  | 0.60 [0.52, 0.68] | 0.09 [0.02, 0.17]      | 0.74 [0.59, 0.86]     | 0.86 [0.76, 0.95]         | 0.78 [0.67, 0.87]        | 0.28 [0.19, 0.37]   | 0.92 [0.77, 1.00] |
| human-llm        | A1 vs gpt-oss-20b#r1             | 1.00 [1.00, 1.00]   | 0.89 [0.69, 1.00]      | 0.85 [0.69, 0.97]     | 0.72 [0.59, 0.83]       | 0.21 [-0.05, 0.49]  | 0.15 [0.10, 0.20] | 0.13 [0.04, 0.23]      | 0.54 [0.36, 0.71]     | 0.80 [0.68, 0.90]         | 0.70 [0.58, 0.81]        | 0.03 [-0.02, 0.08]  | 0.85 [0.61, 1.00] |
| human-llm        | A1 vs gpt-oss-20b#r2             | 1.00 [1.00, 1.00]   | 0.95 [0.81, 1.00]      | 0.94 [0.85, 1.00]     | 0.73 [0.60, 0.84]       | 0.23 [-0.04, 0.53]  | 0.12 [0.07, 0.18] | 0.12 [0.03, 0.21]      | 0.43 [0.25, 0.61]     | 0.79 [0.66, 0.89]         | 0.70 [0.58, 0.81]        | 0.01 [-0.04, 0.05]  | 0.85 [0.61, 1.00] |
| human-llm        | A1 vs gpt-oss-20b#r3             | 0.00 [0.00, 0.00]   | 0.79 [0.53, 0.96]      | 0.91 [0.79, 1.00]     | 0.71 [0.57, 0.83]       | 0.37 [-0.02, 0.66]  | 0.15 [0.09, 0.20] | 0.09 [0.01, 0.19]      | 0.51 [0.32, 0.67]     | 0.78 [0.66, 0.89]         | 0.73 [0.61, 0.84]        | 0.06 [0.02, 0.10]   | 0.80 [0.57, 0.96] |
| human-llm        | A1 vs mistral-7b#r1              | -0.01 [-0.03, 0.00] | 0.63 [0.40, 0.82]      | 0.71 [0.54, 0.85]     | 0.52 [0.36, 0.67]       | 0.06 [-0.08, 0.24]  | 0.23 [0.14, 0.32] | 0.01 [-0.02, 0.04]     | 0.50 [0.32, 0.65]     | 0.48 [0.32, 0.63]         | 0.43 [0.29, 0.57]        | 0.01 [-0.03, 0.04]  | 0.00 [0.00, 0.00] |
| human-llm        | A1 vs mistral-7b#r2              | -0.01 [-0.03, 0.00] | 0.19 [0.05, 0.34]      | 0.51 [0.35, 0.65]     | 0.38 [0.22, 0.54]       | -0.00 [-0.09, 0.10] | 0.30 [0.18, 0.41] | 0.04 [-0.03, 0.11]     | 0.43 [0.27, 0.57]     | 0.57 [0.41, 0.69]         | 0.34 [0.19, 0.49]        | 0.05 [0.00, 0.09]   | 0.00 [0.00, 0.00] |
| human-llm        | A1 vs mistral-7b#r3              | -0.01 [-0.03, 0.00] | 0.63 [0.40, 0.82]      | 0.78 [0.62, 0.90]     | 0.50 [0.33, 0.64]       | 0.00 [-0.09, 0.17]  | 0.23 [0.15, 0.32] | 0.01 [-0.02, 0.04]     | 0.49 [0.30, 0.65]     | 0.52 [0.35, 0.67]         | 0.41 [0.27, 0.55]        | 0.02 [-0.02, 0.06]  | 0.00 [0.00, 0.00] |
| human-llm        | A1 vs qwen3-8b#r1                | -0.01 [-0.02, 0.00] | 0.83 [0.58, 1.00]      | 0.89 [0.75, 0.98]     | 0.50 [0.34, 0.63]       | 0.06 [-0.07, 0.28]  | 0.22 [0.14, 0.31] | 0.00 [0.00, 0.01]      | 0.36 [0.17, 0.52]     | 0.48 [0.31, 0.63]         | 0.45 [0.31, 0.58]        | 0.07 [-0.03, 0.17]  | 0.00 [0.00, 0.00] |
| human-llm        | A1 vs qwen3-8b#r2                | -0.01 [-0.02, 0.00] | 0.83 [0.58, 1.00]      | 0.89 [0.75, 0.98]     | 0.47 [0.32, 0.62]       | 0.06 [-0.07, 0.28]  | 0.24 [0.14, 0.34] | 0.01 [0.00, 0.02]      | 0.36 [0.17, 0.52]     | 0.48 [0.31, 0.63]         | 0.43 [0.29, 0.56]        | 0.11 [0.00, 0.20]   | 0.00 [0.00, 0.00] |
| human-llm        | A1 vs qwen3-8b#r3                | -0.01 [-0.02, 0.00] | 0.83 [0.58, 1.00]      | 0.89 [0.75, 0.98]     | 0.50 [0.34, 0.64]       | 0.07 [-0.07, 0.30]  | 0.21 [0.13, 0.30] | 0.00 [0.00, 0.01]      | 0.42 [0.23, 0.58]     | 0.51 [0.35, 0.66]         | 0.45 [0.31, 0.58]        | 0.08 [-0.02, 0.18]  | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs LLM_prior                  | 0.00 [0.00, 0.00]   | 0.82 [0.60, 0.97]      | 0.77 [0.62, 0.91]     | 0.77 [0.66, 0.87]       | 0.30 [-0.03, 0.57]  | 0.63 [0.54, 0.70] | 0.07 [0.00, 0.15]      | 0.79 [0.65, 0.91]     | 0.86 [0.75, 0.94]         | 0.74 [0.62, 0.84]        | 0.27 [0.18, 0.35]   | 0.92 [0.77, 1.00] |
| human-llm        | A2 vs gpt-oss-20b#r1             | 1.00 [1.00, 1.00]   | 0.82 [0.61, 1.00]      | 0.77 [0.60, 0.91]     | 0.66 [0.53, 0.79]       | 0.25 [-0.04, 0.56]  | 0.20 [0.15, 0.25] | 0.07 [-0.01, 0.17]     | 0.58 [0.38, 0.76]     | 0.83 [0.71, 0.92]         | 0.68 [0.56, 0.80]        | 0.04 [0.00, 0.09]   | 0.85 [0.61, 1.00] |
| human-llm        | A2 vs gpt-oss-20b#r2             | 1.00 [1.00, 1.00]   | 0.78 [0.56, 0.95]      | 0.87 [0.73, 0.97]     | 0.73 [0.61, 0.84]       | 0.28 [-0.03, 0.60]  | 0.16 [0.10, 0.22] | 0.08 [-0.01, 0.17]     | 0.51 [0.31, 0.70]     | 0.78 [0.66, 0.89]         | 0.71 [0.59, 0.81]        | 0.03 [-0.01, 0.06]  | 0.85 [0.61, 1.00] |
| human-llm        | A2 vs gpt-oss-20b#r3             | 0.00 [0.00, 0.00]   | 0.73 [0.48, 0.91]      | 0.84 [0.68, 0.95]     | 0.71 [0.58, 0.83]       | 0.44 [-0.02, 0.76]  | 0.19 [0.13, 0.25] | 0.07 [-0.01, 0.15]     | 0.60 [0.40, 0.77]     | 0.77 [0.65, 0.89]         | 0.76 [0.65, 0.86]        | 0.05 [0.02, 0.09]   | 0.80 [0.57, 0.96] |
| human-llm        | A2 vs mistral-7b#r1              | -0.01 [-0.03, 0.00] | 0.67 [0.44, 0.84]      | 0.70 [0.54, 0.84]     | 0.43 [0.27, 0.58]       | 0.09 [-0.06, 0.26]  | 0.34 [0.24, 0.44] | 0.01 [-0.03, 0.03]     | 0.59 [0.40, 0.74]     | 0.51 [0.34, 0.65]         | 0.34 [0.20, 0.48]        | 0.00 [-0.03, 0.04]  | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs mistral-7b#r2              | -0.01 [-0.03, 0.00] | 0.18 [0.04, 0.33]      | 0.57 [0.42, 0.71]     | 0.33 [0.17, 0.50]       | 0.02 [-0.07, 0.13]  | 0.37 [0.24, 0.49] | 0.05 [-0.00, 0.11]     | 0.35 [0.20, 0.50]     | 0.59 [0.44, 0.72]         | 0.30 [0.16, 0.45]        | 0.04 [-0.01, 0.08]  | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs mistral-7b#r3              | -0.01 [-0.03, 0.00] | 0.67 [0.44, 0.84]      | 0.81 [0.67, 0.93]     | 0.40 [0.24, 0.55]       | 0.02 [-0.08, 0.19]  | 0.32 [0.22, 0.41] | 0.01 [-0.03, 0.03]     | 0.57 [0.38, 0.74]     | 0.54 [0.37, 0.69]         | 0.32 [0.18, 0.45]        | 0.00 [-0.03, 0.04]  | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs qwen3-8b#r1                | -0.01 [-0.02, 0.00] | 0.67 [0.41, 0.88]      | 0.81 [0.66, 0.93]     | 0.44 [0.28, 0.58]       | 0.08 [-0.06, 0.31]  | 0.35 [0.25, 0.44] | 0.00 [0.00, 0.01]      | 0.47 [0.26, 0.67]     | 0.51 [0.34, 0.66]         | 0.38 [0.24, 0.51]        | 0.12 [0.01, 0.22]   | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs qwen3-8b#r2                | -0.01 [-0.02, 0.00] | 0.67 [0.41, 0.88]      | 0.81 [0.66, 0.93]     | 0.42 [0.26, 0.56]       | 0.08 [-0.06, 0.31]  | 0.31 [0.19, 0.42] | 0.01 [0.00, 0.02]      | 0.47 [0.26, 0.67]     | 0.51 [0.34, 0.66]         | 0.36 [0.23, 0.50]        | 0.13 [0.02, 0.23]   | 0.00 [0.00, 0.00] |
| human-llm        | A2 vs qwen3-8b#r3                | -0.01 [-0.02, 0.00] | 0.67 [0.41, 0.88]      | 0.81 [0.66, 0.93]     | 0.44 [0.28, 0.58]       | 0.09 [-0.06, 0.34]  | 0.33 [0.22, 0.42] | 0.00 [0.00, 0.01]      | 0.49 [0.27, 0.69]     | 0.54 [0.37, 0.68]         | 0.38 [0.24, 0.51]        | 0.10 [-0.00, 0.20]  | 0.00 [0.00, 0.00] |
| llm-llm          | gpt-oss-20b#r1 vs LLM_prior      | 0.00 [0.00, 0.00]   | 0.89 [0.69, 1.00]      | 0.80 [0.65, 0.94]     | 0.76 [0.65, 0.86]       | 0.68 [0.37, 0.89]   | 0.18 [0.10, 0.25] | 0.70 [0.58, 0.80]      | 0.58 [0.38, 0.76]     | 0.82 [0.69, 0.92]         | 0.65 [0.52, 0.77]        | 0.22 [0.07, 0.36]   | 0.77 [0.52, 0.94] |
| llm-llm          | gpt-oss-20b#r1 vs mistral-7b#r1  | -0.01 [-0.03, 0.00] | 0.59 [0.33, 0.78]      | 0.61 [0.43, 0.77]     | 0.45 [0.29, 0.62]       | 0.40 [0.16, 0.61]   | 0.20 [0.12, 0.27] | 0.12 [0.02, 0.22]      | 0.53 [0.31, 0.70]     | 0.56 [0.39, 0.71]         | 0.38 [0.23, 0.53]        | -0.06 [-0.16, 0.06] | 0.00 [0.00, 0.00] |
| llm-llm          | gpt-oss-20b#r1 vs qwen3-8b#r1    | -0.01 [-0.02, 0.00] | 0.76 [0.48, 0.95]      | 0.72 [0.52, 0.88]     | 0.51 [0.34, 0.66]       | 0.83 [0.59, 1.00]   | 0.18 [0.09, 0.27] | 0.02 [0.00, 0.06]      | 0.72 [0.48, 0.89]     | 0.60 [0.44, 0.75]         | 0.42 [0.28, 0.56]        | 0.02 [-0.02, 0.07]  | 0.00 [0.00, 0.00] |
| llm-llm          | mistral-7b#r1 vs LLM_prior       | 0.00 [0.00, 0.00]   | 0.61 [0.34, 0.81]      | 0.62 [0.44, 0.77]     | 0.38 [0.24, 0.52]       | 0.50 [0.25, 0.70]   | 0.22 [0.12, 0.34] | 0.12 [0.00, 0.24]      | 0.52 [0.33, 0.69]     | 0.53 [0.35, 0.69]         | 0.35 [0.22, 0.49]        | -0.04 [-0.14, 0.06] | 0.00 [0.00, 0.00] |
| llm-llm          | mistral-7b#r1 vs qwen3-8b#r1     | -0.01 [-0.02, 0.00] | 0.59 [0.34, 0.78]      | 0.66 [0.48, 0.81]     | 0.61 [0.42, 0.78]       | 0.55 [0.33, 0.73]   | 0.44 [0.29, 0.57] | 0.15 [0.00, 0.36]      | 0.53 [0.31, 0.71]     | 0.62 [0.44, 0.78]         | 0.61 [0.42, 0.78]        | 0.11 [0.03, 0.18]   | n/d               |
| llm-llm          | qwen3-8b#r1 vs LLM_prior         | 0.00 [0.00, 0.00]   | 0.81 [0.53, 1.00]      | 0.73 [0.54, 0.87]     | 0.39 [0.25, 0.53]       | 0.54 [0.22, 0.78]   | 0.32 [0.22, 0.41] | 0.03 [0.00, 0.08]      | 0.39 [0.17, 0.60]     | 0.53 [0.35, 0.69]         | 0.37 [0.23, 0.50]        | 0.10 [-0.01, 0.20]  | 0.00 [0.00, 0.00] |
| self-consistency | gpt-oss-20b#r1 vs gpt-oss-20b#r2 | 1.00 [1.00, 1.00]   | 0.89 [0.70, 1.00]      | 0.85 [0.71, 0.96]     | 0.76 [0.63, 0.86]       | 0.74 [0.39, 0.94]   | 0.33 [0.15, 0.49] | 0.69 [0.57, 0.79]      | 0.80 [0.61, 0.94]     | 0.78 [0.65, 0.89]         | 0.71 [0.60, 0.83]        | 0.53 [0.22, 0.74]   | 0.88 [0.66, 1.00] |
| self-consistency | gpt-oss-20b#r1 vs gpt-oss-20b#r3 | 0.00 [0.00, 0.00]   | 0.79 [0.53, 0.96]      | 0.88 [0.75, 0.97]     | 0.74 [0.61, 0.85]       | 0.74 [0.41, 0.94]   | 0.46 [0.31, 0.59] | 0.62 [0.49, 0.74]      | 0.70 [0.48, 0.86]     | 0.70 [0.55, 0.83]         | 0.80 [0.69, 0.89]        | 0.36 [0.05, 0.59]   | 0.83 [0.59, 1.00] |
| self-consistency | gpt-oss-20b#r2 vs gpt-oss-20b#r3 | 0.00 [0.00, 0.00]   | 0.79 [0.53, 0.96]      | 0.91 [0.79, 1.00]     | 0.78 [0.66, 0.88]       | 0.70 [0.32, 0.94]   | 0.32 [0.16, 0.47] | 0.64 [0.52, 0.76]      | 0.71 [0.50, 0.87]     | 0.72 [0.59, 0.85]         | 0.80 [0.68, 0.89]        | 0.48 [0.13, 0.72]   | 0.72 [0.41, 0.92] |
| self-consistency | mistral-7b#r1 vs mistral-7b#r2   | 1.00 [1.00, 1.00]   | 0.05 [-0.09, 0.20]     | 0.50 [0.35, 0.65]     | 0.41 [0.22, 0.59]       | 0.07 [-0.07, 0.23]  | 0.46 [0.34, 0.57] | -0.09 [-0.20, 0.03]    | 0.33 [0.18, 0.47]     | 0.51 [0.36, 0.65]         | 0.41 [0.22, 0.59]        | 0.51 [0.36, 0.65]   | n/d               |
| self-consistency | mistral-7b#r1 vs mistral-7b#r3   | 1.00 [1.00, 1.00]   | 1.00 [1.00, 1.00]      | 0.89 [0.78, 0.98]     | 0.92 [0.82, 1.00]       | 0.81 [0.66, 0.93]   | 0.95 [0.89, 0.99] | 1.00 [1.00, 1.00]      | 0.86 [0.73, 0.96]     | 0.92 [0.83, 0.98]         | 0.92 [0.82, 1.00]        | 0.86 [0.70, 0.98]   | n/d               |
| self-consistency | mistral-7b#r2 vs mistral-7b#r3   | 1.00 [1.00, 1.00]   | 0.05 [-0.09, 0.20]     | 0.52 [0.36, 0.66]     | 0.38 [0.20, 0.56]       | 0.11 [-0.04, 0.27]  | 0.47 [0.35, 0.57] | -0.09 [-0.20, 0.03]    | 0.35 [0.20, 0.49]     | 0.51 [0.36, 0.65]         | 0.38 [0.20, 0.56]        | 0.49 [0.30, 0.65]   | n/d               |
| self-consistency | qwen3-8b#r1 vs qwen3-8b#r2       | 1.00 [1.00, 1.00]   | 1.00 [1.00, 1.00]      | 1.00 [1.00, 1.00]     | 0.97 [0.91, 1.00]       | 0.90 [0.73, 1.00]   | 0.36 [0.18, 0.51] | 0.39 [0.00, 0.74]      | 1.00 [1.00, 1.00]     | 1.00 [1.00, 1.00]         | 0.97 [0.91, 1.00]        | 0.86 [0.76, 0.93]   | n/d               |
| self-consistency | qwen3-8b#r1 vs qwen3-8b#r3       | 1.00 [1.00, 1.00]   | 1.00 [1.00, 1.00]      | 1.00 [1.00, 1.00]     | 0.95 [0.86, 1.00]       | 0.95 [0.81, 1.00]   | 0.78 [0.65, 0.88] | 1.00 [1.00, 1.00]      | 0.92 [0.77, 1.00]     | 0.92 [0.82, 1.00]         | 0.95 [0.86, 1.00]        | 0.96 [0.92, 0.99]   | n/d               |
| self-consistency | qwen3-8b#r2 vs qwen3-8b#r3       | 1.00 [1.00, 1.00]   | 1.00 [1.00, 1.00]      | 1.00 [1.00, 1.00]     | 0.97 [0.91, 1.00]       | 0.95 [0.82, 1.00]   | 0.49 [0.33, 0.62] | 0.39 [0.00, 0.74]      | 0.92 [0.77, 1.00]     | 0.92 [0.82, 1.00]         | 0.97 [0.91, 1.00]        | 0.85 [0.75, 0.92]   | n/d               |

## 2. Autoconsistencia intra-modelo (techo de rendimiento)

**gpt-oss-20B** — κ entre corridas, por par:

| variable                |   r1-r2 (deterministic/sampled) |   r1-r3 (deterministic/sampled) |   r2-r3 (sampled/sampled) |
|:------------------------|--------------------------------:|--------------------------------:|--------------------------:|
| D1_imryd_objetivo       |                           1.000 |                           0.000 |                     0.000 |
| D1_imryd_metodologia    |                           0.893 |                           0.787 |                     0.787 |
| D1_imryd_resultados     |                           0.847 |                           0.880 |                     0.912 |
| D1_imryd_conclusiones   |                           0.756 |                           0.739 |                     0.777 |
| D1_orden_logico         |                           0.737 |                           0.737 |                     0.701 |
| D2_coherencia           |                           0.328 |                           0.459 |                     0.317 |
| D3_contextualizacion    |                           0.685 |                           0.622 |                     0.635 |
| D3_metodo_detallado     |                           0.802 |                           0.696 |                     0.711 |
| D3_resultados_concretos |                           0.777 |                           0.698 |                     0.724 |
| D3_conclusion_responde  |                           0.714 |                           0.800 |                     0.796 |
| D4_consistencia         |                           0.526 |                           0.360 |                     0.485 |
| no_evaluable            |                           0.882 |                           0.832 |                     0.720 |

**Mistral 7B** — κ entre corridas, por par:

| variable                |   r1-r2 (deterministic/sampled) |   r1-r3 (deterministic/sampled) |   r2-r3 (sampled/sampled) |
|:------------------------|--------------------------------:|--------------------------------:|--------------------------:|
| D1_imryd_objetivo       |                           1.000 |                           1.000 |                     1.000 |
| D1_imryd_metodologia    |                           0.046 |                           1.000 |                     0.046 |
| D1_imryd_resultados     |                           0.505 |                           0.890 |                     0.518 |
| D1_imryd_conclusiones   |                           0.410 |                           0.922 |                     0.381 |
| D1_orden_logico         |                           0.074 |                           0.812 |                     0.107 |
| D2_coherencia           |                           0.459 |                           0.945 |                     0.468 |
| D3_contextualizacion    |                          -0.088 |                           1.000 |                    -0.088 |
| D3_metodo_detallado     |                           0.327 |                           0.858 |                     0.353 |
| D3_resultados_concretos |                           0.513 |                           0.916 |                     0.513 |
| D3_conclusion_responde  |                           0.410 |                           0.922 |                     0.381 |
| D4_consistencia         |                           0.513 |                           0.857 |                     0.486 |
| no_evaluable            |                         nan     |                         nan     |                   nan     |

**Qwen3 8B** — κ entre corridas, por par:

| variable                |   r1-r2 (deterministic/sampled) |   r1-r3 (deterministic/sampled) |   r2-r3 (sampled/sampled) |
|:------------------------|--------------------------------:|--------------------------------:|--------------------------:|
| D1_imryd_objetivo       |                           1.000 |                           1.000 |                     1.000 |
| D1_imryd_metodologia    |                           1.000 |                           1.000 |                     1.000 |
| D1_imryd_resultados     |                           1.000 |                           1.000 |                     1.000 |
| D1_imryd_conclusiones   |                           0.973 |                           0.947 |                     0.973 |
| D1_orden_logico         |                           0.902 |                           0.949 |                     0.949 |
| D2_coherencia           |                           0.360 |                           0.777 |                     0.488 |
| D3_contextualizacion    |                           0.388 |                           1.000 |                     0.388 |
| D3_metodo_detallado     |                           1.000 |                           0.916 |                     0.916 |
| D3_resultados_concretos |                           1.000 |                           0.922 |                     0.922 |
| D3_conclusion_responde  |                           0.973 |                           0.947 |                     0.973 |
| D4_consistencia         |                           0.856 |                           0.961 |                     0.852 |
| no_evaluable            |                         nan     |                         nan     |                   nan     |

> Un modelo cuya autoconsistencia en una variable es baja no puede concordar con nadie en esa variable: ese kappa es el techo del kappa humano-LLM. El par de corridas muestreadas (r2-r3) es el que mide la inestabilidad propia del modelo; los pares con r1 mezclan decodificacion determinista y muestreada.

## 3. Contraste central: delta-kappa = kappa(ancla, LLM) - kappa(A1, A2)

| llm            | variable                |   delta |   delta_lo |   delta_hi |   p_boot |   p_adj_bh | verdict                       |
|:---------------|:------------------------|--------:|-----------:|-----------:|---------:|-----------:|:------------------------------|
| gpt-oss-20b#r1 | D1_imryd_objetivo       |   0.000 |      0.000 |      0.000 |    1.000 |      1.000 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r1 | D1_imryd_metodologia    |   0.060 |     -0.123 |      0.254 |    0.563 |      0.601 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r1 | D1_imryd_resultados     |  -0.075 |     -0.249 |      0.078 |    0.328 |      0.356 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r1 | D1_imryd_conclusiones   |  -0.164 |     -0.302 |     -0.029 |    0.018 |      0.025 | LLM peor que humano           |
| gpt-oss-20b#r1 | D1_orden_logico         |  -0.491 |     -0.826 |     -0.133 |    0.002 |      0.003 | LLM peor que humano           |
| gpt-oss-20b#r1 | D2_coherencia           |  -0.618 |     -0.680 |     -0.551 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r1 | D3_contextualizacion    |  -0.568 |     -0.786 |     -0.294 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r1 | D3_metodo_detallado     |  -0.166 |     -0.342 |      0.009 |    0.070 |      0.088 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r1 | D3_resultados_concretos |  -0.172 |     -0.285 |     -0.080 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r1 | D3_conclusion_responde  |  -0.133 |     -0.264 |     -0.009 |    0.041 |      0.053 | LLM peor que humano           |
| gpt-oss-20b#r1 | D4_consistencia         |  -0.720 |     -0.804 |     -0.630 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r1 | no_evaluable            |  -0.153 |     -0.387 |      0.000 |    0.102 |      0.121 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r2 | D1_imryd_objetivo       |   0.000 |      0.000 |      0.000 |    1.000 |      1.000 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r2 | D1_imryd_metodologia    |   0.116 |     -0.078 |      0.345 |    0.276 |      0.310 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r2 | D1_imryd_resultados     |   0.020 |     -0.099 |      0.145 |    0.842 |      0.871 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r2 | D1_imryd_conclusiones   |  -0.149 |     -0.277 |     -0.032 |    0.011 |      0.016 | LLM peor que humano           |
| gpt-oss-20b#r2 | D1_orden_logico         |  -0.471 |     -0.820 |     -0.109 |    0.007 |      0.011 | LLM peor que humano           |
| gpt-oss-20b#r2 | D2_coherencia           |  -0.648 |     -0.716 |     -0.576 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r2 | D3_contextualizacion    |  -0.578 |     -0.780 |     -0.326 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r2 | D3_metodo_detallado     |  -0.272 |     -0.448 |     -0.088 |    0.006 |      0.010 | LLM peor que humano           |
| gpt-oss-20b#r2 | D3_resultados_concretos |  -0.179 |     -0.306 |     -0.076 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r2 | D3_conclusion_responde  |  -0.134 |     -0.262 |     -0.012 |    0.029 |      0.040 | LLM peor que humano           |
| gpt-oss-20b#r2 | D4_consistencia         |  -0.741 |     -0.827 |     -0.656 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r2 | no_evaluable            |  -0.153 |     -0.392 |      0.000 |    0.095 |      0.115 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r3 | D1_imryd_objetivo       |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r3 | D1_imryd_metodologia    |  -0.046 |     -0.306 |      0.168 |    0.660 |      0.695 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r3 | D1_imryd_resultados     |  -0.010 |     -0.145 |      0.119 |    0.824 |      0.856 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r3 | D1_imryd_conclusiones   |  -0.170 |     -0.306 |     -0.048 |    0.005 |      0.008 | LLM peor que humano           |
| gpt-oss-20b#r3 | D1_orden_logico         |  -0.331 |     -0.653 |     -0.012 |    0.027 |      0.037 | LLM peor que humano           |
| gpt-oss-20b#r3 | D2_coherencia           |  -0.622 |     -0.689 |     -0.548 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r3 | D3_contextualizacion    |  -0.601 |     -0.807 |     -0.353 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r3 | D3_metodo_detallado     |  -0.199 |     -0.368 |     -0.030 |    0.020 |      0.028 | LLM peor que humano           |
| gpt-oss-20b#r3 | D3_resultados_concretos |  -0.190 |     -0.318 |     -0.076 |    0.001 |      0.002 | LLM peor que humano           |
| gpt-oss-20b#r3 | D3_conclusion_responde  |  -0.109 |     -0.224 |      0.002 |    0.054 |      0.069 | indistinguible (IC incluye 0) |
| gpt-oss-20b#r3 | D4_consistencia         |  -0.691 |     -0.756 |     -0.615 |    0.000 |      0.000 | LLM peor que humano           |
| gpt-oss-20b#r3 | no_evaluable            |  -0.195 |     -0.431 |     -0.040 |    0.031 |      0.042 | LLM peor que humano           |
| mistral-7b#r1  | D1_imryd_objetivo       |  -1.010 |     -1.027 |     -1.006 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D1_imryd_metodologia    |  -0.198 |     -0.417 |     -0.010 |    0.048 |      0.061 | LLM peor que humano           |
| mistral-7b#r1  | D1_imryd_resultados     |  -0.216 |     -0.391 |     -0.065 |    0.006 |      0.010 | LLM peor que humano           |
| mistral-7b#r1  | D1_imryd_conclusiones   |  -0.363 |     -0.535 |     -0.181 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D1_orden_logico         |  -0.637 |     -0.887 |     -0.295 |    0.001 |      0.002 | LLM peor que humano           |
| mistral-7b#r1  | D2_coherencia           |  -0.543 |     -0.627 |     -0.456 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D3_contextualizacion    |  -0.685 |     -0.873 |     -0.426 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D3_metodo_detallado     |  -0.208 |     -0.374 |     -0.051 |    0.013 |      0.019 | LLM peor que humano           |
| mistral-7b#r1  | D3_resultados_concretos |  -0.487 |     -0.650 |     -0.339 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D3_conclusion_responde  |  -0.403 |     -0.571 |     -0.222 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | D4_consistencia         |  -0.745 |     -0.815 |     -0.662 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r1  | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D1_imryd_objetivo       |  -1.010 |     -1.027 |     -1.006 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D1_imryd_metodologia    |  -0.643 |     -0.820 |     -0.454 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D1_imryd_resultados     |  -0.415 |     -0.560 |     -0.278 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D1_imryd_conclusiones   |  -0.496 |     -0.667 |     -0.318 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D1_orden_logico         |  -0.706 |     -0.977 |     -0.283 |    0.012 |      0.018 | LLM peor que humano           |
| mistral-7b#r2  | D2_coherencia           |  -0.470 |     -0.572 |     -0.362 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D3_contextualizacion    |  -0.658 |     -0.839 |     -0.419 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D3_metodo_detallado     |  -0.274 |     -0.451 |     -0.091 |    0.007 |      0.011 | LLM peor que humano           |
| mistral-7b#r2  | D3_resultados_concretos |  -0.401 |     -0.554 |     -0.274 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D3_conclusion_responde  |  -0.499 |     -0.668 |     -0.329 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | D4_consistencia         |  -0.705 |     -0.779 |     -0.617 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r2  | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D1_imryd_objetivo       |  -1.010 |     -1.027 |     -1.006 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D1_imryd_metodologia    |  -0.198 |     -0.417 |     -0.010 |    0.048 |      0.061 | LLM peor que humano           |
| mistral-7b#r3  | D1_imryd_resultados     |  -0.147 |     -0.292 |     -0.026 |    0.017 |      0.024 | LLM peor que humano           |
| mistral-7b#r3  | D1_imryd_conclusiones   |  -0.384 |     -0.568 |     -0.211 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D1_orden_logico         |  -0.698 |     -0.953 |     -0.315 |    0.001 |      0.002 | LLM peor que humano           |
| mistral-7b#r3  | D2_coherencia           |  -0.535 |     -0.617 |     -0.449 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D3_contextualizacion    |  -0.685 |     -0.873 |     -0.426 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D3_metodo_detallado     |  -0.219 |     -0.385 |     -0.056 |    0.013 |      0.019 | LLM peor que humano           |
| mistral-7b#r3  | D3_resultados_concretos |  -0.451 |     -0.617 |     -0.311 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D3_conclusion_responde  |  -0.422 |     -0.595 |     -0.243 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | D4_consistencia         |  -0.732 |     -0.804 |     -0.644 |    0.000 |      0.000 | LLM peor que humano           |
| mistral-7b#r3  | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D1_imryd_objetivo       |  -1.006 |     -1.017 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D1_imryd_metodologia    |  -0.000 |     -0.288 |      0.262 |    0.956 |      0.972 | indistinguible (IC incluye 0) |
| qwen3-8b#r1    | D1_imryd_resultados     |  -0.037 |     -0.202 |      0.102 |    0.566 |      0.601 | indistinguible (IC incluye 0) |
| qwen3-8b#r1    | D1_imryd_conclusiones   |  -0.384 |     -0.553 |     -0.216 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D1_orden_logico         |  -0.643 |     -0.925 |     -0.268 |    0.001 |      0.002 | LLM peor que humano           |
| qwen3-8b#r1    | D2_coherencia           |  -0.547 |     -0.629 |     -0.463 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D3_contextualizacion    |  -0.694 |     -0.882 |     -0.435 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D3_metodo_detallado     |  -0.347 |     -0.528 |     -0.177 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D3_resultados_concretos |  -0.485 |     -0.649 |     -0.339 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D3_conclusion_responde  |  -0.389 |     -0.542 |     -0.228 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | D4_consistencia         |  -0.678 |     -0.798 |     -0.555 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r1    | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D1_imryd_objetivo       |  -1.006 |     -1.017 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D1_imryd_metodologia    |  -0.000 |     -0.288 |      0.262 |    0.956 |      0.972 | indistinguible (IC incluye 0) |
| qwen3-8b#r2    | D1_imryd_resultados     |  -0.037 |     -0.202 |      0.102 |    0.566 |      0.601 | indistinguible (IC incluye 0) |
| qwen3-8b#r2    | D1_imryd_conclusiones   |  -0.406 |     -0.573 |     -0.234 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D1_orden_logico         |  -0.643 |     -0.926 |     -0.267 |    0.001 |      0.002 | LLM peor que humano           |
| qwen3-8b#r2    | D2_coherencia           |  -0.529 |     -0.624 |     -0.427 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D3_contextualizacion    |  -0.687 |     -0.875 |     -0.430 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D3_metodo_detallado     |  -0.347 |     -0.528 |     -0.177 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D3_resultados_concretos |  -0.485 |     -0.649 |     -0.339 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D3_conclusion_responde  |  -0.408 |     -0.560 |     -0.248 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | D4_consistencia         |  -0.646 |     -0.759 |     -0.530 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r2    | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D1_imryd_objetivo       |  -1.006 |     -1.017 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D1_imryd_metodologia    |  -0.000 |     -0.288 |      0.262 |    0.956 |      0.972 | indistinguible (IC incluye 0) |
| qwen3-8b#r3    | D1_imryd_resultados     |  -0.037 |     -0.202 |      0.102 |    0.566 |      0.601 | indistinguible (IC incluye 0) |
| qwen3-8b#r3    | D1_imryd_conclusiones   |  -0.384 |     -0.554 |     -0.216 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D1_orden_logico         |  -0.633 |     -0.923 |     -0.252 |    0.001 |      0.002 | LLM peor que humano           |
| qwen3-8b#r3    | D2_coherencia           |  -0.558 |     -0.642 |     -0.470 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D3_contextualizacion    |  -0.694 |     -0.882 |     -0.435 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D3_metodo_detallado     |  -0.284 |     -0.473 |     -0.107 |    0.003 |      0.005 | LLM peor que humano           |
| qwen3-8b#r3    | D3_resultados_concretos |  -0.453 |     -0.616 |     -0.310 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D3_conclusion_responde  |  -0.389 |     -0.543 |     -0.225 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | D4_consistencia         |  -0.672 |     -0.794 |     -0.552 |    0.000 |      0.000 | LLM peor que humano           |
| qwen3-8b#r3    | no_evaluable            |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| LLM_prior      | D1_imryd_objetivo       |  -1.000 |     -1.000 |     -1.000 |    0.000 |      0.000 | LLM peor que humano           |
| LLM_prior      | D1_imryd_metodologia    |   0.060 |     -0.131 |      0.255 |    0.541 |      0.585 | indistinguible (IC incluye 0) |
| LLM_prior      | D1_imryd_resultados     |  -0.081 |     -0.242 |      0.057 |    0.242 |      0.274 | indistinguible (IC incluye 0) |
| LLM_prior      | D1_imryd_conclusiones   |  -0.099 |     -0.215 |      0.014 |    0.089 |      0.109 | indistinguible (IC incluye 0) |
| LLM_prior      | D1_orden_logico         |  -0.447 |     -0.736 |     -0.142 |    0.001 |      0.002 | LLM peor que humano           |
| LLM_prior      | D2_coherencia           |  -0.168 |     -0.245 |     -0.093 |    0.000 |      0.000 | LLM peor que humano           |
| LLM_prior      | D3_contextualizacion    |  -0.605 |     -0.802 |     -0.352 |    0.000 |      0.000 | LLM peor que humano           |
| LLM_prior      | D3_metodo_detallado     |   0.032 |     -0.093 |      0.159 |    0.624 |      0.660 | indistinguible (IC incluye 0) |
| LLM_prior      | D3_resultados_concretos |  -0.106 |     -0.208 |     -0.019 |    0.013 |      0.019 | LLM peor que humano           |
| LLM_prior      | D3_conclusion_responde  |  -0.058 |     -0.178 |      0.054 |    0.328 |      0.356 | indistinguible (IC incluye 0) |
| LLM_prior      | D4_consistencia         |  -0.474 |     -0.560 |     -0.388 |    0.000 |      0.000 | LLM peor que humano           |
| LLM_prior      | no_evaluable            |  -0.084 |     -0.235 |      0.000 |    0.285 |      0.317 | indistinguible (IC incluye 0) |

Filas donde las anclas A1 y A2 no coinciden en la conclusion: **18**.

## 4. Alpha de Krippendorff multi-anotador por variable

| variable                | metric   |   alpha_A1_A2 |   alpha_runs_gpt-oss-20b |   alpha_runs_mistral-7b |   alpha_runs_qwen3-8b |   alpha_all |
|:------------------------|:---------|--------------:|-------------------------:|------------------------:|----------------------:|------------:|
| D1_imryd_objetivo       | nominal  |         1.000 |                    0.499 |                   1.000 |                 1.000 |       0.193 |
| D1_imryd_metodologia    | nominal  |         0.833 |                    0.823 |                   0.265 |                 1.000 |       0.548 |
| D1_imryd_resultados     | nominal  |         0.923 |                    0.881 |                   0.615 |                 1.000 |       0.725 |
| D1_imryd_conclusiones   | nominal  |         0.881 |                    0.758 |                   0.552 |                 0.964 |       0.546 |
| D1_orden_logico         | nominal  |         0.702 |                    0.726 |                   0.272 |                 0.933 |       0.363 |
| D2_coherencia           | ordinal  |         0.745 |                    0.338 |                   0.590 |                 0.493 |       0.240 |
| D3_contextualizacion    | nominal  |         0.697 |                    0.648 |                   0.118 |                 0.488 |       0.089 |
| D3_metodo_detallado     | nominal  |         0.704 |                    0.737 |                   0.461 |                 0.943 |       0.517 |
| D3_resultados_concretos | nominal  |         0.968 |                    0.734 |                   0.625 |                 0.947 |       0.640 |
| D3_conclusion_responde  | nominal  |         0.836 |                    0.770 |                   0.552 |                 0.964 |       0.522 |
| D4_consistencia         | ordinal  |         0.738 |                    0.380 |                   0.692 |                 0.866 |       0.046 |
| no_evaluable            | nominal  |         1.000 |                    0.811 |                 nan     |               nan     |       0.364 |

