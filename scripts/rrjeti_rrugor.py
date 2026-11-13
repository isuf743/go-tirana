"""
Rrjeti rrugor i Tiranes: gjen rrugen qe ndjek nje automjet mes dy pikave.
=========================================================================

Perdoret nga 02_nderto_grafin.py per te vizatuar linjat e autobusit pergjate rrugeve
(dhe jo ne vije te drejte nga stacioni ne stacion).

Si funksionon:
  1. Nga harta e Shqiperise (albania-latest.osm.pbf) marrim vetem rruget e makinave
     brenda Tiranes (highway = primary, secondary, residential, ...).
  2. I kthejme ne graf: nyjet = kryqezimet dhe pikat e rruges, brinjet = copat e rruges
     mes tyre, me koston = gjatesine ne metra. Rruget njedrejtimeshe (oneway) marrin
     brinje vetem ne nje drejtim, sepse edhe autobusi s'mund te hyje kunder drejtimit.
  3. Per dy pika, gjejme nyjen me te afert te secila ("snap") dhe kerkojme rrugen
     me te shkurter me algoritmin A* (Dijkstra + nje "udhezues": distanca ne vije te
     drejte deri te objektivi, qe e ben kerkimin te shkoje me shpejt drejt tij).
"""

import heapq
import json
import math

try:
    import osmium
except ImportError:
    osmium = None

# Rruget ku mund te kaloje autobusi
LLOJET_AUTOBUS = {
    "motorway", "motorway_link", "trunk", "trunk_link", "primary", "primary_link",
    "secondary", "secondary_link", "tertiary", "tertiary_link", "unclassified",
    "residential", "living_street", "service", "busway", "road",
}

# Rruget ku mund te ecet ne kembe (pa autostrada; trotuaret, rrugicat, shkallet, sheshet...)
LLOJET_KEMBE = {
    "trunk", "trunk_link", "primary", "primary_link", "secondary", "secondary_link",
    "tertiary", "tertiary_link", "unclassified", "residential", "living_street", "service",
    "road", "footway", "pedestrian", "path", "steps", "track", "cycleway", "corridor",
}

BBOX_TIRANA = (41.25, 19.65, 41.42, 19.95)   # (jug, perendim, veri, lindje), pak me e gjere se qyteti


def _metra(lat1, lon1, lat2, lon2):
    """Distanca e perafert ne metra (mjafton per distanca brenda qytetit)."""
    dy = (lat2 - lat1) * 110540
    dx = (lon2 - lon1) * 111320 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


class _LexoRruget(osmium.SimpleHandler if osmium else object):
    def __init__(self, profili, bbox):
        super().__init__()
        self.profili = profili    # "autobus" ose "kembe"
        self.bbox = bbox
        self.koordinatat = {}     # id e nyjes -> (lat, lon)
        self.brinjet = {}         # id e nyjes -> [(fqinji, metra), ...]

    def way(self, w):
        hw = w.tags.get("highway")
        if self.profili == "kembe":
            if hw not in LLOJET_KEMBE:
                return
            # rruget private ose ku ndalohet ecja
            if w.tags.get("foot") == "no" or (w.tags.get("access") in ("no", "private") and w.tags.get("foot") != "yes"):
                return
        elif hw not in LLOJET_AUTOBUS:
            return
        nyjet = []
        for n in w.nodes:
            if not n.location.valid():
                return
            lat, lon = n.location.lat, n.location.lon
            nyjet.append((n.ref, lat, lon))
        s, wst, n_, e = self.bbox
        if not any(s <= lat <= n_ and wst <= lon <= e for _, lat, lon in nyjet):
            return

        if self.profili == "kembe":
            mbrapsht = para = True   # kembesori ecen ne te dy drejtimet, edhe ne rruget njedrejtimeshe
        else:
            para, mbrapsht = self._drejtimi(w)
        for (a, la, lo), (b, lb, lob) in zip(nyjet, nyjet[1:]):
            self.koordinatat[a] = (la, lo)
            self.koordinatat[b] = (lb, lob)
            d = _metra(la, lo, lb, lob)
            if para:
                self.brinjet.setdefault(a, []).append((b, d))
            if mbrapsht:
                self.brinjet.setdefault(b, []).append((a, d))

    @staticmethod
    def _drejtimi(w):
        # Drejtimi: oneway=yes -> vetem para, oneway=-1 -> vetem mbrapsht.
        # Autostradat dhe rrethrrotullimet jane njedrejtimeshe edhe pa etiketen.
        ow = w.tags.get("oneway", "")
        para = mbrapsht = True
        if ow in ("yes", "true", "1") or w.tags.get("junction") in ("roundabout", "circular") \
                or w.tags.get("highway") == "motorway":
            mbrapsht = False
        elif ow == "-1":
            para = False
        # Autobusi lejohet shpesh kunder drejtimit ne korsi te dedikuara (oneway:bus=no / busway)
        if w.tags.get("oneway:bus") == "no" or w.tags.get("oneway:psv") == "no":
            para = mbrapsht = True
        return para, mbrapsht


class RrjetiRrugor:
    def __init__(self, skedari_pbf, profili="autobus", bbox=BBOX_TIRANA):
        if osmium is None:
            raise RuntimeError("mungon libraria osmium (pip install osmium)")
        self.profili = profili
        h = _LexoRruget(profili, bbox)
        h.apply_file(skedari_pbf, locations=True)
        self.koord = h.koordinatat
        self.brinjet = h.brinjet
        # Rrjete katrore (grid) me qeliza ~200 m, per te gjetur shpejt nyjen me te afert
        self.qeliza = 0.002
        self.rrjeta = {}
        for nid, (lat, lon) in self.koord.items():
            if nid in self.brinjet:   # vetem nyjet nga mund te nisesh
                self.rrjeta.setdefault((int(lat / self.qeliza), int(lon / self.qeliza)), []).append(nid)

    def __len__(self):
        return len(self.koord)

    def nyja_me_e_afert(self, lat, lon, maks_m=150):
        ki, kj = int(lat / self.qeliza), int(lon / self.qeliza)
        me_e_mira, dm = None, maks_m
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for nid in self.rrjeta.get((ki + di, kj + dj), ()):
                    la, lo = self.koord[nid]
                    d = _metra(lat, lon, la, lo)
                    if d < dm:
                        me_e_mira, dm = nid, d
        return me_e_mira

    def rruga(self, a, b, maks_faktor=3.0):
        """Kthen ([[lon, lat], ...], metra) per rrugen nga a=(lat,lon) te b=(lat,lon), ose None.

        maks_faktor: nese rruga e gjetur eshte me shume se 3x vija e drejte, ka shume mundesi
        qe snap-i ka zgjedhur rrugen e gabuar (p.sh. anen tjeter te autostrades); e refuzojme.
        """
        na, nb = self.nyja_me_e_afert(*a), self.nyja_me_e_afert(*b)
        if na is None or nb is None:
            return None
        if na == nb:
            return [[a[1], a[0]], [b[1], b[0]]], _metra(*a, *b)
        lb, lob = self.koord[nb]
        h = lambda n: _metra(*self.koord[n], lb, lob)   # udhezuesi i A*

        g = {na: 0.0}
        prej = {}
        radha = [(h(na), na)]
        vizituar = set()
        while radha:
            _, u = heapq.heappop(radha)
            if u == nb:
                break
            if u in vizituar:
                continue
            vizituar.add(u)
            if len(vizituar) > 60000:      # mbrojtje: mos kerko pafundesisht
                return None
            for v, d in self.brinjet.get(u, ()):
                ng = g[u] + d
                if ng < g.get(v, float("inf")):
                    g[v] = ng
                    prej[v] = u
                    heapq.heappush(radha, (ng + h(v), v))
        if nb not in g:
            return None
        if g[nb] > maks_faktor * _metra(*a, *b) + 300:
            return None

        nyjet = [nb]
        while nyjet[-1] != na:
            nyjet.append(prej[nyjet[-1]])
        nyjet.reverse()
        koord = [[a[1], a[0]]] + [[round(self.koord[n][1], 6), round(self.koord[n][0], 6)] for n in nyjet] + [[b[1], b[0]]]
        return koord, g[nb] + _metra(*a, *self.koord[na]) + _metra(*self.koord[nb], *b)

    def eksporto_json(self, skedari):
        """Ruan rrjetin ne nje JSON kompakt per shfletuesin (js/ecja.js).

        Formati (per te zene sa me pak vend):
          "n": [lon1, lat1, lon2, lat2, ...]  koordinatat x 100000 si numra te plote
          "b": [a1, b1, a2, b2, ...]          brinjet si indekse nyjesh (te dy drejtimet vlejne)
        Gjatesia e brinjes llogaritet ne shfletues nga koordinatat.
        """
        indeksi, n = {}, []
        for nid, (lat, lon) in self.koord.items():
            indeksi[nid] = len(indeksi)
            n.extend((round(lon * 1e5), round(lat * 1e5)))
        b, pare = [], set()
        for a, fqinjet in self.brinjet.items():
            for v, _ in fqinjet:
                cift = (a, v) if a < v else (v, a)
                if cift not in pare:
                    pare.add(cift)
                    b.extend((indeksi[cift[0]], indeksi[cift[1]]))
        with open(skedari, "w", encoding="utf-8") as f:
            json.dump({"n": n, "b": b}, f, separators=(",", ":"))
        return len(indeksi), len(b) // 2
