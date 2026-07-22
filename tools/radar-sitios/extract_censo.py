#!/usr/bin/env python3
"""Radar de Sitios — pipeline v1b: demografía real del corredor desde el Censo 2020.

Entrada:
  - Censo 2020 AGEB/manzana urbana NL (INEGI, gratis, sin key):
      https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip
  - DENUE NL (para la lista de AGEBs del corredor en Monterrey) — reusa extract_denue.

Salida: data/demografia_corredor.json — POBTOT y proxies de nivel socioeconómico
(escolaridad, % con auto, % con internet, hacinamiento) por grupo del corredor.
Nivel [V-Censo] = dato duro. Santiago y Allende = total municipal (municipios chicos,
casi todo urbano). Monterrey-corredor = suma de AGEBs donde caen negocios del corredor.

Proxies SES (el Censo no trae ingreso directo): GRAPROES (grado promedio de escolaridad),
% viviendas con automóvil y con internet — separan bien tramos de ingreso.
"""
import csv
import json
import pathlib
import sys

import extract_denue as den  # reusa in_corridor, MUN, fnum, lectura DENUE

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"

# columnas por nombre (el header trae BOM en ENTIDAD)
COLS = ["POBTOT", "GRAPROES", "VIVPAR_HAB", "VPH_AUTOM", "VPH_INTER", "PROM_OCUP"]


def to_num(v):
    v = (v or "").strip()
    if v in ("", "*", "N/D", "N/A"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def corridor_mty_agebs(denue_csv):
    """Set de (loc, ageb) de Monterrey dentro del corredor, según DENUE (cualquier giro)."""
    agebs = set()
    with open(denue_csv, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("cve_mun") or "").strip().zfill(3) != "039":
                continue
            lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
            if den.in_corridor("039", lat, lon):
                loc = (row.get("cve_loc") or "").strip().lstrip("0") or "0"
                ageb = (row.get("ageb") or "").strip().upper().zfill(4)
                agebs.add((loc, ageb))
    return agebs


def agg(rows):
    """Agrega una lista de dicts de census → POBTOT + proxies (ponderando escolaridad por pob)."""
    pob = sum(r["POBTOT"] for r in rows if r.get("POBTOT"))
    viv = sum(r["VIVPAR_HAB"] for r in rows if r.get("VIVPAR_HAB"))
    auto = sum(r["VPH_AUTOM"] for r in rows if r.get("VPH_AUTOM"))
    inter = sum(r["VPH_INTER"] for r in rows if r.get("VPH_INTER"))
    esc_num = sum((r["GRAPROES"] or 0) * (r["POBTOT"] or 0) for r in rows if r.get("GRAPROES"))
    esc_den = sum(r["POBTOT"] or 0 for r in rows if r.get("GRAPROES"))
    return {
        "pobtot": int(pob),
        "escolaridad_grados": round(esc_num / esc_den, 2) if esc_den else None,
        "pct_auto": round(100 * auto / viv, 1) if viv else None,
        "pct_internet": round(100 * inter / viv, 1) if viv else None,
        "viviendas": int(viv),
        "fuente": "Censo 2020 INEGI, AGEB urbana NL",
        "confianza": "V-Censo",
    }


def main():
    if len(sys.argv) < 3:
        print("uso: extract_censo.py <censo_ageb.csv> <denue_19.csv>", file=sys.stderr)
        return 1
    censo_csv, denue_csv = sys.argv[1], sys.argv[2]

    mty_agebs = corridor_mty_agebs(denue_csv)
    print(f"AGEBs del corredor en Monterrey (DENUE): {len(mty_agebs)}")

    santiago, allende, mty = [], [], []
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f)
        header = next(r)
        # normaliza header (quita BOM)
        header = [h.lstrip("﻿") for h in header]
        idx = {name: header.index(name) for name in ["MUN", "LOC", "AGEB", "MZA"] + COLS}
        for row in r:
            def _i(v):
                try:
                    return int((v or "").strip())
                except ValueError:
                    return -1
            mun = _i(row[idx["MUN"]])
            loc_i = _i(row[idx["LOC"]])
            mza_i = _i(row[idx["MZA"]])
            loc = str(loc_i) if loc_i >= 0 else "0"
            ageb = row[idx["AGEB"]].strip().upper().zfill(4)
            rec = {c: to_num(row[idx[c]]) for c in COLS}
            # totales de municipio: LOC=0, AGEB=0000, MZA=0
            if loc_i == 0 and ageb == "0000":
                if mun == 49:
                    santiago.append(rec)
                elif mun == 4:
                    allende.append(rec)
                continue
            # Monterrey corredor: filas AGEB-total (MZA=0, AGEB real) en la whitelist
            if mun == 39 and mza_i == 0 and ageb != "0000" and (loc, ageb) in mty_agebs:
                mty.append(rec)

    out = {
        "_meta": {"fuente": "Censo de Población y Vivienda 2020, INEGI (AGEB urbana NL)",
                  "confianza": "V-Censo", "nota": "Proxies SES; el Censo no trae ingreso directo."},
        "Santiago": agg(santiago),
        "Allende": agg(allende),
        "Monterrey-corredor": agg(mty),
    }
    DATA.mkdir(exist_ok=True)
    (DATA / "demografia_corredor.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in ("Santiago", "Allende", "Monterrey-corredor"):
        d = out[k]
        print(f"  {k:20} pob={d['pobtot']:>7} escolaridad={d['escolaridad_grados']} "
              f"%auto={d['pct_auto']} %internet={d['pct_internet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
