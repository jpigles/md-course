---
num: 1
title: What molecular dynamics is, and what it can tell you
short: What MD is
part: Part I · Foundations
hours: 4
summary: Describe the MD algorithm in six lines, say which physics it keeps and which it throws away, and name the three kinds of error every simulation has.
videos: 1
papers: A
tags: biomolecules
---

<div class="box goal" markdown="1">
#### After this module you can

- write the MD loop from memory and say what each line costs;
- explain why atoms can be treated as classical particles, and where that breaks;
- place a process (a bond vibration, a loop motion, an unbinding event) on the time axis and say whether plain MD can reach it;
- separate the three sources of error: the model, the sampling, and the set-up.
</div>

## Watch first

Start with one of the whole-course playlists below. You do not need to finish it now: watch the first one or two lectures to get the overall picture, then come back to the same playlist as you move through the modules.

{{WATCH}}

## The idea in one paragraph

<div data-videos="dEmAnuO8RhQ GcGClviieOU O3YgILmo5V8 GUASx0_NyEE"></div>

A molecular dynamics (MD) simulation takes a set of particles, a rule that gives the potential energy $U(\mathbf r_1,\dots,\mathbf r_N)$ for any arrangement of them, and Newton's second law. It then moves the particles forward in time in very small steps. The output is a **trajectory**: the positions and velocities of every particle at each saved step. Everything else you will ever report from MD (a free energy, a diffusion constant, an RMSD plot, a binding affinity) is a statistic computed from one or more trajectories.

There are three ingredients, and the course follows them:

| Ingredient | Question it answers | Modules |
|---|---|---|
| Equations of motion and how to integrate them | How do the particles move, and how do we step forward in time without the error growing? | 2, 4, 8, 9 |
| The force field $U(\mathbf r)$ | What are the forces between atoms? | 5, 6, 7, 15, 17 |
| Statistical mechanics | Why does a trajectory tell us about thermodynamics, and how many samples do we need? | 3, 11, 12, 13, 14, 16 |

## The algorithm

<div data-videos="IlwC3PSyZ0Q QiZk_uT-40E AtExb5EprvE NItXk8epkNM TEg1Nx4yGjc gQ1YPzcHZqo"></div>

For particle $i$ with mass $m_i$ and position $\mathbf r_i$, Newton's second law is

$$
m_i \frac{d^2 \mathbf r_i}{dt^2} = \mathbf F_i = -\frac{\partial U}{\partial \mathbf r_i}.
$$

In general there is no closed-form solution for three or more interacting particles, so we solve it numerically. The most common scheme, velocity Verlet (derived in Module 4), is:

$$
\begin{aligned}
\mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) &= \mathbf v_i(t) + \frac{\Delta t}{2 m_i}\,\mathbf F_i(t) \\
\mathbf r_i(t+\Delta t) &= \mathbf r_i(t) + \Delta t\,\mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) \\
\mathbf F_i(t+\Delta t) &= -\nabla_i U\big(\mathbf r(t+\Delta t)\big) \\
\mathbf v_i(t+\Delta t) &= \mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) + \frac{\Delta t}{2 m_i}\,\mathbf F_i(t+\Delta t)
\end{aligned}
$$

In words:

1. Give every atom a position (from a structure) and a velocity (random, from the Maxwell-Boltzmann distribution at the target temperature).
2. Compute the force on every atom from the force field.
3. Use the forces to update the velocities by half a step.
4. Use the velocities to update the positions by a full step.
5. Compute the forces at the new positions and finish the velocity update.
6. Every so often, write positions and energies to disk. Go to 3.

Step 5, the force calculation, takes most of the computer time (the pair interactions alone take more than half). The rest of the "engine" part of this course (cutoffs, neighbour lists, particle-mesh Ewald, constraints) exists to make that step cheaper or to allow a larger $\Delta t$.

<div class="widget" data-widget="md2d"></div>

### The same thing in 35 lines of Python

<div data-videos="kvJ1siWcBfM"></div>

Read this code line by line. It is a complete simulation of a Lennard-Jones fluid (a good model of liquid argon) in reduced units. Every production MD program is this loop with a more elaborate force routine.

```python
import numpy as np

def lj_forces(x, L, rc=2.5):
    """Lennard-Jones forces and potential energy (reduced units, periodic box)."""
    d = x[:, None, :] - x[None, :, :]            # all pair vectors r_i - r_j
    d -= L * np.round(d / L)                     # minimum-image convention
    r2 = (d ** 2).sum(-1)
    np.fill_diagonal(r2, np.inf)                 # no self-interaction
    inside = r2 < rc ** 2
    inv6 = np.where(inside, 1.0 / r2 ** 3, 0.0)  # (sigma/r)^6 with sigma = 1
    shift = 4 * (rc ** -12 - rc ** -6)           # makes U continuous at the cutoff
    u = 0.5 * np.sum(np.where(inside, 4 * (inv6 ** 2 - inv6) - shift, 0.0))
    f = (24 * (2 * inv6 ** 2 - inv6) / r2)[:, :, None] * d
    return f.sum(axis=1), u

rng = np.random.default_rng(0)
n, rho, T, dt = 5, 0.8, 1.0, 0.004               # 5 x 5 x 5 = 125 atoms
N = n ** 3
L = (N / rho) ** (1 / 3)                         # box edge from the density
g = (np.arange(n) + 0.5) * L / n
x = np.array(np.meshgrid(g, g, g)).reshape(3, -1).T   # start on a lattice
v = rng.normal(0.0, np.sqrt(T), (N, 3))          # Maxwell-Boltzmann velocities
v -= v.mean(axis=0)                              # remove centre-of-mass motion

f, u = lj_forces(x, L)
for step in range(2001):
    v += 0.5 * dt * f                            # half kick
    x += dt * v                                  # drift
    x %= L                                       # wrap back into the box
    f, u = lj_forces(x, L)                       # new forces (the expensive line)
    v += 0.5 * dt * f                            # half kick
    if step % 200 == 0:
        k = 0.5 * (v ** 2).sum()
        print(f"step {step:5d}  T = {2 * k / (3 * N - 3):.3f}  E/N = {(k + u) / N:.5f}")
```

The total energy per particle printed in the last column should stay constant to about three decimal places (it wanders by a few $10^{-4}$, because the force still has a small jump at the cutoff), while the temperature changes by several percent. The temperature does not stay at its starting value of 1.0: as the lattice melts, kinetic and potential energy are exchanged, and the temperature settles a little lower and keeps fluctuating. That is equilibration, which you will meet again in Module 10.

## Which physics is kept, and which is dropped

<div data-videos="4uloreO4qHA qnDkRUaz57g"></div>

The exact description of a molecule is the time-dependent Schrödinger equation for all nuclei and electrons. MD makes two approximations to get from there to Newton's law.

**1. Born-Oppenheimer.** Electrons are about 1,800 times lighter than a proton, so they adjust almost instantly to the nuclear positions. For a given arrangement of nuclei the electrons sit in their ground state, and the electronic ground-state energy as a function of nuclear positions is the potential energy surface $U(\mathbf r)$. In classical MD we do not solve for the electrons at all: we replace $U(\mathbf r)$ by a cheap fitted formula, the **force field**. Consequence: bonds cannot break or form, and electrons cannot polarise (in standard force fields).

**2. Classical nuclei.** A particle behaves classically when its thermal de Broglie wavelength

$$
\Lambda = \frac{h}{\sqrt{2\pi m k_B T}}
$$

is small compared with the distances over which the potential changes. At 300 K this gives $\Lambda \approx 1.0$ Å for hydrogen and $0.29$ Å for carbon, while interatomic distances are 1 to 4 Å. Heavy atoms are safely classical. Hydrogen is borderline.

A second test is to compare the vibrational quantum $\hbar\omega$ with the thermal energy $k_BT$ (208 cm$^{-1}$ at 300 K). A C-H stretch at about 3,000 cm$^{-1}$ has $\hbar\omega \approx 14\,k_BT$: in reality it sits in its quantum ground state and does not exchange energy with its surroundings. A classical spring with the same frequency would hold a full $k_BT$ of energy. This is one physical reason why it is acceptable, even preferable, to freeze bonds to hydrogen with constraints (Module 9). Slow, soft motions (torsions, diffusion, domain motions) have $\hbar\omega \ll k_BT$ and are well described classically.

<div class="box key" markdown="1">
**What MD cannot do without extra methods:** chemical reactions (needs QM/MM or reactive force fields), proton transfer and changes in protonation state (needs constant-pH methods), electronic excitation, and nuclear tunnelling.
</div>

## Units and the numbers worth memorising

Most biomolecular codes use one of two unit systems. GROMACS uses nm, ps, atomic mass units (u), kJ/mol and elementary charges. These are consistent: 1 u nm$^2$ ps$^{-2}$ = 1 kJ/mol, so no conversion factors appear in Newton's law. AMBER, CHARMM and NAMD use Å and kcal/mol. With Å, u and kcal/mol the consistent time unit is about 48.9 fs, so these programs convert internally, and you give the time step in ps (AMBER, CHARMM) or in fs (NAMD).

| Quantity | Value |
|---|---|
| $k_B$ | 0.0083145 kJ mol$^{-1}$ K$^{-1}$ = 0.0019872 kcal mol$^{-1}$ K$^{-1}$ |
| $k_BT$ at 300 K | 2.494 kJ/mol = 0.596 kcal/mol |
| 1 kcal/mol | 4.184 kJ/mol |
| Coulomb constant $1/(4\pi\varepsilon_0)$ | 138.935 kJ mol$^{-1}$ nm $e^{-2}$ = 332.06 kcal mol$^{-1}$ Å $e^{-2}$ |
| Typical time step | 1 fs (flexible bonds), 2 fs (bonds to H constrained), 4 fs (with hydrogen mass repartitioning) |
| Factor of 10 in a binding constant at 298 K | $RT\ln 10$ = 5.71 kJ/mol = 1.36 kcal/mol |
| Number density of water | 33.4 molecules per nm$^3$, about 100 atoms per nm$^3$ |

## Time and length scales

<div data-videos="_TiQYNWJwYg ryJFDd0dF44"></div>

The time step must resolve the fastest motion in the system, and the fastest motion is a bond vibration with a period of about 10 fs. Everything interesting in biology is slower by many orders of magnitude:

| Process | Typical time | Steps at 2 fs |
|---|---|---|
| Bond stretch (C-H) | 10 fs | 5 |
| Water reorientation, hydrogen-bond lifetime | 1 to 10 ps | $5\times10^2$ to $5\times10^3$ |
| Side-chain rotamer flips at the surface | 10 ps to 1 ns | $5\times10^3$ to $5\times10^5$ |
| Loop motions, helix formation | 1 ns to 1 µs | $5\times10^5$ to $5\times10^8$ |
| Fast protein folding, small-ligand binding | 1 µs to 1 ms | $5\times10^8$ to $5\times10^{11}$ |
| Unbinding of a nanomolar complex | seconds to hours | $5\times10^{14}$ or more |

A single GPU today gives roughly 100 to 1,000 ns per day for a solvated protein of 50,000 to 100,000 atoms (the exact figure depends on the hardware, the system and the settings, so measure it for your own system). That is about $5\times10^8$ steps per day at best: one microsecond per day. The special-purpose machine Anton reached one millisecond for a small protein in 2010. Seconds are far outside the range of direct simulation, and this gap is the reason Modules 12 to 16 exist: free-energy methods, enhanced sampling, coarse-graining and kinetic models are all ways to answer questions about slow processes without simulating them directly.

Cost per step is set by the number of pair interactions. With about 100 atoms per nm$^3$ and a 1 nm cutoff, each atom has $\tfrac{4}{3}\pi (1\,\text{nm})^3 \times 100 \approx 420$ neighbours. A 100,000-atom system therefore evaluates about $2\times10^7$ pair interactions per step (each pair counted once), plus the long-range electrostatics.

## A short history

<div data-videos="PGqCeSjNuTY eNuV8pYd-is SgH_GcFhQf8"></div>

- **1957, [Alder and Wainwright](cite:alder1957).** First MD simulation: hard spheres, showing a fluid-solid transition.
- **1964, [Rahman](cite:rahman1964).** 864 argon atoms with a Lennard-Jones potential: the first simulation with a continuous potential, and agreement with experiment on the structure and diffusion of the liquid.
- **1967, [Verlet](cite:verlet1967).** The integrator and the neighbour list that are still in use.
- **1971, [Rahman and Stillinger](cite:rahman1971).** Liquid water, 216 molecules.
- **1977, [McCammon, Gelin and Karplus](cite:mccammon1977).** First protein simulation: the 58-residue inhibitor BPTI, in vacuum, for less than 10 ps. The lasting result was qualitative: the interior of a protein is fluid-like, not rigid.
- **1977, [Ryckaert, Ciccotti and Berendsen](cite:ryckaert1977).** SHAKE: bond constraints, which allow a larger time step.
- **1980s.** Thermostats and barostats (Andersen, Berendsen, Nosé, Hoover, Parrinello and Rahman), free-energy perturbation applied to biomolecules, the first AMBER, CHARMM, GROMOS and OPLS force fields.
- **1993 to 1995.** Particle-mesh Ewald makes proper long-range electrostatics affordable.
- **2010 to 2011, [Shaw and co-workers](cite:shaw2010).** Millisecond simulation of BPTI and reversible folding of twelve small proteins on Anton.
- **2013.** Nobel Prize in Chemistry to Karplus, Levitt and Warshel for multiscale models of complex chemical systems.
- **Since about 2015.** GPUs make microsecond simulations routine; machine-learned potentials and generative models of ensembles appear (Module 17).

## What you get out, and the three kinds of error

<div data-videos="XrLfl_b4X5k 4zhx74oR_dM"></div>

MD gives three classes of result:

- **Structure**: average geometries, distributions of distances and angles, radial distribution functions, the ensemble of conformations.
- **Thermodynamics**: averages and fluctuations (energy, density, heat capacity) and, with extra work, free-energy differences.
- **Dynamics**: diffusion constants, relaxation times, rates. These depend on the thermostat and the model more than structural averages do.

Every number from MD carries three kinds of error, and it helps to keep them apart:

1. **Model error (accuracy of the force field).** The energy function is an approximation. More sampling does not fix this. You detect it by comparing with experiment.
2. **Sampling error (precision).** The trajectory is finite, and consecutive frames are correlated. You detect it with repeats from different starting velocities, block averaging and convergence checks (Module 11).
3. **Set-up and implementation error.** Wrong protonation state, a box that is too small, a thermostat that distorts the ensemble, a cutoff that is inconsistent with the force field. You avoid it by knowing what every setting does, which is the purpose of Modules 7 to 10.

A common mistake is to treat a single long trajectory as "the answer". It is one sample path of a chaotic system. Change the initial velocities and you get a different path with the same statistics, if and only if both runs are long enough.

## Check yourself

<details markdown="1"><summary>1. Why is the time step about 1 to 2 fs, and what would happen at 10 fs?</summary>
The integrator must take roughly ten or more steps per period of the fastest motion. Bonds to hydrogen vibrate with a period near 10 fs, so unconstrained simulations use 1 fs. With those bonds constrained, the next fastest motions allow 2 fs. At 10 fs the integration of bond and angle vibrations is unstable: energy grows without bound within a few steps and the program stops with an error (in GROMACS usually a LINCS or SETTLE warning).
</details>

<details markdown="1"><summary>2. You double the number of atoms. How does the cost per step change?</summary>
With a cutoff and a neighbour list the number of pairs within the cutoff grows linearly with $N$, so the short-range cost doubles. Particle-mesh Ewald scales as $N\log N$. Without a cutoff the cost would grow as $N^2$.
</details>

<details markdown="1"><summary>3. A colleague says a 500 ns simulation "shows the binder stays bound, so the affinity is high". What is wrong?</summary>
A complex with a micromolar dissociation constant typically has a residence time of milliseconds or longer, which is thousands of times the simulated time. Both a weak and a strong binder will stay bound for 500 ns. Staying bound only rules out very unstable poses. Affinity is a free-energy difference and needs the methods of Modules 12 and 13.
</details>

<details markdown="1"><summary>4. Which approximation makes it impossible for a standard force field to describe an enzyme reaction?</summary>
The fixed bonding topology that replaces the electronic problem. The list of bonds is an input, and the bond term is a spring that cannot break.
</details>

## Exercises

1. Run the Python code above. Plot total, kinetic and potential energy against time. Then increase `dt` to 0.01 and 0.02 and describe what happens to the total energy.
2. Compute the thermal de Broglie wavelength for deuterium and for oxygen at 300 K.
3. A system has 80,000 atoms and runs at 250 ns/day with a 2 fs step. How many pair forces per second is the GPU evaluating, assuming 420 neighbours per atom? How long would 1 ms take?
4. Use the live simulation above with the thermostat on. Find the temperature below which the fluid condenses into a droplet. Why is there no sharp transition in such a small system?

## Read

{{READ}}

## Key papers

{{PAPERS}}
