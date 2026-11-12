/* Go Tirana: formulari i kontaktit
   Validim në shfletues (për përvojën e përdoruesit) + validim në server (për sigurinë).
   Mbrojtja nga spam-i: fushë e fshehur, token i nënshkruar me kohë, kufi mesazhesh në server. */
(function () {
  "use strict";
  const form = document.getElementById("contact-form");
  if (!form) return;
  const msg = JSON.parse(form.dataset.msg);
  const status = document.getElementById("form-status");
  const btn = form.querySelector('button[type="submit"]');
  const api = form.getAttribute("action");

  // Token-i nga serveri: provon që formulari u hap të paktën disa sekonda para dërgimit
  fetch(api + "?token=1", { credentials: "same-origin" })
    .then(r => r.ok ? r.json() : null)
    .then(j => { if (j && j.token) form.token.value = j.token; })
    .catch(() => {});

  const emailOk = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  function check(field) {
    const v = field.type === "checkbox" ? field.checked : field.value.trim();
    let e = "";
    if (field.name === "name" && !v) e = msg.required;
    if (field.name === "email") e = !v ? msg.required : (!emailOk(v) ? msg.email : "");
    if (field.name === "message") e = !v ? msg.required : v.length < 10 ? msg.short : v.length > 2000 ? msg.long : "";
    if (field.name === "consent" && !v) e = msg.consent;
    const out = document.getElementById("e-" + field.name);
    if (out) out.textContent = e;
    field.setAttribute("aria-invalid", e ? "true" : "false");
    return !e;
  }
  const fields = ["name", "email", "message", "consent"].map(n => form.elements[n]);
  fields.forEach(f => f.addEventListener(f.type === "checkbox" ? "change" : "blur", () => check(f)));

  function show(text, ok) {
    status.hidden = false;
    status.className = "form-status " + (ok ? "form-status--ok" : "form-status--err");
    status.textContent = text;
  }

  form.addEventListener("submit", async ev => {
    ev.preventDefault();
    const results = fields.map(check);
    if (results.includes(false)) {
      fields[results.indexOf(false)].focus();
      return;
    }
    btn.disabled = true; const label = btn.textContent; btn.textContent = msg.sending;
    try {
      const r = await fetch(api, { method: "POST", body: new FormData(form), credentials: "same-origin" });
      const j = await r.json().catch(() => ({}));
      if (r.ok && j.ok) { form.reset(); show(msg.ok, true); }
      else show(r.status === 429 ? msg.rate : msg.server, false);
    } catch (e) {
      show(msg.server, false);
    } finally {
      btn.disabled = false; btn.textContent = label;
    }
  });
})();
