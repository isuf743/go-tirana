/* Go Tirana: harta e vogël në faqen e vendit (ngarkohet vetëm kur del në ekran) */
(function () {
  "use strict";
  const el = document.getElementById("mini-map");
  if (!el) return;
  function init() {
    if (!window.maplibregl) return;
    const lon = parseFloat(el.dataset.lon), lat = parseFloat(el.dataset.lat);
    const map = new maplibregl.Map({
      container: el, style: "https://tiles.openfreemap.org/styles/positron",
      center: [lon, lat], zoom: 15.2, attributionControl: { compact: true }, cooperativeGestures: true,
    });
    const pin = document.createElement("div");
    pin.className = "map-pin"; pin.style.setProperty("--c", el.dataset.color);
    new maplibregl.Marker({ element: pin, anchor: "bottom" }).setLngLat([lon, lat]).addTo(map);
  }
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(e => { if (e[0].isIntersecting) { io.disconnect(); window.maplibregl ? init() : window.addEventListener("load", init); } }, { rootMargin: "200px" });
    io.observe(el);
  } else window.addEventListener("load", init);
})();
