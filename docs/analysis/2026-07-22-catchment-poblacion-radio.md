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

## 6. Cómo se conecta al Radar

- Con σ base y la venta objetivo, el Radar puede pintar, por colonia, si su **población en
  radio** alcanza el objetivo — y sumar la demanda de anclas como bono.
- Pinear la **densidad real** por colonia (en vez de las estimaciones del §2.4) requiere los
  polígonos AGEB del Marco Geoestadístico (F4 del plan de colonias) — gratis.
