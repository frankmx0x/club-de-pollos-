# Anexo de construcción (aplica en cuanto hay repo — es decir, YA)

## Flujo

- **Push tras CADA commit.**
- **Gate de verificación antes de todo commit**: typecheck + lint + build + suites.
  En CI desde el día uno, con **versiones pineadas exactas**.
- Migraciones de DB: aditivas cuando se pueda, con runbook, y **no se declaran aplicadas
  sin pegar la salida de su verificación**.

## Arquitectura — las 4 que siempre pagan

a) **`branch_id` (sucursal) en TODA tabla y query desde el día uno** — una cadena son
   N cocinas.
b) Toda integración externa (POS, cámaras, proveedor de AI, WhatsApp) **DESACOPLADA en
   su capa**.
c) **Bitácora de eventos APPEND-ONLY para lo operativo**; estado + evento en UNA
   transacción.
d) **Jamás un valor ausente viajando como 0/"" disfrazado de real.**

## TDD con goldens

- Casos reales verificados a mano, congelados en suite.
- RED visto antes del código.
- Al modificar algo verificado, la suite vieja pasa SIN editar asserts.
