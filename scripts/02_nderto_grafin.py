"""
HAPI 3a: Ndertimi i grafit te rrjetit te autobuseve
====================================================

Cfare eshte nje graf:
  Nje graf perbehet nga NYJE (pika) dhe BRINJE (lidhje mes pikave), ku cdo brinje
  ka nje "kosto". Ne rastin tone:
    - NYJET   = stacionet e autobusit
    - BRINJET = menyrat per te kaluar nga nje stacion te tjetri, me koston ne sekonda:
        1. me autobus:  nga nje stacion te stacioni i radhes i se njejtes linje
        2. ne kembe:    mes dy stacioneve qe jane afer njeri-tjetrit (p.sh. dy anet e rruges)

  Kur kemi grafin, gjetja e rruges me te shpejte nga A te B behet nje problem klasik:
  "rruga me e shkurter ne graf", qe e zgjidh algoritmi Dijkstra (hapi 3b).

Cfare ben ky skript:
  1. Lexon data/linjat.json (nga hapi 1).
  2. Rendit stacionet sipas pozicionit te tyre pergjate gjurmes se linjes
     (ne OpenStreetMap ato shpesh nuk jane ne radhe).
  3. Pastron stacionet e dyfishta (pika pa emer prane nje stacioni me emer).
  4. Per cdo linje llogarit kohen e udhetimit mes stacioneve te njepasnjeshme,
     nga distanca reale ne rruge.
  5. Gjen te gjitha ciftet e stacioneve qe jane brenda 400 m dhe shton brinje ecjeje.
  6. Ruan gjithcka ne data/grafi.json, qe do ta lexoje faqja web.

Si ekzekutohet:
  python scripts/02_nderto_grafin.py
"""

import json
import math
import os
import sys
import unicodedata

KETU = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(KETU, "..", "data"))

# ---- Supozimet e modelit (mund t'i ndryshosh dhe te shohesh si ndryshojne rezultatet) ----
SHPEJTESIA_AUTOBUSIT_KMH = 15    # shpejtesia mesatare ne qytet, perfshire ndalesat dhe trafikun
SHPEJTESIA_ECJES_KMH = 4.8       # shpejtesia normale e ecjes
FAKTORI_RRUGES_ECJE = 1.3        # ecja nuk eshte vije e drejte: rruget kthehen, prandaj +30%
DISTANCA_MAKS_ECJE_M = 400       # deri ku pranojme te ecim per te nderruar stacion

# ---- Frekuencat (sa minuta kalojne mes dy autobuseve te se njejtes linje) ----
# Rradha e perparesise:
#   1. FREKUENCAT_MANUALE: vlerat qe vendos ti nga njohurite e tua (kane perparesi mbi te gjitha)
#   2. etiketa "interval" ne OpenStreetMap (e kane vetem disa linja)
#   3. INTERVALI_PARAZGJEDHUR per linjat qe s'kane asnje informacion
# Ndrysho vlerat poshte sipas asaj qe di per linjat e Tiranes dhe riekzekuto skriptin.
FREKUENCAT_MANUALE = {
    "L4": 30,          # Vore: vjen shume me rralle se linjat urbane
    "L18/1": 30,       # Arbane: linje periferike
}
INTERVALI_PARAZGJEDHUR = 15


def distanca_m(lat1, lon1, lat2, lon2):
    """Distanca ne metra mes dy pikave mbi siperfaqen e Tokes (formula Haversine)."""
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Renditja e stacioneve pergjate gjurmes
# ---------------------------------------------------------------------------
def ne_metra(lon, lat, lat0):
    """Kthen [lon, lat] ne koordinata x, y ne metra (projeksion i thjeshte lokal).
    Per nje qytet te vogel si Tirana, gabimi eshte i paperfillshem."""
    return (lon * 111320 * math.cos(math.radians(lat0)), lat * 110540)


def bashko_segmentet(segmentet, fillimi=None):
    """Bashkon segmentet e rrugeve ne nje gjurme te vetme.

    Problemi: ne OpenStreetMap segmentet e nje linje jane zakonisht ne radhe, por
    jo gjithmone. Ndonjehere jane te perziera ne copa, p.sh. A, C, B ne vend te A, B, C.
    Gjithashtu cdo segment mund te jete i vizatuar ne drejtimin e kundert.

    Zgjidhja ne dy hapa:
      1. Ndajme segmentet ne COPA te vazhdueshme (aty ku fundi i njerit takon fillimin e tjetrit).
      2. Ndertojme zinxhirin: fillojme nga copa me afer stacionit te pare (fillimi),
         dhe gjithmone shtojme copen qe ka nje skaj me afer fundit te zinxhirit.
    """
    if not segmentet:
        return []

    def d(a, b):
        return math.hypot((a[0] - b[0]) * 83600, (a[1] - b[1]) * 111320)

    LIDHUR_M = 30   # dy segmente konsiderohen te lidhur nese skajet jane brenda 30 m

    # ---- Hapi 1: copat e vazhdueshme ----
    copat = []
    copa = list(segmentet[0])
    for i, seg in enumerate(segmentet[1:], start=1):
        seg = list(seg)
        # ne fillim te nje cope te re, ndoshta segmenti i pare duhet kthyer
        if len(copa) == len(segmentet[i - 1]) and min(d(copa[0], seg[0]), d(copa[0], seg[-1])) < \
                min(d(copa[-1], seg[0]), d(copa[-1], seg[-1])):
            copa = copa[::-1]
        if d(copa[-1], seg[0]) < LIDHUR_M:
            copa.extend(seg)
        elif d(copa[-1], seg[-1]) < LIDHUR_M:
            copa.extend(seg[::-1])
        else:                       # boshllek: mbyllim copen dhe nisim te re
            copat.append(copa)
            copa = seg
    copat.append(copa)

    # ---- Hapi 2: zinxhiri ----
    if fillimi is None:
        fillimi = copat[0][0]
    # copa e pare: ajo me nje skaj me afer stacionit te pare
    i_par = min(range(len(copat)), key=lambda i: min(d(copat[i][0], fillimi), d(copat[i][-1], fillimi)))
    c = copat.pop(i_par)
    gjurma = c if d(c[0], fillimi) <= d(c[-1], fillimi) else c[::-1]
    while copat:
        fundi = gjurma[-1]
        i_tj = min(range(len(copat)), key=lambda i: min(d(copat[i][0], fundi), d(copat[i][-1], fundi)))
        c = copat.pop(i_tj)
        gjurma = gjurma + (c if d(c[0], fundi) <= d(c[-1], fundi) else c[::-1])
    return gjurma


def rendit_stacionet(stops, segmentet):
    """Rendit stacionet sipas distances se tyre pergjate gjurmes se linjes.

    Per cdo stacion gjejme pikën me te afert ne gjurme (projeksion mbi segmentin
    me te afert) dhe sa metra larg fillimit ndodhet ajo pike. Pastaj renditim.
    Kthen listen e renditur, ku cdo stacion ka edhe fushen 'km_ne_linje'.
    """
    fillimi = [stops[0]["lon"], stops[0]["lat"]] if stops else None
    gjurma = bashko_segmentet(segmentet, fillimi)
    if len(gjurma) < 2:
        return [dict(s, km_ne_linje=None) for s in stops], None, None

    lat0 = gjurma[0][1]
    pikat = [ne_metra(lon, lat, lat0) for lon, lat in gjurma]
    # distanca kumulative nga fillimi deri te cdo pike e gjurmes
    kum = [0.0]
    for p, q in zip(pikat, pikat[1:]):
        kum.append(kum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))

    rezultati = []
    for s in stops:
        x, y = ne_metra(s["lon"], s["lat"], lat0)
        me_e_mira = (float("inf"), 0.0)   # (distanca nga gjurma, pozicioni ne gjurme)
        for k in range(len(pikat) - 1):
            (x1, y1), (x2, y2) = pikat[k], pikat[k + 1]
            dx, dy = x2 - x1, y2 - y1
            gjat2 = dx * dx + dy * dy
            # t = sa larg pergjate segmentit bie projeksioni (0 = fillim, 1 = fund)
            t = 0.0 if gjat2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / gjat2))
            px, py = x1 + t * dx, y1 + t * dy
            larg = math.hypot(x - px, y - py)
            if larg < me_e_mira[0]:
                me_e_mira = (larg, kum[k] + t * math.sqrt(gjat2))
        rezultati.append(dict(s, km_ne_linje=me_e_mira[1] / 1000))

    rezultati.sort(key=lambda s: s["km_ne_linje"])
    return rezultati, gjurma, kum


def copa_e_gjurmes(gjurma, kum, m1, m2):
    """Pikat e gjurmes nga pozicioni m1 deri te m2 (ne metra nga fillimi), me skajet e interpoluara."""
    def pika_ne(m):
        for k in range(len(kum) - 1):
            if kum[k + 1] >= m:
                t = 0 if kum[k + 1] == kum[k] else (m - kum[k]) / (kum[k + 1] - kum[k])
                (x1, y1), (x2, y2) = gjurma[k], gjurma[k + 1]
                return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]
        return list(gjurma[-1])
    mes = [list(p) for p, km in zip(gjurma, kum) if m1 < km < m2]
    return [pika_ne(m1)] + mes + [pika_ne(m2)]


def pastro_vijen(koord):
    """Rrumbullakos koordinatat (5 shifra = ~1 m) dhe heq pikat e njepasnjeshme te njejta."""
    dal = []
    for lon, lat in koord:
        p = [round(lon, 5), round(lat, 5)]
        if not dal or dal[-1] != p:
            dal.append(p)
    return dal


def pastro_stacionet(lista):
    """Heq pikat pa emer qe kane nje stacion me emer ngjitur, brenda 80 m.

    Ne OpenStreetMap nje stacion shpesh shenohet dy here: pika ne rruge ku ndalon
    autobusi (pa emer) dhe pika ne trotuar ku pret pasagjeri (me emer).
    """
    rezultati = []
    for i, s in enumerate(lista):
        if s["emri"] == "(pa emer)":
            fqinjet = [lista[j] for j in (i - 1, i + 1) if 0 <= j < len(lista)]
            if any(f["emri"] != "(pa emer)" and
                   distanca_m(s["lat"], s["lon"], f["lat"], f["lon"]) < 80 for f in fqinjet):
                continue
        # i njejti stacion dy here radhazi (p.sh. pika ne rruge + ne trotuar me te njejtin emer)
        if rezultati and rezultati[-1]["emri"] == s["emri"] and \
                distanca_m(s["lat"], s["lon"], rezultati[-1]["lat"], rezultati[-1]["lon"]) < 80:
            continue
        rezultati.append(s)
    return rezultati


def ref_e_linjes(l):
    """Disa linja nuk kane kod; e nxjerrim nga emri, p.sh. 'Bus Q: ...' -> 'Q'."""
    if l["ref"]:
        return l["ref"]
    emri = l["emri"]
    if emri.startswith("Bus ") and ":" in emri:
        return emri[4:emri.index(":")].strip()
    return emri


def kontrollo_cilesine(l, stops_renditur):
    """Kthen nje liste me problemet e gjetura per linjen (bosh = linja eshte ne rregull).

    Te dhenat e OpenStreetMap jane te shkruara nga vullnetare dhe ndonjehere jane te gabuara.
    Nje planifikues udhetimesh qe sugjeron nje autobus ne drejtimin e gabuar eshte me keq
    se nje qe thote "nuk di". Prandaj linjat e dyshimta i perjashtojme nga grafi.
    """
    problemet = []
    stops = l["stacionet"]
    if len(stops) < 2:
        return ["ka me pak se 2 stacione"]

    # 1. Gjurma e rruges duhet te mbuloje te pakten distancen mes stacioneve me te larguar.
    #    Nese gjurma eshte shume me e shkurter, mungon pjesa me e madhe e rruges.
    hapesira = max(distanca_m(a["lat"], a["lon"], b["lat"], b["lon"]) for a in stops for b in stops)
    if l["gjatesia_km"] * 1000 < 0.9 * hapesira:
        problemet.append(f"gjurma e rruges eshte e paplote ({l['gjatesia_km']} km per nje hapesire "
                         f"prej {hapesira / 1000:.1f} km)")

    # 2. Nese shume stacione perseriten, ka shume mundesi qe te dy drejtimet jane perzier ne nje.
    #    (Linjat rrethore perserisin normalisht 2-3 stacione, prandaj kufiri eshte 25%.)
    emrat = [x["emri"] for x in stops if x["emri"] != "(pa emer)"]
    te_perseritur = {e for e in emrat if emrat.count(e) > 1}
    if emrat and len(te_perseritur) > 0.25 * len(set(emrat)):
        problemet.append(f"{len(te_perseritur)} stacione perseriten: duket se te dy drejtimet jane perzier")

    # 3. Pas renditjes, rruga stacion-pas-stacioni (ne vije te drejte) s'mund te jete me e gjate
    #    se gjurma reale. Nese eshte, renditja ka dale gabim (autobusi "kercen" para-mbrapa).
    zinxhiri = sum(distanca_m(a["lat"], a["lon"], b["lat"], b["lon"])
                   for a, b in zip(stops_renditur, stops_renditur[1:]))
    if zinxhiri > 1.3 * l["gjatesia_km"] * 1000 + 500:
        problemet.append(f"renditja e stacioneve s'perputhet me gjurmen ({zinxhiri / 1000:.1f} km "
                         f"stacion-pas-stacioni kunder {l['gjatesia_km']} km gjurme)")
    return problemet


def lexo_intervalin(teksti):
    """Kthen intervalin ne minuta nga etiketa e OSM: "15" -> 15, "00:10:00" -> 10."""
    teksti = (teksti or "").strip()
    if not teksti:
        return None
    try:
        if ":" in teksti:
            pjeset = [int(x) for x in teksti.split(":")]
            ore, minuta = pjeset[0], pjeset[1]
            return ore * 60 + minuta
        return int(float(teksti))
    except ValueError:
        return None


def normalizo(emri):
    """Emri pa shkronja te medha dhe pa diakritike, qe "Katëshet" == "kateshet"."""
    pa_diakritike = unicodedata.normalize("NFKD", emri).encode("ascii", "ignore").decode()
    return " ".join(pa_diakritike.lower().split())


def lexo_linjat_manuale(linjat_raw, rrjeti=None):
    """Lexon data/linjat_manuale.json dhe gjen per cdo emer stacioni pikën ne OSM.

    Kthen (lista e linjave, lista e paralajmerimeve). Cdo linje ka "stacionet" si objekte
    me id/emri/lat/lon, njesoj si linjat nga OSM.
    """
    skedari = os.path.join(DATA_DIR, "linjat_manuale.json")
    if not os.path.exists(skedari):
        return [], []
    with open(skedari, encoding="utf-8") as f:
        te_dhenat = json.load(f)

    # Te gjitha stacionet me emer nga te gjitha linjat e OSM (edhe ato te perjashtuara)
    sipas_emrit = {}
    for l in linjat_raw:
        for st in l["stacionet"]:
            if st["emri"] != "(pa emer)":
                sipas_emrit.setdefault(normalizo(st["emri"]), {})[st["id"]] = st

    linjat, paralajmerime = [], []
    for ml in te_dhenat.get("linjat", []):
        stops, i_meparshmi = [], None
        for emri in ml["stacionet"]:
            kandidatet = list(sipas_emrit.get(normalizo(emri), {}).values())
            if not kandidatet:
                paralajmerime.append(f"{ml['emri']}: nuk u gjet stacioni \"{emri}\"")
                continue
            if i_meparshmi and len(kandidatet) > 1:
                # Dy anet e rruges: marrim ate qe ka RRUGEN me te shkurter nga stacioni i meparshem.
                # (Ne vije te drejte te dy jane njesoj afer, por vetem njera eshte ne drejtimin e autobusit.)
                def kosto(c):
                    if rrjeti:
                        r = rrjeti.rruga((i_meparshmi["lat"], i_meparshmi["lon"]), (c["lat"], c["lon"]), maks_faktor=20)
                        if r:
                            return r[1]
                    return distanca_m(c["lat"], c["lon"], i_meparshmi["lat"], i_meparshmi["lon"]) * 3
                kandidatet.sort(key=kosto)
            i_meparshmi = kandidatet[0]
            stops.append(i_meparshmi)
        linjat.append({**ml, "stacionet": stops})
    return linjat, paralajmerime


def main():
    with open(os.path.join(DATA_DIR, "linjat.json"), encoding="utf-8") as f:
        linjat_raw = json.load(f)

    # Rrjeti rrugor (per te vizatuar linjat pergjate rrugeve). Nese mungon, vijat dalin te drejta.
    pbf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DATA_DIR, "albania-latest.osm.pbf")
    rrjeti = None
    try:
        from rrjeti_rrugor import RrjetiRrugor
        print("Po ndertoj rrjetin rrugor te Tiranes (rreth 10-20 sekonda)...")
        rrjeti = RrjetiRrugor(pbf)
        print(f"  {len(rrjeti):,} nyje rrugesh.")
    except Exception as e:
        print(f"  Rrjeti rrugor nuk u ngarkua ({e}). Segmentet pa gjurme do vizatohen ne vije te drejte.")
    statistika = {"gjurma": 0, "rrjeti": 0, "drejt": 0}

    def gjurma_e_segmentit(a, b, gjurma=None, kum=None):
        """Kthen (koordinatat, metra) per segmentin a -> b, nga burimi me i mire qe kemi."""
        drejt = distanca_m(a["lat"], a["lon"], b["lat"], b["lon"])
        # 1. Copa e gjurmes se linjes (nese pozicionet kane kuptim)
        if gjurma and a.get("km_ne_linje") is not None and b.get("km_ne_linje") is not None:
            m1, m2 = a["km_ne_linje"] * 1000, b["km_ne_linje"] * 1000
            if m2 > m1 and (m2 - m1) <= 2.5 * drejt + 200:
                statistika["gjurma"] += 1
                return pastro_vijen(copa_e_gjurmes(gjurma, kum, m1, m2)), max(m2 - m1, drejt)
        # 2. Rruga me e shkurter ne rrjetin rrugor
        if rrjeti:
            r = rrjeti.rruga((a["lat"], a["lon"]), (b["lat"], b["lon"]))
            if r:
                statistika["rrjeti"] += 1
                return pastro_vijen(r[0]), max(r[1], drejt)
        # 3. Vije e drejte
        statistika["drejt"] += 1
        return [[round(a["lon"], 5), round(a["lat"], 5)], [round(b["lon"], 5), round(b["lat"], 5)]], drejt * 1.25

    # ------------------------------------------------------------------
    # 1. Nyjet: stacionet unike. Cdo stacion merr nje numer (indeks) 0, 1, 2, ...
    #    sepse eshte me e shpejte te punosh me numra se me ID te gjata te OSM.
    # ------------------------------------------------------------------
    stacionet = []          # lista e stacioneve
    indeksi_i = {}          # osm_id -> indeksi ne liste

    def shto_stacion(s):
        if s["id"] not in indeksi_i:
            indeksi_i[s["id"]] = len(stacionet)
            stacionet.append({"emri": s["emri"], "lat": round(s["lat"], 6), "lon": round(s["lon"], 6)})
        return indeksi_i[s["id"]]

    # ------------------------------------------------------------------
    # 2. Brinjet me autobus: per cdo linje, kohet mes stacioneve te njepasnjeshme
    # ------------------------------------------------------------------
    # Intervali nga OSM per cdo kod linje (nese njeri drejtim e ka, vlen per te dy)
    intervalet_osm = {}
    for l in linjat_raw:
        v = lexo_intervalin(l.get("intervali"))
        if v:
            intervalet_osm[ref_e_linjes(l)] = v

    linjat = []
    perjashtuara = []
    for l in linjat_raw:
        if not l["stacionet"]:
            continue  # linjat pa stacione (p.sh. ato periferike) nuk mund te perdoren per rruge
        stops, gjurma, kum = rendit_stacionet(l["stacionet"], l["segmentet"])
        stops = pastro_stacionet(stops)
        problemet = kontrollo_cilesine(l, stops)
        if problemet:
            perjashtuara.append((l["emri"], problemet))
            continue

        shpejtesia_ms = SHPEJTESIA_AUTOBUSIT_KMH / 3.6
        kohet, gjurmet = [], []
        for a, b in zip(stops, stops[1:]):
            # distanca reale ne rruge: nga gjurma e linjes, ose nga rrjeti rrugor
            koord, rruge = gjurma_e_segmentit(a, b, gjurma, kum)
            kohet.append(round(rruge / shpejtesia_ms))
            gjurmet.append(koord)

        ref = ref_e_linjes(l)
        if ref in FREKUENCAT_MANUALE:
            intervali, burimi = FREKUENCAT_MANUALE[ref], "manual"
        elif ref in intervalet_osm:
            intervali, burimi = intervalet_osm[ref], "osm"
        else:
            intervali, burimi = INTERVALI_PARAZGJEDHUR, "vleresim"

        linjat.append({
            "ref": ref,
            "emri": l["emri"],
            "ngjyra": l.get("ngjyra", ""),
            "intervali_min": intervali,
            "burimi_intervalit": burimi,
            "stacionet": [shto_stacion(s) for s in stops],
            "kohet": kohet,   # kohet[k] = sekonda nga stacioni k te stacioni k+1
            "gjurmet": gjurmet,   # gjurmet[k] = vija ne rruge nga stacioni k te stacioni k+1
        })

    # ------------------------------------------------------------------
    # 2b. Linjat manuale (data/linjat_manuale.json): te shkruara nga njohesit e qytetit
    # ------------------------------------------------------------------
    manuale, paralajmerime_manuale = lexo_linjat_manuale(linjat_raw, rrjeti)
    for ml in manuale:
        # Nese zevendeson nje linje te OSM, e heqim nga lista e te perjashtuarave dhe nga grafi
        if ml.get("zevendeson"):
            perjashtuara = [p for p in perjashtuara if p[0] != ml["zevendeson"]]
            linjat = [l for l in linjat if l["emri"] != ml["zevendeson"]]
        stops = ml["stacionet"]
        if len(stops) < 2:
            continue
        # Pa gjurme nga OSM: rruga dhe distanca nga rrjeti rrugor
        shpejtesia_ms = SHPEJTESIA_AUTOBUSIT_KMH / 3.6
        kohet, gjurmet = [], []
        for a, b in zip(stops, stops[1:]):
            koord, rruge = gjurma_e_segmentit(a, b)
            kohet.append(round(rruge / shpejtesia_ms))
            gjurmet.append(koord)
        linjat.append({
            "ref": ml["ref"], "emri": ml["emri"], "ngjyra": ml.get("ngjyra", ""),
            "intervali_min": ml.get("intervali_min", INTERVALI_PARAZGJEDHUR),
            "burimi_intervalit": "manual",
            "manuale": True,
            "zevendeson": ml.get("zevendeson", ""),
            "stacionet": [shto_stacion(s) for s in stops],
            "kohet": kohet,
            "gjurmet": gjurmet,
        })

    # ------------------------------------------------------------------
    # 3. Brinjet ne kembe: cdo cift stacionesh brenda DISTANCA_MAKS_ECJE_M
    #    Krahasimi i cdo cifti eshte O(n^2): per ~600 stacione jane ~180 000 krahasime,
    #    qe Python-i i ben per nje sekonde. (Per qytete te medha do perdornim nje
    #    strukture hapesinore si grid ose KD-tree.)
    # ------------------------------------------------------------------
    # Rrjeti i kembesoreve: per distancat reale ne kembe dhe per shfletuesin (data/rruget_kembe.json)
    kembe = None
    try:
        from rrjeti_rrugor import RrjetiRrugor
        print("Po ndertoj rrjetin e kembesoreve (rreth 10-20 sekonda)...")
        kembe = RrjetiRrugor(pbf, profili="kembe", bbox=(41.28, 19.73, 41.40, 19.89))
        nyje, brinje = kembe.eksporto_json(os.path.join(DATA_DIR, "rruget_kembe.json"))
        print(f"  {nyje:,} nyje, {brinje:,} copa rrugesh -> data/rruget_kembe.json")
    except Exception as e:
        print(f"  Rrjeti i kembesoreve nuk u ngarkua ({e}). Ecja do llogaritet ne vije te drejte x {FAKTORI_RRUGES_ECJE}.")

    shpejtesia_ecje_ms = SHPEJTESIA_ECJES_KMH / 3.6
    ecjet = []
    sa_me_rrjet = 0
    n = len(stacionet)
    for i in range(n):
        a = stacionet[i]
        for j in range(i + 1, n):
            b = stacionet[j]
            d = distanca_m(a["lat"], a["lon"], b["lat"], b["lon"])
            if d <= DISTANCA_MAKS_ECJE_M:
                metra = d * FAKTORI_RRUGES_ECJE           # vleresimi nese s'kemi rrjet
                if kembe:
                    r = kembe.rruga((a["lat"], a["lon"]), (b["lat"], b["lon"]), maks_faktor=2.5)
                    if r:
                        metra = max(r[1], d)
                        sa_me_rrjet += 1
                ecjet.append([i, j, round(metra / shpejtesia_ecje_ms)])

    grafi = {
        "parametrat": {
            "shpejtesia_autobusit_kmh": SHPEJTESIA_AUTOBUSIT_KMH,
            "shpejtesia_ecjes_kmh": SHPEJTESIA_ECJES_KMH,
            "faktori_rruges_ecje": FAKTORI_RRUGES_ECJE,
        },
        "stacionet": stacionet,
        "linjat": linjat,
        "ecjet": ecjet,   # [i, j, sekonda], vlen ne te dy drejtimet
    }
    with open(os.path.join(DATA_DIR, "grafi.json"), "w", encoding="utf-8") as f:
        json.dump(grafi, f, ensure_ascii=False, separators=(",", ":"))

    # ------------------------------------------------------------------
    # Permbledhja
    # ------------------------------------------------------------------
    brinje_bus = sum(len(l["kohet"]) for l in linjat)
    print("Grafi u ndertua!")
    print("-" * 50)
    print(f"Nyje (stacione):            {len(stacionet)}")
    print(f"Drejtime linjash:           {len(linjat)}")
    print(f"Brinje me autobus:          {brinje_bus}")
    print(f"Brinje ne kembe (<= {DISTANCA_MAKS_ECJE_M} m):  {len(ecjet)}  ({sa_me_rrjet} me distance reale ne rruge)")
    print("-" * 50)

    # Shembull: koha e plote e disa linjave, per te kontrolluar qe numrat jane te arsyeshem
    print(f"{'Linja':<8}{'Stacione':>9}{'Udhetimi':>10}{'Intervali':>11}  Burimi")
    print("-" * 50)
    pare = set()
    for l in sorted(linjat, key=lambda x: x["ref"]):
        if l["ref"] in pare:
            continue          # nje rresht per linje mjafton (drejtimet jane te ngjashme)
        pare.add(l["ref"])
        min_ = sum(l["kohet"]) / 60
        print(f"{l['ref'][:8]:<8}{len(l['stacionet']):>9}{min_:>7.0f} min{l['intervali_min']:>7} min  {l['burimi_intervalit']}")
    print()
    print(f"Vijat e segmenteve: {statistika['gjurma']} nga gjurma e linjes, {statistika['rrjeti']} nga rrjeti rrugor, "
          f"{statistika['drejt']} ne vije te drejte")
    manuale_ne_graf = [l for l in linjat if l.get("manuale")]
    if manuale_ne_graf:
        print()
        print(f"Linja manuale (nga data/linjat_manuale.json): {len(manuale_ne_graf)}")
        for l in manuale_ne_graf:
            print(f"  + {l['emri']}: {len(l['stacionet'])} stacione, ~{sum(l['kohet']) / 60:.0f} min, "
                  f"cdo {l['intervali_min']} min")
    for pr in paralajmerime_manuale:
        print(f"  KUJDES: {pr}")
    if perjashtuara:
        print()
        print(f"KUJDES: {len(perjashtuara)} linja u perjashtuan per shkak te te dhenave te dyshimta:")
        for emri, problemet in perjashtuara:
            print(f"  - {emri}")
            for pr in problemet:
                print(f"      * {pr}")
        print("  Keto mund t'i rregullosh ne OpenStreetMap (openstreetmap.org) dhe te shkarkosh harten perseri.")
    print()
    print(f"U ruajt: {os.path.join(DATA_DIR, 'grafi.json')}")


if __name__ == "__main__":
    main()
