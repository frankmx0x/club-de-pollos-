#!/usr/bin/env python3
"""Radar de Sitios — empaqueta un snapshot COMPACTO para la web app (Radar v2).

Combina seed.json (zonas/scores/demografía/competencia) + competencia_corredor.json
(competidores georreferenciados) + anclas_corredor.json (escuelas, supermercados, etc.)
en un solo bundle que el app de presentación consume. Añade el bloque `fuentes` con
procedencia oficial y la última sincronización (timestamp real de esta corrida).

Es un SNAPSHOT de nuestro pipeline (fuente de verdad = este repo), fechado y citado.
No hay "datos live": son datasets oficiales con fecha de corte (ley 4).

Salida: data/app_data.json
"""
import datetime
import json
import pathlib

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"

# Mapa tramo (DENUE) → zona (seed.json)
TRAMO_A_ZONA = {
    "Tec/Garza Sada": "garza-sada-tec",
    "Contry": "garza-sada-tec",
    "Carr.Nacional/Estanzuela": "carretera-nacional-estanzuela",
    "Santiago": "santiago-cercado",
    "Allende": "allende-centro",
}
CAT_SHORT = {"escuela": "esc", "supermercado": "sup", "banco": "ban",
             "farmacia": "far", "gimnasio": "gim"}


def main():
    seed = json.loads((DATA / "seed.json").read_text(encoding="utf-8"))
    comp = json.loads((DATA / "competencia_corredor.json").read_text(encoding="utf-8"))
    anc = json.loads((DATA / "anclas_corredor.json").read_text(encoding="utf-8"))

    # Competidores (puntos)
    puntos = [{"n": e["nombre"][:40], "lat": round(e["lat"], 5), "lon": round(e["lon"], 5),
               "frito": bool(e["pollo_frito"]), "tramo": e.get("tramo", ""), "mun": e["municipio"]}
              for e in comp["establecimientos"] if e.get("lat") and e.get("lon")]

    # Anclas de demanda (puntos, categoría corta)
    anclas = [{"n": a["nombre"][:30], "lat": round(a["lat"], 5), "lon": round(a["lon"], 5),
               "cat": CAT_SHORT.get(a["cat"], a["cat"]), "tramo": a.get("tramo", "")}
              for a in anc["anclas"] if a.get("lat") and a.get("lon")]

    # Conteo de anclas por zona (para el panel y para alimentar el score de demanda)
    zona_anclas = {}
    for cat, portramo in anc["conteo_por_tramo"].items():
        for tramo, n in portramo.items():
            z = TRAMO_A_ZONA.get(tramo)
            if not z:
                continue
            zona_anclas.setdefault(z, {})
            zona_anclas[z][cat] = zona_anclas[z].get(cat, 0) + n
    for zona in seed["tramos"]:
        zona["anclas_denue"] = {"conteo": zona_anclas.get(zona["id"], {}),
                                "fuente": "DENUE may-2026", "confianza": "V-DENUE"}

    ahora = datetime.datetime.now().astimezone()

    fuentes = {
        "ultima_sincronizacion": ahora.isoformat(timespec="minutes"),
        "ultima_sincronizacion_txt": ahora.strftime("%d/%m/%Y %H:%M") + " (America/Monterrey)",
        "modo": "snapshot",
        "aviso_live": "Datos de fuentes OFICIALES con fecha de corte; no es tiempo real. "
                      "'Última sincronización' = fecha en que corrió el pipeline de este proyecto.",
        "datasets": [
            {"nombre": "DENUE — Directorio Estadístico Nacional de Unidades Económicas",
             "institucion": "INEGI", "corte": "mayo 2026", "confianza": "V-DENUE",
             "cobertura": "Nuevo León — competencia de pollo y anclas de demanda (escuelas, supermercados, bancos, farmacias, gimnasios)",
             "url": "https://www.inegi.org.mx/app/mapa/denue/",
             "licencia": "Datos Abiertos INEGI", "actualizacion": "≈ semestral"},
            {"nombre": "Censo de Población y Vivienda 2020 — AGEB urbana",
             "institucion": "INEGI", "corte": "2020", "confianza": "V-Censo",
             "cobertura": "Nuevo León — demografía y nivel socioeconómico (población, escolaridad, internet, automóvil)",
             "url": "https://www.inegi.org.mx/programas/ccpv/2020/",
             "licencia": "Datos Abiertos INEGI", "actualizacion": "decenal"},
        ],
        "metodo": "Extracción georreferenciada al corredor (polilínea ITESM→Allende, buffer 2 km en Monterrey). "
                  "Pipeline reproducible en el repo club-de-pollos- (tools/radar-sitios/).",
        "pendiente_S": "La RENTA aún es snapshot de búsqueda [S], no oficial; por confirmar.",
    }

    corridor = [
        {"n": "ITESM / Tec", "lat": 25.6512, "lon": -100.2895},
        {"n": "Contry", "lat": 25.6300, "lon": -100.2700},
        {"n": "La Estanzuela", "lat": 25.5900, "lon": -100.2550},
        {"n": "Santiago (El Cercado)", "lat": 25.4318, "lon": -100.1520},
        {"n": "Allende centro", "lat": 25.2793, "lon": -100.0155},
    ]

    # Colonias (fase colonias): unidad fina de decisión. Las zonas quedan como contexto.
    try:
        col = json.loads((DATA / "colonias_corredor.json").read_text(encoding="utf-8"))
        colonias, col_meta = col["colonias"], col["_meta"]
    except FileNotFoundError:
        colonias, col_meta = [], None

    # Metodología (cómo se llegó a cada número) y puntos óptimos multi-colonia
    try:
        metodologia = json.loads((HERE / "metodologia.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        metodologia = None
    try:
        puntos_opt = json.loads((DATA / "puntos_optimos.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        puntos_opt = None

    # Insights curados (banco de conclusiones con su respaldo — HERE/insights.json)
    try:
        ins = json.loads((HERE / "insights.json").read_text(encoding="utf-8"))
        insights, ins_meta = sorted(ins["insights"], key=lambda x: x["orden"]), ins["_meta"]
    except FileNotFoundError:
        insights, ins_meta = [], None

    bundle = {
        "_meta": {"titulo": "Radar de Sitios — Corredor Sur (Club de Pollos)",
                  "snapshot": seed["_meta"]["fecha"], "version": seed["_meta"]["version"],
                  "niveles": seed["_meta"]["niveles"]},
        "fuentes": fuentes,
        "metodologia": metodologia,
        "puntos_optimos": puntos_opt,
        "insights": insights,
        "insights_meta": ins_meta,
        "colonias": colonias,
        "colonias_meta": col_meta,
        "zonas": seed["tramos"],
        "club_de_pollos": seed["club_de_pollos_en_corredor"],
        "puntos": puntos,
        "anclas": anclas,
        "corredor": corridor,
    }
    out = DATA / "app_data.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"OK: {out.name} · zonas={len(bundle['zonas'])} · competidores={len(puntos)} · "
          f"anclas={len(anclas)} · {out.stat().st_size/1024:.1f} KB")
    print(f"   última sincronización: {fuentes['ultima_sincronizacion_txt']}")


if __name__ == "__main__":
    main()
