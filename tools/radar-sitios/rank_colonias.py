#!/usr/bin/env python3
"""Radar de Sitios — mini-ranking de colonias candidatas (síntesis + capa turística).

Combina, por colonia candidata (centro derivado de DENUE):
  - población en radio 2 km (Censo POBTOT sobre AGEBs con centroide en el radio),
  - competencia de POLLO FRITO en 2 km (DENUE, todo NL),
  - SES del catchment: escolaridad y % internet ponderados (Censo AGEB en el radio),
  - venta residencial estimada = pob × gasto per cápita (por SES) × σ base 6%,
  - CAPA TURÍSTICA: visitantes de atracciones OSETUR cercanas (<=5 km) × captura × ticket,
  - venta_total = residencial + turismo,
  - score compuesto transparente (hueco / encaje / demanda).

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
R_TOUR = 5.0        # km: atracción accesible desde la colonia
CAPT_TUR = 0.05     # captura del flujo turístico (SUPUESTO, a confirmar en campo)

COLONIAS = [
    ("Contry", "contry", "039"),
    ("Tecnológico", "tecnologico", "039"),
    ("La Estanzuela", "estanzuela", "039"),
    ("Valle Alto", "valle alto", "039"),
    ("San Ángel", "san angel", "039"),
    ("El Cercado (Santiago)", "cercado", "049"),
    ("Centro de Allende", "centro", "004"),
]

# TDPA (SICT Datos Viales 2014) proyectado a hoy con crecimiento del parque vehicular NL.
# NL: ~1.8M veh (2014) → ~2.8M hoy (+55%, El Horizonte); ICV +30% 2015-24; El Norte +52%/8a.
# Central usado: +40% (rango +30% a +55%). El corredor Carr. Nacional probablemente lo supera.
GROW = 1.40
TDPA = {"El Cercado (Santiago)": {
        "veh_dia_2014": 19389, "veh_dia_hoy_est": int(19389*GROW),
        "rango_hoy": [int(19389*1.30), int(19389*1.55)],
        "crecimiento": "+40% aprox 2014→2026 (parque vehicular NL, INEGI VMRC / ICV)",
        "tramo": "Carretera Nacional (Cd. Victoria–Monterrey), est. El Cercado",
        "fuente": "SICT Datos Viales 2014 + crecimiento parque vehicular NL",
        "confianza": "SICT 2014 (dato) × crecimiento (estimación)"}}


def percapita_por_ses(esc):
    if esc is None: return 130
    if esc >= 11.5: return 160
    if esc >= 10.0: return 140
    return 115


def key(mun, loc, ageb):
    def i(x):
        try: return int(str(x).strip())
        except: return -1
    return (i(mun), i(loc), (ageb or "").strip().upper().zfill(4))


def cargar_atracciones():
    try:
        pk = json.loads((DATA / "visitantes_parques_nl.json").read_text(encoding="utf-8"))["parques"]
    except Exception:
        return []
    meses = ["v_enero","v_febrero","v_marzo","v_abril","v_mayo","v_junio",
             "v_julio","v_agosto","v_septiembre","v_octubre","v_noviembre","v_diciembre"]
    atr = []
    for p in pk:
        p = {k.strip(): v for k, v in p.items()}  # el header del xlsx trae espacios ('latitud ')
        try:
            lat = float(str(p.get("latitud")).strip()); lon = float(str(p.get("longitud")).strip())
        except (TypeError, ValueError):
            continue
        vals = [float(p[m]) for m in meses if isinstance(p.get(m), (int, float))]
        if vals:
            atr.append((lat, lon, p.get("parque", ""), sum(vals)/len(vals)))  # visitantes/mes promedio
    return atr


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
                fritos.append((lat, lon))
    ageb_cent = {k: (v[0]/v[2], v[1]/v[2]) for k, v in agsum.items() if v[2] > 0}

    ses = {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); h = [c.lstrip("﻿") for c in next(r)]
        ix = {n: h.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT", "GRAPROES", "VPH_INTER", "VIVPAR_HAB"]}
        def num(x):
            try: return float((x or "").strip())
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
    atracciones = cargar_atracciones()

    rows = []
    for name, tok, mun in COLONIAS:
        pts = colpts[name]
        if not pts: continue
        clat = sum(p[0] for p in pts)/len(pts); clon = sum(p[1] for p in pts)/len(pts)
        pob = escn = escd = intn = intd = 0.0
        for (alat, alon), dd in cent_ses:
            if den._haversine_km(clat, clon, alat, alon) <= R_KM:
                pob += dd["pob"]
                if dd["esc"] is not None: escn += dd["esc"]*dd["pob"]; escd += dd["pob"]
                if dd["inter"] is not None and dd["viv"]: intn += dd["inter"]; intd += dd["viv"]
        esc = round(escn/escd, 2) if escd else None
        pct_int = round(100*intn/intd, 1) if intd else None
        nfrito = sum(1 for flat, flon in fritos if den._haversine_km(clat, clon, flat, flon) <= R_KM)
        pc = percapita_por_ses(esc)
        venta_res = int(pob * pc * SIGMA_BASE)

        # Capa turística: visitantes/mes de atracciones a <=R_TOUR km
        flujo = 0.0; atr_cerca = []
        for alat, alon, aname, vmes in atracciones:
            if den._haversine_km(clat, clon, alat, alon) <= R_TOUR:
                flujo += vmes; atr_cerca.append(f"{aname} (~{int(vmes):,}/mes)")
        venta_tur = int(flujo * CAPT_TUR * 220)
        rows.append({"colonia": name, "centro": {"lat": round(clat, 5), "lon": round(clon, 5)},
                     "pob_2km": int(pob), "frito_2km": nfrito, "escolaridad": esc,
                     "pct_internet": pct_int, "percapita": pc,
                     "venta_residencial": venta_res,
                     "flujo_turistico_mes": int(flujo), "atracciones": atr_cerca,
                     "venta_turismo": venta_tur, "venta_total": venta_res + venta_tur,
                     "tdpa": TDPA.get(name)})

    # Score compuesto (transparente): hueco 40 / encaje 40 / demanda 20
    maxf = max((x["frito_2km"] for x in rows), default=1) or 1
    escs = [x["escolaridad"] for x in rows if x["escolaridad"] is not None]
    emin, emax = (min(escs), max(escs)) if escs else (9, 12)
    for x in rows:
        hueco = 100*(1 - x["frito_2km"]/maxf)
        encaje = 100*(emax - x["escolaridad"])/(emax - emin) if x["escolaridad"] is not None and emax > emin else 50
        demanda = min(100, 100*x["pob_2km"]/100000)
        x["subscores"] = {"hueco": round(hueco), "encaje": round(encaje), "demanda": round(demanda)}
        x["score"] = round(0.4*hueco + 0.4*encaje + 0.2*demanda)
    rows.sort(key=lambda x: -x["venta_total"])  # ordena por venta total (residencial + turismo)

    out = {"_meta": {"radio_km": R_KM, "sigma_base": SIGMA_BASE, "radio_turismo_km": R_TOUR,
                     "captura_turismo": CAPT_TUR,
                     "fuente": "DENUE may-2026 + Censo 2020 + OSETUR visitantes parques + SICT TDPA",
                     "percapita_regla": ">=11.5 esc→$160 · 10-11.5→$140 · <10→$115",
                     "nota": "captura turística 5% = SUPUESTO a confirmar con conteo de campo",
                     "confianza": "V-DENUE + V-Censo + V-OSETUR (radio/captura aprox)"}, "colonias": rows}
    (DATA / "ranking_colonias.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"MINI-RANKING de colonias (radio {R_KM}km, σ {int(SIGMA_BASE*100)}%, captura turismo {int(CAPT_TUR*100)}%):\n")
    print(f"  {'#':2}{'colonia':22}{'pob2km':>8}{'frito':>6}{'escol':>6}{'v.resid':>10}{'flujo tur':>10}{'v.turismo':>10}{'V.TOTAL':>11}")
    for i, x in enumerate(rows, 1):
        print(f"  {i:<2}{x['colonia']:22}{x['pob_2km']:>8,}{x['frito_2km']:>6}"
              f"{(x['escolaridad'] or 0):>6}{('$'+format(x['venta_residencial'],',')):>10}"
              f"{x['flujo_turistico_mes']:>10,}{('$'+format(x['venta_turismo'],',')):>10}"
              f"{('$'+format(x['venta_total'],',')):>11}")


if __name__ == "__main__":
    main()
