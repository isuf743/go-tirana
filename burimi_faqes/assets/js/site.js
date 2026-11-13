/* GO TIRANA: skriptet e përbashkëta
   koka që ndryshon gjatë scroll-it, menyja në telefon, gjuha, pëlqimi për statistikat, animacionet */
(function () {
  "use strict";
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* p.sh. dritare private */ } },
  };
  const hdr = document.getElementById("hdr");

  // ---- Koka: e tejdukshme mbi hero, e bardhë pasi lëviz poshtë ----
  if (hdr) {
    let ticking = false;
    const update = () => { hdr.classList.toggle("is-scrolled", window.scrollY > 24); ticking = false; };
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // ---- Menyja në telefon ----
  const toggle = document.querySelector(".nav-toggle");
  if (toggle && hdr) {
    const setOpen = open => {
      hdr.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    };
    toggle.addEventListener("click", () => setOpen(!hdr.classList.contains("is-open")));
    document.addEventListener("keydown", e => { if (e.key === "Escape" && hdr.classList.contains("is-open")) { setOpen(false); toggle.focus(); } });
    document.querySelectorAll(".nav a").forEach(a => a.addEventListener("click", () => setOpen(false)));
    window.matchMedia("(min-width: 1021px)").addEventListener("change", e => { if (e.matches) setOpen(false); });
  }

  // ---- Gjuha: e mbajmë mend zgjedhjen ----
  document.querySelectorAll("[data-setlang]").forEach(a =>
    a.addEventListener("click", () => store.set("gt-lang", a.dataset.setlang)));
  store.set("gt-lang", document.body.dataset.lang);

  // ---- Animacionet kur elementet dalin në ekran ----
  const reveal = document.querySelectorAll("[data-reveal]");
  const qeta = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!("IntersectionObserver" in window) || qeta) {
    reveal.forEach(el => el.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    }), { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveal.forEach(el => io.observe(el));
  }

  // ---- Pëlqimi për statistikat (GoatCounter ngarkohet VETËM pasi vizitori pranon) ----
  const banner = document.querySelector(".consent");
  const code = document.body.dataset.goatcounter;
  function ngarkoStatistikat() {
    if (!code || document.querySelector("script[data-goatcounter]")) return;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://gc.zgo.at/count.js";
    s.dataset.goatcounter = "https://" + code + ".goatcounter.com/count";
    document.head.appendChild(s);
  }
  function shfaqBanderolen() { if (banner) { banner.hidden = false; banner.querySelector("button").focus({ preventScroll: true }); } }
  const zgjedhja = store.get("gt-consent");
  if (zgjedhja === "yes") ngarkoStatistikat();
  else if (zgjedhja !== "no") shfaqBanderolen();
  if (banner) {
    banner.querySelectorAll("[data-consent]").forEach(b => b.addEventListener("click", () => {
      store.set("gt-consent", b.dataset.consent);
      banner.hidden = true;
      if (b.dataset.consent === "yes") ngarkoStatistikat();
    }));
  }
  document.querySelectorAll("[data-open-consent]").forEach(b => b.addEventListener("click", shfaqBanderolen));


  // ---- "Hapur tani / Mbyllur": sipas orës së Tiranës, edhe kur vizitori është në një zonë tjetër kohore ----
  // data-orari = "gjithmone" ose 7 ditë [hënë..diel], secila null ose ["09:00","17:00"]; mbyllja pas mesnatës lejohet.
  const shenjat = document.querySelectorAll(".open-badge[data-orari]");
  const tekstetOrari = document.getElementById("orari-tekste");
  if (shenjat.length && tekstetOrari) {
    const T = JSON.parse(tekstetOrari.textContent);
    const minuta = s => { const [h, m] = s.split(":").map(Number); return h * 60 + m; };
    function tani() {   // dita (0 = e hënë) dhe minutat në Tiranë
      const pj = {};
      new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Tirane", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
        .formatToParts(new Date()).forEach(x => { pj[x.type] = x.value; });
      return { dita: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].indexOf(pj.weekday), min: +pj.hour * 60 + +pj.minute };
    }
    function gjendja(orari) {
      if (orari === "gjithmone") return { hapur: true, tekst: T.always };
      const { dita, min } = tani();
      // Intervalet e dje (nëse mbyllen pas mesnatës) dhe të sotme, në minuta nga mesnata e sotme
      for (const [d, zhvendosje] of [[(dita + 6) % 7, -1440], [dita, 0]]) {
        const o = orari[d]; if (!o) continue;
        const a = minuta(o[0]) + zhvendosje; let b = minuta(o[1]) + zhvendosje;
        if (minuta(o[1]) <= minuta(o[0])) b += 1440;   // mbyllet pas mesnatës (p.sh. 23:00–03:00 ose 07:00–00:00)
        if (min >= a && min < b) return { hapur: true, tekst: T.open + " · " + T.closes.replace("{t}", o[1]) };
      }
      for (let i = 0; i < 7; i++) {   // hapja e radhës
        const d = (dita + i) % 7, o = orari[d];
        if (!o || (i === 0 && minuta(o[0]) <= min)) continue;
        const t = i === 0 ? T.opens.replace("{t}", o[0]) : i === 1 ? T.opens_tomorrow.replace("{t}", o[0]) : T.opens_day.replace("{d}", T.days[d]).replace("{t}", o[0]);
        return { hapur: false, tekst: T.closed + " · " + t };
      }
      return { hapur: false, tekst: T.closed };
    }
    function rifresko() {
      shenjat.forEach(el => {
        try {
          const g = gjendja(JSON.parse(el.dataset.orari));
          el.textContent = g.tekst; el.classList.toggle("is-open", g.hapur); el.classList.toggle("is-closed", !g.hapur); el.hidden = false;
        } catch (e) { el.hidden = true; }
      });
    }
    rifresko();
    setInterval(rifresko, 60000);
  }

  // ---- Hero: slider me foto (fotot e Wikimedia ngarkohen pasi faqja hapet plotësisht) ----
  (function () {
    const media = document.querySelector(".hero__media"), ctl = document.querySelector(".hero__ctl");
    if (!media || !ctl) return;
    const slides = [...media.querySelectorAll(".hero__slide")], dots = [...ctl.querySelectorAll(".hero__dot")];
    const btn = ctl.querySelector(".hero__toggle"), label = document.querySelector(".hero__label");
    const credit = document.querySelector(".hero__credit"), coords = document.querySelector(".hero__coords");
    const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const KOHA = 3000;
    let cur = 0, timer = null, paused = calm, loaded = false;

    function load(sl) {
      const img = sl.querySelector("img[data-src]");
      if (!img) return Promise.resolve(true);
      return new Promise(res => {
        img.onload = () => { sl.dataset.ok = "1"; res(true); };
        img.onerror = () => { sl.dataset.bad = "1"; res(false); };
        img.srcset = img.dataset.srcset; img.src = img.dataset.src;
        img.removeAttribute("data-src");
      });
    }
    function show(i) {
      if (i === cur) return;
      const sl = slides[i];
      if (sl.dataset.bad) return;
      const go = () => {
        slides[cur].classList.remove("is-on"); sl.classList.add("is-on"); cur = i;
        dots.forEach((d, k) => d.setAttribute("aria-pressed", k === i ? "true" : "false"));
        if (label) label.textContent = sl.dataset.label;
        if (credit) {
          if (sl.dataset.artist) {
            credit.textContent = ctl.dataset.photo + ": " + sl.dataset.artist + ", " + sl.dataset.license;
            credit.href = sl.dataset.page; credit.hidden = false; if (coords) coords.hidden = true;
          } else { credit.hidden = true; if (coords) coords.hidden = false; }
        }
      };
      sl.dataset.ok || !sl.querySelector("img[data-src]") ? go() : load(sl).then(ok => ok && go());
    }
    function next() {
      for (let k = 1; k <= slides.length; k++) { const j = (cur + k) % slides.length; if (!slides[j].dataset.bad) return show(j); }
    }
    function plan() { clearTimeout(timer); if (!paused && !document.hidden && loaded) timer = setTimeout(() => { next(); plan(); }, KOHA); }
    function setPaused(p) {
      paused = p; btn.classList.toggle("is-paused", p);
      btn.setAttribute("aria-label", p ? ctl.dataset.play : ctl.dataset.pause); plan();
    }
    dots.forEach((d, k) => d.addEventListener("click", () => { show(k); plan(); }));
    btn.addEventListener("click", () => setPaused(!paused));
    document.addEventListener("visibilitychange", plan);
    ctl.hidden = false; setPaused(paused);
    // Fotot e tjera vetëm pasi faqja të ketë mbaruar (që të mos vonojnë foton e parë)
    const start = () => setTimeout(() => {
      const ngarko = slides.slice(1).reduce((p, sl) => p.then(() => load(sl)), Promise.resolve());
      loaded = true; plan();
      ngarko.then(() => slides.forEach((sl, k) => { if (sl.dataset.bad && dots[k]) dots[k].hidden = true; }));
    }, 1200);
    document.readyState === "complete" ? start() : window.addEventListener("load", start);
  })();

  // ---- Moti në hero (Open-Meteo, pa çelës). Ruhet 20 min që të mos e kërkojmë në çdo faqe ----
  (function () {
    const el = document.getElementById("wx");
    if (!el || !window.fetch) return;
    const M = JSON.parse(el.dataset.msg);
    const URL_MOTI = "https://api.open-meteo.com/v1/forecast?latitude=41.3275&longitude=19.8187" +
      "&current=temperature_2m,weather_code,is_day&daily=precipitation_probability_max&timezone=Europe%2FTirane&forecast_days=1";
    const S = 'stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"';
    const RE = '<path d="M7 17.5a4 4 0 0 1-.6-8 5.5 5.5 0 0 1 10.6 1.5 3.3 3.3 0 0 1 .3 6.5z" ' + S + '/>';
    const IK = {
      sun: '<circle cx="12" cy="12" r="4.2" ' + S + '/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" ' + S + '/>',
      moon: '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z" ' + S + '/>',
      part: '<circle cx="8.5" cy="8" r="3.2" ' + S + '/><path d="M8.5 2v1.3M3.2 8H2M4.7 4.2l.9.9M12.3 4.2l-.9.9" ' + S + '/><path d="M9 19.5a3.5 3.5 0 0 1-.4-7 4.8 4.8 0 0 1 9.2 1.3 2.9 2.9 0 0 1 .3 5.7z" ' + S + '/>',
      cloud: RE,
      rain: '<path d="M7 14.5a4 4 0 0 1-.6-8 5.5 5.5 0 0 1 10.6 1.5 3.3 3.3 0 0 1 .3 6.5z" ' + S + '/><path d="M8.5 17.5l-1 2.5M12.5 17.5l-1 2.5M16.5 17.5l-1 2.5" ' + S + '/>',
      snow: '<path d="M7 14.5a4 4 0 0 1-.6-8 5.5 5.5 0 0 1 10.6 1.5 3.3 3.3 0 0 1 .3 6.5z" ' + S + '/><path d="M8.5 18.5h.01M12 20h.01M15.5 18.5h.01" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
      storm: '<path d="M7 14.5a4 4 0 0 1-.6-8 5.5 5.5 0 0 1 10.6 1.5 3.3 3.3 0 0 1 .3 6.5z" ' + S + '/><path d="M12.5 15l-2 3.5h3l-2 3.5" ' + S + '/>',
      fog: '<path d="M4 9h16M3 13h18M5 17h14" ' + S + '/>',
    };
    function shfaq(d) {
      const c = d.current, kodi = c.weather_code, dite = c.is_day === 1, t = Math.round(c.temperature_2m);
      const shi = (d.daily && d.daily.precipitation_probability_max && d.daily.precipitation_probability_max[0]) || 0;
      let lloji, ik;
      if (kodi === 0) { lloji = dite ? "clear" : "night"; ik = dite ? "sun" : "moon"; }
      else if (kodi <= 2) { lloji = dite ? "mostly" : "night"; ik = dite ? "part" : "moon"; }
      else if (kodi === 3) { lloji = "cloudy"; ik = "cloud"; }
      else if (kodi <= 48) { lloji = "fog"; ik = "fog"; }
      else if (kodi <= 57) { lloji = "drizzle"; ik = "rain"; }
      else if (kodi <= 67) { lloji = "rain"; ik = "rain"; }
      else if (kodi <= 77 || kodi === 85 || kodi === 86) { lloji = "snow"; ik = "snow"; }
      else if (kodi <= 82) { lloji = "showers"; ik = "rain"; }
      else { lloji = "storm"; ik = "storm"; }
      const lageshti = ["drizzle", "rain", "showers", "storm"].includes(lloji) || (dite && shi >= 70);
      const k = lageshti ? "rain" : lloji === "snow" || t < 8 ? "cold" : !dite ? "night" : t >= 31 ? "hot"
              : ["clear", "mostly"].includes(lloji) ? "nice" : "grey";
      el.querySelector(".wx__ic").innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24">' + IK[ik] + "</svg>";
      el.querySelector(".wx__t").textContent = t + "°";
      el.querySelector(".wx__d").textContent = M.d[lloji];
      el.querySelector(".wx__tip").textContent = M.tip[k];
      el.href = M.links[k];
      el.title = M.src;
      el.setAttribute("aria-label", `${M.label}: ${t}°, ${M.d[lloji]}. ${M.tip[k]}`);
      el.hidden = false;
    }
    let ruajtur = null;
    try { ruajtur = JSON.parse(sessionStorage.getItem("gt-wx") || "null"); } catch (e) {}
    if (ruajtur && Date.now() - ruajtur.koha < 20 * 60 * 1000) return shfaq(ruajtur.d);
    fetch(URL_MOTI).then(r => r.ok ? r.json() : Promise.reject()).then(d => {
      if (!d.current) return;
      shfaq(d);
      try { sessionStorage.setItem("gt-wx", JSON.stringify({ koha: Date.now(), d })); } catch (e) {}
    }).catch(() => {});
  })();

  // ---- Faqja pa internet: service worker (vetëm në HTTPS ose localhost, siç kërkojnë shfletuesit) ----
  if ("serviceWorker" in navigator && (location.protocol === "https:" || ["localhost", "127.0.0.1"].includes(location.hostname))) {
    window.addEventListener("load", () => navigator.serviceWorker.register(document.body.dataset.root + "sw.js").catch(() => {}));
  }
})();
