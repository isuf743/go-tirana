/*
 * HAPI 3b: Gjetja e rrugës më të shpejtë me algoritmin Dijkstra
 * ===============================================================
 *
 * IDEJA E DIJKSTRËS
 *   Fillojmë nga pika e nisjes me kosto 0. Në çdo hap marrim nyjen me koston më të
 *   vogël që s'e kemi përpunuar ende, dhe "relaksojmë" fqinjët e saj: nëse duke kaluar
 *   nga kjo nyje arrijmë te një fqinj më shpejt se ç'e njihnim deri tani, e përditësojmë.
 *   Kur nxjerrim destinacionin nga radha, kemi gjetur rrugën më të shpejtë.
 *   Për ta gjetur shpejt nyjen me koston më të vogël përdorim një "heap" (radhë me përparësi).
 *
 * PSE NUK MJAFTON GRAFI I THJESHTË "STACION -> STACION"
 *   Nëse nyjet do të ishin vetëm stacionet, algoritmi s'do ta dinte nëse je ende brenda
 *   autobusit apo ke zbritur, dhe s'do të llogariste dot kohën e pritjes kur ndërron linjë.
 *   Prandaj nyjet tona janë GJENDJE:
 *
 *     KËMBË(s)      = jam në stacionin s, në këmbë (kam zbritur ose sapo kam ardhur)
 *     BORD(L, k)    = jam brenda autobusit të linjës L, te stacioni i k-të i saj
 *     NISJA, FUNDI  = pikat që klikon përdoruesi në hartë
 *
 *   Brinjët (kalimet e mundshme mes gjendjeve):
 *     NISJA     -> KËMBË(s)      ec deri te stacionet afër (deri në 800 m)
 *     NISJA     -> FUNDI         ec direkt, nëse destinacioni është afër
 *     KËMBË(s)  -> KËMBË(t)      ec te një stacion afër (brinjët "ecjet" të grafit)
 *     KËMBË(s)  -> BORD(L, k)    hip në autobus: kosto = koha mesatare e pritjes
 *     BORD(L,k) -> BORD(L, k+1)  udhëto një stacion: kosto = koha nga grafi
 *     BORD(L,k) -> KËMBË(s)      zbrit: kosto 0
 *     KËMBË(s)  -> FUNDI         ec nga stacioni te destinacioni
 *
 *   Kështu çdo ndërrim linje kushton automatikisht një pritje të re, dhe algoritmi
 *   preferon natyrshëm rrugët me më pak ndërrime.
 *
 * PRITJA SIPAS FREKUENCËS
 *   Nëse një autobus vjen çdo 20 minuta dhe ti mbërrin në stacion në një moment të rastësishëm,
 *   mesatarisht pret gjysmën e intervalit: 10 minuta. Prandaj pritja = intervali / 2,
 *   dhe linjat e rralla (p.sh. Vora, çdo 30 min) "kushtojnë" më shumë.
 *
 * LINJAT PARALELE ("merr cilëndo që vjen e para")
 *   Nëse dy linja shkojnë nga i njëjti stacion te i njëjti destinacion, nuk ke pse pret
 *   një linjë të caktuar. Me disa linja bashkë, autobusët vijnë më shpesh:
 *     frekuenca totale = 1/intervali1 + 1/intervali2 + ...
 *     pritja mesatare  = 1 / (2 * frekuenca totale)
 *   P.sh. dy linja çdo 15 min = një autobus çdo 7.5 min, pra pritje ~4 min në vend të ~8.
 *
 * DISA OPSIONE
 *   Pasi gjejmë rrugën më të mirë, "ndalojmë" linjat që përdori dhe kërkojmë përsëri.
 *   Kështu marrim alternativa me linja të tjera (teknikë e thjeshtë e njohur si "penalizim").
 */

const PARAMETRAT = {
  intervaliParazgjedhurMin: 15,   // nëse një linjë s'ka interval në grafi.json
  ngjitur: 80,             // dy stacione brenda 80 m konsiderohen "i njëjti vend" për linjat paralele
  maksEcjeFillimM: 800,    // sa larg pranojmë të ecim nga pika e klikuar te stacioni
  rrezjaPemesM: 3500,      // deri ku kërkon Dijkstra në këmbë nga pika e klikuar (edhe për ecjen direkte)
  shpejtesiaEcjesKmh: 4.8,
  faktoriRrugesEcje: 1.3,  // ecja s'është vijë e drejtë

  // ---- Parametrat e kalibrimit (i gjen automatikisht skeda "Kalibrimi") ----
  // grafi.json i ka kohët e llogaritura me 15 km/h. Nëse autobusët në realitet ecin me v km/h,
  // çdo kohë udhëtimi shumëzohet me 15 / v. P.sh. v = 12 km/h -> kohët zgjaten 25%.
  shpejtesiaBazeKmh: 15,
  shpejtesiaAutobusitKmh: 15,
  // Shumëzuesi i pritjes: 1 = pritja është saktësisht gjysma e intervalit.
  // Nëse autobusët vonohen më shumë se orari, kalibrimi do ta rrisë mbi 1.
  faktoriPritjes: 1,
};

const faktoriShpejtesise = () => PARAMETRAT.shpejtesiaBazeKmh / PARAMETRAT.shpejtesiaAutobusitKmh;

function distancaM(lat1, lon1, lat2, lon2) {          // formula Haversine
  const R = 6371000, rad = Math.PI / 180;
  const dp = (lat2 - lat1) * rad, dl = (lon2 - lon1) * rad;
  const a = Math.sin(dp / 2) ** 2 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dl / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

const pritjaSek = linja =>
  (linja.intervali_min || PARAMETRAT.intervaliParazgjedhurMin) * 60 / 2 * PARAMETRAT.faktoriPritjes;

function kohaEcjes(metra) {         // metra në vijë të drejtë -> sekonda (me faktorin e rrugës)
  return metra * PARAMETRAT.faktoriRrugesEcje / (PARAMETRAT.shpejtesiaEcjesKmh / 3.6);
}
const kohaEcjesReale = metra => metra / (PARAMETRAT.shpejtesiaEcjesKmh / 3.6);   // metra në rrugë

// ---------------------------------------------------------------------------
// Rrjeti i këmbësorëve (js/ecja.js). Nëse është ngarkuar, ecja llogaritet përgjatë rrugëve.
// Pemët e Dijkstrës nga pikat e klikuara i ruajmë në memorie, sepse gjejOpsionet dhe
// kalibrimi e thërrasin gjejRrugen shumë herë me të njëjtat pika.
// ---------------------------------------------------------------------------
let RRJETI_KEMBE = null;
const _pemet = new Map();
function pemaKembe(p) {
  if (!RRJETI_KEMBE) return null;
  const celesi = p.lat.toFixed(6) + "," + p.lon.toFixed(6);
  if (!_pemet.has(celesi)) {
    if (_pemet.size > 40) _pemet.delete(_pemet.keys().next().value);
    _pemet.set(celesi, RRJETI_KEMBE.pema(p.lat, p.lon, PARAMETRAT.rrezjaPemesM));
  }
  return _pemet.get(celesi);
}

// ---------------------------------------------------------------------------
// Radha me përparësi (min-heap): nxjerr gjithmonë elementin me koston më të vogël.
// Shtimi dhe nxjerrja janë O(log n), në vend të O(n) që do të kishte një listë e thjeshtë.
// ---------------------------------------------------------------------------
class MinHeap {
  constructor() { this.a = []; }
  get size() { return this.a.length; }
  push(kosto, nyja) {
    const a = this.a; a.push([kosto, nyja]);
    let i = a.length - 1;
    while (i > 0) {                                   // ngjite lart sa kohë prindi është më i madh
      const p = (i - 1) >> 1;
      if (a[p][0] <= a[i][0]) break;
      [a[p], a[i]] = [a[i], a[p]]; i = p;
    }
  }
  pop() {
    const a = this.a, top = a[0], last = a.pop();
    if (a.length) {
      a[0] = last;
      let i = 0;
      for (;;) {                                      // zbrite poshtë te fëmija më i vogël
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && a[l][0] < a[m][0]) m = l;
        if (r < a.length && a[r][0] < a[m][0]) m = r;
        if (m === i) break;
        [a[m], a[i]] = [a[i], a[m]]; i = m;
      }
    }
    return top;
  }
}

// ---------------------------------------------------------------------------
// Përgatitja e grafit (bëhet një herë, kur ngarkohet faqja)
// ---------------------------------------------------------------------------
function pergatitGrafin(grafi) {
  const N = grafi.stacionet.length;

  // Numërojmë gjendjet BORD: çdo linjë merr një bllok numrash pas stacioneve
  const fillimiBord = [];
  let id = N;
  for (const l of grafi.linjat) { fillimiBord.push(id); id += l.stacionet.length; }
  const NISJA = id, FUNDI = id + 1, GJITHSEJ = id + 2;

  // Për çdo stacion: ku mund të hipësh (cila linjë, cili pozicion)
  const hipjet = Array.from({ length: N }, () => []);
  grafi.linjat.forEach((l, li) => l.stacionet.forEach((s, k) => {
    if (k < l.stacionet.length - 1) hipjet[s].push([li, k]);   // te stacioni i fundit s'ka ku të shkosh
  }));

  // Lista e fqinjëve në këmbë (brinjët vlejnë në të dy drejtimet)
  const ecjet = Array.from({ length: N }, () => []);
  for (const [i, j, sek] of grafi.ecjet) { ecjet[i].push([j, sek]); ecjet[j].push([i, sek]); }

  return { ...grafi, N, fillimiBord, NISJA, FUNDI, GJITHSEJ, hipjet, ecjetAdj: ecjet };
}

// Nga numri i gjendjes, nxjerrim [linja, pozicioni] (për gjendjet BORD)
function deshifroBord(g, nyja) {
  let li = g.fillimiBord.length - 1;
  while (g.fillimiBord[li] > nyja) li--;
  return [li, nyja - g.fillimiBord[li]];
}

// ---------------------------------------------------------------------------
// Dijkstra
// ---------------------------------------------------------------------------
// ndaluara: Set me indekset e linjave që s'lejohen (për të gjetur alternativa)
function gjejRrugen(g, nga, per, ndaluara = new Set()) {
  const { N, NISJA, FUNDI, GJITHSEJ } = g;
  const fs = faktoriShpejtesise();
  const kosto = new Float64Array(GJITHSEJ).fill(Infinity);
  const ngaKu = new Int32Array(GJITHSEJ).fill(-1);    // për të rindërtuar rrugën në fund
  const heap = new MinHeap();
  let perpunuara = 0;

  // Distanca nga pikat e klikuara te stacionet (llogaritet një herë).
  // Me rrjetin e këmbësorëve: distanca reale në rrugë nga pema e Dijkstrës; pa të: vijë e drejtë x 1.3
  const pA = pemaKembe(nga), pB = pemaKembe(per);
  const ecja = (pema, a, b) => {
    if (pema) { const m = RRJETI_KEMBE.metraDeri(pema, b.lat, b.lon); return isFinite(m) ? kohaEcjesReale(m) : Infinity; }
    return kohaEcjes(distancaM(a.lat, a.lon, b.lat, b.lon));
  };
  const ecjaNgaNisja = [], ecjaDeriFund = new Map();
  g.stacionet.forEach((s, i) => {
    if (distancaM(nga.lat, nga.lon, s.lat, s.lon) <= PARAMETRAT.maksEcjeFillimM) {
      const t = ecja(pA, nga, s); if (isFinite(t)) ecjaNgaNisja.push([i, t]);
    }
    if (distancaM(s.lat, s.lon, per.lat, per.lon) <= PARAMETRAT.maksEcjeFillimM) {
      const t = ecja(pB, per, s); if (isFinite(t)) ecjaDeriFund.set(i, t);
    }
  });

  function relakso(ngaNyja, neNyje, k) {
    if (k < kosto[neNyje]) { kosto[neNyje] = k; ngaKu[neNyje] = ngaNyja; heap.push(k, neNyje); }
  }

  kosto[NISJA] = 0;
  heap.push(0, NISJA);

  while (heap.size) {
    const [k, u] = heap.pop();
    if (k > kosto[u]) continue;         // element i vjetëruar në heap: e kemi gjetur më mirë
    perpunuara++;
    if (u === FUNDI) break;             // destinacioni u nxor: rruga më e shpejtë u gjet

    if (u === NISJA) {
      for (const [s, sek] of ecjaNgaNisja) relakso(u, s, sek);
      const direkt = ecja(pA, nga, per);
      relakso(u, FUNDI, isFinite(direkt) ? direkt : kohaEcjes(distancaM(nga.lat, nga.lon, per.lat, per.lon)));
    } else if (u < N) {                 // KËMBË(s)
      for (const [t, sek] of g.ecjetAdj[u]) relakso(u, t, k + sek);
      for (const [li, poz] of g.hipjet[u]) {
        if (!ndaluara.has(li)) relakso(u, g.fillimiBord[li] + poz, k + pritjaSek(g.linjat[li]));
      }
      if (ecjaDeriFund.has(u)) relakso(u, FUNDI, k + ecjaDeriFund.get(u));
    } else {                            // BORD(L, k)
      const [li, poz] = deshifroBord(g, u);
      const linja = g.linjat[li];
      if (poz < linja.stacionet.length - 1) relakso(u, u + 1, k + linja.kohet[poz] * fs);   // vazhdo
      if (poz > 0) relakso(u, linja.stacionet[poz], k);                               // zbrit
    }
  }

  if (ngaKu[FUNDI] === -1) return null;

  // Rindërtimi: ndjekim shigjetat "ngaKu" nga FUNDI mbrapsht deri te NISJA
  const rruga = [];
  for (let v = FUNDI; v !== -1; v = ngaKu[v]) rruga.push(v);
  rruga.reverse();

  return { kohaSek: kosto[FUNDI], hapat: ndertoHapat(g, rruga, kosto, nga, per, pA, pB), perpunuara };
}

// ---------------------------------------------------------------------------
// Nga vargu i gjendjeve, ndërtojmë hapa të kuptueshëm për njeriun:
//   [{lloji: "ecje", ...}, {lloji: "autobus", linja, stacionet: [...]}, ...]
// ---------------------------------------------------------------------------
function ndertoHapat(g, rruga, kosto, nga, per, pA, pB) {
  const pika = v => v === g.NISJA ? { ...nga, emri: "Nisja" }
                  : v === g.FUNDI ? { ...per, emri: "Destinacioni" }
                  : g.stacionet[v];
  const hapat = [];
  let i = 0;
  while (i < rruga.length - 1) {
    const v = rruga[i], w = rruga[i + 1];
    if (w >= g.N && w < g.NISJA) {
      // hipje në autobus: mbledhim të gjithë stacionet deri sa të zbresim
      const [li, pozFillim] = deshifroBord(g, w);
      const linja = g.linjat[li];
      let j = i + 1;
      while (j + 1 < rruga.length && rruga[j + 1] === rruga[j] + 1 && rruga[j + 1] < g.NISJA) j++;
      const [, pozFund] = deshifroBord(g, rruga[j]);
      const hap = {
        lloji: "autobus",
        li, linja: linja.ref, emri: linja.emri, ngjyra: linja.ngjyra,
        intervaliMin: linja.intervali_min, burimi: linja.burimi_intervalit,
        pozFillim, pozFund,   // pozicionet në linjë, për të marrë gjurmën e rrugës
        idStacionesh: linja.stacionet.slice(pozFillim, pozFund + 1),
        stacionet: linja.stacionet.slice(pozFillim, pozFund + 1).map(s => g.stacionet[s]),
        pritjaSek: pritjaSek(linja),
        kohaSek: kosto[rruga[j]] - kosto[w],
      };
      hap.paralele = linjatParalele(g, hap);
      hapat.push(hap);
      i = j + 1;                         // rruga[j+1] është KËMBË(stacioni ku zbritëm)
    } else {
      // ecje: bashkojmë ecjet e njëpasnjëshme në një hap
      const nisja = pika(v);
      let j = i + 1;
      while (j + 1 < rruga.length && rruga[j] < g.N && (rruga[j + 1] < g.N || rruga[j + 1] === g.FUNDI)) j++;
      const fundi = pika(rruga[j]);
      const pikat = rruga.slice(i, j + 1).map(pika);
      const sek = kosto[rruga[j]] - kosto[v];
      if (sek > 0) hapat.push({ lloji: "ecje", nga: nisja, deri: fundi, pikat, kohaSek: sek,
                                gjurma: gjurmaEEcjes(rruga.slice(i, j + 1), g, pikat, pA, pB) });
      i = j;
    }
  }
  return hapat;
}

// ---------------------------------------------------------------------------
// Linjat paralele: cilat linja të tjera shkojnë nga stacioni i hipjes te stacioni i zbritjes?
// "I njëjti stacion" = brenda 80 m (shpesh janë dy pika në anë të ndryshme të kryqëzimit).
// ---------------------------------------------------------------------------
function linjatParalele(g, hap) {
  const s0 = g.stacionet[hap.idStacionesh[0]];
  const s1 = g.stacionet[hap.idStacionesh[hap.idStacionesh.length - 1]];
  const afer = (id, ref) => {
    const s = g.stacionet[id];
    return distancaM(s.lat, s.lon, ref.lat, ref.lon) <= PARAMETRAT.ngjitur;
  };
  const gjetura = new Map();      // ref -> opsioni më i shpejtë për atë linjë
  g.linjat.forEach((l, li) => {
    if (li === hap.li || l.ref === hap.linja) return;   // jo vetë linja (as drejtimi tjetër i saj)
    for (let i = 0; i < l.stacionet.length - 1; i++) {
      if (!afer(l.stacionet[i], s0)) continue;
      let koha = 0;
      for (let j = i + 1; j < l.stacionet.length; j++) {
        koha += l.kohet[j - 1] * faktoriShpejtesise();
        if (afer(l.stacionet[j], s1)) {
          const ekz = gjetura.get(l.ref);
          if (!ekz || koha < ekz.kohaSek) {
            gjetura.set(l.ref, { li, linja: l.ref, emri: l.emri, ngjyra: l.ngjyra,
                                 intervaliMin: l.intervali_min, kohaSek: koha });
          }
          break;
        }
      }
    }
  });
  // Mbajmë vetëm ato që s'janë shumë më të ngadalta (p.sh. linja që bën xhiro të gjatë rrethore)
  const kufiri = hap.kohaSek * 1.5 + 180;
  return [...gjetura.values()].filter(p => p.kohaSek <= kufiri).sort((a, b) => a.kohaSek - b.kohaSek);
}

// Pritja mesatare kur merr cilëndo nga disa linja
function pritjaePerbashket(intervaletMin) {
  const frekuenca = intervaletMin.reduce((sh, m) => sh + 1 / (m || PARAMETRAT.intervaliParazgjedhurMin), 0);
  return 60 / (2 * frekuenca) * PARAMETRAT.faktoriPritjes;
}

// ---------------------------------------------------------------------------
// Disa opsione: gjejmë rrugën më të mirë, ndalojmë linjat e saj dhe kërkojmë përsëri
// ---------------------------------------------------------------------------
function gjejOpsionet(g, nga, per, maks = 4) {
  const opsionet = [], parë = new Set(), ndaluara = new Set();
  let perpunuara = 0;
  for (let provo = 0; provo < maks + 2 && opsionet.length < maks; provo++) {
    const r = gjejRrugen(g, nga, per, ndaluara);
    if (!r) break;
    perpunuara += r.perpunuara;
    const autobusat = r.hapat.filter(h => h.lloji === "autobus");
    const nenshkrimi = autobusat.map(h => h.linja).join(">") || "ecje";
    if (!parë.has(nenshkrimi)) {
      parë.add(nenshkrimi);
      // Koha reale: me linja paralele pritja është më e shkurtër (merr cilëndo që vjen e para)
      r.kohaRealeSek = r.kohaSek;
      for (const h of autobusat) {
        h.pritjaPerbashketSek = pritjaePerbashket([h.intervaliMin, ...h.paralele.map(p => p.intervaliMin)]);
        r.kohaRealeSek -= h.pritjaSek - h.pritjaPerbashketSek;
      }
      opsionet.push(r);
    }
    if (!autobusat.length) break;   // rruga në këmbë: s'ka linja për të ndaluar, ndalojmë kërkimin
    // ndalojmë linjat e përdorura (edhe linjat paralele, se ato i kemi treguar tashmë si "ose")
    for (const h of autobusat) {
      ndaluara.add(h.li);
      for (const p of h.paralele) ndaluara.add(p.li);
    }
  }
  opsionet.sort((a, b) => a.kohaRealeSek - b.kohaRealeSek);
  return { opsionet, perpunuara };
}

// ---------------------------------------------------------------------------
// Vija e një hapi në këmbë, përgjatë rrugëve. Çdo copë merret nga burimi më i shpejtë:
//   NISJA -> stacion:   nga pema e Dijkstrës së nisjes (është llogaritur tashmë)
//   stacion -> FUNDI:   nga pema e destinacionit, e kthyer mbrapsht
//   stacion -> stacion: me A*
// ---------------------------------------------------------------------------
function gjurmaEEcjes(gjendjet, g, pikat, pA, pB) {
  if (!RRJETI_KEMBE) return null;
  const koord = [];
  for (let k = 0; k < gjendjet.length - 1; k++) {
    const a = pikat[k], b = pikat[k + 1];
    let copa = null;
    if (gjendjet[k] === g.NISJA && pA) copa = RRJETI_KEMBE.rrugaNePeme(pA, b.lat, b.lon);
    else if (gjendjet[k + 1] === g.FUNDI && pB) { copa = RRJETI_KEMBE.rrugaNePeme(pB, a.lat, a.lon); if (copa) copa.reverse(); }
    if (!copa) copa = RRJETI_KEMBE.aStar(a, b);          // rezervë: kërkim direkt mes dy pikave
    if (!copa) copa = [[a.lon, a.lat], [b.lon, b.lat]];  // vetëm nëse s'ka asnjë rrugë në rrjet
    koord.push(...(koord.length ? copa.slice(1) : copa));
  }
  return koord;
}
