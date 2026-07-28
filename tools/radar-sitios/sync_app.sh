#!/usr/bin/env bash
# Radar de Sitios — sincroniza los datos del pipeline hacia el repo del app.
#
# Fuente de verdad: ESTE repo (club-de-pollos-). El app (club-pollos-radar) es capa
# de presentación y SOLO consume lo que el pipeline produce. Los datos NUNCA se
# editan a mano en el repo del app (ver DECISIONS D-010: el agente de Lovable
# reescribió cifras a mano y las inventó).
#
# Uso:  ./sync_app.sh [ruta_al_repo_del_app]
#       (default: /workspace/club-pollos-radar)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_REPO="${1:-/workspace/club-pollos-radar}"
SRC="$HERE/data/app_data.json"
DST="$APP_REPO/public/data/app_data.json"

[ -f "$SRC" ] || { echo "ERROR: falta $SRC — corre build_appdata.py primero"; exit 1; }
[ -d "$APP_REPO" ] || { echo "ERROR: no existe el repo del app en $APP_REPO"; exit 1; }

python3 -c "import json,sys; json.load(open('$SRC'))" || { echo "ERROR: $SRC no es JSON válido"; exit 1; }

cp "$SRC" "$DST"
echo "OK: app_data.json sincronizado ($(wc -c <"$DST") bytes) → $DST"
python3 - "$DST" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print(f"   version: {d['_meta']['version']}")
print(f"   zonas={len(d['zonas'])} competidores={len(d['puntos'])} anclas={len(d['anclas'])}")
print(f"   sync:    {d['fuentes']['ultima_sincronizacion_txt']}")
PY
echo
echo "Siguiente: cd $APP_REPO && npx tsc --noEmit && npm run build && git commit + push"
