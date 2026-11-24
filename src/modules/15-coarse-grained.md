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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

An all-atom simulation follows every atom, and most of those atoms are water. For many questions that is more detail than the answer needs, and it limits you to small systems and short times. A coarse-grained model keeps fewer particles and can follow them for longer. This module explains what such a model is, how the main families are built, and what each of them can be trusted for.

One idea runs through the whole module. When you remove particles from a model, their effect does not disappear. It has to be put into the interactions between the particles that stay.

The interactions of a coarse-grained model are therefore averages over everything that was removed. An average of that kind is a free energy, and a free energy behaves differently from an ordinary energy. Most of the warnings in this module follow from that one fact.

The module has four layers:

1. **Why and what.** What coarse-graining removes, what it gains, and how atoms are grouped into beads.
2. **The theory.** What the correct potential between beads would be, how it is approximated in practice, and what happens to time, energy and temperature.
3. **The model families.** Martini, structure-based (Gō) models, one-bead-per-residue models for disordered proteins, and implicit solvent.
4. **Using the result.** Going back to atoms, and a list of questions to ask before you believe a coarse-grained result.

Layer 2 is the most abstract. If it is heavy on a first reading, keep its three conclusions (the potential is a free energy, it depends on the conditions, and simulated time is not real time) and go on to the models.

### How to read the formulas

Every displayed formula in the main text is followed by a list that says what each letter in it means. The table gives the notation that is new in this module or that it uses heavily. The general conventions (bold letters for vectors, $\sum$ for sums, and so on) are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\mathbf r$ and $\mathbf R$ | Lower-case bold $\mathbf r$: the positions of all atoms. Capital bold $\mathbf R$: the positions of all beads. In this module lower case belongs to the atomistic model and capitals to the coarse-grained one: $u$ and $U_{CG}$, $i$ and $I$, $\mathbf f$ and $\mathbf F$. |
| $\mathbf M(\mathbf r)$ | The **mapping**: the rule that computes the bead positions from the atom positions. |
| AA, CG | Subscripts for "all-atom" and "coarse-grained". |
| $k_BT$ and $\beta$ | The thermal energy, 2.494 kJ/mol at 300 K, and its inverse $\beta=1/k_BT$ (Module 3). |
| $\ln x$ | The natural logarithm, the inverse of the exponential: $\ln(e^x)=x$. |
| $\langle A\rangle$ | The average of $A$ over the frames of a simulation. |
| $\int d\mathbf r$ | An integral over all atom positions: "add up over every possible configuration". |
| $\delta(x)$ | The Dirac delta function, zero unless $x=0$. Inside an integral it selects the configurations for which its argument is zero. |
| $\propto$ | "Is proportional to": equal up to a constant factor. |
| $\sim$ | "Has the form of", for a relation that leaves out details. |
| $\lambda\in[0,1]$ | $\lambda$ is a number between 0 and 1, the ends included. |
| A large brace with two lines | A function that is given by different formulas in different ranges of its variable. |
| $\nabla$ and $\nabla\cdot$ | The gradient and the divergence (Module 2). |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which is meant each time.

- $\varepsilon$ and $\varepsilon_{ij}$ are energies: the depth of an attractive well in the Lennard-Jones and contact potentials. $\varepsilon_0$, $\varepsilon_r$, $\varepsilon_{in}$, $\varepsilon_{out}$ and $\varepsilon(\mathbf r)$ are dielectric constants, which say how strongly a medium weakens electric forces.
- $\lambda$ is the stickiness of a residue. $\lambda_D$ is the Debye length.
- $\phi$ is a dihedral angle in the Gō model and the electrostatic potential in the Poisson-Boltzmann equation.
- $q$ is a general coordinate in Boltzmann inversion and a charge everywhere else.
- $R$ appears in the bead positions $\mathbf R$, the Born radius $R_i$, the gas constant in $RT$ and the radius of gyration $R_g$.
- $e$ is the base of the exponential. In the formula for the Debye length it is also the elementary charge.
- $I$ labels a bead. In the Debye-Hückel formula it is the ionic strength.
- $\gamma$ is an energy per area in the non-polar solvation term and a friction coefficient in Langevin dynamics.
- $\sigma$ is always a distance, but its exact meaning differs between the Lennard-Jones formula and the Gō contact formula.
- $i$ and $j$ label atoms in most formulas, beads of a chain in the Gō and residue-level formulas, amino-acid types in the statistical contact potential, and kinds of ion in the Poisson-Boltzmann equation.
- $\mathbf r$ in bold is the list of all atom positions, except in the Poisson-Boltzmann equation, where it is one point in space. $r$ without bold is a distance.
- Q, P, N and C are names of Martini bead types. $Q$ is also the fraction of native contacts, and $N$ a number of beads or residues.
</div>

## Why coarse-grain

<div data-videos="yBnn567JXdo 0XZ8tAwNHdE 0NJxWb-sXg8"></div>

This section answers two questions: what a coarse-grained model is, and why it is so much cheaper than an all-atom one.

All-atom simulation spends most of its effort on water and on fast local motions. "Effort" means computer time. Most of the atoms in a simulation box belong to water molecules, and the time step is set by the fastest vibrations in the system, those of bonds to hydrogen (Modules 4 and 9). If the question is how a membrane bends or how two proteins find each other, most of that work goes into details that the answer does not depend on.

A coarse-grained (CG) model replaces groups of atoms by single interaction sites ("beads"). A bead is one particle that stands for a small group of atoms: four water molecules, a stretch of four carbon atoms with their hydrogens, an amino-acid side chain, or a whole residue. The beads interact through a force field of their own, and the simulation moves beads with the same algorithms that move atoms.

A road map is a useful picture of the idea. It leaves out the houses and keeps the towns and the roads, and that is why a whole country fits on one sheet. The picture breaks down in one place that matters. A map only has to show where things are, while a CG model must also make the beads attract, repel and move in the right way. Deciding what the interactions between beads should be is the hard part, and the next section is about it.

The gain comes from four sources at once: fewer particles, shorter-ranged and simpler interactions, a larger time step because the fast vibrations are gone, and faster effective dynamics because the energy landscape is smoother. Speed-ups of $10^2$ to $10^5$ result, which brings membranes, large assemblies, folding, binding and phase separation within reach.

### Where the speed comes from, with numbers

Take the four sources one at a time. The example is a box of pure water, with the Martini settings given later in this module: four water molecules per bead, a cutoff of 1.1 nm and a time step of 20 fs.

**1. Fewer particles.** Liquid water has 33.4 molecules per nm$^3$, which is 100 atoms per nm$^3$. With four molecules per bead there are $33.4/4=8.4$ beads per nm$^3$. That is 12 times fewer particles.

**2. Shorter-ranged and simpler interactions.** The cost of one MD step is roughly proportional to the number of pairs of particles that are closer than the cutoff (Module 7). A sphere of radius 1.1 nm has a volume of 5.6 nm$^3$. In the all-atom model it contains about 560 atoms, in the CG model about 47 beads. So each particle has 12 times fewer neighbours, and with 12 times fewer particles the number of pairs falls by about $12\times12=144$. The interactions are also simpler: in the usual Martini setting the electrostatic interactions are treated with a reaction field inside the same cutoff (see below), so there is no Ewald sum (Module 7) to compute.

**3. A larger time step.** The time step must be a small fraction, a tenth to a twentieth, of the period of the fastest vibration (Module 4). In an all-atom model that is a bond to hydrogen, with a period near 11 fs (Module 2). In a CG model the hydrogens are inside the beads. What is left are heavy beads joined by soft springs, and the angular frequency of a spring is $\omega=\sqrt{k/\mu}$, where $k$ is the stiffness and $\mu$ the reduced mass of the two particles (Module 2, and the [primer](physics.html#oscillator)).

Say two beads of 50 u each are joined by a spring with $k=10{,}000$ kJ mol$^{-1}$ nm$^{-2}$ (round numbers for illustration). Then $\mu=25$ u, $\omega=\sqrt{10{,}000/25}=20$ ps$^{-1}$ and the period is $2\pi/\omega=0.31$ ps, or 310 fs. That is about 30 times longer than the period of a bond to hydrogen. Martini uses 20 fs where an all-atom simulation with constrained bonds uses 2 fs: a factor of 10.

**4. Faster effective dynamics.** In an all-atom liquid a molecule that moves has to push past its neighbours, and every small rearrangement (a hydrogen bond that breaks, a side chain that turns) is a small energy barrier. Beads are larger and softer than atoms, and the small barriers have been averaged away. This is what "the energy landscape is smoother" means. The same process then needs fewer simulated nanoseconds. For diffusion in Martini the factor is about 4 (see the section on time below).

**Together.** $144\times10\times4$ is about 5,800, between $10^3$ and $10^4$, inside the range quoted above. A model with one bead per residue and no water at all removes still more. A protein of 100 residues (about 1,600 atoms) in a box with 10,000 water molecules is about 31,600 atoms in the all-atom model and 100 beads in such a CG model. These are estimates of how the cost scales. They are not measurements of any program.

### What is given up

The price is that the model answers fewer questions, and you must know which. Four things are lost, and each returns later in the module.

- **Detail inside a bead.** The positions of single atoms, the direction of a hydrogen bond and the orientation of a side chain or of a water molecule no longer exist in the model. A question about them cannot be asked.
- **Real time.** The beads move faster than the groups of atoms they stand for, by a factor that differs from process to process.
- **Energies and entropies as separate quantities.** The interactions between beads are free energies. Only free-energy differences (populations, binding constants) can be compared with experiment or with an all-atom model.
- **Validity away from the conditions of the fit.** A CG force field is tuned at one temperature and composition and is not automatically correct at another.

CG models differ in how many atoms go into one bead. This is the **resolution** of the model. The table lists the common levels from the finest to the coarsest.

| Resolution | Sites | Examples |
|---|---|---|
| All-atom | every atom | AMBER, CHARMM |
| United-atom | non-polar H merged | GROMOS |
| About 4 heavy atoms per bead | 2 to 5 beads per residue | Martini, SIRAH |
| One bead per residue | C$\alpha$ | Gō and structure-based models, elastic network models, HPS, CALVADOS, AWSEM (three sites) |
| Many residues per bead | domains | Shape-based and domain-level models, patchy-particle models |

Some words in the table. A **heavy atom** is any atom other than hydrogen. In a **united-atom** model each non-polar hydrogen is merged into the carbon it is bonded to, so a CH$_3$ group is one particle. C$\alpha$ is the central carbon atom of a residue's backbone, the one that carries the side chain. An **elastic network model** joins the beads of a known structure by springs (it returns in the Martini section).

The names in the last column are force fields and models. This module treats Martini, the Gō and structure-based models, HPS and CALVADOS. The other names are listed so that you recognise them in a paper.

## What a coarse-grained potential is

<div data-videos="TqHS4tpujnw"></div>

A CG model needs a force field for its beads. This section asks what that force field should be if the beads are to behave as the same groups of atoms behave in the all-atom simulation. The question has an exact answer. The answer cannot be computed for a real system, but it shows what every practical CG force field is an approximation to, and what such an approximation can and cannot get right.

The section has four steps: the mapping from atoms to beads, the exact potential, three consequences of the fact that it is a free energy, and the two ways of building an approximation (bottom-up and top-down).

### The mapping from atoms to beads

Let $\mathbf r$ be the atomistic coordinates and $\mathbf R=\mathbf M(\mathbf r)$ the CG coordinates, for example the centre of mass of each group.

In words: $\mathbf r$ is the long list of the positions of all $n$ atoms, and $\mathbf R$ is the shorter list of the positions of all $N$ beads. The **mapping** $\mathbf M$ is the rule that turns the first list into the second. You choose it when you design the model: you decide which atoms belong to which bead, and where in the group the bead sits. The most common choice puts each bead at the centre of mass of its atoms:

$$
\mathbf R_I=\frac{\sum_{i\in I}m_i\,\mathbf r_i}{\sum_{i\in I}m_i}.
$$

<div class="legend" markdown="1">
- $I$: the label of one bead, from 1 to $N$. It is a capital letter to tell it from the atom label $i$.
- $\mathbf R_I$: the position of bead $I$, a vector with three components, in nm.
- $i\in I$: "atom $i$ belongs to bead $I$". Both sums run over the atoms of that bead only.
- $m_i$: the mass of atom $i$, in atomic mass units (u).
- $\mathbf r_i$: the position of atom $i$.
- The denominator $\sum_{i\in I}m_i$: the total mass of the group. It is the natural choice for the mass of the bead.
</div>

Read it like this: the bead sits at the average position of its atoms, and heavy atoms count more than light ones. An example along a line: a carbon atom (12 u) at $x=0$ and a hydrogen atom (1 u) at $x=0.11$ nm have their centre of mass at $(12\times0+1\times0.11)/13=0.0085$ nm, almost on the carbon. A mapping of this kind, in which each bead position is a weighted sum of atom positions, is called a **linear mapping**. The term comes back in the paragraph on force matching.

The mapping goes one way only. Each atomistic configuration gives exactly one set of bead positions. But one set of bead positions corresponds to a very large number of atomistic configurations: the four water molecules behind a water bead can be turned and shifted in countless ways without moving their common centre of mass. The coordinates that the mapping discards (the orientations and internal arrangements of the groups) are called the **eliminated degrees of freedom**. A degree of freedom is one independent way in which the system can move (Module 2).

### The exact answer: a potential of mean force

Two reminders from Module 3. First, at temperature $T$ an atomistic configuration $\mathbf r$ with potential energy $u(\mathbf r)$ occurs with a probability proportional to its **Boltzmann factor** $e^{-\beta u(\mathbf r)}$, where $\beta=1/k_BT$. Configurations of low energy are common and those of high energy are exponentially rare. Second, the probability of anything less detailed than a full configuration is found by adding up the Boltzmann factors of all the configurations that agree with it.

<div class="box maths" markdown="1">
**Maths you need here: a sum over all configurations, and the delta function that selects some of them.** The sign $\int d\mathbf r$ is an integral over every coordinate of every atom. Read it as "add up the expression that follows over all possible configurations". If the atoms could take only a finite list of configurations it would be an ordinary sum, and the worked example below uses such a sum.

The **Dirac delta function** $\delta(x)$ is zero for every $x$ except $x=0$, and it is so high at that one point that its integral is exactly 1. Its use is to pick one value out of an integral: $\int f(x)\,\delta(x-a)\,dx=f(a)$. For example, $\int x^2\,\delta(x-3)\,dx=9$.

Under the integral over configurations, $\delta\big(\mathbf M(\mathbf r)-\mathbf R\big)$ does the same job for a whole configuration. It keeps the configurations $\mathbf r$ whose bead positions $\mathbf M(\mathbf r)$ are equal to $\mathbf R$ and discards all the others. More in the toolbox: [integrals](maths.html#integral) and [delta functions](maths.html#delta).
</div>

The probability of finding the beads at $\mathbf R$ in the all-atom simulation is therefore the sum of the Boltzmann factors of all atomistic configurations that map to $\mathbf R$:

$$
p_{AA}(\mathbf R)=\frac1Z\int d\mathbf r\;\delta\big(\mathbf M(\mathbf r)-\mathbf R\big)\,e^{-\beta u(\mathbf r)} .
$$

<div class="legend" markdown="1">
- $p_{AA}(\mathbf R)$: the [probability density](maths.html#probability) of the bead positions $\mathbf R$ in the all-atom (AA) simulation. It is what you get by mapping every frame to beads and making a histogram.
- $Z$: the normalisation constant $\int d\mathbf r\,e^{-\beta u(\mathbf r)}$, which makes the total probability equal to 1. It is the configurational partition function of Module 3.
- $\int d\mathbf r$: the sum over all atomistic configurations (see the box).
- $\delta\big(\mathbf M(\mathbf r)-\mathbf R\big)$: the delta function that keeps only the configurations that map to $\mathbf R$.
- $u(\mathbf r)$: the atomistic potential energy, that is, the all-atom force field. It is a lower-case $u$, to tell it from the CG potential.
- $\beta$: $1/k_BT$, with $k_B$ the Boltzmann constant and $T$ the temperature. At 300 K, $k_BT=2.494$ kJ/mol.
</div>

A CG simulation with a potential $U_{CG}(\mathbf R)$ follows the same rule with its own energy function. It visits the bead configuration $\mathbf R$ with the probability

$$
p_{CG}(\mathbf R)=\frac{1}{Z_{CG}}\,e^{-\beta U_{CG}(\mathbf R)} .
$$

<div class="legend" markdown="1">
- $p_{CG}(\mathbf R)$: the probability density of the bead positions in the CG simulation.
- $U_{CG}(\mathbf R)$: the potential energy function of the CG model, the unknown we are looking for.
- $Z_{CG}$: the normalisation constant of the CG model, $\int d\mathbf R\,e^{-\beta U_{CG}(\mathbf R)}$.
- Other symbols: as in the list above.
</div>

<div class="box maths" markdown="1">
**Maths you need here: the logarithm, which turns probabilities into energies.** The natural logarithm $\ln$ undoes the exponential: $\ln(e^x)=x$. Three rules are used again and again in this module: $\ln(ab)=\ln a+\ln b$, $\ln(a/b)=\ln a-\ln b$, and $\ln1=0$. The logarithm of a number below 1 is negative.

A probability is proportional to $e^{-E/k_BT}$, where $E$ is an energy. Taking $-k_BT\ln$ of a probability therefore gives back an energy, and a ratio of probabilities becomes a difference of energies. If one state is 10 times more probable than another, it lies lower by $k_BT\ln10=2.303\,k_BT$, which is 5.74 kJ/mol at 300 K. More in the [toolbox](maths.html#exp-log).
</div>

We want the two probabilities to be equal for every $\mathbf R$. Set the two right-hand sides equal, take the logarithm of both sides and multiply by $-k_BT$. The logarithm turns the products into sums, so the two constants $Z$ and $Z_{CG}$ end up in one additive constant that does not depend on $\mathbf R$. Every step can be reversed, which is why the statement holds in both directions ("if and only if"). The CG model reproduces the atomistic distribution of $\mathbf R$ exactly if and only if its potential is

$$
\boxed{U_{CG}(\mathbf R) = -k_BT\ln\int d\mathbf r\;\delta\big(\mathbf M(\mathbf r)-\mathbf R\big)\,e^{-\beta u(\mathbf r)}+\text{const}}
$$

<div class="legend" markdown="1">
- $U_{CG}(\mathbf R)$: the potential that the CG model must have, a function of all bead positions together.
- $-k_BT\ln$: turns the sum of Boltzmann factors back into an energy (see the box on the logarithm).
- $\int d\mathbf r\;\delta(\dots)\,e^{-\beta u(\mathbf r)}$: the sum of the Boltzmann factors of all atomistic configurations that map to $\mathbf R$.
- $\mathbf M(\mathbf r)$: the mapping from atom positions to bead positions.
- $u(\mathbf r)$: the atomistic potential energy.
- const: a number that does not depend on $\mathbf R$. It shifts all energies by the same amount and has no effect on forces or probabilities.
- $k_BT$ and $\beta=1/k_BT$: the thermal energy and its inverse, as in the lists above.
- The frame around the formula marks it as the main result of the section.
</div>

Read it like this. To find the CG energy of one arrangement of the beads, collect every atomistic configuration that looks like that arrangement after mapping, add up their Boltzmann factors, and take $-k_BT\ln$ of the sum. An arrangement gets a low $U_{CG}$ for two different reasons: because the atomistic configurations behind it have low energy, or because there are many of them. The second reason is entropy, and it is what makes $U_{CG}$ a free energy.

<div class="box key" markdown="1">
**Worked example: the CG potential of a system with two bead arrangements.** Suppose the beads can be in only two arrangements. "Compact" (C) corresponds to a single atomistic configuration of energy 0. "Extended" (E) corresponds to 1,000 atomistic configurations, each of energy $+10$ kJ/mol. (This is the two-state example of Module 3.) With a finite list of configurations the integral is a sum: for each arrangement, $U_{CG}=-k_BT\ln\sum e^{-u/k_BT}$, where the sum runs over the configurations behind that arrangement and $u$ is the energy of each.

At 300 K, $k_BT=2.494$ kJ/mol. For C the sum is $e^0=1$, so $U_{CG}(\text{C})=0$. For E the sum is $1000\,e^{-10/2.494}=18.1$, so $U_{CG}(\text{E})=-2.494\times\ln18.1=-7.2$ kJ/mol. The CG model must make the extended arrangement *lower* by 7.2 kJ/mol, although every atomistic configuration behind it is *higher* in energy by 10 kJ/mol. The difference is the entropy term, $-k_BT\ln1000=-17.2$ kJ/mol: $10-17.2=-7.2$.

At 350 K, $k_BT=2.910$ kJ/mol. The same calculation gives $1000\,e^{-10/2.910}=32.2$ and $U_{CG}(\text{E})=-2.910\times\ln32.2=-10.1$ kJ/mol. The atomistic energies did not change. The correct CG potential did.
</div>

This is the **many-body potential of mean force** of the CG sites: the PMF of Module 3 with all the CG coordinates as the collective variables.

Three terms in that sentence need a reminder. A **collective variable** is a quantity computed from the atom positions that describes the system with fewer numbers (Module 14). Here the collective variables are the bead positions themselves. A CG **site** is another word for a bead. **Many-body** is explained under the second consequence below.

The **potential of mean force** (PMF) along a set of collective variables is the free energy as a function of them, that is, $-k_BT\ln$ of their probability (Modules 3 and 12). The name says what its slope is. For a centre-of-mass mapping, the force on bead $I$ (the sum of the forces on its atoms), averaged over all the atomistic configurations that map to $\mathbf R$, is minus the gradient of $U_{CG}$ with respect to the position of that bead.

Three consequences follow directly from the fact that it is a free energy, not an energy.

1. **It depends on the thermodynamic state.** Entropy of the eliminated degrees of freedom is folded in, so $U_{CG}$ changes with temperature, density and composition. A model fitted at 300 K is not automatically valid at 350 K. This is the **transferability** problem.
2. **It is many-body.** Even if the atomistic potential is pairwise, the integral is not. Practical CG models approximate $U_{CG}$ by pair potentials, and that approximation, not the idea of coarse-graining, is the main source of error.
3. **Not all properties can be right together.** A pair-potential model that reproduces the structure (the distribution functions) does not in general reproduce the pressure or the energy. This is the **representability** problem. Energies and entropies taken separately from a CG model do not correspond to the atomistic ones; only the free energy does.

Each of the three points is unpacked below.

**Consequence 1: the potential depends on the conditions.** A free energy has an energy part and an entropy part (Module 3, and the [primer](physics.html#thermodynamics)). For the CG potential the split reads

$$
U_{CG}(\mathbf R)=\langle u\rangle_{\mathbf R}-T\,S(\mathbf R)+\text{const}.
$$

<div class="legend" markdown="1">
- $\langle u\rangle_{\mathbf R}$: the average atomistic energy over the configurations that map to $\mathbf R$. The subscript says that the beads are held at $\mathbf R$ while everything else is averaged.
- $S(\mathbf R)$: the entropy of the eliminated degrees of freedom with the beads held at $\mathbf R$. It is larger when more atomistic configurations are available behind this arrangement of the beads.
- $T$: the temperature, in kelvin.
- const: a number that does not depend on $\mathbf R$, as before.
</div>

In the worked example the energy part of the extended arrangement is 10 kJ/mol and its entropy is $S=k_B\ln1000$. The entropy part is multiplied by $T$, so the potential changes when the temperature changes: from $-7.2$ kJ/mol at 300 K to $-10.1$ kJ/mol at 350 K in the example. It also changes with density and composition, because these change which atomistic configurations are available. The attraction that two beads feel through the water, for instance, depends on what else is dissolved in the water.

The **thermodynamic state** is the set of conditions (temperature, pressure or density, composition) that fix the macroscopic behaviour of a system. **Transferability** is the question whether a CG potential fitted in one state can be used in another. The formula says that there is no general reason why it should.

**Consequence 2: the potential is many-body.** A **pair potential** is an energy function that is a sum of terms, one for each pair of particles, each of which depends only on the distance within that pair. The atomistic non-bonded terms of Module 5 are of this kind. The integral in the boxed formula does not keep this form.

Picture two oily beads in water that attract each other because pushing them together releases the water between them. If a third bead already sits next to them, part of that water is gone, and the attraction of the first two is different. The energy of the pair depends on where the third bead is. Written out, the exact potential is a series:

$$
U_{CG}(\mathbf R)=\sum_{I<J}U^{(2)}(R_{IJ})+\sum_{I<J<K}U^{(3)}(\mathbf R_I,\mathbf R_J,\mathbf R_K)+\dots
$$

<div class="legend" markdown="1">
- $\sum_{I<J}$: a sum over all pairs of beads, each pair counted once.
- $U^{(2)}(R_{IJ})$: the pair term, a function of the distance $R_{IJ}$ between beads $I$ and $J$.
- $\sum_{I<J<K}$: a sum over all triplets of beads.
- $U^{(3)}$: the three-body term, the part of the energy of three beads that is not the sum of its three pairs.
- The dots: terms for four beads, five beads and so on.
- The numbers in brackets, $(2)$ and $(3)$, are labels. They are not powers.
</div>

Practical CG models keep the pair terms (and the bonded terms along a chain) and drop the rest. The best pair potential is then a compromise, and the compromise depends on the surroundings in which it was fitted. That is a second reason why a CG force field may not transfer.

**Consequence 3: one model cannot get every property right.** Reproducing the *structure* means that the CG simulation gives the same distributions of bead positions as the mapped all-atom simulation. An example is the radial distribution function $g(r)$: the density of beads at a distance $r$ from a given bead, divided by the average density (Module 11). A correct structure does not make other properties correct.

The pressure, for instance, is computed from the forces between the particles (the virial of Module 3), and a pair potential tuned for the structure in general gives a different pressure from the all-atom model. A correction that repairs the pressure changes the structure, so one has to choose. **Representability** is the name for this limit: a simplified model cannot represent all properties of the detailed one at the same time.

The last sentence of point 3 is the worked example again. The average of $U_{CG}$ in a CG simulation is not the average atomistic energy, because $U_{CG}$ already contains the entropy of the eliminated coordinates. In the example the extended arrangement has $U_{CG}=-7.2$ kJ/mol and an atomistic energy of $+10$ kJ/mol. So do not split a CG free energy into an "energy" and an "entropy" and compare the parts with experiment or with all-atom values. Compare free energies: populations, binding constants, partition coefficients.

### Bottom-up parameterisation

Fit the CG model to an atomistic simulation.

**Parameterisation** means choosing the numbers in a force field (Module 6). In the bottom-up route the reference is a model one level below. You run an all-atom simulation of the system, map every frame to beads, and ask which CG potential would produce the same bead statistics. The exact answer is the boxed formula, which cannot be evaluated. Each of the four methods below therefore matches something smaller that can be measured in the mapped trajectory:

| Method | What it tries to reproduce |
|---|---|
| Boltzmann inversion | the distribution of one coordinate |
| Iterative Boltzmann inversion | the radial distribution function of a pair of bead types |
| Force matching | the forces on the beads |
| Relative entropy | the whole distribution of bead positions |

On a first reading, Boltzmann inversion is the one to follow in detail. For the other three, the idea in the first paragraphs of each part is enough.

#### Boltzmann inversion

The first method reads a potential directly off a histogram.

**Boltzmann inversion.** For a single coordinate $q$ with distribution $P(q)$ from the atomistic reference, use $U(q)=-k_BT\ln\big[P(q)/J(q)\big]$, where $J$ is the Jacobian of the coordinate: $J=r^2$ for a bond length, $J=\sin\theta$ for a bond angle, $J=1$ for a dihedral. (Without it the potential picks up a spurious $-2k_BT\ln r$ or $-k_BT\ln\sin\theta$, which is badly wrong for angles near 180°.) Adequate for a coordinate that is nearly independent of the rest, such as a stiff bond or angle. For coupled coordinates (non-bonded pairs in a dense liquid) it gives only the pair PMF $-k_BT\ln g(r)$, which does not reproduce the target distribution.

<div class="legend" markdown="1">
- $q$: one coordinate of the CG model: the distance between two bonded beads, the angle formed by three, or the dihedral angle of four. It is not a charge here.
- $P(q)$: the probability density of $q$, that is, the normalised histogram of $q$ over the mapped all-atom frames.
- $U(q)$: the CG potential-energy term for this coordinate.
- $J(q)$: the **Jacobian**, the amount of space that is available at each value of $q$ (explained below).
- $r$, $\theta$: a bond length and a bond angle, two particular choices of $q$.
- $g(r)$: the radial distribution function of two bead types (Module 11).
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
</div>

**Where the formula comes from.** Suppose the coordinate $q$ moves in a potential $U(q)$ and nothing else acts on it. The Boltzmann distribution then gives its probability density as

$$
P(q)\propto J(q)\,e^{-U(q)/k_BT} .
$$

<div class="legend" markdown="1">
- $\propto$: "is proportional to". The missing constant factor is fixed by requiring that the total probability is 1.
- $e^{-U(q)/k_BT}$: the Boltzmann factor of the value $q$.
- $J(q)$: the Jacobian. It is there because some values of $q$ correspond to more configurations than others, whatever the energy.
- Other symbols: as in the list above.
</div>

Now solve for $U$. Divide both sides by $J(q)$ and take the logarithm: $\ln\big[P(q)/J(q)\big]=-U(q)/k_BT+\text{const}$. Multiply by $-k_BT$:

$$
U(q)=-k_BT\ln\frac{P(q)}{J(q)}+\text{const}.
$$

<div class="legend" markdown="1">
- const: a number that does not depend on $q$. It is usually chosen so that the minimum of $U$ is zero.
- Other symbols: as in the two lists above.
</div>

This is the formula of the paragraph above. "Inversion" refers to this step: the Boltzmann relation normally gives a distribution from a potential, and here it is used backwards. In practice you make a histogram of $q$ from the mapped frames, divide the count in each bin by $J$ at the centre of the bin, take $-k_BT\ln$, and fit a smooth function through the result.

**The Jacobian.** The three cases in the paragraph come from geometry.

- *Bond length.* Fix one bead and ask where the other can be if their distance lies between $r$ and $r+dr$. The answer is a spherical shell of area $4\pi r^2$ and thickness $dr$. The shell grows as $r^2$, so longer distances have more room. Two beads with no interaction at all would still show a histogram that rises as $r^2$.
- *Bond angle.* Fix two beads and let the third swing around. The directions that make an angle $\theta$ with the axis form a circle whose radius is proportional to $\sin\theta$. The circle is largest at 90° and shrinks to a point at 0° and at 180°. Three beads with no angle potential therefore show a histogram proportional to $\sin\theta$: straight arrangements are rare for a geometric reason.
- *Dihedral.* Every value of the rotation angle has the same room, so $J=1$.

If you forget to divide by $J$, the geometric factor is read as an energy. Since $\ln(P/J)=\ln P-\ln J$, the potential then contains an extra term $-k_BT\ln J$. That is $-2k_BT\ln r$ for a bond and $-k_BT\ln\sin\theta$ for an angle.

At 300 K the angle term is 0.4 kJ/mol at 120°, 2.7 kJ/mol at 160° and 4.4 kJ/mol at 170°, and it grows without limit towards 180°: a wall that is not in the atomistic system. For a stiff bond that moves between 0.36 and 0.40 nm, the bond term changes by only 0.5 kJ/mol over the whole range. This is why the Jacobian matters most for angles.

**From a histogram to a spring.** A common case: after division by $J$, the histogram of a bond length is close to a Gaussian (a bell curve, see the [toolbox](maths.html#gaussian)) centred at $q_0$ with standard deviation $s$, so $P/J\propto\exp\big[-(q-q_0)^2/2s^2\big]$. Taking $-k_BT\ln$ gives $U(q)=k_BT\,(q-q_0)^2/2s^2$. This is a harmonic spring $\tfrac12k\,(q-q_0)^2$ with stiffness $k=k_BT/s^2$. With $s=0.01$ nm at 300 K, $k=2.494/0.01^2$, which is about 24,900 kJ mol$^{-1}$ nm$^{-2}$. A narrower histogram gives a stiffer spring.

**When it is good enough.** Boltzmann inversion returns the free energy along $q$, a PMF, which contains the averaged effect of everything else in the system. Used as a potential-energy term, it is correct only if nothing else in the CG model acts on $q$. For a stiff bond or angle that is nearly true, because the other forces are too weak to move it. For the distance between two non-bonded beads in a liquid it fails. There the recipe gives $-k_BT\ln g(r)$ (the factor $r^2$ is already divided out in the definition of $g$), and this pair PMF includes the pushing and pulling of all the neighbours.

If you use the pair PMF as the pair potential, the neighbours are present in the CG simulation as well, and their effect is counted twice. The simulated $g(r)$ then differs from the target. Only in a very dilute system, where two beads meet with no neighbours around, is $-k_BT\ln g(r)$ the pair potential.

#### Iterative Boltzmann inversion

The second method repairs this by trial and correction.

**Iterative Boltzmann inversion.** For non-bonded pair potentials, correct the potential until the CG simulation reproduces the target radial distribution function: $U_{n+1}(r)=U_n(r)+k_BT\ln\big[g_n(r)/g_{target}(r)\big]$.

On its own line the update rule is

$$
U_{n+1}(r)=U_n(r)+k_BT\ln\frac{g_n(r)}{g_{target}(r)} .
$$

<div class="legend" markdown="1">
- $n$: the number of the iteration: 0, 1, 2 and so on.
- $r$: the distance between two non-bonded beads.
- $U_n(r)$: the pair potential used in iteration $n$.
- $g_n(r)$: the radial distribution function measured in the CG simulation that was run with $U_n$.
- $g_{target}(r)$: the radial distribution function of the beads in the mapped all-atom simulation.
- $U_{n+1}(r)$: the corrected potential for the next iteration.
- $k_BT\ln$: the thermal energy times the natural logarithm. It turns the ratio of the two distribution functions into an energy.
</div>

Read it like this. Start from a guess, for example the pair PMF $U_0=-k_BT\ln g_{target}$. Run a CG simulation and measure $g_0$.

At a distance where the simulation has too many pairs ($g_n>g_{target}$) the logarithm is positive and the potential is raised there, which pushes pairs away in the next round. Where it has too few pairs, the logarithm is negative and the potential is lowered. Where the two agree the ratio is 1, $\ln1=0$, and nothing changes.

An example: if $g_n=1.2$ at a distance where the target is 1.0, the potential at that distance is raised by $2.494\times\ln1.2=0.45$ kJ/mol at 300 K. The loop stops when $g_n$ matches the target everywhere within the noise. Keep in mind what has been matched: the pair structure, in one thermodynamic state. By consequence 3, the pressure and the energy need not follow.

#### Force matching

The third method fits forces instead of distributions.

**Force matching** (multiscale coarse-graining; [Izvekov and Voth 2005](cite:izvekov2005)). Choose the CG force field whose forces best match the atomistic forces projected onto the CG sites, minimising $\chi^2=\big\langle\sum_I|\mathbf F_I^{CG}(\mathbf M(\mathbf r))-\mathbf f_I(\mathbf r)|^2\big\rangle$. It can be shown ([Noid et al. 2008](cite:noid2008)) that, for a linear mapping in which each atom contributes to at most one site (the usual case; the paper's condition is slightly weaker), the force field that minimises $\chi^2$ over all possible force fields is the mean force, $\mathbf F^{CG}=-\nabla U_{CG}$, with $U_{CG}$ the many-body PMF.

<div class="legend" markdown="1">
- $\chi^2$ ("chi squared"): the misfit, a single number. It would be zero if the CG forces were equal to the reference forces in every frame.
- $\langle\ \rangle$: the average over all frames of the all-atom trajectory.
- $\sum_I$: a sum over all beads.
- $\mathbf f_I(\mathbf r)$: the atomistic force **projected** onto bead $I$. For a centre-of-mass mapping it is the sum of the all-atom forces on the atoms of bead $I$ in this frame.
- $\mathbf F_I^{CG}(\mathbf M(\mathbf r))$: the force that the CG force field gives on bead $I$ when the beads are placed at the mapped positions of the same frame.
- $|\ \ |^2$: the squared length of the difference between the two force vectors.
- $\mathbf F^{CG}=-\nabla U_{CG}$: the forces on all beads obtained as minus the gradient of the many-body PMF (the gradient is explained in Module 2).
</div>

<div class="box maths" markdown="1">
**Maths you need here: a least-squares fit.** To fit a model with adjustable numbers to data, define the misfit as the sum of the squared differences between model and data, and choose the numbers that make it smallest. Squaring makes every difference count as positive and penalises large errors more than small ones.

Example: fit the line $y=ax$ to the three points $(1,\ 2.1)$, $(2,\ 3.9)$ and $(3,\ 6.2)$. The misfit is $\chi^2(a)=\sum_n(y_n-ax_n)^2$, where $n$ numbers the points. At its minimum the derivative with respect to $a$ is zero: $-2\sum_nx_n(y_n-ax_n)=0$. Solving for $a$ gives $a=\sum_nx_ny_n\big/\sum_nx_n^2=28.5/14=2.04$.

A special case is used below. If the "model" is a single constant $c$ that has to stand for several scattered numbers, the least-squares answer is their mean. For the numbers 3, 5 and 10 the misfit $\sum_n(y_n-c)^2$ is smallest at $c=6$. More in the [toolbox](maths.html#fitting).
</div>

**Why the best fit is the mean force.** Many all-atom frames have nearly the same bead positions $\mathbf R$ and different forces on the beads, because the atoms inside and around the beads are arranged differently in each frame. A CG force field knows only $\mathbf R$, so it must answer with one force for all of these frames. By the special case in the box, the least-squares choice is their mean. The mean force on the beads at $\mathbf R$ is minus the gradient of the potential of mean force. Force matching and the boxed formula therefore aim at the same target from two sides.

The condition in the brackets of the paragraph is met by the centre-of-mass mapping above: each bead position is a weighted sum of atom positions (linear), and no atom is shared between two beads.

**In practice.** "All possible force fields" includes many-body ones. A practical CG force field is restricted, for example to pair forces described by a table of adjustable numbers. The minimum of $\chi^2$ within that family is the member closest to the mean force, and what it misses is the many-body part (consequence 2). When the forces depend linearly on the adjustable numbers, minimising $\chi^2$ is the same least-squares problem as in the box, with many unknowns instead of one.

#### Relative entropy

The fourth method compares the two probability distributions as wholes.

**Relative entropy** ([Shell 2008](cite:shell2008)). Minimise $S_{rel}=\sum_{\mathbf R}p_{AA}(\mathbf R)\ln\big[p_{AA}(\mathbf R)/p_{CG}(\mathbf R)\big]$, where $p_{AA}(\mathbf R)$ is the atomistic distribution mapped onto the CG coordinates. It measures how unlikely the atomistic configurations are under the CG model, it is zero only for a perfect match, and with a fully flexible potential its minimum is the many-body PMF.

On its own line:

$$
S_{rel}=\sum_{\mathbf R}p_{AA}(\mathbf R)\,\ln\frac{p_{AA}(\mathbf R)}{p_{CG}(\mathbf R)} .
$$

<div class="legend" markdown="1">
- $S_{rel}$: the relative entropy, a pure number with no unit. It measures the mismatch between two probability distributions.
- $\sum_{\mathbf R}$: a sum over all bead configurations. For continuous coordinates it is an integral.
- $p_{AA}(\mathbf R)$: the probability of the bead configuration $\mathbf R$ in the mapped all-atom simulation.
- $p_{CG}(\mathbf R)$: the probability of the same configuration in the CG model. It depends on the CG potential, which is what is being adjusted.
- $\ln\big[p_{AA}/p_{CG}\big]$: zero where the two agree, positive where the CG model gives $\mathbf R$ too little probability, negative where it gives too much.
</div>

Read it like this. Go through every bead configuration. Compare the probability that the all-atom simulation gives it with the probability that the CG model gives it, take the logarithm of the ratio, and average these logarithms with the all-atom probabilities as weights. Configurations that the all-atom system visits often count most. If the CG model considers such a configuration very unlikely ($p_{CG}$ small), the ratio is large and the penalty is heavy.

A two-configuration example. Let the all-atom probabilities be 0.8 and 0.2. A CG model that gives 0.5 and 0.5 has $S_{rel}=0.8\ln(0.8/0.5)+0.2\ln(0.2/0.5)=0.376-0.183=0.193$. A better model, which gives 0.7 and 0.3, has $S_{rel}=0.107-0.081=0.026$. The perfect model has $S_{rel}=0$, and it can be shown that $S_{rel}$ is never negative, so zero is the smallest value it can take.

**Why its minimum is the PMF.** $S_{rel}=0$ requires $p_{CG}=p_{AA}$ for every $\mathbf R$, and the derivation at the start of this section showed that this happens exactly when $U_{CG}$ is the many-body PMF. With a restricted potential (pair terms only) zero cannot be reached. The minimum is then the pair model whose overall distribution is closest to the atomistic one by this measure. In statistics the same quantity is called the Kullback-Leibler divergence. The word "entropy" is used because the formula is built like the statistical formula for an entropy, from terms of the form $p\ln p$.

### Top-down parameterisation

Fit the CG model directly to experimental data: partition free energies, densities, radii of gyration, phase behaviour. Martini and the residue-level models for disordered proteins are built this way.

Here the reference is one level *above* the model: measured, macroscopic numbers. You choose a simple functional form (for example a Lennard-Jones term between each pair of bead types), simulate, compare the result with experiment, and adjust the parameters until the two agree. The four kinds of data named above are these.

- **Partition free energy.** Shake a solute with water and an oily solvent that do not mix, and measure its concentration in each layer at equilibrium. The ratio of the two concentrations, the partition coefficient $K=c_{oil}/c_{water}$, gives the free energy of moving the solute from water to oil: $\Delta G=-k_BT\ln K$. If the solute is 100 times more concentrated in the oil, $\Delta G=-2.494\times\ln100=-11.5$ kJ/mol at 300 K. This one number says how hydrophobic a chemical group is.
- **Density.** The mass per volume of a liquid. It constrains the sizes of the beads.
- **Radius of gyration.** The root-mean-square distance of the parts of a molecule from its centre (Module 11), a measure of how expanded a chain is.
- **Phase behaviour.** The conditions (temperature, concentration) under which a mixture separates into two phases, for example a protein solution that forms dense droplets.

The two routes fail in different ways. A bottom-up model reproduces the all-atom simulation it was fitted to, including the errors of that simulation, and may not transfer. A top-down model reproduces the experimental numbers it was fitted to, and says little about anything that those numbers do not constrain: many different sets of parameters can give the same density. A model can mix the two routes, as Martini does (see below).

## Time, energy and temperature in a coarse-grained model

In an all-atom simulation you read three things off the output without a second thought: the time in nanoseconds, the energies in kJ/mol and the temperature in kelvin. In a CG model none of the three can be taken at face value. This short section says why. It applies to every model in the rest of the module.

- **Time.** Removing degrees of freedom removes friction and smooths the landscape, so CG dynamics are faster than real dynamics by a factor that is not constant across processes. Martini quotes a factor of about 4 for diffusion. For C$\alpha$ models run with low-friction Langevin dynamics, simulated time has no simple relation to real time. Use CG models for thermodynamics and mechanisms; treat time scales as qualitative unless calibrated.
- **Energy scale.** In top-down and structure-based models the interaction strength is a free parameter, often expressed in reduced units, and is calibrated against an experimental observable (a folding temperature, a binding constant, a radius of gyration).
- **Temperature.** For the same reason, the temperature of a structure-based model is a reduced temperature relative to its folding temperature, not Kelvin, unless the energy scale has been calibrated.

### Why coarse-grained time is not real time

Two things slow a real molecule down. One is **friction**: as it moves, it collides with solvent molecules and with its own neighbouring groups, and each collision takes away some of its directed motion (see the [primer](physics.html#diffusion)). The other is the roughness of the energy landscape: many small barriers that have to be crossed one after the other. Coarse-graining removes the particles that caused the collisions and averages the small barriers away. The beads therefore move faster than the groups of atoms they stand for.

The speed-up factor is different for each process, because each process loses a different share of its friction and of its barriers. A factor measured for one property (about 4 for diffusion in Martini) says nothing certain about another, such as the time a complex takes to dissociate. If a simulated microsecond of Martini is reported as "4 µs of effective time", that conversion holds for diffusion and is a guess for anything else.

**Langevin dynamics** (Module 8) moves the particles with an added friction force and random kicks that stand for the missing solvent. The strength of the friction is a number that the user sets. With a low value the chain explores its conformations quickly, which is the reason for choosing it, and the clock of the simulation then has no fixed relation to a real clock.

What survives is everything that does not depend on how fast the system moves. The equilibrium populations of states are fixed by the potential alone, through the Boltzmann factor. Free-energy differences, binding constants and average structures are therefore meaningful, and this is what "thermodynamics" means in the list above. The "mechanism" survives in the sense of which states exist and which lie between which. To **calibrate** a time scale means to compare one rate or one diffusion constant from the model with its experimental or all-atom value, and to rescale the simulated time by the ratio, for that process only.

### Reduced units, and how an energy scale is calibrated

A CG force field that was built top-down, or from a structure, has an overall energy unit that the model itself cannot fix. The reason is in the Boltzmann factor $e^{-U/k_BT}$: only the ratio $U/k_BT$ enters. Multiply every energy in the model by 2 and the temperature by 2, and every probability stays the same.

Such models are therefore written in **reduced units**. One energy of the model, usually the depth $\varepsilon$ of an attractive well, is taken as the unit. All energies are given as multiples of it, and the temperature is given as the ratio

$$
T^*=\frac{k_BT}{\varepsilon}.
$$

<div class="legend" markdown="1">
- $T^*$: the **reduced temperature**, a pure number. $T^*=1$ means that the thermal energy is equal to the well depth.
- $k_BT$: the thermal energy at the real temperature $T$, with $k_B=0.0083145$ kJ mol$^{-1}$ K$^{-1}$.
- $\varepsilon$: the energy unit of the model, the depth of one attractive contact. It has a value in kJ/mol only after calibration. It is an energy here, not a dielectric constant.
</div>

Read it like this. At low $T^*$ a contact is worth many $k_BT$ and stays formed. At high $T^*$ thermal motion breaks it at once.

To connect $T^*$ with kelvin you need one experimental number. Say a structure-based model shows its folding transition at $T^*=1.1$ and the real protein unfolds at 350 K (both numbers are illustrations). Setting the two equal gives $\varepsilon=k_B\times350\ \text{K}/1.1=2.65$ kJ/mol. A simulation at $T^*=1.0$ then corresponds to $350/1.1=318$ K, and room temperature (300 K) is $T^*=0.94$.

The calibration uses up the observable that it was fitted to. A model whose energy scale was set with the folding temperature cannot predict the folding temperature. A model whose scale was set with a binding constant cannot predict that binding constant. This is the meaning of the second and third points of the list.

Even after calibration, the temperature *dependence* of such a model is not reliable. By consequence 1 of the previous section the correct CG potential itself changes with temperature, and a fixed set of parameters does not.

## Martini

<div data-videos="Yq1f8vDfPe4 EVcw-w-Lcnk"></div>

Martini is a general-purpose CG force field: a fixed set of bead types from which lipids, proteins, sugars and other molecules are assembled, in the same way as an all-atom force field has a fixed set of atom types. Its central idea is that a small chemical group is described well enough by one property, how much it prefers water over oil. The force field is tuned so that each bead type has the right preference.

[Marrink et al. (2007)](cite:marrink2007); Martini 3 by [Souza et al. (2021)](cite:souza2021). Among the most widely used CG models for biomolecular systems, especially membranes.

The list of settings further down uses the Lennard-Jones potential of Module 5. As a reminder, it describes two particles that repel at short distance and attract weakly at longer distance:

$$
U_{LJ}(r)=4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right].
$$

<div class="legend" markdown="1">
- $r$: the distance between the two particles (here two beads), in nm.
- $\varepsilon$: the depth of the attractive well, in kJ/mol. A larger $\varepsilon$ means that the two beads attract more strongly. It is an energy here, not a dielectric constant.
- $\sigma$: the distance at which the energy passes through zero. It sets the size of the particles.
- $(\sigma/r)^{12}$: the repulsion, which rises steeply when the particles overlap.
- $(\sigma/r)^{6}$: the attraction.
- The factor 4: it makes the depth of the well exactly $\varepsilon$ (shown below).
- "12-6": the short name of this form, after the two exponents.
</div>

The minimum lies at $r=2^{1/6}\sigma=1.12\,\sigma$, where $U_{LJ}=-\varepsilon$. To check, set the [derivative](maths.html#derivative) of the bracket with respect to $r$ to zero: $-12\sigma^{12}/r^{13}+6\sigma^6/r^7=0$ gives $r^6=2\sigma^6$. At that distance $(\sigma/r)^6=\tfrac12$, so $U_{LJ}=4\varepsilon\,(\tfrac14-\tfrac12)=-\varepsilon$.

The settings of the model:

- **Mapping.** About four heavy atoms per bead (two to three for rings and small groups). One water bead represents four water molecules. Each amino acid is one backbone bead plus zero to four side-chain beads (five for tryptophan in Martini 3).
- **Bead types.** Chemical character is encoded in the type: charged (Q), polar (P), intermediate (N) and apolar (C), each with sub-levels, in three sizes in Martini 3 (regular, small, tiny). Martini 3 also has classes for halogens, divalent ions and water, and labels for hydrogen-bond donors and acceptors.
- **Interactions.** Lennard-Jones 12-6 between beads with $\varepsilon$ taken from a fixed interaction matrix of levels, a cutoff of 1.1 nm, and Coulomb interactions with reaction field and a relative dielectric constant of 15 (2.5 with the polarizable water model).
- **Parameterisation.** Top-down for non-bonded terms: reproduce experimental partitioning free energies between polar and apolar solvents. Bonded terms come from atomistic simulations.
- **Time step.** 20 fs.

### What each setting means

**Mapping.** By the four-to-one rule, a chain of four carbon atoms with its hydrogens is one bead, and four water molecules (twelve atoms) are one bead. A water bead has no orientation and makes no hydrogen bonds. A residue keeps one bead for its backbone and up to a few for its side chain, so the rough shape and chemical character of each side chain survive.

**Bead types and the interaction matrix.** Each bead carries a type, and the type is a statement about polarity, from charged (Q) through polar (P) and intermediate (N) to apolar (C). The **interaction matrix** is a table with one row and one column for each bead type. The entry for a pair of types is the Lennard-Jones $\varepsilon$ used between two such beads, chosen from a short list of fixed levels.

The well depth is what tells the levels of polarity apart. The table fixes how strongly each pair of bead types attracts, and with that which types mix and which separate, as oil separates from water. No special hydrophobic force is added: between neutral beads the Lennard-Jones term is the only non-bonded interaction.

The different bead sizes exist because rings and small groups cannot be cut into pieces of four heavy atoms. They are mapped with fewer atoms per bead, and a bead that stands for fewer atoms has to be smaller.

<div class="box physics" markdown="1">
**Physics you need here: the dielectric constant.** Two charges $q_i$ and $q_j$ at a distance $r$ in empty space have the Coulomb energy $q_iq_j/(4\pi\varepsilon_0r)$. The constant $\varepsilon_0$, the permittivity of vacuum, only fixes the units: with charges in units of the elementary charge $e$ and $r$ in nm, the energy is $138.935\,q_iq_j/r$ kJ/mol (Module 5). In a material the energy is smaller by a factor $\varepsilon_r$, the **relative dielectric constant** of the material:

$$
U_C(r)=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_r\,r}.
$$

The reason is that the molecules of the material respond to the charges. A water molecule is a small dipole, with a positive and a negative end. Around a positive charge the water molecules turn their negative ends towards it, and this layer of oriented dipoles cancels most of the charge as seen from a distance. The weakening of an interaction by charges or dipoles that rearrange around it is called **screening**.

Water screens strongly: $\varepsilon_r$ is about 78 at 25 °C. An oil, or the inside of a protein, screens weakly, with an $\varepsilon_r$ of a few units. Vacuum has $\varepsilon_r=1$.

Example: two opposite unit charges 1 nm apart have an energy of $-138.9$ kJ/mol in vacuum, $-9.3$ kJ/mol in a medium with $\varepsilon_r=15$, and $-1.8$ kJ/mol in water. In an all-atom simulation with explicit water there is no $\varepsilon_r$ in the formula, because the water molecules are present and do the screening themselves. A dielectric constant appears as soon as the water is simplified or removed. More in the [primer](physics.html#electrostatics).
</div>

**Interactions.** A **cutoff** of 1.1 nm means that two beads further apart than 1.1 nm do not interact at all (Module 7). **Reaction field** is the method of Module 7 for charges: inside the cutoff the Coulomb interaction is computed directly, and everything beyond the cutoff is treated as a uniform dielectric medium. Only charged beads have a Coulomb term, so most pairs interact through the Lennard-Jones term alone.

The relative dielectric constant of 15 is there because a plain water bead cannot do what real water does. It is a single neutral particle, so it cannot turn a dipole towards a charge and screen it. The screening is put in by hand, as a uniform $\varepsilon_r$ in Coulomb's law. The polarizable water model named in the list lets the water bead respond to charges to some extent, so less screening has to be added by hand.

**Parameterisation.** This is the top-down route, with the partition free energy of the previous section as the target: each bead type must prefer water or oil to the measured degree. The bonded terms (the bonds and angles that hold the beads of one molecule together) follow the bottom-up route and are set by comparison with atomistic simulations.

**Time step.** 20 fs is ten times the 2 fs of an all-atom simulation with constrained bonds (Module 9). It is possible because the beads are heavy and their interactions are soft, the third source of speed in the first section.

### What Martini cannot do for proteins

Limits for proteins: Martini cannot fold a protein or change its secondary structure. The secondary structure is an input, and the tertiary structure is held by an **elastic network** of harmonic springs between backbone beads within a cutoff, or by a Gō-like contact map (GōMartini). Martini 2 over-estimated protein-protein and protein-sugar attraction. Martini 3 was rebalanced, though later studies report that the stickiness of some systems and the compactness of disordered proteins still need case-by-case adjustment (for example by rescaling protein-water interactions).

**Secondary structure as an input.** The secondary structure of a protein (which stretches are helix, strand or coil) is held together by hydrogen bonds between backbone groups, and these bonds have a direction. One backbone bead per residue has no separate N-H and C=O groups, and so no directional hydrogen bonds. The model cannot decide by itself whether a stretch should be a helix. You tell it, and what you have told it stays fixed for the whole run.

**The elastic network.** The same holds one level up. The **tertiary structure**, the three-dimensional fold, is kept by an added device. In an elastic network, every pair of backbone beads that are closer than a cutoff distance in the starting structure is joined by a harmonic spring. The energy of one spring is $\tfrac12k\,(r-r_0)^2$, where $r$ is the present distance of the pair, $r_0$ its distance in the starting structure and $k$ the stiffness.

The springs let the protein fluctuate around its starting structure and pull it back from anything else. A large conformational change, unfolding, or folding upon binding cannot happen. A Gō-like contact map (next section) replaces the springs by contacts that can break and form again. That allows larger changes, but still only towards or away from the one known structure.

**Stickiness.** "Over-estimated attraction" means that proteins and sugars in the model associated more strongly than in experiments. A CG model knows the balance between protein-protein and protein-water attraction only through the numbers in its interaction matrix, and a small error per bead adds up over the many beads of an interface. The repair mentioned at the end, rescaling protein-water interactions, multiplies the $\varepsilon$ between protein beads and water beads by a common factor. A factor above 1 makes water hold on to the protein surface more strongly, so proteins have less to gain from touching each other, and a disordered chain becomes more expanded.

For any Martini study of protein association, ask how the interaction strength was checked for that system.

## Structure-based (Gō) models

<div data-videos="tRVeUbgcGVY AsKi8lXJWyM"></div>

Suppose you know the folded structure of a protein, or of a complex, and want to study how the chain gets there: in which order the parts come together, where the barrier is, what happens when you pull on it. An all-atom simulation of folding is out of reach for most proteins. A structure-based model makes the problem cheap by a drastic step. It writes the known structure into the energy function as the state of lowest energy. The model then knows where the chain will end up, and what you study is the route.

These models are also called Gō models, after one of the authors of the first model of this kind (cited below).

### The idea: only native contacts attract

**The physical idea.** Energy landscape theory holds that natural proteins are *minimally frustrated*: the interactions present in the native structure are mutually consistent and much more stabilising than random non-native ones, so the landscape is a funnel towards the native state. A structure-based model takes this to the limit: **only interactions present in the known native structure are attractive**. The model is defined by a structure, not by chemistry.

Some words in this paragraph need explaining. **Native** means "as in the folded, functional structure". A **native contact** is a pair of residues that are close together in that structure although they are not neighbours along the chain.

**Frustration** is a word for conflict between interactions: an interaction is frustrated when satisfying it prevents another favourable interaction from forming. A random sequence of amino acids has many such conflicts. It has many compact shapes of similar, mediocre energy, and it gets stuck in one or another of them. "Minimally frustrated" says that in a natural protein the native contacts can all be satisfied at once and are much more favourable than the alternatives.

The **funnel** is a picture of the resulting energy landscape. The unfolded state is the wide rim: many arrangements of the chain, few native contacts, high energy. As native contacts form, the energy goes down and the number of arrangements shrinks, down to the single native structure at the bottom. From almost anywhere on the rim, going downhill leads to the same place.

A structure-based model is a perfect funnel. It has no non-native attractions at all, so nothing competes with the native contacts. "Defined by a structure, not by chemistry" is meant literally: the input is a list of which residues touch, and in the simplest version two proteins with different sequences and the same fold give the same model. Such a model is called **native-centric**.

### The C$\alpha$ model, term by term

**The C$\alpha$ model** ([Clementi, Nymeyer and Onuchic 2000](cite:clementi2000)). One bead per residue at the C$\alpha$ position:

$$
\begin{aligned}
U={}&\sum_{bonds}K_r\,(r-r_0)^2+\sum_{angles}K_\theta\,(\theta-\theta_0)^2
+\sum_{dihedrals}K_\phi\Big\{\big[1-\cos(\phi-\phi_0)\big]+\tfrac12\big[1-\cos3(\phi-\phi_0)\big]\Big\}\\
&+\sum_{native\ contacts}\varepsilon\left[5\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12}-6\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{10}\right]
+\sum_{non\text{-}native}\varepsilon\left(\frac{\sigma_{rep}}{r_{ij}}\right)^{12}
\end{aligned}
$$

<div class="legend" markdown="1">
- $U$: the total potential energy of the chain.
- $\sum_{bonds}$: a sum over the bonds between consecutive beads. A chain of $N$ residues has $N-1$ of them.
- $r$, $r_0$: the present length of a bond and its length in the native structure (about 0.38 nm between consecutive C$\alpha$ atoms).
- $K_r$: the stiffness of the bonds. This formula has no factor $\tfrac12$, so $K_r$ is half the spring constant $k$ of the convention $\tfrac12k\,(r-r_0)^2$.
- $\sum_{angles}$, $\theta$, $\theta_0$, $K_\theta$: the same for the angle formed by three consecutive beads ($N-2$ angles): its present value, its native value and its stiffness.
- $\sum_{dihedrals}$, $\phi$, $\phi_0$, $K_\phi$: the same for the **dihedral angle** of four consecutive beads ($N-3$ of them). It is the angle by which the fourth bead is rotated about the line through the second and third, relative to the first. Here $\phi$ is an angle, not an electrostatic potential.
- $1-\cos(\phi-\phi_0)$ and $1-\cos3(\phi-\phi_0)$: two periodic terms. Each is zero, its lowest value, at the native angle. The second repeats three times per full turn and has half the weight.
- $\sum_{native\ contacts}$: a sum over the pairs of beads $i$, $j$ that are in contact in the native structure.
- $r_{ij}$: the present distance between beads $i$ and $j$.
- $\sigma_{ij}$: the distance between beads $i$ and $j$ in the native structure, a different number for every contact.
- $\varepsilon$: the energy of one native contact, the unit of energy of the model. It is an energy, not a dielectric constant.
- The numbers 5 and 6 and the powers 12 and 10: chosen so that the minimum of the contact term is at $r_{ij}=\sigma_{ij}$ and has the value $-\varepsilon$ (shown below).
- $\sum_{non\text{-}native}$: a sum over all remaining pairs, those that are neither bonded neighbours nor native contacts.
- $\sigma_{rep}$: the distance that sets the size of the repulsive core of a bead.
</div>

Read it like this. The first three sums are the **bonded terms**. They act along the chain and hold its local geometry near the native one: the bond lengths, the angle at each bead and the twist of each stretch of four beads. The fourth sum is the heart of the model, an attractive well for every native contact. The fifth says that two beads that are not supposed to touch only repel, so the chain cannot pass through itself.

In the native structure the bonded terms are exactly zero and every contact sits at the bottom of its well. The native structure is built to be the state of lowest energy.

**The dihedral term.** At the native angle both cosines are 1 and the term is zero. Half a turn away, at $\phi-\phi_0=180^\circ$, the first bracket is 2 and the second is also 2, so the term reaches its maximum, $K_\phi\,(2+\tfrac12\times2)=3K_\phi$.

**The 12-10 contact well.** At the native distance, $\sigma_{ij}/r_{ij}=1$ and the contact term is $\varepsilon\,(5-6)=-\varepsilon$. To see that this is the minimum, differentiate the contact term with respect to $r_{ij}$, using the rule that the derivative of $r^{-n}$ is $-n\,r^{-n-1}$:

$$
\frac{dU_{contact}}{dr_{ij}}=\frac{60\,\varepsilon}{r_{ij}}\left[\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{10}-\left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12}\right].
$$

<div class="legend" markdown="1">
- $U_{contact}$: the energy of one native contact, $\varepsilon\big[5(\sigma_{ij}/r_{ij})^{12}-6(\sigma_{ij}/r_{ij})^{10}\big]$.
- $dU_{contact}/dr_{ij}$: its slope. The force along the line that joins the two beads is minus this slope.
- 60: it comes from $5\times12$ and from $6\times10$.
- Other symbols: as in the list above.
</div>

The bracket is zero when the two powers are equal, which happens only at $r_{ij}=\sigma_{ij}$. At larger distances the bracket is positive: the energy rises as the beads separate, so they attract. At shorter distances it is negative and they repel. So in this formula $\sigma_{ij}$ is the position of the minimum, while in the Lennard-Jones formula $\sigma$ is the distance at which the energy is zero.

The well is narrow. At $r_{ij}=1.2\,\sigma_{ij}$ the energy is already back up to $-0.41\,\varepsilon$, and at $1.5\,\sigma_{ij}$ it is $-0.07\,\varepsilon$. A Lennard-Jones 12-6 well with the same minimum would still have $-0.56\,\varepsilon$ and $-0.17\,\varepsilon$ at these two distances. A Gō contact is therefore either formed or broken, with little in between, and it does not reach far.

Every reference value ($r_0$, $\theta_0$, $\phi_0$, $\sigma_{ij}$) is measured in the native structure. The 12-10 contact term has its minimum of depth $-\varepsilon$ exactly at the native distance $\sigma_{ij}$. Native contacts are found from the structure: with the CSU contact program in the original paper (pairs fewer than four residues apart are left out), with a distance cutoff or a shadow-map algorithm in later implementations. All other pairs only repel. In the original model every native contact has the same $\varepsilon$, with $K_r=100\varepsilon$, $K_\theta=20\varepsilon$, $K_\phi=\varepsilon$ and $\sigma_{rep}=0.4$ nm (the paper gives the non-native repulsion its own constant, which the formula above simply sets to $\varepsilon$), and energies and temperatures are in units of $\varepsilon$. The first model of this kind, the two-dimensional lattice model of [Taketomi, Ueda and Gō (1975)](cite:taketomi1975), also used one energy for all native pairs.

**How the native contacts are chosen.** The list of contacts is the main input of the model, and there is more than one way to make it. The original paper used a dedicated contact-analysis program (CSU). A **distance cutoff** calls two residues a contact when chosen atoms of the two are closer than a set distance. A **shadow map** also starts from a cutoff on the all-atom structure and then removes the pairs that have a third atom between them, which blocks the contact.

Pairs that are close along the chain are left out because the bonded terms already fix their distance. Different choices give somewhat different lists, so a paper should say which one was used.

**The parameters.** All native contacts have the same depth $\varepsilon$, and the three constants of the bonded terms are given as multiples of it. The dihedral constant multiplies a pure number, so $K_\phi=\varepsilon$ is complete as it stands: it is the same as the depth of one contact. $K_r$ and $K_\theta$ multiply a squared length and a squared angle, so they need a unit of length and a unit of angle as well, and the original paper states neither.

The paper gives its lengths in ångström (it quotes $\sigma_{rep}$ as 4 Å), which points to $K_r=100\,\varepsilon$ per Å$^2$ and $K_\theta=20\,\varepsilon$ per rad$^2$. This is a reading of the paper and is not stated in it, so check the units, and whether a factor $\tfrac12$ is included, in the program you use. With this reading the chain is stiff: at $k_BT=\varepsilon$ a bond length fluctuates by about 0.07 Å and an angle by about 9°.

Because everything is a multiple of $\varepsilon$, the model is in reduced units and its temperature is $T^*=k_BT/\varepsilon$, as in the section on time, energy and temperature. The repulsive distance $\sigma_{rep}=0.4$ nm is close to the distance between consecutive C$\alpha$ atoms.

A **lattice model**, in the last sentence, places the residues on the points of a regular grid instead of letting them move freely in space.

### Variants

**Variants.**

- **Sequence-dependent contact energies.** [Karanicolas and Brooks (2002)](cite:karanicolas2002) weight each side-chain native contact by its Miyazawa-Jernigan residue-pair energy (hydrogen-bond contacts keep one uniform strength) and use a contact potential with a small desolvation barrier,
  $U_{ij}=\varepsilon_{ij}\left[13(\sigma_{ij}/r)^{12}-18(\sigma_{ij}/r)^{10}+4(\sigma_{ij}/r)^6\right]$, together with sequence-dependent backbone dihedral terms. This puts some chemistry back.
- **All-atom structure-based models**: every heavy atom is a bead, contacts and dihedrals are native-centric. The SMOG 2 software builds these, the C$\alpha$ model above and several variants (in its implementation the contact strength and the non-native repulsion have separate constants).
- **Electrostatics.** Charged residues interact through a Debye-Hückel term (below), which adds non-native, sequence-dependent interactions and salt dependence.
- **Multi-basin models** combine the contact maps of two or more structures to simulate conformational change.

**The 12-10-6 contact potential.** On its own line, the contact term of the first variant is

$$
U_{ij}(r)=\varepsilon_{ij}\left[13\left(\frac{\sigma_{ij}}{r}\right)^{12}-18\left(\frac{\sigma_{ij}}{r}\right)^{10}+4\left(\frac{\sigma_{ij}}{r}\right)^{6}\right].
$$

<div class="legend" markdown="1">
- $U_{ij}(r)$: the energy of the native contact between residues $i$ and $j$ when they are a distance $r$ apart.
- $\varepsilon_{ij}$: the depth of the well of this contact, now a different number for each pair of residue types.
- $\sigma_{ij}$: the distance of the pair in the native structure.
- $r$: the present distance of the pair.
- 13, 18 and 4: chosen so that the minimum is still at $r=\sigma_{ij}$ with the value $-\varepsilon_{ij}$. At that distance the bracket is $13-18+4=-1$.
</div>

The new piece is the last term, $+4(\sigma_{ij}/r)^6$. It is positive and falls off slowly with distance, so outside the well the energy rises above zero before it returns to zero far away. At $r=1.5\,\sigma_{ij}$, for example, the 12-10-6 form gives $+0.14\,\varepsilon_{ij}$, where the 12-10 form gives $-0.07\,\varepsilon$. This bump is the **desolvation barrier**.

Its physical meaning: two residues that approach each other in water must push out the last layer of water molecules between them before they can touch. At a distance where a water molecule no longer fits and the residues are not yet in contact, the pair is worse off than either together or apart. Exercise 3 asks you to find the top of the barrier, and the demo in the section on implicit solvent plots the three contact potentials side by side.

**Sequence-dependent contact energies.** In the plain model a contact between two alanines and a contact between two tryptophans are worth the same $\varepsilon$. Weighting each contact by a residue-pair energy makes some contacts stronger than others, so that the sequence also influences which parts form first. The pair energies come from the statistical potential described further down. "Sequence-dependent backbone dihedral terms" are dihedral potentials that depend on which amino acids are involved.

**All-atom structure-based models** keep every heavy atom, so side chains have their real shape and must pack against each other. The energy function is still native-centric: it contains no chemistry beyond the native geometry.

**Electrostatics and multi-basin models** relax the rule "one structure, no chemistry" in two directions. Charges bring in an interaction that does not come from the native contact list, so two residues that never touch in the native structure can now attract or repel. A multi-basin model has two or more native structures, for example the open and the closed form of an enzyme, and its energy function has a minimum at each.

### Statistical contact potentials

**Statistical contact potentials.** The Miyazawa-Jernigan matrix gives an effective contact energy for each of the 210 residue pairs, derived from how often the pair is found in contact in known crystal structures (side-chain centres within 6.5 Å), compared with a reference state in which residues and solvent are randomly mixed, in the spirit of $e_{ij}\sim-k_BT\ln(\text{observed}/\text{expected})$. It is a knowledge-based potential of mean force, not a physical energy (the statistical basis of such potentials is debated, and they depend on the choice of reference state), and its values are dimensionless, in units of $RT$ (the authors take $RT=0.6$ kcal/mol).

<div class="legend" markdown="1">
- $e_{ij}$: the effective contact energy of residue types $i$ and $j$ (for example leucine with valine). Here $i$ and $j$ label amino-acid types, not positions in a chain, and $e$ is not the elementary charge.
- observed: how often the two types are found in contact in the set of known structures.
- expected: how often they would be in contact if residues had no preferences. Defining this number is the job of the **reference state**.
- $\sim$: the formula shows the form of the relation and leaves out details.
- $RT$: the thermal energy per mole, the same quantity as $k_BT$ in the per-mole units of this course. $R$ is the gas constant.
</div>

The number 210 comes from counting: 20 amino-acid types give 20 pairs of a type with itself and $20\times19/2=190$ pairs of two different types.

The logic is Boltzmann inversion applied to a database in place of a simulation. In a simulation, a configuration that is seen often has a low free energy. By analogy, a pair of residue types that is found in contact more often than chance would predict is given a favourable (negative) energy, and a pair found less often an unfavourable one. If a pair is seen twice as often as expected, the formula gives $-\ln2=-0.69$ in units of $RT$, about $-0.42$ kcal/mol with the authors' value of $RT$.

The words "knowledge-based" and "not a physical energy" are a warning. A set of crystal structures of different proteins is not one system in thermal equilibrium at one temperature, so the Boltzmann relation is used here by analogy only. The numbers also change when the reference state is defined differently. They are useful as relative weights, which is how the structure-based model above uses them. They should not be read as measured interaction energies.

### What a structure-based model can and cannot tell you

**What Gō models are good for.** Folding mechanisms, transition states and their dependence on topology (and, with sequence-weighted contacts, on sequence: the model of [Karanicolas and Brooks 2002](cite:karanicolas2002) reproduces the different folding routes of proteins L and G, which share one topology); coupled folding and binding of disordered proteins when the bound structure is known; mechanical unfolding; large conformational transitions. The fraction of native contacts $Q$ is the natural reaction coordinate and usually a good one.

The **topology** of a fold is its wiring: which parts of the chain are in contact with which, and how far apart they are along the sequence. A **transition state** is the set of conformations at the top of the free-energy barrier between unfolded and folded (Module 16). **Coupled folding and binding** is what many disordered proteins do: they have no fixed structure alone and take one up as they bind a partner. **Mechanical unfolding** means pulling the two ends of the chain apart. A **reaction coordinate** is a single number that measures how far a process has gone (Module 14).

The fraction of native contacts is

$$
Q=\frac{\text{number of native contacts formed in this frame}}{\text{total number of native contacts}} .
$$

<div class="legend" markdown="1">
- $Q$: the fraction of native contacts, between 0 (none formed) and 1 (all formed, the native state). It is not a charge and not a Martini bead type.
- "formed": the two beads of the contact are within a chosen tolerance of their native distance (Module 11).
</div>

$Q$ suits these models because of how they are built. Apart from the bonded terms, the energy goes down by about $\varepsilon$ for every native contact that forms, so $Q$ and the energy go together. In a real protein non-native contacts matter as well, and $Q$ is a less complete description.

All the items in the list are questions about how a chain reaches or leaves a known structure. The answer to such a question is dominated by the geometry of that structure, and the geometry is what the model contains.

**What they cannot do.** They cannot predict a structure, or any intermediate that depends on non-native contacts, because non-native attraction is absent by construction. Intermediates and kinetic traps built from native contacts alone can still appear. They do not give absolute stabilities or affinities: the energy scale is calibrated per system, and a model built from a predicted complex inherits every error of that prediction and will stabilise it regardless. Comparisons are most meaningful between closely related systems treated identically.

Each limit follows from the construction.

- **No structure prediction.** The structure is the input.
- **No non-native intermediates.** An **intermediate** is a partly folded state that lives long enough to be seen. A **kinetic trap** is a state that the chain enters easily and leaves slowly. A state held together by contacts that are absent from the native structure has no attraction in the model, so if the real folding route passes through such a state, or gets stuck in a misfolded one, the model does not show it. States built from a subset of the native contacts can appear.
- **No absolute stabilities or affinities.** The well depth $\varepsilon$ is not predicted. It is set for each system so that one observable matches (see reduced units above). After that the model cannot tell you, as an independent result, how stable the protein is or how tightly a complex binds.
- **No check of the input.** If the input structure is wrong, the model makes the wrong structure stable. A predicted complex with a wrongly placed partner gives a simulation in which the wrong pose is stable. Nothing in the output warns you.

What remains valid are comparisons: two variants of one protein, or two related complexes, built with the same contact definition, the same $\varepsilon$ and the same protocol. Errors that are common to both largely cancel in the difference.

## Residue-level models for disordered proteins and condensates

<div data-videos="jFmGNUUVHzg _6iAcwmknek"></div>

A disordered protein has no single folded structure. In solution it moves through a wide range of shapes. Many such proteins gather into liquid-like droplets called **condensates**, by a process called **phase separation**: above a certain concentration the solution splits into a dense phase that is rich in protein and a dilute phase. A structure-based model has nothing to work with here, because there is no list of native contacts. What is left to decide how the chain behaves is its sequence: where the sticky residues are and where the charges are.

For disordered proteins there is no native structure to encode. These models use one bead per residue, bonded by springs, with two non-bonded terms.

"Bonded by springs" means that consecutive beads are joined by a harmonic bond with the energy $\tfrac12k\,(r-r_0)^2$, where $r$ is the distance between the two beads, $r_0$ its preferred value and $k$ the stiffness. The chain is a flexible string of beads. Each bead has three properties: a size, a stickiness and a charge. The two **non-bonded** terms act between beads that are not bonded neighbours, within one chain and between different chains.

The first term is a Lennard-Jones potential (see the Martini section) with an adjustable amount of attraction. **Hydropathy** is a measure of how strongly a residue avoids water. It is high for an oily side chain such as that of leucine or phenylalanine and low for a charged or very polar one.

**Hydropathy-scaled Lennard-Jones** (Ashbaugh-Hatch form), where each residue has a "stickiness" $\lambda_i\in[0,1]$ and $\lambda=\tfrac12(\lambda_i+\lambda_j)$:

$$
U_{AH}(r)=\begin{cases}U_{LJ}(r)+(1-\lambda)\,\varepsilon, & r\le2^{1/6}\sigma\\[2pt]\lambda\,U_{LJ}(r), & r>2^{1/6}\sigma\end{cases}
$$

<div class="legend" markdown="1">
- $U_{AH}(r)$: the energy of two non-bonded beads at a distance $r$.
- $U_{LJ}(r)$: the Lennard-Jones function $4\varepsilon\big[(\sigma/r)^{12}-(\sigma/r)^6\big]$ of the Martini section.
- $\varepsilon$: the Lennard-Jones well depth, an energy. As written, it is one value for all pairs.
- $\sigma$: the Lennard-Jones size parameter of this pair of residues, a distance.
- $\lambda_i$, $\lambda_j$: the stickiness of residue $i$ and of residue $j$, numbers between 0 and 1 (this is what $\in[0,1]$ says). There is one value for each amino-acid type.
- $\lambda$: the stickiness of the pair, the average of the two. It is not the Debye length $\lambda_D$.
- $2^{1/6}\sigma$: the position of the Lennard-Jones minimum, $1.12\,\sigma$. It separates the repulsive side from the attractive side.
- The brace: the function is given by the upper line at short distance and by the lower line at long distance.
</div>

The repulsive force does not depend on $\lambda$ (the repulsive branch is only shifted in energy), and the depth of the attractive well is $\lambda\varepsilon$.

Check the two statements. First the repulsive force. The upper line adds the constant $(1-\lambda)\,\varepsilon$ to $U_{LJ}$. A constant shifts the energy and leaves the slope, and so the force, as it was.

Then the depth. At $r=2^{1/6}\sigma$ the Lennard-Jones energy is $-\varepsilon$. The upper line gives $-\varepsilon+(1-\lambda)\,\varepsilon=-\lambda\varepsilon$ and the lower line gives $\lambda\times(-\varepsilon)=-\lambda\varepsilon$. The two lines meet at the same energy. Both have zero slope there, so the potential and the force are continuous.

Three cases. With $\lambda=1$ the formula is the plain Lennard-Jones potential with its full well depth $\varepsilon$. With $\lambda=0$ the lower line is zero and the upper line is $U_{LJ}+\varepsilon$, which falls to zero at $2^{1/6}\sigma$: the two beads only repel, like two soft balls. In between, the well depth is the fraction $\lambda$ of $\varepsilon$.

An example with $\varepsilon=1$ kJ/mol (a round number for illustration): a residue with $\lambda_i=0.9$ and one with $\lambda_j=0.3$ have $\lambda=0.6$ and a well of 0.6 kJ/mol, while two residues with $\lambda=0.9$ have a well of 0.9 kJ/mol. The behaviour of a chain comes from the sum of very many such pair contacts, within the chain and between chains.

**Screened electrostatics** (Debye-Hückel) between charged residues.

The second term acts between residues that carry a charge at neutral pH: negative for aspartate and glutamate, positive for lysine and arginine (histidine is only partly charged near neutral pH, so each model has to make a choice for it). Its formula, $U_{DH}$, is explained in the next section, where it belongs with the other implicit-solvent terms. In short, it is Coulomb's law in water multiplied by a factor that makes the interaction die away within about a nanometre at the salt concentration of a cell.

In the HPS model ([Dignon et al. 2018](cite:dignon2018)) the $\lambda$ values come from a hydrophobicity scale. In CALVADOS ([Tesei et al. 2021](cite:tesei2021) and later versions) they are optimised against SAXS and paramagnetic relaxation data for many disordered proteins. These models reproduce radii of gyration (in CALVADOS these are training data, so the independent tests are its predictions for pairs of chains and for phase separation), and qualitative trends in the tendency to phase-separate, from sequence alone, at a cost that allows a hundred or more chains. Absolute transition temperatures are not reliable ([Dignon et al. 2018](cite:dignon2018)). In [Tesei et al. (2021)](cite:tesei2021), for example, the saturation concentrations matched experiments done near 24 °C only when the model was simulated at 50 °C.

**Where the $\lambda$ values come from.** A **hydrophobicity scale** is a table that gives each of the 20 amino acids one number for how strongly it prefers an oily environment to water. Rescaled to run from 0 to 1, such a table can be used directly as the set of $\lambda$ values. The other route treats the 20 values as adjustable and fits them: simulate many disordered proteins, compare with measurements, change the $\lambda$ values, and repeat.

**The experiments.** **SAXS** (small-angle X-ray scattering) gives the average size of a protein in solution, as the radius of gyration $R_g$. **Paramagnetic relaxation** experiments are NMR measurements in which a label attached to one residue reports which other residues come close to it, in the same chain or in another chain.

**Training data and tests.** A model reproduces what it was fitted to, and that agreement proves little. This is why the paragraph separates the radii of gyration, which were used in the fit, from the predictions for pairs of chains and for phase separation, which were not. Only the second kind is a test.

**Phase separation in a simulation.** With a hundred or more chains in one box, the chains can gather into a dense region that coexists with a dilute one. The concentration of the dilute phase is the **saturation concentration**: the protein concentration above which droplets form. A low saturation concentration means a strong tendency to phase-separate. A **transition temperature** is a temperature at which the two phases stop being distinct.

**Why the temperatures are off.** What follows is this course's reading of the last two sentences of the paragraph, in the light of the first sections. It is not a result quoted from the papers. The $\lambda$ values stand for free energies of interaction, and they were fitted at particular conditions. One plausible reading of the 24 °C and 50 °C result is that the stickiness of real residues changes with temperature in a way that fixed $\lambda$ values do not follow (consequence 1). The temperature axis of the model would then be shifted relative to the real one.

The HPS paper points the same way for its own model. Its authors write that making the absolute temperature comparable with experiment would need an added solvation energy term that depends on temperature, and more comparison with experimental data. Trends across sequences at one condition (this sequence phase-separates more readily than that one) are safer than a transition temperature in kelvin.

## Implicit solvent

<div data-videos="2yf__V4EhGI AzCzDYLimvc"></div>

Replace the water by its average effect on the solute.

In the models so far the water was grouped into beads (Martini) or left out without comment (Gō and residue-level models). This section looks at what "leaving out the water" means and what has to be put in its place.

The idea is that of the section on the CG potential, with one particular mapping: keep every coordinate of the solute and drop every coordinate of the solvent. The exact effective energy of the solute is then again a potential of mean force. It is the solute's own energy plus the free energy of the water and ions that arrange themselves around it. Implicit-solvent models are formulas that approximate this second part.

Water does three things to a solute that the formulas must imitate:

1. it weakens the electrostatic interactions between the charges of the solute, and it stabilises each charge by itself (dielectric screening and solvation);
2. the salt dissolved in it weakens electrostatic interactions further, and over a shorter range (screening by ions);
3. it resists the creation of the cavity that the solute occupies, and it attracts the solute weakly through dispersion (the non-polar part, which includes the hydrophobic effect).

Debye-Hückel covers the screening in points 1 and 2 in the simplest way, and leaves out the stabilisation of each charge by itself. Poisson-Boltzmann covers them with the true shape of the solute. Generalised Born is a fast approximation to that. A surface-area term covers point 3.

Debye-Hückel and generalised Born are the formulas you will meet in simulation input files. The part on Poisson-Boltzmann explains where they come from and can be read more lightly the first time.

All of these are **mean-field**, or **continuum**, descriptions. The water is no longer made of molecules. It is a featureless medium with a dielectric constant (see the physics box in the Martini section), and the ions are a smooth cloud of charge that takes its average shape at once. Fluctuations are gone, and so is anything that depends on one particular water molecule or ion.

### Screening by salt: Debye-Hückel

Put a positive charge into salt water. The negative ions of the salt are attracted to it and the positive ions are pushed away. Thermal motion keeps them from piling up on the charge, so the result is a diffuse cloud around it in which negative ions are slightly in excess.

Seen from outside the cloud, the charge and its cloud nearly cancel. A second charge feels the first one at full strength only if it is well inside the cloud. The thickness of the cloud is the **Debye length**, $\lambda_D$.

The ions that matter are counted by the **ionic strength**, $I=\tfrac12\sum_sc_sz_s^2$. The sum runs over the kinds of ion $s$ in the solution, $c_s$ is the concentration of each kind in mol/L (M) and $z_s$ is its charge in units of the elementary charge. For 150 mM NaCl, $I=\tfrac12(0.15\times1^2+0.15\times1^2)=0.15$ M. Doubly charged ions count four times: 50 mM MgCl$_2$ has $I=\tfrac12(0.05\times2^2+0.10\times1^2)=0.15$ M as well.

**Debye-Hückel.** In a salt solution, mobile ions screen electrostatic interactions. Linearising the Poisson-Boltzmann equation around a point charge gives

$$
U_{DH}(r)=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_r\,r}\,e^{-r/\lambda_D},\qquad
\lambda_D=\sqrt{\frac{\varepsilon_0\varepsilon_rk_BT}{2N_Ae^2I}}\approx\frac{0.304}{\sqrt{I\,[\text{M}]}}\ \text{nm (water, 25 °C)},
$$

with $I$ the ionic strength.

<div class="legend" markdown="1">
- $U_{DH}(r)$: the Debye-Hückel energy of two charges at a distance $r$ in salt water.
- $q_i$, $q_j$: the two charges. They are charges here, not coordinates.
- $r$: the distance between them, in nm.
- $\varepsilon_0$: the permittivity of vacuum, a constant that fixes the units: $1/(4\pi\varepsilon_0)=138.935$ kJ mol$^{-1}$ nm $e^{-2}$.
- $\varepsilon_r$: the relative dielectric constant of the solvent, about 78 for water at 25 °C.
- $e^{-r/\lambda_D}$: the screening factor from the ions, between 1 (no screening) and 0. Here $e$ is the base of the exponential.
- $\lambda_D$: the Debye length, the distance over which the screening factor falls by a factor $e\approx2.7$.
- $k_BT$: the thermal energy.
- $N_A$: Avogadro's number, $6.022\times10^{23}$ per mole. It converts moles of ions into numbers of ions.
- $e^2$ under the square root: the square of the elementary charge (the charge of a proton). It is a different $e$ from the one in the exponential.
- $I$: the ionic strength, not a bead label. In the short form, $I\,[\text{M}]$ is the number you get when $I$ is expressed in mol/L.
- Units in the square-root formula: it gives $\lambda_D$ in metres when everything under the root is in SI units. That means $\varepsilon_0=8.854\times10^{-12}$ C$^2$ J$^{-1}$ m$^{-1}$, $k_BT=4.116\times10^{-21}$ J at 25 °C, $e=1.602\times10^{-19}$ C and $I$ in mol/m$^3$ (1 mol/L is 1000 mol/m$^3$). The value of $1/(4\pi\varepsilon_0)$ in kJ mol$^{-1}$ nm $e^{-2}$ given above belongs to the first formula only.
- $\approx$ and "(water, 25 °C)": the short form has the constants for water at 25 °C already filled in.
</div>

Read it like this. The first factor is Coulomb's law in water, already 78 times weaker than in vacuum. The second factor is the effect of the salt.

At distances much shorter than $\lambda_D$ the second factor is close to 1, and the charges interact as in pure water. At $r=\lambda_D$ it is $1/e=0.37$, and at $r=3\lambda_D$ it is 0.05. The square-root formula says what makes the cloud thin: $\lambda_D$ falls as $1/\sqrt{I}$, so four times more salt halves it.

The number 0.304 is what the square root gives for water at 25 °C ($\varepsilon_r=78.4$) and $I=1$ mol/L. For other salt concentrations, divide by $\sqrt{I}$:

| Ionic strength | Debye length $\lambda_D$ |
|---|---|
| 10 mM | 3.04 nm |
| 50 mM | 1.36 nm |
| 150 mM | 0.79 nm |
| 500 mM | 0.43 nm |
| 1 M | 0.30 nm |

At 150 mM, $\lambda_D$ = 0.79 nm. The arithmetic: $0.304/\sqrt{0.15}=0.304/0.387=0.785$ nm. That is the width of about three water molecules, so at the salt concentration of a cell, charges on a protein feel each other only at short range.

A worked example: two opposite unit charges 1 nm apart at 150 mM. Coulomb's law in water gives $-138.935/(78\times1)=-1.78$ kJ/mol. The screening factor is $e^{-1/0.785}=0.28$. So $U_{DH}=-0.50$ kJ/mol, a fifth of $k_BT$. At 0.5 nm the same pair has $-3.56\times0.53=-1.9$ kJ/mol.

The formula follows from the Poisson-Boltzmann equation below, by the approximation called linearising. The derivation is in an optional block after that equation.

Assumptions: weak potentials (the linearisation fails near highly charged groups), point ions, and a uniform dielectric constant, which is far from true at a protein interface where water is excluded. It contains no desolvation penalty.

- **Weak potentials.** The derivation assumes that the electrostatic energy of an ion is small compared with $k_BT$ everywhere. Far from a single charge that is true. At 0.3 nm from a unit charge in water, the energy of a second unit charge is $138.935/(78\times0.3)=5.9$ kJ/mol, more than twice $k_BT$. So close to a charged group, and all around a highly charged molecule, the assumption fails.
- **Point ions.** The ions have no size in the theory, so nothing stops the cloud from being denser near the charge than real ions could pack.
- **Uniform dielectric constant.** The formula uses one $\varepsilon_r$, that of water, everywhere. Where two proteins touch, the water has been pushed out, and the space between two charges is filled with protein, which screens far less. The true interaction there can be several times stronger than the formula says.
- **No desolvation penalty.** A charge in water is strongly stabilised by the water around it (the Born energy, in the part on generalised Born below). When a charged group is buried at an interface it loses part of that water, and this costs free energy whether or not an opposite charge is waiting there. A formula that depends only on the distance between two charges has no place for a cost that belongs to one charge and its surroundings.

The word "mean field" can be made concrete here. At 150 mM there are 0.18 ions per nm$^3$, and a sphere of radius $\lambda_D$ has a volume of 2.0 nm$^3$, so it holds 0.4 ions on average. The "cloud" is an average over time. It is not a crowd of ions that is present at every instant.

The demo shows both kinds of term from this module. On the left are three contact potentials with the same minimum and depth: Lennard-Jones 12-6, the Gō 12-10 form and the 12-10-6 form with its desolvation barrier. On the right is the Debye-Hückel energy of two opposite unit charges, in units of $k_BT$, with sliders for the ionic strength and the dielectric constant. It also prints the **Bjerrum length**, the distance at which two unit charges in the medium have an interaction energy of exactly $k_BT$. In water at room temperature it is 0.71 nm.

<div class="widget" data-widget="cgpot"></div>

### The continuum picture in full: Poisson-Boltzmann

Debye-Hückel treats the solute as point charges in uniform water. The Poisson-Boltzmann (PB) equation keeps the same two ingredients, a dielectric medium and a cloud of ions, and adds the shape of the solute: a region of low dielectric constant, from which water and ions are excluded, inside a medium of high dielectric constant.

It is an equation for the **electrostatic potential** $\phi(\mathbf r)$. The potential at a point is the energy that a unit charge would have if it were placed there, so a charge $q$ at the point $\mathbf r$ has the energy $q\,\phi(\mathbf r)$ (see the [primer](physics.html#electrostatics)). Once $\phi$ is known everywhere, the electrostatic part of the solvation free energy can be computed from its values at the charges of the solute.

The equation combines two statements, which give it its name.

- **Poisson.** Charges are the sources of the potential. The left-hand side of the equation measures how the potential bends around a point, and it is equal to minus the charge density at that point. It is Coulomb's law rewritten for a medium whose dielectric constant changes from place to place.
- **Boltzmann.** The mobile ions are not fixed. Each kind of ion is found at a place with a probability given by the Boltzmann factor of its energy there, $e^{-q_i\phi/k_BT}$. Positive ions gather where the potential is negative and avoid places where it is positive.

The potential decides where the ions go, and the ions are charges that change the potential. The equation has to be satisfied by both at once.

**Poisson-Boltzmann.** The full continuum treatment solves, for a solute with low dielectric constant inside and high outside,

$$
\nabla\cdot\big[\varepsilon(\mathbf r)\nabla\phi(\mathbf r)\big]=-\rho_{solute}(\mathbf r)-\sum_ic_i^\infty q_i\,e^{-\beta q_i\phi(\mathbf r)} .
$$

<div class="legend" markdown="1">
- $\phi(\mathbf r)$: the electrostatic potential at the point $\mathbf r$, the unknown of the equation. It is not a dihedral angle here, and this $\mathbf r$ is one point in space, not the list of all atom positions.
- $\nabla\phi$: the gradient of the potential (Module 2, and the [toolbox](maths.html#gradient)). Minus the gradient is the electric field.
- $\varepsilon(\mathbf r)$: the dielectric constant at the point $\mathbf r$, with the factor $\varepsilon_0$ included. It is low inside the solute and high in the water.
- $\nabla\cdot[\ \ ]$: the divergence (Module 2, and the [toolbox](maths.html#divergence)), which measures how much the quantity in the bracket spreads out from a point.
- $\rho_{solute}(\mathbf r)$: the charge density of the solute, charge per volume. It is built from the partial charges of the solute atoms.
- $\sum_i$: a sum over the kinds of mobile ion, for NaCl the ions Na$^+$ and Cl$^-$. Here $i$ labels kinds of ion, not atoms.
- $c_i^\infty$: the concentration (number per volume) of ions of kind $i$ far from the solute, where $\phi=0$. The superscript $\infty$ means "far away".
- $q_i$: the charge of one ion of kind $i$.
- $e^{-\beta q_i\phi(\mathbf r)}$: the Boltzmann factor of an ion of charge $q_i$ at a place where the potential is $\phi$, with $\beta=1/k_BT$.
</div>

Read it like this. The right-hand side is minus the total charge density at each point: the fixed charges of the solute, plus the mobile ions, whose local concentration is the far-away concentration times the Boltzmann factor. Where $\phi=0$ the Boltzmann factors are 1 and the ion charges add up to zero, because the solution as a whole is neutral. Near a positively charged patch of the solute $\phi>0$, so negative ions ($q_i<0$) have a factor above 1 and positive ions a factor below 1. A net negative cloud forms there, as in the Debye-Hückel picture.

One thing the equation as written does not show: the ion term belongs only to the region that the ions can reach. Inside the solute there are no mobile ions, and in the full equation the ion term is multiplied by a function that is 1 in the solvent and 0 inside the solute.

The unknown $\phi$ appears on the left and also inside the exponentials on the right, and this is what makes the equation hard to solve.

Accurate within the continuum picture, but too slow to solve at every MD step.

"Within the continuum picture" means that it is the best answer you can get once you have agreed to treat water as a structureless dielectric and the ions as a smooth cloud. It does not repair what that picture leaves out. For a molecule of realistic shape the equation is solved numerically: space is divided into a fine three-dimensional grid, and the value of $\phi$ at every grid point is adjusted until the equation holds. That takes far longer than one force evaluation with a force field, and MD needs the forces at every one of millions of steps. A faster approximation is needed during the dynamics.

<details markdown="1"><summary>Optional: from Poisson-Boltzmann to Debye-Hückel and the Debye length</summary>
The Debye-Hückel formula is the solution of the PB equation in the simplest case: one point charge, a uniform dielectric constant and a weak potential. Five steps.

**Step 1, uniform dielectric.** Set $\varepsilon(\mathbf r)=\varepsilon_0\varepsilon_r$ everywhere. A constant can be taken out of the divergence, and the divergence of a gradient is the Laplacian $\nabla^2$ (see the [toolbox](maths.html#divergence)):

$$
\varepsilon_0\varepsilon_r\nabla^2\phi=-\rho_{solute}-\sum_ic_i^\infty q_i\,e^{-\beta q_i\phi} .
$$

**Step 2, linearise.** If $\beta q_i\phi$ is much smaller than 1, the exponential can be replaced by the first two terms of its [Taylor expansion](maths.html#taylor), $e^{-x}\approx1-x$. The sum over the ions becomes $\sum_ic_i^\infty q_i-\beta\phi\sum_ic_i^\infty q_i^2$.

**Step 3, use neutrality.** The first sum is the total charge density of the ions far from the solute, which is zero. Only the second sum is left. Outside the solute charge, where $\rho_{solute}=0$, the equation is now

$$
\nabla^2\phi=\frac{\phi}{\lambda_D^2},\qquad\frac{1}{\lambda_D^2}=\frac{\sum_ic_i^\infty q_i^2}{\varepsilon_0\varepsilon_rk_BT} .
$$

The combination of constants on the right has the unit of one over a length squared, and this defines the Debye length.

**Step 4, rewrite with the ionic strength.** An ion of kind $i$ has the charge $q_i=z_ie$, and its number density is $c_i^\infty=N_AC_i$, where $C_i$ is its concentration in mol/m$^3$. Then $\sum_ic_i^\infty q_i^2=N_Ae^2\sum_iC_iz_i^2=2N_Ae^2I$, because $I=\tfrac12\sum_iC_iz_i^2$. Putting this in gives $\lambda_D=\sqrt{\varepsilon_0\varepsilon_rk_BT/(2N_Ae^2I)}$, the formula in the text.

**Step 5, solve for a point charge.** For a potential that depends only on the distance $r$ from the charge, the Laplacian is $\nabla^2\phi=\frac1r\frac{d^2(r\phi)}{dr^2}$. Try $r\phi=A\,e^{-r/\lambda_D}$ with a constant $A$. Differentiating twice gives $A\,e^{-r/\lambda_D}/\lambda_D^2$, so $\nabla^2\phi=\phi/\lambda_D^2$: the equation is satisfied. Very close to the charge the ions have had no room to screen it, so there the potential must be the Coulomb potential in water, which fixes $A=q_i/(4\pi\varepsilon_0\varepsilon_r)$. The potential of charge $q_i$ is therefore $\phi(r)=\dfrac{q_i}{4\pi\varepsilon_0\varepsilon_r\,r}\,e^{-r/\lambda_D}$, and a second charge $q_j$ at the distance $r$ has the energy $q_j\,\phi(r)=U_{DH}(r)$.
</details>

### A fast approximation: generalised Born

Generalised Born (GB) replaces the numerical solution by a formula that can be evaluated for every pair of atoms at every step. It starts from the one case in which the continuum problem has a short exact answer, a single spherical ion, and stretches that answer to cover a molecule.

<div class="box physics" markdown="1">
**Physics you need here: the Born energy of an ion.** Model an ion as a sphere of radius $R$ that carries a charge $q$, in a medium with relative dielectric constant $\varepsilon_r$. Building up the charge costs work, because each new bit of charge is repelled by the charge that is already there. When the sphere carries a charge $q'$, the potential at its surface is $q'/(4\pi\varepsilon_0\varepsilon_rR)$, and adding a small amount $dq'$ costs that potential times $dq'$. Adding up from 0 to $q$ gives the charging energy $q^2/(8\pi\varepsilon_0\varepsilon_rR)$. The 8 in place of the 4 is the factor $\tfrac12$ from $\int_0^qq'\,dq'=\tfrac12q^2$.

The charging energy is smaller in a medium with a larger $\varepsilon_r$. Moving the ion from a medium with $\varepsilon_{in}$ to one with $\varepsilon_{out}$ therefore changes its free energy by

$$
\Delta G_{Born}=-\frac{q^2}{8\pi\varepsilon_0R}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right).
$$

This is the **Born formula**. For a unit charge of radius 0.2 nm that goes from vacuum ($\varepsilon_{in}=1$) to water ($\varepsilon_{out}=78$) it gives $-\tfrac12\times(138.935/0.2)\times(1-1/78)=-343$ kJ/mol. Two things to remember: the solvation of a charge is very favourable, more than a hundred times $k_BT$, and it is stronger for a small ion than for a large one, because the water comes closer to the charge. More in the [primer](physics.html#electrostatics).
</div>

**Generalised Born** ([Still et al. 1990](cite:still1990)). A fast approximation to the Poisson solution. The pair function below is Still's; in the 1990 paper the Born radii were still computed numerically, and analytical recipes for them came later:

$$
\Delta G_{pol}=-\frac{1}{8\pi\varepsilon_0}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right)\sum_{i,j}\frac{q_iq_j}{f_{GB}},\qquad
f_{GB}=\sqrt{r_{ij}^2+R_iR_j\exp\left(-\frac{r_{ij}^2}{4R_iR_j}\right)} .
$$

<div class="legend" markdown="1">
- $\Delta G_{pol}$: the polar (electrostatic) part of the solvation free energy of the whole molecule. It is the change in free energy when the surroundings of the molecule are switched from a medium with dielectric constant $\varepsilon_{in}$ to the solvent.
- $\varepsilon_0$: the permittivity of vacuum. $1/(8\pi\varepsilon_0)$ is half of 138.935 kJ mol$^{-1}$ nm $e^{-2}$.
- $\varepsilon_{in}$: the relative dielectric constant assigned to the inside of the solute, a low number.
- $\varepsilon_{out}$: the relative dielectric constant of the solvent, about 78 for water.
- $\sum_{i,j}$: a sum over all ordered pairs of solute atoms. It includes $i=j$ (each atom with itself), and it contains every pair of different atoms twice, as $(i,j)$ and as $(j,i)$.
- $q_i$, $q_j$: the partial charges of atoms $i$ and $j$.
- $r_{ij}$: the distance between atoms $i$ and $j$. For $i=j$ it is zero.
- $R_i$, $R_j$: the effective Born radii of the two atoms, in nm (explained below). They are not bead positions.
- $f_{GB}$: a quantity with the unit of length that takes the place of the distance in Coulomb's law. It goes smoothly from the Born radius at $r_{ij}=0$ to $r_{ij}$ at large separation.
- $\exp(\ )$: the exponential function, written this way because its argument is long.
</div>

"The Poisson solution" is the solution of the PB equation without the ion term: the formula contains the dielectric response of the water and no salt.

$R_i$ is the effective **Born radius** of atom $i$, a measure of how deeply it is buried.

For an ion alone in water, $R_i$ is close to the radius of the ion itself. An atom inside a molecule is different. The other atoms of the molecule occupy space that would otherwise be water, so the water is on average further from the charge and solvates it less.

The effective Born radius expresses this with one number: it is the radius that a lone spherical ion would need in order to have the same solvation free energy as atom $i$ has at its place in the molecule. An atom at the surface has a small $R_i$, not much larger than its own atomic radius. An atom deep inside a protein has a much larger one. The radii depend on the conformation and must be computed again as the molecule moves.

For $i=j$ the term reduces to the Born formula for the solvation of an ion of radius $R_i$.

To check, put $r_{ij}=0$ and $R_j=R_i$ into $f_{GB}$. The exponential is $e^0=1$, so $f_{GB}=\sqrt{0+R_i^2}=R_i$. The term of the sum is then $-\frac{1}{8\pi\varepsilon_0}\big(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\big)\frac{q_i^2}{R_i}$, which is the Born formula of the box. These **self terms** are the desolvation penalty that the Debye-Hückel formula lacks. When a charged atom becomes buried, its $R_i$ grows, its self term becomes less negative, and the free energy goes up.

For distant atoms, the GB pair term added to the direct Coulomb interaction (computed with $\varepsilon_{in}$) gives Coulomb's law with the solvent dielectric constant.

The steps: for two different atoms far apart, $r_{ij}^2$ is much larger than $R_iR_j$ and the exponential is close to zero, so $f_{GB}\approx r_{ij}$. The pair appears twice in the sum, which turns the $8\pi$ into $4\pi$. The force field of the solute supplies the direct Coulomb interaction of the two charges in a medium of dielectric constant $\varepsilon_{in}$. Adding the two:

$$
\underbrace{\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_{in}\,r_{ij}}}_{\text{direct Coulomb}}\;\underbrace{-\,\frac{q_iq_j}{4\pi\varepsilon_0\,r_{ij}}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right)}_{\text{GB pair term with }f_{GB}=r_{ij}}=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_{out}\,r_{ij}} .
$$

<div class="legend" markdown="1">
- The braces underneath only name the two parts. They are not part of the formula.
- Other symbols: as in the list above.
</div>

The two terms with $1/\varepsilon_{in}$ cancel, and what is left is Coulomb's law in the solvent. Two exposed charges far apart interact as weakly as they would in water, as they should.

Between the two limits, $f_{GB}$ interpolates. For two atoms that are close together and both deeply buried (large $R_iR_j$), $f_{GB}$ stays well above $r_{ij}$. The GB term then cancels only a part of the direct interaction, and the pair interacts strongly, as two charges inside a protein should. An illustration with $\varepsilon_{in}=1$ and $\varepsilon_{out}=78$: two unit charges 0.5 nm apart have an interaction energy of magnitude 4.3 kJ/mol if both have $R=0.15$ nm (exposed), and 152 kJ/mol if both have $R=1.0$ nm (buried). Coulomb's law gives 278 kJ/mol in vacuum and 3.6 kJ/mol in water for the same pair.

A non-polar term proportional to the solvent-accessible surface area, $\gamma\cdot\mathrm{SASA}$, is added for cavity formation and dispersion (GB/SA).

$\Delta G_{pol}$ is only the electrostatic part. A solute with no charges at all still changes the free energy of the water. The water has to make room for it (**cavity formation**, the origin of the hydrophobic effect, see the [primer](physics.html#intermolecular)), and the solute and the water attract each other weakly through dispersion (the attractive part of the Lennard-Jones interaction, Module 5). Both effects grow roughly in proportion to the area of contact between solute and water.

The **solvent-accessible surface area** (SASA) measures that area: roll a sphere of the size of a water molecule over the solute, and take the surface traced out by the centre of the sphere. The coefficient $\gamma$ is an empirical energy per area. It is not the friction coefficient of Langevin dynamics.

With, say, $\gamma=2$ kJ mol$^{-1}$ nm$^{-2}$ as an illustration, two non-polar surfaces that come together and hide 5 nm$^2$ from the water gain 10 kJ/mol. This is how an implicit-solvent model produces hydrophobic association without any water molecules. The complete effective energy of a GB/SA model is the sum of three parts:

$$
U_{eff}=U_{solute}+\Delta G_{pol}+\gamma\cdot\mathrm{SASA}.
$$

<div class="legend" markdown="1">
- $U_{eff}$: the effective energy that drives the solute in the implicit-solvent simulation. It approximates the potential of mean force of the solute with the solvent averaged out.
- $U_{solute}$: the ordinary force-field energy of the solute atoms alone, with their Coulomb interactions computed with $\varepsilon_{in}$.
- $\Delta G_{pol}$: the generalised Born term above.
- $\gamma$: the non-polar coefficient, an energy per area, in kJ mol$^{-1}$ nm$^{-2}$.
- SASA: the solvent-accessible surface area of the solute in its present conformation, in nm$^2$.
</div>

All three parts depend on the conformation, and the forces on the solute atoms are minus the gradient of the sum.

Implicit solvent removes the cost of water and the viscosity that slows conformational change. It loses specific water molecules (bridging waters, the structure of the first hydration shell), and tends to over-stabilise salt bridges and helices, depending on the variant.

The first sentence names two gains. The cost: the water was most of the atoms. The viscosity: real water resists motion, so a chain in water changes shape slowly, and without water the same change happens in fewer steps. (Simulated time is then no longer real time, as in every CG model.)

The second sentence names the losses. A **bridging water** is a single water molecule that makes hydrogen bonds to two groups of the solute at once and holds them at a fixed distance. The **first hydration shell** is the layer of water molecules in direct contact with the solute. A continuum has neither.

A **salt bridge** is a pair of opposite charges in contact, for example a lysine and a glutamate side chain. Its strength is a balance between two large numbers of opposite sign: the direct attraction of the two charges and the desolvation of each. A small error in either part changes the result a lot, and in implicit-solvent models the error tends to be on the side of too much stability.

### Dynamics without solvent

**Dynamics.** With no explicit solvent there are no collisions, so CG and implicit-solvent models are usually run with Langevin or Brownian dynamics (Module 8), which supply friction and thermal noise. The friction coefficient then sets the time scale.

Water does one more thing that the energy terms above do not replace: its molecules collide with the solute all the time. The collisions slow the solute down (friction) and also keep it moving (random kicks), and together they hold it at the temperature of the bath. **Langevin dynamics** adds both by hand: a friction force proportional to the velocity of each particle, and a random force of matching strength. **Brownian dynamics** is its high-friction limit, in which the velocities are not followed at all and each particle makes small random steps that are biased by the force on it.

In both, the user chooses the friction coefficient, written $\gamma$ in Module 8, in ps$^{-1}$. The equilibrium distribution does not depend on it (Module 8). The speed of every motion does.

A free particle of mass $m$ has the diffusion constant $D=k_BT/(m\gamma)$. A bead of 100 u with $\gamma=1$ ps$^{-1}$ at 300 K has $D=2.494/(100\times1)=0.025$ nm$^2$/ps. A small molecule in real water diffuses at about $10^{-3}$ nm$^2$/ps ($10^{-5}$ cm$^2$/s), so this bead is some 25 times too fast.

A low friction is often chosen on purpose, to sample faster. The result is correct populations on an arbitrary clock.

## Back to atoms, and when to trust a coarse-grained result

### Back-mapping

A CG simulation ends with bead positions. Sometimes you want atoms again: to look at the hydrogen bonds in an interface that has formed, to continue with an all-atom simulation from a state that only the CG model could reach, or to compute an observable that needs atomic detail. **Back-mapping** is the step from a CG configuration to an all-atom configuration that is consistent with it.

It cannot be a formula, because the mapping is many-to-one. A very large number of atomistic configurations share the same bead positions, and the CG simulation has kept no record of which one was meant. Back-mapping picks one plausible member of that set. The procedure has three stages:

1. **Place the atoms.** Put the atoms of each group near their bead, using a standard geometry for each kind of group (a residue, a lipid, a cluster of water molecules).
2. **Relax.** The first guess has stretched bonds and overlapping atoms. Energy minimisation with the all-atom force field removes them (Module 10).
3. **Equilibrate with restraints.** Run a short all-atom simulation while each group is held near its bead position, then release the restraints step by step.

The result is an all-atom structure that agrees with the CG one at the level of the beads. Its atomic details (side-chain orientations, hydrogen bonds, water positions) come from the all-atom force field during the relaxation. They do not come from the CG simulation. If the back-mapped structure drifts away quickly once the restraints are released, and a second, more careful back-mapping does the same, the all-atom model does not support the state that the CG model found. That is useful information.

### When to trust a coarse-grained result

The warnings of this module fit into six questions. Ask them of your own simulation and of any CG paper.

1. **Is the quantity one that the model can represent?** Populations, free-energy differences and structure at the level of beads: yes. Time scales: only after calibration, and only for the calibrated process. Energies and entropies taken separately: no. Anything inside a bead (hydrogen bonds, side-chain packing, single water molecules): no.
2. **Is the model used at the conditions for which it was built?** A CG potential is a free energy and depends on temperature, salt and composition. Results far from the conditions of the fit, and temperature dependences in particular, need independent support.
3. **Was the result fitted or predicted?** Agreement with the data that were used to set the parameters or the energy scale is not evidence. Look for a test on data that played no part in the fit.
4. **Does the conclusion depend on an input that was assumed?** The secondary structure and the elastic network in Martini, the list of native contacts in a Gō model, the starting structure of a predicted complex: the model keeps what it was given.
5. **Is it a comparison or an absolute number?** Differences between closely related systems treated identically are more reliable than a single binding free energy or transition temperature.
6. **Does it survive a change of the uncertain parameters, and a check at higher resolution?** Repeat with a different contact definition, energy scale or protein-water scaling. Back-map a few important states and see whether an all-atom simulation keeps them.

A CG result that passes these questions is a hypothesis about the real system that is worth testing. One that fails them is a statement about the model.

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

<details markdown="1"><summary>5. A bond-angle histogram from mapped all-atom frames has 500 counts in the bin at 120° and 50 counts in the bin at 160° (equal bin widths). What is the Boltzmann-inverted energy difference between the two angles at 300 K, without and with the Jacobian?</summary>
Without the Jacobian: $k_BT\ln(500/50)=2.494\times\ln10=5.7$ kJ/mol. With the Jacobian $J=\sin\theta$, first divide the counts: $500/\sin120^\circ=577$ and $50/\sin160^\circ=146$. Then $U(160^\circ)-U(120^\circ)=2.494\times\ln(577/146)=3.4$ kJ/mol.

The difference of 2.3 kJ/mol between the two answers is the smaller amount of room near 180°, which is geometry and should not be counted as energy. Without the correction the CG chain would avoid straight angles more than the atomistic one does.
</details>

<details markdown="1"><summary>6. A structure-based model has its folding transition at the reduced temperature 1.2, and the real protein unfolds at 60 °C (333 K). What is the contact energy in kJ/mol, and which reduced temperature corresponds to 300 K?</summary>
$T^*=k_BT/\varepsilon$, so $\varepsilon=k_BT/T^*=0.0083145\times333/1.2=2.31$ kJ/mol. At 300 K, $T^*=2.494/2.31=1.08$. The folding temperature was used to set the scale, so it is no longer a prediction of the model.
</details>

<details markdown="1"><summary>7. In the worked example (one compact configuration of energy 0, and 1,000 extended configurations of energy 10 kJ/mol each), which arrangement has the lower CG potential at 100 K?</summary>
$k_BT=0.0083145\times100=0.831$ kJ/mol. $U_{CG}(\text{E})-U_{CG}(\text{C})=10-0.831\times\ln1000=10-5.74=+4.3$ kJ/mol, so the compact arrangement is now the lower one. At 300 K the difference was $-7.2$ kJ/mol. The sign changed with temperature although no atomistic energy changed, so a CG potential fitted at one temperature can be qualitatively wrong at another.
</details>

## Exercises

1. Take a 100 ns all-atom trajectory of a small peptide. Map it to one bead per residue. Compute the distribution of bead-bead bond lengths and angles and derive bonded CG potentials by Boltzmann inversion, with and without the Jacobian. How large is the difference for the angles?
2. Build a C$\alpha$ structure-based model of a small protein with the SMOG web server and run it at several temperatures. Plot $Q$ against time near the folding temperature and identify the two states.
3. Plot the 12-10 and the 12-10-6 contact potentials on the same axes for $\sigma$ = 0.6 nm. Where is the desolvation barrier and how high is it in units of $\varepsilon$?
4. Compute $f_{GB}$ for two atoms with Born radii of 0.2 nm at separations of 0, 0.3 and 2 nm. Show that $f_{GB}\to R$ at zero separation (the Born limit) and $f_{GB}\to r$ at large separation, and that in the second case the GB pair term plus the direct Coulomb term with $\varepsilon_{in}$ equals Coulomb's law with $\varepsilon_{out}$.
5. Run a single-chain CALVADOS simulation of a disordered sequence of your choice and compare its radius of gyration with the Flory scaling $R_g\approx0.2\,N^{0.6}$ nm. ($N$ is the number of residues.)

## Read

{{READ}}

## Key papers

{{PAPERS}}
