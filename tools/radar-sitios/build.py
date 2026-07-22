#!/usr/bin/env python3
"""Radar de Sitios — build v0.

Inyecta data/seed.json dentro de radar.html (entre los marcadores SEED) para
producir un archivo self-contained que abre en cualquier navegador o teléfono,
sin servidor ni red.

Uso:  python3 build.py
Reproducible: reemplaza SIEMPRE el bloque entre marcadores; correr N veces da lo mismo.

Cuando se abra el acceso a INEGI DENUE + Google Places, el pipeline real
reemplazará seed.json por datos completos georreferenciados y este mismo build
regenerará el mapa. La estructura de datos (tramos/score/fuente/confianza) no cambia.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
HTML = HERE / "radar.html"
SEED = HERE / "data" / "seed.json"

START = "// >>> SEED >>>"
END = "// <<< SEED <<<"


def main() -> int:
    if not SEED.exists():
        print(f"ERROR: falta {SEED}", file=sys.stderr)
        return 1
    data = json.loads(SEED.read_text(encoding="utf-8"))  # valida el JSON
    html = HTML.read_text(encoding="utf-8")

    inline = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    block = f"{START} (build.py inyecta data/seed.json entre estos marcadores)\nconst DATA = {inline};\n{END}"

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(html):
        print("ERROR: no encuentro los marcadores SEED en radar.html", file=sys.stderr)
        return 1
    new_html = pattern.sub(lambda _m: block, html, count=1)
    HTML.write_text(new_html, encoding="utf-8")

    n = len(data.get("tramos", []))
    print(f"OK: inyectados {n} tramos de {SEED.name} en {HTML.name} (self-contained).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
