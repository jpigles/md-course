---
num: 15
title: Coarse-grained models, from Martini to Gō models and implicit solvent
short: Coarse-grained models
part: Part V · Beyond all-atom
hours: 8
summary: Understand what a coarse-grained potential is in statistical-mechanical terms, how the main model families are built, and what each can and cannot predict.
videos: 14
papers: J
tags: coarse-graining
---

<div class="box goal" markdown="1">
#### After this module you can

- define a coarse-grained mapping and show that the ideal coarse-grained potential is a many-body potential of mean force;
- explain bottom-up (Boltzmann inversion, force matching, relative entropy) and top-down parameterisation;
- describe the Martini model and its settings;
- write the energy function of a C$\alpha$ structure-based (Gō) model and explain what "native-centric" implies;
- write the Debye-Hückel and generalised Born expressions and state their assumptions;
- judge what time, energy and temperature mean in a coarse-grained simulation.
</div>

## Watch first

{{WATCH}}

## Why coarse-grain

<div data-videos="yBnn567JXdo 0XZ8tAwNHdE 0NJxWb-sXg8"></div>

All-atom simulation spends most of its effort on water and on fast local motions. A coarse-grained (CG) model replaces groups of atoms by single interaction sites ("beads"). The gain comes from four sources at once: fewer particles, shorter-ranged and simpler interactions, a larger time step because the fast vibrations are gone, and faster effective dynamics because the energy landscape is smoother. Speed-ups of $10^2$ to $10^5$ result, which brings membranes, large assemblies, folding, binding and phase separation within reach.

The price is that the model answers fewer questions, and you must know which.

| Resolution | Sites | Examples |
|---|---|---|
| All-atom | every atom | AMBER, CHARMM |
| United-atom | non-polar H merged | GROMOS |
| About 4 heavy atoms per bead | 2 to 5 beads per residue | Martini, SIRAH |
| One bead per residue | C$\alpha$ | Gō and structure-based models, elastic network models, HPS, CALVADOS, AWSEM (three sites) |
| Many residues per bead | domains | Shape-based and domain-level models, patchy-particle models |

## What a coarse-grained potential is

<div data-videos="TqHS4tpujnw"></div>

Let $\mathbf r$ be the atomistic coordinates and $\mathbf R=\mathbf M(\mathbf r)$ the CG coordinates, for example the centre of mass of each group. The CG model reproduces the atomistic distribution of $\mathbf R$ exactly if and only if its potential is

$$
\boxed{U_{CG}(\mathbf R) = -k_BT\ln\int d\mathbf r\;\delta\big(\mathbf M(\mathbf r)-\mathbf R\big)\,e^{-\beta u(\mathbf r)}+\text{const}}
$$

This is the **many-body potential of mean force** of the CG sites: the PMF of Module 3 with all the CG coordinates as the collective variables. Three consequences follow directly from the fact that it is a free energy, not an energy.

1. **It depends on the thermodynamic state.** Entropy of the eliminated degrees of freedom is folded in, so $U_{CG}$ changes with temperature, density and composition. A model fitted at 300 K is not automatically valid at 350 K. This is the **transferability** problem.
2. **It is many-body.** Even if the atomistic potential is pairwise, the integral is not. Practical CG models approximate $U_{CG}$ by pair potentials, and that approximation, not the idea of coarse-graining, is the main source of error.
3. **Not all properties can be right together.** A pair-potential model that reproduces the structure (the distribution functions) does not in general reproduce the pressure or the energy. This is the **representability** problem. Energies and entropies taken separately from a CG model do not correspond to the atomistic ones; only the free energy does.

### Bottom-up parameterisation

Fit the CG model to an atomistic simulation.

- **Boltzmann inversion.** For a single coordinate $q$ with distribution $P(q)$ from the atomistic reference, use $U(q)=-k_BT\ln\big[P(q)/J(q)\big]$, where $J$ is the Jacobian of the coordinate: $J=r^2$ for a bond length, $J=\sin\theta$ for a bond angle, $J=1$ for a dihedral. (Without it the potential picks up a spurious $-2k_BT\ln r$ or $-k_BT\ln\sin\theta$, which is badly wrong for angles near 180°.) Adequate for bonds and angles, which are nearly independent of the rest.
- **Iterative Boltzmann inversion.** For non-bonded pair potentials, correct the potential until the CG simulation reproduces the target radial distribution function: $U_{n+1}(r)=U_n(r)+k_BT\ln\big[g_n(r)/g_{target}(r)\big]$.
- **Force matching** (multiscale coarse-graining; [Izvekov and Voth 2005](cite:izvekov2005)). Choose the CG force field whose forces best match the atomistic forces projected onto the CG sites, minimising $\chi^2=\big\langle\sum_I|\mathbf F_I^{CG}(\mathbf M(\mathbf r))-\mathbf f_I(\mathbf r)|^2\big\rangle$. It can be shown ([Noid et al. 2008](cite:noid2008)) that, for a linear mapping in which each atom contributes to at most one site, the force field that minimises $\chi^2$ over all possible force fields is the mean force, $\mathbf F^{CG}=-\nabla U_{CG}$, with $U_{CG}$ the many-body PMF.
- **Relative entropy** ([Shell 2008](cite:shell2008)). Minimise $S_{rel}=\sum p_{AA}\ln(p_{AA}/p_{CG})$, the information lost when the CG model stands in for the atomistic ensemble.

### Top-down parameterisation

Fit the CG model directly to experimental data: partition free energies, densities, radii of gyration, phase behaviour. Martini and the residue-level models for disordered proteins are built this way.

## Time, energy and temperature in a coarse-grained model

- **Time.** Removing degrees of freedom removes friction and smooths the landscape, so CG dynamics are faster than real dynamics by a factor that is not constant across processes. Martini quotes a factor of about 4 for diffusion. For C$\alpha$ models run with low-friction Langevin dynamics, simulated time has no simple relation to real time. Use CG models for thermodynamics and mechanisms; treat time scales as qualitative unless calibrated.
- **Energy scale.** In top-down and structure-based models the interaction strength is a free parameter, often expressed in reduced units, and is calibrated against an experimental observable (a folding temperature, a binding constant, a radius of gyration).
- **Temperature.** For the same reason, the temperature of a structure-based model is a reduced temperature relative to its folding temperature, not Kelvin, unless the energy scale has been calibrated.

## Martini

<div data-videos="Yq1f8vDfPe4 EVcw-w-Lcnk"></div>

[Marrink et al. (2007)](cite:marrink2007); Martini 3 by [Souza et al. (2021)](cite:souza2021). Among the most widely used CG models for biomolecular systems, especially membranes.

- **Mapping.** About four heavy atoms per bead (two to three for rings and small groups). One water bead represents four water molecules. Each amino acid is one backbone bead plus zero to four side-chain beads (five for tryptophan in Martini 3).
- **Bead types.** Chemical character is encoded in the type: charged (Q), polar (P), intermediate (N) and apolar (C), each with sub-levels, in three sizes in Martini 3 (regular, small, tiny). Martini 3 also has classes for halogens, divalent ions and water, and labels for hydrogen-bond donors and acceptors.
- **Interactions.** Lennard-Jones 12-6 between beads with $\varepsilon$ taken from a fixed interaction matrix of levels, a cutoff of 1.1 nm, and Coulomb interactions with reaction field and a relative dielectric constant of 15 (2.5 with the polarizable water model).
- **Parameterisation.** Top-down for non-bonded terms: reproduce experimental partitioning free energies between polar and apolar solvents. Bonded terms come from atomistic simulations.
- **Time step.** 20 fs.

Limits for proteins: Martini cannot fold a protein or change its secondary structure. The secondary structure is an input, and the tertiary structure is held by an **elastic network** of harmonic springs between backbone beads within a cutoff, or by a Gō-like contact map (GōMartini). Martini 2 over-estimated protein-protein and protein-sugar attraction. Martini 3 was rebalanced, though later studies report that the stickiness of some systems and the compactness of disordered proteins still need case-by-case adjustment (for example by rescaling protein-water interactions).

## Structure-based (Gō) models

<div data-videos="tRVeUbgcGVY AsKi8lXJWyM"></div>

**The physical idea.** Energy landscape theory holds that natural proteins are *minimally frustrated*: the interactions present in the native structure are mutually consistent and much more stabilising than random non-native ones, so the landscape is a funnel towards the native state. A structure-based model takes this to the limit: **only interactions present in the known native structure are attractive**. The model is defined by a structure, not by chemistry.

**The C$\alpha$ model** ([Clementi, Nymeyer and Onuchic 2000](cite:clementi2000)). One bead per residue at the C$\alpha$ position:

$$
\begin{aligned}
U={}&\sum_{bonds}K_r\,(r-r_0)^2+\sum_{angles}K_\theta\,(\theta-\theta_0)^2
+\sum_{dihedrals}K_\phi\Big\{\big[1-\cos(\phi-\phi_0)\big]+\tfrac12\big[1-\cos3(\phi-\phi_0)\big]\Big\}\\
&+\sum_{native\ contacts}\varepsilon\left[5\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12}-6\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{10}\right]
+\sum_{non\text{-}native}\varepsilon\left(\frac{\sigma_{rep}}{r_{ij}}\right)^{12}
\end{aligned}
$$

Every reference value ($r_0$, $\theta_0$, $\phi_0$, $\sigma_{ij}$) is measured in the native structure. The 12-10 contact term has its minimum of depth $-\varepsilon$ exactly at the native distance $\sigma_{ij}$. Native contacts are found from the structure with a cutoff or a shadow-map algorithm. All other pairs only repel. In the original model every contact has the same $\varepsilon$, and energies and temperatures are in units of $\varepsilon$.

**Variants.**

- **Sequence-dependent contact energies.** [Karanicolas and Brooks (2002)](cite:karanicolas2002) weight each side-chain native contact by its Miyazawa-Jernigan residue-pair energy (hydrogen-bond contacts keep one uniform strength) and use a contact potential with a small desolvation barrier,
  $U_{ij}=\varepsilon_{ij}\left[13(\sigma_{ij}/r)^{12}-18(\sigma_{ij}/r)^{10}+4(\sigma_{ij}/r)^6\right]$, together with sequence-dependent backbone dihedral terms. This puts some chemistry back.
- **All-atom structure-based models**: every heavy atom is a bead, contacts and dihedrals are native-centric. The SMOG 2 software builds these, the C$\alpha$ model above and several variants (in its implementation the contact strength and the non-native repulsion have separate constants).
- **Electrostatics.** Charged residues interact through a Debye-Hückel term (below), which adds non-native, sequence-dependent interactions and salt dependence.
- **Multi-basin models** combine the contact maps of two or more structures to simulate conformational change.

**Statistical contact potentials.** The Miyazawa-Jernigan matrix gives an effective contact energy for each of the 210 residue pairs, derived from how often the pair is found in contact in known structures compared with a reference state, in the spirit of $e_{ij}\sim-k_BT\ln(\text{observed}/\text{expected})$. It is a knowledge-based potential of mean force, not a physical energy, and its values are in units of $k_BT$ at an effective temperature.

**What Gō models are good for.** Folding mechanisms, transition states and their dependence on topology (and, with sequence-weighted contacts, on sequence: the model of [Karanicolas and Brooks 2002](cite:karanicolas2002) reproduces the different folding routes of proteins L and G, which share one topology); coupled folding and binding of disordered proteins when the bound structure is known; mechanical unfolding; large conformational transitions. The fraction of native contacts $Q$ is the natural reaction coordinate and usually a good one.

**What they cannot do.** They cannot predict a structure, a non-native intermediate or a misfolded state, because non-native attraction is absent by construction. They do not give absolute stabilities or affinities: the energy scale is calibrated per system, and a model built from a predicted complex inherits every error of that prediction and will stabilise it regardless. Comparisons are most meaningful between closely related systems treated identically.

## Residue-level models for disordered proteins and condensates

<div data-videos="jFmGNUUVHzg _6iAcwmknek"></div>

For disordered proteins there is no native structure to encode. These models use one bead per residue, bonded by springs, with two non-bonded terms.

**Hydropathy-scaled Lennard-Jones** (Ashbaugh-Hatch form), where each residue has a "stickiness" $\lambda_i\in[0,1]$ and $\lambda=\tfrac12(\lambda_i+\lambda_j)$:

$$
U_{AH}(r)=\begin{cases}U_{LJ}(r)+(1-\lambda)\,\varepsilon, & r\le2^{1/6}\sigma\\[2pt]\lambda\,U_{LJ}(r), & r>2^{1/6}\sigma\end{cases}
$$

The repulsive force does not depend on $\lambda$ (the repulsive branch is only shifted in energy), and the depth of the attractive well is $\lambda\varepsilon$.

**Screened electrostatics** (Debye-Hückel) between charged residues.

In the HPS model ([Dignon et al. 2018](cite:dignon2018)) the $\lambda$ values come from a hydrophobicity scale. In CALVADOS ([Tesei et al. 2021](cite:tesei2021) and later versions) they are optimised against SAXS and paramagnetic relaxation data for many disordered proteins. These models reproduce radii of gyration (in CALVADOS these are training data, so the independent tests are its predictions for pairs of chains and for phase separation), and qualitative trends in the tendency to phase-separate, from sequence alone, at a cost that allows a hundred or more chains. Absolute transition temperatures are not reliable ([Dignon et al. 2018](cite:dignon2018)). In [Tesei et al. (2021)](cite:tesei2021), for example, the saturation concentrations matched experiments done near 24 °C only when the model was simulated at 50 °C.

## Implicit solvent

<div data-videos="2yf__V4EhGI AzCzDYLimvc"></div>

Replace the water by its average effect on the solute.

**Debye-Hückel.** In a salt solution, mobile ions screen electrostatic interactions. Linearising the Poisson-Boltzmann equation around a point charge gives

$$
U_{DH}(r)=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_r\,r}\,e^{-r/\lambda_D},\qquad
\lambda_D=\sqrt{\frac{\varepsilon_0\varepsilon_rk_BT}{2N_Ae^2I}}\approx\frac{0.304}{\sqrt{I\,[\text{M}]}}\ \text{nm (water, 25 °C)},
$$

with $I$ the ionic strength. At 150 mM, $\lambda_D$ = 0.79 nm. Assumptions: weak potentials (the linearisation fails near highly charged groups), point ions, and a uniform dielectric constant, which is far from true at a protein interface where water is excluded. It contains no desolvation penalty.

<div class="widget" data-widget="cgpot"></div>

**Poisson-Boltzmann.** The full continuum treatment solves, for a solute with low dielectric constant inside and high outside,

$$
\nabla\cdot\big[\varepsilon(\mathbf r)\nabla\phi(\mathbf r)\big]=-\rho_{solute}(\mathbf r)-\sum_ic_i^\infty q_i\,e^{-\beta q_i\phi(\mathbf r)} .
$$

Accurate within the continuum picture, but too slow to solve at every MD step.

**Generalised Born** ([Still et al. 1990](cite:still1990)). An analytical approximation to the Poisson solution that is fast enough for MD:

$$
\Delta G_{pol}=-\frac{1}{8\pi\varepsilon_0}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right)\sum_{i,j}\frac{q_iq_j}{f_{GB}},\qquad
f_{GB}=\sqrt{r_{ij}^2+R_iR_j\exp\left(-\frac{r_{ij}^2}{4R_iR_j}\right)} .
$$

$R_i$ is the effective **Born radius** of atom $i$, a measure of how deeply it is buried. For $i=j$ the term reduces to the Born formula for the solvation of an ion of radius $R_i$. For distant atoms, the GB pair term added to the direct Coulomb interaction (computed with $\varepsilon_{in}$) gives Coulomb's law with the solvent dielectric constant. A non-polar term proportional to the solvent-accessible surface area, $\gamma\cdot\mathrm{SASA}$, is added for cavity formation and dispersion (GB/SA). Implicit solvent removes the cost of water and the viscosity that slows conformational change. It loses specific water molecules (bridging waters, the structure of the first hydration shell), and tends to over-stabilise salt bridges and helices, depending on the variant.

**Dynamics.** With no explicit solvent there are no collisions, so CG and implicit-solvent models are run with Langevin or Brownian dynamics (Module 8), which supply friction and thermal noise. The friction coefficient then sets the time scale.

## Check yourself

<details markdown="1"><summary>1. Why is a coarse-grained potential temperature-dependent even when the atomistic one is not?</summary>
It is a free energy obtained by integrating out degrees of freedom, $U_{CG}=-k_BT\ln\int\dots$. The entropy of the eliminated coordinates contributes a term proportional to $T$.
</details>

<details markdown="1"><summary>2. You build a Gō model from a predicted complex in which the binder is docked in the wrong orientation. What will the simulation show?</summary>
A stable complex in the wrong orientation, with a well-behaved binding free-energy profile. The model makes whatever contacts it is given attractive, so it cannot detect that the input structure is wrong. Structure-based models rank and characterise poses; they do not validate them.
</details>

<details markdown="1"><summary>3. What is the Debye length at 50 mM and at 500 mM ionic strength, and what does it imply for a salt bridge with a 0.4 nm separation?</summary>
$0.304/\sqrt{0.05}=1.36$ nm and $0.304/\sqrt{0.5}=0.43$ nm. The screening factor $e^{-r/\lambda_D}$ at 0.4 nm is 0.75 and 0.39: Debye-Hückel predicts the interaction is halved by the higher salt. At such short range the continuum assumptions are doubtful, so treat this as a trend.
</details>

<details markdown="1"><summary>4. A Martini simulation shows a protein complex dissociating after 2 µs. Can you quote a residence time of 2 µs?</summary>
No. Martini dynamics are accelerated by a factor that is roughly 4 for lipid and water diffusion and unknown for protein-protein dissociation, and Martini's protein-protein interaction strengths are approximate. The observation says the complex is weakly bound in the model.
</details>

## Exercises

1. Take a 100 ns all-atom trajectory of a small peptide. Map it to one bead per residue. Compute the distribution of bead-bead bond lengths and angles and derive bonded CG potentials by Boltzmann inversion, with and without the Jacobian. How large is the difference for the angles?
2. Build a C$\alpha$ structure-based model of a small protein with the SMOG web server and run it at several temperatures. Plot $Q$ against time near the folding temperature and identify the two states.
3. Plot the 12-10 and the 12-10-6 contact potentials on the same axes for $\sigma$ = 0.6 nm. Where is the desolvation barrier and how high is it in units of $\varepsilon$?
4. Compute $f_{GB}$ for two atoms with Born radii of 0.2 nm at separations of 0, 0.3 and 2 nm. Show that $f_{GB}\to R$ at zero separation (the Born limit) and $f_{GB}\to r$ at large separation, and that in the second case the GB pair term plus the direct Coulomb term with $\varepsilon_{in}$ equals Coulomb's law with $\varepsilon_{out}$.
5. Run a single-chain CALVADOS simulation of a disordered sequence of your choice and compare its radius of gyration with the Flory scaling $R_g\approx0.2\,N^{0.6}$ nm.

## Read

{{READ}}

## Key papers

{{PAPERS}}
