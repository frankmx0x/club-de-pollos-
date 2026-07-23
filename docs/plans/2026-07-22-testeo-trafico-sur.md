# Plan de testeo — validar el multiplicador de tráfico/turismo del sur

**Fecha:** 2026-07-22 (America/Monterrey) · **Para:** Francisco.
**Objetivo:** medir si el flujo de visitantes/tráfico a Santiago/El Cercado/Allende aporta el
**~5× sobre la base residencial** que el sur necesita para llegar a $600k-$800k/mes (ver
`docs/analysis/2026-07-22-catchment-poblacion-radio.md`). Convierte una hipótesis en dato.

## Lo que YA sabemos (con fuente)

- **Santiago es destino de DÍA, no de pernocta:** ocupación hotelera ~25% anual (vienen de
  Monterrey, a 30 km) [scielo, estudio territorial del turismo en Santiago]. → Los visitantes
  COMEN y se van: bueno para un QSR.
- **Perfil del visitante (SECTUR 2014):** 99% nacional; interés principal = recreación
  (comer en restaurantes, comprar); gasto promedio **~US$60/persona/visita**. La comida es
  actividad central del paseo.
- **Escala estatal (referencia, NO Santiago-específico):** Semana Santa 2025, NL estimó
  **136,000 turistas hospedados** y derrama **$1,282 MDP** [NL Gob / Nitu]. Ojo: "hospedados"
  excluye a los day-trippers de Santiago → subestima su flujo real.
- **Indicador propio [V-DENUE]:** El Cercado tiene 1 restaurante por 102 residentes vs
  Monterrey 1 por 158 → ~1.5× más oferta F&B por residente (señal de demanda no-residente,
  moderada y confundida con ingreso bajo).

**Conclusión:** el flujo es real pero **no hay conteo público de visitantes de Santiago**; hay
que medirlo. Abajo, cómo.

## Qué nos hace falta — 3 capas

### A. Desk (Claude puede perseguir, gratis)
1. **SICT — Datos Viales 2025** → TDPA (Tránsito Diario Promedio Anual) de Carretera Nacional
   en el tramo del sitio candidato: vehículos/día que pasan frente al local.
   Fuente: micrs.sct.gob.mx (Dirección Gral. de Servicios Técnicos, Datos Viales 2025).
2. **NL — Observatorio de Turismo Sostenible + DATATUR** → visitantes y estacionalidad de
   Santiago por mes. Fuentes: nl.gob.mx/observatorioturistico; DATATUR "Turismo en Cifras".
3. **Cola de Caballo / Presa de la Boca** → el parque COBRA entrada, así que tiene conteo real
   de afluencia. Dato no público pero existe: se pide al parque/municipio de Santiago.
4. **Perfil de gasto** (SECTUR ~US$60/persona, % en comida) → cuánto vale un visitante.

### B. Campo (Francisco/equipo ejecuta — EL instrumento)
Conteo en el/los sitios candidatos, sobre la avenida/ruta:
- **Cuándo:** 2 sábados + 1 domingo (temporada normal) + 1 día entre semana (línea base). Si
  se puede, 1 fin de semana largo. Franjas de comida: **13:00-15:00 y 18:00-20:00**.
- **Qué contar** (ventanas de 15 min, extrapolar a día/semana):
  - Vehículos que pasan frente al punto.
  - Peatones.
  - **% con placa foránea / de otra ciudad** (proxy visitante vs local).
  - Autos/personas que se detienen en food cercano.
- **Observar competencia vecina:** fila/aforo en pico, ticket aproximado, horas fuertes.
- **Registrar contexto:** clima, evento especial (festival, Cielo Mágico) para no sesgar.
- Plantilla de captura (rellena en campo):

| Fecha | Día | Franja | Autos/15min | Peatones/15min | %placa foránea | Se detienen a comer | Notas |
|---|---|---|---|---|---|---|---|

### C. Herramienta (opcional, acelera y valida sin ir)
- **Google Places "popular times"** de las anclas (Cola de Caballo, Soriana Los Cavazos, plaza
  de Santiago): curva de afluencia por hora/día. Gratis manual en la app de Maps; o vía
  Places API (requiere key GCP → a secret management).

## Cómo se convierte en VEREDICTO

```
venta_visitante/mes ≈ (visitantes o autos-que-paran por día) × %-que-come × captura × ticket
venta_total = venta_residencial (ya calculada) + venta_visitante
```
Y el back-solve ya lo tenemos: El Cercado necesita **~5.4×** su base residencial ($111k) para
$600k. La pregunta que el conteo responde: **¿el tráfico medido da para ese 5×?** Si sí, el sur
es viable; si no, el norte (Contry) es el camino seguro.

## Resultados del DESK PASS (2026-07-22)

Lo que se obtuvo y lo que NO (honesto):
- **Macro (con fuente):** Semana Santa 2026, NL esperaba **>700,000 personas** en parques del
  estado, con **Cola de Caballo entre los de mayor afluencia** [NL Gob]; SS2025 = 136k
  hospedados / $1,282 MDP (estatal). Perfil: day-trip, ~US$60/persona, comida central.
- **Fuentes de la cifra dura CONFIRMADAS, pero portal-gated:**
  - **TDPA de la carretera:** SICT `appdatosviales.sctcloud.com.mx` (portal interactivo:
    mapa → estación de Carretera Nacional/Fed. 85 → TDPA + histórico 2009-2025, descarga
    PDF/CSV/Excel). **No extraíble por fetch** (portal JS / 403). Pull manual de ~5 min.
  - **Afluencia Cola de Caballo:** el parque cobra entrada → tiene conteo; se pide al
    parque/municipio de Santiago (no público).
  - Prensa y `vialidades.com.mx` devolvieron **403** al fetch.

**Por qué estas dos cifras DECIDEN — la palanca del tráfico (ilustrativo, [estimación]):**
`venta_visitante/mes ≈ TDPA × tasa_captura × ticket × 30`. Los corredores federales
suburbanos suelen traer **decenas de miles de vehículos/día** (a confirmar en SICT):

| TDPA (veh/día) | Captura 0.2% | Captura 0.5% | Captura 1.0% |
|---|--:|--:|--:|
| 15,000 | $198k/mes | $495k/mes | $990k/mes |
| 25,000 | $330k/mes | $825k/mes | $1.65M/mes |
| 40,000 | $528k/mes | $1.32M/mes | $2.64M/mes |

→ Con un flujo de decenas de miles/día, **capturar apenas 0.3-0.5% cierra el 5×** que el sur
necesita. La apuesta se reduce a DOS números medibles: **(1) el TDPA real** (SICT / conteo) y
**(2) la tasa de captura** (conteo de campo: cuántos de los que pasan se detienen y compran).
Caveat: el TDPA es promedio anual; el turismo se concentra en fin de semana → la venta es
grumosa (findes fuertes, entre semana floja) → por eso se combina con base residencial.

## Reparto (ley 6: Claude prepara, Francisco ejecuta)

- **Claude (desk):** perseguir TDPA (SICT), visitantes (Observatorio NL/DATATUR), y afinar el
  modelo con esos números. [siguiente paso inmediato si Francisco lo aprueba]
- **Francisco/equipo (campo):** el conteo con la plantilla, en el/los sitios finalistas del sur.
- **Opcional:** capa Google Places (popular times) — necesita key GCP.
