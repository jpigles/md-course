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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Module 5 wrote down the energy function of a force field: springs for bonds and angles, cosines for torsions, the Lennard-Jones term for repulsion and dispersion, and Coulomb's law between partial charges. That function is an empty form. It contains thousands of numbers (spring constants, charges, atom sizes), and the form says nothing about their values. This module is about where those numbers come from, and about what follows for you when you choose a force field.

You will probably never fit a force field yourself. You still need to know how it is done, for three reasons:

- The names in every methods section (ff14SB, CHARMM36m, TIP3P, OPC) are names of parameter sets, and you have to pick one.
- The way a set was fitted tells you what it can be trusted for and what it was never tested on.
- Most rules for setting up a simulation ("do not mix families", "use the water model that goes with the force field") follow from one idea: the parameters are fitted as a set, and each one compensates for the errors of the others.

The module has four layers:

1. **Fitting.** What it means to fit a parameter, what the reference data are, and how torsions and charges are obtained.
2. **The families.** AMBER, CHARMM, OPLS and GROMOS, then the water models and the ions.
3. **Limits and repairs.** Why older force fields failed for disordered proteins, what was changed, and what polarizable force fields add.
4. **Practice.** How a force field is tested, and what the file that carries the parameters of your own system looks like.

On a first reading the essential parts are the first section up to the end of "Transferability", the warning box "Rules that save months", the table of water models and the section on disordered proteins. The algebra of the charge fit (everything after the first formula in "Fitting charges") and the algebra of the Drude model can wait for a second reading.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The notation below is the part that is new in this module. Each item is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\chi^2$ | "Chi squared", read as one symbol: the total misfit between a model and its reference data. It is a sum of squares, so it is never negative. No quantity $\chi$ belongs to it. (The side-chain angle $\chi$ in the section on the families is a different thing.) |
| $A^{calc}$, $A^{ref}$, $V^{QM}$ | A word or an abbreviation written as a superscript is a **label**, not a power. $V^{QM}$ is "the potential from quantum mechanics". |
| $\mathbf p$ | A bold letter is a list of numbers. Here $\mathbf p$ is the list of all the parameters that are being fitted. (For positions, $\mathbf r_i$ is the list of the three coordinates of atom $i$, as in Module 2.) |
| $\sum_k$ | Add up the expression that follows for every value of the label $k$. |
| $\vert\mathbf r_k-\mathbf r_i\vert$ | Bars around a vector mean its length. Here: the distance between the point $\mathbf r_k$ and atom $i$. Bars around a single number, as in $\vert q\vert$, mean its size without its sign. |
| $\partial f/\partial q_j$ | A **partial derivative**: the slope of $f$ when only $q_j$ changes and every other variable is held fixed. |
| $i\in\text{heavy atoms}$ | "$i$ is a member of": the sum runs only over the atoms that are named. |
| $\approx$, $\equiv$, $\ll$, $\gg$ | "Is approximately equal to", "is defined as", "is much smaller than", "is much larger than". |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which meaning applies each time.

- $k$ numbers the reference data or the grid points in the fitting formulas, but $k_b$ and $k_D$ are spring constants, $k$ alone in $\omega=\sqrt{k/\mu}$ and in $\tfrac12kx^2$ is the force constant of a spring, and $k_B$ is the Boltzmann constant.
- $\varepsilon$ is the depth of a Lennard-Jones well, and $\varepsilon_0$ is the constant in Coulomb's law. The dielectric constant of water is a third thing, written out in words here.
- $\alpha$ is a polarisability in the formulas, and the name of a helix or of a region of backbone angles in the text.
- $\mu$ is a dipole moment, except in $\omega=\sqrt{k/\mu}$, where it is the reduced mass of Module 2. $q$ is a charge (in Module 2 it was a generalised coordinate).
- $\phi$ is any torsion angle in the fitting formulas and one particular backbone angle in the sections on proteins.
- $E$ with a label, as in $E_{QM}$, is an energy. $E$ alone is an energy in the first maths box and in the enthalpy $H = E + PV$. Everywhere else $E$ alone, or bold as $\mathbf E$, is an electric field.
- $A$ is a reference property in the first formula, a geometric factor $A_{ki}$ in the charge fit and a constant in the Karplus relation.
- $\chi^2$ is the misfit of a fit. $\chi$ alone, in the section on the families, is the name of the side-chain torsion angles.
- $e$ after a number, as in $0.5\,e$, is the elementary charge. $e$ with an exponent, as in $e^{10}$, is the number 2.718...
- $d$ is the stretch of a bond in the first maths box, the distance between the two charges of a dipole, and the displacement of a Drude particle.
- $D$ in italics is the diffusion coefficient. An upright D after a number is the unit debye.
</div>

## Parameterisation is a fitting problem

<div data-videos="1yAba9WBSS4 QCE6eyHWx6Y -EVNaaA6hYk gP6HfBQ_LkI"></div>

To **parameterise** a force field is to choose the values of its parameters. None of them can be measured directly. No experiment returns "the charge on a carbonyl oxygen" or "the Lennard-Jones size of a nitrogen", because these are numbers inside a model.

What can be measured or computed are properties of whole molecules and liquids, such as the energy of a conformation or the density of a liquid. So the parameters are found indirectly: you adjust them until the model reproduces a list of known properties as well as it can. That is **fitting**.

The smallest example is a straight line drawn through measured points. The line has two parameters, its slope and its intercept, and you choose the two values for which the line passes as close as possible to all the points together. A force field does the same with more parameters and more kinds of data.

A force field has thousands of parameters. They are found by minimising a weighted sum of squared deviations from reference data:

$$
\chi^2(\mathbf p) = \sum_{k} w_k\,\big[A_k^{calc}(\mathbf p) - A_k^{ref}\big]^2 .
$$

<div class="legend" markdown="1">
- $\mathbf p$: the list of all parameters that are being fitted (charges, force constants, Lennard-Jones sizes and depths, and so on).
- $k$: a label that numbers the pieces of reference data, from 1 to however many there are. It is not a spring constant here.
- $A_k^{ref}$: the reference value of datum $k$. For example the quantum-chemical energy of one conformation, or the measured density of one liquid.
- $A_k^{calc}(\mathbf p)$: the same quantity computed with the force field. The bracket $(\mathbf p)$ says that it changes when the parameters change.
- $A_k^{calc}(\mathbf p) - A_k^{ref}$: the **residual** (or deviation) of datum $k$: how far the model is from the reference.
- The square: it makes every term positive, so that an error that is too high cannot cancel one that is too low, and it counts a large deviation much more than a small one.
- $w_k$: the **weight** of datum $k$, a positive number that says how much this datum counts. It also removes the units, so that terms of different kinds can be added.
- $\sum_k$: add up over all the reference data.
- $\chi^2$: the total misfit, one number. It is zero only if the model reproduces every datum exactly.
</div>

**Read it like this.** For each piece of reference data, compute the same quantity with the force field, take the difference, square it, multiply by a weight and add everything up. The result says in one number how badly the present parameters do. "Minimising" means searching for the parameter values that make this number as small as possible. Picture a landscape like the energy landscape of Module 2, with the parameters as the coordinates and $\chi^2$ as the height: fitting is walking downhill to the lowest point. This way of fitting is called **least squares**, and the reference data are also called **target data**.

Take one term as an example: datum $k$ is the density of a liquid, the reference is 1000 kg/m$^3$ and the model gives 980 kg/m$^3$. The residual is $-20$ kg/m$^3$ and its square is 400 (kg/m$^3$)$^2$. Take the weight $w_k = 1/(10\ \text{kg/m}^3)^2$, which says "a deviation of 10 kg/m$^3$ counts as one unit". The term then contributes $400/100 = 4$ to $\chi^2$. The weight has removed the unit, so this 4 can be added to a term that comes from an energy in kJ/mol with its own weight.

<div class="box maths" markdown="1">
**Maths you need here: least squares, residuals and overfitting.** Take a model with one parameter. A bond is stretched by three small amounts, $d_1 = 0.005$, $d_2 = 0.010$ and $d_3 = 0.015$ nm, and a quantum-chemical calculation gives the energies $E_1 = 3.2$, $E_2 = 13.1$ and $E_3 = 29.0$ kJ/mol. (The numbers are invented for the illustration.) The model is the harmonic bond of Module 5, $E = \tfrac12 k_b d^2$, with one unknown, the force constant $k_b$.

With all weights equal to 1, the misfit is $\chi^2(k_b) = \sum_k \left(\tfrac12 k_b d_k^2 - E_k\right)^2$, a sum of three terms. At its minimum the slope of $\chi^2$ with respect to $k_b$ is zero. The chain rule gives the slope as $\sum_k 2\left(\tfrac12 k_b d_k^2 - E_k\right)\tfrac12 d_k^2$. Set it to zero and solve for $k_b$:

$$
k_b = \frac{\sum_k \tfrac12 d_k^2\,E_k}{\sum_k \left(\tfrac12 d_k^2\right)^2} = \frac{3.96\times10^{-3}}{1.53\times10^{-8}} \approx 2.58\times10^{5}\ \text{kJ mol}^{-1}\,\text{nm}^{-2} .
$$

With this value the model gives 3.23, 12.92 and 29.08 kJ/mol. The **residuals** (model minus reference) are $+0.03$, $-0.18$ and $+0.08$ kJ/mol. They are not zero, because one parameter cannot pass exactly through three points. Least squares spreads the misfit over all of them.

The answer came in one step, without any search, because the model is **linear** in the parameter: $k_b$ only multiplies a known number. Whenever all parameters enter in this way, least squares leads to linear equations that a computer solves directly. Partial charges and torsion force constants, below, are of this kind.

**Overfitting.** If you add parameters, the smallest $\chi^2$ that the fit can reach never goes up and usually goes down, and with as many parameters as data points it can reach zero. That is not a success. The extra parameters have started to reproduce the noise and the peculiarities of these particular data, and the model then does worse on data it has not seen. The protection is to use many more data than parameters, and to test the result on data that were kept out of the fit (see "How force fields are validated" below). More in the [toolbox](maths.html#fitting).
</div>

Three choices decide what a fit produces: the form of the model (Module 5), the target data and the weights. The last two are not visible in the formula, and they are where the force-field families differ.

### What the model is fitted to

The reference data are of two kinds:

- **Quantum chemistry** on small model compounds: optimised geometries, vibrational frequencies, the electrostatic potential around the molecule, energy scans along torsions, interaction energies of dimers.
- **Experiment**, mostly on pure liquids and solutions: density, heat of vaporisation, hydration free energy, and for proteins NMR observables.

The two kinds complement each other. A quantum-chemical calculation can be done for any small molecule and any shape of it, and it gives many numbers per molecule. But it describes one or two molecules in empty space. Experiments on liquids give few numbers per substance, but they report on what a simulation is for: many molecules together at room temperature.

<div class="box physics" markdown="1">
**Physics you need here: what a quantum-chemical calculation gives.** A molecule consists of nuclei and electrons, and the electrons obey quantum mechanics (see the [primer](physics.html#quantum)). A quantum-chemical calculation, QM for short, takes the nuclei at fixed positions and solves, approximately, the equation that governs the electrons. It returns two things: the **energy** of the molecule in that geometry, and the **electron density**, which says how much electron charge sits at each point of space. Everything in the first item of the list above is derived from these two:

- *Optimised geometry.* Move the nuclei downhill in energy until the forces on them vanish. The result is the structure of lowest energy, with its bond lengths and angles.
- *Vibrational frequencies.* The curvature of the energy at that minimum (the Hessian of Module 2) gives the frequencies at which the molecule vibrates.
- *Electrostatic potential.* The nuclei and the electron density together are a distribution of charge, and the electric potential at any point around the molecule follows from it.
- *Energy scan along a torsion.* Rotate one bond in steps and record the energy at each step.
- *Interaction energy of a dimer.* A dimer is a pair of molecules. Compute the pair together and each molecule alone. The energy of the pair minus the two separate energies says how strongly the two attract.

Such a calculation uses no fitted parameters for the molecule at hand, which is why it can serve as a reference. Its price is computer time, which grows steeply with the number of electrons. For that reason the calculations are done on small **model compounds**, small molecules that each contain one chemical group of interest (a small amide can stand in for the peptide group of a protein), and often for a single molecule or a pair in empty space. "In the gas phase" is the usual name for that situation: one molecule with nothing around it.

**Level of theory.** The equation for the electrons cannot be solved exactly for anything larger than a few electrons, so every method makes an approximation in the way it treats the repulsion between electrons. The "level of theory" is the name of that approximation. The cheapest common one is Hartree-Fock, HF: each electron feels the average cloud of all the others and not their positions at each instant. More expensive methods, with names such as MP2 or coupled cluster, correct for the fact that electrons avoid each other. A "higher" level means a better approximation and a much longer calculation.

**Basis set.** The program builds the electron cloud from a fixed list of simple building-block functions centred on the atoms, and only adjusts how much of each is used. That list is the basis set. A larger list lets the cloud take more shapes, which brings the result closer to the best that the chosen method can give, at a higher cost. The names are labels of standard lists: 6-31G\* is a small to medium one, and the star says that extra functions were added on the non-hydrogen atoms so that the cloud around them can shift off-centre. A calculation is described as "method/basis set", for example HF/6-31G\*. In common use, "level of theory" often means the method and the basis set together, as in the sentence below that calls HF/6-31G\* a low level of theory.
</div>

The experimental data come mostly from liquids of small molecules, because their properties have been measured precisely and a box of a few hundred small molecules is cheap to simulate. Four kinds of data appear again and again.

**Density.** The mass per volume of the liquid. In a simulation at constant pressure the box shrinks or grows until the liquid has found its own density. It tests how closely the model molecules pack, which depends mostly on the sizes of the atoms.

**Heat of vaporisation.** The energy needed to move molecules from the liquid into the gas, per mole, at constant pressure. It measures how strongly the molecules in the liquid hold on to each other. A simulation of the liquid gives it through

$$
\Delta H_{vap} \approx -\,U_{liq} + RT .
$$

<div class="legend" markdown="1">
- $\Delta H_{vap}$: the heat (more exactly the enthalpy) of vaporisation, in kJ/mol. The $\Delta$ means "difference", here gas minus liquid. For water near room temperature it is about 44 kJ/mol.
- $U_{liq}$: the average potential energy of the interactions between molecules in the liquid, per mole of molecules. It is negative, because the molecules attract each other.
- $R$: the gas constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$. It is the Boltzmann constant $k_B$ of Module 3 for energies counted per mole.
- $T$: the temperature in kelvin. At 298 K, $RT = 2.48$ kJ/mol.
- $\approx$: the formula assumes that the vapour is an ideal gas (a gas whose molecules do not interact with each other), that the volume of the liquid is negligible next to that of the gas, and that a molecule has the same internal energy in both phases (exact for a rigid molecule).
</div>

Where it comes from: the heat of vaporisation is the difference in enthalpy $H = E + PV$ between gas and liquid, where $E$ is the total energy, $P$ the pressure and $V$ the volume (see the [primer](physics.html#thermodynamics)). The kinetic energy is the same in both phases at the same temperature and cancels. In the gas the molecules are far apart and their interaction energy is close to zero, in the liquid it is $U_{liq}$, so the energy difference is $0 - U_{liq}$. One mole of ideal gas has $PV = RT$, and the $PV$ of the liquid is more than a thousand times smaller (1.8 J/mol for water at 1 bar). For water the formula gives a target of $U_{liq} \approx -(44 - 2.5) = -41.5$ kJ/mol.

**Hydration free energy.** The change in free energy when one molecule is moved from the gas into water. A free energy is the quantity that decides which of two states is more populated at a given temperature, and it combines energy and entropy (Module 3 and the [primer](physics.html#thermodynamics)). A negative hydration free energy means that the molecule prefers water, and each 5.7 kJ/mol ($RT\ln10$ at 300 K) makes that preference ten times stronger. It tests the interaction of a molecule with water, which for polar groups is dominated by the charges. Module 13 shows how it is computed.

**NMR observables.** Quantities measured by nuclear magnetic resonance spectroscopy on a peptide or protein in solution. Several of them depend in a known way on a torsion angle or on a distance within the molecule. Each measured value is an average over all the conformations that the molecules visit, so these data test whether the force field populates the right conformations. The section on validation describes the individual observables.

The table collects which data mainly fix which parameters. The symbols are those of Module 5: $r_0$ and $\theta_0$ are the equilibrium bond length and angle, $k_b$ and $k_\theta$ the force constants, $\sigma$ and $\varepsilon$ the size and the well depth of the Lennard-Jones term. From Module 2, $\omega$ is the angular frequency of a vibration, $k$ the force constant of the spring and $\mu$ the reduced mass of the two atoms.

| Target data | Parameters they mainly fix | Why |
|---|---|---|
| Crystal structures, QM optimised geometries | $r_0$, $\theta_0$ | The lowest-energy structure shows where the minima of the bond and angle springs must be |
| Vibrational frequencies | $k_b$, $k_\theta$ | A stiffer spring vibrates faster: $\omega = \sqrt{k/\mu}$ (Module 2) |
| QM electrostatic potential, QM interaction energies with a water molecule | Partial charges | Neighbouring molecules feel the charge distribution through this potential |
| Liquid density | Lennard-Jones parameters, mostly the sizes | It depends on how tightly the molecules pack |
| Heat of vaporisation | Lennard-Jones parameters, mostly the depths, and charges | It depends on how strongly the molecules attract |
| Hydration free energy | Charges of polar groups | It measures how strongly the molecule interacts with water |
| QM energy scan along a torsion | Torsion force constants | It is the energy profile of rotating about one bond |
| NMR observables of peptides and proteins | Backbone and side-chain torsions | They depend on which conformations are populated in solution |

### The order of fitting

The terms are fitted roughly in the order below, because each depends on the ones before. The order is not strict. The cycle is repeated until the parameters stop changing, since a change of charges forces a refit of the torsions (OPLS-AA and CHARMM22 were built this way), and in the original AMBER work the torsions were tuned together with the non-bonded terms:

1. **Equilibrium bond lengths and angles** from crystal structures and QM geometries; **force constants** from vibrational frequencies.
2. **Partial charges** from the QM electrostatic potential or from interactions with water.
3. **Lennard-Jones parameters** from liquid densities and heats of vaporisation, since those depend on how tightly molecules pack and how strongly they attract.
4. **Torsions last**, as a correction: $U_{tors}(\phi) \approx E_{QM}(\phi) - E_{MM}^{\,no\ tors}(\phi)$. The torsion term is the difference between a QM energy scan and what all the other terms already give.

<div class="legend" markdown="1">
- $\phi$: the torsion angle about one bond (the dihedral angle of Module 5).
- $E_{QM}(\phi)$: the quantum-chemical energy of the molecule when that torsion is held at the value $\phi$.
- $E_{MM}^{\,no\ tors}(\phi)$: the energy of the same structures computed with the force field, using every term except the torsion term for this bond. "MM" stands for molecular mechanics, another name for a force-field calculation. "no tors" is a label.
- $U_{tors}(\phi)$: the torsion term that is to be determined.
</div>

Why is there an order at all? Each kind of target data depends mostly on one kind of term and a little on all the others. So one starts with the terms that depend least on the rest and ends with the term that depends on everything.

*Step 1.* Bonds and angles are stiff springs. Their equilibrium values can be read from structures: crystal structures (the positions of the atoms in a crystal of the compound, measured by X-ray diffraction) and QM optimised geometries. Their force constants follow from vibrational frequencies, because the angular frequency of a spring is $\omega=\sqrt{k/\mu}$ (Module 2), where $\mu$ is the reduced mass of the two atoms and $\omega$ is $2\pi$ times the number of vibrations per unit of time. A measured or computed frequency therefore gives the force constant $k$. These terms hardly notice a change in the charges, so they can be fixed first.

*Step 2.* The charges are the subject of the section "Fitting charges" below.

*Step 3.* A liquid is held together by the attraction between its molecules and kept from collapsing by their repulsion. Its density and the energy needed to evaporate it therefore react to the Lennard-Jones size $\sigma$ and depth $\varepsilon$ of each atom type. The charges must be known first, because they hold the liquid together as well.

*Step 4.* The torsion term comes last because it is defined as what is left over. The next section explains this, and it also explains the sentence about the cycle: when the charges change, the "everything else" changes, so the leftover has to be fitted again.

### Torsion scans, and what "residual" means

The torsion term is fitted to a **torsion scan**, also called a dihedral scan or an energy scan along a torsion. The recipe:

1. Take a small molecule that contains the bond of interest, for example butane for the rotation about a C-C bond.
2. Hold the torsion angle $\phi$ about that bond at a series of values, for example every 15° from $-180$° to 165°, which makes 24 structures.
3. For each structure compute the QM energy, usually after letting all the other coordinates relax. This gives the curve $E_{QM}(\phi)$, the rotational profile of the real molecule.
4. Compute the energy of the same 24 structures with the force field, with the torsion term for this bond switched off. This gives $E_{MM}^{\,no\ tors}(\phi)$.
5. Subtract the second curve from the first. The difference is what the torsion term has to supply.

The difference is then fitted with the cosine series that Module 5 introduced for torsions:

$$
U_{tors}(\phi) = \sum_{n} k_{\phi,n}\,\big[1+\cos(n\phi-\delta_n)\big] .
$$

<div class="legend" markdown="1">
- $n$: the multiplicity, a whole number. The term with multiplicity $n$ repeats $n$ times in a full turn. Commonly $n = 1, 2, 3$.
- $k_{\phi,n}$: the force constant of term $n$, in kJ/mol. It is half the barrier height of that term. These are the parameters to be fitted.
- $\delta_n$: the phase of term $n$, 0 or 180° in most force fields. It decides whether the term has its maximum or its minimum at $\phi=0$.
- $\sum_n$: add the terms for the few multiplicities that are used.
- $\phi$, $U_{tors}$: as in the list above.
</div>

The fit minimises

$$
\chi^2_{tors} = \sum_{m}\Big[E_{QM}(\phi_m) - E_{MM}^{\,no\ tors}(\phi_m) - c - \sum_n k_{\phi,n}\big[1+\cos(n\phi_m-\delta_n)\big]\Big]^2 .
$$

<div class="legend" markdown="1">
- $\chi^2_{tors}$: the misfit of the torsion fit, the quantity that is minimised.
- $m$: a label that numbers the structures of the scan. $\phi_m$ is the torsion angle of structure $m$.
- $\sum_m$: add up over all structures of the scan.
- $c$: a constant, fitted together with the force constants. QM and force-field energies are counted from different zero points, and only differences of energy between conformations matter, so one free constant takes care of the offset.
- Other symbols: as in the two lists above.
</div>

This is the general $\chi^2$ of the start of the section. The reference data are the differences $E_{QM}-E_{MM}^{\,no\ tors}$ at the scan points, the model is the cosine series plus a constant, and all weights are 1. With the phases $\delta_n$ chosen beforehand, the unknowns $k_{\phi,n}$ and $c$ enter linearly, so the fit is solved in one step, like the spring in the maths box.

Now look at what the torsion term contains. Rotating about a bond changes more than a "rotation energy" of that bond. The two end atoms of the torsion move closer together and further apart, so their Coulomb and Lennard-Jones energies change, and the angles are strained a little. The force field already has terms for all of that, each with its own error.

The torsion term is fitted to what remains, the **residual**. It therefore holds two things at once: the part of the rotational energy that no other term describes, and the sum of the errors that all the other terms make along this rotation, with the opposite sign.

The end atoms of a torsion are three bonds apart and are called a 1-4 pair. Force fields reduce the non-bonded interaction of 1-4 pairs by a fixed factor, the 1-4 scaling, which differs between families: Module 5 lists 1/1.2 for the Coulomb part in AMBER, 0.5 in OPLS-AA and 1 in CHARMM.

Because torsions are a residual, they are specific to the charges, 1-4 scaling and Lennard-Jones set they were fitted with. Parameters are not transferable between families.

### Transferability, and why families cannot be mixed

**Transferable** means: fitted in one place and valid in another. The word is used at two levels.

*Between molecules, inside one force field.* Nobody fits parameters for each protein. Parameters are fitted on small model compounds and then reused for every atom of the same atom type in any molecule. (An atom type is a label for an element in a particular chemical environment.) This reuse is the working assumption of every force field. It holds as long as the surroundings of the atom in the large molecule resemble those in the model compound.

*Between families.* Here it fails, for the reason given in the two sentences above. An illustration with invented numbers: suppose QM says that conformation B of a molecule lies 10 kJ/mol above conformation A. In family 1, the non-bonded and angle terms already give 6 kJ/mol, so the fitted torsion term supplies the remaining 4. In family 2, with other charges and another 1-4 scaling, the same terms give 9 kJ/mol, and its torsion term supplies 1. Both families reproduce the 10 kJ/mol.

Now combine the torsion term of family 1 with the charges of family 2. The result is $4 + 9 = 13$ kJ/mol, an error of 3 kJ/mol. That is more than the thermal energy $k_BT = 2.494$ kJ/mol at 300 K, and through the Boltzmann factor of Module 3 it changes the population of B relative to A by a factor $e^{3/2.494}\approx 3.3$.

The same holds, to a smaller degree, for the other parameters. Lennard-Jones parameters were fitted with certain charges, and charges with a certain water model in mind. Module 5 called such parameters *effective*: they work as a set, in the conditions they were fitted for. An error in one term has been absorbed by another, and if you exchange one piece the compensation is gone.

The demo below gives you a made-up scan of the kind described above. The dots are a "QM" energy minus the force-field energy without the torsion term, every 15°. Fit them by hand with three cosine terms, then let the least-squares button do it.

<div class="widget" data-widget="torsionfit"></div>

### Fitting charges: ESP and RESP

Partial charges decide how strongly molecules attract, repel and orient each other, so they are fitted with special care. Module 5 introduced them: each atom carries a fixed charge at its nucleus, a fraction of the elementary charge $e$, which stands for the uneven distribution of the electrons in the molecule.

A partial charge cannot be observed. The electrons of a molecule form one continuous cloud, and there is no unique way to cut the cloud into pieces that belong to atoms. What a neighbouring molecule does feel is the electric potential that the nuclei and the cloud create in the space around the molecule. The method of this section therefore asks: which point charges, placed on the atoms, create the same potential outside the molecule as the real distribution of charge? "ESP" stands for electrostatic potential.

<div class="box physics" markdown="1">
**Physics you need here: the electrostatic potential.** The electrostatic potential $V$ at a point in space is the energy that a small test charge would have at that point, divided by the size of the test charge. It is an energy per unit charge, in MD units kJ mol$^{-1}$ $e^{-1}$. Multiply the potential at a point by a charge placed there and you have the Coulomb energy of that charge.

A single point charge $q$ creates, at a distance $r$, the potential $V = q/(4\pi\varepsilon_0 r)$. Here $1/(4\pi\varepsilon_0) = 138.935$ kJ mol$^{-1}$ nm $e^{-2}$ is the constant of Coulomb's law. Example: a charge of $+1\,e$ creates, at 0.3 nm, a potential of $138.935/0.3 = 463$ kJ mol$^{-1}$ $e^{-1}$. A second charge of $-0.5\,e$ placed there has the energy $-0.5\times463 = -232$ kJ/mol.

Potentials add: the potential of several charges is the sum of their separate potentials. Around a molecule the potential is positive near the hydrogens of an O-H or N-H group, where the electron cloud is thin, and negative near the lone pairs of an oxygen (pairs of outer electrons that take no part in a bond). A map of this potential is the electrostatic face that the molecule shows to its neighbours. More in the [primer](physics.html#electrostatics).
</div>

Compute the QM electrostatic potential $V^{QM}(\mathbf r_k)$ on a few thousand points $k$ around the molecule, outside the van der Waals surface. Choose atom-centred charges whose Coulomb potential reproduces it, with the total charge fixed by a Lagrange multiplier $\lambda$:

$$
\chi^2_{ESP} = \sum_k\Big[V^{QM}(\mathbf r_k) - \sum_i\frac{q_i}{4\pi\varepsilon_0|\mathbf r_k-\mathbf r_i|}\Big]^2 + \lambda\Big(\sum_iq_i-Q_{tot}\Big).
$$

<div class="legend" markdown="1">
- $\chi^2_{ESP}$: the function whose derivatives are set to zero: the misfit to the potential, which is to be made as small as possible, plus a term that enforces the total charge.
- $k$: a label that numbers the points around the molecule. $\sum_k$ adds up over all of them. Together these points are called the grid.
- $\mathbf r_k$: the position of point $k$.
- $V^{QM}(\mathbf r_k)$: the quantum-chemical electrostatic potential at that point. These are the reference data.
- $i$: a label that numbers the atoms of the molecule. $\sum_i$ adds up over all of them.
- $q_i$: the partial charge on atom $i$, in units of $e$. The charges are the unknowns.
- $\mathbf r_i$: the position of the nucleus of atom $i$. "Atom-centred" means that the charge sits exactly there.
- $|\mathbf r_k-\mathbf r_i|$: the distance between atom $i$ and point $k$.
- $4\pi\varepsilon_0$: the constant of Coulomb's law, with $1/(4\pi\varepsilon_0) = 138.935$ kJ mol$^{-1}$ nm $e^{-2}$.
- $\sum_i q_i/(4\pi\varepsilon_0|\mathbf r_k-\mathbf r_i|)$: the potential that the point charges create at point $k$. This is the model value.
- $Q_{tot}$: the total charge of the molecule, a whole number of elementary charges: 0 for a neutral molecule, $-1$ for an acetate ion.
- $\lambda$: a Lagrange multiplier, an extra unknown whose only task is to force the charges to add up to $Q_{tot}$ (see the box below).
</div>

**Read it like this.** The first term is the general $\chi^2$ of the start of the module: the QM potential at each point is the reference, the potential of the point charges is the model, and all weights are 1. The second term is not a misfit. It is a device that forces the sum of the charges to equal the total charge of the molecule.

Two phrases of the recipe need a comment. The **van der Waals surface** is the surface of the molecule when each atom is drawn as a sphere with its van der Waals radius, roughly the closest that another atom can approach. Points inside it are left out, because no neighbouring atom can get there, and because close to the nuclei the real potential has a shape that a few point charges cannot imitate. The total charge is fixed because it is known exactly. A fit that returned a total of 0.03 for a neutral residue would give every copy of that residue a small charge that does not exist.

<div class="box maths" markdown="1">
**Maths you need here: the Lagrange multiplier.** The task is to find the minimum of a function when the variables must also satisfy a condition. The recipe: write the condition as "something $= 0$", multiply it by a new unknown $\lambda$ and add it to the function. Then set the derivatives with respect to all variables to zero, and solve these equations together with the condition.

Example: find the smallest value of $x^2+y^2$ when $x+y=1$ is required. Form $x^2+y^2+\lambda(x+y-1)$. The derivative with respect to $x$ gives $2x+\lambda=0$, and the one with respect to $y$ gives $2y+\lambda=0$, so $x=y=-\lambda/2$. The condition $x+y=1$ then gives $\lambda=-1$ and $x=y=\tfrac12$. Without the condition the minimum would be at $x=y=0$, which violates it.

The multiplier is a helper. Its value comes out along the way and is then not used. More in the [toolbox](maths.html#lagrange-multipliers).
</div>

Setting $\partial\chi^2/\partial q_j=0$ gives a linear system, solved in one step. Here are the steps. To shorten the writing, give names to two things that do not depend on the charges:

$$
V_k \equiv V^{QM}(\mathbf r_k), \qquad A_{ki} \equiv \frac{1}{4\pi\varepsilon_0|\mathbf r_k-\mathbf r_i|} .
$$

<div class="legend" markdown="1">
- $V_k$: the QM potential at point $k$, a known number.
- $A_{ki}$: the potential that a charge of $1\,e$ on atom $i$ would create at point $k$. It is a known number, fixed by the geometry. It has two labels and is not the $A_k$ of the first formula of the module.
- $\equiv$: "is defined as".
- Other symbols: as in the list above.
</div>

With these names, the potential of the point charges at point $k$ is $\sum_i A_{ki}q_i$. Now take the partial derivative of $\chi^2_{ESP}$ with respect to the charge $q_j$ of one atom, holding the other charges fixed. By the [chain rule](maths.html#chain-rule), each squared bracket gives two times the bracket times the derivative of the bracket, and the derivative of the bracket with respect to $q_j$ is $-A_{kj}$. The second term of $\chi^2_{ESP}$ gives $\lambda$. Set the result to zero:

$$
\frac{\partial\chi^2_{ESP}}{\partial q_j} = -2\sum_k A_{kj}\Big[V_k-\sum_i A_{ki}q_i\Big] + \lambda = 0 .
$$

<div class="legend" markdown="1">
- $j$: the label of the atom whose charge is varied. There is one such equation for each atom.
- $\partial\chi^2_{ESP}/\partial q_j$: the slope of $\chi^2_{ESP}$ when only the charge of atom $j$ changes. At the minimum it is zero for every atom.
- Other symbols: as in the lists above.
</div>

Divide by 2, multiply out the bracket and move the term without charges to the right-hand side:

$$
\sum_i\Big(\sum_k A_{kj}A_{ki}\Big)\,q_i + \frac{\lambda}{2} = \sum_k A_{kj}V_k , \qquad j = 1,\dots,N .
$$

<div class="legend" markdown="1">
- $N$: the number of atoms in the molecule.
- $\sum_k A_{kj}A_{ki}$: a known number for each pair of atoms $j$ and $i$, computed from the geometry.
- $\sum_k A_{kj}V_k$: a known number for each atom $j$, computed from the geometry and the QM potential.
- Other symbols: as in the lists above.
</div>

Together with the condition $\sum_i q_i = Q_{tot}$ these are $N+1$ equations for $N+1$ unknowns, the $N$ charges and $\lambda$. Every unknown appears only to the first power, multiplied by a known number. Such a set of equations is called a **linear system**, and a computer solves it exactly in one step (it is a [matrix](maths.html#matrices) equation). No search and no starting guess are needed. The reason is the same as for the spring in the first maths box: the model potential is linear in the charges.

The problem is that charges on buried atoms (a carbon surrounded by hydrogens) are poorly determined: the potential outside barely depends on them, so they come out large and unstable from one molecule to the next.

To see why, take the carbon of a methyl group, hidden behind its three hydrogens. Every point of the grid is far from the carbon and close to at least one hydrogen. Add some charge to the carbon and remove the same amount from the hydrogens around it: seen from outside, the two changes nearly cancel, and the potential on the grid hardly moves. Many different sets of charges therefore fit the potential almost equally well.

Least squares still returns the single best set, but tiny details of the data decide which one that is. The buried charge can then come out at $-0.6\,e$ in one molecule and at $+0.2\,e$ in a closely related one (invented numbers), although nothing physical differs that much. This is the overfitting of the first maths box in another form: the data do not contain enough information to fix that parameter.

The second problem needs two ideas from the physics of charges.

<div class="box physics" markdown="1">
**Physics you need here: dipole moment, polarisation and polarisability.** Two opposite charges $+q$ and $-q$ held a distance $d$ apart form a **dipole**. Its strength is the **dipole moment** $\mu = q\,d$, and it points from the negative to the positive charge. A neutral molecule whose electrons are unevenly distributed has a dipole moment. The usual unit is the debye, D, with 1 D $= 0.0208\,e$ nm. An isolated water molecule has 1.85 D (Module 5).

An electric field pulls the electrons of a molecule one way and the nuclei the other way. The electron cloud shifts a little, and the molecule acquires an extra dipole, the **induced dipole**. This response is called **electronic polarisation**. For fields of ordinary strength the induced dipole is proportional to the field, $\Delta\mu = \alpha E$, and the constant $\alpha$ is the **polarisability** of the molecule: it says how easily the cloud is deformed.

In a liquid every molecule sits in the field of its neighbours and is polarised by them. This is why a water molecule in liquid water has a larger dipole than one in the gas phase. A force field with fixed charges has no way to shift charge in response to a field. More in the [primer](physics.html#dipoles).
</div>

A second, separate problem is that even well-determined charges depend on the conformation used for the fit, because fixed charges cannot follow electronic polarisation; AMBER ff94 fitted charges to several conformations at once to average this.

In other words: when a molecule changes its shape, its groups polarise each other differently, and the real distribution of charge changes. One set of fixed charges cannot be right for all shapes. Fitting to several conformations at once means that the sum over points in $\chi^2_{ESP}$ runs over the grids of all the conformations, with one common set of charges. The result is a compromise between the shapes: it is exact for none of them.

**RESP** (restrained ESP; [Bayly et al. 1993](cite:bayly1993)) adds a hyperbolic penalty that pulls poorly determined charges towards zero:

$$
\chi^2_{RESP} = \chi^2_{ESP} + a\sum_{i\,\in\,\text{heavy atoms}}\left(\sqrt{q_i^2+b^2}-b\right).
$$

<div class="legend" markdown="1">
- $\chi^2_{RESP}$: the function that RESP minimises.
- $\chi^2_{ESP}$: the function of the ESP fit above, with its total-charge term.
- $i\in\text{heavy atoms}$: the sum runs over the non-hydrogen atoms only.
- $q_i$: the charge on atom $i$.
- $a$: the strength of the penalty. A larger $a$ pulls the charges harder towards zero.
- $b$: a constant with the unit of charge. It sets the width of the rounded bottom of the penalty: for charges much smaller than $b$ the penalty is a parabola.
- $\sqrt{q_i^2+b^2}-b$: the penalty for one atom. It is zero for $q_i=0$ and grows as the charge moves away from zero in either direction.
</div>

**Read it like this.** A **restraint**, or penalty, is an extra term that makes some solutions more expensive without forbidding them. The fit now has to balance two wishes: reproduce the potential, and keep the charges on heavy atoms small. For a well-determined charge, any change spoils the fit to the potential quickly, so the penalty moves it very little. For a poorly determined charge the potential hardly objects, the penalty wins, and the charge is pulled towards zero. Among the many sets of charges that fit almost equally well, the penalty selects one with small charges on the buried atoms.

The shape of the penalty explains the word "hyperbolic" (the curve $\sqrt{q^2+b^2}$ is a hyperbola). Two limits show the shape:

- For a small charge, $|q|\ll b$: write $\sqrt{q^2+b^2} = b\sqrt{1+q^2/b^2}\approx b\,(1+q^2/2b^2)$, using $\sqrt{1+x}\approx1+x/2$ for small $x$ (a [Taylor expansion](maths.html#taylor)). The penalty is then $a\,q^2/2b$: a parabola, like a spring that pulls the charge to zero.
- For a large charge, $|q|\gg b$: $\sqrt{q^2+b^2}\approx|q|$, and the penalty is $a\,(|q|-b)$: a straight line.

The slope of the penalty, $a\,q/\sqrt{q^2+b^2}$, is the "force" with which a charge is pulled towards zero. It grows with the charge only up to about $|q| = b$ and then levels off at $a$. A penalty proportional to $q^2$ would pull harder and harder on large charges, and it would spoil charges that are large for a good reason, such as the charge of a carbonyl oxygen. The hyperbola does not do that. As an illustration, take $b = 0.1\,e$: the penalty divided by $a$ is 0.0005 for $q = 0.01\,e$, 0.041 for $q=0.1\,e$ and 0.41 for $q = 0.5\,e$, and the slope divided by $a$ is 0.10, 0.71 and 0.98.

One consequence: the equations are no longer linear, because the slope of the penalty contains the charge under a square root. The charges can no longer be found in one step. They are found by iteration: start from a guess, improve it, and repeat until the charges stop changing.

The penalty acts on the non-hydrogen atoms only. Hydrogens sit at the surface of the molecule, where the potential determines their charges well.

AMBER deliberately uses a low level of theory, HF/6-31G\*, for this step. It overestimates gas-phase dipole moments, typically by 10 to 20 % (Cornell et al. compare this with the roughly 20 % by which the TIP3P and SPC models enhance the dipole of water), which roughly mimics the polarisation a molecule experiences in water. This is how a fixed-charge model includes average polarisation. The over-polarisation is a rough device and varies between chemical groups, which is why AMBER ff15ipq instead uses charges halfway between gas-phase and aqueous values ([Nerenberg and Head-Gordon 2018](cite:nerenberg2018)).

This paragraph describes the deliberate use of an error. The QM calculation is done on one molecule in empty space, and the simulation will put that molecule in water, where it is polarised and its real dipole is larger than in the gas. Fixed charges cannot grow by themselves, so the enlarged, liquid-like dipole has to be built into the charges from the start. The Hartree-Fock method with this small basis set makes molecules too polar by about the right amount, so its gas-phase potential is used as a stand-in for the potential of the polarised molecule in water. A more accurate method would give the smaller gas-phase dipole, which is right for the gas and too small for the liquid.

Two definitions for the last sentence of that paragraph: "aqueous" means "in water", and the gas-phase and aqueous values of a charge are the values that fit the potential of the isolated molecule and of the molecule polarised by surrounding water.

The other families use different philosophies for the same goal. CHARMM adjusts charges to reproduce QM interaction energies and geometries of the molecule with individual water molecules. OPLS fits charges and Lennard-Jones parameters together to liquid properties. GROMOS (sets 53A5 and 53A6) fits first to pure-liquid densities and heats of vaporisation and to solvation free enthalpies in cyclohexane, and then re-adjusts the charges of polar groups to hydration free enthalpies, so that partitioning between water and non-polar media comes out right ([Oostenbrink et al. 2004](cite:oostenbrink2004)).

The goal they share is a set of charges that is right for the liquid, with the average polarisation included. The routes differ in the reference data:

- *Interaction with individual water molecules* (CHARMM). The reference is a QM calculation of the model compound together with a single water molecule: how strongly do the two attract, and at what distance and orientation do they sit? The charges are adjusted until the force field gives the same.
- *Liquid properties* (OPLS). Charges and Lennard-Jones parameters are varied together until simulations of the liquid reproduce measured properties such as the density and the heat of vaporisation.
- *Free energies of transfer* (GROMOS). "Free enthalpy" is another name for the Gibbs free energy, the free energy at constant pressure. The solvation free enthalpy in cyclohexane is the free energy of moving a molecule from the gas into liquid cyclohexane, a non-polar solvent. The hydration free enthalpy is the same for water. If both are right, their difference is right, and that difference decides how a molecule **partitions**, that is, how it divides itself between water and a non-polar environment such as the interior of a protein or of a membrane.

## The protein force-field families

<div data-videos="kglSEWaMGyU OrfOZ1wmElo Ck7EMuIStpM"></div>

A force-field **family** is a line of parameter sets developed over decades, each new member a revision of an older one. The current members of a family usually share the details of the energy function (for example the 1-4 scaling) and a way of obtaining charges. The four families in the table all use the functional form of Module 5, with small variations. They differ in the choices described in the previous section, and those choices are what the table compares.

| Family | Typical current choice for proteins | Atom resolution | Fitting philosophy | Native water |
|---|---|---|---|---|
| AMBER | ff14SB, ff19SB | All-atom | RESP charges from QM; torsions fitted to QM energy scans, with the ff14SB backbone adjusted empirically against NMR data | TIP3P (ff14SB); OPC is recommended with ff19SB |
| CHARMM | CHARMM36m | All-atom | Charges from interactions with individual water molecules; CMAP backbone correction and side-chain torsions re-fitted to QM and NMR data | CHARMM-modified TIP3P |
| OPLS | OPLS-AA/M (open), OPLS4 (commercial) | All-atom | Charges and Lennard-Jones parameters fitted to liquid properties (heats of vaporisation, densities); torsions fitted to QM energy scans | TIP3P, TIP4P |
| GROMOS | 53A6 (2004), 54A7 | United-atom (non-polar H merged into C) | Pure-liquid density and heat of vaporisation, then charges re-fitted to hydration and solvation free energies | SPC |

How to read the columns:

- **Atom resolution.** In an *all-atom* force field every atom, including every hydrogen, is a particle. In a *united-atom* force field the non-polar hydrogens are merged into the carbon they are bonded to: a CH$_3$ group is one particle, with the mass of the whole group and Lennard-Jones parameters that describe the group. Hydrogens on nitrogen and oxygen are kept, because they form hydrogen bonds. Fewer particles make the simulation cheaper.
- **Fitting philosophy.** Which target data fix the charges, the Lennard-Jones parameters and the torsions, in the sense of the previous section. "Empirically" means "on the basis of experiment": the backbone parameters were adjusted so that simulations agreed better with measured NMR quantities.
- **CMAP.** A reminder from Module 5: a correction $U_{CMAP}(\phi,\psi)$ that depends on the two backbone torsion angles $\phi$ and $\psi$ of a residue together, stored as a table on a grid. It captures the coupling between the two angles, which separate one-dimensional torsion terms cannot.
- **Native water.** The water model that the force field is meant to be used with. Protein and water parameters have to be in balance, so the water model is part of the choice of force field and not a free option. The water models are the subject of the next section.
- **Open, commercial.** Whether the parameter files are freely available or come with a commercial program.

The lineage is worth knowing because papers cite specific versions. In AMBER: the united-atom force field of [Weiner et al. (1984)](cite:weiner1984), with a 10-12 hydrogen-bond term and 1-4 factors of 0.5; the all-atom force field of [Cornell et al. (1995)](cite:cornell1995), usually called ff94, with RESP charges and a 1-4 Coulomb factor of 1/1.2; ff99, ff99SB (backbone fix, 2006), ff99SB-ILDN (side chains of Ile, Leu, Asp, Asn; [Lindorff-Larsen et al. 2010](cite:lindorfflarsen2010)), ff14SB ([Maier et al. 2015](cite:maier2015)), ff19SB (an amino-acid-specific CMAP backbone fitted to QM energy surfaces computed in implicit solvent, and recommended with OPC water although it was not fitted with it; [Tian et al. 2020](cite:tian2020)). In CHARMM: CHARMM22 ([MacKerell et al. 1998](cite:mackerell1998)), CHARMM22/CMAP (2004), CHARMM36 ([Best et al. 2012](cite:best2012)), CHARMM36m ([Huang et al. 2017](cite:huang2017)).

Words in this paragraph that may be new:

- A **10-12 hydrogen-bond term** is a separate pair term for hydrogen bonds, with a repulsion proportional to $r^{-12}$ and an attraction proportional to $r^{-10}$, where $r$ is the distance between the hydrogen and the acceptor atom of the hydrogen bond. Modern force fields have no such term (Module 5): a hydrogen bond results from the Coulomb and Lennard-Jones terms.
- **1-4 factors** are the scaling factors for the non-bonded interactions of atoms three bonds apart, as explained above.
- A **backbone fix** is a re-fit of the torsion terms of the backbone angles $\phi$ and $\psi$. A re-fit of side chains is a re-fit of the torsion terms of the side-chain angles $\chi$.
- A **QM energy surface** is the energy computed on a grid of values of two angles at once, here $\phi$ and $\psi$. It is the two-dimensional version of a torsion scan: a surface over a map, where a scan gives a curve along a line.
- **Implicit solvent** means that the water is represented as a continuous medium that weakens electrostatic interactions, without individual molecules (Module 15).
- **Amino-acid-specific** means that the correction map depends on the type of amino acid.

The pattern in both lines is similar: most new versions re-fit part of the parameters of the previous one. Module 5 made the point that almost every revision of a protein force field in the last 25 years is mainly a re-fit of backbone or side-chain torsions. Torsions are fitted last, and they are also corrected most often.

For anything that is not a standard residue you need a **general force field** designed to be compatible with the protein one: GAFF/GAFF2 with AMBER, CGenFF with CHARMM, and the Open Force Field series (Parsley, Sage), which assigns bonded and Lennard-Jones parameters by chemical substructure patterns (the charges come from the AM1-BCC model), is distributed in an open format, and is validated together with AMBER protein force fields.

A **standard residue** is a building block for which the family provides ready parameters, such as the twenty amino acids. A drug-like ligand, a cofactor or a chemically modified amino acid is not in that library. A general force field covers such molecules by rules: it recognises the chemical groups in the molecule you give it and assigns parameters to them from tables that were fitted on many small organic molecules. "Compatible" means that it was built with the same conventions as the protein force field of its family (the way charges are obtained, the 1-4 scaling, the balance of the Lennard-Jones terms), so that ligand and protein parameters can be used together.

Two phrases about the Open Force Field series. A classical force field first gives every atom an atom type and then looks up the parameters by combinations of types. "By chemical substructure patterns" means that the parameters are attached to descriptions of fragments of a molecule (a pattern says, for example, "a carbon double-bonded to an oxygen"), and every bond, angle or torsion that matches a pattern receives its parameters. A "charge model" is a recipe that assigns partial charges to any molecule.

<div class="box warn" markdown="1">
**Rules that save months.** (1) Use the protein force field with the water model and ion parameters it was validated with. (2) Use the cutoff scheme it was developed with (CHARMM36: force switch from 1.0 to 1.2 nm; the original CHARMM22 paper used atom-based shifting and switching functions, and stresses that the cutoff scheme is part of the model). (3) Never combine protein parameters from one family with ligand parameters from another. (4) Read the force field's own paper for the recommended combination; do not rely on a tutorial's defaults.
</div>

All four rules are one statement, "the parameters work as a set", applied to different parts of the set.

1. The interactions of the protein with water and with ions were balanced using one water model and one set of ion parameters. Another water model has other charges and another Lennard-Jones term, and the balance shifts. The section on disordered proteins shows how much this can matter.
2. A **cutoff scheme** is the rule for what happens to an interaction at large distance: beyond which distance it is no longer computed, and how it is brought to zero there. Shifting and switching functions are two ways of making an interaction go to zero smoothly at the cutoff instead of dropping abruptly. "Force switch from 1.0 to 1.2 nm" means that the force is left unchanged up to 1.0 nm and then taken smoothly to zero at 1.2 nm. Module 7 gives the details. The scheme changes how much attraction is counted in total, and with it densities and energies, so parameters fitted with one scheme reproduce their target data only with that scheme.
3. The torsions, charges and 1-4 scaling of two families do not fit together, as the example with the invented numbers showed.
4. A tutorial shows one working set of settings, often for another force field than yours. The paper of the force field states the combination that was tested.

## Water models

<div data-videos="6RzCFya08iE"></div>

Water is 80 to 90 % of the atoms in a simulation, and its model decides hydration, screening and diffusion.

Three words in that sentence. **Hydration** is the way water molecules arrange themselves around a solute and how strongly they bind to it. **Screening** is the weakening of the interaction between two charges by the water between them, whose dipoles turn so as to oppose the field of the charges. **Diffusion** is the random wandering of molecules through the liquid. The solvent sets its pace for everything that is dissolved in it.

A water model is a small object made of **sites**. A site is a point that carries a charge, or a Lennard-Jones centre, or both. The model is defined by the positions of the sites relative to each other (its geometry), by the charge on each site, and by the Lennard-Jones size $\sigma$ and depth $\varepsilon$.

*Rigid* means that the distances between the sites never change. There are no bond and angle springs. The shape is held by constraints (Module 9), which also removes the fast O-H vibration and allows a longer time step. *Fixed charges* means that the charges are the same in every environment, as in the rest of a fixed-charge force field.

Models are classed by their number of sites, also called points:

- **Three-site.** The sites are the three atoms. Each hydrogen carries a positive charge $q_H$, and the oxygen carries $-2q_H$, so that the molecule is neutral. The oxygen is also the Lennard-Jones centre (the only one, in the layout of the table below). Once the geometry is chosen, three numbers remain to be fitted: $q_H$, $\sigma$ and $\varepsilon$.
- **Four-site.** The negative charge is taken off the oxygen and placed on a fourth site, called M, on the bisector of the H-O-H angle (the line through the oxygen that divides the angle into two equal halves). The oxygen keeps the Lennard-Jones centre. M has no mass and no motion of its own: the program computes its position from the three atoms at every step and passes the force that acts on it on to them. The distance from O to M is one more adjustable number, which gives more freedom to shape the electric field around the molecule.
- **Five-site.** Two extra sites carry negative charge where the two lone pairs of the oxygen point. (A lone pair is a pair of outer electrons of the oxygen that is not used in a bond.)

Extra sites buy a better description of how the charge is spread over the molecule. They cost time: every extra charged site adds site-to-site distances that must be computed for each pair of nearby molecules.

<div class="box physics" markdown="1">
**Physics you need here: the properties used to judge a water model.** The table and the text below compare the models by a handful of measurable properties of liquid water.

- **Density**: the mass per volume. It tests how closely the model molecules pack. Real water is unusual in that its density is highest at 4 °C and falls on further cooling.
- **Heat of vaporisation**: the energy needed to take molecules out of the liquid (first section). It tests how strongly the molecules hold on to each other.
- **Self-diffusion coefficient** $D$: how fast a molecule wanders through the liquid. The mean squared distance that a molecule has travelled after a time $t$ is $6Dt$ (Module 11). It tests the dynamics. See the [primer](physics.html#diffusion).
- **Viscosity**: the resistance of the liquid to flow. A liquid in which the molecules diffuse too fast is also too thin, and everything dissolved in it moves too fast.
- **Dielectric constant**: the factor by which the liquid weakens the interaction between two charges that are far apart in it, compared with empty space. For water it is 78. It results from the screening described above. See the [primer](physics.html#electrostatics).
- **Structure**: the way the neighbours of a molecule are arranged around it, measured as the average density of other molecules at each distance. The nearest neighbours form the *first shell*.
- **Phase diagram**: the map that shows at which temperatures and pressures water is ice, liquid or vapour. The melting temperature is one point of it.

A model has only a few adjustable numbers, so it cannot be tuned to every property separately. Each model was tuned to a short list of properties, and the others are predictions, which may be good or poor. The columns "Strength" and "Known weakness" of the table record the outcome.
</div>

The common models are rigid, with fixed charges:

| Model | Sites | Idea | Strength | Known weakness |
|---|---|---|---|---|
| SPC, SPC/E | 3 | Charges on O and H, one Lennard-Jones site on O. SPC/E is SPC refitted with slightly larger charges ($q_H=+0.4238$ instead of $+0.41$), chosen after the polarisation self-energy is subtracted from the target energy. | SPC/E: good diffusion and structure | Dielectric constant somewhat low |
| TIP3P | 3 | Same three-site layout, but with the real water geometry (OH 0.09572 nm, HOH 104.52 degrees) instead of the tetrahedral SPC angle, and reparametrised to improve the energy and density of the liquid ([Jorgensen et al. 1983](cite:jorgensen1983)) | Default of AMBER and CHARMM; huge validation history | Diffuses about twice too fast; too little structure beyond the first shell |
| TIP4P-Ew, TIP4P/2005 | 4 | Negative charge moved off the oxygen to a massless site M on the bisector | TIP4P-Ew: TIP4P re-fitted for Ewald electrostatics. TIP4P/2005: excellent phase diagram, density and dynamics | Dielectric constant too low (about 60); TIP4P/2005 melts about 20 K too low |
| OPC | 4 | Three charges on four sites, placed without the usual bond-length and angle constraints so as to best reproduce six bulk properties ([Izadi et al. 2014](cite:izadi2014)) | Very good dielectric constant, density and diffusion together | 4-site cost |
| TIP4P-D, a99SB-disp water | 4 | Dispersion ($C_6$) increased | Reduces the over-compaction of disordered proteins | On its own it destabilises helices and some folded proteins, which is why a99SB-disp also re-fitted protein terms |
| TIP5P | 5 | Explicit lone-pair sites | Designed to give the density maximum at 4 °C (with Ewald electrostatics it shifts to about 285 K) | Cost; less used with proteins |

Terms in the table:

- The **tetrahedral angle**, 109.47°, is the angle between the lines from the centre of a regular tetrahedron to two of its corners.
- The **polarisation self-energy** is the energy it costs to enlarge the dipole of a molecule. The box 'The "missing term" of SPC/E' below explains it.
- **Ewald electrostatics** is the standard method for computing Coulomb interactions without cutting them off (Module 7). "Re-fitted for Ewald electrostatics" means that the parameters were tuned again in simulations that use this method. This is rule 2 of the warning box at work: a model tuned with one treatment of the long-range Coulomb interaction gives a slightly different liquid with another.
- **Dispersion** is the attraction between any two atoms that comes from the fluctuations of their electron clouds (Module 5). In the Lennard-Jones term it is the part $-C_6/r^6$, where $r$ is the distance between the two atoms and $C_6 = 4\varepsilon\sigma^6$. A larger $C_6$ on water makes water attract other atoms, protein atoms included, more strongly.
- **Bulk properties** are properties of the liquid far from any surface or solute.
- "Placed without the usual bond-length and angle constraints" (OPC): the positions of the charges were treated as adjustable numbers in the fit, instead of being put where the atoms of the real molecule are. The model is still rigid when it is simulated.
- "Destabilises helices and some folded proteins": a stronger attraction between water and protein favours states in which the protein is exposed to water, and with it a model can go too far in the other direction.

Rough numbers to anchor the table, at about 298 K: experimental water has a self-diffusion coefficient of $2.3\times10^{-5}$ cm$^2$/s and a dielectric constant of 78. TIP3P gives a diffusion coefficient above $5\times10^{-5}$ cm$^2$/s and a dielectric constant in the 90s. SPC/E and OPC are close to experiment for diffusion. The exact values reported depend on cutoffs and system size. The original TIP3P and SPC/E papers report no dielectric constants, and the 1983 TIP3P paper gives no diffusion coefficient for TIP3P, so take these numbers from later systematic comparisons of water models.

What these numbers mean in a simulation. In MD units, 1 cm$^2$/s is 100 nm$^2$/ps, so the experimental value is $D = 2.3\times10^{-3}$ nm$^2$/ps. With a mean squared displacement of $6Dt$, a water molecule travels in 1 ns ($t = 1000$ ps) a root-mean-square distance of $\sqrt{6\times2.3\times10^{-3}\times1000} = \sqrt{13.8}\approx3.7$ nm, about the diameter of a small protein. With a diffusion coefficient of $5\times10^{-5}$ cm$^2$/s the distance is $\sqrt{30}\approx5.5$ nm.

For the dielectric constant: two unit charges 1 nm apart interact with 138.935 kJ/mol in empty space. In a continuous medium with a dielectric constant of 78 this becomes $138.935/78 = 1.8$ kJ/mol, less than the thermal energy $k_BT$ (2.494 kJ/mol at 300 K). With a dielectric constant of 60 it is 2.3 kJ/mol, and with 90 it is 1.5 kJ/mol. A water model with too low a dielectric constant therefore makes charged groups interact too strongly at long range, and one with too high a value makes them interact too weakly.

Two consequences for protein simulations: with TIP3P, everything that depends on solvent viscosity (diffusion, some conformational rates) is too fast by a factor of 2 to 3; and the balance between protein-water and protein-protein interactions, which decides whether a disordered chain is expanded or collapsed, depends strongly on the water model.

The first consequence is about speeds. A protein, or a part of it, moves through water like an object through a viscous liquid: the thinner the liquid, the faster the motion. If you compare a simulated diffusion coefficient or rate with experiment, take the water model into account. The second consequence is about which states are populated, and it is the subject of the section on disordered proteins.

<div class="box key" markdown="1">
**The "missing term" of SPC/E.** A fixed-charge water has an enhanced dipole $\mu$ compared with the gas-phase value $\mu_0$. Creating that induced dipole costs energy, $E_{pol} = (\mu-\mu_0)^2/2\alpha$ with $\alpha$ the polarisability: 3.7 kJ/mol for the SPC dipole of 2.27 D and 5.2 kJ/mol for 2.35 D. [Berendsen, Grigera and Straatsma (1987)](cite:berendsen1987) pointed out that this cost must be added when comparing the model's heat of vaporisation with experiment. Refitting with it included gave SPC/E, with slightly larger charges and much better dynamics. The same reasoning matters whenever a fixed-charge model is fitted to a transfer between phases.
</div>

The box in steps.

*The enhanced dipole.* A fixed-charge water model is given the dipole of a molecule in the liquid, which is larger than that of an isolated molecule, for the reason given in the box on dipoles. In the box above, $\mu_0$ is the dipole of the isolated molecule (1.85 D, Module 5) and $\mu$ is the dipole of the model.

*The cost.* Enlarging the dipole of a real molecule is like stretching a spring. The field pulls the electron cloud out of its preferred shape, and the cloud resists. A spring with stiffness $k$ that is stretched by $x$ stores the energy $\tfrac12kx^2$ (Module 2). For a polarisable molecule the "stretch" is the extra dipole $\mu-\mu_0$ and the "stiffness" is $1/\alpha$: a molecule that is easy to polarise (large $\alpha$) is a soft spring. The stored energy is therefore

$$
E_{pol} = \frac{(\mu-\mu_0)^2}{2\alpha} .
$$

<div class="legend" markdown="1">
- $E_{pol}$: the polarisation self-energy, the energy it costs to deform the electron cloud of one molecule from its gas-phase shape to its shape in the liquid. It is positive.
- $\mu$: the dipole moment of the molecule in the liquid. In a fixed-charge model this is the fixed dipole of the model.
- $\mu_0$: the dipole moment of the isolated molecule.
- $\alpha$: the polarisability of the molecule, the induced dipole per unit of electric field.
- The square: the cost grows with the square of the change of the dipole, as the energy of a spring grows with the square of its stretch.
</div>

*Why it must be added.* When a real water molecule leaves the liquid, two things happen. It loses the attractive interactions with its neighbours, which costs energy. And its electron cloud relaxes back to the gas-phase shape, which returns the energy $E_{pol}$. The measured heat of vaporisation contains both.

A fixed-charge model molecule only does the first, because it keeps its enlarged dipole in the gas. The formula for the heat of vaporisation of the first section therefore needs one more term before a model is compared with experiment:

$$
\Delta H_{vap} \approx -\,U_{liq} - E_{pol} + RT .
$$

<div class="legend" markdown="1">
- $E_{pol}$: the polarisation self-energy per mole of molecules, a positive number.
- $\Delta H_{vap}$, $U_{liq}$, $R$, $T$: as in the formula for the heat of vaporisation in the first section.
</div>

**Read it like this.** For a given measured $\Delta H_{vap}$, the model liquid has to be bound more strongly than one would think without the correction, by the amount $E_{pol}$. With the round numbers of the first section the target for $U_{liq}$ was about $-41.5$ kJ/mol. With a correction of 5.2 kJ/mol it moves to about $-46.7$ kJ/mol (round numbers that show the size of the effect; the paper has the exact ones). Stronger binding needs larger charges, which is the step from SPC to SPC/E in the table.

*The last sentence of the box.* A hydration free energy is a transfer between phases too. The molecule goes from the gas, where its real dipole is the small one, into water, where it is the enlarged one. A fixed-charge model has the enlarged dipole on both sides, so the cost of polarisation is missing from the comparison and has to be accounted for.

<details markdown="1"><summary>Optional: checking the two numbers in the box</summary>
The formula needs consistent units. Convert the dipoles with 1 D $= 0.02082\,e$ nm. The polarisability of a molecule is usually tabulated as a volume, $\alpha' = \alpha/(4\pi\varepsilon_0)$. For the water molecule the measured value is about $1.45\times10^{-3}$ nm$^3$. Since $1/(4\pi\varepsilon_0) = 138.935$ kJ mol$^{-1}$ nm $e^{-2}$, this gives $\alpha = 1.45\times10^{-3}/138.935 = 1.04\times10^{-5}$ $e^2$ nm$^2$ mol kJ$^{-1}$.

For the SPC dipole, $\mu-\mu_0 = 2.27-1.85 = 0.42$ D $= 0.00874\,e$ nm, and $E_{pol} = 0.00874^2/(2\times1.04\times10^{-5}) = 3.7$ kJ/mol. For 2.35 D, $\mu-\mu_0 = 0.50$ D $= 0.01041\,e$ nm, and $E_{pol} = 0.01041^2/(2\times1.04\times10^{-5}) = 5.2$ kJ/mol. Both agree with the box.
</details>

### Ions

In a fixed-charge force field a simple ion such as Na$^+$ or Cl$^-$ is the simplest object there is: one point charge at the centre of one Lennard-Jones sphere. The charge is known, a whole number of elementary charges. Only two numbers can be fitted, the Lennard-Jones size $\sigma$ and depth $\varepsilon$ of the ion. They decide how close water molecules and other ions can come, and through that how strongly the ion binds water and how strongly it pairs with ions of the opposite charge.

Ion parameters are specific to the water model ([Joung and Cheatham 2008](cite:joung2008) for AMBER with TIP3P, SPC/E or TIP4P-Ew).

The reason is the one behind rule 1 of the warning box. How strongly an ion binds water depends on the size of the ion and on the charges and the geometry of the water model together. The same ion parameters give a different strength of hydration in each water model, so they have to be fitted for each water model separately.

With the older AMBER parameters (cations and chloride taken from two different sources), KCl crystallised in long simulations above about 0.2 M and NaCl above about 1 M, far below their real solubility, which is what prompted the re-fit.

M is the unit mol per litre, and the **solubility** of a salt is the highest concentration that stays dissolved. Whether a salt stays dissolved is decided by a competition: each ion can surround itself with water, or sit next to ions of the opposite charge. If a model makes the contact between ions too favourable compared with the contact between ion and water, the ions cluster and form crystals at concentrations at which the real salt dissolves completely. The remark in brackets is the mixing problem again, on the smallest possible scale: parameters from two sources had not been balanced against each other.

Fixed-charge models also tend to over-stabilise salt bridges and ion-phosphate contacts; pair-specific corrections (NBFIX, or scaled ion charges in the "ECC" approach) reduce this.

A **salt bridge** is a contact between a positively and a negatively charged group of a protein, for example a lysine or arginine side chain with an aspartate or glutamate side chain. An ion-phosphate contact is an ion that sits on a phosphate group, as found in DNA, RNA and lipids. "Over-stabilise" means that the model makes these contacts form more often and last longer than they really do. One reason lies in the missing polarisation: in reality the electron clouds of the surrounding molecules respond to two nearby full charges and weaken their attraction, and fixed charges cannot do that.

The two corrections work in different ways. NBFIX (Module 5) replaces the Lennard-Jones parameters that the combining rule gives for one specific pair of atom types by values fitted for that pair. In the ECC approach (the letters stand for electronic continuum correction) the charges of the ions are multiplied by a factor smaller than one, as a stand-in for the missing screening by the electrons. Their Coulomb attraction to opposite charges becomes weaker.

## The disordered-protein problem

<div data-videos="jFmGNUUVHzg _6iAcwmknek"></div>

This matters if you work with intrinsically disordered proteins or regions (IDPs, IDRs).

An **intrinsically disordered protein** has no stable folded structure, although it is a functional protein. It exists as an **ensemble**: a very large set of different conformations that interconvert all the time. An intrinsically disordered region is a stretch of this kind in a protein that also has folded parts.

For a folded protein, the question put to a force field is "does the known structure stay stable?". A disordered protein has no structure to hold, and the question becomes "does the simulation produce the right mixture of conformations?". That is a harder test, and the force fields of the time failed it.

Force fields up to about 2014 were developed mostly with folded proteins and short peptides in mind. When simulated with them, disordered proteins and unfolded states collapsed into compact globules, with radii of gyration well below SAXS and FRET measurements.

The **radius of gyration** $R_g$ is the usual measure of the size of a flexible chain: the root-mean-square distance of its atoms from its centre. A compact, roughly spherical conformation (a globule) has a small $R_g$, and an expanded chain a large one.

Two experiments report on the size. **SAXS** (small-angle X-ray scattering) measures how a solution of the protein scatters X-rays at small angles, and the average $R_g$ of the molecules follows from the scattering curve. **FRET** (Förster resonance energy transfer) uses two dyes attached to the chain. The efficiency with which energy passes from one dye to the other falls steeply with their distance, so it reports the average distance between two chosen positions.

The cause was a general imbalance: protein-protein interactions were too favourable compared with protein-water interactions.

**What "balance" means here.** Every group of a protein chain has a choice: it can be in contact with water or with another group of the same chain. The chain as a whole expands when contacts with water are preferred and collapses when contacts with itself are preferred. A single contact is worth little, often less than the thermal energy $k_BT$. But a chain makes hundreds of them, and small errors of the same sign add up. An illustration with invented numbers: if each of 100 contacts inside the chain is too favourable by only $0.1\,k_BT$ (0.25 kJ/mol), a collapsed conformation is favoured over an expanded one by $10\,k_BT$ too much, which is a factor $e^{10}\approx22{,}000$ in population.

**Why folded proteins did not reveal the problem.** The native structure of a folded protein is held by a tight and specific packing of its side chains. A simulation that starts from that structure stays in it when protein-protein contacts are somewhat too strong, and too-strong contacts can even help it pass the test "the native state is stable". The error shows only when the chain is free to choose between compact and expanded states, which is the situation of an unfolded or disordered chain.

Two explanations were proposed, and each led to a fix: protein-water Lennard-Jones attraction that is too weak ([Best, Zheng and Mittal 2014](cite:best2014)), and water models that underestimate dispersion ([Piana et al. 2015](cite:piana2015)). The fixes took several routes (the table lists four; a fifth, weakening the protein-protein attraction to match osmotic coefficients, is described by [Nerenberg and Head-Gordon 2018](cite:nerenberg2018)):

| Approach | Example | What was changed |
|---|---|---|
| Strengthen protein-water Lennard-Jones | ff03ws ([Best, Zheng and Mittal 2014](cite:best2014)) | The Lennard-Jones $\varepsilon$ between water oxygen and every protein atom scaled by 1.10, with TIP4P/2005 water |
| Change the water model | TIP4P-D ([Piana et al. 2015](cite:piana2015)) | Water dispersion coefficient $C_6$ increased: about 50 % above TIP3P, about 20 % above its parent model TIP4P/2005 |
| Re-fit protein and water together | a99SB-disp ([Robustelli, Piana and Shaw 2018](cite:robustelli2018)) | Backbone torsions, a backbone hydrogen-bond Lennard-Jones pair and a modified TIP4P-D water model, validated on both folded and disordered proteins |
| Re-fit the backbone only | CHARMM36m ([Huang et al. 2017](cite:huang2017)) | The CMAP backbone correction (to remove an excess of left-handed helix) and one pair-specific Lennard-Jones term (arginine with carboxylate). The water model stays CHARMM-modified TIP3P |

How to read the table, row by row:

- *Row 1.* Normally the Lennard-Jones depth $\varepsilon_{ij}$ of a pair of unlike atoms follows from a combining rule (Module 5). Here the rule is overridden for one kind of pair: for water oxygen with any protein atom, $\varepsilon_{ij}$ is multiplied by 1.10, which makes every protein-water well 10 % deeper. Protein-protein and water-water interactions stay as they were.
- *Row 2.* The dispersion coefficient $C_6 = 4\varepsilon\sigma^6$ of the water model itself is raised. Through the combining rule this strengthens the attraction between water and every other atom. Unlike row 1, it also changes the interaction of water with itself.
- *Row 3.* Protein and water parameters were adjusted together. "A backbone hydrogen-bond Lennard-Jones pair" is the Lennard-Jones term between the two backbone atom types that meet in a backbone hydrogen bond, given its own value. The phrase to notice is "validated on both folded and disordered proteins": the result was tested on both classes.
- *Row 4.* Only protein terms were changed. CMAP is the two-angle backbone correction recalled in the section on families. A left-handed helix is a backbone conformation that winds in the opposite sense to the usual α-helix. An "excess" of it means that simulations populated it too much. "Arginine with carboxylate" is the salt bridge between an arginine side chain and a negatively charged carboxylate group, and its pair-specific Lennard-Jones term is an NBFIX of the kind described under "Ions".
- *The fifth route.* An **osmotic coefficient** measures how the molecules of a solute affect each other in a concentrated solution. It is the measured osmotic pressure divided by the value expected if the solute molecules ignored each other. Solute molecules that attract each other too strongly in a model give a value that is too low, so matching it calibrates the attraction between solute molecules directly.

The usual choices for systems with both folded and disordered parts are a99SB-disp with its own water, CHARMM36m with its modified TIP3P, and ff19SB with OPC. They are not equally well tested for this. a99SB-disp was validated on both classes. CHARMM36m removes a backbone bias, but in its authors' own tests, and in the a99SB-disp comparison, it still makes longer disordered chains too compact. ff19SB was validated on peptides and folded proteins; its use for disordered proteins rests on the properties of OPC water and was left by its authors for future work. No force field is right for every system: check against whatever experimental data exist for yours (SAXS radius of gyration, NMR chemical shifts, PRE).

Three terms in the last sentence. The SAXS radius of gyration gives the overall size of the chain. A **chemical shift** is the position of the NMR signal of one nucleus. It depends on the local conformation of the backbone around that nucleus, so the shifts along a chain report how much helix or strand each residue populates on average.

**PRE** (paramagnetic relaxation enhancement) uses a small paramagnetic label (a chemical group with an unpaired electron) attached at one position of the chain. The label broadens the NMR signals of nuclei that come close to it, even if they do so for a small fraction of the time, so it detects transient contacts between distant parts of the chain. Together the three test the overall size, the local structure and the contacts.

The practical reading of this paragraph: "validated on" is the phrase to look for. A force field is known to work for a class of systems only when it was tested on that class, and the three choices differ in exactly this.

## Beyond fixed charges: polarizable force fields

<div data-videos="Y2ixvZBrM8Q I2zm3hAO-eI"></div>

Everything so far used fixed charges, with polarisation included only on average, by enlarging the charges. That average can be right for one environment at most. A molecule that moves from water into the interior of a membrane, or an ion that approaches a binding site, meets very different electric fields, and its real distribution of charge changes on the way. A **polarizable** force field lets the charge distribution respond. This section describes three ways of doing that and what they cost.

In a polarizable model the charge distribution responds to the local electric field $\mathbf E$.

The **electric field** $\mathbf E$ at a point is the force that a test charge would feel at that point, divided by the size of the test charge. It is a vector, in MD units kJ mol$^{-1}$ nm$^{-1}$ $e^{-1}$. A point charge $q$ creates at a distance $r$ a field of size $q/(4\pi\varepsilon_0r^2)$: for a charge of $1\,e$ at 0.3 nm this is $138.935/0.3^2 = 1544$ kJ mol$^{-1}$ nm$^{-1}$ $e^{-1}$. "Local" means the field at the position of the atom in question, created by all the other charges of the system.

- **Drude oscillator** (CHARMM Drude): each heavy atom carries an auxiliary charged particle attached by a spring with constant $k_D$. In a field the particle is displaced by $d = q_DE/k_D$, giving an induced dipole $\mu=q_Dd$ and a polarisability $\alpha = q_D^2/k_D$. It is run with an extended Lagrangian in which the Drude particles are kept cold, and needs a 1 fs step.
- **Induced point dipoles** (AMOEBA): each atom has a polarisability, and its induced dipole $\boldsymbol\mu_i = \alpha_i\,\mathbf E_i$ depends on the field from permanent charges *and* from all other induced dipoles, which requires a self-consistent solution every step (by iteration, by direct solution of the linear equations, or with an extended Lagrangian). AMOEBA also replaces point charges by permanent multipoles up to quadrupoles.
- **Fluctuating charges**: charges flow between atoms to equalise electronegativity.

### The Drude oscillator, step by step

Picture the atom as a core with a small charged particle tied to it by a spring. Without a field the particle sits on the core and has no effect. A field pushes the particle away from the core, the spring pulls it back, and the particle settles where the two forces are equal:

$$
k_D\,d = q_D\,E \quad\Longrightarrow\quad d = \frac{q_DE}{k_D} .
$$

<div class="legend" markdown="1">
- $d$: the displacement of the Drude particle from its core atom, in nm.
- $k_D$: the spring constant, in kJ mol$^{-1}$ nm$^{-2}$. The product $k_Dd$ is the force with which the spring pulls the particle back.
- $q_D$: the charge of the Drude particle, in units of $e$. The core carries the opposite charge in addition to the ordinary partial charge of the atom, so the pair adds no net charge.
- $E$: the size of the local electric field at the atom. The product $q_DE$ is the electric force on the particle.
- $\Longrightarrow$: "from which it follows". Here: divide both sides by $k_D$.
</div>

A charge $q_D$ displaced by $d$ from an opposite charge is a dipole (see the box on dipoles), with the moment

$$
\mu = q_D\,d = \frac{q_D^2}{k_D}\,E , \qquad\text{so that}\qquad \alpha = \frac{q_D^2}{k_D} .
$$

<div class="legend" markdown="1">
- $\mu$: the induced dipole moment of the atom, charge times displacement.
- $\alpha$: the polarisability of the atom, defined by $\mu = \alpha E$: the induced dipole per unit of field.
- Other symbols: as in the list above.
</div>

**Read it like this.** A soft spring or a large Drude charge makes a polarisable atom. Only the combination $q_D^2/k_D$ matters for the polarisability. A numerical illustration with round values: take $q_D = 1.5\,e$, $k_D = 4\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ and the field of a unit charge at 0.3 nm computed above. Then $d = 1.5\times1544/(4\times10^5) = 0.0058$ nm, about 2 % of the distance to the charge that causes the field, and $\mu = 1.5\times0.0058 = 0.0087\,e$ nm $= 0.42$ D.

The other phrases of the bullet concern how the model is run. In principle the Drude particles should sit, at every step, exactly where the forces on them balance, and finding those positions for all atoms at once would need a calculation by iteration. The cheaper route treats each Drude particle as a real particle with a small mass and lets it move by the ordinary equations of motion. This is the "extended Lagrangian" recipe of Module 2: give an invented variable a mass and a kinetic energy, and it obtains an equation of motion.

"Kept cold" means that a separate thermostat (an algorithm that controls a temperature, Module 8) holds the motion of the Drude particles relative to their atoms at a very low temperature, so that they stay close to their balance positions. A light particle on a stiff spring oscillates fast (Module 2: the angular frequency of a spring is the square root of its stiffness over the mass), which is why the time step has to be short.

### Induced point dipoles, step by step

Here there is no extra particle. Each atom $i$ is given a polarisability $\alpha_i$ and carries, in addition to its permanent charge, an induced dipole that is computed again at every step from the field at the atom:

$$
\boldsymbol\mu_i = \alpha_i\,\mathbf E_i , \qquad \mathbf E_i = \mathbf E_i^{perm} + \sum_{j\ne i}\mathbf T_{ij}\,\boldsymbol\mu_j .
$$

<div class="legend" markdown="1">
- $\boldsymbol\mu_i$: the induced dipole on atom $i$. It is a vector (a bold Greek letter), with a size and a direction.
- $\alpha_i$: the polarisability of atom $i$.
- $\mathbf E_i$: the total electric field at the position of atom $i$.
- $\mathbf E_i^{perm}$: the part of that field that is created by the permanent charges (and permanent multipoles) of the other atoms. "perm" is a label.
- $\sum_{j\ne i}$: a sum over all the other atoms $j$.
- $\mathbf T_{ij}$: a table of $3\times3$ numbers (a matrix) that converts the dipole on atom $j$ into the field it creates at atom $i$. It depends only on the vector from $j$ to $i$, and its entries fall off as the inverse cube of the distance.
- $\mathbf T_{ij}\,\boldsymbol\mu_j$: the matrix applied to the vector, which gives the field at atom $i$ caused by the dipole on atom $j$.
</div>

The difficulty is in the second formula. The field at atom $i$ contains the dipoles of all the other atoms, and each of those depends on the field at its own position, which contains the dipole of atom $i$. Every dipole depends on every other one.

A set of dipoles that satisfies all these equations at once is called **self-consistent**. The equations are linear in the dipoles, so they can be solved directly as one large linear system, or by iteration: start with the dipoles caused by the permanent field alone, compute the fields again, update the dipoles, and repeat until they stop changing. Either way it has to be done at every time step, and that is the main cost of the model.

<details markdown="1"><summary>Optional: two polarisable atoms, solved by hand</summary>
Two identical atoms with polarisability $\alpha$ sit a distance $r$ apart, in a field $E$ from permanent charges that points along the line joining them. By symmetry both carry the same induced dipole $\mu$, along that line. A dipole $\mu$ creates, at a distance $r$ along its own axis, the field $2\mu/(4\pi\varepsilon_0r^3)$. So each atom feels $E$ plus the field of the other dipole:

$$
\mu = \alpha\left(E + \frac{2\mu}{4\pi\varepsilon_0r^3}\right) \quad\Longrightarrow\quad \mu = \frac{\alpha E}{1-2\alpha'/r^3}, \qquad \alpha' = \frac{\alpha}{4\pi\varepsilon_0} .
$$

The second form follows by collecting the terms with $\mu$ on the left-hand side, $\mu\,(1-2\alpha'/r^3)=\alpha E$, and dividing by the bracket. The quantity $\alpha'$ has the unit of a volume, and it is the form in which polarisabilities are usually tabulated. With the illustrative values $\alpha' = 0.001$ nm$^3$ and $r=0.3$ nm, $2\alpha'/r^3 = 0.002/0.027 = 0.074$, so $\mu = 1.08\,\alpha E$: each dipole is 8 % larger than it would be without the other.

Iteration reaches the same answer. Start with $\mu = \alpha E$ (no mutual induction) and insert it on the right-hand side: the result is $1.074\,\alpha E$. Insert that: $1.0796\,\alpha E$. Once more: $1.07997\,\alpha E$. The sequence converges to $1.08\,\alpha E$, the self-consistent value.
</details>

"Permanent multipoles up to quadrupoles" concerns the charges that are not induced. A point charge on an atom says how much charge the atom has. A point dipole on the atom adds the information that the charge is shifted to one side, and a quadrupole that it is stretched or flattened. Together they describe features that atom-centred point charges cannot, such as lone pairs (Module 5).

In the third model, **electronegativity** is the strength with which an atom attracts electrons. The partial charges are variables: at every step, charge is moved between the atoms of a molecule until all atoms pull on the electrons equally hard, and the field of the surroundings shifts that balance.

### What polarisation costs

The cost is a few times that of a fixed-charge simulation: the Drude model costs about twice as much per step and, with its 1 fs time step, about four times overall, and induced-dipole models cost more. They can adapt to molecules that move between very different environments (ions, membranes, interfaces). Whether they are more accurate overall is still open: a 2018 review judged that AMOEBA needed more development before it would beat the best fixed-charge force fields for solvation and binding free energies, and that multivalent ions with nucleic acids remained hard for the Drude model ([Nerenberg and Head-Gordon 2018](cite:nerenberg2018)). For routine protein simulation they have not yet displaced the additive models, which have had far more tuning.

The factor four is two times two: each step costs twice as much, and a time step of 1 fs needs twice as many steps per nanosecond as the 2 fs that are usual with constrained bonds (Module 9).

"Additive" is the name for fixed-charge force fields. Their total electrostatic energy is a sum of pair terms, and the term for one pair does not depend on which other atoms are near. In a polarizable model it does, because the neighbours change the dipoles.

"Solvation and binding free energies" are the free energies of moving a molecule into a solvent and of binding a ligand to a protein (Modules 12 and 13). "Multivalent ions" carry more than one elementary charge, such as Mg$^{2+}$. Their strong fields polarise everything around them, which is why they are hard to model.

## How force fields are validated

**Fitting** and **validation** use the same kind of comparison, a simulation against a reference, for opposite purposes. Fitting data are used to choose the parameters. Validation data are kept out of the fit and used afterwards to test the result.

Agreement with the fitting data shows only that the fit worked. Agreement with validation data shows that the model predicts something it was not told, and that is the evidence that it may work for your system. The first maths box gave the reason: with enough parameters, a model reproduces any data it was fitted to.

The border between the two moves with time. When a validation test fails, the next version of a force field is often adjusted against that kind of data, as the ff14SB backbone was adjusted against NMR data. For the new version, data of that kind are then no longer an independent test.

Know these tests, because they are what "this force field is good" means in a paper:

- **Small-molecule liquids**: density, heat of vaporisation, hydration free energy (errors of about 4 kJ/mol are typical).
- **Peptides**: NMR scalar couplings ($^3J$, via the Karplus relation to $\phi$), helix propensities, populations of polyproline II, β and α regions.
- **Folded proteins**: stability of the native state over microseconds, NMR order parameters, residual dipolar couplings.
- **Folding**: reversible folding of small fast-folding proteins to the right structure and melting temperature.
- **Disordered proteins**: radius of gyration from SAXS, chemical shifts, paramagnetic relaxation enhancement.

The observables in this list, in the order in which they appear:

- **Density, heat of vaporisation, hydration free energy**: see the first section. An error of 4 kJ/mol is $4/2.494 = 1.6\,k_BT$ at 300 K, or about 1 kcal/mol. It changes a predicted equilibrium ratio of concentrations by a factor $e^{1.6}\approx5$.
- **Scalar coupling** $^3J$: a splitting of NMR signals caused by two nuclei that are three bonds apart. Its size depends on the torsion angle about the middle bond through the **Karplus relation**, which has the form $J = A\cos^2\theta + B\cos\theta + C$, where $\theta$ is the torsion angle between the two nuclei and $A$, $B$, $C$ are constants found from experiment. For the two hydrogens on either side of the backbone N-Cα bond, that angle follows from the backbone angle $\phi$. The measured value is an average over all conformations, so it tests the distribution of $\phi$.
- **Helix propensity**: the fraction of the time that a peptide, or one residue of it, spends in a helix.
- **Polyproline II, β and α regions**: three regions of the map of the backbone angles $(\phi,\psi)$, the Ramachandran map, in which most residues are found. Their relative populations are a sensitive test of the backbone torsion terms.
- **Stability of the native state over microseconds**: a simulation started from the experimental structure should stay close to it for as long as one can simulate.
- **NMR order parameter**: a number between 0 and 1 for each bond vector, usually the backbone N-H bond, which says how restricted the motion of its direction is. 1 means rigid and 0 means free. It tests the amplitude of the fast local motions.
- **Residual dipolar couplings**: NMR quantities, measured on weakly aligned molecules, that depend on the average direction of each bond vector relative to the molecule as a whole. They test the structure and its fluctuations.
- **Reversible folding**: the simulated protein folds and unfolds several times in one trajectory, so that the populations of the two states can be compared with experiment. The **melting temperature** is the temperature at which the folded and the unfolded state are equally populated.
- **Radius of gyration from SAXS, chemical shifts, paramagnetic relaxation enhancement**: see the section on disordered proteins.

[Lindorff-Larsen et al. (2012)](cite:lindorfflarsen2012), who compared eight force fields on folded proteins, peptides and the folding of two small proteins, and [Robustelli et al. (2018)](cite:robustelli2018), who added disordered proteins, are the standard systematic comparisons.

"Systematic" means that all the force fields were run on the same systems, in the same way, and compared with the same data, so that a difference in the result can be assigned to the force field.

## What a topology file contains

<div data-videos="uLlWNqoPNA0"></div>

The parameter files of a force field are general tables: for each atom type and each combination of types, the numbers. Your protein is a particular list of atoms. The **topology** is what you get when the tables are applied to that list. It says which atoms exist, which type, charge and mass each one has, and which atoms are joined in bonds, angles and torsions. The name reflects that it records who is connected to whom, while the positions of the atoms are stored separately, in the coordinate file.

The force field is applied to your molecule by a program (`gmx pdb2gmx`, `tleap`, CHARMM-GUI, OpenMM's `ForceField`) that matches residues to templates and produces a **topology** (a file in GROMACS, AMBER and CHARMM; an in-memory `System` object in OpenMM). Reading one is the best way to make the functional form concrete. A GROMACS topology has these sections:

```
[ atoms ]      ; nr  type  resnr  residue  atom  cgnr  charge    mass
                  1   N3     1      ALA     N     1    0.1414   14.01
[ bonds ]      ; ai  aj  funct   (r0 and kb are looked up from the atom types)
[ pairs ]      ; the 1-4 pairs, with scaled non-bonded interactions
[ angles ]     ; ai  aj  ak  funct
[ dihedrals ]  ; ai  aj  ak  al  funct   (9 = proper, 4 = improper in AMBER ports)
```

How to read it. Everything after a semicolon is a comment.

- `[ atoms ]`: one line per atom. `nr` is the number of the atom in the molecule, `type` its atom type, `resnr` and `residue` the number and the name of the residue it belongs to, `atom` its name within the residue, `cgnr` the number of its charge group (a bookkeeping label), `charge` its partial charge in units of $e$, and `mass` its mass in u. The example line is atom 1, the atom N of residue 1, an alanine, with type `N3`, charge $+0.1414\,e$ and mass 14.01 u.
- `[ bonds ]`: one line per bond. `ai` and `aj` are the numbers of the two bonded atoms, and `funct` is a number that selects the functional form, for example the harmonic bond of Module 5. The equilibrium length $r_0$ and the force constant $k_b$ are not written here. The program finds them in the parameter tables from the types of the two atoms.
- `[ pairs ]`: the list of 1-4 pairs, the atoms three bonds apart whose non-bonded interaction is scaled.
- `[ angles ]` and `[ dihedrals ]`: the same for groups of three and four atoms. For dihedrals, the function number tells proper torsions from impropers (the terms of Module 5 that keep groups planar).

The atom **type** (here `N3`) is the key into the parameter tables: two atoms with the same type have the same Lennard-Jones parameters and take part in the same bonded parameters. The **charge** is per atom, set by the residue template.

Everything the simulation knows about the chemistry of your system is in this file. When a simulation behaves strangely, the topology is a good first place to look: a wrong charge, a missing torsion, or a total charge that is not a whole number can be seen there.

## Check yourself

<details markdown="1"><summary>1. Why are torsion parameters fitted last?</summary>
Rotating about a bond also changes the 1-4 Coulomb and Lennard-Jones energies and slightly strains angles. The torsion term is defined as whatever is needed to make the total match the QM rotational profile, so it can only be fitted after the other terms are fixed.
</details>

<details markdown="1"><summary>2. You find a ligand parameterised with GAFF and want to simulate it with a CHARMM36m protein. Is that acceptable?</summary>
No. The charge models (RESP at HF/6-31G\* or AM1-BCC in GAFF, against charges fitted to water-interaction energies in CHARMM), 1-4 scaling (0.833 and 0.5 against 1.0) and the Lennard-Jones balance differ. Use CGenFF for the ligand with CHARMM36m, or switch the protein to an AMBER force field with GAFF2 or OpenFF.
</details>

<details markdown="1"><summary>3. A disordered region collapses onto the folded domain within 200 ns in ff14SB/TIP3P. What do you check before believing it?</summary>
Whether the same happens in a force field validated on disordered proteins (a99SB-disp first, then CHARMM36m and ff19SB/OPC as further checks). AMBER force fields of that generation combined with TIP3P water over-compact disordered chains ([Robustelli et al. 2018](cite:robustelli2018) show it for a99SB\*-ILDN with TIP3P), so the collapse may be an artefact. If SAXS data exist, compare the radius of gyration.
</details>

<details markdown="1"><summary>4. Why does TIP3P water have a larger dipole moment than a real gas-phase water molecule?</summary>
In the liquid each molecule is polarised by its neighbours and its average dipole is larger than in the gas. A fixed-charge model cannot respond, so it is built with the enhanced, liquid-like dipole from the start.
</details>

<details markdown="1"><summary>5. A colleague reports that new torsion parameters reproduce the QM scans they were fitted to within 0.1 kJ/mol. Why is this not yet evidence that the force field is good?</summary>
It shows only that the fit worked. A cosine series with enough terms reproduces any scan, including its noise. Evidence comes from data that were kept out of the fit: other molecules, properties of liquids and solutions, NMR observables of peptides and proteins.
</details>

<details markdown="1"><summary>6. What does the RESP penalty for one atom look like for a charge much smaller than b, and for a charge much larger than b?</summary>
For $|q|\ll b$ it is approximately $a\,q^2/2b$, a parabola. For $|q|\gg b$ it is approximately $a\,(|q|-b)$, a straight line. Here $q$ is the charge of the atom, and $a$ and $b$ are the strength and the width constant of the penalty. The slope, which is the pull towards zero, never exceeds $a$, so large, well-determined charges are not forced down.
</details>

<details markdown="1"><summary>7. What is the difference between a three-site and a four-site water model, and what does the fourth site cost?</summary>
In a three-site model the charges sit on the three atoms. In a four-site model the negative charge is moved from the oxygen to a massless site M on the bisector of the H-O-H angle, which gives one more adjustable number and a better description of how the charge is spread. The price is computer time, because the extra site adds distances to compute for every pair of nearby molecules.
</details>

## Exercises

1. Download the ff14SB and CHARMM36m parameter files (both are distributed with GROMACS ports). Find the backbone N-CA-C angle parameters in each and convert them to the same units and convention.
2. Set up the ESP fitting equations for a diatomic molecule with two charges and a total-charge constraint, and solve them symbolically. Show the result fixes only the dipole.
3. Simulate 1,000 molecules of TIP3P and of OPC water for 1 ns each (Module 10 gives the workflow). Compute the density and the self-diffusion coefficient from the mean squared displacement (Module 11). Compare with experiment.
4. Read the abstract and validation figures of [Robustelli et al. 2018](cite:robustelli2018). List the classes of experimental data used and which force fields failed which class.

## Read

{{READ}}

## Key papers

{{PAPERS}}
