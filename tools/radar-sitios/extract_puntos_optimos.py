#!/usr/bin/env python3
"""Radar de Sitios — PUNTOS ÓPTIMOS: ubicaciones que sirven a VARIAS colonias a la vez.

Pregunta de Francisco: "¿habrá un punto que pueda servir dos colonias al mismo tiempo?"

Método (sin doble conteo): los catchments de colonias vecinas se TRASLAPAN, así que
sumar colonias contaría a la misma gente dos veces. Aquí se evalúa cada punto candidato
por la población ÚNICA a <=2 km (cada AGEB del Censo se cuenta una sola vez), junto con
competencia de frito y anclas en ese radio. Candidatos = centroides de AGEB del corredor
(ubicaciones reales pobladas). Se eligen los mejores con supresión de vecinos (>=1.5 km
entre puntos) para que sean zonas distintas, y se reporta a qué colonias sirve cada uno
(centros de colonia a <=2 km).

Uso: extract_puntos_optimos.py <denue.csv> <censo_ageb.csv>
Salida: data/puntos_optimos.json
"""
import csv
import json
import pathlib
import sys

import extract_denue as den

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
R = 2.0          # radio de servicio
SUPR = 1.5       # km mínimos entre puntos elegidos (zonas distintas)
TOP = 10
# D-016: share de la categoría pollo (8% del QSR) repartido entre jugadores.
SHARE_POLLO, PESO_ALITAS, TICKET = 0.08, 0.5, 220


def key(mun, loc, ageb):
    def i(x):
        try: return int(str(x).strip())
        except (TypeError, ValueError): return -1
    return (i(mun), i(loc), (ageb or "").strip().upper().zfill(4))


def main():
    denue_csv, censo_csv = sys.argv[1], sys.argv[2]

    # centroides de AGEB (desde DENUE, solo corredor) + fritos + anclas
    agsum, fritos, alitas, anclas = {}, [], [], []
    with open(denue_csv, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            cvem = (row.get("cve_mun") or "").strip().zfill(3)
            if cvem not in den.MUN:
                continue
            lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
            if lat is None or lon is None or not den.in_corridor(cvem, lat, lon):
                continue
            k = key(row.get("cve_mun"), row.get("cve_loc"), row.get("ageb"))
            s = agsum.setdefault(k, [0.0, 0.0, 0]); s[0] += lat; s[1] += lon; s[2] += 1
            act = (row.get("codigo_act") or "").strip()
            if act.startswith("722"):
                # Categoría por nombre (D-013): el SCIAN 722514 mete pizzerías
                # y taquerías en "pollo" porque su descripción las nombra a todas.
                _cat = den.categoria(row.get("nom_estab") or "")
                if _cat == "pollo_frito":
                    fritos.append((lat, lon))
                elif _cat == "alitas":
                    alitas.append((lat, lon))
            else:
                if den.ancla(act):
                    anclas.append((lat, lon))
    cent = {k: (v[0]/v[2], v[1]/v[2]) for k, v in agsum.items() if v[2] > 0}

    # población por AGEB (Censo)
    pob = {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); h = [c.lstrip("﻿") for c in next(r)]
        ix = {n: h.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT"]}
        def i(x):
            try: return int((x or "").strip())
            except ValueError: return -1
        for row in r:
            ageb = row[ix["AGEB"]].strip().upper().zfill(4)
            if i(row[ix["LOC"]]) > 0 and i(row[ix["MZA"]]) == 0 and ageb != "0000":
                p = i(row[ix["POBTOT"]])
                if p > 0:
                    pob[key(row[ix["MUN"]], i(row[ix["LOC"]]), ageb)] = p

    puntos_pob = [(xy, pob[k]) for k, xy in cent.items() if k in pob]
    colonias = json.loads((DATA / "colonias_corredor.json").read_text(encoding="utf-8"))["colonias"]

    # evaluar cada centroide de AGEB como punto candidato
    candidatos = []
    for k, (clat, clon) in cent.items():
        if k not in pob:
            continue
        p2 = sum(p for (alat, alon), p in puntos_pob if den._haversine_km(clat, clon, alat, alon) <= R)
        f2 = sum(1 for a, b in fritos if den._haversine_km(clat, clon, a, b) <= R)
        al2 = sum(1 for a, b in alitas if den._haversine_km(clat, clon, a, b) <= R)
        a2 = sum(1 for a, b in anclas if den._haversine_km(clat, clon, a, b) <= R)
        candidatos.append({"lat": clat, "lon": clon, "pob_2km": int(p2), "frito_2km": f2,
                           "alitas_2km": al2, "anclas_2km": a2})

    # greedy: mejor población única, suprimiendo vecinos a < SUPR km
    candidatos.sort(key=lambda x: -x["pob_2km"])
    elegidos = []
    for c in candidatos:
        if all(den._haversine_km(c["lat"], c["lon"], e["lat"], e["lon"]) >= SUPR for e in elegidos):
            elegidos.append(c)
        if len(elegidos) >= TOP:
            break

    # a qué colonias sirve cada punto + comparación vs la mejor colonia individual
    max_col = max(c["demografia"]["poblacion_2km"] for c in colonias)
    for e in elegidos:
        sirve = [(c["colonia"], den._haversine_km(e["lat"], e["lon"], c["centro"]["lat"], c["centro"]["lon"]))
                 for c in colonias]
        e["sirve_a"] = [n for n, dkm in sorted(sirve, key=lambda x: x[1]) if dkm <= R][:5]
        # D-016: pastel de la categoría (percápita medio $140) repartido entre
        # nosotros + fritos (peso 1) + alitas (peso 0.5) del radio del punto.
        jug = 1 + e["frito_2km"] + PESO_ALITAS * e["alitas_2km"]
        e["venta_residencial_est"] = int(round(e["pob_2km"] * 140 * SHARE_POLLO / jug))
        e["vs_mejor_colonia_pct"] = round(100 * e["pob_2km"] / max_col - 100, 1)

    out = {"_meta": {"metodo": "población ÚNICA a <=2 km (cada AGEB contado una vez) evaluada en cada centroide de AGEB del corredor; top con supresión de 1.5 km. SIN doble conteo entre colonias.",
                     "percapita_ref": 140, "share_pollo": SHARE_POLLO, "peso_alitas": PESO_ALITAS,
                     "fuente": "Censo 2020 + DENUE may-2026", "confianza": "V-Censo aprox + V-DENUE",
                     "caveat": "Venta residencial de referencia: pastel de la categoría pollo (8% del gasto QSR, percápita medio $140) repartido entre nosotros y los competidores del radio (fritos peso 1, alitas 0.5). No incluye turismo/tráfico; el punto exacto se elige en campo."},
           "puntos": elegidos}
    (DATA / "puntos_optimos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"TOP {len(elegidos)} PUNTOS ÓPTIMOS (población única a 2 km, sin doble conteo):\n")
    print(f"  {'#':<3}{'pob única 2km':>13}{'fritos':>8}{'anclas':>8}{'venta ref':>11}  sirve a")
    for i, e in enumerate(elegidos, 1):
        print(f"  {i:<3}{e['pob_2km']:>13,}{e['frito_2km']:>8}{e['anclas_2km']:>8}"
              f"{('$'+format(e['venta_residencial_est'],',')):>11}  {' + '.join(e['sirve_a'][:4])}")


if __name__ == "__main__":
    main()
