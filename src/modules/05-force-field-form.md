---
num: 5
title: Force fields I, the energy function term by term
short: Force fields: the terms
part: Part II · The engine
hours: 6
summary: Write the standard biomolecular energy function, know what each term represents physically and what typical parameter values are, and derive the force from each term.
videos: 5
papers: F
tags: force-fields
---

<div class="box goal" markdown="1">
#### After this module you can

- write the full additive force-field energy and name every parameter in it;
- convert a force constant into a thermal fluctuation and a vibration period;
- explain where the $r^{-6}$ and $r^{-12}$ terms come from and what the combining rules are;
- derive the force for a pair term and outline it for an angle or dihedral;
- list what a fixed-charge force field leaves out.
</div>

## Watch first

{{WATCH}}

## The functional form

A classical (Class I, additive) force field writes the potential energy as a sum of simple terms:

$$
\begin{aligned}
U(\mathbf r) ={}& \sum_{bonds}\tfrac12 k_b\,(r-r_0)^2
+ \sum_{angles}\tfrac12 k_\theta\,(\theta-\theta_0)^2
+ \sum_{dihedrals}\sum_n k_{\phi,n}\,\big[1+\cos(n\phi-\delta_n)\big] \\
&+ \sum_{impropers}\tfrac12 k_\omega\,(\omega-\omega_0)^2
+ \sum_{i<j}^{non\text{-}bonded} \left\{4\varepsilon_{ij}\left[\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12}-\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{6}\right] + \frac{q_iq_j}{4\pi\varepsilon_0\,r_{ij}}\right\}
\end{aligned}
$$

The first four sums are the **bonded** terms. They run over lists that are fixed when the system is built (the topology). The last sum is the **non-bonded** part and runs over all pairs of atoms, apart from the exclusions discussed below. AMBER, CHARMM, OPLS-AA and GROMOS all use this form with small variations.

<div class="box warn" markdown="1">
**Convention trap.** GROMACS writes harmonic terms as $\tfrac12k(x-x_0)^2$. AMBER and CHARMM parameter files write $K(x-x_0)^2$ without the half, so $k_{GROMACS} = 2K_{AMBER}$. Add the unit change from kcal mol$^{-1}$ Å$^{-2}$ to kJ mol$^{-1}$ nm$^{-2}$ (a factor 418.4), and the same C-C bond appears as 310 in one file and 259,408 in another.
</div>

## Bond stretching

$$
U_b = \tfrac12 k_b\,(r-r_0)^2
$$

The true bond energy is closer to a Morse curve $D_e[1-e^{-a(r-r_0)}]^2$, which allows dissociation. At room temperature a bond explores only the very bottom of its well, where the harmonic term is an adequate fit.

How stiff is it? In the canonical ensemble a harmonic coordinate has variance $k_BT/k$:

| Bond | $r_0$ (nm) | $k_b$ (kJ mol$^{-1}$ nm$^{-2}$) | Thermal fluctuation $\sqrt{k_BT/k_b}$ at 300 K |
|---|---|---|---|
| C-C (aliphatic) | 0.153 | about $2.6\times10^5$ | 0.003 nm |
| C-H | 0.109 | about $2.8\times10^5$ | 0.003 nm |
| C=O | 0.123 | about $4.8\times10^5$ | 0.002 nm |

Bonds fluctuate by about 2 % of their length. They carry almost no conformational information, which is why constraining them (Module 9) costs little accuracy.

## Angle bending

$$
U_\theta = \tfrac12 k_\theta\,(\theta-\theta_0)^2
$$

Typical $k_\theta$ is 300 to 700 kJ mol$^{-1}$ rad$^{-2}$, giving fluctuations of $\sqrt{2.494/500} \approx 0.07$ rad, about 4°. CHARMM adds a **Urey-Bradley** term, a harmonic spring between atoms 1 and 3 of the angle, to improve vibrational spectra. GROMOS uses a harmonic function of $\cos\theta$, which is cheaper and avoids a singularity at 180°.

## Torsions (proper dihedrals)

The dihedral angle $\phi$ of four bonded atoms i-j-k-l is the angle between the planes (i,j,k) and (j,k,l). Rotation about the central bond is periodic, so the energy is a short Fourier series:

$$
U_\phi = \sum_{n} k_{\phi,n}\,\big[1+\cos(n\phi-\delta_n)\big],\qquad n = 1,2,3,(4,6).
$$

$n$ is the multiplicity (the number of minima in a full turn), $\delta_n$ the phase (0 or 180° in most force fields), and $k_{\phi,n}$ is half the barrier height of that component. For ethane-like rotation about an sp$^3$-sp$^3$ bond, $n=3$ with a total barrier near 12 kJ/mol ($\approx 5\,k_BT$).

<div class="box key" markdown="1">
**Torsions are where the biology is.** Barriers of a few $k_BT$ mean torsions are the soft degrees of freedom that change during conformational transitions: the backbone $\phi$ and $\psi$ angles and the side-chain $\chi$ angles. They are also the least "physical" term: the torsion parameters absorb everything the other terms get wrong, and they are fitted last (Module 6). Almost every revision of a protein force field in the last 25 years (ff99SB, ILDN, ff14SB, CHARMM22/CMAP, CHARMM36, CHARMM36m) is mainly a re-fit of backbone or side-chain torsions.
</div>

Two variants you will meet:

- **Ryckaert-Bellemans** form, a power series in $\cos\psi$ with $\psi=\phi-180°$, used by OPLS in GROMACS. It is mathematically equivalent to a Fourier series.
- **CMAP** (CHARMM and ff19SB): a two-dimensional correction $U_{CMAP}(\phi,\psi)$ stored on a grid and interpolated with bicubic splines. It captures the coupling between the two backbone dihedrals that separate one-dimensional terms cannot.

## Improper dihedrals

$$
U_\omega = \tfrac12 k_\omega\,(\omega-\omega_0)^2\quad\text{(CHARMM, GROMOS)}\qquad\text{or}\qquad k\,[1+\cos(2\omega-180°)]\quad\text{(AMBER)}
$$

An improper keeps four atoms in a plane (the peptide bond, aromatic rings, carboxylates) or, in united-atom force fields, preserves the chirality of a carbon whose hydrogen is not represented.

## Lennard-Jones: repulsion and dispersion

$$
U_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right]
= \frac{C_{12}}{r^{12}}-\frac{C_6}{r^6},\qquad C_6 = 4\varepsilon\sigma^6,\; C_{12} = 4\varepsilon\sigma^{12}.
$$

- $\sigma$ is the distance where the energy is zero, the "size" of the atom pair.
- The minimum is at $r_{min} = 2^{1/6}\sigma\approx1.122\,\sigma$ with depth $-\varepsilon$. AMBER and CHARMM files list $R_{min}/2$ per atom instead of $\sigma$.
- **The $r^{-6}$ attraction is physical.** It is the London dispersion energy: a fluctuation of the electron cloud on one atom creates an instantaneous dipole, which induces a dipole on the other, and the interaction of the two falls off as $r^{-6}$.
- **The $r^{-12}$ repulsion is a convenience.** Pauli repulsion from overlapping electron clouds is closer to exponential. $r^{-12}$ was chosen because it is the square of $r^{-6}$ and so costs one multiplication. It is somewhat too steep. The Buckingham potential $A e^{-Br} - C/r^6$ is more realistic and slower.

Typical values of $\varepsilon$ are 0.1 to 1 kJ/mol, well below $k_BT$ = 2.5 kJ/mol. A single dispersion contact is weak. Their importance comes from their number: a buried side chain has dozens.

### Combining rules

Force fields store $\sigma_i$ and $\varepsilon_i$ per atom type and build pair parameters from a rule:

| Rule | $\sigma_{ij}$ | $\varepsilon_{ij}$ | Used by |
|---|---|---|---|
| Lorentz-Berthelot | $\tfrac12(\sigma_i+\sigma_j)$ | $\sqrt{\varepsilon_i\varepsilon_j}$ | AMBER, CHARMM |
| Geometric | $\sqrt{\sigma_i\sigma_j}$ | $\sqrt{\varepsilon_i\varepsilon_j}$ | OPLS, GROMOS (on $C_6$, $C_{12}$) |

The rules are approximations. Where they fail badly, force fields override them for specific pairs (**NBFIX** in CHARMM, for example for ion-carboxylate pairs).

<div class="widget" data-widget="lj"></div>

## Electrostatics

$$
U_C = \frac{q_iq_j}{4\pi\varepsilon_0\,r_{ij}} = 138.935\ \frac{q_iq_j}{r_{ij}}\ \text{kJ/mol}\quad(q \text{ in } e,\ r \text{ in nm}).
$$

Each atom carries a fixed **partial charge** placed at its nucleus. The charges represent the uneven distribution of electrons in the molecule: in a peptide group, about $-0.5\,e$ on O, $+0.5\,e$ on C, $-0.4\,e$ on N and $+0.3\,e$ on H (values vary by force field). There is no explicit hydrogen-bond term in modern force fields. A hydrogen bond is the sum of the Coulomb attraction between a positive H and a negative acceptor and the Lennard-Jones terms of the heavy atoms.

There is no dielectric constant in the formula ($\varepsilon_r=1$). Screening by water is produced explicitly by the water molecules reorienting.

Two features make electrostatics the hardest part:

- **It is long-ranged.** $1/r$ decays so slowly that it cannot be truncated without artefacts. Module 7 covers the solution, Ewald summation.
- **It is large.** Two unit charges at 0.3 nm in vacuum interact with 463 kJ/mol, about 186 $k_BT$. Net effects in solution are small differences between large numbers (direct interaction against desolvation), which is one reason binding energies are hard to compute.

## Which pairs count: exclusions and 1-4 scaling

Atoms separated by one bond (1-2) or two bonds (1-3) are **excluded** from the non-bonded sum, since the bond and angle terms already describe them. Atoms separated by three bonds (1-4, the ends of a dihedral) interact through a scaled non-bonded term:

| Force field | 1-4 Lennard-Jones | 1-4 Coulomb |
|---|---|---|
| AMBER | × 0.5 | × 1/1.2 = 0.833 |
| OPLS-AA | × 0.5 | × 0.5 |
| CHARMM | × 1 (special 1-4 parameters for some types) | × 1 |
| GROMOS | separate 1-4 parameter list | × 1 |

The torsion parameters are fitted together with a particular 1-4 scaling. This is one of several reasons you cannot mix parameters from different force-field families.

## From energy to force

MD needs $\mathbf F_i = -\partial U/\partial\mathbf r_i$ for every term. For any term that depends on the distance between two atoms (bonds, Lennard-Jones, Coulomb), Module 2 gave

$$
\mathbf F_i = -\frac{dU}{dr}\,\frac{\mathbf r_{ij}}{r_{ij}},\qquad \mathbf F_j=-\mathbf F_i .
$$

For Lennard-Jones:

$$
-\frac{dU_{LJ}}{dr} = \frac{24\varepsilon}{r}\left[2\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right]
\quad\Longrightarrow\quad
\mathbf F_i = \frac{24\varepsilon}{r^2}\left[2\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right]\mathbf r_{ij}.
$$

Only $r^2$ appears, never $r$ itself, so no square root is needed. This is the real reason for the 12-6 form. For Coulomb, $\mathbf F_i = 138.935\,q_iq_j\,\mathbf r_{ij}/r^3$.

For angles and dihedrals, use the chain rule through the internal coordinate, $\mathbf F_i = -\dfrac{dU}{d\theta}\dfrac{\partial\theta}{\partial\mathbf r_i}$. For an angle i-j-k with $\cos\theta = \hat{\mathbf r}_{ji}\cdot\hat{\mathbf r}_{jk}$,

$$
\frac{\partial\cos\theta}{\partial\mathbf r_i} = \frac{1}{r_{ji}}\left(\hat{\mathbf r}_{jk} - \cos\theta\,\hat{\mathbf r}_{ji}\right),
\qquad \mathbf F_i = \frac{1}{\sin\theta}\frac{dU}{d\theta}\,\frac{\partial\cos\theta}{\partial\mathbf r_i},
$$

with the analogous expression for $k$, and $\mathbf F_j = -\mathbf F_i-\mathbf F_k$ because internal forces sum to zero. Dihedral forces follow the same route with more algebra. The standard derivation is in the GROMACS reference manual and in Allen and Tildesley.

<div class="box key" markdown="1">
**Always test forces numerically.** Move one atom by $\pm h$ along $x$ (with $h\approx10^{-5}$ nm), compute $-[U(x+h)-U(x-h)]/2h$ and compare with the analytic force. This five-line test catches most bugs in a new potential, including in machine-learned force fields.
</div>

## How many terms?

For a protein in water with $N$ atoms there are about $N$ bonds, $2N$ angles and $3N$ dihedrals, all cheap. The non-bonded sum has $N(N-1)/2$ pairs, about $5\times10^9$ for 100,000 atoms. Reducing that to the roughly $2\times10^7$ pairs inside a cutoff, while still treating the long-range part correctly, is the subject of Module 7.

## What this model leaves out

- **Electronic polarisation.** Charges are fixed, so a molecule has the same charge distribution in water, in a protein interior and at a membrane. Force fields compensate on average by using charges that are larger than in the gas phase. The water models have dipole moments of 2.2 to 2.4 D, against 1.85 D for an isolated water molecule. Polarizable force fields (Module 6) address this at higher cost.
- **Charge transfer and bond breaking.** No chemistry.
- **Many-body dispersion and anisotropy.** Atom-centred charges cannot represent lone pairs, $\pi$ clouds or $\sigma$-holes (halogen bonds) unless extra sites are added.
- **Coupling between terms.** Class II force fields (for materials) add cross terms such as bond-angle coupling. Biomolecular force fields mostly do not.

Each omission is absorbed, as far as possible, into the fitted parameters. That makes the parameters **effective**: they work as a set, in the conditions they were fitted for.

## Check yourself

<details markdown="1"><summary>1. Convert the AMBER C-C bond constant K = 310 kcal mol⁻¹ Å⁻² to GROMACS units and convention.</summary>
$k = 2\times310\times4.184\times100 = 259{,}408$ kJ mol$^{-1}$ nm$^{-2}$. The 2 is the convention, 4.184 converts kcal to kJ, 100 converts Å$^{-2}$ to nm$^{-2}$.
</details>

<details markdown="1"><summary>2. At what distance is the Lennard-Jones force zero? Where is it most attractive?</summary>
Zero at the minimum, $r = 2^{1/6}\sigma$. The most attractive force is where $d^2U/dr^2=0$: $r = (26/7)^{1/6}\sigma \approx 1.245\,\sigma$.
</details>

<details markdown="1"><summary>3. Why is there no explicit dielectric constant of 80 in the Coulomb term of an explicit-solvent simulation?</summary>
The dielectric constant is a macroscopic average of how water dipoles reorient and screen charges. In explicit solvent the water molecules are present and do the screening themselves, so the bare interaction with $\varepsilon_r=1$ is the correct microscopic law. A dielectric constant appears only in implicit-solvent models (Module 15).
</details>

<details markdown="1"><summary>4. A torsion has a single term with n = 3 and k = 6 kJ/mol. How high is the barrier and how often is it crossed, roughly?</summary>
The barrier is $2k = 12$ kJ/mol $= 4.8\,k_BT$ at 300 K. With an attempt frequency of the order of $10^{12}$ to $10^{13}$ s$^{-1}$, the rate is about $10^{12.5}e^{-4.8}\approx3\times10^{10}$ s$^{-1}$: one crossing every few tens of picoseconds. Easily sampled.
</details>

## Exercises

1. Write a Python function that returns the energy and forces of a bond, an angle and a Lennard-Jones pair. Verify each force with the finite-difference test.
2. Plot the torsional energy of butane using three Fourier terms of your choice so that the trans minimum is 3.5 kJ/mol below gauche. Compute the trans population at 300 K by numerical integration.
3. For two water molecules in a linear hydrogen bond (O...O distance 0.28 nm), sum the nine Coulomb terms and the O-O Lennard-Jones term using TIP3P parameters ($q_O=-0.834$, $q_H=+0.417$, $\sigma=0.3151$ nm, $\varepsilon=0.636$ kJ/mol). Which term dominates?
4. Using the pair-energy demo, find the charge product at which the Coulomb term equals the Lennard-Jones well depth at the minimum.

## Read

{{READ}}

## Key papers

{{PAPERS}}
