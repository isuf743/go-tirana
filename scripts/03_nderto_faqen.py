"""
HAPI 5: Ndërtimi i website-it Go Tirana (gjenerues faqesh statike)
==================================================================

Pse statike: faqet e gatshme HTML hapen shumë shpejt, s'kanë nevojë për databazë dhe
motorët e kërkimit (Google) i lexojnë pa problem. E vetmja pjesë dinamike është
formulari i kontaktit (api/contact.php).

Lexon:
  burimi_faqes/konfigurimi.json   emri, adresa e faqes, emaili, GoatCounter
  burimi_faqes/vendet.json        vendet në tre gjuhë
  burimi_faqes/fotot.json         fotot nga Wikimedia Commons (me autorin dhe licencën)
  burimi_faqes/tekstet.py         tekstet e ndërfaqes dhe faqet ligjore
  burimi_faqes/templates/*.html   shabllonet (Jinja2)

Krijon (në dosjen e projektit):
  index.html            zgjedh gjuhën automatikisht
  en/ it/ sq/           faqet për çdo gjuhë
  404.html              faqja "nuk u gjet"
  sitemap.xml, robots.txt, site.webmanifest, .htaccess
  assets/               stili, skriptet, shkronjat, imazhet

Si ekzekutohet:
  pip install jinja2
  python scripts/03_nderto_faqen.py
"""

import json
import math
import os
import shutil
import sys
import urllib.parse
from datetime import date

KETU = os.path.dirname(os.path.abspath(__file__))
PROJEKTI = os.path.normpath(os.path.join(KETU, ".."))
BURIMI = os.path.join(PROJEKTI, "burimi_faqes")
sys.path.insert(0, BURIMI)

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    raise SystemExit("Mungon Jinja2. Instaloje me:  pip install jinja2")

import arti
from tekstet_info import INFO, URGJENCA, BURIMET, KONTROLLUAR
from tekstet_itinerare import ITINERARET, UI as IT_UI, KUFIRI_ECJES
import tekstet_udhetime as UDH
import tekstet_hero as HERO
from tekstet import GJUHET, EMRAT_E_GJUHEVE, LOCALE, KATEGORITE, KATEGORITE_PERSHKRIM, T, PRIVATESIA, KUSHTET

VERSIONI = "31"   # rrit këtë numër kur ndryshon CSS/JS, që shfletuesit të marrin versionin e ri


def lexo_json(emri):
    with open(os.path.join(BURIMI, emri), encoding="utf-8") as f:
        return json.load(f)


def shkruaj(rruga_relative, permbajtja):
    rruga = os.path.join(PROJEKTI, rruga_relative)
    os.makedirs(os.path.dirname(rruga), exist_ok=True)
    with open(rruga, "w", encoding="utf-8", newline="\n") as f:
        f.write(permbajtja)


def metra(a, b):
    dy = (a["lat"] - b["lat"]) * 110540
    dx = (a["lon"] - b["lon"]) * 111320 * math.cos(math.radians(a["lat"]))
    return math.hypot(dx, dy)


def kohezgjatja(t, d):
    a, b = d
    if b < 60:
        return t["dur_min"].format(a=a, b=b)
    if a < 60:
        return t["dur_mixed"].format(a=a, b=f"{b / 60:g}")
    return t["dur_h"].format(a=f"{a / 60:g}", b=f"{b / 60:g}")


def distanca_tekst(m, lang):
    if m < 950:
        return f"{int(round(m / 50.0) * 50)} m"
    km = f"{m / 1000:.1f}"
    return (km if lang == "en" else km.replace(".", ",")) + " km"


def pergatit_itinerar(it, lang, sipas_slug, root):
    """Ndalesat, segmentet mes tyre (ecje ose autobus) dhe shifrat përmbledhëse të një itinerari."""
    ui = IT_UI[lang]
    ndalesat = [{"n": i + 1, "time": koha, "p": sipas_slug[slug], "note": shenim[lang]}
                for i, (koha, slug, shenim) in enumerate(it["stops"])]
    nisja = sipas_slug[it["start"]] if it.get("start") else None

    def segment(a, b):
        m = metra(a, b) * 1.3                       # rrugët nuk janë vijë e drejtë: +30%
        seg = {"m": m, "dist": distanca_tekst(m, lang)}
        if metra(a, b) > KUFIRI_ECJES:
            seg["type"] = "bus"
            seg["text"] = ui["bus"].format(km=distanca_tekst(m, lang).replace(" km", ""))
            seg["href"] = (f"{root}planner/?from={a['lat']},{a['lon']}&fromname={urllib.parse.quote(a['name'])}"
                           f"&to={b['lat']},{b['lon']}&name={urllib.parse.quote(b['name'])}&lang={lang}")
        else:
            seg["type"] = "walk"
            seg["text"] = ui["walk"].format(m=max(2, int(round(m / 80 + 0.5))))
            seg["href"] = ("https://www.google.com/maps/dir/?api=1&travelmode=walking"
                           f"&origin={a['lat']},{a['lon']}&destination={b['lat']},{b['lon']}")
        return seg

    hyrja = segment(nisja, ndalesat[0]["p"]) if nisja else None
    for i, nd in enumerate(ndalesat[:-1]):
        nd["next"] = segment(nd["p"], ndalesat[i + 1]["p"])
    segmentet = ([hyrja] if hyrja else []) + [nd["next"] for nd in ndalesat[:-1]]
    ecja = sum(s["m"] for s in segmentet if s["type"] == "walk")
    autobus = sum(1 for s in segmentet if s["type"] == "bus")
    harta = {"stops": [{"n": nd["n"], "name": nd["p"]["name"], "lat": nd["p"]["lat"], "lon": nd["p"]["lon"]} for nd in ndalesat],
             "start": {"name": nisja["name"], "lat": nisja["lat"], "lon": nisja["lon"]} if nisja else None,
             "legs": [s["type"] for s in segmentet]}
    # E gjithë rruga në Google Maps: nisja, ndalesat e ndërmjetme (maks. 9) dhe ndalesa e fundit
    pikat = ([nisja] if nisja else []) + [nd["p"] for nd in ndalesat]
    gm = (f"https://www.google.com/maps/dir/?api=1&origin={pikat[0]['lat']},{pikat[0]['lon']}"
          f"&destination={pikat[-1]['lat']},{pikat[-1]['lon']}"
          + ("&waypoints=" + urllib.parse.quote("|".join(f"{q['lat']},{q['lon']}" for q in pikat[1:-1][:9])) if len(pikat) > 2 else "")
          + ("&travelmode=walking" if autobus == 0 else ""))
    return {"gmaps_route": gm, "slug": it["slug"], "title": it["title"][lang], "summary": it["summary"][lang], "lead": it["lead"][lang],
            "when": it["when"][lang], "hero": sipas_slug[it["hero"]], "stops": ndalesat, "start": nisja, "intro": hyrja,
            "walk_text": distanca_tekst(ecja, lang), "bus_n": autobus, "n": len(ndalesat),
            "span": f"{ndalesat[0]['time']}–{ndalesat[-1]['time']}",
            "map_json": json.dumps(harta, ensure_ascii=False).replace("</", "<\\/")}


# Fotoja që përfaqëson çdo kategori në faqen kryesore, dhe tri ndalesat e seksionit "Një ditë në Tiranë"
FOTO_KATEGORIE = {"history": "national-historical-museum", "photo": "pyramid", "nature": "mount-dajti",
                  "food": "new-bazaar", "nightlife": "komiteti"}
DITA = ["skanderbeg-square", "dajti-ekspres", "sky-tower"]
# Vendet e zgjedhura në faqen kryesore (sipas brief-it) dhe fotot e seksionit "Rreth Tiranës"
TE_ZGJEDHURA = ["skanderbeg-square", "pyramid", "bunkart-2", "grand-park", "new-bazaar", "mount-dajti"]
FOTO_HISTORIA = ["pyramid", "etem-bey-mosque"]
FOTO_RRETH = "skanderbeg-square"
FOTO_INFO = "clock-tower"


def foto_wikimedia(f):
    """URL-të e miniaturave në madhësitë standarde të Wikimedia (500, 960, 1280 px)."""
    baza = "https://upload.wikimedia.org/wikipedia/commons/thumb/" + f["path"]
    emri = f["name"] + (".png" if f["name"].lower().endswith(".svg") else "")
    return {**f, **{f"src{w}": f"{baza}/{w}px-{emri}" for w in (500, 960, 1280)}}


def slidet_hero(lang):
    """Fotot e slider-it me URL-të e Wikimedia (960/1280/1920 px janë madhësi standarde)."""
    dalja = []
    for f in HERO.SLIDET:
        baza = "https://upload.wikimedia.org/wikipedia/commons/thumb/" + f["path"] + "/"
        dalja.append({**f, "label": f["label"][lang], "src": baza + "1280px-" + f["name"],
                      "srcset": ", ".join(f"{baza}{w}px-{f['name']} {w}w" for w in (960, 1280, 1920))})
    return dalja


def main():
    cfg = lexo_json("konfigurimi.json")
    vendet_raw = lexo_json("vendet.json")
    fotot = lexo_json("fotot.json")
    fotot_lokale = lexo_json("fotot_lokale.json") if os.path.exists(os.path.join(BURIMI, "fotot_lokale.json")) else {}
    site = cfg["site_url"].rstrip("/")

    env = Environment(loader=FileSystemLoader(os.path.join(BURIMI, "templates")),
                      autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

    # ---- Asetet: kopjojmë stilin, skriptet, shkronjat, MapLibre dhe imazhet ----
    shutil.copytree(os.path.join(BURIMI, "assets"), os.path.join(PROJEKTI, "assets"), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(BURIMI, "rrenja")):      # favicon, ikonat e rrënjës
        shutil.copy2(os.path.join(BURIMI, "rrenja", f), os.path.join(PROJEKTI, f))
    shutil.copytree(os.path.join(BURIMI, "api"), os.path.join(PROJEKTI, "api"), dirs_exist_ok=True)
    # Planifikuesi i autobusëve (hapat 1-4) jeton te planner/ dhe lexon ../data dhe ../js
    shutil.copytree(os.path.join(BURIMI, "planner"), os.path.join(PROJEKTI, "planner"), dirs_exist_ok=True)
    # Çelësi i Google Maps për hartën e planifikuesit (nga konfigurimi.json)
    pl = os.path.join(PROJEKTI, "planner", "index.html")
    with open(pl, encoding="utf-8") as f:
        html_pl = f.read()
    with open(pl, "w", encoding="utf-8") as f:
        f.write(html_pl.replace("__GMAPS_KEY__", cfg.get("google_maps_key", "")))
    # Lista zyrtare e linjave nga Bashkia (emrat, operatorët) që lexon planifikuesi
    os.makedirs(os.path.join(PROJEKTI, "data"), exist_ok=True)
    shutil.copy2(os.path.join(BURIMI, "linjat_zyrtare.json"), os.path.join(PROJEKTI, "data", "linjat_zyrtare.json"))
    shkruaj("private/.htaccess", "# Kjo dosje nuk shërbehet kurrë nga Apache (sekrete dhe mesazhe)\nRequire all denied\n")

    logo = arti.logo()
    faqet_sitemap = []   # (rruga_relative_pa_gjuhë, prioriteti)

    def url(lang, rruga):
        return f"{site}/{lang}/{rruga}"

    for lang in GJUHET:
        t = T[lang]
        kategorite = []
        for slug, k in KATEGORITE.items():
            kategorite.append({"slug": slug, "name": k[lang], "color": k["color"], "desc": KATEGORITE_PERSHKRIM[slug][lang],
                               "count": sum(1 for v in vendet_raw if slug in v["cats"])})
        kat_sipas_slug = {k["slug"]: k for k in kategorite}

        # Vendet me tekstet e gjuhës aktuale
        vendet = []
        for v in vendet_raw:
            p = {**v,
                 "name": v["name"][lang], "summary": v["summary"][lang], "about": v["about"][lang],
                 "tips": v["tips"][lang], "hours": (v.get("hours") or {}).get(lang),
                 "duration_text": kohezgjatja(t, v["duration"]),
                 "cat_objs": [kat_sipas_slug[c] for c in v["cats"]]}
            p["alt"] = f'{p["name"]}, Tirana'
            p["img"] = foto_wikimedia(fotot[v["slug"]]) if v["slug"] in fotot else None
            if v["slug"] in fotot_lokale:   # fotot e tua (scripts/04_pergatit_fotot.py) kanë përparësi
                baza = f'{cfg["base_path"]}assets/img/vendet/{v["slug"]}/'
                p["gallery"] = [{"src500": f'{baza}{f["n"]}-500.webp', "full": f'{baza}{f["n"]}-full.webp',
                                 "w": f["w"], "h": f["h"], "ratio": f["h"] / f["w"]} for f in fotot_lokale[v["slug"]]]
                g0 = p["gallery"][0]
                p["img"] = {"local": True, "src500": g0["src500"], "full": g0["full"], "w": g0["w"], "ratio": g0["ratio"],
                            "src1280": f'{site}/assets/img/vendet/{v["slug"]}/1-full.webp'}   # URL e plotë për Google/OG
            if not p["img"]:
                p["placeholder"] = arti.nate(v["slug"], kat_sipas_slug[v["cats"][0]]["color"])
            if v.get("website"):
                p["website_label"] = urllib.parse.urlparse(v["website"]).netloc.replace("www.", "")
            vendet.append(p)

        def render(shabllon, rruga, faqja, thellesia, **kw):
            root = "../" * thellesia
            faqja.setdefault("og_image", f"{site}/assets/img/og-default.png")
            faqja["path"] = rruga
            faqja["url"] = url(lang, rruga)
            faqja["alternates"] = {l: url(l, rruga) for l in GJUHET}
            html = env.get_template(shabllon).render(
                lang=lang, t=t, cfg=cfg, page=faqja, root=root, langs=GJUHET, lang_names=EMRAT_E_GJUHEVE,
                locale=LOCALE[lang], cat_list=kategorite, brand_mark=logo, v=VERSIONI, year=date.today().year, **kw)
            shkruaj(f"{lang}/{rruga}index.html", html)

        emri = cfg["site_name"]
        sipas_slug = {p["slug"]: p for p in vendet}
        # ---- Të dhënat e hartës (faqja kryesore dhe Eksploro) ----
        def miniatura(p):
            if not p["img"]:
                return None
            return p["img"]["src500"]

        def te_dhenat_harte(lista):
            return json.dumps([{"slug": p["slug"], "name": p["name"], "lat": p["lat"], "lon": p["lon"],
                                "color": p["cat_objs"][0]["color"], "cat": p["cat_objs"][0]["name"],
                                "cats": p["cats"], "area": p["area"], "img": miniatura(p)} for p in lista],
                              ensure_ascii=False).replace("</", "<\\/")

        def json_attr(d):
            return json.dumps(d, ensure_ascii=False).replace("'", "&#39;")

        # ---- Itineraret (përgatiten këtu se dalin edhe në faqen kryesore) ----
        itineraret = {d: [pergatit_itinerar(it, lang, sipas_slug, "../" * d) for it in ITINERARET] for d in (1, 2, 3)}

        # ---- Faqja kryesore ----
        sipas_kat = {k["slug"]: [p for p in vendet if p["cats"][0] == k["slug"]] for k in kategorite}
        render("home.html", "", {
            "title": t["site_title_home"], "desc": t["site_desc"],
            "jsonld": json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": emri,
                                  "url": url(lang, ""), "inLanguage": lang, "description": t["site_desc"]}, ensure_ascii=False),
        }, 1, featured=[sipas_slug[s] for s in TE_ZGJEDHURA if s in sipas_slug],
           cat_img={k: sipas_slug[s]["img"] for k, s in FOTO_KATEGORIE.items() if sipas_slug.get(s, {}).get("img")},
           places=vendet, places_json=te_dhenat_harte(vendet), places_by_cat=sipas_kat,
           story_imgs=[sipas_slug[s] for s in FOTO_HISTORIA], credit_list=vendet, itins=itineraret[1], it_ui=IT_UI[lang],
           hero_slides=slidet_hero(lang), hero_ui=HERO.UI[lang],
           wx_msgs=json.dumps({**HERO.MOTI[lang], "links": {k: "../" + lang + "/" + v for k, v in HERO.LIDHJET_MOTI.items()}}, ensure_ascii=False),
           bus_msgs=json_attr({k: t[k] for k in ("locating", "loc_denied", "loc_outside", "loc_unavailable",
                                                 "form_err_to", "form_err_same", "my_location")}),
           nl_msgs=json_attr({k: t[k] for k in ("nl_ok", "nl_sending", "nl_err_email", "nl_err_consent",
                                                "nl_err_server", "nl_err_rate")}))
        faqet_sitemap.append(("", "1.0"))

        # ---- Eksploro (të gjitha + një faqe për çdo kategori) ----
        render("explore.html", "explore/", {"title": f"{t['nav_explore']}: {t['explore_title']} | {emri}",
                                            "desc": t["explore_lead"].format(n=len(vendet))},
               2, active="explore", heading=t["explore_title"], lead=t["explore_lead"].format(n=len(vendet)),
               places=vendet, current=None, places_json=te_dhenat_harte(vendet))
        faqet_sitemap.append(("explore/", "0.9"))
        for k in kategorite:
            lista = [p for p in vendet if k["slug"] in p["cats"]]
            foto = sipas_slug.get(FOTO_KATEGORIE.get(k["slug"], ""), {}).get("img")
            render("explore.html", f"explore/{k['slug']}/",
                   {"title": f"{k['name']} | {emri}", "desc": k["desc"],
                    "og_image": foto["src1280"] if foto else None},
                   3, active="explore", heading=k["name"], lead=k["desc"], hero_img=foto, current_color=k["color"],
                   places=lista, current=k["slug"], places_json=te_dhenat_harte(lista))
            faqet_sitemap.append((f"explore/{k['slug']}/", "0.8"))

        # ---- Destinacionet: të gjitha vendet sipas kategorisë kryesore ----
        render("destinations.html", "destinations/", {"title": f"{t['dest_title']} | {emri}",
                                                      "desc": t["dest_lead"].format(n=len(vendet))},
               2, active="destinations", total=len(vendet), all_places=vendet,
               groups=[{"cat": k, "places": sipas_kat[k["slug"]]} for k in kategorite if sipas_kat[k["slug"]]])
        faqet_sitemap.append(("destinations/", "0.8"))

        # ---- Rreth Tiranës ----
        vendet_kapitujt = {slug: sipas_slug[slug] for _, slug, _, _ in t["about_sections"]}
        render("about.html", "about/", {"title": f"{t['about_page_title']} | {emri}", "desc": t["about_page_lead"],
                                        "og_image": sipas_slug[FOTO_RRETH]["img"]["src1280"]},
               2, active="about", hero_place=sipas_slug[FOTO_RRETH], sections_places=vendet_kapitujt,
               credit_list=[sipas_slug[FOTO_RRETH]] + list(vendet_kapitujt.values()))
        faqet_sitemap.append(("about/", "0.6"))

        # ---- Informacion praktik ----
        ikonat = {"bus": arti.ikona_info("bus"), "airport": arti.ikona_info("airport"),
                  "taxi": arti.ikona_info("taxi"), "money": arti.ikona_info("money")}
        render("info.html", "info/", {"title": f"{INFO[lang]['title']} | {emri}", "desc": INFO[lang]["lead"],
                                      "og_image": sipas_slug[FOTO_INFO]["img"]["src1280"]},
               2, active="info", info=INFO[lang], info_icons=ikonat, emergency=URGJENCA, sources=BURIMET,
               checked=KONTROLLUAR[lang], hero_place=sipas_slug[FOTO_INFO])
        faqet_sitemap.append(("info/", "0.7"))

        # ---- Udhëtime ditore jashtë Tiranës ----
        uu = UDH.UI[lang]
        udhetimet = []
        for d in UDH.UDHETIMET:
            x = {k: (v[lang] if isinstance(v, dict) and lang in v else v) for k, v in d.items()}
            x["see"] = [(a[lang], b[lang]) for a, b in d["see"]]
            x["img"] = foto_wikimedia(UDH.FOTOT[d["foto"]])
            x["alt"] = f'{x["name"]}, Albania'
            udhetimet.append(x)
        render("daytrips.html", "day-trips/", {"title": f"{uu['title']} | {emri}", "desc": uu["lead"],
                                               "og_image": udhetimet[2]["img"]["src1280"]},
               2, active="daytrips", ui=uu, trips=udhetimet, terminal=UDH.TERMINALI,
               terminal_name=UDH.TERMINALI["name"][lang], sources=UDH.BURIMET, checked=UDH.KONTROLLUAR[lang])
        faqet_sitemap.append(("day-trips/", "0.8"))

        # ---- Itineraret: lista dhe një faqe për secilin ----
        ui = IT_UI[lang]
        render("itineraries.html", "itineraries/", {"title": f"{ui['index_title']} | {emri}", "desc": ui["index_lead"],
                                                    "og_image": itineraret[2][0]["hero"]["img"]["src1280"]},
               2, active="itineraries", ui=ui, itins=itineraret[2], credit_list=[i["hero"] for i in itineraret[2]], dt_ui=UDH.UI[lang])
        faqet_sitemap.append(("itineraries/", "0.8"))
        for it in itineraret[3]:
            jsonld = {"@context": "https://schema.org", "@type": "TouristTrip", "name": it["title"], "description": it["summary"],
                      "url": url(lang, f"itineraries/{it['slug']}/"), "inLanguage": lang,
                      "itinerary": {"@type": "ItemList", "numberOfItems": it["n"], "itemListElement": [
                          {"@type": "ListItem", "position": nd["n"], "item": {"@type": "TouristAttraction", "name": nd["p"]["name"],
                                                                              "url": url(lang, f"places/{nd['p']['slug']}/")}}
                          for nd in it["stops"]]}}
            if it["hero"]["img"]:
                jsonld["image"] = it["hero"]["img"]["src1280"]
            te_tjera = [x for x in itineraret[3] if x["slug"] != it["slug"]]
            render("itinerary.html", f"itineraries/{it['slug']}/", {
                "title": f"{it['title']}: {ui['eyebrow'].lower()} | {emri}", "og_title": it["title"], "desc": it["summary"],
                "og_image": it["hero"]["img"]["src1280"] if it["hero"]["img"] else None, "jsonld": json.dumps(jsonld, ensure_ascii=False),
            }, 3, active="itineraries", ui=ui, it=it, others=te_tjera,
               credit_list=[it["hero"]] + [nd["p"] for nd in it["stops"]] + [x["hero"] for x in te_tjera])
            faqet_sitemap.append((f"itineraries/{it['slug']}/", "0.8"))

        # ---- Faqja e çdo vendi ----
        for p in vendet:
            afer = sorted((x for x in vendet if x["slug"] != p["slug"]), key=lambda x: metra(p, x))[:3]
            jsonld = {"@context": "https://schema.org", "@type": "TouristAttraction", "name": p["name"],
                      "alternateName": p["local"], "description": p["summary"], "url": url(lang, f"places/{p['slug']}/"),
                      "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lon"]},
                      "address": {"@type": "PostalAddress", "addressLocality": "Tirana", "addressCountry": "AL"}}
            if p["img"]:
                jsonld["image"] = p["img"]["src1280"]
            render("place.html", f"places/{p['slug']}/", {
                "title": f"{p['name']}, Tirana | {emri}", "og_title": p["name"], "desc": p["summary"], "og_type": "article",
                "og_image": p["img"]["src1280"] if p["img"] else None, "jsonld": json.dumps(jsonld, ensure_ascii=False),
            }, 3, p=p, nearby=afer, active="explore")
            faqet_sitemap.append((f"places/{p['slug']}/", "0.7"))

        # ---- Kontakti dhe faqet ligjore ----
        mesazhet = {"required": t["f_err_required"], "email": t["f_err_email"], "short": t["f_err_short"],
                    "long": t["f_err_long"], "consent": t["f_err_consent"], "server": t["f_err_server"],
                    "rate": t["f_err_rate"], "ok": t["f_ok"], "sending": t["f_sending"]}
        render("contact.html", "contact/", {"title": f"{t['contact_title']} | {emri}", "desc": t["contact_lead"],
                                            "jsonld": json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                                                                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
                                                                 ensure_ascii=False)},
               2, active="contact", form_msgs=json.dumps(mesazhet, ensure_ascii=False).replace("'", "&#39;"))
        faqet_sitemap.append(("contact/", "0.4"))
        for rruga, titulli, seksionet in (("privacy/", t["privacy"], PRIVATESIA[lang]), ("terms/", t["terms"], KUSHTET[lang])):
            seksionet = [(a, b.format(owner=cfg["owner"], email=cfg["email"])) for a, b in seksionet]
            render("legal.html", rruga, {"title": f"{titulli} | {emri}", "desc": f"{titulli}: {emri}"},
                   2, heading=titulli, sections=seksionet)
            faqet_sitemap.append((rruga, "0.2"))

    # ---- 404: shërbehet në çdo adresë, ndaj përdor rrugë absolute (base_path) ----
    t = T["en"]
    kat_en = [{"slug": s, "name": k["en"], "color": k["color"], "desc": KATEGORITE_PERSHKRIM[s]["en"]} for s, k in KATEGORITE.items()]
    html = env.get_template("notfound.html").render(
        lang="en", t=t, cfg=cfg, root=cfg["base_path"], langs=GJUHET, lang_names=EMRAT_E_GJUHEVE, locale=LOCALE["en"],
        cat_list=kat_en, brand_mark=logo, v=VERSIONI, year=date.today().year,
        page={"title": f"{t['nf_title']} | {cfg['site_name']}", "desc": t["nf_text"], "path": "", "url": site + "/404.html",
              "alternates": {l: f"{site}/{l}/" for l in GJUHET}, "og_image": f"{site}/assets/img/og-default.png"})
    html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    shkruaj("404.html", html)

    # ---- offline.html: shfaqet nga service worker kur s'ka internet dhe faqja s'është ruajtur ----
    html = env.get_template("offline.html").render(
        lang="en", t=t, T=T, cfg=cfg, root=cfg["base_path"], langs=GJUHET, lang_names=EMRAT_E_GJUHEVE, locale=LOCALE["en"],
        cat_list=kat_en, brand_mark=logo, v=VERSIONI, year=date.today().year,
        page={"title": f"{t['off_title']} | {cfg['site_name']}", "desc": t["off_text"], "path": "", "url": site + "/offline.html",
              "alternates": {l: f"{site}/{l}/" for l in GJUHET}, "og_image": f"{site}/assets/img/og-default.png"})
    shkruaj("offline.html", html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))

    # ---- sw.js: faqja punon edhe pa internet (ruan faqet kryesore dhe ato që hap vizitori) ----
    para = ["offline.html", "site.webmanifest", "favicon.svg", "icon-192.png", "assets/fonts/manrope-var.woff2",
            f"assets/css/site.css?v={VERSIONI}", f"assets/js/site.js?v={VERSIONI}", f"assets/js/placesmap.js?v={VERSIONI}"]
    para += [f"{l}/{r}" for l in GJUHET for r in ("", "info/", "explore/")]
    with open(os.path.join(BURIMI, "sw.js"), encoding="utf-8") as fh:
        shkruaj("sw.js", fh.read().replace("__VERSIONI__", VERSIONI).replace("__PARA__", json.dumps(para, ensure_ascii=False)))

    # ---- index.html: zgjedh gjuhën (e ruajtur, ose e shfletuesit) ----
    shkruaj("index.html", f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{cfg["site_name"]}: Tirana travel guide</title>
<meta name="description" content="{T["en"]["site_desc"]}">
<link rel="canonical" href="{site}/en/">
{"".join(f'<link rel="alternate" hreflang="{l}" href="{site}/{l}/">' for l in GJUHET)}
<link rel="alternate" hreflang="x-default" href="{site}/en/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>
(function(){{var g=["en","it","sq"],z=null;try{{z=localStorage.getItem("gt-lang")}}catch(e){{}}
if(g.indexOf(z)<0){{z=((navigator.languages||[navigator.language||"en"])[0]||"en").slice(0,2).toLowerCase();}}
if(g.indexOf(z)<0)z="en";location.replace(z+"/");}})();
</script>
<style>body{{font:17px/1.5 system-ui,sans-serif;max-width:560px;margin:15vh auto;padding:0 20px;color:#1e242b}}a{{display:inline-block;margin:6px 16px 6px 0;font-weight:700}}</style>
</head><body><h1>{cfg["site_name"]}</h1>
{"".join(f'<a href="{l}/" hreflang="{l}" lang="{l}">{EMRAT_E_GJUHEVE[l]}</a>' for l in GJUHET)}
</body></html>
''')

    # ---- sitemap.xml (me lidhjet mes gjuhëve) dhe robots.txt ----
    rreshta = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    pare = set()
    for rruga, prioriteti in faqet_sitemap:
        if rruga in pare:
            continue
        pare.add(rruga)
        for lang in GJUHET:
            rreshta.append(f"  <url><loc>{url(lang, rruga)}</loc><lastmod>{cfg['updated']}</lastmod><priority>{prioriteti}</priority>")
            for l2 in GJUHET:
                rreshta.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{url(l2, rruga)}"/>')
            rreshta.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en", rruga)}"/>')
            rreshta.append("  </url>")
    rreshta.append("</urlset>")
    shkruaj("sitemap.xml", "\n".join(rreshta) + "\n")
    shkruaj("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /private/\nDisallow: /burimi_faqes/\nDisallow: /scripts/\n\nSitemap: {site}/sitemap.xml\n")

    # ---- site.webmanifest ----
    shkruaj("site.webmanifest", json.dumps({
        "name": cfg["site_name"], "short_name": cfg["site_name"], "id": "./", "start_url": "./", "scope": "./", "display": "standalone",
        "description": T["en"]["site_desc"], "lang": "en",
        "background_color": "#ffffff", "theme_color": "#171c22",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")

    # ---- .htaccess: HTTPS, siguria, cache, ngjeshja, 404 ----
    shkruaj(".htaccess", f"""# Go Tirana: konfigurimi i Apache (gjeneruar nga scripts/03_nderto_faqen.py)

ErrorDocument 404 {cfg["base_path"]}404.html
Options -Indexes

# --- Detyro HTTPS (përveç localhost, ku s'ka certifikatë) ---
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{{HTTPS}} off
  RewriteCond %{{HTTP:X-Forwarded-Proto}} !https
  RewriteCond %{{HTTP_HOST}} !^(localhost|127\\.0\\.0\\.1|192\\.168\\.)
  RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]
  # Dosjet e brendshme nuk shërbehen kurrë
  RewriteRule ^(burimi_faqes|scripts|private)(/|$) - [F,L]
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Permissions-Policy "geolocation=(self), camera=(), microphone=()"
  # HSTS vetëm kur faqja shërbehet me HTTPS
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains" "expr=%{{HTTPS}} == 'on'"

  # Faqet dhe të dhënat: shfletuesi pyet gjithmonë për version të ri
  <FilesMatch "\\.(html|json|webmanifest|xml|txt)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  # CSS/JS (me ?v=), shkronjat dhe imazhet: ruhen gjatë
  <FilesMatch "\\.(css|js|woff2|png|svg|ico|webp|mp4)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
  # Service worker: duhet kontrolluar gjithmonë për version të ri
  <FilesMatch "^sw\\.js$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
</IfModule>

# --- Ngjeshja (gzip): p.sh. rruget_kembe.json nga 4 MB në rreth 1 MB ---
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json application/manifest+json image/svg+xml
</IfModule>
<IfModule mod_mime.c>
  AddType application/manifest+json .webmanifest
</IfModule>
""")

    n = len({r for r, _ in faqet_sitemap})
    print(f"U ndërtuan {n} faqe x {len(GJUHET)} gjuhë = {n * len(GJUHET)} faqe HTML, plus 404, sitemap, robots dhe .htaccess.")
    if "example" in site or cfg["owner"].startswith("["):
        print("KUJDES: ndrysho site_url, owner dhe email te burimi_faqes/konfigurimi.json para publikimit.")
    if not cfg.get("goatcounter_code"):
        print("Statistikat janë çaktivizuar: shto goatcounter_code te konfigurimi.json kur të kesh llogari.")


if __name__ == "__main__":
    main()
