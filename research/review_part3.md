# Technical review, part 3 (modules 13 to 17, formula sheet, projects)

Reviewer's arithmetic was done with `wsl python3`. A 500-particle Lennard-Jones Monte Carlo run (T* = 1.0, rho* = 0.8, rc = 2.5) was used to check the Project 1 reference values. Findings are identified by quotation, not line number.

---

## 13-alchemical-free-energy.md

### 13.1 Sign of the restraint term in double decoupling
- **Quote**: "$\Delta G^\circ_{bind} = \Delta G_{decouple}^{solvent}-\Delta G_{decouple}^{site}+\Delta G_{restr}^\circ$" together with "The free energy of releasing a non-interacting ligand from these restraints into the standard volume $V^\circ$ is analytical: $\Delta G_{restr}^\circ = -k_BT\ln[\dots]$"
- **Problem**: The text defines $\Delta G^\circ_{restr}$ as the free energy of *releasing* the restraints (decoupled, restrained ligand to free ligand at $V^\circ$), and the formula given is indeed the release free energy. In the binding direction, though, the cycle goes the other way: decoupled ligand at standard concentration, then restrained (cost $-\Delta G^\circ_{restr}$), then recoupled in the site ($-\Delta G^{site}_{decouple}$). With the text's definition the term must enter with a minus sign. As written, the equation counts the translational and rotational entropy loss of binding as a gain. For typical restraints ($K_r$ = 10 kcal mol⁻¹ Å⁻², angle and dihedral constants 100 kcal mol⁻¹ rad⁻², $r_0$ = 5 Å, angles 90°) the release term is about −6.8 kcal/mol, so the sign error is worth about 14 kcal/mol in $\Delta G^\circ_{bind}$.
- **Correct**: "$\Delta G^\circ_{bind} = \Delta G_{decouple}^{solvent}-\Delta G_{decouple}^{site}-\Delta G_{restr}^\circ$, where $\Delta G_{restr}^\circ$ (below) is the free energy of releasing the restrained, non-interacting ligand into the standard volume." Equivalently, keep the "+" and define $\Delta G^\circ_{restr}=+k_BT\ln[\dots]$ as the free energy of *imposing* the restraints. That term is positive and makes binding less favourable.
- **Evidence**: Restrained configurational integral = $r_0^2\sin\theta_{A,0}\sin\theta_{B,0}\prod_{k=1}^{6}\sqrt{2\pi k_BT/K_k}$. Free integral at standard state = $8\pi^2V^\circ$. Release = $-k_BT\ln(Z_{free}/Z_{restr})$, which is the text's formula. The cycle L(solvent) → decoupled at $V^\circ$ ($\Delta G^{solv}_{dec}$) → decoupled and restrained ($-\Delta G^\circ_{release}$) → coupled in the site ($-\Delta G^{site}_{dec}$) gives $\Delta G_{bind}=\Delta G^{solv}_{dec}-\Delta G^{site}_{dec}-\Delta G^\circ_{release}$. Numbers: argument of the log is 1.0×10⁵, and $-k_BT\ln$ = −6.83 kcal/mol at 298 K.
- **Severity**: wrong
- **Confidence**: high

### 13.2 Soft-core functional form attributed to Beutler et al. 1994
- **Quote**: "The fix (Beutler et al. 1994) is a soft-core Lennard-Jones potential … $U_{sc}(r,\lambda) = 4\varepsilon(1-\lambda)\big[(\alpha\lambda+(r/\sigma)^6)^{-2}-(\alpha\lambda+(r/\sigma)^6)^{-1}\big]$"
- **Problem**: Beutler et al. wrote the soft-core term with a power of the coupling parameter both outside ($\lambda^n$) and inside the denominator ($\alpha(1-\lambda)^2$, in their convention where $\lambda=1$ is fully coupled). The form shown, with a linear $\alpha\lambda$ shift and prefactor $(1-\lambda)$, is the common GROMACS variant (`sc-power = 1`). It is a valid soft-core potential, but it is not Beutler's equation.
- **Correct**: "The fix (Beutler et al. 1994) is a soft-core Lennard-Jones potential in which $\lambda$ also shifts the distance. A widely used form (GROMACS with sc-power = 1; Beutler's original uses $\alpha\lambda^2$ in the denominator and $(1-\lambda)^n$ in front) is …"
- **Evidence**: Beutler, Mark, van Schaik, Gerber, van Gunsteren, Chem. Phys. Lett. 222, 529 (1994), doi:10.1016/0009-2614(94)00397-1 (Crossref confirms the record). The exponent details come from my memory of eq. 5 of the paper and the GROMACS manual's sc-power option. I could not fetch the full text.
- **Severity**: imprecise
- **Confidence**: medium (check eq. 5 of the paper)

### 13.3 MM/PBSA uses complex snapshots only
- **Quote**: "MM/PBSA and MM/GBSA estimate binding free energy from snapshots of the complex only"
- **Problem**: This describes only the single-trajectory protocol. The three-trajectory protocol (separate simulations of complex, receptor and ligand) is also standard, and it is the only variant that captures reorganisation of the partners.
- **Correct**: "MM/PBSA and MM/GBSA estimate binding free energy from MD snapshots, usually of the complex alone (single-trajectory protocol, in which receptor and ligand are extracted from the same frames), sometimes from separate simulations of complex, receptor and ligand: …"
- **Evidence**: Genheden and Ryde, Expert Opin. Drug Discov. 10, 449 (2015) describe both protocols.
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the definition of $\Delta A$ from partition functions; the Zwanzig derivation; the second-order cumulant $\langle\Delta U\rangle-\beta\sigma^2/2$; Jensen's bound $\Delta A\le\langle\Delta U\rangle_A$; the TI derivation (signs of $-k_BT/Q\cdot\partial Q/\partial\lambda$); Kirkwood 1935, Zwanzig 1954, Bennett 1976; Bennett's identity with $e^{-\beta C}$ (re-derived); the Fermi-function property $f(x)/f(-x)=e^{-x}$; the optimal $C=\Delta A+k_BT\ln(N_B/N_A)$; the equal-N BAR equation; the divergence of $\langle\partial U/\partial\lambda\rangle$ with linear LJ scaling; soft-core finite at $r=0$ and equal to LJ at $\lambda=0$; charges-before-LJ order; the relative-binding cycle closure and $\Delta\Delta G$ sign; Wang et al. 2015 at about 1 kcal/mol; the Boresch 6-DOF restraint (1 distance, 2 angles, 3 dihedrals) and the release formula itself, including $8\pi^2$ and $(2\pi k_BT)^3$; Jarzynski 1997, Crooks 1999 (forms and sign), the crossing at $W=\Delta A$; BAR on work values; Check 1 (FEP overestimates $\Delta A$); Check 3 (σ = 25 kJ/mol = 10.0 $k_BT$, $\beta\sigma^2/2$ = 125.3 kJ/mol, result 55 kJ/mol); Check 4; Mey et al. 2020 LiveCoMS.

---

## 14-enhanced-sampling.md

### 14.1 Waiting time for a 60 kJ/mol barrier
- **Quote**: "A barrier of 40 kJ/mol gives waiting times of microseconds to milliseconds, and 60 kJ/mol gives milliseconds to seconds."
- **Problem**: With the stated prefactor range of $10^9$ to $10^{12}$ s⁻¹ at 300 K, 60 kJ/mol gives waiting times of 28 ms to 28 s, so the upper end is tens of seconds, not seconds. The 40 kJ/mol value (9 µs to 9 ms) is fine.
- **Correct**: "… and 60 kJ/mol gives tens of milliseconds to tens of seconds."
- **Evidence**: $\beta\Delta F$ = 60/2.494 = 24.06, $e^{-24.06}$ = 3.6×10⁻¹¹, $1/k$ = 0.028 s ($k_0=10^{12}$) to 28 s ($k_0=10^9$).
- **Severity**: imprecise
- **Confidence**: high

### 14.2 What enters the REST2 exchange criterion
- **Quote**: "Since only the solute's degrees of freedom enter the exchange criterion, a handful to a dozen replicas suffice."
- **Problem**: The water-water term cancels, but the solute-water energy $U_{pw}$ does enter, with weight $\sqrt{\lambda_m}-\sqrt{\lambda_n}$. The acceptance is $\exp\{-\beta_0[(\lambda_m-\lambda_n)(U_{pp}(x_n)-U_{pp}(x_m))+(\sqrt{\lambda_m}-\sqrt{\lambda_n})(U_{pw}(x_n)-U_{pw}(x_m))]\}$. The number of replicas therefore scales with the solute and its solvation shell, not with the solute alone.
- **Correct**: "Because the water-water energy cancels from the exchange criterion and only the solute-solute and solute-water energies remain, the number of replicas grows with the size of the solute and its interface rather than of the whole box. A handful to a dozen replicas suffice for peptides and small proteins."
- **Evidence**: Wang, Friesner, Berne, J. Phys. Chem. B 115, 9431 (2011), exchange criterion derived from $U_m$ as given in the text.
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: 5.7 kJ/mol per decade at 300 K ($RT\ln10$ = 5.74); the replica-exchange acceptance (re-derived from the joint Boltzmann factors) and its sanity check; velocity rescaling by $\sqrt{T_{new}/T_{old}}$; $M\propto\sqrt{N_{df}}\ln(T_{max}/T_{min})$; geometric ladder; "50 to 60 replicas" for 30,000 atoms over 300 to 450 K (Gaussian-overlap estimate with about 10,000 waters and $C_U\approx6k_B$ per water gives about 55 at 20 % acceptance); REST2 scaling $\lambda U_{pp}+\sqrt\lambda U_{pw}+U_{ww}$ with $\lambda=T_0/T_m$, and its attribution; the Hamiltonian-exchange acceptance (after minus before); the entropic-barrier remark; Laio-Parrinello 2002; the hill sum; $V\to-F$; the well-tempered hill height, the limit $-\frac{\Delta T}{T+\Delta T}F$, sampling at $T+\Delta T$, $\gamma$ limits, $F=-\frac{\gamma}{\gamma-1}V$, the reweighting factor $e^{\beta(V-c(t))}$; Barducci-Bussi-Parrinello 2008; Check 2 (18×10/9 = 20 kJ/mol, sign); ABF (Darve and Pohorille 2001, applied force = minus the mean force); the SMD spring and the $10^5$ to $10^7$ speed ratio; logarithmic speed dependence; the aMD boost formula, Hamelberg-Mongan-McCammon 2004, weights $e^{\beta\Delta V}$; the GaMD cumulant reweighting; weighted ensemble (Huber and Kim 1996, Biophys. J., confirmed on Crossref), split and merge rules; infrequent metadynamics in Check 4; Check 1.

---

## 15-coarse-grained.md

### 15.1 Boltzmann inversion without the Jacobian
- **Quote**: "For a single coordinate $q$ with distribution $P(q)$ from the atomistic reference, use $U(q)=-k_BT\ln P(q)$. Adequate for bonds and angles"
- **Problem**: For bonds and angles the raw histogram includes the volume element: $P(r)\propto r^2e^{-\beta U(r)}$ and $P(\theta)\propto\sin\theta\,e^{-\beta U(\theta)}$. Inverting without dividing by the Jacobian gives a potential with a spurious $-2k_BT\ln r$ or $-k_BT\ln\sin\theta$ term, which is badly wrong for angles near 180°. Exercise 1 asks students to do exactly this.
- **Correct**: "For a single coordinate $q$ with distribution $P(q)$ from the atomistic reference, use $U(q)=-k_BT\ln[P(q)/J(q)]$, where $J$ is the Jacobian: $J=r^2$ for a bond length, $J=\sin\theta$ for a bond angle, $J=1$ for a dihedral."
- **Evidence**: Standard result, for example Tschöp et al., Acta Polym. 49, 61 (1998), and the VOTCA documentation for Boltzmann inversion.
- **Severity**: misleading
- **Confidence**: high

### 15.2 Force-matching optimum: sign and conditions
- **Quote**: "It can be shown that the minimum over all possible force fields is the gradient of the many-body PMF."
- **Problem**: The optimum force is the *negative* gradient of the many-body PMF (the mean force). The result also holds only under consistency conditions on the mapping (linear mapping, each atom contributing to at most one site, and the matching force operator defined accordingly; Noid et al. 2008).
- **Correct**: "It can be shown that, for a linear mapping that meets the consistency conditions of Noid et al. (2008), the force field minimising $\chi^2$ over all possible force fields is the mean force, $\mathbf F^{CG}=-\nabla U_{CG}$, with $U_{CG}$ the many-body PMF."
- **Evidence**: Noid et al., J. Chem. Phys. 128, 244114 (2008).
- **Severity**: imprecise
- **Confidence**: high

### 15.3 Elastic networks listed as "many residues per bead"
- **Quote**: table row "Many residues per bead | domains | Elastic networks, patchy-particle models"
- **Problem**: The standard elastic network models (GNM, ANM, and the elastic networks used with Martini, discussed later in this module) have one node per residue at the Cα atom. Only some specialised versions use coarser nodes.
- **Correct**: Move elastic networks to the one-bead-per-residue row ("… Gō and structure-based models, elastic network models, HPS, CALVADOS, AWSEM (three sites)"). Keep the many-residues row for "shape-based or domain-level models, patchy-particle models".
- **Evidence**: Bahar et al., Fold. Des. 2, 173 (1997) (GNM); Atilgan et al., Biophys. J. 80, 505 (2001) (ANM). Both use Cα nodes.
- **Severity**: misleading
- **Confidence**: high

### 15.4 Martini side-chain bead count
- **Quote**: "Each amino acid is one backbone bead plus zero to four side-chain beads."
- **Problem**: This is true for Martini 2. In Martini 3 tryptophan has five side-chain beads (SC1 to SC5; SC3 is a massless virtual site).
- **Correct**: "Each amino acid is one backbone bead plus zero to four side-chain beads (five for tryptophan in Martini 3)."
- **Evidence**: martinize2/vermouth Martini 3.0.0.1 topology, `vermouth/data/force_fields/martini3001/05-aminoacids.ff`, TRP block: BB, SC1 (TC4), SC2 (TN6d), SC3 (TC5, mass 0), SC4 (TC5), SC5 (TC5).
- **Severity**: imprecise
- **Confidence**: high

### 15.5 Generalised Born far-field limit
- **Quote**: "for distant atoms it reduces to Coulomb's law with the solvent dielectric constant."
- **Problem**: The GB pair term alone does not reduce to Coulomb's law with $\varepsilon_{out}$. For $r_{ij}\gg R$ the $(i,j)+(j,i)$ GB terms give $-\frac{q_iq_j}{4\pi\varepsilon_0r}(1/\varepsilon_{in}-1/\varepsilon_{out})$. Only that sum *plus* the direct Coulomb term $q_iq_j/(4\pi\varepsilon_0\varepsilon_{in}r)$ equals $q_iq_j/(4\pi\varepsilon_0\varepsilon_{out}r)$. Exercise 4 asks students to "show the two limits stated above" and cannot succeed for this one as worded.
- **Correct**: "for distant atoms, the GB pair term added to the direct Coulomb interaction (computed with $\varepsilon_{in}$) gives Coulomb's law with the solvent dielectric constant."
- **Evidence**: With $f_{GB}\to r$: $2\times\big(-\frac{1}{8\pi\varepsilon_0}\big)(1/\varepsilon_{in}-1/\varepsilon_{out})\frac{q_iq_j}{r}+\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_{in}r}=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_{out}r}$.
- **Severity**: imprecise
- **Confidence**: high

### 15.6 Ashbaugh-Hatch: "the repulsive core is the same for all pairs"
- **Quote**: "The repulsive core is the same for all pairs and the depth of the attractive well is $\lambda\varepsilon$."
- **Problem**: In HPS and CALVADOS, $\sigma_{ij}=(\sigma_i+\sigma_j)/2$ is residue-specific, so the core differs between pairs. What is pair-independent is the shape of the repulsive branch, which does not depend on $\lambda$.
- **Correct**: "The repulsive branch does not depend on $\lambda$ (only on the pair's $\sigma_{ij}$), and the depth of the attractive well is $\lambda\varepsilon$."
- **Evidence**: Dignon et al., PLoS Comput. Biol. 14, e1005941 (2018), residue-specific σ; Tesei et al., PNAS 118, e2111696118 (2021).
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the many-body PMF definition and its three consequences; the IBI update sign; Izvekov-Voth 2005 and Shell 2008 attributions and $S_{rel}$; the Martini time factor of 4, 1.1 nm cutoff, $\varepsilon_r$ = 15 (2.5 with polarisable water), 20 fs, the four-to-one water bead, Q/P/N/C and three sizes in Martini 3, Marrink 2007 and Souza 2021, IDP compaction in Martini 3; the Clementi-Nymeyer-Onuchic 2000 Cα energy function (dihedral 1:½ ratio), the 12-10 minimum at $\sigma_{ij}$ with depth $-\varepsilon$; the Karanicolas-Brooks 2002 potential (value −ε and zero slope at $\sigma$; desolvation barrier of 0.143 ε at $r$ = 1.448 σ, useful for Exercise 3; Protein Sci. record confirmed on Crossref); 210 MJ pairs; the Ashbaugh-Hatch piecewise form; HPS (Dignon 2018) and CALVADOS (Tesei 2021, SAXS + PRE, confirmed on Crossref); the Debye length expression (coefficient computed from constants: 0.3040 nm at 25 °C, $\varepsilon_r$ = 78.4, with $I$ in mol/m³), 0.79 nm at 150 mM; Check 3 (1.36 nm, 0.43 nm, factors 0.745 and 0.394, ratio 0.53); the PB equation; the Still 1990 GB expression, $f_{GB}$ and the Born ($i=j$) limit; Flory $R_g\approx0.2N^{0.6}$ nm (Kohn et al. 2004: $R_0$ = 1.93 Å, ν = 0.598).

---

## 16-kinetics-msm.md

### 16.1 Direction of the "function of the committor" statement
- **Quote**: "A collective variable $\xi$ is a good reaction coordinate to the extent that it is a function of the committor."
- **Problem**: The condition runs the other way. A good coordinate is one whose value determines the committor, $p_B(\mathbf x)\approx g(\xi(\mathbf x))$ with $g$ monotonic. "ξ is a function of $p_B$" admits useless coordinates. A constant, for example, is a function of $p_B$, and so is any ξ that merges different committor values.
- **Correct**: "A collective variable $\xi$ is a good reaction coordinate to the extent that the committor is a function of it, $p_B(\mathbf x)\approx g(\xi(\mathbf x))$ with $g$ monotonic, so that each isosurface of $\xi$ is an isocommittor surface."
- **Evidence**: Definition used by Best and Hummer, PNAS 102, 6732 (2005), and Peters, Annu. Rev. Phys. Chem. 67, 669 (2016).
- **Severity**: imprecise
- **Confidence**: high

Checked and found correct: the two-state master equation, the ratio $k_{AB}/k_{BA}=e^{-\beta\Delta G_{AB}}$, relaxation rate $k_{AB}+k_{BA}$; $K_d=k_{off}/k_{on}$; the 10 nM example (100 s); the TST flux expression and its harmonic limit $\omega_0/2\pi$ (re-derived); $k_BT/h$ = 6.25×10¹² s⁻¹ at 300 K; TST as an upper bound and Bennett-Chandler; Kramers 1940 high-friction formula with $\gamma\gg\omega_b$, turnover; the MFPT double integral (reflecting at −∞, absorbing at $b$); the committor and $p_B=\tfrac12$ definitions; the MSM definitions $T_{ij}$, $\mathbf p^T\mathbf T^k$, the row-normalised MLE, detailed balance, the left eigenvector for π, $t_i=-\tau/\ln\lambda_i$; the TICA generalised eigenproblem; the CK test; the implied-time-scale lag choice; Check 1 ($k_{off}$ = 10⁻³ s⁻¹, 1000 s, 10⁴ s ≈ 10¹⁰ × 1 µs); Check 3 (194.96 ns); Checks 2 and 4.

---

## 17-machine-learning.md

### 17.1 BioEmu throughput
- **Quote**: "They generate thousands of statistically independent conformations in GPU-minutes."
- **Problem**: The BioEmu paper states thousands of independent samples *per hour* on one GPU. "GPU-minutes" overstates its speed by about an order of magnitude. Speed varies across emulators and protein lengths.
- **Correct**: "They generate thousands of statistically independent conformations in about a GPU-hour (BioEmu's figure for a small protein), far less than the MD needed to sample the same ensemble."
- **Evidence**: Lewis et al., bioRxiv 10.1101/2024.12.05.626885 (abstract, retrieved from Crossref): "can generate thousands of statistically independent samples from the protein structure ensemble per hour on a single graphics processing unit". The Science 2025 version keeps this claim.
- **Severity**: imprecise
- **Confidence**: high

### 17.2 Typical MLIP cutoff
- **Quote**: "within a cutoff $r_c$ (typically 0.5 to 0.6 nm)"
- **Problem**: Many current models use cutoffs below 0.5 nm. NequIP and MACE-OFF commonly use 0.4 to 0.5 nm, ANI-1 uses 0.52 nm (radial) and 0.35 nm (angular), and Behler-Parrinello potentials commonly use 0.6 nm or more.
- **Correct**: "(typically 0.4 to 0.6 nm)"
- **Evidence**: The NequIP paper (Batzner et al. 2022) uses 4 to 5 Å in its benchmarks. MACE-OFF23 uses 4.5 Å (small/medium) and 5 Å (large). ANI-1 (Smith et al. 2017) uses $R_c$ = 5.2 Å radial and 3.5 Å angular. These values are from my memory of the papers and were not re-fetched.
- **Severity**: imprecise
- **Confidence**: medium

Checked and found correct: the conservative-force argument; translation, rotation and permutation invariance and force equivariance; the atomic-energy locality form and linear cost; the Behler-Parrinello 2007 radial symmetry function; ANI (Smith, Isayev, Roitberg 2017); GAP with SOAP and kernel regression; the message-passing update and the receptive field $T\times r_c$; SchNet 2018 (distance-only messages); NequIP 2022 (Nat. Commun., confirmed on Crossref; "up to three orders of magnitude" less data in the abstract fits "hundreds versus tens of thousands"); MACE 2022 higher body order and fewer layers; Allegro strictly local; the energy-force loss and $3N$ components; CGnet (Wang et al. 2019) force-matching loss; Majewski et al. 2023; the Boltzmann-generator change of variables $p_X=p_Z(f^{-1})|\det\partial f^{-1}/\partial\mathbf x|$ and weights $e^{-\beta U}/p_X$ (Noé et al. 2019); BioEmu training data (PDB/AFDB, over 200 ms of MD, experimental stabilities; matches the abstract); Checks 1 to 4.

---

## formula-sheet.md

### F.1 Ewald sum without its Coulomb prefactor
- **Quote**: "$U_{Ewald}=\frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\frac{\mathrm{erfc}(\alpha r)}{r}+\frac{2\pi}{V}\sum_{\mathbf k\ne0}\dots-\frac{\alpha}{\sqrt\pi}\sum_iq_i^2$"
- **Problem**: The expression is in Gaussian units, with no $1/(4\pi\varepsilon_0)$. Elsewhere the sheet uses SI and lists $1/(4\pi\varepsilon_0)$ = 138.935 kJ mol⁻¹ nm e⁻² in the constants table, and the force-field line includes it. Plugging charges in $e$ and lengths in nm into the formula as written gives energies too small by a factor of 138.9.
- **Correct**: "$U_{Ewald}=\frac{1}{4\pi\varepsilon_0}\Big[\frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\frac{\mathrm{erfc}(\alpha|\mathbf r_{ij}+\mathbf nL|)}{|\mathbf r_{ij}+\mathbf nL|}+\frac{2\pi}{V}\sum_{\mathbf k\ne0}\frac{e^{-k^2/4\alpha^2}}{k^2}|S(\mathbf k)|^2-\frac{\alpha}{\sqrt\pi}\sum_iq_i^2\Big]$"
- **Evidence**: The bracketed terms are the standard Gaussian-unit Ewald sum (Frenkel and Smit, ch. 12). The SI form multiplies all three terms by $1/(4\pi\varepsilon_0)$.
- **Severity**: imprecise
- **Confidence**: high

### F.2 Binding constant from the PMF needs a stated zero of W
- **Quote**: "$K_a=4\pi\int_{bound}r^2e^{-\beta W(r)}dr$"
- **Problem**: The formula holds only when $W(r)$ is set to zero at large separation (where the partners no longer interact) and no orientational or positional restraints remain. A PMF with an arbitrary additive constant gives an arbitrary $K_a$.
- **Correct**: "$K_a=4\pi\int_{bound}r^2e^{-\beta W(r)}dr$, with $W(r\to\infty)=0$ and no other restraints"
- **Evidence**: Module 12 and Doudou, Burton and Henchman, J. Chem. Theory Comput. 5, 909 (2009), derive the formula with $W(\infty)$ = 0.
- **Severity**: imprecise
- **Confidence**: medium (Module 12 may already state the convention; the sheet does not)

Checked and found correct: $k_B$ in kJ and kcal; $k_BT$ at 300 K (2.494 kJ/mol, 0.596 kcal/mol); $RT\ln10$ at 298 K (5.705 kJ/mol, 1.364 kcal/mol); 138.935; $V^\circ$ = 1.661 nm³; Debye coefficient 0.304; AMBER to GROMACS factor 418.4 together with $k=2K$; Newton, Hamilton, the pair force, Liouville ($\partial\rho/\partial t=-\{\rho,H\}$); $Q$ with $N!\Lambda^{3N}$; $T_{inst}$, $\sigma_T/T=\sqrt{2/N_{df}}$, $C_V$, $\langle\delta V^2\rangle$; the virial pressure; velocity Verlet; Trotter splitting; $\omega\Delta t<2$; $\tilde H=H+O(\Delta t^2)$; the force field with ½ factors; $r_{min}$; Lorentz-Berthelot; minimum image and $r_c\le L/2$; the LJ tail correction $\tfrac83\pi N\rho\varepsilon\sigma^3[\tfrac13(\sigma/r_c)^9-(\sigma/r_c)^3]$; Berendsen λ²; Langevin, the O step, Brownian; Nosé-Hoover; the MC barostat acceptance; the SHAKE expressions and $N_{df}=3N-N_c-3$; $g(r)$; MSD → 6Dt; Yeh-Hummer 2.837; statistical inefficiency and SE; WHAM and MBAR equations; $\Delta G^\circ=-k_BT\ln(K_aC^\circ)$; FEP, TI, BAR, Jarzynski, Crooks and $\Delta\Delta G$ (consistent with Module 13); replica exchange and WT-metadynamics (consistent with Module 14); the Gō contact, Debye-Hückel and GB expressions (consistent with Module 15); the kinetics and MSM formulas (consistent with Module 16); the ML formulas (consistent with Module 17).

---

## projects.md

### P.1 Slope of ln k against h in Project 4
- **Quote**: "**Check.** A plot of $\ln k$ against $h$ is a straight line of slope $-1$, and the three estimates agree where they overlap."
- **Problem**: For $U(x)=h(x^2-1)^2$ the Kramers (and MFPT) prefactor itself depends on $h$: $U''(\pm1)=8h$ and $|U''(0)|=4h$, so in the overdamped limit $k=\frac{D\beta}{2\pi}\sqrt{8h\cdot4h}\,e^{-\beta h}\propto h\,e^{-\beta h}$. Then $d\ln k/dh=-1+1/h$, which is −0.67 to −0.83 over $h$ = 3 to 6 $k_BT$ (mean slope −0.77). A student with correct results would see a curved line with slope well short of −1 and conclude that something was wrong.
- **Correct**: "**Check.** A plot of $\ln(k/h)$ against $h$ (in units of $k_BT$) is a straight line of slope $-1$, because the Kramers prefactor of this potential is proportional to $h$. The three estimates agree where they overlap."
- **Evidence**: $\ln h-h$ = −1.90, −2.61, −3.39, −4.21 at $h$ = 3, 4, 5, 6; slope between $h$ = 3 and 6 is −0.769.
- **Severity**: wrong
- **Confidence**: high

Checked and found correct: the $\Delta t^2$ scaling of NVE energy fluctuations; the $g(r)$ first peak at T* = 1.0, ρ* = 0.8 (my MC run: peak at r = 1.08 σ, height 2.66, consistent with "near 1.1 σ, close to 2.7"; for the truncated, unshifted potential at rc = 2.5, U/N = −5.11 and P = 1.71 without tail corrections, U/N = −5.54 and P = 1.03 with them); NIST SRSD covers T* = 1.0 (LAMMPS-MD NVT isotherms 0.65 to 1.20); four Verlet steps per RK4 step at equal force-evaluation cost; the velocity Verlet shadow invariant $\tfrac12v^2+\tfrac12\omega^2(1-\tfrac14\omega^2\Delta t^2)x^2$ (conserved to 4×10⁻¹⁵ in a numerical test at ωΔt = 0.5); the Euler, RK4 and Verlet energy behaviour; the $1/\sqrt{\text{run length}}$ error scaling; ethanol hydration free energy (FreeSolv −5.00 kcal/mol = −20.9 kJ/mol) and the 4 kJ/mol tolerance.
