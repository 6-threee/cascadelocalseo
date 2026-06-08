/* ============================================================
   CASCADE - Executive Dashboard logic
   Revenue half = illustrative model (arrays below).
   Ops half = LIVE data fetched from exec-dashboard-data edge fn.
   ============================================================ */
(function () {
  "use strict";

  const TOKEN = new URLSearchParams(location.search).get("token") || "";
  const DATA_URL = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/exec-dashboard-data?token=" + encodeURIComponent(TOKEN);
  let LIVE = null; // populated by fetch; ops renders fall back to defaults if null

  /* ---------------- ILLUSTRATIVE REVENUE DATA (model, not actuals) ---------------- */
  const MONTHS = ["Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun"];
  const YEAR   = ["'25","'25","'25","'25","'25","'25","'26","'26","'26","'26","'26","'26"];
  const STARTER  = [6000,8000,10000,12000,14000,16000,19000,21000,24000,27000,30000,33000];
  const STANDARD = [6000,7500,9000,10500,13500,15000,16500,19500,21000,24000,25500,28500];
  const FULL     = [3000,3000,6000,6000,6000,9000,9000,9000,12000,12000,15000,15000];
  const COUNTS   = { Starter:[6,8,10,12,14,16,19,21,24,27,30,33], Standard:[4,5,6,7,9,10,11,13,14,16,17,19], Full:[1,1,2,2,2,3,3,3,4,4,5,5] };
  const ONETIME  = [2000,2500,3000,2500,3500,3000,3500,4000,4500,4000,5000,4500];
  const ADSPEND  = [1200,1500,1900,2200,2600,3000,3200,3500,3900,4200,4600,4900];
  const NEWMRR   = [15000,4000,7500,4500,6500,7500,6000,6500,9500,7500,9500,8000];
  const CHURNED  = [500,500,1000,1000,1500,1000,1500,1500,2000,1500,2000,2000];
  const NEWCLI   = [11,5,8,5,7,7,6,6,9,7,9,7];
  const MRR = MONTHS.map((_, i) => STARTER[i] + STANDARD[i] + FULL[i]);
  const REVENUE = MONTHS.map((_, i) => MRR[i] + ONETIME[i]);
  const INDUSTRIES = [
    { name: "Med spas / aesthetics", mrr: 22500, clients: 16, chg: +9.2, icon: "sparkle" },
    { name: "Chiropractors", mrr: 16500, clients: 12, chg: +6.4, icon: "pulse" },
    { name: "Dentists", mrr: 12000, clients: 9, chg: +4.1, icon: "tooth" },
    { name: "Law firms", mrr: 9000, clients: 6, chg: +12.0, icon: "scale" },
    { name: "HVAC / home services", mrr: 9000, clients: 8, chg: -2.3, icon: "wrench" },
    { name: "Other local service", mrr: 7500, clients: 6, chg: +3.0, icon: "store" }
  ];
  const ICONS = {
    sparkle: '<path d="M12 2 14 9l7 2-7 2-2 7-2-7-7-2 7-2z"/>',
    pulse: '<path d="M3 12h4l3 8 4-16 3 8h4"/>',
    tooth: '<path d="M7 3c-2 0-3 2-3 5 0 5 1 13 3 13s2-6 3-6 1 6 3 6 3-8 3-13c0-3-1-5-3-5-2 0-3 1-4 1s-2-1-2-1z"/>',
    scale: '<path d="M12 3v18M5 7h14M7 7l-3 6h6zM17 7l-3 6h6z"/>',
    wrench: '<path d="M15 4a4 4 0 0 0-5 5L3 16l3 3 7-7a4 4 0 0 0 5-5l-3 3-2-2z"/>',
    store: '<path d="M3 9 5 4h14l2 5M4 9v11h16V9M4 9h16"/>'
  };

  /* ---------------- HELPERS ---------------- */
  const $ = (s, r) => (r || document).querySelector(s);
  const CHEX = { Starter: "#DABE79", Standard: "#4AC4E0", Full: "#8FCBA1" };
  function money(n) {
    if (Math.abs(n) >= 1e6) return "$" + (n / 1e6).toFixed(2).replace(/\.?0+$/, "") + "M";
    if (Math.abs(n) >= 1000) return "$" + (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1) + "K";
    return "$" + Math.round(n).toLocaleString();
  }
  const moneyFull = (n) => "$" + Math.round(n).toLocaleString();
  function pct(n) { return (n >= 0 ? "+" : "") + n.toFixed(1) + "%"; }
  function deltaPct(cur, prev) { return prev ? ((cur - prev) / prev) * 100 : 0; }

  let RANGE = 12;
  function sliceIdx() { const s = MONTHS.length - RANGE; return { s, n: RANGE }; }

  /* ---------------- KPI TILES (illustrative) ---------------- */
  function sparkline(values, color) {
    const w = 100, h = 30, min = Math.min(...values), max = Math.max(...values), span = max - min || 1;
    const pts = values.map((v, i) => [(i / (values.length - 1)) * w, h - ((v - min) / span) * (h - 4) - 2]);
    const d = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
    const last = pts[pts.length - 1];
    return `<svg class="chart" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
      <path d="${d}" fill="none" stroke="${color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="2.4" fill="${color}"/>
    </svg>`;
  }
  function renderKPIs() {
    const last = 11, prev = 10;
    const arpa = MRR[last] / (COUNTS.Starter[last] + COUNTS.Standard[last] + COUNTS.Full[last]);
    const clients = COUNTS.Starter[last] + COUNTS.Standard[last] + COUNTS.Full[last];
    const clientsPrev = COUNTS.Starter[prev] + COUNTS.Standard[prev] + COUNTS.Full[prev];
    const cac = ADSPEND[last] / NEWCLI[last];
    const tiles = [
      { label: "Monthly Recurring Revenue", val: money(MRR[last]), spark: MRR, color: "var(--tan)", delta: deltaPct(MRR[last], MRR[prev]), vs: "vs " + money(MRR[prev]) + " last mo" },
      { label: "Annual Run-Rate (ARR)", val: money(MRR[last] * 12), spark: MRR.map(v => v * 12), color: "var(--blue)", delta: deltaPct(MRR[last], MRR[prev]), vs: money(MRR[last] * 12) + " annualized" },
      { label: "Net New MRR", val: "+" + money(MRR[last] - MRR[prev]), spark: MONTHS.map((_, i) => i ? MRR[i] - MRR[i - 1] : NEWMRR[0]), color: "var(--sage)", delta: deltaPct(MRR[last] - MRR[prev], MRR[prev] - MRR[9]), vs: money(NEWMRR[last]) + " new · " + money(CHURNED[last]) + " churned" },
      { label: "Active Clients", val: String(clients), spark: COUNTS.Starter.map((v, i) => v + COUNTS.Standard[i] + COUNTS.Full[i]), color: "var(--tan)", delta: deltaPct(clients, clientsPrev), vs: "+" + (clients - clientsPrev) + " net this mo" },
      { label: "Blended CAC", val: moneyFull(cac), spark: ADSPEND.map((v, i) => v / NEWCLI[i]), color: "var(--blue)", delta: -deltaPct(cac, ADSPEND[prev] / NEWCLI[prev]), vs: "payback ≈ 0.6 mo" },
      { label: "Net Revenue Retention", val: "108%", spark: [101,102,103,104,105,106,106,107,107,108,108,108], color: "var(--sage)", delta: 1.0, vs: "gross churn 2.6%", rawDelta: true }
    ];
    $("#kpiRow").innerHTML = tiles.map(t => {
      const up = t.delta >= 0;
      const dlabel = t.rawDelta ? "+1.0 pt" : pct(t.delta);
      return `<div class="panel kpi">
        <div class="label">${t.label}</div>
        <div class="val">${t.val}</div>
        <div class="spark">${sparkline(t.spark, t.color)}</div>
        <div class="foot">
          <span class="delta ${up ? "up" : "down"}"><span class="arr">${up ? "▲" : "▼"}</span>${dlabel}</span>
          <span class="vs">${t.vs}</span>
        </div>
      </div>`;
    }).join("");
  }

  /* ---------------- STACKED AREA: MRR by plan (illustrative) ---------------- */
  const SERIES = [
    { key: "Starter", data: STARTER, on: true },
    { key: "Standard", data: STANDARD, on: true },
    { key: "Full", data: FULL, on: true }
  ];
  function renderMRRChart() {
    const wrap = $("#mrrChart");
    const W = wrap.clientWidth || 760, H = 320;
    const m = { t: 16, r: 16, b: 28, l: 52 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const { s, n } = sliceIdx();
    const idx = []; for (let i = s; i < MONTHS.length; i++) idx.push(i);
    const active = SERIES.filter(se => se.on);
    const stackTotals = idx.map(i => active.reduce((a, se) => a + se.data[i], 0));
    const maxV = Math.max(...stackTotals, 1) * 1.08;
    const x = (k) => m.l + (n === 1 ? iw / 2 : (k / (n - 1)) * iw);
    const y = (v) => m.t + ih - (v / maxV) * ih;
    let cum = idx.map(() => 0);
    const layers = active.map(se => {
      const lower = cum.slice();
      cum = cum.map((c, k) => c + se.data[idx[k]]);
      const upper = cum.slice();
      return { key: se.key, lower, upper };
    });
    let svg = `<svg class="chart" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet"><defs>`;
    active.forEach(se => {
      svg += `<linearGradient id="g-${se.key}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${CHEX[se.key]}" stop-opacity="0.55"/>
        <stop offset="1" stop-color="${CHEX[se.key]}" stop-opacity="0.06"/>
      </linearGradient>`;
    });
    svg += `</defs>`;
    const ticks = 4;
    for (let t = 0; t <= ticks; t++) {
      const val = (maxV / ticks) * t, yy = y(val);
      svg += `<line class="grid-line" x1="${m.l}" y1="${yy.toFixed(1)}" x2="${W - m.r}" y2="${yy.toFixed(1)}"/>`;
      svg += `<text class="axis-label" x="${m.l - 10}" y="${(yy + 3).toFixed(1)}" text-anchor="end">${money(val)}</text>`;
    }
    idx.forEach((i, k) => {
      if (n > 8 && k % 2 && k !== n - 1) return;
      svg += `<text class="axis-label" x="${x(k).toFixed(1)}" y="${H - 8}" text-anchor="middle">${MONTHS[i]}</text>`;
    });
    layers.forEach(L => {
      const top = L.upper.map((v, k) => `${x(k).toFixed(1)},${y(v).toFixed(1)}`);
      const bot = L.lower.map((v, k) => `${x(k).toFixed(1)},${y(v).toFixed(1)}`).reverse();
      svg += `<polygon class="area-path" fill="url(#g-${L.key})" points="${top.concat(bot).join(" ")}"/>`;
      svg += `<polyline class="line-path" stroke="${CHEX[L.key]}" points="${top.join(" ")}"/>`;
    });
    svg += `<g id="mrrHover" style="opacity:0"><line class="hover-line" y1="${m.t}" y2="${m.t + ih}"/>${active.map(se => `<circle class="dot dot-${se.key}" r="4" fill="${CHEX[se.key]}"/>`).join("")}</g>`;
    svg += `<rect id="mrrCapture" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}" fill="transparent"/></svg>`;
    wrap.innerHTML = svg;
    const capture = $("#mrrCapture", wrap), hover = $("#mrrHover", wrap), tip = $("#mrrTip"), svgEl = wrap.querySelector("svg");
    function pos(e) {
      const r = svgEl.getBoundingClientRect();
      const px = ((e.clientX - r.left) / r.width) * W;
      let k = Math.round(((px - m.l) / iw) * (n - 1));
      return Math.max(0, Math.min(n - 1, k));
    }
    capture.addEventListener("pointermove", (e) => {
      const k = pos(e), i = idx[k];
      hover.style.opacity = 1;
      hover.querySelector(".hover-line").setAttribute("x1", x(k));
      hover.querySelector(".hover-line").setAttribute("x2", x(k));
      let cumv = 0;
      active.forEach(se => { cumv += se.data[i]; const dot = hover.querySelector(".dot-" + se.key); if (dot) { dot.setAttribute("cx", x(k)); dot.setAttribute("cy", y(cumv)); } });
      const total = active.reduce((a, se) => a + se.data[i], 0);
      tip.innerHTML = `<div class="tt-m">${MONTHS[i]} ${YEAR[i]}</div>` +
        active.map(se => `<div class="tt-row"><span class="sw" style="background:${CHEX[se.key]}"></span><span class="k">${se.key}</span><span class="v">${moneyFull(se.data[i])}</span></div>`).join("") +
        `<div class="tt-total"><span class="k">Total MRR</span><span class="v">${moneyFull(total)}</span></div>`;
      tip.classList.add("show");
      const wr = wrap.getBoundingClientRect();
      let tx = (x(k) / W) * wr.width + 16;
      if (tx + 190 > wr.width) tx = (x(k) / W) * wr.width - 190;
      tip.style.left = tx + "px"; tip.style.top = "8px";
    });
    capture.addEventListener("pointerleave", () => { hover.style.opacity = 0; tip.classList.remove("show"); });
  }
  function renderLegend() {
    $("#mrrLegend").innerHTML = SERIES.map(se =>
      `<button data-key="${se.key}" class="${se.on ? "" : "off"}"><span class="sw" style="background:${CHEX[se.key]}"></span>${se.key} · ${money(se.data[11])}</button>`
    ).join("");
    $("#mrrLegend").querySelectorAll("button").forEach(b => {
      b.addEventListener("click", () => {
        const se = SERIES.find(s => s.key === b.dataset.key);
        if (se.on && SERIES.filter(s => s.on).length === 1) return;
        se.on = !se.on; b.classList.toggle("off", !se.on); renderMRRChart();
      });
    });
  }

  /* ---------------- REVENUE vs AD SPEND (illustrative) ---------------- */
  function renderRevChart() {
    const wrap = $("#revChart");
    const W = wrap.clientWidth || 460, H = 280;
    const m = { t: 16, r: 46, b: 28, l: 50 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const { s, n } = sliceIdx();
    const idx = []; for (let i = s; i < MONTHS.length; i++) idx.push(i);
    const maxRev = Math.max(...idx.map(i => REVENUE[i])) * 1.12;
    const maxAd = Math.max(...idx.map(i => ADSPEND[i])) * 1.6;
    const bw = (iw / n) * 0.5;
    const xc = (k) => m.l + (k + 0.5) * (iw / n);
    const yR = (v) => m.t + ih - (v / maxRev) * ih;
    const yA = (v) => m.t + ih - (v / maxAd) * ih;
    let svg = `<svg class="chart" viewBox="0 0 ${W} ${H}">`;
    const ticks = 4;
    for (let t = 0; t <= ticks; t++) {
      const val = (maxRev / ticks) * t, yy = yR(val);
      svg += `<line class="grid-line" x1="${m.l}" y1="${yy.toFixed(1)}" x2="${W - m.r}" y2="${yy.toFixed(1)}"/>`;
      svg += `<text class="axis-label" x="${m.l - 9}" y="${(yy + 3).toFixed(1)}" text-anchor="end">${money(val)}</text>`;
    }
    idx.forEach((i, k) => {
      const h = ih - (yR(REVENUE[i]) - m.t);
      svg += `<rect x="${(xc(k) - bw / 2).toFixed(1)}" y="${yR(REVENUE[i]).toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(0, h).toFixed(1)}" rx="3" fill="var(--tan)" opacity="0.85"><title>${MONTHS[i]}: ${moneyFull(REVENUE[i])} revenue</title></rect>`;
      if (n <= 8 || k % 2 === 0 || k === n - 1)
        svg += `<text class="axis-label" x="${xc(k).toFixed(1)}" y="${H - 8}" text-anchor="middle">${MONTHS[i]}</text>`;
    });
    const lpts = idx.map((i, k) => `${xc(k).toFixed(1)},${yA(ADSPEND[i]).toFixed(1)}`);
    svg += `<polyline class="line-path" stroke="var(--coral)" stroke-dasharray="0" points="${lpts.join(" ")}"/>`;
    idx.forEach((i, k) => { svg += `<circle class="dot" cx="${xc(k).toFixed(1)}" cy="${yA(ADSPEND[i]).toFixed(1)}" r="3.4" fill="var(--coral)"><title>${MONTHS[i]}: ${moneyFull(ADSPEND[i])} ad spend</title></circle>`; });
    for (let t = 0; t <= ticks; t++) {
      const val = (maxAd / ticks) * t, yy = yA(val);
      svg += `<text class="axis-label" x="${W - m.r + 8}" y="${(yy + 3).toFixed(1)}" text-anchor="start" fill="var(--coral)" opacity="0.8">${money(val)}</text>`;
    }
    svg += `</svg>`;
    wrap.innerHTML = svg;
  }

  /* ---------------- NET NEW vs CHURNED (illustrative) ---------------- */
  function renderFlowChart() {
    const wrap = $("#flowChart");
    const W = wrap.clientWidth || 460, H = 280;
    const m = { t: 18, r: 14, b: 28, l: 50 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const { s, n } = sliceIdx();
    const idx = []; for (let i = s; i < MONTHS.length; i++) idx.push(i);
    const maxNew = Math.max(...idx.map(i => NEWMRR[i]));
    const maxChn = Math.max(...idx.map(i => CHURNED[i]));
    const zero = m.t + (maxNew / (maxNew + maxChn)) * ih;
    const upH = zero - m.t, dnH = m.t + ih - zero;
    const bw = (iw / n) * 0.46;
    const xc = (k) => m.l + (k + 0.5) * (iw / n);
    let svg = `<svg class="chart" viewBox="0 0 ${W} ${H}">`;
    svg += `<line class="grid-line" x1="${m.l}" y1="${zero.toFixed(1)}" x2="${W - m.r}" y2="${zero.toFixed(1)}" stroke="var(--line-2)"/>`;
    svg += `<text class="axis-label" x="${m.l - 9}" y="${(m.t + 8)}" text-anchor="end" fill="var(--up)">${money(maxNew)}</text>`;
    svg += `<text class="axis-label" x="${m.l - 9}" y="${(m.t + ih)}" text-anchor="end" fill="var(--down)">${money(maxChn)}</text>`;
    idx.forEach((i, k) => {
      const hN = (NEWMRR[i] / maxNew) * upH * 0.92;
      const hC = (CHURNED[i] / maxChn) * dnH * 0.92;
      svg += `<rect x="${(xc(k) - bw / 2).toFixed(1)}" y="${(zero - hN).toFixed(1)}" width="${bw.toFixed(1)}" height="${hN.toFixed(1)}" rx="3" fill="var(--up)" opacity="0.82"><title>${MONTHS[i]}: +${moneyFull(NEWMRR[i])} new+expansion</title></rect>`;
      svg += `<rect x="${(xc(k) - bw / 2).toFixed(1)}" y="${zero.toFixed(1)}" width="${bw.toFixed(1)}" height="${hC.toFixed(1)}" rx="3" fill="var(--down)" opacity="0.8"><title>${MONTHS[i]}: -${moneyFull(CHURNED[i])} churned</title></rect>`;
      if (n <= 8 || k % 2 === 0 || k === n - 1)
        svg += `<text class="axis-label" x="${xc(k).toFixed(1)}" y="${H - 8}" text-anchor="middle">${MONTHS[i]}</text>`;
    });
    svg += `</svg>`;
    wrap.innerHTML = svg;
  }

  /* ---------------- DONUT (illustrative) ---------------- */
  function renderDonut() {
    const last = 11;
    const data = [
      { key: "Starter", mrr: STARTER[last], clients: COUNTS.Starter[last] },
      { key: "Standard", mrr: STANDARD[last], clients: COUNTS.Standard[last] },
      { key: "Full", mrr: FULL[last], clients: COUNTS.Full[last] }
    ];
    const total = data.reduce((a, d) => a + d.mrr, 0);
    const R = 78, r = 52, cx = 90, cy = 90;
    let a0 = -Math.PI / 2, paths = "";
    data.forEach(d => {
      const a1 = a0 + (d.mrr / total) * Math.PI * 2;
      const large = a1 - a0 > Math.PI ? 1 : 0;
      const p = (ang, rad) => [cx + rad * Math.cos(ang), cy + rad * Math.sin(ang)];
      const [x0, y0] = p(a0, R), [x1, y1] = p(a1, R), [x2, y2] = p(a1, r), [x3, y3] = p(a0, r);
      paths += `<path d="M${x0.toFixed(1)} ${y0.toFixed(1)} A${R} ${R} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)} L${x2.toFixed(1)} ${y2.toFixed(1)} A${r} ${r} 0 ${large} 0 ${x3.toFixed(1)} ${y3.toFixed(1)} Z" fill="${CHEX[d.key]}" opacity="0.9"><title>${d.key}: ${moneyFull(d.mrr)} (${Math.round(d.mrr / total * 100)}%)</title></path>`;
      a0 = a1;
    });
    $("#donut").innerHTML = `<svg width="180" height="180" viewBox="0 0 180 180">${paths}
      <text class="mono" x="90" y="84" text-anchor="middle" font-size="12" fill="#A1B8A9">MRR</text>
      <text class="donut-center" x="90" y="109" text-anchor="middle" font-size="27" fill="#F4F1E6">${money(total)}</text></svg>`;
    $("#donutLegend").innerHTML = data.map(d =>
      `<div class="dl-item"><span class="sw" style="background:${CHEX[d.key]}"></span>
        <span class="k">${d.key}<small>$${d.key === "Starter" ? "1,000" : d.key === "Standard" ? "1,500" : "3,000"}/mo</small></span>
        <span class="v"><b>${moneyFull(d.mrr)}</b><small>${d.clients} clients · ${Math.round(d.mrr / total * 100)}%</small></span>
      </div>`).join("");
  }

  /* ---------------- UNIT ECONOMICS (illustrative) ---------------- */
  function renderMetrics() {
    const last = 11;
    const clients = COUNTS.Starter[last] + COUNTS.Standard[last] + COUNTS.Full[last];
    const arpa = MRR[last] / clients;
    const cac = ADSPEND[last] / NEWCLI[last];
    const ltv = (arpa * 0.82) / 0.026;
    const mktRoi = (NEWMRR[last] + ONETIME[last]) / ADSPEND[last];
    const items = [
      { k: "ARPA (avg / client)", v: moneyFull(Math.round(arpa)), note: clients + " active clients" },
      { k: "Gross margin", v: "82%", note: "automation-led delivery" },
      { k: "Blended CAC", v: moneyFull(Math.round(cac)), note: NEWCLI[last] + " new clients in Jun" },
      { k: "CAC payback", v: "0.6 <small>mo</small>", note: "high-margin retainers" },
      { k: "Est. LTV", v: money(ltv), note: "≈ " + Math.round(ltv / cac) + "× CAC" },
      { k: "Marketing ROI", v: mktRoi.toFixed(1) + "×", note: "new rev ÷ ad spend" }
    ];
    $("#metrics").innerHTML = items.map(it => `<div class="m"><div class="k">${it.k}</div><div class="v num">${it.v}</div><div class="note">${it.note}</div></div>`).join("");
  }

  /* ---------------- INDUSTRIES TABLE (illustrative) ---------------- */
  function renderTable() {
    const max = Math.max(...INDUSTRIES.map(d => d.mrr));
    $("#indTable tbody").innerHTML = INDUSTRIES.map(d => {
      const up = d.chg >= 0;
      return `<tr>
        <td><div class="ind"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">${ICONS[d.icon]}</svg></span><div>${d.name}<div class="bar"><i style="width:${(d.mrr / max * 100).toFixed(0)}%"></i></div></div></div></td>
        <td class="r">${d.clients}</td>
        <td class="r"><span class="mrr">${moneyFull(d.mrr)}</span></td>
        <td class="r"><span class="chg ${up ? "up" : "down"}">${up ? "▲" : "▼"} ${Math.abs(d.chg).toFixed(1)}%</span></td>
      </tr>`;
    }).join("");
  }

  /* ============================================================
     DAILY OPERATIONS - LIVE (fall back to defaults if no LIVE)
     ============================================================ */
  const DEF = {
    tasks: [
      { id: "approve-replies", title: "Triage prospect replies awaiting a response", meta: "Inbound · respond same day", tag: "review" },
      { id: "approve-backlog", title: "Approve a batch from the audit backlog", meta: "Verified-email audits ready to send", tag: "audit" }
    ],
    pipeline: [
      { l: "Audits sent", n: 0, c: "#DABE79" },
      { l: "Replies received", n: 0, c: "#4AC4E0" },
      { l: "Calls booked", n: 0, c: "#8FCBA1" },
      { l: "New clients closed", n: 0, c: "#8FCBA1" }
    ],
    goals: [
      { k: "Audits sent (MTD)", now: 0, target: 400 },
      { k: "New clients (MTD)", now: 0, target: 3 },
      { k: "Foundations sold (MTD)", now: 0, target: 4 },
      { k: "Cold replies (7d)", now: 0, target: 5 }
    ],
    last24: [{ k: "Audits sent", v: "0", hot: true }],
    health: { rows: [{ k: "Sent", v: "0 cold" }, { k: "Open rate", v: "0.0%" }, { k: "Reply rate", v: "0.0%" }, { k: "Booked calls", v: "n/a" }], leak: null },
    watch: { rows: [{ k: "Foundations sold (MTD)", v: "0" }, { k: "Cold replies (7d)", v: "0" }], backlog: { n: 0, sub: "audits awaiting approval" } },
    feed: [{ t: "No recent activity loaded", time: "", c: "var(--muted-2)" }]
  };
  function ops(key) { return (LIVE && LIVE[key] != null) ? LIVE[key] : DEF[key]; }

  const CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg>';
  function opsState() { try { return JSON.parse(localStorage.getItem("cascade_tasks") || "{}"); } catch (e) { return {}; } }
  function saveOps(s) { try { localStorage.setItem("cascade_tasks", JSON.stringify(s)); } catch (e) {} }

  function renderTasks() {
    const TASKS = ops("tasks");
    const done = opsState();
    const total = TASKS.length || 1;
    const cleared = TASKS.filter(t => done[t.id]).length;
    $("#taskList").innerHTML = TASKS.map(t =>
      `<div class="task ${done[t.id] ? "done" : ""}" data-id="${t.id}">
        <span class="tcheck">${CHECK}</span>
        <div class="tbody"><div class="ttitle">${t.title}</div><div class="tmeta">${t.meta}</div></div>
        <span class="ttag ${t.tag}">${t.tag === "gbp" ? "GBP" : t.tag}</span>
      </div>`).join("");
    $("#taskBar").style.width = (cleared / total * 100) + "%";
    $("#taskLbl").textContent = cleared + " of " + TASKS.length + " cleared";
    $("#taskList").querySelectorAll(".task").forEach(el => el.addEventListener("click", () => {
      const s = opsState(); s[el.dataset.id] = !s[el.dataset.id]; saveOps(s); renderTasks();
    }));
  }
  function renderGoals() {
    $("#goalList").innerHTML = ops("goals").map(g => {
      const p = Math.min(100, g.target ? g.now / g.target * 100 : 0);
      const fmt = g.money ? money : (v) => v;
      return `<div class="gl-row">
        <div class="gl-top"><span class="gl-k">${g.k}</span><span class="gl-v"><b>${fmt(g.now)}</b> / ${fmt(g.target)}</span></div>
        <div class="gl-bar ${p >= 90 ? "ok" : ""}"><i style="width:${p.toFixed(0)}%"></i></div>
      </div>`;
    }).join("");
  }
  function renderPipeline() {
    const P = ops("pipeline");
    const top = Math.max(P[0].n, 1);
    $("#pipeline").innerHTML = P.map((s, i) => {
      const w = (s.n / top * 100).toFixed(0);
      const p = i === 0 ? "" : `<span class="fn-p">${(s.n / top * 100).toFixed(0)}% of sent</span>`;
      return `<div class="fn-step"><div class="fn-bar"><i style="background:${s.c};width:${w}%"></i><span class="fn-n num">${s.n}</span><span class="fn-l">${s.l}</span>${p}</div></div>`;
    }).join("");
    const conv = P[0].n ? (P[3].n / P[0].n * 100).toFixed(1) : "0.0";
    $("#pipeConv").innerHTML = `Sent → client conversion <b>${conv}%</b> · ${P[1].n} replies this week`;
  }
  function renderFeed() {
    $("#feed").innerHTML = ops("feed").map(f =>
      `<div class="feed-item"><span class="fi-dot" style="background:${f.c}"></span>
       <div class="fi-body"><div class="fi-t">${f.t}</div><div class="fi-time">${f.time}</div></div></div>`).join("");
  }
  function renderLast24() {
    $("#last24").innerHTML = ops("last24").map(m =>
      `<div class="mr"><span class="k">${m.k}</span><span class="v num ${m.hot ? "hot" : ""}">${m.v}</span></div>`).join("");
  }
  function renderHealth() {
    const H = ops("health");
    let html = H.rows.map(r =>
      `<div class="mr"><span class="k">${r.k}</span><span class="v num">${r.v}${r.t ? `<span class="trend ${r.tc || ""}">${r.t}</span>` : ""}</span></div>`).join("");
    if (H.leak) html += `<div class="leak"><div class="lk-t">${H.leak.t}</div><div class="lk-s">${H.leak.s}</div></div>`;
    $("#health").innerHTML = html;
  }
  function renderWatch() {
    const W = ops("watch");
    let html = W.rows.map(r =>
      r.bad
        ? `<div class="watch-row"><span class="wk">${r.k}</span><span class="wv bad"><span class="rd"></span>${r.v}</span></div>`
        : `<div class="watch-row"><span class="wk">${r.k}</span><span class="wv num">${r.v}</span></div>`).join("");
    if (W.backlog) html += `<div class="backlog"><div class="bl-t"><b>${W.backlog.n.toLocaleString()}</b> ${W.backlog.sub}</div>${W.backlog.detail ? `<div class="bl-s">${W.backlog.detail}</div>` : ""}</div>`;
    $("#watch").innerHTML = html;
  }

  /* ---------------- RENDER ALL ---------------- */
  function renderRevenue() { renderKPIs(); renderLegend(); renderMRRChart(); renderRevChart(); renderFlowChart(); renderDonut(); renderMetrics(); renderTable(); }
  function renderOps() { renderTasks(); renderGoals(); renderPipeline(); renderFeed(); renderLast24(); renderHealth(); renderWatch(); }
  function renderAll() { renderRevenue(); renderOps(); }

  function applyBanner() {
    const txt = $("#illusText"), upd = $("#updatedLbl");
    if (LIVE && LIVE.generatedPT) upd.textContent = "Updated " + LIVE.generatedPT;
    // The revenue panels use a fixed illustrative MODEL (not yet wired to real MRR), so they stay
    // labeled "illustrative" regardless of revenueLive - never present modeled numbers as live.
    // When the revenue arrays are wired to live MRR later, drop the tags + flip this message then.
    txt.innerHTML = "Revenue panels are an <b>illustrative model</b>; daily-operations data below is <b>live</b>.";
  }

  // range toggle (revenue charts only)
  document.querySelectorAll("#rangeSeg button").forEach(b => {
    b.addEventListener("click", () => {
      document.querySelectorAll("#rangeSeg button").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      RANGE = parseInt(b.dataset.range, 10);
      renderMRRChart(); renderRevChart(); renderFlowChart();
    });
  });
  let rt;
  window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(renderAll, 150); });

  /* ---- collapsible bottom panels ---- */
  function setupCollapse() {
    const chev = '<span class="chev"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span>';
    const panels = [];
    document.querySelectorAll(".row-ops .panel, .row-24 .panel").forEach(p => panels.push(p));
    const feed = document.querySelector("#feed");
    if (feed) panels.push(feed.closest(".panel"));
    panels.forEach(p => {
      if (p.dataset.collapseInit) return;
      p.dataset.collapseInit = "1";
      p.classList.add("collapsible");
      const head = p.querySelector(".panel-head");
      head.insertAdjacentHTML("beforeend", chev);
      head.addEventListener("click", () => p.classList.toggle("collapsed"));
    });
    document.querySelectorAll(".row-24 .panel").forEach(p => p.classList.add("collapsed"));
    if (feed) feed.closest(".panel").classList.add("collapsed");
  }

  /* ---------------- INIT ---------------- */
  renderAll();      // first paint with defaults/illustrative (instant)
  setupCollapse();
  applyBanner();
  // then hydrate ops with live data
  fetch(DATA_URL, { headers: { "Accept": "application/json" } })
    .then(r => r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status)))
    .then(j => { LIVE = j; applyBanner(); renderOps(); })
    .catch(() => { /* keep defaults; banner already notes live-ops intent */ });
})();
