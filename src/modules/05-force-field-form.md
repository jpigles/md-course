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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Module 2 showed that an MD program needs one thing from physics: the potential energy $U$, a function that returns an energy for every arrangement of the atoms. The forces are minus the slopes of $U$ (a force points downhill in energy), and the forces move the atoms. This module is about the formula that MD programs use for $U$. That formula, together with the table of numbers that goes into it, is called a **force field**.

The formula is a sum of a few kinds of simple terms: springs for the bonds and the angles, a wave-shaped term for rotation about a bond, and two terms that act between atoms that are not bonded to each other. The module takes them one at a time. For each term you get a picture of the motion it controls, the formula with every symbol defined, the meaning and typical size of each parameter, the size of the energy compared with the thermal energy $k_BT$ (box below), and the force, which is the derivative of the energy.

The module has four layers:

1. **The whole formula.** What a force field is, what it replaces, and why its terms fall into two groups.
2. **The bonded terms.** Bond stretching, angle bending, torsions and improper dihedrals.
3. **The non-bonded terms.** Lennard-Jones and Coulomb, and the rules for which pairs of atoms they apply to.
4. **Using the formula.** The force on each atom, the number of terms, and what the model leaves out.

On a first reading, the sections on the individual terms are the essential part. In "From energy to force" the pair forces are essential, and the algebra for angles and dihedrals can be skipped as long as you read what the result says.

<div class="box physics" markdown="1">
**Physics you need here: the thermal energy $k_BT$.** Atoms at a temperature $T$ are in constant random motion. The energy that this motion typically puts into any one spring, hinge or contact is of the order of $k_BT$. Here $k_B$ is the Boltzmann constant, $0.0083145$ kJ mol$^{-1}$ K$^{-1}$, and $T$ is the temperature in kelvin. At 300 K, $k_BT = 2.494$ kJ/mol, which is 0.596 kcal/mol.

This number is the yardstick for every energy in this module. A motion that costs many times $k_BT$ is stiff: thermal motion hardly produces it. A motion that costs about one $k_BT$ happens all the time. More in the [primer](physics.html#temperature).
</div>

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The conventions below are the ones this module relies on. The general ones (bold letters for vectors, $\sum$ for a sum, $\partial$ for a partial derivative) are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $r$, $r_{ij}$ | A **distance** between two atoms: one positive number, in nanometres. The labels in $r_{ij}$ name the two atoms, $i$ and $j$. |
| $\mathbf r_{ij}$ | In bold, the **vector** $\mathbf r_i-\mathbf r_j$ that points from atom $j$ to atom $i$. Its length is $r_{ij}$. |
| $\hat{\mathbf r}$ | A hat marks a **unit vector**: a vector of length 1, which carries a direction and nothing else. |
| $r_0$, $\theta_0$, $\omega_0$ | A subscript 0 on a length or an angle marks its **equilibrium value**, the value at which that term has its lowest energy. |
| $\sum_{bonds}$ | Add up the expression that follows for every entry of a list, here the list of bonds. |
| $\sum_{i<j}$ | Add up over all pairs of atoms, each pair counted once. |
| i-j-k-l | Atoms bonded in a chain: $i$ to $j$, $j$ to $k$, $k$ to $l$. |
| 1-2, 1-3, 1-4 | Two atoms separated by one, two or three bonds. |
| $r^{-6}$ | A negative power means "one over": $r^{-6} = 1/r^6$. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The usual names collide. The lists under the formulas say which meaning applies each time.

- $\varepsilon$ (epsilon): with no subscript, or with atom labels as in $\varepsilon_{ij}$, it is the depth of the Lennard-Jones well, an energy. $\varepsilon_0$ is the vacuum permittivity, a constant of nature in Coulomb's law. $\varepsilon_r$ is the dielectric constant, a pure number. The three are unrelated.
- $k$: $k_b$, $k_\theta$, $k_{\phi,n}$ and $k_\omega$ are force constants, each with its own unit. $k_B$ is the Boltzmann constant. In "i-j-k" the $k$ is the label of an atom. A capital $K$ is a force constant in the AMBER and CHARMM convention, without the factor $\tfrac12$. $K_b$ in the GROMOS bond term is a different quantity, defined where it appears.
- $\phi$ and $\psi$: $\phi$ is the dihedral angle of any four bonded atoms. In a protein, $\phi$ and $\psi$ are also the names of two particular backbone dihedrals. In the Ryckaert-Bellemans form, $\psi$ means $\phi-180°$.
- $\omega$ (omega): here the improper dihedral angle. In Module 2 the same letter was an angular frequency.
- $e$: after a number, as in $-0.5\,e$, it is the unit of charge. In $e^{-a(r-r_0)}$ it is the base of the exponential function.
- $r$: the distance between whichever two atoms the term is about, a bond length in one section and the distance of a non-bonded pair in another.
- $C$: $C_6$ and $C_{12}$ are Lennard-Jones coefficients. $C_0$, $C_1$ and $C_2$ are the coefficients of the Ryckaert-Bellemans torsion, and $C$ with no subscript is the dispersion coefficient of the Buckingham potential. A plain C in "C-C" or "C=O" is a carbon atom.
</div>

## The functional form

<div data-videos="OBg5wtvNuv4 1oQlCIUm0Bo 8oZSa0zlnIc vpqo0q3zvJU MK5BrpgUMUM L2qEWQb11oc"></div>

Atoms are made of nuclei and electrons, and it is the electrons that hold a molecule together. To compute the energy of a molecule from first principles, you have to solve the equations of quantum mechanics for all of its electrons. That is feasible for small molecules. It is far too slow for a protein in water, where the forces are needed at every one of millions of time steps.

A force field replaces that calculation by a formula. The electrons are no longer in the model. What remains is one point per atom, and an energy that depends only on where those points are. What the electrons do (make bonds, keep atoms from overlapping, gather on some atoms more than on others) is represented by simple terms, with numbers fitted beforehand to quantum calculations and to experiments (Module 6).

<div class="box physics" markdown="1">
**Physics you need here: why the energy can be a function of the atomic positions alone.** A proton is about 1836 times heavier than an electron, so nuclei are slow and electrons are fast. For every arrangement of the nuclei, the electrons settle almost at once into their state of lowest energy, and the energy of that state depends only on where the nuclei are. This is the Born-Oppenheimer idea.

The function it gives is the potential energy $U$ on which the nuclei move, and a force field is a cheap, approximate formula for it. The price is that anything in which the electrons rearrange, such as a chemical reaction, is outside the model. More in the [primer](physics.html#quantum).
</div>

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

<div class="legend" markdown="1">
- $U(\mathbf r)$: the potential energy of the whole system, in kJ/mol. $\mathbf r$ stands for the positions of all the atoms together.
- $\sum_{bonds}$, $\sum_{angles}$, $\sum_{dihedrals}$, $\sum_{impropers}$: add up the expression that follows for every bond, angle, dihedral and improper in the lists of the molecule.
- $r$, $r_0$, $k_b$: the present length of a bond, its equilibrium length, and the stiffness of the bond.
- $\theta$, $\theta_0$, $k_\theta$ (theta): the present value of an angle between two bonds, its equilibrium value, and its stiffness.
- $\phi$ (phi): a dihedral angle, the angle of rotation about a bond.
- $n$, $\sum_n$: a whole number that counts how many times a wave repeats in one full turn. A dihedral can have several such waves, and $\sum_n$ adds them.
- $k_{\phi,n}$, $\delta_n$ (delta): the size and the shift of wave number $n$. The wave is $2k_{\phi,n}$ high from bottom to top, so $k_{\phi,n}$ is half its height.
- $\cos$: the cosine function.
- $\omega$, $\omega_0$, $k_\omega$ (omega): an improper dihedral angle (a measure of how far four atoms are from lying in one plane), its equilibrium value, and its stiffness.
- $\sum_{i<j}^{non\text{-}bonded}$: add up over all pairs of atoms $i$ and $j$ that count as non-bonded, each pair once.
- $r_{ij}$: the distance between atoms $i$ and $j$.
- $\varepsilon_{ij}$, $\sigma_{ij}$ (epsilon, sigma): the strength and the size of the Lennard-Jones interaction of that pair. The factor 4 and the powers 12 and 6 are explained in the Lennard-Jones section.
- $q_i$, $q_j$: the electric charges of the two atoms.
- $\varepsilon_0$, $4\pi$: the vacuum permittivity, a constant of nature, and a factor that comes with it in Coulomb's law.
- $\tfrac12$, the brackets and the braces: a conventional factor, and grouping signs with no special meaning.
</div>

You do not have to take in the whole formula now. Each term has its own section below, with its own list of symbols. What matters here is the structure.

**Read it like this.** Picture the molecule as a construction of balls and springs. Each bond is a spring between two balls, each angle is a hinge with a spring in it, and each dihedral is an axle that turns with some resistance. On top of that, every ball feels every other ball that it is not directly linked to: the balls cannot overlap, they stick to each other a little at close range (Lennard-Jones), and those that carry charges attract or repel (Coulomb). The picture fails in one place that matters: real bonds can break and form, and the springs of a force field cannot.

The first four sums are the **bonded** terms. They run over lists that are fixed when the system is built (the topology). The **topology** is the description of the molecules that you give the program before the run: which atoms there are, what kind each one is, what charge it carries, and which atoms are bonded to which. From the bonds the program derives the lists of angles and dihedrals. Because the lists are fixed, no bond is made or broken during the simulation.

The last sum is the **non-bonded** part and runs over all pairs of atoms, apart from the exclusions discussed below. It includes pairs in different molecules, such as a protein atom and a water atom, and pairs in the same molecule that are far apart along the chain. AMBER, CHARMM, OPLS-AA and GROMOS all use this form with small variations. These are the four main families of biomolecular force fields, compared in Module 6.

### Why two groups of terms

The split reflects two kinds of interaction. A covalent bond is a pair of electrons shared between two atoms. It is strong, and it holds the atoms at specific distances and angles. The bonded terms describe this local geometry with stiff springs.

The non-bonded terms describe what any two atoms do to each other through space: repel when they touch, attract weakly at close range, and attract or repel through their charges. Each pair is weak, but there are very many pairs, and together they decide how a chain folds, what binds to what, and how water arranges itself.

The split is also practical. The bonded lists are short and never change. The non-bonded pairs change as the atoms move, and they take nearly all of the computer time (see "How many terms?" below).

### What the words in brackets mean

*Classical* means that the atoms are points that obey Newton's law (Module 2). No quantum mechanics is done during the run.

*Additive* means two things. The total is a plain sum, so each term can be computed without looking at the others. And each non-bonded term involves two atoms only: the energy of a pair does not depend on which other atoms are nearby. That second statement is an approximation, and the last section says what it leaves out.

*Class I* is the name for this simplest family: each bonded term depends on a single **internal coordinate**, and no term couples two of them. An internal coordinate is a number that describes the shape of a molecule: a bond length, an angle or a dihedral. It is computed from the positions of two, three or four atoms, and it does not change when the molecule as a whole is moved or turned. The last section says what Class II adds.

### Where the numbers come from: atom types

The formula contains no numbers. They come from the parameter table of the force field, which is organised by **atom type**. An atom type is finer than a chemical element: a carbon in a C=O group and a carbon in a CH$_3$ group are both carbon, but they are different atom types, with different charges, sizes and springs.

Every atom in the topology is given a type. The program looks up $r_0$ and $k_b$ of a bond from the types of its two atoms, $\theta_0$ and $k_\theta$ from the types of the three atoms of an angle, and so on. The assumption is that a group of atoms behaves in the same way in every molecule in which it occurs. Module 6 explains how the numbers are obtained.

All energies in this module are in kJ/mol and all distances in nanometres. "Per mole" means the energy of $6.022\times10^{23}$ copies of that bond or pair, which is how chemists quote energies. Forces are in kJ mol$^{-1}$ nm$^{-1}$, an energy divided by a distance (1 kJ mol$^{-1}$ nm$^{-1}$ is 1.66 piconewton). More on the units in the [primer](physics.html#units).

<div class="box warn" markdown="1">
**Convention trap.** GROMACS writes harmonic terms as $\tfrac12k(x-x_0)^2$. AMBER and CHARMM parameter files write $K(x-x_0)^2$ without the half, so $k_{GROMACS} = 2K_{AMBER}$. Add the unit change from kcal mol$^{-1}$ Å$^{-2}$ to kJ mol$^{-1}$ nm$^{-2}$ (a factor 418.4), and the same C-C bond appears as 310 in one file and 259,408 in another.
</div>

In the box, $x$ stands for any bond length or angle, $x_0$ for its equilibrium value, and $k$ and $K$ for the force constant in the two conventions. The box in numbers, for an AMBER value of $K = 310$ kcal mol$^{-1}$ Å$^{-2}$. The convention gives a factor 2, because $K(x-x_0)^2$ and $\tfrac12k(x-x_0)^2$ are the same energy only if $k = 2K$. The unit of energy gives 4.184, since 1 kcal is 4.184 kJ. The unit of length gives 100: 1 nm is 10 Å, so a stretch of 1 nm costs $10^2$ times the energy of a stretch of 1 Å.

Together, $4.184\times100 = 418.4$ and $k = 2\times310\times418.4 = 259{,}408$ kJ mol$^{-1}$ nm$^{-2}$. Nothing about the bond has changed, so check the convention and the units whenever you copy a force constant.

## Bond stretching

<div data-videos="7yEGYWIqSdU"></div>

Two atoms joined by a covalent bond have a preferred distance. Push them together or pull them apart and the energy rises. The simplest model with this behaviour is a spring between the two atoms:

$$
U_b = \tfrac12 k_b\,(r-r_0)^2
$$

<div class="legend" markdown="1">
- $U_b$: the energy of one bond, in kJ/mol. It is zero when the bond has its preferred length and positive otherwise.
- $r$: the present distance between the two bonded atoms, in nm.
- $r_0$: the **equilibrium bond length**, the distance at which the energy is lowest. For the bonds in the table below it is between 0.1 and 0.16 nm.
- $k_b$: the **force constant**, the stiffness of the spring, in kJ mol$^{-1}$ nm$^{-2}$. A larger $k_b$ means that the same stretch costs more energy.
- $(r-r_0)^2$: the stretch, squared. Because of the square, a compression and an extension of the same size cost the same.
- $\tfrac12$: a convention. With it, the force is $k_b$ times the stretch, with no factor 2 (see the trap box above).
</div>

A function of this shape, a constant times a squared displacement, is called **harmonic**. Its graph is a parabola with its lowest point at $r_0$. The [primer](physics.html#oscillator) has more on springs.

**Read it like this.** The energy depends only on how far the bond is from its preferred length, and it grows with the square of that: twice the stretch costs four times the energy. Take the C-C bond of the table below, with $k_b = 2.6\times10^5$ kJ mol$^{-1}$ nm$^{-2}$. Stretching it by 0.01 nm, about 7 % of its length, costs $\tfrac12\times2.6\times10^5\times0.01^2 = 13$ kJ/mol. That is about 5 $k_BT$ at 300 K, so thermal motion rarely stretches a bond that far.

### The force of a bond

<div class="box maths" markdown="1">
**Maths you need here: the derivative of a power, and the chain rule.** The derivative of a function is its slope. For a power of $x$ the rule is: bring the exponent down as a factor and lower the exponent by one, $\dfrac{d}{dx}x^n = n\,x^{n-1}$. So the derivative of $x^2$ is $2x$. The rule also holds for negative exponents: the derivative of $x^{-6}$ is $-6\,x^{-7}$, and the derivative of $x^{-1} = 1/x$ is $-x^{-2}$. Negative powers of this kind are all that the Lennard-Jones and Coulomb terms need (the derivative of $x^{-12}$ is $-12\,x^{-13}$ by the same rule).

The **chain rule** handles a function inside a function: differentiate the outer one, then multiply by the derivative of the inner one. Example: $(r-r_0)^2$ is "something squared", with $r-r_0$ inside. The outer derivative is $2(r-r_0)$, and the inner derivative, of $r-r_0$ with respect to $r$, is 1. The result is $2(r-r_0)$. More in the toolbox: [the derivative](maths.html#derivative), [the chain rule](maths.html#chain-rule).
</div>

Module 2 showed that a force is minus the slope of the potential energy. Differentiate $U_b$ with respect to the bond length: the constant $\tfrac12k_b$ stays, the square gives $2(r-r_0)$ by the box above, and the 2 cancels the $\tfrac12$:

$$
-\frac{dU_b}{dr} = -k_b\,(r-r_0)
$$

<div class="legend" markdown="1">
- $dU_b/dr$: the slope of the bond energy, that is, how fast the energy rises when the bond gets longer.
- $-dU_b/dr$: the force along the bond, in kJ mol$^{-1}$ nm$^{-1}$. The minus sign is there because a force is minus a slope. A negative value acts to make the bond shorter, a positive value to make it longer.
- $k_b$, $r$, $r_0$: the force constant, the present length and the equilibrium length, as in the list above.
</div>

**Read it like this.** For a stretched bond ($r>r_0$) the result is negative: the spring pulls the two atoms towards each other. For a compressed bond it is positive: the spring pushes them apart. Either way the force points back towards $r_0$, and it is proportional to the stretch. For the C-C bond stretched by 0.01 nm it is $-2.6\times10^5\times0.01 = -2600$ kJ mol$^{-1}$ nm$^{-1}$. The section "From energy to force" turns this number into a force vector on each of the two atoms.

### Why a spring, and where it fails

Near the bottom of any smooth well, the energy curve looks like a parabola. That is the Taylor expansion of Module 2: at a minimum the slope is zero, so the first term that matters is the one with the square of the displacement (see the [toolbox](maths.html#taylor)). The spring is therefore the natural first approximation to any bond, and it is good as long as the bond stays close to $r_0$.

The true bond energy is closer to a Morse curve $D_e[1-e^{-a(r-r_0)}]^2$, which allows dissociation.

<div class="legend" markdown="1">
- $D_e$: the depth of the well, in kJ/mol. It is the energy needed to pull the two atoms completely apart.
- $a$: a constant that sets how narrow the well is, in nm$^{-1}$.
- $e^{-a(r-r_0)}$: the exponential function (see the [toolbox](maths.html#exp-log)). It equals 1 at $r=r_0$, falls towards 0 when the bond is stretched, and grows quickly when the bond is compressed.
- $r$, $r_0$: the present and the equilibrium bond length.
</div>

At $r=r_0$ the exponential is 1, the bracket is zero and so is the energy. When the bond is stretched far, the exponential goes to zero, the bracket goes to 1, and the energy levels off at $D_e$. A flat curve has no slope, so there is no force and the atoms are free of each other. That is **dissociation**, the breaking of the bond. On the other side, when the bond is compressed, the exponential grows fast and the energy rises steeply.

The parabola differs in both respects. It rises for ever on both sides, so a harmonic bond can never break. And it is symmetric, while the Morse curve is steeper for compression than for extension.

Close to $r_0$ the two curves agree. For a small number $x$, $e^{-x}\approx1-x$. With $x = a(r-r_0)$ the bracket becomes $a(r-r_0)$ and the Morse energy becomes $D_e\,a^2(r-r_0)^2$. Comparing with $\tfrac12k_b(r-r_0)^2$ gives $k_b = 2D_e\,a^2$: a deep, narrow well is a stiff spring.

The table shows where the agreement ends. It is an illustration with round numbers: $k_b = 2.6\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ as for the C-C bond, and $D_e = 350$ kJ/mol, a value of the size of a covalent bond energy. The relation above then gives $a = \sqrt{k_b/2D_e} = 19.3$ nm$^{-1}$.

| Stretch $r-r_0$ (nm) | Harmonic energy (kJ/mol) | Morse energy (kJ/mol) |
|---|---|---|
| 0.003 | 1.2 | 1.1 |
| 0.01 | 13 | 10.8 |
| 0.05 | 325 | 134 |
| 0.3 | 11,700 | 348 |

At room temperature a bond explores only the very bottom of its well, where the harmonic term is an adequate fit. The first row of the table is that region. The harmonic bond is the wrong model in the last rows: when a bond is stretched by much more than its thermal fluctuation, and whenever a bond should break.

GROMOS writes the bond term as a quartic in the length, $\tfrac14K_b(b^2-b_0^2)^2$, to save square roots; in the physical range it is practically the same as a harmonic term with $k=2K_bb_0^2$ ([Oostenbrink et al. 2004](cite:oostenbrink2004)).

<div class="legend" markdown="1">
- $b$, $b_0$: the present and the equilibrium bond length. GROMOS writes $b$ where this module writes $r$.
- $K_b$: the GROMOS force constant, in kJ mol$^{-1}$ nm$^{-4}$.
- $k$: the force constant of the harmonic term that it corresponds to, in kJ mol$^{-1}$ nm$^{-2}$.
</div>

"Quartic" means that the length appears to the fourth power. A program gets the squared distance directly from the coordinates, as $b^2 = \Delta x^2+\Delta y^2+\Delta z^2$, where $\Delta x$, $\Delta y$ and $\Delta z$ are the differences between the coordinates of the two atoms. The distance $b$ itself needs a square root on top of that, a slower operation, and the quartic form avoids it.

<details markdown="1"><summary>Optional: why the quartic form is nearly a spring</summary>
Factorise: $b^2-b_0^2 = (b-b_0)(b+b_0)$. For a bond close to its equilibrium length, $b+b_0\approx2b_0$. So $\tfrac14K_b(b^2-b_0^2)^2\approx\tfrac14K_b\,(2b_0)^2(b-b_0)^2 = K_bb_0^2\,(b-b_0)^2$. This is $\tfrac12k(b-b_0)^2$ with $k = 2K_bb_0^2$.
</details>

### How stiff is a bond? Fluctuation and vibration period

A force constant of $2.6\times10^5$ says little by itself. Two numbers make it concrete: how far the bond length wanders at room temperature, and how fast the bond vibrates.

<div class="box physics" markdown="1">
**Physics you need here: how far thermal motion stretches a spring.** Module 3 showed that a system held at a temperature $T$ visits each arrangement with a probability proportional to the Boltzmann factor $e^{-U/k_BT}$, so high energies are exponentially rare. The collection of states visited at a fixed temperature is called the **canonical ensemble**.

Put in the energy of a spring, $U = \tfrac12kx^2$, where $x = r-r_0$ is the displacement. The probability of finding the displacement $x$ is then proportional to $e^{-kx^2/2k_BT}$. This bell-shaped curve is a **Gaussian**. In general a Gaussian centred on zero is written $e^{-x^2/2s^2}$, where $s$ is its **standard deviation**, the typical distance of $x$ from zero, and $s^2$ is the **variance**, the average of $x^2$. Comparing the two exponents gives $s^2 = k_BT/k$.

So the typical thermal displacement of a spring is $s = \sqrt{k_BT/k}$, larger when it is hotter and smaller when the spring is stiffer. More on the [Gaussian](maths.html#gaussian) and on the [variance](maths.html#averages) in the toolbox.
</div>

How stiff is it? In the canonical ensemble a harmonic coordinate has variance $k_BT/k$:

| Bond | $r_0$ (nm) | $k_b$ (kJ mol$^{-1}$ nm$^{-2}$) | Thermal fluctuation $\sqrt{k_BT/k_b}$ at 300 K |
|---|---|---|---|
| C-C (aliphatic) | 0.153 | about $2.6\times10^5$ | 0.003 nm |
| C-H | 0.109 | about $2.8\times10^5$ | 0.003 nm |
| C=O | 0.123 | about $4.8\times10^5$ | 0.002 nm |

A "harmonic coordinate" is any quantity whose energy is a parabola, here the bond length. The last column is the standard deviation $s$ of the box, with $k = k_b$. For the first row it is $\sqrt{2.494/(2.6\times10^5)} = 0.0031$ nm. The units work out because kJ/mol divided by kJ mol$^{-1}$ nm$^{-2}$ leaves nm$^2$. "Aliphatic" means a carbon in a chain of single bonds.

Bonds fluctuate by about 2 % of their length. For the C-C bond that is $0.003/0.153 = 0.02$. They carry almost no conformational information, which is why constraining them (Module 9) costs little accuracy. The shape of a molecule changes through rotations about its bonds, and a change of 2 % in a bond length adds almost nothing to that. **Constraining** a bond means holding its length exactly at $r_0$ with an algorithm, in place of the spring.

The second number is the vibration period. Module 2 showed that two atoms joined by a spring oscillate with the angular frequency $\sqrt{k/\mu}$, and that one oscillation takes $2\pi$ divided by the angular frequency. For a bond,

$$
\tau = 2\pi\sqrt{\frac{\mu}{k_b}}
$$

<div class="legend" markdown="1">
- $\tau$ (tau): the **period** of the bond vibration, the time of one full oscillation, in ps.
- $\mu$ (mu): the **reduced mass** of the two bonded atoms, $\mu = m_1m_2/(m_1+m_2)$, in atomic mass units (u). $m_1$ and $m_2$ are the two masses. The reduced mass is always smaller than the lighter of the two.
- $k_b$: the force constant of the bond, in kJ mol$^{-1}$ nm$^{-2}$.
- $2\pi$: the number that converts an angular frequency into a period.
</div>

**Read it like this.** A stiffer bond vibrates faster, and so does a bond with lighter atoms. For the C-H bond, $\mu = 12\times1/13 = 0.923$ u and $\tau = 2\pi\sqrt{0.923/(2.8\times10^5)} = 0.0114$ ps, or 11.4 fs (the worked example of Module 2). For the C-C bond, $\mu = 12\times12/24 = 6$ u and $\tau = 2\pi\sqrt{6/(2.6\times10^5)} = 0.030$ ps, or 30 fs. No conversion factor is needed, because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$. Bond vibrations are the fastest motions in the system, and they are the reason why an MD time step is about 1 fs (Module 4).

## Angle bending

<div data-videos="baRZYahRmSc"></div>

Three atoms bonded in a row, i-j-k, form an angle at the middle atom $j$. The two bond springs fix the distances i-j and j-k, but they say nothing about the angle between the two bonds. Without another term, the molecule could fold at atom $j$ like a hinge with no resistance. The angle term puts a spring on that hinge:

$$
U_\theta = \tfrac12 k_\theta\,(\theta-\theta_0)^2
$$

<div class="legend" markdown="1">
- $U_\theta$: the energy of one angle, in kJ/mol.
- $\theta$ (theta): the present angle between the bonds j-i and j-k, measured at the middle atom $j$.
- $\theta_0$: the **equilibrium angle**. It is close to 109.5° at a carbon with four single bonds, whose neighbours sit at the corners of a tetrahedron, and close to 120° at an atom with three neighbours in a plane.
- $k_\theta$: the **force constant** of the angle, in kJ mol$^{-1}$ rad$^{-2}$. With this unit the difference $\theta-\theta_0$ must be in radians (see the box below).
- $\tfrac12$ and the square: as for the bond.
</div>

<div class="box maths" markdown="1">
**Maths you need here: radians.** An angle can be measured in degrees, where a full turn is 360°, or in **radians**, where a full turn is $2\pi\approx6.283$. The radian is defined so that, on a circle of radius 1, an angle is equal to the length of the arc that it cuts out. To convert, multiply degrees by $\pi/180$: 10° is 0.1745 rad, and 1 rad is 57.3°. The rules for the derivatives of sine and cosine hold only in radians, which is why force constants are given per rad$^2$.
</div>

**Read it like this.** This is the bond formula again, with an angle in place of a length. Bend an angle with $k_\theta = 500$ kJ mol$^{-1}$ rad$^{-2}$ by 10°, which is 0.1745 rad. The cost is $\tfrac12\times500\times0.1745^2 = 7.6$ kJ/mol, about 3 $k_BT$. Angles are softer than bonds, but still stiff on the scale of $k_BT$.

Typical $k_\theta$ is 300 to 700 kJ mol$^{-1}$ rad$^{-2}$, giving fluctuations of $\sqrt{2.494/500} \approx 0.07$ rad, about 4°. This is the formula $\sqrt{k_BT/k}$ of the bond section, with $k_BT = 2.494$ kJ/mol and a middle value $k_\theta = 500$. In degrees, $0.07\times57.3\approx4$.

The force follows as for the bond: $-dU_\theta/d\theta = -k_\theta(\theta-\theta_0)$. A "force" that acts on an angle is a **torque**, a turning force, in kJ mol$^{-1}$ rad$^{-1}$. It is negative when the angle is too wide, which means that it acts to close the angle. For an angle that is 10° too wide it is $-500\times0.1745 = -87$ kJ mol$^{-1}$ rad$^{-1}$. The section "From energy to force" shows how this torque becomes a force on each of the three atoms.

Two variations of the angle term are in use.

CHARMM adds a **Urey-Bradley** term, a harmonic spring between atoms 1 and 3 of the angle, to improve vibrational spectra. Atoms 1 and 3 are the two end atoms, $i$ and $k$. They are not bonded, but the distance between them grows when the angle opens and when either bond stretches, so a spring on that distance ties the angle and the two bond lengths together. The **vibrational spectrum** of a molecule is the set of frequencies at which it vibrates. It can be measured with infrared light, and it is used to check force constants.

GROMOS uses a harmonic function of $\cos\theta$, which is cheaper and avoids a singularity at 180°. Written out, that is a term of the form $\tfrac12k\,(\cos\theta-\cos\theta_0)^2$, with a force constant $k$ in kJ/mol. It is cheaper because a program obtains $\cos\theta$ directly from the atomic positions (as a dot product, see "From energy to force"), while $\theta$ itself needs one more step, the inverse cosine. A **singularity** is a place where a formula divides by zero. The force from a term written in $\theta$ contains a division by $\sin\theta$, and $\sin180° = 0$.

## Torsions (proper dihedrals)

<div data-videos="H-NiSB-2bmo KmuYjxL0Kfw fst8oSeAQ98"></div>

Bonds and angles are stiff, so they cannot be what lets a protein change its shape. The freedom is in rotation about single bonds. Take four atoms bonded in a row, i-j-k-l. With all bond lengths and angles held fixed, one motion is left: the atom at one end can swing around the central bond j-k, like a door on its hinges. The torsion term says how the energy changes during that rotation.

The dihedral angle $\phi$ of four bonded atoms i-j-k-l is the angle between the planes (i,j,k) and (j,k,l). A simpler way to see it: look along the central bond from $j$ to $k$. The bond to atom $i$ and the bond to atom $l$ then look like the two hands of a clock, and $\phi$ is the angle between the hands. In the convention used here, $\phi = 0$ when atom $l$ is hidden straight behind atom $i$ (the *cis* or eclipsed position) and $\phi = 180°$ when the two are on opposite sides (*trans*).

"Torsion angle" and "dihedral angle" are two names for the same thing. "Proper" separates these dihedrals, whose four atoms are bonded in a chain, from the "improper" ones of the next section.

<div class="box maths" markdown="1">
**Maths you need here: periodic functions, the cosine and the Fourier series.** A function is **periodic** if it repeats. Turning a bond by a full 360° brings the atoms back to where they were, so the energy at $\phi+360°$ must equal the energy at $\phi$.

The basic periodic function is the **cosine**. $\cos\phi$ is 1 at $\phi = 0$, falls to 0 at 90° and to $-1$ at 180°, and is back at 1 at 360°: one wave per turn. $\cos(n\phi)$ with a whole number $n$ goes through $n$ waves per turn. For example $\cos(3\phi)$ is 1 at 0°, $-1$ at 60° and 1 again at 120°, with three maxima and three minima in a full turn. Subtracting a **phase** $\delta$ inside the cosine, $\cos(n\phi-\delta)$, slides the whole wave along the axis by an angle $\delta/n$ without changing its shape.

A **Fourier series** is a sum of such waves with $n = 1, 2, 3, \dots$, each with its own height and phase. Any smooth periodic function can be built in this way, and each wave you add lets the sum follow finer detail. "Short" means that a few waves are enough. More in the [toolbox](maths.html#fourier).
</div>

Rotation about the central bond is periodic, so the energy is a short Fourier series:

$$
U_\phi = \sum_{n} k_{\phi,n}\,\big[1+\cos(n\phi-\delta_n)\big],\qquad n = 1,2,3,(4,6).
$$

<div class="legend" markdown="1">
- $U_\phi$: the energy of one dihedral, in kJ/mol.
- $\phi$ (phi): the dihedral angle. It runs over a full turn, from $-180°$ to $180°$.
- $n$: the **multiplicity** of one wave of the series, a whole number. That wave repeats $n$ times in a full turn.
- $\sum_n$: add the waves for the values of $n$ that this dihedral uses, one or several. In the list $n = 1,2,3,(4,6)$ the brackets mark values that are used less often.
- $k_{\phi,n}$: the **force constant** of the wave with multiplicity $n$, in kJ/mol. It sets the height of that wave.
- $\delta_n$ (delta): the **phase** of that wave, an angle. It sets where the wave has its maxima and minima.
- $1+\cos(\dots)$: the cosine runs from $-1$ to 1, so the bracket runs from 0 to 2. The 1 only shifts the energy so that its lowest value is zero.
</div>

$n$ is the multiplicity (the number of minima in a full turn), $\delta_n$ the phase (0 or 180° in most force fields), and $k_{\phi,n}$ is half the barrier height of that component. For ethane-like rotation about an sp$^3$-sp$^3$ bond, $n=3$ with a total barrier near 12 kJ/mol ($\approx 5\,k_BT$).

**Read it like this.** Take a single wave, $k\,[1+\cos(n\phi-\delta)]$. Its lowest value is 0, where the cosine is $-1$, and its highest value is $2k$, where the cosine is 1. To get from one minimum to the next, the dihedral has to pass over a maximum. The height of that **barrier** is $2k$, so $k$ is half the barrier height.

Where the minima are depends on the phase. With $\delta = 0$ the cosine is $-1$ when $n\phi = 180°$, $540°$, and so on. For $n = 3$ that is at $\phi = 60°$, 180° and 300°, with maxima at 0°, 120° and 240°. With $\delta = 180°$ the wave is turned upside down, because $\cos(n\phi-180°) = -\cos(n\phi)$: the minima are where the maxima were. A wave with $n = 2$ and $\delta = 180°$ has its minima at 0° and 180°, the two arrangements in which the four atoms lie in one plane.

The ethane example works like this. An sp$^3$ carbon is a carbon with four single bonds that point to the corners of a tetrahedron. Seen along the central bond, each of the two carbons carries three other atoms, 120° apart. Turning one end by 120° gives an arrangement that looks the same as before, so the energy repeats three times per turn and $n = 3$. The minima are the *staggered* positions, where the atoms of the far carbon sit in the gaps between those of the near one, and the maxima are the *eclipsed* positions, where they sit straight behind them.

In a chain such as butane the two end carbons can be told apart from the hydrogens. The staggered position with the end carbons at 180° is then the *trans* one, and the two with the end carbons at $\pm60°$ are called *gauche* (exercise 2 uses these words).

"Total barrier" is said for a reason. Several sets of four atoms i-j-k-l share the same central bond: in ethane there are nine, one for each pair of a hydrogen on the first carbon and a hydrogen on the second. Each set can have its own dihedral term, and the non-bonded terms between the end atoms contribute too (see "Which pairs count" below). The barrier that the molecule feels is the sum of all of these. In units of the thermal energy it is $12/2.494 = 4.8\,k_BT$.

The torque about the central bond is minus the derivative of the energy with respect to $\phi$. The derivative of $\cos$ is $-\sin$, and by the chain rule the $n\phi$ inside the cosine gives a factor $n$:

$$
-\frac{dU_\phi}{d\phi} = \sum_n n\,k_{\phi,n}\,\sin(n\phi-\delta_n)
$$

<div class="legend" markdown="1">
- $-dU_\phi/d\phi$: the torque about the central bond, in kJ mol$^{-1}$ rad$^{-1}$. A positive value acts to increase $\phi$.
- $\sin$: the sine function. It is zero where the cosine has a maximum or a minimum.
- The factor $n$ in front of $k_{\phi,n}$: a wave that repeats $n$ times per turn is $n$ times steeper than a wave of the same height that repeats once.
- Other symbols: as in the list above.
</div>

**Read it like this.** At the minima and at the tops of the barriers the sine is zero and there is no torque. Halfway up a barrier the torque is largest, $n\,k_{\phi,n}$ for a single wave. For $n = 3$ and $k = 6$ kJ/mol that is 18 kJ mol$^{-1}$ rad$^{-1}$, against 87 for the angle bent by 10° in the previous section. Torsions are the softest of the bonded terms.

<div class="box key" markdown="1">
**Torsions are where the biology is.** Barriers of a few $k_BT$ mean torsions are the soft degrees of freedom that change during conformational transitions: the backbone $\phi$ and $\psi$ angles and the side-chain $\chi$ angles. They are also the least "physical" term: the torsion parameters absorb everything the other terms get wrong, and they are fitted last (Module 6). Almost every revision of a protein force field in the last 25 years (ff99SB, ILDN, ff14SB, CHARMM22/CMAP, CHARMM36, CHARMM36m) is mainly a re-fit of backbone or side-chain torsions.
</div>

Some words in this box need explaining.

*Soft degrees of freedom.* A degree of freedom is one independent way in which the system can move (Module 2). "Soft" means that moving it costs only a few $k_BT$, so thermal motion changes it all the time. The backbone angles $\phi$ and $\psi$ are the rotations about the N-C$\alpha$ bond and the C$\alpha$-C bond of each residue, and $\chi_1$, $\chi_2$ and so on ($\chi$ is the Greek letter chi) are the dihedrals along a side chain.

*Least physical, fitted last.* Bond springs, charges and Lennard-Jones terms each stand for something identifiable. The torsion term does not stand for one separate interaction. In practice the other parameters are chosen first. Then the energy of rotation about a bond is computed with quantum chemistry, and whatever part of it the other terms fail to reproduce is assigned to the torsion term. The torsion parameters therefore correct the errors of the rest, and they are only meaningful together with the rest.

The names in the last sentence of the box are versions of the AMBER and CHARMM protein force fields (Module 6).

Two variants you will meet:

- **Ryckaert-Bellemans** form, a power series in $\cos\psi$ with $\psi=\phi-180°$, used by OPLS in GROMACS. It is mathematically equivalent to a Fourier series.
- **CMAP** (CHARMM and ff19SB): a two-dimensional correction $U_{CMAP}(\phi,\psi)$ stored on a grid and interpolated with bicubic splines. It captures the coupling between the two backbone dihedrals that separate one-dimensional terms cannot.

*Ryckaert-Bellemans.* A power series in $\cos\psi$ is a polynomial, $C_0+C_1\cos\psi+C_2\cos^2\psi+\dots$, with coefficients $C_0$, $C_1$, $C_2$ in kJ/mol. It describes the same curves as a Fourier series, because every $\cos(n\phi)$ can be rewritten as a polynomial in $\cos\phi$: for example $\cos2\phi = 2\cos^2\phi-1$ and $\cos3\phi = 4\cos^3\phi-3\cos\phi$. The shift by 180° only changes where the angle is counted from. Since $\cos\psi = \cos(\phi-180°) = -\cos\phi$, the *trans* position is $\psi = 0$ in this convention. The rewriting works wave by wave when the phases are 0 or 180°, which is the usual case.

*CMAP.* The one-dimensional terms give the two backbone dihedrals of a residue an energy of the form $U_\phi(\phi)+U_\psi(\psi)$: one function of $\phi$ plus one function of $\psi$. With such a sum, the energy change on turning $\phi$ is the same whatever the value of $\psi$. In a real peptide it is not, because the atoms moved by one rotation come close to the atoms moved by the other. That dependence of one on the other is what **coupling** means, and CMAP adds one function of both angles to describe it.

The CMAP function has no formula. Its values are stored in a table for regularly spaced values of $\phi$ and $\psi$ (the **grid**), and **interpolation** is the calculation of a value between the grid points. A bicubic spline does it with pieces of smooth surface, each a cubic polynomial in the two angles, joined so that the energy and its slopes are continuous. The slopes must be continuous because they are the forces.

## Improper dihedrals

Some groups of atoms are flat: the peptide group, an aromatic ring, a carboxylate. In the real molecule the flatness comes from electrons that are shared over several atoms. The force field has no electrons, and the bond and angle springs resist bending out of the plane only weakly. One more term is added to keep such groups flat.

Take a central atom bonded to three others. The improper dihedral angle $\omega$ measures how far these four atoms are from lying in one plane. It is computed like a dihedral, as the angle between two planes that each pass through three of the four atoms. With the usual ordering of the atoms, $\omega = 0$ when all four lie in one plane. It is called "improper" because the four atoms are not bonded in a chain, so no rotation about a bond is involved.

$$
U_\omega = \tfrac12 k_\omega\,(\omega-\omega_0)^2\quad\text{(CHARMM, GROMOS)}\qquad\text{or}\qquad k\,[1+\cos(2\omega-180°)]\quad\text{(AMBER)}
$$

<div class="legend" markdown="1">
- $U_\omega$: the energy of one improper dihedral, in kJ/mol.
- $\omega$ (omega): the improper dihedral angle.
- $\omega_0$: its equilibrium value. It is zero for a group that should be flat.
- $k_\omega$: the force constant of the harmonic form, in kJ mol$^{-1}$ rad$^{-2}$.
- "or": the formula shows two alternatives. A force field uses one of them, and the names in brackets say which family uses which.
- $k$: the force constant of the second form, in kJ/mol, as for a proper torsion.
- $2\omega-180°$: the second form is a torsion wave with multiplicity 2 and phase 180°.
</div>

**Read it like this.** The first form is the angle spring again: the energy is zero at $\omega_0$ and grows with the square of the deviation, and the torque is $-dU_\omega/d\omega = -k_\omega(\omega-\omega_0)$. The second form is the wave met in the torsion section. Because $\cos(2\omega-180°) = -\cos2\omega$, it equals $k\,[1-\cos2\omega]$, which is zero for the flat arrangement and rises to $2k$ at $\omega = \pm90°$.

Close to the plane the two forms agree. For a small angle $x$ in radians, $\cos x\approx1-\tfrac12x^2$. With $x = 2\omega$ this gives $1-\cos2\omega\approx2\omega^2$, so the second form is $2k\,\omega^2 = \tfrac12(4k)\,\omega^2$. It behaves like the harmonic form with $k_\omega = 4k$.

An improper keeps four atoms in a plane (the peptide bond, aromatic rings, carboxylates) or, in united-atom force fields, preserves the chirality of a carbon whose hydrogen is not represented. CHARMM writes the improper as $K_{imp}(\omega-\omega_0)^2$ without the ½, as it does for bonds and angles. Here $K_{imp}$ is the CHARMM force constant, and the trap box of the first section applies: $k_\omega = 2K_{imp}$.

The second use needs an explanation. A **united-atom** force field does not represent the hydrogens bonded to carbon as separate atoms: a CH, CH$_2$ or CH$_3$ group is one particle. Chirality is the handedness of a carbon with four different neighbours, such as the C$\alpha$ of an amino acid.

With all four neighbours present, the carbon cannot turn into its mirror image without passing through arrangements of very high angle energy. If the hydrogen is not represented, the carbon has three neighbours in the model, and it could flip through the plane of those three like an umbrella in the wind. An improper with a non-zero $\omega_0$ holds it on the correct side.

## Lennard-Jones: repulsion and dispersion

<div data-videos="D3kHLAj8ozI EuwL12-5pXY keXmqiGN1Qc zNiUrSxZdsQ"></div>

Now the atoms that are not bonded to each other. Two facts about any pair of atoms have to be in the model. Atoms cannot be pushed into each other: at short distance the energy rises steeply. And at a slightly larger distance any two atoms attract each other weakly, even when they carry no charge, which is why a gas of uncharged atoms such as argon becomes a liquid when it is cooled. The Lennard-Jones function is the simplest formula with both features:

$$
U_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right]
= \frac{C_{12}}{r^{12}}-\frac{C_6}{r^6},\qquad C_6 = 4\varepsilon\sigma^6,\; C_{12} = 4\varepsilon\sigma^{12}.
$$

<div class="legend" markdown="1">
- $U_{LJ}(r)$: the Lennard-Jones energy of one pair of atoms, in kJ/mol, as a function of their distance.
- $r$: the distance between the two atoms, in nm.
- $\varepsilon$ (epsilon): the **well depth**, in kJ/mol. The lowest value of the energy is $-\varepsilon$. It says how strongly the pair attracts.
- $\sigma$ (sigma): the distance at which the energy passes through zero, in nm. It says how large the pair is. The oxygen of the TIP3P water model in exercise 3 has $\sigma = 0.3151$ nm.
- $(\sigma/r)^{12}$: the repulsive term. It is positive and grows very fast when $r$ becomes smaller than $\sigma$.
- $(\sigma/r)^{6}$: the attractive term. It enters with a minus sign.
- The factor 4: chosen so that the depth of the well is exactly $\varepsilon$ (shown below).
- $C_{12}$, $C_6$: the same function written with two coefficients in place of $\sigma$ and $\varepsilon$, in kJ mol$^{-1}$ nm$^{12}$ and kJ mol$^{-1}$ nm$^{6}$. The second equals sign only multiplies out the brackets.
</div>

**Read it like this.** Picture two balls that are hard and slightly sticky. The table follows the energy as the two atoms approach, with the distance in units of $\sigma$ and the energy in units of $\varepsilon$.

| $r/\sigma$ | $U_{LJ}/\varepsilon$ | What happens |
|---|---|---|
| 3.0 | $-0.005$ | Almost nothing. |
| 2.0 | $-0.062$ | A weak attraction. |
| 1.5 | $-0.32$ | The attraction grows. |
| 1.122 | $-1$ | The minimum: the atoms are in contact. |
| 1.0 | 0 | The repulsion has cancelled the attraction. |
| 0.95 | $+1.96$ | The wall. |
| 0.9 | $+6.6$ | A little closer, and more than three times higher. |

Far apart, both terms are tiny and the $r^{-6}$ term is the larger one, so the energy is slightly negative. Below $r = \sigma$ the $r^{-12}$ term wins and the energy shoots up. In between there is a well.

- $\sigma$ is the distance where the energy is zero, the "size" of the atom pair.
- The minimum is at $r_{min} = 2^{1/6}\sigma\approx1.122\,\sigma$ with depth $-\varepsilon$. AMBER and CHARMM files list $R_{min}/2$ per atom instead of $\sigma$.
- **The $r^{-6}$ attraction is physical.** It is the London dispersion energy: a fluctuation of the electron cloud on one atom creates an instantaneous dipole, which induces a dipole on the other, and the interaction of the two falls off as $r^{-6}$.
- **The $r^{-12}$ repulsion is a convenience.** Pauli repulsion from overlapping electron clouds is closer to exponential. $r^{-12}$ was chosen because it is the square of $r^{-6}$ and so costs one multiplication. It is somewhat too steep. The Buckingham potential $A e^{-Br} - C/r^6$ is more realistic and slower.

The next three subsections take these points in turn: where the minimum is, the two ways of stating the size, and where the two powers come from.

### Where the minimum is

<div class="box maths" markdown="1">
**Maths you need here: finding a minimum.** At the lowest point of a smooth curve the curve is flat: its slope is zero. So to find where a function $f(x)$ has its minimum, compute the derivative $df/dx$, set it equal to zero and solve for $x$. Example: $f(x) = x^2-4x$ has $df/dx = 2x-4$, which is zero at $x = 2$. The same condition holds at a maximum, so check which of the two you have found. More in the [toolbox](maths.html#derivative).
</div>

Write the function with powers of $r$, as $4\varepsilon\,[\sigma^{12}r^{-12}-\sigma^{6}r^{-6}]$, and differentiate each term with the power rule (the derivative of $r^{-12}$ is $-12\,r^{-13}$, that of $r^{-6}$ is $-6\,r^{-7}$):

$$
\frac{dU_{LJ}}{dr} = 4\varepsilon\left[-\frac{12\,\sigma^{12}}{r^{13}}+\frac{6\,\sigma^{6}}{r^{7}}\right]
$$

<div class="legend" markdown="1">
- $dU_{LJ}/dr$: the slope of the Lennard-Jones energy, that is, how fast the energy changes when the distance grows.
- The numbers 12 and 6: the exponents, brought down by the power rule.
- Other symbols: as in the list above.
</div>

Now set the slope to zero. The bracket must vanish, so $12\,\sigma^{12}/r^{13} = 6\,\sigma^{6}/r^{7}$. Multiply both sides by $r^{13}$ and divide both sides by $6\,\sigma^{6}$: this leaves $2\,\sigma^{6} = r^{6}$. Take the sixth root: $r_{min} = 2^{1/6}\sigma\approx1.122\,\sigma$.

For the depth, put this distance back into the energy. At $r_{min}$, $(\sigma/r)^6 = \tfrac12$ and $(\sigma/r)^{12} = \tfrac14$, so $U_{LJ} = 4\varepsilon\,(\tfrac14-\tfrac12) = -\varepsilon$. This is the reason for the factor 4 in the formula: without it the depth would be $\varepsilon/4$.

### Two ways to state the size of an atom

The same curve can be described by $\sigma$, the distance where the energy crosses zero, or by $r_{min}$, the distance where it is lowest. The two differ by the fixed factor $2^{1/6} = 1.122$. Force-field files that use the second choice call it $R_{min}$. In terms of $R_{min}$ the function reads

$$
U_{LJ}(r) = \varepsilon\left[\left(\frac{R_{min}}{r}\right)^{12}-2\left(\frac{R_{min}}{r}\right)^{6}\right]
$$

<div class="legend" markdown="1">
- $R_{min}$: the distance at which the energy of the pair is lowest, $R_{min} = 2^{1/6}\sigma$.
- The factor 2 in front of the second term: it replaces the 4 of the $\sigma$ form.
- Other symbols: as in the list above.
</div>

To get this form, put $\sigma^6 = R_{min}^6/2$ and $\sigma^{12} = R_{min}^{12}/4$ into the original formula. The 4 in front cancels the 4 under the first term and leaves a 2 with the second.

AMBER and CHARMM files list half of this distance, $R_{min}/2$, for each atom type. Half of the contact distance of two equal atoms plays the part of a radius, and for a pair of different atoms the two radii are added (the first combining rule below). To convert a file value to $\sigma$: $\sigma = 2\times(R_{min}/2)/2^{1/6} = 1.782\times(R_{min}/2)$. Mixing up the two conventions makes every atom about 12 % too large or too small.

### Where the two powers come from

<div class="box physics" markdown="1">
**Physics you need here: dipoles, and why dispersion falls off as $r^{-6}$.** A **dipole** is a pair of equal and opposite charges a small distance apart. A molecule with more electrons at one end than at the other is a dipole. A single neutral atom is not, on average, because its electron cloud is centred on the nucleus. But the electrons move, and at any instant the cloud is slightly off-centre. For that instant the atom is a small dipole, pointing in a random direction.

This instantaneous dipole creates an electric field around the atom, and the field of a dipole weakens with distance as $1/r^3$. A second atom at a distance $r$ feels the field. Its own electron cloud is pulled a little to one side, so it becomes an **induced dipole**, with a size proportional to the field, that is, to $1/r^3$. The induced dipole always points in the direction that lowers the energy, so the two atoms attract. The energy gained is proportional to the induced dipole times the field in which it sits: $1/r^3\times1/r^3 = 1/r^6$.

This attraction is called the London dispersion energy, and also the van der Waals attraction. It acts between all atoms, charged or not. More in the primer: [dipoles](physics.html#dipoles) and [forces between molecules](physics.html#intermolecular).
</div>

The repulsion has a different origin. The **Pauli principle** of quantum mechanics forbids two electrons from being in the same state. When two atoms come so close that their electron clouds overlap, some electrons are forced into states of higher energy, and the energy of the pair rises steeply. The overlap of two clouds shrinks roughly exponentially with the distance, which is why an exponential describes the repulsion better than a power of $r$.

The power 12 was a practical choice. Once a program has the attractive part, one multiplication gives the repulsive part:

```python
s6  = (sigma / r)**6        # the attractive part
s12 = s6 * s6               # the repulsive part, for one more multiplication
u   = 4 * eps * (s12 - s6)  # the Lennard-Jones energy
```

"Somewhat too steep" means that the $r^{-12}$ wall rises faster than the true repulsion, so the atoms of the model are a little too hard. In the Buckingham potential $A e^{-Br} - C/r^6$, the first term is an exponential wall and the second is the same dispersion attraction as before.

<div class="legend" markdown="1">
- $A$: the height of the repulsive wall, in kJ/mol.
- $B$: how fast the wall falls off with distance, in nm$^{-1}$.
- $e^{-Br}$: the exponential function of the distance. This $e$ is not the unit of charge.
- $C$: the strength of the dispersion attraction, in kJ mol$^{-1}$ nm$^{6}$, like $C_6$.
- $r$: the distance between the two atoms.
</div>

It is slower because an exponential costs more to compute than a multiplication, and because it needs the distance $r$ itself, which takes a square root.

Typical values of $\varepsilon$ are 0.1 to 1 kJ/mol, well below $k_BT$ = 2.5 kJ/mol. A single dispersion contact is weak. Their importance comes from their number: a buried side chain has dozens. As an illustration, 30 contacts of 0.5 kJ/mol each add up to 15 kJ/mol, about 6 $k_BT$. The force of the Lennard-Jones term is worked out in "From energy to force".

### Combining rules

The Lennard-Jones formula needs a $\sigma_{ij}$ and an $\varepsilon_{ij}$ for every pair of atoms. A force field with, say, 50 atom types has $50\times51/2 = 1275$ different pairs of types, too many to fit one by one. Force fields store $\sigma_i$ and $\varepsilon_i$ per atom type and build pair parameters from a rule:

| Rule | $\sigma_{ij}$ | $\varepsilon_{ij}$ | Used by |
|---|---|---|---|
| Lorentz-Berthelot | $\tfrac12(\sigma_i+\sigma_j)$ | $\sqrt{\varepsilon_i\varepsilon_j}$ | AMBER, CHARMM |
| Geometric | $\sqrt{\sigma_i\sigma_j}$ | $\sqrt{\varepsilon_i\varepsilon_j}$ | OPLS, GROMOS (on $C_6$, $C_{12}$) |

<div class="legend" markdown="1">
- $\sigma_i$, $\varepsilon_i$: the Lennard-Jones size and well depth stored for the type of atom $i$. They are the pair values for two atoms of that same type.
- $\sigma_j$, $\varepsilon_j$: the same for atom $j$.
- $\sigma_{ij}$, $\varepsilon_{ij}$: the values used in the formula for the pair of atoms $i$ and $j$.
</div>

<div class="box maths" markdown="1">
**Maths you need here: two kinds of mean.** The **arithmetic mean** of two numbers $a$ and $b$ is half their sum, $\tfrac12(a+b)$. The **geometric mean** is the square root of their product, $\sqrt{ab}$. The two are close when $a$ and $b$ are similar, and the geometric mean is the smaller one when they differ. For 0.30 and 0.40 the arithmetic mean is 0.350 and the geometric mean is 0.346. For 0.2 and 0.8 they are 0.5 and 0.4.
</div>

The arithmetic mean for $\sigma$ has a simple picture. If the atoms were hard spheres with diameters $\sigma_i$ and $\sigma_j$, they would touch when their centres are one radius plus the other radius apart, which is $\tfrac12(\sigma_i+\sigma_j)$. The geometric mean for $\varepsilon$ gives the pair a strength between those of the two atoms, closer to the weaker one.

The note "on $C_6$, $C_{12}$" says that the geometric mean is applied to the coefficients, $C_{6,ij} = \sqrt{C_{6,i}\,C_{6,j}}$ and the same for $C_{12}$. The result is the same as in the second row of the table. With $C_6 = 4\varepsilon\sigma^6$, the square root of $4\varepsilon_i\sigma_i^6\times4\varepsilon_j\sigma_j^6$ is $4\sqrt{\varepsilon_i\varepsilon_j}\,(\sqrt{\sigma_i\sigma_j})^6$, which is $4\varepsilon_{ij}\sigma_{ij}^6$ with both parameters combined geometrically.

The rules are approximations. Where they fail badly, force fields override them for specific pairs (**NBFIX** in CHARMM, for example for ions with carboxylates and, in CHARMM36m, for arginine with carboxylates). To override means that a separate table lists $\sigma_{ij}$ and $\varepsilon_{ij}$ for one particular pair of atom types, and the program uses those values in place of the rule.

The demo below plots the pair energy against the distance. Leave the charge product at zero first and move $\varepsilon$ and $\sigma$: one changes the depth of the well, the other shifts it sideways. Then add charge and watch the Coulomb term of the next section take over.

<div class="widget" data-widget="lj"></div>

## Electrostatics

<div data-videos="_CElNDa1hoI ZdZXckzHktM 5z8IWRDqgy8"></div>

The electrons of a molecule are not shared equally between its atoms. Oxygen and nitrogen pull electrons towards themselves more strongly than carbon and hydrogen do. An oxygen in a molecule therefore carries a little more negative charge than its nucleus balances, and a hydrogen bonded to it carries a little less. A force field represents this by giving every atom a small fixed charge and letting all the charges interact through Coulomb's law.

<div class="box physics" markdown="1">
**Physics you need here: charge and Coulomb's law.** Electric charge comes in two kinds, positive and negative. Its natural unit is the **elementary charge** $e$: a proton has the charge $+1\,e$ and an electron $-1\,e$. Two charges of the same sign repel each other, and two of opposite sign attract.

**Coulomb's law** gives the energy of two point charges $q_1$ and $q_2$ at a distance $r$: it is proportional to $q_1q_2/r$. For like charges the product is positive, so the energy is positive and falls when they move apart: repulsion. For opposite charges it is negative and falls further when they approach: attraction. Halving the distance doubles the energy, and the energy is counted from zero for charges that are infinitely far apart. More in the [primer](physics.html#electrostatics).
</div>

$$
U_C = \frac{q_iq_j}{4\pi\varepsilon_0\,r_{ij}} = 138.935\ \frac{q_iq_j}{r_{ij}}\ \text{kJ/mol}\quad(q \text{ in } e,\ r \text{ in nm}).
$$

<div class="legend" markdown="1">
- $U_C$: the Coulomb energy of one pair of atoms, in kJ/mol.
- $q_i$, $q_j$: the charges of atoms $i$ and $j$, in units of the elementary charge $e$.
- $r_{ij}$: the distance between the two atoms, in nm.
- $\varepsilon_0$: the **vacuum permittivity**, a constant of nature that sets the strength of the electric interaction. It is not the Lennard-Jones $\varepsilon$.
- $4\pi$: a factor that belongs to the way $\varepsilon_0$ is defined.
- 138.935: the value of $1/(4\pi\varepsilon_0)$ in the units of MD, kJ mol$^{-1}$ nm $e^{-2}$. It is the energy, in kJ/mol, of two elementary charges 1 nm apart.
- The words in brackets: the number 138.935 is correct only with charges in $e$ and distances in nm.
</div>

<details markdown="1"><summary>Optional: where the number 138.935 comes from</summary>
In SI units the energy of two elementary charges at a distance $r$ is $e^2/(4\pi\varepsilon_0r)$, with $e = 1.602177\times10^{-19}$ coulomb and $\varepsilon_0 = 8.854188\times10^{-12}$ C$^2$ J$^{-1}$ m$^{-1}$. For $r$ equal to 1 nm, which is $10^{-9}$ m, this gives $2.3071\times10^{-19}$ J for one pair. MD energies are per mole, so multiply by the Avogadro constant, $6.02214\times10^{23}$ per mole. The result is 138,935 J/mol, or 138.935 kJ/mol.
</details>

**Read it like this.** A charge of $+1$ and a charge of $-1$ at 1 nm have an energy of $-138.9$ kJ/mol, which is 56 $k_BT$. At 2 nm it is half of that. The energy scales with the product of the charges, so two charges of $+0.3$ and $-0.5$ interact with $0.3\times0.5 = 0.15$ times the strength of two unit charges at the same distance.

Each atom carries a fixed **partial charge** placed at its nucleus. "Partial" means a fraction of an elementary charge. "Fixed" means that the value stays the same for the whole simulation, whatever surrounds the atom. "Placed at its nucleus" means that the charge is a point at the position of the atom.

The charges represent the uneven distribution of electrons in the molecule: in a peptide group, about $-0.5\,e$ on O, $+0.5\,e$ on C, $-0.4\,e$ on N and $+0.3\,e$ on H (values vary by force field). The peptide group is the C=O of one residue and the N-H of the next. The partial charges of a molecule add up to its total charge, which is zero for a neutral molecule and a whole number for an ion. Partial charges are parameters of the model: they cannot be measured one by one, and Module 6 describes how they are chosen.

There is no explicit hydrogen-bond term in modern force fields. A hydrogen bond is the sum of the Coulomb attraction between a positive H and a negative acceptor and the Lennard-Jones terms of the heavy atoms. The acceptor is the atom at which the hydrogen points, and "heavy atoms" are all atoms other than hydrogen.

The table shows how this works for the hydrogen bond N-H...O=C between two peptide groups, with the charges quoted above. It is an illustration with a simple geometry: the four atoms on a straight line, N-H = 0.10 nm, H...O = 0.19 nm and C=O = 0.123 nm. Each row is one application of the formula, $138.935\,q_iq_j/r_{ij}$.

| Pair | Charges ($e$) | Distance (nm) | Coulomb energy (kJ/mol) |
|---|---|---|---|
| H and O | $+0.3$, $-0.5$ | 0.19 | $-109.7$ |
| N and O | $-0.4$, $-0.5$ | 0.29 | $+95.8$ |
| H and C | $+0.3$, $+0.5$ | 0.313 | $+66.6$ |
| N and C | $-0.4$, $+0.5$ | 0.413 | $-67.3$ |
| Sum | | | $-14.6$ |

Four terms of 67 to 110 kJ/mol, two attractive and two repulsive, leave a net attraction of 14.6 kJ/mol, about 6 $k_BT$. The Lennard-Jones terms of the same atoms come on top, and their repulsive wall is what stops the atoms from coming closer. So a hydrogen bond in a force field is ordinary electrostatics, and its energy is a small difference between large numbers, a point that returns below.

<div class="box physics" markdown="1">
**Physics you need here: the dielectric constant and screening.** Put two charges in water, and the energy between them is much smaller than in empty space. The reason is that a water molecule is a dipole, negative at its oxygen and positive at its hydrogens. Water molecules near a positive charge turn their oxygens towards it, and those near a negative charge turn their hydrogens towards it. The turned molecules produce an electric field of their own, which opposes the field of the charge. Seen from a distance, the charge looks weaker than it is, and this is called **screening**.

For charges that are far apart compared with the size of a water molecule, the whole effect is summed up in one number, the **dielectric constant** $\varepsilon_r$ (also called the relative permittivity). The energy is the vacuum value divided by $\varepsilon_r$, that is, $q_iq_j/(4\pi\varepsilon_0\varepsilon_r\,r_{ij})$. Vacuum has $\varepsilon_r = 1$, and liquid water has a value of about 80. Two unit charges 1 nm apart interact with 138.9 kJ/mol in vacuum and with $138.9/80\approx1.7$ kJ/mol in water, less than $k_BT$. More in the [primer](physics.html#electrostatics).
</div>

There is no dielectric constant in the formula ($\varepsilon_r=1$). Screening by water is produced explicitly by the water molecules reorienting. In the simulation the water molecules are present, as atoms with partial charges, and the Coulomb forces turn them towards the charges around them, as in real water. The screening is therefore a result of the simulation. Putting a factor 80 in the formula as well would count it twice.

Two features make electrostatics the hardest part:

- **It is long-ranged.** $1/r$ decays so slowly that it cannot be truncated without artefacts. Module 7 covers the solution, Ewald summation.
- **It is large.** Two unit charges at 0.3 nm in vacuum interact with 463 kJ/mol, about 186 $k_BT$. Net effects in solution are small differences between large numbers (direct interaction against desolvation), which is one reason binding energies are hard to compute.

*Long-ranged.* Compare the two non-bonded terms when the distance grows from 0.3 nm to 1 nm. The Lennard-Jones attraction, which goes as $r^{-6}$, drops to $0.3^6 = 0.0007$ of its value, while the Coulomb energy, which goes as $1/r$, is still at 0.3 of its value. On top of that, the number of atoms at a distance between $r$ and a little more than $r$ grows as $r^2$, the area of a sphere. If all the charges had the same sign, the atoms in such a shell would together contribute in proportion to $r^2\times1/r = r$, so distant shells would count for more than near ones.

In a real system positive and negative charges largely cancel in every shell, which keeps the total finite. But the cancellation is delicate, and to **truncate** the sum (to leave out all pairs beyond a chosen distance) disturbs it. An **artefact** is a feature of the result that comes from the method and not from the physics.

*Large.* The two numbers are $138.935/0.3 = 463$ kJ/mol and $463/2.494 = 186$. Consider two opposite charges that meet in water. Each is surrounded by water molecules turned the favourable way, and this **solvation** lowers its energy by a large amount. When the two charges come into contact, each gives up part of its water shell, a loss called **desolvation**. The gain from the direct attraction and the loss from desolvation are both large, with opposite signs, and a small relative error in either is a large relative error in their difference.

The force of the Coulomb term is worked out in "From energy to force".

## Which pairs count: exclusions and 1-4 scaling

The non-bonded sum runs over "all pairs", with some exceptions. To see why, apply the Lennard-Jones formula to two bonded carbons, which sit 0.153 nm apart, far inside the repulsive wall. With illustrative values $\sigma = 0.34$ nm and $\varepsilon = 0.4$ kJ/mol, the formula gives $4\times0.4\times[(0.34/0.153)^{12}-(0.34/0.153)^{6}]\approx23{,}000$ kJ/mol. That number means nothing. The Lennard-Jones parameters describe the contact of atoms that are not bonded, and everything about the bonded pair is already in its bond term.

Pairs of atoms in the same molecule are named by counting along the chain of bonds. In a chain 1-2-3-4, atoms 1 and 2 are bonded (a 1-2 pair), atoms 1 and 3 are the two ends of an angle (a 1-3 pair), and atoms 1 and 4 are the two ends of a dihedral (a 1-4 pair).

Atoms separated by one bond (1-2) or two bonds (1-3) are **excluded** from the non-bonded sum, since the bond and angle terms already describe them. Atoms separated by three bonds (1-4, the ends of a dihedral) interact through a scaled non-bonded term:

| Force field | 1-4 Lennard-Jones | 1-4 Coulomb |
|---|---|---|
| AMBER (Cornell et al. 1995 and later; the 1984 force field used 0.5 for both) | × 0.5 | × 1/1.2 = 0.833 |
| OPLS-AA | × 0.5 | × 0.5 |
| CHARMM | × 1 (special 1-4 parameters for some types) | × 1 |
| GROMOS | separate 1-4 parameter list | × 1 |

The 1-3 distance is fixed by two bond lengths and the angle between them, so the bond and angle springs say everything about that pair. The 1-4 pair is different. Its distance changes when the dihedral turns: the two end atoms are closest in the *cis* position and farthest apart in *trans*. The non-bonded energy of the 1-4 pair is therefore a real part of the energy of rotation, and it cannot be dropped.

"Scaled" means multiplied by a fixed factor: an entry "× 0.5" says that the Lennard-Jones energy of every 1-4 pair, and the force that goes with it, is multiplied by 0.5. "Special 1-4 parameters" and "separate 1-4 parameter list" mean that some atom types have a second set of $\sigma$ and $\varepsilon$ that is used only in 1-4 pairs. At the short 1-4 distances the non-bonded formula, whose parameters were made for contacts between separate molecules, is at its least reliable, and each family settled on its own treatment. Pairs that are four or more bonds apart, and all pairs of atoms in different molecules, interact at full strength.

The torsion parameters are fitted together with a particular 1-4 scaling. This is one of several reasons you cannot mix parameters from different force-field families. The energy of rotation about a bond is the sum of the torsion waves and the scaled 1-4 terms, and the torsion constants were chosen last, so that the sum comes out right. As an illustration, suppose that the 1-4 Coulomb energy of some dihedral differs by 20 kJ/mol between *cis* and *trans*. With the factor 0.833 it contributes 16.7 kJ/mol to the rotation energy and with 0.5 only 10 kJ/mol, a difference of 2.7 $k_BT$, the same size as a torsion barrier of a few $k_BT$.

## From energy to force

<div data-videos="BnT6Onll1eQ"></div>

An MD program does not move the atoms with the energy. It moves them with the forces (Module 2). So every term of the force field has to be differentiated once, by hand, and the result is written into the program. This section does that in full for the three pair terms and in outline for angles and dihedrals.

All the terms have the same structure. The energy depends on one internal coordinate (a distance, an angle or a dihedral), and that coordinate depends on the positions of two, three or four atoms. The chain rule then gives the force as a product of two factors: how fast the energy changes with the coordinate, times how fast the coordinate changes when the atom moves. The first factor is the derivative found in each section above. The second is geometry.

MD needs $\mathbf F_i = -\partial U/\partial\mathbf r_i$ for every term. The symbol $\partial U/\partial\mathbf r_i$ is the gradient of $U$ with respect to the position of atom $i$: the vector of the three slopes of $U$ when atom $i$ is moved along $x$, $y$ and $z$ while all other atoms stay where they are (Module 2 and the [toolbox](maths.html#gradient)). For any term that depends on the distance between two atoms (bonds, Lennard-Jones, Coulomb), Module 2 gave

$$
\mathbf F_i = -\frac{dU}{dr}\,\frac{\mathbf r_{ij}}{r_{ij}},\qquad \mathbf F_j=-\mathbf F_i .
$$

<div class="legend" markdown="1">
- $\mathbf F_i$: the force on atom $i$ from this one term, a vector, in kJ mol$^{-1}$ nm$^{-1}$.
- $U$: the energy of the term, a function of the distance $r$ between atoms $i$ and $j$.
- $dU/dr$: the slope of that energy with respect to the distance, taken at the present distance.
- $\mathbf r_{ij}$ (bold): the vector $\mathbf r_i-\mathbf r_j$, which points from atom $j$ to atom $i$.
- $r_{ij}$ (not bold): the length of that vector, the distance between the two atoms. The ratio $\mathbf r_{ij}/r_{ij}$ is a unit vector: it has length 1 and only gives the direction.
- $\mathbf F_j$: the force on the other atom. It is equal and opposite, which is Newton's third law.
</div>

**Read it like this.** The first factor, $-dU/dr$, is one number: the strength of the force. The second factor is the geometry. The distance between two atoms grows fastest when atom $i$ moves straight away from atom $j$, and then it grows exactly as fast as the atom moves (Module 2 derives this). A pair force therefore acts along the line through the two atoms. If $-dU/dr$ is positive, the force on $i$ points away from $j$ (repulsion), and if it is negative, it points towards $j$ (attraction).

### The three pair terms, worked through

**The bond.** The bond section found $dU_b/dr = k_b(r-r_0)$. Put it into the pair formula:

$$
\mathbf F_i = -k_b\,(r_{ij}-r_0)\,\frac{\mathbf r_{ij}}{r_{ij}}
$$

<div class="legend" markdown="1">
- $k_b$, $r_0$: the force constant and the equilibrium length of the bond.
- $r_{ij}$: the present bond length, called $r$ in the bond section.
- Other symbols: as in the list above.
</div>

Example. Put atom $j$ at the origin and atom $i$ on the $x$ axis at 0.163 nm, with $r_0 = 0.153$ nm and $k_b = 2.6\times10^5$ kJ mol$^{-1}$ nm$^{-2}$. The unit vector is $(1,0,0)$ and the stretch is 0.01 nm, so $\mathbf F_i = (-2600, 0, 0)$ kJ mol$^{-1}$ nm$^{-1}$, towards $j$. The force on $j$ is $(+2600, 0, 0)$, towards $i$. The stretched spring pulls both atoms inwards.

**Lennard-Jones.** The Lennard-Jones section found the slope, $dU_{LJ}/dr = 4\varepsilon\,[-12\,\sigma^{12}/r^{13}+6\,\sigma^{6}/r^{7}]$. Two steps bring it to the usual form. First change the sign. Then take the common factor $6/r$ out of the bracket, using $12\,\sigma^{12}/r^{13} = (6/r)\times2(\sigma/r)^{12}$ and $6\,\sigma^{6}/r^{7} = (6/r)\times(\sigma/r)^{6}$. With $4\times6 = 24$ this is the first formula below, and multiplying by the unit vector $\mathbf r_{ij}/r$ brings one more division by $r$ and gives the second.

For Lennard-Jones:

$$
-\frac{dU_{LJ}}{dr} = \frac{24\varepsilon}{r}\left[2\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right]
\quad\Longrightarrow\quad
\mathbf F_i = \frac{24\varepsilon}{r^2}\left[2\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right]\mathbf r_{ij}.
$$

<div class="legend" markdown="1">
- $-dU_{LJ}/dr$: the strength of the Lennard-Jones force along the line between the two atoms, in kJ mol$^{-1}$ nm$^{-1}$. Positive is repulsion, negative is attraction.
- $r$: the distance between the two atoms, short for $r_{ij}$.
- $\varepsilon$, $\sigma$: the well depth and the size parameter of the pair.
- $\Longrightarrow$: "from which it follows".
- $\mathbf F_i$: the force vector on atom $i$.
- $\mathbf r_{ij}$: the vector from atom $j$ to atom $i$.
</div>

**Read it like this.** The sign is decided by the bracket. It is positive at distances below $2^{1/6}\sigma$, where the atoms repel, zero at the minimum of the well, and negative beyond, where they attract. At $r = \sigma$ the bracket is 1 and the repulsive force is $24\,\varepsilon/\sigma$. The attraction is strongest at $r = 1.245\,\sigma$, where the force is $-2.40\,\varepsilon/\sigma$ (question 2 of "Check yourself"). With the illustrative values $\varepsilon = 0.4$ kJ/mol and $\sigma = 0.34$ nm these are 28 and $-2.8$ kJ mol$^{-1}$ nm$^{-1}$, small next to the 2600 of the stretched bond.

Only even powers of $r$ appear, so the Lennard-Jones term on its own needs no square root, which was a real saving in early codes. (In a biomolecular simulation the Coulomb term for the same pair needs $r$ anyway.) For Coulomb, $\mathbf F_i = 138.935\,q_iq_j\,\mathbf r_{ij}/r^3$.

The remark about the square root has the same reason as for the GROMOS bond. The coordinates give $r^2$ directly, and both $(\sigma/r)^6 = (\sigma^2/r^2)^3$ and the factor $24\varepsilon/r^2$ can be computed from it:

```python
r2 = dx*dx + dy*dy + dz*dz               # squared distance; dx, dy, dz = components of r_ij
s6 = (sigma*sigma / r2)**3               # (sigma/r)^6 without a square root
f_over_r2 = 24*eps*(2*s6*s6 - s6) / r2   # the factor in front of the vector r_ij
fx, fy, fz = f_over_r2*dx, f_over_r2*dy, f_over_r2*dz
```

**Coulomb.** Write the energy as $138.935\,q_iq_j\,r^{-1}$. The derivative of $r^{-1}$ is $-r^{-2}$, so $-dU_C/dr = 138.935\,q_iq_j/r^2$. For like charges this is positive, a repulsion, and for opposite charges it is negative, an attraction. Multiplying by the unit vector $\mathbf r_{ij}/r$ gives the vector form quoted above, with $r^3$ underneath.

The $r^3$ does not mean that the force falls off with the cube of the distance. One of the three powers only cancels the length of the vector $\mathbf r_{ij}$. The strength of the force is $138.935\,q_iq_j/r^2$, in kJ mol$^{-1}$ nm$^{-1}$ with charges in $e$ and distances in nm: for two unit charges at 0.3 nm, $138.935/0.09 = 1544$. The odd power $r^3 = r^2\times r$ is why this term needs the distance itself, and so a square root.

### Angles: the chain rule through the angle

The algebra of this subsection can be skipped on a first reading. The paragraph "Read it like this" below says what comes out.

<div class="box maths" markdown="1">
**Maths you need here: the dot product.** The **dot product** of two vectors is the number $\mathbf a\cdot\mathbf b = a_xb_x+a_yb_y+a_zb_z$. It is equal to the product of the two lengths times the cosine of the angle between the vectors. For two unit vectors (vectors of length 1, marked with a hat, $\hat{\mathbf r} = \mathbf r/r$) the dot product is the cosine of the angle between them: 1 if they are parallel, 0 if they are perpendicular, $-1$ if they are opposite. Example: $(1,0,0)\cdot(0.5,0.866,0) = 0.5$, the cosine of 60°. More in the toolbox: [vectors](maths.html#vectors), [the dot product](maths.html#dot-product).
</div>

For angles and dihedrals, use the chain rule through the internal coordinate, $\mathbf F_i = -\dfrac{dU}{d\theta}\dfrac{\partial\theta}{\partial\mathbf r_i}$. For an angle i-j-k with $\cos\theta = \hat{\mathbf r}_{ji}\cdot\hat{\mathbf r}_{jk}$,

$$
\frac{\partial\cos\theta}{\partial\mathbf r_i} = \frac{1}{r_{ji}}\left(\hat{\mathbf r}_{jk} - \cos\theta\,\hat{\mathbf r}_{ji}\right),
\qquad \mathbf F_i = \frac{1}{\sin\theta}\frac{dU}{d\theta}\,\frac{\partial\cos\theta}{\partial\mathbf r_i},
$$

with the analogous expression for $k$, and $\mathbf F_j = -\mathbf F_i-\mathbf F_k$ because internal forces sum to zero.

<div class="legend" markdown="1">
- $\theta$: the angle at atom $j$ between the bonds to $i$ and to $k$.
- $\hat{\mathbf r}_{ji}$, $\hat{\mathbf r}_{jk}$: the unit vectors that point from the middle atom $j$ to atom $i$ and to atom $k$, that is, $\hat{\mathbf r}_{ji} = (\mathbf r_i-\mathbf r_j)/r_{ji}$ and $\hat{\mathbf r}_{jk} = (\mathbf r_k-\mathbf r_j)/r_{jk}$, where $r_{jk}$ is the length of the bond between $j$ and $k$. Take care with the order of the labels: here the first label is the atom where the vector starts, the opposite of the pair-force convention $\mathbf r_{ij} = \mathbf r_i-\mathbf r_j$ used above. With the labels read the other way round, the force would come out with the wrong sign.
- $r_{ji}$: the length of the bond between $j$ and $i$.
- $\partial\theta/\partial\mathbf r_i$, $\partial\cos\theta/\partial\mathbf r_i$: the gradients of $\theta$ and of $\cos\theta$ with respect to the position of atom $i$. Each is a vector that says how the quantity changes when atom $i$ alone is moved.
- $dU/d\theta$: the slope of the angle energy, $k_\theta(\theta-\theta_0)$ for the harmonic term.
- $\sin\theta$: the sine of the angle. It appears when a change of $\cos\theta$ is converted into a change of $\theta$.
- $\mathbf F_i$, $\mathbf F_j$, $\mathbf F_k$: the forces on the three atoms.
</div>

The second formula follows from the chain rule in one step. A program computes $\cos\theta$, not $\theta$, so the gradient of $\cos\theta$ is the natural quantity. The derivative of $\cos\theta$ with respect to $\theta$ is $-\sin\theta$, so a small change of the angle and the change of its cosine are related by $\Delta\cos\theta = -\sin\theta\,\Delta\theta$. This gives $\partial\theta/\partial\mathbf r_i = -(1/\sin\theta)\,\partial\cos\theta/\partial\mathbf r_i$. Put it into $\mathbf F_i = -(dU/d\theta)\,\partial\theta/\partial\mathbf r_i$: the two minus signs cancel and the second formula results.

<details markdown="1"><summary>Optional: where the gradient of the cosine comes from</summary>
Write $\mathbf a = \mathbf r_i-\mathbf r_j$ and $\mathbf b = \mathbf r_k-\mathbf r_j$ for the two bond vectors, with lengths $a = r_{ji}$ and $b = r_{jk}$. Then $\cos\theta = \mathbf a\cdot\mathbf b/(ab)$. Moving atom $i$ changes $\mathbf a$ and leaves $\mathbf b$ alone. Two things in the expression depend on $\mathbf a$.

The dot product on top is $a_xb_x+a_yb_y+a_zb_z$, so its slope along $a_x$ is $b_x$, and its gradient with respect to $\mathbf a$ is the vector $\mathbf b$. The length $a$ underneath has the gradient $\mathbf a/a$ (the result of Module 2 for a distance), and by the power rule and the chain rule the gradient of $1/a$ is $-(1/a^2)\,\mathbf a/a$. The product rule adds the two contributions:

$$
\frac{\partial\cos\theta}{\partial\mathbf r_i} = \frac{\mathbf b}{ab}-\frac{\mathbf a\cdot\mathbf b}{a^2\,b}\,\frac{\mathbf a}{a} = \frac1a\left(\hat{\mathbf b}-\cos\theta\,\hat{\mathbf a}\right).
$$

The last step uses $\hat{\mathbf a} = \mathbf a/a$, $\hat{\mathbf b} = \mathbf b/b$ and $\mathbf a\cdot\mathbf b/(ab) = \cos\theta$. With $a = r_{ji}$, $\hat{\mathbf a} = \hat{\mathbf r}_{ji}$ and $\hat{\mathbf b} = \hat{\mathbf r}_{jk}$ this is the formula above.
</details>

**Read it like this.** The vector in the brackets, $\hat{\mathbf r}_{jk}-\cos\theta\,\hat{\mathbf r}_{ji}$, is what is left of the direction from $j$ to $k$ after its part along the bond j-i has been removed. It lies in the plane of the three atoms, it is perpendicular to the bond j-i, and its length is $\sin\theta$, which cancels the $\sin\theta$ in the denominator. So the force on atom $i$ is perpendicular to its bond, and its size is the torque divided by the bond length, $(dU/d\theta)/r_{ji}$. A long bond is a long lever: the same torque needs a smaller force at its end.

The direction is the one you expect. If the angle is too wide, $dU/d\theta$ is positive and the force on $i$ points to the side where $k$ is, which closes the angle. For the angle of the earlier example, 10° too wide with $k_\theta = 500$ kJ mol$^{-1}$ rad$^{-2}$, the torque is 87 kJ mol$^{-1}$ rad$^{-1}$. With a bond length of 0.153 nm the force on the end atom is $87/0.153 = 570$ kJ mol$^{-1}$ nm$^{-1}$.

"The analogous expression for $k$" is the same formula with the roles of $i$ and $k$ exchanged: $\partial\cos\theta/\partial\mathbf r_k = (1/r_{jk})\,(\hat{\mathbf r}_{ji}-\cos\theta\,\hat{\mathbf r}_{jk})$. The force on the middle atom needs no derivation of its own. The angle energy depends on the shape of the three atoms and not on where they are, so shifting all three by the same small step leaves the energy unchanged. The change of energy in such a shift is minus the sum of the three forces times the step, and it can vanish for every step only if $\mathbf F_i+\mathbf F_j+\mathbf F_k = 0$.

The formula also shows the singularity mentioned in the angle section. At $\theta = 180°$ the three atoms lie on a line, $\sin\theta = 0$, and "perpendicular to the bond, in the plane of the three atoms" is no longer a defined direction. With the GROMOS form $\tfrac12k\,(\cos\theta-\cos\theta_0)^2$ the force is $\mathbf F_i = -k\,(\cos\theta-\cos\theta_0)\,\partial\cos\theta/\partial\mathbf r_i$, with no division by $\sin\theta$.

### Dihedrals in outline

Dihedral forces follow the same route with more algebra. The standard derivation is in the GROMACS reference manual and in Allen and Tildesley. For each of the four atoms, $\mathbf F_i = -(dU/d\phi)\,\partial\phi/\partial\mathbf r_i$. The first factor is the torque from the torsion section, $\sum_n n\,k_{\phi,n}\sin(n\phi-\delta_n)$, and the second is geometry again.

<div class="box maths" markdown="1">
**Maths you need here: the cross product.** The **cross product** $\mathbf a\times\mathbf b$ of two vectors is a third vector that is perpendicular to both. Its length is the product of the two lengths times the sine of the angle between them. Two vectors that lie in a plane therefore give, through their cross product, the direction perpendicular to that plane, which is called the **normal** of the plane. More in the [toolbox](maths.html#cross-product).
</div>

A program finds the dihedral angle in this way. The cross product of the bond vectors i-j and j-k is the normal of the plane (i,j,k), and the cross product of the bond vectors j-k and k-l is the normal of the plane (j,k,l). The angle between the two normals is the angle between the two planes, and that is $\phi$. Its sign says on which side of the first plane atom $l$ lies.

The result of the algebra can be stated in words:

- The force on the end atom $i$ is perpendicular to the plane (i,j,k). Pushing atom $i$ out of that plane is the only way of moving it that changes $\phi$.
- Its size is the torque divided by the distance of atom $i$ from the axis j-k. That distance is $r_{ij}\sin\theta_{ijk}$, where $r_{ij}$ is the length of the bond i-j and $\theta_{ijk}$ is the angle at atom $j$. It is the lever rule again.
- The same holds for the other end atom $l$, with the plane (j,k,l).
- The forces on the two middle atoms are fixed by three conditions: the four forces add up to zero, together they do not set the molecule as a whole spinning, and neither middle force has a part along the central bond (sliding atom $j$ or atom $k$ along the axis j-k does not change $\phi$).

<div class="box key" markdown="1">
**Always test forces numerically.** Move one atom by $\pm h$ along $x$ (with $h\approx10^{-5}$ nm), compute $-[U(x+h)-U(x-h)]/2h$ and compare with the analytic force. This five-line test catches most bugs in a new potential, including in machine-learned force fields.
</div>

The test uses the definition of a derivative: the slope of a curve at a point is close to the slope of the straight line between two nearby points on it. Taking one point on each side, at $x+h$ and $x-h$, is called a **central difference**. $U(x+h)$ is the energy with the atom moved by $h$, $U(x-h)$ the energy with it moved the other way, and $2h$ is the distance between the two positions. The "analytic force" is the one from your formula.

The step $h$ must be neither too large nor too small. If it is too large, the curve bends between the two points and the straight line is a poor estimate of the slope. If it is too small, the two energies agree in almost all of their 16 digits and their difference is lost in round-off. Here is the test for a bond that lies along $x$:

```python
def U(x):                      # bond energy in kJ/mol; x is the bond length in nm
    k, r0 = 2.6e5, 0.153
    return 0.5 * k * (x - r0)**2

def F(x):                      # the analytic force, -dU/dx
    k, r0 = 2.6e5, 0.153
    return -k * (x - r0)

x, h = 0.160, 1e-5
print(F(x), -(U(x + h) - U(x - h)) / (2 * h))   # both print -1820.00000000..., the same to about 12 digits
```

The two numbers agree to better than one part in a billion. A wrong sign, a missing factor 2 or a force constant in the wrong convention would show at once.

## How many terms?

How much work is one evaluation of the whole formula? The answer decides where an MD program spends its time.

A protein with $N_p$ atoms has about $N_p$ bonds, $2N_p$ angles and $3N_p$ dihedrals, all cheap (rigid water adds none). Here $N_p$ is the number of atoms of the protein. The bonded lists grow in proportion to it: a protein twice as large has twice as many terms of each kind. A rigid water molecule is one whose shape is held fixed by constraints (Module 9), so it has no bond or angle term to compute.

The non-bonded sum over a solvated system of $N$ atoms has $N(N-1)/2$ pairs, about $5\times10^9$ for 100,000 atoms. Here $N$ counts all atoms, those of the protein, the water and the ions ("solvated" means surrounded by solvent). Each of the $N$ atoms can be paired with $N-1$ others, which gives $N(N-1)$, and that counts every pair twice, so divide by 2. For $N = 10^5$ the result is $10^5\times99{,}999/2\approx5\times10^9$. The number of pairs grows with the square of the number of atoms: ten times as many atoms means a hundred times as many pairs.

Reducing that to the roughly $2\times10^7$ pairs inside a cutoff, while still treating the long-range part correctly, is the subject of Module 7. A **cutoff** is a distance beyond which the program does not compute a pair directly. A rough count shows where the smaller number comes from. Liquid water contains about 100 atoms per nm$^3$ (33 molecules of three atoms each), so with a cutoff of, say, 1 nm, the sphere around an atom has a volume of $\tfrac43\pi\times1^3 = 4.2$ nm$^3$ and holds about 420 other atoms. That makes $10^5\times420/2\approx2\times10^7$ pairs, more than 200 times fewer than all pairs.

## What this model leaves out

<div data-videos="nO4c0CfZx3k"></div>

The formula is fast because it is simple. This section lists what the simplicity costs.

<div class="box physics" markdown="1">
**Physics you need here: the dipole moment and polarisation.** The **dipole moment** of a molecule measures how far its positive and its negative charge are separated. For two charges $+q$ and $-q$ at a distance $d$ it is $q\,d$. The usual unit is the debye (D), and 1 D is 0.0208 $e$ nm. Two charges of $+0.4\,e$ and $-0.4\,e$ that are 0.1 nm apart have a dipole moment of $0.04\,e$ nm, which is 1.9 D.

**Polarisation** is the response of the electrons to an electric field. The electron cloud of a molecule is not rigid. In the field of its neighbours it shifts a little, and the dipole moment of the molecule changes. A water molecule in liquid water sits in the field of the water molecules around it, so its charges are pulled further apart than in an isolated molecule and its dipole moment is larger. More in the [primer](physics.html#dipoles).
</div>

- **Electronic polarisation.** Charges are fixed, so a molecule has the same charge distribution in water, in a protein interior and at a membrane. Force fields compensate on average by using charges that are larger than in the gas phase. The common rigid water models have dipole moments of about 2.2 to 2.5 D (SPC 2.27, TIP3P and SPC/E 2.35, OPC 2.48 D), against 1.85 D for an isolated water molecule. Polarizable force fields (Module 6) address this at higher cost.
- **Charge transfer and bond breaking.** No chemistry.
- **Many-body dispersion and anisotropy.** Atom-centred charges cannot represent lone pairs, $\pi$ clouds or $\sigma$-holes (halogen bonds) unless extra sites are added.
- **Coupling between terms.** Class II force fields (for materials) add cross terms such as bond-angle coupling. Biomolecular force fields mostly do not (the polarizable AMOEBA force field, which has a bond-angle cross term and anharmonic bonds, is an exception).

Each of the four points uses words that need explaining.

*Electronic polarisation.* The "gas phase" is a molecule on its own, with no neighbours. The water models listed have a dipole moment between 23 and 34 % larger than that of an isolated molecule ($2.27/1.85 = 1.23$ and $2.48/1.85 = 1.34$). The extra amount stands for the polarisation that a water molecule has in the liquid, built into the fixed charges once and for all. "On average" is the weak point: the charges stay the same where the electric field is weaker, such as the interior of a protein or a membrane. A polarizable force field lets the charge distribution of each molecule respond to its surroundings during the run.

*Charge transfer and bond breaking.* The list of bonds is fixed, a harmonic bond cannot break, and every atom keeps its charge. So no electron passes from one molecule to another (charge transfer) and no reaction takes place. That is the meaning of "no chemistry".

*Many-body dispersion and anisotropy.* "Many-body" refers to more than two atoms at once: the model takes the Lennard-Jones energy of three atoms to be the sum of the three pair energies, while in reality the third atom changes the interaction of the other two a little. "Anisotropy" means dependence on direction. A point charge at the nucleus makes an atom look the same from every side, and real atoms in molecules do not.

Three examples are named. A lone pair is a pair of electrons that takes no part in a bond and sticks out to one side of an oxygen or a nitrogen. A $\pi$ cloud is the electron density above and below the plane of a double bond or an aromatic ring. A $\sigma$-hole is a patch of positive potential on a bonded halogen atom, on the side opposite to its bond, which lets the halogen attract a negative atom (this $\sigma$ has nothing to do with the Lennard-Jones $\sigma$).

"Extra sites" are additional point charges that do not sit on a nucleus.

*Coupling between terms.* A **cross term** is an energy term that depends on two internal coordinates at once. A bond-angle cross term has, for example, the form $k_{r\theta}\,(r-r_0)(\theta-\theta_0)$, where $k_{r\theta}$ is a coupling constant. With such a term the preferred length of a bond depends on the angle next to it. CMAP, met in the torsion section, is a cross term between two dihedrals. "Anharmonic bonds" are bond terms with higher powers of the stretch added to the parabola, which brings them closer to the Morse curve.

Each omission is absorbed, as far as possible, into the fitted parameters. That makes the parameters **effective**: they work as a set, in the conditions they were fitted for. An effective parameter is not a property of an atom that could be measured on its own. A charge is larger than the real one to make up for the missing polarisation, and a torsion constant contains corrections for the 1-4 terms. Change one of them, or use the set under conditions far from those of the fit, and the errors that used to cancel no longer do.

## Check yourself

<details markdown="1"><summary>1. Convert the AMBER C-C bond constant K = 310 kcal mol⁻¹ Å⁻² to GROMACS units and convention.</summary>
$k = 2\times310\times4.184\times100 = 259{,}408$ kJ mol$^{-1}$ nm$^{-2}$. The 2 is the convention, 4.184 converts kcal to kJ, 100 converts Å$^{-2}$ to nm$^{-2}$.
</details>

<details markdown="1"><summary>2. At what distance is the Lennard-Jones force zero? Where is it most attractive?</summary>
Zero at the minimum, $r = 2^{1/6}\sigma$. The force $-dU/dr$ has its most negative value where its own slope, which is minus the second derivative $d^2U/dr^2$, is zero. Differentiating $dU/dr = 4\varepsilon\,[-12\,\sigma^{12}r^{-13}+6\,\sigma^{6}r^{-7}]$ once more gives $4\varepsilon\,[156\,\sigma^{12}r^{-14}-42\,\sigma^{6}r^{-8}]$, which vanishes when $r^6 = (156/42)\,\sigma^6 = (26/7)\,\sigma^6$. The most attractive force is where $d^2U/dr^2=0$: $r = (26/7)^{1/6}\sigma \approx 1.245\,\sigma$.
</details>

<details markdown="1"><summary>3. Why is there no explicit dielectric constant of 80 in the Coulomb term of an explicit-solvent simulation?</summary>
The dielectric constant is a macroscopic average of how water dipoles reorient and screen charges. In explicit solvent the water molecules are present and do the screening themselves, so the bare interaction with $\varepsilon_r=1$ is the correct microscopic law. ("Explicit solvent" means that the water molecules are in the simulation as atoms, and an implicit-solvent model leaves them out and represents their effect by a formula.) A dielectric constant appears only in implicit-solvent models (Module 15).
</details>

<details markdown="1"><summary>4. A torsion has a single term with n = 3 and k = 6 kJ/mol. How high is the barrier and how often is it crossed, roughly?</summary>
The barrier is $2k = 12$ kJ/mol $= 4.8\,k_BT$ at 300 K. With an attempt frequency of the order of $10^{12}$ to $10^{13}$ s$^{-1}$, the rate is about $10^{12.5}e^{-4.8}\approx3\times10^{10}$ s$^{-1}$: one crossing every few tens of picoseconds. (The attempt frequency is the number of times per second that the dihedral swings against the barrier, and $e^{-4.8}$ is the Boltzmann factor of the barrier height, the fraction of attempts with enough energy to cross.) Easily sampled.
</details>

<details markdown="1"><summary>5. A bond between two atoms of 14 u and 1 u has a force constant of 4.0 × 10⁵ kJ mol⁻¹ nm⁻² (round values). How far does its length fluctuate at 300 K, and what is its vibration period?</summary>
The fluctuation is $\sqrt{k_BT/k_b} = \sqrt{2.494/(4.0\times10^5)} = 0.0025$ nm. The reduced mass is $\mu = 14\times1/15 = 0.933$ u, and the period is $\tau = 2\pi\sqrt{\mu/k_b} = 2\pi\sqrt{0.933/(4.0\times10^5)} = 0.0096$ ps, or 9.6 fs.
</details>

<details markdown="1"><summary>6. A torsion wave has n = 2, a phase of 180° and k = 10 kJ/mol. Where are its minima, and how high is the barrier between them?</summary>
The wave is $k\,[1+\cos(2\phi-180°)] = k\,[1-\cos2\phi]$. It is zero where $\cos2\phi = 1$, at $\phi = 0°$ and $\phi = 180°$, and it reaches $2k = 20$ kJ/mol at $\phi = \pm90°$. The barrier is 20 kJ/mol, which is 8 $k_BT$ at 300 K. Such a wave keeps four atoms close to one plane.
</details>

<details markdown="1"><summary>7. Two bonded atoms have partial charges of +0.4 e and −0.8 e and are 0.1 nm apart. What does the Coulomb formula give for this pair, and how much of it enters the energy of the simulation?</summary>
The formula gives $138.935\times0.4\times(-0.8)/0.1 = -445$ kJ/mol. None of it enters the energy. Two bonded atoms are a 1-2 pair, and 1-2 pairs are excluded from the non-bonded sum. The bond term describes everything about that pair.
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
