---
num: 7
title: Periodic boundaries, cutoffs and Ewald summation
short: Boundaries and Ewald
part: Part II · The engine
hours: 7
summary: Simulate a small box that behaves like bulk liquid, cut the short-range interactions correctly, and derive the Ewald sum that makes long-range electrostatics exact.
videos: 6 7
papers: E
tags: pbc-cutoffs, electrostatics-ewald
---

<div class="box goal" markdown="1">
#### After this module you can

- apply the minimum-image convention and choose a box shape and size;
- write the Lennard-Jones tail correction and explain shifted and switched potentials;
- explain how Verlet and cell lists make the cost linear in $N$;
- derive the three terms of the Ewald sum and say what PME changes;
- read the non-bonded section of an input file and know what each setting does.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

A force field (Module 5) gives the energy of a pair of atoms as a function of the distance between them. Before a program can add those pair energies up, two practical questions need an answer.

First, the box holds between ten thousand and a million atoms, while a single drop of solution holds about $10^{21}$ molecules. How do you make so few atoms behave like the inside of the drop? Second, every atom interacts with every other atom. Which pairs can be left out, and what has to be done about the pairs that cannot?

The module answers in four layers:

1. **Periodic boundaries.** The box is surrounded by copies of itself, so that it has no surface.
2. **Cutoffs for the Lennard-Jones interaction.** This interaction fades quickly with distance, so pairs further apart than about 1 nm are skipped. The cut has three side effects that must be repaired, and neighbour lists make it cheap to find the pairs that remain.
3. **Why charges cannot be treated the same way, and the Ewald sum.** The interaction between charges fades too slowly for a cutoff. Ewald summation rewrites the sum over all periodic copies as two sums that both converge quickly.
4. **What programs do with it.** Particle-mesh Ewald (PME), the settings in an input file, and a cheaper alternative called the reaction field.

The Ewald section is the heaviest mathematics of the course so far. On a first reading it is enough to follow it up to the interactive demo (the idea of the split), read the table that summarises the terms, and go on to PME. The derivation of each term is marked, and you can come back to it later.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The notation below appears for the first time in this module. The general conventions (bold letters for vectors, the sum sign, bars) are explained in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $x \leftarrow \dots$ | "Replace $x$ by what stands on the right." An instruction for a program: the new value of $x$ is computed from the old one. |
| $\mathrm{round}(x)$ | The whole number nearest to $x$. $\mathrm{round}(0.4)=0$, $\mathrm{round}(0.6)=1$, $\mathrm{round}(-0.9)=-1$. |
| $r^{-6}$ | The same as $1/r^6$. A negative power means "one divided by". |
| $\propto$ | "Is proportional to." |
| $O(N)$, $O(N^2)$ | "Of order $N$", "of order $N^2$". It says how the cost of a calculation grows with the number of atoms $N$. With $O(N)$, twice as many atoms cost twice as much. With $O(N^2)$ they cost four times as much. |
| $\sum_{\mathbf n}$ | A sum over all the periodic copies of the box. |
| $\sum{}^{'}$ | A prime on a sum sign: some terms are left out. Which ones is stated under the formula. |
| $\tilde\rho(\mathbf k)$ | A tilde over a letter, with $\mathbf k$ in brackets: the amount of the wave $\mathbf k$ contained in the function $\rho$ (its Fourier coefficient, explained in the Ewald section). |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which meaning applies each time.

- $\rho$ is the number of particles per volume in the Lennard-Jones sections, and the electric charge per volume in the Ewald section.
- $\varepsilon$ alone is the depth of the Lennard-Jones energy well. With a subscript ($\varepsilon_0$, $\varepsilon_r$, $\varepsilon_{rf}$) it is an electrical quantity, a permittivity or dielectric constant.
- $i$ is the label of an atom, as in $q_i$. In an exponent such as $e^{i\mathbf k\cdot\mathbf r_j}$ it is the imaginary unit, the number whose square is $-1$.
- $e$ is the base of the exponential, 2.718, in formulas such as $e^{-k^2/4\alpha^2}$. In running text it is also the unit of charge, the charge of one proton.
- $\mathbf n$ in bold is the shift from the box to one of its copies. $n_x$, $n_y$, $n_z$ are whole numbers that count how many times a wave fits into the box.
- $k$ and $\mathbf k$ are a wave vector in the Ewald section. $k_{rf}$ in the last section is an unrelated constant of the reaction-field formula.
</div>

## Periodic boundary conditions

<div data-videos="gVVqjmTAJGI x20QP1x3U7c J3aB9xp1YIE Wbzopzywt-Q IpdTtx98AWQ"></div>

A molecule at the surface of a liquid is in a different situation from one deep inside. It has neighbours on one side only, so it feels different forces and moves differently. Experiments on solutions measure the inside, which is called the **bulk**: in a glass of water fewer than one molecule in ten million is at the surface. A simulation is far from that situation.

A simulation box holds $10^4$ to $10^6$ atoms. If it had walls, a large fraction of the molecules would sit at a surface: in a cube of 10,000 water molecules about a quarter are in the outermost molecular layer.

The arithmetic is short. 10,000 molecules packed into a cube make $10000^{1/3}\approx 21.5$ molecules along each edge. Strip one layer from every face and a cube of 19.5 molecules per edge is left, which holds $19.5^3\approx 7400$ molecules. The other 2,600, about a quarter, formed the outer layer. With a million molecules the edge is 100 molecules, the inner cube holds $98^3 = 941{,}192$, and 6 % are still at the surface.

To imitate bulk solution we remove the surface by making the box **periodic**: it is surrounded by an infinite lattice of identical copies. A particle that leaves through one face enters through the opposite face with the same velocity.

Some old video games work in the same way: a ship that flies off the right edge of the screen comes back in at the left edge. The comparison stops at one point. In the game the copies are only a rule for the edges. In a simulation the atoms near a face of the box interact with the atoms of the neighbouring copy, as if that copy were really there.

Three words are used from here on:

- A **lattice** is a regular arrangement that repeats in all directions, like the squares of graph paper continued in three dimensions.
- An **image** of a particle is its copy in one of the other boxes. If the box edge along $x$ has the length $L_x$ and the particle is at $x$, its images are at $x+L_x$, $x-L_x$, $x+2L_x$ and so on, and likewise along $y$ and $z$.
- The **central box** is the one whose particles the program stores. All images of a particle move together with it, so $N$ positions are enough to describe the whole infinite system.

When a particle leaves the central box, one of its images enters at the same moment through the opposite face. The number of particles in the box therefore stays $N$. There are no walls and no surface, and every molecule has other molecules on all sides. The price is that nothing larger than the box can exist in the system, which has consequences listed at the end of this section.

### The minimum-image convention

<div data-videos="pzM7ju9DNtM AbidqaoH7Wo"></div>

Every particle now has infinitely many images. When the program computes the interaction of particle $i$ with particle $j$, which image of $j$ should it take? For an interaction that fades quickly with distance, only the closest one matters.

Each particle interacts with the **nearest image** of every other particle. For a rectangular box with edges $L_x,L_y,L_z$:

$$
\Delta x \leftarrow \Delta x - L_x\,\mathrm{round}\!\left(\frac{\Delta x}{L_x}\right)
$$

and the same for $y$ and $z$. This is the line `d -= L * np.round(d / L)` in the Module 1 code.

<div class="legend" markdown="1">
- $\Delta x$: the $x$ component of the separation of two particles, $x_i - x_j$, computed from the coordinates as the program stores them. In nm.
- $L_x$: the length of the box edge along $x$, in nm. $L_y$ and $L_z$ are the edges along $y$ and $z$.
- $\Delta x/L_x$: the same separation counted in box lengths instead of nm.
- $\mathrm{round}(\ )$: the nearest whole number. Here it gives the separation in box lengths, rounded to the nearest whole number.
- $\leftarrow$: "replace the left side by the right side". The line is an instruction that changes $\Delta x$.
</div>

Read it like this: count how many whole box lengths separate the two stored positions, and take that many box lengths away. What is left is the separation between particle $i$ and the closest image of particle $j$. After the replacement $\Delta x$ always lies between $-L_x/2$ and $+L_x/2$, so no pair is ever counted as more than half a box apart along any axis.

An example with numbers. Take $L_x = 3$ nm, particle $i$ at $x_i = 0.2$ nm and particle $j$ at $x_j = 2.9$ nm. The stored separation is $\Delta x = 0.2 - 2.9 = -2.7$ nm. In box lengths that is $-2.7/3 = -0.9$, which rounds to $-1$. The new value is $\Delta x = -2.7 - 3\times(-1) = +0.3$ nm.

In words: the stored particle $j$ is 2.7 nm to the right of $i$, but its image in the box on the left sits at $2.9 - 3 = -0.1$ nm, only 0.3 nm from $i$. A second pair with $\Delta x = 1.2$ nm gives $1.2/3 = 0.4$, which rounds to 0, and nothing is changed: the stored particle is already the closest image.

The convention goes together with a **cutoff**: a distance $r_c$ beyond which a pair is not computed at all (the subject of the next section). It is consistent with a cutoff $r_c$ only if

$$
r_c \le \tfrac12 L_{min},
$$

so that at most one image of each neighbour lies inside the cutoff sphere.

<div class="legend" markdown="1">
- $r_c$: the cutoff distance, in nm. Pairs further apart than $r_c$ are skipped. Typical values are 0.9 to 1.2 nm.
- $L_{min}$: the shortest of the three box edges $L_x$, $L_y$, $L_z$.
- $\le$: "is smaller than or equal to".
- $\tfrac12$: one half.
</div>

The **cutoff sphere** of a particle is the sphere of radius $r_c$ around it: everything inside is computed, everything outside is ignored. Two images of the same neighbour are at least one box edge apart, that is, at least $L_{min}$. A sphere of radius $r_c$ is $2r_c$ wide, so if $2r_c$ is no larger than the box it cannot hold two of them.

Here is what goes wrong otherwise. Take $L_x = 3$ nm again and a cutoff of 1.8 nm, which is more than half the box. A neighbour at $\Delta x = +1.4$ nm has another image at $1.4 - 3 = -1.6$ nm. Both are inside the cutoff sphere, but the minimum-image rule returns only the first, and the second interaction is lost.

The condition forbids this case. With a cutoff of 1.0 to 1.2 nm it asks for a box of at least 2.0 to 2.4 nm. Boxes that hold a solvated protein are larger than that for other reasons, given next.

### Box shape and size

Most of the atoms in a simulation of a protein belong to the water around it, so the amount of water decides the cost. This section is about how little water you can use without letting the protein notice that it lives in a periodic system.

A protein is roughly spherical, so a cube wastes water in its corners. Space-filling shapes that are closer to a sphere need less solvent for the same distance between periodic images:

| Box | Volume for the same image distance $d$ | Saving against the cube |
|---|---|---|
| Cube | $d^3$ | 0 |
| Truncated octahedron | $0.77\,d^3$ | 23 % |
| Rhombic dodecahedron | $0.71\,d^3$ | 29 % |

<div class="legend" markdown="1">
- $d$: the image distance, the distance between the centre of the box and the centre of the nearest copy, in nm. For a cube it is the edge length.
- $d^3$: the volume of a cube with that edge, in nm$^3$.
- $0.77$ and $0.71$: pure numbers from the geometry of the two shapes, $4/(3\sqrt3)$ and $\sqrt2/2$.
</div>

A shape is **space-filling** when copies of it stack without gaps. Cubes do, and spheres do not, which is why a sphere itself cannot be used. A truncated octahedron is a cube with its eight corners cut off, which leaves 14 faces. A rhombic dodecahedron has 12 identical diamond-shaped faces. Both stack without gaps.

Read the table with an example. For $d = 8$ nm the cube has a volume of $8^3 = 512$ nm$^3$. Liquid water has about 33 molecules per nm$^3$, so the cube holds about 17,000 water molecules. The rhombic dodecahedron with the same $d$ has $0.71\times512\approx 360$ nm$^3$ and about 12,000 water molecules. That is 5,000 molecules fewer to compute at every step, with the protein as far from its nearest copy as before.

Codes implement these as triclinic cells. A **triclinic cell** is a box whose three edges need not be at right angles, a brick pushed sideways. Any periodic arrangement can be described by three edge vectors, so one general kind of box covers the cube and both shapes of the table. For this reason a system that was set up as a rhombic dodecahedron can look like a slanted brick in a viewer. The two pictures show the same periodic system with a different outline drawn around it.

Rules for the size:

- The solute must never see its own image: the shortest distance between the solute and any periodic copy must stay larger than the cutoff at all times. In practice, leave at least 1.0 to 1.2 nm of solvent between the solute and each box face (so at least 2.0 nm between copies).
- An elongated or flexible molecule can rotate or extend. Size the box for the longest dimension it can reach, or check the minimum image distance during the run (`gmx mindist -pi`).
- For binding or unbinding simulations the box must hold the separated state with both partners out of range of each other and of all images.

The **solute** is the molecule you study, for example the protein, and the **solvent** is the water and ions around it. "Seeing its own image" means that an atom of the protein comes within the cutoff of an atom of a copy of the same protein. The protein would then interact directly with itself, which no single protein in a dilute solution does. The arithmetic of the first rule: 1.0 nm of water between the protein and the face, and another 1.0 nm between that face and the copy behind it, makes 2.0 nm between the two. The command in the second rule is a GROMACS tool that reports this distance for each frame of a trajectory.

Periodicity does have artefacts: no fluctuation with a wavelength longer than the box exists, diffusion is slowed by hydrodynamic interaction with the images (a correction is given in Module 11), and a charged solute interacts with its copies.

An **artefact** is a feature of the result that comes from the method and not from the system. The three named here, in words:

- *No long waves.* A slow ripple, for example the bending of a membrane or a variation of density from place to place, must fit a whole number of times into the box. Ripples longer than the box are missing.
- *Slower diffusion.* Diffusion is the random wandering of a molecule through the liquid. A moving molecule drags the liquid around it along. In a periodic box that flow meets the flows around the images of the same molecule, and the net effect is to hold the molecule back.
- *Interaction of charges with their copies.* The interaction between charges reaches very far, as the second half of this module shows, so a solute with a net charge feels its own images even in a large box.

## Cutting off short-range interactions

<div data-videos="JQPHMpR37Co y-jUCgk4rCI hi7gvv-I-0o"></div>

With periodic boundaries each atom has an unlimited number of partners: all other atoms and all their images. A program can compute only a limited number of pairs per step. This section shows that for one kind of interaction the distant pairs can be left out, and what has to be repaired afterwards.

The interaction in question is the Lennard-Jones energy of Module 5. As a reminder:

$$
U_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right]
$$

<div class="legend" markdown="1">
- $U_{LJ}(r)$: the Lennard-Jones energy of one pair of atoms, in kJ/mol.
- $r$: the distance between the two atoms, in nm.
- $\sigma$: the distance at which the energy is zero, the "size" of the pair. A few tenths of a nanometre.
- $\varepsilon$: the depth of the energy well. Module 5 gives 0.1 to 1 kJ/mol as typical. This $\varepsilon$ is not the electrical $\varepsilon_0$ that appears later.
- $(\sigma/r)^{12}$: the repulsion at short distance. $-(\sigma/r)^{6}$: the attraction at larger distance, called dispersion.
</div>

At distances of a few $\sigma$ the repulsive term is negligible, and what remains is the attraction $-4\varepsilon(\sigma/r)^6$. The Lennard-Jones attraction falls as $r^{-6}$, fast enough to truncate at $r_c$ = 0.9 to 1.2 nm.

A number shows how fast. With $\sigma = 0.3$ nm, a pair at $r = 1.0$ nm has $(\sigma/r)^6 = 0.3^6 = 0.00073$, so its energy is $-0.0029\,\varepsilon$: three thousandths of the well depth. Doubling the distance divides the energy by $2^6 = 64$.

"Fast enough" needs an argument, though, because the number of distant partners is large. The argument counts the partners shell by shell.

<div class="box maths" markdown="1">
**Maths you need here: adding up over spherical shells.** Draw a sphere of radius $r$ around one atom, and a slightly larger one of radius $r+dr$. The space between them is a thin **shell**. The surface of a sphere is $4\pi r^2$, so the volume of the shell is $4\pi r^2\,dr$. If the liquid holds $\rho$ atoms per unit volume, the shell holds $4\pi r^2\rho\,dr$ atoms. Example: for $r = 1$ nm, $dr = 0.1$ nm and $\rho = 33$ nm$^{-3}$, the shell has a volume of $4\pi\times1^2\times0.1 = 1.26$ nm$^3$ and holds about 42 molecules.

The number of partners in a shell grows as $r^2$. To get the total energy of the atom with all partners beyond $r_c$, multiply the number in each shell by the pair energy $u(r)$ at that distance and add up all shells. Adding up infinitely many thin slices is an [integral](maths.html#integral):

$$
\int_{r_c}^{\infty} 4\pi r^2\rho\; u(r)\,dr .
$$

One rule of integration is all that is needed. For a power $n$ larger than 1,

$$
\int_{r_c}^{\infty}\frac{dr}{r^{n}} = \frac{1}{(n-1)\,r_c^{\,n-1}} ,
$$

a finite number that gets smaller when $r_c$ gets larger. For $n = 4$ it is $1/(3r_c^3)$. For $n = 1$ or smaller the integral has no finite value: the sum keeps growing however far you go.
</div>

Apply this to the attraction, $u(r) = -4\varepsilon\sigma^6/r^6$. Each shell contributes $4\pi r^2\rho$ partners times an energy proportional to $r^{-6}$, so the contribution of a shell is proportional to $r^2\times r^{-6} = r^{-4}$. The shells get more populated as $r^2$, but the pair energy drops as $r^{-6}$ and wins.

The rule above with $n = 4$ gives a finite total, proportional to $1/r_c^3$. So the sum over all distant partners exists and is small, and cutting it off is a controlled approximation. Keep this argument in mind: for charges it will fail.

Three issues arise.

**1. The jump at the cutoff.** Plain truncation makes $U$ discontinuous at $r_c$, so the force has a delta-function spike and energy is not conserved.

Plain truncation means: use $U_{LJ}(r)$ when $r$ is smaller than $r_c$, and zero otherwise. At $r_c$ the energy then steps from the small negative value $U_{LJ}(r_c)$ straight to zero. "Discontinuous" is the word for a function with such a step.

The force is minus the slope of the energy (Module 2). A step is a slope that is infinitely steep over a distance of zero width, and the matching force is an infinitely strong push that lasts for no time. That object is the [delta function](maths.html#delta) of the sentence above.

A program computes forces only once per time step and never meets the spike. So when a pair moves across $r_c$, its potential energy changes by $U_{LJ}(r_c)$ and the kinetic energy does not change to compensate. The total energy makes a small jump at every crossing, and there are very many crossings.

Remedies:

- **Potential shift**: use $U(r)-U(r_c)$ inside the cutoff. The energy is continuous, the force is unchanged inside and still jumps to zero at $r_c$ (a small jump). This is the GROMACS default.
- **Force switch or potential switch**: multiply by a smooth function that takes the force (or potential) to zero between $r_{sw}$ and $r_c$. CHARMM force fields were parameterised with a force switch from 1.0 to 1.2 nm, and membrane properties in particular depend on using it.

Written out, the shifted potential is

$$
U_{shift}(r) = \begin{cases} U_{LJ}(r) - U_{LJ}(r_c) & \text{for } r < r_c \\ 0 & \text{for } r \ge r_c \end{cases}
$$

<div class="legend" markdown="1">
- $U_{shift}(r)$: the pair energy that the program uses, in kJ/mol.
- $U_{LJ}(r)$: the Lennard-Jones energy of the pair at the distance $r$.
- $U_{LJ}(r_c)$: the same function evaluated at the cutoff. It is one fixed number for each kind of pair.
- $r_c$: the cutoff distance.
- The brace: "use the upper line in the first case and the lower line in the second".
</div>

Read it like this: the whole curve inside the cutoff is lifted by the small amount that makes it arrive at exactly zero at $r_c$. Lifting a curve by a constant does not change its slope, so the force inside the cutoff is the same as before. At $r_c$ the force drops from its small value there to zero. With $\sigma = 0.3$ nm and $r_c = 1.0$ nm that value is $0.017\,\varepsilon$ per nm, which is why the list calls the jump small. The Python code of Module 1 does the same thing in its line `shift = 4 * (rc ** -12 - rc ** -6)`.

A **switch** goes one step further and removes the jump in the force as well. The switching function is equal to 1 up to the distance $r_{sw}$ where switching starts, and falls smoothly to 0 at $r_c$. A potential switch multiplies the energy by it. A force switch changes the force so that it goes smoothly to zero, and the energy that belongs to that force follows from it.

"Parameterised with" means that the numbers of the force field were fitted while this treatment was in use. The treatment of the cutoff is then part of the model, and changing it changes the results.

The second issue uses two terms. The **number density** $\rho$ is the number of particles per unit volume, $N/V$ for $N$ particles in a box of volume $V$. The **radial distribution function** $g(r)$ (Module 11) compares the density of particles found at the distance $r$ from a given particle with the average density $\rho$. Close to a particle $g(r)$ has peaks, the shells of neighbours. Further out it settles at 1, which means "as many particles as in a liquid without any structure".

**2. The neglected tail.** Beyond $r_c$ the liquid is nearly uniform ($g(r)\approx1$), so the missing energy can be added analytically. For $N$ particles of number density $\rho$:

$$
U_{tail} = \frac{N\rho}{2}\int_{r_c}^{\infty}4\pi r^2\,U_{LJ}(r)\,dr
= \frac{8}{3}\pi N\rho\,\varepsilon\sigma^3\left[\frac13\left(\frac{\sigma}{r_c}\right)^{9}-\left(\frac{\sigma}{r_c}\right)^{3}\right].
$$

<div class="legend" markdown="1">
- $U_{tail}$: the Lennard-Jones energy of all pairs further apart than $r_c$, for the whole system, in kJ/mol. The "tail" is the part of the energy curve beyond the cutoff.
- $N$: the number of particles in the box.
- $\rho$: the number density, particles per nm$^3$ (here not a charge density).
- $\int_{r_c}^{\infty}\dots\,dr$: add up the contributions of all shells from $r_c$ outwards.
- $4\pi r^2\,dr$: the volume of the shell at distance $r$ (see the box above).
- $U_{LJ}(r)$: the Lennard-Jones pair energy, with its parameters $\varepsilon$ (well depth, kJ/mol) and $\sigma$ (size, nm).
- $\tfrac12$ in $N\rho/2$: every pair would otherwise be counted twice, once from each of its two particles.
- $r_c$: the cutoff distance, in nm.
- $\pi$: the number 3.14159.
</div>

"Analytically" means with a formula worked out on paper, in place of a sum over pairs done by the computer. The steps from the middle expression to the right one:

1. *One particle.* The shell at distance $r$ holds $4\pi r^2\rho\,dr$ particles (uniform liquid, $g = 1$), each with the energy $U_{LJ}(r)$. Adding up the shells gives the energy of one particle with everything beyond the cutoff, $\rho\int_{r_c}^{\infty}4\pi r^2\,U_{LJ}(r)\,dr$.
2. *All particles.* Multiply by $N$, and divide by 2 because each pair has been counted from both ends. That is the middle expression.
3. *Insert the Lennard-Jones formula.* The integrand becomes $16\pi\varepsilon\,(\sigma^{12}r^{-10} - \sigma^{6}r^{-4})$, because $r^2\times r^{-12} = r^{-10}$ and $r^2\times r^{-6} = r^{-4}$.
4. *Integrate each power* with the rule of the box: $\int_{r_c}^\infty r^{-10}dr = 1/(9r_c^9)$ and $\int_{r_c}^\infty r^{-4}dr = 1/(3r_c^3)$. The integral is $16\pi\varepsilon\sigma^3\left[\tfrac19(\sigma/r_c)^9 - \tfrac13(\sigma/r_c)^3\right]$.
5. *Collect the factors.* Multiplying by $N\rho/2$ and taking a factor $\tfrac13$ out of the bracket gives the right-hand side.

Read it like this. The bracket is negative, because $(\sigma/r_c)^3$ is much larger than $\tfrac13(\sigma/r_c)^9$ when $r_c$ is a few $\sigma$. The correction lowers the energy: it restores attraction that the cutoff removed. It grows with the density and shrinks as $1/r_c^3$ when the cutoff is made longer.

A number, with round values chosen as an illustration: $\sigma = 0.3$ nm, $\varepsilon = 0.6$ kJ/mol, $\rho = 33$ nm$^{-3}$ and $r_c = 1.0$ nm. Then $(\sigma/r_c)^3 = 0.027$, the term with the ninth power is negligible, and $U_{tail}/N = \tfrac83\pi\times33\times0.6\times0.027\times(-0.027) = -0.12$ kJ/mol per particle. That looks small next to the thermal energy $k_BT = 2.5$ kJ/mol at 300 K (Boltzmann's constant $k_B$ times the temperature $T$, Module 3). For 10,000 particles it adds up to $-1200$ kJ/mol, and its effect on the pressure is larger still.

There is a matching correction to the pressure. It is negative (the missing attraction pulls the system together), so leaving it out gives a density that is too low. In GROMACS this is `DispCorr = EnerPres`. It assumes a homogeneous system, so it is not appropriate for membranes and interfaces, where Lennard-Jones PME (a lattice sum for the $r^{-6}$ term) is the rigorous alternative.

Some explanation of these four sentences. The pressure of a liquid has a part that comes from the forces between the particles (the virial of Module 3), and attractive forces lower it. Exercise 2 gives the formula of the correction. With the illustrative numbers above it comes to about $-8$ kJ mol$^{-1}$ nm$^{-3}$, which is about $-130$ bar (1 kJ mol$^{-1}$ nm$^{-3}$ is 16.6 bar).

A run at constant pressure (Module 8) adjusts the box until the pressure matches the target. If the attraction of the tail is missing, the computed pressure is too high, the box grows, and the density ends up too low.

The setting name reads "dispersion correction for energy and pressure". **Homogeneous** means that the average density is the same everywhere, which is what step 1 of the derivation assumed. In a membrane the lipid tails and the water have different densities and different Lennard-Jones parameters, so one average $\rho$ describes neither. A **lattice sum** is a sum over all periodic images, like the Ewald sum derived below for charges.

**3. Finding the neighbours.** Testing all $N(N-1)/2$ pairs each step to find those within $r_c$ would itself cost $O(N^2)$.

The count: each of the $N$ atoms can pair with $N-1$ others, and dividing by 2 avoids counting the pair $i$-$j$ again as $j$-$i$. For $N = 100{,}000$ that is $5\times10^9$ distances to compute at every step.

Yet few of those pairs are within the cutoff. Water has about 100 atoms per nm$^3$, so a sphere of radius 1.0 nm, with a volume of $\tfrac43\pi\times1.0^3 = 4.2$ nm$^3$, holds about 420 atoms. The pairs that matter number $100{,}000\times420/2 = 2\times10^7$, about 240 times fewer. The cutoff has made the energy cheap, and the search for the pairs has become the expensive part.

### Neighbour lists

<div data-videos="OURKkL8XqDo"></div>

Atoms in a liquid move slowly compared with the length of a time step, so an atom has almost the same neighbours now as it had ten steps ago. A neighbour list uses this: find the neighbours once, write them down, and reuse the list for a number of steps.

- **Verlet list.** For each atom keep a list of all atoms within $r_l = r_c + \delta$, where $\delta$ is the "skin" or buffer. Use the list for many steps. It is guaranteed to stay valid until some atom has moved more than $\delta/2$, because only then can a pair that was outside $r_l$ come inside $r_c$.
- **Cell list.** Divide the box into cells of edge at least $r_l$. Neighbours of an atom can only be in its own cell or the 26 around it. Building the Verlet list this way costs $O(N)$.

<div class="legend" markdown="1">
- $r_c$: the cutoff distance of the interaction, in nm.
- $\delta$: the skin, an extra margin (say 0.1 nm) added so that the list stays correct while the atoms move.
- $r_l$: the radius used when the list is built, $r_c + \delta$.
- $\delta/2$: half the skin. It is the distance each of two atoms may travel before the pair can have closed a gap of $\delta$.
- $O(N)$: the cost grows in proportion to the number of atoms $N$.
</div>

Why $\delta/2$. A pair that is not on the list was further apart than $r_c+\delta$ when the list was built. To come within $r_c$ the two atoms must reduce their distance by more than $\delta$. In the worst case they fly straight towards each other, and each needs to cover $\delta/2$. As long as no atom has moved that far, no pair is missing.

A number. A water molecule at 300 K has a mean thermal speed of about 0.6 nm/ps (from the Maxwell-Boltzmann distribution of Module 3). In a time step of 2 fs it covers about 0.0012 nm. With a skin of $\delta = 0.1$ nm it would need about 40 steps in a straight line to cover $\delta/2 = 0.05$ nm, and in a liquid it does not move in a straight line. So one list serves for some tens of steps, and during those steps the program computes only the pairs on the list.

Building the list still requires finding all pairs within $r_l$, and the cell list does that without testing all pairs. The 26 cells around a cell are its neighbours in a block of $3\times3\times3 = 27$ cells, minus the cell itself. Because a cell is at least $r_l$ wide, an atom further away than the neighbouring cells is certainly further away than $r_l$. Sorting the atoms into cells takes one pass over the atoms.

Then each atom is compared only with the atoms of 27 cells, a number that depends on the density and on $r_l$ and not on the size of the system. With 100 atoms per nm$^3$ and $r_l = 1.1$ nm that is $27\times100\times1.1^3\approx3600$ candidates per atom, whether the box holds ten thousand atoms or ten million. The total work is that number times $N$.

Modern codes build on these ideas. GROMACS sorts the atoms on a grid into small clusters of fixed size and keeps a buffered list of cluster pairs, so that SIMD instructions or a GPU can process whole clusters together ([Páll and Hess 2013](cite:pall2013)). It chooses the buffer automatically from the temperature and the allowed energy drift (`verlet-buffer-tolerance`). You rarely set this by hand, but you should recognise that a too-small buffer or too-infrequent update shows up as energy drift.

The words of this paragraph:

- A **cluster** is a small group of atoms that lie close together. The list stores pairs of clusters in place of pairs of atoms.
- **SIMD instructions** ("single instruction, multiple data") are processor instructions that do the same arithmetic on several numbers at once. A **GPU** is a graphics card, which does the same on thousands of numbers at once. Both are fast only when the data come in regular blocks, which is what clusters of fixed size provide.
- A **buffered** list is a list with a skin $\delta$, as above.
- **Energy drift** is a slow, steady change of the total energy in a run that should conserve it (Module 2). Here it has a direct cause: if the skin is too small or the list is kept for too long, some pairs come within $r_c$ without being on the list. Their interaction is missing until the next update and then appears suddenly, and each such event changes the total energy a little.

## Why electrostatics cannot be cut off

The second non-bonded interaction of a force field is the one between charges. The shell argument that justified the Lennard-Jones cutoff gives the opposite answer here. This section explains why, and what goes wrong in a simulation that cuts the interaction off anyway.

<div class="box physics" markdown="1">
**Physics you need here: charge and Coulomb's law.** In a force field every atom carries a fixed **partial charge**, a positive or negative number given in units of the proton charge $e$ (Module 5). Two charges $q_i$ and $q_j$ at a distance $r$ have the Coulomb energy

$$
U_C(r) = \frac{q_iq_j}{4\pi\varepsilon_0\,r} = 138.935\ \frac{q_iq_j}{r}\ \text{kJ/mol}\qquad(q \text{ in } e,\ r \text{ in nm}).
$$

Here $\varepsilon_0$ is the permittivity of vacuum, a constant of nature that fixes the strength of the electric interaction. In the units of MD the combination $1/(4\pi\varepsilon_0)$ is the number 138.935 kJ mol$^{-1}$ nm $e^{-2}$. Two charges of the same sign have a positive energy that falls when they move apart, so they repel. Two charges of opposite sign attract.

The energy falls as $1/r$: at twice the distance it is half as large. Compare that with the Lennard-Jones attraction, which at twice the distance is 64 times smaller. More in the [primer](physics.html#electrostatics).
</div>

The Coulomb energy falls as $1/r$, while the number of charges in a shell at distance $r$ grows as $r^2$.

Put the two together as in the previous section. A shell holds a number of charges proportional to $r^2$, each with an energy proportional to $1/r$, so the contribution of a shell is proportional to $r^2\times r^{-1} = r$. It grows with distance. If all charges had the same sign, the sum of the shells out to a distance $R$ would grow as $R^2$ and never settle. The two interactions side by side:

| Interaction | Energy of one pair | Partners in a shell | Contribution of a shell | Sum of all shells beyond $r_c$ |
|---|---|---|---|---|
| Lennard-Jones attraction | $\propto r^{-6}$ | $\propto r^{2}$ | $\propto r^{-4}$ | finite, $\propto 1/r_c^3$ |
| Coulomb | $\propto r^{-1}$ | $\propto r^{2}$ | $\propto r$ | no finite value |

The contribution of each shell grows with distance unless positive and negative charges cancel, so the sum over all periodic images is only **conditionally convergent**: its value depends on the order of summation.

A solution as a whole is neutral, so every distant shell holds positive and negative charges in almost equal amounts. Their contributions are both large and almost cancel. The result is a small difference between two very large numbers, and a sum of that kind behaves in a way that finite sums never do.

<div class="box maths" markdown="1">
**Maths you need here: sums whose value depends on the order.** When you add finitely many numbers, the order does not matter. With infinitely many it can. Take

$$
1 - \tfrac12 + \tfrac13 - \tfrac14 + \tfrac15 - \tfrac16 + \dots = \ln 2 = 0.693 .
$$

Here $\ln$ is the natural [logarithm](maths.html#exp-log). Now add the same numbers in another order, one positive term followed by two negative ones:

$$
1 - \tfrac12 - \tfrac14 + \tfrac13 - \tfrac16 - \tfrac18 + \tfrac15 - \dots = \tfrac12\ln 2 = 0.347 .
$$

Every term of the first sum appears exactly once in the second, and the result is half as large. This can happen when the positive terms alone add up to infinity and the negative terms alone to minus infinity. The result is then a balance between two infinite amounts, and it depends on how fast you take terms from each.

Such a sum is called **conditionally convergent**. A sum whose terms add up to a finite number even when all signs are made positive is **absolutely convergent**, and its value is the same in any order. The Lennard-Jones tail is of the second kind. The Coulomb sum is of the first.
</div>

For the periodic system, "the order of summation" means the order in which the copies of the box are added. You can add them in growing spheres around the central box, or in growing slabs, and the answers differ. Physically, each order builds a very large crystal of a different outer shape, and the charges on the surface of that crystal act back on the inside however large it gets. A method for electrostatics has to fix this choice. Ewald summation does, in a way described under "tin-foil" below.

A plain cutoff at 1 nm discards interactions that are individually large (two unit charges at 1 nm: 139 kJ/mol) and leaves a net charge inside every cutoff sphere.

A **unit charge** is a charge of $1\,e$, for example a sodium ion. The number comes from the formula in the box: $138.935\times1\times1/1.0 = 139$ kJ/mol, which is 56 times $k_BT$ at 300 K. At the same distance the Lennard-Jones energy of a pair, with the illustrative numbers of the previous section, is about 0.002 kJ/mol. So the cutoff that removed almost nothing from the Lennard-Jones energy removes very large terms here.

The **net charge** of a region is the sum of all charges inside it. A water molecule is neutral as a whole, with a negative partial charge on the oxygen and positive ones on the hydrogens. The cutoff sphere of an atom cuts through the molecules at its edge: the oxygen of a molecule can be inside while one of its hydrogens is outside. The charges inside the sphere then do not add up to zero, and the atom at the centre feels a net charge that does not exist in the real liquid.

The known artefacts include artificial layering of water at the cutoff distance, wrong ion-ion distributions, distorted DNA and unstable proteins, and wrong dielectric properties.

"Ion-ion distributions" are the radial distribution functions $g(r)$ between ions, which say how often two ions are found at each distance. "Dielectric properties" describe how strongly the liquid weakens the interaction between charges, explained in the box below.

Two approaches are used. **Reaction field** treats everything beyond the cutoff as a dielectric continuum (see the end of this module). **Ewald summation** computes the full periodic sum exactly, and is the standard for atomistic simulation.

<div class="box physics" markdown="1">
**Physics you need here: dielectrics and the dielectric constant.** A **dielectric** is a material that does not conduct electricity but responds to charges. A water molecule has a positive and a negative end (it has a **dipole**), and near a charge the molecules turn so that the end of opposite sign points towards it. This response is called **polarisation**. The turned molecules partly cancel the effect of the charge, so two charges inside the material interact more weakly than in vacuum. This weakening is called **screening**.

The factor by which the interaction is weakened is the **dielectric constant** $\varepsilon_r$ (also called relative permittivity), a pure number:

$$
U_C(r) = \frac{q_iq_j}{4\pi\varepsilon_0\,\varepsilon_r\,r} .
$$

Vacuum has $\varepsilon_r = 1$ and liquid water about 80. A **continuum** description forgets the single molecules and treats the material as a uniform medium with this one number. A simulation that contains the water molecules explicitly uses $\varepsilon_r = 1$ in the formula, because the molecules do the screening themselves (Module 5).

A **conductor**, such as a metal, contains charges that move freely until they cancel a field completely. It behaves like a dielectric with an infinitely large $\varepsilon_r$. More in the primer, under [Coulomb's law](physics.html#electrostatics) and [dipoles](physics.html#dipoles).
</div>

## Ewald summation

<div data-videos="SSmIMof0KvA DnOTgjUZxbE YPryFf7MQTg"></div>

The task of this section is to compute the electrostatic energy of the periodic system exactly: every charge with every other charge and with all the images. Done directly, the sum converges slowly and only conditionally. Ewald summation gets its value by rearranging it into two sums that both converge quickly.

The idea in one sentence: write $1/r$ as the sum of a part that is sharp but short-ranged and a part that is long-ranged but smooth. The first part is summed over nearby pairs with a cutoff, like the Lennard-Jones energy. The second is summed as a small number of waves.

The section has five steps: the sum we want, the trick, the three terms of the result one by one, the total with its corrections, and the choice of the parameter $\alpha$. For a first reading, the first two steps and the summary table under "The total" are the essential ones.

### The sum we want

We want the electrostatic energy of $N$ charges in a box of volume $V$ with all periodic images $\mathbf n$ (in units where $1/4\pi\varepsilon_0=1$; multiply by 138.935 for kJ/mol with nm and $e$):

$$
U = \frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}\frac{q_iq_j}{|\mathbf r_{ij}+\mathbf n|},
$$

where the prime means $i\neq j$ when $\mathbf n=0$.

<div class="legend" markdown="1">
- $U$: the total Coulomb energy of the periodic system, counted for one box.
- $q_i$, $q_j$: the charges of atoms $i$ and $j$, in units of $e$.
- $\sum_{i,j}$: a double sum. $i$ runs over all $N$ charges of the central box, and so does $j$.
- $\mathbf r_{ij}$: the vector from charge $j$ to charge $i$ inside the central box, $\mathbf r_i-\mathbf r_j$.
- $\mathbf n$: a **lattice vector**, the shift that leads from the central box to one of its copies. For a rectangular box it is $(aL_x, bL_y, cL_z)$ with whole numbers $a$, $b$, $c$ that can be positive, negative or zero. $\mathbf n = 0$ is the central box itself.
- $\sum_{\mathbf n}$: a sum over all copies, without end.
- $|\mathbf r_{ij}+\mathbf n|$: the distance between charge $j$ and the image of charge $i$ in the copy $\mathbf n$. The bars mean "length of the vector".
- The prime on the sum: in the central box ($\mathbf n=0$) the terms with $i = j$ are left out, because a charge does not interact with itself. In the other boxes $i=j$ stays in: a charge does interact with its own images.
- $\tfrac12$: every pair appears twice in the double sum, once as $(i,j)$ and once as $(j,i)$.
</div>

About the units. The constant $1/4\pi\varepsilon_0$ would stand in front of every formula of this section, so it is left out to keep them short. The energies then come out in units of $e^2$/nm, and you multiply by 138.935 at the end to get kJ/mol. For example, two unit charges 1 nm apart have $q_iq_j/r = 1$ in these units, which is 138.935 kJ/mol.

This is the sum that the previous section showed to be conditionally convergent. Adding it term by term is both slow and ambiguous. The rest of the section replaces it by something that can be computed.

<div class="box physics" markdown="1">
**Physics you need here: charge density, potential and Poisson's equation.** Three ideas are used from here on.

A **charge density** $\rho(\mathbf r)$ describes charge that is spread out in space and does not sit at points. It is the amount of charge per unit volume near the point $\mathbf r$. A "charge cloud" is a charge density. Its total charge is the integral of $\rho$ over all space.

The **electrostatic potential** $\phi(\mathbf r)$ is the energy that a test charge of $+1$ would have at the point $\mathbf r$ because of all the other charges. A charge $q$ placed there has the energy $q\,\phi(\mathbf r)$. In the units of this section a point charge $q_j$ creates the potential $q_j/r$ at the distance $r$, and the potentials of several charges add.

**Poisson's equation**, $\nabla^2\phi = -4\pi\rho$, connects the two: if you know the charge density everywhere, it determines the potential. The Laplacian $\nabla^2\phi$ is the sum of the second derivatives of $\phi$ along $x$, $y$ and $z$. It measures how much $\phi$ at a point differs from its average over the points around it. You will not have to solve this equation. One fact is used later: for a wave, taking the Laplacian is the same as multiplying by a number.

One consequence is used several times. Seen from outside, a round cloud of total charge $q$ creates the same potential as a point charge $q$ at its centre. More in the toolbox under [divergence and Laplacian](maths.html#divergence) and in the [primer](physics.html#electrostatics).
</div>

### The trick: wrap every charge in a cloud

The function $1/r$ is difficult for two reasons at the same time. At short distance it is sharp: it changes steeply and becomes infinite at $r = 0$. At long distance it decays slowly.

A sharp function is handled well pair by pair, if it is also short-ranged. A slowly decaying function is handled well as a sum of waves, if it is also smooth. $1/r$ is neither short-ranged nor smooth, so neither method works on its own.

Nature offers a hint. A neutral atom is a positive nucleus inside a negative cloud of electrons, and from a distance it exerts almost no electric force, because the cloud cancels the nucleus. Ewald summation does the same thing artificially to every charge of the system. The clouds are a device of the calculation and not part of the physics, so they must be taken out again at the end.

**The trick.** Around each point charge $q_i$, add a Gaussian cloud of charge $-q_i$ with width set by a parameter $\alpha$,

$$
\rho_i^{G}(\mathbf r) = -q_i\left(\frac{\alpha^2}{\pi}\right)^{3/2}e^{-\alpha^2|\mathbf r-\mathbf r_i|^2},
$$

and then subtract the same clouds again.

<div class="legend" markdown="1">
- $\rho_i^{G}(\mathbf r)$: the charge density of the cloud placed around charge $i$, at the point $\mathbf r$. The $G$ stands for Gaussian. This $\rho$ is a charge per volume, not a number density.
- $\mathbf r$: any point in space. $\mathbf r_i$: the position of charge $i$, which is the centre of its cloud.
- $|\mathbf r-\mathbf r_i|$: the distance of the point from that centre.
- $q_i$: the point charge. The minus sign gives the cloud the opposite sign, and its total charge is $-q_i$.
- $\alpha$: the **splitting parameter** (also called the Ewald parameter), in nm$^{-1}$. Its inverse $1/\alpha$ sets the width of the cloud: a large $\alpha$ means a narrow cloud. A typical value is 3 nm$^{-1}$.
- $e^{-\alpha^2|\mathbf r-\mathbf r_i|^2}$: the bell shape. It is 1 at the centre, 0.37 at the distance $1/\alpha$, and practically zero beyond a few times $1/\alpha$.
- $(\alpha^2/\pi)^{3/2}$: the factor that makes the total charge of the cloud come out as exactly $-q_i$ (see the box below).
- $\pi$: the number 3.14159.
</div>

<div class="box maths" markdown="1">
**Maths you need here: the Gaussian in three dimensions.** The function $e^{-\alpha^2x^2}$ is the bell curve, also called a Gaussian. Its area is known: $\int_{-\infty}^{\infty}e^{-\alpha^2x^2}dx = \sqrt\pi/\alpha$.

In three dimensions, $e^{-\alpha^2(x^2+y^2+z^2)}$ is the product of three such bells, one for each of $x$, $y$ and $z$. Its integral over all space is therefore $(\sqrt\pi/\alpha)^3 = (\pi/\alpha^2)^{3/2}$. Multiplying the bell by $(\alpha^2/\pi)^{3/2}$, the inverse of that number, gives a cloud whose total is exactly 1. That is the factor in the formula above.

The width of the bell is described by its standard deviation along each axis, $1/(\alpha\sqrt2)$. For $\alpha = 3.12$ nm$^{-1}$ that is 0.23 nm, about the size of an atom. More in the [toolbox](maths.html#gaussian).
</div>

Adding a cloud and taking it away again changes nothing: the total charge distribution is what it was. But the three ingredients can now be grouped differently,

$$
\text{point charges} = \big(\text{point charges} + \text{clouds of } {-q_i}\big) + \big(\text{clouds of } {+q_i}\big).
$$

<div class="legend" markdown="1">
- Point charges: the real charges $q_i$ of the atoms, each at its position $\mathbf r_i$.
- Clouds of $-q_i$: the Gaussian screening clouds of the formula above, one around each charge.
- Clouds of $+q_i$: the same clouds with the sign reversed. They undo the screening clouds, so that the right side adds up to the left side.
</div>

This splits the problem into two easy pieces:

- **Point charges plus screening clouds.** Seen from a distance, each charge with its cloud is neutral, so its potential dies off quickly. This part is short-ranged and can be summed directly with a cutoff.
- **Minus the clouds.** A smooth, periodic charge distribution. Smooth periodic functions have rapidly converging Fourier series, so this part is summed in reciprocal space.

Some comments on the two pieces. In the first, the round cloud of total charge $-q_i$ looks from outside like a point charge $-q_i$ at the same place, and cancels the $+q_i$ that sits there. "From a distance" means a few cloud widths, which is less than a nanometre. Inside the cloud the cancellation is incomplete, and that remainder is the short-ranged interaction.

In the second piece, "minus the clouds" are the clouds of $+q_i$: bells with the same sign as the point charges they belong to. This distribution has no sharp points, and it repeats from box to box because the charges do. A **Fourier series** writes a periodic function as a sum of waves, and **reciprocal space** is the name for working with those waves. Both are explained further down, where they are used.

### The error function and the split of 1/r

The split of the charges into two groups becomes a split of the function $1/r$ into two functions. To write them down, one new function is needed.

<div class="box maths" markdown="1">
**Maths you need here: the error function.** The area under the bell curve $e^{-t^2}$ between 0 and $x$ cannot be written with the usual functions (powers, exponentials, sines). It has therefore been given a name of its own, the **error function**:

$$
\mathrm{erf}(x) = \frac{2}{\sqrt\pi}\int_0^x e^{-t^2}\,dt , \qquad \mathrm{erfc}(x) = 1 - \mathrm{erf}(x).
$$

The factor $2/\sqrt\pi$ is chosen so that $\mathrm{erf}(x)$ tends to 1 when $x$ becomes large. So $\mathrm{erf}$ starts at 0, rises, and levels off at 1. The **complementary error function** $\mathrm{erfc}$ is what is missing to 1: it starts at 1 and falls to 0, and for large $x$ it falls about as fast as $e^{-x^2}$, much faster than any power of $1/x$.

| $x$ | 0 | 0.5 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| $\mathrm{erf}(x)$ | 0 | 0.520 | 0.843 | 0.9953 | 0.99998 |
| $\mathrm{erfc}(x)$ | 1 | 0.480 | 0.157 | 0.0047 | 0.000022 |

For small $x$ the bell is close to 1 over the whole range of the integral, so $\mathrm{erf}(x)\approx 2x/\sqrt\pi$. Every numerical library has both functions (in Python, `math.erf` and `math.erfc`). More in the [toolbox](maths.html#gaussian).
</div>

The split is the identity

$$
\frac1r = \underbrace{\frac{\mathrm{erfc}(\alpha r)}{r}}_{\text{short-ranged}} + \underbrace{\frac{\mathrm{erf}(\alpha r)}{r}}_{\text{smooth, long-ranged}},
$$

because $q\,\mathrm{erf}(\alpha r)/r$ is the potential of a Gaussian charge cloud.

<div class="legend" markdown="1">
- $r$: the distance from a charge, in nm.
- $1/r$: the potential of a point charge of $+1$ at that distance, in the units of this section. It is the Coulomb interaction that has to be split.
- $\alpha$: the splitting parameter, in nm$^{-1}$.
- $\alpha r$: the distance measured in units of $1/\alpha$, a pure number.
- $\mathrm{erf}$, $\mathrm{erfc}$: the error function and the complementary error function of the box above.
- $\mathrm{erfc}(\alpha r)/r$: the potential of the unit charge together with its screening cloud.
- $\mathrm{erf}(\alpha r)/r$: the potential of a cloud of $+1$ alone.
- $q$ (in the sentence under the formula): the total charge of a cloud.
- The braces underneath only attach the two names. They are not part of the formula.
</div>

As a piece of algebra the identity says little: $\mathrm{erfc} + \mathrm{erf} = 1$ by definition, so the two fractions add up to $1/r$ for any value of $\alpha$. What matters is the physical meaning of each fraction. A Gaussian cloud of total charge $q$ creates the potential $q\,\mathrm{erf}(\alpha r)/r$ at the distance $r$ from its centre. A point charge $q$ with a screening cloud of $-q$ around it therefore creates $q/r - q\,\mathrm{erf}(\alpha r)/r = q\,\mathrm{erfc}(\alpha r)/r$.

Read the two parts through their limits:

- *Far away* ($\alpha r$ large). $\mathrm{erf}$ is 1, so the cloud alone gives $q/r$, the potential of a point charge. Its shape no longer matters. $\mathrm{erfc}$ is 0, so the charge with its screening cloud gives nothing.
- *Close by* ($r$ towards 0). $\mathrm{erf}(\alpha r)\approx2\alpha r/\sqrt\pi$, so $\mathrm{erf}(\alpha r)/r$ tends to the finite number $2\alpha/\sqrt\pi$. The cloud has no infinite peak at its centre, and that is the meaning of "smooth". The infinite peak of $1/r$ is entirely in the $\mathrm{erfc}$ part.

In numbers, for $\alpha = 3.12$ nm$^{-1}$ (all three columns in nm$^{-1}$; multiply by 138.935 for the energy of two unit charges in kJ/mol):

| $r$ (nm) | $1/r$ | $\mathrm{erfc}(\alpha r)/r$ | $\mathrm{erf}(\alpha r)/r$ |
|---|---|---|---|
| 0.1 | 10.0 | 6.59 | 3.41 |
| 0.3 | 3.33 | 0.62 | 2.71 |
| 0.5 | 2.00 | 0.055 | 1.95 |
| 1.0 | 1.00 | 0.00001 | 1.00 |

At 1.0 nm the short-ranged part has dropped to a hundred-thousandth of the full interaction, so it can be cut off there. The smooth part never exceeds $2\alpha/\sqrt\pi = 3.52$ nm$^{-1}$.

<details markdown="1"><summary>Optional: checking that erf(αr)/r is the potential of a Gaussian cloud</summary>
Exercise 4 asks you to derive this by solving Poisson's equation. Here is the check in the other direction: insert $\phi = q\,\mathrm{erf}(\alpha r)/r$ into the equation and see that the Gaussian comes out.

For a function that depends only on the distance $r$ from the centre, the Laplacian is $\nabla^2\phi = \dfrac1r\dfrac{d^2}{dr^2}(r\phi)$. Here $r\phi = q\,\mathrm{erf}(\alpha r)$.

*First derivative.* By its definition, the derivative of $\mathrm{erf}(x)$ is $\tfrac{2}{\sqrt\pi}e^{-x^2}$. With $x=\alpha r$ the chain rule adds a factor $\alpha$: $\dfrac{d}{dr}\,q\,\mathrm{erf}(\alpha r) = q\,\dfrac{2\alpha}{\sqrt\pi}\,e^{-\alpha^2r^2}$.

*Second derivative.* Differentiating $e^{-\alpha^2r^2}$ gives $-2\alpha^2r\,e^{-\alpha^2r^2}$, so $\dfrac{d^2}{dr^2}\,q\,\mathrm{erf}(\alpha r) = -q\,\dfrac{4\alpha^3r}{\sqrt\pi}\,e^{-\alpha^2r^2}$.

*Divide by $r$.* $\nabla^2\phi = -q\,\dfrac{4\alpha^3}{\sqrt\pi}\,e^{-\alpha^2r^2}$.

*Compare.* Poisson's equation asks for $-4\pi\rho$, and for a cloud of charge $q$ that is $-4\pi q\,(\alpha^2/\pi)^{3/2}e^{-\alpha^2r^2}$. Since $4\pi(\alpha^2/\pi)^{3/2} = 4\pi\alpha^3/\pi^{3/2} = 4\alpha^3/\sqrt\pi$, the two sides agree.
</details>

In the demo you can move $\alpha$ and the cutoff and see how the two parts share the interaction between them.

<div class="widget" data-widget="ewald"></div>

### The real-space term

The first piece is the interaction of every charge with the other charges as they look through their screening clouds. It is called the real-space term because it is computed in ordinary space, from positions and distances, in contrast to the reciprocal space of waves used for the second piece.

**Real-space term.** The screened interaction, summed over pairs within the cutoff:

$$
U_{real} = \frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\,\frac{\mathrm{erfc}(\alpha|\mathbf r_{ij}+\mathbf n|)}{|\mathbf r_{ij}+\mathbf n|}.
$$

<div class="legend" markdown="1">
- $U_{real}$: the real-space part of the Coulomb energy.
- $\mathrm{erfc}(\alpha|\mathbf r_{ij}+\mathbf n|)$: the complementary error function, evaluated at the distance between charge $j$ and the image of charge $i$ in the copy $\mathbf n$, multiplied by $\alpha$.
- Other symbols ($\tfrac12$, $\sum_{\mathbf n}$ with its prime, $\sum_{i,j}$, $q_i$, $q_j$, $\mathbf r_{ij}$, $\mathbf n$, the bars): as in the list under "The sum we want".
</div>

Read it like this: it is the sum we started from, with $1/r$ replaced by $\mathrm{erfc}(\alpha r)/r$. The sum over the copies $\mathbf n$ is still there, but the factor $\mathrm{erfc}$ makes every term beyond about 1 nm negligible. With a cutoff of at most half the box, each pair contributes at most once, through its nearest image, and the images of a charge itself are too far away to contribute. What a program evaluates is

$$
U_{real} \approx \sum_{i<j,\; r_{ij}<r_c} q_iq_j\,\frac{\mathrm{erfc}(\alpha r_{ij})}{r_{ij}} .
$$

<div class="legend" markdown="1">
- $\sum_{i<j,\; r_{ij}<r_c}$: a sum over all pairs of charges, each pair counted once, and only pairs closer than the cutoff. Counting each pair once replaces the factor $\tfrac12$.
- $r_{ij}$: the distance between charges $i$ and $j$ after the minimum-image convention.
- $r_c$: the real-space cutoff.
- $\approx$: "approximately equal". The terms beyond the cutoff are dropped.
- Other symbols: as in the list above.
</div>

This is a pair sum with a cutoff, of the same kind as the Lennard-Jones sum, and programs compute both in the same loop over the same neighbour list. The size of what is dropped is set by $\mathrm{erfc}(\alpha r_c)$. With $\alpha = 3.12$ nm$^{-1}$ and $r_c = 1.0$ nm it is $10^{-5}$, so two unit charges at the cutoff have a real-space energy of $138.935\times10^{-5} = 0.0014$ kJ/mol, against 139 kJ/mol for the full interaction.

### The reciprocal-space term

The second piece is the energy of the charges in the potential of the smooth clouds of $+q_i$. It is long-ranged, so no cutoff in distance is possible. But it is smooth and periodic, and such a function is described economically by waves. Two tools are needed before the formulas.

<div class="box maths" markdown="1">
**Maths you need here: Fourier series and wave vectors.** Take a function $f(x)$ that repeats after a length $L$, so that $f(x+L) = f(x)$. A **Fourier series** builds it from waves that each fit a whole number of times into $L$:

$$
f(x) = a_0 + \sum_{n=1}^{\infty}\left[a_n\cos\!\left(\frac{2\pi n x}{L}\right) + b_n\sin\!\left(\frac{2\pi n x}{L}\right)\right].
$$

The whole number $n$ counts how many full waves fit into $L$, so the wavelength is $L/n$. The numbers $a_n$ and $b_n$ say how much of each wave the function contains. They are its **Fourier coefficients**, and $a_0$ is the average of $f$. Example: $f(x) = 3 + 2\cos(2\pi x/L)$ has two coefficients that are not zero, $a_0 = 3$ and $a_1 = 2$.

It is convenient to write $k = 2\pi n/L$, the **wave number**, so that the wave is $\cos(kx)$. Its unit is one over a length (nm$^{-1}$), and a large $k$ means a short wavelength $\lambda$, because $\lambda = 2\pi/k$. In three dimensions a wave can have $n_x$ periods along $x$, $n_y$ along $y$ and $n_z$ along $z$, and its three wave numbers form the **wave vector** $\mathbf k = 2\pi(n_x/L_x,\ n_y/L_y,\ n_z/L_z)$. The wave vector points in the direction in which the wave runs, and its length is $2\pi/\lambda$.

A function can be described by its value at every point, or by its coefficient for every wave. The two descriptions hold the same information. The first is called **real space**. The second is called **reciprocal space** (the unit of $k$ is the reciprocal of a length), or Fourier space, or $k$-space.

*Why a smooth function needs few waves.* A wave cannot draw details much finer than its wavelength. To build a bump of width $w$ you need wavelengths down to about $w$, and shorter ones add almost nothing. A bell 0.3 nm wide needs wavelengths down to about 0.3 nm, which means $k$ up to about $2\pi/0.3\approx20$ nm$^{-1}$.

A point charge has no width at all, so it needs every wavelength, however short, and its series never ends. This is why Ewald summation replaces points by clouds. More in the [toolbox](maths.html#fourier).
</div>

<div class="box maths" markdown="1">
**Maths you need here: the complex exponential.** A wave needs a cosine and a sine. The **complex exponential** carries both in one symbol:

$$
e^{i\theta} = \cos\theta + i\sin\theta .
$$

Here $i$ is the imaginary unit, defined by $i^2 = -1$ (not the label of an atom), and $\theta$ is any angle in radians. A complex number $z = a + ib$ has a real part $a$ and an imaginary part $b$. Its size squared is $\vert z\vert^2 = a^2 + b^2$, a real number that is never negative. Its complex conjugate is $z^{*} = a - ib$, and $z\,z^{*} = \vert z\vert^2$.

Examples: $e^{i\cdot0} = 1$, $e^{i\pi/2} = i$, $e^{i\pi} = -1$ and $e^{2\pi i} = 1$. For any angle, $\vert e^{i\theta}\vert^2 = \cos^2\theta + \sin^2\theta = 1$.

In the formulas below, every complex exponential can be replaced by its cosine and its sine, and the energy at the end is an ordinary real number. The complex notation keeps the formulas short. More in the [toolbox](maths.html#complex).
</div>

**Reciprocal-space term.** The Gaussian clouds form a periodic density with Fourier coefficients $\tilde\rho(\mathbf k) = S(\mathbf k)\,e^{-k^2/4\alpha^2}$, where the **structure factor** is

$$
S(\mathbf k) = \sum_{j=1}^Nq_j\,e^{i\mathbf k\cdot\mathbf r_j},\qquad \mathbf k = 2\pi\left(\frac{n_x}{L_x},\frac{n_y}{L_y},\frac{n_z}{L_z}\right).
$$

<div class="legend" markdown="1">
- $S(\mathbf k)$: the structure factor, one complex number for each wave vector. It measures how strongly the arrangement of the charges follows the wave $\mathbf k$.
- $\mathbf k$: a wave vector, in nm$^{-1}$. Its length is written $k$, and $k^2 = k_x^2+k_y^2+k_z^2$.
- $n_x$, $n_y$, $n_z$: whole numbers (positive, negative or zero), the number of periods of the wave along each box edge. They are not the components of the lattice vector $\mathbf n$.
- $L_x$, $L_y$, $L_z$: the box edges, in nm. $2\pi$: the angle of one full turn, in radians.
- $\sum_{j=1}^N$: a sum over all $N$ charges of the central box.
- $q_j$: the charge of atom $j$. $\mathbf r_j$: its position.
- $\mathbf k\cdot\mathbf r_j$: the [dot product](maths.html#dot-product) $k_xx_j+k_yy_j+k_zz_j$. It is the phase of the wave at the position of charge $j$, an angle in radians.
- $e^{i\mathbf k\cdot\mathbf r_j}$: the complex exponential of that angle, $\cos(\mathbf k\cdot\mathbf r_j) + i\sin(\mathbf k\cdot\mathbf r_j)$. Here $i$ is the imaginary unit.
- $\tilde\rho(\mathbf k)$ (in the sentence above the formula): the Fourier coefficient of the charge density of the clouds for the wave $\mathbf k$.
- $e^{-k^2/4\alpha^2}$: a Gaussian factor in $k$. It is close to 1 for long waves (small $k$) and close to 0 for short ones. $\alpha$ is the splitting parameter.
</div>

Read $S(\mathbf k)$ like this: every charge votes with the value of the wave at its own position, weighted by its charge. If the positive charges sit on the crests of the wave and the negative charges in its troughs, the votes add up and $S$ is large. If the charges are placed without any relation to the wave, the votes cancel and $S$ is close to zero.

A small example. In a box of length $L$ along $x$, put a charge $+1$ at $x = 0$ and a charge $-1$ at $x = L/2$. For the wave with one period along $x$, which has $k = 2\pi/L$, the phases $kx$ at the two charges are 0 and $\pi$, so $S = e^{i\cdot0} - e^{i\pi} = 1-(-1) = 2$. The charges follow this wave perfectly. For the wave with two periods the phases are 0 and $2\pi$, and $S = 1 - 1 = 0$: this wave has a crest at both charges and cannot tell them apart.

The clouds in question are the clouds of $+q_j$. The factor $e^{-k^2/4\alpha^2}$ is the effect of smearing each point into a bell: long waves do not notice the smearing, and short waves are wiped out by it. In a program the complex numbers disappear, because the only thing needed is $\vert S(\mathbf k)\vert^2 = \big[\sum_jq_j\cos(\mathbf k\cdot\mathbf r_j)\big]^2 + \big[\sum_jq_j\sin(\mathbf k\cdot\mathbf r_j)\big]^2$.

From the density of the clouds to the energy takes two more steps: from the density to the potential, and from the potential to the energy.

Poisson's equation $\nabla^2\phi = -4\pi\rho$ is algebraic in Fourier space, $\tilde\phi(\mathbf k) = 4\pi\tilde\rho(\mathbf k)/k^2$, which gives the potential $\phi_G$ of the smooth clouds. The energy of the point charges in that potential, $\tfrac12\sum_iq_i\,\phi_G(\mathbf r_i)$, then becomes

$$
U_{recip} = \frac{2\pi}{V}\sum_{\mathbf k\neq0}\frac{e^{-k^2/4\alpha^2}}{k^2}\,\big|S(\mathbf k)\big|^2 .
$$

The Gaussian factor makes the sum converge after a modest number of $\mathbf k$ vectors.

<div class="legend" markdown="1">
- $U_{recip}$: the reciprocal-space part of the Coulomb energy, the energy of the point charges in the potential of the smooth clouds.
- $V$: the volume of the box, $L_xL_yL_z$, in nm$^3$.
- $\sum_{\mathbf k\neq0}$: a sum over all allowed wave vectors except $\mathbf k = 0$ (the case $n_x=n_y=n_z=0$, discussed under "The total").
- $k^2$: the squared length of the wave vector, in nm$^{-2}$.
- $e^{-k^2/4\alpha^2}/k^2$: the weight of each wave. The $1/k^2$ comes from Poisson's equation and the Gaussian from the smearing.
- $\big|S(\mathbf k)\big|^2$: the squared size of the structure factor, a real number that is never negative.
- $\phi$, $\tilde\phi(\mathbf k)$ (in the sentence above the formula): the electrostatic potential and its Fourier coefficient for the wave $\mathbf k$. $\phi_G$ is the potential created by all the clouds of $+q_j$ together.
- $2\pi$: a pure number that collects the $4\pi$ of Poisson's equation and the $\tfrac12$ of the energy.
- $\nabla^2$, $\rho$ (in the sentence above the formula): the Laplacian and the charge density of the clouds, as in the box on Poisson's equation.
- Other symbols ($\alpha$, $\mathbf k$, $S(\mathbf k)$, $\tilde\rho(\mathbf k)$, the base $e$ of the exponential): as in the list above.
</div>

"Algebraic" means "solved by ordinary division". Poisson's equation contains second derivatives, and differentiating a wave twice gives the same wave back, multiplied by $-k^2$. So for each wave separately the equation reads $-k^2\tilde\phi = -4\pi\tilde\rho$, and dividing by $-k^2$ solves it. No differential equation is left, which is the reason for going to reciprocal space.

Read $U_{recip}$ like this: every wave contributes the squared strength with which the charges follow it, times a weight. The weight falls quickly with $k$. For $\alpha = 3.12$ nm$^{-1}$ the Gaussian factor is 0.53 at $k = 5$ nm$^{-1}$, 0.077 at 10, 0.0031 at 15 and 0.00003 at 20, and the $1/k^2$ lowers the weight further. So the sum can stop near $k = 20$ nm$^{-1}$, a wavelength of 0.3 nm, which is the estimate of the box on Fourier series.

How many waves is that? As an illustration, stop where the Gaussian factor has fallen to $10^{-5}$, which is at $k = 21.2$ nm$^{-1}$. In a cubic box with an edge of 8 nm the allowed values of each component of $\mathbf k$ are $2\pi/8 = 0.79$ nm$^{-1}$ apart. A sphere of radius 21.2 nm$^{-1}$ in $k$-space then holds about 82,000 wave vectors, and because $\mathbf k$ and $-\mathbf k$ give the same term, about 41,000 have to be computed. That is the "modest number": it is finite, and no sum over distant images is left.

<details markdown="1"><summary>Optional: where the reciprocal-space formula comes from</summary>
Four steps. The convention used here: a function with the periodicity of the box is written as $f(\mathbf r) = \frac1V\sum_{\mathbf k}\tilde f(\mathbf k)\,e^{-i\mathbf k\cdot\mathbf r}$, and its coefficients are $\tilde f(\mathbf k) = \int_V f(\mathbf r)\,e^{i\mathbf k\cdot\mathbf r}\,d^3r$, an integral over the volume of the box. Other texts, and the [toolbox](maths.html#fourier) of this course, put the minus sign in the other exponent, and the toolbox also puts the factor $1/V$ (in one dimension $1/L$) into the coefficient. The energy at the end is the same.

**Step 1: the coefficients of the cloud density.** The clouds of $+q_j$ have the density $\rho_G(\mathbf r) = \sum_jq_j\,G(\mathbf r-\mathbf r_j)$, repeated in every copy of the box, where $G(\mathbf r) = (\alpha^2/\pi)^{3/2}e^{-\alpha^2r^2}$ is a cloud of total charge 1. Integrating the periodic density over one box gives the same result as integrating the clouds of the central box over all space. (The part of a cloud that sticks out of the box is replaced by an equal part of an image cloud that sticks in, and the wave has the same value at both places.) With the substitution $\mathbf s = \mathbf r-\mathbf r_j$,

$$
\tilde\rho(\mathbf k) = \sum_jq_j\,e^{i\mathbf k\cdot\mathbf r_j}\int G(\mathbf s)\,e^{i\mathbf k\cdot\mathbf s}\,d^3s = S(\mathbf k)\,e^{-k^2/4\alpha^2}.
$$

The last integral is a standard result: the wave content of a bell of width $1/\alpha$ is again a bell, of width $2\alpha$ in $k$. A narrow cloud (large $\alpha$) contains a wide range of waves, and a wide cloud a narrow range.

**Step 2: Poisson's equation, wave by wave.** Insert the series for $\phi_G$ and for $\rho_G$ into $\nabla^2\phi = -4\pi\rho$. Differentiating $e^{-i\mathbf k\cdot\mathbf r}$ twice with respect to $x$ multiplies it by $(-ik_x)^2 = -k_x^2$, so the Laplacian multiplies each wave by $-k^2$. Comparing the two sides wave by wave gives $-k^2\tilde\phi_G(\mathbf k) = -4\pi\tilde\rho(\mathbf k)$, that is, $\tilde\phi_G(\mathbf k) = 4\pi\tilde\rho(\mathbf k)/k^2$. For $\mathbf k = 0$ the division is not possible, and that term is left out.

**Step 3: the potential at the position of charge $i$.** Put the coefficients back into the series:

$$
\phi_G(\mathbf r_i) = \frac1V\sum_{\mathbf k\neq0}\frac{4\pi}{k^2}\,e^{-k^2/4\alpha^2}\,S(\mathbf k)\,e^{-i\mathbf k\cdot\mathbf r_i}.
$$

**Step 4: the energy.** Multiply by $q_i$, sum over $i$ and take half. The half is the $\tfrac12$ of the sum we started from: each pair would otherwise be counted twice. The sum over $i$ meets only the last factor, and $\sum_iq_i\,e^{-i\mathbf k\cdot\mathbf r_i}$ is the complex conjugate $S(\mathbf k)^{*}$. With $S\,S^{*} = \vert S\vert^2$,

$$
U_{recip} = \frac12\sum_iq_i\,\phi_G(\mathbf r_i) = \frac{1}{2V}\sum_{\mathbf k\neq0}\frac{4\pi}{k^2}\,e^{-k^2/4\alpha^2}\,S(\mathbf k)\,S(\mathbf k)^{*} ,
$$

and $4\pi/2 = 2\pi$ gives the formula of the main text.
</details>

### The self term

**Self term.** The reciprocal sum includes the interaction of each point charge with its own Gaussian cloud, which is not physical. Remove it:

$$
U_{self} = -\frac{\alpha}{\sqrt\pi}\sum_iq_i^2 .
$$

<div class="legend" markdown="1">
- $U_{self}$: the correction that removes the energy of each charge in the potential of its own cloud.
- $\alpha$: the splitting parameter, in nm$^{-1}$.
- $\sqrt\pi$: the square root of $\pi$, 1.772.
- $\sum_i$: a sum over all $N$ charges.
- $q_i^2$: the square of the charge of atom $i$. It is positive for either sign of the charge, so $U_{self}$ is always negative.
</div>

Where it comes from. The reciprocal term was computed as "all point charges in the potential of all clouds", and "all clouds" includes the cloud that was placed around charge $i$ itself. In the split of the charges, that cloud exists only to undo the screening cloud of charge $i$. Its interaction with its own point charge has no counterpart in the sum we want.

Its size follows from a result above. The potential of the cloud of charge $q_i$ at its own centre is the limit of $q_i\,\mathrm{erf}(\alpha r)/r$ for $r$ towards 0, which is $2\alpha q_i/\sqrt\pi$. The energy of charge $q_i$ in that potential, with the factor $\tfrac12$ that the reciprocal term carries, is $\tfrac12\times q_i\times2\alpha q_i/\sqrt\pi = \alpha q_i^2/\sqrt\pi$. Summing over the charges and changing the sign, to remove it, gives the formula.

Read it like this: the term is large, and it is a constant. For $\alpha = 3.12$ nm$^{-1}$ a unit charge contributes $-3.12/1.772 = -1.76$ in the units of this section, which is $-245$ kJ/mol. It does not depend on where the atoms are, so it creates no force. It only sets the zero of the energy correctly, and it makes the total independent of $\alpha$.

### The total, and what else is in it

**Total.**

$$
\boxed{U_{Coulomb} = U_{real} + U_{recip} + U_{self}\;(+\;U_{excl}\;+\;U_{surface})}
$$

<div class="legend" markdown="1">
- $U_{Coulomb}$: the electrostatic energy of the periodic system, for one box. It is the value of the sum we started from.
- $U_{real}$, $U_{recip}$, $U_{self}$: the three terms derived above.
- $U_{excl}$, $U_{surface}$: two corrections explained below. The round brackets mark them as additions to the basic three-term formula.
- The frame around the formula marks it as the main result.
</div>

| Term | What it is | How it is computed |
|---|---|---|
| $U_{real}$ | Point charges seen through their screening clouds | Pair loop with the cutoff $r_c$, on the same neighbour list as Lennard-Jones |
| $U_{recip}$ | Point charges in the potential of the smooth clouds | Sum over waves $\mathbf k$ (with PME: a grid and a fast Fourier transform) |
| $U_{self}$ | Removes each charge's interaction with its own cloud | A constant, computed once |
| $U_{excl}$ | Removes the smooth part for pairs that should not interact | Loop over the excluded pairs |
| $U_{surface}$ | Depends on what surrounds the infinite lattice | Zero with the usual choice |

Two further corrections appear in practice. Pairs excluded by the topology (1-2 and 1-3 neighbours) are present in the reciprocal sum and must be subtracted, $U_{excl} = -\sum_{excl}q_iq_j\,\mathrm{erf}(\alpha r_{ij})/r_{ij}$. The $\mathbf k=0$ term is omitted, which corresponds to surrounding the infinite lattice with a conductor ("tin-foil" boundary conditions, $U_{surface}=0$) and, for a system with net charge, to adding a uniform neutralising background.

<div class="legend" markdown="1">
- $U_{excl}$: the correction for excluded pairs.
- $\sum_{excl}$: a sum over all excluded pairs of atoms, each pair once.
- $q_i$, $q_j$: the charges of the two atoms of the pair. $r_{ij}$: their distance.
- $\mathrm{erf}(\alpha r_{ij})/r_{ij}$: the smooth part of the split, with the splitting parameter $\alpha$.
- $\mathbf k = 0$: the wave vector with $n_x=n_y=n_z=0$, the "wave" that is the same everywhere.
- $U_{surface}$: the surface term, explained below.
</div>

**Excluded pairs.** In a force field, atoms joined by one bond (1-2) or by two bonds (1-3) have no non-bonded interaction with each other, because the bond and angle terms already describe them (Module 5). The **topology** is the list of atoms and bonds of the system, which defines these pairs. In the real-space term the program leaves such a pair out of the loop. In the reciprocal term it cannot: $S(\mathbf k)$ is built from all charges together, and no single pair can be taken out of it. The smooth part of the interaction of each excluded pair is therefore inside $U_{recip}$ and has to be subtracted by hand.

**The $\mathbf k = 0$ term.** In the formula for $U_{recip}$ the weight contains $1/k^2$, which is infinite at $k = 0$. The quantity it multiplies, $S(0) = \sum_jq_j$, is the total charge of the box, and for a neutral system it is zero. Zero times infinity has no definite value. This is the place where the conditional convergence of the original sum has gone: the missing value depends on the shape of the very large crystal and on the material around it.

Leaving the term out is a definite choice. It corresponds to a crystal surrounded by a conductor, which cancels the field of any charge on the surface of the crystal. Aluminium foil is a conductor, hence the name "tin-foil". With another surrounding, for example vacuum, an extra energy $U_{surface}$ appears. It depends on the total dipole moment of the box, $\sum_iq_i\mathbf r_i$, and on the dielectric constant of the surrounding material, and it is zero for a conductor.

**Net charge.** If the charges of the box do not add up to zero, $S(0)$ is not zero and the $\mathbf k=0$ term would be infinite: an endless lattice of charged boxes has an infinite energy. Leaving the term out removes the average charge density from the calculation. That has the same effect as spreading a charge of the opposite sign evenly over the whole box, so that the total is zero again. This is the "uniform neutralising background". With a net charge the three terms alone are no longer independent of $\alpha$: the background adds one more constant, $-\pi\big(\sum_iq_i\big)^2/(2\alpha^2V)$ with the box volume $V$, which creates no force on the atoms. The warning box in the PME section says what the background does to the results.

### Choosing α: where the work goes

The result does not depend on $\alpha$. A large $\alpha$ (narrow Gaussians) makes the real-space sum converge within a short cutoff and pushes work into reciprocal space, and the reverse. With the best balance, classical Ewald scales as $O(N^{3/2})$.

The first sentence can be seen in numbers. Take eight ions of charge $+1$ and $-1$ arranged as in rock salt, in a cubic box of edge 2 with nearest neighbours at the distance 1 (the system of Exercise 3, in the units of this section). The three terms for three values of $\alpha$:

| $\alpha$ | $U_{real}$ | $U_{recip}$ | $U_{self}$ | Total |
|---|---|---|---|---|
| 1.0 | $-2.49$ | $0.01$ | $-4.51$ | $-6.99$ |
| 2.0 | $-0.11$ | $2.15$ | $-9.03$ | $-6.99$ |
| 3.0 | $-0.0005$ | $6.55$ | $-13.54$ | $-6.99$ |

Each term changes strongly and the total does not move. $\alpha$ is a parameter of the method and not of the physics: it decides how the same energy is shared between the sums.

What $\alpha$ does change is the work. The real-space sum must go out to the distance where $\mathrm{erfc}(\alpha r)$ is negligible, and that distance is proportional to $1/\alpha$. The reciprocal sum must go up to the wave vector where $e^{-k^2/4\alpha^2}$ is negligible, and that wave vector is proportional to $\alpha$. As an illustration, ask for $10^{-5}$ in both:

| $\alpha$ (nm$^{-1}$) | Real-space cutoff, $3.12/\alpha$ (nm) | Largest $k$, $6.79\,\alpha$ (nm$^{-1}$) | Shortest wavelength, $2\pi/k$ (nm) |
|---|---|---|---|
| 2.0 | 1.56 | 13.6 | 0.46 |
| 3.12 | 1.00 | 21.2 | 0.30 |
| 5.0 | 0.62 | 33.9 | 0.19 |

<div class="legend" markdown="1">
- $3.12$: the value of $x$ at which $\mathrm{erfc}(x) = 10^{-5}$. The cutoff must satisfy $\alpha r_c = 3.12$.
- $6.79$: the value of $k/\alpha$ at which $e^{-k^2/4\alpha^2} = 10^{-5}$, equal to $2\sqrt{\ln 10^5}$.
- $2\pi/k$: the wavelength of the wave with wave number $k$.
</div>

A longer cutoff means more pairs: their number grows as $r_c^3$. A larger $k$ means more waves: their number grows as the cube of the largest $k$. Moving $\alpha$ shifts the cost from one sum to the other, and somewhere in between the total cost is lowest.

The last sentence of the paragraph above is about how that lowest cost grows with the size of the system. $O(N^{3/2})$ means that 100 times more atoms cost $100^{3/2} = 1000$ times more. That is better than the $O(N^2)$ of a sum over all pairs, where the factor would be 10,000, but it is far from the $O(N)$ of the Lennard-Jones part.

<details markdown="1"><summary>Optional: where the power 3/2 comes from</summary>
Keep the density and the accuracy fixed and let the number of atoms $N$ grow.

*Real space.* The cutoff is proportional to $1/\alpha$, and each atom has a number of neighbours proportional to $r_c^3$, that is, to $1/\alpha^3$. The cost is $T_{real} = A\,N/\alpha^3$, with a constant $A$.

*Reciprocal space.* Wave vectors are needed up to a largest $k$ proportional to $\alpha$. The allowed wave vectors are $2\pi/L$ apart in each direction, so the number inside a sphere of that radius is proportional to $V\alpha^3$, and at fixed density $V$ is proportional to $N$. Each wave vector needs $S(\mathbf k)$, a sum over $N$ charges. The cost is $T_{recip} = B\,N^2\alpha^3$, with a constant $B$.

*The best $\alpha$.* The total $T = A\,N/\alpha^3 + B\,N^2\alpha^3$ has a first part that falls with $\alpha$ and a second that rises. It is lowest where its derivative with respect to $\alpha$ is zero: $-3AN/\alpha^4 + 3BN^2\alpha^2 = 0$, which gives $\alpha^6 = A/(BN)$, or $\alpha^3 = \sqrt{A/(BN)}$.

*The cost at that $\alpha$.* Inserting it, $T_{real} = AN\sqrt{BN/A} = \sqrt{AB}\,N^{3/2}$ and $T_{recip} = BN^2\sqrt{A/(BN)} = \sqrt{AB}\,N^{3/2}$. The two parts are equal, and the total is $2\sqrt{AB}\,N^{3/2}$.
</details>

### Particle-mesh Ewald

<div data-videos="VWsMUaA7UWw"></div>

The real-space term costs about as much as the Lennard-Jones term, because it uses the same pairs. The reciprocal term is the expensive one, and this section shows how programs make it cheap.

Computing $S(\mathbf k)$ directly costs $N$ operations for each of many $\mathbf k$ vectors. **PME** replaces it.

Numbers show the problem. The 8 nm box of the example above, filled with water, holds about 50,000 atoms. Each of the 41,000 wave vectors needs a sum over all of them: $41{,}000\times50{,}000 = 2\times10^9$ operations per step. The real-space loop of the same system has about $50{,}000\times420/2 = 10^7$ pairs. The reciprocal term would need two hundred times more operations than the real-space loop.

The name says how PME gets around this. "Particle" stands for the charges and "mesh" is another word for a grid. The charges are moved onto a regular grid, because for data on a regular grid there is an algorithm that computes all Fourier coefficients at once. Two tools are needed.

<div class="box maths" markdown="1">
**Maths you need here: interpolation on a grid, Lagrange polynomials and B-splines.** A **grid** is a regular set of points, like the corners of the squares on graph paper. **Interpolation** estimates the value of a function between the grid points from its values at the grid points.

The simplest kind is linear: join two neighbouring grid values by a straight line. At a fraction $u$ of the way from the first point to the second, the estimate is $(1-u)f_0 + uf_1$, where $f_0$ and $f_1$ are the two grid values. Example: $f_0 = 2$, $f_1 = 4$ and $u = 0.3$ give $0.7\times2 + 0.3\times4 = 2.6$. The numbers $1-u$ and $u$ are called **weights**, and they add up to 1.

Interpolation with **Lagrange polynomials** of order $p$ takes the $p$ nearest grid points and uses the one polynomial of degree $p-1$ that passes through all $p$ values. For $p = 2$ this is the straight line above, for $p = 4$ a cubic curve. The pieces do not join smoothly at the places where the set of nearest points changes.

A **B-spline** of order $p$ is a smooth, bell-shaped weight function. It is made of polynomial pieces of degree $p-1$, joined so that the function and its first $p-2$ derivatives have no jumps. Because the slope of a B-spline has no jumps, a quantity built from B-splines can be differentiated to give a force without jumps.

Order 4 is the cubic B-spline. It gives four weights, for the four nearest grid points along a line. At $u = 0.3$ they are 0.057, 0.590, 0.348 and 0.005, which add up to 1.

The same weights work in both directions. They read a function that lives on the grid at the position of a particle (interpolation). And they distribute something that the particle carries, such as its charge, over the grid points around it (spreading).
</div>

<div class="box maths" markdown="1">
**Maths you need here: the fast Fourier transform.** Suppose a function is known at $M$ points of a regular grid. Such data can contain $M$ different waves, so there are $M$ Fourier coefficients to compute. Each coefficient is a sum over all $M$ grid points, and the direct calculation costs $M\times M = M^2$ operations.

The **fast Fourier transform** (FFT) is an algorithm that delivers all $M$ coefficients in about $M\log_2M$ operations. It splits the problem into two halves, each half into two halves again, and reuses the partial results. $\log_2M$ is the number of times $M$ can be halved before 1 is reached: $\log_2 1024 = 10$, and $\log_2 10^6\approx20$. It grows so slowly that $M\log M$ is close to proportional to $M$.

Example: for $M = 300{,}000$ grid points, $M^2 = 9\times10^{10}$ and $M\log_2M = 5.5\times10^6$, sixteen thousand times less. The same algorithm run backwards, the inverse FFT, goes from the coefficients back to the values on the grid. The FFT works only for data on a regular grid, and atoms are not on a grid. That is the reason for the spreading step of PME. More in the toolbox under [Fourier series and transforms](maths.html#fourier) and [logarithms](maths.html#exp-log).
</div>

The original method of [Darden, York and Pedersen 1993](cite:darden1993) interpolated the reciprocal-space pair potential and its gradient with Lagrange polynomials on a grid. The smooth version of [Essmann et al. 1995](cite:essmann1995) is the one in use today, and it interpolates the structure factor itself with B-splines:

1. Spread each charge onto a regular 3D grid using B-spline interpolation (order 4 touches $4^3=64$ grid points per charge).
2. Fast Fourier transform the gridded charge density: $O(M\log M)$ for $M$ grid points.
3. Multiply by the influence function $e^{-k^2/4\alpha^2}/k^2$, corrected for the B-spline spreading.
4. Transform back to get the potential on the grid, and obtain the forces by differentiating the same B-splines analytically. The reciprocal force is then the exact gradient of the approximate energy, so energy is conserved, but momentum is conserved only to within the force error (one reason why codes remove centre-of-mass motion).

<div class="legend" markdown="1">
- $M$: the number of grid points in the box, the product of the numbers along $x$, $y$ and $z$.
- $O(M\log M)$: the cost grows as $M$ times the logarithm of $M$, which is close to proportional to $M$.
- $4^3 = 64$: four grid points along each of the three directions.
- $k$: the length of a wave vector. $\alpha$: the splitting parameter.
- $e^{-k^2/4\alpha^2}/k^2$: the weight of each wave in the formula for $U_{recip}$.
</div>

The four steps in more words, with the 8 nm box as the example:

**Step 1, spreading.** With grid points 0.12 nm apart, an edge of 8 nm needs at least $8/0.12 = 67$ points, and the whole box about $67^3\approx300{,}000$. Each charge is shared out among the $4\times4\times4$ grid points nearest to it. The weight of a grid point is the product of three one-dimensional B-spline weights, one for each direction. The weights of one charge add up to 1, so no charge is lost. The result is the "gridded charge density": one number at each grid point.

**Step 2, the transform.** One FFT gives the Fourier coefficients of the gridded density for all the waves that the grid can represent. These coefficients take the place of $S(\mathbf k)$. The cost is about $5\times10^6$ operations, against $2\times10^9$ for the direct sums.

**Step 3, the influence function.** Each coefficient is multiplied by the weight $e^{-k^2/4\alpha^2}/k^2$ that appeared in $U_{recip}$. The $1/k^2$ solves Poisson's equation, and the Gaussian accounts for the clouds. The correction is needed because spreading a charge over 64 grid points blurs it a little, in addition to the intended Gaussian blur. For B-splines the effect of that extra blur on each wave is known, so it can be largely compensated wave by wave.

**Step 4, back to the particles.** The inverse FFT turns the coefficients into the potential of the smooth clouds at every grid point. The potential at an atom is read off the grid with the same 64 weights. The force on the atom is its charge times the slope of that potential, with a minus sign, and the slope is obtained from the formula for the derivative of the B-spline weights. "Analytically" means exactly that: by formula, without taking differences of neighbouring grid values.

Step 4 contains two statements about conservation. The energy computed on the grid is an approximation of $U_{recip}$. The forces are the exact derivative of that approximate energy with respect to the positions of the atoms. An integrator conserves energy when the forces are the gradient of the energy function in use (Module 2), whether or not that function is itself an approximation, so energy is conserved.

Momentum is a different matter. It is conserved when the force of atom $j$ on atom $i$ is exactly minus the force of $i$ on $j$ (Newton's third law, Module 2). Forces that pass through a grid obey this only approximately. The sum of all forces is then a small remainder in place of zero, and the system as a whole can slowly pick up speed unless the program removes that motion.

The cost is $O(N\log N)$, and on current hardware PME is typically a sizeable part of the run time (how large depends on what is offloaded to the GPU). The settings that matter:

| Setting (GROMACS name) | Typical value | Meaning |
|---|---|---|
| `rcoulomb` | 1.0 to 1.2 nm | Real-space cutoff |
| `fourierspacing` | 0.10 to 0.12 nm | Maximum grid spacing |
| `pme-order` | 4 | B-spline order (cubic) |
| `ewald-rtol` | $10^{-5}$ | Size of the real-space term at the cutoff; fixes $\alpha$ through $\mathrm{erfc}(\alpha r_c)=$ `ewald-rtol` |

<div class="legend" markdown="1">
- $O(N\log N)$: the cost grows as the number of atoms $N$ times its logarithm.
- $\alpha$: the splitting parameter, in nm$^{-1}$. $r_c$: the real-space cutoff, the value of `rcoulomb`.
- $\mathrm{erfc}(\alpha r_c)$: the complementary error function at the cutoff. It is the fraction of the bare interaction $1/r_c$ that the real-space term still has there.
</div>

Where $N\log N$ comes from: spreading and reading back cost 64 operations per charge, which is proportional to $N$. The grid spacing is fixed, so the number of grid points $M$ is proportional to the volume and therefore to $N$, and the FFT costs $M\log M$. The real-space part has a fixed cutoff and costs $O(N)$ with a neighbour list. Going from 10,000 to 1,000,000 atoms multiplies the cost by about 150, where classical Ewald would give a factor 1000. "Offloaded to the GPU" means computed on the graphics card and not on the processor.

The four settings, row by row:

- `rcoulomb` is the $r_c$ of the real-space term.
- `fourierspacing` is an upper limit for the distance between neighbouring grid points. The program chooses the number of grid points along each edge so that the spacing is no larger than this.
- `pme-order` is the order $p$ of the B-splines. With 4, each charge is spread over 4 grid points in each direction.
- `ewald-rtol` is the value that $\mathrm{erfc}(\alpha r_c)$ must have. You never set $\alpha$ yourself. You choose the cutoff and this tolerance, and $\alpha$ follows.

With $r_c = 1.0$ nm and a tolerance of $10^{-5}$, $\alpha = 3.12$ nm$^{-1}$. Cutoff and grid spacing can be scaled together at constant accuracy to shift load between the CPU or GPU real-space part and the FFT, and GROMACS does this automatically at the start of a run.

The number follows from the error function: $\mathrm{erfc}(x) = 10^{-5}$ at $x = 3.12$, so $\alpha = 3.12/r_c$. A cutoff of 1.2 nm gives $\alpha = 2.60$ nm$^{-1}$.

The scaling works like this. Make the cutoff 1.2 times longer at the same tolerance. $\alpha$ becomes 1.2 times smaller and the Gaussian clouds 1.2 times wider. A wider cloud is described by longer waves, so the grid can be 1.2 times coarser, for example 0.144 nm in place of 0.12 nm, without loss of accuracy.

The grid then has $1.2^3 = 1.7$ times fewer points, and the real-space loop has 1.7 times more pairs. The energy is as accurate as before, and work has moved from the FFT to the pair loop. Which division is fastest depends on the machine, which is why the program settles it at the start of a run.

<div class="box warn" markdown="1">
**Net charge.** With Ewald, a system with net charge is silently neutralised by a uniform background charge. The simulation runs, but the background distorts pressure and free energies, especially in systems with regions of different dielectric constant (membranes). Always add counter-ions to make the system neutral. For free-energy calculations that change the net charge, see the finite-size corrections in Module 13.
</div>

The background is the consequence of leaving out the $\mathbf k = 0$ term, as explained under "The total". **Counter-ions** are ions of the opposite sign, for example sodium or chloride, that you add to the solvent until the charges of the box add up to zero. They differ from the background in one respect: real ions stay in the water, and the background is spread evenly over everything, including the inside of a membrane, where ions would not be. A **finite-size correction** is a term that removes the effect of the limited box and of the background from a computed free energy.

### Reading the non-bonded part of an input file

[Module 10](10-running-a-simulation.html) contains a complete input file for a production run. Its non-bonded lines are the following. The format is that of a GROMACS parameter file, and the text after a semicolon is a comment.

```
cutoff-scheme           = Verlet        ; buffered neighbour list (Module 7)
rvdw                    = 1.0           ; Lennard-Jones cutoff (nm)
vdw-modifier            = Potential-shift
DispCorr                = EnerPres      ; tail correction for energy and pressure

coulombtype             = PME           ; particle-mesh Ewald (Module 7)
rcoulomb                = 1.0
pme-order               = 4
fourierspacing          = 0.12
```

Every line corresponds to a part of this module:

| Line | What it controls | Where it is explained |
|---|---|---|
| `cutoff-scheme = Verlet` | Pairs are found with a neighbour list that has a skin | Neighbour lists |
| `rvdw = 1.0` | The cutoff $r_c$ of the Lennard-Jones interaction, in nm | Cutting off short-range interactions |
| `vdw-modifier = Potential-shift` | The Lennard-Jones energy is shifted so that it is zero at the cutoff | Issue 1, the jump at the cutoff |
| `DispCorr = EnerPres` | The tail correction is added to the energy and the pressure | Issue 2, the neglected tail |
| `coulombtype = PME` | The Coulomb energy is computed by particle-mesh Ewald | Particle-mesh Ewald |
| `rcoulomb = 1.0` | The cutoff of the real-space term, in nm | The real-space term |
| `pme-order = 4` | Cubic B-splines for spreading and interpolation | Particle-mesh Ewald |
| `fourierspacing = 0.12` | The largest allowed distance between grid points, in nm | Particle-mesh Ewald |

For a CHARMM force field Module 10 gives `rvdw = 1.2`, `rvdw-switch = 1.0` and `vdw-modifier = Force-switch` in place of the shift, together with `rcoulomb = 1.2` and `DispCorr = no`. The first three are the force switch from 1.0 to 1.2 nm of issue 1.

## Reaction field

Ewald summation repairs the cutoff by adding everything that lies beyond it. The reaction field keeps the cutoff and repairs it more cheaply. It fills the space beyond the cutoff with a uniform material that responds to the charges inside, where a plain cutoff leaves that space empty.

A cheaper alternative assumes that beyond $r_c$ the medium is a continuum with dielectric constant $\varepsilon_{rf}$. Its polarisation creates a field that acts back on the charges inside:

$$
U_{RF}(r) = \frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_r}\left[\frac1r + k_{rf}\,r^2 - c_{rf}\right],\qquad
k_{rf} = \frac{1}{r_c^3}\,\frac{\varepsilon_{rf}-\varepsilon_r}{2\varepsilon_{rf}+\varepsilon_r},\qquad c_{rf}=\frac{1}{r_c}+k_{rf}r_c^2 .
$$

<div class="legend" markdown="1">
- $U_{RF}(r)$: the energy of a pair of charges at the distance $r$ in the reaction-field method, for $r$ smaller than $r_c$. Beyond $r_c$ it is zero.
- $q_i$, $q_j$: the two charges, in units of $e$.
- $1/(4\pi\varepsilon_0)$: the Coulomb constant, 138.935 kJ mol$^{-1}$ nm $e^{-2}$. In this formula it is written out, unlike in the Ewald section.
- $\varepsilon_r$: the dielectric constant used inside the cutoff sphere. It is 1 for an atomistic force field with explicit water (Module 5).
- $\varepsilon_{rf}$: the dielectric constant assumed for the continuum beyond the cutoff. Both are pure numbers, and neither is the Lennard-Jones $\varepsilon$.
- $1/r$: the direct Coulomb interaction of the pair.
- $k_{rf}\,r^2$: the effect of the reaction field. $k_{rf}$ is a constant in nm$^{-3}$ (not a wave vector).
- $c_{rf}$: a constant in nm$^{-1}$ that shifts the energy so that it is zero at the cutoff.
- $r_c$: the cutoff distance, in nm.
</div>

The words of the sentence above the formula were defined in the box on dielectrics: a continuum is a material without single molecules, and its polarisation is the turning of its dipoles in response to charges. A **field** is the force that a charge of $+1$ would feel at a given place. The charges inside the cutoff sphere polarise the material outside, and the polarised material in turn produces a field inside the sphere. This response is the **reaction field**.

The force goes smoothly to zero at $r_c$ when $\varepsilon_{rf}=\infty$. Three checks on the formula show this and a little more:

- *At the cutoff the energy is zero.* Insert $r = r_c$ in the bracket: $1/r_c + k_{rf}r_c^2 - c_{rf}$, which is zero by the definition of $c_{rf}$. So the energy has no step at $r_c$, as with the potential shift.
- *The force is weakened towards the cutoff.* The force is minus the slope of the energy, so it is proportional to $1/r^2 - 2k_{rf}\,r$. The first part is Coulomb's force. The second part works against it and grows with $r$.
- *With a conductor outside, the force reaches zero.* For $\varepsilon_{rf}=\infty$ the fraction $(\varepsilon_{rf}-\varepsilon_r)/(2\varepsilon_{rf}+\varepsilon_r)$ becomes $\tfrac12$, so $k_{rf} = 1/(2r_c^3)$. At $r = r_c$ the force is then proportional to $1/r_c^2 - 2r_c/(2r_c^3) = 0$.

A number. Take $r_c = 1.0$ nm, $\varepsilon_r = 1$ and $\varepsilon_{rf} = \infty$, so that $k_{rf} = 0.5$ nm$^{-3}$ and $c_{rf} = 1.5$ nm$^{-1}$. For two unit charges at $r = 0.5$ nm the bracket is $2 + 0.125 - 1.5 = 0.625$ nm$^{-1}$ and the energy $138.935\times0.625 = 87$ kJ/mol, against 278 kJ/mol for plain Coulomb. Most of that difference is the constant $c_{rf}$, which creates no force.

The force itself is proportional to $1/r^2 - 2k_{rf}\,r = 4 - 0.5 = 3.5$ nm$^{-2}$ in place of 4, about 12 % weaker. With $\varepsilon_{rf} = 80$ in place of infinity the fraction is $79/161 = 0.49$, and almost nothing changes.

It is a pair interaction with a cutoff, so it is fast and simple to parallelise. GROMOS force fields were developed with it, and the Martini coarse-grained model (Module 15) uses it. It is less accurate than PME for strongly inhomogeneous or highly charged systems such as nucleic acids.

To **parallelise** a calculation is to divide it over many processors. A pair interaction with a cutoff needs only the atoms close by, so each processor can work on its own region of the box. A **coarse-grained** model represents a group of atoms by one particle. The method assumes the same uniform material beyond the cutoff of every atom. In an **inhomogeneous** system, for example a membrane in water, what lies beyond the cutoff differs from place to place, and the assumption is poor.

## Check yourself

<details markdown="1"><summary>1. A protein is 6 nm long in its most extended conformation and you use a 1.2 nm cutoff. What is the minimum box edge for a cubic box if it can tumble freely?</summary>
The protein must not come within the cutoff of its image, so the edge must be at least $6 + 1.2 = 7.2$ nm. The usual rule of 1.0 to 1.2 nm of solvent on each side gives 8.0 to 8.4 nm, which also keeps the hydration shells of the copies apart.
</details>

<details markdown="1"><summary>2. Why can the Ewald real-space sum be cut off at 1 nm when the bare Coulomb sum cannot?</summary>
The real-space term is the interaction between a point charge and another point charge that is screened by a Gaussian cloud of opposite sign. It decays as $\mathrm{erfc}(\alpha r)/r$, faster than exponentially. The long-range part has not been thrown away: it is in the reciprocal-space sum.
</details>

<details markdown="1"><summary>3. Does the total Ewald energy depend on α?</summary>
No, the exact sum is independent of $\alpha$. In practice both sums are truncated, so $\alpha$ controls how the error is divided between them. It is chosen so that both truncation errors are below the tolerance.
</details>

<details markdown="1"><summary>4. You forget the dispersion correction in a liquid simulation at constant pressure. What changes?</summary>
The missing long-range attraction makes the pressure too high at a given density, so at fixed pressure the box expands. The density comes out too low, by up to a few percent with short cutoffs, and the potential energy is too high.
</details>

<details markdown="1"><summary>5. A box has an edge of 4 nm along $x$. Particle $i$ is at $x_i = 3.7$ nm and particle $j$ at $x_j = 0.4$ nm. What separation does the minimum-image convention give?</summary>
The stored separation is $\Delta x = 3.7 - 0.4 = 3.3$ nm. In box lengths that is $3.3/4 = 0.825$, which rounds to 1. The new value is $3.3 - 4\times1 = -0.7$ nm. The closest image of $j$ is the one in the next box to the right, at $0.4 + 4 = 4.4$ nm, which is 0.7 nm from $i$.
</details>

<details markdown="1"><summary>6. Use the shell argument to say why the Lennard-Jones attraction can be cut off and the Coulomb interaction cannot.</summary>
The number of partners in a shell at the distance $r$ grows as $r^2$. For the Lennard-Jones attraction the pair energy falls as $r^{-6}$, so a shell contributes as $r^{-4}$, and the sum over all shells beyond the cutoff $r_c$ is finite and small, proportional to $1/r_c^3$. For charges the pair energy falls only as $r^{-1}$, so a shell contributes as $r$. Distant shells then count more than near ones, and only the cancellation between positive and negative charges keeps the sum finite. A cutoff destroys that cancellation.
</details>

<details markdown="1"><summary>7. You change the real-space cutoff from 1.0 to 1.2 nm and keep the tolerance at $10^{-5}$. What happens to $\alpha$, and what can you do with the PME grid?</summary>
$\alpha$ is fixed by $\mathrm{erfc}(\alpha r_c) = 10^{-5}$, which means $\alpha r_c = 3.12$. So $\alpha$ falls from 3.12 to $3.12/1.2 = 2.60$ nm$^{-1}$. The Gaussian clouds become 1.2 times wider, and the grid spacing can be raised by the same factor, for example from 0.12 to 0.144 nm. The grid then has $1.2^3 = 1.7$ times fewer points, the real-space loop has 1.7 times more pairs, and the accuracy stays the same.
</details>

## Exercises

1. Add a Verlet neighbour list with a skin to the Python code of Module 1. Measure the speed-up for 1,000 atoms and check that energy conservation is unchanged.
2. Derive the tail correction to the pressure, $P_{tail} = \frac{16}{3}\pi\rho^2\varepsilon\sigma^3\left[\frac23(\sigma/r_c)^9-(\sigma/r_c)^3\right]$, from the virial.
3. Implement the classical Ewald sum for the NaCl crystal (8 ions in a cubic cell). Reproduce the Madelung constant 1.7476 and show the result is independent of $\alpha$ once both sums are converged.
4. Prove that the potential of a spherical Gaussian charge distribution of total charge $q$ is $q\,\mathrm{erf}(\alpha r)/r$ by solving Poisson's equation in spherical coordinates.

<div class="legend" markdown="1">
- $P_{tail}$ (exercise 2): the correction to the pressure for the Lennard-Jones interactions beyond the cutoff. With $\rho$ in nm$^{-3}$ and $\varepsilon$ in kJ/mol it comes out in kJ mol$^{-1}$ nm$^{-3}$.
- $\rho$: the number density. $\varepsilon$, $\sigma$: the Lennard-Jones well depth and size. $r_c$: the cutoff.
- The virial (exercise 2): the part of the pressure that comes from the forces between the particles (Module 3).
- The Madelung constant (exercise 3): the Coulomb energy of the crystal for each pair of one positive and one negative ion, divided by $-q^2/d$, where $q$ is the charge of an ion and $d$ the distance between nearest neighbours (in units where $1/4\pi\varepsilon_0 = 1$). Eight ions are four pairs, so the total energy of the cell is $-4\times1.7476\,q^2/d$.
- $q$, $\alpha$, $r$ (exercise 4): the total charge of the cloud, the splitting parameter and the distance from the centre of the cloud.
</div>

## Read

{{READ}}

## Key papers

{{PAPERS}}
