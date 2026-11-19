---
num: 9
title: Constraints, freezing the fastest motions
short: Constraints
part: Part II · The engine
hours: 4
summary: Derive constrained dynamics with Lagrange multipliers, understand how SHAKE, RATTLE, SETTLE and LINCS solve it, and know what hydrogen mass repartitioning and virtual sites do to the time step.
videos: 9
papers: C
tags: constraints
---

<div class="box goal" markdown="1">
#### After this module you can

- explain why constraining bonds is physically reasonable and what it buys;
- write the constrained equations of motion and solve them for one bond;
- describe how SHAKE, RATTLE, SETTLE and LINCS differ;
- account for constraints in the temperature and the pressure;
- explain how hydrogen mass repartitioning allows a 4 fs time step.
</div>

## Watch first

{{WATCH}}

## Why constrain

The time step is limited by the fastest vibration (Module 4). Bonds to hydrogen vibrate with a period near 10 fs and force $\Delta t\approx1$ fs. These vibrations:

- are almost decoupled from the slow conformational motions we care about;
- have $\hbar\omega\approx14\,k_BT$, so in reality they sit in their quantum ground state. A rigid bond is arguably a better classical model of a quantum oscillator in its ground state than a classical spring carrying $k_BT$ of energy.

Fixing the bond lengths removes them and allows 2 fs: twice the simulation for the same cost. The usual choices are `h-bonds` (only bonds involving hydrogen), which is the standard for AMBER and CHARMM force fields, and `all-bonds`. Bond *angles* are not usually constrained in proteins, because angle bending is coupled to torsional transitions and freezing it changes barrier heights noticeably. Water is the exception: the common water models are defined as fully rigid.

## Constrained equations of motion

A bond constraint between atoms $i$ and $j$ is a **holonomic constraint**, an equation between coordinates:

$$
\sigma_k(\mathbf r) = |\mathbf r_i-\mathbf r_j|^2 - d_k^2 = 0 .
$$

Following Lagrange (Module 2), add each constraint to the Lagrangian with a multiplier $\lambda_k$. The equations of motion become

$$
m_i\ddot{\mathbf r}_i = \mathbf F_i + \mathbf G_i,\qquad \mathbf G_i = -\sum_k\lambda_k\,\nabla_i\sigma_k .
$$

$\mathbf G_i$ is the **constraint force**. For a bond constraint $\nabla_i\sigma_k = 2\mathbf r_{ij}$, so the constraint force acts along the bond, equal and opposite on the two atoms. It does no work, because the velocity of a constrained system has no component along $\nabla\sigma$. The multipliers $\lambda_k(t)$ are unknowns to be determined at every step so that the constraints hold.

## SHAKE

Ryckaert, Ciccotti and Berendsen (1977). Take a normal, unconstrained Verlet step to positions $\mathbf r'$, then add the displacement caused by the constraint forces, which are evaluated along the bond directions at the *start* of the step:

$$
\mathbf r_i(t+\Delta t) = \mathbf r_i' - \frac{\Delta t^2}{m_i}\sum_k\lambda_k\,\nabla_i\sigma_k\big(\mathbf r(t)\big).
$$

**One constraint, solved explicitly.** Let $\mathbf s = \mathbf r_i(t)-\mathbf r_j(t)$ be the old bond vector (length $d$) and $\mathbf s' = \mathbf r_i'-\mathbf r_j'$ the unconstrained new one. With $g = 2\lambda\Delta t^2$,

$$
\mathbf r_i = \mathbf r_i' - \frac{g}{m_i}\mathbf s,\qquad \mathbf r_j = \mathbf r_j' + \frac{g}{m_j}\mathbf s,
\qquad\text{so the new bond vector is}\quad \mathbf s' - g\left(\frac1{m_i}+\frac1{m_j}\right)\mathbf s .
$$

Requiring its length to be $d$ gives a quadratic equation in $g$:

$$
|\mathbf s'|^2 - 2g\,\mu^{-1}\,\mathbf s\cdot\mathbf s' + g^2\mu^{-2}d^2 = d^2,\qquad \mu^{-1} = \frac1{m_i}+\frac1{m_j}.
$$

Dropping the small $g^2$ term gives the SHAKE update:

$$
\boxed{g \approx \frac{|\mathbf s'|^2-d^2}{2\,\mu^{-1}\;\mathbf s\cdot\mathbf s'}}
$$

**Many constraints.** Atoms share constraints (a CH$_3$ group has three), so the equations are coupled. SHAKE treats them one at a time: apply the single-constraint correction to each in turn, and sweep through the list repeatedly until every bond length is within a relative tolerance (typically $10^{-4}$ to $10^{-8}$) of its target. This is a Gauss-Seidel iteration. It is simple and general, but its sequential nature makes it awkward to parallelise, and convergence slows when many constraints are coupled.

**RATTLE** (Andersen 1983) is the version for velocity Verlet. It also removes the component of the velocities along each bond, enforcing the time derivative of the constraint, $\dot\sigma_k = 2\,\mathbf r_{ij}\cdot\mathbf v_{ij} = 0$, so that positions and velocities are both consistent at each step.

## SETTLE

For a rigid three-site water molecule there are exactly three constraints on three atoms, and the problem can be solved analytically: Miyamoto and Kollman (1992) find the rotated position of the rigid triangle directly. No iteration and no tolerance. Since most atoms in a simulation are water, every major code uses SETTLE or an equivalent for water and a general algorithm for the solute.

## LINCS

Hess, Bekker, Berendsen and Fraaije (1997); the default for non-water constraints in GROMACS. Write all constraints at once in matrix form. With $\mathbf B$ the matrix of normalised bond directions at time $t$ and $\mathbf M$ the diagonal mass matrix, the constrained positions are a projection of the unconstrained ones:

$$
\mathbf r(t+\Delta t) = \mathbf r' - \mathbf M^{-1}\mathbf B^{T}\left(\mathbf B\mathbf M^{-1}\mathbf B^{T}\right)^{-1}\left(\mathbf B\mathbf r' - \mathbf d\right).
$$

The expensive part is inverting the $K\times K$ constraint-coupling matrix $\mathbf B\mathbf M^{-1}\mathbf B^T$. LINCS writes it as $\mathbf S(\mathbf 1-\mathbf A)\mathbf S$ with $\mathbf S$ diagonal, where $\mathbf A$ is sparse and has non-zero entries only for constraints that share an atom, and uses the series

$$
(\mathbf 1-\mathbf A)^{-1} = \mathbf 1+\mathbf A+\mathbf A^2+\mathbf A^3+\dots
$$

truncated after a few terms (`lincs-order = 4`). Because the projection uses the old bond directions, the new bonds come out slightly too long after rotation. A final correction step fixes the length (`lincs-iter = 1`).

LINCS is non-iterative, fast and easy to parallelise (P-LINCS). The series only converges when the eigenvalues of $\mathbf A$ are below 1, which holds for bond constraints in molecules but **not** for coupled angle constraints, so LINCS cannot be used for rigid triangles other than through special handling. When a simulation becomes unstable, the first symptom in GROMACS is usually a "LINCS warning": a bond has rotated by more than 30° in one step. The constraint algorithm is reporting the problem, and is rarely the cause. Look for bad contacts, a time step that is too large, or a system that was not equilibrated.

## Consequences for the statistics

**Degrees of freedom.** Each constraint removes one degree of freedom. The temperature must be computed with

$$
N_{df} = 3N - N_{c} - 3 .
$$

A solvated protein with rigid water loses a third of its degrees of freedom this way. Codes do this for you, but when you thermostat groups separately or analyse a subset of atoms you need the right count for each group.

**Pressure.** Constraint forces contribute to the virial, $\Xi_{c} = -\tfrac12\sum_k\mathbf r_{ij}\cdot\mathbf G_{ij}$. Leaving them out gives a pressure that is wrong by hundreds of bar.

**Distributions.** Rigidly constrained and very stiff flexible systems do not have exactly the same distribution of the remaining coordinates: integrating out the constrained momenta leaves a factor depending on the mass-metric tensor (the Fixman correction). For bond-length constraints the effect is negligible. For constrained angles and dihedrals it is not, another reason these are left free.

## Going beyond 2 fs

After constraining bonds to hydrogen, the fastest remaining motions involve hydrogens: bond-angle vibrations (H-X-H, H-X-Y) and the rotation of hydroxyl and methyl groups, with periods around 20 fs. Two techniques slow them down.

### Hydrogen mass repartitioning (HMR)

Increase the mass of each hydrogen (for example from 1 to 3 or 4 u) and subtract the same amount from the heavy atom it is bonded to. The total mass of every group is unchanged. Frequencies of hydrogen motions fall by $\sqrt{m_H'/m_H}$, a factor of up to 2, which allows $\Delta t$ = 4 fs with bonds to hydrogen constrained.

Why it is legitimate: the equilibrium distribution of positions does not depend on masses (Module 3), so thermodynamics is unchanged. Dynamics are slightly altered, mainly rates that involve the light atoms. Hopkins et al. (2015) validated it for proteins. Water is usually not repartitioned, because it is rigid already and changing its hydrogen masses would change its rotational dynamics and viscosity.

### Virtual sites

Remove the hydrogen degrees of freedom entirely: the hydrogen position is constructed each step from the positions of its heavy-atom neighbours, the force on it is redistributed to those atoms, and its mass is added to them. With all hydrogen motions gone, 4 to 5 fs is possible. The same machinery implements the massless charge sites of four- and five-site water models and the off-centre sites used for lone pairs.

## Check yourself

<details markdown="1"><summary>1. A system has 60,000 atoms: a 3,000-atom protein with 1,500 bonds to hydrogen constrained, and 19,000 rigid three-site water molecules. How many degrees of freedom?</summary>
$3\times60{,}000 = 180{,}000$. Constraints: 1,500 for the protein plus $3\times19{,}000 = 57{,}000$ for water. $N_{df} = 180{,}000 - 58{,}500 - 3 = 121{,}497$.
</details>

<details markdown="1"><summary>2. Why does the constraint force do no work?</summary>
It is parallel to $\nabla\sigma$, and the constraint $\sigma=0$ for all time implies $\dot\sigma = \sum_i\nabla_i\sigma\cdot\mathbf v_i = 0$. The power $\sum_i\mathbf G_i\cdot\mathbf v_i = -\lambda\sum_i\nabla_i\sigma\cdot\mathbf v_i$ is therefore zero.
</details>

<details markdown="1"><summary>3. Does hydrogen mass repartitioning change the free energy difference between two conformations?</summary>
No. Configurational free energies depend only on $U(\mathbf r)$. Only kinetic quantities such as rates and diffusion constants change.
</details>

<details markdown="1"><summary>4. GROMACS prints LINCS warnings and then crashes at step 12 of the first NVT run. What do you do?</summary>
Do not loosen the LINCS settings. Go back: check that energy minimisation converged (maximum force below about 1,000 kJ mol$^{-1}$ nm$^{-1}$), look at the atoms named in the warning for clashes or wrong protonation, check for missing atoms and wrong box size, and try a shorter time step with position restraints for the first picoseconds.
</details>

## Exercises

1. Solve the quadratic equation for $g$ exactly and show that the SHAKE approximation is its first-order expansion. How large is the neglected term for a C-H bond displaced by 1 % in one step?
2. Implement SHAKE for a chain of five atoms with four bond constraints in Python. Plot the number of iterations needed against the tolerance.
3. For a diatomic molecule, simulate the flexible (harmonic) and the rigid (SHAKE) versions and compare the largest stable time step.
4. Compute the new C-H stretch and H-C-H bending periods after repartitioning hydrogens to 3 u (taking the mass from the carbon). Is the bond stretch still the problem if it is constrained?

## Read

{{READ}}

## Key papers

{{PAPERS}}
