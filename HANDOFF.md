# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-31 (America/Monterrey).
> Sesión: **Etapa 5** — explorador de colonias (42), puntos óptimos multi-colonia,
> auditoría de datos, metodología por métrica, rediseño sin emojis, deploy a prod.

## Repos (dos, con frontera clara)

| Repo | Rol | Rama |
|---|---|---|
| `frankmx0x/club-de-pollos-` | **Fuente de verdad**: documentos, decisiones, pipeline de datos | `claude/club-de-pollos-setup-975vyg` |
| `frankmx0x/club-pollos-radar` | App de presentación (React) | `main` |

Flujo: pipeline python (este repo) → `tools/radar-sitios/sync_app.sh` → `public/data/app_data.json`
del app. **Los datos nunca se editan a mano en el app** (D-010).

## Hecho (con evidencia)

- **Sistema de trabajo instanciado** (GUIA, CONCEPTO, DECISIONS, HANDOFF + `reglas/`).
- **Research de mercado y del corredor** (`docs/research/`). Somos **franquiciatarios**
  (D-005), territorio ITESM→Allende, plan 1/año → 10 en 5-6 años.
- **Pipeline de datos** (`tools/radar-sitios/`, todo gratis, sin key): DENUE (241
  competidores + 1,183 anclas), Censo 2020 AGEB, OSETUR, SICT. Nuevo esta sesión:
  - `colonias.json` — lista canónica de **42 colonias** (único input curado a mano).
  - `extract_colonias.py` — catchment 2 km por colonia: competencia (pollo/frito/
    restaurantes/hamburguesas/pizza), anclas, demografía, turismo, venta estimada.
  - `extract_puntos_optimos.py` — **población ÚNICA a 2 km** por candidato (sin doble
    conteo; los círculos vecinos se traslapan). Top: Tec+Altavista+Roma 101,570 (4 fritos);
    **Altamira+Sierra Ventana+Burócratas+Contry 83,629 (1 frito)** ← el sweet spot.
  - `audit_datos.py` — **auditoría adversarial** (10 checks, camino de código independiente)
    que re-deriva los números del app desde las fuentes crudas. Motivo: Lovable inventó
    datos (D-010). Estado: **10 PASS**.
  - `insights.json` (12 insights con evidencia) + `metodologia.json` (fórmula/fuente/
    confianza de CADA número del app).
- **App Radar v3** (rediseño con reglas de Francisco: sin emojis, márgenes, simetría,
  copy mínimo): explorador de 42 colonias ordenable con **estrellas de finalistas**
  (los socios marcan, el app no dictamina), capa de puntos óptimos en el mapa (círculo
  2 km + popup "sirve a"), card de metodología, insights expandibles. Commits `90d8fb1`,
  `de8099c`. Gate `tsc + build` en verde; auditoría de bundle byte a byte.
- **Deploy propio a Cloudflare Workers ACTIVADO**: Francisco cargó los 2 secrets; el
  workflow fallaba porque la action instalaba wrangler 3.90 (no lee `wrangler.json`);
  anclado a 4.116.0 en `1f4d91a`. URL de prod: ver `DEPLOY.md` del app / última corrida
  de Actions.

## Los dos finalistas de sitio (decisión pendiente de Francisco)

| | **Contry** | **El Cercado (Santiago)** |
|---|--:|--:|
| Venta residencial est. | **$810k** | $111k |
| + turismo (Cola de Caballo, 30,673 vis/mes) | — | **$337k → $448k total** (a 8%: $651k) |
| Competencia frito 2 km | 2 | **0** |
| Escolaridad (encaje bajo/medio) | 12.9 (alto) | 10.8 (medio) |
| TDPA | — | ~27,144 veh/día (SICT 2014 +40%) |

Además, del análisis de puntos óptimos: un local en **Altamira/Sierra Ventana** sirve a
83,629 personas únicas con 1 solo competidor de frito — combina volumen de Contry con
hueco competitivo. Los socios marcan finalistas con estrellas en el explorador del app.

## Pendientes — de Francisco

1. **Decidir sitio** con los socios usando el explorador (estrellas → shortlist).
2. **Conteo de campo** para la tasa de captura (única incógnita del modelo) — plan en
   `docs/plans/2026-07-22-testeo-trafico-sur.md`.
3. **Desconectar Lovable del repo del app** una vez confirmado el deploy propio en verde
   (Lovable aún puede pushear a `main`).
4. **Términos de la franquicia** (AUV real, regalías, exclusividad, POS) → forecast a socios.
5. Viejos: roles/equity Xavier/Juan (→ DECISIONS); `GIT_AUTHOR_*` vacías; fusionar rama
   de setup a `main` en el repo de datos.

## Pendientes — de Claude

- Verificar corrida de deploy post-fix `1f4d91a` en verde y registrar la URL de prod aquí.
- Capa Google Places (ratings/abiertos) — requiere key GCP en secret management.
- Renta real por zona (hoy sigue en `[S]`, único dato no duro del Radar).

## Siguiente paso

Confirmar deploy en verde → compartir URL de prod a los socios → sesión de estrellas
(shortlist de colonias) → visita de campo con el plan de conteo.

## Prueba de continuidad

Una sesión nueva sin este chat continúa con: `GUIA.md` → este HANDOFF → `DECISIONS.md`
(D-001…D-011) → `docs/analysis/` y `docs/research/` → `tools/radar-sitios/` (correr
`extract_denue.py`, `extract_colonias.py`, `extract_puntos_optimos.py`, `audit_datos.py`,
`build_appdata.py`, `sync_app.sh`; DENUE/Censo se re-descargan al scratchpad — el
contenedor es efímero). El app se clona de `frankmx0x/club-pollos-radar` y se verifica
con `bunx tsc --noEmit && bun run build`. Todo está pusheado; ningún dato vive solo en
el chat.
