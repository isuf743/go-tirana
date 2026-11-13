"""
HAPI 1: Shkarkimi i linjave te autobuseve te Tiranes nga OpenStreetMap
=======================================================================

Cfare ben ky skript:
  1. I dergon nje pyetje (query) serverit Overpass, qe eshte "motori i kerkimit"
     i OpenStreetMap. I kerkojme te gjitha linjat e autobusit (route=bus)
     brenda nje drejtkendeshi qe mbulon Tiranen.
  2. Ruan pergjigjen e plote ne data/osm_raw.json (te dhenat e paperpunuara).
  3. Nxjerr prej saj ate qe na duhet: emrin e linjes, stacionet (me koordinata)
     dhe gjurmen e rruges, dhe i ruan ne:
        - data/linjat.json      -> per kodin tone (hapat e ardhshem)
        - data/linjat.geojson   -> per ta pare ne harte (p.sh. ne geojson.io)
  4. Printon nje permbledhje ne ekran.

Si ekzekutohet:
  python scripts/01_shkarko_linjat.py

Nuk ka nevoje per librari shtese, perdor vetem Python-in standard.
"""

import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

# Drejtkendeshi qe mbulon Tiranen: (lat_jug, lon_perendim, lat_veri, lon_lindje)
TIRANA_BBOX = (41.25, 19.70, 41.40, 19.92)

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# Sa here i provojme te gjithe serverat para se te heqim dore,
# dhe sa sekonda presim mes raundeve (serverat e mbingarkuar cliren pas pak).
RAUNDE = 3
PRITJA_SEKONDA = 20

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def nderto_query(bbox):
    """Pyetja ne gjuhen Overpass QL.

    - rel["route"="bus"](bbox)  -> te gjitha relacionet qe jane linja autobusi
    - way(r.linjat)             -> rruget (segmentet) qe perbejne cdo linje
    - node(r.linjat)            -> pikat (stacionet) qe i perkasin linjave
    - "out geom" na jep koordinatat e rrugeve direkt.
    """
    s, w, n, e = bbox
    return f"""
[out:json][timeout:120];
rel["route"="bus"]({s},{w},{n},{e})->.linjat;
.linjat out body;
way(r.linjat);
out geom;
node(r.linjat);
out body;
"""


def shkarko(query):
    data = urllib.parse.urlencode({"data": query}).encode("utf-8")
    gabimi_fundit = None
    for raundi in range(1, RAUNDE + 1):
        print(f"--- Raundi {raundi} nga {RAUNDE} ---")
        for url in OVERPASS_SERVERS:
            try:
                print(f"Po lidhem me {url} ...")
                req = urllib.request.Request(url, data=data, headers={"User-Agent": "tirana-transit-student-project"})
                with urllib.request.urlopen(req, timeout=180) as resp:
                    pergjigja = json.loads(resp.read().decode("utf-8"))
                print("  U shkarkua me sukses!")
                return pergjigja
            except Exception as e:  # provojme serverin tjeter
                print(f"  Nuk funksionoi: {e}")
                gabimi_fundit = e
        if raundi < RAUNDE:
            print(f"Te gjithe serverat jane te zene. Po pres {PRITJA_SEKONDA} sekonda dhe riprovoj...")
            time.sleep(PRITJA_SEKONDA)
    raise SystemExit(
        f"Asnje server nuk u pergjigj. Gabimi i fundit: {gabimi_fundit}\n"
        "Provo perseri pas disa minutash."
    )


def distanca_m(lat1, lon1, lat2, lon2):
    """Distanca ne metra mes dy pikave (formula Haversine)."""
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def perpuno(raw):
    elementet = raw.get("elements", [])
    nyjet = {el["id"]: el for el in elementet if el["type"] == "node"}
    rruget = {el["id"]: el for el in elementet if el["type"] == "way"}
    relacionet = [el for el in elementet if el["type"] == "relation"]

    linjat = []
    for rel in relacionet:
        tags = rel.get("tags", {})
        stacionet = []
        segmentet = []
        for m in rel.get("members", []):
            roli = m.get("role", "")
            if m["type"] == "node" and m["ref"] in nyjet and roli.startswith(("stop", "platform")):
                nd = nyjet[m["ref"]]
                emri = nd.get("tags", {}).get("name", "(pa emer)")
                # shmangim dublikatet (stop + platform me te njejtin emer njeri pas tjetrit)
                if stacionet and stacionet[-1]["emri"] == emri:
                    continue
                stacionet.append({"id": nd["id"], "emri": emri, "lat": nd["lat"], "lon": nd["lon"]})
            elif m["type"] == "way" and m["ref"] in rruget and roli in ("", "forward", "backward"):
                geom = rruget[m["ref"]].get("geometry", [])
                if geom:
                    segmentet.append([[p["lon"], p["lat"]] for p in geom])

        gjatesia = sum(
            distanca_m(a[1], a[0], b[1], b[0]) for seg in segmentet for a, b in zip(seg, seg[1:])
        )
        linjat.append({
            "osm_id": rel["id"],
            "ref": tags.get("ref", ""),
            "emri": tags.get("name", "(pa emer)"),
            "nga": tags.get("from", ""),
            "per": tags.get("to", ""),
            "operatori": tags.get("operator", ""),
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
            features.append({
                "type": "Feature",
                "properties": {**props, "lloji": "linje"},
                "geometry": {"type": "MultiLineString", "coordinates": l["segmentet"]},
            })
        for s in l["stacionet"]:
            features.append({
                "type": "Feature",
                "properties": {"lloji": "stacion", "emri": s["emri"], "linja": l["ref"] or l["emri"]},
                "geometry": {"type": "Point", "coordinates": [s["lon"], s["lat"]]},
            })
    return {"type": "FeatureCollection", "features": features}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    if "--offline" in sys.argv:  # perdor skedarin e shkarkuar me pare
        with open(os.path.join(DATA_DIR, "osm_raw.json"), encoding="utf-8") as f:
            raw = json.load(f)
    else:
        raw = shkarko(nderto_query(TIRANA_BBOX))
        with open(os.path.join(DATA_DIR, "osm_raw.json"), "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False)

    linjat = perpuno(raw)

    with open(os.path.join(DATA_DIR, "linjat.json"), "w", encoding="utf-8") as f:
        json.dump(linjat, f, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA_DIR, "linjat.geojson"), "w", encoding="utf-8") as f:
        json.dump(ne_geojson(linjat), f, ensure_ascii=False)

    # Permbledhja
    print()
    print(f"U gjenden {len(linjat)} linja (cdo drejtim llogaritet vecmas).")
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
    print("Skedaret u ruajten ne dosjen data/:")
    print("  osm_raw.json, linjat.json, linjat.geojson")
    print("Hap linjat.geojson ne https://geojson.io per t'i pare ne harte.")


if __name__ == "__main__":
    main()
