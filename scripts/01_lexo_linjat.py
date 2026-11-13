"""
HAPI 1 (versioni 2): Leximi i linjave te autobuseve te Tiranes nga skedari i OpenStreetMap
==========================================================================================

Pse versioni 2:
  Serverat Overpass nuk pranonin kerkesa nga lidhja jone. Prandaj e shkarkojme
  harten e plote te Shqiperise si nje skedar te vetem (albania-latest.osm.pbf)
  nga Geofabrik dhe e lexojme lokalisht. Nuk varemi me nga asnje server.

Cfare eshte skedari .osm.pbf:
  Eshte e gjithe harta e OpenStreetMap per Shqiperine, e kompresuar.
  Ka tre lloje objektesh:
    - node (nyje):      nje pike me koordinata, p.sh. nje stacion autobusi
    - way (rruge):      nje varg nyjesh, p.sh. nje segment rruge
    - relation (relacion): grup objektesh, p.sh. nje linje autobusi
                        = stacionet e saj + rruget nga kalon

Si funksionon skripti (ne dy kalime mbi skedarin):
  Kalimi 1: gjejme te gjitha relacionet me route=bus dhe kujtojme
            cilat nyje dhe rruge u perkasin.
  Kalimi 2: lexojme vetem ato nyje (stacionet) dhe rruge (me koordinata)
            qe na duhen.
  Pastaj mbajme vetem linjat qe kalojne brenda Tiranes dhe ruajme:
    - data/linjat.json      -> per kodin tone (hapat e ardhshem)
    - data/linjat.geojson   -> per ta pare ne harte (p.sh. ne geojson.io)

Si ekzekutohet:
  pip install osmium
  python scripts/01_lexo_linjat.py
"""

import json
import math
import os
import sys

try:
    import osmium
except ImportError:
    raise SystemExit("Mungon libraria 'osmium'. Instaloje me:  pip install osmium")

# Drejtkendeshi qe mbulon Tiranen: (lat_jug, lon_perendim, lat_veri, lon_lindje)
TIRANA_BBOX = (41.25, 19.70, 41.40, 19.92)

KETU = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(KETU, "..", "data"))
SKEDARI_OSM = os.path.join(DATA_DIR, "albania-latest.osm.pbf")


# ---------------------------------------------------------------------------
# Kalimi 1: gjej linjat e autobusit
# ---------------------------------------------------------------------------
class GjejLinjat(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.relacionet = []
        self.nyjet_e_nevojshme = set()
        self.rruget_e_nevojshme = set()

    def relation(self, r):
        if r.tags.get("route") != "bus":
            return
        anetaret = []
        for m in r.members:
            anetaret.append({"type": {"n": "node", "w": "way", "r": "relation"}[m.type],
                             "ref": m.ref, "role": m.role})
            if m.type == "n":
                self.nyjet_e_nevojshme.add(m.ref)
            elif m.type == "w":
                self.rruget_e_nevojshme.add(m.ref)
        # objekti 'r' nuk vlen pas ketij funksioni, prandaj kopjojme te dhenat
        self.relacionet.append({"type": "relation", "id": r.id,
                                "tags": {t.k: t.v for t in r.tags},
                                "members": anetaret})


# ---------------------------------------------------------------------------
# Kalimi 2: lexo stacionet dhe gjeometrine e rrugeve
# ---------------------------------------------------------------------------
class LexoGjeometrine(osmium.SimpleHandler):
    def __init__(self, nyjet, rruget):
        super().__init__()
        self.nyjet_kerkuara = nyjet
        self.rruget_kerkuara = rruget
        self.nyjet = {}
        self.rruget = {}

    def node(self, n):
        if n.id in self.nyjet_kerkuara and n.location.valid():
            self.nyjet[n.id] = {"type": "node", "id": n.id,
                                "lat": n.location.lat, "lon": n.location.lon,
                                "tags": {t.k: t.v for t in n.tags}}

    def way(self, w):
        if w.id not in self.rruget_kerkuara:
            return
        gjeom = [{"lat": nd.location.lat, "lon": nd.location.lon}
                 for nd in w.nodes if nd.location.valid()]
        if gjeom:
            self.rruget[w.id] = {"type": "way", "id": w.id, "geometry": gjeom}


# ---------------------------------------------------------------------------
# Perpunimi
# ---------------------------------------------------------------------------
def distanca_m(lat1, lon1, lat2, lon2):
    """Distanca ne metra mes dy pikave (formula Haversine)."""
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def brenda_tiranes(lat, lon):
    s, w, n, e = TIRANA_BBOX
    return s <= lat <= n and w <= lon <= e


def nderto_linjat(relacionet, nyjet, rruget):
    linjat = []
    for rel in relacionet:
        tags = rel["tags"]
        stacionet, segmentet = [], []
        for m in rel["members"]:
            roli = m["role"]
            if m["type"] == "node" and m["ref"] in nyjet and roli.startswith(("stop", "platform")):
                nd = nyjet[m["ref"]]
                emri = nd["tags"].get("name", "(pa emer)")
                # shmangim dublikatet (stop + platform me te njejtin emer njeri pas tjetrit)
                if stacionet and stacionet[-1]["emri"] == emri:
                    continue
                stacionet.append({"id": nd["id"], "emri": emri, "lat": nd["lat"], "lon": nd["lon"]})
            elif m["type"] == "way" and m["ref"] in rruget and roli in ("", "forward", "backward"):
                segmentet.append([[p["lon"], p["lat"]] for p in rruget[m["ref"]]["geometry"]])

        # mbajme vetem linjat qe kane te pakten nje pike brenda Tiranes
        pikat = [(s["lat"], s["lon"]) for s in stacionet] + \
                [(p[1], p[0]) for seg in segmentet for p in seg]
        if not any(brenda_tiranes(lat, lon) for lat, lon in pikat):
            continue

        gjatesia = sum(distanca_m(a[1], a[0], b[1], b[0])
                       for seg in segmentet for a, b in zip(seg, seg[1:]))
        linjat.append({
            "osm_id": rel["id"],
            "ref": tags.get("ref", ""),
            "emri": tags.get("name", "(pa emer)"),
            "nga": tags.get("from", ""),
            "per": tags.get("to", ""),
            "operatori": tags.get("operator", ""),
            "ngjyra": tags.get("colour", ""),        # ngjyra zyrtare e linjes, p.sh. "#E30613"
            "intervali": tags.get("interval", ""),   # sa minuta mes dy autobuseve, p.sh. "15"
            "gjatesia_km": round(gjatesia / 1000, 1),
            "stacionet": stacionet,
            "segmentet": segmentet,
        })
    linjat.sort(key=lambda l: (l["ref"], l["emri"]))
    return linjat


def ne_geojson(linjat):
    features = []
    for l in linjat:
        props = {k: l[k] for k in ("ref", "emri", "nga", "per", "gjatesia_km")}
        if l["segmentet"]:
            features.append({"type": "Feature",
                             "properties": {**props, "lloji": "linje"},
                             "geometry": {"type": "MultiLineString", "coordinates": l["segmentet"]}})
        for s in l["stacionet"]:
            features.append({"type": "Feature",
                             "properties": {"lloji": "stacion", "emri": s["emri"], "linja": l["ref"] or l["emri"]},
                             "geometry": {"type": "Point", "coordinates": [s["lon"], s["lat"]]}})
    return {"type": "FeatureCollection", "features": features}


def main():
    skedari = sys.argv[1] if len(sys.argv) > 1 else SKEDARI_OSM
    if not os.path.exists(skedari):
        raise SystemExit(
            f"Nuk u gjet skedari:\n  {skedari}\n"
            "Shkarkoje nga https://download.geofabrik.de/europe/albania-latest.osm.pbf\n"
            "dhe vendose ne dosjen data/ te projektit."
        )

    print("Kalimi 1: po kerkoj linjat e autobusit ne te gjithe Shqiperine...")
    k1 = GjejLinjat()
    k1.apply_file(skedari)
    print(f"  U gjenden {len(k1.relacionet)} linja autobusi ne Shqiperi.")

    print("Kalimi 2: po lexoj stacionet dhe rruget e tyre (mund te zgjase 1-2 minuta)...")
    k2 = LexoGjeometrine(k1.nyjet_e_nevojshme, k1.rruget_e_nevojshme)
    k2.apply_file(skedari, locations=True)  # locations=True: na jep koordinatat e cdo rruge

    linjat = nderto_linjat(k1.relacionet, k2.nyjet, k2.rruget)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "linjat.json"), "w", encoding="utf-8") as f:
        json.dump(linjat, f, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA_DIR, "linjat.geojson"), "w", encoding="utf-8") as f:
        json.dump(ne_geojson(linjat), f, ensure_ascii=False)

    # Permbledhja
    print()
    print(f"Ne Tirane: {len(linjat)} linja (cdo drejtim llogaritet vecmas).")
    print("-" * 78)
    print(f"{'Ref':<6} {'Stacione':>8} {'Km':>6}  Emri")
    print("-" * 78)
    for l in linjat:
        print(f"{l['ref']:<6} {len(l['stacionet']):>8} {l['gjatesia_km']:>6}  {l['emri'][:55]}")
    pa_stacione = sum(1 for l in linjat if not l["stacionet"])
    unike = {s["id"] for l in linjat for s in l["stacionet"]}
    print("-" * 78)
    print(f"Stacione unike gjithsej: {len(unike)}")
    print(f"Linja pa asnje stacion te shenuar: {pa_stacione}  (keto do t'i plotesojme vete)")
    print()
    print(f"Skedaret u ruajten ne: {DATA_DIR}")
    print("  linjat.json, linjat.geojson")
    print("Hap linjat.geojson ne https://geojson.io per t'i pare ne harte.")


if __name__ == "__main__":
    main()
