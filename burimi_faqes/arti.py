"""
Ilustrimet e Go Tirana si SVG (pa imazhe të jashtme): fasadat e lyera të Tiranës.
Të gjitha janë deterministe: i njëjti input jep gjithmonë të njëjtin vizatim.
"""
import random

NGJYRAT = ["#a33c26", "#11707c", "#8f5a0a", "#2d6a31", "#5b3fa6", "#c8102e"]
INK = "#1e242b"


def _pallat(x, y_baze, w, h, ngjyra, rnd, dritare="#ffffff", errësirë=None):
    """Një pallat: drejtkëndësh me rrjet dritaresh (disa të fikura nëse errësirë jepet)."""
    pjeset = [f'<rect x="{x}" y="{y_baze - h}" width="{w}" height="{h}" fill="{ngjyra}"/>']
    kolona = max(2, int(w // 18))
    hap_x = w / kolona
    dw, dh = hap_x * 0.46, 11
    rreshta = int((h - 26) // 26)
    for r in range(rreshta):
        for k in range(kolona):
            dx = x + k * hap_x + (hap_x - dw) / 2
            dy = y_baze - h + 16 + r * 26
            ngj = dritare
            if errësirë is not None and rnd.random() < errësirë:
                ngj = "rgba(0,0,0,.28)"
            pjeset.append(f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh}" rx="1.5" fill="{ngj}" opacity=".9"/>')
    # brez çatie
    pjeset.append(f'<rect x="{x - 3}" y="{y_baze - h - 6}" width="{w + 6}" height="6" fill="{INK}" opacity=".85"/>')
    return "".join(pjeset)


def fasadat(w=640, h=380, me_autobus=True, fara=7):
    rnd = random.Random(fara)
    y_baze = h - 6
    x, pjeset, i = 0, [], 0
    lartesite = [210, 300, 170, 330, 240, 280, 190, 315, 225]
    gjeresite = [70, 86, 58, 92, 74, 80, 62, 88, 72]
    while x < w:
        bw = gjeresite[i % len(gjeresite)]
        bh = lartesite[i % len(lartesite)]
        pjeset.append(_pallat(x + 4, y_baze, bw - 8, bh, NGJYRAT[i % len(NGJYRAT)], rnd))
        x += bw
        i += 1
    if me_autobus:   # autobusi i qytetit përpara pallateve
        bx, by = 70, y_baze - 52
        pjeset.append(
            f'<g><rect x="{bx}" y="{by}" width="190" height="48" rx="10" fill="#c8102e"/>'
            f'<rect x="{bx}" y="{by + 34}" width="190" height="6" fill="#a30d25"/>'
            + "".join(f'<rect x="{bx + 14 + k * 30}" y="{by + 9}" width="22" height="16" rx="3" fill="#fff" opacity=".92"/>' for k in range(5))
            + f'<rect x="{bx + 164}" y="{by + 9}" width="16" height="25" rx="3" fill="#fff" opacity=".92"/>'
            f'<circle cx="{bx + 42}" cy="{by + 48}" r="10" fill="{INK}"/><circle cx="{bx + 42}" cy="{by + 48}" r="4" fill="#cfd5da"/>'
            f'<circle cx="{bx + 150}" cy="{by + 48}" r="10" fill="{INK}"/><circle cx="{bx + 150}" cy="{by + 48}" r="4" fill="#cfd5da"/></g>')
    return (f'<svg class="facades" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'preserveAspectRatio="xMidYMax meet">{"".join(pjeset)}</svg>')


def nate(fara, ngjyra="#5b3fa6", w=960, h=600):
    """Ilustrim i natës për lokalet pa foto: qiell i errët, dritare të ndezura."""
    rnd = random.Random(fara)
    pjeset = [f'<rect width="{w}" height="{h}" fill="#20233a"/>',
              f'<circle cx="{w * 0.8:.0f}" cy="{h * 0.2:.0f}" r="34" fill="#f6e7b6" opacity=".9"/>']
    for _ in range(40):
        pjeset.append(f'<circle cx="{rnd.random() * w:.0f}" cy="{rnd.random() * h * 0.45:.0f}" r="{rnd.random() * 1.6 + .4:.1f}" fill="#fff" opacity=".6"/>')
    x, i = 0, 0
    tone = [ngjyra, "#2f3350", "#3a2f63", ngjyra, "#2a3a4f"]
    while x < w:
        bw = rnd.choice([110, 140, 90, 160])
        bh = rnd.randint(int(h * .35), int(h * .8))
        pjeset.append(_pallat(x + 6, h, bw - 12, bh, tone[i % len(tone)], rnd, dritare="#ffd36e", errësirë=.45))
        x += bw; i += 1
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'preserveAspectRatio="xMidYMid slice" aria-hidden="true">{"".join(pjeset)}</svg>')


def logo(madhesia=36):
    """Logoja GO TIRANA: katror i kuq me një kunj harte të bardhë dhe një rrugë me dy stacione poshtë tij."""
    return (f'<svg class="brand__mark" width="{madhesia}" height="{madhesia}" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            + LOGO_BRENDA + '</svg>')


LOGO_BRENDA = ('<rect width="40" height="40" rx="11" fill="#d31332"/>'
               '<path d="M8.5 32.5h23" stroke="#fff" stroke-opacity=".45" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 5.4"/>'
               '<circle cx="8.6" cy="32.5" r="2.4" fill="#fff"/><circle cx="31.4" cy="32.5" r="2.4" fill="#fff"/>'
               '<path d="M20 6.5c-5.3 0-9.3 4-9.3 9.1 0 6.3 9.3 14.4 9.3 14.4s9.3-8.1 9.3-14.4c0-5.1-4-9.1-9.3-9.1z" fill="#fff"/>'
               '<circle cx="20" cy="15.6" r="3.7" fill="#d31332"/>')


def diagrami_linjes(emrat, ecje, ngjyra="#c8102e"):
    """Diagram i një udhëtimi: ecje -> autobus -> ecje, me emrat e stacioneve."""
    a, b, c, d = emrat
    return f'''<svg viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg" role="img" font-family="Overpass, system-ui, sans-serif">
  <line x1="40" y1="40" x2="40" y2="92" stroke="#8a929a" stroke-width="4" stroke-dasharray="1 8" stroke-linecap="round"/>
  <line x1="40" y1="100" x2="40" y2="208" stroke="{ngjyra}" stroke-width="8" stroke-linecap="round"/>
  <line x1="40" y1="216" x2="40" y2="262" stroke="#8a929a" stroke-width="4" stroke-dasharray="1 8" stroke-linecap="round"/>
  <circle cx="40" cy="32" r="9" fill="#fff" stroke="#13865a" stroke-width="4"/>
  <circle cx="40" cy="100" r="9" fill="#fff" stroke="{ngjyra}" stroke-width="4"/>
  <circle cx="40" cy="154" r="5" fill="{ngjyra}"/>
  <circle cx="40" cy="208" r="9" fill="#fff" stroke="{ngjyra}" stroke-width="4"/>
  <rect x="31" y="262" width="18" height="18" rx="3" fill="{ngjyra}"/>
  <text x="66" y="37" font-size="16" font-weight="700" fill="{INK}">{a}</text>
  <text x="66" y="68" font-size="13" fill="#59626b">{ecje[0]}</text>
  <rect x="66" y="88" width="46" height="24" rx="6" fill="{ngjyra}"/>
  <text x="89" y="105" font-size="13" font-weight="800" fill="#fff" text-anchor="middle">L5B</text>
  <text x="122" y="105" font-size="16" font-weight="700" fill="{INK}">{b}</text>
  <text x="66" y="213" font-size="16" font-weight="700" fill="{INK}">{c}</text>
  <text x="66" y="244" font-size="13" fill="#59626b">{ecje[1]}</text>
  <text x="66" y="277" font-size="16" font-weight="700" fill="{INK}">{d}</text>
</svg>'''


_IKONAT_INFO = {
    "bus": '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 10h14M8 20v-3M16 20v-3"/><circle cx="8.5" cy="13.5" r=".6" fill="currentColor"/><circle cx="15.5" cy="13.5" r=".6" fill="currentColor"/>',
    "airport": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "taxi": '<path d="M5 16V12l2-5h10l2 5v4"/><path d="M3.5 12h17v4.5h-17zM9 4.5h6"/><circle cx="7.5" cy="19" r="1.5"/><circle cx="16.5" cy="19" r="1.5"/>',
    "money": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6.5 9.5v5M17.5 9.5v5"/>',
}


def ikona_info(emri):
    """Ikonë e thjeshtë me vija (24x24) për seksionet e faqes Informacion praktik."""
    return (f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_IKONAT_INFO[emri]}</svg>')
