# Análisis — ¿Cuánta gente y en qué radio para vender $600k / $800k / $1M al mes?

**Fecha:** 2026-07-22 (America/Monterrey) · **Para:** Francisco, decisión de sitio.
**Naturaleza:** modelo de catchment (área de influencia) con supuestos EXPLÍCITOS y
sensibilidad. NO es un dato; es un marco para aterrizar el objetivo de venta a población y
radio. Los dos supuestos que dominan (ticket y captura por persona) SOLO los calibra bien el
franquiciador con sus ventas/unidad reales — ver §5.

## 1. El modelo (una línea)

```
Población necesaria en el área de influencia  P = Ventas_mensuales / c
   donde c = gasto mensual promedio, por persona del área, QUE NOS LLEGA A NOSOTROS.
Radio  R = sqrt( P / (π · D) )   con D = densidad (personas/km²).
```

`c` se descompone de forma sourced:
`c = (gasto QSR per cápita/mes) × (σ = share que capturamos de ese gasto)`.

## 2. Supuestos numerados (con fuente/confianza)

1. **Gasto QSR per cápita/mes en México ≈ $147 MXN.** Derivado: mercado QSR MX ~US$11.5 mil
   millones (2025) [F1] ÷ ~130M hab ÷ 12 ≈ US$7.4 ≈ $147 MXN/persona/mes en TODA la comida
   rápida (todas las marcas). [F1, derivado]
2. **σ = share de ese gasto que capturamos** (una sola marca de pollo entre KFC/Popeyes/
   tacos/burgers…): conservador 4% · base 7% · agresivo 10%. [SUPUESTO — depende de
   marketing/servicio/competencia; calibrar con franquiciador]
   → c = $5.9 (4%) · $10.3 (7%) · $14.7 (10%) por persona/mes.
3. **Ticket promedio:** bajo/medio "más barato que KFC". Referencia QSR MX ~$250-281 [F1];
   asumimos ~$180 base. Afecta transacciones/día (operación), NO la población necesaria.
   [CONFIRMAR — dato del franquiciador]
4. **Densidad D (personas/km²):** estimaciones urbanas por tipo de colonia [estimación, a
   pinear con polígonos AGEB]:
   - Colonia densa MTY (Contry, Tecnológico): ~8,000
   - Suburbana / Carretera Nacional (Estanzuela, Valle Alto): ~4,000
   - Centro de pueblo (Santiago, Allende): ~2,500
5. **Solo residentes** (modelo conservador). No cuenta trabajadores, tráfico de paso, ni
   anclas (escuelas/plazas) — que SUMAN demanda. Ver §4.

## 3. Resultado — población necesaria en el área

**P = Ventas / c**, por escenario de captura σ:

| Venta/mes | σ=4% (conserv.) | σ=7% (base) | σ=10% (agresivo) |
|---|--:|--:|--:|
| $600,000 | ~102,000 | **~58,000** | ~41,000 |
| $800,000 | ~136,000 | **~78,000** | ~54,000 |
| $1,000,000 | ~170,000 | **~97,000** | ~68,000 |

**Traducción a RADIO** (caso base σ=7%), según densidad de la colonia:

| Venta/mes | Densa ~8k/km² | Suburb. ~4k/km² | Pueblo ~2.5k/km² |
|---|--:|--:|--:|
| $600,000 | ~1.5 km | ~2.2 km | ~2.7 km |
| $800,000 | ~1.8 km | ~2.5 km | ~3.2 km |
| $1,000,000 | ~2.0 km | ~2.8 km | ~3.5 km |

**Lectura:** en caso base necesitas **~58k–97k residentes**, que caben en un radio de
**~1.5–3.5 km** según qué tan densa sea la colonia. Denso (Contry/Tec) = radio chico (~1.5-2
km); suburbano/pueblo = radio más grande (~2.5-3.5 km).

## 4. Sanity check y qué NO cuenta el modelo (importante)

- **Transacciones/día** (ticket $180): $600k→111/día · $800k→148/día · $1M→185/día. Muy
  alcanzable para un QSR (una unidad ocupada hace 300-600+/día). El cuello NO es la cocina;
  es catchment × captura.
- **El modelo es RESIDENCIAL y conservador.** Un QSR también captura: trabajadores, tráfico
  de paso, y **anclas** (escuelas, plazas, supermercados). Por eso el Radar cuenta anclas: una
  colonia con 105 escuelas + Soriana + Cinépolis (ej. El Cercado) rinde MÁS que su población
  residente sola. Un buen sitio sobre avenida con anclas puede lograr la venta con MENOS
  residentes que la tabla.
- **Delivery** extiende el alcance a 5-8 km (apps), pero a 30-35% de comisión — suma población
  alcanzable a menor margen.

## 5. La calibración que lo vuelve real (ley 4/10)

Todo pivotea en **σ (captura)** y **ticket** — ambos [CONFIRMAR]. El mejor calibrador NO es
este modelo: es el **franquiciador**. Preguntas concretas a hacerle (due-diligence):
1. ¿Venta mensual promedio de una sucursal comparable (AUV)?
2. ¿Qué población/trade-area sirve típicamente una unidad?
3. ¿Ticket promedio real y mezcla piso/llevar/delivery?
Con esos 3, se despeja σ real y este marco pasa de estimación a forecast presentable a socios.

## 5-bis. CALIBRADO con datos de Francisco (2026-07-22)

Inputs confirmados por Francisco: **ticket = $220 MXN**; **una sucursal típica sirve
~100,000 personas** (trade-area del franquiciador). Esto CIERRA el modelo.

**A. Con 100,000 personas, ¿qué venta sale según la captura σ?** (Ventas = 100,000 × $147 × σ)

| Captura σ (del gasto QSR) | Venta mensual | Transacciones/día (@$220) |
|---|--:|--:|
| 4% | ~$588,000 | ~89 |
| 5% | ~$735,000 | ~111 |
| 6% | ~$882,000 | ~134 |
| **7% (base)** | **~$1,029,000** | ~156 |

→ La trade-area de 100k del franquiciador, a captura base (7%), soporta **~$1.0M/mes**. El
piso de **$600k solo necesita ~4%** de captura — cómodo. Cada +1% de captura ≈ +$147k/mes.
Penetración implícita para $1M: ~2.3% de los 100k como clientes activos (visita ~2×/mes).

**B. ¿En qué RADIO caben 100,000 residentes?** (R = √(100,000 / π·D))

| Densidad de la colonia | Radio para 100k |
|---|--:|
| Densa (Contry/Tec ~8k/km²) | **~2.0 km** |
| Suburbana (Estanzuela/Valle Alto ~4k) | ~2.8 km |
| Pueblo (Santiago/Allende ~2.5k) | ~3.6 km |

## 5-ter. ⚠️ HALLAZGO que reordena la decisión (ley 9)

**Santiago (46,784 hab) y Allende (35,289 hab) NO tienen 100,000 residentes** — ni en un
radio grande; son municipios chicos (dato Censo 2020, nuestro pipeline). No pueden cumplir la
"sucursal típica de 100k" con residentes. En cambio, el tramo Monterrey del corredor tiene
**241,104 personas** en sus 99 AGEBs (dato Censo), así que **100k caben en ~2 km** en las
colonias densas (Contry, Tecnológico, La Estanzuela).

Esto tensiona el ranking previo del Radar, que favorecía al sur por hueco de frito + encaje
bajo/medio:
- **A favor del sur (Santiago/Allende):** 0 competidores de pollo frito (captura σ MÁS alta al
  no repartir el gasto) · Carretera Nacional = tráfico intermunicipal fuerte · Santiago es
  destino de fin de semana (Pueblo Mágico) · delivery amplía alcance. Estos NO son residentes,
  y el modelo residencial los subestima — pero son reales.
- **A favor del norte denso (Contry/Tec/Estanzuela):** cumple los 100k residentes en ~2 km sin
  depender de tráfico ni turismo. Pero ingreso más alto (peor encaje bajo/medio) y algo más de
  competencia.

**Conclusión honesta:** con la vara de "100k personas por unidad", el sur solo funciona si su
demanda viene de **tráfico + captura alta + delivery**, no de residentes. El norte cumple por
residentes pero pelea encaje y competencia. Esto es exactamente lo que el Radar debe mostrar:
población-en-radio JUNTO A hueco, encaje y anclas — no un solo número.

## 5-quater. Triangulación de los priors del franquiciador (2026-07-22)

Francisco: el ticket $220 y los 100k/unidad **son del franquiciador, pero de BAJA robustez**
(experiencia + algo de análisis). Se tratan como **priors SOFT**, a calibrar contra fuentes
externas. Método de la casa: verificar contra la fuente, no contra la afirmación.

**Ticket $220** → vs QSR MX ~$250-281 [F1]. Está ~12-22% por debajo del promedio QSR:
consistente con "value / bajo-medio, más barato que KFC". **Plausible, riesgo bajo.**

**Trade-area 100k/unidad** → cross-check con ratios población/unidad (conteos públicos [F1],
MX ~130M hab 2024):
- KFC: 375 unidades → ~**347,000** hab/unidad.
- Pollo Feliz: >1,000 unidades → **<130,000** hab/unidad.
→ 100k/unidad es DENSO: ~3.5× más denso que KFC, en zona de Pollo Feliz. Es concebible como
*trade-area urbana* (catchments que se traslapan), pero es el prior **más optimista**. Si el
comportamiento real se parece más a KFC, el catchment efectivo necesario sería mayor a 100k.
Los ratios nacionales mezclan lo rural (subestiman densidad urbana), así que es una cota, no
un veredicto. **Optimista; el input más débil del modelo.**

**Cross-check de AUV:** meta $600k-$1M/mes = ~US$360k-600k/año/unidad (@~20 MXN/USD). Vs
benchmarks EE.UU. 2024 [V]: Campero $3.17M, Cane's $6.56M, Chick-fil-A $7.49M. La meta MX es
~1/5 a 1/10 del AUV gringo — lo esperado para un mercado de precio-valor. **Orden de magnitud
sano.** (Las cadenas MX no publican AUV — KFC no garantiza cifras — por eso se calibra por
ratios, no por un número limpio.)

**Veredicto de robustez para socios:**
- **$600k = piso defendible** (solo ~4% de captura; resiliente aunque los 100k sean optimistas).
- **$800k = base razonable** (~5.4% captura).
- **$1M = upside** — depende de que los 100k Y la captura base (~7%) se cumplan a la vez; el
  input más blando (100k) es justo el que lo sostiene. Presentar como techo, no como base.

## 5-quinquies. Calibración externa LIGERA (2026-07-22, búsquedas dirigidas)

**Ticket $220 → VALIDADO.** Precios KFC MX 2025-26: combos individuales $199-299, bucket para
dos $199, 12 piezas ~$499 [F1, menús KFC]. Un ticket promedio ~$220 (mezcla individual+familiar)
es realista y consistente con "más barato que KFC" (precio por pieza menor; los buckets suben el
promedio). Riesgo bajo.

**Gasto per cápita → CALIBRADO con ENIGH 2024 (INEGI).** Hogares gastaron ~$3,896/trimestre =
**~$1,299/mes/hogar** en alimentos fuera del hogar; ÷ ~3.6 personas ≈ **$361/persona/mes** en
TODO lo que se come fuera (restaurantes, taquerías, calle, QSR). El QSR es un subconjunto → mi
supuesto de **$147/persona/mes en QSR ≈ 41% de eso: plausible**. [F1, ENIGH 2024]
- **Clave para bajo/medio:** los deciles bajos gastan 9.4% de su gasto en comer fuera vs 36% el
  decil 10 [F1, ENIGH]. El segmento bajo/medio gasta MENOS per cápita → su QSR per cápita ronda
  ~**$100-130** (estimación), no $147. Baja la demanda esperada en Allende/Santiago.

**Captura σ → CALIBRADA con market share.** El pollo en QSR ≈ **8% de las ventas del sector
QSR** (2018), de las cuales ~1/3 fue KFC [F1, 2018]. Es decir, el "pastel de pollo frito de
cadena" local vale ~8% del gasto QSR. Entonces:
- σ = captura LOCAL de una unidad bien puesta (mayor que el promedio nacional, que se diluye).
- **Cota dura:** en zona 0-competidores (Santiago/Allende) te acercas a capturar ese ~8% (+ algo
  de sustitución); donde hay KFC/Popeyes lo repartes.
- **Banda σ recalibrada (reemplaza mi 4/7/10% supuesto):** **conservador ~4% · base ~6% ·
  optimista ~8%.** Mi 10% previo era optimista de más (excede el 8% de share del pollo → exigiría
  robar gasto a no-pollo).

**Recálculo con inputs calibrados (100k personas):**
| | per cápita $147 (zona ingreso medio) | per cápita ~$115 (bajo/medio) |
|---|--:|--:|
| σ=4% | $588k | $460k |
| σ=6% (base) | **$882k** | **$690k** |
| σ=8% | $1,176k | $920k |

**Conclusión calibrada:**
- **Doble restricción del sur:** Santiago/Allende no tienen 100k residentes Y su per cápita es
  más bajo → solo llegan a $800k-$1M vía tráfico/turismo/delivery/captura casi-monopólica.
- **El norte denso** (Contry/Tec) sí tiene la población y mayor per cápita, pero σ está disputada
  (KFC presente) y el encaje bajo/medio es peor.
- **El punto óptimo es intermedio:** una colonia **densa-suficiente, ingreso medio, con pocos
  competidores de frito** — ni el norte saturado ni el sur despoblado. Eso es exactamente lo que
  el Radar por colonia debe encontrar. Marco de venta para socios se sostiene: **$600k piso /
  $800k base / $1M upside** (el $1M exige captura casi-monopólica o tráfico alto).

## 5-sexies. POBLACIÓN EN RADIO por colonia — DATO DURO (2026-07-22)

Motor: `extract_poblacion_radio.py`. Suma POBTOT (Censo 2020) de los AGEBs cuyo centroide
cae en el radio. Centroide de AGEB derivado del promedio de coords DENUE (aprox; evita
shapefiles). **Cobertura validada: Monterrey 98.6% · Santiago 97.2% · Allende 99.8%** de la
población censal → método confiable [V-Censo aprox]. Datos vivos en `data/poblacion_radio.json`.

| Colonia | Pob @1.5km | Pob @2.0km | Pob @2.5km | ¿Llega a 100k? | Venta est. @2km* |
|---|--:|--:|--:|:--:|--:|
| **Tecnológico** | 49,673 | **98,753** | 150,505 | Sí (~2 km) | ~$871k |
| **Contry** | 47,008 | 84,405 | 119,905 | Sí (~2.5 km) | ~$744k |
| **San Ángel** | 39,573 | 70,637 | 105,827 | Sí (~2.5 km) | ~$623k |
| La Estanzuela | 38,147 | 46,462 | 57,140 | No | ~$410k |
| Valle Alto | 33,658 | 40,581 | 47,172 | No (premium, baja densidad) | ~$358k |
| La Herradura | 8,687 | 8,708 | 14,554 | No (exclusiva) | ~$77k |
| El Cercado (Santiago) | 10,552 | 13,215 | 15,903 | No | ~$117k |
| Centro de Allende | 11,907 | 18,331 | 22,423 | No | ~$162k |

*Venta estimada = pob@2km × $147/persona/mes × σ 6% (base, ingreso medio). Sin ajuste por
ingreso ni tráfico/turismo/delivery — solo residentes.

**Confirmado con dato duro:**
- El objetivo de **100k solo lo cumplen las colonias densas del norte** (Tecnológico ~99k@2km;
  Contry ~120k@2.5km; San Ángel ~106k@2.5km). Ahí $800k-$1M es alcanzable por residentes.
- **Santiago (El Cercado 13k@2km) y Allende (Centro 18k@2km) están MUY por debajo** de 100k —
  su venta residencial tope ~$117k-$162k/mes. Solo llegan a las metas con **tráfico de
  Carretera Nacional + turismo (Pueblo Mágico) + delivery + captura casi-monopólica** (0
  competidores) — real, pero dependiente de tráfico y más difícil de suscribir.
- **Valle Alto y La Herradura**: pocos residentes (premium/baja densidad) + ingreso alto (mal
  encaje bajo/medio) → descartables para este posicionamiento.

**El punto óptimo intermedio con nombre:** las candidatas que combinan población suficiente +
ingreso no-tan-alto + competencia manejable son **Contry, San Ángel y (con matiz de ingreso)
Tecnológico** — a validar contra su SES exacto y su competencia de frito por colonia (fase
colonias del plan).

## 6. Cómo se conecta al Radar

- Con σ base y la venta objetivo, el Radar puede pintar, por colonia, si su **población en
  radio** alcanza el objetivo — y sumar la demanda de anclas como bono.
- Pinear la **densidad real** por colonia (en vez de las estimaciones del §2.4) requiere los
  polígonos AGEB del Marco Geoestadístico (F4 del plan de colonias) — gratis.
