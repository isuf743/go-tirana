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

  // ---- Faqja pa internet: service worker (vetëm në HTTPS ose localhost, siç kërkojnë shfletuesit) ----
  if ("serviceWorker" in navigator && (location.protocol === "https:" || ["localhost", "127.0.0.1"].includes(location.hostname))) {
    window.addEventListener("load", () => navigator.serviceWorker.register(document.body.dataset.root + "sw.js").catch(() => {}));
  }
})();
