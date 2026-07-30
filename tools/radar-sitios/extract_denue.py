#!/usr/bin/env python3
"""Radar de Sitios — pipeline v1: extrae competencia real del corredor sur desde DENUE.

Entrada: CSV masivo DENUE de Nuevo León (INEGI, gratis, sin key).
  Descargar:  curl -o denue_19.zip \
    https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip
  Descomprimir: conjunto_de_datos/denue_inegi_19_.csv

Salida (en data/):
  - competencia_corredor.json : cada establecimiento de pollo/QSR del corredor
    con colonia, AGEB, lat/lon, personal, SCIAN. Fuente dura [V-DENUE].
  - saturacion_corredor.json  : conteos por municipio y por tramo.

El corredor = Monterrey SUR (bounding box del eje Garza Sada→Carretera Nacional) +
Santiago (completo) + Allende (completo). Monterrey se geo-filtra porque el municipio
completo (1.1M hab) desbordaría el corredor.

REGLA (ley 4): esto es DENUE (censo oficial de unidades económicas, corte may-2026),
nivel [V-DENUE] = dato duro con fuente. Distinto de los datos [S] de la semilla.
"""
import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
DEFAULT_CSV = HERE / "conjunto_de_datos" / "denue_inegi_19_.csv"

# cve_mun dentro de Nuevo León (cve_ent=19)
MUN = {"039": "Monterrey", "049": "Santiago", "004": "Allende", "026": "Guadalupe"}

# Corredor sur como POLILÍNEA real (no caja): eje ITESM → Contry → La Estanzuela →
# Santiago (El Cercado) → Allende centro. Para Monterrey incluimos lo que esté a <=2.5 km
# de esta línea — esto AÍSLA el corredor sur y DEJA FUERA el Centro/norte de Monterrey
# (que quedaba mal incluido con un bounding box). Santiago y Allende se toman completos.
CORRIDOR_LINE = [
    (25.6512, -100.2895),  # ITESM / Tecnológico
    (25.6300, -100.2700),  # Contry
    (25.5900, -100.2550),  # La Estanzuela / Carretera Nacional
    (25.4318, -100.1520),  # Santiago (El Cercado)
    (25.2793, -100.0155),  # Allende centro
]
CORRIDOR_LABELS = ["Tec/Garza Sada", "Contry", "Carr.Nacional/Estanzuela", "Santiago", "Allende"]
MTY_BUFFER_KM = 2.0

# Clasificación de competencia por palabra clave (nom_estab / nombre_act, sin acentos, lower)
POLLO_KW = ("pollo", "kfc", "church", "popeye", "rostiz", "pollos", "fried chicken", "campero")
POLLO_FRITO_KW = ("kfc", "church", "popeye", "frito", "fried", "broaster", "crispy", "club de pollo")

# Comida rápida vecina (contexto competitivo, no pollo): por palabra clave.
HAMB_KW = ("hamburgues", "burger", "carls", "carl's", "mcdonald", "wendy")
PIZZA_KW = ("pizza", "domino", "little caesar", "papa john")

# Anclas de demanda: otras unidades económicas del corredor (no competidores), por SCIAN.
# Generan tráfico / demanda alrededor de un local candidato.
ANCLAS = {
    "escuela": lambda a: a.startswith("611"),
    "supermercado": lambda a: a.startswith("4621"),
    "banco": lambda a: a.startswith("5221"),
    "farmacia": lambda a: a.startswith("46411"),
    "gimnasio": lambda a: a.startswith("71394"),
}


def norm(s: str) -> str:
    s = (s or "").lower()
    for a, b in zip("áéíóúñ", "aeioun"):
        s = s.replace(a, b)
    return s


def _haversine_km(a_lat, a_lon, b_lat, b_lon):
    from math import radians, sin, cos, asin, sqrt
    dlat, dlon = radians(b_lat - a_lat), radians(b_lon - a_lon)
    h = sin(dlat / 2) ** 2 + cos(radians(a_lat)) * cos(radians(b_lat)) * sin(dlon / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(h))


def _dist_to_segment_km(p_lat, p_lon, a, b):
    # Aproximación plana local (equirectangular) para proyección punto→segmento; luego
    # haversine para la distancia final. Suficiente a escala de pocos km.
    from math import radians, cos
    lat0 = radians((a[0] + b[0]) / 2)
    def xy(lat, lon):
        return (radians(lon) * cos(lat0) * 6371.0, radians(lat) * 6371.0)
    px, py = xy(p_lat, p_lon); ax, ay = xy(*a); bx, by = xy(*b)
    dx, dy = bx - ax, by - ay
    seg2 = dx * dx + dy * dy
    t = 0.0 if seg2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / seg2))
    proj_lat = a[0] + t * (b[0] - a[0])
    proj_lon = a[1] + t * (b[1] - a[1])
    return _haversine_km(p_lat, p_lon, proj_lat, proj_lon)


def dist_to_corridor_km(lat, lon):
    return min(_dist_to_segment_km(lat, lon, CORRIDOR_LINE[i], CORRIDOR_LINE[i + 1])
              for i in range(len(CORRIDOR_LINE) - 1))


def nearest_tramo(lat, lon):
    if lat is None or lon is None:
        return "sin-coord"
    dists = [_haversine_km(lat, lon, v[0], v[1]) for v in CORRIDOR_LINE]
    return CORRIDOR_LABELS[dists.index(min(dists))]


def in_corridor(cve_mun: str, lat: float, lon: float) -> bool:
    if cve_mun in ("049", "004"):  # Santiago, Allende completos
        return True
    if cve_mun == "039":  # Monterrey: solo lo cercano a la polilínea del corredor
        return (lat is not None and lon is not None
                and dist_to_corridor_km(lat, lon) <= MTY_BUFFER_KM)
    return False


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main() -> int:
    csv_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.exists():
        print(f"ERROR: falta {csv_path}. Descarga y descomprime denue_19.zip primero.", file=sys.stderr)
        return 1

    # DENUE viene en latin-1 / cp1252
    enc = "latin-1"
    pollo, sat_total, sat_pollo = [], {}, {}
    tramo_counts = {}
    anclas, ancla_counts = [], {}

    with csv_path.open(encoding=enc, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            cve_mun = (row.get("cve_mun") or "").strip().zfill(3)
            if cve_mun not in MUN:
                continue
            lat, lon = fnum(row.get("latitud")), fnum(row.get("longitud"))
            if not in_corridor(cve_mun, lat, lon):
                continue
            act = (row.get("codigo_act") or "").strip()
            mun = MUN[cve_mun]
            tramo = nearest_tramo(lat, lon)

            if act.startswith("722"):  # restaurantes: competencia potencial
                sat_total[mun] = sat_total.get(mun, 0) + 1
                name = row.get("nom_estab") or ""
                blob = norm(name) + " " + norm(row.get("nombre_act"))
                if any(k in blob for k in POLLO_KW):
                    sat_pollo[mun] = sat_pollo.get(mun, 0) + 1
                    tramo_counts[tramo] = tramo_counts.get(tramo, 0) + 1
                    pollo.append({
                        "nombre": name.strip(),
                        "scian": act,
                        "actividad": (row.get("nombre_act") or "").strip(),
                        "pollo_frito": any(k in blob for k in POLLO_FRITO_KW),
                        "tramo": tramo,
                        "colonia": (row.get("nomb_asent") or "").strip(),
                        "municipio": mun,
                        "ageb": (row.get("ageb") or "").strip(),
                        "cp": (row.get("cod_postal") or "").strip(),
                        "personal": (row.get("per_ocu") or "").strip(),
                        "lat": lat, "lon": lon,
                        "fuente": "DENUE INEGI 19 (may-2026)",
                        "confianza": "V-DENUE",
                    })
                continue

            for cat, fn in ANCLAS.items():  # anclas de demanda (no restaurantes)
                if fn(act):
                    ancla_counts.setdefault(cat, {})
                    ancla_counts[cat][tramo] = ancla_counts[cat].get(tramo, 0) + 1
                    anclas.append({
                        "nombre": (row.get("nom_estab") or "").strip()[:40],
                        "cat": cat, "tramo": tramo, "municipio": mun,
                        "lat": lat, "lon": lon,
                    })
                    break

    pollo.sort(key=lambda x: (x["municipio"], not x["pollo_frito"], x["colonia"]))
    DATA.mkdir(exist_ok=True)
    (DATA / "competencia_corredor.json").write_text(
        json.dumps({"_meta": {"fuente": "DENUE INEGI Nuevo León, corte may-2026",
                              "corte": "2026-05-12", "confianza": "V-DENUE",
                              "n": len(pollo)}, "establecimientos": pollo},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    (DATA / "saturacion_corredor.json").write_text(
        json.dumps({"restaurantes_722_por_municipio": sat_total,
                    "pollo_por_municipio": sat_pollo,
                    "pollo_por_tramo": tramo_counts,
                    "fuente": "DENUE INEGI 19 (may-2026)"},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    (DATA / "anclas_corredor.json").write_text(
        json.dumps({"_meta": {"fuente": "DENUE INEGI Nuevo León, corte may-2026",
                              "corte": "2026-05-12", "confianza": "V-DENUE", "n": len(anclas)},
                    "conteo_por_tramo": ancla_counts, "anclas": anclas},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"OK. Competencia de pollo en corredor: {len(pollo)}")
    print(f"   Anclas de demanda: {len(anclas)} { {k: sum(v.values()) for k, v in ancla_counts.items()} }")
    print(f"   Restaurantes 722* por municipio: {sat_total}")
    print(f"   Pollo por municipio: {sat_pollo}")
    print(f"   Pollo por tramo: {tramo_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
