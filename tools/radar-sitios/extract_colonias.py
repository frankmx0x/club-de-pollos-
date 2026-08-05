#!/usr/bin/env python3
"""Radar de Sitios — fase COLONIAS: scorea colonias nombradas, no zonas grandes.

Una franquicia no se pone "en el corredor": se pone en Contry o en El Cercado. Esta
es la resolución real de la decisión (ver docs/plans/2026-07-22-colonias-scoring.md).

Por cada colonia de colonias.json (lista canónica curada a mano):
  - competencia de pollo y de pollo FRITO en radio 2 km              [V-DENUE]
  - anclas de demanda (escuelas, súper, bancos, farmacias, gyms) 2km [V-DENUE]
  - población y SES del catchment 2 km (AGEBs del Censo)             [V-Censo aprox]
  - flujo turístico de atracciones OSETUR a <=5 km                   [V-OSETUR]
  - venta estimada = residencial + turismo, y sub-scores + score

Uso: extract_colonias.py <denue.csv> <censo_ageb.csv>
Salida: data/colonias_corredor.json
"""
import csv
import json
import pathlib
import sys

import extract_denue as den

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
R_KM = 2.0            # radio de catchment
R_TOUR = 5.0          # radio para considerar una atracción turística accesible
SIGMA = 0.06          # captura base del gasto QSR local (calibrada, ver análisis)
CAPT_TUR = 0.05       # captura del flujo turístico — SUPUESTO a confirmar en campo
TICKET = 220


def percapita(esc):
    """Gasto QSR/persona/mes según SES del catchment (proxy: escolaridad)."""
    if esc is None:
        return 130
    return 160 if esc >= 11.5 else (140 if esc >= 10.0 else 115)


def key(mun, loc, ageb):
    def i(x):
        try:
            return int(str(x).strip())
        except (TypeError, ValueError):
            return -1
    return (i(mun), i(loc), (ageb or "").strip().upper().zfill(4))


def cargar_atracciones():
    try:
        pk = json.loads((DATA / "visitantes_parques_nl.json").read_text(encoding="utf-8"))["parques"]
    except Exception:
        return []
    meses = ["v_enero", "v_febrero", "v_marzo", "v_abril", "v_mayo", "v_junio",
             "v_julio", "v_agosto", "v_septiembre", "v_octubre", "v_noviembre", "v_diciembre"]
    out = []
    for p in pk:
        p = {k.strip(): v for k, v in p.items()}   # el header del xlsx trae espacios
        try:
            lat, lon = float(str(p["latitud"]).strip()), float(str(p["longitud"]).strip())
        except (KeyError, TypeError, ValueError):
            continue
        vals = [float(p[m]) for m in meses if isinstance(p.get(m), (int, float))]
        if vals:
            out.append((lat, lon, p.get("parque", ""), sum(vals) / len(vals)))
    return out


def main():
    denue_csv, censo_csv = sys.argv[1], sys.argv[2]
    cfg = json.loads((HERE / "colonias.json").read_text(encoding="utf-8"))["colonias"]

    puntos = {c["id"]: [] for c in cfg}     # coords de establecimientos de la colonia
    agsum, pollo, frito, anclas = {}, [], [], []
    alitas = []                             # categoría propia: alitas y boneless (D-013)
    rest, hamb, pizza = [], [], []          # contexto: restaurantes totales y fast-food vecino
    total_corredor = 0
    asignados = 0

    with open(denue_csv, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            cvem = (row.get("cve_mun") or "").strip().zfill(3)
            if cvem not in den.MUN:
                continue
            lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
            if lat is None or lon is None or not den.in_corridor(cvem, lat, lon):
                continue
            total_corredor += 1

            # centroide de AGEB (para demografía por radio)
            k = key(row.get("cve_mun"), row.get("cve_loc"), row.get("ageb"))
            s = agsum.setdefault(k, [0.0, 0.0, 0]); s[0] += lat; s[1] += lon; s[2] += 1

            # asignación a colonia canónica
            asent = den.norm(row.get("nomb_asent"))
            for c in cfg:
                if c["mun"] != cvem:
                    continue
                if any(x in asent for x in c.get("excluye", [])):
                    continue
                if any(t in asent for t in c["tokens"]):
                    puntos[c["id"]].append((lat, lon)); asignados += 1
                    break

            act = (row.get("codigo_act") or "").strip()
            if act.startswith("722"):
                nom = (row.get("nom_estab") or "").strip()
                # Categoría por NOMBRE (den.categoria); el SCIAN solo define el
                # universo 722*. Ver D-013 y el comentario en extract_denue.py.
                cat = den.categoria(nom)
                rest.append((lat, lon, nom, cat))
                if cat in den.CATS_POLLO:
                    pollo.append((lat, lon))
                    if cat == "pollo_frito":
                        frito.append((lat, lon, nom))
                    elif cat == "alitas":
                        alitas.append((lat, lon, nom))
                elif cat == "hamburguesas":
                    hamb.append((lat, lon))
                elif cat == "pizza":
                    pizza.append((lat, lon))
            else:
                cat_a = den.ancla(act)
                if cat_a:
                    anclas.append((lat, lon, cat_a))

    ageb_cent = {k: (v[0] / v[2], v[1] / v[2]) for k, v in agsum.items() if v[2] > 0}

    # Censo por AGEB
    ses = {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); h = [c.lstrip("﻿") for c in next(r)]
        ix = {n: h.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT", "GRAPROES", "VPH_INTER", "VIVPAR_HAB"]}
        def num(x):
            try: return float((x or "").strip())
            except ValueError: return None
        def i(x):
            try: return int((x or "").strip())
            except ValueError: return -1
        for row in r:
            if i(row[ix["LOC"]]) > 0 and i(row[ix["MZA"]]) == 0 and row[ix["AGEB"]].strip().upper().zfill(4) != "0000":
                ses[key(row[ix["MUN"]], row[ix["LOC"]], row[ix["AGEB"]])] = {
                    "pob": num(row[ix["POBTOT"]]) or 0, "esc": num(row[ix["GRAPROES"]]),
                    "inter": num(row[ix["VPH_INTER"]]), "viv": num(row[ix["VIVPAR_HAB"]])}
    cent_ses = [(ageb_cent[k], ses[k]) for k in ageb_cent if k in ses]
    atracciones = cargar_atracciones()

    filas = []
    for c in cfg:
        pts = puntos[c["id"]]
        if not pts:
            print(f"  [aviso] {c['nombre']}: sin establecimientos — se omite", file=sys.stderr)
            continue
        clat = sum(p[0] for p in pts) / len(pts)
        clon = sum(p[1] for p in pts) / len(pts)
        near = lambda a, b, R=R_KM: den._haversine_km(clat, clon, a, b) <= R

        pob = escn = escd = intn = intd = 0.0
        for (alat, alon), d in cent_ses:
            if near(alat, alon):
                pob += d["pob"]
                if d["esc"] is not None: escn += d["esc"] * d["pob"]; escd += d["pob"]
                if d["inter"] is not None and d["viv"]: intn += d["inter"]; intd += d["viv"]
        esc = round(escn / escd, 2) if escd else None

        n_pollo = sum(1 for a, b in pollo if near(a, b))
        fr = [n for a, b, n in frito if near(a, b)]
        al = [n for a, b, n in alitas if near(a, b)]
        # Índices del padrón (data/establecimientos_corredor.json) a 2 km:
        # alimentan el drill-down del app — cada conteo se puede abrir y auditar.
        idx = [i for i, (a, b, _n, _c) in enumerate(rest) if near(a, b)]
        n_rest = sum(1 for a, b, _n, _c in rest if near(a, b))
        n_hamb = sum(1 for a, b in hamb if near(a, b))
        n_pizza = sum(1 for a, b in pizza if near(a, b))
        anc = {}
        for a, b, cat in anclas:
            if near(a, b): anc[cat] = anc.get(cat, 0) + 1

        flujo, atr = 0.0, []
        for alat, alon, aname, vmes in atracciones:
            if den._haversine_km(clat, clon, alat, alon) <= R_TOUR:
                flujo += vmes; atr.append(aname)

        pc = percapita(esc)
        v_res = int(pob * pc * SIGMA)
        # Redondear el flujo ANTES de calcular: así el número que muestra el app es
        # recomputable a mano (visitantes × captura × ticket), sin residuos de decimales.
        flujo = round(flujo)
        v_tur = int(flujo * CAPT_TUR * TICKET)
        filas.append({
            "id": c["id"], "colonia": c["nombre"], "tramo": c["tramo"], "orden": c["orden"],
            "municipio": den.MUN[c["mun"]], "n_establecimientos": len(pts),
            "centro": {"lat": round(clat, 5), "lon": round(clon, 5)},
            "competencia": {"pollo_2km": n_pollo, "frito_2km": len(fr), "fritos": fr[:6],
                            "alitas_2km": len(al), "alitas": al[:8],
                            "restaurantes_2km": n_rest, "hamburguesas_2km": n_hamb,
                            "pizza_2km": n_pizza,
                            "fuente": "DENUE may-2026", "confianza": "V-DENUE"},
            "rest_idx": idx,
            "anclas": {"conteo": anc, "total": sum(anc.values()),
                       "fuente": "DENUE may-2026", "confianza": "V-DENUE"},
            "demografia": {"poblacion_2km": int(pob), "escolaridad": esc,
                           "pct_internet": round(100 * intn / intd, 1) if intd else None,
                           "percapita_qsr": pc, "fuente": "Censo 2020 INEGI",
                           "confianza": "V-Censo aprox"},
            "turismo": ({"atracciones": atr, "visitantes_mes": int(flujo),
                         "venta_turismo": v_tur, "confianza": "V-OSETUR"} if flujo else None),
            "venta": {"residencial": v_res, "turismo": v_tur, "total": v_res + v_tur},
        })

    # Sub-scores normalizados SOBRE EL CONJUNTO DE COLONIAS (no sobre las 4 zonas)
    maxf = max((x["competencia"]["frito_2km"] for x in filas), default=0) or 1
    escs = [x["demografia"]["escolaridad"] for x in filas if x["demografia"]["escolaridad"] is not None]
    emin, emax = (min(escs), max(escs)) if escs else (9.0, 12.5)
    maxanc = max((x["anclas"]["total"] for x in filas), default=0) or 1
    for x in filas:
        hueco = 100 * (1 - x["competencia"]["frito_2km"] / maxf)
        e = x["demografia"]["escolaridad"]
        encaje = 100 * (emax - e) / (emax - emin) if e is not None and emax > emin else 50
        demanda = 100 * x["anclas"]["total"] / maxanc      # proxy de demanda: densidad de anclas
        x["subscores"] = {"hueco": round(hueco), "encaje": round(encaje), "demanda": round(demanda)}
        x["score"] = round(0.4 * hueco + 0.4 * encaje + 0.2 * demanda)
    filas.sort(key=lambda x: -x["score"])

    cobertura = round(100 * asignados / total_corredor, 1) if total_corredor else 0
    out = {"_meta": {
        "radio_km": R_KM, "radio_turismo_km": R_TOUR, "sigma": SIGMA,
        "captura_turismo": CAPT_TUR, "ticket": TICKET,
        "proxy_demanda": "densidad de anclas (escuelas+súper+bancos+farmacias+gyms) en 2 km",
        "cobertura_pct": cobertura,
        "cobertura_nota": f"{asignados} de {total_corredor} establecimientos del corredor caen en una colonia canónica; el resto son colonias no listadas.",
        "fuente": "DENUE may-2026 + Censo 2020 + OSETUR",
        "confianza": "V-DENUE + V-Censo aprox + V-OSETUR",
        "caveat": "Demografía por catchment de 2 km (AGEBs), no por polígono exacto de colonia. Captura turística 5% = supuesto.",
    }, "colonias": filas}
    DATA.mkdir(exist_ok=True)
    (DATA / "colonias_corredor.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"Cobertura: {cobertura}% ({asignados}/{total_corredor} establecimientos del corredor)")
    print(f"\n  {'#':<3}{'colonia':22}{'tramo':26}{'pob2km':>8}{'frito':>6}{'anclas':>7}{'escol':>6}{'venta est':>12}{'score':>6}")
    for i, x in enumerate(filas, 1):
        print(f"  {i:<3}{x['colonia'][:21]:22}{x['tramo'][:25]:26}{x['demografia']['poblacion_2km']:>8,}"
              f"{x['competencia']['frito_2km']:>6}{x['anclas']['total']:>7}"
              f"{(x['demografia']['escolaridad'] or 0):>6}{('$'+format(x['venta']['total'],',')):>12}{x['score']:>6}")


if __name__ == "__main__":
    main()
