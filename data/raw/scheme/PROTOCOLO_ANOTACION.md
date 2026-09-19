# Protocolo de anotación de la calidad estructural de resúmenes de tesis multidisciplinarios

**Versión 2.0 · 2026-08-11**

Manual para los tres anotadores independientes (A1, A2, A3) del patrón de referencia
humano de la tesis doctoral *«Modelos de inteligencia artificial para la evaluación
automatizada de resúmenes de tesis multidisciplinarios en repositorios de la región
Puno»*.

---

## Índice

1. Finalidad y alcance
2. Marco conceptual
3. Qué se anota y qué no
4. Principio rector: la función antes que la forma
5. Adaptación disciplinar
6. Dimensión 1 — Adherencia a IMRyD
7. Dimensión 2 — Coherencia organizacional
8. Dimensión 3 — Completitud de componentes
9. Dimensión 4 — Consistencia metodológica
10. Campos de control
11. Catálogo de casos límite
12. Ejemplos completos resueltos
13. Procedimiento de trabajo
14. Agregación de puntuaciones
15. Control de calidad
16. Registro de decisiones de calibración
17. Glosario
18. Referencias

---

## 1. Finalidad y alcance

### 1.1 Para qué sirve lo que vas a hacer

Vas a evaluar resúmenes de tesis. Tus valoraciones, junto con las de los otros dos
anotadores, constituyen el **patrón de referencia** contra el que se validarán cuatro
modelos de inteligencia artificial.

Esto significa dos cosas que conviene tener presentes:

**Tu criterio es la vara de medir.** No hay una respuesta «correcta» externa contra la
que se te vaya a comparar. Lo que los tres acordéis *es* la definición operativa de
calidad estructural en este estudio.

**El acuerdo entre vosotros acota el estudio entero.** Si en una dimensión los tres
discrepáis sistemáticamente, ningún modelo automático podrá validarse contra ella —
porque no habrá un criterio estable contra el que compararlo. Ese límite se reportará
como resultado, no se ocultará.

### 1.2 Qué NO estás evaluando

| No evalúas | Por qué |
|---|---|
| La calidad de la investigación | No has leído la tesis, solo el resumen |
| La relevancia del tema | Es irrelevante para la estructura |
| La corrección ortográfica o gramatical | Un resumen con faltas puede estar perfectamente estructurado |
| El prestigio de la institución | No sabes cuál es, y es deliberado |
| Si los resultados te parecen creíbles | No tienes los datos para juzgarlo |

Evalúas **cómo está construido el resumen como pieza de comunicación científica**.

### 1.3 Volumen y calendario

| Fase | Resúmenes | Tiempo estimado | Entra en el cálculo |
|---|---:|---|---|
| Calibración | 30 | ~3 h | No |
| Principal | 200 | ~20 h | Sí |

---

## 2. Marco conceptual

### 2.1 La estructura IMRyD

La secuencia Introducción – Metodología – Resultados – Discusión es la convención
dominante de comunicación científica. Su función no es formal sino informativa:
permite al lector localizar rápidamente qué se investigó, cómo, qué se halló y qué
significa.

En el resumen esa estructura aparece comprimida. Un resumen que la respeta permite
decidir en treinta segundos si el trabajo interesa; uno que no la respeta obliga a
leer la tesis completa para averiguarlo.

### 2.2 Resumen estructurado frente a resumen narrativo

Un **resumen estructurado** lleva encabezados explícitos (`Objetivo:`, `Métodos:`,
`Resultados:`, `Conclusiones:`). Un **resumen narrativo** presenta la misma
información en prosa corrida.

En el corpus de esta investigación **solo el 6,3 % de los resúmenes son
estructurados**. Los encabezados, por tanto, son la excepción: la anotación se basa
en identificar la función de cada segmento, no en localizar etiquetas.

### 2.3 Por qué hacen falta tres anotadores

Con un solo evaluador no hay forma de saber si sus juicios son reproducibles o
idiosincrásicos. Con dos se puede medir el acuerdo, pero cuando discrepan hay que
decidir quién tiene razón, y esa decisión es discrecional.

Con tres, la mayoría resuelve automáticamente y el criterio es defendible. Además
permite calcular el kappa de Fleiss, que admite más de dos jueces.

---

## 3. Qué se anota y qué no

### 3.1 El material

Cada entrada del cuadernillo contiene:

- Un **identificador opaco** (`CAL-001`, `GT-001`…)
- El **título** de la tesis
- El **resumen** completo, tal como figura en el repositorio

No verás institución, año, autor ni área de conocimiento. **Es deliberado:** esos
datos activan expectativas que contaminan la valoración.

### 3.2 Prohibiciones

**No busques la tesis original.** El modelo de IA con el que se te comparará tampoco
la verá. Si tú evalúas con información adicional, la comparación deja de ser válida.

**No consultes con los otros anotadores durante la fase principal.** El valor del
acuerdo depende de la independencia. Si os coordináis, el kappa mide vuestra
conversación.

**No vuelvas atrás a «corregir» valoraciones anteriores** una vez avanzada la sesión.
Si a mitad del cuadernillo cambias de criterio, anótalo en observaciones y sigue con
el nuevo criterio; el cambio se detectará en el análisis.

---

## 4. Principio rector: la función antes que la forma

> **Evalúa si el resumen cumple la FUNCIÓN, no si emplea la FORMA canónica.**

Esta es la regla que resuelve la mayoría de las dudas. Un resumen de una tesis de
literatura no tiene «muestra» ni «p-valor», y no por ello está incompleto.

En cada dimensión pregúntate **qué necesita saber un lector**, no **si aparece la
palabra que esperabas**.

| Componente | Su función informativa | Pregunta que responde |
|---|---|---|
| Objetivo | Delimitar qué se propuso averiguar | ¿Qué buscaba este trabajo? |
| Metodología | Permitir juzgar la solidez del procedimiento | ¿Cómo lo averiguó? |
| Resultados | Comunicar el hallazgo | ¿Qué encontró? |
| Conclusiones | Situar el hallazgo en su significado | ¿Y eso qué implica? |

**Ante la duda entre penalizar la ausencia de forma o reconocer la función cumplida,
reconoce la función** y déjalo escrito en `observaciones`.

---

## 5. Adaptación disciplinar

El corpus abarca las seis áreas OCDE. La estructura esperable varía sustancialmente
entre ellas, y el protocolo debe absorber esa variación sin premiar ni castigar
disciplinas.

### 5.1 Formas válidas de cada componente por tradición

| Componente | Cuantitativo experimental | Cuantitativo observacional | Cualitativo | Humanidades |
|---|---|---|---|---|
| **Objetivo** | Hipótesis contrastable | Pregunta de asociación | Pregunta comprensiva | Problema interpretativo, objeto de estudio |
| **Metodología** | Diseño, grupos, intervención, muestra | Diseño, población, muestreo, instrumento | Enfoque, participantes, técnica de recogida, análisis | Corpus, fuentes, marco teórico, procedimiento hermenéutico |
| **Resultados** | Estadísticos, contraste de hipótesis | Coeficientes, prevalencias | Categorías, temas emergentes, patrones | Lecturas, hallazgos interpretativos, evidencia documental |
| **Conclusiones** | Aceptación o rechazo de hipótesis | Implicaciones de la asociación | Comprensión alcanzada | Tesis defendida, aportación al debate |

### 5.2 Errores de anotación que esta tabla previene

**Penalizar a Humanidades por no tener muestra.** Un trabajo sobre la obra de un
autor no tiene «población» ni «muestreo». Si declara el corpus analizado y el marco
interpretativo, la metodología está presente.

**Penalizar a un estudio cualitativo por no dar cifras.** «Emergieron tres categorías:
X, Y y Z» es un resultado concreto tanto como «r = 0,72».

**Premiar la jerga.** Que un resumen diga «se aplicó el método científico
hipotético-deductivo» no aporta ninguna precisión sobre cómo se hizo. Eso **no**
cuenta como metodología detallada.

### 5.3 Datos del corpus que conviene conocer

La exploración previa del corpus completo (31 300 resúmenes) mostró estas medias de
componentes presentes, sobre 4:

| Área | Media |
|---|---:|
| Ciencias Médicas y de la Salud | 3,08 |
| Ciencias Sociales | 2,20 |
| Ciencias Agrícolas | 2,15 |
| Ciencias Naturales | 1,80 |
| Ingeniería y Tecnología | 1,68 |
| Humanidades | 1,07 |

**Esto no significa que Humanidades escriba peor.** Puede significar que la rejilla
IMRyD no le encaja. Uno de los objetivos de esta anotación es distinguir ambas cosas.
Aplica el principio de la sección 4 con especial cuidado en Humanidades.

---

## 6. Dimensión 1 — Adherencia a IMRyD

**Qué mide:** si los cuatro componentes canónicos están presentes y en orden.
**Cinco campos, cada uno 0 o 1.**

### 6.1 `D1_imryd_objetivo`

**Vale 1** cuando se puede responder «¿qué se propuso averiguar este trabajo?» leyendo
solo el resumen.

Formas que cuentan:
- Enunciado explícito: «El objetivo fue determinar…»
- Propósito en prosa: «La presente investigación busca analizar…»
- Objetivo implícito inequívoco: «se centra en evaluar los efectos de X sobre Y»
- Hipótesis enunciada como propósito

Formas que **no** cuentan:
- Que el objetivo solo se deduzca del **título**, sin aparecer en el resumen
- Enunciados vacíos: «se realizó un estudio sobre el tema»
- Descripción del tema sin propósito: «Las redes sociales son un fenómeno creciente…»

### 6.2 `D1_imryd_metodologia`

**Vale 1** cuando se indica de algún modo cómo se obtuvo el conocimiento.

Umbral mínimo: **una** indicación procedimental concreta. «Se aplicó una encuesta»
basta para el 1 (mínimo, pero presente). Para la D3 hará falta más.

No cuentan las fórmulas huecas: «se utilizó el método científico», «se empleó una
metodología adecuada», «la investigación es de tipo científico».

### 6.3 `D1_imryd_resultados`

**Vale 1** cuando se comunica **qué se encontró**, no solo qué se hizo.

Distinción central:

| Enunciado | ¿Resultado? |
|---|---|
| «Se aplicó el cuestionario a 200 estudiantes» | No — es método |
| «El 47 % presentó conocimiento regular» | Sí |
| «Los resultados fueron favorables» | No — no comunica ningún contenido |
| «No se hallaron diferencias significativas» | Sí — un resultado nulo es un resultado |

### 6.4 `D1_imryd_conclusiones`

**Vale 1** cuando hay un cierre que **va más allá de repetir el resultado**:
interpretación, implicación, respuesta explícita al objetivo, recomendación fundada.

| Enunciado | ¿Conclusión? |
|---|---|
| «El 47 % tuvo conocimiento regular. En conclusión, el 47 % tuvo conocimiento regular» | No — repetición |
| «Se concluye que el nivel es predominantemente regular» | Sí — sintetiza y responde al objetivo |
| «Se recomienda capacitar al personal» | Sí — implicación derivada |

### 6.5 `D1_orden_logico`

**Vale 1** cuando los componentes presentes aparecen en secuencia coherente
(objetivo → método → resultados → conclusión).

Reglas:
- Se juzga **solo sobre los componentes presentes**. Si faltan dos, se evalúa el orden de los otros dos.
- Si hay **0 o 1** componentes presentes, vale **0** automáticamente.
- Un dato metodológico suelto dentro de los resultados no rompe el orden. Lo rompe que el bloque entero esté desplazado.

### 6.6 Árbol de decisión

```
¿Puedo decir qué se propuso averiguar?            → sí: objetivo = 1
¿Puedo decir cómo lo hizo, con algo concreto?     → sí: metodología = 1
¿Puedo decir qué encontró (no qué hizo)?          → sí: resultados = 1
¿Hay cierre que interprete o responda?            → sí: conclusiones = 1
¿Los presentes van en secuencia lógica?           → sí: orden = 1
    (si hay 0 o 1 componentes → orden = 0)
```

---

## 7. Dimensión 2 — Coherencia organizacional

**Qué mide:** cómo fluye el texto. Progresión temática, conexión entre partes,
consistencia terminológica. **Escala 1 a 5.**

### 7.1 Anclajes

| Valor | Descriptor | Señales típicas |
|---|---|---|
| **5** | Progresión impecable. Cada oración prepara la siguiente. Se lee de un tirón | Transiciones naturales; un solo término por concepto; sin repeticiones |
| **4** | Fluye bien, con alguna aspereza menor que no estorba | Algún salto breve; una repetición; adjetivación superflua |
| **3** | Se entiende, pero cuesta | Saltos de tema; el mismo concepto con dos nombres; frases inconexas aisladas |
| **2** | Hay que releer para reconstruir el hilo | Ideas desordenadas; datos sueltos sin encuadre; párrafo que no viene a cuento |
| **1** | Incoherente | Frases sin relación; contradicciones internas sin resolver |

### 7.2 Qué NO descuenta en esta dimensión

- Faltas de ortografía o errores gramaticales
- Que falten componentes (eso lo mide la D1)
- Que los resultados sean vagos (eso lo mide la D3)
- Longitud excesiva o insuficiente

Evalúa **exclusivamente el flujo**.

### 7.3 Señales frecuentes de descuento

- **Adjetivación valorativa innecesaria**: «un minucioso análisis», «una sólida base de datos», «los valientes bomberos». Delata redacción poco cuidada y suele acompañar saltos.
- **Deriva terminológica**: llamar «participantes» y luego «pacientes» y luego «usuarios» a lo mismo.
- **Cambio abrupto de foco**: pasar de resultados de la variable principal a características demográficas sin transición.

---

## 8. Dimensión 3 — Completitud de componentes

**Qué mide:** si lo presente tiene sustancia suficiente para ser útil. La D1 pregunta
*si está*; la D3, *si sirve*. **Cuatro campos, cada uno 0 o 1.**

### 8.1 `D3_contextualizacion`

**Vale 1** cuando el resumen sitúa el problema: por qué importa, dónde ocurre, a quién
afecta, contra qué norma o marco se contrasta.

| Ejemplo | Valor |
|---|---|
| «La escasez de agua potable ha forzado a muchas comunidades a utilizar aguas subterráneas, algunas con arsénico en concentraciones peligrosas» | 1 |
| «El objetivo del presente trabajo fue determinar el nivel de conocimiento…» (empieza directamente por el objetivo) | 0 |

Es el campo que más se puntúa 0 en el corpus: la mayoría de los resúmenes arrancan
directamente por el objetivo.

### 8.2 `D3_metodo_detallado`

**Vale 1** cuando se dan **al menos dos** precisiones concretas sobre el procedimiento.

Cuentan como precisión: diseño, tipo de estudio, tamaño de muestra, técnica de
muestreo, instrumento nombrado, prueba estadística, corpus analizado, número de
observaciones, criterio de selección.

| Ejemplo | Precisiones | Valor |
|---|---|---|
| «Diseño descriptivo transversal que abarcó 70 bomberos» | diseño + n | 1 |
| «Se utilizó el método científico» | ninguna | 0 |
| «Se aplicó una encuesta» | una (instrumento genérico) | 0 |
| «105 briquetas, diseño experimental explicativo, fichas de observación» | tres | 1 |

### 8.3 `D3_resultados_concretos`

**Vale 1** cuando los resultados aportan contenido específico: cifras, magnitudes,
categorías nombradas, relaciones con dirección.

| Ejemplo | Valor | Comentario |
|---|---|---|
| «47 % con conocimiento regular y 40 % alto» | 1 | Magnitudes |
| «r = 0,72 entre motivación y rendimiento» | 1 | Coeficiente y dirección |
| «Emergieron tres categorías: adaptación, resistencia y negociación» | 1 | Cualitativo, igualmente concreto |
| «Los resultados muestran mejoras significativas» | 0 | Sin contenido |
| «Sig. > 0,05 en todas las dimensiones» | **caso límite** | Ver 11.4 |

### 8.4 `D3_conclusion_responde`

**Vale 1** cuando la conclusión contesta **al objetivo enunciado**, no a otra cosa.

Casos de 0:
- El objetivo era comparar dos grupos y la conclusión habla de la importancia del tema
- El objetivo era describir un nivel y la conclusión propone políticas sin haber medido su efecto
- La conclusión afirma algo que los resultados no sostienen

**Si el componente no está presente en la D1, su campo correspondiente de la D3 es 0.**

---

## 9. Dimensión 4 — Consistencia metodológica

**Qué mide:** coherencia entre lo que el resumen **dice que hizo** y lo que
**presenta**. **Escala 1 a 5.**

### 9.1 Anclajes

| Valor | Descriptor |
|---|---|
| **5** | Enfoque, diseño, resultados y conclusiones encajan sin fisuras |
| **4** | Coherente, con una imprecisión terminológica menor |
| **3** | Una discordancia visible que no invalida el conjunto |
| **2** | Varias discordancias, o la conclusión excede lo que los datos sostienen |
| **1** | Contradicción abierta que invalida la conclusión |

### 9.2 Catálogo de discordancias

| Discordancia | Gravedad orientativa |
|---|---|
| Usar «significativo» en sentido coloquial, sin prueba estadística | 4 |
| Declarar enfoque mixto y presentar solo resultados cuantitativos | 3 |
| Declarar diseño correlacional y concluir en términos causales | 3 |
| Conclusión más amplia que la muestra permite (generalizar desde un caso) | 2–3 |
| Afirmar diferencias tras reportar p > 0,05 | **1** |
| Declarar estudio cualitativo y reportar p-valores | **1** |

### 9.3 Cuándo marcar `no_evaluable`

Si el resumen **no declara ninguna metodología**, la D4 no puede evaluarse: no hay
nada contra lo que contrastar la coherencia.

Marca `no_evaluable = 1` y **deja vacía** la puntuación de D4. **No pongas 1**: un 1
significa «hay contradicción abierta», que es una afirmación distinta de «no hay
información».

---

## 10. Campos de control

| Campo | Cuándo se usa |
|---|---|
| `no_evaluable` | El texto no es un resumen (carátula, licencia, texto truncado, índice) o carece de metodología para la D4. Si no es un resumen en absoluto, deja todos los demás campos vacíos |
| `observaciones` | Dudas, casos límite, motivo de una decisión discutible, cambios de criterio a media sesión |

**Usa `observaciones` con generosidad.** En la reunión de calibración es el material
más valioso: cada duda anotada se convierte en una regla del protocolo.

---

## 11. Catálogo de casos límite

Resueltos de antemano para que los tres decidáis igual.

### 11.1 El objetivo solo está en el título

El resumen empieza por la metodología y nunca enuncia qué buscaba.
→ `D1_imryd_objetivo = 0`. El resumen debe ser autocontenido.

### 11.2 Objetivo implícito pero inequívoco

«La investigación se centra en evaluar los efectos de X sobre Y.»
→ `D1_imryd_objetivo = 1`. La función está cumplida aunque no diga «objetivo».

### 11.3 Resultados que en realidad son método

«Los resultados muestran que se aplicaron 200 encuestas.»
→ `D1_imryd_resultados = 0`. Describe la ejecución, no el hallazgo.

### 11.4 Significancia sin magnitud

«Sig. > 0,05 en todas las dimensiones», sin dar el estadístico ni el valor exacto.
→ `D1_imryd_resultados = 1` (hay un hallazgo: no hay diferencias)
→ `D3_resultados_concretos = 0` (no hay magnitud reportada)

Esta combinación es frecuente y perfectamente coherente: el resultado existe pero
está mal comunicado.

### 11.5 Conclusión que contradice los resultados

Reporta p > 0,05 y luego afirma que sí hay diferencias.
→ `D4_consistencia = 1`. Es el error más grave del catálogo.
→ `D3_conclusion_responde = 0`.

### 11.6 Resumen extremadamente largo

Algunos superan las 700 palabras y parecen una introducción completa.
→ No se penaliza la longitud por sí misma. Evalúa las dimensiones con normalidad.
Si la extensión rompe el flujo, se refleja en la D2.

### 11.7 Resumen bilingüe

Algunos incluyen la versión en inglés a continuación.
→ Evalúa **solo la versión en castellano**. Anótalo en observaciones.

### 11.8 El texto no es un resumen

Carátula, nota de licencia, índice, texto truncado a media frase.
→ `no_evaluable = 1` y todo lo demás vacío.

### 11.9 Estudio cualitativo sin cifras

«Se entrevistó a 12 docentes; emergieron tres categorías…»
→ Método detallado = 1 (n + técnica). Resultados concretos = 1 (categorías nombradas).
**No penalices la ausencia de estadísticos.**

### 11.10 Palabras clave dentro del resumen

Algunos terminan con «Palabras clave: …».
→ Ignóralas. No suman ni restan en ninguna dimensión.

---

## 12. Ejemplos completos resueltos

Cuatro resúmenes reales del corpus, anotados con justificación. **No pertenecen a la
muestra**, así que no los encontrarás en tu cuadernillo.

### 12.1 Ejemplo A — Ciencias de la Salud (267 palabras)

> El objetivo de presente trabajo fue demostrar cual es el nivel de conocimiento sobre
> reanimación cardiopulmonar básica en el adulto de los efectivos de las compañías de
> bomberos voluntarios del departamento de Puno durante el 2022. En el estudio
> realizado, se llevó a cabo un minucioso análisis descriptivo transversal que abarcó
> un total de 70 valientes bomberos […] se empleó el software de análisis predictivo
> SPSS versión 25 […] Los resultados muestran que de los bomberos voluntarios
> obtuvieron 47% con conocimiento regular y un 40% con conocimiento alto en RCP […]
> el promedio en edad es de 29.93 años, con una prevalencia de 69% del sexo masculino
> […] Del estudio se concluye que el nivel de conocimientos sobre RCP de los efectivos
> bomberiles del departamento de Puno es predominantemente regular demostrando la gran
> capacidad de respuesta de los efectivos bomberiles.

| Campo | Valor | Justificación |
|---|---|---|
| D1 objetivo | 1 | Explícito y delimitado |
| D1 metodología | 1 | Diseño, n, software |
| D1 resultados | 1 | Porcentajes concretos |
| D1 conclusiones | 1 | Sintetiza y responde |
| D1 orden | 1 | Secuencia canónica |
| **D2 coherencia** | **4** | Fluye, pero la adjetivación («minucioso», «valientes», «sólida base de datos») y el salto sin transición del nivel de conocimiento a las características demográficas restan un punto |
| D3 contextualización | 0 | Arranca directamente por el objetivo; no dice por qué importa el RCP en bomberos |
| D3 método detallado | 1 | Diseño + n = dos precisiones |
| D3 resultados concretos | 1 | 47 %, 40 %, 29,93 años |
| D3 conclusión responde | 1 | El objetivo era el nivel; la conclusión da el nivel |
| **D4 consistencia** | **3** | «Predominantemente regular» **no sostiene** «demostrando la gran capacidad de respuesta». La conclusión añade una afirmación que los datos no respaldan |

**Lo que enseña este caso:** un resumen puede tener los cuatro componentes y aun así
fallar en consistencia, por un salto en la última frase.

### 12.2 Ejemplo B — Ciencias Sociales (226 palabras)

> El objetivo de la investigación es determinar si existen diferencias significativas
> en la adicción a las redes sociales en estudiantes universitarios de la ciudad de
> Juliaca. […] enfoque cuantitativo con diseño no experimental, de tipo comparativo y
> de corte transversal. Se contó con la participación de 200 estudiantes […] El
> instrumento utilizado fue el Cuestionario de Adicción a las redes sociales (ARS), que
> consta de 24 ítems […] Al tratar con una variable de distribución no normal, se optó
> por el estadístico U de Mann Whitney cuyos valores indican que **no existen
> diferencias significativas** (Sig. >0.05) […] **Sin embargo, se evidenció que los
> estudiantes reportaron un mayor nivel de adicción a las redes sociales.**

| Campo | Valor | Justificación |
|---|---|---|
| D1 objetivo | 1 | Explícito |
| D1 metodología | 1 | Enfoque, diseño, instrumento, prueba |
| D1 resultados | 1 | Resultado nulo, que es un resultado |
| D1 conclusiones | 0 | No hay cierre interpretativo; termina con una afirmación suelta |
| D1 orden | 1 | Correcto en lo presente |
| **D2 coherencia** | **3** | La última frase contradice lo anterior sin explicarlo |
| D3 contextualización | 0 | Arranca por el objetivo |
| D3 método detallado | 1 | n, instrumento nombrado, prueba justificada |
| **D3 resultados concretos** | **0** | Reporta «Sig. >0.05» sin valor exacto ni estadístico U. Ver caso 11.4 |
| D3 conclusión responde | 0 | No hay conclusión propiamente dicha |
| **D4 consistencia** | **2** | Elige Mann-Whitney justificando la no normalidad (bien), pero concluye «mayor nivel de adicción» tras afirmar que no hay diferencias significativas |

**Lo que enseña este caso:** obsérvese que la elección metodológica es **correcta** —
justifica la prueba no paramétrica— y aun así la D4 baja, porque la última frase
contradice el resultado. La D4 mide coherencia interna, no corrección técnica.

### 12.3 Ejemplo C — Ingeniería y Tecnología (217 palabras)

> La presente investigación tuvo como objetivo principal evaluar la calidad del agua
> destinada al consumo humano en el Centro Poblado de Thunco […] contrastados con los
> Límites Máximos Permisibles establecidos en el D.S. N.º 031-2010-SA. El estudio se
> desarrolló bajo un enfoque cuantitativo y nivel descriptivo, realizando la toma de
> muestras en tres puntos estratégicos […] el agua presentó un color de (5.67 UCV), con
> una turbidez (1.13 UNT) […] pH es de (7.67) […] ausencia de coliformes totales (0
> UFC/100 mL) […] En consecuencia, se concluye que el agua potable del Centro Poblado
> de Thunco cumple satisfactoriamente con los estándares […] siendo considerada apta
> para el consumo humano.

| Campo | Valor | Justificación |
|---|---|---|
| D1 objetivo | 1 | Explícito, con criterio de contraste |
| D1 metodología | 1 | Enfoque, nivel, puntos de muestreo |
| D1 resultados | 1 | Valores con unidades |
| D1 conclusiones | 1 | Responde y dictamina aptitud |
| D1 orden | 1 | Canónico |
| **D2 coherencia** | **5** | Progresión limpia, terminología constante |
| **D3 contextualización** | **1** | Sitúa el problema: agua de consumo humano en una localidad concreta, contra una norma nombrada |
| D3 método detallado | 1 | Enfoque + puntos de muestreo + parámetros |
| D3 resultados concretos | 1 | Magnitudes con unidades |
| D3 conclusión responde | 1 | El objetivo era evaluar contra la norma; concluye sobre el cumplimiento |
| **D4 consistencia** | **5** | Descriptivo, resultados descriptivos, conclusión descriptiva. Sin fisuras |

**Lo que enseña este caso:** es el patrón de excelencia. Nótese que no usa
encabezados: es prosa corrida y aun así obtiene la máxima puntuación.

### 12.4 Ejemplo D — Ingeniería y Tecnología (293 palabras)

> La investigación denominada «Incidencia del empleo de escoria negra y polvo de
> granito sobre la resistencia a la compresión de un concreto convencional producido en
> la ciudad de Juliaca», **se centra en evaluar los efectos** de estos materiales a la
> resistencia del concreto. La metodología es científica, con un diseño experimental
> explicativo y de tipo aplicado, abarcando una muestra de 105 briquetas […] A los 28
> días, el concreto estándar tenía una resistencia de 213.42 kg/cm². Los concretos con
> escoria negra presentaron resistencias mayores: 233.60 kg/cm² (2%), 248.76 kg/cm²
> (4%) […] Estos resultados demuestran una **mejora significativa** en la peculiaridad
> mecánicas del concreto […] presentándose como una opción viable para optimizar las
> peculiaridades del concreto en aplicaciones constructivas.

| Campo | Valor | Justificación |
|---|---|---|
| **D1 objetivo** | **1** | Implícito pero inequívoco: «se centra en evaluar los efectos». Ver caso 11.2 |
| D1 metodología | 1 | Diseño, tipo, n de briquetas |
| D1 resultados | 1 | Resistencias con unidades por dosificación |
| D1 conclusiones | 1 | Interpreta y proyecta aplicación |
| D1 orden | 1 | Canónico |
| **D2 coherencia** | **4** | Buena progresión; «peculiaridad mecánicas» y «peculiaridades» por «propiedades» delatan deriva terminológica |
| D3 contextualización | 0 | No explica por qué importa mejorar el concreto ni qué problema resuelve |
| D3 método detallado | 1 | Diseño + n + instrumentos |
| D3 resultados concretos | 1 | Valores por porcentaje de adición |
| D3 conclusión responde | 1 | Responde al efecto de los materiales |
| **D4 consistencia** | **4** | Afirma «mejora significativa» sin haber reportado ninguna prueba estadística: usa el término en sentido coloquial. Descuento de un punto (ver 9.2) |

**Lo que enseña este caso:** el objetivo implícito **sí cuenta**, y el uso coloquial de
«significativo» descuenta en D4 pero no invalida el resumen.

---

## 13. Procedimiento de trabajo

### 13.1 Antes de empezar

1. Lee este protocolo entero. No lo hojees: los casos límite de la sección 11 y los ejemplos de la 12 son los que evitan discrepancias.
2. Ten el protocolo abierto mientras anotas, al menos las primeras sesiones.
3. Comprueba que tu cuadernillo es el que te corresponde (A1, A2 o A3).

### 13.2 Fase de calibración (30 resúmenes)

Anota las 30 **en solitario**. Después, reunión de los tres:

1. Se comparan las 30 valoraciones campo por campo.
2. Se discuten **únicamente** los casos con discrepancia.
3. Cada regla nueva se escribe en la sección 16 y pasa a ser vinculante.
4. **Las 30 se descartan** del cálculo final.

Sin esta fase, el primer kappa saldrá bajo por ambigüedades del instrumento y ya no
podrá distinguirse eso de un desacuerdo real entre jueces.

### 13.3 Fase principal (200 resúmenes)

- **Sin consultas entre anotadores.** Ninguna.
- Sesiones de **máximo 40 resúmenes**. A partir de ahí la atención decae y las últimas valoraciones dejan de ser comparables con las primeras.
- Ritmo orientativo: **6 minutos por resumen**. Si vas mucho más rápido, probablemente no estás aplicando los criterios; mucho más lento, probablemente estás sobreanalizando.
- Anota la fecha de cada sesión: permite detectar deriva del criterio en el análisis.

### 13.4 Qué hacer ante una duda genuina

1. Consulta la sección 11 (casos límite).
2. Consulta los ejemplos de la sección 12.
3. Aplica el principio de la sección 4: función antes que forma.
4. Decide, anota el motivo en `observaciones` y **sigue adelante**.

No dejes campos en blanco por indecisión. Un campo vacío destruye el caso para el
cálculo de acuerdo; una decisión discutible documentada, no.

---

## 14. Agregación de puntuaciones

Lo calcula el script. Se documenta para que sepas qué pesa cada campo.

```
AI (Adherencia IMRyD, 0–100) = (suma de los 5 campos D1 / 5) × 100
CO (Coherencia, 1–5)          = D2_coherencia
CC (Completitud, 0–100)       = (suma de los 4 campos D3 / 4) × 100
CM (Consistencia, 1–5)        = D4_consistencia

ICEG = 0,30·AI + 0,25·(CO×20) + 0,25·CC + 0,20·(CM×20)
```

Las escalas 1–5 se multiplican por 20 para homogeneizar a 0–100.

**Ejemplo con el caso C** (todos los campos a 1, D2 = 5, D4 = 5):
AI = 100 · CO = 5 · CC = 100 · CM = 5
ICEG = 0,30·100 + 0,25·100 + 0,25·100 + 0,20·100 = **100**

**Ejemplo con el caso B:**
AI = (1+1+1+0+1)/5 × 100 = 80 · CO = 3 · CC = (0+1+0+0)/4 × 100 = 25 · CM = 2
ICEG = 0,30·80 + 0,25·60 + 0,25·25 + 0,20·40 = 24 + 15 + 6,25 + 8 = **53,25**

---

## 15. Control de calidad

### 15.1 Qué se calculará con vuestras anotaciones

| Estadístico | Sobre qué |
|---|---|
| Kappa de Fleiss | Cada campo binario (D1 y D3), con los tres jueces |
| Kappa ponderado cuadrático | D2 y D4, por pares y promediado |
| ICC(2,3) | El índice agregado ICEG |
| Kappa por área OCDE | Los cinco campos de D1, por disciplina |

### 15.2 Interpretación del kappa (Landis y Koch, 1977)

| Valor | Lectura |
|---|---|
| < 0,00 | Peor que el azar |
| 0,00 – 0,20 | Leve |
| 0,21 – 0,40 | Aceptable |
| 0,41 – 0,60 | Moderado |
| 0,61 – 0,80 | Sustancial |
| 0,81 – 1,00 | Casi perfecto |

**Objetivo:** kappa ≥ 0,61 en todas las dimensiones tras la calibración. Por debajo de
0,41 en alguna dimensión, esa dimensión debe revisarse o reportarse como no fiable.

### 15.3 Por qué el kappa ponderado en las escalas 1–5

El kappa simple trata igual discrepar 3 frente a 4 que 1 frente a 5. En una escala
ordinal eso es incorrecto: la primera discrepancia es trivial y la segunda es grave.
El kappa ponderado cuadrático penaliza proporcionalmente al cuadrado de la distancia.

---

## 16. Registro de decisiones de calibración

Se rellena en la reunión posterior a las 30. Cada regla acordada es vinculante para la
fase principal y se incorpora a la sección 11 en la siguiente versión del protocolo.

| # | Caso discutido (id) | Discrepancia | Regla acordada | Fecha |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |

---

## 17. Glosario

| Término | Definición operativa en este protocolo |
|---|---|
| **Resumen estructurado** | El que lleva encabezados explícitos de sección |
| **Resumen narrativo** | El que presenta la misma información en prosa corrida |
| **Componente** | Cada una de las cuatro funciones informativas: objetivo, metodología, resultados, conclusiones |
| **Precisión metodológica** | Dato concreto sobre el procedimiento: diseño, n, instrumento, técnica, prueba |
| **Resultado concreto** | Hallazgo con contenido específico: cifra, magnitud, categoría nombrada o relación con dirección |
| **Discordancia** | Desajuste entre lo declarado y lo presentado |
| **Kappa** | Índice de acuerdo corregido por el azar |
| **Ground truth / patrón de referencia** | El conjunto de valoraciones humanas contra el que se validan los modelos |
| **FORD** | *Fields of Research and Development*, clasificación de áreas de la OCDE, obligatoria en RENATI |

---

## 18. Referencias

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and
Psychological Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104

Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters.
*Psychological Bulletin, 76*(5), 378–382.

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for
categorical data. *Biometrics, 33*(1), 159–174. https://doi.org/10.2307/2529310

Shrout, P. E., & Fleiss, J. L. (1979). Intraclass correlations: Uses in assessing rater
reliability. *Psychological Bulletin, 86*(2), 420–428.

> **Nota:** verificar volumen, número y páginas de Fleiss (1971) y Shrout & Fleiss
> (1979) contra la fuente original antes de incorporarlas al documento final de tesis.

---

*Fin del protocolo. Versión 2.0 · 2026-08-11*
