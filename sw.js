/* GO TIRANA: service worker (gjeneruar nga scripts/03_nderto_faqen.py nga burimi_faqes/sw.js)
   Qëllimi: faqja të hapet edhe pa internet, p.sh. sapo turisti zbret në aeroport pa të dhëna celulare.
   - Faqet kryesore (kreu, Eksploro, Informacion praktik, në 3 gjuhë) ruhen që në vizitën e parë.
   - Çdo faqe tjetër që hap vizitori ruhet automatikisht për herën tjetër.
   - Faqet HTML: provojmë internetin më parë (që të shihen ndryshimet), pastaj kopjen e ruajtur.
   - CSS, JS, shkronjat, fotot dhe të dhënat e autobusëve: kopja e ruajtur menjëherë, rifreskohet në sfond.
   - Pllakat e hartës dhe statistikat nuk ruhen (janë shumë të mëdha / s'kanë kuptim offline). */
"use strict";
const VERSIONI = "28";
const PARA = "gt-para-" + VERSIONI;        // ruhen gjatë instalimit
const GJATE = "gt-gjate-" + VERSIONI;      // ruhen gjatë përdorimit
const LISTA = ["offline.html", "site.webmanifest", "favicon.svg", "icon-192.png", "assets/fonts/manrope-var.woff2", "assets/css/site.css?v=28", "assets/js/site.js?v=28", "assets/js/placesmap.js?v=28", "en/", "en/info/", "en/explore/", "it/", "it/info/", "it/explore/", "sq/", "sq/info/", "sq/explore/"];
const FOTOT_E_JASHTME = ["upload.wikimedia.org"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(PARA).then(c => c.addAll(LISTA)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith("gt-") && k !== PARA && k !== GJATE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

const ruaj = (req, res) => {
  if (res && (res.ok || res.type === "opaque")) caches.open(GJATE).then(c => c.put(req, res));
};

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;                       // formularët (api/) kalojnë gjithmonë në rrjet
  const url = new URL(req.url);
  const imi = url.origin === self.location.origin;

  if (imi && url.pathname.includes("/api/")) return;
  if (req.headers.has("range") || url.pathname.endsWith(".mp4")) return;   // video: shfletuesi e shkarkon me copa, s'e ruajmë

  if (req.mode === "navigate") {                          // faqe HTML
    e.respondWith(fetch(req).then(res => { ruaj(req, res.clone()); return res; }).catch(async () =>
      (await caches.match(req)) || (await caches.match(req, { ignoreSearch: true })) ||
      (await caches.match(new URL("offline.html", self.registration.scope).href))));
    return;
  }

  if (imi || FOTOT_E_JASHTME.includes(url.hostname)) {   // asete: nga kopja, rifreskim në sfond
    e.respondWith(caches.match(req).then(kopja => {
      const rrjeti = fetch(req).then(res => { ruaj(req, res.clone()); return res; }).catch(() => kopja);
      return kopja || rrjeti;
    }));
  }
});
