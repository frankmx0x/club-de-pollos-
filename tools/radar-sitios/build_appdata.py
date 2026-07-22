#!/usr/bin/env python3
"""Radar de Sitios — empaqueta un snapshot COMPACTO para la web app (Radar v2).

Combina seed.json (zonas + scores + demografía + competencia agregada) con
competencia_corredor.json (puntos georreferenciados) en un solo bundle que el app
de presentación (Lovable) consume. Es un SNAPSHOT de nuestro pipeline (fuente de
verdad = este repo), con fecha y fuente; no reemplaza a los datos canónicos.

Salida: data/app_data.json
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"


def main():
    seed = json.loads((DATA / "seed.json").read_text(encoding="utf-8"))
    comp = json.loads((DATA / "competencia_corredor.json").read_text(encoding="utf-8"))

    # Puntos compactos: solo lo que el mapa necesita
    puntos = []
    for e in comp["establecimientos"]:
        if e.get("lat") is None or e.get("lon") is None:
            continue
        puntos.append({
            "n": e["nombre"][:40],
            "lat": round(e["lat"], 5),
            "lon": round(e["lon"], 5),
            "frito": bool(e["pollo_frito"]),
            "tramo": e.get("tramo", ""),
            "mun": e["municipio"],
        })

    # Vértices del corredor para dibujar la polilínea (desde extract_denue)
    corridor = [
        {"n": "ITESM / Tec", "lat": 25.6512, "lon": -100.2895},
        {"n": "Contry", "lat": 25.6300, "lon": -100.2700},
        {"n": "La Estanzuela", "lat": 25.5900, "lon": -100.2550},
        {"n": "Santiago (El Cercado)", "lat": 25.4318, "lon": -100.1520},
        {"n": "Allende centro", "lat": 25.2793, "lon": -100.0155},
    ]

    bundle = {
        "_meta": {
            "titulo": "Radar de Sitios — Corredor Sur (Club de Pollos)",
            "snapshot": seed["_meta"]["fecha"],
            "version": seed["_meta"]["version"],
            "niveles": seed["_meta"]["niveles"],
            "fuente": "Snapshot del pipeline en repo club-de-pollos- (DENUE may-2026 + Censo 2020 INEGI).",
        },
        "zonas": seed["tramos"],
        "club_de_pollos": seed["club_de_pollos_en_corredor"],
        "puntos": puntos,
        "corredor": corridor,
    }
    out = DATA / "app_data.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"OK: {out.name} · zonas={len(bundle['zonas'])} · puntos={len(puntos)} · "
          f"{out.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
