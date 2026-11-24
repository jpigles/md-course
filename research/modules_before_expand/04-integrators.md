---
num: 4
title: Integrating the equations of motion
short: Integrators
part: Part II · The engine
hours: 6
summary: Derive the Verlet family of integrators twice (from Taylor series and from the Liouville operator), and understand why a simple second-order method beats higher-order ones for molecular dynamics.
videos: 4
papers: B
tags: integrators
---

<div class="box goal" markdown="1">
#### After this module you can

- derive the Verlet, velocity Verlet and leap-frog schemes and show they generate the same positions;
- explain "symplectic", "time-reversible" and "shadow Hamiltonian" and why they matter more than the order of accuracy;
- compute the stability limit of the time step for a harmonic bond and justify 1, 2 and 4 fs;
- describe multiple-time-step integration and its limits.
</div>

## Watch first

{{WATCH}}

## The problem

<div data-videos="dOpKIWFDW0s _CTZDDFaE5A"></div>

We need $\mathbf r(t+\Delta t)$ and $\mathbf v(t+\Delta t)$ from $\mathbf r(t)$, $\mathbf v(t)$ and the forces. What makes MD different from most numerical ODE problems:

- the force evaluation is by far the most expensive part, so a method should need **one force evaluation per step**;
- we integrate for $10^7$ to $10^{10}$ steps, so **long-time stability** matters more than the accuracy of any single step;
- the system is chaotic, so reproducing the exact trajectory is impossible anyway (Module 2). What we need is correct statistics.

## Verlet from Taylor series

<div data-videos="g55QvpAev0I qT8pxV53FA4 ld5VABtBkF0"></div>

Expand the position forward and backward in time:

$$
\begin{aligned}
\mathbf r(t+\Delta t) &= \mathbf r(t) + \mathbf v(t)\Delta t + \tfrac12\mathbf a(t)\Delta t^2 + \tfrac16\mathbf b(t)\Delta t^3 + O(\Delta t^4)\\
\mathbf r(t-\Delta t) &= \mathbf r(t) - \mathbf v(t)\Delta t + \tfrac12\mathbf a(t)\Delta t^2 - \tfrac16\mathbf b(t)\Delta t^3 + O(\Delta t^4)
\end{aligned}
$$

Here $\mathbf b$ is the third time derivative of the position. Add the two lines. The odd terms cancel:

$$
\boxed{\mathbf r(t+\Delta t) = 2\mathbf r(t) - \mathbf r(t-\Delta t) + \mathbf a(t)\,\Delta t^2 + O(\Delta t^4)},\qquad \mathbf a = \mathbf F/m .
$$

This is the original **Verlet** algorithm (1967). The error of one step is $O(\Delta t^4)$, and the accumulated error over a fixed time is $O(\Delta t^2)$: a second-order method. Velocities do not appear. If needed they come from the difference $\mathbf v(t) = [\mathbf r(t+\Delta t)-\mathbf r(t-\Delta t)]/2\Delta t$, one step late.

### Velocity Verlet

<div data-videos="ii-N61PeeQU 1kER3-3x8VI"></div>

The form used in practice carries positions and velocities at the same time ([Swope, Andersen, Berens and Wilson, 1982](cite:swope1982)):

$$
\begin{aligned}
\mathbf v(t+\tfrac{\Delta t}{2}) &= \mathbf v(t) + \tfrac{\Delta t}{2}\,\mathbf a(t) &&\text{half kick}\\
\mathbf r(t+\Delta t) &= \mathbf r(t) + \Delta t\,\mathbf v(t+\tfrac{\Delta t}{2}) &&\text{drift}\\
\mathbf v(t+\Delta t) &= \mathbf v(t+\tfrac{\Delta t}{2}) + \tfrac{\Delta t}{2}\,\mathbf a(t+\Delta t) &&\text{half kick}
\end{aligned}
$$

To see that it is the same algorithm, write the drift for two consecutive steps and subtract: you get $\mathbf r(t+\Delta t) - 2\mathbf r(t)+\mathbf r(t-\Delta t) = \Delta t\,[\mathbf v(t+\tfrac{\Delta t}{2}) - \mathbf v(t-\tfrac{\Delta t}{2})] = \mathbf a(t)\Delta t^2$.

### Leap-frog

<div data-videos="pVudb6-_FaM"></div>

Merge the second half kick of one step with the first half kick of the next:

$$
\mathbf v(t+\tfrac{\Delta t}{2}) = \mathbf v(t-\tfrac{\Delta t}{2}) + \Delta t\,\mathbf a(t),\qquad
\mathbf r(t+\Delta t) = \mathbf r(t) + \Delta t\,\mathbf v(t+\tfrac{\Delta t}{2}).
$$

Positions live on integer steps and velocities on half steps, "leaping" over each other. This is the default `integrator = md` in GROMACS. The trajectory of positions is identical to velocity Verlet. The only difference is bookkeeping: kinetic energy at time $t$ must be estimated from the two neighbouring half-step velocities, which slightly changes the reported temperature and how thermostats and barostats are coupled.

## Velocity Verlet from the Liouville operator

<div data-videos="5OZO5GPuSJY Uyg9asVcMOc"></div>

The Taylor derivation hides *why* the method is so good. The operator derivation ([Tuckerman, Berne and Martyna, 1992](cite:tuckerman1992)) shows it. From Module 2, the state evolves as $\Gamma(t) = e^{iLt}\Gamma(0)$ with

$$
iL = iL_r + iL_p,\qquad iL_r = \sum_i \mathbf v_i\cdot\frac{\partial}{\partial\mathbf r_i},\qquad iL_p = \sum_i \frac{\mathbf F_i}{m_i}\cdot\frac{\partial}{\partial\mathbf v_i}.
$$

Each piece alone is trivial to apply exactly. Because $e^{c\,\partial/\partial x}f(x) = f(x+c)$ (Taylor's theorem), $e^{iL_r\Delta t}$ shifts every position by $\mathbf v\Delta t$ with velocities fixed (a drift), and $e^{iL_p\Delta t}$ shifts every velocity by $\mathbf F\Delta t/m$ with positions fixed (a kick).

The two operators do not commute, so $e^{(iL_r+iL_p)\Delta t} \ne e^{iL_r\Delta t}e^{iL_p\Delta t}$. The symmetric **Trotter (Strang) splitting** is accurate to second order:

$$
e^{iL\Delta t} = e^{iL_p\Delta t/2}\;e^{iL_r\Delta t}\;e^{iL_p\Delta t/2} + O(\Delta t^3).
$$

Read from right to left: half kick, drift, half kick. That is velocity Verlet. The derivation gives three properties for free. (Tuckerman, Berne and Martyna state the first, reversibility. The other two are standard results for integrators built from exact flows and are not discussed in their paper.)

**1. Time-reversible.** The product is symmetric, so applying it with $-\Delta t$ exactly undoes a step.

**2. Symplectic.** A drift is the exact flow of the Hamiltonian $K$ alone, and a kick is the exact flow of $U$ alone. Each is therefore a symplectic map, and a composition of symplectic maps is symplectic. One visible consequence: a drift changes $\mathbf r$ by a function of $\mathbf v$ only, and a kick changes $\mathbf v$ by a function of $\mathbf r$ only, so each is a shear in phase space with Jacobian determinant exactly 1, and the numerical map preserves phase-space volume exactly, as the true dynamics does (Liouville's theorem). Symplectic is the stronger property: every symplectic map preserves volume, but not every volume-preserving map is symplectic.

**3. A conserved shadow Hamiltonian.** Each sub-step is the exact flow of a Hamiltonian ($K$ or $U$ alone). The Baker-Campbell-Hausdorff formula then shows that the product is the exact flow of a nearby Hamiltonian

$$
\tilde H = H + \Delta t^2\,H_2 + \Delta t^4\,H_4+\dots
$$

The numerical trajectory conserves $\tilde H$, not $H$ (up to effects that are exponentially small for small $\Delta t$). Since $\tilde H - H = O(\Delta t^2)$ and is bounded, the true energy **oscillates** around a constant with amplitude $\propto\Delta t^2$ and does not drift. A non-symplectic method has no such protection.

<div class="box key" markdown="1">
**Exact result for a harmonic oscillator.** For $H = \tfrac12 v^2 + \tfrac12\omega^2x^2$, one velocity Verlet step is the linear map

$$
\begin{pmatrix}x'\\ v'\end{pmatrix} = \begin{pmatrix} 1-\tfrac12\omega^2\Delta t^2 & \Delta t\\ -\omega^2\Delta t\,(1-\tfrac14\omega^2\Delta t^2) & 1-\tfrac12\omega^2\Delta t^2\end{pmatrix}\begin{pmatrix}x\\ v\end{pmatrix}.
$$

Its determinant is 1 (volume preserved), and you can check by substitution that it conserves exactly

$$
\tilde H = \tfrac12 v^2 + \tfrac12\omega^2\left(1-\tfrac14\omega^2\Delta t^2\right)x^2 .
$$

The shadow Hamiltonian is an oscillator with a slightly softer spring. It only makes sense while the bracket is positive, which gives the stability limit below.
</div>

<div class="widget" data-widget="integrators"></div>

## How large can the time step be?

Insert $x_n = e^{i\theta n}$ into the Verlet recursion for the harmonic oscillator, $x_{n+1} - 2x_n + x_{n-1} = -\omega^2\Delta t^2 x_n$:

$$
\cos\theta = 1 - \tfrac12\omega^2\Delta t^2 .
$$

A real $\theta$ (a bounded oscillation) exists only if

$$
\boxed{\omega\,\Delta t < 2\qquad\Longleftrightarrow\qquad \Delta t < \frac{T_{period}}{\pi}}
$$

Beyond this the solution grows exponentially. Below it, the numerical frequency is $\omega_{num} = \theta/\Delta t \approx \omega\,(1 + \omega^2\Delta t^2/24)$: slightly too fast.

Stability is not accuracy. Real potentials are anharmonic, and energy must also flow correctly between modes, so in practice one uses 10 to 20 steps per period of the fastest motion:

| Fastest motion left in the system | Period | Usual $\Delta t$ |
|---|---|---|
| Bonds to hydrogen (X-H stretch, about 3,000 cm$^{-1}$) | 11 fs | 0.5 to 1 fs |
| Heavy-atom bonds and angles involving H, after constraining X-H bonds | about 20 fs | 2 fs |
| After hydrogen mass repartitioning (H mass about 3 to 4 u) or virtual-site hydrogens | about 30 to 40 fs | 4 fs |
| Coarse-grained beads (Martini) | hundreds of fs | 20 fs |

**How to test your own choice.** Run NVE (no thermostat) for a few hundred picoseconds and measure the drift of the total energy. Express it per atom, in units of $k_BT$ per nanosecond, and compare it with what the developers of your MD program consider acceptable: the designers of the GROMACS pair-list scheme, for example, accept about 0.1 $k_BT$ per nanosecond per atom ([Páll and Hess 2013](cite:pall2013)), which is harmless once a thermostat is on. The fluctuation of the energy should fall by a factor of four when you halve the time step. If it does not, something other than the integrator (a cutoff discontinuity, loose constraint tolerance, neighbour-list buffer) is the source.

## Why not a higher-order method?

<div data-videos="zLnIWwvfuo4"></div>

- **Runge-Kutta 4** needs four force evaluations per step. For the same cost you could take four Verlet steps. It is not symplectic: the energy drifts monotonically, as the demo shows.
- **Gear predictor-corrector** methods use one force evaluation and are more accurate than Verlet at small $\Delta t$, but they are neither reversible nor symplectic and drift at the step sizes used in practice. They were common in the 1970s and 1980s and have disappeared from biomolecular codes.
- **Higher-order symplectic** methods (Forest-Ruth, Yoshida) exist but need several force evaluations and do not allow a larger step for stiff molecular systems.

The stiffness of bond vibrations limits $\Delta t$ by stability, not by accuracy, so a higher order buys nothing.

## Multiple time steps

<div data-videos="CRbC_-iGnZM"></div>

Forces differ in how fast they change. Bonded forces change on the 10 fs scale, short-range non-bonded forces on the 100 fs scale, and the long-range (reciprocal-space) electrostatics more slowly still. Split $iL_p = iL_p^{fast} + iL_p^{slow}$ and nest the Trotter splitting (r-RESPA):

$$
e^{iL\Delta t} \approx e^{iL_p^{slow}\Delta t/2}\Big[e^{iL_p^{fast}\delta t/2}\,e^{iL_r\delta t}\,e^{iL_p^{fast}\delta t/2}\Big]^{n}e^{iL_p^{slow}\Delta t/2},\qquad \delta t = \Delta t/n .
$$

The cheap fast forces are evaluated every inner step, the expensive slow forces once per outer step. The scheme stays reversible and symplectic. Tuckerman, Berne and Martyna showed the reversibility, and showed on Lennard-Jones test systems that the scheme is more stable at large steps than the earlier, non-reversible RESPA. The resonance limit described next was worked out later. The catch is **resonance**: the slow force is applied as periodic impulses, and when the outer step approaches half the period of the fastest motion the impulses pump energy into it. With constrained bonds to hydrogen this limits the outer step to about 4 to 5 fs. GROMACS, NAMD, OpenMM and Desmond all offer some version of this (for example evaluating PME every second or third step).

## Stochastic integrators

With a Langevin thermostat (Module 8) the equations of motion gain a friction term and a random force. The same splitting idea applies, with three pieces: B (kick), A (drift), O (the friction-plus-noise part, which can be solved exactly). [Leimkuhler and Matthews](cite:leimkuhler2012) showed that the ordering **BAOAB** cancels the leading $\Delta t^2$ error in averages of functions of the positions. At high friction its configurational error is up to two orders of magnitude smaller than that of the alternatives at the same $\Delta t$; at low friction the methods behave similarly. OpenMM's `LangevinMiddleIntegrator` uses a closely related "middle" discretisation with the same advantage.

## Check yourself

<details markdown="1"><summary>1. Why does the energy in velocity Verlet oscillate but not drift?</summary>
Because the algorithm is the exact solution of a slightly different Hamiltonian $\tilde H = H + O(\Delta t^2)$. $\tilde H$ is conserved, so $H = \tilde H - O(\Delta t^2)$ varies only by a bounded amount.
</details>

<details markdown="1"><summary>2. A flexible water model has an O-H stretch at 3,500 cm⁻¹. What is the largest stable time step, and what would you use?</summary>
Period $= 1/(c\tilde\nu) = 1/(2.998\times10^{10}\,\text{cm/s}\times3500\,\text{cm}^{-1}) = 9.5$ fs. Stability limit $T/\pi = 3.0$ fs. For accuracy use 0.5 fs (19 steps per period).
</details>

<details markdown="1"><summary>3. Positions from leap-frog and velocity Verlet are identical. Why can the reported temperatures differ?</summary>
Leap-frog has velocities at half steps. The kinetic energy at step $t$ is computed as the average of the kinetic energies at $t\pm\Delta t/2$ (or from averaged velocities), which differs from the velocity Verlet on-step value by a term of order $\Delta t^2$.
</details>

<details markdown="1"><summary>4. Your NVE test shows the energy rising linearly, and halving Δt does not change the slope. What do you suspect?</summary>
Not the integrator, whose error scales with $\Delta t^2$. Likely causes: a truncated potential with a jump at the cutoff, a neighbour list updated too rarely (particles enter the cutoff unnoticed), too loose a constraint tolerance, or single-precision arithmetic (the OpenMM developers measured a clear drift in single precision for a system of only 24,000 atoms, which mixed precision removed).
</details>

## Exercises

1. Starting from the 2×2 matrix in the box above, verify that its determinant is 1 and that $\tilde H$ is conserved. Compute its eigenvalues and show they leave the unit circle when $\omega\Delta t>2$.
2. Implement forward Euler, velocity Verlet and RK4 for the pendulum $\ddot\theta = -\sin\theta$ with large amplitude (anharmonic). Plot energy against time for 1,000 periods.
3. In the Python code from Module 1, run with $\Delta t$ = 0.001, 0.002, 0.004 and 0.008. Measure the standard deviation of the total energy and show on a log-log plot that it scales as $\Delta t^2$.
4. Show by a Taylor expansion that $e^{A/2}e^{B}e^{A/2} = e^{A+B+O(3)}$, where the leading error terms are the double commutators $[B,[B,A]]$ and $[A,[A,B]]$.

## Read

{{READ}}

## Key papers

{{PAPERS}}
