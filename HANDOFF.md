# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-21 (America/Monterrey).
> Sesión: **Etapa 1 — Research de mercado + aclaración de modelo de negocio**.
> (Etapa 0 — instanciación del sistema — cerró el mismo día, commit `2c0a437`.)

## Hecho (con evidencia)

- **Research profundo completado y persistido** en
  `docs/research/2026-07-21-mercado-cdp.md` (harness: 109 agentes / 26 fuentes / 25 claims
  verificados adversarialmente, 20 confirmados / 5 refutados; + pasada complementaria para
  módulos C/D/G). Dos niveles de evidencia marcados: [V] verificado vs [F1] fuente única.
- **Pregunta #1 RESUELTA (DECISIONS D-005):** entramos como **franquiciatarios** de Club
  de Pollos (cadena existente), NO creando la marca. Territorio: zona sur de Monterrey,
  corredor ITESM → Allende NL. Plan: 1 franquicia/año acelerando a 10 en 5-6 años.
  Evidencia de aclaración: mensaje de Francisco, 2026-07-21.
- Verificado (búsqueda dirigida): unidades de CdP en metro norte/centro (Escobedo, San
  Nicolás vía Rappi/directorio oficial); NINGUNA confirmada en el corredor sur → zona
  plausiblemente libre, [CONFIRMAR contra directorio completo]. Términos de franquicia de
  CdP: no públicos (solo rangos de categoría).
- CONCEPTO.md → v0.2: reencuadrado a operar como franquiciatario (sección 0 resuelta, rol
  como operador, territorio y plan de crecimiento, nueva §5 economía de unidad con capas
  de franquicia). Research doc con nota de actualización al inicio (sin reescribir el
  cuerpo — snapshot preservado).

## En vuelo

- **Forecast (research §F): marco y sensibilidades listos; escenarios NO publicados.** El
  cambio a franquicia AFINA qué falta: el número que gobierna ya no son los benchmarks
  internacionales sino **las ventas/unidad reales de Club de Pollos + los términos de
  franquicia** (cuota, regalías, inversión/unidad), todos datos del franquiciador.
- **Research del corredor sur:** primera pasada hecha. La verificación automatizada FALLÓ
  (403 en todas las fuentes hiperlocales); se RESCATÓ la capa de búsqueda a
  `docs/research/2026-07-21-corredor-sur.md`, marcado nivel [S] (snippet, sin verificar).
  Hipótesis principal: norte del corredor (Garza Sada/Tec) saturado de pollo frito; hueco
  hacia el sur; Allende encaja mejor con bajo/medio que Santiago (más ingreso). TODO
  requiere confirmación manual/herramienta antes de decidir sitio.
- **Evaluación de herramientas:** mapzot.ai descartado (cobertura MX no verificable, precio
  enterprise). Google lanzó (2025-26) Grounding-with-Maps (Gemini API, $25/1k prompts),
  Places Aggregate API y Places Insights en BigQuery — **México SÍ cubierto** (preview, top
  cities; Santiago/Allende [CONFIRMAR]). Stack recomendado: Google Places + INEGI (gratis)
  + dato del franquiciador. NO decidido/registrado aún; requiere key de Google Cloud
  (a secret management, no al repo).

## Pendientes — de Francisco

1. **Términos de la franquicia** (del franquiciador, ley 6 — solo los da Francisco):
   ventas/unidad reales, cuota inicial, % de regalías, fondo de publicidad, inversión por
   unidad, y **cláusula de exclusividad territorial** para el corredor ITESM→Allende.
2. Revisar el research (`docs/research/2026-07-21-mercado-cdp.md`, resumen ejecutivo
   primero) y responder las preguntas que siguen vivas: ticket/mezcla de canal por unidad,
   curva de apertura año-por-año, capital disponible.
3. Definición exacta del territorio (municipios/polígono) para el contrato: Monterrey sur
   y ¿Santiago/Allende?
4. Pendientes heredados de Etapa 0: alcance de roles Xavier/Juan y equity del grupo
   franquiciatario (van a DECISIONS al definirse); invariantes de GUIA por afinar;
   `GIT_AUTHOR_*` vacías en el entorno; decidir fusión de la rama de setup a `main`.

## Pendientes — de Claude

- **Instrumento de due-diligence de franquicia** (ley 6): preparar checklist de qué exigir
  y verificar del franquiciador antes de firmar (términos, exclusividad, ventas/unidad,
  qué POS/sistemas obliga la marca, soporte, cláusulas de salida). Es el siguiente
  entregable natural — Francisco lo lleva a la mesa con el franquiciador.
- Segunda pasada de research reordenada por el modelo franquicia: (a) mapa de unidades CdP
  existentes en el corredor sur para confirmar que la zona está libre; (b) demografía por
  micro-zona del corredor (validar bajo/medio vs tramos de ingreso alto); (c) food cost
  real de pollo frito. Bajó prioridad: IMPI (ya es del franquiciador).
- Con ventas/unidad + términos: publicar escenarios conservador/base/optimista del §F
  aterrizados al plan de 10 unidades en 5-6 años.

## Siguiente paso

Decisiones abiertas para Francisco (ninguna tomada aún):
1. **Herramientas:** ¿(a) doc de recomendación de herramientas para DECISIONS con costos y
   modo de adopción, (b) diseño de la consulta de saturación del corredor con Places
   Aggregate + INEGI para correr con key de Google Cloud, o ambos?
2. **Corredor:** el mapa de hipótesis está; el siguiente paso natural es confirmarlo con
   herramienta de mapas (resolvería los 403) o visita de campo.
3. **Franquicia:** checklist de due-diligence al franquiciador sigue pendiente y es el
   entregable que desbloquea el forecast.

## Prueba de continuidad

Una sesión nueva sin este chat continúa con: GUIA.md → este HANDOFF → DECISIONS.md
(D-005 es la decisión que gobierna) → `docs/research/2026-07-21-mercado-cdp.md` (con su
nota de actualización). Todo lo dicho y hallado hoy está persistido; ningún dato vive solo
en el chat. Los 5 claims refutados están en el research §3 para que nadie los reuse.
