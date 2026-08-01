# Plan de testeo — medir la tasa de captura del sur

**Creado:** 2026-07-22 · **Revisado:** 2026-08-01 (America/Monterrey) · **Para:** Francisco.

> **Qué cambió en la revisión del 1-ago:** la capa de escritorio quedó **cerrada** (ya tenemos
> TDPA y visitantes), y se corrigió un **error de método** de la versión original: la tasa de
> captura no se puede medir en un terreno vacío. Ahora el conteo se hace en **dos sitios
> distintos**. También se separan dos tasas que la versión anterior confundía.

**Objetivo:** convertir la última incógnita del modelo —**qué fracción de los que pasan se
detiene y compra**— de supuesto en dato medido. Es lo único que falta para decidir sitio.

---

## 1 · Lo que YA está cerrado (no volver a perseguir)

| Dato | Valor | Fuente | Confianza |
|---|--:|---|---|
| TDPA Carretera Nacional, El Cercado | 19,389 veh/día (2014) → **~27,144 hoy** | SICT Datos Viales + crecimiento del parque vehicular NL (+40%, rango +30 a +55%) | SICT + estimación |
| Visitantes Cola de Caballo | **30,673 /mes** (368k/año) | OSETUR / Observatorio de Turismo NL | V-OSETUR |
| Competencia de pollo frito a 2 km en El Cercado | **0** | DENUE INEGI may-2026 | V-DENUE |
| Residentes a 2 km de El Cercado | 13,215 | Censo 2020 INEGI | V-Censo |
| Perfil del visitante | day-trip, ~US$60/persona/visita, comida como actividad central | SECTUR 2014 | F1 |
| Santiago = destino de día, no de pernocta | ocupación hotelera ~25% anual | estudio territorial (scielo) | F1 |

**Lo único que falta es la tasa de captura.** No existe en ningún archivo público: hay que
medirla o comprarla (ver §6).

---

## 2 · El error de método que corrige esta revisión

La versión original mandaba a contar tráfico **en el sitio candidato** y de ahí sacar la
captura. No se puede: en un terreno vacío puedes contar cuántos autos pasan, pero no cuántos
*se habrían detenido en tu local*, porque el local no existe. Tienes denominador sin numerador.

**Solución: medir en dos lugares distintos y combinar.**

```
SITIO CANDIDATO (sur)         →  mide el FLUJO
   autos, peatones, % placa foránea, horarios pico

ANÁLOGO YA OPERANDO           →  mide la CAPTURA
   de los que pasan, ¿cuántos entran?  → porcentaje empírico

venta_tráfico = FLUJO(candidato) × CAPTURA(análogo) × ticket × 30
```

**Análogos válidos** (QSR sobre vialidad, no dentro de plaza): KFC Contry, KFC Chapultepec,
Church's Allende, o cualquier comida rápida sobre la Nacional con estacionamiento propio y
entrada visible desde la calle. Entre más parecido al formato que vamos a operar, mejor.

---

## 3 · Dos tasas de captura distintas (no confundirlas)

| | **σ residencial** | **Captura de tráfico** |
|---|---|---|
| Qué mide | porción del gasto en comida rápida de quien **vive** a 2 km | fracción de vehículos que **pasan** y se detienen |
| Rango que usamos | 4% / 6% / 8% | 0.2% / 0.5% / 1.0% |
| Sostiene | la venta de Contry, Altamira, todo el norte del corredor | **la tesis completa de El Cercado** |
| Cómo se calibra mejor | AUV real del franquiciador + benchmarks de industria | **este conteo de campo** |

El conteo responde la segunda. Medir semanas para responder la primera sería trabajo
desperdiciado: para esa, una llamada al franquiciador vale más.

---

## 4 · El protocolo

### Cuándo
- **2 sábados + 1 domingo** (el flujo turístico real)
- **1 día entre semana** como línea base — **no es opcional**: sin él no puedes separar cuánto
  del flujo es turismo y cuánto es vida cotidiana, y esa diferencia *es* la tesis del sur.
- Franjas: **13:00-15:00 y 18:00-20:00**.
- Anotar clima y si hay evento especial (festival, Cielo Mágico) para no sesgar la muestra.

### Con qué — graba, no cuentes en vivo
Un teléfono en tripié apuntando a la entrada del análogo, **30 minutos continuos**, y cuentas
después en casa con pausa y a doble velocidad. Contar dos flujos simultáneos en vivo se degrada
rápido y no puedes verificar tu propio conteo; el video sí. Filmar desde vía pública no tiene
problema; no metas la cámara a propiedad privada.

En el sitio candidato basta contar tráfico, que es un solo flujo — ahí sí sirve el conteo en
vivo con contador de tally.

### Qué registrar

**En el sitio candidato (flujo):**

| Fecha | Día | Franja | Autos/15min | Peatones/15min | % placa foránea | Clima / evento |
|---|---|---|---|---|---|---|

**En el análogo (captura) — la tabla que decide:**

| Fecha | Día | Franja | Autos que PASAN /15min | Autos que ENTRAN /15min | Captura % | Personas saliendo con bolsa /15min |
|---|---|---|---|---|---|---|

### Dos observaciones extra que valen mucho y cuestan nada
1. **Bolsas a la salida** en hora pico → transacciones/hora del análogo. Con el ticket, te da
   su venta por hora: un benchmark de competidor real, no estimado.
2. **Compra tú mismo** en el análogo, en pico. Confirmas el ticket real, mides el tiempo de
   servicio, y conoces por dentro a la competencia.

---

## 5 · Qué hace el número con la decisión

Con **TDPA ~27,144 veh/día** y **ticket $220**:

| Captura | Autos que paran/día | Venta de tráfico / mes |
|--:|--:|--:|
| 0.2% | 54 | **~$358k** |
| 0.5% | 136 | **~$896k** |
| 1.0% | 271 | **~$1.79M** |

Ese rango es la diferencia entre *"El Cercado no llega"* y *"El Cercado es el mejor sitio del
corredor"*. Ningún análisis adicional de escritorio mueve esa aguja.

**Supuestos explícitos de la tabla** (para poder discutirlos):
- Un auto que se detiene = **una** transacción de $220. Si viajan en familia y ordenan junto,
  es conservador; si van solos, es optimista.
- El TDPA es **promedio anual**: el fin de semana el flujo es bastante mayor y entre semana
  menor. La venta del sur será **grumosa** — findes fuertes, entre semana floja. Por eso el
  día entre semana del conteo importa tanto.
- El TDPA de SICT cuenta ambos sentidos de la carretera.

---

## 6 · La alternativa que puede valer más que el conteo

El franquiciador **ya opera 82 unidades** y sabe lo que vende una. Si entrega ventas por unidad
de tiendas comparables (formato y entorno parecidos), tienes un dato **observado** en vez de
estimado, en una llamada.

Pero según **D-009**, sus cifras son *priors blandos* (experiencia, no estudio formal). Por eso:

> **El conteo no reemplaza esa llamada — la verifica.** Es la única forma de detectar si el
> número que te dan viene inflado, antes de firmar. Contra una inversión de esta escala, tres
> fines de semana contando coches son un seguro barato.

Preguntas para la misma llamada: AUV real por unidad, regalías, exclusividad del corredor, y si
el punto de venta es obligatorio (esto último importa: define quién es dueño de tus datos de
venta).

---

## 7 · Reparto (ley 6: Claude prepara el instrumento, Francisco ejecuta)

- **Claude:** desk cerrado (§1). Al volver del campo: recalcular el modelo con la captura
  medida, actualizar el Radar y marcar el nivel de confianza que corresponda.
- **Francisco y equipo:** el conteo de §4, en el sitio candidato y en el análogo.
- **Francisco:** la llamada al franquiciador (§6).
- **Opcional:** capa Google Places (*popular times* de las anclas) para validar curvas de
  afluencia sin ir — requiere key GCP en el manejo de secretos.
