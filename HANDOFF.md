# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-23 (America/Monterrey).
> Sesión: **Etapas 0-4** — sistema de trabajo, research, Radar de Sitios (datos + app),
> salida de Lovable y deploy propio.

## Repos (dos, con frontera clara)

| Repo | Rol | Rama |
|---|---|---|
| `frankmx0x/club-de-pollos-` | **Fuente de verdad**: documentos, decisiones, pipeline de datos | `claude/club-de-pollos-setup-975vyg` |
| `frankmx0x/club-pollos-radar` | App de presentación (React) | `main` |

Flujo: pipeline python (este repo) → `tools/radar-sitios/sync_app.sh` → `public/data/app_data.json`
del app. **Los datos nunca se editan a mano en el app** (D-010).

## Hecho (con evidencia)

- **Sistema de trabajo instanciado** (GUIA, CONCEPTO, DECISIONS, HANDOFF + `reglas/`).
- **Research de mercado** (`docs/research/2026-07-21-mercado-cdp.md`) y **del corredor sur**
  (`…-corredor-sur.md`). Hallazgo raíz: somos **franquiciatarios** de una cadena existente
  (D-005), territorio corredor ITESM→Allende, plan 1/año → 10 en 5-6 años.
- **Pipeline de datos** (`tools/radar-sitios/`, todo gratis, sin key):
  `extract_denue.py` (241 competidores + 1,183 anclas), `extract_censo.py` (demografía/SES
  por AGEB), `extract_poblacion_radio.py` (población en radio, cobertura 97-99.8%),
  `rank_colonias.py` (ranking con capa turística), `build_appdata.py`, `sync_app.sh`.
- **Análisis de catchment** (`docs/analysis/2026-07-22-catchment-poblacion-radio.md`):
  ticket $220 y 100k/unidad calibrados y triangulados (D-008, D-009); σ recalibrada a
  4/6/8%; población-en-radio y turismo con dato duro.
- **App Radar v2**: mapa Leaflet + panel + sliders + capas + fuentes. Se edita **directo en
  el repo** con gate `tsc + build` (D-010). Últimos commits: datos reales restaurados
  (`dcedd47`), fix de overflow + pulido (`b1c1a04`), cards por concepto (`d03ba20`),
  CI de deploy (`1c4aa17`).
- **Deploy propio** a Cloudflare Workers vía GitHub Actions (D-011).

## Los dos finalistas de sitio (decisión pendiente de Francisco)

| | **Contry** | **El Cercado (Santiago)** |
|---|--:|--:|
| Venta residencial est. | **$810k** | $111k |
| + turismo (Cola de Caballo, 30,673 vis/mes) | — | **$337k → $448k total** (a 8% captura: $651k) |
| Competencia frito 2 km | 2 | **0** |
| Escolaridad (encaje bajo/medio) | 12.9 (alto) | 10.8 (medio) |
| TDPA | — | ~27,144 veh/día (SICT 2014 +40%) |

- **A · Contry**: volumen residencial predecible; exige flexionar el posicionamiento.
- **B · El Cercado**: fiel a bajo/medio, 0 competidores, turismo verificado; pende de la
  **tasa de captura** (única incógnita) y de un local **sobre la ruta a la cascada**.

## Pendientes — de Francisco

1. **Decidir A o B** (o C: redefinir meta a $200-300k con unidad chica al sur).
2. **Conteo de campo** para la tasa de captura — plan e instrumento listos en
   `docs/plans/2026-07-22-testeo-trafico-sur.md` (2 sáb + 1 dom + 1 entre semana, franjas
   de comida, % placa foránea).
3. **Activar el deploy**: cuenta Cloudflare + `CLOUDFLARE_API_TOKEN` y
   `CLOUDFLARE_ACCOUNT_ID` como secrets de GitHub (pasos en `DEPLOY.md` del app).
4. **Términos de la franquicia** (ventas/unidad reales, regalías, exclusividad del corredor,
   POS obligatorio) → desbloquean el forecast a socios.
5. Pendientes viejos: roles/equity de Xavier y Juan (→ DECISIONS); `GIT_AUTHOR_*` vacías;
   fusionar la rama de setup a `main` en el repo de datos.

## Pendientes — de Claude

- **Limpieza**: reemplazar `@lovable.dev/vite-tanstack-config` por config estándar de Vite
  (habilitaría salida estática + GitHub Pages; hoy el preset `static` falla).
- **Fase colonias** del Radar (`docs/plans/2026-07-22-colonias-scoring.md`): scorear ~12-15
  colonias en vez de 4 zonas. Falta que Francisco apruebe la lista canónica.
- Capa Google Places (ratings/abiertos/reseñas) — requiere key GCP en secret management.
- Renta real por zona (hoy sigue en `[S]`, único dato no duro del Radar).

## Siguiente paso

Francisco decide sitio (A/B/C) y/o activa el deploy con los 2 secrets. Ambas cosas son
independientes: el Radar ya es usable para la decisión y para la visita de campo.

## Prueba de continuidad

Una sesión nueva sin este chat continúa con: `GUIA.md` → este HANDOFF → `DECISIONS.md`
(D-005 modelo de negocio · D-006 stack de datos · D-008/D-009 supuestos · D-010 salida de
Lovable · D-011 deploy) → `docs/analysis/` y `docs/research/` → `tools/radar-sitios/`
(correr los `extract_*.py`, luego `build_appdata.py` y `sync_app.sh`). El app se clona de
`frankmx0x/club-pollos-radar` y se verifica con `bunx tsc --noEmit && bun run build`.
Todo está pusheado; ningún dato vive solo en el chat.
