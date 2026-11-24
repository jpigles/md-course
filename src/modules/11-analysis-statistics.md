---
num: 11
title: Analysing trajectories and putting error bars on the results
short: Analysis and statistics
part: Part III · Practice
hours: 8
summary: Compute the standard structural and dynamical observables, and above all estimate their statistical uncertainty from correlated data.
videos: 11
tags: analysis-errors
---

<div class="box goal" markdown="1">
#### After this module you can

- compute RMSD, RMSF, radius of gyration, radial distribution functions, hydrogen bonds and contacts, and say what each means;
- get a diffusion coefficient from the mean squared displacement and correct it for box size;
- compute an autocorrelation time, the number of independent samples and a standard error by block averaging;
- decide how much of a trajectory to discard as equilibration;
- run a principal component analysis and avoid its best-known pitfall.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

A finished simulation is a file of numbers: the positions of all atoms, written out every few picoseconds. Nothing in that file says "the protein is stable" or "this loop is flexible". Analysis turns the file into a few quantities that answer your question, and then states how far each quantity can be trusted.

The second task is the one that is skipped most often. A number without an error bar cannot be compared with an experiment, with another force field or with a mutant, because you cannot tell a real difference from noise. Error bars are harder to get from a simulation than from a set of separate measurements, because every frame of a trajectory resembles the frame before it. Most of the mathematics in this module deals with that one fact.

The module has four layers:

1. **The trajectory and its preparation.** What the file contains, and two repairs it needs before any number is computed from it.
2. **Observables.** The standard measures of structure (RMSD, RMSF, radius of gyration, contacts, the radial distribution function) and of motion (diffusion, time correlation functions): what each one is, how it is computed and what it tells you.
3. **Error bars.** Mean, standard deviation and standard error from the beginning, why correlated frames change the count of samples, and the practical methods: autocorrelation time, block averaging, the bootstrap, independent repeats, and the choice of what to discard as equilibration.
4. **Maps and comparisons.** Principal component analysis, free energies from histograms, and how to compute what an experiment measures.

On a first reading, give layer 3 the most time. The formulas of layer 2 are definitions that a program evaluates for you. The reasoning of layer 3 is work you have to do yourself, for every number you report.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The table collects the notation that this module uses most. Each entry is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $A$, $A(t)$ | Any **observable**: a single number computed from one frame, such as a distance or the radius of gyration. $A(t)$ is its value in the frame at time $t$. |
| $\langle A\rangle$ | Angle brackets: the **average** of $A$. In this module it is an average over the frames of the trajectory and, where the text says so, also over equivalent molecules. |
| $\bar A$ | A bar: the average computed from your finite set of frames. It is used when this must be told apart from the exact average $\langle A\rangle$ that an infinitely long run would give. |
| $\delta A$ | $A-\langle A\rangle$: the deviation of $A$ from its average in one frame, positive in some frames and negative in others. This $\delta$ is not a small step and not a delta function. |
| $\lvert\mathbf v\rvert$ | Bars around a vector: its length, $\sqrt{v_x^2+v_y^2+v_z^2}$. |
| $\sum_{i=1}^{N}$, $\sum_{k\ge1}$ | Add up the expression that follows for every value of the label: from 1 to $N$, or for $k = 1, 2, 3$ and so on. |
| $\int_0^\infty\dots\,dt$ | An integral: the area under the curve that follows, from $t=0$ onwards. |
| $\min_x$ | The smallest value that the expression that follows can take when $x$ is varied. |
| $\to$ | "Approaches", for long times or large distances. |
| $\approx$, $\gg$ | "Approximately equal to" and "much larger than". |
| $\ln$ | The natural logarithm (explained where it is first used). |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** Analysis borrows formulas from structural biology, liquid theory and statistics, and their letters collide.

- $g$: with a distance in brackets, $g(r)$ or $g_{AB}(r)$, it is the radial distribution function. Alone, $g$ is the statistical inefficiency.
- $N$: the number of atoms in the structural formulas, the number of frames in the statistical ones.
- $t$: a time. But $\mathbf t$ (bold) in the RMSD formula is a shift of the whole molecule, and $t_{n-1}$ in the section on repeats is a factor from statistics. $t_0$ is a starting time in the mean squared displacement and the length of the discarded part in the section on equilibration.
- $T$: the temperature in $k_BT$. $T_{sim}$ is the length of the simulation.
- $A$, $B$, $C$: $A$ is an observable. A and B are also the two kinds of particle in $g_{AB}$, and $A$, $B$, $C$ are the constants of the Karplus relation. $B_i$ is a crystallographic B-factor. $C_{AA}(t)$ is a time correlation function, $C_{ab}$ a covariance matrix, and lower-case $c(t)$ the normalised autocorrelation function.
- $n$: a count of particles, a coordination number, or the number of repeated simulations.
- $k$: a lag counted in frames in the statistical formulas, and the number of a principal component in $p_k$.
- $R$: $\mathbf R$ (bold) is a rotation, $R_g$ the radius of gyration, $R_0$ the Förster distance of a pair of dyes.
- $s$ and $S$: $s$ is a standard deviation estimated from a few values, $S^2$ an NMR order parameter.

The lists under the formulas say which is meant each time.
</div>

## A trajectory is a table of numbers

A trajectory file is a sequence of **frames**. One frame holds the three coordinates $x$, $y$, $z$ of every atom at one instant, together with the time and the size of the box. A system of 50,000 atoms saved every 10 ps for 100 ns gives 10,000 frames of 150,000 numbers each. Think of it as a table with 10,000 rows, one per frame, and 150,000 columns.

Nobody reads such a table. An **observable** is a rule that reduces one row to a single number: the distance between two chosen atoms, the number of hydrogen bonds, the size of the protein. Applying the rule to every frame gives a **time series** $A_1, A_2, \dots, A_N$, one value per frame, where $N$ is the number of frames. Everything in this module is done either to one frame (compute an observable) or to a time series (summarise it).

The first summary of a time series is its average. [Module 3](03-statistical-mechanics.html) gave the reason: an experiment measures an average over a huge number of molecules, and the ergodic hypothesis says that the average along a long enough trajectory equals it. The second summary is the size of the fluctuations around the average. Both are defined in the box.

<div class="box maths" markdown="1">
**Maths you need here: mean, variance and standard deviation.** Take five values of a distance, in nm: 1.0, 1.2, 0.9, 1.1, 1.3.

The **mean** is the sum divided by the count: $(1.0+1.2+0.9+1.1+1.3)/5 = 1.1$ nm. It is written $\langle A\rangle$ or $\bar A$.

The **deviations** from the mean are $-0.1$, $0.1$, $-0.2$, $0$ and $0.2$ nm. Their own mean is always zero, because the positive and the negative ones cancel, so it cannot measure the spread. Square them first, which makes all of them positive: 0.01, 0.01, 0.04, 0 and 0.04. The mean of the squares, $0.10/5 = 0.02$ nm$^2$, is the **variance**, written $\langle\delta A^2\rangle$ or $\sigma^2$.

The square root of the variance, $\sqrt{0.02} = 0.14$ nm, is the **standard deviation** $\sigma$ (Greek sigma). It has the unit of the data, and it is the typical distance of one value from the mean. For data with a bell-shaped (Gaussian) distribution, about two thirds of the values lie within one $\sigma$ of the mean and about 95 % within two.

"Root mean square" (RMS), which appears in the names RMSD and RMSF, is the same recipe read from right to left: square, take the mean, take the root.

One detail: when the mean was computed from the same few values, dividing the sum of squares by the count minus one ($0.10/4 = 0.025$, root 0.16 nm) gives a better estimate of the spread, and this version is written $s$. With thousands of frames the two versions agree, with five values they differ by 12 %. More in the [toolbox](maths.html#averages).
</div>

The standard deviation describes the molecule: how much the distance fluctuates. It does not say how well you know the mean. That is a different number, the standard error, and it is the subject of the section on statistical error.

## Before any analysis

The raw trajectory contains two things that are real in the file and are not the motion you want to study: molecules cut by the box, and the tumbling of the whole solute.

Two bookkeeping steps come first. **Make molecules whole and centre the solute**: periodic wrapping splits molecules across the box in the raw trajectory, and distances computed on such frames are wrong. **Remove overall rotation and translation** by least-squares fitting each frame to a reference when you want internal motion. The tools are `gmx trjconv`, MDAnalysis transformations, or `cpptraj autoimage`.

### Why molecules look broken in the raw file

A simulation uses periodic boundary conditions ([Module 7](07-boundaries-electrostatics.html)): the box is surrounded by copies of itself, and an atom that leaves through one face comes back in through the opposite one. The raw trajectory can store every atom at its position inside the central box, which is called "wrapped". A protein that has drifted across a face is then written with one part at one side of the box and the rest at the other side. The simulation is not wrong: together with its periodic copies the molecule is intact. A program that reads the stored coordinates and computes ordinary distances, however, sees a molecule torn in two.

A small example. The box is 5 nm long, and two bonded atoms are stored at $x = 4.9$ nm and $x = 0.2$ nm, because the second one crossed the face and was wrapped. The stored coordinates give a distance of 4.7 nm. The real distance, through the face, is $0.2 + 5 - 4.9 = 0.3$ nm.

"Making a molecule whole" shifts atoms by whole box lengths until every molecule is in one piece. "Centring" then puts the solute in the middle of the box, with the solvent wrapped around it, so that pictures and distances to the solvent make sense.

### Why the overall motion is removed

A protein in water drifts and tumbles as a whole. If you compare the positions of its atoms in two frames directly, almost all of the difference comes from this rigid-body motion, and it says nothing about a change of shape. **Fitting** (also called superposition or alignment) moves and turns each frame as a rigid body until it lies as well as possible on a reference structure, usually the starting structure. "As well as possible" is meant in the least-squares sense of the box. The formula comes with the RMSD below.

<div class="box maths" markdown="1">
**Maths you need here: least squares.** To fit something "in the least-squares sense" means: choose the adjustable quantities so that the sum of the squared mismatches is as small as possible.

The smallest example: find the single number $c$ that lies closest to the three values 1, 2 and 6. The sum of squared mismatches is $(1-c)^2+(2-c)^2+(6-c)^2$. At its minimum the derivative with respect to $c$ is zero: $-2(1-c)-2(2-c)-2(6-c) = 0$, which gives $3c = 9$ and $c = 3$.

That is the mean of the three values. So the mean is the least-squares fit of one number to a set of values, and a superposition is the least-squares fit of a rotation and a shift to a set of atoms. More in the [toolbox](maths.html#fitting).
</div>

Fit when the quantity depends on positions in space and you want the internal motion: RMSD, RMSF and principal component analysis. Do not fit for quantities that describe the motion of the whole molecule, such as its diffusion. Quantities built only from distances inside the molecule (the radius of gyration, contacts, hydrogen bonds) do not change when the molecule is turned or shifted, so they need no fit. They do need whole molecules.

### Where periodic boundaries still cause errors in analysis

Many wrong numbers in a first analysis come from the periodic box. The usual cases:

- **A sudden jump in a time series.** If the RMSD, the radius of gyration or a distance inside a molecule jumps by something like a box length from one frame to the next, a molecule is broken. A protein does not change its size by nanometres between two saved frames.
- **Two molecules in different copies.** A protein and its ligand, or the two chains of a complex, can each be whole and still be stored in different periodic copies. Their distance then looks like several nanometres although they are in contact. Make the complex whole as one unit, or use the **minimum-image distance**: the shortest distance between one molecule and any periodic copy of the other.
- **Distances longer than half the box.** In a cubic box of edge $L$, a partner that is further away than $L/2$ along an axis has a periodic copy that is closer. When the nearest copy is always taken, a spherical shell of radius larger than $L/2$ is cut off by the faces of the box and is no longer complete, so a radial distribution function is computed only up to half the box edge. (A distance inside one whole molecule can be longer than $L/2$ and is still correct.)
- **Diffusion.** The mean squared displacement needs coordinates in which molecules are *not* wrapped back into the box (see the section on diffusion).
- **The order of the repairs.** Do the periodic repairs first and the fit second. The fit rotates the coordinates, and after that the box no longer matches them.

After the repairs, look at the trajectory in a molecular viewer before you compute anything.

## Structural observables

<div data-videos="whO1h7rAMSs 42-bolWBrBM UvH-h9i03rM"></div>

A structural observable is computed from the positions in one frame. Each one compresses the frame into one number or a few, and each answers a different question:

| Observable | The question it answers | One value per |
|---|---|---|
| RMSD | How far is this frame from a reference structure? | frame |
| RMSF | How much does this atom move about its average position? | atom |
| Radius of gyration | How compact is the molecule? | frame |
| Contacts, hydrogen bonds | Which parts touch? | frame (a count) |
| Solvent-accessible surface area | How much of the molecule can the solvent reach? | frame |
| Radial distribution function | How are particles of one kind arranged around particles of another kind? | distance |

### RMSD: how far from a reference

Lay the frame over a reference structure as well as you can. For each atom, measure how far it lies from its partner in the reference. Summarise these distances by their root mean square. The result is one number per frame that says how different the two structures are.

**RMSD**, the root mean square deviation from a reference structure after optimal superposition:

$$
\mathrm{RMSD}(t) = \min_{\mathbf R,\mathbf t}\sqrt{\frac1N\sum_{i=1}^N\big|\mathbf R\,\mathbf r_i(t)+\mathbf t-\mathbf r_i^{ref}\big|^2}.
$$

<div class="legend" markdown="1">
- $\mathrm{RMSD}(t)$: the result for the frame at time $t$, a length in nm (often reported in ångström, Å; 1 nm = 10 Å).
- $N$: the number of atoms included, for example all backbone atoms or all C$\alpha$ atoms. Here $N$ is not the number of frames.
- $i$: the label of one atom, from 1 to $N$. $\sum_{i=1}^N$ adds up over these atoms.
- $\mathbf r_i(t)$: the position of atom $i$ in the frame at time $t$, a vector of three numbers.
- $\mathbf r_i^{ref}$: the position of the same atom in the reference structure. "ref" is a label, not a power.
- $\mathbf R$: a rotation, written as a $3\times3$ matrix (a table of nine numbers). $\mathbf R\,\mathbf r_i$ is the position of atom $i$ after the whole frame has been turned.
- $\mathbf t$: a shift (translation), one vector that is added to every atom. It is not a time.
- $\big|\ \ \big|^2$: the squared length of the vector between the bars. Here it is the squared distance between atom $i$, after turning and shifting, and its reference position.
- $\frac1N\sum$ and $\sqrt{\ \ }$: the mean of the squared distances, and then its root.
- $\min_{\mathbf R,\mathbf t}$: of all possible rotations and shifts, use the one that makes the result smallest. This is the "optimal superposition".
</div>

Read it like this, from the inside out. Turn the frame by $\mathbf R$ and shift it by $\mathbf t$. For each atom take the squared distance to its reference position. Average over the atoms and take the root. Among all possible turns and shifts, keep the one that gives the smallest result.

A small example: after the fit, three atoms lie 0.1, 0.2 and 0.2 nm from their reference positions. The RMSD is $\sqrt{(0.01+0.04+0.04)/3} = \sqrt{0.03} = 0.17$ nm. Because the distances are squared before they are averaged, large deviations count more than small ones. Nine atoms that are off by 0.1 nm and one loop atom that is off by 1.0 nm give an RMSD of 0.33 nm, although the plain average deviation is 0.19 nm. The same RMSD can therefore come from a small change everywhere or from a large change in one place.

How is the best fit found? The shift is the easy part: the best superposition puts the centre of the frame (the mean position of the chosen atoms) on the centre of the reference. Both sets of coordinates are therefore first "centred", which means that the centre is subtracted from every position.

The optimal rotation $\mathbf R$ comes from the singular value decomposition of the $3\times3$ covariance matrix of the two centred coordinate sets (the Kabsch algorithm). That matrix is a table of nine numbers: for each pair of axes, such as $x$ in the frame and $y$ in the reference, the sum over the atoms of the product of the two coordinates. Singular value decomposition is a standard matrix operation, related to finding eigenvectors, that every numerical library provides. You will not do this by hand, because every analysis program does the fit for you.

What you do choose is the set of atoms. A common practice is to fit on the backbone of the rigid part of a protein and then to compute the RMSD of a loop or a ligand without fitting again. The result tells you how the loop or the ligand moved relative to the rest.

RMSD compresses 3N coordinates into one number: two very different structures can have the same RMSD from the reference. A plateau in RMSD shows the structure stopped drifting away from the start. It does not show that sampling has converged.

The first statement has an everyday counterpart. Two towns that are both 100 km from yours can be 200 km from each other, one to the north and one to the south. A structure has $3N$ coordinates, so it has far more "directions" than a map.

For the second statement you need the word **converged**: sampling has converged when running longer would not change your averages, because all the relevant conformations have been visited many times and in the right proportions. A flat RMSD says only that the structure stays at about the same distance from the start. It may be wandering among many conformations at that distance, or it may be stuck in one.

### RMSF: which parts move

The RMSD gives one number per frame, about the whole molecule. The RMSF gives one number per atom, about the whole trajectory: the typical distance of that atom from its own average position. In the language of the maths box above, it is the standard deviation of the position of the atom.

**RMSF**, the fluctuation of each atom about its mean position, $\mathrm{RMSF}_i = \sqrt{\langle|\mathbf r_i-\langle\mathbf r_i\rangle|^2\rangle}$. It shows which parts are flexible, and compares with crystallographic B-factors through $B_i = \tfrac{8\pi^2}{3}\mathrm{RMSF}_i^2$.

<div class="legend" markdown="1">
- $\mathrm{RMSF}_i$: the root mean square fluctuation of atom $i$, in nm. There is one value per atom. It is often reported per residue, using the C$\alpha$ atom.
- $\mathbf r_i$: the position of atom $i$ in one frame, after the frame has been fitted to the reference.
- $\langle\mathbf r_i\rangle$ (inner brackets): the mean position of atom $i$ over all frames.
- $|\mathbf r_i-\langle\mathbf r_i\rangle|^2$: the squared distance of the atom from its mean position in one frame.
- The outer $\langle\ \rangle$: the average of that squared distance over all frames. The root comes last.
- $B_i$: the crystallographic B-factor of atom $i$ (see the box below).
- $\tfrac{8\pi^2}{3}$: a pure number, 26.3.
</div>

The RMSF is computed in three passes over the trajectory. Fit every frame to the reference. Average the position of each atom over all frames. Then average the squared distance of the atom from that mean position and take the root. Without the fit, the result would measure the tumbling of the whole molecule.

The usual picture is a plot of RMSF against residue number. It is low in the tightly packed parts of a protein and has peaks at loops and at the two ends of the chain.

<div class="box physics" markdown="1">
**Physics you need here: the crystallographic B-factor.** An X-ray crystal structure reports, for each atom, a position and a B-factor (also called the temperature factor). In the electron density the atom is not a point. It is smeared over a small region, because the atom vibrates and because the many copies of the molecule in the crystal are not perfectly identical. The B-factor measures the size of the smear, in Å$^2$.

Its relation to the fluctuation is the formula above: $B$ is $\tfrac{8\pi^2}{3}$ times the mean squared displacement of the atom from its mean position, and that mean squared displacement is the RMSF squared. An RMSF of 0.05 nm = 0.5 Å gives $B = 26.3\times0.5^2 = 6.6$ Å$^2$. An RMSF of 0.1 nm = 1 Å gives 26.3 Å$^2$. Convert the RMSF to Å before you use the formula, because B-factors in structure files are in Å$^2$.

Compare the pattern along the chain (which residues are high and which are low) more than the absolute values. A crystal also contains *static disorder*: copies of the molecule that are frozen in slightly different conformations, which raises $B$ without any motion. A simulation in solution has none of that.
</div>

### Radius of gyration: how compact

The radius of gyration says how far the mass of a molecule is spread out around its centre. A compact globule has a small radius of gyration. The same chain stretched out has a large one.

**Radius of gyration**, the overall size:

$$
R_g^2 = \frac{\sum_im_i|\mathbf r_i-\mathbf r_{cm}|^2}{\sum_im_i}.
$$

<div class="legend" markdown="1">
- $R_g$: the radius of gyration, in nm. The formula gives its square, so take the root at the end.
- $i$: the label of one atom. Both sums run over all atoms of the molecule, or of the part you selected.
- $m_i$: the mass of atom $i$, in atomic mass units (u).
- $\mathbf r_i$: the position of atom $i$ in the frame.
- $\mathbf r_{cm}$: the centre of mass of the molecule in that frame, the mass-weighted mean position $\sum_im_i\mathbf r_i/\sum_im_i$.
- $|\mathbf r_i-\mathbf r_{cm}|^2$: the squared distance of atom $i$ from the centre of mass.
- $\sum_im_i$ in the denominator: the total mass. Dividing by it turns the sum into a mass-weighted mean.
</div>

Read it like this: $R_g$ is the root mean square distance of the atoms from the centre of mass, with each atom counted in proportion to its mass. Three examples with equal masses:

- Two atoms 1 nm apart. The centre is halfway, each atom is 0.5 nm from it, and $R_g = 0.5$ nm.
- Three atoms on a line at 0, 1 and 2 nm. The centre is at 1 nm, the squared distances are 1, 0 and 1 nm$^2$, their mean is $2/3$, and $R_g = \sqrt{2/3} = 0.82$ nm.
- A solid ball of uniform density and radius $R$ has $R_g = \sqrt{3/5}\,R = 0.77R$. It is smaller than the radius because most of the mass lies inside, not at the surface. A globular protein that fills a ball of radius 2 nm therefore has $R_g$ near 1.5 nm.

For the same number of atoms, a more extended shape has a larger $R_g$. The radius of gyration depends only on distances inside the molecule, so it needs no fit to a reference. It does need a whole molecule.

The main observable for disordered proteins, directly comparable with SAXS. A disordered protein has no single fold, so a distance from a reference structure means little for it. The average $R_g$ and the shape of its distribution describe the whole set of conformations. SAXS is small-angle X-ray scattering: X-rays are scattered by the molecules in a solution, and the way the scattered intensity falls off at the smallest angles gives the average $R_g^2$ of the molecules. So compare the experiment with the root of the average of $R_g^2$ over the frames, not with the average of $R_g$. For a stricter comparison, compute the scattering curve itself, as in the table of the section "Comparing with experiment".

### Contacts and hydrogen bonds

Many questions about a structure are questions about which parts touch: is this helix still packed against that sheet, is the ligand still in its pocket, how many hydrogen bonds hold the hairpin together. A contact turns a continuous distance into a yes or a no, which can be counted.

**Contacts and hydrogen bonds.** A contact is usually a pair of heavy atoms closer than 0.45 nm, or C$\alpha$ atoms closer than 0.8 nm. A hydrogen bond is counted by geometry: donor-acceptor distance below 0.35 nm and hydrogen-donor-acceptor angle below 30°. The **fraction of native contacts** $Q$ is the fraction of contacts present in a reference structure that are formed in a frame, and is the standard coordinate for folding and binding.

A **heavy atom** is any atom other than hydrogen. The C$\alpha$ atom is the central carbon of an amino-acid residue, one per residue, so a C$\alpha$ contact is a contact between two residues. The count you get depends on the cut-off distance. State the cut-off, and use the same one for all the systems you compare.

<div class="box physics" markdown="1">
**Physics you need here: the hydrogen bond.** A hydrogen atom bonded to nitrogen or oxygen carries a partial positive charge. When it points at another oxygen or nitrogen, which carries a partial negative charge, the two attract. The atom that holds the hydrogen is the **donor** (D), the atom it points at is the **acceptor** (A), and the arrangement D-H···A is a hydrogen bond. It is strongest when the three atoms lie nearly on a line. More in the [primer](physics.html#intermolecular).

A simulation does not label hydrogen bonds. You decide afterwards, from the geometry of each frame, whether a donor and an acceptor count as bonded. The two conditions in the text do this. The distance condition says that D and A are close. The angle is measured at the donor, between the direction to its hydrogen and the direction to the acceptor: it is 0° when the hydrogen lies exactly on the line from D to A, and "below 30°" means that the hydrogen points nearly straight at the acceptor.

The two numbers of the text are one common convention, not a law of nature. Other definitions in use have other cut-offs, or measure the angle at the hydrogen (donor-hydrogen-acceptor, which is near 180° for a straight bond). The number of hydrogen bonds you count depends on the definition, so state the one you used and use the same one for everything you compare.
</div>

For $Q$, first list the contacts in the reference structure. For a protein this is usually the **native** structure, the folded form found by experiment. Then count, in each frame, how many contacts of that list are present.

If the reference has 100 contacts and 80 of them are present in a frame, $Q = 0.8$. $Q$ runs from 0 (none of the reference contacts) to 1 (all of them). Contacts in the frame that are not on the list do not count.

A "coordinate" in the last sentence of the definition is a single number that follows the progress of a process. For folding, $Q$ rises from near 0 to near 1. For binding, the same count is made with the contacts between the two partners.

### Other structural measures

**Solvent-accessible surface area**, **secondary structure** (DSSP), and specific distances and dihedral angles complete the usual set.

- **Solvent-accessible surface area (SASA).** Roll a sphere the size of a water molecule (a radius of about 0.14 nm is the usual choice) over the surface of the molecule. The area traced out by the centre of the sphere is the SASA, in nm$^2$. Per residue, it says whether the residue is buried or exposed. For a complex of two molecules, the area that binding hides from the solvent is the SASA of the two separate partners added together, minus the SASA of the complex.
- **Secondary structure.** The local shape of the protein backbone: helix, strand, turn or irregular coil. DSSP is a widely used program that assigns one of these classes to every residue from the pattern of hydrogen bonds between backbone groups. Applied to every frame, it shows when and where a helix frays or a strand forms.
- **A specific distance.** The distance between two chosen atoms, or between the centres of two groups, is the most direct way to follow one event, such as a salt bridge that opens or a ligand that leaves.
- **A dihedral angle.** Four atoms bonded in a row, a-b-c-d, define the angle by which the bond c-d is rotated about the bond b-c relative to the bond a-b. It runs from $-180$° to 180°. The backbone angles $\phi$ and $\psi$ and the side-chain angles $\chi$ are dihedral angles. Take care when you average an angle: $-179$° and 179° are two degrees apart, but their plain mean is 0°.

### Radial distribution function

<div data-videos="FqqPhoyRCCM X0vdXv7aTvk DMQifMiY_oI fw6feNSZ4jE"></div>

A liquid has no fixed structure, but it is not random either. Around any molecule, the neighbours keep preferred distances. The radial distribution function describes this average arrangement.

The picture: sit on one particle of kind A, say a sodium ion. Draw a thin spherical shell of radius $r$ around it and count the particles of kind B, say water oxygens, inside the shell. Average the count over all A particles and all frames. Then divide by the count you would expect if B were spread evenly through the box. The ratio is $g$ at that distance.

For particles of types A and B, $g_{AB}(r)$ is the density of B at distance $r$ from an A, divided by the bulk density of B:

$$
g_{AB}(r) = \frac{\langle n_B(r,r+dr)\rangle}{4\pi r^2\,dr\;\rho_B}.
$$

<div class="legend" markdown="1">
- $g_{AB}(r)$: the radial distribution function, a pure number with no unit. It is not the statistical inefficiency $g$ of the later sections.
- A, B: two kinds of particle, for example sodium ions and water oxygens. They can be the same kind (oxygen around oxygen).
- $r$: the distance from the central A particle, in nm.
- $dr$: the thickness of the shell. In practice it is the bin width of a histogram of distances, a small fraction of an atomic diameter.
- $n_B(r,r+dr)$: the number of B particles whose distance from the central A lies between $r$ and $r+dr$, in one frame.
- $\langle\ \rangle$: the average over all A particles and over all frames.
- $4\pi r^2\,dr$: the volume of the shell, which is the surface area of a sphere, $4\pi r^2$, times the thickness.
- $\rho_B$ (Greek rho): the bulk number density of B, the number of B particles divided by the volume of the box, in nm$^{-3}$.
</div>

Read it like this. The numerator is what you count. The denominator is what an evenly spread fluid would give: density times the volume of the shell. So $g = 1$ means "as crowded as the average", $g = 2$ means "twice as crowded", and $g = 0$ means "never found here". At very short distances $g$ is 0, because two atoms cannot overlap.

A numerical example. Liquid water has about 33 molecules per nm$^3$. Take the shell between 0.27 and 0.29 nm around a water oxygen. Its volume is $4\pi\times0.28^2\times0.02 = 0.0197$ nm$^3$, so an evenly spread fluid would put $33\times0.0197 = 0.65$ oxygens in it. If the simulation finds, say, 1.6 on average, then $g = 1.6/0.65 = 2.5$ at this distance.

It tends to 1 at large $r$. Far from the central particle its influence is gone, and the density is the average one.

Peaks are solvation shells. The first peak holds the nearest neighbours, which touch the central particle. After it comes a minimum, a distance at which a neighbour would fit neither in the first layer nor in the second. The second peak is the second layer, and each further peak is lower and broader than the one before.

<div class="box maths" markdown="1">
**Maths you need here: an integral as a sum of thin slices.** The integral $\int_a^b f(r)\,dr$ is what you get when you cut the range from $a$ to $b$ into thin slices of width $dr$, multiply the value of $f$ in each slice by the width, and add up. Example: a ball of radius $R$ is a set of nested shells, each of volume $4\pi r^2\,dr$. Adding them up gives $\int_0^R4\pi r^2\,dr = \tfrac43\pi R^3$, the volume of the ball. More in the [toolbox](maths.html#integral).
</div>

The integral up to the first minimum gives the coordination number, $n = 4\pi\rho_B\int_0^{r_{min}}g(r)\,r^2dr$.

<div class="legend" markdown="1">
- $n$: the coordination number, the average number of B particles in the first shell around an A.
- $r_{min}$: the distance of the first minimum of $g(r)$, the outer edge of the first shell.
- $\int_0^{r_{min}}\dots dr$: add up over all thin shells from the centre out to $r_{min}$.
- $g(r)\,r^2$: the radial distribution function times the factor $r^2$ that comes from the volume of each shell.
- $4\pi\rho_B$: the remaining constant factors of the shell volume and the bulk density.
</div>

The formula follows from the definition in one step. Multiply both sides of the definition by the denominator: the average number of B particles in one thin shell is $\rho_B\,g(r)\,4\pi r^2\,dr$. Adding this up over the shells from 0 to $r_{min}$ gives $n$. A check: for an evenly spread fluid, $g = 1$ everywhere, the integral is $r_{min}^3/3$ and $n = \rho_B\times\tfrac43\pi r_{min}^3$, the density times the volume of a ball, as it must be.

<div class="box maths" markdown="1">
**Maths you need here: the natural logarithm.** The logarithm $\ln$ undoes the exponential: if $y = e^x$ then $x = \ln y$. Here $e = 2.718$ is a fixed number, and $e^x$ is that number raised to the power $x$. Three values to remember: $\ln 1 = 0$, $\ln 2 = 0.69$, $\ln 10 = 2.30$. The logarithm of a number above 1 is positive and that of a number between 0 and 1 is negative.

Two rules do most of the work: $\ln(ab) = \ln a+\ln b$ and $\ln(a/b) = \ln a-\ln b$. So $\ln 100 = 2\ln 10 = 4.61$ and $\ln(1/2) = -0.69$. In this module the logarithm turns a ratio of probabilities into a difference of free energies. More in the [toolbox](maths.html#exp-log).
</div>

And $w(r) = -k_BT\ln g(r)$ is the potential of mean force between the two species (Module 3).

<div class="legend" markdown="1">
- $w(r)$: the potential of mean force, in kJ/mol. It is the free energy of the pair as a function of their distance, with the positions of all other molecules averaged out, and it is zero at large distance.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature, in kelvin. $k_BT = 2.494$ kJ/mol at 300 K.
- $\ln g(r)$: the natural logarithm of the radial distribution function at that distance.
- The minus sign: where the pair is found more often than average, the free energy is lower.
</div>

The reason for the logarithm is the Boltzmann rule of [Module 3](03-statistical-mechanics.html): the probability of an arrangement is proportional to $e^{-w/k_BT}$. Since $g$ is the probability of the distance $r$ relative to an even spread, $g(r) = e^{-w(r)/k_BT}$. Taking the logarithm of both sides gives $\ln g = -w/k_BT$, and multiplying by $-k_BT$ gives the formula. In numbers, at 300 K: a peak with $g = 3$ is a well of $-2.494\times\ln3 = -2.7$ kJ/mol, a minimum with $g = 0.5$ is a barrier of $+1.7$ kJ/mol, and $g = 1$ gives $w = 0$.

$g(r)$ is measured by X-ray and neutron scattering, which makes it a primary test of water and ion models. A scattering experiment does not see single molecules. It sees the average arrangement of pairs of atoms, which is what $g(r)$ describes.

## Dynamical observables

<div data-videos="3b6ZM21PmPU rWoV7HoufdA Mm1WfLi86-0 nuAs_GlCdDU"></div>

A structural observable uses one frame at a time. You could shuffle the frames and get the same RMSF and the same $g(r)$. A dynamical observable asks how fast things change, so it compares frames that are a certain time apart, and the order of the frames and the time between them matter.

### Diffusion: how far molecules travel

A molecule in a liquid collides with its neighbours all the time and changes direction at every collision. Its path is a **random walk**. A random walker does not get far: the distance from the starting point grows only as the square root of the time. The diffusion coefficient $D$ measures how fast a molecule spreads in this way.

<div class="box maths" markdown="1">
**Maths you need here: the random walk.** A walker takes steps of length $a$ along a line, each one to the left or to the right with equal probability. After $n$ steps the position is the sum of the steps, $x_n = s_1+s_2+\dots+s_n$, where each $s_k$ is $+a$ or $-a$.

Averaged over many walkers, $\langle x_n\rangle = 0$: there is no preferred direction. Now square the position. The square of a sum contains every step squared and every product of two different steps:

$$
x_n^2 = \sum_k s_k^2 + \sum_{k\ne l}s_k s_l .
$$

Each $s_k^2$ equals $a^2$. Each product $s_ks_l$ of two different steps is $+a^2$ or $-a^2$ with equal probability, because the steps are independent, so its average is zero. What remains is $\langle x_n^2\rangle = n\,a^2$.

The mean squared displacement grows in proportion to the number of steps, that is, to the time. The typical distance, $\sqrt{\langle x_n^2\rangle} = a\sqrt n$, grows only as the square root: 100 steps take the walker about 10 step lengths away, 400 steps about 20. A test with 10,000 walkers on a computer gave $\langle x_n^2\rangle = 100.5\,a^2$ after 100 steps and $401\,a^2$ after 400. More in the [toolbox](maths.html#random-numbers) and the [primer](physics.html#diffusion).
</div>

**Diffusion.** The mean squared displacement grows linearly at long times (Einstein relation):

$$
\mathrm{MSD}(t) = \big\langle|\mathbf r(t_0+t)-\mathbf r(t_0)|^2\big\rangle \;\to\; 6Dt .
$$

<div class="legend" markdown="1">
- $\mathrm{MSD}(t)$: the mean squared displacement over a time interval of length $t$, in nm$^2$.
- $t$: the length of the interval (the "lag time"). It is not the time since the start of the simulation.
- $t_0$: the starting time of one interval (a "time origin").
- $\mathbf r(t_0)$, $\mathbf r(t_0+t)$: the position of one molecule, usually its centre of mass, at the start and at the end of the interval.
- $|\ \ |^2$: the squared length of the displacement between the two positions.
- $\langle\ \rangle$: the average over all starting times $t_0$ in the trajectory and over all molecules of the same kind.
- $\to$: "approaches, when $t$ is long".
- $D$: the diffusion coefficient, in nm$^2$ ps$^{-1}$. In the units of the experimental literature, 1 nm$^2$ ps$^{-1}$ = $10^{-2}$ cm$^2$ s$^{-1}$.
- $6$: two times the number of dimensions. Each of the directions $x$, $y$ and $z$ contributes $2Dt$.
</div>

Read it like this. For every pair of frames a time $t$ apart, ask how far each molecule has moved, square the distance and average. Plot the result against $t$. At long times the plot is a straight line, and its slope is $6D$.

The 6 comes from the random walk. In one dimension the maths box above gives $\langle x^2\rangle$ proportional to the time, and the constant of proportionality is written $2D$, which defines $D$. The motions along $x$, $y$ and $z$ are independent and their squared displacements add, so in three dimensions the mean squared displacement is $3\times2Dt = 6Dt$.

A numerical example. Suppose the MSD of the molecules rises from 0.6 nm$^2$ at $t = 50$ ps to 3.0 nm$^2$ at 250 ps. The slope is $2.4/200 = 0.012$ nm$^2$/ps, so $D = 0.012/6 = 0.002$ nm$^2$/ps, which is $2\times10^{-5}$ cm$^2$/s (a round value of the order of that of liquid water at room temperature). With this $D$, a molecule moves by a root mean square distance of $\sqrt{6\times0.002\times1000} = 3.5$ nm in one nanosecond.

Fit the linear part, not the short-time ballistic part. "Ballistic" describes the first fraction of a picosecond, before the molecule has collided with anything. It flies in a straight line at its velocity $v$, its displacement is $vt$, and the MSD grows as $t^2$, a curve and not a line. A straight line fitted there gives a wrong $D$.

At the longest lag times the MSD is also unusable, for a different reason: few intervals of that length fit into the trajectory, so the average is noisy. Fit a line by least squares over the range in between, and check on the plot that the MSD is straight there.

Equivalently, by the Green-Kubo relation, $D = \tfrac13\int_0^\infty\langle\mathbf v(0)\cdot\mathbf v(t)\rangle\,dt$.

<div class="legend" markdown="1">
- $\mathbf v(0)$, $\mathbf v(t)$: the velocity of one molecule at a starting time, called 0, and a time $t$ later.
- $\mathbf v(0)\cdot\mathbf v(t)$: the dot product of the two velocities, $v_x(0)v_x(t)+v_y(0)v_y(t)+v_z(0)v_z(t)$. It is positive when the molecule still moves in roughly the same direction and negative when it has turned back.
- $\langle\ \rangle$: the average over all starting times and all molecules. The averaged quantity is called the velocity autocorrelation function.
- $\int_0^\infty\dots dt$: the area under that function.
- $\tfrac13$: one over the number of dimensions.
</div>

In words: the diffusion coefficient is one third of the area under the velocity autocorrelation function. That function starts at the mean squared velocity and decays to zero as collisions erase the memory of the initial velocity. A molecule that keeps its direction for longer travels further before it turns, the area is larger, and $D$ is larger. This route needs velocities saved every few femtoseconds, which ordinary trajectories do not contain, so the MSD is the usual route.

<details markdown="1"><summary>Optional: why the two formulas for D agree</summary>
The displacement of a molecule is the integral of its velocity, $\mathbf r(t)-\mathbf r(0) = \int_0^t\mathbf v(t')\,dt'$. Squaring it means multiplying the integral by itself (as a dot product). Each of the two copies needs its own integration variable, $t'$ and $t''$, and both run from 0 to $t$. The product is a double integral, and averaging gives

$$
\mathrm{MSD}(t) = \int_0^t\!\!\int_0^t\langle\mathbf v(t')\cdot\mathbf v(t'')\rangle\,dt'\,dt'' .
$$

At equilibrium the average depends only on the time difference $s = |t'-t''|$. Write it as $C_v(s)$. For a given difference $s$, the earlier of the two times can lie anywhere between 0 and $t-s$, and either $t'$ or $t''$ can be the earlier one. Each value of $s$ therefore occurs with the weight $2(t-s)$, so

$$
\mathrm{MSD}(t) = 2\int_0^t(t-s)\,C_v(s)\,ds .
$$

$C_v(s)$ is zero except at short $s$. For $t$ much longer than its decay time, $t-s$ can be replaced by $t$ where it matters, and the upper limit by infinity: $\mathrm{MSD}(t)\approx2t\int_0^\infty C_v(s)\,ds$. Setting this equal to $6Dt$ and dividing both sides by $6t$ gives $D = \tfrac13\int_0^\infty C_v(s)\,ds$.
</details>

Use unwrapped coordinates. Wrapping puts a molecule that leaves the box back in at the opposite face, so its stored position jumps by a box length, and a displacement computed from stored positions can never be larger than the box. Unwrapped coordinates follow the molecule continuously through the periodic copies. Unwrapping removes every jump of about a box length between consecutive frames, so the frames must be close enough in time that no molecule really moves half a box between two of them.

### The finite-size correction

A molecule that moves through a liquid pushes solvent ahead of it and drags solvent along. This flow reaches far, and through it the motion of one molecule affects others at a distance. This is a **hydrodynamic interaction**. In a periodic box every molecule is surrounded by copies of itself that move in the same way, and the flow each one sets up is confined by the box. The net effect is that molecules diffuse more slowly than in an infinite liquid, and the smaller the box, the larger the effect.

<div class="box physics" markdown="1">
**Physics you need here: viscosity.** The viscosity $\eta$ (Greek eta) measures the resistance of a liquid to flow: honey has a high viscosity and water a low one. A liquid of high viscosity also slows the molecules that move through it, so a high viscosity goes with slow diffusion. The SI unit is the pascal second, Pa s. Water near room temperature has a viscosity close to $10^{-3}$ Pa s. More in the [primer](physics.html#diffusion).
</div>

Diffusion in a periodic box is slowed by hydrodynamic interaction with the periodic images. For a cubic box of edge $L$ and solvent viscosity $\eta$ ([Yeh and Hummer 2004](cite:yeh2004)):

$$
D_\infty = D_{PBC} + \frac{2.837\,k_BT}{6\pi\eta L}.
$$

<div class="legend" markdown="1">
- $D_{PBC}$: the diffusion coefficient you measured in the periodic box, from the MSD. PBC stands for periodic boundary conditions.
- $D_\infty$: the value for an infinitely large system, which is the one to compare with experiment.
- $k_B$, $T$: the Boltzmann constant and the temperature. For this formula use SI units: $k_BT = 4.14\times10^{-21}$ J at 300 K.
- $\eta$: the viscosity of the solvent, in Pa s. Strictly it is the viscosity of the water model you simulate, which can differ from that of real water.
- $L$: the edge length of the cubic box, in metres (1 nm = $10^{-9}$ m).
- $2.837$: a pure number that belongs to the cubic arrangement of the periodic copies.
- $6\pi$: a numerical factor from the hydrodynamics of the solvent.
</div>

Read it like this: the correction is always positive, because the periodic box makes diffusion too slow. It is proportional to $1/L$, so doubling the box edge halves it. As written, it does not contain any property of the diffusing molecule: the same amount is added whatever the size of the measured diffusion coefficient, so in relative terms it matters more for whatever diffuses slowly. This is the leading term only. The same paper gives a further term that makes the correction smaller for a solute whose radius is not small compared with $L$, and it found a smaller correction than this formula for the charged solutes it tested (ions and a small RNA).

The arithmetic for one case: $L = 3$ nm and, say, $\eta = 0.85\times10^{-3}$ Pa s (about the viscosity of water near 300 K). The correction is $2.837\times4.14\times10^{-21}/(6\pi\times0.85\times10^{-3}\times3\times10^{-9}) = 2.4\times10^{-10}$ m$^2$/s, which is $2.4\times10^{-4}$ nm$^2$/ps. Next to the diffusion coefficient of $2\times10^{-3}$ nm$^2$/ps of the example above, that is 12 %.

For water in a 3 nm box the correction is more than 10 %.

### Time correlation functions

The velocity autocorrelation function is one member of a family. For any observable you can ask how long it remembers its value: if the radius of gyration is above its average now, is it still above its average 100 ps later?

**Time correlation functions.** For any observable, $C_{AA}(t)=\langle\delta A(0)\,\delta A(t)\rangle$ with $\delta A = A-\langle A\rangle$. Their decay gives relaxation times, and their integrals give transport coefficients. The rotational correlation function of N-H bond vectors gives NMR order parameters $S^2$.

<div class="legend" markdown="1">
- $A$: the observable. $\langle A\rangle$: its mean over the trajectory.
- $\delta A(0)$: the deviation of $A$ from its mean at a starting time, called 0. $\delta A(t)$: its deviation a time $t$ later.
- $\langle\ \rangle$ around the product: the average over all starting times in the trajectory.
- $C_{AA}(t)$: the time correlation function of $A$ with itself, also called its autocorrelation function. The two subscripts name the two quantities that are multiplied. Its unit is the unit of $A$ squared.
</div>

Read it like this: at $t = 0$ the product is $\delta A^2$ and its average is the variance of $A$. At short $t$ the two deviations still have the same sign in most pairs of frames, the products are mostly positive, and $C_{AA}$ is close to the variance. At long $t$ the two deviations are unrelated, positive and negative products cancel, and $C_{AA}$ is zero. The time this takes is the **relaxation time** of the observable: how long it remembers a fluctuation.

<div class="box maths" markdown="1">
**Maths you need here: exponential decay.** The simplest decay is $e^{-t/\tau}$, where $\tau$ (Greek tau) is a time. It equals 1 at $t = 0$ and is multiplied by the same factor in every equal interval of time: 0.37 at $t = \tau$, 0.14 at $2\tau$, 0.05 at $3\tau$. So $\tau$ is the time in which the function falls to 37 % ($1/e$) of its value, and after three times $\tau$ almost nothing is left. The area under the curve from 0 to infinity is exactly $\tau$. More in the [toolbox](maths.html#exp-log).
</div>

A **transport coefficient** is a number that says how fast something is carried through a material: matter (the diffusion coefficient), momentum (the viscosity), heat (the thermal conductivity) or charge (the electrical conductivity). The Green-Kubo relations state that each of them is, apart from a constant factor, the time integral, the area under the curve, of an autocorrelation function measured in an ordinary equilibrium simulation. For diffusion the function is that of the velocity, as above. For the viscosity it is that of the shear stress in the liquid (the off-diagonal components of the pressure tensor). You do not have to push the system to measure how it responds to a push: the way its spontaneous fluctuations die away contains the same information.

For the last sentence of the definition, take the N-H bond of one residue and describe its direction by a vector of length 1, $\hat{\boldsymbol\mu}$. After the overall tumbling of the protein has been removed by fitting, the rotational correlation function asks how similar the direction at time $t$ is to the direction at time 0. The usual form is $\langle P_2(\hat{\boldsymbol\mu}(0)\cdot\hat{\boldsymbol\mu}(t))\rangle$ with $P_2(x) = \tfrac12(3x^2-1)$, where $x$ is the cosine of the angle between the two directions. $P_2$ equals 1 when the two directions coincide, and it averages to 0 when the later direction is completely random, because the average of $x^2$ is then $1/3$.

For a residue in a folded protein this function starts at 1 and falls to a plateau. The height of the plateau is the **order parameter** $S^2$. A value near 1 means that the bond keeps its direction inside the molecule (a rigid residue). A value near 0 means that the bond can point anywhere (a very flexible residue). NMR relaxation experiments give $S^2$ for each residue, so this is a residue-by-residue test of the fast motions in a simulation.

## Statistical error: the part most often done wrong

<div data-videos="e3Ygft3fjRg 8Y9dgl6jsBo"></div>

You have a time series and its mean. How far can that mean be from the true value, the one an infinitely long simulation would give? The answer is called the **standard error**, and the textbook way of computing it fails for simulation data. This section builds the correct estimate in three steps: the standard error of independent data, the reason why frames are not independent, and the correction for it. The practical methods follow.

The essential parts are the difference between standard deviation and standard error, the framed formula, and block averaging. The derivation in the "Optional" block can be skipped on a first reading.

### Spread of the data and uncertainty of the mean

Two numbers are easily confused.

- The **standard deviation** $\sigma_A$ says how much $A$ fluctuates from frame to frame. It is a property of the molecule. A longer simulation does not make it smaller. It only measures it better.
- The **standard error** $\mathrm{SE}(\bar A)$ says how much the computed mean $\bar A$ would change if you repeated the whole simulation. It is a property of your estimate. More data make it smaller.

An everyday case: the heights of the adults in a city have a standard deviation of, say, 10 cm, however many people you measure. The mean height, though, is known to within 1 cm after 100 people and to within 0.1 cm after 10,000.

<div class="box maths" markdown="1">
**Maths you need here: the standard error of the mean of independent values.** Values are **independent** when knowing one of them tells you nothing about another. For $N$ independent values with standard deviation $\sigma$, the standard error of their mean is

$$
\mathrm{SE} = \frac{\sigma}{\sqrt N}.
$$

The reason is a rule about variances: the variance of a sum of independent quantities is the sum of their variances. The sum of the $N$ values therefore has variance $N\sigma^2$. The mean is the sum divided by $N$, and dividing a quantity by $N$ divides its variance by $N^2$. So the mean has variance $N\sigma^2/N^2 = \sigma^2/N$, and the square root is $\sigma/\sqrt N$.

Example: a radius of gyration with $\sigma = 0.10$ nm. From 100 independent values the mean is known to $0.10/\sqrt{100} = 0.010$ nm, from 10,000 values to 0.001 nm. A hundred times more data buy a ten times smaller error.

A result is reported as mean ± standard error, for example $1.50\pm0.01$ nm. The mean of many independent values has a nearly Gaussian distribution, whatever the distribution of the single values (the central limit theorem). The true value then lies within one standard error of your mean in about two cases out of three, and within two standard errors in about 95 % of the cases. More in the [toolbox](maths.html#averages).
</div>

### Why successive frames are not independent

A trajectory of $N$ frames is not $N$ independent measurements. Frames close in time are similar.

The structure 10 ps after a given frame is almost the same structure, and the radius of gyration has hardly changed. If you know the value in one frame you can predict the next one almost exactly, so the second frame adds almost no new information. It is like reading an outdoor thermometer every second for an hour. You get 3,600 readings and know the temperature of that hour very well, but you know the average temperature of the month no better than from a single reading. Putting the number of frames into $\sigma/\sqrt N$ therefore gives an error bar that is far too small, often by a factor of ten or more.

To correct this you need a measure of how long the similarity lasts.

The quantity that tells you how similar is the normalised autocorrelation function

$$
c(t) = \frac{\langle\delta A(0)\,\delta A(t)\rangle}{\langle\delta A^2\rangle},
$$

which starts at 1 and decays to 0.

<div class="legend" markdown="1">
- $A$: the observable whose time series you analyse.
- $\delta A(0)$: the deviation of $A$ from its mean in some frame, whose time is called 0. $\delta A(t)$: the deviation a time $t$ later. The time difference $t$ is called the **lag**.
- $\langle\delta A(0)\,\delta A(t)\rangle$: the average of the product over all pairs of frames that are a time $t$ apart. It is the function $C_{AA}(t)$ of the previous section.
- $\langle\delta A^2\rangle$: the variance of $A$, which is $\sigma_A^2$. It is the value of the numerator at $t = 0$.
- $c(t)$: the normalised autocorrelation function, a pure number. "Normalised" means divided by its value at lag zero, so that it starts at 1.
</div>

**How to picture it.** Draw the time series on two transparent sheets and lay one over the other. They match exactly: that is $c(0) = 1$. Now slide the upper sheet sideways by a lag $t$ and compare each point with the point that is now under it. For a small shift the two curves still rise and fall together, and $c$ stays near 1. For a shift longer than the memory of the observable, highs lie over lows as often as over highs, and $c$ is near 0.

**How to compute it**, for a lag of $k$ frames: subtract the mean from every value, multiply each deviation by the deviation $k$ frames later, average the products, and divide by the variance.

**A small example by hand.** Twelve frames of a toy radius of gyration, in nm: 1.42, 1.45, 1.47, 1.44, 1.52, 1.55, 1.58, 1.54, 1.49, 1.47, 1.51, 1.56. The mean is 1.50 nm, and the deviations are $-0.08$, $-0.05$, $-0.03$, $-0.06$, $0.02$, $0.05$, $0.08$, $0.04$, $-0.01$, $-0.03$, $0.01$, $0.06$. Their mean square, the variance, is 0.00242 nm$^2$.

For a lag of one frame there are eleven products of neighbours: $(-0.08)\times(-0.05) = 0.0040$, $(-0.05)\times(-0.03) = 0.0015$, and so on. Their average is 0.00132 nm$^2$, so $c = 0.00132/0.00242 = 0.55$ at a lag of one frame. Neighbouring frames are more alike than chance would make them: low values come in runs, and so do high values.

**A longer example**, which the rest of this section uses. A toy series of 20,000 frames was generated on a computer with mean 1.50 nm, standard deviation 0.10 nm and an autocorrelation function that is known exactly, $e^{-k/50}$ at a lag of $k$ frames. (This is the model of the demo further down. The numbers quoted here come from one run of the same model in Python.) Its measured autocorrelation function:

| Lag $k$ (frames) | Measured $c$ | Exact $e^{-k/50}$ | Sum of the measured $c$ from lag 1 to lag $k$ |
|---|---|---|---|
| 0 | 1.000 | 1.000 | |
| 10 | 0.835 | 0.819 | 9.1 |
| 25 | 0.632 | 0.607 | 19.9 |
| 50 | 0.368 | 0.368 | 32.1 |
| 100 | 0.116 | 0.135 | 43.2 |
| 150 | 0.002 | 0.050 | 45.5 |
| 200 | 0.014 | 0.018 | 45.8 |

The function falls to 0.37 at a lag of 50 frames. That lag is the **correlation time** of this series: the time after which the memory of a fluctuation has dropped to 37 %. Beyond about three correlation times the measured values are small and noisy.

With frames saved every $\Delta t_s$, the **integrated autocorrelation time** is the sum over the saved lags, $\tau_{int}=\Delta t_s\sum_{k\ge1}c(k\,\Delta t_s)$ (for $\tau_{int}\gg\Delta t_s$ this is the integral $\int_0^\infty c(t)\,dt$).

<div class="legend" markdown="1">
- $\Delta t_s$: the time between two saved frames (the subscript s stands for "saved"), for example 10 ps. It is not the integration time step, which is a few femtoseconds.
- $k$: the lag counted in frames, 1, 2, 3 and so on. $k\,\Delta t_s$ is the same lag as a time.
- $c(k\,\Delta t_s)$: the normalised autocorrelation function at that lag.
- $\sum_{k\ge1}$: the sum over all lags from one frame upwards.
- $\tau_{int}$: the integrated autocorrelation time, with the unit of time.
- $\gg$: "much larger than".
</div>

Read it like this. Each term of the sum is the height of the curve $c$ at one saved lag. Multiplying by $\Delta t_s$ turns it into a bar of that width, so the sum is the area under the curve $c(t)$.

For an exponential decay $e^{-t/\tau}$ this area is $\tau$, so for such a function the integrated autocorrelation time and the correlation time are the same number. In the table the sum levels off near 46, so $\tau_{int}$ is about 46 frames. The exact value for this model is 49.5 frames.

In practice the sum has to be stopped once $c$ has decayed into noise, because the noisy tail adds error and no information. The function in the code below stops at the first lag at which $c$ is no longer positive.

### From correlation time to error bar

Define the **statistical inefficiency**

$$
g = 1+2\sum_{k\ge1}c(k\,\Delta t_s) = 1+\frac{2\tau_{int}}{\Delta t_s},\qquad N_{eff} = \frac{N}{g},\qquad
\boxed{\mathrm{SE}(\bar A) = \frac{\sigma_A}{\sqrt{N_{eff}}}\approx\sigma_A\sqrt{\frac{2\tau_{int}}{T_{sim}}}}
$$

<div class="legend" markdown="1">
- $g$: the statistical inefficiency, the number of saved frames that are worth one independent sample. It is a pure number, 1 for independent frames and larger for correlated ones. It is not the radial distribution function.
- $1+2\sum_{k\ge1}c$: the 1 stands for the frame itself. The sum collects the correlation with all later frames, and the factor 2 accounts for the earlier frames, which are correlated with it in the same way.
- $N$: the number of frames in the series (here not the number of atoms).
- $N_{eff}$: the effective number of independent samples.
- $\bar A$: the mean of the $N$ values. $\mathrm{SE}(\bar A)$: its standard error.
- $\sigma_A$: the standard deviation of $A$, the spread of the data.
- $T_{sim}$: the total simulated time that was analysed, $N\,\Delta t_s$.
- $\tau_{int}$, $\Delta t_s$, $c$: as in the list above.
- The frame around the last formula marks it as the result to remember. It has no mathematical meaning.
</div>

(For a series of finite length $N$ each term of the sum is weighted by $1-k/N$, as in the code below.) The last form shows what matters: the error depends on the simulated time in units of the correlation time, not on how many frames you saved. A 100 ns trajectory of an observable with $\tau_{int}$ = 10 ns contains about five independent samples, whether you stored 1,000 frames or 1,000,000.

Read the three formulas from left to right.

1. $g$ converts frames into independent samples. If the frames are independent, $c$ is zero at every lag from 1 upwards, and $g = 1$. If they are strongly correlated, the sum is large and so is $g$.
2. $N_{eff} = N/g$ is the number of samples you really have.
3. The standard error is the formula for independent data with $N$ replaced by $N_{eff}$.

The last form follows in two lines. When $\tau_{int}$ is much longer than $\Delta t_s$, the 1 in $g$ is negligible and $g\approx2\tau_{int}/\Delta t_s$. Then $N_{eff} = N/g\approx N\Delta t_s/2\tau_{int} = T_{sim}/2\tau_{int}$, because $N\Delta t_s$ is the total time. In words: one independent sample for every $2\tau_{int}$ of simulation. In the example of the text, 100 ns divided by $2\times10$ ns is five.

Three consequences. Saving frames more often does not help, because $N$ and $g$ grow together. Halving the error takes four times the simulated time, because of the square root. And an observable with a long correlation time has a large error however long the list of frames is.

For the toy series, the exact $g$ is 100. With 20,000 frames that makes $N_{eff} = 200$ and a standard error of $0.10/\sqrt{200} = 0.0071$ nm. The naive value, $0.10/\sqrt{20000} = 0.0007$ nm, is ten times too small. The function `statistical_inefficiency` below, applied to the series, returned $g = 92$, so about 218 samples. With the standard deviation measured on this series, 0.1045 nm, that is again a standard error of $0.1045/\sqrt{218} = 0.0071$ nm. The measured mean was 1.505 nm, 0.005 nm from the true 1.500 nm: less than one standard error away, as it should be most of the time.

<details markdown="1"><summary>Optional: where the factor g comes from</summary>
Number the frames $i = 1,\dots,N$ and write $A_i$ for the value in frame $i$, $\delta A_i$ for its deviation from the true mean $\langle A\rangle$, and $c_k$ for $c(k\,\Delta t_s)$. The computed mean is $\bar A = \frac1N\sum_iA_i$, so its deviation from the true mean is $\frac1N\sum_i\delta A_i$. The variance of the computed mean is the average of the square of this deviation, taken over many imagined repetitions of the simulation. The square of a sum is a double sum over all pairs of frames:

$$
\big\langle(\bar A-\langle A\rangle)^2\big\rangle = \frac1{N^2}\sum_{i=1}^N\sum_{j=1}^N\langle\delta A_i\,\delta A_j\rangle .
$$

By the definition of the autocorrelation function, $\langle\delta A_i\,\delta A_j\rangle = \sigma_A^2\,c_k$ when the two frames are $k$ frames apart. Now count the pairs. There are $N$ pairs with $i = j$, for which $c_0 = 1$. There are $2(N-k)$ pairs that are $k$ frames apart: $N-k$ choices of the earlier frame, times 2 because each pair appears in both orders. Therefore

$$
\big\langle(\bar A-\langle A\rangle)^2\big\rangle = \frac{\sigma_A^2}{N^2}\Big[N+2\sum_{k=1}^{N-1}(N-k)\,c_k\Big] = \frac{\sigma_A^2}{N}\Big[1+2\sum_{k=1}^{N-1}\Big(1-\frac kN\Big)c_k\Big].
$$

The second step divides the bracket by $N$. The bracket on the right is $g$, including the weight $1-k/N$ that the text mentions. When $N$ is much larger than the lags at which $c_k$ differs from zero, $k/N$ is negligible there and the bracket becomes $1+2\sum_{k\ge1}c_k$. The standard error is the square root of the variance: $\sigma_A\sqrt{g/N} = \sigma_A/\sqrt{N_{eff}}$. For independent frames every $c_k$ with $k\ge1$ is zero, and the result is $\sigma_A/\sqrt N$ again.
</details>

### Block averaging

<div data-videos="BACN9Ydiw5I 0KqCK0yG9T0"></div>

The autocorrelation route needs the function $c$ out to long lags, where it is noisy. Block averaging reaches the same standard error without it. The idea: if single frames are not independent, group them into pieces that are long enough for the *pieces* to be independent, and apply $\sigma/\sqrt N$ to the pieces.

The practical method, described in detail by [Flyvbjerg and Petersen (1989)](cite:flyvbjerg1989), who note that it was already part of the folklore of the simulation community. Cut the series into $M$ consecutive blocks, average within each block, and treat the block averages as independent:

$$
\mathrm{SE}_{block} = \frac{s(\text{block means})}{\sqrt M}.
$$

<div class="legend" markdown="1">
- $M$: the number of blocks. Each block holds $N/M$ consecutive frames.
- block means: the $M$ averages, one per block.
- $s(\text{block means})$: the standard deviation of those $M$ numbers, in the version with $M-1$ in the denominator (see the first maths box of this module).
- $\sqrt M$: the square root of the number of blocks.
- $\mathrm{SE}_{block}$: the resulting estimate of the standard error of the overall mean, for this choice of block length.
</div>

Read it like this. It is the formula $\sigma/\sqrt N$ for independent data, applied to the block means in place of the frames. The overall mean is the mean of the block means, so if the block means are independent, this is its standard error.

Step by step, with the twelve frames of the example above and blocks of four frames:

1. The blocks are (1.42, 1.45, 1.47, 1.44), (1.52, 1.55, 1.58, 1.54) and (1.49, 1.47, 1.51, 1.56).
2. Their means are 1.445, 1.5475 and 1.5075 nm.
3. The mean of the three block means is 1.50 nm, the overall mean. Their deviations from it are $-0.055$, $0.0475$ and $0.0075$. The sum of the squares is 0.00534. Divided by $M-1 = 2$ it is 0.00267, and the root is $s = 0.052$ nm.
4. $\mathrm{SE}_{block} = 0.052/\sqrt3 = 0.030$ nm.

With blocks of one frame, which is the naive calculation, $s = 0.051$ nm over twelve values (with $12-1 = 11$ in the denominator; the variance of 0.00242 nm$^2$ quoted earlier has 12 in the denominator, and its root is 0.049 nm) and the standard error is $0.051/\sqrt{12} = 0.015$ nm, half as large. Twelve frames and three blocks are far too few to trust either number. The steps are the same for twelve frames and for twelve million.

Repeat for increasing block length. While blocks are shorter than the correlation time, the estimate rises. When it reaches a plateau, the blocks are independent and the plateau value is the standard error. **If there is no plateau before you run out of blocks, the simulation is too short to give an error estimate**: the largest value reached is only a lower bound on the true standard error, so the mean cannot be trusted either.

Why the estimate rises: a short block with a high mean tends to be followed by another block with a high mean, because the observable has not had time to forget. Neighbouring block means are then correlated, and treating them as independent underestimates the error, as it did for single frames. The rise does not end at one correlation time. For an autocorrelation function that decays exponentially, the estimate is on average still about 40 % too low when the block length equals the correlation time, about 6 % too low at eight correlation times and about 2.5 % too low at twenty.

Why it stops rising: once the blocks are much longer than the correlation time, two neighbouring blocks share their memory only through the few frames at their common border. Making the blocks longer still changes nothing on average, because the scatter $s$ of the block means and $\sqrt M$ then shrink by the same factor.

The toy series of 20,000 frames, analysed with the function below:

| Block length (frames) | Number of blocks $M$ | $\mathrm{SE}_{block}$ (nm) |
|---|---|---|
| 1 | 20,000 | 0.0007 |
| 10 | 2,000 | 0.0023 |
| 50 | 400 | 0.0046 |
| 100 | 200 | 0.0056 |
| 200 | 100 | 0.0063 |
| 400 | 50 | 0.0069 |
| 500 | 40 | 0.0067 |
| 1,000 | 20 | 0.0081 |
| 2,000 | 10 | 0.0052 |
| 4,000 | 5 | 0.0055 |

The exact standard error for this model is 0.0071 nm. The estimate climbs steeply while the blocks are shorter than a few correlation times (50 frames here) and levels off near 0.007 nm from a block length of about 400 frames. With 20 blocks or fewer the values scatter: 0.0081, 0.0052, 0.0055. That scatter is not a new trend. A standard deviation estimated from $M$ values is itself uncertain by a fraction of about $1/\sqrt{2(M-1)}$: 7 % for 100 blocks, 16 % for 20 blocks, 35 % for 5 blocks.

So read the plateau where the blocks are long enough to be independent and still numerous enough, several tens, to give a stable value. Here the answer is 0.007 nm, ten times the naive 0.0007 nm. The same two numbers give the statistical inefficiency: divide the plateau value by the naive value and square the result, here about $10^2 = 100$.

```python
import numpy as np

def block_average(a, n_blocks_list=(5, 10, 20, 40, 80, 160)):
    """Standard error of the mean of a correlated series, for several block counts."""
    a = np.asarray(a, float)
    out = []
    for nb in n_blocks_list:
        m = len(a) // nb                         # samples per block
        means = a[: m * nb].reshape(nb, m).mean(axis=1)
        out.append((m, means.std(ddof=1) / np.sqrt(nb)))
    return out                                    # list of (block length, standard error)

def statistical_inefficiency(a):
    """g = 1 + 2 tau / dt. Sums the autocorrelation function until it first turns negative,
    a simple rule; pymbar uses a faster and more robust estimator of the same quantity."""
    a = np.asarray(a, float) - np.mean(a)
    n, var, g = len(a), np.var(a), 1.0
    for t in range(1, n // 2):
        c = np.dot(a[:-t], a[t:]) / ((n - t) * var)
        if c <= 0.0:
            break
        g += 2.0 * c * (1.0 - t / n)
    return g
```

What the code does: in `block_average`, `m` is the number of frames per block, and frames left over at the end are dropped. `reshape(nb, m)` arranges the series as a table with one block per row, and `.mean(axis=1)` averages each row. `std(ddof=1)` is the standard deviation with $M-1$ in the denominator. The function returns one pair (block length, standard error) for each number of blocks you ask for. Plot the second against the first and look for the plateau.

`statistical_inefficiency` follows the recipe for $c$ given above. It subtracts the mean, computes $c$ for a lag of `t` frames, and adds $2c$ times the weight $1-t/n$ to $g$, until $c$ is no longer positive. From $g$ you get the number of independent samples as `len(a) / g` and the standard error as `np.std(a) / np.sqrt(len(a) / g)`.

The demo generates the toy series of this section with a correlation time of your choice and draws the block-averaging curve.

<div class="widget" data-widget="blockavg"></div>

### The bootstrap

Block averaging and $\sigma/\sqrt N$ give the error of a mean. Many results are not plain means: a free-energy difference computed from the logarithm of a ratio of populations, a diffusion coefficient from a fitted slope, the position of a peak. For such a result there is often no ready formula for the error. The **bootstrap** replaces the formula by computation.

The idea: you would like to repeat the whole study many times and see how much the result varies. You cannot, so you imitate the repetition by drawing new data sets from the data you have.

1. Start from $n$ independent pieces of data: independent simulations, or blocks that are long enough to be independent (use a block length at which the block-averaging curve of the previous section has reached its plateau).
2. Draw $n$ pieces at random **with replacement**: the same piece may be drawn twice and another not at all. This is one "resample".
3. Compute your result from the resample exactly as you computed it from the real data.
4. Repeat steps 2 and 3 a thousand times or more. The standard deviation of the collected results is the standard error of your result, and the range that holds the middle 95 % of them is a 95 % confidence interval.

An example that was run for this lesson. Six independent simulations gave 12.1, 12.4, 11.8, 12.6, 12.0 and 12.3 (in kJ/mol, say). The mean is 12.2, the standard deviation $s$ is 0.29, and the formula gives a standard error of $0.29/\sqrt6 = 0.118$. One resample was 12.3, 12.6, 12.0, 12.6, 12.3, 12.3, with mean 12.35. Another was 12.6, 12.6, 12.3, 12.4, 12.0, 11.8, with mean 12.28.

The means of 10,000 resamples had a standard deviation of 0.109. That is close to the 0.118 of the formula and a little smaller, because with few pieces the bootstrap underestimates the error somewhat (for the mean of six values, by 9 %). The 95 % range of step 4 suffers more. Here it runs from 11.98 to 12.42, a half-width of 0.22, against 0.30 from the $t$ factor of the section on independent repeats. In a test with sets of six Gaussian values, such a range held the true mean in about 87 % of the cases, not in 95 %. With only a few pieces, use the $t$ interval for a mean and keep the bootstrap for results that have no formula.

Two warnings. Resample independent pieces, never single correlated frames: resampling frames repeats the mistake of putting the number of frames into $\sigma/\sqrt N$. And the bootstrap cannot see what the data do not contain. If all your simulations are stuck in the same state, every resample agrees with every other, and the error bar is small and wrong.

### Independent repeats

Every method so far tries to find out, from inside one trajectory, how many independent samples it contains. The alternative is to make the samples independent by construction.

The most reliable error bar comes from several independent simulations: compute the observable in each, and report the mean and the standard error across runs.

"Independent" means started with different random velocities, and for slow processes also from different starting structures ([Module 2](02-classical-mechanics.html) explained why different velocities are enough for the fast motions). Each run gives one number, its own average over the part kept after equilibration. For $n$ runs the standard error is $s/\sqrt n$, where $s$ is the standard deviation of the $n$ numbers. No autocorrelation function is needed.

Repeats also catch something no single-trajectory analysis can: a run that is trapped in a different state. "Trapped" means that the run stays in one conformation for its whole length, because leaving it takes longer than the simulation.

With few repeats, report a confidence interval and not only a standard error: for $n$ independent values the 95 % interval is the mean $\pm\,t_{n-1}\,s/\sqrt n$, and the factor $t$ is large when $n$ is small (4.3 for three repeats, 2.6 for six).

<div class="legend" markdown="1">
- $n$: the number of independent simulations.
- $s$: the standard deviation of the $n$ values, with $n-1$ in the denominator.
- $s/\sqrt n$: the standard error of their mean.
- $t_{n-1}$: Student's $t$ factor for $n-1$ "degrees of freedom". It is a number from a statistics table, or from `scipy.stats.t.ppf(0.975, n-1)`. It is not a time.
- $\pm$: the interval runs from the mean minus the quantity that follows to the mean plus that quantity.
</div>

<div class="box maths" markdown="1">
**Maths you need here: the confidence interval and the factor $t$.** A 95 % confidence interval is a range produced by a recipe that captures the true value in 95 % of the cases in which the recipe is used. If the standard deviation were known exactly, the range would be the mean ± 1.96 standard errors. But $s$ is itself estimated from $n$ values, and with few values it can be much too small by chance. To keep the 95 % promise the range has to be widened, and the factor $t_{n-1}$ says by how much.

The factor is 4.30 for $n = 3$, 3.18 for $n = 4$, 2.78 for $n = 5$, 2.57 for $n = 6$, 2.26 for $n = 10$, 2.09 for $n = 20$, and 1.96 for very large $n$.

Example: three runs give 12.1, 12.3 and 12.6. The mean is 12.33, $s = 0.25$ and the standard error is $0.25/\sqrt3 = 0.15$. The 95 % interval is $12.33\pm4.30\times0.15$, that is $12.3\pm0.6$. More in the [toolbox](maths.html#averages).
</div>

With fewer than about ten values, show the individual points as well. If three runs give 12.1, 12.3 and 17.8, you have learned that there are at least two long-lived states and that none of the runs has sampled the transition between them.

The arithmetic for these three values gives a mean of 14.1, $s = 3.2$, a standard error of 1.9 and a 95 % interval of ±8.0. "14 ± 8" hides the message. The three values are not scattered around a common mean: two agree to within 0.2, and the third lies about 5.6 away from them. A reader who sees the three points understands this at once, which is the reason for showing them.

### Equilibration: what to discard

A simulation starts from a prepared structure: for example a crystal structure placed in a freshly built box of water, then heated and brought to the right pressure in short runs ([Module 10](10-running-a-simulation.html)). That starting point is not a typical state of the system at the simulated temperature. The water has not yet settled around the protein, the volume of the box is still adjusting, and side chains still sit in their crystal positions. During the first part of the run the system relaxes towards the states in which it will spend the rest of the time. This relaxation is called **equilibration**, and the same word is used for the part of the trajectory that you throw away because of it.

The start of a production run still remembers its preparation. Including it biases the average. Discarding too much wastes data.

A **bias** is an error that pushes the result in one direction. Unlike the random error that the standard error measures, it does not average away within the run. Discarding data has the opposite cost: fewer independent samples and a larger standard error. The choice of the cut is a trade between the two.

Three ways to see where equilibration ends:

- **Plot the time series.** A drift at the start, followed by fluctuations about a steady level, is the sign. Do this for the observable you care about, because each observable has its own equilibration time.
- **Compare two halves.** Split the data you intend to keep into a first and a second half and compare the two means. If they differ by much more than their standard errors, the series is still drifting.
- **Maximise the number of independent samples.** This is the rule of the next paragraph.

A principled choice ([Chodera 2016](cite:chodera2016)): for each candidate cut-off time $t_0$, compute the number of effectively independent samples $N_{eff}(t_0)$ in the remainder, and choose the $t_0$ that maximises it.

<div class="legend" markdown="1">
- $t_0$: the length of the part discarded at the start, as a time or as a number of frames.
- $N_{eff}(t_0)$: the number of frames that remain after the cut, divided by the statistical inefficiency $g$ computed from those remaining frames.
</div>

Why there is a maximum: if you cut too little, the drift is still in the series. To the autocorrelation function a drift looks like one very slow fluctuation, so $g$ is large and $N_{eff}$ small. If you cut too much, $g$ no longer changes and you only lose frames. The best cut lies in between.

A test on the toy series, with a slow relaxation added to its start (0.40 nm at frame 0, decaying as $e^{-k/1000}$ with the frame number $k$):

| Discarded frames $t_0$ | Mean of the rest (nm) | $g$ | $N_{eff}$ |
|---|---|---|---|
| 0 | 1.525 | 284 | 70 |
| 500 | 1.518 | 134 | 145 |
| 1,000 | 1.515 | 99 | 192 |
| 1,500 | 1.511 | 88 | 210 |
| 2,000 | 1.511 | 89 | 202 |
| 3,000 | 1.513 | 91 | 188 |
| 5,000 | 1.508 | 93 | 161 |
| 10,000 | 1.503 | 106 | 94 |

$N_{eff}$ is largest for a cut near 1,500 frames, where the added relaxation has decayed to less than the size of the ordinary fluctuations. With nothing discarded the mean is 1.525 nm, of which 0.020 nm is bias from the first frames (the same series without the relaxation has a mean of 1.505 nm), and the series seems to hold only 70 independent samples.

The two-halves test agrees. With no cut the two halves differ by 0.043 nm, about four times the standard error of either half (0.01 nm). After a cut of 2,000 frames they differ by 0.010 nm.

In practice also look at the time series, and check that the result does not change when you discard twice as much. If doubling the discarded part moves the mean by more than its standard error, the first cut was too short.

<div class="box warn" markdown="1">
**You cannot prove convergence.** Every test above detects correlation on time scales shorter than the trajectory. A process slower than the trajectory is invisible: all observables look flat and well converged within one state. Protect yourself with independent repeats from *different* starting structures, with physical knowledge of what the slow processes are likely to be, and by stating clearly what the simulation length can and cannot support.
</div>

An example of what the box describes. Suppose a loop flips between two conformations about once per microsecond, and you run 100 ns starting in the first one. The RMSD is flat, block averaging shows a clean plateau, and the number of independent samples is large. Every test is passed, and the second conformation is missing from every average. Nothing inside the trajectory can tell you so.

## Collective motions: principal component analysis

<div data-videos="qcfV1z_UZLE 0pK0EWyinVo"></div>

A protein of 300 residues has 900 C$\alpha$ coordinates, and all of them fluctuate. They do not fluctuate independently: neighbouring atoms move together, and sometimes whole domains do. Principal component analysis (PCA) looks for a small number of patterns of joint motion that account for most of the fluctuation.

The picture in two dimensions: plot the $x$ coordinate of one atom against the $x$ coordinate of another, one point per frame. If the two atoms move together, the cloud of points is a stretched ellipse along the diagonal. The long axis of the ellipse is the direction in which the pair moves most. That direction is the first principal component, and the short axis is the second. PCA does the same for all $3N$ coordinates at once.

<div class="box maths" markdown="1">
**Maths you need here: covariance.** The variance says how much one quantity fluctuates. The **covariance** of two quantities says whether they fluctuate together. For each frame, multiply the deviation of the first quantity from its mean by the deviation of the second from its mean, and average the products. If the first is above its mean when the second is above its mean, the products are positive and so is the covariance. If one is high when the other is low, it is negative, and if the two are unrelated, positive and negative products cancel and it is near zero.

Example: four frames with $x$ = 1, 2, 3, 4 and $y$ = 2, 3, 5, 6. The means are 2.5 and 4. The deviations of $x$ are $-1.5$, $-0.5$, $0.5$, $1.5$ and those of $y$ are $-2$, $-1$, $1$, $2$. The products are 3, 0.5, 0.5 and 3, and their mean, the covariance, is 1.75. The covariance of a quantity with itself is its variance: 1.25 for $x$ and 2.5 for $y$.

Dividing the covariance by the two standard deviations gives the **correlation coefficient**, a pure number between $-1$ and 1. Here it is $1.75/\sqrt{1.25\times2.5} = 0.99$: the two quantities move almost perfectly together. More in the [toolbox](maths.html#averages).
</div>

After fitting to a reference, build the covariance matrix of atomic positions,

$$
C_{ab} = \big\langle(x_a-\langle x_a\rangle)(x_b-\langle x_b\rangle)\big\rangle,
$$

and diagonalise it.

<div class="legend" markdown="1">
- $a$, $b$: labels that run over the $3N$ coordinates of the chosen atoms ($x$ of atom 1, $y$ of atom 1, $z$ of atom 1, $x$ of atom 2 and so on), not over the atoms. For 300 C$\alpha$ atoms each label takes 900 values.
- $x_a$: the value of coordinate $a$ in one frame, after the fit.
- $\langle x_a\rangle$: its average over all frames.
- $x_a-\langle x_a\rangle$: the deviation of coordinate $a$ from its average in one frame.
- The outer $\langle\ \rangle$: the average of the product over all frames.
- $C_{ab}$: the covariance of the coordinates $a$ and $b$, in nm$^2$. All of them together form the covariance matrix, a table with $3N$ rows and $3N$ columns. The entries on the diagonal, $C_{aa}$, are the variances of the single coordinates.
</div>

The fit comes first because otherwise the largest "motion" in the data would be the tumbling of the whole molecule.

<div class="box maths" markdown="1">
**Maths you need here: the eigenvectors of a covariance matrix.** [Module 2](02-classical-mechanics.html) introduced eigenvectors. A matrix multiplied by a vector gives another vector. For special vectors, the **eigenvectors** of the matrix, the result is the same vector multiplied by a number, the **eigenvalue**. To "diagonalise" a matrix is to find all its eigenvectors and eigenvalues, which a numerical library does for you.

For a covariance matrix they have a direct meaning. The eigenvector with the largest eigenvalue is the direction along which the cloud of data points is most spread out, and its eigenvalue is the variance of the data along that direction.

Example: two coordinates that each have variance 2 and that have covariance 1. To multiply a matrix by a vector, take each row of the matrix, multiply its entries by the entries of the vector, and add. The first row below gives $2\times1+1\times1 = 3$.

$$
\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix} = \begin{pmatrix}3\\3\end{pmatrix} = 3\begin{pmatrix}1\\1\end{pmatrix},
\qquad
\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}1\\-1\end{pmatrix} = \begin{pmatrix}1\\-1\end{pmatrix}.
$$

So $(1,1)$, the pattern "both coordinates increase together", is an eigenvector with eigenvalue 3. And $(1,-1)$, "one increases while the other decreases", is an eigenvector with eigenvalue 1. The total variance is $2+2 = 4$, which is also the sum of the eigenvalues. The first pattern holds three quarters of it, 75 %. More in the [toolbox](maths.html#eigen).
</div>

The eigenvectors with the largest eigenvalues are the directions of largest fluctuation, and a handful usually account for most of the motion ("essential dynamics").

Here an eigenvector is a list of $3N$ numbers, one displacement for each coordinate. It is a pattern in which every atom has a direction and a relative amplitude, such as two domains that close like a hinge. Each eigenvector is called a **principal component**, and its eigenvalue is the variance of the structure along that pattern, in nm$^2$. Sort the eigenvalues from the largest down and call them $\lambda_1$, $\lambda_2$ and so on (Greek lambda). The fraction of the total fluctuation that component $k$ accounts for is $\lambda_k$ divided by the sum of all eigenvalues.

To see where one frame lies along a component, project the frame on it:

$$
p_k(t) = \sum_a v_{k,a}\,\big(x_a(t)-\langle x_a\rangle\big).
$$

<div class="legend" markdown="1">
- $p_k(t)$: the projection of the frame at time $t$ on principal component $k$, in nm. It says how far the structure is displaced along that pattern, in the positive or the negative sense.
- $v_{k,a}$: entry $a$ of eigenvector $k$. The eigenvector is scaled to length 1.
- $x_a(t)-\langle x_a\rangle$: the deviation of coordinate $a$ from its average in that frame.
- $\sum_a$: the sum over all $3N$ coordinates. The whole expression is the dot product of the eigenvector with the deviation of the frame.
</div>

Each projection is a time series like any other observable, and its statistics need the same care.

That alone does not show that they are collective motions: for pure random diffusion in many dimensions the first three components already hold more than 80 % of the variance ([Hess 2000](cite:hess2000)).

A **collective motion** is one in which many atoms move together in a concerted way. "Random diffusion in many dimensions" means that every coordinate performs its own random walk, independent of all the others. By construction it contains no collective motion at all, and PCA still reports a few dominant components. A few components that hold most of the variance are what PCA gives for any data that drift slowly.

Projecting the trajectory on the first two gives a map of the conformations visited. Plot $p_1$ against $p_2$, one point per frame. Regions with many points are conformations that the simulation visited often.

### The pitfall: cosines from a random walk

The pitfall: a random walk in high dimensions, that is an unconverged simulation, produces first principal components that look like smooth half-cosines in time, and a projection that looks like a meaningful U-shaped pathway. Hess ([2000](cite:hess2000)) derived this for random diffusion and showed that cosine-shaped components appear in protein simulations that are too short. Hess ([2002](cite:hess2002)) defined the cosine content of a component, from 0 (no cosine) to 1 (a perfect one). It is a negative indicator only: if your first component is a cosine of period twice the trajectory length, you are looking at diffusion, not at a functional motion, but a low cosine content proves nothing. A better check is to split the trajectory into parts and compare their principal components.

Several terms in this paragraph need explaining.

*A half-cosine in time.* The projection $p_1(t)$ follows $\cos(\pi t/T_{sim})$, where $T_{sim}$ is the length of the trajectory. It starts at one extreme, ends at the opposite one, passes through zero once and never returns. This is what "a cosine of period twice the trajectory length" means: only half a wave fits into the run. Such a curve describes a system that is still drifting away from its start.

*The U shape.* A run of Exercise 4 in a smaller size (500 dimensions, 5,000 steps) shows it. The first three components held 60 %, 15 % and 7 % of the variance, 82 % together, and they followed cosines with one, two and three half-waves almost exactly.

If $p_1$ is a half-wave and $p_2$ a full wave, the identity $\cos2\theta = 2\cos^2\theta-1$ ties them together: after scaling both to run between $-1$ and 1, $p_2 = 2p_1^2-1$ (or its mirror image, since the sign of an eigenvector is arbitrary). That is a parabola. In the map of $p_1$ against $p_2$ the points trace a U, which looks like a pathway from one state through an intermediate to another. It is the signature of drift.

*A negative indicator.* A high cosine content is a reason to distrust a component. A low one is no proof that the sampling has converged. A *functional motion* is one that the protein uses to do its work, such as the opening of a binding site.

*Comparing parts.* Run the PCA on the first half and on the second half of the trajectory separately. If both halves sample the same collective motions, their first eigenvectors are similar: the dot product of two eigenvectors of length 1 is near 1 or $-1$ for the same pattern and near 0 for unrelated ones. If the first eigenvectors of the two halves have little in common, the "motions" were made by drift.

Time-lagged independent component analysis (TICA, Module 16) is the related method that finds the *slowest* rather than the largest motions. Largest and slowest are different things. A floppy chain end can have the largest amplitude and relax within a nanosecond, while a small rearrangement in a binding site can take microseconds.

## Free-energy surfaces from histograms

<div data-videos="yt6-v3jZals"></div>

A system at equilibrium visits each conformation in proportion to its probability. Counting how often a trajectory is found at each value of a coordinate therefore measures a probability, and a probability converts into a free energy.

<div class="box maths" markdown="1">
**Maths you need here: histograms and probability.** Choose a coordinate, divide its range into bins of equal width, and count the frames that fall into each bin. That is a **histogram**. The count in a bin divided by the total number of frames is the **probability** $P$ of that bin, and the probabilities of all bins add up to 1.

Example: of 10,000 frames, 2,000 have a certain distance between 0.50 and 0.55 nm. The probability of that bin is 0.20. Dividing by the bin width gives the **probability density**, $0.20/0.05 = 4$ nm$^{-1}$, which does not depend on the bin width you happened to choose.

Bins that are too wide blur the features of the curve. Bins that are too narrow hold few frames each and give a noisy curve. More in the [toolbox](maths.html#probability).
</div>

<div class="box physics" markdown="1">
**Physics you need here: populations and free energy.** At a fixed temperature, a state of low free energy is populated more than a state of high free energy, and the rule is exponential: the probability of a state is proportional to $e^{-F/k_BT}$, where $F$ is its free energy ([Module 3](03-statistical-mechanics.html)). Unlike the potential energy, the free energy also counts in how many ways the rest of the system (the other parts of the molecule, the solvent) can arrange itself while the state is occupied. That is why populations follow $F$ and not the energy alone. More in the [primer](physics.html#thermodynamics).
</div>

If a trajectory samples the equilibrium distribution, the free energy along any coordinate is $F(\xi) = -k_BT\ln P(\xi)$, from a histogram.

<div class="legend" markdown="1">
- $\xi$ (Greek xi): the coordinate you chose, any single number computed from a frame: a distance, the radius of gyration, $Q$, a projection on a principal component. It is also called a collective variable ([Module 12](12-free-energy-pmf.html)).
- $P(\xi)$: the probability of finding the system at the value $\xi$, taken from the histogram.
- $k_BT$: the Boltzmann constant times the temperature, 2.494 kJ/mol at 300 K.
- $\ln$: the natural logarithm.
- $F(\xi)$: the free energy as a function of $\xi$, in kJ/mol, also called a free-energy profile or a potential of mean force. It is defined up to an additive constant, which is usually chosen so that the lowest point is zero.
</div>

"The equilibrium distribution" is the set of probabilities of all states at the simulated temperature. A trajectory "samples" it when it visits the states in those proportions.

One trap: when $\xi$ is the distance $r$ between two particles, $F(r)$ from a histogram is not the function $w(r)$ of the section on the radial distribution function. The histogram of $r$ still contains the shell volume $4\pi r^2\,dr$, which $g(r)$ has divided out, so $F(r) = w(r)-2k_BT\ln r$ plus a constant. [Module 12](12-free-energy-pmf.html) explains this.

The formula is the exponential rule solved for $F$. Start from $P(\xi)\propto e^{-F(\xi)/k_BT}$, where $\propto$ means "is proportional to". Take the logarithm of both sides: $\ln P = -F/k_BT+\text{constant}$. Multiply by $-k_BT$ and drop the constant. Only differences of $F$ have a meaning, and they depend only on ratios of probabilities:

$$
F(\xi_2)-F(\xi_1) = -k_BT\ln\frac{P(\xi_2)}{P(\xi_1)}.
$$

<div class="legend" markdown="1">
- $\xi_1$, $\xi_2$: two values of the coordinate, that is, two bins of the histogram.
- $P(\xi_2)/P(\xi_1)$: the ratio of their probabilities, which equals the ratio of the numbers of frames in the two bins.
- Other symbols: as in the list above.
</div>

Read it like this. Equal populations give a difference of zero. At 300 K, a bin with ten times fewer frames lies $k_BT\ln10 = 5.7$ kJ/mol higher, a bin with a hundred times fewer lies 11.5 kJ/mol higher, and a bin with a thousand times fewer 17.2 kJ/mol. Two states populated 90 % and 10 % differ by $2.494\times\ln9 = 5.5$ kJ/mol.

This sets the range of a histogram. If the most populated bin holds 10,000 frames, a bin with a single frame lies $k_BT\ln10^4 = 23$ kJ/mol above it. A plain trajectory cannot show free energies higher than that, and the top of the range rests on a handful of frames.

This is only valid where transitions between the regions have been sampled many times. A beautiful two-dimensional free-energy map made from a single trajectory that crossed the barrier once is a picture of one trajectory. Modules 12 and 14 give the methods for the case that matters.

The reason is counting. The relative population of two wells is known only if the system has gone back and forth between them many times, because each crossing is one independent answer to the question "which well?". With a single crossing, the ratio of the times spent in the two wells records only the moment at which the crossing happened to occur. Had it come later, the map would show different depths. Within one well, where the system moves about freely, the shape of the profile is reliable.

The same counting gives an error estimate. A bin that the trajectory entered on $n$ independent occasions has a population that is uncertain by a fraction of about $1/\sqrt n$, and its free energy is then uncertain by about $k_BT/\sqrt n$: 1.2 kJ/mol for four visits, 0.25 kJ/mol for a hundred. Here $n$ counts separate visits, not frames. For an error bar on a whole profile, compute the profile in each of several blocks or independent runs and take the spread, or bootstrap over them.

A two-dimensional map is made in the same way from a two-dimensional histogram. Divide the plane of two coordinates, for example $p_1$ and $p_2$, into small squares, count the frames in each, and apply the formula. The valleys of the map are the states. Because the frames are spread over many more bins, a map needs far more data than a profile.

"The case that matters" is a barrier too high to be crossed many times in a plain simulation. [Module 12](12-free-energy-pmf.html) and [Module 14](14-enhanced-sampling.html) describe simulations that are built to cross it.

## Comparing with experiment

<div data-videos="TlKg7luoRmY a15IlXIhz1k"></div>

An experiment does not measure coordinates. It measures a signal, such as the splitting of an NMR line, the intensity of scattered X-rays or the fraction of light passed from one dye to another. The signal depends on the coordinates through a formula that is known, or known approximately, and the experiment averages it over a huge number of molecules and over the measuring time. To compare, compute the same signal from every frame with that formula, and then average over the frames. The table lists the standard cases.

| Experiment | What to compute |
|---|---|
| NMR scalar couplings $^3J$ | Karplus relation $^3J(\theta) = A\cos^2\theta+B\cos\theta+C$ averaged over the trajectory (for the backbone coupling $^3J_{HNH\alpha}$, $\theta=\phi-60°$; $A$, $B$, $C$ depend on the coupling) |
| NMR relaxation, order parameters $S^2$ | Long-time limit of the bond-vector rotational correlation function |
| NMR chemical shifts | Empirical predictors (SPARTA+, SHIFTX2) applied per frame, then averaged |
| NOE distances | $\langle r^{-6}\rangle^{-1/6}$ when the internal motion is slower than overall tumbling, $\langle r^{-3}\rangle^{-1/3}$ when it is faster; both are dominated by the shortest distances |
| SAXS | Scattering curve per frame (CRYSOL, Pepsi-SAXS), then averaged; or $R_g$ |
| FRET efficiency | Average of $1/[1+(r/R_0)^6]$ over the distance distribution |
| Crystallographic B-factors | RMSF (remembering that crystals also contain static disorder) |

<div class="legend" markdown="1">
- $^3J$: a scalar coupling, the splitting of an NMR line caused by a nucleus three bonds away, in hertz. Its size depends on the dihedral angle about the middle bond.
- $\theta$ (Greek theta): that dihedral angle. $\phi$: the backbone dihedral angle phi of the residue.
- $A$, $B$, $C$ in the Karplus relation: three empirical constants, in hertz, fitted for each kind of coupling. Here they are not observables.
- $^3J_{HNH\alpha}$: the coupling between the amide hydrogen and the H$\alpha$ of the same residue.
- $S^2$: the order parameter of the section on time correlation functions, between 0 and 1.
- NOE: the nuclear Overhauser effect, an NMR signal between two hydrogen nuclei that are close in space. $r$ is their distance in one frame.
- $\langle r^{-6}\rangle^{-1/6}$: average $r^{-6}$ over the frames, then raise the result to the power $-1/6$, which turns it back into a length. $\langle r^{-3}\rangle^{-1/3}$ is built in the same way.
- SAXS: small-angle X-ray scattering (see the radius of gyration).
- FRET: the transfer of energy between two dyes attached to the molecule. $r$ is the distance between the dyes in one frame. $R_0$ is the Förster distance of the dye pair, the distance at which the efficiency is one half.
- B-factors: see the box in the section on RMSF.
</div>

Average the **observable**, not the structure: experimental signals are non-linear in the coordinates.

"Non-linear" is the point. For a non-linear function, the function of the average differs from the average of the function. Take the square: the values 1 and 3 have the average 2, whose square is 4, but the average of their squares is $(1+9)/2 = 5$.

The NOE shows how large the effect can be. Such a signal is seen for hydrogens closer than roughly 0.5 nm.

Suppose two hydrogens are 0.3 nm apart in 10 % of the frames and 1.0 nm apart in the other 90 %. Their mean distance is 0.93 nm, far too long for a signal. The NOE average is $\langle r^{-6}\rangle = 0.1\times0.3^{-6}+0.9\times1.0^{-6} = 138$ nm$^{-6}$, and $138^{-1/6} = 0.44$ nm, short enough for one. The few close frames dominate.

"Averaging the structure" means averaging the coordinates over the frames first and computing the signal from that single average structure. It fails for the same reason, and for one more: the average structure is often not a possible structure. A side chain that flips between two positions has its averaged atoms in between, where they never are.

The computed value is the mean of a time series, so it needs an error bar from the methods of this module. The formula that turns a structure into a signal has an uncertainty of its own (the Karplus constants, the chemical-shift predictors), which adds to the statistical error.

## Tools

<div data-videos="_v3WU0RAfRM Tso29WxWWHg x39p_SrJLY4 8ZhNuhBXB0o p3OUUnHXQjU MzVk6VO5dyc"></div>

A standard analysis is short in practice. The example computes the backbone RMSD and the radius of gyration with the MDAnalysis library. It assumes that the molecules in the trajectory file have already been made whole.

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms

u = mda.Universe("md.tpr", "md.xtc")            # topology + trajectory
ref = mda.Universe("md.tpr", "npt.gro")          # reference structure
R = rms.RMSD(u, ref, select="backbone").run()    # fit and compute per frame
time_ps, rmsd_A = R.results.rmsd[:, 1], R.results.rmsd[:, 2]

ca = u.select_atoms("name CA")
rg = [ca.radius_of_gyration() for ts in u.trajectory]
```

Line by line:

- `mda.Universe(...)` joins a topology file (which atoms exist and how they are bonded, here `md.tpr`) with coordinates: the trajectory `md.xtc` for `u`, the single structure `npt.gro` for the reference.
- `rms.RMSD(u, ref, select="backbone").run()` goes through the frames, superimposes the backbone atoms of each frame on those of the reference, and evaluates the RMSD formula of this module.
- `R.results.rmsd` is a table with one row per frame. Column 0 is the frame number, column 1 the time and column 2 the RMSD. The variable names record the units that MDAnalysis uses, picoseconds and ångström. Divide by 10 to get nm.
- `u.select_atoms("name CA")` picks the C$\alpha$ atoms. The last line steps through the trajectory: each pass of the loop loads the next frame, and `ca.radius_of_gyration()` is evaluated on that frame.

The two results are time series. Pass them to `block_average` from this module to get the standard errors of their means.

MDAnalysis and MDTraj are two widely used general Python libraries. The GROMACS tools (`gmx rms`, `rmsf`, `gyrate`, `rdf`, `hbond`, `msd`, `energy`, `analyze -ee` for block averaging) and AMBER's `cpptraj` cover the standard analyses. VMD, PyMOL, ChimeraX and NGLview display trajectories: always watch the trajectory before trusting any number computed from it.

Watching takes minutes and catches what a single averaged number hides: a broken molecule, a ligand that has left its site, a domain that has unfolded.

## Check yourself

<details markdown="1"><summary>1. A 200 ns trajectory was saved every 10 ps. The radius of gyration has a standard deviation of 0.10 nm and an integrated autocorrelation time of 5 ns. What is the standard error of its mean?</summary>
$N = 20{,}000$ frames, $g = 1+2\times5000/10 = 1001$, $N_{eff}\approx20$. SE $=0.10/\sqrt{20} = 0.022$ nm. (Here $N$ is the number of frames, 200 ns divided by 10 ps, $g$ is the statistical inefficiency with $\tau_{int} = 5000$ ps and $\Delta t_s = 10$ ps, and $N_{eff} = N/g$. The short form gives the same count: $T_{sim}/2\tau_{int} = 200/10 = 20$ samples.) The naive $0.10/\sqrt{20000} = 0.0007$ nm is too small by a factor of 32.
</details>

<details markdown="1"><summary>2. The backbone RMSD levels off at 0.2 nm after 20 ns. Is the simulation converged?</summary>
It shows only that the distance from the starting structure stopped increasing. Many different conformations lie at 0.2 nm from the start, and slow transitions between them, or to states further away, may not have occurred. Check observables relevant to your question, their block-averaged errors, and independent repeats.
</details>

<details markdown="1"><summary>3. Why should you compute a NOE-derived distance as ⟨r⁻⁶⟩^(−1/6) and not as ⟨r⟩?</summary>
The NOE intensity is proportional to $r^{-6}$, and the experiment averages the intensity (for motions slower than the tumbling of the molecule; for faster internal motion the average is over $r^{-3}$). Two protons that are close for 10 % of the time give a strong NOE even if their mean distance is large.
</details>

<details markdown="1"><summary>4. Block averaging gives standard errors of 0.8, 1.5, 2.6 and 3.9 kJ/mol for blocks of 1, 5, 20 and 50 ns in a 200 ns run. What do you conclude?</summary>
There is no plateau: the error estimate is still growing at the longest block length for which you have a few blocks. The correlation time is comparable with or longer than the run, and neither the mean nor its error is reliable. Run longer or use enhanced sampling.
</details>

<details markdown="1"><summary>5. You extend a simulation from 100 ns to 400 ns. What happens to the standard deviation of the radius of gyration, and what to the standard error of its mean?</summary>
The standard deviation stays about the same. It is the size of the fluctuations of the molecule, and more data only measure it better. The standard error halves: the number of independent samples is proportional to the simulated time, and the error falls as one over its square root, $1/\sqrt4 = 1/2$. Both statements assume that the first 100 ns had already visited the relevant conformations.
</details>

<details markdown="1"><summary>6. After superposition, four atoms lie 0.1, 0.1, 0.1 and 0.5 nm from their reference positions. What is the RMSD, and why is it larger than the mean deviation?</summary>
The squared deviations are 0.01, 0.01, 0.01 and 0.25 nm$^2$. Their mean is $0.28/4 = 0.07$ nm$^2$ and the root is 0.26 nm. The mean deviation is 0.2 nm. The RMSD is larger because squaring gives the one large deviation more weight than the three small ones.
</details>

<details markdown="1"><summary>7. In a histogram of a distance at 300 K, the most populated bin holds 5,000 frames and another bin holds 50. What is the free-energy difference between them, and what else must you know before you trust it?</summary>
The ratio of the populations is 100, so the difference is $k_BT\ln100 = 2.494\times4.61 = 11.5$ kJ/mol. Before trusting it you must know on how many separate occasions the trajectory entered the rare bin. Fifty consecutive frames are a single visit, and one visit gives no usable estimate of a population.
</details>

## Exercises

1. For the simulation from Module 10, compute backbone RMSD, per-residue RMSF and radius of gyration. Compare RMSF with the B-factors in the PDB file.
2. Compute the oxygen-oxygen radial distribution function of the water and the coordination number of the first shell. Compare the peak positions with the experimental values (first peak near 0.28 nm).
3. Apply `block_average` and `statistical_inefficiency` to the potential energy, the radius of gyration and one side-chain dihedral angle. Which converges fastest, and why?
4. Generate a 1,000-dimensional random walk of 10,000 steps, run PCA on it, and plot the projections on the first three components against time. Compare with cosines.
5. Compute the diffusion coefficient of water from your trajectory, apply the finite-size correction, and compare with experiment.

## Read

{{READ}}
