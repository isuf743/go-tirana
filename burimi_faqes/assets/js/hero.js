/* Go Tirana: video në sfond të hero-s
   - Ngarkohet vetëm pasi faqja është hapur (nuk ngadalëson tekstin dhe butonat).
   - Telefoni merr versionin 480p, kompjuteri 720p.
   - Nuk luhet nëse përdoruesi ka zgjedhur "më pak lëvizje" ose "kurse të dhënat": mbetet fotoja.
   - Butoni pauzë/luaj e lejon vizitorin ta ndalë (kërkesë e aksesueshmërisë për lëvizje > 5 sekonda). */
(function () {
  "use strict";
  const v = document.getElementById("hero-video");
  const btn = document.getElementById("hero-toggle");
  if (!v || !btn) return;
  const qeta = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const kursim = navigator.connection && navigator.connection.saveData;
  if (qeta || kursim) return;

  let ndaluarNgaPerdoruesi = false;
  try { ndaluarNgaPerdoruesi = localStorage.getItem("gt-hero-paused") === "1"; } catch (e) {}

  function gjendja(luan) {
    btn.classList.toggle("is-paused", !luan);
    btn.setAttribute("aria-label", luan ? btn.dataset.pause : btn.dataset.play);
  }

  function nis() {
    v.src = window.matchMedia("(min-width: 900px)").matches ? v.dataset.srcLg : v.dataset.srcSm;
    v.addEventListener("playing", () => v.classList.add("is-ready"), { once: true });
    btn.hidden = false;
    if (ndaluarNgaPerdoruesi) { gjendja(false); v.load(); return; }
    v.play().then(() => gjendja(true)).catch(() => gjendja(false));
  }

  btn.addEventListener("click", () => {
    if (v.paused) { v.play(); gjendja(true); ndaluarNgaPerdoruesi = false; }
    else { v.pause(); gjendja(false); ndaluarNgaPerdoruesi = true; }
    try { localStorage.setItem("gt-hero-paused", ndaluarNgaPerdoruesi ? "1" : "0"); } catch (e) {}
  });

  // Kursejmë bateri: videoja ndalet kur hero nuk duket në ekran
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => {
      if (!v.src || ndaluarNgaPerdoruesi) return;
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    }).observe(v);
  }

  if (document.readyState === "complete") nis();
  else window.addEventListener("load", nis, { once: true });
})();
