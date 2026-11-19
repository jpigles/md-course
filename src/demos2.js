/* Molecular Dynamics course: the toy-data playgrounds (one per module).
   Every demo generates its own small data set in the browser and can hand it to you as a CSV file.
   Uses the helpers exported by course.js as window.MDC. */
(function () {
  'use strict';
  const { el, fmt, Plot, slider, button, gauss, linspace, steps, downloadCSV, widgets } = window.MDC;

  function select(parent, label, options) {
    const l = el('label', '', label + ' '); const s = document.createElement('select');
    s.innerHTML = options.map(o => `<option value="${o[0]}">${o[1]}</option>`).join(''); l.append(s); parent.append(l); return s;
  }
  function head(host, title, sub) { host.append(el('h4', '', title), el('p', 'sub', sub)); const c = el('div', 'w-controls'); host.append(c); return c; }
  function row(host) { const r = el('div', 'w-row'); host.append(r); const a = el('div'), b = el('div'); r.append(a, b); return [a, b]; }
  function hist(values, lo, hi, nb) { const h = new Float64Array(nb), w = (hi - lo) / nb; let n = 0; for (const v of values) { const j = Math.floor((v - lo) / w); if (j >= 0 && j < nb) { h[j]++; n++; } } return { h, w, n, edges: linspace(lo, hi, nb + 1) }; }
  const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
  const sd = a => { const m = mean(a); return Math.sqrt(a.reduce((s, v) => s + (v - m) * (v - m), 0) / Math.max(1, a.length - 1)); };
  function erfc(x) { const z = Math.abs(x), t = 1 / (1 + 0.5 * z); const r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))))))); return x >= 0 ? r : 2 - r; }

  /* ---------- module 2: Liouville's theorem ---------- */
  widgets.liouville = function (host) {
    const c = head(host, 'Try it: a cloud of initial conditions in phase space',
      'The blue outline encloses a set of starting points (x, p). Every point follows Hamilton\'s equations. Watch the shape stretch and fold while its area stays the same, then switch on friction.');
    const sys = select(c, 'system', [['ho', 'harmonic oscillator'], ['pend', 'pendulum'], ['dw', 'double well']]);
    const sG = slider(c, 'friction γ', 0, 0.5, 0.01, 0, v => v.toFixed(2));
    const bRun = button(c, 'Start', true), bReset = button(c, 'Reset');
    const p = new Plot(host, { xLabel: 'position x', yLabel: 'momentum p', hover: false, height: 330 });
    const st = el('div', 'w-stats'); host.append(st);
    const F = { ho: x => -x, pend: x => -Math.sin(x), dw: x => -4 * x * (x * x - 1) };
    const R = { ho: [[-2.5, 2.5], [-2.5, 2.5]], pend: [[-3.6, 3.6], [-2.8, 2.8]], dw: [[-2, 2], [-2.8, 2.8]] };
    const START = { ho: [1.2, 0.6, 0.4], pend: [1.5, 0.8, 0.4], dw: [0.9, 1.0, 0.3] };
    const ORB = { ho: [[0.6, 0], [1.2, 0], [1.8, 0], [2.3, 0]], pend: [[0.8, 0], [1.8, 0], [2.7, 0], [3.1, 0], [-3.6, 2.2], [3.6, -2.2]], dw: [[1.25, 0], [1.4, 0], [1.6, 0], [1.8, 0], [-1.25, 0]] };
    let xs, ps, t, a0, running = false, orbits = [];
    const area = () => { let a = 0; const n = xs.length; for (let i = 0; i < n; i++) { const j = (i + 1) % n; a += xs[i] * ps[j] - xs[j] * ps[i]; } return Math.abs(a) / 2; };
    function reset() {
      const k = sys.value, f = F[k]; orbits = [];
      for (const [x0, p0] of ORB[k]) { let x = x0, q = p0; const ox = [x], op = [q]; for (let i = 0; i < 1400; i++) { q += 0.005 * f(x); x += 0.01 * q; q += 0.005 * f(x); ox.push(x); op.push(q); } orbits.push({ name: '', color: '--line', x: ox, y: op, width: 1 }); }
      const [cx, cp, r] = START[k]; xs = []; ps = [];
      for (let i = 0; i < 240; i++) { const a = 6.283185307 * i / 240; xs.push(cx + r * Math.cos(a)); ps.push(cp + r * Math.sin(a)); }
      t = 0; a0 = area(); draw();
    }
    function draw() {
      const k = sys.value;
      p.set(orbits.concat([{ name: 'cloud', color: '--s1', x: xs.concat([xs[0]]), y: ps.concat([ps[0]]), width: 2 }]), { xRange: R[k][0], yRange: R[k][1] });
      const g = +sG.value;
      st.innerHTML = `<span>time = <b>${t.toFixed(1)}</b></span><span>area / initial area = <b>${(area() / a0).toFixed(3)}</b></span><span>expected e<sup>−γt</sup> = <b>${Math.exp(-g * t).toFixed(3)}</b></span><span>boundary points: <b>${xs.length}</b></span>`;
    }
    function frame() {
      if (!running) return;
      const f = F[sys.value], g = +sG.value, dt = 0.01, damp = Math.exp(-g * dt);
      for (let s = 0; s < 6; s++) { for (let i = 0; i < xs.length; i++) { let q = ps[i] + 0.5 * dt * f(xs[i]); const x = xs[i] + dt * q; q += 0.5 * dt * f(x); xs[i] = x; ps[i] = q * damp; } t += dt; }
      if (xs.length < 6000) {                       // keep the outline resolved as it stretches
        const nx = [], np = []; const n = xs.length;
        for (let i = 0; i < n; i++) { const j = (i + 1) % n; nx.push(xs[i]); np.push(ps[i]); if (Math.hypot(xs[j] - xs[i], ps[j] - ps[i]) > 0.05) { nx.push(0.5 * (xs[i] + xs[j])); np.push(0.5 * (ps[i] + ps[j])); } }
        xs = nx; ps = np;
      }
      draw(); requestAnimationFrame(frame);
    }
    bRun.addEventListener('click', () => { running = !running; bRun.textContent = running ? 'Pause' : 'Start'; if (running) requestAnimationFrame(frame); });
    bReset.addEventListener('click', () => { running = false; bRun.textContent = 'Start'; reset(); });
    sys.addEventListener('change', () => { running = false; bRun.textContent = 'Start'; reset(); });
    reset();
    host.append(el('div', 'w-cap', 'Grey curves are trajectories. With γ = 0 the outlined area is conserved to within the resolution of the outline (Liouville\'s theorem), however distorted the shape becomes: in the pendulum and the double well, points with more energy run ahead and the cloud is sheared into a spiral. With friction the area shrinks as e^(−γt): the flow is no longer Hamiltonian.'));
  };

  /* ---------- module 3: the Boltzmann distribution ---------- */
  widgets.boltzmann = function (host) {
    const c = head(host, 'Try it: watch a trajectory build the Boltzmann distribution',
      'One particle moves in a one-dimensional potential under thermal noise. The histogram of where it has been converges to exp(−U/k_BT)/Z. Change the temperature and the potential.');
    const pot = select(c, 'potential', [['dw', 'double well'], ['tilt', 'tilted double well'], ['ho', 'harmonic']]);
    const sT = slider(c, 'k_BT', 0.3, 3, 0.05, 1, v => v.toFixed(2));
    const bRun = button(c, 'Start', true), bReset = button(c, 'Reset'), bD = button(c, 'Download samples (CSV)');
    const [a, b] = row(host);
    const pU = new Plot(a, { xLabel: 'x', yLabel: 'potential energy U(x)', xRange: [-2.2, 2.2], yRange: [-1.5, 8], height: 260 });
    const pH = new Plot(b, { xLabel: 'x', yLabel: 'probability density', xRange: [-2.2, 2.2], height: 260 });
    const st = el('div', 'w-stats'); host.append(st);
    const U = { dw: x => 4 * (x * x - 1) ** 2, tilt: x => 4 * (x * x - 1) ** 2 + 0.8 * x, ho: x => 2 * x * x };
    const dU = { dw: x => 16 * x * (x * x - 1), tilt: x => 16 * x * (x * x - 1) + 0.8, ho: x => 4 * x };
    const xs = linspace(-2.2, 2.2, 221); let x, samples, running = false, nsteps;
    function exact() { const T = +sT.value, u = U[pot.value]; const w = xs.map(v => Math.exp(-u(v) / T)); const dx = xs[1] - xs[0]; const Z = w.reduce((s, v) => s + v, 0) * dx; const pR = xs.reduce((s, v, i) => s + (v > 0 ? w[i] : 0), 0) * dx / Z; const eU = xs.reduce((s, v, i) => s + u(v) * w[i], 0) * dx / Z; return { p: w.map(v => v / Z), pR, eU }; }
    function reset() { x = pot.value === 'ho' ? 0 : -1; samples = []; nsteps = 0; draw(); }
    function draw() {
      const u = U[pot.value], ex = exact();
      pU.set([{ name: 'U(x)', color: '--s1', x: xs, y: xs.map(u) }]);
      const h = hist(samples, -2.2, 2.2, 55), s = steps(h.edges, Array.from(h.h, v => h.n ? v / h.n / h.w : 0));
      pH.set([{ name: 'histogram of the trajectory', color: '--s2', x: s.x, y: s.y, width: 1.5 }, { name: 'exp(−U/k_BT)/Z', color: '--s1', x: xs, y: ex.p }], { yRange: [0, Math.max.apply(null, ex.p) * 1.5] });
      const pR = samples.length ? samples.filter(v => v > 0).length / samples.length : NaN, eU = samples.length ? mean(samples.map(u)) : NaN;
      let txt = `<span>samples: <b>${samples.length}</b></span><span>⟨U⟩ sampled <b>${fmt(eU)}</b>, exact <b>${fmt(ex.eU)}</b></span>`;
      if (pot.value !== 'ho') txt += `<span>fraction with x &gt; 0: sampled <b>${fmt(pR)}</b>, exact <b>${fmt(ex.pR)}</b></span><span>ΔF(left→right) = −k_BT ln(p_R/p_L) = <b>${fmt(-(+sT.value) * Math.log(ex.pR / (1 - ex.pR)))}</b></span>`;
      st.innerHTML = txt;
    }
    function frame() {
      if (!running) return;
      const T = +sT.value, d = dU[pot.value], dt = 0.002, sq = Math.sqrt(2 * dt);
      for (let s = 0; s < 4000; s++) { x += -d(x) / T * dt + sq * gauss(); if (++nsteps % 20 === 0 && samples.length < 200000) samples.push(x); }
      draw(); requestAnimationFrame(frame);
    }
    bRun.addEventListener('click', () => { running = !running; bRun.textContent = running ? 'Pause' : 'Start'; if (running) requestAnimationFrame(frame); });
    bReset.addEventListener('click', reset); pot.addEventListener('change', reset); sT.addEventListener('input', reset);
    bD.addEventListener('click', () => downloadCSV('boltzmann_samples.csv', ['sample', 'x', 'U_over_kBT'], samples.map((v, i) => [i, v, U[pot.value](v) / (+sT.value)])));
    reset();
    host.append(el('div', 'w-cap', 'Things to try: (1) double well at k_BT = 1: after a few crossings the two peaks are equal. (2) k_BT = 0.3: the particle is trapped on one side and the histogram is wrong, although nothing in the trace warns you. This is the sampling problem. (3) Tilted well: the population ratio gives a free-energy difference. Compare it with the 0.8 × 2 = 1.6 difference in energy between the two minima, and note how it changes with temperature.'));
  };

  /* ---------- module 6: fit a torsion to toy quantum-chemistry data ---------- */
  widgets.torsionfit = function (host) {
    const c = head(host, 'Try it: fit torsion parameters to a toy quantum-chemistry scan',
      'The dots are a made-up dihedral scan: the "QM" energy minus the force-field energy computed without the torsion term, every 15°. Fit them with a three-term cosine series. This is how real torsion parameters are obtained.');
    const s1 = slider(c, 'k₁', -4, 12, 0.1, 2, v => v.toFixed(1)), s2 = slider(c, 'k₂', -4, 12, 0.1, 2, v => v.toFixed(1)), s3 = slider(c, 'k₃', -4, 12, 0.1, 2, v => v.toFixed(1));
    const bFit = button(c, 'Least-squares fit', true), bNew = button(c, 'New molecule'), bD = button(c, 'Download scan (CSV)');
    const p = new Plot(host, { xLabel: 'dihedral angle φ (degrees)', yLabel: 'energy (kJ/mol)', xRange: [-180, 180], height: 280 });
    const st = el('div', 'w-stats'); host.append(st);
    const phi = linspace(-180, 165, 24), rad = v => v * Math.PI / 180;
    const basis = f => [1, 1 + Math.cos(rad(f)), 1 + Math.cos(2 * rad(f) - Math.PI), 1 + Math.cos(3 * rad(f))];
    let E, truth;
    function gen() { truth = [0, 6 * Math.random(), 8 * Math.random(), 1 + 6 * Math.random()]; E = phi.map(f => { const bb = basis(f); return truth[1] * bb[1] + truth[2] * bb[2] + truth[3] * bb[3] + 0.35 * gauss(); }); const m = Math.min.apply(null, E); E = E.map(v => v - m); }
    function model(k, f) { const bb = basis(f); return k[1] * bb[1] + k[2] * bb[2] + k[3] * bb[3]; }
    function draw() {
      const k = [0, +s1.value, +s2.value, +s3.value];
      const off = mean(E.map((e, i) => e - model(k, phi[i])));            // best constant offset for these k
      const fine = linspace(-180, 180, 181);
      p.set([{ name: 'model: Σ kₙ[1 + cos(nφ − δₙ)]', color: '--s1', x: fine, y: fine.map(f => model(k, f) + off) }, { name: 'toy QM scan (residual)', color: '--s2', x: phi, y: E, points: true }]);
      const rmse = Math.sqrt(mean(E.map((e, i) => (e - model(k, phi[i]) - off) ** 2)));
      st.innerHTML = `<span>RMS error of the fit: <b>${rmse.toFixed(2)} kJ/mol</b></span><span>phases fixed at δ₁ = 0°, δ₂ = 180°, δ₃ = 0°</span><span>noise added to the toy data: 0.35 kJ/mol</span>`;
    }
    function lsq() {                                                      // normal equations, 4 unknowns
      const A = Array.from({ length: 4 }, () => new Float64Array(5));
      phi.forEach((f, i) => { const bb = basis(f); for (let r = 0; r < 4; r++) { for (let q = 0; q < 4; q++) A[r][q] += bb[r] * bb[q]; A[r][4] += bb[r] * E[i]; } });
      for (let i = 0; i < 4; i++) { let m = i; for (let r = i + 1; r < 4; r++) if (Math.abs(A[r][i]) > Math.abs(A[m][i])) m = r; [A[i], A[m]] = [A[m], A[i]]; for (let r = 0; r < 4; r++) if (r !== i) { const f = A[r][i] / A[i][i]; for (let q = i; q < 5; q++) A[r][q] -= f * A[i][q]; } }
      const k = A.map((r, i) => r[4] / r[i]);
      [s1, s2, s3].forEach((s, i) => { s.value = k[i + 1].toFixed(1); s.dispatchEvent(new Event('input')); });
    }
    [s1, s2, s3].forEach(s => s.addEventListener('input', draw));
    bFit.addEventListener('click', lsq); bNew.addEventListener('click', () => { gen(); draw(); });
    bD.addEventListener('click', () => downloadCSV('toy_torsion_scan.csv', ['phi_deg', 'E_residual_kJ_per_mol'], phi.map((f, i) => [f, E[i]])));
    gen(); draw();
    host.append(el('div', 'w-cap', 'Try to fit by hand first: k₃ sets the three-fold ripple, k₂ the difference between planar and perpendicular, k₁ the difference between cis and trans. Then press the least-squares button. The fit is linear in the kₙ, so it is solved in one step. The remaining error is the noise.'));
  };

  /* ---------- module 7: the Ewald split ---------- */
  widgets.ewald = function (host) {
    const c = head(host, 'Try it: split 1/r into a short-ranged and a smooth part',
      'The Ewald trick writes 1/r = erfc(αr)/r + erf(αr)/r. Move α and the cutoff and see which part is left for real space and which for reciprocal space.');
    const sA = slider(c, 'α (nm⁻¹)', 0.5, 6, 0.02, 3.12, v => v.toFixed(2)), sR = slider(c, 'cutoff r_c (nm)', 0.6, 1.4, 0.01, 1.0, v => v.toFixed(2));
    const p = new Plot(host, { xLabel: 'distance r (nm)', yLabel: 'potential of a unit charge (1/nm)', xRange: [0, 2], yRange: [0, 8], height: 280 });
    const st = el('div', 'w-stats'); host.append(st);
    const r = linspace(0.02, 2, 300);
    function draw() {
      const al = +sA.value, rc = +sR.value;
      p.set([{ name: '1/r (bare Coulomb)', color: '--axis', x: r, y: r.map(v => 1 / v), width: 3 }, { name: 'erfc(αr)/r, summed in real space', color: '--s1', x: r, y: r.map(v => erfc(al * v) / v) },
        { name: 'erf(αr)/r, summed in reciprocal space', color: '--s2', x: r, y: r.map(v => (1 - erfc(al * v)) / v) }, { name: 'cutoff', color: '--muted', x: [rc, rc], y: [0, 8], width: 1.5, dash: [5, 4] }]);
      const tol = erfc(al * rc);
      st.innerHTML = `<span>erfc(α r_c) = <b>${tol.toExponential(1)}</b> (the GROMACS setting ewald-rtol)</span><span>energy thrown away at the cutoff for two unit charges: <b>${(138.935 * tol / rc).toExponential(1)} kJ/mol</b> (bare Coulomb there: ${(138.935 / rc).toFixed(0)} kJ/mol)</span><span>width of the Gaussian cloud, 1/(α√2) = <b>${(1 / (al * Math.SQRT2)).toFixed(3)} nm</b></span><span>erf(αr)/r at r = 0: <b>${(2 * al / Math.sqrt(Math.PI)).toFixed(2)}</b> (finite, hence smooth)</span>`;
    }
    sA.addEventListener('input', draw); sR.addEventListener('input', draw); draw();
    host.append(el('div', 'w-cap', 'With the defaults (α = 3.12 nm⁻¹, r_c = 1.0 nm) the real-space term has fallen to 10⁻⁵ of the bare interaction at the cutoff. Lower α and the real-space part no longer fits inside the cutoff. Raise α and the smooth part becomes sharply peaked, so it needs a finer reciprocal-space grid.'));
  };

  /* ---------- module 8: thermostats and the distribution of temperature ---------- */
  widgets.thermostats = function (host) {
    const c = head(host, 'Try it: what each thermostat does to the temperature fluctuations',
      'A toy system of 24 independent oscillators at a target temperature of 1. The instantaneous temperature must fluctuate, with a known (gamma) distribution. Compare the thermostats against it.');
    const th = select(c, 'thermostat', [['csvr', 'stochastic velocity rescaling'], ['ber', 'Berendsen'], ['lan', 'Langevin'], ['none', 'none (NVE)']]);
    const sTau = slider(c, 'coupling time τ', 0.02, 5, 0.02, 0.5, v => v.toFixed(2));
    const bRun = button(c, 'Start', true), bReset = button(c, 'Reset'), bD = button(c, 'Download T(t) (CSV)');
    const [a, b] = row(host);
    const pT = new Plot(a, { xLabel: 'time', yLabel: 'instantaneous temperature', yRange: [0, 2.5], height: 250 });
    const pH = new Plot(b, { xLabel: 'instantaneous temperature', yLabel: 'probability density', xRange: [0, 2.5], height: 250 });
    const st = el('div', 'w-stats'); host.append(st);
    const N = 24, T0 = 1, dt = 0.02, w2 = Array.from({ length: N }, (_, i) => (0.5 + 1.5 * i / (N - 1)) ** 2);
    const tg = linspace(0.01, 2.5, 200), a_ = N / 2, th_ = 2 * T0 / N, gam = tg.map(v => Math.exp((a_ - 1) * Math.log(v) - v / th_ - a_ * Math.log(th_) - Math.log(39916800)));
    let x, v, t, Ts, running = false;
    const kin = () => { let k = 0; for (let i = 0; i < N; i++) k += v[i] * v[i]; return 0.5 * k; };
    function reset() { x = new Float64Array(N); v = new Float64Array(N); for (let i = 0; i < N; i++) { x[i] = Math.sqrt(T0 / w2[i]) * gauss(); v[i] = Math.sqrt(T0) * gauss(); } t = 0; Ts = []; draw(); }
    function step() {
      const mode = th.value, tau = +sTau.value;
      for (let i = 0; i < N; i++) { v[i] -= 0.5 * dt * w2[i] * x[i]; x[i] += dt * v[i]; v[i] -= 0.5 * dt * w2[i] * x[i]; }
      if (mode === 'ber') { const T = 2 * kin() / N, l = Math.sqrt(Math.max(0, 1 + dt / tau * (T0 / T - 1))); for (let i = 0; i < N; i++) v[i] *= l; }
      else if (mode === 'csvr') {
        const K = kin(), Kb = 0.5 * N * T0, cc = Math.exp(-dt / tau), r1 = gauss(); let s = 0; for (let i = 1; i < N; i++) { const g = gauss(); s += g * g; }
        const Kn = K + (1 - cc) * (Kb * (r1 * r1 + s) / N - K) + 2 * r1 * Math.sqrt(cc * (1 - cc) * K * Kb / N), al = Math.sqrt(Math.max(0, Kn / K));
        for (let i = 0; i < N; i++) v[i] *= al;
      } else if (mode === 'lan') { const c1 = Math.exp(-dt / tau), c2 = Math.sqrt(T0 * (1 - c1 * c1)); for (let i = 0; i < N; i++) v[i] = c1 * v[i] + c2 * gauss(); }
      t += dt;
    }
    function draw() {
      const n = Ts.length, last = Ts.slice(-500);
      pT.set([{ name: 'T(t)', color: '--s1', x: last.map((_, i) => (n - last.length + i) * dt * 5), y: last, width: 1.5 }]);
      const h = hist(Ts, 0, 2.5, 50), s = steps(h.edges, Array.from(h.h, q => h.n ? q / h.n / h.w : 0));
      pH.set([{ name: 'simulation', color: '--s1', x: s.x, y: s.y, width: 1.5 }, { name: 'canonical (gamma) distribution', color: '--s2', x: tg, y: gam }], { yRange: [0, 3.2] });
      st.innerHTML = n ? `<span>mean T = <b>${mean(Ts).toFixed(3)}</b> (target 1)</span><span>standard deviation = <b>${sd(Ts).toFixed(3)}</b>, canonical √(2/N) = <b>${Math.sqrt(2 / N).toFixed(3)}</b></span><span>samples: <b>${n}</b></span>` : '<span>Press Start.</span>';
    }
    function frame() { if (!running) return; for (let s = 0; s < 1500; s++) { step(); if (s % 5 === 0 && Ts.length < 300000) Ts.push(2 * kin() / N); } draw(); requestAnimationFrame(frame); }
    bRun.addEventListener('click', () => { running = !running; bRun.textContent = running ? 'Pause' : 'Start'; if (running) requestAnimationFrame(frame); });
    bReset.addEventListener('click', reset); th.addEventListener('change', reset); sTau.addEventListener('change', reset);
    bD.addEventListener('click', () => downloadCSV('thermostat_temperature.csv', ['time', 'T_inst'], Ts.map((q, i) => [+(i * dt * 5).toFixed(3), q])));
    reset();
    host.append(el('div', 'w-cap', 'Things to try: (1) Stochastic velocity rescaling and Langevin reproduce the gamma distribution for any τ. (2) Berendsen with τ = 0.05: the mean is right but the distribution is far too narrow. This is the "wrong ensemble". (3) No thermostat: these oscillators do not exchange energy, so the distribution is whatever the starting velocities gave. A thermostat is also what makes this toy system ergodic.'));
  };

  /* ---------- module 9: flexible bonds against SHAKE ---------- */
  widgets.shake = function (host) {
    const c = head(host, 'Try it: the time step with and without bond constraints',
      'A bent three-atom molecule tumbling in a plane. Its two bonds are very stiff, its angle is soft. The same motion is integrated twice: with flexible bonds, and with the bonds held rigid by SHAKE. Raise the time step.');
    const sD = slider(c, 'time step Δt', 0.002, 0.12, 0.002, 0.01, v => v.toFixed(3));
    const p = new Plot(host, { xLabel: 'time', yLabel: 'total-energy error (%)', yRange: [-20, 20], height: 260 });
    const st = el('div', 'w-stats'); host.append(st);
    const kb = 2500, ka = 20, th0 = 110 * Math.PI / 180;
    function angle(r, f) {                                  // energy of the angle term; adds forces to f
      const ax = r[0] - r[2], ay = r[1] - r[3], cx = r[4] - r[2], cy = r[5] - r[3], la = Math.hypot(ax, ay), lc = Math.hypot(cx, cy);
      const cs = Math.max(-1, Math.min(1, (ax * cx + ay * cy) / (la * lc))), th = Math.acos(cs), sn = Math.max(1e-6, Math.sin(th)), g = ka * (th - th0) / sn;
      const fax = g / la * (cx / lc - cs * ax / la), fay = g / la * (cy / lc - cs * ay / la), fcx = g / lc * (ax / la - cs * cx / lc), fcy = g / lc * (ay / la - cs * cy / lc);
      f[0] += fax; f[1] += fay; f[4] += fcx; f[5] += fcy; f[2] -= fax + fcx; f[3] -= fay + fcy; return 0.5 * ka * (th - th0) ** 2;
    }
    function bonds(r, f) { let u = 0; for (const [i, j] of [[0, 1], [1, 2]]) { const dx = r[2 * i] - r[2 * j], dy = r[2 * i + 1] - r[2 * j + 1], l = Math.hypot(dx, dy), g = -kb * (l - 1) / l; f[2 * i] += g * dx; f[2 * i + 1] += g * dy; f[2 * j] -= g * dx; f[2 * j + 1] -= g * dy; u += 0.5 * kb * (l - 1) ** 2; } return u; }
    const init = () => ({ r: [Math.sin(th0 / 2), Math.cos(th0 / 2), 0, 0, -Math.sin(th0 / 2), Math.cos(th0 / 2)], v: [0.6, -0.5, 0, 0.9, -0.6, -0.4] });
    function run(dt, rigid, T) {
      let { r, v } = init(); const n = Math.floor(T / dt), ts = [], es = []; let f = new Float64Array(6), e0 = null, iters = 0, maxdev = 0;
      const ener = () => { const ff = new Float64Array(6); let u = angle(r, ff); if (!rigid) u += bonds(r, ff); return u + 0.5 * v.reduce((s, q) => s + q * q, 0); };
      const force = () => { f = new Float64Array(6); angle(r, f); if (!rigid) bonds(r, f); };
      if (rigid) for (const [i, j] of [[0, 1], [1, 2]]) {          // remove velocity along the bonds at the start
        const dx = r[2 * i] - r[2 * j], dy = r[2 * i + 1] - r[2 * j + 1], q = ((v[2 * i] - v[2 * j]) * dx + (v[2 * i + 1] - v[2 * j + 1]) * dy) / 2;
        v[2 * i] -= q * dx; v[2 * i + 1] -= q * dy; v[2 * j] += q * dx; v[2 * j + 1] += q * dy;
      }
      force(); e0 = ener();
      for (let s = 0; s < n; s++) {
        const old = r.slice();
        for (let k = 0; k < 6; k++) { v[k] += 0.5 * dt * f[k]; r[k] += dt * v[k]; }
        if (rigid) {                                          // SHAKE: correct positions along the old bond vectors
          let it = 0, done = false;
          while (!done && it < 200) { done = true; it++; for (const [i, j] of [[0, 1], [1, 2]]) { const sx = old[2 * i] - old[2 * j], sy = old[2 * i + 1] - old[2 * j + 1], px = r[2 * i] - r[2 * j], py = r[2 * i + 1] - r[2 * j + 1], diff = px * px + py * py - 1; if (Math.abs(diff) > 1e-8) { done = false; const g = diff / (4 * (sx * px + sy * py)); r[2 * i] -= g * sx; r[2 * i + 1] -= g * sy; r[2 * j] += g * sx; r[2 * j + 1] += g * sy; } } }
          iters += it; for (let k = 0; k < 6; k++) v[k] = (r[k] - old[k]) / dt;
        }
        force(); for (let k = 0; k < 6; k++) v[k] += 0.5 * dt * f[k];
        if (rigid) for (const [i, j] of [[0, 1], [1, 2]]) {       // RATTLE: remove velocity along the bonds
          const dx = r[2 * i] - r[2 * j], dy = r[2 * i + 1] - r[2 * j + 1], q = ((v[2 * i] - v[2 * j]) * dx + (v[2 * i + 1] - v[2 * j + 1]) * dy) / 2;
          v[2 * i] -= q * dx; v[2 * i + 1] -= q * dy; v[2 * j] += q * dx; v[2 * j + 1] += q * dy;
        }
        for (const [i, j] of [[0, 1], [1, 2]]) maxdev = Math.max(maxdev, Math.abs(Math.hypot(r[2 * i] - r[2 * j], r[2 * i + 1] - r[2 * j + 1]) - 1));
        const e = ener(), err = 100 * (e - e0) / Math.abs(e0); ts.push((s + 1) * dt); es.push(isFinite(err) ? Math.max(-1e4, Math.min(1e4, err)) : 1e4);
        if (!isFinite(e) || Math.abs(err) > 1e4) break;
      }
      return { ts, es, iters: iters / Math.max(1, n), maxdev };
    }
    function draw() {
      const dt = +sD.value, fl = run(dt, false, 40), rg = run(dt, true, 40);
      p.set([{ name: 'flexible bonds', color: '--s2', x: fl.ts, y: fl.es }, { name: 'rigid bonds (SHAKE)', color: '--s1', x: rg.ts, y: rg.es }], { xRange: [0, 40] });
      const wmax = Math.sqrt(3 * kb), blown = fl.es.some(e => Math.abs(e) > 1000);
      st.innerHTML = `<span>fastest bond vibration: period <b>${(6.2832 / wmax).toFixed(3)}</b>, so flexible bonds need Δt &lt; 2/ω = <b>${(2 / wmax).toFixed(3)}</b></span><span>flexible: <b>${blown ? 'unstable, energy explodes' : 'stable, largest error ' + fmt(Math.max.apply(null, fl.es.map(Math.abs))) + ' %'}</b></span><span>SHAKE: largest error <b>${fmt(Math.max.apply(null, rg.es.map(Math.abs)))} %</b>, <b>${rg.iters.toFixed(1)}</b> iterations per step, bond length kept within <b>${rg.maxdev.toExponential(0)}</b></span>`;
    }
    sD.addEventListener('input', draw); draw();
    host.append(el('div', 'w-cap', 'The stiff bonds limit the flexible molecule to Δt below about 0.023. With the bonds constrained, the fastest motion left is the soft angle, and the same molecule can be integrated with a time step several times larger. This is exactly why constraining bonds to hydrogen allows 2 fs instead of 1 fs.'));
  };

  /* ---------- module 10: how big will my system be? ---------- */
  widgets.syscalc = function (host) {
    const c = head(host, 'Try it: size your system before you build it',
      'Estimates from the rules in this module: box volume from the solute size and the padding, 33.4 water molecules per nm³, 0.0602 ion pairs per nm³ for each 100 mM of salt.');
    const sM = slider(c, 'protein mass (kDa)', 2, 300, 1, 25, v => String(v)), sL = slider(c, 'longest dimension (nm)', 1.5, 20, 0.1, 5, v => v.toFixed(1)), sP = slider(c, 'padding per side (nm)', 0.8, 2.5, 0.05, 1.2, v => v.toFixed(2));
    const box = select(c, 'box', [['0.707', 'rhombic dodecahedron'], ['0.770', 'truncated octahedron'], ['1', 'cube']]);
    const sC = slider(c, 'salt (mM)', 0, 500, 10, 150, v => String(v)), sQ = slider(c, 'net charge (e)', -30, 30, 1, -4, v => (v > 0 ? '+' : '') + v);
    const sN = slider(c, 'run length (ns)', 10, 2000, 10, 500, v => String(v)), sS = slider(c, 'save every (ps)', 1, 200, 1, 20, v => String(v));
    const st = el('div', 'w-stats'); host.append(st);
    function draw() {
      const M = +sM.value, d = +sL.value + 2 * +sP.value, V = +box.value * d ** 3, Vp = 1.23 * M, Vw = Math.max(0, V - Vp), nw = Math.round(33.4 * Vw), pairs = Math.round(0.6022 * (+sC.value / 1000) * Vw), q = +sQ.value;
      const na = pairs + Math.max(0, -q), cl = pairs + Math.max(0, q), pa = Math.round(M * 1000 / 6.9), tot = pa + 3 * nw + na + cl, frames = Math.round(+sN.value * 1000 / +sS.value);
      st.innerHTML = `<span>distance between periodic copies: <b>${d.toFixed(1)} nm</b></span><span>box volume: <b>${V.toFixed(0)} nm³</b></span><span>protein: about <b>${pa.toLocaleString('en-US')}</b> atoms</span><span>water molecules: <b>${nw.toLocaleString('en-US')}</b></span><span>Na⁺: <b>${na}</b>, Cl⁻: <b>${cl}</b></span><span>total atoms: <b>${tot.toLocaleString('en-US')}</b> (${(100 * 3 * nw / tot).toFixed(0)} % of them water)</span><span>frames saved: <b>${frames.toLocaleString('en-US')}</b></span><span>trajectory, all atoms, uncompressed: <b>${(frames * tot * 12 / 1e9).toFixed(1)} GB</b>; protein only: <b>${(frames * pa * 12 / 1e9).toFixed(2)} GB</b></span>`;
    }
    [sM, sL, sP, sC, sQ, sN, sS].forEach(s => s.addEventListener('input', draw)); box.addEventListener('change', draw); draw();
    host.append(el('div', 'w-cap', 'Approximations: protein volume 1.23 nm³ per kDa, 6.9 Da per protein atom, three atoms per water, 12 bytes per atom per frame (compressed formats such as XTC are about three times smaller). Notice how the padding and the box shape change the atom count far more than the protein does, and how much disk you save by not storing the water.'));
  };

  /* ---------- module 11: correlated data and block averaging ---------- */
  widgets.blockavg = function (host) {
    const c = head(host, 'Try it: how many independent samples are in a trajectory?',
      'A toy "radius of gyration" time series with mean 1.50 nm, standard deviation 0.10 nm and a correlation time you choose. Block averaging finds the real error bar; dividing by √N does not.');
    const sTau = slider(c, 'correlation time (frames)', 1, 400, 1, 50, v => String(v)), sLen = slider(c, 'log₁₀ of the number of frames', 3, 5.3, 0.1, 4.3, v => Math.round(10 ** v).toLocaleString('en-US'));
    const bGen = button(c, 'Generate a new trajectory', true), bD = button(c, 'Download series (CSV)');
    const [a, b] = row(host);
    const pS = new Plot(a, { xLabel: 'frame', yLabel: 'toy R_g (nm)', height: 250 });
    const pB = new Plot(b, { xLabel: 'log₂ of the block length (frames)', yLabel: 'standard error of the mean (nm)', height: 250 });
    const st = el('div', 'w-stats'); host.append(st);
    let x = [];
    function gen() {
      const tau = +sTau.value, n = Math.round(10 ** +sLen.value), ph = Math.exp(-1 / tau), q = Math.sqrt(1 - ph * ph); x = new Float64Array(n); let v = gauss();
      for (let i = 0; i < n; i++) { v = ph * v + q * gauss(); x[i] = 1.5 + 0.1 * v; }
      const k = Math.max(1, Math.floor(n / 1500)), sx = [], sy = []; for (let i = 0; i < n; i += k) { sx.push(i); sy.push(x[i]); }
      pS.set([{ name: 'series', color: '--s1', x: sx, y: sy, width: 1 }]);
      const m = mean(x), s = sd(x), naive = s / Math.sqrt(n), g = (1 + ph) / (1 - ph), truth = 0.1 * Math.sqrt(g / n), bx = [], by = []; let plateau = 0;
      for (let L = 1; n / L >= 5; L *= 2) { const nb = Math.floor(n / L), bm = []; for (let j = 0; j < nb; j++) { let t = 0; for (let i = 0; i < L; i++) t += x[j * L + i]; bm.push(t / L); } const se = sd(bm) / Math.sqrt(nb); bx.push(Math.log2(L)); by.push(se); if (nb >= 16) plateau = Math.max(plateau, se); }
      pB.set([{ name: 'block-averaged estimate', color: '--s1', x: bx, y: by }, { name: 'naive σ/√N', color: '--s2', x: [bx[0], bx[bx.length - 1]], y: [naive, naive], dash: [6, 4] }, { name: 'true value for this model', color: '--s3', x: [bx[0], bx[bx.length - 1]], y: [truth, truth], dash: [2, 3] }], { yRange: [0, Math.max(truth, plateau) * 1.6] });
      st.innerHTML = `<span>mean = <b>${m.toFixed(4)} nm</b> (true 1.5000)</span><span>naive error σ/√N = <b>${naive.toExponential(1)}</b></span><span>block-average plateau = <b>${plateau.toExponential(1)}</b></span><span>true error = <b>${truth.toExponential(1)}</b></span><span>statistical inefficiency g = <b>${g.toFixed(0)}</b>, so <b>${Math.round(n / g).toLocaleString('en-US')}</b> independent samples in ${n.toLocaleString('en-US')} frames</span>`;
    }
    bGen.addEventListener('click', gen); sTau.addEventListener('change', gen); sLen.addEventListener('change', gen);
    bD.addEventListener('click', () => downloadCSV('toy_rg_series.csv', ['frame', 'rg_nm'], Array.from(x, (v, i) => [i, v])));
    gen();
    host.append(el('div', 'w-cap', 'Things to try: (1) correlation time 1: the naive and block estimates agree, the frames are independent. (2) correlation time 400 with 1,000 frames: the block curve never flattens. There are only one or two independent samples, and no honest error bar can be given. (3) Download the series and reproduce the plateau with the Python function in this module.'));
  };

  /* ---------- module 13: FEP in both directions and BAR ---------- */
  widgets.fep = function (host) {
    const c = head(host, 'Try it: free-energy perturbation against BAR on a toy system',
      'State A is a spring centred at 0 with stiffness 1. State B is a spring of stiffness k centred at d. The exact answer is ΔA = ½ k_BT ln k, whatever d is. Every estimate below is repeated 200 times to show its bias and its scatter.');
    const sDd = slider(c, 'shift d', 0, 5, 0.1, 1.5, v => v.toFixed(1)), sK = slider(c, 'stiffness k of B', 0.2, 6, 0.1, 2, v => v.toFixed(1)), sNn = slider(c, 'log₁₀ samples per state', 1, 4, 0.25, 2, v => String(Math.round(10 ** v)));
    const bGo = button(c, 'Resample', true), bD = button(c, 'Download one data set (CSV)');
    const p = new Plot(host, { xLabel: 'ΔU = U_B − U_A  (units of k_BT)', yLabel: 'probability density', height: 260 });
    const st = el('div', 'w-stats'); host.append(st);
    let last = null;
    function trial(d, k, n) {
      const dA = [], dB = [], xa = [], xb = [];
      for (let i = 0; i < n; i++) { const a = gauss(); xa.push(a); dA.push(0.5 * k * (a - d) ** 2 - 0.5 * a * a); const b = d + gauss() / Math.sqrt(k); xb.push(b); dB.push(0.5 * k * (b - d) ** 2 - 0.5 * b * b); }
      const lse = (arr, sgn) => { const m = Math.max.apply(null, arr.map(v => sgn * v)); return m + Math.log(arr.reduce((s, v) => s + Math.exp(sgn * v - m), 0) / arr.length); };
      const fwd = -lse(dA, -1), rev = lse(dB, +1);
      let lo = -60, hi = 60;
      for (let it = 0; it < 60; it++) { const C = 0.5 * (lo + hi); let g = 0; for (const v of dA) g += 1 / (1 + Math.exp(v - C)); for (const v of dB) g -= 1 / (1 + Math.exp(-(v - C))); if (g > 0) hi = C; else lo = C; }
      return { fwd, rev, bar: 0.5 * (lo + hi), dA, dB, xa, xb };
    }
    function go() {
      const d = +sDd.value, k = +sK.value, n = Math.round(10 ** +sNn.value), ex = 0.5 * Math.log(k), F = [], R = [], B = [];
      for (let t = 0; t < 200; t++) { last = trial(d, k, n); F.push(last.fwd); R.push(last.rev); B.push(last.bar); }
      const all = last.dA.concat(last.dB).sort((a, b) => a - b), lo = all[Math.floor(0.01 * all.length)], hi = all[Math.floor(0.99 * all.length)], pad = 0.1 * (hi - lo) + 0.5;
      const big = trial(d, k, 20000), hA = hist(big.dA, lo - pad, hi + pad, 60), hB = hist(big.dB, lo - pad, hi + pad, 60), sA = steps(hA.edges, Array.from(hA.h, v => v / big.dA.length / hA.w)), sB = steps(hB.edges, Array.from(hB.h, v => v / big.dB.length / hB.w));
      const top = Math.max(Math.max.apply(null, sA.y), Math.max.apply(null, sB.y)) * 1.15;
      p.set([{ name: 'ΔU sampled in state A', color: '--s1', x: sA.x, y: sA.y, width: 1.5 }, { name: 'ΔU sampled in state B', color: '--s2', x: sB.x, y: sB.y, width: 1.5 }, { name: 'exact ΔA', color: '--muted', x: [ex, ex], y: [0, top], dash: [5, 4], width: 1.5 }], { yRange: [0, top], xRange: [lo - pad, hi + pad] });
      const row_ = (nm, arr) => `<span>${nm}: <b>${mean(arr).toFixed(2)} ± ${sd(arr).toFixed(2)}</b> (bias ${(mean(arr) - ex >= 0 ? '+' : '') + (mean(arr) - ex).toFixed(2)})</span>`;
      st.innerHTML = `<span>exact ΔA = <b>${ex.toFixed(2)} k<sub>B</sub>T</b></span>` + row_('FEP from A', F) + row_('FEP from B', R) + row_('BAR', B);
    }
    [sDd, sK, sNn].forEach(s => s.addEventListener('change', go)); bGo.addEventListener('click', go);
    bD.addEventListener('click', () => { if (last) downloadCSV('toy_fep_samples.csv', ['sampled_in_state', 'x', 'dU_over_kBT'], last.xa.map((x, i) => ['A', x, last.dA[i]]).concat(last.xb.map((x, i) => ['B', x, last.dB[i]]))); });
    go();
    host.append(el('div', 'w-cap', 'The two histograms always cross at the exact ΔA (Crooks). Things to try: (1) d = 0.5: the histograms overlap and all three estimators agree. (2) d = 4 with 100 samples: the two one-sided estimates are biased in opposite directions by several k_BT, with small scatter, so each looks converged. BAR, which uses both sets, stays close. (3) Raise the number of samples and watch how slowly the one-sided estimates improve.'));
  };

  /* ---------- module 14: metadynamics ---------- */
  widgets.metad = function (host) {
    const c = head(host, 'Try it: well-tempered metadynamics fills a double well',
      'The same double well as in Module 12, U(x) = h (x² − 1)² in units of k_BT. Gaussian hills are dropped where the particle is, and their height shrinks as bias accumulates. The free energy is read from the bias.');
    const sH = slider(c, 'barrier h (k_BT)', 2, 12, 0.5, 8, v => v.toFixed(1)), sG = slider(c, 'bias factor γ', 1.5, 20, 0.5, 8, v => v.toFixed(1)), sW = slider(c, 'hill height w₀', 0.05, 1.5, 0.05, 0.4, v => v.toFixed(2)), sS = slider(c, 'hill width σ', 0.05, 0.4, 0.01, 0.12, v => v.toFixed(2));
    const bRun = button(c, 'Start', true), bReset = button(c, 'Reset');
    const [a, b] = row(host);
    const pF = new Plot(a, { xLabel: 'x', yLabel: 'energy (k_BT)', xRange: [-1.8, 1.8], height: 270 });
    const pX = new Plot(b, { xLabel: 'time', yLabel: 'position x', yRange: [-1.8, 1.8], height: 270 });
    const st = el('div', 'w-stats'); host.append(st);
    const NG = 181, gx = linspace(-1.8, 1.8, NG), dg = gx[1] - gx[0], DT = 0.001;
    let V, x, t, tr, hills, cross, side, running = false;
    const U = (q, h) => h * (q * q - 1) ** 2, dU = (q, h) => 4 * h * q * (q * q - 1);
    const interp = (arr, q) => { const u = (q - gx[0]) / dg, i = Math.max(0, Math.min(NG - 2, Math.floor(u))), f = u - i; return arr[i] * (1 - f) + arr[i + 1] * f; };
    function reset() { V = new Float64Array(NG); x = -1; t = 0; tr = { t: [], x: [] }; hills = 0; cross = 0; side = -1; draw(); }
    function draw() {
      const h = +sH.value, g = +sG.value, ex = gx.map(q => U(q, h)), est = Array.from(V, v => -g / (g - 1) * v), m = Math.min.apply(null, est), felt = gx.map((q, i) => U(q, h) + V[i]), mf = Math.min.apply(null, felt);
      pF.set([{ name: 'exact U(x)', color: '--axis', x: gx, y: ex, width: 3 }, { name: 'estimate from the bias', color: '--s1', x: gx, y: est.map(v => v - m) }, { name: 'U + bias: what the particle feels now', color: '--s2', x: gx, y: felt.map(v => v - mf), width: 1.5 }], { yRange: [-0.5, Math.max(6, h * 1.5)] });
      pX.set([{ name: 'x(t)', color: '--s1', x: tr.t, y: tr.x, width: 1 }]);
      let s = 0, n = 0; gx.forEach((q, i) => { if (Math.abs(q) < 1.3) { s += (est[i] - m - ex[i]) ** 2; n++; } });
      st.innerHTML = `<span>hills deposited: <b>${hills}</b></span><span>barrier crossings: <b>${cross}</b></span><span>height of the next hill: <b>${fmt(+sW.value * Math.exp(-interp(V, x) / (g - 1)))}</b></span><span>RMS error of the estimate: <b>${fmt(Math.sqrt(s / n))} k<sub>B</sub>T</b></span>`;
    }
    function frame() {
      if (!running) return;
      const h = +sH.value, g = +sG.value, w0 = +sW.value, sg = +sS.value, sq = Math.sqrt(2 * DT);
      for (let s = 0; s < 6000; s++) {
        const u = (x - gx[0]) / dg, i = Math.max(0, Math.min(NG - 2, Math.floor(u))), dV = (V[i + 1] - V[i]) / dg;
        x += -(dU(x, h) + dV) * DT + sq * gauss(); x = Math.max(-1.79, Math.min(1.79, x)); t += DT;
        if (side < 0 && x > 0.7) { side = 1; cross++; } else if (side > 0 && x < -0.7) { side = -1; cross++; }
        if (s % 300 === 0) { const w = w0 * Math.exp(-interp(V, x) / (g - 1)); for (let j = 0; j < NG; j++) V[j] += w * Math.exp(-((gx[j] - x) ** 2) / (2 * sg * sg)); hills++; }
        if (s % 600 === 0) { tr.t.push(t); tr.x.push(x); if (tr.t.length > 1500) { tr.t.shift(); tr.x.shift(); } }
      }
      draw(); requestAnimationFrame(frame);
    }
    bRun.addEventListener('click', () => { running = !running; bRun.textContent = running ? 'Pause' : 'Start'; if (running) requestAnimationFrame(frame); });
    bReset.addEventListener('click', () => { running = false; bRun.textContent = 'Start'; reset(); }); sH.addEventListener('change', reset);
    reset();
    host.append(el('div', 'w-cap', 'Watch three stages: the left well fills, the particle escapes and the right well fills, then it moves back and forth while the hills shrink and the estimate settles. Things to try: (1) γ = 2 on a barrier of 12: the residual barrier h/γ = 6 k_BT is still too high and crossings stay rare. (2) Large, wide hills: fast but rough. (3) Stop after the first crossing and look at the estimate. It is badly wrong on the right. One crossing is not convergence.'));
  };

  /* ---------- module 15: coarse-grained contact potentials and screening ---------- */
  widgets.cgpot = function (host) {
    const c = head(host, 'Try it: contact potentials and salt screening in coarse-grained models',
      'Left: three contact potentials with the same minimum and depth. Right: the Debye-Hückel interaction between two opposite unit charges, in units of k_BT, against ionic strength.');
    const sI = slider(c, 'log₁₀ ionic strength (M)', -2.3, 0, 0.05, -0.82, v => (10 ** v * 1000).toFixed(0) + ' mM'), sE = slider(c, 'dielectric constant ε_r', 10, 80, 1, 78, v => String(v));
    const [a, b] = row(host);
    const pC = new Plot(a, { xLabel: 'distance / native distance (r/σ)', yLabel: 'energy / ε', xRange: [0.85, 2.4], yRange: [-1.2, 1.2], height: 270 });
    const pD = new Plot(b, { xLabel: 'distance r (nm)', yLabel: 'energy (k_BT)', xRange: [0.3, 3], height: 270 });
    const st = el('div', 'w-stats'); host.append(st);
    const r = linspace(0.85, 2.4, 300), q = r.map(v => 1 / v);
    pC.set([{ name: 'Lennard-Jones 12-6', color: '--s1', x: r, y: q.map(s => s ** 12 - 2 * s ** 6) }, { name: 'Gō 12-10', color: '--s2', x: r, y: q.map(s => 5 * s ** 12 - 6 * s ** 10) }, { name: '12-10-6 with desolvation barrier', color: '--s3', x: r, y: q.map(s => 13 * s ** 12 - 18 * s ** 10 + 4 * s ** 6) }]);
    const rr = linspace(0.3, 3, 200);
    function draw() {
      const I = 10 ** +sI.value, er = +sE.value, lB = 138.935 / (er * 2.494), lD = 0.304 / Math.sqrt(I) * Math.sqrt(er / 78.4);
      pD.set([{ name: 'unscreened Coulomb / ε_r', color: '--axis', x: rr, y: rr.map(v => -lB / v), width: 3 }, { name: 'Debye-Hückel', color: '--s1', x: rr, y: rr.map(v => -lB / v * Math.exp(-v / lD)) }], { yRange: [Math.min(-3, -lB / 0.3 * 1.05), 0.3] });
      st.innerHTML = `<span>Debye length λ_D = <b>${lD.toFixed(2)} nm</b></span><span>Bjerrum length (where the bare interaction equals k_BT) = <b>${lB.toFixed(2)} nm</b></span><span>screened energy at 0.5 nm: <b>${(-lB / 0.5 * Math.exp(-0.5 / lD)).toFixed(2)} k<sub>B</sub>T</b>, at 1.0 nm: <b>${(-lB / 1.0 * Math.exp(-1 / lD)).toFixed(2)} k<sub>B</sub>T</b></span>`;
    }
    sI.addEventListener('input', draw); sE.addEventListener('input', draw); draw();
    host.append(el('div', 'w-cap', 'Left: the 12-10 well is narrower than Lennard-Jones, so a Gō contact is more specific about distance. The 12-10-6 form adds a small barrier (0.14 ε near 1.45 σ) that mimics the cost of squeezing out the last water layer. Right: at 150 mM a salt bridge at 0.5 nm keeps about half of its unscreened strength and is nearly gone by 2 nm. Lower ε_r to 20, as inside a protein interface, and the same charges interact several times more strongly: this is why a single uniform dielectric constant is the weak point of the model.'));
  };

  /* ---------- module 16: a Markov state model from toy data ---------- */
  widgets.msm = function (host) {
    const c = head(host, 'Try it: build a Markov state model from a toy trajectory',
      'A particle diffuses in a three-well potential. The trajectory is cut into 30 bins, transitions are counted at several lag times, and the eigenvalues of the transition matrix give the relaxation times.');
    const sW = slider(c, 'well depth (k_BT)', 2, 6, 0.25, 4, v => v.toFixed(2)), sL = slider(c, 'log₁₀ trajectory frames', 4, 5.6, 0.1, 5, v => Math.round(10 ** v).toLocaleString('en-US'));
    const bGo = button(c, 'Generate and analyse', true), bD = button(c, 'Download trajectory (CSV)');
    const [a, b] = row(host);
    const pT = new Plot(a, { xLabel: 'lag time τ', yLabel: 'implied time scale', height: 270 });
    const pP = new Plot(b, { xLabel: 'x', yLabel: 'equilibrium probability per bin', xRange: [-2.4, 2.4], height: 270 });
    const st = el('div', 'w-stats'); host.append(st);
    const NB = 30, X0 = -2.4, DX = 4.8 / NB, xc = linspace(X0 + DX / 2, 2.4 - DX / 2, NB), DT = 0.002, SAVE = 10;
    let traj = new Float64Array(0);
    const Uf = (x, w) => 0.05 * x ** 6 - w * (Math.exp(-((x + 1.4) ** 2) / 0.2) + 0.85 * Math.exp(-x * x / 0.2) + 1.1 * Math.exp(-((x - 1.4) ** 2) / 0.2));
    const dUf = (x, w) => 0.3 * x ** 5 + w * 10 * ((x + 1.4) * Math.exp(-((x + 1.4) ** 2) / 0.2) + 0.85 * x * Math.exp(-x * x / 0.2) + 1.1 * (x - 1.4) * Math.exp(-((x - 1.4) ** 2) / 0.2));
    function jacobi(A, n) {                                   // eigenvalues of a symmetric matrix
      for (let sweep = 0; sweep < 30; sweep++) { let off = 0; for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q]; if (off < 1e-18) break;
        for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) { if (Math.abs(A[p][q]) < 1e-14) continue; const th = (A[q][q] - A[p][p]) / (2 * A[p][q]), tt = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1)), cs = 1 / Math.sqrt(tt * tt + 1), sn = tt * cs;
          for (let k = 0; k < n; k++) { const akp = A[k][p], akq = A[k][q]; A[k][p] = cs * akp - sn * akq; A[k][q] = sn * akp + cs * akq; } for (let k = 0; k < n; k++) { const apk = A[p][k], aqk = A[q][k]; A[p][k] = cs * apk - sn * aqk; A[q][k] = sn * apk + cs * aqk; } } }
      return Array.from({ length: n }, (_, i) => A[i][i]).sort((x, y) => y - x);
    }
    function analyse(lag) {
      const C = Array.from({ length: NB }, () => new Float64Array(NB)), b = v => Math.max(0, Math.min(NB - 1, Math.floor((v - X0) / DX)));
      for (let i = 0; i + lag < traj.length; i++) C[b(traj[i])][b(traj[i + lag])]++;
      const keep = []; for (let i = 0; i < NB; i++) { let s = 0; for (let j = 0; j < NB; j++) s += C[i][j] + C[j][i]; if (s > 0) keep.push(i); }
      const n = keep.length, S = Array.from({ length: n }, () => new Float64Array(n)), cs = new Float64Array(n);
      keep.forEach((i, a_) => keep.forEach((j, b_) => { S[a_][b_] = 0.5 * (C[i][j] + C[j][i]); cs[a_] += S[a_][b_]; }));
      const tot = cs.reduce((s, v) => s + v, 0), pi = new Float64Array(NB); keep.forEach((i, a_) => { pi[i] = cs[a_] / tot; });
      for (let a_ = 0; a_ < n; a_++) for (let b_ = 0; b_ < n; b_++) S[a_][b_] /= Math.sqrt(cs[a_] * cs[b_]);
      return { ev: jacobi(S, n), pi };
    }
    function go() {
      const w = +sW.value, n = Math.round(10 ** +sL.value), sq = Math.sqrt(2 * DT); traj = new Float64Array(n); let x = -1.4, trans = 0, side = -1;
      for (let i = 0; i < n; i++) { for (let s = 0; s < SAVE; s++) x += -dUf(x, w) * DT + sq * gauss(); traj[i] = x; if (side < 0 && x > 1.0) { side = 1; trans++; } else if (side > 0 && x < -1.0) { side = -1; trans++; } }
      const lags = [1, 2, 5, 10, 20, 50, 100, 200, 500].filter(l => l < n / 20), t1 = [], t2 = [], lt = [], fr = DT * SAVE; let res = null;
      for (const l of lags) { res = analyse(l); const e = res.ev; lt.push(l * fr); t1.push(e[1] > 0 && e[1] < 1 ? -l * fr / Math.log(e[1]) : NaN); t2.push(e[2] > 0 && e[2] < 1 ? -l * fr / Math.log(e[2]) : NaN); }
      pT.set([{ name: 'slowest process', color: '--s1', x: lt, y: t1 }, { name: 'second slowest', color: '--s2', x: lt, y: t2 }, { name: 'time scale = lag (nothing faster can be resolved)', color: '--muted', x: lt, y: lt, dash: [4, 4], width: 1.5 }], { yRange: [0, Math.max.apply(null, t1.filter(isFinite).concat([1])) * 1.3] });
      const bz = xc.map(v => Math.exp(-Uf(v, w))), Z = bz.reduce((s, v) => s + v, 0), first = analyse(lags[Math.min(3, lags.length - 1)]);
      pP.set([{ name: 'exact Boltzmann', color: '--axis', x: xc, y: bz.map(v => v / Z), width: 3 }, { name: 'stationary distribution of the model', color: '--s1', x: xc, y: Array.from(first.pi), points: true, r: 3.5 }]);
      st.innerHTML = `<span>frames: <b>${n.toLocaleString('en-US')}</b> (total time ${fmt(n * fr)})</span><span>left ↔ right transitions seen: <b>${trans}</b></span><span>slowest relaxation time at the longest lag: <b>${fmt(t1[t1.length - 1])}</b></span>`;
    }
    bGo.addEventListener('click', go); bD.addEventListener('click', () => downloadCSV('toy_three_well_trajectory.csv', ['frame', 'time', 'x'], Array.from(traj, (v, i) => [i, +(i * DT * SAVE).toFixed(3), v])));
    go();
    host.append(el('div', 'w-cap', 'Read the left plot the way you would for a real model: the implied time scales rise at short lags (the bins are not Markovian yet) and should level off. Choose the lag where they are flat. Things to try: (1) well depth 6 with 10,000 frames: only a handful of transitions, the slow time scale never levels off and the populations are wrong. (2) More frames at the same depth. (3) Download the trajectory and build the transition matrix yourself with NumPy.'));
  };

  /* ---------- module 17: a neural network fitted to toy energies ---------- */
  widgets.nnfit = function (host) {
    const c = head(host, 'Try it: train a small neural network on toy energies, then leave the training range',
      'The reference energy is the double well E(x) = (x² − 1)². A network with two hidden layers of 16 units is trained on energies sampled only inside the range you choose. Forces are obtained by differentiating the network.');
    const sR = slider(c, 'training range ±', 0.5, 2.0, 0.05, 1.2, v => v.toFixed(2)), sM = slider(c, 'training points', 4, 60, 1, 16, v => String(v));
    const bTr = button(c, 'Train', true), bNew = button(c, 'New data and new network');
    const [a, b] = row(host);
    const pE = new Plot(a, { xLabel: 'x', yLabel: 'energy', xRange: [-2.3, 2.3], yRange: [-1.5, 8], height: 270 });
    const pFo = new Plot(b, { xLabel: 'x', yLabel: 'force −dE/dx', xRange: [-2.3, 2.3], yRange: [-20, 20], height: 270 });
    const st = el('div', 'w-stats'); host.append(st);
    const H = 16, NP = H + H + H * H + H + H + 1, xs = linspace(-2.3, 2.3, 185), Et = x => (x * x - 1) ** 2, Ft = x => -4 * x * (x * x - 1);
    let w, mA, vA, step, xt, yt, job = 0;
    function init() { w = new Float64Array(NP); for (let i = 0; i < NP; i++) w[i] = 0.6 * gauss() / Math.sqrt(i < 2 * H ? 1 : H); mA = new Float64Array(NP); vA = new Float64Array(NP); step = 0; }
    function data() { const R = +sR.value, M = +sM.value; xt = Array.from({ length: M }, () => (2 * Math.random() - 1) * R); yt = xt.map(Et); }
    function fwd(x, a1, a2) { let o = w[NP - 1]; for (let i = 0; i < H; i++) a1[i] = Math.tanh(w[i] * x + w[H + i]); for (let j = 0; j < H; j++) { let s = w[2 * H + H * H + j]; for (let i = 0; i < H; i++) s += w[2 * H + j * H + i] * a1[i]; a2[j] = Math.tanh(s); o += w[2 * H + H * H + H + j] * a2[j]; } return o; }
    function train(n) {
      const a1 = new Float64Array(H), a2 = new Float64Array(H), g = new Float64Array(NP), d2 = new Float64Array(H), d1 = new Float64Array(H); let loss = 0;
      for (let it = 0; it < n; it++) {
        g.fill(0); loss = 0;
        for (let k = 0; k < xt.length; k++) {
          const y = fwd(xt[k], a1, a2), e = y - yt[k], dy = 2 * e / xt.length; loss += e * e / xt.length; g[NP - 1] += dy; d1.fill(0);
          for (let j = 0; j < H; j++) { g[2 * H + H * H + H + j] += dy * a2[j]; d2[j] = dy * w[2 * H + H * H + H + j] * (1 - a2[j] * a2[j]); g[2 * H + H * H + j] += d2[j]; for (let i = 0; i < H; i++) { g[2 * H + j * H + i] += d2[j] * a1[i]; d1[i] += d2[j] * w[2 * H + j * H + i]; } }
          for (let i = 0; i < H; i++) { const d = d1[i] * (1 - a1[i] * a1[i]); g[i] += d * xt[k]; g[H + i] += d; }
        }
        step++; const lr = 0.01;
        for (let i = 0; i < NP; i++) { mA[i] = 0.9 * mA[i] + 0.1 * g[i]; vA[i] = 0.999 * vA[i] + 0.001 * g[i] * g[i]; w[i] -= lr * (mA[i] / (1 - 0.9 ** step)) / (Math.sqrt(vA[i] / (1 - 0.999 ** step)) + 1e-8); }
      }
      return loss;
    }
    function draw(loss) {
      const a1 = new Float64Array(H), a2 = new Float64Array(H), R = +sR.value, pe = xs.map(x => fwd(x, a1, a2)), pf = xs.map(x => -(fwd(x + 1e-4, a1, a2) - fwd(x - 1e-4, a1, a2)) / 2e-4);
      pE.set([{ name: 'reference energy', color: '--axis', x: xs, y: xs.map(Et), width: 3 }, { name: 'network', color: '--s1', x: xs, y: pe }, { name: 'training data', color: '--s2', x: xt, y: yt, points: true, r: 3.5 },
        { name: '', color: '--muted', x: [-R, -R], y: [-1.5, 8], dash: [4, 4], width: 1 }, { name: '', color: '--muted', x: [R, R], y: [-1.5, 8], dash: [4, 4], width: 1 }]);
      pFo.set([{ name: 'reference force', color: '--axis', x: xs, y: xs.map(Ft), width: 3 }, { name: 'network force', color: '--s1', x: xs, y: pf }, { name: '', color: '--muted', x: [-R, -R], y: [-20, 20], dash: [4, 4], width: 1 }, { name: '', color: '--muted', x: [R, R], y: [-20, 20], dash: [4, 4], width: 1 }]);
      let si = 0, ni = 0, so = 0, no = 0; xs.forEach((x, i) => { const e = (pf[i] - Ft(x)) ** 2; if (Math.abs(x) <= R) { si += e; ni++; } else { so += e; no++; } });
      st.innerHTML = `<span>training steps: <b>${step}</b></span><span>training loss (energies): <b>${loss == null ? '–' : loss.toExponential(1)}</b></span><span>force error inside the training range: <b>${fmt(Math.sqrt(si / ni))}</b></span><span>outside it: <b>${no ? fmt(Math.sqrt(so / no)) : '–'}</b></span>`;
    }
    function run() { const my = ++job; let n = 0; (function f() { if (my !== job) return; const l = train(60); n += 60; draw(l); if (n < 4200) requestAnimationFrame(f); })(); }
    bTr.addEventListener('click', run); bNew.addEventListener('click', () => { job++; data(); init(); draw(null); });
    sR.addEventListener('change', () => { job++; data(); init(); draw(null); }); sM.addEventListener('change', () => { job++; data(); init(); draw(null); });
    data(); init(); draw(null);
    host.append(el('div', 'w-cap', 'Dashed lines mark the edge of the training data. Inside, a few dozen points are enough for good energies and good forces. Outside, the network has no reason to follow the reference: the walls of the well are missing, and a simulation run with this model would walk out of the training range and never come back. Things to try: (1) train on ±0.7 only: the barrier region is covered and both minima are not. (2) Four points: the energies are fitted perfectly and the forces between them are wrong. Energies alone under-determine the model, which is why real potentials are trained on forces too.'));
  };
})();
