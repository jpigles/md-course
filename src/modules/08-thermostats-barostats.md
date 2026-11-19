---
num: 8
title: Thermostats and barostats, controlling temperature and pressure
short: Thermostats and barostats
part: Part II · The engine
hours: 7
summary: Understand how each thermostat and barostat modifies the equations of motion, which of them sample the correct ensemble, and which to use for equilibration and for production.
videos: 8
papers: D
tags: thermostats-barostats
---

<div class="box goal" markdown="1">
#### After this module you can

- compute temperature and pressure from a trajectory and say how much they should fluctuate;
- write the equations of the Berendsen, velocity-rescale, Andersen, Langevin and Nosé-Hoover thermostats;
- show that Langevin dynamics and Nosé-Hoover dynamics have the canonical distribution as their stationary state;
- explain Berendsen, Parrinello-Rahman, Monte Carlo and stochastic cell rescaling barostats;
- choose a defensible combination and coupling time for your own simulation.
</div>

## Watch first

{{WATCH}}

## Why control temperature at all

<div data-videos="5LALoxDs0ic"></div>

Newtonian MD conserves energy and samples the microcanonical (NVE) ensemble. We usually want the canonical (NVT) or isothermal-isobaric (NPT) ensemble because:

- experiments are done at fixed temperature and pressure;
- numerical errors (integration, cutoffs, constraints) add or remove energy slowly, and without a thermostat the temperature drifts;
- non-equilibrium procedures (pulling, alchemical changes, equilibration from a poor start) put work into the system that has to be removed.

From Module 3, the instantaneous temperature is $T_{inst} = 2K/(N_{df}k_B)$, and in the canonical ensemble it must fluctuate with relative standard deviation $\sqrt{2/N_{df}}$. A thermostat's job is to make the *distribution* of kinetic energy correct, not to pin $T_{inst}$ to a number. More precisely, the kinetic energy must follow a gamma distribution:

$$
P(K)\propto K^{N_{df}/2-1}\,e^{-\beta K}.
$$

## Thermostats

<div data-videos="l-uZaSvlycY ey1tv0yoyGc HiZ7gvtmDbk pCm2i6kQs4E X3K5A96-U4E"></div>

### Simple velocity scaling, and Berendsen

The crudest method multiplies all velocities each step by $\lambda=\sqrt{T_0/T_{inst}}$. This fixes the kinetic energy exactly, which is the wrong distribution.

The **Berendsen** thermostat ([1984](cite:berendsen1984)) relaxes the temperature towards the target with a time constant $\tau_T$, as if the system were weakly coupled to a bath:

$$
\frac{dT}{dt} = \frac{T_0-T}{\tau_T}
\qquad\Longrightarrow\qquad
\lambda^2 = 1+\frac{\Delta t}{\tau_T}\left(\frac{T_0}{T_{inst}}-1\right).
$$

It is stable and brings a system to the target temperature quickly and smoothly. It does **not** generate the canonical ensemble: it suppresses the fluctuations of the kinetic energy, and in doing so it slowly transfers energy from high-frequency internal motions into low-frequency ones. The extreme case is the "flying ice cube", where kinetic energy ends up in the translation of the whole system. If you use it at all, use it for equilibration only: current best-practice guides ([Braun et al. 2018](cite:braun2018)) recommend a thermostat that samples the correct ensemble even there.

### Stochastic velocity rescaling

[Bussi, Donadio and Parrinello (2007)](cite:bussi2007b) kept the idea of a global rescaling but made the target kinetic energy itself a random variable with the correct canonical distribution. The kinetic energy follows

$$
dK = \left(\bar K - K\right)\frac{dt}{\tau_T} + 2\sqrt{\frac{K\bar K}{N_{df}\,\tau_T}}\;dW,\qquad \bar K = \tfrac12N_{df}k_BT_0,
$$

where $dW$ is a Wiener noise. The first term is Berendsen. The second supplies exactly the fluctuations Berendsen removes. The result samples the canonical ensemble and has first-order (non-oscillating) relaxation. Because it acts on all velocities with one scale factor, it leaves constraints and the centre-of-mass motion untouched, and with a coupling time that is not too short (0.1 ps or more) it disturbs the dynamics very little. It also has an energy-like quantity that should stay nearly constant along a run: a drift in it means the time step is too large. This is `tcoupl = V-rescale` in GROMACS and a good default.

### Andersen

At random times, with collision frequency $\nu$, a particle's velocity is replaced by a fresh draw from the Maxwell-Boltzmann distribution. This samples the canonical ensemble rigorously. The collisions decorrelate velocities, so diffusion and other dynamical properties are altered. It is useful when dynamics do not matter.

### Langevin dynamics

<div data-videos="AzCzDYLimvc jonJHFcYTso"></div>

Add a friction force and a random force to each particle:

$$
m\,\dot{\mathbf v} = \mathbf F(\mathbf r) - \gamma m\,\mathbf v + \sqrt{2\gamma m k_BT}\;\boldsymbol\eta(t),\qquad \langle\eta_a(t)\,\eta_b(t')\rangle = \delta_{ab}\,\delta(t-t').
$$

The friction removes energy and the noise adds it. The two are tied together by the **fluctuation-dissipation theorem**: the noise amplitude must be $\sqrt{2\gamma mk_BT}$ for the system to settle at temperature $T$.

<div class="box key" markdown="1">
**Why that amplitude.** Take one velocity component with no force: $dv = -\gamma v\,dt + \sigma\,dW$. This is an Ornstein-Uhlenbeck process with solution

$$
v(t) = v(0)\,e^{-\gamma t} + \sigma\int_0^te^{-\gamma(t-s)}dW(s).
$$

Its mean decays to zero and its variance tends to $\sigma^2/2\gamma$. The Maxwell-Boltzmann distribution requires a variance of $k_BT/m$, so $\sigma^2 = 2\gamma k_BT/m$. With forces present, one can check that $\rho\propto e^{-\beta H}$ is the stationary solution of the corresponding Fokker-Planck equation: the Hamiltonian part of the flow leaves $e^{-\beta H}$ unchanged (Liouville, Module 2), and the friction and noise terms cancel each other exactly for a Maxwell-Boltzmann distribution of velocities.
</div>

The exact solution over one time step is what integrators use for the "O" step (Module 4):

$$
\mathbf v \leftarrow e^{-\gamma\Delta t}\,\mathbf v + \sqrt{\frac{k_BT}{m}\left(1-e^{-2\gamma\Delta t}\right)}\;\boldsymbol\xi,\qquad \boldsymbol\xi\sim\mathcal N(0,1).
$$

Properties: canonical, local (each particle is thermostatted, so it also equilibrates poorly coupled parts of the system), and very robust. The cost is that momentum is not conserved and dynamics are slowed: the friction adds to the natural friction of the solvent. For explicit solvent $\gamma$ = 0.1 to 1 ps$^{-1}$ is a mild perturbation. For implicit-solvent and coarse-grained models there is no solvent friction, and $\gamma$ becomes a parameter that sets the time scale: with low friction the dynamics are much faster than in reality, which helps sampling but means simulated time has no physical meaning.

In the limit of high friction the inertial term can be dropped, giving **Brownian (overdamped Langevin) dynamics**:

$$
d\mathbf r = \frac{D}{k_BT}\,\mathbf F\,dt + \sqrt{2D\,dt}\;\boldsymbol\xi,\qquad D = \frac{k_BT}{m\gamma}.
$$

The umbrella-sampling demo in Module 12 uses this equation.

### Nosé-Hoover

A deterministic alternative. Add one extra dynamical variable, a friction coefficient $\xi$ that responds to the kinetic energy:

$$
\dot{\mathbf r}_i = \frac{\mathbf p_i}{m_i},\qquad
\dot{\mathbf p}_i = \mathbf F_i - \xi\,\mathbf p_i,\qquad
\dot\xi = \frac{1}{Q}\left(\sum_i\frac{\mathbf p_i^2}{m_i} - N_{df}k_BT_0\right).
$$

When the system is too hot the bracket is positive, $\xi$ grows and the friction cools the system. When it is too cold, $\xi$ becomes negative and heats it. The "mass" $Q$ sets the response time: $Q = N_{df}k_BT_0\,\tau_T^2$ up to a numerical factor, where $\tau_T$ is the period of the temperature oscillations.

**Proof that this is canonical.** The flow is no longer incompressible. Its divergence is

$$
\sum_i\frac{\partial\dot{\mathbf p}_i}{\partial\mathbf p_i} = -N_{df}\,\xi .
$$

The generalised Liouville equation for a density $f(\mathbf r,\mathbf p,\xi)$ then requires $d\ln f/dt = +N_{df}\,\xi$ along a trajectory. Try $f\propto\exp\left[-\beta\left(H+\tfrac12Q\xi^2\right)\right]$:

$$
\frac{d\ln f}{dt} = -\beta\left(\dot H + Q\xi\dot\xi\right)
= -\beta\left(-\xi\sum_i\frac{\mathbf p_i^2}{m_i} + \xi\sum_i\frac{\mathbf p_i^2}{m_i} - \xi N_{df}k_BT_0\right) = N_{df}\,\xi .\quad\checkmark
$$

So $e^{-\beta H}$ times a Gaussian in $\xi$ is stationary. The dynamics are smooth and time-reversible and conserve an extended energy.

Two caveats. The proof shows the canonical density is *a* stationary state, not that the dynamics reach it: for small or stiff systems (a single harmonic oscillator is the textbook case) Nosé-Hoover is not ergodic. **Nosé-Hoover chains** ([Martyna, Klein and Tuckerman 1992](cite:martyna1992)), where the thermostat variable is itself thermostatted by a second, and so on, fix this. And the temperature approaches its target with oscillations, so it is a poor choice for equilibrating a system that starts far from the target.

### Summary of thermostats

| Thermostat | Canonical? | Perturbs dynamics | Good for |
|---|---|---|---|
| Berendsen | No | Little | Fast, smooth equilibration only |
| Stochastic velocity rescaling | Yes | Very little | Equilibration and production |
| Andersen | Yes | Strongly | Sampling when dynamics are irrelevant |
| Langevin | Yes | Depends on $\gamma$ | Implicit solvent, coarse-grained models, free-energy calculations, GPU codes |
| Nosé-Hoover (chains) | Yes | Little | Production of well-equilibrated systems |

**Practical points.** Use $\tau_T$ of 0.1 to 1 ps for velocity rescaling and Nosé-Hoover, and $\gamma\approx1$ ps$^{-1}$ for Langevin in explicit solvent. Thermostat the protein and the solvent as separate groups only if each group is large; coupling very small groups separately creates artefacts. Remove centre-of-mass motion.

<div class="widget" data-widget="thermostats"></div>

## Pressure

The instantaneous pressure comes from the virial (Module 3):

$$
P_{inst} = \frac{2}{3V}\left(K - \Xi\right),\qquad \Xi = -\frac12\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}.
$$

In an anisotropic system it is a tensor $\mathbf P = \frac{2}{V}(\mathbf K-\boldsymbol\Xi)$.

**The pressure fluctuates enormously.** Water is nearly incompressible, $\kappa_T = 4.5\times10^{-5}$ bar$^{-1}$, so a relative volume fluctuation of only 0.1 % corresponds to a pressure change of about 20 bar. In a box of a few nanometres, instantaneous pressures swing by several hundred bar from step to step. This is physical. A pressure of "1.0 ± 250 bar" is normal: judge the average over a long window, and judge equilibration by the **density**, which converges much faster.

In the NPT ensemble the volume fluctuates as

$$
\langle\delta V^2\rangle = k_BT\,\langle V\rangle\,\kappa_T ,
$$

and a correct barostat must reproduce this.

## Barostats

<div data-videos="rGOyUWV0fX0"></div>

All barostats change the volume by scaling the box and the particle coordinates. They differ in how the scaling factor is determined.

### Berendsen

First-order relaxation of the pressure, the analogue of the Berendsen thermostat:

$$
\frac{dP}{dt}=\frac{P_0-P}{\tau_P}\qquad\Longrightarrow\qquad
\mu = \left[1-\frac{\kappa_T\,\Delta t}{\tau_P}\,(P_0-P_{inst})\right]^{1/3},
$$

with coordinates and box edges scaled by $\mu$ each step. Robust and non-oscillating, but it gives the wrong volume fluctuations, so it does not sample NPT. Equilibration only.

### Extended-system barostats: Andersen, Parrinello-Rahman, MTTK

[Andersen (1980)](cite:andersen1980) made the volume a dynamical variable with a fictitious mass $W$ and a "kinetic energy", driven by the imbalance between internal and external pressure:

$$
W\,\ddot V = P_{inst}-P_0 .
$$

[Parrinello and Rahman (1981)](cite:parrinello1981) generalised this to the full box matrix $\mathbf h$, so that the box can change shape as well as size, which is needed for crystals and membranes. [Martyna, Tobias and Klein (1994)](cite:martyna1994), and later the same authors with Tuckerman (MTTK), derived extended-system equations that sample the exact NPT ensemble. Parrinello-Rahman, the form most used in GROMACS, gives correct averages for a well-equilibrated system, but its volume fluctuations are not guaranteed to be exactly those of NPT: use MTTK, stochastic cell rescaling or a Monte Carlo barostat when the fluctuations themselves matter. Like Nosé-Hoover, all these methods are second-order: far from equilibrium the box oscillates and can become unstable. Do not start an NPT run with Parrinello-Rahman from an unequilibrated density.

### Stochastic cell rescaling

[Bernetti and Bussi (2020)](cite:bernetti2020) did for pressure what velocity rescaling did for temperature: Berendsen's first-order relaxation plus a noise term of exactly the right size,

$$
d\varepsilon = -\frac{\kappa_T}{\tau_P}\left(P_0-P_{inst}\right)dt + \sqrt{\frac{2k_BT\,\kappa_T}{V\,\tau_P}}\;dW,\qquad \varepsilon = \ln\frac{V}{V_0}.
$$

It samples the correct NPT ensemble, does not oscillate, and can be used from the start of equilibration through production, provided the coupling time $\tau_P$ is not too short and the pressure coupling is applied often enough (the original paper found errors with very small $\tau_P$ and with coupling only every ten steps or more). In GROMACS it is `pcoupl = C-rescale`.

### Monte Carlo barostat

Every few steps, propose a random volume change $V\to V'$, scale the coordinates of molecular centres, and accept with probability

$$
P_{acc} = \min\left\{1,\ \exp\left[-\beta\left(\Delta U + P_0\,\Delta V\right) + N_{mol}\ln\frac{V'}{V}\right]\right\},
$$

where $N_{mol}$ is the number of independently scaled centres (molecules, when each molecule is moved as a rigid body) and the trial volume is drawn uniformly in $V$. It needs no virial, which is convenient for GPU codes and unusual potentials, and it samples NPT exactly. This is OpenMM's `MonteCarloBarostat` and an option in AMBER. The barostat does not use the instantaneous pressure, though OpenMM can compute it on request (`computeCurrentPressure`).

### Coupling types

- **Isotropic**: one scale factor. Proteins in water.
- **Semi-isotropic**: $x$ and $y$ coupled together, $z$ separately. Membranes, where area and thickness must adjust independently.
- **Anisotropic**: full tensor. Crystals. In a liquid it lets the box deform without limit, so avoid it.

## A defensible protocol

| Stage | Thermostat | Barostat |
|---|---|---|
| Heating and first equilibration (NVT), 100 ps | Velocity rescaling or Langevin, $\tau_T$ = 0.1 ps | none |
| Density equilibration (NPT), 100 ps to 1 ns | same | Stochastic cell rescaling (or Berendsen), $\tau_P$ = 1 to 2 ps |
| Production (NPT) | Velocity rescaling, Langevin or Nosé-Hoover chains | Stochastic cell rescaling, Parrinello-Rahman ($\tau_P$ = 2 to 5 ps) or Monte Carlo |

State the thermostat, barostat and coupling constants in your methods section. They are part of the model.

## Check yourself

<details markdown="1"><summary>1. Your temperature plot is a perfectly flat line at 300.00 K. Is that good?</summary>
No. The instantaneous temperature must fluctuate with standard deviation $T\sqrt{2/N_{df}}$. A flat line means the kinetic energy is being pinned (isokinetic scaling or an extremely short Berendsen time constant), which is not the canonical ensemble.
</details>

<details markdown="1"><summary>2. Why is the Berendsen thermostat acceptable for equilibration but not for production?</summary>
During equilibration the goal is to reach the target state quickly and stably, and the ensemble is irrelevant because the data are discarded. In production the distribution of kinetic energy is too narrow, so fluctuation-based properties are wrong, and energy is redistributed unphysically between degrees of freedom over long times.
</details>

<details markdown="1"><summary>3. In an implicit-solvent Langevin simulation you lower γ from 50 ps⁻¹ to 1 ps⁻¹ and conformational transitions become ten times faster. Did the free-energy landscape change?</summary>
No. The stationary distribution of Langevin dynamics is $e^{-\beta H}$ for every $\gamma>0$ (exactly for the continuous equations; an integrator with a finite time step samples a slightly different distribution, with an error that depends on $\Delta t$ and hardly on $\gamma$). Only the kinetics changed. Populations are comparable between the two runs; rates and times are not.
</details>

<details markdown="1"><summary>4. The average pressure over 100 ps is −14 bar with a target of 1 bar. Is the barostat broken?</summary>
Not necessarily. With fluctuations of a few hundred bar and a correlation time of the order of a picosecond, the standard error of a 100 ps average is tens of bar. Check the density instead and average the pressure over nanoseconds.
</details>

## Exercises

1. Add a Langevin thermostat (BAOAB) to the Python code of Module 1. Verify that the average temperature matches the target and that the kinetic energy histogram matches the gamma distribution (up to an error of order $\Delta t^2$, which shrinks as you reduce the time step).
2. Simulate a single harmonic oscillator with a Nosé-Hoover thermostat and plot the $(x,p)$ points visited. Compare with the Gaussian you expect. Then add a second thermostat in a chain and repeat.
3. Add a Berendsen thermostat to the same code and compare the variance of the kinetic energy with the canonical value $\tfrac12N_{df}(k_BT)^2$ for several values of $\tau_T$.
4. From an NPT simulation of water, compute the isothermal compressibility from the volume fluctuations, once with a Berendsen barostat and once with stochastic cell rescaling. Compare with the experimental $4.5\times10^{-5}$ bar$^{-1}$ and with the value of your water model itself (TIP3P gives about $6\times10^{-5}$ bar$^{-1}$).

## Read

{{READ}}

## Key papers

{{PAPERS}}
