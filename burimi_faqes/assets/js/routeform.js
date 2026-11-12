/* GO TIRANA: formulari "Planifiko një udhëtim" në faqen kryesore
   Zgjedh nisjen (një vend ose vendndodhjen tënde) dhe destinacionin, pastaj hap planifikuesin
   me të dyja pikat (?from=lat,lon&to=lat,lon), ku llogaritet rruga e vërtetë. */
(function () {
  "use strict";
  const form = document.getElementById("route-form");
  if (!form) return;
  const M = JSON.parse(form.dataset.msg);
  const from = document.getElementById("rf-from"), to = document.getElementById("rf-to");
  const geo = document.getElementById("rf-geo"), msg = document.getElementById("rf-msg");
  let geoLL = null;
  const inTirana = (lat, lon) => lat > 41.1 && lat < 41.6 && lon > 19.5 && lon < 20.1;   // kufijtë që pranon planifikuesi

  function say(text, info) { msg.textContent = text || ""; msg.classList.toggle("form-msg--info", !!info); }

  function locate() {
    if (!navigator.geolocation) { from.value = ""; say(M.loc_unavailable); return; }
    geo.setAttribute("aria-busy", "true"); say(M.locating, true);
    navigator.geolocation.getCurrentPosition(pos => {
      geo.removeAttribute("aria-busy");
      const { latitude: lat, longitude: lon } = pos.coords;
      if (!inTirana(lat, lon)) { geoLL = null; from.value = ""; say(M.loc_outside); return; }
      geoLL = `${lat.toFixed(5)},${lon.toFixed(5)}`;
      from.value = "geo"; say("");
    }, err => {
      geo.removeAttribute("aria-busy");
      geoLL = null; from.value = "";
      say(err.code === 1 ? M.loc_denied : M.loc_unavailable);
    }, { enableHighAccuracy: true, timeout: 12000, maximumAge: 60000 });
  }

  geo.addEventListener("click", locate);
  from.addEventListener("change", () => { say(""); if (from.value === "geo" && !geoLL) locate(); });
  to.addEventListener("change", () => say(""));

  document.getElementById("rf-swap").addEventListener("click", () => {
    const a = from.value, b = to.value;
    from.value = b || "";
    to.value = a === "geo" ? "" : a;   // "vendndodhja ime" mund të jetë vetëm nisje
    say("");
  });

  const ll = sel => sel.selectedOptions[0] && sel.selectedOptions[0].dataset.ll;
  const name = sel => sel.selectedOptions[0] ? sel.selectedOptions[0].textContent.trim() : "";

  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!to.value) { say(M.form_err_to); to.focus(); return; }
    if (from.value && from.value === to.value) { say(M.form_err_same); from.focus(); return; }
    const p = new URLSearchParams({ lang: form.elements.lang.value, to: ll(to), name: name(to) });
    if (from.value === "geo" && geoLL) { p.set("from", geoLL); p.set("fromname", M.my_location); }
    else if (from.value && from.value !== "geo") { p.set("from", ll(from)); p.set("fromname", name(from)); }
    window.location.href = form.getAttribute("action") + "?" + p.toString();
  });
})();
