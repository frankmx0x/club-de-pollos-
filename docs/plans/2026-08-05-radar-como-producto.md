# Plan: el Radar como producto — "Cuadrante" (nombre provisional)

**Fecha:** 2026-08-05 (America/Monterrey) · **Estado:** plan aprobado por Francisco para fase 0.
**Registrado en el chat con fuentes; este doc es el instrumento persistido.**

## Tesis

No vendemos datos (son públicos y gratis). Vendemos la **decisión auditable**: análisis de zona
donde cada número se abre con un clic, entregado en días, a fracción del precio de un consultor
de geomarketing ($40-120k MXN [S], semanas). La propiedad diferencial —confianza verificable—
nació de nuestra propia experiencia: 4 errores de clasificación encontrados y corregidos
(D-013, D-014, D-015) gracias a que los números se pueden abrir.

## Clientes (en orden)

1. **Franquiciadores (whitelabel)** — venden ubicaciones a franquiciatarios todo el año.
   Sergio = prospecto #1, ya viendo el demo sin saberlo.
2. **Cadenas regionales 3-50 unidades** — abren 2-10 locales/año; suscripción.
3. **Brokers de locales comerciales** — el reporte justifica rentas.
NO es cliente: el restaurante individual (compra única, no paga suscripción).

## Mercado (bottom-up)

~1,500 marcas de franquicia en MX; ~30% F&B → ~450 franquiciadores F&B [F1: Forbes/AMF/El CEO].
Cadenas regionales no franquiciadas 3+ unidades: ~1,000-2,000 [estimación; contable con DENUE].
Escenario 24 meses: 20 whitelabel × $20k/mes + 60 cadenas × $5k/mes = **$8.4M MXN ARR**.
Encuadre: side-business rentable de 2 personas, NO startup de VC. Techo conocido.

## Moat

1. Curaduría codificada de los errores del DENUE/SCIAN (D-013/14/15) — el competidor nuevo se
   come los mismos bugs y su cliente no puede detectarlos sin drill-down.
2. El drill-down como estándar de la categoría (vs PDF caja negra del consultor).
3. Calibración acumulada con AUVs reales de clientes (dato no público; se aprecia con escala).

## Productos y precios (hipótesis a validar en fase 1)

| Producto | Cliente | Precio |
|---|---|---|
| Reporte de zona | cualquiera | $9,500 MXN / corredor |
| Expansión (suscripción) | cadenas | $4,900 MXN/mes por ciudad |
| Whitelabel | franquiciadores | desde $19,500 MXN/mes |

Costo marginal de reporte: ~medio día (curar lista de colonias; el resto es pipeline).

## GTM por fases con puertas

- **Fase 0 (→4 sem):** arreglar modelo de venta (descuento por competencia — bloqueante para
  cobrar); leer la reacción de Sergio (experimento #1, ya corriendo); landing + lista de espera.
  Salida: 3 conversaciones con franquiciadores/cadenas ≠ Sergio. Cero código nuevo antes.
- **Fase 1 (mes 2-3):** 3 reportes piloto COBRADOS (aunque sea $4,500 c/u); cobertura ZMM
  completa. Salida: 3 pagos + 1 LOI de whitelabel.
- **Fase 2 (mes 4-6):** si pasó F1 → automatizar generación, CDMX+GDL, evaluar entidad legal.
  Si no pasó → archivar sin drama; queda como herramienta interna.

**Kill criteria:** sin 5 clientes de pago o 1 whitelabel firmado en 6 meses → se archiva.
Riesgo #1 = distraer de abrir la primera sucursal (el negocio real).

## Riesgos

Foco (mitigado con fases/kill criteria) · DENUE semestral (venderlo como censo semestral) ·
modelo de venta cojo (se arregla en F0) · replicabilidad teórica (moat §arriba) ·
dependencia de Claude como único dev (pipeline simple, documentado en repos + DECISIONS).

## Siguiente acción

Landing "Cuadrante" con demo sobre datos reales del corredor (sin backend) + lista de espera.
