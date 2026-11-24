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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

An MD program moves the atoms forward in small jumps of time. The length of one jump, the time step, is set by the fastest motion in the system. In a biomolecule the fastest motion is the vibration of the bonds to hydrogen, and it tells you nothing about folding, binding or any other slow process. This module is about removing it. Each of these bonds is replaced by a rigid rod of fixed length, and the time step can then be doubled.

The idea fits in one sentence. The work is in carrying it out inside an integrator, because the force field has no formula for the force of a rod. The program has to find, at every step, the forces that the rods exert on the atoms, from the single requirement that the bond lengths stay fixed.

The module has five layers:

1. **Why.** Why bonds to hydrogen limit the time step, and why freezing them is acceptable physics.
2. **The theory.** A constraint as an equation that the positions must satisfy, the force that enforces it, and the Lagrange multiplier, which is the unknown strength of that force.
3. **The algorithms.** SHAKE and RATTLE correct one bond at a time and repeat. SETTLE is an exact formula for water. LINCS treats all bonds at once with matrices.
4. **The consequences.** What constraints do to the temperature, the pressure and the probabilities that a simulation reports.
5. **Beyond 2 fs.** Heavier hydrogens and virtual sites.

The matrix part of LINCS is the heaviest. On a first reading, the one-bond version at the start of that section is enough, and the matrices can wait.

### How to read the formulas

Every displayed formula in this module is followed by a list that says what each letter in it means. The notation in the table first appears in this module. The general conventions (bold letters for vectors, dots for time derivatives, the sum sign) are explained in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\mathbf r_{ij}$ | The vector that points from atom $j$ to atom $i$, $\mathbf r_i-\mathbf r_j$. For two bonded atoms it is the **bond vector**, and its length is the bond length. |
| $\vert\mathbf a\vert$, $\vert\mathbf a\vert^2$ | The length of the vector $\mathbf a$, and that length squared, $a_x^2+a_y^2+a_z^2$. |
| $\mathbf r'$, $\mathbf s'$ | A prime marks a position or a bond vector after a step taken without the constraints, before it has been corrected. In this module a prime is never a derivative. |
| $\hat{\mathbf s}$ | A hat marks a **unit vector**: a vector of length 1, which only gives a direction. |
| $\sigma_k$ | The constraint function of constraint number $k$. It is zero when bond $k$ has its target length. |
| $\Delta t$ | The time step, the amount of time by which the simulation advances in one step. |
| $\mathbf B$, $\mathbf M$, $\mathbf A$, $\mathbf S$ | A bold capital letter is a **matrix**, a rectangular table of numbers. |
| $\mathbf B^T$ | The **transpose** of $\mathbf B$: the same table with rows and columns exchanged. |
| $\mathbf M^{-1}$ | The **inverse** of $\mathbf M$: the matrix that undoes what $\mathbf M$ does. |
| $\mathbf 1$ | The **identity matrix**, with ones on the diagonal and zeros elsewhere. Multiplying by it changes nothing. |

<div class="box warn" markdown="1">
**Letters that mean two things.** $\sigma$ is the constraint function here. In Module 5 it is a length in the Lennard-Jones potential, and in statistics it is a standard deviation. $\lambda$ is the Lagrange multiplier here, the Lyapunov exponent in Module 2 and the coupling parameter in Module 13. $k$ is the number of a constraint, not a spring constant. $d$ is a bond length ($d_k$ for bond $k$, and $\mathbf d$ for the list of all of them), not the $d$ of a derivative such as $d/dt$. $K$ is the number of constraints in the LINCS section and the kinetic energy in the sections on temperature and pressure. A superscript $T$ on a matrix means "transpose", while $T$ on its own is the temperature. Small $\mathbf s$ is a bond vector and capital $\mathbf S$ is a matrix. $p$ is the target for a projection in the LINCS section, while bold $\mathbf p_i$ is a momentum in the section on hydrogen mass repartitioning. $l$ is the length of a bond, except in "entry $(k,l)$" of a matrix, where it is the number of a second constraint.
</div>

## Why constrain

A simulation advances in jumps of time. The length of one jump is the **time step**, $\Delta t$, measured in femtoseconds (1 fs is $10^{-15}$ s, or 0.001 ps). One step costs about the same computer time whatever its length, because nearly all of the cost is the calculation of the forces. A longer time step therefore gives more simulated time for the same cost.

The limit comes from the fastest vibration in the system. [Module 4](04-integrators.html) shows that the integrator becomes unstable, with an energy that grows without bound, when $\Delta t$ is longer than about a third of the period of that vibration, and that in practice one uses 10 to 20 steps per period. So to know how long the time step can be, you have to know which motion is the fastest.

For two atoms joined by a bond that behaves like a spring, [Module 2](02-classical-mechanics.html) gave the angular frequency $\omega = \sqrt{k_b/\mu}$. Here $k_b$ is the stiffness of the spring and $\mu = m_1m_2/(m_1+m_2)$ is the reduced mass of the two atoms. It is always smaller than the lighter of the two masses, and close to it when the other atom is much heavier. The period of one oscillation is $2\pi/\omega$.

A stiff spring and a light atom both make the vibration fast. Covalent bonds are the stiffest springs in a force field and hydrogen is the lightest atom, so bonds to hydrogen are the fastest motion in a biomolecule. The worked example of Module 2 found a period of 11.4 fs for a C-H bond.

The time step is limited by the fastest vibration (Module 4). Bonds to hydrogen vibrate with a period near 10 fs and force $\Delta t\approx1$ fs. These vibrations:

- are almost decoupled from the slow conformational motions we care about;
- have $\hbar\omega\approx14\,k_BT$, so in reality they sit in their quantum ground state. A rigid bond is arguably a better classical model of a quantum oscillator in its ground state than a classical spring carrying $k_BT$ of energy.

These two points are the reason why freezing the bonds is acceptable physics, so each gets a closer look.

**Decoupled.** Two motions are coupled when energy passes easily from one to the other. That happens when their rhythms are similar, in the way that a child's swing only gains height when you push in time with it. A bond to hydrogen completes almost ninety oscillations in one picosecond (1000 fs divided by 11.4 fs), while a change of conformation takes from picoseconds to far longer. The slow motion feels only the average length of the bond. The average of a small, fast oscillation is very nearly a fixed length, which is what a rod has.

**In the quantum ground state.** This point needs one idea from quantum mechanics.

<div class="box physics" markdown="1">
**Physics you need here: the energy levels of a quantum oscillator.** A classical spring can hold any amount of energy. A quantum oscillator can hold only certain amounts, which form a ladder of **energy levels** with equal spacing $\hbar\omega$. Here $\omega$ is the angular frequency of the vibration and $\hbar$ (read "h-bar") is the reduced Planck constant, 0.0635 kJ mol$^{-1}$ ps in MD units. The lowest level is called the **ground state**.

Whether the higher levels are ever reached depends on how $\hbar\omega$ compares with the thermal energy $k_BT$, which is 2.494 kJ/mol at 300 K ($k_B$ is the Boltzmann constant and $T$ the temperature, Module 3). For the C-H bond of Module 2, $\omega = 551$ ps$^{-1}$, so $\hbar\omega = 0.0635\times551 = 35.0$ kJ/mol, which is $35.0/2.494 = 14$ times $k_BT$. The first step of the ladder is 14 times higher than a typical thermal push. The chance of finding the bond one level up, compared with finding it in the ground state, is the Boltzmann factor $e^{-14}\approx 8\times10^{-7}$: less than one in a million.

So a real bond to hydrogen stays in its ground state at room temperature. It does not take up heat and does not give any back. More in the primer, on [why atoms can be treated as classical balls](physics.html#quantum) and on [the harmonic oscillator](physics.html#oscillator).
</div>

A classical spring behaves differently. By the equipartition rule of Module 3 it holds on average $\tfrac12k_BT$ of kinetic energy and $\tfrac12k_BT$ of potential energy, $k_BT$ in total, and it trades this energy with its surroundings all the time. That is the "classical spring carrying $k_BT$ of energy" of the list above, and the real bond does not do this.

A rigid rod holds no vibrational energy and exchanges none. In this respect the rod is closer to the real bond than the spring is. Neither model is exact, which is why the text says "arguably": the real ground state has a small spread of bond lengths, and the rod ignores it.

So the vibrations of the bonds to hydrogen can be given up. Fixing the bond lengths removes them and allows 2 fs: twice the simulation for the same cost. With the bonds to hydrogen rigid, the fastest motions that are left have periods around 20 fs (the last section of this module says which they are), and ten steps per period gives 2 fs.

The usual choices are `h-bonds` (only bonds involving hydrogen), which is the standard for AMBER and CHARMM force fields, and `all-bonds`. These two words are values of the constraint setting in the input file of an MD program. The spelling differs between programs: the GROMACS input file of Module 10 contains the line `constraints = h-bonds`. `all-bonds` makes every covalent bond rigid, including those between two heavy atoms. One warning about the first name: `h-bonds` here means covalent bonds in which one of the two atoms is a hydrogen, such as C-H, N-H and O-H. It does not mean hydrogen bonds, the weak attractions between molecules, which are never constrained.

Bond *angles* are not usually constrained in proteins, because angle bending is coupled to torsional transitions and freezing it changes barrier heights noticeably. A torsional transition is a rotation about a bond that takes a molecule from one stable arrangement to another. During the rotation, atoms pass close to each other, and the bond angles open a little to make room. If the angles are frozen they cannot give way, the atoms are squeezed harder, and the energy barrier of the rotation is higher than it should be. A higher barrier means fewer transitions, so frozen angles would change the slow motions, which are the ones the simulation is run for.

Water is the exception: the common water models are defined as fully rigid. "Fully rigid" means that the two O-H bond lengths and the H-O-H angle are all fixed. The angle is fixed by a third distance constraint, between the two hydrogens: a triangle with three fixed sides cannot change its shape. For water you do not choose whether to constrain. A rigid water model is rigid by definition (Module 6).

### Constraint or restraint

The two words sound alike and mean different things.

- A **constraint** is a condition that holds exactly at every step: "this bond has length $d$". There is no energy term for it. The constrained quantity cannot fluctuate, and one way in which the molecule could move is gone.
- A **restraint** is an extra term in the potential energy, usually a spring such as $\tfrac12 k_r(x-x_0)^2$, that makes deviations cost energy. Here $x$ is the restrained quantity, $x_0$ its reference value and $k_r$ the stiffness you chose. The quantity still fluctuates around $x_0$, and nothing is removed from the system.

The position restraints that hold a protein in place during equilibration (Module 10) are restraints. The rigid bonds of this module are constraints.

For the time step the difference is large. A restraint is a spring, and a stiffer spring vibrates faster ($\omega = \sqrt{k_b/\mu}$ again). Making a restraint ten times stiffer shortens its period by a factor $\sqrt{10}\approx3.2$, so a very stiff restraint forces a *shorter* time step. A constraint has no vibration at all.

## Constrained equations of motion

<div data-videos="N2Lf-U8aIgM -6QUI57indo"></div>

This section answers one question: how do the atoms move when some of the distances between them are fixed? The picture to keep in mind is two atoms joined by a rigid rod that has no mass. Each atom feels the ordinary forces of the force field. In addition, the rod pulls or pushes on both atoms along its own direction, with whatever strength is needed to keep them at the right distance.

That last phrase is the difficulty. The force of a spring is given by a formula: stiffness times stretch. The force of a rod is given by no formula. It is whatever it has to be. The theory below shows in which direction this force points, gives its strength a name ($\lambda$), and leaves that strength as an unknown to be solved for.

First the condition has to be written as an equation. A bond constraint between atoms $i$ and $j$ is a **holonomic constraint**, an equation between coordinates:

$$
\sigma_k(\mathbf r) = |\mathbf r_i-\mathbf r_j|^2 - d_k^2 = 0 .
$$

<div class="legend" markdown="1">
- $k$: the number of the constraint. A system has one such equation for every rigid bond.
- $\sigma_k$: the **constraint function** of bond $k$, in nm$^2$. This $\sigma$ is not the Lennard-Jones length of Module 5.
- $\mathbf r$: the positions of all atoms together. The brackets say that $\sigma_k$ depends on positions only.
- $\mathbf r_i$, $\mathbf r_j$: the positions of the two atoms joined by bond $k$.
- $|\mathbf r_i-\mathbf r_j|^2$: the squared distance between the two atoms. The bars mean "length of the vector".
- $d_k$: the length that bond $k$ must have, a constant taken from the force field, in nm.
- $= 0$: the condition itself. The constraint is satisfied when the function is zero.
</div>

Read it like this. $\sigma_k$ measures the error of bond $k$. It is zero when the bond has the right length, positive when the bond is too long and negative when it is too short. With $d_k = 0.1$ nm, a bond stretched to 0.101 nm has $\sigma_k = 0.101^2 - 0.1^2 = 0.000201$ nm$^2$.

The squares are there for convenience. The condition "distance equals $d_k$" and the condition "squared distance equals $d_k^2$" say the same thing, but the squared distance, $(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2$, has no square root in it and is easier to differentiate.

"Holonomic" is the name for a constraint that can be written in this way, as a function of the positions set equal to zero. No velocity appears in it. Every constraint in this module is of this kind.

### The Lagrange multiplier

The rod has to be turned into a force that can be put into Newton's law. The tool for that is the Lagrange multiplier. It is a general piece of mathematics, so it is introduced first on a small example that has nothing to do with atoms.

<div class="box maths" markdown="1">
**Maths you need here: the Lagrange multiplier.** The tool answers this kind of question: find the smallest (or largest) value of a function when its variables must satisfy a condition.

A small example. Among all points $(x, y)$ on the straight line $x + y = 2$, which one is closest to the origin? The quantity to make small is the squared distance to the origin, $f = x^2 + y^2$. The condition is $c = x + y - 2 = 0$.

The reasoning is geometric. Walk along the line. As long as $f$ still changes when you take a small step along the line, you are not yet at the closest point. At the closest point a small step along the line does not change $f$.

So the gradient of $f$ (the direction in which $f$ rises fastest) has no part along the line: it is perpendicular to the line. The gradient of $c$ is also perpendicular to the line, because $c$ stays zero all along it. Two vectors in a plane that are perpendicular to the same line are parallel, so one is a multiple of the other:

$$
\nabla f = \lambda\,\nabla c .
$$

The number $\lambda$ is the **Lagrange multiplier**. It is not known in advance. Here $\nabla f = (2x, 2y)$ and $\nabla c = (1, 1)$, so $2x = \lambda$ and $2y = \lambda$, which gives $x = y = \lambda/2$. Now use the condition to find $\lambda$: $x + y = \lambda/2 + \lambda/2 = \lambda$ must equal 2. So $\lambda = 2$, and the closest point is $(1, 1)$.

The pattern to remember: a condition contributes a term "unknown number times the gradient of the condition", and the unknown number is found at the end by demanding that the condition holds. More in the [toolbox](maths.html#lagrange-multipliers).
</div>

The mechanical version follows the same pattern. A rod can act only in the direction in which its constraint function changes, which is the gradient of $\sigma_k$. How strongly it acts is an unknown number $\lambda_k$, found by demanding that the constraint holds.

Following Lagrange (Module 2), add each constraint to the Lagrangian with a multiplier $\lambda_k$. In Module 2 the Lagrangian was $L = K - U$, kinetic minus potential energy, and the Euler-Lagrange equation turned it into Newton's law. With constraints the Lagrangian gets one more term for each constraint:

$$
L_c = \sum_i \tfrac12 m_i\dot{\mathbf r}_i^2 - U(\mathbf r) - \sum_k \lambda_k\,\sigma_k(\mathbf r) .
$$

<div class="legend" markdown="1">
- $L_c$: the Lagrangian of the constrained system. The subscript c stands for "constrained".
- $\sum_i \tfrac12 m_i\dot{\mathbf r}_i^2$: the kinetic energy $K$, summed over all atoms $i$. $m_i$ is the mass of atom $i$ and $\dot{\mathbf r}_i$ its velocity.
- $U(\mathbf r)$: the potential energy of the force field.
- $\sum_k$: a sum over all constraints.
- $\lambda_k$: the multiplier of constraint $k$, an unknown number that can be different at every instant.
- $\sigma_k(\mathbf r)$: the constraint function of bond $k$, as defined above.
</div>

Every $\sigma_k$ is zero when the constraints hold, so the new term has the value zero and does not change the energy. Its slope is what matters. The Euler-Lagrange equation of Module 2, written for the position of atom $i$, compares two derivatives of $L_c$:

1. The derivative with respect to the velocity $\dot{\mathbf r}_i$ is the momentum $m_i\dot{\mathbf r}_i$. Its rate of change in time is $m_i\ddot{\mathbf r}_i$, mass times acceleration.
2. The derivative with respect to the position $\mathbf r_i$ is $-\nabla_iU - \sum_k\lambda_k\nabla_i\sigma_k$. The first part, $-\nabla_iU$, is the ordinary force $\mathbf F_i$.

The Euler-Lagrange equation says that the two are equal. The equations of motion become

$$
m_i\ddot{\mathbf r}_i = \mathbf F_i + \mathbf G_i,\qquad \mathbf G_i = -\sum_k\lambda_k\,\nabla_i\sigma_k .
$$

<div class="legend" markdown="1">
- $m_i$: the mass of atom $i$, in u.
- $\ddot{\mathbf r}_i$: the acceleration of atom $i$.
- $\mathbf F_i$: the force on atom $i$ from the force field, $-\nabla_iU$. It contains everything that is not a constraint: angles, torsions, Lennard-Jones and Coulomb forces, and the bonds that were left flexible.
- $\mathbf G_i$: the constraint force on atom $i$, the sum of the forces of all rods attached to it.
- $\lambda_k$: the Lagrange multiplier of constraint $k$. It sets how strongly rod $k$ acts. One number per constraint, unknown, and different at every instant.
- $\nabla_i\sigma_k$: the gradient of constraint function $k$ with respect to the position of atom $i$ (the gradient is explained in the [toolbox](maths.html#gradient)). It gives the direction in which rod $k$ acts on atom $i$, and it is zero if atom $i$ is not one of the two atoms of bond $k$.
- $\sum_k$: a sum over all constraints. Only the rods attached to atom $i$ contribute.
- The minus sign: a convention. It decides what a positive $\lambda_k$ means, as shown below.
</div>

Read it like this. The first equation is Newton's law with one more force on the right. The second says what that force is made of: for each rod, a known direction ($\nabla_i\sigma_k$) times an unknown strength ($\lambda_k$).

### The constraint force for a bond

$\mathbf G_i$ is the **constraint force**. For a bond constraint $\nabla_i\sigma_k = 2\mathbf r_{ij}$, so the constraint force acts along the bond, equal and opposite on the two atoms.

To see where the $2\mathbf r_{ij}$ comes from, write the constraint function in components:

$$
\sigma_k = (x_i-x_j)^2 + (y_i-y_j)^2 + (z_i-z_j)^2 - d_k^2 .
$$

<div class="legend" markdown="1">
- $x_i$, $y_i$, $z_i$: the three coordinates of atom $i$. The same with $j$ for atom $j$.
- $d_k$: the target length of bond $k$, a constant.
- $\sigma_k$: the constraint function of bond $k$.
</div>

Differentiate with respect to $x_i$ and hold everything else fixed (a partial derivative). Only the first bracket contains $x_i$, and the rule for the derivative of a square gives $\partial\sigma_k/\partial x_i = 2(x_i-x_j)$. The same holds for $y_i$ and $z_i$.

Collected into one vector, the gradient is $\nabla_i\sigma_k = 2(\mathbf r_i-\mathbf r_j) = 2\mathbf r_{ij}$. For atom $j$ the bracket contains $-x_j$, which adds a minus sign: $\nabla_j\sigma_k = -2\mathbf r_{ij}$. Put both into the definition of $\mathbf G$:

$$
\mathbf G_i = -2\lambda_k\,\mathbf r_{ij},\qquad \mathbf G_j = +2\lambda_k\,\mathbf r_{ij} .
$$

<div class="legend" markdown="1">
- $\mathbf G_i$, $\mathbf G_j$: the forces that rod $k$ exerts on atom $i$ and on atom $j$, in kJ mol$^{-1}$ nm$^{-1}$.
- $\mathbf r_{ij} = \mathbf r_i-\mathbf r_j$: the bond vector, pointing from atom $j$ to atom $i$.
- $\lambda_k$: the multiplier of this bond.
</div>

Read it like this:

- **Direction.** Both forces lie along the bond vector. A rod cannot push sideways.
- **Equal and opposite.** The two forces add up to zero. The rod cannot move the molecule as a whole, and the total momentum is conserved (Newton's third law, Module 2).
- **The sign of $\lambda_k$.** If $\lambda_k$ is positive, the force on atom $i$ points along $-\mathbf r_{ij}$, from $i$ towards $j$. The rod pulls the two atoms together, as it must when they try to fly apart. If $\lambda_k$ is negative, the rod pushes them apart.
- **The unit of $\lambda_k$.** A force is $\lambda_k$ times a length, so $\lambda_k$ has the unit kJ mol$^{-1}$ nm$^{-2}$, the unit of a spring constant. It is not a property of the bond, though. It changes from one instant to the next.

Now back to the constraint force $\mathbf G_i$. It does no work, because the velocity of a constrained system has no component along $\nabla\sigma$. "Work" is the energy that a force gives to an object, and the rate at which a force $\mathbf G$ gives energy to an atom with velocity $\mathbf v$ is the dot product $\mathbf G\cdot\mathbf v$. Only the part of the velocity along the force counts.

Here is the argument for one bond. The bond length is constant, so its square, $\mathbf r_{ij}\cdot\mathbf r_{ij}$, is constant and its time derivative is zero. By the product rule that derivative is $2\,\mathbf r_{ij}\cdot\mathbf v_{ij}$, where $\mathbf v_{ij} = \mathbf v_i-\mathbf v_j$ is the velocity of atom $i$ relative to atom $j$. A dot product of zero means that the two vectors are perpendicular. The two atoms can circle around each other, but they cannot approach or separate.

The rate at which the rod gives energy to the pair is then

$$
\mathbf G_i\cdot\mathbf v_i + \mathbf G_j\cdot\mathbf v_j = -2\lambda_k\,\mathbf r_{ij}\cdot(\mathbf v_i-\mathbf v_j) = -2\lambda_k\,\mathbf r_{ij}\cdot\mathbf v_{ij} = 0 .
$$

<div class="legend" markdown="1">
- $\mathbf v_i$, $\mathbf v_j$: the velocities of the two atoms.
- $\mathbf v_{ij}$: their relative velocity, $\mathbf v_i-\mathbf v_j$.
- $\cdot$: the [dot product](maths.html#dot-product). It is zero for perpendicular vectors.
- Other symbols: as in the list above.
</div>

The rod acts like the string of a ball that is whirled in a circle. The string pulls towards the centre and the ball moves sideways, so the string changes the direction of the motion without adding energy. This is why a simulation with constraints still conserves the total energy.

The multipliers $\lambda_k(t)$ are unknowns to be determined at every step so that the constraints hold. One case can be done by hand, and it shows what kind of number $\lambda$ is.

<div class="box key" markdown="1">
**Worked example: the pull of a rod on a spinning pair.** Two atoms of mass $m = 12$ u are joined by a rod of length $d = 0.15$ nm. No other force acts. The pair spins about its centre, and each atom has a speed $v = 0.5$ nm/ps. (Round values for illustration. The thermal speed of a carbon atom along one direction at 300 K is $\sqrt{k_BT/m} = 0.46$ nm/ps.)

1. Each atom moves on a circle of radius $R = d/2 = 0.075$ nm.
2. An object that moves on a circle needs a force $mv^2/R$ towards the centre, or it would fly off along a straight line. Here that is $12\times0.5^2/0.075 = 40$ kJ mol$^{-1}$ nm$^{-1}$.
3. Only the rod can supply this force. The size of the constraint force is $2\lambda d$, from $\mathbf G_i = -2\lambda\,\mathbf r_{ij}$ with $|\mathbf r_{ij}| = d$.
4. So $2\lambda\times0.15 = 40$, which gives $\lambda = 133$ kJ mol$^{-1}$ nm$^{-2}$. It is positive: the rod pulls inward.

Nobody chose this $\lambda$. It came out of the motion. If the pair spins twice as fast, the force and $\lambda$ are four times larger. If it does not spin, $\lambda$ is zero. In a real molecule the other forces also pull on the atoms, the motion is not a circle, and $\lambda$ has to be found numerically at every step.
</div>

Counting shows that the problem can be solved. A system with $K$ constraints has $K$ unknown multipliers and $K$ equations $\sigma_k = 0$, as many equations as unknowns. The algorithms in the next sections differ only in how they solve these equations.

They share one decision. They do not try to follow the exact $\lambda_k(t)$ of the continuous motion. At each time step they choose the values that make every constraint hold at the *end* of that step, exactly or to within a chosen accuracy. Errors then cannot build up over many steps, because each step starts from bonds of the correct length.

## SHAKE

<div data-videos="9Vj7h1TJePw --zH0AJjVqk _zwgPkBeO_I"></div>

SHAKE solves the problem in the most direct way. First ignore the rods and move the atoms with the ordinary forces. The bonds now have slightly wrong lengths. Then move the two atoms of each bond towards each other or apart, along the direction that the bond had at the start of the step, until the length is right again. The second move is the effect of the constraint force, and finding how far to move is the same as finding $\lambda$.

For the first move, recall the Verlet step of Module 4:

$$
\mathbf r_i(t+\Delta t) = 2\,\mathbf r_i(t) - \mathbf r_i(t-\Delta t) + \frac{\Delta t^2}{m_i}\,\mathbf F_i(t) .
$$

<div class="legend" markdown="1">
- $\mathbf r_i(t)$: the position of atom $i$ now, at time $t$.
- $\mathbf r_i(t-\Delta t)$: its position one step ago.
- $\mathbf r_i(t+\Delta t)$: its position one step ahead, which is what the formula computes.
- $\Delta t$: the time step, in ps.
- $m_i$: the mass of atom $i$.
- $\mathbf F_i(t)$: the force on atom $i$ at time $t$.
</div>

The force appears only in the last term. A force $\mathbf F$ on an atom of mass $m$ shifts its new position by $\mathbf F\Delta t^2/m$. With constraints the force is $\mathbf F_i+\mathbf G_i$. So the new position is the one computed with $\mathbf F_i$ alone, which is called $\mathbf r_i'$, plus a shift $\mathbf G_i\Delta t^2/m_i$ caused by the rods.

[Ryckaert, Ciccotti and Berendsen (1977)](cite:ryckaert1977). Take a normal, unconstrained Verlet step to positions $\mathbf r'$, then add the displacement caused by the constraint forces, which are evaluated along the bond directions at the *start* of the step:

$$
\mathbf r_i(t+\Delta t) = \mathbf r_i' - \frac{\Delta t^2}{m_i}\sum_k\lambda_k\,\nabla_i\sigma_k\big(\mathbf r(t)\big).
$$

<div class="legend" markdown="1">
- $\mathbf r_i(t+\Delta t)$: the final position of atom $i$ at the end of the step, with all constraints satisfied.
- $\mathbf r_i'$: the position of atom $i$ after the unconstrained step. The prime is not a derivative.
- $\Delta t$: the time step.
- $m_i$: the mass of atom $i$.
- $\lambda_k$: the multiplier of constraint $k$ for this step, the unknown.
- $\nabla_i\sigma_k\big(\mathbf r(t)\big)$: the gradient of constraint function $k$, computed from the positions at the start of the step, time $t$. For a bond it is plus or minus twice the *old* bond vector.
- $\sum_k$: a sum over all constraints. Only the bonds of atom $i$ contribute.
</div>

Read it like this: new position equals unconstrained position plus the shifts from the rods. Each shift is divided by the mass, so a light atom is moved further than a heavy one. The directions of the shifts are known, because they are the old bond vectors. Only the numbers $\lambda_k$ are unknown.

Why the *old* bond direction? The Verlet step uses every force as it is at time $t$, and at time $t$ each rod points along its bond as it is at time $t$. So this is the Verlet rule applied to the constraint force, with no extra approximation. It is also convenient, because the old bond vectors are known numbers.

**One constraint, solved explicitly.** Let $\mathbf s = \mathbf r_i(t)-\mathbf r_j(t)$ be the old bond vector (length $d$) and $\mathbf s' = \mathbf r_i'-\mathbf r_j'$ the unconstrained new one.

For a single bond the sum over $k$ has one term, and the previous section gave the two gradients: $2\mathbf s$ for atom $i$ and $-2\mathbf s$ for atom $j$. Atom $i$ is therefore shifted by $-(\Delta t^2/m_i)\,\lambda\,2\mathbf s$, and atom $j$ by the same expression with $m_j$ and the opposite sign. The combination $2\lambda\Delta t^2$ occurs in both shifts, so it gets a letter of its own.

With $g = 2\lambda\Delta t^2$,

$$
\mathbf r_i = \mathbf r_i' - \frac{g}{m_i}\mathbf s,\qquad \mathbf r_j = \mathbf r_j' + \frac{g}{m_j}\mathbf s,
\qquad\text{so the new bond vector is}\quad \mathbf s' - g\left(\frac1{m_i}+\frac1{m_j}\right)\mathbf s .
$$

<div class="legend" markdown="1">
- $\mathbf r_i$, $\mathbf r_j$: the final positions of the two atoms at time $t+\Delta t$. The time is no longer written.
- $\mathbf r_i'$, $\mathbf r_j'$: their positions after the unconstrained step.
- $\mathbf s$: the old bond vector, $\mathbf r_i(t)-\mathbf r_j(t)$. Its length is exactly $d$.
- $\mathbf s'$: the bond vector after the unconstrained step, $\mathbf r_i'-\mathbf r_j'$. Its length is slightly wrong.
- $g$: the unknown, $2\lambda\Delta t^2$. Its unit is a mass (u), because $\lambda$ is in u ps$^{-2}$ (1 kJ/mol is 1 u nm$^2$ ps$^{-2}$). This $g$ is not the acceleration of gravity.
- $m_i$, $m_j$: the masses of the two atoms.
</div>

The third expression is the first minus the second: $\mathbf r_i-\mathbf r_j = (\mathbf r_i'-\mathbf r_j') - (g/m_i)\,\mathbf s - (g/m_j)\,\mathbf s$.

Read it like this. Both atoms move along the old bond, in opposite directions. The ratio $g/m_i$ is a pure number: atom $i$ moves by that fraction of the old bond vector. A hydrogen (1 u) bonded to a carbon (12 u) moves 12 times as far as the carbon. The centre of mass of the pair does not move, because $m_i\times(-g/m_i) + m_j\times(g/m_j) = 0$.

The bracket $1/m_i+1/m_j$ is one divided by the reduced mass $\mu$ of Module 2, and is written $\mu^{-1}$ from here on. For a C-H bond it is $1/1 + 1/12 = 1.083$ u$^{-1}$.

The unknown $g$ is fixed by demanding that the new bond vector has length $d$. That needs the squared length of a difference of two vectors.

<div class="box maths" markdown="1">
**Maths you need here: the length of a difference of two vectors.** The squared length of a vector is its dot product with itself, $|\mathbf a|^2 = \mathbf a\cdot\mathbf a$. A dot product can be multiplied out like ordinary brackets, so

$$
|\mathbf a-\mathbf b|^2 = (\mathbf a-\mathbf b)\cdot(\mathbf a-\mathbf b) = |\mathbf a|^2 - 2\,\mathbf a\cdot\mathbf b + |\mathbf b|^2 .
$$

Check with numbers: $\mathbf a = (3, 1)$ and $\mathbf b = (1, 2)$ give $\mathbf a-\mathbf b = (2, -1)$, with squared length $4 + 1 = 5$. On the right-hand side, $|\mathbf a|^2 = 10$, $\mathbf a\cdot\mathbf b = 3 + 2 = 5$ and $|\mathbf b|^2 = 5$, so $10 - 10 + 5 = 5$. More in the [toolbox](maths.html#dot-product).
</div>

Requiring its length to be $d$ gives a quadratic equation in $g$:

$$
|\mathbf s'|^2 - 2g\,\mu^{-1}\,\mathbf s\cdot\mathbf s' + g^2\mu^{-2}d^2 = d^2,\qquad \mu^{-1} = \frac1{m_i}+\frac1{m_j}.
$$

<div class="legend" markdown="1">
- $|\mathbf s'|^2$: the squared length of the bond after the unconstrained step.
- $\mathbf s\cdot\mathbf s'$: the dot product of the old and the unconstrained bond vector. It is close to $d^2$ when the bond has turned and stretched only a little.
- $\mu$: the reduced mass of the two atoms, in u. $\mu^{-1}$ is one divided by it, and $\mu^{-2}$ is one divided by its square.
- $d$: the target bond length. $d^2$ appears on the left as the squared length of the old bond vector $\mathbf s$, and on the right as the squared length that the new bond must have.
- $g$: the unknown.
</div>

The steps: use the box with $\mathbf a = \mathbf s'$ and $\mathbf b = g\mu^{-1}\mathbf s$. The three terms are $|\mathbf s'|^2$, then $-2g\mu^{-1}\,\mathbf s\cdot\mathbf s'$, then $g^2\mu^{-2}|\mathbf s|^2$. In the last one, $|\mathbf s|^2 = d^2$ because the bond had the correct length at the start of the step. The sum must be $d^2$. The equation is called quadratic because the unknown appears squared.

Dropping the small $g^2$ term gives the SHAKE update:

$$
\boxed{g \approx \frac{|\mathbf s'|^2-d^2}{2\,\mu^{-1}\;\mathbf s\cdot\mathbf s'}}
$$

<div class="legend" markdown="1">
- $g$: the amount of correction, in u. Atom $i$ is then moved by $-(g/m_i)\,\mathbf s$ and atom $j$ by $+(g/m_j)\,\mathbf s$.
- $\approx$: "approximately equal", because one term was dropped.
- $|\mathbf s'|^2-d^2$: how far the squared length of the unconstrained bond is from its target.
- The frame around the formula marks it as a main result. It has no mathematical meaning.
- Other symbols: as in the list above.
</div>

The steps: without the $g^2$ term the equation reads $|\mathbf s'|^2 - 2g\mu^{-1}\,\mathbf s\cdot\mathbf s' = d^2$. Move $d^2$ to the left and the term with $g$ to the right, which gives $|\mathbf s'|^2-d^2 = 2g\mu^{-1}\,\mathbf s\cdot\mathbf s'$. Then divide both sides by $2\mu^{-1}\,\mathbf s\cdot\mathbf s'$.

Why is the dropped term small? The product $g\mu^{-1}$ is the fraction of its own length by which the bond vector is corrected, a few per cent at most in one step. The $g^2$ term is smaller than the term with $g$ by the factor $g\mu^{-1}/2$ (divide one by the other and use $\mathbf s\cdot\mathbf s'\approx d^2$). For a correction of 3 % that factor is 0.015.

Read the update like this:

- **The numerator** is the error. If the unconstrained bond is too long, $g$ is positive and the atoms are pulled together. If it is too short, $g$ is negative and they are pushed apart. If the length is already right, $g = 0$ and nothing moves.
- **The denominator** contains $\mathbf s\cdot\mathbf s'$, which is close to $d^2$. It becomes small when the bond has turned through a large angle during the step, and it is zero at 90°. A push along the old direction cannot repair a bond that now points sideways. This is why every constraint algorithm assumes that a bond turns by only a few degrees in one step.

Dropping a term has a price. After the correction the length is close to $d$ but not equal to it. The cure is to repeat: take the corrected positions as the new "unconstrained" ones, keep the same old bond vector $\mathbf s$, and apply the formula again. Each pass leaves an error of the order of the square of the previous one, so two or three passes are enough.

For a single bond the quadratic equation could also be solved exactly (Exercise 1). SHAKE does not do that, because with several bonds that share atoms there is no such formula, and repetition is needed there in any case.

<div class="box key" markdown="1">
**Worked example: SHAKE for one C-H bond.** The numbers are round values chosen for illustration, in two dimensions to keep them short. Atom $i$ is the hydrogen ($m_i = 1$ u), atom $j$ the carbon ($m_j = 12$ u), and the bond length is $d = 0.1$ nm. Positions are in nm.

1. *Start of the step.* Hydrogen at $(0.100, 0)$, carbon at $(0, 0)$. The old bond vector is $\mathbf s = (0.100, 0)$.
2. *Unconstrained step.* Suppose the ordinary forces move the hydrogen to $(0.104, 0.010)$ and the carbon to $(0.001, 0)$. Then $\mathbf s' = (0.103, 0.010)$, with $|\mathbf s'|^2 = 0.103^2 + 0.010^2 = 0.010709$ nm$^2$ and a length of 0.10348 nm. The bond is 3.5 % too long.
3. *The ingredients.* $d^2 = 0.01$ nm$^2$. $\mathbf s\cdot\mathbf s' = 0.100\times0.103 + 0\times0.010 = 0.0103$ nm$^2$. $\mu^{-1} = 1/1 + 1/12 = 1.0833$ u$^{-1}$.
4. *The update.* $g = (0.010709 - 0.01)/(2\times1.0833\times0.0103) = 0.000709/0.022317 = 0.03177$ u.
5. *Move the atoms.* The hydrogen moves by $-(g/m_i)\,\mathbf s = (-0.00318, 0)$ and the carbon by $+(g/m_j)\,\mathbf s = (+0.00026, 0)$. New positions: hydrogen $(0.10082, 0.010)$, carbon $(0.00126, 0)$.
6. *Check.* The bond vector is now $(0.09956, 0.010)$ and its length is 0.10006 nm. The error fell from 3.5 % to 0.06 %.
7. *Repeat.* A second pass with the same $\mathbf s$ gives $g = 0.00055$ u and a length of 0.10000002 nm, a relative error of $2\times10^{-7}$. A third pass brings the error below $10^{-13}$.
8. *Back to $\lambda$.* The three values of $g$ add up to 0.03232 u. With $\Delta t = 2$ fs $= 0.002$ ps, $\lambda = g/(2\Delta t^2) = 0.03232/(2\times0.002^2) = 4040$ kJ mol$^{-1}$ nm$^{-2}$. The rod pulled the two atoms together with a force $2\lambda d = 808$ kJ mol$^{-1}$ nm$^{-1}$ during this step.

Three things to see. The correction is along the old bond, here the $x$ direction: the $y$ components did not change. The final bond is not parallel to the old one. It has turned by 5.7°, and that rotation is real motion, which the constraint leaves alone. And the hydrogen moved 12 times as far as the carbon.
</div>

The same calculation in Python. It prints the value of $g$ and the bond length after each pass, and it is a starting point for Exercise 2.

```python
import numpy as np

d, m_i, m_j = 0.1, 1.0, 12.0            # bond length (nm), masses (u)
s = np.array([0.100, 0.0])              # old bond vector, r_i(t) - r_j(t)
r_i = np.array([0.104, 0.010])          # positions after the unconstrained step
r_j = np.array([0.001, 0.0])
mu_inv = 1/m_i + 1/m_j

for sweep in range(3):
    s_new = r_i - r_j
    g = (np.dot(s_new, s_new) - d**2) / (2 * mu_inv * np.dot(s, s_new))
    r_i = r_i - g/m_i * s               # the light atom moves more
    r_j = r_j + g/m_j * s
    print(sweep + 1, g, np.linalg.norm(r_i - r_j))
```

**Many constraints.** Atoms share constraints (a CH$_3$ group has three), so the equations are coupled. SHAKE treats them one at a time: apply the single-constraint correction to each in turn, and sweep through the list repeatedly until every bond length is within a relative tolerance (typically $10^{-4}$ to $10^{-8}$) of its target. This is a Gauss-Seidel iteration. It is simple and general, but its sequential nature makes it awkward to parallelise, and convergence slows when many constraints are coupled.

Several words in this paragraph need unpacking.

*Coupled* means that the unknowns cannot be found one by one. In a CH$_3$ group the three C-H bonds share the carbon. Correcting the first bond moves the carbon a little, and that changes the lengths of the other two. Correcting the second moves the carbon again and spoils the first. No bond can be finished before the others.

A *sweep* is one pass through the list of constraints, in which each bond is corrected once. After every sweep the program compares each bond length with its target. The *relative tolerance* is the largest value of $|l-d|/d$ that is accepted, where $l$ is the actual length of a bond and $d$ its target. With a tolerance of $10^{-4}$, a bond of 0.1 nm may be wrong by $10^{-5}$ nm. When every bond passes the test, the step is finished.

<div class="box maths" markdown="1">
**Maths you need here: solving coupled equations by repetition.** Take two equations in which each unknown depends on the other: $x = (3+y)/4$ and $y = (3+x)/4$. The solution is $x = y = 1$, as you can check by putting the numbers in. Suppose you could not see that. Start from a guess, $x = y = 0$, and use the two equations in turn, each time with the newest value of the other unknown:

| Sweep | $x = (3+y)/4$ | $y = (3+x)/4$ |
|---|---|---|
| 1 | 0.75 | 0.9375 |
| 2 | 0.9844 | 0.9961 |
| 3 | 0.9990 | 0.9998 |

Every sweep brings both numbers closer to 1, here by a factor of 16 per sweep. This way of solving, one unknown at a time with the latest values of the others, is called a **Gauss-Seidel iteration**. It does not give the exact answer in a finite number of sweeps. You stop when the remaining error is smaller than a tolerance that you chose.
</div>

<div class="box key" markdown="1">
**Worked example: two bonds that share an atom.** Three atoms of equal mass lie in a plane. Two bonds of length 0.1 nm share the middle atom (round numbers for illustration, positions in nm). At the start of the step atom 1 is at $(-0.08, 0.06)$, atom 2 at $(0, 0)$ and atom 3 at $(0.08, 0.06)$. Both bonds have the correct length, and the angle between them is 106°. The unconstrained step moves the atoms to $(-0.082, 0.061)$, $(0.001, -0.001)$ and $(0.079, 0.063)$. Bond 1-2 is now 0.10360 nm long and bond 2-3 is 0.10090 nm.

Correct bond 1-2 with the SHAKE update. Its length becomes 0.10006 nm. But atom 2 has moved, and bond 2-3, which was 0.9 % too long, is now 1.3 % too long (0.10133 nm).

Correct bond 2-3. It becomes 0.10001 nm, and bond 1-2 is disturbed in turn, to 0.10025 nm. That was one sweep. The largest relative error after each sweep is:

| Sweep | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Largest error | $2.5\times10^{-3}$ | $6.2\times10^{-5}$ | $1.1\times10^{-6}$ | $2.1\times10^{-8}$ | $3.9\times10^{-10}$ |

Each sweep reduces the error by a factor of about 50. A tolerance of $10^{-4}$ is reached after 2 sweeps and a tolerance of $10^{-8}$ after 5. A tighter tolerance costs more sweeps, and every extra digit costs about the same number of extra sweeps.
</div>

*Awkward to parallelise*: the corrections have to be made one after another, because each one uses positions that the previous correction changed. When a large molecule is divided over several processors, a bond on one processor has to wait for its neighbour on another.

*Convergence slows when many constraints are coupled*: in a long chain with every bond constrained, a correction at one place disturbs the neighbouring bonds, their corrections disturb the next ones, and the error has to be passed along the chain and worn down over many sweeps.

**RATTLE** ([Andersen 1983](cite:andersen1983)) is the version for velocity Verlet. It also removes the component of the velocities along each bond, enforcing the time derivative of the constraint, $\dot\sigma_k = 2\,\mathbf r_{ij}\cdot\mathbf v_{ij} = 0$, so that positions and velocities are both consistent at each step.

Velocity Verlet (Module 4) stores positions and velocities at the same instants. One step is a half kick of the velocities by the forces, a drift of the positions with the new velocities, and a second half kick. After the drift, RATTLE corrects the positions in the same way as SHAKE, and changes the velocities by the matching amount (the shift divided by $\Delta t$). But the velocities at the end of the step are stored too, and they must agree with rigid bonds.

The condition on the velocities is the time derivative of the constraint. Write $\sigma_k = \mathbf r_{ij}\cdot\mathbf r_{ij} - d_k^2$. The product rule gives $\dot\sigma_k = 2\,\mathbf r_{ij}\cdot\dot{\mathbf r}_{ij}$, and $\dot{\mathbf r}_{ij} = \mathbf v_i-\mathbf v_j = \mathbf v_{ij}$ is the relative velocity of the two atoms. If $\sigma_k$ is zero at all times, its rate of change $\dot\sigma_k$ is zero too.

In words: the two atoms may not move towards each other or apart. After the second half kick this is in general not true, because the ordinary forces have pushed the atoms along the bond.

RATTLE therefore makes a second correction, to the velocities. It has the same form as the correction of the positions: along the bond, opposite for the two atoms, and divided by the mass. For one bond,

$$
\mathbf v_i \to \mathbf v_i - \frac{h}{m_i}\,\mathbf r_{ij},\qquad \mathbf v_j \to \mathbf v_j + \frac{h}{m_j}\,\mathbf r_{ij},\qquad h = \frac{\mathbf r_{ij}\cdot\mathbf v_{ij}}{\mu^{-1}\,d^2} .
$$

<div class="legend" markdown="1">
- $\mathbf v_i$, $\mathbf v_j$: the velocities of the two atoms after the second half kick, in nm/ps.
- $\to$: "is replaced by".
- $\mathbf r_{ij}$: the bond vector at the new time. The positions were already corrected, so its length is $d$.
- $\mathbf v_{ij}$: the relative velocity $\mathbf v_i-\mathbf v_j$ before the correction.
- $h$: the strength of the velocity correction, a second multiplier, in u/ps.
- $m_i$, $m_j$: the masses of the two atoms.
- $\mu^{-1}$: $1/m_i+1/m_j$, as before.
- $d$: the bond length.
</div>

The steps: subtract the second replacement from the first. The new relative velocity is $\mathbf v_{ij} - h\mu^{-1}\mathbf r_{ij}$. Demand that its dot product with $\mathbf r_{ij}$ is zero: $\mathbf r_{ij}\cdot\mathbf v_{ij} - h\mu^{-1}|\mathbf r_{ij}|^2 = 0$. With $|\mathbf r_{ij}|^2 = d^2$, solving for $h$ gives the formula.

This equation has no squared unknown, so for one bond the result is exact and needs no repetition. When several bonds share atoms, the velocity corrections are swept through in the same way as the position corrections.

An example with the C-H bond used above. The bond vector is $\mathbf r_{ij} = (0.1, 0)$ nm, the hydrogen has velocity $(1.0, 0.5)$ nm/ps and the carbon $(0.1, 0)$ nm/ps. Then $\mathbf v_{ij} = (0.9, 0.5)$, $\mathbf r_{ij}\cdot\mathbf v_{ij} = 0.09$, and $h = 0.09/(1.0833\times0.01) = 8.31$ u/ps.

The velocity of the hydrogen becomes $(0.169, 0.5)$ and that of the carbon $(0.169, 0)$. Along the bond both atoms now move at the same 0.169 nm/ps, so the bond length does not change. Across the bond the hydrogen keeps its 0.5 nm/ps, which is the rotation of the bond.

SHAKE has no such step, because the position form of the Verlet algorithm stores no velocities. Velocities that are computed afterwards from differences of positions (Module 4) satisfy this condition only approximately.

## SETTLE

<div data-videos="fueOYcMgFfQ"></div>

Water is the special case that decides the cost of a simulation, because most of the atoms are water.

A rigid three-site water molecule is a triangle with the oxygen and the two hydrogens at its corners. "Three-site" means that the model has three points that carry interactions, one on each atom. Three fixed distances define the triangle: the two O-H bond lengths and the H-H distance, which fixes the angle.

Three atoms have nine coordinates. Three constraints leave six ways to move: three for the position of the molecule and three for its orientation. The molecule moves as a rigid body.

For a rigid three-site water molecule there are exactly three constraints on three atoms, and the problem can be solved analytically: [Miyamoto and Kollman (1992)](cite:miyamoto1992) find the rotated position of the rigid triangle directly. No iteration and no tolerance. Since most atoms in a simulation are water, every major code uses SETTLE or an equivalent for water and a general algorithm for the solute.

"Solved analytically" means by a formula, in a fixed number of arithmetic operations, instead of by repeated approximation.

Here is why a formula can exist. The unconstrained step leaves a triangle that is slightly out of shape. The constraint forces act inside the molecule, in equal and opposite pairs, so they cannot move its centre of mass. The centre of mass after the unconstrained step is therefore already the final one.

The shape of the final triangle is known too: it is the rigid geometry of the water model. The only thing left to find is how the rigid triangle is turned about its centre of mass, and for three atoms that geometric problem can be solved directly.

"No iteration and no tolerance" means that the three distances come out correct in one pass, to the rounding precision of the computer, and that there is no accuracy setting to choose. An iterative method stops when it reaches its tolerance, and its cost depends on how many sweeps that took.

The "solute" is everything that is not solvent: the protein, a ligand, the ions. In the system of the first "Check yourself" question below, 57,000 of the 60,000 atoms are water. A method that treats those quickly and exactly matters more for the total cost than the method used for the protein.

## LINCS

LINCS solves the same problem as SHAKE with a different plan. SHAKE corrects one bond at a time and repeats until a test is passed. LINCS treats all bonds together, in a fixed number of operations, with no test and no loop. The name stands for "linear constraint solver", the title of the paper.

[Hess, Bekker, Berendsen and Fraaije (1997)](cite:hess1997); the default for non-water constraints in GROMACS.

The method makes two moves. A **projection** sets the length of every bond, measured *along its old direction*, to the target. A **correction** then removes a small lengthening that the first move leaves behind. Both moves are easiest to see for a single bond, so that case comes first and the matrices come after it.

### LINCS for a single bond

Let $\hat{\mathbf s} = \mathbf s/d$ be the unit vector along the old bond. The bond vector after the unconstrained step, $\mathbf s'$, can be split into a part along $\hat{\mathbf s}$ and a part across it. The size of the part along $\hat{\mathbf s}$ is the dot product $\hat{\mathbf s}\cdot\mathbf s'$. It is called the **projection** of $\mathbf s'$ on the old direction: the length of the shadow that $\mathbf s'$ casts on the line of the old bond.

*Move 1, the projection.* Shift the two atoms along $\hat{\mathbf s}$, in opposite directions and in inverse proportion to their masses as in SHAKE, until the projection equals $d$. The part across the old bond is left as it is:

$$
\mathbf s' \;\to\; \mathbf s' - \left(\hat{\mathbf s}\cdot\mathbf s' - d\right)\hat{\mathbf s} .
$$

<div class="legend" markdown="1">
- $\mathbf s'$: the bond vector after the unconstrained step.
- $\hat{\mathbf s}$: the unit vector along the old bond, $\mathbf s/d$.
- $\hat{\mathbf s}\cdot\mathbf s'$: the projection of $\mathbf s'$ on the old direction, in nm.
- $d$: the target bond length.
- $\to$: "is replaced by".
</div>

Read it like this: measure how much the shadow of the bond on its old direction is too long, and take that amount away along the old direction. The condition "projection equals $d$" contains the unknown shift only to the first power. It is solved in one stroke, with nothing dropped and nothing to repeat. This is the "linear" in the name.

*What move 1 leaves behind.* The bond now has a part of length $d$ along the old direction, and it still has its part across that direction, of length $q$, say. By Pythagoras' theorem its length is $l = \sqrt{d^2+q^2}$, which is larger than $d$.

If $\theta$ is the angle between the new bond and the old one, then $d = l\cos\theta$, so $l = d/\cos\theta$. The bond is too long by the factor $1/\cos\theta$. A bond that turns by 1.8° in one step comes out too long by $5\times10^{-4}$ of its length, and a bond that turns by 30° by 15 %.

*Move 2, the correction.* Shift the atoms along $\hat{\mathbf s}$ once more, so that the part along the old direction becomes a little shorter than $d$, by the amount that makes the total length right. The part across the old direction is still $q$, with $q^2 = l^2-d^2$. By Pythagoras again, the total length is $d$ when the part along the old direction is

$$
p = \sqrt{d^2-q^2} = \sqrt{2d^2-l^2} .
$$

<div class="legend" markdown="1">
- $p$: the new target for the projection of the bond on its old direction, in nm.
- $d$: the target bond length.
- $q$: the size of the part of the bond vector across the old direction. Move 1 did not change it.
- $l$: the length of the bond after move 1.
</div>

For a single bond the result is exact. With the bond of the SHAKE example, $\mathbf s = (0.100, 0)$ and $\mathbf s' = (0.103, 0.010)$, the projection is 0.103 nm. Move 1 sets it to 0.100 and gives the bond vector $(0.100, 0.010)$, with length $l = 0.10050$ nm: too long by 0.5 %, which is $1/\cos\theta$ for $\theta = 5.7$°. Move 2 sets the projection to $p = \sqrt{2\times0.01-0.0101} = 0.09950$ nm and gives $(0.09950, 0.010)$, with length 0.10000 nm. This is the bond that SHAKE reached after three passes.

### All bonds at once: the matrix form

With many bonds that share atoms, move 1 has to be made for all bonds together, because shifting the atoms of one bond changes the projections of its neighbours. That is a set of coupled linear equations, and matrices are the standard way to write and solve such a set.

<div class="box maths" markdown="1">
**Maths you need here: matrices.** A **matrix** is a rectangular table of numbers. A matrix times a list of numbers (a vector) gives a new list. Each entry of the result is one row of the matrix, multiplied entry by entry with the list and added up. For example

$$
\begin{pmatrix} 2 & 1\\ 0 & 3 \end{pmatrix}\begin{pmatrix} 1\\ 2 \end{pmatrix} = \begin{pmatrix} 2\times1 + 1\times2\\ 0\times1 + 3\times2 \end{pmatrix} = \begin{pmatrix} 4\\ 6 \end{pmatrix} .
$$

Four more words:

- The **transpose** $\mathbf B^T$ is $\mathbf B$ with rows and columns exchanged.
- A **diagonal** matrix has non-zero numbers only on the line from top left to bottom right.
- The **inverse** $\mathbf C^{-1}$ of a square matrix $\mathbf C$ undoes it: if $\mathbf C\mathbf x = \mathbf y$ then $\mathbf x = \mathbf C^{-1}\mathbf y$. For a diagonal matrix the inverse is easy, one divided by each diagonal entry. For a general matrix with $K$ rows it costs of the order of $K^3$ operations.
- A matrix is **sparse** when most of its entries are zero.

More in the [toolbox](maths.html#matrices).
</div>

Write all constraints at once in matrix form. With $\mathbf B$ the matrix of normalised bond directions at time $t$ and $\mathbf M$ the diagonal mass matrix, the constrained positions are a projection of the unconstrained ones:

$$
\mathbf r(t+\Delta t) = \mathbf r' - \mathbf M^{-1}\mathbf B^{T}\left(\mathbf B\mathbf M^{-1}\mathbf B^{T}\right)^{-1}\left(\mathbf B\mathbf r' - \mathbf d\right).
$$

<div class="legend" markdown="1">
- $\mathbf r'$: the positions of all $N$ atoms after the unconstrained step, written as one list of $3N$ numbers $(x_1, y_1, z_1, x_2, \dots)$.
- $\mathbf r(t+\Delta t)$: the same list after the constraints have been applied.
- $K$: the number of constraints. In this section $K$ is not the kinetic energy.
- $\mathbf B$: a table with $K$ rows and $3N$ columns. Row $k$ describes bond $k$ between atoms $i$ and $j$. It holds the old unit vector $\hat{\mathbf s}_k$ in the three columns of atom $i$, $-\hat{\mathbf s}_k$ in the three columns of atom $j$, and zeros everywhere else. "Normalised" means "of length 1".
- $\mathbf B\mathbf r'$: a list of $K$ numbers. Entry $k$ is $\hat{\mathbf s}_k\cdot(\mathbf r_i'-\mathbf r_j')$, the projection of the unconstrained bond $k$ on its old direction.
- $\mathbf d$: the list of the $K$ target bond lengths.
- $\mathbf B\mathbf r'-\mathbf d$: the error of every bond along its old direction, $K$ numbers in nm.
- $\mathbf M$: the diagonal matrix with $3N$ rows that holds the mass of each atom three times, once for each of $x$, $y$ and $z$. Its inverse $\mathbf M^{-1}$ holds $1/m$ on the diagonal.
- $\mathbf B^T$: the transpose of $\mathbf B$, with $3N$ rows and $K$ columns.
- $\mathbf B\mathbf M^{-1}\mathbf B^{T}$: a table with $K$ rows and $K$ columns, the **constraint-coupling matrix**. The power $-1$ outside the bracket is its inverse.
</div>

Read the formula from right to left:

1. $\mathbf B\mathbf r'-\mathbf d$ measures, for every bond, how far its projection on the old direction is from the target.
2. The inverse of the coupling matrix turns these errors into the strength of the correction that each bond needs. It takes into account that bonds share atoms, so that correcting one bond changes its neighbours. These $K$ strengths play the part of $g$ in SHAKE: one unknown per bond.
3. $\mathbf B^T$ turns the strength of each bond into shifts of its two atoms, along the old bond direction and opposite for the two.
4. $\mathbf M^{-1}$ divides each shift by the mass of the atom, so light atoms move more.
5. The result is subtracted from the unconstrained positions.

For one bond this is move 1 of the previous subsection. $\mathbf B$ has a single row, $(\hat{\mathbf s}, -\hat{\mathbf s})$. The coupling matrix is the single number $1/m_i+1/m_j = \mu^{-1}$, and its inverse is $\mu$. Atom $i$ is shifted by $-(\mu/m_i)(\hat{\mathbf s}\cdot\mathbf s'-d)\,\hat{\mathbf s}$ and atom $j$ by $+(\mu/m_j)(\hat{\mathbf s}\cdot\mathbf s'-d)\,\hat{\mathbf s}$. Since $\mu/m_i+\mu/m_j = 1$, the bond vector changes by $-(\hat{\mathbf s}\cdot\mathbf s'-d)\,\hat{\mathbf s}$, as before.

Why does $\mathbf B$ hold unit vectors, while SHAKE had $2\mathbf r_{ij}$? LINCS writes each constraint with the length, $|\mathbf r_i-\mathbf r_j|-d_k = 0$, instead of the squared length. The gradient of a length with respect to $\mathbf r_i$ is the unit vector along the bond (Module 2). So the rows of $\mathbf B$ are the gradients of the constraints, and $\mathbf B^T$ plays the part that $\nabla_i\sigma_k$ played in SHAKE.

To check that the formula does what is claimed, multiply it from the left by $\mathbf B$:

$$
\mathbf B\,\mathbf r(t+\Delta t) = \mathbf B\mathbf r' - \left(\mathbf B\mathbf M^{-1}\mathbf B^{T}\right)\left(\mathbf B\mathbf M^{-1}\mathbf B^{T}\right)^{-1}\left(\mathbf B\mathbf r'-\mathbf d\right) = \mathbf B\mathbf r' - \left(\mathbf B\mathbf r'-\mathbf d\right) = \mathbf d .
$$

<div class="legend" markdown="1">
- $\mathbf B\,\mathbf r(t+\Delta t)$: the projections of the final bonds on their old directions.
- A matrix times its own inverse is the identity matrix and drops out. That is the step from the second to the third expression.
- Other symbols: as in the list above.
</div>

After the step, the projection of every bond on its old direction equals its target length, for all bonds at the same time. "Projection" is also the mathematical name for an operation of this kind: it removes the part of the positions that violates the constraints and leaves the rest alone.

### The series that replaces the inverse

The expensive part is inverting the $K\times K$ constraint-coupling matrix $\mathbf B\mathbf M^{-1}\mathbf B^T$. A protein has a thousand or more constraints, and the bond directions change at every step, so the matrix would have to be inverted anew at every step. A direct inverse is far too expensive for that.

The entries of the coupling matrix can be written down. On the diagonal, entry $(k,k)$ is $1/m_i+1/m_j$ for the two atoms of bond $k$, the $\mu^{-1}$ of SHAKE. Off the diagonal, entry $(k,l)$ is zero unless bonds $k$ and $l$ share an atom. If they share an atom of mass $m_c$, its size is $|\cos\phi|/m_c$, where $\phi$ is the angle between the two bonds, and its sign depends on the order in which the two atoms of each bond are written. These off-diagonal entries are the coupling: they say how much a correction of bond $l$ changes the projection of bond $k$.

LINCS writes it as $\mathbf S(\mathbf 1-\mathbf A)\mathbf S$ with $\mathbf S$ diagonal, where $\mathbf A$ is sparse and has non-zero entries only for constraints that share an atom, and uses the series

$$
(\mathbf 1-\mathbf A)^{-1} = \mathbf 1+\mathbf A+\mathbf A^2+\mathbf A^3+\dots
$$

truncated after a few terms (`lincs-order = 4`).

<div class="legend" markdown="1">
- $\mathbf S$: a diagonal matrix with $K$ rows. Its entry for bond $k$ is $\sqrt{1/m_i+1/m_j}$, the square root of the diagonal entry of the coupling matrix. It is not the bond vector $\mathbf s$. (The LINCS paper gives the name $\mathbf S$ to the inverse of this matrix and writes the inverse of the coupling matrix with it. The matrix $\mathbf A$ is the same in both ways of writing.)
- $\mathbf 1$: the identity matrix with $K$ rows.
- $\mathbf A$: a matrix with $K$ rows and columns and zeros on its diagonal. Entry $(k,l)$ is minus the entry of the coupling matrix divided by $S_{kk}S_{ll}$. Its entries are pure numbers.
- $(\mathbf 1-\mathbf A)^{-1}$: the inverse of the matrix $\mathbf 1-\mathbf A$.
- $\mathbf A^2$, $\mathbf A^3$: $\mathbf A$ applied twice, three times.
- The dots: the sum continues without end.
</div>

The first step is a rescaling. Dividing row $k$ and column $k$ of the coupling matrix by $S_{kk}$ turns every diagonal entry into 1. What is left off the diagonal is called $-\mathbf A$.

So the coupling matrix equals $\mathbf S(\mathbf 1-\mathbf A)\mathbf S$, and its inverse is $\mathbf S^{-1}(\mathbf 1-\mathbf A)^{-1}\mathbf S^{-1}$. $\mathbf S$ is diagonal, so its inverse costs nothing. All the difficulty is now in $(\mathbf 1-\mathbf A)^{-1}$, and for that there is a trick that is known from ordinary numbers.

<div class="box maths" markdown="1">
**Maths you need here: the geometric series.** For a number $x$ between $-1$ and 1,

$$
\frac{1}{1-x} = 1 + x + x^2 + x^3 + \dots
$$

To see why, call the sum up to the term $x^n$ by the name $s_n$ and multiply it by $(1-x)$. All terms cancel in pairs except the first and the last: $(1-x)\,s_n = 1-x^{n+1}$. When $x$ is smaller than 1 in size, $x^{n+1}$ shrinks towards zero as $n$ grows, so $s_n$ approaches $1/(1-x)$.

With $x = 0.2$ the exact value is $1/0.8 = 1.25$, and the sums are 1, 1.2, 1.24, 1.248, 1.2496. After the term $x^4$ the error is 0.0004. The smaller $x$ is, the fewer terms are needed.

With $x = 1.2$ the sums are 1, 2.2, 3.64, 5.37 and grow without limit, while $1/(1-1.2) = -5$. The series is useless when $x$ is larger than 1 in size. It is the Taylor expansion of $1/(1-x)$ around $x = 0$ ([toolbox](maths.html#taylor)).
</div>

The same series holds with the matrix $\mathbf A$ in the place of the number $x$ and the identity matrix in the place of 1. That is the formula above. You can check it in the same way: multiply $\mathbf 1+\mathbf A+\dots+\mathbf A^n$ by $(\mathbf 1-\mathbf A)$, and all terms cancel except $\mathbf 1-\mathbf A^{n+1}$.

Why is this cheaper than inverting? The program never builds the powers of $\mathbf A$ as tables. It needs only the product of the inverse with one list of numbers, the errors. So it multiplies that list by $\mathbf A$, multiplies the result by $\mathbf A$ again, and so on, and adds up the lists. Because $\mathbf A$ is sparse, one such multiplication costs a few operations per bond.

Each term has a meaning. The term $\mathbf 1$ corrects every bond as if it were alone. The term $\mathbf A$ adds the effect that the correction of each bond has on its direct neighbours. The term $\mathbf A^2$ adds the effect over two bonds, which includes the echo of a bond on itself through a neighbour, and so on.

Cutting the series after $\mathbf A^4$ ignores coupling over more than four bonds. The setting `lincs-order` says where the series is cut. In the algorithm printed in the LINCS paper the order is the number of multiplications by $\mathbf A$, which is the highest power of $\mathbf A$ that is kept.

How fast the terms shrink depends on the size of the entries of $\mathbf A$, which is set by the masses and by $\cos\phi$.

Three illustrations, with masses of 1 and 12 u. For two C-H bonds on the same carbon at an angle of 110° the entry is about 0.03, because the shared carbon is heavy and enters as $1/12$. For two bonds between carbons that share a carbon at 110° it is 0.17. For an angle of 90° it would be zero. With entries of this size the terms of the series shrink quickly.

### The correction for rotation

Because the projection uses the old bond directions, the new bonds come out slightly too long after rotation, by a factor $1/\cos\theta$ for a rotation angle $\theta$ in one step (a relative error of about $5\times10^{-4}$ rms for a protein at 2 fs). This is the lengthening that the one-bond picture showed. "rms" stands for root mean square, a kind of average over all bonds: square each error, take the mean, and take the square root.

A relative error of $5\times10^{-4}$ is what a rotation by 1.8° produces, and that is the size of rotation to expect from thermal motion. At 300 K a hydrogen moves at about $\sqrt{k_BT/m} = 1.6$ nm/ps along each direction, which is 0.0032 nm in a step of 2 fs. A sideways move of 0.0032 nm at the end of a bond of 0.1 nm is an angle of 0.032 radians, or 1.8°.

A final correction step reduces this to about $10^{-6}$ (`lincs-iter = 1`). It is not exactly zero, because the correction itself rotates coupled bonds slightly.

The correction step is move 2 of the one-bond picture, made for all bonds together. The program measures the length $l_k$ of every bond after the projection, computes the new targets $p_k = \sqrt{2d_k^2-l_k^2}$, and applies the projection formula once more with the list of the $p_k$ in the place of $\mathbf d$. The same series is used again.

For a bond on its own this would be exact. With coupled bonds, the shift of a shared atom turns the neighbouring bonds a little, which is the reason for the remaining $10^{-6}$. The setting `lincs-iter` is the number of correction steps.

The formula for $p_k$ has no solution when $l_k^2$ is larger than $2d_k^2$. That happens when a bond has turned by more than 45° in one step, because then $1/\cos\theta$ is larger than $\sqrt2$. No shift along the old direction can repair such a bond.

<div class="box key" markdown="1">
**Worked example: LINCS for two bonds that share an atom.** Take the three atoms of the SHAKE example again: equal masses of 12 u, old positions $(-0.08, 0.06)$, $(0, 0)$ and $(0.08, 0.06)$ nm, bonds of 0.1 nm. Bond 1 runs from atom 2 to atom 1 and bond 2 from atom 2 to atom 3, so the old unit vectors are $\hat{\mathbf s}_1 = (-0.8, 0.6)$ and $\hat{\mathbf s}_2 = (0.8, 0.6)$. The matrix $\mathbf B$ has two rows, one per bond, and six columns, for $x_1, y_1, x_2, y_2, x_3, y_3$:

$$
\mathbf B = \begin{pmatrix} -0.8 & 0.6 & 0.8 & -0.6 & 0 & 0\\ 0 & 0 & -0.8 & -0.6 & 0.8 & 0.6 \end{pmatrix} .
$$

1. *The errors.* The unconstrained positions are $(-0.082, 0.061)$, $(0.001, -0.001)$ and $(0.079, 0.063)$. The projections $\mathbf B\mathbf r'$ are 0.1036 and 0.1008 nm, so $\mathbf B\mathbf r'-\mathbf d = (0.0036, 0.0008)$ nm.
2. *The coupling matrix.* The diagonal entries are $1/12+1/12 = 0.1667$ u$^{-1}$. The two bonds share atom 2 at an angle of 106°, with $\cos\phi = -0.28$, so the off-diagonal entries are $-0.28/12 = -0.0233$ u$^{-1}$.
3. *$\mathbf S$ and $\mathbf A$.* $S_{11} = S_{22} = \sqrt{0.1667} = 0.408$. Dividing the off-diagonal entry by $0.408\times0.408 = 0.1667$ and changing its sign gives $A_{12} = A_{21} = 0.14$.
4. *The series.* Summed up to $\mathbf A^4$, it has 1.019984 on the diagonal and 0.142744 off it. The exact inverse of $\mathbf 1-\mathbf A$ has 1.019992 and 0.142799. Cut after $\mathbf A^4$, each entry is off by less than $6\times10^{-5}$.
5. *The strengths.* Without coupling, each bond would get a correction of its error divided by 0.1667, which is 0.0216 and 0.0048 (in u nm). With coupling the values are 0.0227 and 0.0080. Bond 2 needs much more than its own error suggests, because the large correction of bond 1 pulls on the shared atom.
6. *After the projection.* The bond lengths are 0.100004 and 0.100034 nm. The bonds turned by 0.5° and 1.5° during the step, and they are too long by $4\times10^{-5}$ and $3\times10^{-4}$ of their length, the factor $1/\cos\theta$.
7. *After one correction.* The relative errors are $1\times10^{-6}$ and $-3\times10^{-6}$.

The final positions agree with those of SHAKE, iterated to convergence, to within $2\times10^{-7}$ nm. LINCS got there with a fixed amount of work: two projections, each with four multiplications by $\mathbf A$.
</div>

### What LINCS gains, and when the series fails

LINCS has no convergence loop (its accuracy is set by the order of the series and the number of correction steps), was three to four times faster than SHAKE at equal accuracy in the authors' tests, and is easy to parallelise because a bond is coupled only to bonds a few steps away (P-LINCS).

"No convergence loop" means that the amount of work per step is known in advance. "Coupled only to bonds a few steps away" follows from the series: cut after $\mathbf A^4$, the new position of an atom depends only on bonds a few bonds away (about as many as the order of the series), and the correction step doubles that reach. A processor that holds one part of a molecule therefore needs to know only a thin layer of the neighbouring part. P-LINCS is the name of the parallel version.

The series only converges when all eigenvalues of $\mathbf A$ are smaller than 1 in absolute value. An eigenvalue of a matrix is a number $a$ for which there is a list of numbers, an eigenvector, that the matrix only multiplies by $a$ (Module 2 and the [toolbox](maths.html#eigen)). Applying $\mathbf A$ to such a list $n$ times multiplies it by $a^n$.

If every eigenvalue is smaller than 1 in size, the terms of the series shrink, like $x^n$ in the box above. If one of them is larger than 1, the terms grow and the sum has no meaning. In the worked example the eigenvalues of $\mathbf A$ are $+0.14$ and $-0.14$.

This always holds for bond constraints in molecules, even with rings. It can fail when angles are also constrained through extra distance constraints, which create small rings with high connectivity: Hess et al. found a largest eigenvalue of 0.8 for angle-constrained butane and 1.2 for pentane.

An angle is constrained by adding a rod between the two outer atoms, as in rigid water. Each such rod closes a triangle of three constraints in which every constraint shares an atom with the other two, and neighbouring triangles share a side. That is the meaning of "small rings with high connectivity". Every constraint is coupled to many others, and the eigenvalues grow.

With an eigenvalue of 0.8 the series still converges, but slowly: $0.8^5 = 0.33$, so after the term $\mathbf A^4$ a third of that part of the error is still there. With 1.2 the terms grow, as in the box.

The projection itself is still valid then, but the matrix has to be inverted another way, so rigid triangles and similar groups need special handling.

### LINCS warnings

When a simulation becomes unstable, the first symptom in GROMACS is usually a "LINCS warning": a bond has rotated by more than 30° in one step. The constraint algorithm is reporting the problem, and is rarely the cause. Look for bad contacts, a time step that is too large, or a system that was not equilibrated.

Why does the warning speak of rotation? The whole method assumes that the old bond direction is still a good guide, which is true when bonds turn by a small angle in one step. Thermal motion turns a bond to hydrogen by about 2° in 2 fs, as estimated above.

A turn of 30° needs the hydrogen to move about 0.05 nm sideways in a single step, more than fifteen times its thermal speed. An atom becomes that fast only when a very large force acts on it. Such a force has a cause outside the constraint algorithm: two atoms that overlap (a "bad contact"), or a trajectory that has already become unstable.

At 30° a bond would come out 15 % too long after the projection, and at 45° the correction has no solution. The warning comes before the method breaks down.

### What the accuracy settings mean

| Setting | What it controls | Looser or lower | Tighter or higher |
|---|---|---|---|
| SHAKE relative tolerance ($10^{-4}$ to $10^{-8}$) | The largest relative error of a bond length at which SHAKE stops sweeping | Fewer sweeps, but every bond may be wrong by that fraction at every step | More sweeps per step |
| `lincs-order` (4) | Where the series is cut (the order of the expansion), that is, over how many bonds the coupling is followed | Cheaper, less accurate for strongly coupled bonds | More multiplications by $\mathbf A$, and a wider layer to exchange between processors |
| `lincs-iter` (1) | The number of correction steps for the lengthening by rotation | With none, the error of about $5\times10^{-4}$ quoted above stays | One more projection per step for each extra correction |
| SETTLE | Nothing to set: the result is exact | | |

LINCS has no tolerance. Its accuracy follows from the two numbers in the table and from how far the bonds turn in one step, so it gets worse when the time step is longer or the atoms are faster.

Why care about the fourth or sixth digit of a bond length? Because of the energy. A bond length that is slightly wrong in a different way at every step means constraint forces that are slightly wrong at every step, and those do a little work. Over millions of steps the total energy drifts. Module 4 lists a loose constraint tolerance among the things to suspect when the energy of a run without thermostat does not behave as the integrator predicts.

The demo below compares a small molecule with flexible bonds and the same molecule with its bonds held rigid by SHAKE. Its units are arbitrary, not femtoseconds. Raise the time step and watch the error of the total energy. The flexible molecule becomes unstable at the limit set by its stiff bonds, while the rigid one stays stable up to a time step several times larger. The line of numbers under the plot also reports how many SHAKE sweeps were needed per step and how well the bond lengths were kept.

<div class="widget" data-widget="shake"></div>

## Consequences for the statistics

Rigid bonds change three things that you compute from a simulation: the temperature, the pressure and, very slightly, the probabilities of the conformations. The program takes care of the first two, but you need to know what it does in order to read its output and to avoid mistakes in your own analysis.

**Degrees of freedom.** Each constraint removes one degree of freedom. A **degree of freedom** is one independent way in which the system can move (Module 2). $N$ free atoms have $3N$ of them, one for each coordinate. A constraint is one equation that ties coordinates together, so it takes one away.

Two free atoms have 6 degrees of freedom. Joined by a rod they have 5: three for moving the pair as a whole and two for turning it. The vibration along the bond is the one that is gone.

This matters for the temperature. In a simulation the temperature is computed from the kinetic energy (Module 3). At equilibrium every degree of freedom carries on average $\tfrac12k_BT$ of kinetic energy, so

$$
T_{inst} = \frac{2K}{N_{df}\,k_B} .
$$

<div class="legend" markdown="1">
- $T_{inst}$: the instantaneous temperature, the temperature computed from one frame of the simulation, in K.
- $K$: the total kinetic energy, $\sum_i\tfrac12m_iv_i^2$, in kJ/mol. Here $K$ is not the number of constraints.
- $N_{df}$: the number of degrees of freedom that carry kinetic energy.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
</div>

A frozen vibration carries no kinetic energy, so it must not be counted in $N_{df}$. The temperature must be computed with

$$
N_{df} = 3N - N_{c} - 3 .
$$

<div class="legend" markdown="1">
- $N$: the number of atoms. $3N$ is the number of coordinates.
- $N_c$: the number of constraints (called $K$ in the LINCS section).
- $3$: the three components of the total momentum. In a periodic box they are held at zero, which removes three more degrees of freedom (Module 2).
- $N_{df}$: the number that goes into the temperature formula above.
</div>

A solvated protein with rigid water loses a third of its degrees of freedom this way. A rigid water molecule has 9 coordinates and 3 constraints, so 6 of its 9 degrees of freedom are left, and most atoms of the system are water.

A wrong count gives a wrong temperature. Suppose a program divided by $3N$ instead of $N_{df}$. For the system of the first "Check yourself" question, $N_{df}$ is 121,497 and $3N$ is 180,000. The same kinetic energy would be reported as a temperature that is too low by the factor $121{,}497/180{,}000 = 0.675$: a system at 300 K would read 202 K. A thermostat that trusted this number would heat the system until the wrong formula showed 300 K, which is a true temperature of 444 K.

Codes do this for you, but when you thermostat groups separately or analyse a subset of atoms you need the right count for each group. In the same system the protein (3,000 atoms, 1,500 constraints) has $9{,}000-1{,}500 = 7{,}500$ degrees of freedom, and the water has $19{,}000\times6 = 114{,}000$. If you compute "the temperature of the protein" yourself from its velocities, use 7,500 and not 9,000. (The 3 for the total momentum belongs to the system as a whole and makes no visible difference for groups of this size.)

**Pressure.** Constraint forces contribute to the virial, $\Xi_{c} = -\tfrac12\sum_k\mathbf r_{ij}\cdot\mathbf G_{ij}$. Leaving them out gives a pressure that is wrong by hundreds of bar.

To see what this means, recall how the pressure is computed (Modules 3 and 8). It has two ingredients: the kinetic energy, and the **virial**, a sum over all pairs of atoms of the distance between them times the force along it:

$$
P_{inst} = \frac{2}{3V}\left(K - \Xi\right),\qquad \Xi = -\frac12\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}.
$$

<div class="legend" markdown="1">
- $P_{inst}$: the instantaneous pressure, computed from one frame.
- $V$: the volume of the simulation box, in nm$^3$.
- $K$: the total kinetic energy.
- $\Xi$ (capital Greek xi): the virial, in kJ/mol.
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once.
- $\mathbf r_{ij}$: the vector from atom $j$ to atom $i$.
- $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$.
</div>

Read it like this. A force that pulls two atoms together points against $\mathbf r_{ij}$, so $\mathbf r_{ij}\cdot\mathbf F_{ij}$ is negative, $\Xi$ gets a positive contribution and the pressure goes down. A force that pushes them apart raises the pressure.

The kinetic energy stands for the atoms hitting the walls, and the virial corrects for the forces between them. For the units: 1 kJ mol$^{-1}$ nm$^{-3}$ is 16.6 bar, and the pressure of the atmosphere is about 1 bar.

A rod is a force between two atoms like any other, so it has to be in the sum. In $\Xi_c$ the sum runs over the constraints $k$, $\mathbf r_{ij}$ is the bond vector of constraint $k$, and $\mathbf G_{ij}$ is the force of its rod on atom $i$, which is $-2\lambda_k\mathbf r_{ij}$. Putting that in gives

$$
\Xi_c = -\tfrac12\sum_k \mathbf r_{ij}\cdot\left(-2\lambda_k\,\mathbf r_{ij}\right) = \sum_k \lambda_k\,d_k^2 .
$$

<div class="legend" markdown="1">
- $\Xi_c$: the part of the virial that comes from the constraint forces.
- $\sum_k$: a sum over all constraints.
- $\lambda_k$: the multiplier of constraint $k$, which the constraint algorithm has already computed.
- $d_k$: the length of bond $k$. The last step uses $\mathbf r_{ij}\cdot\mathbf r_{ij} = d_k^2$.
</div>

A rod under tension ($\lambda_k>0$) pulls its two atoms together, adds a positive amount to the virial and lowers the pressure, like any attraction.

The spinning pair of the earlier worked example shows that this term is not small. Its rod has $\lambda = 133$ kJ mol$^{-1}$ nm$^{-2}$ and $d = 0.15$ nm, so $\Xi_c = \lambda d^2 = 3.0$ kJ/mol. The kinetic energy of the spinning is $2\times\tfrac12\times12\times0.5^2 = 3.0$ kJ/mol, the same number.

In $K-\Xi$ the two cancel. That makes physical sense: a molecule that only spins does not push on the walls of its container, and it is the virial of the rod that removes the spinning from the pressure. Every rigid molecule in the box has such a term, which is why leaving them out does so much damage. A rough size for water: if a rigid water molecule turned freely, the virial of its three rods would equal its rotational kinetic energy, on average $\tfrac32k_BT$. Leaving that out for every molecule would raise the pressure by $nk_BT$, with $n$ the number of molecules per volume. For liquid water, $n = 33.4$ nm$^{-3}$ gives $33.4\times2.494 = 83$ kJ mol$^{-1}$ nm$^{-3}$, about 1,400 bar. The "hundreds of bar" quoted above is therefore a cautious figure for a box of water.

**Distributions.** Rigidly constrained and very stiff flexible systems do not have exactly the same distribution of the remaining coordinates: integrating out the constrained momenta leaves a factor depending on the mass-metric tensor (the Fixman correction). For bond-length constraints the effect is negligible. For constrained angles and dihedrals it is not, another reason these are left free.

This is the subtlest point of the module. On a first reading, the last two sentences of that paragraph are what you need. The idea behind the first sentence is this.

Module 3 shows that without constraints the probability of an arrangement of the atoms depends only on its potential energy. The momenta can be "integrated out", that is, summed over all their possible values, and the sum gives the same number for every arrangement.

With rods this is no longer exactly true. A rod forbids motion along its own direction, and that direction turns with the molecule. The set of allowed momenta therefore depends on the shape of the molecule, and summing over it leaves a factor that depends on the shape. A very stiff spring leaves no such factor, because its atoms can still move along the bond.

The "mass-metric tensor" is the table of masses and bond directions from which this factor is computed, and "Fixman correction" is the name under which the factor is known.

<details markdown="1"><summary>Optional: how large the factor is for two bonds</summary>
The factor is built from the determinant of the constraint-coupling matrix that LINCS inverts. (A determinant is a single number computed from a square matrix. For a table with two rows it is the product of the two diagonal entries minus the product of the other two.)

For one bond the matrix is the single number $1/m_i+1/m_j$. It does not depend on the shape of the molecule, so one constraint on its own changes nothing. For two bonds that share an atom of mass $m_c$, with outer atoms of mass $m_i$ and $m_j$ and an angle $\phi$ between the bonds, the determinant is

$$
\left(\frac1{m_i}+\frac1{m_c}\right)\left(\frac1{m_j}+\frac1{m_c}\right) - \frac{\cos^2\phi}{m_c^2} .
$$

It depends on the shape only through the angle $\phi$. For two C-H bonds on one carbon (masses of 1 and 12 u) the first term is 1.1736 u$^{-2}$, and the second is at most $1/144 = 0.007$ u$^{-2}$. Between $\phi = 100$° and $\phi = 120$° the determinant changes by 0.13 %. A change of that size in a probability corresponds to an energy of about 0.001 $k_BT$, far below anything a simulation can resolve. The effect is small because the shared atom is heavy and enters as $1/m_c$, and because bond angles vary little.

When angles are constrained as well, the rods form triangles that share sides, and the determinant depends on the torsion angles. Those are the coordinates that describe the conformation, so the factor then changes the populations that you want to measure.
</details>

## Going beyond 2 fs

With ten steps per period, a fastest period of 20 fs is what holds the time step at 2 fs. To reach 4 fs the fastest period has to be near 40 fs.

After constraining bonds to hydrogen, the fastest remaining motions involve hydrogens: bond-angle vibrations (H-X-H, H-X-Y) and the rotation of hydroxyl and methyl groups, with periods around 20 fs. Two techniques slow them down.

In "H-X-H" and "H-X-Y", X and Y stand for any heavy atoms, such as carbon, nitrogen or oxygen. The first is the opening and closing of the angle between two hydrogens on the same atom, the second the swinging of one hydrogen. A hydroxyl group is O-H and a methyl group is CH$_3$. Both techniques act on the hydrogens, because the small mass of the hydrogens is what makes these motions fast.

### Hydrogen mass repartitioning (HMR)

Increase the mass of each hydrogen (for example from 1 to 3 or 4 u) and subtract the same amount from the heavy atom it is bonded to. The total mass of every group is unchanged. Frequencies of hydrogen motions fall by $\sqrt{m_H'/m_H}$, a factor of up to 2, which allows $\Delta t$ = 4 fs with bonds to hydrogen constrained.

The idea rests on the formula $\omega = \sqrt{k_b/\mu}$: for a given stiffness, a heavier mass vibrates more slowly. The force field, and with it every stiffness, is left untouched. Only the masses in the input are changed.

In the factor, $m_H$ is the normal mass of a hydrogen (1 u) and $m_H'$ its increased mass. With $m_H' = 3$ u the factor is $\sqrt3 = 1.73$, and with 4 u it is $\sqrt4 = 2$. These factors are upper limits, because the heavy atom becomes lighter at the same time and the frequency follows the reduced mass (Exercise 4). The periods grow from about 20 fs to between 30 and 40 fs (the table in Module 4), which is what makes a time step of 4 fs possible.

The bookkeeping for a methyl group: a carbon of 12 u and three hydrogens of 1 u make 15 u. With hydrogens of 3 u, each hydrogen has taken 2 u from the carbon, which is left with $12-3\times2 = 6$ u. The total is still $6+3\times3 = 15$ u.

Why it is legitimate: without constraints the equilibrium distribution of positions does not depend on masses at all (Module 3), and with bond constraints the only mass dependence is the small metric-tensor factor mentioned above, which is negligible for bonds to hydrogen. Thermodynamics is therefore unchanged to an excellent approximation. Dynamics are slightly altered, mainly rates that involve the light atoms. [Hopkins et al. (2015)](cite:hopkins2015) validated it for proteins. Water is usually not repartitioned, because it is rigid already and changing its hydrogen masses would change its rotational dynamics and viscosity.

Changing masses can look like cheating, so here is the first step of that argument in full. At equilibrium the probability of a state with positions $\mathbf r$ and momenta $\mathbf p$ is proportional to the Boltzmann factor $e^{-\beta H}$ (Module 3). The energy $H$ is a sum of a kinetic and a potential part, and the exponential of a sum is a product:

$$
e^{-\beta H} = e^{-\beta\sum_i \mathbf p_i^2/2m_i}\times e^{-\beta U(\mathbf r)} .
$$

<div class="legend" markdown="1">
- $H$: the total energy, kinetic plus potential (the Hamiltonian of Module 2).
- $\beta$: $1/k_BT$. At 300 K, $k_BT$ is 2.494 kJ/mol.
- $e$: the base of the exponential function. $e^{-\beta H}$ is small for states of high energy.
- $\mathbf p_i$: the momentum of atom $i$, mass times velocity.
- $m_i$: the mass of atom $i$.
- $\mathbf p_i^2/2m_i$: the kinetic energy of atom $i$. $\sum_i$ adds it up over all atoms.
- $U(\mathbf r)$: the potential energy, a function of the positions only.
</div>

The masses appear only in the first factor, which contains momenta and no positions. The second factor decides how probable each arrangement of the atoms is, and it contains no mass. So the masses decide how fast the system moves through its conformations, and they have no say in how often each conformation occurs. Heavier balls roll more slowly over an energy landscape, but its hills and valleys stay where they are.

"Thermodynamics" here means everything that depends only on how often states occur: average structures, populations, free-energy differences. "Dynamics" means everything that depends on how fast things happen: rates, diffusion constants, relaxation times.

The last sentence, on water, has a simple reason. A rigid water molecule has no internal vibration to slow down, so nothing would be gained. Something would be lost: moving mass from the oxygen to the hydrogens changes how easily the molecule turns, and with it how fast water molecules rotate and how viscous the liquid is. The solute would then move in a different solvent.

### Virtual sites

Remove the hydrogen degrees of freedom entirely: the hydrogen position is constructed each step from the positions of its heavy-atom neighbours, the force on it is redistributed to those atoms, and its mass is added to them. With all hydrogen motions gone, 4 to 5 fs is possible. The same machinery implements the massless charge sites of four- and five-site water models and the off-centre sites used for lone pairs.

A **virtual site** is a point that interacts with other atoms, through a charge or Lennard-Jones parameters, but is not moved by the integrator. Its position is not an independent quantity. At every step it is computed by a fixed geometric rule from the positions of real atoms. It has no degree of freedom of its own, so it cannot vibrate, and it is not counted in $N_{df}$.

The simplest rule places the site on the line between two atoms:

$$
\mathbf r_v = (1-a)\,\mathbf r_1 + a\,\mathbf r_2 ,\qquad \mathbf F_1 \leftarrow \mathbf F_1 + (1-a)\,\mathbf F_v,\qquad \mathbf F_2 \leftarrow \mathbf F_2 + a\,\mathbf F_v .
$$

<div class="legend" markdown="1">
- $\mathbf r_v$: the position of the virtual site.
- $\mathbf r_1$, $\mathbf r_2$: the positions of the two real atoms from which it is built.
- $a$: a fixed number, chosen once. $a = 0$ puts the site on atom 1, and $a = 0.5$ puts it halfway between the two atoms.
- $\mathbf F_v$: the force that the force field computes on the site, from its interactions with all other atoms.
- $\mathbf F_1$, $\mathbf F_2$: the forces on the two real atoms.
- $\leftarrow$: "is replaced by".
</div>

Read it like this. The first formula is the construction. The other two are the redistribution of the force. The site feels a force but cannot respond to it, because it has no mass and no equation of motion. The force is therefore passed on to the atoms that define the site.

The shares follow from the construction. If atom 1 moves by a small amount, the site moves by $(1-a)$ times that amount, so a force on the site acts on atom 1 with the weight $(1-a)$. The two shares add up to the whole force, so nothing is lost. A hydrogen needs a rule with more neighbours, which can place it off the line, but the principle is the same.

"Its mass is added to them" keeps the total mass of the molecule right: the hydrogen is no longer a moving atom, so its mass is carried by its heavy neighbours.

The last sentence of the paragraph names two other uses. A four-site water model puts its negative charge on a point near the oxygen that has no mass (Module 6). That point is a virtual site built from the three atoms. "Lone pairs" are the electron pairs of atoms such as oxygen that take no part in a bond, and some models represent them by a charged site placed away from the centre of the atom.

## Check yourself

<details markdown="1"><summary>1. A system has 60,000 atoms: a 3,000-atom protein with 1,500 bonds to hydrogen constrained, and 19,000 rigid three-site water molecules. How many degrees of freedom?</summary>
$3\times60{,}000 = 180{,}000$. Constraints: 1,500 for the protein plus $3\times19{,}000 = 57{,}000$ for water. $N_{df} = 180{,}000 - 58{,}500 - 3 = 121{,}497$.
</details>

<details markdown="1"><summary>2. Why does the constraint force do no work?</summary>
It is parallel to $\nabla\sigma$, and the constraint $\sigma=0$ for all time implies $\dot\sigma = \sum_i\nabla_i\sigma\cdot\mathbf v_i = 0$. The power $\sum_i\mathbf G_i\cdot\mathbf v_i = -\lambda\sum_i\nabla_i\sigma\cdot\mathbf v_i$ is therefore zero.

Here $\sigma$ is the constraint function, $\nabla_i\sigma$ its gradient with respect to the position of atom $i$, $\mathbf v_i$ the velocity of atom $i$, $\mathbf G_i = -\lambda\nabla_i\sigma$ the constraint force on atom $i$ and $\lambda$ the multiplier. "Power" is the rate at which a force does work, force times velocity.
</details>

<details markdown="1"><summary>3. Does hydrogen mass repartitioning change the free energy difference between two conformations?</summary>
No, to an excellent approximation. Without constraints, configurational free energies depend only on $U(\mathbf r)$. With bond constraints a small mass-dependent factor (the Fixman determinant) appears, which is negligible for bonds to hydrogen. Only kinetic quantities such as rates and diffusion constants change appreciably.
</details>

<details markdown="1"><summary>4. GROMACS prints LINCS warnings and then crashes at step 12 of the first NVT run. What do you do?</summary>
Do not loosen the LINCS settings. Go back: check that energy minimisation converged (maximum force below about 1,000 kJ mol$^{-1}$ nm$^{-1}$), look at the atoms named in the warning for clashes or wrong protonation, check for missing atoms and wrong box size, and try a shorter time step with position restraints for the first picoseconds.
</details>

<details markdown="1"><summary>5. A colleague proposes to replace the constraints on bonds to hydrogen by very stiff harmonic restraints on the same bond lengths. Does this allow a longer time step?</summary>
No. A restraint is a spring, and its frequency is $\omega = \sqrt{k_b/\mu}$, with $k_b$ the stiffness and $\mu$ the reduced mass of the two atoms. A stiffer spring vibrates faster and needs a shorter time step. A constraint removes the vibration altogether, which is why it allows a longer one.
</details>

<details markdown="1"><summary>6. In the SHAKE update, the unconstrained bond is too short. What is the sign of $g$, and which way do the two atoms move?</summary>
The numerator $|\mathbf s'|^2-d^2$ is negative and the denominator is positive, so $g$ is negative. Atom $i$ moves by $-(g/m_i)\,\mathbf s$, which now points along $+\mathbf s$, away from atom $j$. Atom $j$ moves by $+(g/m_j)\,\mathbf s$, along $-\mathbf s$, away from atom $i$. The rod pushes the atoms apart, and the lighter atom moves further.
</details>

<details markdown="1"><summary>7. The largest eigenvalue of the LINCS matrix $\mathbf A$ of some molecule is 0.3 in size. Roughly how large is the error of the series cut after $\mathbf A^4$? What changes if it is 1.2?</summary>
The terms shrink like $0.3^n$. The first neglected term is of size $0.3^5 = 0.0024$, and all neglected terms together are at most $0.3^5/(1-0.3) = 0.0035$, by the geometric series. So the strengths of the corrections are right to a few parts in a thousand.

With 1.2 the terms grow instead of shrinking, and the series cannot be used at all. This is the case of the angle-constrained pentane in the text.
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
