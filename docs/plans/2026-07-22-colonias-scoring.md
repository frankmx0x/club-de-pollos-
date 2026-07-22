# Plan de implementación — Score por COLONIA (Radar de Sitios)

**Fecha:** 2026-07-22 (America/Monterrey) · **Estado:** propuesta, pendiente de aprobación de Francisco.
**Motivo:** una franquicia se ubica en una colonia (Contry, El Cercado…), no en "el corredor".
La colonia es la resolución real de la decisión. Verificado factible contra DENUE + Censo
(ver desglose en el chat: Contry 613 unidades / 8 pollo, Valle Alto 100 / 0 frito, etc.).

## 0. Qué cambia y qué NO

- **Cambia:** la unidad scoreada pasa de **4 zonas → ~12-15 colonias nombradas**. Las 4 zonas
  quedan como "tramo" de contexto (agrupación). El ranking del app lista colonias.
- **NO cambia:** el modelo de score (misma fórmula huecoFrito/encaje/demanda), el mapa base,
  las fuentes, el flujo (pipeline en repo → app_data.json → Lovable). Se extiende, no se tira.

## 1. Decisiones que requieren a Francisco (datos duros del negocio, ley 4/10)

1. **Lista canónica de colonias** (cuáles scorear). Propuesta inicial (de los datos + su lista):
   - **Monterrey/tramo norte-medio:** Contry · Tecnológico/Altavista · La Estanzuela · Valle
     Alto · La Herradura · Las Misiones · San Ángel · Roma/Sierra Ventana.
   - **Santiago:** El Cercado · Centro de Santiago.
   - **Allende:** Centro de Allende · San Javier.
   → Francisco agrega/quita. [CONFIRMAR CON FRANCISCO]
2. **Proxy de demanda a nivel colonia.** Recomendación: **densidad de anclas** (escuelas +
   supermercados alrededor), más precisa que población por colonia (que es difusa). Alternativa:
   población aprox por AGEBs. [CONFIRMAR — recomiendo anclas]
3. **Mantener las 4 zonas como contexto** (agrupar el ranking por tramo): recomendado sí.
   [CONFIRMAR]

## 2. Modelo de datos (por colonia)

```
colonia = {
  id, nombre_canonico, tramo, municipio,
  fragmentos: [<asentamientos DENUE que la componen>],   # curado
  agebs: [(loc, ageb)...],                                # derivado de sus fragmentos
  centroide: {lat, lon},                                  # media de sus establecimientos (marcador)
  competencia: { pollo_total, pollo_frito_directo, fritos[], indirecta[] },  # V-DENUE
  anclas: { escuela, supermercado, banco, farmacia, gimnasio },              # V-DENUE
  demografia: { poblacion_aprox, escolaridad, pct_internet, pct_auto, ingreso, n_agebs },  # V-Censo aprox
  demanda_proxy,                                          # densidad de anclas (o pob)
  subscores: { huecoFrito, encaje, demanda }, score
}
```

## 3. Pipeline (nuevo `extract_colonias.py`, mismo patrón que anclas)

1. **Config curada `colonias.json`** (hecho a mano, aprobado por Francisco): nombre canónico →
   { tramo, municipio, fragmentos: [strings de asentamiento], aliases }. Es el único input humano.
2. **Match:** por cada establecimiento del corredor (DENUE), normaliza su `nomb_asent` y mapéalo
   a su colonia canónica vía `fragmentos`. Lo no mapeado cae en "otras" (se reporta el % de
   cobertura — no se esconde).
3. **Agrega por colonia:** competidores (pollo/frito/lista), anclas por categoría, set de AGEBs,
   centroide (media lat/lon).
4. **Demografía:** por cada colonia, agrega el Censo sobre su set de AGEBs (escolaridad ponderada
   por población, %auto, %internet, población sumada). Marca `n_agebs`; si es 1-2, banderea
   "muestra chica".
5. **Demanda:** densidad de anclas (escuelas+supermercados) por colonia, normalizada.
6. **Salida:** `data/colonias_corredor.json`.

## 4. Scoring

- Sub-scores por colonia: `huecoFrito = 100*(1 - frito/max_frito)`; `encaje = normaliza
  escolaridad (menor=mejor)`; `demanda = normaliza densidad de anclas`. Rangos min/max
  **recalculados sobre el conjunto de colonias** (no los de las 4 zonas).
- Fórmula ponderada idéntica (wHueco/wEncaje/wDemanda) — los sliders del app siguen igual.

## 5. Empaquetado y app

- `build_appdata.py`: emitir `colonias[]` como unidad scoreada (además de `zonas[]` como
  contexto/tramo). Bump `_meta.version`. Regenerar `app_data.json`.
- **App (Lovable):**
  - Ranking lista **colonias**, agrupadas por tramo (colapsable) por ser ~12-15.
  - Mapa: marcador por colonia en su centroide con su score; clic → detalle (misma estructura).
  - Detalle por colonia: competencia, anclas, demografía (con nota "aprox por AGEB"), demanda,
    score_notas, sub-scores. Etiquetas de confianza: competencia/anclas V-DENUE, demografía
    **V-Censo aprox**.
  - Sliders/modelo intactos.

## 6. Fases

- **F1 — Datos:** curar `colonias.json` (Francisco aprueba) → `extract_colonias.py` →
  `colonias_corredor.json`. Verificar conteos y % de cobertura antes de seguir. (sin key)
- **F2 — Score + empaque:** scoring por colonia + `build_appdata.py` → `app_data.json`.
- **F3 — App:** actualizar ranking + mapa + detalle a nivel colonia en Lovable (prompt).
- **F4 — (opcional, después):** polígonos de colonia/AGEB (Marco Geoestadístico) para choropleth
  real en vez de marcadores de centroide.

## 7. Riesgos y mitigaciones

- **Curación de fragmentos** (Contry×4, Valle Alto×4…): esfuerzo manual; se mitiga empezando con
  ~12-15 colonias y reportando cobertura.
- **Demografía por colonia aprox** (colonias ≠ AGEBs): se marca V-Censo **aprox** + n_agebs; no se
  presenta como exacta.
- **Población por colonia poco fiable** → usar densidad de anclas como demanda (decisión #2).
- **Saturación del mapa** con más marcadores → agrupar/clusterizar; ranking por tramo.
- **Refactor del app** (ranking/detalle para N colonias) → cambio acotado en Panel + SiteMap.

## 8. Registro

Al aprobar Francisco la lista y el proxy de demanda: entrada en DECISIONS (unidad scoreada =
colonia; proxy de demanda = densidad de anclas) el mismo día. Este plan queda en
`docs/plans/` como referencia.
