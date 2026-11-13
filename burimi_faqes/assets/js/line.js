/* Go Tirana: harta e një linje autobusi (rruga në të dy drejtimet dhe stacionet me emër). */
(function () {
  "use strict";
  const el = document.getElementById("line-map"), dataEl = document.getElementById("line-data");
  if (!el || !dataEl) return;
  const D = JSON.parse(dataEl.textContent);

  function init() {
    if (!window.maplibregl) return;
    const b = new maplibregl.LngLatBounds();
    D.dirs.forEach(d => d.forEach(c => b.extend(c)));
    const map = new maplibregl.Map({ container: el, bounds: b, fitBoundsOptions: { padding: 40, maxZoom: 16 },
      attributionControl: { compact: true }, cooperativeGestures: true });
    map.on("load", () => {
      map.fitBounds(b, { padding: 40, maxZoom: 16, animate: false });
      map.addSource("linja", { type: "geojson", data: { type: "FeatureCollection",
        features: D.dirs.map(d => ({ type: "Feature", properties: {}, geometry: { type: "LineString", coordinates: d } })) } });
      map.addLayer({ id: "linja", type: "line", source: "linja", paint: { "line-color": D.color, "line-width": 4, "line-opacity": .9 } });
    });
    D.stops.forEach(s => {
      const dot = document.createElement("span");
      dot.className = "line-stop"; dot.style.setProperty("--lc", D.color);
      dot.title = s.name; dot.setAttribute("role", "img"); dot.setAttribute("aria-label", s.name);
      new maplibregl.Marker({ element: dot }).setLngLat([s.lon, s.lat]).addTo(map);
    });
  }
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(e => {
      if (e[0].isIntersecting) { io.disconnect(); window.maplibregl ? init() : window.addEventListener("load", init); }
    }, { rootMargin: "200px" });
    io.observe(el);
  } else window.addEventListener("load", init);
})();
