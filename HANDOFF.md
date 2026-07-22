# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-21 (America/Monterrey).
> Sesión: **Etapa 2 — Research del corredor + herramientas + Radar de Sitios v0**.
> (Etapa 0 instanciación y Etapa 1 research de mercado cerraron el mismo día.)

## Hecho (con evidencia)

- **Modelo de negocio resuelto (D-005):** somos franquiciatarios de Club de Pollos;
  territorio corredor sur ITESM→Allende; plan 1/año acelerando a 10 en 5-6 años.
- **Research de mercado** (`docs/research/2026-07-21-mercado-cdp.md`) y **del corredor sur**
  (`docs/research/2026-07-21-corredor-sur.md`, nivel [S] rescatado tras fallo de fetch 403).
- **Evaluación de herramientas cerrada (D-006):** mapzot descartado; stack = INEGI DENUE +
  Censo AGEB (gratis) + Google Places Aggregate/Grounding (key GCP) + franquiciador.
  Diseño en CONCEPTO §8.
- **Radar de Sitios v0 construido** en `tools/radar-sitios/`: `radar.html` self-contained
  (abre en teléfono, sin red), `data/seed.json` (datos [S] con fuente y confianza por
  punto), `build.py` (inyecta seed → html, reproducible e idempotente — verificado: 4
  tramos, 2 corridas iguales). Ranking provisional: Allende 68 > Santiago 63 > Carr.
  Nacional 55 > Garza Sada/Tec 42.

## En vuelo / bloqueado

- **BLOQUEO DE RED (evidencia, ley 1):** INEGI (`www.inegi.org.mx`) y APIs de Google están
  **denegadas por la política de red del entorno** — proxy responde `403 CONNECT`
  (`recentRelayFailures`). Es configuración editable, no arquitectura. Sin esto, el Radar
  se queda en datos semilla [S]; con esto, se llena con DENUE + Censo + Places completos.
- **Forecast (§F):** sigue bloqueado por datos del franquiciador (ventas/unidad, términos).

## Pendientes — de Francisco

1. **Ampliar el allowlist de red del entorno** para la etapa de datos: `www.inegi.org.mx`,
   y las APIs de Google Maps Platform (`*.googleapis.com`, `places.googleapis.com`,
   `areainsights.googleapis.com`). Es lo que desbloquea el Radar con datos reales.
2. **Key de Google Cloud** (Places Aggregate + Grounding): al manejo de secretos / `.env`
   gitignored — jamás al repo ni al entorno. Necesaria para v1.
3. **Términos de la franquicia** (ventas/unidad, cuota, regalías, exclusividad del
   corredor, POS obligatorio) — desbloquean el forecast a socios.
4. Confirmar hipótesis del corredor a mano donde importe (¿CdP en el sur? rentas vigentes).
5. Heredados: roles/equity Xavier-Juan (→ DECISIONS); invariantes GUIA; `GIT_AUTHOR_*`
   vacías; fusión de rama a `main`.

## Pendientes — de Claude (desbloqueables al abrir red/key)

- Pipeline real del Radar: descargar DENUE NL (SCIAN 7225 restaurantes) + Censo AGEB del
  corredor; reemplazar seed.json por datos completos; recalcular scores.
- Capa Google (v1): validar abiertos, ratings, conteos por radio, reseñas.
- Checklist de due-diligence de franquicia (instrumento ley 6) cuando Francisco lo pida.

## Siguiente paso

Francisco decide: (a) abrir el allowlist de red para que Claude corra el pipeline real del
Radar; y/o (b) que Claude prepare el checklist de due-diligence de franquicia. El Radar v0
ya es usable en campo tal cual.

## Prueba de continuidad

Sesión nueva sin este chat continúa con: GUIA.md → este HANDOFF → DECISIONS.md
(D-005 modelo, D-006 herramientas) → `docs/research/` (mercado + corredor) →
`tools/radar-sitios/` (correr `python3 build.py`, abrir `radar.html`). Todo persistido;
ningún dato vive solo en el chat.
