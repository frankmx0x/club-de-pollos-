# DECISIONS — bitácora append-only

> Formato: fecha (America/Monterrey) · decisión · porqué · qué reemplaza.
> JAMÁS se edita una entrada; se supersede con una nueva que la cita.
> Invariante: TODO acuerdo económico, de equity o de responsabilidades entre socios
> que pase por el chat se registra aquí ese mismo día.

---

## 2026-07-21 · D-001 · Se adopta el sistema de trabajo de Francisco (4 documentos + leyes)

- **Decisión:** El proyecto opera con GUIA.md, CONCEPTO.md, DECISIONS.md, HANDOFF.md,
  y reglas detalladas en `reglas/` (LEYES, CONSTRUCCION, ADOPCION-OSS). Claude opera en
  esta fase como sesión única disciplinada (construye y se auto-revisa); al operar
  cocina real se pasa a constructor + revisor en sesiones separadas.
- **Porqué:** Sistema probado por Francisco en otros proyectos; las leyes están pagadas
  con errores reales.
- **Reemplaza:** Nada (arranque).

## 2026-07-21 · D-002 · Repo GitHub privado como fuente de verdad desde el día uno

- **Decisión:** Los documentos y todo el software viven en el repo git privado
  `frankmx0x/club-de-pollos-` (GitHub). Modelo hub/clones: cada sesión en la nube clona
  fresco a un contenedor efímero; solo lo pusheado sobrevive → push tras cada commit.
  La máquina local de Francisco es un clon opcional más.
- **Porqué:** Se construirá software desde el inicio; el contenedor de sesión es
  efímero y el repo es lo único permanente. Privado porque contiene información de
  negocio y socios.
- **Reemplaza:** Nada (arranque).

## 2026-07-21 · D-003 · Roles operativos declarados por Francisco

- **Decisión:** Francisco = Director (decide; único origen de datos duros del negocio).
  Xavier = socio, Operativo Aux Administrativo. Juan = Operativo Gerencial.
- **Porqué:** Declarado por Francisco en el brief de arranque. Se registra el mismo día
  por la invariante de responsabilidades entre socios.
- **Pendiente explícito:** alcance exacto de cada rol, si Juan es socio o empleado, y
  cualquier acuerdo económico/equity = [CONFIRMAR CON FRANCISCO]. Nada de eso está
  acordado en esta entrada.
- **Reemplaza:** Nada (arranque).

## 2026-07-21 · D-004 · Convenciones del entorno de nube

- **Decisión:** `TZ=America/Monterrey` en el entorno (verificado: `date` →
  2026-07-21 CST). Jamás secretos en env vars del entorno ni en el repo; secretos del
  futuro sistema de monitoreo van al manejo de secretos de la plataforma de deploy o a
  `.env` gitignored. Política de red del entorno se ajusta por etapa de research si
  bloquea dominios necesarios.
- **Porqué:** Env vars del entorno son visibles; fechas correctas en esta bitácora.
- **Reemplaza:** Nada (arranque).

## 2026-07-21 · D-005 · Entramos como FRANQUICIATARIOS de Club de Pollos (no creando la marca)

- **Decisión:** El proyecto NO crea la marca Club de Pollos; entramos como
  **franquiciatarios** de la cadena existente (marca real verificada en el research del
  mismo día: pollo frito, fundada en Monterrey ~2019, fundadores Arnoldo Ávila y Abraham
  Torres). Territorio objetivo a asegurar: **zona sur de Monterrey, corredor ITESM →
  Allende, NL**. Plan de crecimiento: **empezar con 1 franquicia/año y acelerar, hasta
  llegar a 10 unidades en 5-6 años**.
- **Porqué:** Aclarado por Francisco el 2026-07-21. El framing "cadena que estoy creando"
  del brief de arranque fue un error de redacción. Esto resuelve la pregunta #1 del
  research (relación con la marca) y elimina el riesgo legal de marca por homonimia.
- **Reemplaza / corrige:** El supuesto "marca nueva que estamos creando" de CONCEPTO v0 y
  v0.1 y del brief de arranque. Cierra la open question #1 del research
  `docs/research/2026-07-21-mercado-cdp.md` y responde parcialmente sus preguntas #6
  (zona = corredor sur) y #8 (modelo = franquicia).
- **Nota (ley 6 — instrumento delicado, dinero/legal):** firmar la franquicia y asegurar
  la exclusividad territorial es operación de dinero y legal. Claude prepara el
  instrumento (checklist de due-diligence al franquiciador: términos, regalías,
  exclusividad de zona, ventas/unidad reales, capex); Francisco ejecuta la firma. Los
  números finos (cuota inicial, % de regalías, inversión/unidad) SOLO los da Francisco
  desde el franquiciador — [CONFIRMAR].

## 2026-07-21 · D-006 · Stack de datos para decisión de sitio + construir "Radar de Sitios"

- **Decisión:** El análisis de ubicación se construye sobre este stack: **INEGI DENUE +
  Censo 2020 por AGEB (gratis, base)** + **Google Places Aggregate API + Grounding-with-Maps
  (capa de validación/calidad, key GCP)** + **datos del franquiciador (ground truth)**. Se
  descarta **mapzot.ai**. Se difiere **Places Insights en BigQuery** hasta tener varias
  unidades. Se construye en el repo la herramienta **Radar de Sitios** (`tools/radar-sitios/`),
  fases v0 (gratis) → v1 (con key) → v2 (integrado). Diseño en CONCEPTO §8.
- **Porqué:** Google cubre México de forma verificable (lista oficial de cobertura del
  preview incluye México); INEGI es fuente oficial gratuita y baja a nivel AGEB; mapzot no
  tenía cobertura MX verificable y es precio enterprise de venta asistida. El tráfico
  peatonal real no lo da ninguna API oficial → se sustituye con anclas + visita de campo.
- **Reemplaza:** Nada (primera decisión de herramientas). Cierra la evaluación de mapzot.
- **Bloqueo registrado (evidencia, ley 1):** hoy `www.inegi.org.mx` y las APIs de Google
  están **denegadas por la política de red del entorno** — el proxy responde `403 CONNECT`
  (registrado en `recentRelayFailures`). Es configuración editable (no arquitectura); para
  llenar el Radar con datos completos, Francisco amplía el allowlist para la etapa de datos.
  Los secretos (key de Google Cloud) van al manejo de secretos de la plataforma de deploy o
  a `.env` gitignored — jamás al repo ni al entorno.

## 2026-07-21 · D-007 · Radar v2 = web app en Lovable (presentación) sobre datos de NUESTRO repo

- **Decisión:** La web app interactiva del Radar (mapa geográfico + panel + sliders de
  score) se construye en **Lovable** (React) y se conecta a GitHub. **La fuente de verdad
  de los DATOS y el pipeline sigue siendo el repo `club-de-pollos-`**; Lovable es capa de
  PRESENTACIÓN desacoplada (invariante b) que consume un snapshot compacto de nuestros
  datos (`tools/radar-sitios/data/app_data.json`, 241 puntos + 4 zonas, con fecha y
  fuente). El código del app sincroniza a su propio repo de GitHub.
- **Porqué:** Francisco prefiere Lovable (más pulido y rápido de iterar). Conectar a GitHub
  mantiene el código versionado; separar datos (nuestro repo) de presentación (Lovable)
  respeta la invariante de fuente de verdad y evita datos ficticios (ley 4): el app nace
  con datos duros DENUE+Censo.
- **Reemplaza:** Complementa D-006 (stack de datos). El esquema `radar.html` del repo
  queda como vista rápida/offline; el tablero principal pasa a Lovable.
- **Costos/acciones (ley 6):** crear el proyecto consume créditos del workspace de
  Francisco; conectar Lovable↔GitHub es un clic suyo en el editor de Lovable. Cualquier
  key (Google Places, futuro) va al manejo de secretos de Lovable/Supabase, jamás al repo.

## 2026-07-22 · D-008 · Inputs de planeación: ticket $220 y trade-area 100k/unidad

- **Decisión (inputs confirmados por Francisco):** ticket promedio **$220 MXN**; una sucursal
  típica sirve **~100,000 personas** (trade-area de referencia del franquiciador). Se usan
  como supuestos base del modelo de catchment y del forecast.
- **Porqué / implicación:** cierran el modelo de `docs/analysis/2026-07-22-catchment-poblacion-radio.md`.
  Resultado: a captura base (~7% del gasto QSR local) los 100k soportan ~$1.0M/mes; $600k
  necesita ~4%. HALLAZGO (ley 9): Santiago (46,784) y Allende (35,289) NO tienen 100k
  residentes → el sur solo cumple vía tráfico/turismo/delivery/captura alta, no residentes; el
  tramo denso de Monterrey (Contry/Tec/Estanzuela, 241,104 hab en el corredor) cumple 100k en
  ~2 km. Esto reordena la lectura del Radar.
- **Pendiente [CONFIRMAR]:** ¿de dónde viene el ticket $220 y la trade-area 100k — dato del
  franquiciador o meta de Francisco? Idealmente confirmar contra el AUV real de una sucursal
  comparable. La captura σ real sigue por calibrar.
- **Reemplaza:** afina los supuestos [CONFIRMAR] de ticket del research y del §F.

## 2026-07-23 · D-010 · El app se edita DIRECTO en su repo; Lovable deja de ser el editor

- **Decisión:** El código del Radar (`frankmx0x/club-pollos-radar`) se edita **directamente en
  el repo** (clonado en la sesión, commit + push a `main`). **Lovable deja de usarse como
  editor**; queda solo como preview/hosting que sincroniza desde GitHub. Los datos siguen
  saliendo del pipeline de ESTE repo y se copian con `tools/radar-sitios/sync_app.sh`
  (nunca a mano). Gate antes de cada commit del app: `tsc --noEmit` + `vite build`.
- **Porqué (evidencia, ley 1/4):** al integrar la capa turística, el agente de Lovable
  **ignoró el `app_data.json` subido y escribió las cifras a mano, inventándolas**:
  visitantes 30,673→"30,000"; TDPA 2014 19,389→"18,500"; crecimiento +40%→"+45%"; venta
  turismo $337,410→"90,000"; venta total $448,416→"360,000". Un editor que parafrasea datos
  es incompatible con la invariante de que ningún dato se inventa. Además, prompts en
  lenguaje natural no dan control fino de UI ni gate de verificación.
- **Corregido:** commit `dcedd47` en el repo del app restaura la salida real del pipeline y
  cambia los tipos de `Turismo` de string a number (el dato viaja numérico; el formato vive
  en la vista, helper `mxn()`). Verificado: tsc exit 0, build exit 0.
- **Reemplaza:** supersede la parte de **D-007** que ponía a Lovable como constructor del app.
  Se mantiene de D-007: la separación datos (este repo, fuente de verdad) / presentación
  (repo del app), y que las keys nunca van al repo.

## 2026-07-23 · D-011 · Deploy propio a Cloudflare Workers; prod deja de depender de Lovable

- **Decisión:** Producción se publica con **GitHub Actions → Cloudflare Workers** desde el
  repo del app (`.github/workflows/deploy.yml`): cada push a `main` corre
  `bun install → tsc --noEmit (gate) → build → deploy`. El `wrangler.json` lo genera nitro
  en el build (worker `frankmx0x-club-pollos-radar`, assets desde `.output/public`).
  Pasos de puesta en marcha en `DEPLOY.md` del repo del app.
- **Porqué:** cerrar la salida de Lovable (D-010) también en el deploy. Antes NO existía
  prod: el proyecto nunca se publicó (`is_published: false`), solo había preview de Lovable.
- **Secrets:** `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` viven en los secrets de
  GitHub — jamás en el repo ni en el entorno. **Los crea Francisco** (cuenta + token);
  hasta entonces el workflow existe pero no publica.
- **Límite cerrado el mismo día (commit `6bb0bfe`):** se eliminó TODA dependencia de
  Lovable del build. `vite.config.ts` es ahora config estándar de Vite con plugins
  explícitos; hubo que restaurar a mano el preset de nitro (`cloudflare-module`, sin él
  caía a `node-server` y no generaba `wrangler.json`) y el dedupe de React. **Además**,
  `bun.lock` apuntaba 7 paquetes (leaflet y afines) al **registro privado de Lovable**
  (`europe-west1-npm.pkg.dev/lovable-core-prod/sandbox-npm-cache`) en vez de npm público —
  eso rompía `bun install` fuera de su sandbox y habría tumbado el CI; repuntados a
  `registry.npmjs.org`. Verificado: `bun install --frozen-lockfile` desde cero (416
  paquetes), tsc 0, build 0, wrangler.json presente, app renderiza sin errores JS.
- **Salida estática descartada (con evidencia):** el preset `static` —que habilitaría
  GitHub Pages sin cuenta de terceros— NO funciona con TanStack Start + este nitro beta
  (`rollupOptions.input should not be an html file when building for SSR`). Se probó con y
  sin el config de Lovable: el límite es del stack, no de Lovable.
- **Reemplaza:** completa D-010 (que sacó a Lovable del rol de editor) llevándolo también
  fuera del deploy.

## 2026-07-22 · D-009 · Los priors del franquiciador son SOFT; se triangulan con fuentes externas

- **Decisión (método):** Ticket $220 y trade-area 100k/unidad (D-008) provienen del
  franquiciador pero son de **baja robustez** (experiencia + algo de análisis, no estudio
  formal — dicho por Francisco). Se tratan como **priors blandos**, y se calibran/triangulan
  contra fuentes externas públicas (estudios de mercado, ratios de industria). El dato del
  franquiciador NO se toma como verdad; sirve de ancla para calibrar lo externo y viceversa.
- **Triangulación (ver `docs/analysis/2026-07-22-catchment-poblacion-radio.md` §5-quater):**
  ticket $220 consistente con QSR MX $250-281 [F1] (plausible); 100k/unidad es OPTIMISTA
  (KFC opera a ~347k hab/unidad, Pollo Feliz <130k) — es el input más débil; AUV meta
  ~US$360-600k/año sano vs benchmarks. Marco para socios: **$600k piso, $800k base, $1M
  upside** (el $1M pende del prior más blando).
- **Sobre mapzot.ai (re-mencionado):** se mantiene descartado (D-006) — cobertura MX sin
  verificar + de pago; la calibración externa se hace con fuentes públicas + INEGI.
- **Reemplaza:** matiza la confianza de D-008 (no la anula); D-008 sigue como los inputs, D-009
  fija su nivel de confianza y el método.

## 2026-07-31 · D-012 · El Radar se organiza alrededor de una pregunta, no de un catálogo de datos

- **Detonante:** Francisco, al usar el tablero: *"la usabilidad del sitio tiene mucha área de
  oportunidad. no logro entender el uso, ni encuentro la manera de obtener valor… la parte de
  data la tenemos bien, también los insights han sido positivos, pero no hemos logrado
  traducirlos visualmente."* Autorizó rehacer el UI desde cero.
- **Diagnóstico:** el tablero apilaba ~10 tarjetas de datos y dejaba al usuario armar la
  conclusión. El trabajo analítico estaba hecho; el producto no lo entregaba.
- **Decisión (producto):** la app abre respondiendo **"¿dónde abre la primera unidad?"** y todo
  lo demás es evidencia bajo demanda. Cuatro vistas: **Decisión** (narrativa con el hallazgo,
  los puntos concretos, la apuesta de turismo y qué falta para decidir), **Mapa**, **Colonias**
  (datos crudos, sin veredicto, con estrellas de finalistas) y **Evidencia** (hallazgos, método,
  fuentes). Se conserva la ley 10: la app **presenta el trade-off, no elige**; los finalistas los
  marcan los socios.
- **Hallazgo que motivó la jerarquía (estaba en los datos, enterrado en la tabla):** de las
  **16** colonias con más de 50 mil personas a 2 km, solo **2** no tienen competencia de pollo
  frito — Las Brisas (63,168) y Del Paseo Residencial (55,858); y en **todo** el corredor hay
  apenas **8** locales de pollo frito. El punto que sirve a Las Brisas + Las Torres + Del Paseo
  junta **70,849 personas únicas con 1 competidor**. Registrado como insight `hueco-masa`
  (11 números verificados contra el bundle por camino independiente).
- **Decisiones técnicas que arrastra:**
  - El CSS de Leaflet se **empaqueta desde node_modules**. Venía de `unpkg.com`: si ese CDN no
    respondía, el mapa se renderizaba en blanco. Ninguna hoja de estilo externa queda en el app.
  - Fuera la carga de Google Fonts y la tipografía Inter; se usa la del sistema (menos
    dependencias externas, cero requests de terceros).
  - Se elimina el **scoring con pesos ajustables** y el modelo de 4 zonas: no se usaban para
    decidir y competían con la unidad real de decisión (colonia y punto).
  - La paleta del cuadrante se validó con el validador del sistema de gráficos: **6/6** en claro
    y oscuro (banda de luminosidad, croma, separación CVD, contraste).
- **Reemplaza:** supersede la organización de UI de D-007 y del pulido posterior; **no** toca
  D-010 (los datos se siguen editando solo en el pipeline y se sincronizan al app) ni D-011
  (deploy propio).

## 2026-08-01 · D-013 · La categoría de un restaurante se deduce del NOMBRE, no del SCIAN; y todo conteo es auditable con un clic

- **Detonante:** Francisco preguntó cómo clasificamos los restaurantes — *"¿utilizamos el nombre
  del local? porque el nombre no nos dice nada"*. Al revisar el código apareció un defecto peor
  que el que sospechaba.
- **El defecto:** el clasificador concatenaba `nom_estab` (nombre) con `nombre_act` (descripción
  de actividad del SCIAN) y buscaba palabras clave en esa cadena. Pero **231 de 241** registros
  compartían la misma descripción del INEGI: *"Restaurantes con servicio de preparación de
  pizzas, hamburguesas, hot dogs y pollos rostizados para llevar"* — que contiene las tres
  palabras a la vez. Consecuencias medidas:
  - `pollo_2km` inflado: **161 de 241** "competidores de pollo" no tenían nada de pollo en su
    nombre (PIZZA INN, JOSE BURGER, TACOS MARROS).
  - `hamburguesas_2km` y `pizza_2km` vaciados por el orden de los `elif` (Altavista marcaba 10
    hamburguesas; el real es 28).
  - `frito_2km` NO estaba contaminado (ninguna palabra de frito aparece en la cadena SCIAN),
    pero sí tenía un falso negativo: **CAPTAIN FRIEND CHICKEN**, typo del DENUE por "fried".
- **Decisión (método):** la categoría se deduce **solo del nombre del establecimiento**, con
  coincidencia por **inicio de palabra** (sin esto, "BREWING" contiene "wing" y una cervecería
  contaba como local de alitas). El SCIAN sigue definiendo el universo (722* = restaurantes),
  nunca la categoría.
- **Decisión (categorías):** se separan `pollo_frito`, `alitas`, `pollo_asado`, `pollo_otro`,
  `hamburguesas`, `pizza`, `otro`. **Alitas y boneless quedan como categoría propia y visible**
  —decisión de Francisco— en vez de forzar un binario dentro/fuera de "pollo frito": venden
  pollo empanizado pero el formato es de bar, no de QSR familiar. Los socios juzgan con el dato
  enfrente (ley 10).
- **Decisión (auditabilidad):** cada conteo que muestra el app se puede **abrir con un clic** y
  ver la lista de establecimientos que lo forman, con el giro registrado en el INEGI a la vista.
  Nuevo archivo `establecimientos.json` (1,802 restaurantes, 164 KB, carga bajo demanda).
  **El conteo y la lista se derivan del MISMO cálculo** en `build_appdata.py`: un primer intento
  los generó por separado y 171 de 252 comprobaciones descuadraban. `audit_datos.py` gana un
  check que falla si vuelven a discrepar.
- **Qué cambió en los números:** competidores de pollo 241 → **125**. Pollo frito en el corredor
  8 → **9**. Alitas y boneless: **25**. Y el hallazgo estrella se debilitó: las colonias con masa
  (>50k) y **cero** pollo frito pasaron de **2 a 1** (solo Las Brisas, que además tiene 5 locales
  de alitas a 2 km). Del Paseo Residencial ya no está: tiene Captain Fried Chicken.
- **Reemplaza:** corrige la clasificación de D-006 y el insight `hueco-masa` publicado el
  31-jul, que quedó **falsificado por estos datos** y fue reescrito. No toca D-010 ni D-012.

## 2026-08-04 · D-014 · Las anclas se clasifican por código SCIAN exacto, no por prefijo

- **Detonante:** Francisco pidió revisar si otros datos duros estaban mal clasificados, después
  del hallazgo de D-013. La misma falla estaba en las anclas de demanda.
- **El defecto:** las anclas se clasificaban por **prefijo** de código SCIAN, y el prefijo
  agrupa cosas que la etiqueta no admite:
  - `4621` → "Supermercados": **228 de 253 eran minisúperes**; supermercados reales: 25.
    Un Soriana ancla una compra semanal; una tiendita de esquina no. Para elegir local, la
    diferencia es la decisión completa.
  - `46411` → "Farmacias": **47 de 172** eran *"productos naturistas, medicamentos
    homeopáticos y de complementos alimenticios"*. 27% de inflación.
  - `611` → "Escuelas": **177 de 528** eran escuelas de arte (52), de deporte (43), de idiomas,
    de oficios y profesores particulares (23). Y no separaba preescolar (119 — los papás dejan
    al niño y se van) de primaria/secundaria/prepa (203 — los alumnos compran su comida), que
    para un QSR es la diferencia entre un ancla real y una irrelevante.
  - `5221` → "Bancos": **limpio**, 93 de 93 banca múltiple.
  - `71394` → "Gimnasios": prácticamente limpio (129 acondicionamiento físico + 8 clubes).
- **Decisión:** clasificación por **código SCIAN exacto** con diccionario explícito. Categorías
  nuevas: `supermercado` (25), `minisuper` (228), `farmacia` (125), `naturista` (47),
  `banco` (93), `escuela_basica` (203), `preescolar` (119), `universidad` (29),
  `escuela_otra` (177), `gimnasio` (137). Mismo principio que D-013 y que las alitas: **separar
  en categorías honestas en vez de lumpear bajo una etiqueta que miente.**
- **Decisión (arquitectura):** las anclas pasan al **mismo padrón** que los restaurantes
  (2,985 registros). Sus conteos y sus listas abribles se derivan del **mismo cálculo** en
  `build_appdata.py`, igual que la competencia. Verificado: **0 descuadres** en las 42 colonias
  sobre competencia y anclas juntas.
- **Hallazgo de negocio que destapa:** **El Cercado no tiene un solo supermercado a 2 km**
  (13 minisúperes). Antes el radar decía "13 supermercados" y eso pintaba un entorno comercial
  que no existe. Contry tiene 5 supermercados reales, no 57.
- **Revisión de la asignación de colonias (sin cambios):** se auditaron los 12,554
  establecimientos del corredor contra los tokens de `colonias.json`. **Ningún asentamiento cae
  en dos colonias a la vez** — los tokens están limpios. Cobertura 70.7%, ya documentada.
  **Pendiente marcado, no resuelto:** el centro de cada colonia se promedia con sus propios
  establecimientos, y hay colonias con muy pocos (La Herradura 26, Del Paseo Residencial 27,
  Los Cristales 28). Su centro —y por tanto todo su catchment de 2 km— tiene más margen de
  error que el de Altavista, que tiene cientos. Hoy la app las presenta con la misma autoridad.
- **Reemplaza:** corrige la definición de anclas de D-006. No toca D-013 (que corrigió la
  clasificación de restaurantes) ni D-012.
