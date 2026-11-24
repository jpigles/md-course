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

## Watch first

{{WATCH}}

## Periodic boundary conditions

<div data-videos="gVVqjmTAJGI x20QP1x3U7c J3aB9xp1YIE Wbzopzywt-Q IpdTtx98AWQ"></div>

A simulation box holds $10^4$ to $10^6$ atoms. If it had walls, a large fraction of the molecules would sit at a surface: in a cube of 10,000 water molecules about a quarter are in the outermost molecular layer. To imitate bulk solution we remove the surface by making the box **periodic**: it is surrounded by an infinite lattice of identical copies. A particle that leaves through one face enters through the opposite face with the same velocity.

### The minimum-image convention

<div data-videos="pzM7ju9DNtM AbidqaoH7Wo"></div>

Each particle interacts with the **nearest image** of every other particle. For a rectangular box with edges $L_x,L_y,L_z$:

$$
\Delta x \leftarrow \Delta x - L_x\,\mathrm{round}\!\left(\frac{\Delta x}{L_x}\right)
$$

and the same for $y$ and $z$. This is the line `d -= L * np.round(d / L)` in the Module 1 code. It is consistent with a cutoff $r_c$ only if

$$
r_c \le \tfrac12 L_{min},
$$

so that at most one image of each neighbour lies inside the cutoff sphere.

### Box shape and size

A protein is roughly spherical, so a cube wastes water in its corners. Space-filling shapes that are closer to a sphere need less solvent for the same distance between periodic images:

| Box | Volume for the same image distance $d$ | Saving against the cube |
|---|---|---|
| Cube | $d^3$ | 0 |
| Truncated octahedron | $0.77\,d^3$ | 23 % |
| Rhombic dodecahedron | $0.71\,d^3$ | 29 % |

Codes implement these as triclinic cells. Rules for the size:

- The solute must never see its own image: the shortest distance between the solute and any periodic copy must stay larger than the cutoff at all times. In practice, leave at least 1.0 to 1.2 nm of solvent between the solute and each box face (so at least 2.0 nm between copies).
- An elongated or flexible molecule can rotate or extend. Size the box for the longest dimension it can reach, or check the minimum image distance during the run (`gmx mindist -pi`).
- For binding or unbinding simulations the box must hold the separated state with both partners out of range of each other and of all images.

Periodicity does have artefacts: no fluctuation with a wavelength longer than the box exists, diffusion is slowed by hydrodynamic interaction with the images (a correction is given in Module 11), and a charged solute interacts with its copies.

## Cutting off short-range interactions

<div data-videos="JQPHMpR37Co y-jUCgk4rCI hi7gvv-I-0o"></div>

The Lennard-Jones attraction falls as $r^{-6}$, fast enough to truncate at $r_c$ = 0.9 to 1.2 nm. Three issues arise.

**1. The jump at the cutoff.** Plain truncation makes $U$ discontinuous at $r_c$, so the force has a delta-function spike and energy is not conserved. Remedies:

- **Potential shift**: use $U(r)-U(r_c)$ inside the cutoff. The energy is continuous, the force is unchanged inside and still jumps to zero at $r_c$ (a small jump). This is the GROMACS default.
- **Force switch or potential switch**: multiply by a smooth function that takes the force (or potential) to zero between $r_{sw}$ and $r_c$. CHARMM force fields were parameterised with a force switch from 1.0 to 1.2 nm, and membrane properties in particular depend on using it.

**2. The neglected tail.** Beyond $r_c$ the liquid is nearly uniform ($g(r)\approx1$), so the missing energy can be added analytically. For $N$ particles of number density $\rho$:

$$
U_{tail} = \frac{N\rho}{2}\int_{r_c}^{\infty}4\pi r^2\,U_{LJ}(r)\,dr
= \frac{8}{3}\pi N\rho\,\varepsilon\sigma^3\left[\frac13\left(\frac{\sigma}{r_c}\right)^{9}-\left(\frac{\sigma}{r_c}\right)^{3}\right].
$$

There is a matching correction to the pressure. It is negative (the missing attraction pulls the system together), so leaving it out gives a density that is too low. In GROMACS this is `DispCorr = EnerPres`. It assumes a homogeneous system, so it is not appropriate for membranes and interfaces, where Lennard-Jones PME (a lattice sum for the $r^{-6}$ term) is the rigorous alternative.

**3. Finding the neighbours.** Testing all $N(N-1)/2$ pairs each step to find those within $r_c$ would itself cost $O(N^2)$.

### Neighbour lists

<div data-videos="OURKkL8XqDo"></div>

- **Verlet list.** For each atom keep a list of all atoms within $r_l = r_c + \delta$, where $\delta$ is the "skin" or buffer. Use the list for many steps. It is guaranteed to stay valid until some atom has moved more than $\delta/2$, because only then can a pair that was outside $r_l$ come inside $r_c$.
- **Cell list.** Divide the box into cells of edge at least $r_l$. Neighbours of an atom can only be in its own cell or the 26 around it. Building the Verlet list this way costs $O(N)$.

Modern codes build on these ideas. GROMACS sorts the atoms on a grid into small clusters of fixed size and keeps a buffered list of cluster pairs, so that SIMD instructions or a GPU can process whole clusters together ([Páll and Hess 2013](cite:pall2013)). It chooses the buffer automatically from the temperature and the allowed energy drift (`verlet-buffer-tolerance`). You rarely set this by hand, but you should recognise that a too-small buffer or too-infrequent update shows up as energy drift.

## Why electrostatics cannot be cut off

The Coulomb energy falls as $1/r$, while the number of charges in a shell at distance $r$ grows as $r^2$. The contribution of each shell grows with distance unless positive and negative charges cancel, so the sum over all periodic images is only **conditionally convergent**: its value depends on the order of summation. A plain cutoff at 1 nm discards interactions that are individually large (two unit charges at 1 nm: 139 kJ/mol) and leaves a net charge inside every cutoff sphere. The known artefacts include artificial layering of water at the cutoff distance, wrong ion-ion distributions, distorted DNA and unstable proteins, and wrong dielectric properties.

Two approaches are used. **Reaction field** treats everything beyond the cutoff as a dielectric continuum (see the end of this module). **Ewald summation** computes the full periodic sum exactly, and is the standard for atomistic simulation.

## Ewald summation

<div data-videos="SSmIMof0KvA DnOTgjUZxbE YPryFf7MQTg"></div>

We want the electrostatic energy of $N$ charges in a box of volume $V$ with all periodic images $\mathbf n$ (in units where $1/4\pi\varepsilon_0=1$; multiply by 138.935 for kJ/mol with nm and $e$):

$$
U = \frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}\frac{q_iq_j}{|\mathbf r_{ij}+\mathbf n|},
$$

where the prime means $i\neq j$ when $\mathbf n=0$.

**The trick.** Around each point charge $q_i$, add a Gaussian cloud of charge $-q_i$ with width set by a parameter $\alpha$,

$$
\rho_i^{G}(\mathbf r) = -q_i\left(\frac{\alpha^2}{\pi}\right)^{3/2}e^{-\alpha^2|\mathbf r-\mathbf r_i|^2},
$$

and then subtract the same clouds again. This splits the problem into two easy pieces:

- **Point charges plus screening clouds.** Seen from a distance, each charge with its cloud is neutral, so its potential dies off quickly. This part is short-ranged and can be summed directly with a cutoff.
- **Minus the clouds.** A smooth, periodic charge distribution. Smooth periodic functions have rapidly converging Fourier series, so this part is summed in reciprocal space.

The split is the identity

$$
\frac1r = \underbrace{\frac{\mathrm{erfc}(\alpha r)}{r}}_{\text{short-ranged}} + \underbrace{\frac{\mathrm{erf}(\alpha r)}{r}}_{\text{smooth, long-ranged}},
$$

because $q\,\mathrm{erf}(\alpha r)/r$ is the potential of a Gaussian charge cloud.

<div class="widget" data-widget="ewald"></div>

**Real-space term.** The screened interaction, summed over pairs within the cutoff:

$$
U_{real} = \frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\,\frac{\mathrm{erfc}(\alpha|\mathbf r_{ij}+\mathbf n|)}{|\mathbf r_{ij}+\mathbf n|}.
$$

**Reciprocal-space term.** The Gaussian clouds form a periodic density with Fourier coefficients $\tilde\rho(\mathbf k) = S(\mathbf k)\,e^{-k^2/4\alpha^2}$, where the **structure factor** is

$$
S(\mathbf k) = \sum_{j=1}^Nq_j\,e^{i\mathbf k\cdot\mathbf r_j},\qquad \mathbf k = 2\pi\left(\frac{n_x}{L_x},\frac{n_y}{L_y},\frac{n_z}{L_z}\right).
$$

Poisson's equation $\nabla^2\phi = -4\pi\rho$ is algebraic in Fourier space, $\tilde\phi(\mathbf k) = 4\pi\tilde\rho(\mathbf k)/k^2$, which gives the potential $\phi_G$ of the smooth clouds. The energy of the point charges in that potential, $\tfrac12\sum_iq_i\,\phi_G(\mathbf r_i)$, then becomes

$$
U_{recip} = \frac{2\pi}{V}\sum_{\mathbf k\neq0}\frac{e^{-k^2/4\alpha^2}}{k^2}\,\big|S(\mathbf k)\big|^2 .
$$

The Gaussian factor makes the sum converge after a modest number of $\mathbf k$ vectors.

**Self term.** The reciprocal sum includes the interaction of each point charge with its own Gaussian cloud, which is not physical. Remove it:

$$
U_{self} = -\frac{\alpha}{\sqrt\pi}\sum_iq_i^2 .
$$

**Total.**

$$
\boxed{U_{Coulomb} = U_{real} + U_{recip} + U_{self}\;(+\;U_{excl}\;+\;U_{surface})}
$$

Two further corrections appear in practice. Pairs excluded by the topology (1-2 and 1-3 neighbours) are present in the reciprocal sum and must be subtracted, $U_{excl} = -\sum_{excl}q_iq_j\,\mathrm{erf}(\alpha r_{ij})/r_{ij}$. The $\mathbf k=0$ term is omitted, which corresponds to surrounding the infinite lattice with a conductor ("tin-foil" boundary conditions, $U_{surface}=0$) and, for a system with net charge, to adding a uniform neutralising background.

The result does not depend on $\alpha$. A large $\alpha$ (narrow Gaussians) makes the real-space sum converge within a short cutoff and pushes work into reciprocal space, and the reverse. With the best balance, classical Ewald scales as $O(N^{3/2})$.

### Particle-mesh Ewald

<div data-videos="VWsMUaA7UWw"></div>

Computing $S(\mathbf k)$ directly costs $N$ operations for each of many $\mathbf k$ vectors. **PME** replaces it. The original method of [Darden, York and Pedersen 1993](cite:darden1993) interpolated the reciprocal-space pair potential and its gradient with Lagrange polynomials on a grid. The smooth version of [Essmann et al. 1995](cite:essmann1995) is the one in use today, and it interpolates the structure factor itself with B-splines:

1. Spread each charge onto a regular 3D grid using B-spline interpolation (order 4 touches $4^3=64$ grid points per charge).
2. Fast Fourier transform the gridded charge density: $O(M\log M)$ for $M$ grid points.
3. Multiply by the influence function $e^{-k^2/4\alpha^2}/k^2$, corrected for the B-spline spreading.
4. Transform back to get the potential on the grid, and obtain the forces by differentiating the same B-splines analytically. The reciprocal force is then the exact gradient of the approximate energy, so energy is conserved, but momentum is conserved only to within the force error (one reason why codes remove centre-of-mass motion).

The cost is $O(N\log N)$, and on current hardware PME is typically a sizeable part of the run time (how large depends on what is offloaded to the GPU). The settings that matter:

| Setting (GROMACS name) | Typical value | Meaning |
|---|---|---|
| `rcoulomb` | 1.0 to 1.2 nm | Real-space cutoff |
| `fourierspacing` | 0.10 to 0.12 nm | Maximum grid spacing |
| `pme-order` | 4 | B-spline order (cubic) |
| `ewald-rtol` | $10^{-5}$ | Size of the real-space term at the cutoff; fixes $\alpha$ through $\mathrm{erfc}(\alpha r_c)=$ `ewald-rtol` |

With $r_c = 1.0$ nm and a tolerance of $10^{-5}$, $\alpha = 3.12$ nm$^{-1}$. Cutoff and grid spacing can be scaled together at constant accuracy to shift load between the CPU or GPU real-space part and the FFT, and GROMACS does this automatically at the start of a run.

<div class="box warn" markdown="1">
**Net charge.** With Ewald, a system with net charge is silently neutralised by a uniform background charge. The simulation runs, but the background distorts pressure and free energies, especially in systems with regions of different dielectric constant (membranes). Always add counter-ions to make the system neutral. For free-energy calculations that change the net charge, see the finite-size corrections in Module 13.
</div>

## Reaction field

A cheaper alternative assumes that beyond $r_c$ the medium is a continuum with dielectric constant $\varepsilon_{rf}$. Its polarisation creates a field that acts back on the charges inside:

$$
U_{RF}(r) = \frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_r}\left[\frac1r + k_{rf}\,r^2 - c_{rf}\right],\qquad
k_{rf} = \frac{1}{r_c^3}\,\frac{\varepsilon_{rf}-\varepsilon_r}{2\varepsilon_{rf}+\varepsilon_r},\qquad c_{rf}=\frac{1}{r_c}+k_{rf}r_c^2 .
$$

The force goes smoothly to zero at $r_c$ when $\varepsilon_{rf}=\infty$. It is a pair interaction with a cutoff, so it is fast and simple to parallelise. GROMOS force fields were developed with it, and the Martini coarse-grained model (Module 15) uses it. It is less accurate than PME for strongly inhomogeneous or highly charged systems such as nucleic acids.

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

## Exercises

1. Add a Verlet neighbour list with a skin to the Python code of Module 1. Measure the speed-up for 1,000 atoms and check that energy conservation is unchanged.
2. Derive the tail correction to the pressure, $P_{tail} = \frac{16}{3}\pi\rho^2\varepsilon\sigma^3\left[\frac23(\sigma/r_c)^9-(\sigma/r_c)^3\right]$, from the virial.
3. Implement the classical Ewald sum for the NaCl crystal (8 ions in a cubic cell). Reproduce the Madelung constant 1.7476 and show the result is independent of $\alpha$ once both sums are converged.
4. Prove that the potential of a spherical Gaussian charge distribution of total charge $q$ is $q\,\mathrm{erf}(\alpha r)/r$ by solving Poisson's equation in spherical coordinates.

## Read

{{READ}}

## Key papers

{{PAPERS}}
