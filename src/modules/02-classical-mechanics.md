---
num: 2
title: Classical mechanics for simulators
short: Classical mechanics
part: Part I · Foundations
hours: 6
summary: Go from Newton to Lagrange to Hamilton, and understand phase space, conservation laws, Liouville's theorem and time reversibility, the four properties a good integrator must respect.
videos: 2
tags: classical-mechanics
---

<div class="box goal" markdown="1">
#### After this module you can

- derive energy conservation from Newton's law for a conservative force;
- write the Lagrangian and the Hamiltonian of a system and obtain its equations of motion;
- explain what phase space is and state Liouville's theorem;
- say which quantities an MD simulation in a periodic box conserves and which it does not;
- explain why two trajectories that start almost at the same point separate exponentially, and why MD is still useful.
</div>

## Watch first

{{WATCH}}

## Newton's formulation

<div data-videos="H0BCYDXEDco 031AX4AsueA mYDrufxpW9E"></div>

For $N$ particles, Newton's second law is $m_i \ddot{\mathbf r}_i = \mathbf F_i$. A force is **conservative** if it is the negative gradient of a function of positions only:

$$
\mathbf F_i = -\nabla_i U(\mathbf r_1,\dots,\mathbf r_N).
$$

All force-field forces are of this type. The key consequence is conservation of the total energy $E = K + U$ with $K = \sum_i \tfrac12 m_i \dot{\mathbf r}_i^2$:

$$
\frac{dE}{dt} = \sum_i m_i \dot{\mathbf r}_i\cdot\ddot{\mathbf r}_i + \sum_i \nabla_i U\cdot\dot{\mathbf r}_i
= \sum_i \dot{\mathbf r}_i\cdot\left(\mathbf F_i - \mathbf F_i\right) = 0 .
$$

This is the first test of any MD code: with no thermostat, the total energy must stay constant apart from small fluctuations from the finite time step.

### Forces from a pair potential

Most of $U$ is a sum over pairs, $U=\sum_{i<j} u(r_{ij})$ with $r_{ij} = |\mathbf r_i - \mathbf r_j|$. By the chain rule, using $\partial r_{ij}/\partial \mathbf r_i = \mathbf r_{ij}/r_{ij}$ with $\mathbf r_{ij} = \mathbf r_i - \mathbf r_j$,

$$
\mathbf F_i = -\sum_{j\ne i} \frac{du}{dr}\bigg|_{r_{ij}} \frac{\mathbf r_{ij}}{r_{ij}}, \qquad \mathbf F_{ij} = -\mathbf F_{ji}.
$$

The second relation is Newton's third law. It means each pair is computed once and applied to both atoms, and it guarantees that the total momentum $\mathbf P = \sum_i m_i \dot{\mathbf r}_i$ is conserved.

## Lagrange's formulation

<div data-videos="OpqJjKDPJBA 3apIZCpmdls"></div>

Newton's law is awkward when the natural coordinates are not Cartesian, for example bond lengths, angles and torsions, or when there are constraints. Lagrangian mechanics works in any set of **generalised coordinates** $q_1,\dots,q_n$. Define

$$
L(q,\dot q) = K(q,\dot q) - U(q).
$$

The path the system actually follows between two times makes the action $S=\int L\,dt$ stationary. The condition for that is the Euler-Lagrange equation, one for each coordinate:

$$
\frac{d}{dt}\frac{\partial L}{\partial \dot q_k} - \frac{\partial L}{\partial q_k} = 0 .
$$

For Cartesian coordinates $L = \sum \tfrac12 m\dot x^2 - U$, so $\partial L/\partial\dot x = m\dot x$ and $\partial L/\partial x = -\partial U/\partial x$, and you recover Newton's law.

**Why you need this for MD.** Three later topics are written in Lagrangian language:

- constraints (Module 9) are added to $L$ with Lagrange multipliers;
- the Nosé-Hoover thermostat and the Parrinello-Rahman barostat (Module 8) are "extended Lagrangians", where a thermostat variable or the box itself is given a fictitious mass and a kinetic energy;
- Car-Parrinello ab initio MD does the same for the electronic orbitals.

<div class="box key" markdown="1">
**Worked example: a pendulum.** One coordinate, the angle $\theta$. $K = \tfrac12 m l^2\dot\theta^2$, $U = -mgl\cos\theta$. Euler-Lagrange gives $ml^2\ddot\theta + mgl\sin\theta = 0$. Note that the constraint (fixed length $l$) never appears: choosing a coordinate that respects the constraint removes it. This is the idea behind internal-coordinate MD.
</div>

## Hamilton's formulation

<div data-videos="61CWqyocuOM hk4fOXsSJzM"></div>

Define the **generalised momentum** conjugate to each coordinate, $p_k = \partial L/\partial \dot q_k$, and the Hamiltonian by a Legendre transform:

$$
H(q,p) = \sum_k p_k\dot q_k - L(q,\dot q).
$$

For Cartesian coordinates $p = m\dot x$ and

$$
H(\mathbf r,\mathbf p) = \sum_i \frac{\mathbf p_i^2}{2m_i} + U(\mathbf r) = K + U ,
$$

the total energy. The equations of motion become two first-order equations per degree of freedom:

$$
\dot q_k = \frac{\partial H}{\partial p_k}, \qquad \dot p_k = -\frac{\partial H}{\partial q_k}.
$$

For the Cartesian Hamiltonian these read $\dot{\mathbf r}_i = \mathbf p_i/m_i$ and $\dot{\mathbf p}_i = -\nabla_i U = \mathbf F_i$: the "drift" and the "kick" of the velocity Verlet algorithm. The Hamiltonian form is the one used by statistical mechanics (Module 3) and by the theory of integrators (Module 4).

### Phase space

<div data-videos="IVQRfHAgLxk yV25sV3rAlo"></div>

The state of the system at one instant is the full set of positions and momenta, a single point $\Gamma = (\mathbf r_1,\dots,\mathbf r_N,\mathbf p_1,\dots,\mathbf p_N)$ in a $6N$-dimensional space called **phase space**. A trajectory is a curve in phase space. Because Hamilton's equations are first order, one curve passes through each point: trajectories never cross. For a one-dimensional harmonic oscillator the trajectory is an ellipse in the $(x,p)$ plane, and its area is $2\pi E/\omega$.

### Time evolution of any observable

<div data-videos="5OZO5GPuSJY"></div>

For a function $A(q,p)$ with no explicit time dependence,

$$
\frac{dA}{dt} = \sum_k\left(\frac{\partial A}{\partial q_k}\dot q_k + \frac{\partial A}{\partial p_k}\dot p_k\right)
= \sum_k\left(\frac{\partial A}{\partial q_k}\frac{\partial H}{\partial p_k} - \frac{\partial A}{\partial p_k}\frac{\partial H}{\partial q_k}\right) \equiv \{A,H\}.
$$

The bracket $\{A,H\}$ is the Poisson bracket. It is convenient to define the **Liouville operator** $iL$ by $iL\,A = \{A,H\}$, so that $\dot A = iL\,A$ with the formal solution

$$
A(t) = e^{iLt}A(0).
$$

For the Cartesian Hamiltonian,

$$
iL = \underbrace{\sum_i \frac{\mathbf p_i}{m_i}\cdot\frac{\partial}{\partial \mathbf r_i}}_{iL_r} + \underbrace{\sum_i \mathbf F_i\cdot\frac{\partial}{\partial \mathbf p_i}}_{iL_p}.
$$

Keep this splitting in mind. In Module 4 the velocity Verlet algorithm falls out of it in two lines.

## Conservation laws

<div data-videos="HLr5ZeQUrBk PuDproV-17s ojEwHlyty4Q"></div>

A quantity $A$ is conserved when $\{A,H\}=0$. Each conservation law comes from a symmetry of $H$ (Noether's theorem):

| Symmetry of $H$ | Conserved quantity | In an MD simulation |
|---|---|---|
| No explicit time dependence | Energy $H$ | Conserved in NVE up to integration error. Not conserved with a thermostat (but an extended energy often is). |
| Translation of all particles | Total linear momentum $\mathbf P$ | Conserved with periodic boundaries. Codes set it to zero at the start and remove any numerical drift ("centre-of-mass motion removal"). |
| Rotation of all particles | Total angular momentum $\mathbf L$ | **Not** conserved with periodic boundaries, because a cubic box is not rotationally symmetric. Conserved in vacuum or droplet simulations. |

The number of conserved quantities affects the number of degrees of freedom used to compute the temperature (Module 3): $3N - 3$ in a periodic box with no constraints.

## Liouville's theorem

<div data-videos="MFqA1nePCNg ddKRdrf9iqI XiFEXVWNlpg 8w4az6IQsNc lQIbcV6dQzw"></div>

Consider not one system but a cloud of systems with slightly different initial conditions, described by a density $\rho(\Gamma,t)$ in phase space. The cloud moves with "velocity" $\dot\Gamma = (\dot q,\dot p)$. The divergence of this velocity field is

$$
\nabla_\Gamma\cdot\dot\Gamma = \sum_k \left(\frac{\partial \dot q_k}{\partial q_k} + \frac{\partial \dot p_k}{\partial p_k}\right)
= \sum_k \left(\frac{\partial^2 H}{\partial q_k\partial p_k} - \frac{\partial^2 H}{\partial p_k\partial q_k}\right) = 0 .
$$

The flow in phase space is **incompressible**. A blob of initial conditions changes shape, often into something very stretched and folded, but its volume stays the same. Combining this with conservation of the number of systems gives the Liouville equation

$$
\frac{\partial\rho}{\partial t} = -\{\rho,H\} = -iL\rho, \qquad\text{equivalently}\qquad \frac{d\rho}{dt}=0 \text{ along a trajectory.}
$$

Two consequences matter for simulation:

1. **Any density that depends on $\Gamma$ only through $H$ is stationary**, since then $\{\rho(H),H\}=0$. The microcanonical density $\delta(H-E)$ and the canonical density $e^{-\beta H}$ are both of this kind. This is why Hamiltonian dynamics is compatible with the equilibrium ensembles.
2. **A good integrator should also preserve the Hamiltonian structure of phase space.** Integrators that do are called symplectic. They preserve phase-space volume, and they preserve more than that (the sum of the oriented areas $dq_k\,dp_k$), and it is this stronger property that gives them a conserved "shadow" energy (Module 4). Integrators without it (for example forward Euler or the classical explicit Runge-Kutta methods) make the cloud grow or shrink steadily, which shows up as an energy drift.

<div class="widget" data-widget="liouville"></div>

## Time reversibility

<div data-videos="sg15UClUY48"></div>

Hamilton's equations are symmetric under $t\to -t$, $\mathbf p \to -\mathbf p$. If you stop a simulation, flip all velocities and continue, an exact solution retraces its path. Velocity Verlet has the same symmetry in exact arithmetic. In practice round-off error and chaos destroy the retracing after a few hundred steps, but the symmetry of the algorithm still protects it from systematic drift. It also matters for Monte Carlo schemes that use MD moves (hybrid Monte Carlo), which need a reversible, volume-preserving integrator to satisfy detailed balance.

## Small oscillations and normal modes

Near a minimum $\mathbf r_0$, expand $U$ to second order:

$$
U(\mathbf r) \approx U(\mathbf r_0) + \tfrac12 \sum_{ab} H_{ab}\,\Delta r_a \Delta r_b,\qquad H_{ab} = \frac{\partial^2 U}{\partial r_a\partial r_b}\bigg|_{\mathbf r_0}.
$$

$H_{ab}$ is the Hessian (not the Hamiltonian). In mass-weighted coordinates $\tilde r_a = \sqrt{m_a}\,\Delta r_a$, the equations of motion are $\ddot{\tilde{\mathbf r}} = -\tilde{\mathbf H}\tilde{\mathbf r}$ with $\tilde H_{ab} = H_{ab}/\sqrt{m_a m_b}$. Diagonalising $\tilde{\mathbf H}$ gives eigenvalues $\omega_k^2$ and eigenvectors, the **normal modes**: independent harmonic oscillators with frequency $\omega_k$.

Why this matters here:

- the highest $\omega_k$ sets the largest stable time step (Module 4): for one harmonic bond between masses $m_1$ and $m_2$, $\omega = \sqrt{k/\mu}$ with reduced mass $\mu = m_1m_2/(m_1+m_2)$. A light hydrogen gives a small $\mu$ and a high frequency;
- the lowest-frequency modes are the collective motions, and normal-mode analysis and elastic network models use them directly;
- the harmonic approximation gives a formula for vibrational entropy that is used in some end-point free-energy methods.

<div class="box key" markdown="1">
**Worked example: the period of a C-H stretch.** With $k \approx 2.8\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ (a typical force-field value in the convention $U=\tfrac12 k(r-r_0)^2$) and $\mu = 12\times1/13 = 0.923$ u, the angular frequency is $\omega = \sqrt{k/\mu} = \sqrt{2.8\times10^5/0.923}\ \text{ps}^{-1} \approx 551\ \text{ps}^{-1}$. The period is $2\pi/\omega \approx 0.0114$ ps $= 11.4$ fs. Ten steps per period means a time step near 1 fs.
</div>

## Chaos, and why MD still works

Many-particle systems are chaotic: two trajectories that start a tiny distance $\delta_0$ apart separate as $\delta(t)\approx\delta_0 e^{\lambda t}$, where $\lambda$ is the largest Lyapunov exponent. For a liquid, $1/\lambda$ is of the order of a picosecond. Round-off error at the 16th digit therefore grows to order one within a few tens of picoseconds. Two consequences:

- A simulated trajectory is **not** the true trajectory from those initial conditions beyond a few picoseconds. Running the same input on two machines, or on a different number of processors, gives different trajectories.
- This does not matter for what MD is used for. We want statistical properties, and a numerical trajectory stays close to *some* true trajectory of a slightly modified Hamiltonian (the "shadow" Hamiltonian of Module 4). Averages over long trajectories are reproducible even though individual trajectories are not.

In practice, chaos is useful: starting copies of a system with different random velocities gives runs whose fast motions are statistically independent within a short time. Copies started from the same structure still share its conformational basin, so for slow motions independent runs should also start from different structures.

## Check yourself

<details markdown="1"><summary>1. Show that the total momentum is conserved when all forces are pair forces.</summary>
$\dot{\mathbf P} = \sum_i \mathbf F_i = \sum_i\sum_{j\ne i}\mathbf F_{ij}$. Each pair appears twice, as $\mathbf F_{ij}$ and $\mathbf F_{ji} = -\mathbf F_{ij}$, so the sum is zero.
</details>

<details markdown="1"><summary>2. Write Hamilton's equations for the one-dimensional harmonic oscillator and solve them.</summary>
$H = p^2/2m + \tfrac12 m\omega^2x^2$. $\dot x = p/m$, $\dot p = -m\omega^2 x$. So $\ddot x = -\omega^2x$ and $x(t) = x_0\cos\omega t + (p_0/m\omega)\sin\omega t$, $p(t) = p_0\cos\omega t - m\omega x_0\sin\omega t$. In the $(x,p)$ plane this is an ellipse traversed clockwise.
</details>

<details markdown="1"><summary>3. Why is angular momentum not conserved in a periodic box?</summary>
Conservation of angular momentum follows from invariance under rotation. A periodic lattice of cubic boxes is invariant only under a few discrete rotations. Equivalently, when a particle leaves through one face and re-enters through the opposite one, its position vector jumps while its momentum does not, so $\mathbf r\times\mathbf p$ jumps.
</details>

<details markdown="1"><summary>4. A friction force $-\gamma \mathbf p$ is added to $\dot{\mathbf p}$. What happens to phase-space volume?</summary>
The divergence becomes $\sum_k \partial(-\gamma p_k)/\partial p_k = -n\gamma$ for $n$ degrees of freedom, so volume contracts as $e^{-n\gamma t}$. Friction alone cools the system to zero temperature. A thermostat must add something that compensates: random kicks in Langevin dynamics, or a friction coefficient that changes sign in Nosé-Hoover dynamics (Module 8).
</details>

## Exercises

1. Derive the equations of motion of two atoms connected by a harmonic bond using the Lagrangian in centre-of-mass and relative coordinates. Show that the relative motion is an oscillator with the reduced mass.
2. For the double pendulum, write the Lagrangian. (You do not need to solve it.) Simulate it numerically with any integrator and plot the distance between two runs whose initial angles differ by $10^{-9}$ radians, on a logarithmic axis. Estimate the Lyapunov exponent from the slope.
3. Build the mass-weighted Hessian of a linear triatomic molecule with two equal springs (a model of CO$_2$ in one dimension) and find its three normal modes. Which one has zero frequency, and why?
4. Prove that $\{H,H\}=0$ and that $\{\rho(H),H\}=0$ for any differentiable function $\rho$.

## Read

{{READ}}
