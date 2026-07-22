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
