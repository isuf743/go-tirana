/* Go Tirana: harta e itinerarit me ndalesat e numëruara dhe rrugën mes tyre.
   Ecja vizatohet me vijë të ndërprerë, autobusi me vijë të plotë. Kliko një numër për të shkuar te ndalesa. */
(function () {
  "use strict";
  const el = document.getElementById("itin-map");
  const dataEl = document.getElementById("itin-data");
  if (!el || !dataEl) return;
  const D = JSON.parse(dataEl.textContent);

  function init() {
    if (!window.maplibregl) return;
    const pikat = (D.start ? [D.start] : []).concat(D.stops);
    const kufijte = new maplibregl.LngLatBounds();
    pikat.forEach(p => kufijte.extend([p.lon, p.lat]));
    const map = new maplibregl.Map({
      container: el, style: "https://tiles.openfreemap.org/styles/positron",
      bounds: kufijte, fitBoundsOptions: { padding: 50, maxZoom: 16 },
      attributionControl: { compact: true }, cooperativeGestures: true,
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");

    map.on("load", () => {
      map.resize(); map.fitBounds(kufijte, { padding: 50, maxZoom: 16, animate: false });
      const features = [];
      for (let i = 0; i < pikat.length - 1; i++) {
        features.push({ type: "Feature", properties: { t: D.legs[i] || "walk" },
          geometry: { type: "LineString", coordinates: [[pikat[i].lon, pikat[i].lat], [pikat[i + 1].lon, pikat[i + 1].lat]] } });
      }
      map.addSource("rruga", { type: "geojson", data: { type: "FeatureCollection", features } });
      map.addLayer({ id: "ecja", type: "line", source: "rruga", filter: ["==", ["get", "t"], "walk"],
        layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": "#171c22", "line-width": 3, "line-dasharray": [0.1, 2] } });
      map.addLayer({ id: "autobusi", type: "line", source: "rruga", filter: ["==", ["get", "t"], "bus"],
        layout: { "line-cap": "round" }, paint: { "line-color": "#d31332", "line-width": 3.5, "line-opacity": .85 } });
    });

    if (D.start) {
      const s = document.createElement("div");
      s.className = "it-pin it-pin--start"; s.title = D.start.name;
      new maplibregl.Marker({ element: s }).setLngLat([D.start.lon, D.start.lat]).addTo(map);
      s.setAttribute("role", "img"); s.setAttribute("aria-label", D.start.name);
    }
    D.stops.forEach(p => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "it-pin"; b.textContent = p.n;
      b.setAttribute("aria-label", p.n + ". " + p.name); b.title = p.name;
      b.addEventListener("click", () => {
        const li = document.getElementById("stop-" + p.n);
        if (li) li.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
      });
      new maplibregl.Marker({ element: b }).setLngLat([p.lon, p.lat]).addTo(map);
    });
  }

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(e => {
      if (e[0].isIntersecting) { io.disconnect(); window.maplibregl ? init() : window.addEventListener("load", init); }
    }, { rootMargin: "200px" });
    io.observe(el);
  } else window.addEventListener("load", init);
})();
