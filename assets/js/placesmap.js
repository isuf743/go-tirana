/* GO TIRANA: harta interaktive e vendeve (faqja kryesore dhe Eksploro)
   Kërkim me emër, filtra sipas kategorisë, lista/kartat dhe pikat në hartë mbahen të sinkronizuara. */
(function () {
  "use strict";
  // GPS i saktë; nëse skadon ose s'ka GPS (shpesh në kompjuter), provo sërish me vendndodhjen e rrjetit
  function geoMeRiprovim(ok, gabim) {
    navigator.geolocation.getCurrentPosition(ok, e => {
      if (e.code === 1) return gabim(e);
      navigator.geolocation.getCurrentPosition(ok, gabim, { enableHighAccuracy: false, timeout: 20000, maximumAge: 300000 });
    }, { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 });
  }
  const box = document.querySelector("[data-places-map]");
  const dataEl = document.getElementById("places-data");
  if (!box || !dataEl) return;
  const data = JSON.parse(dataEl.textContent);
  const root = document.body.dataset.root, lang = document.body.dataset.lang;
  const explore = box.dataset.pmMode === "explore";
  const mapEl = box.querySelector("[data-pm-map]");
  const search = box.querySelector("[data-pm-search]");
  const chips = box.querySelectorAll("[data-pm-cat]");
  const countEl = box.querySelector("[data-pm-count]");
  const emptyEl = box.querySelector("[data-pm-empty]");
  const items = box.querySelectorAll(".citymap__list > li, .card[data-slug]");
  // pa theks (ë -> e, ç -> c), që "skenderbej" të gjejë "Skënderbej"
  const norm = s => (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  items.forEach(it => { it._s = norm(it.dataset.search); it._c = (it.dataset.cats || "").split(" "); });

  let q = "", cat = "", map = null;
  const markers = {};

  function apply() {
    let n = 0;
    const visible = new Set();
    items.forEach(it => {
      const ok = (!cat || it._c.includes(cat)) && (!q || it._s.includes(q));
      it.hidden = !ok;
      if (ok) { n++; visible.add(it.dataset.slug); }
    });
    if (countEl) countEl.textContent = n === 1 && countEl.dataset.tpl1 ? countEl.dataset.tpl1 : countEl.dataset.tpl.replace("{n}", n);
    if (emptyEl) emptyEl.hidden = n > 0;
    for (const slug in markers) markers[slug].getElement().style.display = visible.has(slug) ? "" : "none";
    if (map && !explore && visible.size) fit([...visible]);
  }

  if (search) search.addEventListener("input", () => { q = norm(search.value.trim()); apply(); });
  chips.forEach(ch => ch.addEventListener("click", () => {
    cat = ch.dataset.pmCat;
    chips.forEach(c => c.setAttribute("aria-pressed", String(c === ch)));
    apply();
  }));

  function fit(slugs) {
    const b = new maplibregl.LngLatBounds();
    data.forEach(p => { if (slugs.includes(p.slug)) b.extend([p.lon, p.lat]); });
    if (slugs.length === 1) map.easeTo({ center: b.getCenter(), zoom: 15 });
    else map.fitBounds(b, { padding: 60, maxZoom: 15, duration: 600 });
  }

  function popupContent(p) {
    const a = document.createElement("a");
    a.className = "pm-pop"; a.href = `${root}${lang}/places/${p.slug}/`;
    if (p.img) {
      const w = document.createElement("span"); w.className = "pm-pop__img"; w.style.display = "block";
      const im = document.createElement("img"); im.src = p.img; im.alt = ""; im.loading = "lazy";
      w.appendChild(im); a.appendChild(w);
    }
    const body = document.createElement("span"); body.className = "pm-pop__body"; body.style.display = "block";
    const c = document.createElement("span"); c.className = "pm-pop__cat"; c.textContent = `${p.cat} · ${p.area}`;
    const nm = document.createElement("span"); nm.className = "pm-pop__name"; nm.textContent = p.name;
    const more = document.createElement("span"); more.className = "pm-pop__more"; more.textContent = (box.dataset.more || "") + " →";
    body.append(c, nm, more); a.appendChild(body);
    return a;
  }

  function init() {
    if (map || !window.maplibregl || !mapEl) return;
    map = new maplibregl.Map({
      container: mapEl, center: [19.8187, 41.3275], zoom: 12.6, attributionControl: { compact: true },
      cooperativeGestures: !explore,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    for (const p of data) {
      const el = document.createElement("button");
      el.type = "button"; el.className = "map-pin"; el.style.setProperty("--c", p.color);
      el.setAttribute("aria-label", p.name);
      const popup = new maplibregl.Popup({ offset: 22, closeButton: true, maxWidth: "260px" }).setDOMContent(popupContent(p));
      markers[p.slug] = new maplibregl.Marker({ element: el, anchor: "bottom" }).setLngLat([p.lon, p.lat]).setPopup(popup).addTo(map);
    }
    const all = data.map(p => p.slug);
    if (all.length > 1) map.fitBounds(new maplibregl.LngLatBounds(...bounds(all)), { padding: 50, maxZoom: 15, duration: 0 });
    else if (all.length === 1) map.jumpTo({ center: [data[0].lon, data[0].lat], zoom: 15 });
    apply();
  }
  function bounds(slugs) {
    let w = 180, s = 90, e = -180, n = -90;
    data.forEach(p => { if (slugs.includes(p.slug)) { w = Math.min(w, p.lon); e = Math.max(e, p.lon); s = Math.min(s, p.lat); n = Math.max(n, p.lat); } });
    return [[w, s], [e, n]];
  }

  // Zgjedhja nga lista: harta fluturon te vendi dhe hap kartën e tij
  box.querySelectorAll("[data-pm-focus]").forEach(btn => btn.addEventListener("click", () => {
    init();
    const m = markers[btn.dataset.pmFocus]; if (!m) return;
    box.querySelectorAll(".pm-item.is-active").forEach(x => x.classList.remove("is-active"));
    btn.classList.add("is-active");
    map.flyTo({ center: m.getLngLat(), zoom: 15.2, speed: 1.4 });
    Object.values(markers).forEach(x => { if (x.getPopup().isOpen()) x.togglePopup(); });
    m.togglePopup();
    if (window.matchMedia("(max-width: 900px)").matches) mapEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }));

  // Kartat e Eksplorimit: kalimi i miut thekson pikën në hartë
  box.querySelectorAll(".card[data-slug]").forEach(c => {
    c.addEventListener("mouseenter", () => { const m = markers[c.dataset.slug]; if (m) m.getElement().classList.add("is-active"); });
    c.addEventListener("mouseleave", () => { const m = markers[c.dataset.slug]; if (m) m.getElement().classList.remove("is-active"); });
  });

  // Butoni Harta / Lista në telefon (Eksploro)
  const tbtn = document.querySelector(".view-toggle"), wrap = document.getElementById("explore");
  if (tbtn && wrap) tbtn.addEventListener("click", () => {
    const show = !wrap.classList.contains("show-map");
    wrap.classList.toggle("show-map", show);
    tbtn.textContent = show ? tbtn.dataset.showList : tbtn.dataset.showMap;
    if (show) { init(); setTimeout(() => map && map.resize(), 50); }
  });

  // ---- "Afër meje": rendit kartat sipas largësisë nga personi ----
  const nearBtn = box.querySelector("[data-near]"), nearStatus = box.querySelector("[data-near-status]");
  const cardsEl = box.querySelector(".cards");
  if (nearBtn && cardsEl && "geolocation" in navigator) {
    const M = JSON.parse(nearBtn.dataset.msg);
    const original = [...cardsEl.children];
    const bySlug = Object.fromEntries(data.map(p => [p.slug, p]));
    let meMarker = null;
    const say = (txt) => { nearStatus.textContent = txt; nearStatus.hidden = !txt; };
    const metra = (a, b, c, d) => {          // Haversine, në metra
      const r = Math.PI / 180, x = Math.sin((c - a) * r / 2) ** 2 + Math.cos(a * r) * Math.cos(c * r) * Math.sin((d - b) * r / 2) ** 2;
      return 12742000 * Math.asin(Math.sqrt(x));
    };
    const fmt = m => m < 1000 ? `${Math.max(50, Math.round(m / 50) * 50)} m` : `${(m / 1000).toFixed(m < 10000 ? 1 : 0).replace(".", lang === "en" ? "." : ",")} km`;
    const setLabel = on => { nearBtn.setAttribute("aria-pressed", String(on)); nearBtn.querySelector("span").textContent = on ? M.reset : M.btn; };
    function reset() {
      original.forEach(c => { cardsEl.appendChild(c); c.querySelector(".card__dist")?.remove(); restoreBus(c); });
      if (meMarker) { meMarker.remove(); meMarker = null; }
      setLabel(false); say("");
    }
    function restoreBus(c) { const a = c.querySelector(".card__bus"); if (a && a.dataset.href0) a.href = a.dataset.href0; }
    nearBtn.addEventListener("click", () => {
      if (nearBtn.getAttribute("aria-pressed") === "true") return reset();
      nearBtn.disabled = true; say(M.loading);
      geoMeRiprovim(pos => {
        nearBtn.disabled = false;
        const lat = pos.coords.latitude, lon = pos.coords.longitude, acc = Math.round(pos.coords.accuracy);
        if (!(lat > 41.1 && lat < 41.6 && lon > 19.5 && lon < 20.1)) return say(M.far);
        const list = original.map(c => ({ c, d: bySlug[c.dataset.slug] ? metra(lat, lon, bySlug[c.dataset.slug].lat, bySlug[c.dataset.slug].lon) : Infinity }));
        list.sort((a, b) => a.d - b.d).forEach(({ c, d }) => {
          cardsEl.appendChild(c);
          let tag = c.querySelector(".card__dist");
          if (!tag) { tag = document.createElement("span"); tag.className = "card__dist"; c.querySelector(".card__loc").after(tag); }
          tag.textContent = M.away.replace("{d}", fmt(d));
          // "Shko me autobus" nis direkt nga vendndodhja jote, pa e kërkuar sërish te planifikuesi
          const a = c.querySelector(".card__bus");
          if (a) { a.dataset.href0 = a.dataset.href0 || a.getAttribute("href");
                   a.href = `${a.dataset.href0}&from=${lat.toFixed(5)},${lon.toFixed(5)}&fromname=${encodeURIComponent(M.me)}`; }
        });
        setLabel(true);
        say(acc > 300 ? M.rough.replace("{d}", fmt(acc)) : M.done);
        if (map) {
          const el = document.createElement("span"); el.className = "me-dot"; el.setAttribute("aria-label", M.me);
          if (meMarker) meMarker.remove();
          meMarker = new maplibregl.Marker({ element: el }).setLngLat([lon, lat]).addTo(map);
        }
      }, err => {
        nearBtn.disabled = false;
        say(err.code === 1 ? M.denied : M.fail);
      });
    });
  } else if (nearBtn) nearBtn.hidden = true;

  // Harta ngarkohet vetëm kur afrohet në ekran (kursen të dhëna)
  if (mapEl && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(e => { if (e[0].isIntersecting && mapEl.offsetParent !== null) { io.disconnect(); init(); } }, { rootMargin: "300px" });
    io.observe(mapEl);
  } else init();
  apply();
})();
