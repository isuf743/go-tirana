/* Go Tirana: galeria e fotove (lightbox)
   Përdor <dialog> të shfletuesit: mban fokusin brenda, mbyllet me Esc, dhe është i aksesueshëm.
   Kontrollet: shigjetat e tastierës, butonat, ose rrëshqitje me gisht në telefon. */
(function () {
  "use strict";
  const dlg = document.getElementById("lightbox");
  const data = document.getElementById("gallery-data");
  if (!dlg || !data || typeof dlg.showModal !== "function") return;
  const fotot = JSON.parse(data.textContent);
  const img = document.getElementById("lb-img"), count = document.getElementById("lb-count");
  const prev = document.getElementById("lb-prev"), next = document.getElementById("lb-next");
  let i = 0, kthe = null;

  function show(n) {
    i = (n + fotot.length) % fotot.length;
    img.src = fotot[i];
    count.textContent = `${i + 1} / ${fotot.length}`;
    // ngarkojmë paraprakisht fotot fqinje që kalimi të jetë i menjëhershëm
    [i + 1, i - 1].forEach(k => { const im = new Image(); im.src = fotot[(k + fotot.length) % fotot.length]; });
  }
  function open(n, btn) {
    kthe = btn; show(n); dlg.showModal(); document.documentElement.classList.add("no-scroll");
  }
  dlg.addEventListener("close", () => { document.documentElement.classList.remove("no-scroll"); if (kthe) kthe.focus(); });

  document.querySelectorAll("[data-index]").forEach(b => b.addEventListener("click", () => open(+b.dataset.index, b)));
  prev.onclick = () => show(i - 1);
  next.onclick = () => show(i + 1);
  document.getElementById("lb-close").onclick = () => dlg.close();
  if (fotot.length < 2) { prev.hidden = next.hidden = true; }

  dlg.addEventListener("keydown", e => {
    if (e.key === "ArrowLeft") { e.preventDefault(); show(i - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); show(i + 1); }
  });
  // klikim në sfondin e errët = mbyll
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
  // rrëshqitje me gisht
  let x0 = null;
  dlg.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener("touchend", e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
  });
})();
