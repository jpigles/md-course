/* Molecular Dynamics course: page behaviour and the interactive demos.
   No dependencies except KaTeX (loaded by the page) for the maths. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

  /* ---------- page chrome: maths, theme, menu, progress ---------- */
  function renderMath() {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [{ left: '\\[', right: '\\]', display: true }, { left: '\\(', right: '\\)', display: false }],
        throwOnError: false, strict: false
      });
    }
  }
  function initChrome() {
    const tb = $('#themeBtn');
    if (tb) tb.addEventListener('click', () => {
      const root = document.documentElement;
      const cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      const next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('mdc-theme', next); } catch (e) { /* ignore */ }
      window.dispatchEvent(new Event('mdc-redraw'));
    });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => window.dispatchEvent(new Event('mdc-redraw')));
    const mb = $('#menuBtn');
    if (mb) mb.addEventListener('click', () => document.body.classList.toggle('nav-open'));
    $('.content').addEventListener('click', () => document.body.classList.remove('nav-open'));

    const slug = document.body.dataset.page;
    let done = store.get('mdc-done', []);
    const paint = () => {
      $$('[data-slug]').forEach(li => li.classList.toggle('done', done.includes(li.dataset.slug)));
      const total = $$('.modlist li').length;
      const n = done.filter(s => $(`.modlist li[data-slug="${s}"]`)).length;
      const fill = $('#progressFill'), txt = $('#progressText');
      if (fill) fill.style.width = (total ? 100 * n / total : 0) + '%';
      if (txt) txt.textContent = n + ' of ' + total + ' modules finished';
    };
    const chk = $('#doneChk');
    if (chk) {
      chk.checked = done.includes(slug);
      chk.addEventListener('change', () => {
        done = store.get('mdc-done', []).filter(s => s !== slug);
        if (chk.checked) done.push(slug);
        store.set('mdc-done', done); paint();
      });
    }
    paint();
    const cur = $('.modlist li.current');
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest' });
  }

  /* ---------- a small line-plot helper on canvas ---------- */
  function niceTicks(a, b, n) {
    const span = b - a; if (!(span > 0)) return [a];
    const step0 = span / n, mag = Math.pow(10, Math.floor(Math.log10(step0))), f = step0 / mag;
    const step = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * mag, t = [];
    for (let v = Math.ceil(a / step - 1e-9) * step; v <= b + 1e-9 * span; v += step) t.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    return t;
  }
  function fmt(v) {
    if (!isFinite(v)) return '–';
    const a = Math.abs(v); if (a === 0) return '0';
    if (a >= 1e4 || a < 1e-3) return v.toExponential(1);
    return String(+v.toPrecision(3));
  }
  class Plot {
    constructor(host, o) {
      this.o = Object.assign({ height: 250, xLabel: '', yLabel: '', hover: true, xRange: null, yRange: null }, o);
      this.legend = el('div', 'w-legend'); this.wrap = el('div', 'w-plot');
      this.cv = document.createElement('canvas'); this.tip = el('div', 'w-tip');
      this.wrap.append(this.cv, this.tip); host.append(this.legend, this.wrap);
      this.series = []; this.hover = null;
      this.cv.setAttribute('role', 'img'); this.cv.setAttribute('aria-label', (this.o.yLabel || 'value') + ' against ' + (this.o.xLabel || 'x'));
      if (this.o.hover) {
        this.cv.addEventListener('mousemove', e => { const r = this.cv.getBoundingClientRect(); this.hover = { px: e.clientX - r.left, py: e.clientY - r.top }; this.draw(); });
        this.cv.addEventListener('mouseleave', () => { this.hover = null; this.tip.style.display = 'none'; this.draw(); });
      }
      if (window.ResizeObserver) new ResizeObserver(() => this.draw()).observe(this.wrap);
      window.addEventListener('mdc-redraw', () => this.draw());
    }
    set(series, ranges) { this.series = series; if (ranges) Object.assign(this.o, ranges); this.draw(); }
    draw() {
      const w = this.wrap.clientWidth || 300, h = this.o.height, dpr = window.devicePixelRatio || 1;
      const cv = this.cv; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); cv.style.height = h + 'px';
      const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
      const m = { l: 56, r: 12, t: 10, b: 38 }, pw = w - m.l - m.r, ph = h - m.t - m.b;
      let xr = this.o.xRange, yr = this.o.yRange;
      if (!xr || !yr) {
        let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
        this.series.forEach(s => { for (let i = 0; i < s.x.length; i++) { const X = s.x[i], Y = s.y[i]; if (!isFinite(X) || !isFinite(Y)) continue; if (X < x0) x0 = X; if (X > x1) x1 = X; if (Y < y0) y0 = Y; if (Y > y1) y1 = Y; } });
        if (!isFinite(x0)) { x0 = 0; x1 = 1; y0 = 0; y1 = 1; }
        if (y1 - y0 < 1e-12) { y0 -= 0.5; y1 += 0.5; }
        const pad = 0.06 * (y1 - y0);
        xr = xr || [x0, x1 > x0 ? x1 : x0 + 1]; yr = yr || [y0 - pad, y1 + pad];
      }
      const X = v => m.l + (v - xr[0]) / (xr[1] - xr[0]) * pw, Y = v => m.t + (1 - (v - yr[0]) / (yr[1] - yr[0])) * ph;
      this._map = { xr, yr, m, pw, ph };
      const cLine = cssv('--line'), cAxis = cssv('--axis'), cMuted = cssv('--muted'), cInk2 = cssv('--ink2');
      g.font = '12px system-ui, sans-serif'; g.lineWidth = 1;
      g.strokeStyle = cLine; g.fillStyle = cMuted; g.textAlign = 'right'; g.textBaseline = 'middle';
      niceTicks(yr[0], yr[1], 5).forEach(t => { const y = Math.round(Y(t)) + 0.5; g.beginPath(); g.moveTo(m.l, y); g.lineTo(m.l + pw, y); g.stroke(); g.fillText(fmt(t), m.l - 7, y); });
      g.textAlign = 'center'; g.textBaseline = 'top';
      niceTicks(xr[0], xr[1], Math.max(3, Math.floor(pw / 90))).forEach(t => g.fillText(fmt(t), X(t), m.t + ph + 6));
      g.strokeStyle = cAxis; g.beginPath(); g.moveTo(m.l, m.t + ph + 0.5); g.lineTo(m.l + pw, m.t + ph + 0.5); g.stroke();
      if (yr[0] < 0 && yr[1] > 0) { const y = Math.round(Y(0)) + 0.5; g.beginPath(); g.moveTo(m.l, y); g.lineTo(m.l + pw, y); g.stroke(); }
      g.fillStyle = cInk2; g.fillText(this.o.xLabel, m.l + pw / 2, h - 15);
      g.save(); g.translate(13, m.t + ph / 2); g.rotate(-Math.PI / 2); g.textBaseline = 'middle'; g.fillText(this.o.yLabel, 0, 0); g.restore();
      g.save(); g.beginPath(); g.rect(m.l, m.t, pw, ph); g.clip();
      this.series.forEach(s => {
        if (s.points) {                                   // scatter: data points, not a line
          g.fillStyle = cssv(s.color); g.strokeStyle = cssv('--surface'); g.lineWidth = 1.5; g.globalAlpha = s.alpha || 1;
          for (let i = 0; i < s.x.length; i++) { if (!isFinite(s.y[i])) continue; g.beginPath(); g.arc(X(s.x[i]), Y(s.y[i]), s.r || 4, 0, 6.2832); g.fill(); if ((s.r || 4) >= 3) g.stroke(); }
          g.globalAlpha = 1; return;
        }
        g.strokeStyle = cssv(s.color); g.lineWidth = s.width || 2; g.lineJoin = 'round'; g.globalAlpha = s.alpha || 1;
        g.setLineDash(s.dash || []); g.beginPath(); let pen = false;
        for (let i = 0; i < s.x.length; i++) {
          const yv = s.y[i];
          if (!isFinite(yv)) { pen = false; continue; }
          const px = X(s.x[i]), py = Y(Math.max(yr[0] - (yr[1] - yr[0]), Math.min(yr[1] + (yr[1] - yr[0]), yv)));
          if (pen) g.lineTo(px, py); else { g.moveTo(px, py); pen = true; }
        }
        g.stroke();
      });
      g.setLineDash([]); g.globalAlpha = 1; g.restore();
      const named = this.series.filter(s => s.name);
      this.legend.innerHTML = named.length > 1 ? named.map(s => `<span><i style="background:${cssv(s.color)}${s.points ? ';width:8px;height:8px;border-radius:50%' : ''}"></i>${s.name}</span>`).join('') : '';
      if (this.hover && this.o.hover && named.length) {
        const hx = this.hover.px; if (hx < m.l || hx > m.l + pw) { this.tip.style.display = 'none'; return; }
        const xv = xr[0] + (hx - m.l) / pw * (xr[1] - xr[0]);
        g.strokeStyle = cAxis; g.beginPath(); g.moveTo(Math.round(hx) + 0.5, m.t); g.lineTo(Math.round(hx) + 0.5, m.t + ph); g.stroke();
        let rows = '';
        named.forEach(s => {
          let bi = -1, bd = Infinity;
          for (let i = 0; i < s.x.length; i++) { const d = Math.abs(s.x[i] - xv); if (d < bd && isFinite(s.y[i])) { bd = d; bi = i; } }
          if (bi < 0) return;
          const px = X(s.x[bi]), py = Y(s.y[bi]);
          if (py >= m.t - 1 && py <= m.t + ph + 1) { g.fillStyle = cssv(s.color); g.strokeStyle = cssv('--surface'); g.lineWidth = 2; g.beginPath(); g.arc(px, py, 4, 0, 6.2832); g.fill(); g.stroke(); }
          rows += `<div><i style="background:${cssv(s.color)}"></i>${s.name}: <b>${fmt(s.y[bi])}</b></div>`;
        });
        this.tip.innerHTML = `<div>${this.o.xLabel}: <b>${fmt(xv)}</b></div>` + rows;
        this.tip.style.display = 'block';
        const tw = this.tip.offsetWidth; let left = hx + 14; if (left + tw > w - 4) left = hx - tw - 14;
        this.tip.style.left = Math.max(2, left) + 'px'; this.tip.style.top = Math.max(2, Math.min(h - 80, this.hover.py - 20)) + 'px';
      }
    }
  }
  function slider(parent, label, min, max, step, val, f) {
    const l = el('label', '', label + ' '); const inp = document.createElement('input');
    inp.type = 'range'; inp.min = min; inp.max = max; inp.step = step; inp.value = val;
    const out = document.createElement('output'); out.textContent = (f || String)(+val);
    inp.addEventListener('input', () => { out.textContent = (f || String)(+inp.value); });
    l.append(inp, out); parent.append(l); return inp;
  }
  function button(parent, text, primary) { const b = el('button', primary ? 'primary' : '', text); b.type = 'button'; parent.append(b); return b; }
  function gauss() { let u = 0, v = 0; while (u === 0) u = Math.random(); v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(6.283185307 * v); }
  function linspace(a, b, n) { const o = new Array(n); for (let i = 0; i < n; i++) o[i] = a + (b - a) * i / (n - 1); return o; }

  /* ---------- demo 1: Lennard-Jones and Coulomb pair energy ---------- */
  function wLJ(host) {
    host.append(el('h4', '', 'Try it: the non-bonded pair energy'),
      el('p', 'sub', 'Lennard-Jones plus Coulomb energy of two atoms against their distance. Move the sliders and watch where the minimum sits and how fast each term dies off.'));
    const c = el('div', 'w-controls'); host.append(c);
    const sE = slider(c, 'ε (kJ/mol)', 0.1, 2, 0.05, 0.65, v => v.toFixed(2));
    const sS = slider(c, 'σ (nm)', 0.25, 0.45, 0.005, 0.315, v => v.toFixed(3));
    const sQ = slider(c, 'q₁q₂ (e²)', -0.4, 0.4, 0.01, 0, v => v.toFixed(2));
    const p = new Plot(host, { xLabel: 'distance r (nm)', yLabel: 'energy (kJ/mol)', xRange: [0.2, 1.2], yRange: [-6, 6], height: 270 });
    const st = el('div', 'w-stats'); host.append(st);
    const r = linspace(0.2, 1.2, 400);
    function upd() {
      const e = +sE.value, s = +sS.value, q = +sQ.value;
      const lj = r.map(x => { const a = Math.pow(s / x, 6); return 4 * e * (a * a - a); });
      const co = r.map(x => 138.935 * q / x);
      const series = [{ name: 'Lennard-Jones', color: '--s1', x: r, y: lj }];
      if (q !== 0) series.push({ name: 'Coulomb', color: '--s2', x: r, y: co }, { name: 'Sum', color: '--s3', x: r, y: lj.map((v, i) => v + co[i]) });
      const Y = Math.max(6, 1.15 * Math.abs(138.935 * q / 0.3));
      p.set(series, { yRange: [-Y, Y] });
      const rm = Math.pow(2, 1 / 6) * s;
      st.innerHTML = `<span>LJ minimum at r = 2<sup>1/6</sup>σ = <b>${rm.toFixed(3)} nm</b></span><span>depth = −ε = <b>${(-e).toFixed(2)} kJ/mol</b> (${(e / 2.494).toFixed(2)} k<sub>B</sub>T at 300 K)</span><span>Coulomb at that distance: <b>${(138.935 * q / rm).toFixed(1)} kJ/mol</b></span>`;
    }
    [sE, sS, sQ].forEach(s => s.addEventListener('input', upd)); upd();
    host.append(el('div', 'w-cap', 'Defaults are close to the oxygen–oxygen parameters of TIP3P water (σ = 0.315 nm, ε = 0.64 kJ/mol). The product of two water-like partial charges, 0.4 × 0.4 = 0.16 e², already gives a Coulomb term tens of times larger than ε. The vertical axis rescales when you add charge, so watch the Lennard-Jones well shrink to a dimple.'));
  }

  /* ---------- demo 2: integrators on a harmonic oscillator ---------- */
  function wIntegrators(host) {
    host.append(el('h4', '', 'Try it: three integrators on one spring'),
      el('p', 'sub', 'A harmonic oscillator with m = k = 1 (period 2π ≈ 6.28). The exact energy is constant. Change the time step and compare how each method treats the energy over 30 periods.'));
    const c = el('div', 'w-controls'); host.append(c);
    const sD = slider(c, 'time step Δt', 0.02, 2.2, 0.02, 0.5, v => v.toFixed(2));
    const row = el('div', 'w-row'); host.append(row);
    const a = el('div'), b = el('div'); row.append(a, b);
    const pE = new Plot(a, { xLabel: 'time (periods)', yLabel: 'energy / exact energy', yRange: [0, 3], xRange: [0, 30], height: 260 });
    const pP = new Plot(b, { xLabel: 'position x', yLabel: 'momentum p', xRange: [-2.2, 2.2], yRange: [-2.2, 2.2], height: 260, hover: false });
    const st = el('div', 'w-stats'); host.append(st);
    function run(method, dt, T) {
      let x = 1, v = 0; const n = Math.floor(T / dt), ts = [0], es = [1], xs = [1], ps = [0];
      for (let i = 1; i <= n; i++) {
        if (method === 'euler') { const xn = x + v * dt; v = v - x * dt; x = xn; }
        else if (method === 'vv') { v -= 0.5 * dt * x; x += dt * v; v -= 0.5 * dt * x; }
        else { // RK4
          const k1x = v, k1v = -x, k2x = v + 0.5 * dt * k1v, k2v = -(x + 0.5 * dt * k1x), k3x = v + 0.5 * dt * k2v, k3v = -(x + 0.5 * dt * k2x), k4x = v + dt * k3v, k4v = -(x + dt * k3x);
          x += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v);
        }
        const e = x * x + v * v; ts.push(i * dt / 6.283185307); es.push(isFinite(e) ? Math.min(e, 1e6) : 1e6);
        if (i * dt < 4 * 6.2832) { xs.push(Math.abs(x) < 50 ? x : NaN); ps.push(Math.abs(v) < 50 ? v : NaN); }
      }
      return { ts, es, xs, ps };
    }
    function upd() {
      const dt = +sD.value, T = 30 * 6.283185307;
      const e = run('euler', dt, T), v = run('vv', dt, T), r = run('rk4', dt, T);
      pE.set([{ name: 'Forward Euler', color: '--s2', x: e.ts, y: e.es }, { name: 'Velocity Verlet', color: '--s1', x: v.ts, y: v.es }, { name: 'Runge–Kutta 4', color: '--s3', x: r.ts, y: r.es }]);
      const th = linspace(0, 6.2832, 100);
      pP.set([{ name: 'Exact orbit', color: '--axis', x: th.map(Math.cos), y: th.map(Math.sin), width: 1.5 }, { name: 'Forward Euler', color: '--s2', x: e.xs, y: e.ps, width: 1.5 }, { name: 'Velocity Verlet', color: '--s1', x: v.xs, y: v.ps, width: 1.5 }, { name: 'Runge–Kutta 4', color: '--s3', x: r.xs, y: r.ps, width: 1.5 }]);
      const last = arr => arr[arr.length - 1], vmax = Math.max.apply(null, v.es), vmin = Math.min.apply(null, v.es);
      st.innerHTML = `<span>steps per period: <b>${(6.2832 / dt).toFixed(1)}</b></span><span>Euler after 30 periods: <b>×${fmt(last(e.es))}</b></span><span>Verlet stays within <b>${fmt(vmin)} – ${fmt(vmax)}</b></span><span>RK4 after 30 periods: <b>×${fmt(last(r.es))}</b></span>` + (dt >= 2 ? '<span><b>Δt ≥ 2/ω: Verlet is unstable too.</b></span>' : '');
    }
    sD.addEventListener('input', upd); upd();
    host.append(el('div', 'w-cap', 'Left: energy. Right: the first four periods in phase space. Forward Euler spirals outward for every Δt. Velocity Verlet stays on a slightly deformed closed orbit (it conserves a "shadow" energy) until Δt reaches 2/ω. RK4 is more accurate per step but slowly loses energy, and it needs four force evaluations per step.'));
  }

  /* ---------- demo 3: a 2D Lennard-Jones fluid ---------- */
  function wMD2D(host) {
    host.append(el('h4', '', 'Try it: a live molecular dynamics simulation'),
      el('p', 'sub', '49 Lennard-Jones particles in two dimensions with periodic boundaries, in reduced units (σ = ε = m = k_B = 1). This is a complete MD code: forces, velocity Verlet, an optional Langevin thermostat.'));
    const c = el('div', 'w-controls'); host.append(c);
    const bRun = button(c, 'Start', true), bReset = button(c, 'Reset');
    const sDt = slider(c, 'Δt', 0.001, 0.03, 0.001, 0.005, v => v.toFixed(3));
    const lab = el('label', '', 'thermostat '); const sel = document.createElement('select');
    sel.innerHTML = '<option value="off">off (NVE)</option><option value="on">Langevin (NVT)</option>'; lab.append(sel); c.append(lab);
    const sT = slider(c, 'target T', 0.1, 2.5, 0.05, 0.8, v => v.toFixed(2));
    const row = el('div', 'w-row'); host.append(row);
    const left = el('div', 'w-plot'), right = el('div'); row.append(left, right);
    const cv = document.createElement('canvas'); left.append(cv);
    cv.setAttribute('role', 'img'); cv.setAttribute('aria-label', 'Particles moving in a periodic box');
    const p = new Plot(right, { xLabel: 'time (reduced units)', yLabel: 'energy per particle', height: 300 });
    const st = el('div', 'w-stats'); host.append(st);
    const N = 49, rho = 0.45, L = Math.sqrt(N / rho), rc2 = 6.25, s6c = Math.pow(1 / rc2, 3), ush = 4 * (s6c * s6c - s6c);
    let x, y, vx, vy, fx, fy, pe, t, hist, running = false, e0, tSum, tN, dead = false;
    function forces() {
      fx.fill(0); fy.fill(0); pe = 0;
      for (let i = 0; i < N - 1; i++) for (let j = i + 1; j < N; j++) {
        let dx = x[i] - x[j], dy = y[i] - y[j]; dx -= L * Math.round(dx / L); dy -= L * Math.round(dy / L);
        const r2 = dx * dx + dy * dy;
        if (r2 < rc2) { const ir2 = 1 / r2, s6 = ir2 * ir2 * ir2, ff = 24 * (2 * s6 * s6 - s6) * ir2; fx[i] += ff * dx; fy[i] += ff * dy; fx[j] -= ff * dx; fy[j] -= ff * dy; pe += 4 * (s6 * s6 - s6) - ush; }
      }
    }
    const ke = () => { let k = 0; for (let i = 0; i < N; i++) k += vx[i] * vx[i] + vy[i] * vy[i]; return 0.5 * k; };
    function reset() {
      x = new Float64Array(N); y = new Float64Array(N); vx = new Float64Array(N); vy = new Float64Array(N); fx = new Float64Array(N); fy = new Float64Array(N);
      const n = Math.round(Math.sqrt(N)), a = L / n, T = +sT.value; let sx = 0, sy = 0;
      for (let i = 0; i < N; i++) { x[i] = (i % n + 0.5) * a; y[i] = (Math.floor(i / n) + 0.5) * a; vx[i] = Math.sqrt(T) * gauss(); vy[i] = Math.sqrt(T) * gauss(); sx += vx[i]; sy += vy[i]; }
      for (let i = 0; i < N; i++) { vx[i] -= sx / N; vy[i] -= sy / N; }
      t = 0; hist = { t: [], k: [], u: [], e: [] }; tSum = 0; tN = 0; dead = false; forces(); e0 = null; drawAll();
    }
    function step(dt, thermo, T) {
      const h = 0.5 * dt;
      for (let i = 0; i < N; i++) { vx[i] += h * fx[i]; vy[i] += h * fy[i]; }
      if (thermo) {
        const c1 = Math.exp(-1.0 * dt), c2 = Math.sqrt(T * (1 - c1 * c1));
        for (let i = 0; i < N; i++) { x[i] += h * vx[i]; y[i] += h * vy[i]; vx[i] = c1 * vx[i] + c2 * gauss(); vy[i] = c1 * vy[i] + c2 * gauss(); x[i] += h * vx[i]; y[i] += h * vy[i]; }
      } else for (let i = 0; i < N; i++) { x[i] += dt * vx[i]; y[i] += dt * vy[i]; }
      for (let i = 0; i < N; i++) { x[i] -= L * Math.floor(x[i] / L); y[i] -= L * Math.floor(y[i] / L); }
      forces();
      for (let i = 0; i < N; i++) { vx[i] += h * fx[i]; vy[i] += h * fy[i]; }
      t += dt;
    }
    function drawAll() {
      const w = left.clientWidth || 300, dpr = window.devicePixelRatio || 1, sz = Math.min(w, 300);
      cv.width = Math.round(sz * dpr); cv.height = Math.round(sz * dpr); cv.style.width = sz + 'px'; cv.style.height = sz + 'px';
      const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, sz, sz);
      g.strokeStyle = cssv('--axis'); g.lineWidth = 1; g.strokeRect(0.5, 0.5, sz - 1, sz - 1);
      const sc = sz / L, rad = 0.5 * sc; g.fillStyle = cssv('--s1'); g.strokeStyle = cssv('--surface'); g.lineWidth = 1.5;
      for (let i = 0; i < N; i++) for (let ox = -1; ox <= 1; ox++) for (let oy = -1; oy <= 1; oy++) {
        const px = (x[i] + ox * L) * sc, py = (y[i] + oy * L) * sc;
        if (px < -rad || px > sz + rad || py < -rad || py > sz + rad) continue;
        g.beginPath(); g.arc(px, py, rad * 0.92, 0, 6.2832); g.fill(); g.stroke();
      }
      const k = ke(), e = k + pe; if (e0 == null) e0 = e;
      p.set([{ name: 'kinetic', color: '--s2', x: hist.t, y: hist.k }, { name: 'potential', color: '--s3', x: hist.t, y: hist.u }, { name: 'total', color: '--s1', x: hist.t, y: hist.e }]);
      st.innerHTML = dead ? '<span><b>The simulation blew up: two particles overlapped because the time step was too large. Reset and use a smaller Δt.</b></span>'
        : `<span>t = <b>${t.toFixed(1)}</b></span><span>instantaneous T = <b>${(k / N).toFixed(3)}</b></span><span>mean T = <b>${tN ? (tSum / tN).toFixed(3) : '–'}</b></span><span>total-energy change since start = <b>${(100 * (e - e0) / Math.abs(e0)).toFixed(3)} %</b></span>`;
    }
    function frame() {
      if (!running) return;
      const dt = +sDt.value, thermo = sel.value === 'on', T = +sT.value;
      for (let s = 0; s < 8; s++) step(dt, thermo, T);
      const k = ke(), e = k + pe;
      if (!isFinite(e) || Math.abs(e) / N > 1e4) { dead = true; running = false; bRun.textContent = 'Start'; drawAll(); return; }
      hist.t.push(t); hist.k.push(k / N); hist.u.push(pe / N); hist.e.push(e / N); tSum += k / N; tN++;
      if (hist.t.length > 500) { hist.t.shift(); hist.k.shift(); hist.u.shift(); hist.e.shift(); }
      drawAll(); requestAnimationFrame(frame);
    }
    bRun.addEventListener('click', () => { if (dead) reset(); running = !running; bRun.textContent = running ? 'Pause' : 'Start'; if (running) requestAnimationFrame(frame); });
    bReset.addEventListener('click', () => { running = false; bRun.textContent = 'Start'; reset(); });
    const bD = button(c, 'Download energies (CSV)');
    bD.addEventListener('click', () => downloadCSV('toy_lj_energies.csv', ['time', 'kinetic_per_particle', 'potential_per_particle', 'total_per_particle'], hist.t.map((tt, i) => [+tt.toFixed(4), hist.k[i], hist.u[i], hist.e[i]])));
    sel.addEventListener('change', () => { e0 = null; tSum = 0; tN = 0; });
    window.addEventListener('mdc-redraw', () => drawAll());
    reset();
    host.append(el('div', 'w-cap', 'Things to try: (1) thermostat off, Δt = 0.005: kinetic and potential energy trade places while the total stays flat. (2) Raise Δt towards 0.03 and watch the total energy drift, then explode. (3) Thermostat on: the total energy is no longer conserved, but the mean temperature settles on the target. (4) Set T = 0.2 and watch the particles condense into a droplet.'));
  }

  /* ---------- demo 4: umbrella sampling and WHAM on a double well ---------- */
  function wUmbrella(host) {
    host.append(el('h4', '', 'Try it: why plain MD fails on a barrier, and how umbrella sampling fixes it'),
      el('p', 'sub', 'One particle in the double well U(x) = h (x² − 1)², energies in units of k_BT, moved by overdamped Langevin dynamics. Both methods get the same total number of steps (400,000).'));
    const c = el('div', 'w-controls'); host.append(c);
    const sH = slider(c, 'barrier h (k_BT)', 2, 14, 0.5, 8, v => v.toFixed(1));
    const sM = slider(c, 'windows', 5, 25, 1, 15, v => String(v));
    const sK = slider(c, 'spring k', 5, 120, 5, 40, v => String(v));
    const bP = button(c, 'Run plain MD'), bU = button(c, 'Run umbrella + WHAM', true), bC = button(c, 'Clear');
    const row = el('div', 'w-row'); host.append(row);
    const a = el('div'), b = el('div'); row.append(a, b);
    const pF = new Plot(a, { xLabel: 'x', yLabel: 'free energy (k_BT)', xRange: [-1.8, 1.8], height: 280 });
    const pH = new Plot(b, { xLabel: 'x', yLabel: 'probability density', xRange: [-1.8, 1.8], height: 280 });
    const st = el('div', 'w-stats'); host.append(st);
    const NB = 90, X0 = -1.8, X1 = 1.8, DX = (X1 - X0) / NB, xc = linspace(X0 + DX / 2, X1 - DX / 2, NB), DT = 0.001, TOTAL = 400000;
    let plain = null, umb = null, job = 0;
    const U = (x, h) => h * (x * x - 1) * (x * x - 1), dU = (x, h) => 4 * h * x * (x * x - 1);
    const bin = x => Math.floor((x - X0) / DX);
    function exact() { const h = +sH.value; return xc.map(x => U(x, h)); }
    function fromHist(H) { const tot = H.reduce((s, v) => s + v, 0); const F = H.map(v => v > 0 ? -Math.log(v / tot / DX) : NaN); const mn = Math.min.apply(null, F.filter(isFinite)); return F.map(v => v - mn); }
    function wham(win, h) {
      const M = win.length, f = new Float64Array(M), P = new Float64Array(NB), bias = win.map(wn => xc.map(x => 0.5 * wn.k * (x - wn.c) * (x - wn.c)));
      for (let it = 0; it < 400; it++) {
        for (let j = 0; j < NB; j++) { let num = 0, den = 0; for (let i = 0; i < M; i++) { num += win[i].H[j]; den += win[i].n * Math.exp(-(bias[i][j] - f[i])); } P[j] = den > 0 ? num / den : 0; }
        let dmax = 0;
        for (let i = 0; i < M; i++) { let z = 0; for (let j = 0; j < NB; j++) z += P[j] * Math.exp(-bias[i][j]); const nf = z > 0 ? -Math.log(z) : f[i]; dmax = Math.max(dmax, Math.abs(nf - f[i])); f[i] = nf; }
        if (dmax < 1e-6) break;
      }
      const F = Array.from(P, v => v > 0 ? -Math.log(v) : NaN); const mn = Math.min.apply(null, F.filter(isFinite)); return F.map(v => v - mn);
    }
    function rms(F, ex) { let s = 0, n = 0; for (let j = 0; j < NB; j++) if (Math.abs(xc[j]) < 1.4 && isFinite(F[j])) { s += (F[j] - ex[j]) * (F[j] - ex[j]); n++; } const cov = n / xc.filter(v => Math.abs(v) < 1.4).length; return { rms: n ? Math.sqrt(s / n) : NaN, cov }; }
    function draw() {
      const h = +sH.value, ex = exact();
      const sF = [{ name: 'exact U(x)', color: '--axis', x: xc, y: ex, width: 3 }], sHs = [];
      let txt = '';
      if (plain) { const F = fromHist(plain.H); sF.push({ name: 'plain MD', color: '--s2', x: xc, y: F }); const tot = plain.n || 1; sHs.push({ name: 'plain MD histogram', color: '--s2', x: xc, y: plain.H.map(v => v / tot / DX) }); const r = rms(F, ex); txt += `<span>plain MD: barrier crossings <b>${plain.cross}</b>, covers <b>${(100 * r.cov).toFixed(0)} %</b> of the range, RMS error <b>${fmt(r.rms)} k<sub>B</sub>T</b></span>`; }
      if (umb) { umb.win.forEach((wn, i) => { if (wn.n) sHs.push({ name: i === 0 ? 'umbrella windows (one curve each)' : '', color: '--s1', x: xc, y: wn.H.map(v => v / wn.n / DX), width: 1.5 }); }); if (umb.F) { sF.push({ name: 'umbrella + WHAM', color: '--s1', x: xc, y: umb.F }); const r = rms(umb.F, ex); txt += `<span>umbrella + WHAM: covers <b>${(100 * r.cov).toFixed(0)} %</b>, RMS error <b>${fmt(r.rms)} k<sub>B</sub>T</b></span>`; } }
      pF.set(sF, { yRange: [-0.5, Math.max(6, h * 1.6)] }); pH.set(sHs.length ? sHs : [{ name: '', color: '--axis', x: [X0, X1], y: [0, 0] }]);
      st.innerHTML = txt || '<span>Press a button to run.</span>';
    }
    function runPlain() {
      const my = ++job, h = +sH.value; plain = { H: new Float64Array(NB), n: 0, cross: 0 }; let x = -1, side = -1, done = 0; const sq = Math.sqrt(2 * DT);
      (function chunk() {
        if (my !== job) return;
        for (let s = 0; s < 20000; s++) { x += -dU(x, h) * DT + sq * gauss(); const j = bin(x); if (j >= 0 && j < NB) { plain.H[j]++; plain.n++; } if (side < 0 && x > 0.7) { side = 1; plain.cross++; } else if (side > 0 && x < -0.7) { side = -1; plain.cross++; } }
        done += 20000; draw(); if (done < TOTAL) requestAnimationFrame(chunk);
      })();
    }
    function runUmb() {
      const my = ++job, h = +sH.value, M = +sM.value, k = +sK.value, per = Math.floor(TOTAL / M), sq = Math.sqrt(2 * DT);
      umb = { win: linspace(-1.5, 1.5, M).map(cn => ({ c: cn, k, H: new Float64Array(NB), n: 0 })), F: null }; let i = 0;
      (function chunk() {
        if (my !== job) return;
        const wn = umb.win[i]; let x = wn.c;
        for (let s = 0; s < per; s++) { x += -(dU(x, h) + wn.k * (x - wn.c)) * DT + sq * gauss(); if (s < 500) continue; const j = bin(x); if (j >= 0 && j < NB) { wn.H[j]++; wn.n++; } }
        i++; if (i >= 2) umb.F = wham(umb.win.slice(0, i), h); draw(); if (i < M) requestAnimationFrame(chunk);
      })();
    }
    const bD = button(c, 'Download windows (CSV)');
    bD.addEventListener('click', () => { if (!umb) return; const rows = []; umb.win.forEach(wn => { for (let j = 0; j < NB; j++) rows.push([+wn.c.toFixed(4), wn.k, +xc[j].toFixed(4), wn.H[j]]); }); downloadCSV('toy_umbrella_windows.csv', ['window_centre', 'spring_k', 'x_bin_centre', 'count'], rows); });
    bP.addEventListener('click', runPlain); bU.addEventListener('click', runUmb);
    bC.addEventListener('click', () => { job++; plain = null; umb = null; draw(); });
    sH.addEventListener('input', () => { job++; plain = null; umb = null; draw(); });
    draw();
    host.append(el('div', 'w-cap', 'Things to try: (1) h = 8: plain MD usually stays in the left well, so its free energy is wrong or missing on the right. (2) h = 3: plain MD crosses often and works. (3) Umbrella with only 5 windows and k = 120: the histograms stop overlapping and WHAM cannot connect them. (4) Soft springs (k = 5) on a high barrier: the windows slide off the barrier top.'));
  }

  /* ---------- helpers shared with demos2.js ---------- */
  function downloadCSV(name, header, rows) {
    const text = header.join(',') + '\n' + rows.map(r => r.map(v => (typeof v === 'number' ? (Number.isInteger(v) ? v : +v.toPrecision(7)) : v)).join(',')).join('\n') + '\n';
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv' })); a.download = name;
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
  function steps(edges, counts) {                         // histogram outline as a line: x and y arrays
    const x = [], y = []; for (let i = 0; i < counts.length; i++) { x.push(edges[i], edges[i + 1]); y.push(counts[i], counts[i]); } return { x, y };
  }
  /* section videos: play a lecture inside the page */
  function initVideos() {
    document.addEventListener('click', ev => {
      const a = ev.target.closest('a.sv[data-yt]'); if (!a || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
      ev.preventDefault();
      const box = a.closest('.secvideos'); let pl = box.querySelector('.sv-player');
      const same = pl && pl.dataset.yt === a.dataset.yt;
      if (pl) pl.remove(); box.querySelectorAll('a.sv').forEach(x => x.classList.remove('playing'));
      if (same) return;
      pl = el('div', 'sv-player'); pl.dataset.yt = a.dataset.yt;
      const start = a.dataset.start ? '&start=' + a.dataset.start : '';
      pl.innerHTML = `<div class="sv-frame"><iframe src="https://www.youtube-nocookie.com/embed/${a.dataset.yt}?rel=0${start}" title="${a.textContent.replace(/"/g, '')}" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe></div><div class="sv-under"><a href="${a.href}" target="_blank" rel="noopener">Open on YouTube</a> · <a href="#" class="sv-close">close</a></div>`;
      box.appendChild(pl); a.classList.add('playing');
      pl.querySelector('.sv-close').addEventListener('click', e => { e.preventDefault(); pl.remove(); a.classList.remove('playing'); });
    });
  }

  const WIDGETS = { lj: wLJ, integrators: wIntegrators, md2d: wMD2D, umbrella: wUmbrella };
  window.MDC = { el, $, $$, cssv, fmt, Plot, slider, button, gauss, linspace, steps, downloadCSV, widgets: WIDGETS };
  document.addEventListener('DOMContentLoaded', () => {
    renderMath(); initChrome(); initVideos();
    $$('.widget[data-widget]').forEach(h => { const f = WIDGETS[h.dataset.widget]; if (f) { try { f(h); } catch (e) { h.textContent = 'This demo could not start: ' + e.message; } } });
  });
})();
