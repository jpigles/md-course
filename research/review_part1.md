# Technical review, modules 1 to 6

Reviewer: technical referee (read-only). Findings are identified by quoting the text, not by line number. Arithmetic was recomputed with `wsl python3` (CODATA constants). The Module 1 Python block was extracted and run unchanged (numpy, WSL).

---

## 01-what-is-md.md

### 1.1 Steps per day
- **Quote**: "That is $10^{11}$ steps per day at best."
- **Problem**: 1,000 ns/day at 2 fs is 5×10^8 steps per day (2.5×10^8 at 4 fs). $10^{11}$ is about 200 times too high. It would mean 200 µs/day at 2 fs.
- **Correct**: "That is about $5\times10^{8}$ steps per day at best (1 µs per day at 2 fs)."
- **Evidence**: 1000e-9 s / 2e-15 s = 5.0e8.
- **Severity**: wrong
- **Confidence**: high

### 1.2 "Steps at 2 fs" column is off by a factor of 2
- **Quote**: "Water reorientation, hydrogen-bond lifetime | 1 to 10 ps | $10^3$", "10 ps to 1 ns | $10^4$ to $10^6$", "1 ns to 1 µs | $10^6$ to $10^9$", "1 µs to 1 ms | $10^9$ to $10^{12}$", "$10^{15}$ or more"
- **Problem**: Only the first row (10 fs → 5) is divided by 2 fs. The other rows are time/1 fs. 10 ps / 2 fs = 5×10^3, 1 ns / 2 fs = 5×10^5, 1 µs / 2 fs = 5×10^8, 1 ms / 2 fs = 5×10^11, 1 s / 2 fs = 5×10^14.
- **Correct**: rows: "$5\times10^2$ to $5\times10^3$"; "$5\times10^3$ to $5\times10^5$"; "$5\times10^5$ to $5\times10^8$"; "$5\times10^8$ to $5\times10^{11}$"; "$5\times10^{14}$ or more". (Or rename the column "Steps at 1 fs" and change the first row to 10.)
- **Evidence**: direct division.
- **Severity**: imprecise
- **Confidence**: high

### 1.3 SHAKE is from 1977, not the 1980s
- **Quote**: "**1980s.** Thermostats and barostats (...), constraints (SHAKE), ..."
- **Problem**: SHAKE was published in 1977.
- **Correct**: "**1977.** Ryckaert, Ciccotti and Berendsen: SHAKE bond constraints." and remove "constraints (SHAKE)" from the 1980s line (or write "constraints (SHAKE, 1977; RATTLE, 1983)").
- **Evidence**: Crossref: Ryckaert, Ciccotti, Berendsen, "Numerical integration of the cartesian equations of motion of a system with constraints: molecular dynamics of n-alkanes", J. Comput. Phys. 23, 327, issued 1977-03, doi:10.1016/0021-9991(77)90098-5.
- **Severity**: wrong
- **Confidence**: high

### 1.4 Energy conservation claimed for the Python code
- **Quote**: "The total energy per particle printed in the last column should stay constant to about four decimal places."
- **Problem**: Running the code as written gives E/N between −3.28873 and −3.28804 over the 2,001 steps. That is a spread of 7×10^-4, so it changes in the fourth decimal place. It is constant to about three decimal places, not four. The cause is the truncated-and-shifted potential: the force still jumps at $r_c$, so the dynamics is not exactly Hamiltonian.
- **Correct**: "The total energy per particle printed in the last column should stay constant to about three decimal places (fluctuations of a few $10^{-4}$), while the temperature changes by several percent."
- **Evidence**: output of the unchanged code: step 0 −3.28873, step 600 −3.28804, step 2000 −3.28849. The temperature goes 1.018 → 0.86–1.01, which matches the text's description of the temperature.
- **Severity**: imprecise
- **Confidence**: high

The code itself has no bugs. The minimum image, the force sign (force on i along $\mathbf r_i-\mathbf r_j$ for repulsion), the 0.5 for double counting, the shift applied only inside the cutoff, $r_c=2.5 < L/2 = 2.69$, the velocity Verlet order and the $3N-3$ degrees of freedom are all correct.

### 1.5 "No closed-form solution for more than two particles"
- **Quote**: "There is no closed-form solution for more than two interacting particles"
- **Problem**: Special closed-form solutions of the three-body problem exist (the Euler and Lagrange configurations, and the figure-eight orbit). What does not exist is a general closed-form solution.
- **Correct**: "In general there is no closed-form solution for three or more interacting particles"
- **Evidence**: standard result (Poincaré; the Lagrange L4/L5 solutions).
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the velocity Verlet equations; Λ = 1.00 Å (H) and 0.29 Å (C) at 300 K; $k_BT$ = 208.5 cm⁻¹; 3,000 cm⁻¹ ≈ 14.4 $k_BT$; electron/proton mass ratio about 1/1836; $k_B$ in kJ and kcal; $k_BT$ = 2.494 kJ/mol = 0.596 kcal/mol; 4.184; 138.935 and 332.06; 1 u nm² ps⁻² = 1 kJ/mol; $RT\ln10$ = 5.71 kJ/mol = 1.36 kcal/mol at 298 K; water 33.4 nm⁻³; 420 neighbours and 2×10⁷ pairs; micromolar and nanomolar residence times (koff = Kd·kon with kon 10⁵–10⁸ M⁻¹s⁻¹); 1957 Alder and Wainwright; 1964 Rahman (864 Ar); 1967 Verlet; 1971 Rahman and Stillinger (216 molecules); 1977 McCammon, Gelin and Karplus (BPTI, 58 residues, vacuum, about 9 ps); PME 1993/1995; Anton BPTI millisecond in 2010 and twelve proteins in 2011; the 2013 Nobel; time steps of 1, 2 and 4 fs; the answers to Check yourself 1 to 4; N log N for PME.

---

## 02-classical-mechanics.md

### 2.1 "Symplectic" is equated with "volume-preserving"
- **Quote**: "**A good integrator should also preserve phase-space volume.** Integrators with this property are called symplectic."
- **Problem**: Symplectic means the map preserves the symplectic two-form (the sum of oriented areas $\sum_k dq_k\wedge dp_k$). That implies volume preservation, but the converse is false for more than one degree of freedom: there are volume-preserving maps that are not symplectic. The shadow-Hamiltonian result in Module 4 needs symplecticity, not volume preservation alone. A related point: "Runge-Kutta" is not symplectic only for explicit RK. Implicit Gauss-Legendre RK methods are symplectic.
- **Correct**: "**A good integrator should also preserve the Hamiltonian (symplectic) structure of phase space.** Such integrators are called symplectic. They preserve phase-space volume, but they also preserve more than that, and it is this stronger property that gives them a conserved shadow Hamiltonian. Those without it (for example forward Euler or the classical explicit Runge-Kutta methods) ..."
- **Evidence**: Hairer, Lubich and Wanner, *Geometric Numerical Integration*, ch. VI (symplectic ⇒ volume-preserving; the converse holds only for n = 1).
- **Severity**: imprecise
- **Confidence**: high

The same wording, "Symplectic (volume-preserving)", appears in 04-integrators.md (see 4.1).

Checked and found correct: dE/dt = 0; the pair-force chain rule and Newton's third law; the Euler-Lagrange equation; the pendulum equation $ml^2\ddot\theta+mgl\sin\theta=0$; the Legendre transform and $H=K+U$; Hamilton's equations; the oscillator ellipse area $2\pi E/\omega$; the Poisson bracket and $iL$; the $iL_r + iL_p$ split; the phase-space divergence = 0; the Liouville equation $\partial_t\rho=-\{\rho,H\}$; the conservation table, including the fact that angular momentum is not conserved under PBC; $3N-3$; the mass-weighted Hessian; $\omega=\sqrt{k/\mu}$; the C-H example ($\mu$ = 0.923 u, $\omega$ = 551 ps⁻¹, period 11.4 fs); ln(10¹⁶) ≈ 37, so a few tens of ps at $1/\lambda$ = 1 ps; Check 2 (solution, and the clockwise sense); Check 3; Check 4 (divergence $-n\gamma$).

---

## 03-statistical-mechanics.md

### 3.1 The PMF "mean force" statement needs the Jacobian, and the g(r) example contradicts the definition
- **Quote**: "its slope is the average force along $\xi$: $-dW/d\xi = \langle F_\xi\rangle_\xi$" and "The simplest example is the pair distribution function of a liquid, $g(r) = e^{-\beta w(r)}$."
- **Problem**: With the definition given, $W(\xi) = -k_BT\ln P(\xi)$, the derivative includes a Jacobian (entropic) term whenever $\xi$ is curvilinear. For a distance, $P(r)\propto 4\pi r^2 g(r)$, so $W(r) = w(r) - 2k_BT\ln r + \text{const}$. Then $-dW/dr = \langle F_r\rangle_r + 2k_BT/r$, not $\langle F_r\rangle_r$. The pair potential of mean force $w(r) = -k_BT\ln g(r)$ is the one whose slope is the mean force, and it is not the $W$ defined two lines earlier. The general result is $dW/d\xi = \langle \partial U/\partial\xi - k_BT\,\partial\ln|J|/\partial\xi\rangle_\xi$ (den Otter; Darve and Pohorille).
- **Correct**: "For a Cartesian-like coordinate its slope is the average force along $\xi$, $-dW/d\xi = \langle F_\xi\rangle_\xi$. For curvilinear coordinates there is an extra Jacobian term; for a distance, $-dW/dr = \langle F_r\rangle_r + 2k_BT/r$. The pair potential of mean force of a liquid, $w(r) = -k_BT\ln g(r)$, is defined relative to the ideal-gas $r^2$ factor, and its slope is exactly the mean force."
- **Evidence**: $P(r)=\int\delta(|\mathbf r_{12}|-r)\,e^{-\beta U}/Z \propto r^2 g(r)$; take the log and differentiate.
- **Severity**: misleading
- **Confidence**: high

### 3.2 The binding-constant formula uses the other PMF convention
- **Quote**: "If $W(r)$ is the PMF along the separation of the two partners, with $W\to0$ at large distance, then to a good approximation $K_a = 4\pi\int_{bound} r^2\,e^{-\beta W(r)}\,dr$"
- **Problem**: This is correct only if $W$ is the $g(r)$-type PMF (orientationally averaged, $r^2$ Jacobian removed, so that $W\to0$ at large $r$). With the $W=-k_BT\ln P(\xi)$ defined in the previous subsection, the $r^2$ would be counted twice, and that $W$ does not go to 0 at large $r$ (it goes as $-2k_BT\ln r$). Readers will plug in the $W$ from the previous subsection.
- **Correct**: "If $w(r)$ is the radial PMF defined from the pair distribution, $w(r) = -k_BT\ln g_{PL}(r)$ (so $w\to0$ at large distance; this differs from $-k_BT\ln P(r)$ by $2k_BT\ln r$), then $K_a = 4\pi\int_{bound} r^2 e^{-\beta w(r)}dr$."
- **Evidence**: as in 3.1. Standard form in Roux and co-workers' and Gilson's treatments of $K_a$.
- **Severity**: misleading
- **Confidence**: high

### 3.3 The $\Lambda^{3N}$ factorisation assumes one mass
- **Quote**: "$Q = \frac{1}{N!\,\Lambda^{3N}}\int d\mathbf r^N e^{-\beta U(\mathbf r)}$"
- **Problem**: The line above uses $m_i$, but the result is written with a single $\Lambda$ and a single $N!$. That holds for a one-component system of identical particles only. A biomolecular system has many masses and species.
- **Correct**: "$Q = \dfrac{Z}{\prod_s N_s!\;\prod_i \Lambda_i^{3}}$, with $\Lambda_i = h/\sqrt{2\pi m_i k_BT}$ ($N_s$ the number of particles of species $s$); for a single species this is $Z/(N!\Lambda^{3N})$."
- **Evidence**: each momentum integral gives $(2\pi m_i k_BT)^{3/2}$ separately.
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the ensemble table, including $G=-k_BT\ln\Delta$ and $-PV$ for µVT; the bath-expansion derivation of $P\propto e^{-\beta E}$; the Gaussian momentum integral; $A$, $\langle E\rangle$, $P$, $S$ from $Q$; $\partial^2\ln Q/\partial\beta^2$ = var(E) and $C_V$; $\langle\delta V^2\rangle = k_BTV\kappa_T$; equipartition $\langle ax^2\rangle = k_BT/2$; $T_{inst}$ and $N_{df}$; $\sqrt{2/N_{df}}$ = 8.2 % (100 atoms) and 0.26 % (10⁵ atoms); the virial equation and its pair form; ergodic averaging; $P_B/P_A = Z_B/Z_A$; the two-state example ($Z_B$ = 18.1, ΔA = −7.23 kJ/mol, −TΔS = −17.2 kJ/mol); $1/Z = \langle e^{\beta U}\rangle/V^N$; $\Delta G^\circ = -k_BT\ln(K_aC^\circ)$; $C^\circ$ = 0.6022 nm⁻³; Check 1 (74,997 and 1.55 K); Check 2 (0.035, 96.6 %/3.4 %); Check 3, including the constraint (Fixman) caveat; Check 4.

---

## 04-integrators.md

### 4.1 "Symplectic (volume-preserving)"
- **Quote**: "**2. Symplectic (volume-preserving).** ... Each is a shear in phase space with Jacobian determinant exactly 1. So the numerical map preserves phase-space volume exactly"
- **Problem**: Same as 2.1. The Jacobian-determinant argument proves volume preservation only. Symplecticity follows because each sub-step is the exact flow of a Hamiltonian ($K$ or $U$), and a composition of symplectic maps is symplectic. Point 3 of the same list already uses that argument.
- **Correct**: "**2. Symplectic.** A drift is the exact flow of $H=K$ and a kick the exact flow of $H=U$; each is a symplectic map, so their composition is symplectic. In particular each is a shear with Jacobian determinant exactly 1, so the numerical map preserves phase-space volume exactly, as the true dynamics does (Liouville's theorem)."
- **Evidence**: see 2.1.
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the Taylor derivation of Verlet (local error $O(\Delta t^4)$, global $O(\Delta t^2)$) and the central-difference velocity; velocity Verlet and its equivalence to Verlet (the subtraction argument is right); leap-frog, and GROMACS `integrator = md` being leap-frog; Swope, Andersen, Berens and Wilson 1982; Tuckerman, Berne and Martyna 1992; Strang splitting with error $O(\Delta t^3)$; only even powers in the shadow Hamiltonian. The harmonic-oscillator matrix was re-derived by hand and its determinant is 1. The stated $\tilde H = \tfrac12v^2+\tfrac12\omega^2(1-\tfrac14\omega^2\Delta t^2)x^2$ is conserved to machine precision in a numerical test ($\omega\Delta t$ = 0.7, while $H$ varies by 10 %). Also correct: $\cos\theta = 1-\tfrac12\omega^2\Delta t^2$; $\omega\Delta t<2 \Leftrightarrow \Delta t<T/\pi$; $\omega_{num}\approx\omega(1+\omega^2\Delta t^2/24)$; the time-step table (11 fs, about 20 fs, 1/2/4/20 fs); fluctuation ∝ $\Delta t^2$ (a factor of 4 per halving); the RK4, Gear and Forest-Ruth/Yoshida statements; the r-RESPA formula; MTS availability in GROMACS (`mts`), NAMD, OpenMM and Desmond; BAOAB (Leimkuhler and Matthews 2013) and LangevinMiddleIntegrator; Check 2 (9.5 fs, 3.0 fs, 19 steps); Checks 1, 3 and 4; Exercise 4 (the commutator structure). Not settled: the MTS resonance limit of "4 to 5 fs with constrained bonds to hydrogen". The linear resonance at half the fastest period, and the nonlinear one at a third of it, would give larger values for a 20 fs fastest period. I could not confirm the exact number against the primary sources (Ma, Izaguirre and Skeel 2003; Morrone, Zhou and Berne 2010), so I do not report it as a finding.

---

## 05-force-field-form.md

### 5.1 "Only r² appears ... This is the real reason for the 12-6 form"
- **Quote**: "Only $r^2$ appears, never $r$ itself, so no square root is needed. This is the real reason for the 12-6 form."
- **Problem**: (a) It contradicts the earlier sentence, which gives a different "reason": "$r^{-12}$ was chosen because it is the square of $r^{-6}$ and so costs one multiplication". (b) The claim is not true as stated. Any even-power repulsion ($r^{-8}$, $r^{-10}$) also avoids the square root, so this property does not single out 12. (c) In any biomolecular code the Coulomb or PME real-space term ($\mathrm{erfc}(\beta r)/r$) needs $r$ for the same pair, so the square root is computed anyway. Lennard-Jones himself used other exponents; the 12 became standard mainly for convenience and fitting.
- **Correct**: "Only even powers of $r$ appear, so the Lennard-Jones term alone needs no square root. This was a real saving in early codes. In biomolecular simulation, though, the Coulomb term for the same pair needs $r$ anyway."
- **Evidence**: algebra. In the GROMACS reference manual the non-bonded kernels compute $r^{-1}$ for every pair inside the cutoff because of the electrostatics.
- **Severity**: misleading
- **Confidence**: high

### 5.2 Water-model dipole range excludes OPC
- **Quote**: "The water models have dipole moments of 2.2 to 2.4 D, against 1.85 D for an isolated water molecule."
- **Problem**: OPC, which the course recommends with ff19SB, has a dipole of 2.48 D. TIP3P and SPC/E are 2.35 D, SPC 2.27 D and TIP4P/2005 2.305 D.
- **Correct**: "The common rigid water models have dipole moments of about 2.2 to 2.5 D (SPC 2.27, TIP3P and SPC/E 2.35, OPC 2.48 D), against 1.85 D for an isolated water molecule."
- **Evidence**: Izadi, Anandakrishnan and Onufriev, J. Phys. Chem. Lett. 5, 3863 (2014), Table 1: OPC μ = 2.48 D.
- **Severity**: imprecise
- **Confidence**: high

### 5.3 Term counts are for protein atoms, not "a protein in water"
- **Quote**: "For a protein in water with $N$ atoms there are about $N$ bonds, $2N$ angles and $3N$ dihedrals"
- **Problem**: In a solvated protein most atoms are water: 2 bonds, 1 angle and 0 dihedrals per 3 atoms, or none at all with SETTLE. For the whole system the counts are far below N, 2N and 3N. The counts hold roughly only for the protein atoms (protein alone: about 1.0N bonds, 1.8N angles, 2.5–3N dihedrals).
- **Correct**: "For a protein with $N_p$ atoms there are about $N_p$ bonds, $2N_p$ angles and $3N_p$ dihedrals (water adds few or none), all cheap."
- **Evidence**: topology counting; e.g. an AMBER alanine dipeptide with 22 atoms has 21 bonds, 36 angles and 41 proper dihedrals.
- **Severity**: imprecise
- **Confidence**: medium

Checked and found correct: the functional form; $k_{GROMACS}=2K_{AMBER}$; the factor 418.4; 310 → 259,408; the bond table (0.0031, 0.0030 and 0.0023 nm; "about 2 %"); the angle fluctuation 0.071 rad = 4.0°; Urey-Bradley; the GROMOS cos-harmonic angle; $k_{\phi,n}$ = half the barrier; the ethane barrier of about 12 kJ/mol ≈ 4.8 $k_BT$; RB with ψ = φ − 180° (GROMACS manual); CMAP with bicubic interpolation in CHARMM and ff19SB; AMBER periodic impropers (n = 2, 180°); $r_{min}=2^{1/6}\sigma$ and $C_6$, $C_{12}$; $R_{min}/2$ in AMBER/CHARMM files; the combining-rule table (LB for AMBER/CHARMM, geometric for OPLS, GROMOS on $C_6$/$C_{12}$); ε of 0.1–1 kJ/mol; 138.935; peptide partial charges (ff14SB: O −0.57, C +0.60, N −0.42, H +0.27; CHARMM: −0.51/+0.51/−0.47/+0.31); 463 kJ/mol = 186 $k_BT$; the 1-4 table (AMBER 0.5 and 1/1.2, OPLS 0.5/0.5, CHARMM 1/1, GROMOS pair list and 1.0); the LJ and Coulomb force expressions; $\partial\cos\theta/\partial\mathbf r_i$ and the angle-force sign; $N(N-1)/2$ = 5×10⁹; Check 1; Check 2 ($(26/7)^{1/6}$ = 1.2445); Check 4 (2.6×10¹⁰ s⁻¹, about 40 ps); the TIP3P parameters in Exercise 3.

---

## 06-force-field-parameters.md

### 6.1 The TIP4P-D dispersion increase depends on the reference model
- **Quote**: "TIP4P-D (Piana et al. 2015) | Water dispersion coefficient increased by about 50 %"
- **Problem**: TIP4P-D is a modification of TIP4P/2005. From the published parameters, its $C_6$ is about 22 % larger than TIP4P/2005's and about 50 % larger than TIP3P's. Without the reference model, "about 50 %" reads as an increase over the parent model.
- **Correct**: "Water $C_6$ dispersion coefficient increased (about 50 % above TIP3P, about 20 % above its parent TIP4P/2005)"
- **Evidence**: $C_6=4\varepsilon\sigma^6$ with TIP4P-D (σ = 0.3165 nm, ε = 0.936 kJ/mol), TIP4P/2005 (0.31589 nm, 0.7749 kJ/mol) and TIP3P (0.31506 nm, 0.636 kJ/mol): ratios 1.22 and 1.51. Paper: Piana, Donchev, Robustelli, Shaw, J. Phys. Chem. B 119, 5113 (2015), doi:10.1021/jp508971m. I did not read the paper's own wording of the percentage. The ratios settle the question.
- **Severity**: imprecise
- **Confidence**: medium

### 6.2 The RESP restraint is applied to heavy atoms only
- **Quote**: "$\chi^2_{RESP} = \chi^2_{ESP} + a\sum_i\left(\sqrt{q_i^2+b^2}-b\right)$"
- **Problem**: In standard RESP (Bayly et al. 1993, and the AMBER `resp` program's default two-stage protocol) the hyperbolic restraint acts on non-hydrogen atoms only. The sum over all $i$ also restrains hydrogens, which RESP deliberately does not do.
- **Correct**: "$\chi^2_{RESP} = \chi^2_{ESP} + a\sum_{i\in\text{heavy atoms}}\left(\sqrt{q_i^2+b^2}-b\right)$, with $b = 0.1\,e$; hydrogens are not restrained."
- **Evidence**: Bayly, Cieplak, Cornell, Kollman, J. Phys. Chem. 97, 10269 (1993). The restraints are applied to non-hydrogen atoms (AMBER manual, `resp` chapter: "restraints ... on heavy atoms").
- **Severity**: imprecise
- **Confidence**: medium

Checked and found correct: the fitting order and the torsion-as-residual logic; the ESP least-squares problem with a Lagrange multiplier; RESP 1993; HF/6-31G* overestimating the dipole by 10–20 %; the CHARMM/OPLS/GROMOS charge philosophies; the family table (ff14SB with TIP3P, ff19SB with OPC, CHARMM36m with CHARMM TIP3P, OPLS-AA/M, GROMOS 54A7 united-atom with SPC); the lineage (ff94 Cornell 1995, ff99SB 2006, ILDN = Ile/Leu/Asp/Asn 2010, ff14SB Maier 2015, ff19SB Tian 2020, CHARMM22 1998, CMAP 2004, CHARMM36 Best 2012, CHARMM36m Huang 2017); GAFF/CGenFF/OpenFF; the CHARMM force switch at 1.0–1.2 nm; the water table (SPC/E dielectric constant of about 70, TIP3P D about 5–6×10⁻⁵ cm²/s and ε in the 90s, TIP4P/2005 ε ≈ 60, OPC, TIP5P density maximum near 4 °C); the experimental D = 2.3×10⁻⁵ cm²/s and ε = 78; TIP3P viscosity too low by 2–3×; the SPC/E polarisation correction recomputed with α = 1.608×10⁻⁴⁰ C² m² J⁻¹ (3.7 and 5.2 kJ/mol); Berendsen, Grigera and Straatsma 1987; Joung and Cheatham 2008; Best, Zheng and Mittal 2014 (λ = 1.10); a99SB-disp 2018; the Drude relations $d=q_DE/k_D$, $\alpha=q_D^2/k_D$ and the 1 fs step; AMOEBA multipoles up to quadrupoles; Lindorff-Larsen 2012 (PLoS ONE); the GROMACS topology columns, the ALA N-terminal N3 charge 0.1414, dihedral functions 9 and 4; Checks 1–4.
