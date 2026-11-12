/* Go Tirana: harta e faqes Eksploro (pikat sipas kategorisë, lidhje me kartat) */
(function () {
  "use strict";
  const el = document.getElementById("map");
  const data = JSON.parse(document.getElementById("places-data").textContent);
  const root = document.body.dataset.root, lang = document.body.dataset.lang;
  const wrap = document.getElementById("explore");

  // Butoni Harta / Lista në telefon
  const tbtn = document.querySelector(".view-toggle");
  let map = null;
  if (tbtn) tbtn.addEventListener("click", () => {
    const show = !wrap.classList.contains("show-map");
    wrap.classList.toggle("show-map", show);
    tbtn.textContent = show ? tbtn.dataset.showList : tbtn.dataset.showMap;
    if (show) { if (!map) initMap(); else map.resize(); }
  });

  // Harta ngarkohet kur bëhet e dukshme (kursen të dhëna në telefon)
  function whenVisible(cb) {
    if (el.offsetParent !== null) return cb();
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(e => { if (e[0].isIntersecting) { io.disconnect(); cb(); } });
      io.observe(el);
    }
  }
  window.addEventListener("load", () => whenVisible(() => { if (!map) initMap(); }));

  function initMap() {
    if (!window.maplibregl) return;
    map = new maplibregl.Map({
      container: el, style: "https://tiles.openfreemap.org/styles/positron",
      center: [19.8187, 41.3275], zoom: 12.6, attributionControl: { compact: true },
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    const bounds = new maplibregl.LngLatBounds();
    const markers = {};
    for (const p of data) {
      const m = document.createElement("button");
      m.type = "button"; m.className = "map-pin"; m.style.setProperty("--c", p.color);
      m.setAttribute("aria-label", p.name);
      const popup = new maplibregl.Popup({ offset: 18, closeButton: false })
        .setHTML(`<a href="${root}${lang}/places/${p.slug}/">${p.name}</a>`);
      markers[p.slug] = new maplibregl.Marker({ element: m, anchor: "bottom" }).setLngLat([p.lon, p.lat]).setPopup(popup).addTo(map);
      bounds.extend([p.lon, p.lat]);
    }
    if (data.length > 1) map.fitBounds(bounds, { padding: 50, maxZoom: 15, duration: 0 });
    else if (data.length === 1) map.jumpTo({ center: [data[0].lon, data[0].lat], zoom: 15 });

    // Kur kalon miun mbi një kartë, thekso pikën në hartë
    document.querySelectorAll(".card[data-slug]").forEach(c => {
      const mk = markers[c.dataset.slug]; if (!mk) return;
      c.addEventListener("mouseenter", () => mk.getElement().classList.add("is-active"));
      c.addEventListener("mouseleave", () => mk.getElement().classList.remove("is-active"));
    });
  }
})();
