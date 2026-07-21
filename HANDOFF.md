# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-21 (America/Monterrey).
> Sesión: **Etapa 1 — Research de mercado (primera pasada)**. (Etapa 0 — instanciación del
> sistema — cerró el mismo día, commit `2c0a437`.)

## Hecho (con evidencia)

- **Research profundo completado y persistido** en
  `docs/research/2026-07-21-mercado-cdp.md`. Evidencia del proceso: harness de deep
  research con 109 agentes / 26 fuentes / 35 claims extraídos / 25 verificados
  adversarialmente (20 confirmados, 5 refutados), más pasada complementaria de 6 búsquedas
  dirigidas para los módulos sin cobertura (C, D, G). Dos niveles de evidencia marcados en
  el reporte: [V] verificado vs [F1] fuente única.
- **Hallazgo #1 (verificado):** "Club de Pollos" EXISTE como cadena operando (pollo frito,
  fundada MTY ~2019, ~70-82 sucursales plausibles, fundadores en prensa: Arnoldo Ávila y
  Abraham Torres). Disponibilidad/IMPI: [NO VERIFICADO].
- CONCEPTO.md actualizado a v0.1: situación de marca (nueva sección 0), anclas de
  Francisco del 2026-07-21 (pollo frito, bajo/medio, "más rico y más barato que KFC",
  plaza MTY, piso+llevar+delivery, fase pre-apertura), e insumos de research para el
  diseño del monitoreo.
- Los 4 documentos + reglas/ de la Etapa 0 siguen vigentes sin cambios de fondo.

## En vuelo

- **Forecast (research §F): marco paramétrico y sensibilidades listos; escenarios NO
  publicados** — bloqueados por 3 datos de Francisco (relación con la marca, venta/unidad
  de referencia, capital/ritmo). Es deliberado (regla: sin supuestos sostenidos no se
  presenta a socios).
- Research es iterativo: primera pasada entregada, esperando revisión de Francisco para
  decidir qué módulos profundizar (candidatos: IMPI/legal, mapa de saturación ZMM, food
  cost real, fracasos mexicanos documentados).

## Pendientes — de Francisco

1. **LA PREGUNTA #1: relación nuestra con la cadena Club de Pollos existente**
   (¿franquicia / adquisición / somos parte / homónimo independiente?). Gobierna todo;
   si es homónimo independiente hay riesgo legal de marca. Al responderse → DECISIONS.md.
2. Búsqueda formal en IMPI/MarcaNet de "Club de Pollos" (titular, clases 43/29/30) — o
   autorizar que preparemos el instrumento para hacerla (ley 6: research legal delicado,
   Francisco ejecuta).
3. Revisar el reporte (`docs/research/2026-07-21-mercado-cdp.md`) y responder las 10
   preguntas de su sección 4 — en particular ticket objetivo, mezcla de canal, modelo
   propio/franquicia, capital y ritmo.
4. Datos internos si existen: conteo real de sucursales (82) y venta/unidad de referencia.
5. Pendientes heredados de Etapa 0: invariantes de GUIA por afinar; `GIT_AUTHOR_*` vacías
   en el entorno; decidir fusión de la rama de setup a `main`.

## Pendientes — de Claude

- Segunda pasada de research sobre los módulos que Francisco elija (bloqueado por su
  revisión).
- Al responderse la pregunta #1: registrar la decisión en DECISIONS.md y, si aplica,
  correr el protocolo de adopción (reglas/ADOPCION-OSS.md aplica análogamente a adoptar
  una MARCA/negocio existente: licencia→contrato de franquicia, salud→estados de la
  cadena, README vs código→lo dicho vs lo operando).
- Con los 3 datos bloqueantes: publicar escenarios conservador/base/optimista del §F.

## Siguiente paso

Francisco lee el resumen ejecutivo del research y responde la pregunta #1 → sesión
"Etapa 2" (profundización de research dirigida o CONCEPTO v1, según su respuesta).

## Prueba de continuidad

Una sesión nueva sin este chat continúa con: GUIA.md → este HANDOFF → DECISIONS.md →
`docs/research/2026-07-21-mercado-cdp.md` (resumen ejecutivo primero). Todo lo dicho y
hallado hoy está persistido en el repo; ningún dato vive solo en el chat. Los 5 claims
refutados están listados en el research §3 para que nadie los reuse.
