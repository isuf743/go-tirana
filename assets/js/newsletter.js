/* GO TIRANA: lista e emaileve
   Validim në shfletues + në server; mbrojtje nga spam-i si te formulari i kontaktit
   (fushë e fshehur, token me kohë, kufi në orë). Mesazhi i suksesit shfaqet VETËM kur serveri e ruan emailin. */
(function () {
  "use strict";
  const form = document.getElementById("nl-form");
  if (!form) return;
  const M = JSON.parse(form.dataset.msg);
  const email = form.elements.email, consent = form.elements.consent;
  const status = document.getElementById("nl-status");
  const btn = form.querySelector('button[type="submit"]');
  const api = form.getAttribute("action");
  let tokenLoaded = false;

  function loadToken() {
    if (tokenLoaded) return; tokenLoaded = true;
    fetch(api + "?token=1", { credentials: "same-origin" })
      .then(r => r.ok ? r.json() : null).then(j => { if (j && j.token) form.elements.token.value = j.token; })
      .catch(() => { tokenLoaded = false; });
  }
  // token-i merret kur vizitori afrohet te formulari (kontrolli i kohës në server kërkon disa sekonda)
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(e => { if (e[0].isIntersecting) { io.disconnect(); loadToken(); } }, { rootMargin: "400px" });
    io.observe(form);
  } else loadToken();
  email.addEventListener("focus", loadToken);

  const show = (text, ok) => { status.textContent = text; status.className = "nl-status " + (ok ? "nl-status--ok" : "nl-status--err"); };
  const valid = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const v = email.value.trim();
    email.setAttribute("aria-invalid", valid(v) ? "false" : "true");
    if (!valid(v)) { show(M.nl_err_email, false); email.focus(); return; }
    if (!consent.checked) { show(M.nl_err_consent, false); consent.focus(); return; }
    btn.disabled = true; const label = btn.textContent; btn.textContent = M.nl_sending;
    try {
      const r = await fetch(api, { method: "POST", body: new FormData(form), credentials: "same-origin" });
      const j = await r.json().catch(() => ({}));
      if (r.ok && j.ok) { form.reset(); show(M.nl_ok, true); }
      else if (r.status === 429) show(M.nl_err_rate, false);
      else if (j.error === "validation" && (j.fields || []).includes("email")) show(M.nl_err_email, false);
      else show(M.nl_err_server, false);
    } catch (err) {
      show(M.nl_err_server, false);
    } finally {
      btn.disabled = false; btn.textContent = label;
    }
  });
})();
