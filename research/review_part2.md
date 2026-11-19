# Technical review, modules 07 to 12

Reviewer's scope: every equation, number, attribution and software claim in
07-boundaries-electrostatics.md, 08-thermostats-barostats.md, 09-constraints.md,
10-running-a-simulation.md, 11-analysis-statistics.md and 12-free-energy-pmf.md.
I ran the arithmetic with `wsl python3` and checked attributions against Crossref.
I checked software claims against manual.gromacs.org (mdp options, current
release), docs.openmm.org and the OpenMM source (`openmm/app/modeller.py`, master).
Findings are identified by quotation, not by line number.

---

## 07-boundaries-electrostatics.md

### 07-1. What the reciprocal-space energy is the energy of
- **Quote**: "The energy $\tfrac12\int\rho\,\phi$ of the clouds then becomes $U_{recip} = \frac{2\pi}{V}\sum_{\mathbf k\neq0}\frac{e^{-k^2/4\alpha^2}}{k^2}|S(\mathbf k)|^2$", and later "The reciprocal sum includes the interaction of each Gaussian cloud with itself".
- **Problem**: The formula is right, but it is not the cloud-cloud energy. The cloud-cloud energy $\tfrac12\int\rho_G\phi_G$ has two Gaussian factors, $|\tilde\rho|^2 = |S|^2e^{-k^2/2\alpha^2}$, which corresponds to an $\mathrm{erf}(\alpha r/\sqrt2)/r$ pair term. The single factor $e^{-k^2/4\alpha^2}$ comes from the energy of the **point charges** in the potential of the clouds, $\tfrac12\sum_iq_i\phi_G(\mathbf r_i)$. That is also the only reading consistent with the split $1/r=\mathrm{erfc}/r+\mathrm{erf}/r$ and with the self term $-\alpha/\sqrt\pi\sum q_i^2$. The cloud-cloud self term would be $-\alpha/\sqrt{2\pi}\sum q_i^2$.
- **Correct**: "The energy $\tfrac12\sum_iq_i\,\phi_G(\mathbf r_i)$ of the point charges in the potential $\phi_G$ of the smooth clouds then becomes ..." and "The reciprocal sum includes the interaction of each point charge with its own Gaussian cloud, which is not physical. Remove it:"
- **Evidence**: $\phi_G(\mathbf k)=4\pi S(\mathbf k)e^{-k^2/4\alpha^2}/k^2$. Evaluating it at the point charges gives $\frac{1}{2V}\sum_{\mathbf k}\frac{4\pi}{k^2}e^{-k^2/4\alpha^2}|S|^2=\frac{2\pi}{V}\sum\ldots$ (the formula in the text). Using $\int\rho_G\phi_G$ instead gives $e^{-k^2/2\alpha^2}$. Self term: $\lim_{r\to0}\mathrm{erf}(\alpha r)/r=2\alpha/\sqrt\pi$, times $\tfrac12q_i^2$, gives $\alpha q_i^2/\sqrt\pi$, which is the point-in-own-cloud energy.
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: surface-layer fraction for 10,000 waters (25.8 %); minimum image and $r_c\le L/2$; box volumes 0.770 and 0.707 $d^3$; potential-shift is the GROMACS default `vdw-modifier`; LJ tail energy $\frac83\pi N\rho\varepsilon\sigma^3[\frac13(\sigma/r_c)^9-(\sigma/r_c)^3]$ (re-derived); $P_{tail}$ in exercise 2 (Frenkel-Smit form); sign of the pressure correction and the effect on density; Verlet skin criterion $\delta/2$; cell list of 27 cells, $O(N)$; `verlet-buffer-tolerance`, `DispCorr = EnerPres`; 139 kJ/mol for two unit charges at 1 nm (138.9); normalisation of $\rho^G$; potential $q\,\mathrm{erf}(\alpha r)/r$; Fourier coefficient $e^{-k^2/4\alpha^2}$; Poisson equation in k-space; $U_{recip}$ prefactor $2\pi/V$; $U_{self}$; $U_{excl}$; tin-foil boundary condition and neutralising background for the omitted $\mathbf k=0$ term; $\alpha$-independence; $O(N^{3/2})$ for classical Ewald; Darden-York-Pedersen 1993 and Essmann et al. 1995; $4^3=64$ points for order 4 (cubic); `fourierspacing` (default 0.12 nm), `pme-order`, `ewald-rtol` default $10^{-5}$ with $\mathrm{erfc}(\alpha r_c)=$ rtol; $\alpha=3.123$ nm$^{-1}$ at $r_c=1.0$ nm; the reaction-field formula with $k_{rf}$ and $c_{rf}$ (GROMACS form) and zero force at $r_c$ for $\varepsilon_{rf}=\infty$; check-yourself answers 1 to 4 (7.2 nm; 8.0 to 8.4 nm); Madelung constant 1.7476 and the 8-ion NaCl cell.

---

## 08-thermostats-barostats.md

### 08-1. Parrinello-Rahman grouped with methods that sample exact NPT
- **Quote**: "Martyna, Tobias, Klein and Tuckerman corrected the equations so that they sample the exact NPT ensemble (MTTK). These methods are correct for a well-equilibrated system."
- **Problem**: "These methods" covers Parrinello-Rahman, but the MTK/MTTK correction was made to the Hoover-type isotropic barostat equations, not to Parrinello-Rahman. The Parrinello-Rahman equations as implemented in GROMACS are not proven to give the exact NPT volume distribution. The GROMACS documentation itself warns that Parrinello-Rahman may not be appropriate when exact NPT fluctuations matter. The production row of the protocol table is still fine for averages.
- **Correct**: "Martyna, Tobias and Klein (1994), and later Martyna, Tuckerman, Tobias and Klein (1996, MTTK), derived extended-system equations that sample the exact NPT ensemble. Parrinello-Rahman, the form most used in GROMACS, gives correct averages for a well-equilibrated system, but its volume fluctuations are not guaranteed to be exactly those of NPT. Use MTTK, stochastic cell rescaling or Monte Carlo when the fluctuations themselves matter."
- **Evidence**: manual.gromacs.org/current/user-guide/mdp-options.html, `pcoupl = Parrinello-Rahman`. The page warns that for simulations where the exact NPT fluctuations are important, the method may not be appropriate. Bernetti & Bussi 2020 (doi 10.1063/5.0020514) list Parrinello-Rahman among second-order barostats without claiming it is exact.
- **Severity**: misleading
- **Confidence**: medium

### 08-2. "No instantaneous pressure is reported" by the Monte Carlo barostat
- **Quote**: "This is OpenMM's `MonteCarloBarostat` and an option in AMBER. No instantaneous pressure is reported."
- **Problem**: The barostat does not need a pressure, but OpenMM can compute one. `MonteCarloBarostat.computeCurrentPressure(context)` returns the instantaneous pressure, using the molecular virial with a finite-difference $\partial U/\partial V$.
- **Correct**: "It does not need the pressure to run; in OpenMM the instantaneous pressure can still be obtained on request with `MonteCarloBarostat.computeCurrentPressure(context)`."
- **Evidence**: docs.openmm.org/latest/api-python/generated/openmm.openmm.MonteCarloBarostat.html. The method is documented as computing the instantaneous pressure of a system under this barostat.
- **Severity**: imprecise
- **Confidence**: high

### 08-3. Meaning of $N$ in the Monte Carlo acceptance rule
- **Quote**: "$P_{acc} = \min\{1,\ \exp[-\beta(\Delta U + P_0\Delta V) + N\ln\frac{V'}{V}]\}$" after "scale the coordinates of molecular centres"
- **Problem**: $N$ is not defined. Because the text scales molecular centres, $N$ must be the number of molecules (scaled centres), not the number of atoms. Using the atom count gives the wrong density. The rule also assumes the trial move is uniform in $V$; for moves uniform in $\ln V$ the exponent is $(N+1)\ln(V'/V)$.
- **Correct**: "... $+\,N_{mol}\ln\frac{V'}{V}$, where $N_{mol}$ is the number of independently scaled centres (molecules when molecules are scaled as rigid bodies, atoms when every atom is scaled), for trial volumes drawn uniformly in $V$."
- **Evidence**: The Jacobian of scaling $N_{mol}$ centre-of-mass coordinates is $(V'/V)^{N_{mol}}$. The internal coordinates are unchanged. OpenMM's `scaleMoleculesAsRigid=True` default scales by molecule centroid (same OpenMM doc page).
- **Severity**: imprecise
- **Confidence**: medium

Checked and found correct: relative $T$ fluctuation $\sqrt{2/N_{df}}$; gamma distribution of $K$; Berendsen $\lambda^2$ and Berendsen 1984; SVR equation $dK=(\bar K-K)dt/\tau_T+2\sqrt{K\bar K/(N_{df}\tau_T)}\,dW$ (Bussi, Donadio, Parrinello 2007, doi 10.1063/1.2408420); `tcoupl = V-rescale`; Langevin equation and the fluctuation-dissipation amplitude; OU variance $\sigma^2/2\gamma$; exact O-step; Brownian dynamics with $D=k_BT/m\gamma$; Nosé-Hoover equations; phase-space divergence $-N_{df}\xi$; generalised Liouville sign; the full $d\ln f/dt$ check (re-derived); Martyna-Klein-Tuckerman 1992 NHC; $\tau_T$ as an oscillation period (GROMACS doc); the virial pressure $P=\frac{2}{3V}(K-\Xi)$, $\Xi=-\frac12\sum r_{ij}\cdot F_{ij}$ and tensor $\frac2V(\mathbf K-\boldsymbol\Xi)$ (GROMACS convention, consistent with the virial theorem); $\kappa_T=4.5\times10^{-5}$ bar$^{-1}$ and 0.1 % gives 22 bar; $\langle\delta V^2\rangle=k_BT\langle V\rangle\kappa_T$; Berendsen barostat $\mu$; Andersen $W\ddot V=P-P_0$; Parrinello-Rahman 1981 (J. Appl. Phys., doi 10.1063/1.328693); **stochastic cell rescaling equation**, checked against Bernetti & Bussi 2020 eq. 5 (arXiv 2006.09250): the text matches exactly, because the $k_BT/V$ drift in the $V$ equation cancels under the Itô change of variable to $\varepsilon$; `pcoupl = C-rescale`; check-yourself answers (SE of a 100 ps pressure average, about 40 bar for $\sigma$ = 300 bar and $\tau$ = 1 ps); canonical variance of $K$, $\frac12N_{df}(k_BT)^2$.

---

## 09-constraints.md

### 09-1. "Configurational free energies depend only on U(r)" in a constrained system
- **Quote**: "Why it is legitimate: the equilibrium distribution of positions does not depend on masses (Module 3)" and (check-yourself 3) "No. Configurational free energies depend only on $U(\mathbf r)$."
- **Problem**: This is true for unconstrained systems. HMR is used together with constrained bonds to H, and with holonomic constraints the configurational distribution carries the mass-metric (Fixman) factor $\sqrt{\det\mathbf Z}$, $Z_{kl}=\sum_im_i^{-1}\nabla_i\sigma_k\cdot\nabla_i\sigma_l$. That factor depends on the masses, so HMR changes it. The module's own "Distributions" paragraph says the same thing. The effect is negligible for bond constraints, so the conclusion stands, but the stated reason is wrong.
- **Correct**: "No, to an excellent approximation. Without constraints the configurational distribution depends only on $U(\mathbf r)$. With bond constraints a small mass-dependent factor (the Fixman determinant) appears, which is negligible for bonds to hydrogen. Only kinetic quantities such as rates and diffusion constants change appreciably."
- **Evidence**: The Fixman correction. Integrating out the constrained momenta leaves $\propto\sqrt{\det\mathbf Z(\mathbf r)}\,e^{-\beta U}$, and $\mathbf Z$ contains $1/m_i$. HMR changes $m_H$ and $m_{heavy}$ in it.
- **Severity**: imprecise
- **Confidence**: medium

Checked and found correct: C-H stretch period 11 fs, $\hbar\omega/k_BT=14.4$ at 3000 cm$^{-1}$ and 300 K; H-X-H bend period of about 23 fs; constraint form and $\nabla_i\sigma=2\mathbf r_{ij}$; SHAKE displacement formula; $g=2\lambda\Delta t^2$ bookkeeping; the quadratic in $g$ and its linearisation (re-derived); Ryckaert-Ciccotti-Berendsen 1977; RATTLE (Andersen 1983, doi 10.1016/0021-9991(83)90014-1) and $\dot\sigma=2\mathbf r_{ij}\cdot\mathbf v_{ij}$; SETTLE (Miyamoto & Kollman 1992); LINCS (Hess, Bekker, Berendsen, Fraaije 1997, doi confirmed); the projection formula; the series expansion; `lincs-order = 4` and `lincs-iter = 1` defaults; the 30° LINCS warning angle (`lincs-warnangle` default 30); $N_{df}=3N-N_c-3$; check-yourself 1 (121,497); the constraint virial; Hopkins et al. 2015 (doi 10.1021/ct5010406); the $\sqrt{m'/m}$ frequency argument as an upper bound; check-yourself 2.

---

## 10-running-a-simulation.md

### 10-1. OpenMM `padding` is not the GROMACS `-d`: the OpenMM box gets half the clearance
- **Quote**: "`model.addSolvent(ff, padding=1.2 * unit.nanometer, ionicStrength=0.15 * unit.molar, boxShape="dodecahedron")`" under "The same workflow in OpenMM", next to the GROMACS line "`gmx editconf ... -d 1.2 -bt dodecahedron`" with the comment "at least 1.2 nm between the solute and the box faces".
- **Problem**: In OpenMM the box width is (diameter of the solute's bounding sphere) + `padding`. The solute is therefore guaranteed only `padding` = 1.2 nm from its nearest periodic image, which is 0.6 nm of water per side. `gmx editconf -d 1.2` with a triclinic box gives an image distance of diameter + 2 × 1.2 nm. The OpenMM script builds a much smaller box than the GROMACS one. It also breaks the module 7 rule ("at least 2.0 nm between copies"), even though it still exceeds the 1.0 nm cutoff.
- **Correct**: `model.addSolvent(ff, padding=2.4 * unit.nanometer, ionicStrength=0.15 * unit.molar, boxShape="dodecahedron")   # OpenMM padding = solute-image distance; 2.4 nm matches gmx editconf -d 1.2`
- **Evidence**: OpenMM source `wrappers/python/openmm/app/modeller.py`, `_computeBoxWidth`: `radius = max(norm(center-pos)); return max(2*radius+padding, 2*padding)`. The docstring says the box is set to (sphere diameter)+(padding), which guarantees no solute atom comes closer than the padding to any periodic image. GROMACS editconf help: with `-d` and a triclinic box, the image distance is the solute diameter plus 2 × d.
- **Severity**: misleading
- **Confidence**: high

Checked and found correct: `gmx pdb2gmx -ff amber99sb-ildn -water tip3p -ignh`, `editconf -c -d -bt dodecahedron`, `solvate -cp -cs spc216.gro -p`, `genion -pname NA -nname CL -neutral -conc 0.15` (`-conc` uses the cell volume); 0.0903 ion pairs per nm$^3$, 45 pairs in 500 nm$^3$, 370 waters per pair, 16.6 mM per pair in 100 nm$^3$; the steepest-descent update; em.mdp options (`steep`, `emtol`, `emstep` in nm); restraint fluctuation 0.05 nm per component at $k$ = 1000; the grompp/mdrun chain (`-r`, `-t`); the CHARMM settings (rvdw 1.2, rvdw-switch 1.0, Force-switch, rcoulomb 1.2, no DispCorr); every md.mdp option name and value (`integrator = md` leap-frog, `continuation`, `constraint-algorithm`, `lincs-iter/order`, `vdw-modifier = Potential-shift`, `DispCorr`, `fourierspacing`, `V-rescale`, `tc-grps`, `tau-t`, `ref-t`, `C-rescale`, `pcoupltype`, `tau-p`, `ref-p`, `compressibility`, `gen-vel`); 50,000,000 × 2 fs = 100 ns; 5000 steps = 10 ps; OpenMM imports, `ForceField("amber14-all.xml","amber14/tip3pfb.xml")`, `Modeller.addHydrogens(ff, pH=7.0)`, `boxShape="dodecahedron"`, `createSystem(... nonbondedMethod=app.PME, nonbondedCutoff, constraints=app.HBonds, hydrogenMass=4*amu)`, `MonteCarloBarostat(1 bar, 300 K)` signature, `LangevinMiddleIntegrator(T, friction, dt)`, `Simulation`, `minimizeEnergy`, `setVelocitiesToTemperature`, `DCDReporter`, `StateDataReporter(... density=True, speed=True)`, `CheckpointReporter`; 125,000 × 4 fs = 500 ps, 2500 × 4 fs = 10 ps, 25,000,000 × 4 fs = 100 ns; `compressed-x-grps`; `gmx mindist -pi`; `trjconv -pbc mol -center`; check-yourself 1 (31 pairs; 37 Na$^+$, 31 Cl$^-$).

---

## 11-analysis-statistics.md

### 11-1. Statistical inefficiency is off by one with the integral definition of $\tau_{int}$
- **Quote**: "$\tau_{int}=\int_0^\infty c(t)\,dt$ ... $g = 1+\frac{2\tau_{int}}{\Delta t_s}$"
- **Problem**: With $\tau_{int}$ defined as the continuous integral from 0, the discrete statistical inefficiency is $g=1+2\sum_{k\ge1}c(k\Delta t_s)\approx 2\tau_{int}/\Delta t_s$, not $1+2\tau_{int}/\Delta t_s$. The trapezoid rule gives $\sum_{k\ge1}c\approx\tau_{int}/\Delta t_s-\tfrac12$. The formula $g=1+2\tau/\Delta t_s$ is correct only when $\tau$ is the discrete sum $\Delta t_s\sum_{k\ge1}c(k\Delta t_s)$, which is what the Python function computes. The difference is negligible when $\tau\gg\Delta t_s$, as in check-yourself 1 (1001 vs 1000), and the boxed approximation $\sigma_A\sqrt{2\tau_{int}/T_{sim}}$ is unaffected.
- **Correct**: "$g = 1+2\sum_{k\ge1}c(k\Delta t_s)\;\approx\;\frac{2\tau_{int}}{\Delta t_s}$ for $\tau_{int}\gg\Delta t_s$" (or keep $g=1+2\tau/\Delta t_s$ and define $\tau=\Delta t_s\sum_{k\ge1}c(k\Delta t_s)$).
- **Evidence**: AR(1) with $\phi=0.95$: exact $g=(1+\phi)/(1-\phi)=39.0$; continuous $\tau_{int}=-1/\ln\phi=19.50$ frames; $2\tau_{int}=38.99$; $1+2\tau_{int}=39.99$. The module's `statistical_inefficiency` returned 41.3 on 200,000 samples, consistent with 39.
- **Severity**: imprecise
- **Confidence**: high

### 11-2. NOE averaging $\langle r^{-6}\rangle^{-1/6}$ holds only for slow internal motion
- **Quote**: "NOE distances | $\langle r^{-6}\rangle^{-1/6}$, which is dominated by the shortest distances" and check-yourself 3 "The NOE intensity is proportional to $r^{-6}$, and the experiment averages the intensity."
- **Problem**: $r^{-6}$ averaging applies when the internal distance fluctuations are slow compared with overall tumbling. When they are fast compared with tumbling (and angular motion is limited), the correct average is $\langle r^{-3}\rangle^{-1/3}$. Protein simulations usually report one of these, chosen by time scale, or $\langle r^{-6}\rangle$ over windows shorter than the tumbling time.
- **Correct**: "NOE distances | $\langle r^{-6}\rangle^{-1/6}$ when internal motion is slower than overall tumbling, $\langle r^{-3}\rangle^{-1/3}$ when it is faster; both are dominated by the shortest distances"
- **Evidence**: Tropp, J. Chem. Phys. 72, 6035 (1980), and the standard NOE averaging treatment (e.g. Neuhaus & Williamson, *The Nuclear Overhauser Effect*). The $r^{-3}$ regime comes from averaging the dipolar interaction before the spectral density.
- **Severity**: imprecise
- **Confidence**: medium

### 11-3. Karplus relation written with two different angles
- **Quote**: "Karplus relation $J(\phi) = A\cos^2\theta+B\cos\theta+C$"
- **Problem**: The left side uses $\phi$ and the right side $\theta$, and $\theta$ is not defined. For backbone $^3J_{HNH\alpha}$, $\theta=\phi-60^\circ$, and $A$, $B$, $C$ depend on the coupling.
- **Correct**: "Karplus relation $^3J(\theta) = A\cos^2\theta+B\cos\theta+C$ (for $^3J_{HN H\alpha}$, $\theta=\phi-60^\circ$), averaged over the trajectory"
- **Evidence**: Standard parameterisation (e.g. Vuister & Bax 1993, $^3J_{HNH\alpha}$ with $\theta=\phi-60^\circ$).
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the RMSD definition and Kabsch via SVD; $B=\frac{8\pi^2}{3}\mathrm{RMSF}^2$; $R_g$; contact and H-bond criteria (0.35 nm, 30°, GROMACS defaults); $g(r)$ and the coordination number; $w(r)=-k_BT\ln g$; Einstein $6Dt$ and Green-Kubo $\frac13\int\langle v\cdot v\rangle$; the Yeh-Hummer correction with 2.837 (Yeh & Hummer 2004, doi 10.1021/jp0477147); "more than 10 %" in a 3 nm box (10.2 % with real-water $\eta$ and $D$, 11.8 % for TIP3P); the boxed SE formula; five independent samples in 100 ns at $\tau$ = 10 ns; Flyvbjerg & Petersen 1989 (doi 10.1063/1.457480); the `block_average` and `statistical_inefficiency` code (both run correctly on a synthetic AR(1) series; block SE plateaus near the true 0.044); Chodera's equilibration-detection method (bioRxiv 2015, JCTC 2016); Hess 2000 and 2002 (Phys. Rev. E, dois confirmed) and a cosine of period $2T$ for PC1; FRET $1/[1+(r/R_0)^6]$; MDAnalysis `rms.RMSD(u, ref, select="backbone").run()` with `results.rmsd[:,1]` time in ps and `[:,2]` RMSD in Å, and `AtomGroup.radius_of_gyration()`; `gmx analyze -ee`; check-yourself 1 (20,000 frames, $g$ = 1001, SE 0.022 nm, factor 32); check-yourself 4; O-O first peak 0.28 nm.

---

## 12-free-energy-pmf.md

No errors found.

Checked and found correct: $P(\xi)$ and $W(\xi)$; $e^{-10}=4.5\times10^{-5}$; the radial Jacobian and the $-2k_BT\ln r$ signature; Torrie & Valleau 1977; the biased-distribution derivation and the boxed $W=-k_BT\ln P^b_i-w_i+F_i$ (re-derived); the per-window estimate $P\approx\frac{n_i}{N_i}e^{\beta(w_i-F_i)}$; the WHAM equations (Kumar et al. 1992, doi 10.1002/jcc.540130812); the MBAR self-consistent equation and weights (Shirts & Chodera 2008); $\sigma=\sqrt{k_BT/k}$; the window displacement $\xi_i-W'/k$ (re-derived for a linear PMF plus a harmonic bias); $k$ = 1000 gives 0.050 nm and 20 to 40 windows over 2 nm; check-yourself 2 (0.071 nm, 0.6 nm); the umbrella-integration mean-force formula (Kästner-Thiel form); $K_a=4\pi\int r^2e^{-\beta W}dr$; $V^\circ=1.661$ nm$^3$; $\Delta G^\circ=-k_BT\ln(K_aC^\circ)$; the worked example ($\beta\cdot50=20.05$, $K_a=6.4\times10^8$ nm$^3$, $K_d=2.6$ nM, $\Delta G^\circ=-49.3$ kJ/mol, all recomputed); Woo & Roux 2005 (PNAS) and Gumbart, Roux & Chipot 2013 (JCTC 9, 794; online Nov 2012); six relative rigid-body degrees of freedom; check-yourself 3 and 4.
