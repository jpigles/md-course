---
num: 6
title: Force fields II, where the parameters come from and which to use
short: Force fields: parameters
part: Part II · The engine
hours: 6
summary: Understand how charges, Lennard-Jones and torsion parameters are fitted, how the main protein force fields and water models differ, and what was changed to make them work for disordered proteins.
videos: 18 5
papers: F G
tags: force-fields, water-models
---

<div class="box goal" markdown="1">
#### After this module you can

- describe the fitting pipeline of a force field and the order in which terms are fitted;
- write the RESP charge-fitting problem as a constrained least-squares problem;
- compare AMBER, CHARMM, OPLS and GROMOS, and the common water models, and choose a tested combination;
- explain why older force fields made disordered proteins too compact and what fixed it;
- say what polarizable force fields add and what they cost.
</div>

## Watch first

{{WATCH}}

## Parameterisation is a fitting problem

A force field has thousands of parameters. They are found by minimising a weighted sum of squared deviations from reference data:

$$
\chi^2(\mathbf p) = \sum_{k} w_k\,\big[A_k^{calc}(\mathbf p) - A_k^{ref}\big]^2 .
$$

The reference data are of two kinds:

- **Quantum chemistry** on small model compounds: optimised geometries, vibrational frequencies, the electrostatic potential around the molecule, energy scans along torsions, interaction energies of dimers.
- **Experiment**, mostly on pure liquids and solutions: density, heat of vaporisation, hydration free energy, and for proteins NMR observables.

The terms are fitted in a fixed order, because each depends on the ones before:

1. **Equilibrium bond lengths and angles** from crystal structures and QM geometries; **force constants** from vibrational frequencies.
2. **Partial charges** from the QM electrostatic potential or from interactions with water.
3. **Lennard-Jones parameters** from liquid densities and heats of vaporisation, since those depend on how tightly molecules pack and how strongly they attract.
4. **Torsions last**, as a correction: $U_{tors}(\phi) \approx E_{QM}(\phi) - E_{MM}^{\,no\ tors}(\phi)$. The torsion term is the difference between a QM energy scan and what all the other terms already give.

Because torsions are a residual, they are specific to the charges, 1-4 scaling and Lennard-Jones set they were fitted with. Parameters are not transferable between families.

### Fitting charges: ESP and RESP

Compute the QM electrostatic potential $V^{QM}(\mathbf r_k)$ on a few thousand points $k$ around the molecule, outside the van der Waals surface. Choose atom-centred charges whose Coulomb potential reproduces it, with the total charge fixed by a Lagrange multiplier $\lambda$:

$$
\chi^2_{ESP} = \sum_k\Big[V^{QM}(\mathbf r_k) - \sum_i\frac{q_i}{4\pi\varepsilon_0|\mathbf r_k-\mathbf r_i|}\Big]^2 + \lambda\Big(\sum_iq_i-Q_{tot}\Big).
$$

Setting $\partial\chi^2/\partial q_j=0$ gives a linear system, solved in one step. The problem is that charges on buried atoms (a carbon surrounded by hydrogens) are poorly determined: the potential outside barely depends on them, so they come out large and conformation-dependent. **RESP** (restrained ESP; Bayly et al. 1993) adds a hyperbolic penalty that pulls poorly determined charges towards zero:

$$
\chi^2_{RESP} = \chi^2_{ESP} + a\sum_i\left(\sqrt{q_i^2+b^2}-b\right).
$$

AMBER deliberately uses a low level of theory, HF/6-31G\*, for this step. It overestimates dipole moments by 10 to 20 %, which roughly mimics the polarisation a molecule experiences in water. This is how a fixed-charge model includes average polarisation.

The other families use different philosophies for the same goal. CHARMM adjusts charges to reproduce QM interaction energies and geometries of the molecule with individual water molecules. OPLS fits charges and Lennard-Jones parameters together to liquid properties. GROMOS fits to free energies of solvation and partitioning.

## The protein force-field families

| Family | Typical current choice for proteins | Atom resolution | Fitting philosophy | Native water |
|---|---|---|---|---|
| AMBER | ff14SB, ff19SB | All-atom | RESP charges from QM; torsions from high-level QM, then adjusted to NMR data | TIP3P (ff14SB), OPC (ff19SB) |
| CHARMM | CHARMM36m | All-atom | Water-interaction charges; CMAP backbone correction; target experimental data | CHARMM-modified TIP3P |
| OPLS | OPLS-AA/M (open), OPLS4 (commercial) | All-atom | Liquid-state properties | TIP3P, TIP4P |
| GROMOS | 54A7 | United-atom (non-polar H merged into C) | Solvation and partition free energies | SPC |

The lineage is worth knowing because papers cite specific versions. In AMBER: ff94 (Cornell et al. 1995), ff99, ff99SB (backbone fix, 2006), ff99SB-ILDN (side chains of Ile, Leu, Asp, Asn; Lindorff-Larsen et al. 2010), ff14SB (Maier et al. 2015), ff19SB (CMAP-style backbone, fitted with OPC water; Tian et al. 2020). In CHARMM: CHARMM22 (MacKerell et al. 1998), CHARMM22/CMAP (2004), CHARMM36 (Best et al. 2012), CHARMM36m (Huang et al. 2017).

For anything that is not a standard residue you need a **general force field** designed to be compatible with the protein one: GAFF/GAFF2 with AMBER, CGenFF with CHARMM, and the Open Force Field series (Parsley, Sage), which assigns parameters by chemical substructure patterns and is distributed in an open format.

<div class="box warn" markdown="1">
**Rules that save months.** (1) Use the protein force field with the water model and ion parameters it was validated with. (2) Use the cutoff scheme it was developed with (CHARMM: force switch from 1.0 to 1.2 nm). (3) Never combine protein parameters from one family with ligand parameters from another. (4) Read the force field's own paper for the recommended combination; do not rely on a tutorial's defaults.
</div>

## Water models

Water is 80 to 90 % of the atoms in a simulation, and its model decides hydration, screening and diffusion. The common models are rigid, with fixed charges:

| Model | Sites | Idea | Strength | Known weakness |
|---|---|---|---|---|
| SPC, SPC/E | 3 | Charges on O and H, one Lennard-Jones site on O. SPC/E adds a polarisation self-energy correction. | SPC/E: good diffusion and structure | Dielectric constant somewhat low |
| TIP3P | 3 | Same layout, fitted to density and heat of vaporisation (Jorgensen et al. 1983) | Default of AMBER and CHARMM; huge validation history | Diffuses about twice too fast; too little structure beyond the first shell |
| TIP4P-Ew, TIP4P/2005 | 4 | Negative charge moved off the oxygen to a massless site M on the bisector | TIP4P/2005: excellent phase diagram, density and dynamics | Dielectric constant too low (about 60) |
| OPC | 4 | Charges and geometry optimised freely to reproduce bulk properties (Izadi et al. 2014) | Very good dielectric constant, density and diffusion together | 4-site cost |
| TIP4P-D, a99SB-disp water | 4 | Dispersion ($C_6$) increased | Fixes over-compact disordered proteins | Changes pure-water properties slightly |
| TIP5P | 5 | Explicit lone-pair sites | Density maximum at 4 °C | Cost; less used with proteins |

Rough numbers to anchor the table, at about 298 K: experimental water has a self-diffusion coefficient of $2.3\times10^{-5}$ cm$^2$/s and a dielectric constant of 78. TIP3P gives a diffusion coefficient above $5\times10^{-5}$ cm$^2$/s and a dielectric constant in the 90s. SPC/E and OPC are close to experiment for diffusion. The exact values reported depend on cutoffs and system size, so take them from the original papers when you need them.

Two consequences for protein simulations: with TIP3P, everything that depends on solvent viscosity (diffusion, some conformational rates) is too fast by a factor of 2 to 3; and the balance between protein-water and protein-protein interactions, which decides whether a disordered chain is expanded or collapsed, depends strongly on the water model.

<div class="box key" markdown="1">
**The "missing term" of SPC/E.** A fixed-charge water has an enhanced dipole $\mu$ compared with the gas-phase value $\mu_0$. Creating that induced dipole costs energy, $E_{pol} = (\mu-\mu_0)^2/2\alpha$ with $\alpha$ the polarisability: 3.7 kJ/mol for the SPC dipole of 2.27 D and 5.2 kJ/mol for 2.35 D. Berendsen, Grigera and Straatsma (1987) pointed out that this cost must be added when comparing the model's heat of vaporisation with experiment. Refitting with it included gave SPC/E, with slightly larger charges and much better dynamics. The same reasoning matters whenever a fixed-charge model is fitted to a transfer between phases.
</div>

### Ions

Ion parameters are specific to the water model (Joung and Cheatham 2008 for AMBER with TIP3P, SPC/E or TIP4P-Ew). Older or mismatched parameters caused NaCl and KCl to crystallise at physiological concentration. Fixed-charge models also tend to over-stabilise salt bridges and ion-phosphate contacts; pair-specific corrections (NBFIX, or scaled ion charges in the "ECC" approach) reduce this.

## The disordered-protein problem

This matters if you work with intrinsically disordered proteins or regions (IDPs, IDRs).

Force fields up to about 2014 were tuned on folded proteins. When simulated with them, disordered proteins and unfolded states collapsed into compact globules, with radii of gyration well below SAXS and FRET measurements. The cause was a general imbalance: protein-protein interactions were too favourable compared with protein-water interactions, in part because the water models underestimate dispersion. The fixes took three routes:

| Approach | Example | What was changed |
|---|---|---|
| Strengthen protein-water Lennard-Jones | ff03ws, ff99SBws (Best, Zheng and Mittal 2014) | Protein-water $\varepsilon$ scaled by 1.10 |
| Change the water model | TIP4P-D (Piana et al. 2015) | Water dispersion coefficient increased by about 50 % |
| Re-fit protein and water together | a99SB-disp (Robustelli, Piana and Shaw 2018); CHARMM36m (Huang et al. 2017) | Backbone torsions, selected Lennard-Jones pairs and the water model, validated on both folded and disordered proteins |

The current practical choices for systems with both folded and disordered parts are a99SB-disp with its own water, CHARMM36m with its modified TIP3P, and ff19SB with OPC. No force field is right for every system: check against whatever experimental data exist for yours (SAXS radius of gyration, NMR chemical shifts, PRE).

## Beyond fixed charges: polarizable force fields

In a polarizable model the charge distribution responds to the local electric field $\mathbf E$.

- **Drude oscillator** (CHARMM Drude): each heavy atom carries an auxiliary charged particle attached by a spring with constant $k_D$. In a field the particle is displaced by $d = q_DE/k_D$, giving an induced dipole $\mu=q_Dd$ and a polarisability $\alpha = q_D^2/k_D$. It is run with an extended Lagrangian in which the Drude particles are kept cold, and needs a 1 fs step.
- **Induced point dipoles** (AMOEBA): each atom has a polarisability, and its induced dipole $\boldsymbol\mu_i = \alpha_i\,\mathbf E_i$ depends on the field from permanent charges *and* from all other induced dipoles, which requires a self-consistent iteration every step. AMOEBA also replaces point charges by permanent multipoles up to quadrupoles.
- **Fluctuating charges**: charges flow between atoms to equalise electronegativity.

The cost is typically 3 to 10 times that of a fixed-charge simulation. They are better for ions, for interfaces between very different environments, and for spectroscopy. For routine protein simulation they have not yet displaced the additive models, which have had far more tuning.

## How force fields are validated

Know these tests, because they are what "this force field is good" means in a paper:

- **Small-molecule liquids**: density, heat of vaporisation, hydration free energy (errors of about 4 kJ/mol are typical).
- **Peptides**: NMR scalar couplings ($^3J$, via the Karplus relation to $\phi$), helix propensities, populations of polyproline II, β and α regions.
- **Folded proteins**: stability of the native state over microseconds, NMR order parameters, residual dipolar couplings.
- **Folding**: reversible folding of small fast-folding proteins to the right structure and melting temperature.
- **Disordered proteins**: radius of gyration from SAXS, chemical shifts, paramagnetic relaxation enhancement.

Lindorff-Larsen et al. (2012) and Robustelli et al. (2018) are the standard systematic comparisons.

## What a topology file contains

The force field is applied to your molecule by a program (`gmx pdb2gmx`, `tleap`, CHARMM-GUI, OpenMM's `ForceField`) that matches residues to templates and writes a **topology**. Reading one is the best way to make the functional form concrete. A GROMACS topology has these sections:

```
[ atoms ]      ; nr  type  resnr  residue  atom  cgnr  charge    mass
                  1   N3     1      ALA     N     1    0.1414   14.01
[ bonds ]      ; ai  aj  funct   (r0 and kb are looked up from the atom types)
[ pairs ]      ; the 1-4 pairs, with scaled non-bonded interactions
[ angles ]     ; ai  aj  ak  funct
[ dihedrals ]  ; ai  aj  ak  al  funct   (9 = proper, 4 = improper in AMBER ports)
```

The atom **type** (here `N3`) is the key into the parameter tables: two atoms with the same type have the same Lennard-Jones parameters and take part in the same bonded parameters. The **charge** is per atom, set by the residue template.

## Check yourself

<details markdown="1"><summary>1. Why are torsion parameters fitted last?</summary>
Rotating about a bond also changes the 1-4 Coulomb and Lennard-Jones energies and slightly strains angles. The torsion term is defined as whatever is needed to make the total match the QM rotational profile, so it can only be fitted after the other terms are fixed.
</details>

<details markdown="1"><summary>2. You find a ligand parameterised with GAFF and want to simulate it with a CHARMM36m protein. Is that acceptable?</summary>
No. The charge models (RESP against water-interaction), 1-4 scaling (0.833 and 0.5 against 1.0) and the Lennard-Jones balance differ. Use CGenFF for the ligand with CHARMM36m, or switch the protein to an AMBER force field with GAFF2 or OpenFF.
</details>

<details markdown="1"><summary>3. A disordered region collapses onto the folded domain within 200 ns in ff14SB/TIP3P. What do you check before believing it?</summary>
Whether the same happens in a force field balanced for disorder (a99SB-disp, CHARMM36m, ff19SB/OPC). ff14SB with TIP3P is known to over-compact disordered chains, so the collapse may be an artefact.
</details>

<details markdown="1"><summary>4. Why does TIP3P water have a larger dipole moment than a real gas-phase water molecule?</summary>
In the liquid each molecule is polarised by its neighbours and its average dipole is larger than in the gas. A fixed-charge model cannot respond, so it is built with the enhanced, liquid-like dipole from the start.
</details>

## Exercises

1. Download the ff14SB and CHARMM36m parameter files (both are distributed with GROMACS ports). Find the backbone N-CA-C angle parameters in each and convert them to the same units and convention.
2. Set up the ESP fitting equations for a diatomic molecule with two charges and a total-charge constraint, and solve them symbolically. Show the result fixes only the dipole.
3. Simulate 1,000 molecules of TIP3P and of OPC water for 1 ns each (Module 10 gives the workflow). Compute the density and the self-diffusion coefficient from the mean squared displacement (Module 11). Compare with experiment.
4. Read the abstract and validation figures of Robustelli et al. 2018. List the classes of experimental data used and which force fields failed which class.

## Read

{{READ}}

## Key papers

{{PAPERS}}
