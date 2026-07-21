# CONCEPTO — Club de Pollos (v0)

> La verdad de lo PLANEADO. Nada de software se construye si no está aquí primero.
> Estado: **v0 esqueleto** — creado 2026-07-21 con lo dicho por Francisco en el arranque.
> Todo hueco marcado `[CONFIRMAR CON FRANCISCO]` espera SU dato; nada se inventa.

## 1. Visión del negocio

Cadena de restaurantes en creación por Francisco (director) con Xavier y Juan.

- Visión (qué queremos ser, en una frase de Francisco): [CONFIRMAR CON FRANCISCO]
- ¿Qué hace diferente a Club de Pollos de las cadenas de pollo existentes?:
  [CONFIRMAR CON FRANCISCO]

## 2. Concepto gastronómico

El nombre sugiere pollo como eje, pero el detalle NO está definido aquí todavía:

- Producto central y estilo (¿asado, frito, ambos?; ¿receta propia?): [CONFIRMAR CON FRANCISCO]
- Formato de servicio (comedor / para llevar / domicilio / mixto): [CONFIRMAR CON FRANCISCO]
- Ticket y posicionamiento de precio (rango, no cifras finas aún): [CONFIRMAR CON FRANCISCO]

## 3. Socios y estructura

- Francisco — Director. Decide.
- Xavier — Socio. Operativo Aux Administrativo. Alcance exacto: [CONFIRMAR CON FRANCISCO]
- Juan — Operativo Gerencial. ¿Socio o empleado?: [CONFIRMAR CON FRANCISCO]
- Reparto económico / equity: [CONFIRMAR CON FRANCISCO] — al definirse, va a
  DECISIONS.md el mismo día (invariante de negocio con socios).

## 4. Fases

- Fase actual (¿idea, local en búsqueda, local firmado, en obra, operando?):
  [CONFIRMAR CON FRANCISCO]
- Primera sucursal — plaza/ciudad prevista: [CONFIRMAR CON FRANCISCO]
- Sucursales previstas a mediano plazo (N y dónde): [CONFIRMAR CON FRANCISCO]

Nota de arquitectura ya decidida: aunque la fase 1 sea UNA sucursal, todo el software
lleva `branch_id` desde el día uno (ver reglas/CONSTRUCCION.md).

## 5. Sistema de monitoreo (diseño futuro)

Se diseñará aquí ANTES de construirse. Preguntas abiertas para que valga la pena:

- Cocina: ¿qué debe ver el sistema? (tiempos de preparación, mermas, temperaturas,
  cumplimiento de receta, cámaras…): [CONFIRMAR CON FRANCISCO]
- Atención: ¿qué debe ver? (tiempos de espera, quejas, ventas por hora, propinas…):
  [CONFIRMAR CON FRANCISCO]
- ¿Quién lo consume y con qué frecuencia? (Francisco diario, socios semanal…):
  [CONFIRMAR CON FRANCISCO]
- Integraciones previstas (POS, cámaras, WhatsApp, proveedor de AI): [CONFIRMAR CON
  FRANCISCO] — cada una desacoplada en su capa (reglas/CONSTRUCCION.md).

## 6. Software previsto (además del monitoreo)

Mencionado en el arranque: dashboards, herramientas financieras y de gestión.
Prioridad y alcance de cada una: [CONFIRMAR CON FRANCISCO]
