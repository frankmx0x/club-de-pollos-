#!/usr/bin/env python3
"""Radar de Sitios — población-en-radio por colonia (opción b).

Estima cuánta gente vive dentro de un radio R de un punto, sumando la población
(Censo 2020, POBTOT por AGEB) de los AGEBs cuyo CENTROIDE cae en el radio.

Centroide de cada AGEB: se deriva del promedio de coordenadas de los establecimientos
DENUE en ese AGEB (evita descargar shapefiles del Marco Geoestadístico). Es una
APROXIMACIÓN: los AGEBs sin ningún negocio en DENUE no tienen centroide y quedan fuera
→ se REPORTA la cobertura (ley 4). Para densidad/centroide oficial exacto, usar el Marco
Geoestadístico (F4 del plan) — este método es el v1 barato.

Uso: extract_poblacion_radio.py <denue_19.csv> <censo_ageb.csv>
Salida: data/poblacion_radio.json
"""
import csv
import json
import pathlib
import sys

import extract_denue as den  # _haversine_km, fnum, norm, MUN

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
RADIOS = [1.5, 2.0, 2.5]

# Colonias candidatas (nombre canónico, token en asentamiento sin acentos, municipio)
COLONIAS = [
    ("Contry", "contry", "039"),
    ("Tecnológico", "tecnologico", "039"),
    ("La Estanzuela", "estanzuela", "039"),
    ("Valle Alto", "valle alto", "039"),
    ("La Herradura", "herradura", "039"),
    ("San Ángel", "san angel", "039"),
    ("El Cercado (Santiago)", "cercado", "049"),
    ("Centro de Allende", "centro", "004"),
]


def key(mun, loc, ageb):
    def i(x):
        try: return int(str(x).strip())
        except: return -1
    return (i(mun), i(loc), (ageb or "").strip().upper().zfill(4))


def main():
    denue_csv, censo_csv = sys.argv[1], sys.argv[2]

    # 1) Centroide de AGEB desde DENUE (todo NL) + centros de colonia
    agsum = {}  # key -> [sumlat, sumlon, n]
    colpts = {name: [] for name, _, _ in COLONIAS}
    for row in csv.DictReader(open(denue_csv, encoding="latin-1", newline="")):
        lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
        if lat is None or lon is None:
            continue
        k = key(row.get("cve_mun"), row.get("cve_loc"), row.get("ageb"))
        s = agsum.setdefault(k, [0.0, 0.0, 0]); s[0] += lat; s[1] += lon; s[2] += 1
        cvem = (row.get("cve_mun") or "").strip().zfill(3)
        asent = den.norm(row.get("nomb_asent"))
        for name, tok, mun in COLONIAS:
            if cvem == mun and tok in asent:
                colpts[name].append((lat, lon))
    ageb_centroide = {k: (v[0]/v[2], v[1]/v[2]) for k, v in agsum.items() if v[2] > 0}

    # 2) POBTOT por AGEB (Censo, filas AGEB-total: mza=0, ageb!=0000, loc!=0)
    pob = {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); header = [h.lstrip("﻿") for h in next(r)]
        idx = {n: header.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT"]}
        def i(x):
            try: return int((x or "").strip())
            except: return -1
        for row in r:
            loc_i, mza_i = i(row[idx["LOC"]]), i(row[idx["MZA"]])
            ageb = row[idx["AGEB"]].strip().upper().zfill(4)
            if loc_i > 0 and mza_i == 0 and ageb != "0000":
                p = i(row[idx["POBTOT"]])
                if p >= 0:
                    pob[key(row[idx["MUN"]], loc_i, ageb)] = p

    # 3) Cobertura del método en municipios del corredor
    cov = {}
    for mname, mcode in [("Monterrey", 39), ("Santiago", 49), ("Allende", 4)]:
        tot = sum(p for k, p in pob.items() if k[0] == mcode)
        con = sum(p for k, p in pob.items() if k[0] == mcode and k in ageb_centroide)
        cov[mname] = {"pob_censo": tot, "pob_con_centroide": con,
                      "cobertura_pct": round(100*con/tot, 1) if tot else None}

    # 4) Población-en-radio por colonia
    centroides = [(k, ageb_centroide[k], pob[k]) for k in ageb_centroide if k in pob]
    out_col = []
    for name, tok, mun in COLONIAS:
        pts = colpts[name]
        if not pts:
            out_col.append({"colonia": name, "nota": "sin puntos DENUE para el token"}); continue
        clat = sum(p[0] for p in pts)/len(pts); clon = sum(p[1] for p in pts)/len(pts)
        rad = {}
        for R in RADIOS:
            rad[f"{R}km"] = int(sum(p for _, (alat, alon), p in centroides
                                    if den._haversine_km(clat, clon, alat, alon) <= R))
        out_col.append({"colonia": name, "centro": {"lat": round(clat,5), "lon": round(clon,5)},
                        "n_estab_centro": len(pts), "poblacion_en_radio": rad})

    result = {"_meta": {"fuente": "Censo 2020 POBTOT por AGEB + centroide AGEB derivado de DENUE",
                        "metodo": "aprox: centroide de AGEB = promedio de coords de establecimientos DENUE",
                        "confianza": "V-Censo aprox", "radios_km": RADIOS},
              "cobertura": cov, "colonias": out_col}
    DATA.mkdir(exist_ok=True)
    (DATA / "poblacion_radio.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    print("COBERTURA del método (pob con centroide / pob censo):")
    for m, c in cov.items(): print(f"  {m:10} {c['cobertura_pct']}%  ({c['pob_con_centroide']:,}/{c['pob_censo']:,})")
    print("\nPOBLACIÓN EN RADIO por colonia:")
    print(f"  {'colonia':24}{'1.5km':>9}{'2.0km':>9}{'2.5km':>9}")
    for c in out_col:
        if "poblacion_en_radio" in c:
            r = c["poblacion_en_radio"]
            print(f"  {c['colonia']:24}{r['1.5km']:>9,}{r['2.0km']:>9,}{r['2.5km']:>9,}")
        else:
            print(f"  {c['colonia']:24}  {c['nota']}")


if __name__ == "__main__":
    main()
