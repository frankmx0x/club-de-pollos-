#!/usr/bin/env python3
"""Radar de Sitios — mini-ranking de colonias candidatas (síntesis).

Combina, por colonia candidata (centro derivado de DENUE):
  - población en radio 2 km (Censo POBTOT sobre AGEBs con centroide en el radio),
  - competencia de POLLO FRITO en 2 km (DENUE, todo NL),
  - SES del catchment: escolaridad y % internet ponderados (Censo AGEB en el radio),
  - venta estimada = pob × gasto per cápita (por SES) × σ base 6%,
  - un score compuesto transparente (hueco / encaje / demanda vs meta 100k).

Uso: rank_colonias.py <denue_19.csv> <censo_ageb.csv>
Salida: data/ranking_colonias.json  (+ tabla en consola)
"""
import csv
import json
import pathlib
import sys

import extract_denue as den

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
R_KM = 2.0
SIGMA_BASE = 0.06

COLONIAS = [
    ("Contry", "contry", "039"),
    ("Tecnológico", "tecnologico", "039"),
    ("La Estanzuela", "estanzuela", "039"),
    ("Valle Alto", "valle alto", "039"),
    ("San Ángel", "san angel", "039"),
    ("El Cercado (Santiago)", "cercado", "049"),
    ("Centro de Allende", "centro", "004"),
]


def percapita_por_ses(esc):
    if esc is None: return 130
    if esc >= 11.5: return 160   # ingreso alto
    if esc >= 10.0: return 140   # medio
    return 115                   # bajo/medio


def key(mun, loc, ageb):
    def i(x):
        try: return int(str(x).strip())
        except: return -1
    return (i(mun), i(loc), (ageb or "").strip().upper().zfill(4))


def main():
    denue_csv, censo_csv = sys.argv[1], sys.argv[2]

    agsum, colpts, fritos = {}, {n: [] for n, _, _ in COLONIAS}, []
    for row in csv.DictReader(open(denue_csv, encoding="latin-1", newline="")):
        lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
        if lat is None or lon is None: continue
        k = key(row.get("cve_mun"), row.get("cve_loc"), row.get("ageb"))
        s = agsum.setdefault(k, [0.0, 0.0, 0]); s[0] += lat; s[1] += lon; s[2] += 1
        cvem = (row.get("cve_mun") or "").strip().zfill(3)
        asent = den.norm(row.get("nomb_asent"))
        for name, tok, mun in COLONIAS:
            if cvem == mun and tok in asent:
                colpts[name].append((lat, lon))
        act = (row.get("codigo_act") or "").strip()
        if act.startswith("722"):
            blob = den.norm(row.get("nom_estab")) + " " + den.norm(row.get("nombre_act"))
            if any(k2 in blob for k2 in den.POLLO_FRITO_KW):
                fritos.append((lat, lon, (row.get("nom_estab") or "").strip()))
    ageb_cent = {k: (v[0]/v[2], v[1]/v[2]) for k, v in agsum.items() if v[2] > 0}

    # Censo: POBTOT, GRAPROES, VPH_INTER, VIVPAR_HAB por AGEB
    ses = {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); h = [c.lstrip("﻿") for c in next(r)]
        ix = {n: h.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT", "GRAPROES", "VPH_INTER", "VIVPAR_HAB"]}
        def num(x):
            x = (x or "").strip()
            try: return float(x)
            except: return None
        def i(x):
            try: return int((x or "").strip())
            except: return -1
        for row in r:
            if i(row[ix["LOC"]]) > 0 and i(row[ix["MZA"]]) == 0 and row[ix["AGEB"]].strip().upper().zfill(4) != "0000":
                ses[key(row[ix["MUN"]], row[ix["LOC"]], row[ix["AGEB"]])] = {
                    "pob": num(row[ix["POBTOT"]]) or 0, "esc": num(row[ix["GRAPROES"]]),
                    "inter": num(row[ix["VPH_INTER"]]), "viv": num(row[ix["VIVPAR_HAB"]])}

    cent_ses = [(ageb_cent[k], ses[k]) for k in ageb_cent if k in ses]

    rows = []
    for name, tok, mun in COLONIAS:
        pts = colpts[name]
        if not pts: continue
        clat = sum(p[0] for p in pts)/len(pts); clon = sum(p[1] for p in pts)/len(pts)
        pob = escn = escd = intn = intd = 0.0
        for (alat, alon), d in cent_ses:
            if den._haversine_km(clat, clon, alat, alon) <= R_KM:
                pob += d["pob"]
                if d["esc"] is not None: escn += d["esc"]*d["pob"]; escd += d["pob"]
                if d["inter"] is not None and d["viv"]: intn += d["inter"]; intd += d["viv"]
        esc = round(escn/escd, 2) if escd else None
        pct_int = round(100*intn/intd, 1) if intd else None
        nfrito = sum(1 for flat, flon, _ in fritos if den._haversine_km(clat, clon, flat, flon) <= R_KM)
        pc = percapita_por_ses(esc)
        venta = int(pob * pc * SIGMA_BASE)
        rows.append({"colonia": name, "pob_2km": int(pob), "frito_2km": nfrito,
                     "escolaridad": esc, "pct_internet": pct_int, "percapita": pc,
                     "venta_est_mxn": venta})

    # Score compuesto (transparente): hueco 40 / encaje 40 / demanda 20
    maxf = max((x["frito_2km"] for x in rows), default=1) or 1
    escs = [x["escolaridad"] for x in rows if x["escolaridad"] is not None]
    emin, emax = (min(escs), max(escs)) if escs else (9, 12)
    for x in rows:
        hueco = 100*(1 - x["frito_2km"]/maxf)
        encaje = 100*(emax - x["escolaridad"])/(emax - emin) if x["escolaridad"] is not None and emax > emin else 50
        demanda = min(100, 100*x["pob_2km"]/100000)  # % de la meta 100k
        x["subscores"] = {"hueco": round(hueco), "encaje": round(encaje), "demanda": round(demanda)}
        x["score"] = round(0.4*hueco + 0.4*encaje + 0.2*demanda)
    rows.sort(key=lambda x: -x["score"])

    out = {"_meta": {"radio_km": R_KM, "sigma_base": SIGMA_BASE,
                     "fuente": "DENUE may-2026 (competencia/centroides) + Censo 2020 (pob/SES)",
                     "percapita_regla": ">=11.5 esc→$160 · 10-11.5→$140 · <10→$115",
                     "confianza": "V-DENUE + V-Censo (radio aprox por centroide)"}, "colonias": rows}
    DATA.mkdir(exist_ok=True)
    (DATA / "ranking_colonias.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"MINI-RANKING de colonias (radio {R_KM} km, σ base {int(SIGMA_BASE*100)}%):\n")
    print(f"  {'#':2}{'colonia':22}{'score':>6}{'pob2km':>9}{'frito':>6}{'escol':>7}{'venta est':>12}")
    for i, x in enumerate(rows, 1):
        print(f"  {i:<2}{x['colonia']:22}{x['score']:>6}{x['pob_2km']:>9,}{x['frito_2km']:>6}"
              f"{x['escolaridad'] if x['escolaridad'] else 0:>7}{('$'+format(x['venta_est_mxn'],',')):>12}")


if __name__ == "__main__":
    main()
