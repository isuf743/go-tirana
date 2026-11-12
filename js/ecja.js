/*
 * Ecja në këmbë përgjatë rrugëve (në shfletues)
 * ==============================================
 *
 * Lexon data/rruget_kembe.json (rrjeti i këmbësorëve, i krijuar nga 02_nderto_grafin.py)
 * dhe ofron tre gjëra:
 *
 *   1. pema(lat, lon, maksMetra): një Dijkstra nga pika ku klikoi përdoruesi. Me NJË kërkim
 *      merr distancën në këmbë deri te ÇDO nyje brenda rrezes, pra edhe te të gjitha stacionet
 *      përreth. Kjo është shumë më e shpejtë se një kërkim më vete për çdo stacion.
 *   2. metraDeri / rrugaNePeme: distanca dhe vija nga pika e klikuar deri te një stacion.
 *   3. aStar(a, b): rruga më e shkurtër mes dy pikave (për ndërrimet stacion -> stacion).
 *
 * STRUKTURA E TË DHËNAVE (CSR, "Compressed Sparse Row")
 *   Në vend të një liste fqinjësh për çdo nyje (që do të zinte shumë memorie për 137 mijë nyje),
 *   i mbajmë të gjitha brinjët në një varg të vetëm, të renditura sipas nyjes:
 *     fqinjet[fillimi[u] ... fillimi[u+1]]  =  fqinjët e nyjes u
 *   Kjo është mënyra si i ruajnë grafet e mëdha edhe bibliotekat profesionale.
 */

class RrjetiKembe {
  constructor(json) {
    const n = json.n, b = json.b;
    this.N = n.length / 2;
    this.lon = new Float64Array(this.N);
    this.lat = new Float64Array(this.N);
    for (let i = 0; i < this.N; i++) { this.lon[i] = n[2 * i] / 1e5; this.lat[i] = n[2 * i + 1] / 1e5; }

    // Shkalla (numri i fqinjëve) e çdo nyjeje -> pozicionet në vargun e përbashkët
    const shkalla = new Uint32Array(this.N);
    for (let e = 0; e < b.length; e += 2) { shkalla[b[e]]++; shkalla[b[e + 1]]++; }
    this.fillimi = new Uint32Array(this.N + 1);
    for (let i = 0; i < this.N; i++) this.fillimi[i + 1] = this.fillimi[i] + shkalla[i];
    this.fqinjet = new Int32Array(this.fillimi[this.N]);
    this.metrat = new Float32Array(this.fillimi[this.N]);
    const poz = this.fillimi.slice(0, this.N);
    for (let e = 0; e < b.length; e += 2) {
      const u = b[e], v = b[e + 1], d = this._metra(u, v);
      this.fqinjet[poz[u]] = v; this.metrat[poz[u]++] = d;
      this.fqinjet[poz[v]] = u; this.metrat[poz[v]++] = d;   // këmbësori ecën në të dy drejtimet
    }

    // Rrjetë katrore (~200 m) për të gjetur shpejt nyjen më të afërt me një pikë
    this.qeliza = 0.002;
    this.rrjeta = new Map();
    for (let i = 0; i < this.N; i++) {
      if (shkalla[i] === 0) continue;
      const k = this._celesi(this.lat[i], this.lon[i]);
      if (!this.rrjeta.has(k)) this.rrjeta.set(k, []);
      this.rrjeta.get(k).push(i);
    }
  }

  _celesi(lat, lon) { return Math.floor(lat / this.qeliza) * 100000 + Math.floor(lon / this.qeliza); }
  _metraPika(lat1, lon1, lat2, lon2) {
    const dy = (lat2 - lat1) * 110540, dx = (lon2 - lon1) * 111320 * Math.cos((lat1 + lat2) * Math.PI / 360);
    return Math.hypot(dx, dy);
  }
  _metra(u, v) { return this._metraPika(this.lat[u], this.lon[u], this.lat[v], this.lon[v]); }

  // Nyja më e afërt (brenda maks metrave): { nyja, metra } ose null
  afer(lat, lon, maks = 250) {
    const ki = Math.floor(lat / this.qeliza), kj = Math.floor(lon / this.qeliza);
    let me = -1, dm = maks;
    for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
      for (const i of this.rrjeta.get((ki + di) * 100000 + kj + dj) || []) {
        const d = this._metraPika(lat, lon, this.lat[i], this.lon[i]);
        if (d < dm) { dm = d; me = i; }
      }
    }
    return me < 0 ? null : { nyja: me, metra: dm };
  }

  // Dijkstra nga një pikë, deri në maksMetra. Kthen "pemën" e rrugëve më të shkurtra.
  pema(lat, lon, maksMetra) {
    const fillimi = this.afer(lat, lon);
    if (!fillimi) return null;
    const dist = new Float64Array(this.N).fill(Infinity);
    const prej = new Int32Array(this.N).fill(-1);
    const heap = new MinHeap();
    dist[fillimi.nyja] = fillimi.metra;          // nga pika e klikuar deri te rruga: vijë e drejtë
    heap.push(fillimi.metra, fillimi.nyja);
    while (heap.size) {
      const [d, u] = heap.pop();
      if (d > dist[u]) continue;
      if (d > maksMetra) break;                   // jashtë rrezes: s'na duhet më larg
      for (let k = this.fillimi[u]; k < this.fillimi[u + 1]; k++) {
        const v = this.fqinjet[k], nd = d + this.metrat[k];
        if (nd < dist[v]) { dist[v] = nd; prej[v] = u; heap.push(nd, v); }
      }
    }
    return { dist, prej, lat, lon };
  }

  // Distanca në këmbë nga burimi i pemës deri te një pikë (Infinity nëse s'arrihet)
  metraDeri(pema, lat, lon) {
    const s = this.afer(lat, lon);
    return s ? pema.dist[s.nyja] + s.metra : Infinity;
  }

  // Vija [[lon, lat], ...] nga burimi i pemës deri te pika
  rrugaNePeme(pema, lat, lon) {
    const s = this.afer(lat, lon);
    if (!s || !isFinite(pema.dist[s.nyja])) return null;
    const koord = [[lon, lat]];
    for (let v = s.nyja; v !== -1; v = pema.prej[v]) koord.push([this.lon[v], this.lat[v]]);
    koord.push([pema.lon, pema.lat]);
    return koord.reverse();
  }

  // A*: rruga më e shkurtër mes dy pikave (përdoret për ndërrimet stacion -> stacion)
  aStar(a, b) {
    const sa = this.afer(a.lat, a.lon), sb = this.afer(b.lat, b.lon);
    if (!sa || !sb) return null;
    const g = new Map([[sa.nyja, 0]]), prej = new Map();
    const h = u => this._metraPika(this.lat[u], this.lon[u], this.lat[sb.nyja], this.lon[sb.nyja]);
    const heap = new MinHeap();
    heap.push(h(sa.nyja), sa.nyja);
    let numri = 0;
    while (heap.size && numri++ < 80000) {
      const [, u] = heap.pop();
      if (u === sb.nyja) {
        const koord = [[b.lon, b.lat]];
        for (let v = u; v !== undefined; v = prej.get(v)) koord.push([this.lon[v], this.lat[v]]);
        koord.push([a.lon, a.lat]);
        return koord.reverse();
      }
      for (let k = this.fillimi[u]; k < this.fillimi[u + 1]; k++) {
        const v = this.fqinjet[k], ng = g.get(u) + this.metrat[k];
        if (ng < (g.get(v) ?? Infinity)) { g.set(v, ng); prej.set(v, u); heap.push(ng + h(v), v); }
      }
    }
    return null;
  }
}
