# CONCEPTO — Club de Pollos (v0.1)

> La verdad de lo PLANEADO. Nada de software se construye si no está aquí primero.
> Estado: **v0.1** — v0 creada 2026-07-21; actualizada el mismo día con el research de
> mercado (`docs/research/2026-07-21-mercado-cdp.md`). Todo hueco marcado
> `[CONFIRMAR CON FRANCISCO]` espera SU dato; nada se inventa.

## 0. Situación de la marca (hallazgo del research, 2026-07-21)

**"Club de Pollos" existe HOY como cadena operando en México** (verificado): pollo frito,
fundada en Monterrey ~2019, ~70-82 sucursales plausibles en NL/Tamaulipas y expansión,
modelo de franquicia; fundadores identificados en prensa: Arnoldo Ávila y Abraham Torres
(El Mañana, nov-2022). Registro IMPI y disponibilidad de la marca: [NO VERIFICADO].

> ⚠️ **La pregunta que gobierna el proyecto:** ¿cuál es NUESTRA relación con esa cadena?
> ¿Franquicia, adquisición, somos parte del grupo, o proyecto independiente homónimo (=
> riesgo legal de marca)? [CONFIRMAR CON FRANCISCO]. Ninguna decisión de dinero antes de
> resolver esto y la búsqueda formal en IMPI.

## 1. Visión del negocio

Cadena de restaurantes dirigida por Francisco (director) con Xavier y Juan.

- Ancla dada por Francisco (2026-07-21): pollo frito, segmento bajo/medio, "más rico y
  más barato que KFC, sin exagerar". Referencia de mercado: ticket QSR MX ~$250-281 MXN
  (2025-26, fuente única — ver research §C).
- Visión (qué queremos ser, en una frase de Francisco): [CONFIRMAR CON FRANCISCO]
- Diferenciador concreto vs KFC (~375 unidades MX), Pollo Feliz (>1,000, asado), Popeyes
  (en MTY desde 2022, pipeline nacional 300+/10 años): [CONFIRMAR CON FRANCISCO]

## 2. Concepto gastronómico

- Producto central: pollo frito (ancla de Francisco, 2026-07-21). Receta/estilo y
  guarniciones: [CONFIRMAR CON FRANCISCO]
- Formato de servicio: piso + para llevar + delivery (ancla de Francisco). Dato de
  research que condiciona el diseño: las apps retienen 30-35% del ticket — cada peso por
  app vale ~$0.65-0.70 vs piso (verificado). Mezcla de canal objetivo: [CONFIRMAR CON
  FRANCISCO]
- Ticket objetivo con número (por debajo de la referencia QSR ~$250-281): [CONFIRMAR CON
  FRANCISCO]

## 3. Socios y estructura

- Francisco — Director. Decide.
- Xavier — Socio. Operativo Aux Administrativo. Alcance exacto: [CONFIRMAR CON FRANCISCO]
- Juan — Operativo Gerencial. ¿Socio o empleado?: [CONFIRMAR CON FRANCISCO]
- Reparto económico / equity: [CONFIRMAR CON FRANCISCO] — al definirse, va a
  DECISIONS.md el mismo día (invariante de negocio con socios).

## 4. Fases

- Fase actual: pre-apertura, definiendo concepto (ancla de Francisco, 2026-07-21).
- Plaza inicial: Monterrey y área metropolitana (ancla de Francisco). ZMM: 5.34M hab, 18
  municipios (Censo 2020). Zona específica: [CONFIRMAR CON FRANCISCO — con el mapa de
  saturación de la segunda pasada de research enfrente]
- Sucursales previstas a mediano plazo (N y ritmo): [CONFIRMAR CON FRANCISCO — bloquea el
  forecast del research §F junto con capital y venta/unidad de referencia]

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
- Insumos del research (2026-07-21) para este diseño: (a) medir mezcla y margen POR CANAL
  desde el día uno — apps retienen 30-35% del ticket; (b) las bitácoras obligatorias de
  NOM-251 (temperaturas, limpieza, plagas, recepción de materia prima, capacitación) son
  exactamente nuestra bitácora append-only de eventos → el monitoreo puede generar el
  cumplimiento COFEPRIS como subproducto; (c) alerta de precio del insumo (el pollo puede
  moverse ~9% en una quincena) como señal de primera clase del dashboard financiero.

## 6. Software previsto (además del monitoreo)

Mencionado en el arranque: dashboards, herramientas financieras y de gestión.
Prioridad y alcance de cada una: [CONFIRMAR CON FRANCISCO]
