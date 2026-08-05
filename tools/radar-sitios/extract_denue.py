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
import re
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

# ─────────────────────── Clasificación de restaurantes ───────────────────────
#
# SOLO por nom_estab (el nombre del local). NO se usa nombre_act (la descripción
# del SCIAN) y hay una razón dura: 231 de los 241 establecimientos que el filtro
# viejo devolvía comparten esta misma descripción del INEGI —
#
#   "Restaurantes con servicio de preparación de pizzas, hamburguesas,
#    hot dogs y pollos rostizados para llevar"
#
# — que contiene "pollos", "hamburguesas" Y "pizzas" a la vez. Usarla metía toda
# taquería y pizzería del SCIAN 722514 dentro de "competencia de pollo" (161 de
# 241 no tenían nada de pollo en su nombre) y, por el orden de los elif, vaciaba
# los conteos de hamburguesas y pizza. Ver DECISIONS D-013.
#
# El SCIAN sigue definiendo el universo (722* = restaurantes); ya no la categoría.

FRITO_KW = (
    "kfc", "kentucky", "church", "popeye", "campero",       # cadenas de frito
    "frito", "fried", "broaster", "broster", "crispy",      # descriptores
    "friend chicken",                                        # typo del DENUE por "fried"
    "club de pollo",                                         # nuestra propia cadena
)
ALITAS_KW = ("alita", "boneles", "boneless", "wings", "wing")
ASADO_KW = ("asado", "asada", "rostiz", "a la lena", "al carbon", "lena")
POLLO_KW = ("pollo", "chicken")
HAMB_KW = ("hamburgues", "burger", "carls", "carl's", "mcdonald", "wendy", "whopper")
PIZZA_KW = ("pizza", "domino", "little caesar", "papa john")

# Orden de prioridad: un nombre puede tocar varias listas y se queda con la primera.
# ("PIZZERIA DILIGENCIA PIZZA TACOS WINGS" cae en alitas, no en pizza — el
# drill-down del app deja ver estos casos y juzgarlos.)
CATEGORIAS = (
    ("pollo_frito", FRITO_KW),
    ("alitas", ALITAS_KW),
    ("pollo_asado", ASADO_KW),
    ("pollo_otro", POLLO_KW),
    ("hamburguesas", HAMB_KW),
    ("pizza", PIZZA_KW),
)

# Las que compiten por el mismo antojo de pollo (para el conteo agregado).
CATS_POLLO = ("pollo_frito", "alitas", "pollo_asado", "pollo_otro")


def categoria(nombre: str) -> str:
    """Categoría de un restaurante a partir de su nombre. 'otro' si no cae en ninguna.

    La coincidencia es por INICIO DE PALABRA, no subcadena: sin esto "BREWING"
    contiene "wing" y una cervecería se contaba como local de alitas.
    """
    n = norm(nombre)
    for cat, kws in CATEGORIAS:
        if any(re.search(r"\b" + re.escape(k), n) for k in kws):
            return cat
    return "otro"

# ─────────────────────────── Anclas de demanda ───────────────────────────
#
# Por CÓDIGO SCIAN exacto, no por prefijo. El prefijo mentía sobre la etiqueta
# (D-014): "4621" mete 228 minisúperes junto a 25 supermercados de verdad;
# "46411" mete 47 tiendas naturistas entre las farmacias; y "611" mete escuelas
# de arte, de deporte y profesores particulares junto a las primarias.
# Un Soriana y una tiendita de esquina no son la misma ancla para un local.
ANCLA_POR_CODIGO = {
    "462111": "supermercado",       # 25
    "462112": "minisuper",          # 228
    "464111": "farmacia",           # sin minisúper
    "464112": "farmacia",           # con minisúper
    "464113": "naturista",          # NO es farmacia: naturistas y homeopáticos
    "522110": "banco",
    "611111": "preescolar", "611112": "preescolar",
    "611121": "escuela_basica", "611122": "escuela_basica",   # primaria
    "611131": "escuela_basica", "611132": "escuela_basica",   # secundaria
    "611142": "escuela_basica", "611151": "escuela_basica",
    "611161": "escuela_basica", "611162": "escuela_basica",   # media superior
    "611171": "escuela_basica", "611172": "escuela_basica",   # multinivel
    "611211": "universidad", "611311": "universidad", "611312": "universidad",
}
# El resto de 611* (arte, deporte, idiomas, oficios, necesidades especiales,
# profesores particulares) y 71394* (gimnasios y clubes) se resuelven por prefijo.
ANCLA_POR_PREFIJO = (("611", "escuela_otra"), ("71394", "gimnasio"))

# Categorías que el app agrupa como "anclas de demanda" (generan tráfico).
CATS_ANCLA = ("supermercado", "minisuper", "farmacia", "naturista", "banco",
              "escuela_basica", "preescolar", "universidad", "escuela_otra", "gimnasio")


def ancla(codigo_act: str) -> str | None:
    """Categoría de ancla por código SCIAN exacto; None si no es ancla."""
    a = (codigo_act or "").strip()
    if a in ANCLA_POR_CODIGO:
        return ANCLA_POR_CODIGO[a]
    for pref, cat in ANCLA_POR_PREFIJO:
        if a.startswith(pref):
            return cat
    return None



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
    pollo, todos, sat_total, sat_pollo = [], [], {}, {}
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

            if act.startswith("722"):  # restaurantes: el universo competitivo
                sat_total[mun] = sat_total.get(mun, 0) + 1
                name = (row.get("nom_estab") or "").strip()
                cat = categoria(name)
                reg = {
                    "nombre": name,
                    "cat": cat,
                    "scian": act,
                    "actividad": (row.get("nombre_act") or "").strip(),
                    "tramo": tramo,
                    "colonia": (row.get("nomb_asent") or "").strip(),
                    "municipio": mun,
                    "ageb": (row.get("ageb") or "").strip(),
                    "cp": (row.get("cod_postal") or "").strip(),
                    "personal": (row.get("per_ocu") or "").strip(),
                    "lat": lat, "lon": lon,
                    "fuente": "DENUE INEGI 19 (may-2026)",
                    "confianza": "V-DENUE",
                }
                # Padrón completo: alimenta el drill-down del app (cada número
                # que se muestra se puede abrir y ver de qué locales sale).
                todos.append(reg)
                if cat in CATS_POLLO:
                    sat_pollo[mun] = sat_pollo.get(mun, 0) + 1
                    tramo_counts[tramo] = tramo_counts.get(tramo, 0) + 1
                    pollo.append({**reg, "pollo_frito": cat == "pollo_frito"})
                continue

            cat_a = ancla(act)                  # anclas de demanda (no restaurantes)
            if cat_a:
                ancla_counts.setdefault(cat_a, {})
                ancla_counts[cat_a][tramo] = ancla_counts[cat_a].get(tramo, 0) + 1
                nom_a = (row.get("nom_estab") or "").strip()
                anclas.append({
                    "nombre": nom_a[:40], "cat": cat_a, "tramo": tramo,
                    "municipio": mun, "lat": lat, "lon": lon,
                })
                # Las anclas viven en el MISMO padrón que los restaurantes: así sus
                # conteos también salen de un solo cálculo y también son abribles.
                todos.append({
                    "nombre": nom_a, "cat": cat_a, "scian": act,
                    "actividad": (row.get("nombre_act") or "").strip(),
                    "tramo": tramo, "colonia": (row.get("nomb_asent") or "").strip(),
                    "municipio": mun, "ageb": (row.get("ageb") or "").strip(),
                    "cp": (row.get("cod_postal") or "").strip(),
                    "personal": (row.get("per_ocu") or "").strip(),
                    "lat": lat, "lon": lon,
                    "fuente": "DENUE INEGI 19 (may-2026)", "confianza": "V-DENUE",
                })

    pollo.sort(key=lambda x: (x["municipio"], not x["pollo_frito"], x["colonia"]))
    DATA.mkdir(exist_ok=True)
    (DATA / "competencia_corredor.json").write_text(
        json.dumps({"_meta": {"fuente": "DENUE INEGI Nuevo León, corte may-2026",
                              "corte": "2026-05-12", "confianza": "V-DENUE",
                              "n": len(pollo)}, "establecimientos": pollo},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    # Padrón completo de restaurantes 722* del corredor: la base del drill-down.
    todos.sort(key=lambda x: (x["municipio"], x["cat"], x["nombre"]))
    (DATA / "establecimientos_corredor.json").write_text(
        json.dumps({"_meta": {"fuente": "DENUE INEGI Nuevo León, corte may-2026",
                              "corte": "2026-05-12", "confianza": "V-DENUE",
                              "universo": "restaurantes 722* + anclas de demanda del corredor",
                              "categoria_por": "nom_estab; NO se usa nombre_act (ver D-013)",
                              "n": len(todos)}, "establecimientos": todos},
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
