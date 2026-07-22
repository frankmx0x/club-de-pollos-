# CONCEPTO — Club de Pollos (v0.2)

> La verdad de lo PLANEADO. Nada de software se construye si no está aquí primero.
> Estado: **v0.2** — v0 creada 2026-07-21; v0.1 con el research de mercado
> (`docs/research/2026-07-21-mercado-cdp.md`); v0.2 el mismo día al aclarar Francisco que
> entramos como FRANQUICIATARIOS (ver DECISIONS D-005). Todo hueco marcado
> `[CONFIRMAR CON FRANCISCO]` espera SU dato; nada se inventa.

## 0. Situación de la marca — RESUELTO (DECISIONS D-005, 2026-07-21)

**Club de Pollos es una cadena existente; nosotros entramos como franquiciatarios.** No
creamos la marca (el "cadena que estoy creando" del brief fue error de redacción). Marca
verificada en el research: pollo frito, fundada en Monterrey ~2019, fundadores Arnoldo
Ávila y Abraham Torres, modelo de franquicia, ~70-82 sucursales plausibles.

Implicaciones de operar como franquiciatario (no como creadores de marca):
- La **propuesta de marca, receta y menú los define el franquiciador**; no los inventamos.
- Nuestra palanca competitiva es la **operación**: selección de sitios, ejecución en
  cocina y atención, y **exclusividad territorial** de la zona.
- El instrumento crítico ahora es el **contrato de franquicia** (no el registro IMPI, que
  ya es problema del franquiciador). Due-diligence antes de firmar (ley 6): Claude prepara
  el checklist, Francisco ejecuta.

## 1. Nuestro rol y visión (como franquiciatario)

Grupo franquiciatario dirigido por Francisco (director) con Xavier y Juan.

- Ancla del franquiciador (confirmar contra el contrato): pollo frito, segmento bajo/medio,
  "más rico y más barato que KFC, sin exagerar". Referencia de mercado: ticket QSR MX
  ~$250-281 MXN (2025-26, fuente única — ver research §C).
- Nuestra visión como operador (qué queremos ser en nuestra zona, en una frase de
  Francisco): [CONFIRMAR CON FRANCISCO]
- Por qué ganamos en el corredor sur (sitios, servicio, tiempos) — NO "cómo diferimos de
  KFC", que es tarea del franquiciador: [CONFIRMAR CON FRANCISCO]

## 2. Concepto gastronómico (dado por el franquiciador)

- Producto central: pollo frito. Receta/estilo, menú y guarniciones los fija la marca:
  [CONFIRMAR contra el manual de franquicia]
- Formato de servicio: piso + para llevar + delivery (ancla de Francisco). Dato de research
  que condiciona la operación: las apps retienen 30-35% del ticket — cada peso por app vale
  ~$0.65-0.70 vs piso (verificado). Mezcla de canal objetivo por unidad: [CONFIRMAR CON
  FRANCISCO]
- Ticket real de la marca (por unidad): [CONFIRMAR — dato del franquiciador, no estimar]

## 3. Socios y estructura

- Francisco — Director. Decide.
- Xavier — Socio. Operativo Aux Administrativo. Alcance exacto: [CONFIRMAR CON FRANCISCO]
- Juan — Operativo Gerencial. ¿Socio o empleado?: [CONFIRMAR CON FRANCISCO]
- Reparto económico / equity del grupo franquiciatario: [CONFIRMAR CON FRANCISCO] — al
  definirse, va a DECISIONS.md el mismo día (invariante de negocio con socios).

## 4. Fases y plan de crecimiento (DECISIONS D-005)

- Fase actual: pre-apertura, asegurando la zona y preparando la primera unidad.
- **Territorio a asegurar: zona sur de Monterrey, corredor ITESM → Allende, NL.** Unidades
  de Club de Pollos confirmadas hoy en el metro norte/centro (Escobedo, San Nicolás vía
  Rappi/directorio); NINGUNA confirmada aún en el corredor sur — [CONFIRMAR contra el
  directorio oficial completo si la zona está libre]. Definición municipal/polígono exacta
  para el contrato: [CONFIRMAR — Monterrey sur, y plausiblemente Santiago y Allende].
- **Plan: empezar con 1 franquicia/año y acelerar, hasta 10 unidades en 5-6 años.** Nota
  para el forecast: 1/año lineal daría 5-6 en 5-6 años; llegar a 10 exige que la segunda
  mitad promedie ~2/año (la "aceleración"). Curva año-por-año: [CONFIRMAR CON FRANCISCO]
- Tensión a vigilar en la selección de sitios (ley 9, no relitiga la zona): el corredor de
  Carretera Nacional tiende a ingreso medio-alto en tramos, mientras el posicionamiento es
  bajo/medio. La densidad estudiantil (ITESM) y los centros de Santiago/Allende encajan
  mejor con el ticket bajo/medio. Validar demografía en el micro-sitio, no en el corredor
  como bloque.

Nota de arquitectura ya decidida: aunque la fase 1 sea UNA sucursal, todo el software
lleva `branch_id` desde el día uno (ver reglas/CONSTRUCCION.md). Con 10 unidades a 5-6
años, esto no es teórico.

## 5. Economía de unidad como franquiciatario (marco para el forecast)

Capas del P&L por unidad, sobre lo ya modelado en research §F:

- **Ventas/unidad reales de Club de Pollos**: [CONFIRMAR — dato del franquiciador; es el
  número que gobierna el forecast, más que cualquier benchmark internacional].
- **Cuota inicial de franquicia** (capex de una vez): [CONFIRMAR — no público].
- **Regalías** (% recurrente sobre ventas): [CONFIRMAR — la categoría ronda ~5%, no CdP].
- **Fondo de publicidad** (% recurrente, si aplica): [CONFIRMAR].
- **Inversión por unidad** (obra, equipo): [CONFIRMAR — rango categoría $0.8-2.1M MXN].
- Sobre esas capas aplican food cost (~28-35% estimado industria), renta, nómina, y la
  retención de delivery 30-35% [V]. Sensibilidades del research §F siguen vigentes.

## 6. Sistema de monitoreo (diseño futuro)

Se diseñará aquí ANTES de construirse. Preguntas abiertas para que valga la pena:

- Cocina: ¿qué debe ver el sistema? (tiempos de preparación, mermas, temperaturas,
  cumplimiento de receta, cámaras…): [CONFIRMAR CON FRANCISCO]
- Atención: ¿qué debe ver? (tiempos de espera, quejas, ventas por hora, propinas…):
  [CONFIRMAR CON FRANCISCO]
- ¿Quién lo consume y con qué frecuencia? (Francisco diario, socios semanal…):
  [CONFIRMAR CON FRANCISCO]
- Integraciones previstas (POS, cámaras, WhatsApp, proveedor de AI): [CONFIRMAR CON
  FRANCISCO] — cada una desacoplada en su capa (reglas/CONSTRUCCION.md). Nota de
  franquicia: el franquiciador puede MANDAR un POS/sistema; nuestro monitoreo se acopla a
  lo que exija, no lo reemplaza. [CONFIRMAR qué sistemas obliga la marca.]
- Insumos del research (2026-07-21) para este diseño: (a) medir mezcla y margen POR CANAL
  desde el día uno — apps retienen 30-35% del ticket; (b) las bitácoras obligatorias de
  NOM-251 (temperaturas, limpieza, plagas, recepción de materia prima, capacitación) son
  exactamente nuestra bitácora append-only de eventos → el monitoreo puede generar el
  cumplimiento COFEPRIS como subproducto; (c) alerta de precio del insumo (el pollo puede
  moverse ~9% en una quincena) como señal de primera clase del dashboard financiero.

## 7. Software previsto (además del monitoreo)

Mencionado en el arranque: dashboards, herramientas financieras y de gestión.
Prioridad y alcance de cada una: [CONFIRMAR CON FRANCISCO]

## 8. Radar de Sitios — herramienta de decisión de ubicación (DECISIONS D-006)

Primera pieza de software del proyecto. Propósito: convertir "¿dónde pongo la unidad 1?"
en un **ranking de micro-zonas del corredor sur con evidencia**, no en opinión.

**Capas de datos y quién las aporta:**
| Capa | Fuente | Aporta | Costo |
|---|---|---|---|
| Oferta (competencia) | INEGI **DENUE** (directorio de unidades económicas, coords + giro) | Cada pollo/QSR/rosticería del corredor georreferenciado | Gratis, sin key |
| Demanda (demografía) | INEGI **Censo 2020 por AGEB** | Población, densidad, escolaridad por colonia | Gratis |
| Competencia viva + rating | Google **Places Aggregate API** | Conteos por radio + rating; valida qué del DENUE sigue abierto | Key GCP (preview) |
| Reseñas / debilidades | **Grounding with Maps** (Gemini) | De qué se quejan los competidores por sitio | ~$25 USD/1k |
| Rentas | Portales inmobiliarios (carga manual) | $/m² por tramo | Manual |
| Ground truth | **El franquiciador** | Ventas/unidad reales de zonas análogas | Solo Francisco |

**Análisis (score por punto, no por corredor):** malla de puntos sobre el corredor; cada
punto recibe score = f(demanda en radio, oferta/saturación en radio, encaje bajo/medio,
renta como % de venta, anti-canibalización con futuras unidades 2-10). Cada número lleva
fuente y nivel de confianza ([V]/[F1]/[S]); los huecos se ven como huecos (invariante d:
jamás un ausente disfrazado de 0).

**Fases:**
- **v0** (sin key, gratis): pipeline DENUE + Censo AGEB → mapa/tabla del corredor con
  semáforo por micro-zona. Entregable abrible en el teléfono para la visita de campo.
- **v1** (con key GCP → secret management, jamás al repo): capas Google (abiertos, ratings,
  conteos, reseñas); recálculo del score.
- **v2**: integrado al sistema de gestión, reutilizable para sitios 2-10.

**Honestidad de diseño (ley 4):** el tráfico peatonal real NO existe en API oficial de
Google (los "popular times" no se exponen programáticamente) — era el brillo de mapzot y
tampoco lo tendríamos verificable para MX. Sustituto honesto: anclas de tráfico como proxy
+ **checklist de visita de campo** (conteo manual en hora pico de los 2-3 finalistas). El
Radar reduce 40 km a 3 candidatos; los ojos de Francisco deciden entre esos 3.

**Estado actual:** v0 sembrado con datos [S] rescatados (ver
`docs/research/2026-07-21-corredor-sur.md` y `tools/radar-sitios/`). Bloqueado para datos
completos: INEGI y APIs de Google están vetados por la política de red del entorno
(evidencia: 403 CONNECT en el proxy) — [CONFIRMAR CON FRANCISCO: ampliar allowlist].
