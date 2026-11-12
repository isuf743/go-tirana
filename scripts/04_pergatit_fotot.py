"""
HAPI 6: Përgatitja e fotove të tua për Go Tirana
================================================

Lexon:  fotot_e_mia/<vendi>/*.png|jpg|jpeg|webp   (një dosje për çdo vend, emrat e fotove s'kanë rëndësi)
        fotot_e_mia/<vendi>.png                       (ose një foto e vetme me emrin e vendit, p.sh. oda-garden.png)
Krijon: burimi_faqes/assets/img/vendet/<slug>/<n>-500.webp  (për kartat dhe telefonin)
        burimi_faqes/assets/img/vendet/<slug>/<n>-full.webp (për galerinë, maks. 1600 px)
        burimi_faqes/fotot_lokale.json                       (lista që lexon 03_nderto_faqen.py)

Pse WebP: e njëjta cilësi me JPG, por rreth 30-50% më e lehtë, pra faqja hapet më shpejt.

Si ekzekutohet:
  pip install pillow
  python scripts/04_pergatit_fotot.py
  python scripts/03_nderto_faqen.py
"""

import json
import os
import re
import shutil
import unicodedata

try:
    from PIL import Image, ImageOps
except ImportError:
    raise SystemExit("Mungon Pillow. Instaloje me:  pip install pillow")

KETU = os.path.dirname(os.path.abspath(__file__))
PROJEKTI = os.path.normpath(os.path.join(KETU, ".."))
BURIMI = os.path.join(PROJEKTI, "burimi_faqes")
HYRJA = os.path.join(PROJEKTI, "fotot_e_mia")
DALJA = os.path.join(BURIMI, "assets", "img", "vendet")

# Emra dosjesh që nuk përputhen saktë me "slug"-un e vendit
ALIASET = {"escape": "escape-premium-club", "hemingway": "hemingway-bar", "tunel": "tunel-music-venue",
           "cinco": "cinco-cavalli", "sky": "sky-tower", "radio": "radio-bar", "magic": "magic-club"}

# Cila foto del e para (në kartë dhe në krye të faqes). Të tjerat vijnë sipas emrit.
KRYESORJA = {"frekuence": "grekuence", "hemingway-bar": "hemingway1", "puls": "puls2"}

FORMATET = (".png", ".jpg", ".jpeg", ".webp")
MAKS_FULL = 1600


def thjeshto(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def gjej_slug(emri_dosjes, slugs):
    k = thjeshto(emri_dosjes)
    if k in slugs:
        return k
    if k in ALIASET:
        return ALIASET[k]
    kandidatet = [s for s in slugs if s.startswith(k) or k.startswith(s)]
    return kandidatet[0] if len(kandidatet) == 1 else None


def eshte_kopje(emri):
    return bool(re.search(r"(copy|kopje|\(\d+\))", emri, re.I))


def main():
    if not os.path.isdir(HYRJA):
        raise SystemExit(f"Nuk u gjet dosja {HYRJA}")
    slugs = {v["slug"] for v in json.load(open(os.path.join(BURIMI, "vendet.json"), encoding="utf-8"))}
    rezultati = {}
    # Fotot e vendosura direkt te fotot_e_mia/ me emrin e vendit (p.sh. oda-garden.png) futen te ai vend
    te_lira = {}
    for f in os.listdir(HYRJA):
        if os.path.isfile(os.path.join(HYRJA, f)) and f.lower().endswith(FORMATET) and not eshte_kopje(f):
            slug = gjej_slug(re.sub(r"\d+$", "", os.path.splitext(f)[0]), slugs)
            if slug:
                te_lira.setdefault(slug, []).append(os.path.join(HYRJA, f))
            else:
                print(f"  ! Fotoja '{f}' nuk përputhet me asnjë vend: fute te një dosje me emrin e vendit")
    dosjet = [d for d in sorted(os.listdir(HYRJA)) if os.path.isdir(os.path.join(HYRJA, d))]
    for slug in te_lira:
        if not any(gjej_slug(d, slugs) == slug for d in dosjet):
            dosjet.append(slug)
    for dosja in dosjet:
        rruga = os.path.join(HYRJA, dosja)
        slug = gjej_slug(dosja, slugs)
        if not slug:
            print(f"  ! Dosja '{dosja}' nuk përputhet me asnjë vend: riemërtoje si te vendet.json")
            continue
        fotot = sorted(os.path.join(rruga, f) for f in os.listdir(rruga)
                       if f.lower().endswith(FORMATET) and not eshte_kopje(f)) if os.path.isdir(rruga) else []
        fotot += sorted(te_lira.get(slug, []))
        pare = KRYESORJA.get(slug)
        fotot.sort(key=lambda f: (os.path.splitext(os.path.basename(f))[0] != pare,))
        if not fotot:
            continue
        dal = os.path.join(DALJA, slug)
        shutil.rmtree(dal, ignore_errors=True)
        os.makedirs(dal)
        lista = []
        for i, f in enumerate(fotot, 1):
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
            w, h = im.size
            full = im.copy()
            full.thumbnail((MAKS_FULL, MAKS_FULL), Image.LANCZOS)
            full.save(os.path.join(dal, f"{i}-full.webp"), "WEBP", quality=82, method=6)
            vog = im.copy()
            if w > 500:
                vog = im.resize((500, round(h * 500 / w)), Image.LANCZOS)
            vog.save(os.path.join(dal, f"{i}-500.webp"), "WEBP", quality=78, method=6)
            lista.append({"n": i, "w": full.width, "h": full.height})
        rezultati[slug] = lista
        print(f"  {slug}: {len(lista)} foto (nga '{dosja}')")
    with open(os.path.join(BURIMI, "fotot_lokale.json"), "w", encoding="utf-8") as fh:
        json.dump(rezultati, fh, indent=1)
    print(f"Gati: {sum(len(v) for v in rezultati.values())} foto për {len(rezultati)} vende.")


if __name__ == "__main__":
    main()
