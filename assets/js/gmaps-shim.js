/* GO TIRANA: hartat me Google Maps.
   Ky skedar krijon një përshtatës të vogël me emrin "maplibregl" mbi Google Maps, që skriptet
   (place.js, placesmap.js, itinerary.js) të punojnë pa ndryshime. Google ngarkohet vetëm
   kur harta e parë del në ekran. Çelësi vjen nga <script data-key="..."> (konfigurimi.json).
   Planifikuesi i autobusëve ka kodin e vet për Google Maps (planner/index.html). */
(function () {
  "use strict";
  const me = document.currentScript;
  const KEY = me && me.dataset.key;
  const LANG = document.documentElement.lang || "en";
  let loading = null;

  function loadGoogle() {
    if (loading) return loading;
    loading = new Promise((resolve, reject) => {
      if (window.google && google.maps && google.maps.Map) return resolve();
      window.__gtGmReady = () => resolve();
      const s = document.createElement("script");
      s.src = "https://maps.googleapis.com/maps/api/js?key=" + encodeURIComponent(KEY) +
        "&v=weekly&loading=async&callback=__gtGmReady&language=" + LANG + "&region=AL";
      s.async = true; s.onerror = reject;
      document.head.appendChild(s);
    });
    return loading;
  }

  // MapLibre ka pllaka 512px, Google 256px: i njëjti pamje del me +1 zoom te Google
  const gz = z => Math.round(z + 1);
  const ll = c => Array.isArray(c) ? { lat: c[1], lng: c[0] } : { lat: c.lat, lng: c.lng != null ? c.lng : c.lon };

  // Pamje e çelët e qetë, afër stilit të hartave të tjera të faqes
  const STYLE = [
    { featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] },
    { featureType: "poi.park", elementType: "geometry", stylers: [{ color: "#dfe9d8" }] },
    { featureType: "poi.business", stylers: [{ visibility: "off" }] },
    { featureType: "transit", elementType: "labels.icon", stylers: [{ visibility: "off" }] },
    { featureType: "road", elementType: "geometry", stylers: [{ color: "#ffffff" }] },
    { featureType: "road.arterial", elementType: "labels.icon", stylers: [{ visibility: "off" }] },
    { featureType: "landscape", elementType: "geometry", stylers: [{ color: "#f3f1ec" }] },
    { featureType: "water", elementType: "geometry", stylers: [{ color: "#cfe0ea" }] },
    { elementType: "labels.text.fill", stylers: [{ color: "#5f6670" }] },
  ];

  class LngLatBounds {
    constructor(sw, ne) { this.w = 180; this.s = 90; this.e = -180; this.n = -90; if (sw) this.extend(sw); if (ne) this.extend(ne); }
    extend(c) { const p = ll(c); this.w = Math.min(this.w, p.lng); this.e = Math.max(this.e, p.lng); this.s = Math.min(this.s, p.lat); this.n = Math.max(this.n, p.lat); return this; }
    getCenter() { return { lng: (this.w + this.e) / 2, lat: (this.s + this.n) / 2 }; }
    _g() { return new google.maps.LatLngBounds({ lat: this.s, lng: this.w }, { lat: this.n, lng: this.e }); }
  }

  class Map {
    constructor(o) {
      this._o = o; this._src = {}; this._loadFns = []; this._loaded = false;
      this._ready = loadGoogle().then(() => {
        const g = this.g = new google.maps.Map(o.container, {
          center: ll(o.center || [19.8187, 41.3275]), zoom: gz(o.zoom != null ? o.zoom : 13),
          styles: STYLE, clickableIcons: false, mapTypeControl: false, streetViewControl: false,
          fullscreenControl: false, rotateControl: false, keyboardShortcuts: false,
          gestureHandling: o.cooperativeGestures ? "cooperative" : "greedy",
        });
        if (o.bounds) this.fitBounds(o.bounds, Object.assign({ animate: false }, o.fitBoundsOptions));
        google.maps.event.addListenerOnce(g, "idle", () => { this._loaded = true; this._loadFns.forEach(f => f()); });
        return g;
      });
    }
    _when(f) { return this._ready.then(f); }
    on(ev, fn) { if (ev === "load") { this._loaded ? fn() : this._loadFns.push(fn); } return this; }
    addControl() { return this; }
    resize() { this._when(g => google.maps.event.trigger(g, "resize")); return this; }
    jumpTo(o) { this._when(g => { if (o.center) g.setCenter(ll(o.center)); if (o.zoom != null) g.setZoom(gz(o.zoom)); }); return this; }
    easeTo(o) { this._when(g => { if (o.zoom != null) g.setZoom(gz(o.zoom)); if (o.center) g.panTo(ll(o.center)); }); return this; }
    flyTo(o) { return this.easeTo(o); }
    fitBounds(b, o) {
      o = o || {};
      this._when(g => {
        const bb = Array.isArray(b) ? new LngLatBounds(b[0], b[1]) : b;
        g.fitBounds(bb._g(), o.padding != null ? o.padding : 40);
        if (o.maxZoom != null) google.maps.event.addListenerOnce(g, "idle", () => { if (g.getZoom() > gz(o.maxZoom)) g.setZoom(gz(o.maxZoom)); });
      });
      return this;
    }
    addSource(id, s) { this._src[id] = s.data; return this; }
    addLayer(l) {
      // Vetëm vija (rruga e itinerarit): filtri ["==", ["get", "fusha"], "vlera"]
      this._when(g => {
        const data = this._src[l.source]; if (!data || l.type !== "line") return;
        const f = l.filter, p = l.paint || {};
        const w = p["line-width"] || 3, col = p["line-color"] || "#171c22";
        (data.features || []).forEach(ft => {
          if (f && f[0] === "==" && ft.properties[f[1][1]] !== f[2]) return;
          const path = ft.geometry.coordinates.map(ll);
          const opts = { map: g, path, strokeColor: col, strokeWeight: w, strokeOpacity: p["line-opacity"] != null ? p["line-opacity"] : 1, clickable: false };
          if (p["line-dasharray"]) {
            opts.strokeOpacity = 0;
            opts.icons = [{ icon: { path: google.maps.SymbolPath.CIRCLE, fillColor: col, fillOpacity: 1, strokeOpacity: 0, scale: w / 1.6 }, offset: "0", repeat: (w * 3) + "px" }];
          }
          new google.maps.Polyline(opts);
        });
      });
      return this;
    }
  }

  class Popup {
    constructor(o) { this._o = o || {}; this._open = false; this._node = null; }
    setDOMContent(n) { this._node = n; return this; }
    isOpen() { return this._open; }
    _show(map, pos) {
      if (!this._iw) {
        this._iw = new google.maps.InfoWindow({ content: this._node, maxWidth: parseInt(this._o.maxWidth, 10) || 260,
          pixelOffset: new google.maps.Size(0, -((this._o.offset || 0) + 8)) });
        this._iw.addListener("closeclick", () => { this._open = false; });
      }
      this._iw.setPosition(pos); this._iw.open({ map }); this._open = true;
    }
    _hide() { if (this._iw) this._iw.close(); this._open = false; }
  }

  let HtmlOverlay = null;
  function overlayClass() {
    if (HtmlOverlay) return HtmlOverlay;
    HtmlOverlay = class extends google.maps.OverlayView {
      constructor(m) { super(); this.m = m; }
      onAdd() {
        const w = this.wrap = document.createElement("div");
        w.style.position = "absolute"; w.style.transform = this.m._anchor === "bottom" ? "translate(-50%,-100%)" : "translate(-50%,-50%)";
        w.appendChild(this.m._el);
        google.maps.OverlayView.preventMapHitsAndGesturesFrom(w);
        this.getPanes().overlayMouseTarget.appendChild(w);
      }
      draw() {
        const pr = this.getProjection(); if (!pr || !this.wrap) return;
        const pt = pr.fromLatLngToDivPixel(new google.maps.LatLng(this.m._pos.lat, this.m._pos.lng));
        if (pt) { this.wrap.style.left = pt.x + "px"; this.wrap.style.top = pt.y + "px"; }
      }
      onRemove() { if (this.wrap) this.wrap.remove(); this.wrap = null; }
    };
    return HtmlOverlay;
  }

  class Marker {
    constructor(o) {
      o = o || {};
      this._el = o.element || document.createElement("div");
      this._anchor = o.anchor || "center"; this._pos = { lat: 0, lng: 0 }; this._popup = null;
      this._el.addEventListener("click", () => { if (this._popup) this.togglePopup(); });
    }
    setLngLat(c) { this._pos = ll(c); if (this._ov) this._ov.draw(); return this; }
    getLngLat() { return { lng: this._pos.lng, lat: this._pos.lat }; }
    getElement() { return this._el; }
    setPopup(p) { this._popup = p; return this; }
    getPopup() { return this._popup; }
    addTo(map) {
      this._map = map;
      map._when(g => { const C = overlayClass(); this._ov = new C(this); this._ov.setMap(g); });
      return this;
    }
    togglePopup() {
      const p = this._popup; if (!p || !this._map) return this;
      this._map._when(g => { p.isOpen() ? p._hide() : p._show(g, this._pos); });
      return this;
    }
    remove() { if (this._ov) this._ov.setMap(null); if (this._popup) this._popup._hide(); return this; }
  }

  window.maplibregl = { Map, Marker, Popup, LngLatBounds, NavigationControl: function () {} };
})();
