# GUIA — Club de Pollos

Documento operativo. Corto a propósito. Reglas detalladas en `reglas/`.

## Qué es este proyecto

**Club de Pollos**: cadena de restaurantes en creación. Además del negocio físico,
aquí se construye el software del proyecto: dashboards, herramientas financieras y
de gestión, y (a futuro) el sistema de monitoreo de cocina y atención.

## Quiénes participan

| Persona   | Rol                                      | Notas |
|-----------|------------------------------------------|-------|
| Francisco | Director. Decide. Único origen de datos duros del negocio. | |
| Xavier    | Socio. Operativo Aux Administrativo.     | Alcance exacto: [CONFIRMAR CON FRANCISCO] |
| Juan      | Operativo Gerencial.                     | ¿Socio o empleado?: [CONFIRMAR CON FRANCISCO] |
| Claude    | Sesión única disciplinada: construye Y se auto-revisa contra las leyes. | Al operar cocina real: constructor + revisor en sesiones separadas. |

## Mapa de documentos

- **GUIA.md** (este) — qué es, quiénes, invariantes, protocolo de sesión.
- **CONCEPTO.md** — la verdad de lo PLANEADO. Nada de software se construye si no está ahí primero.
- **DECISIONS.md** — bitácora append-only de decisiones. Jamás se edita una entrada; se supersede.
- **HANDOFF.md** — estado vivo. Se reescribe en cada cierre de sesión.
- **reglas/LEYES.md** — las 10 leyes del sistema de trabajo.
- **reglas/CONSTRUCCION.md** — anexo de construcción (gates, arquitectura, TDD).
- **reglas/ADOPCION-OSS.md** — protocolo antes de construir sobre un repo ajeno.

## Invariantes mínimas del proyecto

1. Datos duros del negocio (precios, domicilios, permisos, cifras a socios) SOLO los da
   Francisco. Dato faltante = `[CONFIRMAR CON FRANCISCO]`, jamás inventado.
2. TODO acuerdo económico, de equity o de responsabilidades entre socios que pase por el
   chat se registra en DECISIONS.md ese mismo día.
3. Nada está "hecho" sin evidencia. Registro ≠ ejecución.
4. Todo se persiste (commit + push) ANTES de cerrar sesión — lo no guardado no existió.
5. Operaciones delicadas (dinero, legal, borrar, producción): Claude prepara el
   instrumento con dry-run; Francisco ejecuta; la verificación queda en el registro.
6. El repo GitHub privado `frankmx0x/club-de-pollos-` es LA fuente de verdad. Los
   contenedores de sesión son efímeros; solo lo pusheado sobrevive.
7. Jamás un secreto en env vars del entorno ni en el repo. Secretos → manejo de secretos
   de la plataforma de deploy o `.env` gitignored.

(Afinar con Francisco: estas son las mínimas del arranque.)

## Protocolo de sesión

**Apertura** — antes de tocar nada, leer en orden:
1. GUIA.md
2. HANDOFF.md completo
3. DECISIONS.md — entradas recientes

**Trabajo** — UNA etapa por sesión, nombrada, cerrada completa y verificada. Nunca a medias.
Push tras cada commit.

**Cierre** — cuando Francisco diga "cierra sesión":
1. HANDOFF.md actualizado con el estado REAL (hecho con evidencia / en vuelo / pendientes con dueño).
2. Decisiones del día registradas en DECISIONS.md.
3. Pegar el HANDOFF completo en el chat.
4. Confirmar que una sesión nueva, sin este chat, podría continuar solo con los documentos.

**Compactación de contexto** — preservar siempre: temas y archivos de la sesión,
pendientes de la etapa en curso, decisiones tomadas con Francisco.

## Entorno de trabajo (nube)

- `TZ=America/Monterrey` (fechas correctas en DECISIONS y research).
- Contenedor efímero, clon fresco por sesión: push tras cada commit es supervivencia, no estilo.
- Env vars visibles: jamás un secreto ahí.
- Dominios bloqueados por política de red en una etapa de research → se ajusta la política
  para esa etapa (configuración editable, no arquitectura).
