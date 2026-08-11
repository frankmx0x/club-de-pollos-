# HANDOFF — estado vivo

> Reescrito en cada cierre de sesión. Última actualización: 2026-08-10 (America/Monterrey).
> Sesión: **Etapa 6** — explorador de colonias (42), puntos óptimos multi-colonia,
> auditoría de datos, metodología por métrica, rediseño sin emojis, deploy a prod.

## Repos (dos, con frontera clara)

| Repo | Rol | Rama |
|---|---|---|
| `frankmx0x/club-de-pollos-` | **Fuente de verdad**: documentos, decisiones, pipeline de datos | `claude/club-de-pollos-setup-975vyg` |
| `frankmx0x/club-pollos-radar` | App de presentación (React) | `main` |

Flujo: pipeline python (este repo) → `tools/radar-sitios/sync_app.sh` → `public/data/app_data.json`
del app. **Los datos nunca se editan a mano en el app** (D-010).

## Hecho (con evidencia)

- **Sistema de trabajo instanciado** (GUIA, CONCEPTO, DECISIONS, HANDOFF + `reglas/`).
- **Research de mercado y del corredor** (`docs/research/`). Somos **franquiciatarios**
  (D-005), territorio ITESM→Allende, plan 1/año → 10 en 5-6 años.
- **Pipeline de datos** (`tools/radar-sitios/`, todo gratis, sin key): DENUE (241
  competidores + 1,183 anclas), Censo 2020 AGEB, OSETUR, SICT. Nuevo esta sesión:
  - `colonias.json` — lista canónica de **42 colonias** (único input curado a mano).
  - `extract_colonias.py` — catchment 2 km por colonia: competencia (pollo/frito/
    restaurantes/hamburguesas/pizza), anclas, demografía, turismo, venta estimada.
  - `extract_puntos_optimos.py` — **población ÚNICA a 2 km** por candidato (sin doble
    conteo; los círculos vecinos se traslapan). Top: Tec+Altavista+Roma 101,570 (4 fritos);
    **Altamira+Sierra Ventana+Burócratas+Contry 83,629 (1 frito)** ← el sweet spot.
  - `audit_datos.py` — **auditoría adversarial** (10 checks, camino de código independiente)
    que re-deriva los números del app desde las fuentes crudas. Motivo: Lovable inventó
    datos (D-010). Estado: **10 PASS**.
  - `insights.json` (12 insights con evidencia) + `metodologia.json` (fórmula/fuente/
    confianza de CADA número del app).
- **App Radar v3** (rediseño con reglas de Francisco: sin emojis, márgenes, simetría,
  copy mínimo): explorador de 42 colonias ordenable con **estrellas de finalistas**
  (los socios marcan, el app no dictamina), capa de puntos óptimos en el mapa (círculo
  2 km + popup "sirve a"), card de metodología, insights expandibles. Commits `90d8fb1`,
  `de8099c`. Gate `tsc + build` en verde; auditoría de bundle byte a byte.
- **PROD EN LÍNEA** (1-ago-2026), independiente de Lovable:
  **https://frankmx0x-club-pollos-radar.francisco-rodriguez-11b.workers.dev**
  Verificado: HTTP 200, `app_data.json` con 42 colonias y 13 insights, y el bundle
  publicado contiene las 7 cadenas del UI nuevo y ninguna de las 4 del viejo.
  Costó tres bugs: wrangler 3.90 no leía `wrangler.json` (`1f4d91a`), wrangler corría
  desde `.output/server` y encontraba dos configs (`d814cc8`), y los secrets no
  llegaban. Se agregó una precondición que verifica las credenciales y falla con
  instrucciones en vez del error críptico de wrangler (`7adc35f`).
- **Rediseño completo del UI** (D-012): la app abre respondiendo "¿dónde abre la
  primera unidad?" en vez de exponer tarjetas de datos. Cuatro vistas: Decisión,
  Mapa, Colonias, Evidencia.
- **Lovable desconectado del repo** (1-ago, confirmado por Francisco). La salida quedó
  completa: editor, build, hosting y acceso al repositorio.
- **Clasificación corregida y conteos auditables (D-013)** — lo detonó una pregunta de
  Francisco sobre cómo categorizamos los restaurantes. El clasificador usaba la descripción
  del SCIAN, que en el 96% de los casos dice "pizzas, hamburguesas, hot dogs y pollos
  rostizados" en una sola cadena. Efecto: 161 de 241 "competidores de pollo" no tenían pollo
  en el nombre. Ahora la categoría sale solo del nombre, por inicio de palabra.
  - Competidores de pollo **241 → 125**; pollo frito **8 → 9** (se recuperó CAPTAIN FRIEND
    CHICKEN, typo del DENUE); alitas y boneless como **categoría propia y visible**: 25.
  - **El hallazgo estrella se debilitó con datos correctos:** colonias con masa y cero pollo
    frito pasaron de 2 a **1** (Las Brisas, con 5 locales de alitas a 2 km). El insight
    `hueco-masa` fue reescrito e incluye la explicación del error.
  - **Drill-down:** cada conteo del app se abre con clic y muestra la lista con el giro del
    INEGI. Padrón de 1,802 restaurantes (164 KB, carga bajo demanda). Conteo y lista salen
    del MISMO cálculo — un primer intento los generó por separado y 171 de 252 descuadraban.
    `audit_datos.py` gana un check que falla si vuelven a discrepar. **Verificado en
    producción: 0 descuadres de 168.**

## El mapa de la decisión (modelo D-016, con descuento por competencia)

| | **Las Brisas** | **El Cercado (Santiago)** | **La Estanzuela** |
|---|--:|--:|--:|
| Venta residencial modelada | **$218k** | $74k | $572k (caso límite: 0 competencia) |
| + turismo (Cola de Caballo) | — | **+$337k → $411k** (a 8% del flujo: $614k) | — |
| Pollo frito / alitas a 2 km | **0** / 5 | **0** / 2 | **0** / 0 |
| Personas a 2 km | 68,000 | 13,215 | 44,674 |
| Supermercados reales | 5 | **0** | 6 |

**Lectura honesta del modelo nuevo:** ninguna colonia llega a $600k solo con su radio
residencial de 2 km. La meta exige trade area mayor, tráfico y delivery — por eso la llamada
del AUV al franquiciador y el conteo de campo son EL siguiente paso, no un refinamiento.
El punto óptimo P3 (Las Brisas + Las Torres + Del Paseo, 70,849 personas únicas, 1 frito)
sigue siendo el mejor equilibrio urbano; La Estanzuela aparece como candidato nuevo por
hueco total, con el caveat del caso límite. Los socios marcan finalistas en el app.

## Pendientes — de Francisco

1. **Decidir sitio** con los socios usando el explorador (estrellas → shortlist).
2. **Conteo de campo** para la tasa de captura, única incógnita del modelo — plan **revisado
   el 1-ago** en `docs/plans/2026-07-22-testeo-trafico-sur.md`: el desk quedó cerrado (TDPA y
   visitantes ya obtenidos) y se corrigió el método — la captura se mide en un **análogo que ya
   opera** (KFC Contry, Church's Allende), no en el terreno vacío, y el flujo en el sitio
   candidato. Grabar video en vez de contar en vivo.
3. **Términos de la franquicia** — AUV real por unidad, regalías, exclusividad del corredor y
   si el POS es obligatorio (define quién es dueño de los datos de venta). Una llamada; sin
   esto no hay forecast que presentar a los socios.
5. Viejos: roles/equity Xavier/Juan (→ DECISIONS); `GIT_AUTHOR_*` vacías; fusionar rama
   de setup a `main` en el repo de datos.

- **Anclas reclasificadas por código SCIAN exacto (D-014)** — Francisco pidió revisar si
  otros datos duros tenían la misma falla que D-013. Tres de cinco la tenían: el prefijo
  `4621` metía **228 minisúperes** junto a 25 supermercados reales; `46411` metía **47
  tiendas naturistas** entre las farmacias; `611` metía escuelas de arte, deporte y
  profesores particulares junto a las primarias, sin separar preescolar de secundaria.
  Bancos y gimnasios estaban limpios. Ahora hay diccionario explícito código → categoría.
  - Las anclas viven en el **mismo padrón** que los restaurantes (2,985 registros): sus
    conteos y sus listas abribles salen del mismo cálculo. **Verificado en producción:
    0 descuadres de 546.**
  - Se auditó también la asignación de colonias por texto: **ningún asentamiento cae en
    dos colonias**; los tokens están limpios. Cobertura 70.7%, ya documentada.
  - **Hallazgo de negocio:** El Cercado no tiene **ni un supermercado** a 2 km (13
    minisúperes) y tampoco alitas ni pollo frito. No hay competencia porque no hay tejido
    comercial: toda su tesis descansa en el flujo de la carretera.
  - Bug propio detectado por la comprobación contra producción: al unificar el padrón,
    `restaurantes_2km` quedó contando también las anclas (Altavista marcaba 953 en vez de
    607). Corregido en `b18cbe1`.

- **Modelo de venta corregido (D-016):** pastel de categoría (8% del QSR) repartido entre
  nosotros + fritos (peso 1) + alitas (0.5). Venta calculada en build_appdata con los mismos
  conteos del padrón; check de auditoría 'venta recomputable'. Metodología del app reescrita
  explicando los tres porcentajes y sus bases.
- **Cuadrante (el Radar como producto):** plan en `docs/plans/2026-08-05-radar-como-producto.md`
  (fases con kill criteria) y landing con demo real sin backend en
  `docs/mockups/2026-08-05-cuadrante-landing.html`. La reacción de Sergio al Radar es el
  experimento #1; señal de whitelabel = que pida usarla para su red.

## Pendientes — de Claude

- **Centro de colonia con pocos establecimientos** (marcado en D-014, sin resolver): el
  centro se promedia con los establecimientos propios de la colonia, y hay colonias con muy
  pocos — Del Paseo Residencial 27, La Herradura 26, Los Cristales 28. Su catchment de 2 km
  cuelga de ese centro y tiene más margen de error que el de Altavista, que tiene cientos.
  Hoy la app las presenta con la misma autoridad. Salidas posibles: usar el centroide del
  AGEB, ampliar los tokens, o marcar la incertidumbre en la app. **Decide Francisco.**
- Capa Google Places (ratings/abiertos) — requiere key GCP en secret management.
- Renta real por zona (hoy sigue en `[S]`, único dato no duro del Radar).

## Siguiente paso

Compartir la URL de prod con Xavier y Juan → sesión de estrellas (cada quien marca sus
finalistas en la vista Colonias) → visita de campo con el plan de conteo para cerrar la
tasa de captura, que sigue siendo la única incógnita grande del modelo.

## Prueba de continuidad

Una sesión nueva sin este chat continúa con: `GUIA.md` → este HANDOFF → `DECISIONS.md`
(D-001…D-014) → `docs/analysis/` y `docs/research/` → `tools/radar-sitios/` (correr
`extract_denue.py`, `extract_colonias.py`, `extract_puntos_optimos.py`, `audit_datos.py`,
`build_appdata.py`, `sync_app.sh`; DENUE/Censo se re-descargan al scratchpad — el
contenedor es efímero). El app se clona de `frankmx0x/club-pollos-radar` y se verifica
con `bunx tsc --noEmit && bun run build`. Todo está pusheado; ningún dato vive solo en
el chat.
