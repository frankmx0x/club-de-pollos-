# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-07-21 (America/Monterrey).
> Sesión: **Etapa 0 — Instanciación del sistema de trabajo**.

## Hecho (con evidencia)

- Repo `frankmx0x/club-de-pollos-` inicializado en rama `claude/club-de-pollos-setup-975vyg`
  con los 4 documentos + `reglas/` (LEYES, CONSTRUCCION, ADOPCION-OSS).
  Evidencia: commit pusheado (ver `git log`).
- DECISIONS.md con D-001…D-004 (sistema de trabajo, repo como fuente de verdad, roles
  declarados, convenciones del entorno).
- Verificado `TZ=America/Monterrey` en el entorno (`date` → 2026-07-21 CST).

## En vuelo

- CONCEPTO.md está en **v0 esqueleto**: estructura completa, pero todos los datos de
  negocio marcados `[CONFIRMAR CON FRANCISCO]`. No se construye software hasta que
  Francisco responda las preguntas de arranque (abajo).

## Pendientes — de Francisco

1. **Responder las preguntas de CONCEPTO.md v0** (están embebidas en el documento):
   visión y diferenciador; concepto gastronómico (producto, formato, rango de precio);
   fase actual; plaza de la primera sucursal y N previstas; qué debe ver el monitoreo
   de cocina y de atención, quién lo consume; alcance de roles de Xavier y Juan
   (¿Juan es socio?) y acuerdos económicos/equity si ya existen.
2. Afinar las invariantes mínimas de GUIA.md (están marcadas "afinar con Francisco").
3. Entorno: `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL` están VACÍAS en este entorno (el brief
   las daba por configuradas). Los commits salen como "Claude" del entorno gestionado.
   Si quieres otra autoría, configúralas en la config del entorno de Claude Code.
4. Decidir si esta rama se fusiona a una rama por defecto (`main`) — el repo nació
   vacío, sin main; hoy todo vive en la rama de setup.

## Pendientes — de Claude (bloqueados por lo de arriba)

- Volcar respuestas de Francisco a CONCEPTO.md v1 y registrar en DECISIONS.md lo que
  constituya decisión (mismo día si toca acuerdos entre socios).
- Cuando haya primer software: instanciar gate de verificación en CI (versiones
  pineadas) según reglas/CONSTRUCCION.md.

## Siguiente paso

Francisco responde las preguntas de arranque → sesión "Etapa 1 — CONCEPTO v1" que
llena CONCEPTO.md, registra decisiones y define la primera pieza de software (si toca).

## Prueba de continuidad

Una sesión nueva sin este chat puede continuar leyendo, en orden: GUIA.md → este
HANDOFF → DECISIONS.md. Todo lo dicho en el chat de arranque está persistido en estos
documentos; ningún dato de negocio vive solo en el chat.
