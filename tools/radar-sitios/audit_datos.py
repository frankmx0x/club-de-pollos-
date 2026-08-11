#!/usr/bin/env python3
"""Radar de Sitios — AUDITORÍA de los datos que ve el app.

Motivo (ley 1 y 4): un agente externo (Lovable) reescribió cifras a mano e inventó
valores. Esta auditoría re-deriva los números DESDE LAS FUENTES CRUDAS con un camino
de código independiente del pipeline, y los compara contra lo que el app sirve.

Comprueba:
  1. El app_data.json del APP es idéntico al que produce el pipeline (detecta ediciones a mano).
  2. Conteos de competencia (pollo/frito) recalculados desde el CSV del DENUE.
  3. Población y escolaridad recalculadas desde el CSV del Censo.
  4. Visitantes turísticos idénticos al XLSX de OSETUR.
  5. Aritmética interna: venta = residencial + turismo; residencial = pob × percápita × σ.
  6. Higiene: sin valores nulos disfrazados de 0, sin campos faltantes, sin duplicados.

Uso: audit_datos.py <denue.csv> <censo_ageb.csv> [ruta_app_data_del_app]
Salida: reporte PASS/FAIL en consola + data/auditoria.json. Exit 1 si algo falla.
"""
import csv
import json
import pathlib
import sys

import extract_denue as den

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
R_KM = 2.0
SIGMA = 0.06
CAPT_TUR = 0.05
TICKET = 220

res = []   # (nivel, check, detalle)


def ok(check, detalle=""):     res.append(("PASS", check, detalle))
def fail(check, detalle=""):   res.append(("FAIL", check, detalle))
def warn(check, detalle=""):   res.append(("WARN", check, detalle))


def main():
    denue_csv, censo_csv = sys.argv[1], sys.argv[2]
    app_path = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else pathlib.Path("/workspace/club-pollos-radar/public/data/app_data.json")

    pipe = json.loads((DATA / "app_data.json").read_text(encoding="utf-8"))

    # ---- 1. El app sirve EXACTAMENTE lo que produjo el pipeline -------------
    if app_path.exists():
        app_raw = app_path.read_text(encoding="utf-8")
        pipe_raw = (DATA / "app_data.json").read_text(encoding="utf-8")
        if app_raw == pipe_raw:
            ok("1. app_data del APP idéntico al del pipeline", f"{len(app_raw):,} bytes")
        else:
            app = json.loads(app_raw)
            difs = [k for k in set(list(app)) | set(list(pipe)) if app.get(k) != pipe.get(k)]
            fail("1. app_data del APP DIFIERE del pipeline (¿edición a mano?)", f"claves distintas: {difs}")
    else:
        warn("1. app_data del APP no encontrado (repo no clonado)", str(app_path))

    # ---- 2. Competencia recalculada desde el DENUE crudo --------------------
    # Camino independiente: recorre el CSV y cuenta pollo/frito por radio.
    colonias = pipe.get("colonias", [])
    centros = [(c["id"], c["centro"]["lat"], c["centro"]["lon"]) for c in colonias]
    pollo_pts, frito_pts, anclas_pts, n_puntos_corr = [], [], [], 0
    with open(denue_csv, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            cvem = (row.get("cve_mun") or "").strip().zfill(3)
            if cvem not in den.MUN:
                continue
            lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
            if lat is None or lon is None or not den.in_corridor(cvem, lat, lon):
                continue
            act = (row.get("codigo_act") or "").strip()
            if act.startswith("722"):
                blob = den.norm(row.get("nom_estab")) + " " + den.norm(row.get("nombre_act"))
                if any(t in blob for t in den.POLLO_KW):
                    n_puntos_corr += 1
                    pollo_pts.append((lat, lon))
                    if any(t in blob for t in den.POLLO_FRITO_KW):
                        frito_pts.append((lat, lon))
            else:
                for cat, fn in den.ANCLAS.items():
                    if fn(act):
                        anclas_pts.append((lat, lon)); break

    if n_puntos_corr == len(pipe.get("puntos", [])):
        ok("2a. competidores de pollo: app == DENUE crudo", f"{n_puntos_corr}")
    else:
        fail("2a. competidores de pollo NO cuadran", f"app={len(pipe.get('puntos', []))} vs crudo={n_puntos_corr}")

    if len(anclas_pts) == len(pipe.get("anclas", [])):
        ok("2b. anclas de demanda: app == DENUE crudo", f"{len(anclas_pts)}")
    else:
        fail("2b. anclas NO cuadran", f"app={len(pipe.get('anclas', []))} vs crudo={len(anclas_pts)}")

    malos = []
    for cid, clat, clon in centros:
        c = next(x for x in colonias if x["id"] == cid)
        p = sum(1 for a, b in pollo_pts if den._haversine_km(clat, clon, a, b) <= R_KM)
        fr = sum(1 for a, b in frito_pts if den._haversine_km(clat, clon, a, b) <= R_KM)
        if p != c["competencia"]["pollo_2km"] or fr != c["competencia"]["frito_2km"]:
            malos.append(f"{c['colonia']}: pollo {c['competencia']['pollo_2km']}≠{p} frito {c['competencia']['frito_2km']}≠{fr}")
    if malos:
        fail("2c. competencia por colonia NO cuadra", "; ".join(malos[:3]))
    else:
        ok("2c. competencia por colonia: app == recálculo", f"{len(centros)} colonias")

    # ---- 3. Demografía recalculada desde el Censo crudo ---------------------
    agsum = {}
    with open(denue_csv, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f):
            cvem = (row.get("cve_mun") or "").strip().zfill(3)
            if cvem not in den.MUN:
                continue
            lat, lon = den.fnum(row.get("latitud")), den.fnum(row.get("longitud"))
            if lat is None or lon is None or not den.in_corridor(cvem, lat, lon):
                continue
            def i(x):
                try: return int(str(x).strip())
                except (TypeError, ValueError): return -1
            k = (i(row.get("cve_mun")), i(row.get("cve_loc")), (row.get("ageb") or "").strip().upper().zfill(4))
            s = agsum.setdefault(k, [0.0, 0.0, 0]); s[0] += lat; s[1] += lon; s[2] += 1
    cent = {k: (v[0]/v[2], v[1]/v[2]) for k, v in agsum.items() if v[2] > 0}

    pobs, mun_tot = {}, {}
    with open(censo_csv, encoding="latin-1", newline="") as f:
        r = csv.reader(f); h = [c.lstrip("﻿") for c in next(r)]
        ix = {n: h.index(n) for n in ["MUN", "LOC", "AGEB", "MZA", "POBTOT", "GRAPROES"]}
        def i(x):
            try: return int((x or "").strip())
            except ValueError: return -1
        for row in r:
            ageb = row[ix["AGEB"]].strip().upper().zfill(4)
            k = (i(row[ix["MUN"]]), i(row[ix["LOC"]]), ageb)
            if i(row[ix["LOC"]]) == 0 and ageb == "0000":
                mun_tot[i(row[ix["MUN"]])] = i(row[ix["POBTOT"]])
            elif i(row[ix["LOC"]]) > 0 and i(row[ix["MZA"]]) == 0 and ageb != "0000":
                # POBTOT y GRAPROES se parsean POR SEPARADO: hay 47 AGEBs con
                # escolaridad suprimida ("*") y población > 0. Parsearlos juntos
                # tiraba esa población a 0 y producía un falso positivo.
                def f(v):
                    try: return float((v or "").strip())
                    except ValueError: return None
                pobs[k] = {"pob": f(row[ix["POBTOT"]]) or 0.0, "esc": f(row[ix["GRAPROES"]])}

    # cruce contra cifras oficiales conocidas del Censo 2020
    for cve, nombre, esperado in [(49, "Santiago", 46784), (4, "Allende", 35289)]:
        if mun_tot.get(cve) == esperado:
            ok(f"3a. POBTOT {nombre} == Censo 2020", f"{esperado:,}")
        else:
            fail(f"3a. POBTOT {nombre} NO cuadra", f"censo={mun_tot.get(cve)} esperado={esperado}")

    malos = []
    for cid, clat, clon in centros:
        c = next(x for x in colonias if x["id"] == cid)
        pob = sum(pobs[k]["pob"] for k, xy in cent.items()
                  if k in pobs and den._haversine_km(clat, clon, xy[0], xy[1]) <= R_KM)
        if int(pob) != c["demografia"]["poblacion_2km"]:
            malos.append(f"{c['colonia']}: {c['demografia']['poblacion_2km']}≠{int(pob)}")
    if malos:
        fail("3b. población por colonia NO cuadra", "; ".join(malos[:3]))
    else:
        ok("3b. población por colonia: app == recálculo Censo", f"{len(centros)} colonias")

    # ---- 4. Turismo idéntico al XLSX de OSETUR ------------------------------
    try:
        parques = json.loads((DATA / "visitantes_parques_nl.json").read_text(encoding="utf-8"))["parques"]
        cola = next(p for p in parques if "caballo" in str(p.get("parque", "")).lower())
        meses = [v for k, v in cola.items() if k.startswith("v_") and isinstance(v, (int, float))]
        prom = int(sum(meses) / len(meses))
        z = next((x for x in pipe["zonas"] if x.get("turismo")), None)
        if z and abs(z["turismo"]["visitantes_mes"] - prom) <= 1:
            ok("4. visitantes Cola de Caballo == OSETUR", f"{prom:,}/mes (promedio de {len(meses)} meses)")
        else:
            fail("4. visitantes NO cuadran", f"app={z['turismo']['visitantes_mes'] if z else None} vs OSETUR={prom}")
    except Exception as e:
        warn("4. turismo no verificable", str(e)[:60])

    # ---- 5. Aritmética interna ---------------------------------------------
    malos = []
    for c in colonias:
        v = c["venta"]
        if v["residencial"] + v["turismo"] != v["total"]:
            malos.append(f"{c['colonia']}: suma")
        esperado = int(c["demografia"]["poblacion_2km"] * c["demografia"]["percapita_qsr"] * SIGMA)
        if abs(esperado - v["residencial"]) > 1:
            malos.append(f"{c['colonia']}: residencial {v['residencial']}≠{esperado}")
        if c.get("turismo"):
            et = int(c["turismo"]["visitantes_mes"] * CAPT_TUR * TICKET)
            if abs(et - v["turismo"]) > 1:
                malos.append(f"{c['colonia']}: turismo {v['turismo']}≠{et}")
    if malos:
        fail("5. aritmética de venta NO cuadra", "; ".join(malos[:3]))
    else:
        ok("5. aritmética de venta consistente", "residencial+turismo, pob×percápita×σ")

    # ---- 6. Higiene de datos ------------------------------------------------
    problemas = []
    ids = [c["id"] for c in colonias]
    if len(ids) != len(set(ids)):
        problemas.append("ids de colonia duplicados")
    for c in colonias:
        if c["demografia"]["poblacion_2km"] == 0:
            problemas.append(f"{c['colonia']}: población 0 (¿ausente disfrazado?)")
        if c["demografia"]["escolaridad"] is None:
            problemas.append(f"{c['colonia']}: escolaridad ausente")
    for p in pipe.get("puntos", []):
        if not (24 < p["lat"] < 27) or not (-101 < p["lon"] < -99):
            problemas.append(f"punto fuera de NL: {p['n']}"); break
    if problemas:
        fail("6. higiene de datos", "; ".join(problemas[:3]))
    else:
        ok("6. higiene de datos", f"{len(colonias)} colonias, {len(pipe.get('puntos', []))} puntos, sin ceros disfrazados")

    # ---- Reporte ------------------------------------------------------------
    print("\nAUDITORÍA DE DATOS — Radar de Sitios\n" + "=" * 64)
    for nivel, check, detalle in res:
        icon = {"PASS": "✓", "FAIL": "✗", "WARN": "!"}[nivel]
        print(f"  {icon} [{nivel}] {check}" + (f"\n        {detalle}" if detalle else ""))
    n_fail = sum(1 for n, _, _ in res if n == "FAIL")
    n_warn = sum(1 for n, _, _ in res if n == "WARN")
    print("=" * 64)
    print(f"  {len(res)-n_fail-n_warn} PASS · {n_fail} FAIL · {n_warn} WARN")

    (DATA / "auditoria.json").write_text(json.dumps(
        {"resultados": [{"nivel": n, "check": c, "detalle": d} for n, c, d in res],
         "resumen": {"pass": len(res)-n_fail-n_warn, "fail": n_fail, "warn": n_warn}},
        ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())

def check_padron_cuadra(app, here):
    """Cada conteo por categoría debe salir EXACTAMENTE de la lista que el app abre
    al hacer clic. Si esto falla, el drill-down miente y el número pierde autoridad."""
    import json as _json
    pad_p = here / "data" / "establecimientos_corredor.json"
    if not pad_p.exists():
        return [("padron", "SKIP", "falta establecimientos_corredor.json")]
    pad = _json.loads(pad_p.read_text(encoding="utf-8"))["establecimientos"]
    CP = ("pollo_frito", "alitas", "pollo_asado", "pollo_otro")
    mal = 0
    for c in app.get("colonias", []):
        idx = c.get("rest_idx")
        if idx is None:
            mal += 1
            continue
        cats = {}
        for i in idx:
            cats[pad[i]["cat"]] = cats.get(pad[i]["cat"], 0) + 1
        k = c["competencia"]
        # El padrón trae restaurantes Y anclas (D-014): "restaurantes" suma solo
        # las categorías de restaurante, no todo el radio.
        CR = ("pollo_frito", "alitas", "pollo_asado", "pollo_otro",
              "hamburguesas", "pizza", "otro")
        pares = [
            (k.get("frito_2km", 0), cats.get("pollo_frito", 0)),
            (k.get("alitas_2km", 0), cats.get("alitas", 0)),
            (k.get("hamburguesas_2km", 0), cats.get("hamburguesas", 0)),
            (k.get("pizza_2km", 0), cats.get("pizza", 0)),
            (k.get("restaurantes_2km", 0), sum(cats.get(x, 0) for x in CR)),
            (k.get("pollo_2km", 0), sum(cats.get(x, 0) for x in CP)),
        ]
        mal += sum(1 for a, b in pares if a != b)
    estado = "PASS" if mal == 0 else "FALLA"
    return [("padron cuadra con el drill-down", estado,
             f"{mal} descuadres entre conteo mostrado y lista abrible")]


def check_venta_recomputable(app, here):
    """La venta residencial debe salir EXACTAMENTE de lo que la tabla muestra:
    pob × percápita × 8% ÷ (1 + fritos + 0.5×alitas). Ver D-016."""
    mal = 0
    for c in app.get("colonias", []):
        k, d, v = c["competencia"], c["demografia"], c["venta"]
        jug = 1 + k.get("frito_2km", 0) + 0.5 * k.get("alitas_2km", 0)
        esp = int(round(d["poblacion_2km"] * d["percapita_qsr"] * 0.08 / jug))
        if v["residencial"] != esp or v["total"] != v["residencial"] + v["turismo"]:
            mal += 1
    return [("venta recomputable a mano (D-016)", "PASS" if mal == 0 else "FALLA",
             f"{mal} colonias con venta que no cuadra con sus propios conteos")]
