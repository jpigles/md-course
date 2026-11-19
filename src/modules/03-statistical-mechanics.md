---
num: 3
title: Statistical mechanics, the link between a trajectory and a measurement
short: Statistical mechanics
part: Part I · Foundations
hours: 8
summary: Derive the Boltzmann distribution, connect partition functions to free energies, and understand why a time average over an MD trajectory equals a thermodynamic average.
videos: 3
tags: stat-mech
---

<div class="box goal" markdown="1">
#### After this module you can

- define a microstate, a macrostate and an ensemble, and say which ensemble a given simulation samples;
- derive the canonical distribution $P\propto e^{-\beta H}$ from a system in contact with a heat bath;
- compute averages and fluctuations from a partition function, and the temperature and pressure from a trajectory;
- explain what a free energy is and why it is harder to compute than an energy;
- define the potential of mean force and write a binding constant as a ratio of partition functions.
</div>

## Watch first

{{WATCH}}

## Microstates, macrostates, ensembles

<div data-videos="lKyrJhN8MFY tcTmOEk8cc4 lLhUpB6oOr8 5LALoxDs0ic HDl63ZSFVwM D1RzvXDXyqA zyId5iqW6Ig"></div>

A **microstate** is one point in phase space, $\Gamma=(\mathbf r,\mathbf p)$: every position and momentum. A **macrostate** is what an experiment controls or measures: number of particles $N$, volume $V$, energy $E$, temperature $T$, pressure $P$. An enormous number of microstates is compatible with one macrostate. An **ensemble** is the probability distribution over microstates that corresponds to a macrostate.

| Ensemble | Fixed | Probability density of a microstate | Thermodynamic potential | MD realisation |
|---|---|---|---|---|
| Microcanonical (NVE) | $N,V,E$ | $\propto \delta(H(\Gamma)-E)$ | Entropy $S = k_B\ln\Omega$ | Plain Newtonian MD |
| Canonical (NVT) | $N,V,T$ | $\propto e^{-\beta H(\Gamma)}$ | Helmholtz $A = -k_BT\ln Q$ | MD with a thermostat |
| Isothermal-isobaric (NPT) | $N,P,T$ | $\propto e^{-\beta (H(\Gamma)+PV)}$ | Gibbs $G = -k_BT\ln\Delta$ | Thermostat and barostat |
| Grand canonical (µVT) | $\mu,V,T$ | $\propto e^{-\beta (H-\mu N)}$ | $-PV$ | Monte Carlo insertion moves |

Here $\beta = 1/k_BT$. Most biomolecular simulation is NPT, matching a test tube at 1 bar.

## Where the Boltzmann factor comes from

<div data-videos="_6AFgt2gkr0 tDKjLzbXYQI aFEovHmSvQk J-qTchJh4Ok EmM1jOV1uSY rhFkYjaM5kE SmmGDn8OnTA"></div>

**Postulate (equal a priori probabilities).** For an isolated system with energy $E$, all accessible microstates are equally likely. The number of them is $\Omega(N,V,E)$, and Boltzmann's entropy is $S = k_B\ln\Omega$.

Now take a small system in thermal contact with a very large bath. Together they are isolated with total energy $E_{tot}$. The probability that the small system is in one particular microstate with energy $E_s$ is proportional to the number of bath microstates that go with it:

$$
P(\text{microstate } s) \propto \Omega_{bath}(E_{tot}-E_s).
$$

Expand the logarithm, which varies slowly, to first order in $E_s \ll E_{tot}$:

$$
\ln\Omega_{bath}(E_{tot}-E_s) \approx \ln\Omega_{bath}(E_{tot}) - E_s \frac{\partial\ln\Omega_{bath}}{\partial E}.
$$

Thermodynamics defines temperature by $1/T = \partial S/\partial E$, so $\partial\ln\Omega_{bath}/\partial E = 1/k_BT = \beta$. Therefore

$$
\boxed{P(s) = \frac{e^{-\beta E_s}}{Q},\qquad Q=\sum_s e^{-\beta E_s}}
$$

This is the canonical (Boltzmann) distribution, and $Q$ is the **partition function**. The only property of the bath that survives is its temperature.

### The classical partition function

<div data-videos="UxJCRnNJCPw 34OuWjAwI8w RT_v0PhXP5E"></div>

For classical particles the sum over states becomes an integral over phase space:

$$
Q(N,V,T) = \frac{1}{N!\,h^{3N}}\int d\mathbf r^N\,d\mathbf p^N\; e^{-\beta H(\mathbf r,\mathbf p)} .
$$

The factor $h^{3N}$ makes $Q$ dimensionless and matches the quantum count of states. The $N!$ corrects for identical particles. With $H = \sum \mathbf p_i^2/2m_i + U(\mathbf r)$ the momentum integrals are Gaussian and can be done exactly:

$$
\int d\mathbf p\,e^{-\beta \mathbf p^2/2m} = (2\pi m k_BT)^{3/2}
\quad\Longrightarrow\quad
Q = \frac{1}{N!\,\Lambda^{3N}}\underbrace{\int d\mathbf r^N e^{-\beta U(\mathbf r)}}_{Z},\qquad \Lambda = \frac{h}{\sqrt{2\pi mk_BT}}.
$$

$Z$ is the **configurational integral**. (The formula is written for identical particles of one mass. With several species, each atom contributes its own $\Lambda_i^3$ and each species $s$ its own $N_s!$: $Q = Z/\big[\prod_sN_s!\,\prod_i\Lambda_i^3\big]$. Nothing below depends on this.) This factorisation has a practical meaning: in classical statistical mechanics, **the distribution of positions does not depend on the masses**, and the momenta always follow the Maxwell-Boltzmann distribution regardless of the forces. All the difficulty, and all the chemistry, is in $Z$. It is also why hydrogen mass repartitioning (Module 9) does not change equilibrium properties.

## From the partition function to thermodynamics

<div data-videos="_ErxZOHwtaA AhNHsYpemII bW30Rj6w8VI"></div>

Everything follows from $Q$:

$$
A = -k_BT\ln Q,\qquad
\langle E\rangle = -\frac{\partial \ln Q}{\partial\beta},\qquad
P = k_BT\frac{\partial\ln Q}{\partial V},\qquad
S = -\frac{\partial A}{\partial T}.
$$

Check the second one: $-\partial_\beta \ln Q = \frac{1}{Q}\sum_s E_s e^{-\beta E_s} = \langle E\rangle$. Differentiating once more gives the fluctuations:

$$
\frac{\partial^2\ln Q}{\partial\beta^2} = \langle E^2\rangle - \langle E\rangle^2
\quad\Longrightarrow\quad
C_V = \frac{\partial \langle E\rangle}{\partial T} = \frac{\langle E^2\rangle-\langle E\rangle^2}{k_BT^2}.
$$

This is a general pattern: **response functions are fluctuations**. The heat capacity is the variance of the energy, the compressibility is the variance of the volume ($\langle\delta V^2\rangle = k_BT\,V\kappa_T$ in NPT), and the dielectric constant is the variance of the total dipole moment. Relative fluctuations scale as $1/\sqrt N$: for a macroscopic sample they are invisible, for a simulation box of $10^5$ atoms they are a fraction of a percent, and for the instantaneous pressure they are large (Module 8).

## Equipartition and temperature

<div data-videos="KthbNCxnj2g b8n1k3Iob0Q uoieTQ3Qb3M MCRHXHskWnE"></div>

For any degree of freedom that appears in $H$ as a quadratic term $a x^2$,

$$
\langle a x^2\rangle = \frac{\int a x^2 e^{-\beta a x^2}dx}{\int e^{-\beta a x^2}dx} = \frac{1}{2}k_BT .
$$

Each momentum component contributes $\tfrac12k_BT$ of kinetic energy, so $\langle K\rangle = \tfrac12 N_{df}k_BT$. MD codes turn this around to *define* the instantaneous temperature:

$$
T_{inst} = \frac{2K}{N_{df}k_B},\qquad N_{df} = 3N - N_{constraints} - 3 .
$$

The 3 accounts for the conserved total momentum in a periodic box. $T_{inst}$ fluctuates even at perfect equilibrium, with relative standard deviation $\sqrt{2/N_{df}}$ in the canonical ensemble. For 100 atoms that is 8 %, for 100,000 atoms 0.26 %.

The velocity of each atom follows the Maxwell-Boltzmann distribution: each Cartesian component is Gaussian with variance $k_BT/m$. Initial velocities are drawn from it.

## Pressure and the virial

<div data-videos="2BJYXuZZK3c jny9W7NtlK4"></div>

Using $P = k_BT\,\partial\ln Q/\partial V$ and scaling the coordinates with the box gives the **virial equation**:

$$
P = \frac{N k_BT}{V} + \frac{1}{3V}\Big\langle \sum_i \mathbf r_i\cdot\mathbf F_i\Big\rangle
= \frac{1}{3V}\Big\langle 2K + \sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}\Big\rangle .
$$

The first term is the ideal-gas pressure. The second, the virial, is the contribution of the interactions: attractive forces lower the pressure, repulsive ones raise it. The pair form on the right is the one to use with periodic boundaries.

## Why a time average equals an ensemble average

<div data-videos="rBni87N8cBs WneHzwWh0Ws Iq9ZxMRbpmc"></div>

An experiment measures a time average over a huge number of molecules. Statistical mechanics gives the ensemble average

$$
\langle A\rangle = \int d\Gamma\,A(\Gamma)\,P(\Gamma).
$$

MD computes a time average along one trajectory. The **ergodic hypothesis** says the two agree for an infinitely long trajectory:

$$
\langle A\rangle = \lim_{\tau\to\infty}\frac{1}{\tau}\int_0^{\tau}A(\Gamma(t))\,dt \;\approx\; \frac{1}{M}\sum_{n=1}^{M}A(\Gamma(t_n)).
$$

This is the single most important equation for using MD, and its weak point is the word "infinitely". A system with high barriers is ergodic in principle but not on the time scale you can afford. If your protein has two conformations separated by a barrier that is crossed once per millisecond, a microsecond trajectory samples one of them and the "average" is wrong, with no warning. Module 11 covers how to detect this and Module 14 how to fight it.

Note what is *not* required: the trajectory does not need to be the true physical trajectory. Any dynamics that visits microstates with the right probability gives correct equilibrium averages. That is why thermostats that perturb the dynamics, Monte Carlo moves, and replica exchange are all legitimate for thermodynamics, while kinetic quantities need more care.

<div class="widget" data-widget="boltzmann"></div>

## Free energy

<div data-videos="3XyGqsgBpIM Lq8GwTlJ9Z8 BznPadIkfKM mg9JWntdfyE"></div>

The Helmholtz free energy $A = -k_BT\ln Q = \langle E\rangle - TS$ counts states, weighted by their Boltzmann factors. The most useful form of this statement is about the relative probability of two **macrostates** A and B (two regions of configuration space, for example "bound" and "unbound", or "folded" and "unfolded"):

$$
\frac{P_B}{P_A} = \frac{\int_B e^{-\beta U}d\mathbf r}{\int_A e^{-\beta U}d\mathbf r} = \frac{Z_B}{Z_A} = e^{-\beta\,\Delta A_{A\to B}},
\qquad \Delta A = -k_BT\ln\frac{Z_B}{Z_A}.
$$

<div class="box key" markdown="1">
**Energy against entropy, a two-state example.** State A is one conformation with energy 0. State B has energy $+10$ kJ/mol but consists of 1,000 conformations of equal energy. At 300 K, $Z_A = 1$ and $Z_B = 1000\,e^{-10/2.494} = 18.1$, so $\Delta A = -2.494\ln 18.1 = -7.2$ kJ/mol: B is favoured 18 to 1 although its energy is higher. The entropy term is $-T\Delta S = -k_BT\ln 1000 = -17.2$ kJ/mol. Looking at energies of single structures, which is what most scoring functions do, would get the sign wrong.
</div>

**Why free energies are hard.** An average like $\langle U\rangle$ is dominated by the configurations the simulation visits most. The free energy is different. One can write

$$
e^{+\beta A_{config}} \propto \frac{1}{Z} = \frac{\langle e^{+\beta U}\rangle}{V^N},
$$

an average dominated by the *high*-energy configurations that a Boltzmann-weighted simulation almost never visits. Absolute free energies are therefore out of reach, and practical methods compute *differences* between states that are made to overlap (Modules 12 and 13).

### The potential of mean force

<div data-videos="pjT7waGUGDI"></div>

Often we care about one coordinate $\xi(\mathbf r)$, a distance, an angle, or a fraction of native contacts, and want the free energy as a function of it. Its probability density is obtained by integrating out everything else:

$$
P(\xi') = \frac{1}{Z}\int d\mathbf r\;\delta\big(\xi(\mathbf r)-\xi'\big)\,e^{-\beta U(\mathbf r)},
\qquad
W(\xi') = -k_BT\ln P(\xi') + \text{const}.
$$

$W(\xi)$ is the **potential of mean force (PMF)**. The name comes from the fact that, for a Cartesian-like coordinate, its slope is the average force along $\xi$: $-dW/d\xi = \langle F_\xi\rangle_\xi$. Its barriers and wells are free energies: they contain the entropy of all the other degrees of freedom, including the solvent.

For a curvilinear coordinate there is an extra geometric (Jacobian) term. The important case is a distance $r$: the volume available grows as $4\pi r^2$, so $P(r)\propto r^2 g(r)$, where $g(r)$ is the pair distribution function. Two "PMFs" along a distance are therefore in use, and they differ by $2k_BT\ln r$:

$$
w(r) = -k_BT\ln g(r)\qquad\text{and}\qquad W(r) = -k_BT\ln P(r) = w(r) - 2k_BT\ln r + \text{const}.
$$

$w(r)$ is the one whose slope is exactly the mean force between the two particles and which goes to zero at large separation. Always check which of the two a paper or a program reports (Module 12).

### Binding constants

<div data-videos="Srj-ZqBzNv4"></div>

For $\text{P} + \text{L}\rightleftharpoons \text{PL}$, the association constant is a ratio of partition functions. If $w(r) = -k_BT\ln g_{PL}(r)$ is the radial PMF along the separation of the two partners (the $g(r)$-type PMF defined above, with $w\to0$ at large distance), then to a good approximation

$$
K_a = \frac{[\text{PL}]}{[\text{P}][\text{L}]} = 4\pi\int_{bound} r^2\,e^{-\beta w(r)}\,dr,
\qquad
\Delta G^\circ_{bind} = -k_BT\ln\big(K_a C^\circ\big),\qquad K_d = 1/K_a .
$$

$C^\circ = 1$ M $= 0.6022$ molecules per nm$^3$ is the standard concentration. It must appear because $K_a$ has units of volume: the "free energy of binding" is only defined relative to a reference concentration. Module 12 develops this fully.

## Check yourself

<details markdown="1"><summary>1. In a canonical simulation of 30,000 atoms with all bonds to hydrogen constrained (15,000 constraints), what is the expected standard deviation of the instantaneous temperature at 300 K?</summary>
$N_{df} = 90{,}000 - 15{,}000 - 3 = 74{,}997$. $\sigma_T = 300\sqrt{2/74997} = 1.55$ K. A temperature trace that fluctuates by ±1.5 K is correct. One that is flat means the thermostat is suppressing fluctuations.
</details>

<details markdown="1"><summary>2. Two conformations differ in free energy by 2 kcal/mol at 300 K. What are their populations?</summary>
$e^{-2/0.596} = 0.035$, so 96.6 % and 3.4 %.
</details>

<details markdown="1"><summary>3. Does the equilibrium distribution of a dihedral angle change if you triple the mass of every hydrogen?</summary>
No. The configurational distribution $e^{-\beta U(\mathbf r)}/Z$ contains no masses. Only dynamical properties change. (With rigid constraints there is a small mass-dependent correction, which is negligible for bond constraints.)
</details>

<details markdown="1"><summary>4. Why can you not get an absolute entropy by averaging something over a trajectory?</summary>
Entropy is $-k_B\int P\ln P$: it depends on the value of the probability density itself, including the normalisation $Z$, which is the volume of all accessible configuration space. A trajectory gives you samples from $P$ but not the value of $Z$.
</details>

## Exercises

1. For a one-dimensional harmonic oscillator, compute $Q$ classically. Derive $\langle E\rangle = k_BT$ and $C_V = k_B$. Compare with the quantum result and find the temperature below which they differ by more than 10 % for a 3,000 cm$^{-1}$ vibration.
2. Take the energies printed by the Python simulation of Module 1 with a Langevin thermostat added (you will write it in Module 8) and estimate $C_V$ from the energy fluctuations.
3. Derive the virial equation for an ideal gas ($\mathbf F=0$ in the bulk) and check it gives $PV = Nk_BT$.
4. A PMF has a square well of depth 40 kJ/mol between $r=0.9$ and $1.1$ nm and is zero outside. Compute $K_a$, $K_d$ in molar units and $\Delta G^\circ$ at 300 K. Then widen the well to 0.8 to 1.2 nm and explain the change in terms of entropy.

## Read

{{READ}}
