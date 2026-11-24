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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

An MD program does one thing. It takes the positions and velocities of all atoms now, computes where they will be a moment later, and repeats. The moment is called the time step, and the recipe that makes the step is called an integrator. The rule it uses is Newton's second law. The equations that say how positions and velocities change in time are called the equations of motion. So why does this module go on to Lagrange and Hamilton, who wrote the same law in two other ways?

Because the rest of the course is written in their language. Statistical mechanics (Module 3) counts states in "phase space", which is defined with Hamilton's coordinates and momenta. The integrators of Module 4 are derived from Hamilton's equations. Constraints (Module 9), the Nosé thermostat and two barostats (Module 8) are derived from Lagrange's. Neither formulation predicts a different motion from Newton's. They are the same physics, rearranged so that certain questions become easy to answer.

The module has three layers:

1. **Newton.** Forces, potential energy, and why the total energy stays constant.
2. **Lagrange and Hamilton.** The same motion written with energies instead of forces.
3. **What follows from Hamilton's form.** Phase space, conservation laws, Liouville's theorem and time reversibility, and then two applications: vibrations and chaos.

### How to read the formulas

Every displayed formula in this course is followed by a list that says what each letter in it means. The conventions below are used throughout. Each one is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\mathbf r_i$ | A letter in bold is a **vector**: a quantity with a direction, stored as three numbers. $\mathbf r_i = (x_i, y_i, z_i)$ is the position of atom $i$. |
| $i$, $j$ | Labels that number the atoms, from 1 to $N$. $N$ is the number of atoms. |
| $\dot x$ | A dot over a letter is its **time derivative**, $dx/dt$: how fast $x$ is changing at this instant. $\dot{\mathbf r}_i$ is the velocity of atom $i$. |
| $\ddot x$ | Two dots: the time derivative of the time derivative. $\ddot{\mathbf r}_i$ is the acceleration, how fast the velocity is changing. |
| $\sum_i$ | Add up the expression that follows for every value of $i$. |
| $\partial f/\partial x$ | A **partial derivative**: the slope of $f$ when only $x$ changes and every other variable is held fixed. |
| $\mathbf a\cdot\mathbf b$ | The **dot product** of two vectors, $a_xb_x + a_yb_y + a_zb_z$. The result is a single number. |
| $\equiv$ | "Is defined as." |
| $\approx$ | "Is approximately equal to." |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** Physics has more quantities than the alphabet has letters, and the usual names collide. $L$ is the Lagrangian, but $iL$ is the Liouville operator and $\mathbf L$ is the angular momentum. $H$ is the Hamiltonian, but $H_{ab}$ with two labels is the Hessian matrix. $k$ is a spring constant (stiffness) in the spring examples under Newton's formulation and in the section on normal modes, a label for coordinates in the sections between, and a label for the normal modes in $\omega_k$. $\delta$ is the Dirac delta function in $\delta(H-E)$ and a distance between two trajectories in $\delta(t)$ and $\delta_0$. The lists under the formulas say which is meant each time.
</div>

## Newton's formulation

<div data-videos="H0BCYDXEDco 031AX4AsueA mYDrufxpW9E"></div>

An atom keeps moving in a straight line at constant speed unless a force acts on it. A force changes the velocity, and the same force changes the velocity of a heavy atom less than that of a light one. That is the whole content of Newton's second law. For $N$ particles, Newton's second law is $m_i \ddot{\mathbf r}_i = \mathbf F_i$:

$$
m_i\,\ddot{\mathbf r}_i = \mathbf F_i , \qquad i = 1,\dots,N .
$$

<div class="legend" markdown="1">
- $i$: the label of one atom. The equation holds for each atom separately.
- $m_i$: the mass of atom $i$. MD programs use the atomic mass unit, u: hydrogen is about 1 u, carbon about 12 u.
- $\mathbf r_i$: the position of atom $i$, a vector $(x_i, y_i, z_i)$, in nanometres.
- $\ddot{\mathbf r}_i$: the acceleration of atom $i$, the rate at which its velocity $\dot{\mathbf r}_i$ is changing.
- $\mathbf F_i$: the total force on atom $i$ from all the other atoms, a vector.
</div>

Read it as "mass times acceleration equals force", or better, as "acceleration equals force divided by mass". If you know the force on every atom, you know how every velocity is changing, and from the velocities you know how every position is changing. That chain, force to velocity to position, is what an MD program computes at every step.

Because $\mathbf r_i$ and $\mathbf F_i$ are vectors, this is really three equations per atom, one for each of $x$, $y$ and $z$: $3N$ equations in all.

### Potential energy, and what "conservative" means

Where do the forces come from? In MD they all come from one function, the **potential energy** $U$. It assigns a single number, an energy, to every arrangement of the atoms.

Picture a landscape of hills and valleys, where the height at each place is $U$. A ball on this landscape is pushed downhill, and the push is stronger where the ground is steeper. That is the relation between force and potential energy. For one particle moving along a line it reads

$$
F = -\frac{dU}{dx} .
$$

<div class="legend" markdown="1">
- $x$: the position of the particle along the line.
- $U$: the potential energy, a function of $x$.
- $dU/dx$: the derivative of $U$, which is the slope of the landscape at $x$.
- $F$: the force on the particle.
- The minus sign: the force points towards lower energy. Where $U$ rises to the right (positive slope), the force points to the left.
</div>

A spring is the standard example. Its energy is $U = \tfrac12 k x^2$, where $x$ is how far it is stretched and $k$ is its stiffness. The slope is $dU/dx = kx$, so $F = -kx$: stretch it to positive $x$ and the force is negative, pulling back. With $k = 100$ kJ mol$^{-1}$ nm$^{-2}$ and $x = 0.1$ nm, the energy is $\tfrac12\times100\times0.1^2 = 0.5$ kJ/mol and the force is $-100\times0.1 = -10$ kJ mol$^{-1}$ nm$^{-1}$.

<div class="box maths" markdown="1">
**Maths you need here: the partial derivative and the gradient.** With many atoms, $U$ depends on $3N$ numbers, not one, so "the slope of $U$" needs more care.

A **partial derivative**, written $\partial U/\partial x_i$, is the slope of $U$ when you change only $x_i$ and hold every other coordinate still. You compute it like an ordinary derivative, treating all other variables as constants. Example: for $U = x^2 + 3y$, $\partial U/\partial x = 2x$ and $\partial U/\partial y = 3$.

The **gradient** with respect to the position of atom $i$ collects its three partial derivatives into one vector:

$$
\nabla_i U = \left(\frac{\partial U}{\partial x_i},\ \frac{\partial U}{\partial y_i},\ \frac{\partial U}{\partial z_i}\right).
$$

It points in the direction in which $U$ increases fastest when atom $i$ is moved, and its length is the slope in that direction. The symbol $\nabla$ is read "del" or "nabla". More in the [toolbox](maths.html#gradient).
</div>

With the gradient, the one-dimensional rule "force is minus the slope" carries over to any number of atoms. A force is **conservative** if it is the negative gradient of a function of positions only:

$$
\mathbf F_i = -\nabla_i U(\mathbf r_1,\dots,\mathbf r_N).
$$

<div class="legend" markdown="1">
- $\mathbf F_i$: the force on atom $i$.
- $U(\mathbf r_1,\dots,\mathbf r_N)$: the potential energy. The brackets list what it depends on: the positions of all $N$ atoms and nothing else.
- $\nabla_i$: the gradient with respect to the position of atom $i$ (see the box above).
- The minus sign: the force points in the direction in which $U$ decreases fastest.
</div>

"Positions only" is the important condition: $U$ does not depend on the velocities or directly on the time. Friction is the usual example of a force that fails it, because friction depends on the velocity. All force-field forces are of this type, that is, conservative. The name comes from what such forces do to the energy, which is the next point.

### Why the total energy is conserved

A moving atom carries **kinetic energy**, the energy of motion. Summed over all atoms it is

$$
K = \sum_i \tfrac12 m_i \dot{\mathbf r}_i^2 .
$$

<div class="legend" markdown="1">
- $K$: the total kinetic energy.
- $m_i$: the mass of atom $i$.
- $\dot{\mathbf r}_i$: the velocity of atom $i$.
- $\dot{\mathbf r}_i^2$: shorthand for $\dot{\mathbf r}_i\cdot\dot{\mathbf r}_i = \dot x_i^2 + \dot y_i^2 + \dot z_i^2$, the speed squared.
</div>

Think of a ball rolling back and forth in a valley. At the bottom it is fast: much kinetic energy, little potential energy. At the top of its swing it stops for an instant: no kinetic energy, much potential energy. Energy passes back and forth between the two forms, and the sum does not change. The key consequence of having conservative forces is exactly this: conservation of the total energy $E = K + U$ with $K = \sum_i \tfrac12 m_i \dot{\mathbf r}_i^2$.

To prove it, compute how fast $E$ changes in time and show that the answer is zero. Three steps.

**Step 1, the kinetic part.** Take one particle on a line, with mass $m$ and velocity $v$. The derivative of $\tfrac12 m v^2$ with respect to time is $m v\,\dot v$, by the [chain rule](maths.html#chain-rule). For a vector velocity the product becomes a dot product: $m_i\,\dot{\mathbf r}_i\cdot\ddot{\mathbf r}_i$.

**Step 2, the potential part.** $U$ changes in time only because the atoms move. The chain rule for a function of many variables says: add up, for each atom, the slope of $U$ in the direction that atom is moving times how fast it moves. That is $\sum_i \nabla_i U\cdot\dot{\mathbf r}_i$.

**Step 3, use Newton's law.** Replace $m_i\ddot{\mathbf r}_i$ by $\mathbf F_i$ in the first sum, and $\nabla_i U$ by $-\mathbf F_i$ in the second. The two sums cancel:

$$
\frac{dE}{dt} = \sum_i m_i \dot{\mathbf r}_i\cdot\ddot{\mathbf r}_i + \sum_i \nabla_i U\cdot\dot{\mathbf r}_i
= \sum_i \dot{\mathbf r}_i\cdot\left(\mathbf F_i - \mathbf F_i\right) = 0 .
$$

<div class="legend" markdown="1">
- $dE/dt$: the rate of change of the total energy $E = K + U$. Zero means $E$ never changes.
- $m_i$: the mass of atom $i$.
- $\dot{\mathbf r}_i$, $\ddot{\mathbf r}_i$: the velocity and the acceleration of atom $i$.
- $\nabla_i U$: the gradient of the potential energy with respect to the position of atom $i$, equal to $-\mathbf F_i$.
- $\mathbf F_i$: the force on atom $i$.
</div>

This is the first test of any MD code: with no thermostat, the total energy must stay constant apart from small fluctuations from the finite time step. (A thermostat, Module 8, deliberately adds and removes energy to hold the temperature, so the test applies to runs without one.)

### Forces from a pair potential

Most of $U$ is a sum over pairs, $U=\sum_{i<j} u(r_{ij})$ with $r_{ij} = |\mathbf r_i - \mathbf r_j|$. In words: every pair of atoms contributes an energy that depends only on the distance between the two.

<div class="legend" markdown="1">
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once. For three atoms the pairs are 1-2, 1-3 and 2-3.
- $u(r)$: the energy of one pair as a function of its distance, for example the Lennard-Jones function of Module 5.
- $r_{ij}$: the distance between atoms $i$ and $j$. The bars $|\ \ |$ mean "length of the vector".
- $\mathbf r_{ij} = \mathbf r_i - \mathbf r_j$ (bold): the vector that points from atom $j$ to atom $i$. Its length is $r_{ij}$.
</div>

To get the force on atom $i$ we need the gradient of each pair term. The pair energy $u$ depends on the distance $r_{ij}$, and the distance depends on the position of atom $i$. So by the chain rule the gradient is a product of two factors: the slope of $u$ with respect to the distance, $du/dr$, times the rate at which the distance changes when atom $i$ moves, $\partial r_{ij}/\partial \mathbf r_i$.

The second factor is worth doing once by hand. Written out, $r_{ij} = \sqrt{(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2}$. Differentiating the square root with respect to $x_i$ gives $(x_i - x_j)/r_{ij}$, and the same for $y_i$ and $z_i$. Collected into a vector, $\partial r_{ij}/\partial \mathbf r_i = \mathbf r_{ij}/r_{ij}$ with $\mathbf r_{ij} = \mathbf r_i - \mathbf r_j$. This is a vector of length 1 that points from $j$ to $i$. It says something obvious: the distance grows fastest when you move atom $i$ straight away from atom $j$, and then it grows at exactly the rate you move.

Putting the two factors together, by the chain rule,

$$
\mathbf F_i = -\sum_{j\ne i} \frac{du}{dr}\bigg|_{r_{ij}} \frac{\mathbf r_{ij}}{r_{ij}}, \qquad \mathbf F_{ij} = -\mathbf F_{ji}.
$$

<div class="legend" markdown="1">
- $\mathbf F_i$: the total force on atom $i$.
- $\sum_{j\ne i}$: a sum over every other atom $j$.
- $\dfrac{du}{dr}\bigg|_{r_{ij}}$: the slope of the pair energy, evaluated at the present distance $r_{ij}$. The vertical bar means "evaluated at".
- $\mathbf r_{ij}/r_{ij}$: the unit vector (length 1) pointing from $j$ to $i$. It only gives the direction.
- $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$, one term of the sum. $\mathbf F_{ji}$ is the force on $j$ caused by $i$. Swapping the two labels leaves the distance unchanged and reverses the vector, $\mathbf r_{ji} = -\mathbf r_{ij}$, so $\mathbf F_{ji} = -\mathbf F_{ij}$.
</div>

Read the first formula like this. If the pair energy falls when the atoms move apart ($du/dr<0$, the atoms repel), the force on $i$ points along $+\mathbf r_{ij}$, away from $j$. If the energy rises when they move apart ($du/dr>0$, they attract), the force points towards $j$. A pair force always acts along the line joining the two atoms.

The second relation is Newton's third law: the force of $j$ on $i$ is equal and opposite to the force of $i$ on $j$. It means each pair is computed once and applied to both atoms, and it guarantees that the total momentum $\mathbf P = \sum_i m_i \dot{\mathbf r}_i$ is conserved. (Momentum is mass times velocity. The total cannot change because every push on one atom is matched by an opposite push on another.)

## Lagrange's formulation

<div data-videos="OpqJjKDPJBA 3apIZCpmdls"></div>

Newton's law is awkward when the natural coordinates are not Cartesian, for example bond lengths, angles and torsions, or when there are constraints. (Cartesian coordinates are the ordinary $x$, $y$, $z$.) A force is a vector, and rewriting vectors in terms of angles is laborious and error-prone. An energy is a single number and is the same number in any coordinates. Lagrange's formulation gets the equations of motion from energies alone.

It also changes the question. Newton asks, at each instant, "what is the force, and so what is the acceleration?" Lagrange asks about the whole journey: "of all the paths the system could take from here to there, which one does it take?" The answer is given below. It sounds stranger than Newton's law, but it leads to exactly the same motion.

Lagrangian mechanics works in any set of **generalised coordinates** $q_1,\dots,q_n$. These are any $n$ numbers that together fix where everything is: for a pendulum, one angle; for a molecule, its bond lengths, angles and torsions, plus six numbers for where the molecule as a whole is and how it is turned. The number $n$ is the number of **degrees of freedom**, the number of independent ways the system can move. Their time derivatives $\dot q_k$ are the generalised velocities. Define

$$
L(q,\dot q) = K(q,\dot q) - U(q).
$$

<div class="legend" markdown="1">
- $L$: the **Lagrangian**, a function with the unit of energy.
- $q$: shorthand for all the coordinates $q_1,\dots,q_n$ at once.
- $\dot q$: shorthand for all their time derivatives.
- $K(q,\dot q)$: the kinetic energy, written in terms of these coordinates and velocities.
- $U(q)$: the potential energy.
</div>

Note the minus sign. $L$ is kinetic *minus* potential energy, so it is not the total energy, which is $K + U$. The Lagrangian has no simple everyday meaning. It is the quantity that makes the following rule work.

Take any imagined path of the system between a starting time and an end time, and add up $L$ along it. The result, $S=\int L\,dt$, is called the **action** of that path (the integral sign $\int$ means "add up over time"; see the [toolbox](maths.html#integral)). The rule is: the path the system actually follows between two times makes the action $S=\int L\,dt$ stationary. "Stationary" means that a small change of the path does not change $S$, in the same way that the height of a ball at the bottom of a valley hardly changes when you nudge it sideways: the change goes with the square of the nudge, so for a small nudge it is negligible. The condition for that is the Euler-Lagrange equation, one for each coordinate:

$$
\frac{d}{dt}\frac{\partial L}{\partial \dot q_k} - \frac{\partial L}{\partial q_k} = 0 .
$$

<div class="legend" markdown="1">
- $k$: the label of one coordinate, from 1 to $n$. There is one equation per coordinate.
- $\partial L/\partial \dot q_k$: the partial derivative of $L$ with respect to the velocity $\dot q_k$, treating coordinates and velocities as separate variables. It turns out to be the momentum.
- $\dfrac{d}{dt}$ in front of it: then take the rate of change of that quantity in time as the system moves.
- $\partial L/\partial q_k$: the partial derivative of $L$ with respect to the coordinate $q_k$. For a Cartesian coordinate it turns out to be the force. For other coordinates it can also contain a part that comes from the kinetic energy.
</div>

So the equation says "rate of change of momentum equals force". It is Newton's law in disguise, and the Cartesian case shows it. For Cartesian coordinates $L = \sum \tfrac12 m\dot x^2 - U$, so $\partial L/\partial\dot x = m\dot x$ and $\partial L/\partial x = -\partial U/\partial x$, and you recover Newton's law. Here the sum runs over all Cartesian coordinates of all atoms, $x$ stands for any one of them and $m$ is the mass of its atom. In full: the first term of the equation is $\frac{d}{dt}(m\dot x) = m\ddot x$, the second is $-(-\partial U/\partial x)$, so the equation reads $m\ddot x + \partial U/\partial x = 0$, which is $m\ddot x = -\partial U/\partial x = F$.

<details markdown="1"><summary>Optional: where the Euler-Lagrange equation comes from</summary>
Take one coordinate $q(t)$ and change the path slightly, to $q(t) + \epsilon\,\eta(t)$. Here $\eta(t)$ is any smooth function that is zero at the start and the end time, so that the end points stay fixed, and $\epsilon$ is a small number. The velocity along the changed path is $\dot q + \epsilon\,\dot\eta$. The action becomes a function of $\epsilon$, and "stationary" means its derivative with respect to $\epsilon$ is zero at $\epsilon = 0$. By the chain rule, $L$ changes with $\epsilon$ through the coordinate (at the rate $\eta$) and through the velocity (at the rate $\dot\eta$):

$$
\frac{dS}{d\epsilon} = \int \left(\frac{\partial L}{\partial q}\,\eta + \frac{\partial L}{\partial \dot q}\,\dot\eta\right) dt = 0 .
$$

The second term contains $\dot\eta$. [Integration by parts](maths.html#integral) moves the time derivative from $\eta$ onto the other factor, and the boundary term vanishes because $\eta$ is zero at both ends:

$$
\int \left(\frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot q}\right)\eta\; dt = 0 .
$$

This must hold for every choice of $\eta(t)$, which is possible only if the bracket is zero at every time. That is the Euler-Lagrange equation.
</details>

**Why you need this for MD.** Three later topics are written in Lagrangian language:

- constraints (Module 9) are added to $L$ with Lagrange multipliers;
- the Nosé thermostat and the Andersen and Parrinello-Rahman barostats (Module 8) start from "extended Lagrangians", where a thermostat variable or the box itself is given a fictitious mass and a kinetic energy (the Nosé-Hoover equations used in practice are a non-Hamiltonian rewriting of Nosé's, with a conserved extended energy);
- Car-Parrinello ab initio MD does the same for the electronic orbitals.

You do not need to understand these yet, and the names are explained in the modules cited (a barostat, for example, does for the pressure what a thermostat does for the temperature). The same holds for the names in the lists and the table further down this page, such as shadow energy, energy drift and hybrid Monte Carlo: each is explained in the module that the text points to. The point to keep is the recipe: write down a kinetic and a potential energy for whatever you want to move, including invented things such as a thermostat variable, and the Euler-Lagrange equation gives you its equation of motion.

<div class="box key" markdown="1">
**Worked example: a pendulum.** One coordinate, the angle $\theta$. $K = \tfrac12 m l^2\dot\theta^2$, $U = -mgl\cos\theta$. Euler-Lagrange gives $ml^2\ddot\theta + mgl\sin\theta = 0$. Note that the constraint (fixed length $l$) never appears: choosing a coordinate that respects the constraint removes it. This is the idea behind internal-coordinate MD.

The steps. A mass $m$ hangs on a rod of length $l$, and $\theta$ is the angle of the rod from the vertical. $g$ is the acceleration of gravity, 9.81 m/s$^2$.

1. *Kinetic energy.* The mass moves on a circle of radius $l$, so its speed is $l\dot\theta$ and $K = \tfrac12 m (l\dot\theta)^2$.
2. *Potential energy.* The mass is a height $l\cos\theta$ below the pivot. Gravitational energy is $mg$ times height, so $U = -mgl\cos\theta$.
3. *Lagrangian.* $L = \tfrac12 m l^2\dot\theta^2 + mgl\cos\theta$.
4. *The two derivatives.* $\partial L/\partial\dot\theta = ml^2\dot\theta$ and $\partial L/\partial\theta = -mgl\sin\theta$.
5. *Euler-Lagrange.* $\frac{d}{dt}(ml^2\dot\theta) - (-mgl\sin\theta) = 0$, which is the equation above.

With Newton's law in $x$ and $y$, the unknown tension in the rod appears in the equations and has to be eliminated. Here it never appeared.
</div>

## Hamilton's formulation

<div data-videos="61CWqyocuOM hk4fOXsSJzM"></div>

Lagrange describes the state of a system by its coordinates and velocities. Hamilton describes it by coordinates and **momenta**, and builds everything on one function, which turns out to be the total energy. The gain is a pair of equations of a very simple kind: one says how fast each coordinate changes, the other how fast each momentum changes. That is the form a computer needs. Given the coordinates and momenta now, the equations give their rates of change now, and so their values a moment later.

Define the **generalised momentum** conjugate to each coordinate, $p_k = \partial L/\partial \dot q_k$. "Conjugate to" means "belonging to": every coordinate $q_k$ has its own momentum $p_k$. For a Cartesian coordinate it is mass times velocity. For an angle it is an angular momentum: the pendulum above has $p_\theta = ml^2\dot\theta$. Then define the Hamiltonian by a Legendre transform:

$$
H(q,p) = \sum_k p_k\dot q_k - L(q,\dot q).
$$

<div class="legend" markdown="1">
- $H$: the **Hamiltonian**, a function of the coordinates and the momenta.
- $q$, $p$: shorthand for all coordinates and all momenta.
- $\sum_k$: a sum over all the coordinates, $k = 1,\dots,n$.
- $p_k$: the momentum conjugate to coordinate $q_k$, defined as $\partial L/\partial\dot q_k$.
- $\dot q_k$: the velocity of coordinate $k$. In $H$ it must be rewritten in terms of the momenta, so that no velocity is left.
- $L$: the Lagrangian of the previous section.
</div>

<div class="box maths" markdown="1">
**Maths you need here: the Legendre transform.** It is a standard way to change which variable a function depends on: from a variable (here the velocity $\dot q$) to the slope of the function with respect to that variable (here $p = \partial L/\partial\dot q$), without losing information. Thermodynamics uses the same step to go from the energy to a free energy (free energies are the subject of Module 3). You do not need the general theory. You need to see it work once.

One particle on a line: $L = \tfrac12 m\dot x^2 - U(x)$. The momentum is $p = \partial L/\partial\dot x = m\dot x$, so $\dot x = p/m$. Then

$$
H = p\,\dot x - L = \frac{p^2}{m} - \left(\frac{p^2}{2m} - U\right) = \frac{p^2}{2m} + U .
$$

The first term is the kinetic energy written with the momentum instead of the velocity ($\tfrac12 m v^2$ with $v = p/m$). So $H$ is kinetic plus potential energy. More in the [toolbox](maths.html#legendre).
</div>

The same happens with many atoms. For Cartesian coordinates $p = m\dot x$ and

$$
H(\mathbf r,\mathbf p) = \sum_i \frac{\mathbf p_i^2}{2m_i} + U(\mathbf r) = K + U ,
$$

the total energy.

<div class="legend" markdown="1">
- $\mathbf r$: all the atomic positions together.
- $\mathbf p$: all the momenta together.
- $\mathbf p_i$: the momentum of atom $i$, equal to $m_i\dot{\mathbf r}_i$.
- $\mathbf p_i^2$: shorthand for $\mathbf p_i\cdot\mathbf p_i$.
- $\mathbf p_i^2/2m_i$: the kinetic energy of atom $i$.
- $K$, $U$: the total kinetic and potential energies.
</div>

The equations of motion become two first-order equations per degree of freedom:

$$
\dot q_k = \frac{\partial H}{\partial p_k}, \qquad \dot p_k = -\frac{\partial H}{\partial q_k}.
$$

<div class="legend" markdown="1">
- $\dot q_k$: the rate of change of coordinate $k$.
- $\dot p_k$: the rate of change of its momentum.
- $\partial H/\partial p_k$: the slope of $H$ with respect to the momentum $p_k$, everything else held fixed.
- $\partial H/\partial q_k$: the slope of $H$ with respect to the coordinate $q_k$.
</div>

<details markdown="1"><summary>Optional: where Hamilton's equations come from</summary>
Take one coordinate. In $H = p\,\dot q - L(q,\dot q)$ the velocity $\dot q$ is not an independent variable: it has been rewritten as a function of $q$ and $p$. Differentiate $H$ with respect to $p$, holding $q$ fixed, using the product rule for the first term and the chain rule for $L$:

$$
\frac{\partial H}{\partial p} = \dot q + p\,\frac{\partial\dot q}{\partial p} - \frac{\partial L}{\partial\dot q}\,\frac{\partial\dot q}{\partial p} = \dot q .
$$

The last two terms cancel because $\partial L/\partial\dot q$ is the momentum $p$ by definition. This is the first of Hamilton's equations. Now differentiate with respect to $q$, holding $p$ fixed:

$$
\frac{\partial H}{\partial q} = p\,\frac{\partial\dot q}{\partial q} - \frac{\partial L}{\partial q} - \frac{\partial L}{\partial\dot q}\,\frac{\partial\dot q}{\partial q} = -\frac{\partial L}{\partial q} .
$$

Again the first and the last term cancel. The Euler-Lagrange equation says that $\partial L/\partial q$ equals $\frac{d}{dt}(\partial L/\partial\dot q)$, which is $\dot p$. So $\partial H/\partial q = -\dot p$, the second of Hamilton's equations.
</details>

These are **Hamilton's equations**. "First-order" means that only first time derivatives (single dots) appear. Newton's law is second-order because it contains the acceleration, a double dot. One second-order equation has been traded for two first-order ones, which is always possible and is what numerical methods work with.

For the Cartesian Hamiltonian these read $\dot{\mathbf r}_i = \mathbf p_i/m_i$ and $\dot{\mathbf p}_i = -\nabla_i U = \mathbf F_i$: the "drift" and the "kick" of the velocity Verlet algorithm. (Velocity Verlet is the integrator derived in Module 4.) To see where they come from, differentiate $H = \sum_i \mathbf p_i^2/2m_i + U$. With respect to $\mathbf p_i$, only the kinetic term depends on it and gives $\mathbf p_i/m_i$, the velocity. With respect to $\mathbf r_i$, only $U$ depends on it and gives $\nabla_i U$. So the first equation says "the position changes at the velocity" and the second says "the momentum changes at the force". In an MD step, moving the positions with the current velocities is called the drift, and changing the momenta with the current forces is called the kick. The Hamiltonian form is the one used by statistical mechanics (Module 3) and by the theory of integrators (Module 4).

### Phase space

<div data-videos="IVQRfHAgLxk yV25sV3rAlo"></div>

A photograph of a ball in the air does not tell you where it will land. You also need to know how it is moving. In the same way, the positions of all atoms are not the full state of a system. The full state is the positions and the momenta together.

The state of the system at one instant is the full set of positions and momenta, a single point $\Gamma = (\mathbf r_1,\dots,\mathbf r_N,\mathbf p_1,\dots,\mathbf p_N)$ in a $6N$-dimensional space called **phase space**.

<div class="legend" markdown="1">
- $\Gamma$ (capital Greek gamma): one complete state of the system, a list of $6N$ numbers.
- $\mathbf r_1,\dots,\mathbf r_N$: the positions of the $N$ atoms, three numbers each.
- $\mathbf p_1,\dots,\mathbf p_N$: their momenta, three numbers each.
- $6N$: three position and three momentum components per atom.
</div>

Nobody can picture a space with $6N$ dimensions, and you do not have to. "A point in phase space" is just a compact way of saying "one complete set of positions and momenta". For one particle on a line there are only two numbers, $x$ and $p$, and phase space is an ordinary plane with $x$ on the horizontal axis and $p$ on the vertical one. The demo further down draws that plane.

A trajectory is a curve in phase space: as time passes, the point $\Gamma$ moves. Because Hamilton's equations are first order, one curve passes through each point: trajectories never cross. The reason is that the point itself fixes its rates of change through Hamilton's equations, so from any state there is only one way to continue.

For a one-dimensional harmonic oscillator the trajectory is an ellipse in the $(x,p)$ plane, and its area is $2\pi E/\omega$. A harmonic oscillator is a mass on a spring, with $H = p^2/2m + \tfrac12 m\omega^2x^2$, where $\omega$ is its angular frequency ($2\pi$ divided by the period of oscillation). Since the energy is conserved, the point $(x,p)$ must stay on the curve $p^2/2m + \tfrac12 m\omega^2 x^2 = E$, and that is the equation of an ellipse. It reaches out to $x_{\max} = \sqrt{2E/m\omega^2}$ along the $x$ axis (where $p=0$) and to $p_{\max} = \sqrt{2mE}$ along the $p$ axis (where $x=0$). The area of an ellipse is $\pi$ times the product of the two, which gives $2\pi E/\omega$.

### Time evolution of any observable

<div data-videos="5OZO5GPuSJY"></div>

An **observable** is any quantity you can compute from the positions and momenta: the energy, the distance between two atoms, the radius of a protein. As the system moves, its value changes. This section finds a general formula for how fast. The formula then gives a compact way of writing "advance the system by a time $t$", and Module 4 derives the integrators from it.

This is the most abstract part of the module. If it is heavy on a first reading, two things are enough to take away: there is an operation, written $iL$, that gives the rate of change of any observable, and it is the sum of two parts, one that moves the positions and one that changes the momenta.

For a function $A(q,p)$ with no explicit time dependence (the formula for $A$ contains the coordinates and momenta but not $t$ itself, so $A$ changes only because they change),

$$
\frac{dA}{dt} = \sum_k\left(\frac{\partial A}{\partial q_k}\dot q_k + \frac{\partial A}{\partial p_k}\dot p_k\right)
= \sum_k\left(\frac{\partial A}{\partial q_k}\frac{\partial H}{\partial p_k} - \frac{\partial A}{\partial p_k}\frac{\partial H}{\partial q_k}\right) \equiv \{A,H\}.
$$

<div class="legend" markdown="1">
- $A$: any observable, a function of the coordinates $q$ and momenta $p$.
- $\sum_k$: a sum over all degrees of freedom, $k = 1,\dots,n$.
- $dA/dt$: how fast the value of $A$ changes as the system moves.
- $\partial A/\partial q_k$, $\partial A/\partial p_k$: the slopes of $A$ with respect to one coordinate or one momentum.
- $\dot q_k$, $\dot p_k$: how fast that coordinate and that momentum are changing.
- $H$: the Hamiltonian.
- $\{A,H\}$: the **Poisson bracket** of $A$ and $H$. It is only a name for the sum in the middle.
</div>

The three parts of the line are three steps. The first equality is the chain rule: $A$ changes because every $q_k$ and every $p_k$ changes, and each contributes "slope times rate". The second replaces $\dot q_k$ and $\dot p_k$ using Hamilton's equations. The third gives the result a name. The bracket $\{A,H\}$ is the Poisson bracket.

Two quick checks that it behaves sensibly, for one particle on a line. Take $A = x$: then $\partial A/\partial x = 1$ and $\partial A/\partial p = 0$, so $\{x,H\} = \partial H/\partial p = p/m$, the velocity, as it should be. Take $A = H$: the two terms are identical and cancel, so $\{H,H\} = 0$ and the energy does not change.

<div class="box maths" markdown="1">
**Maths you need here: operators, and the exponential of an operator.** An **operator** is a rule that turns one function into another. "Differentiate with respect to $x$" is an operator: it turns $x^2$ into $2x$. "Take the Poisson bracket with $H$" is another one: it turns an observable $A$ into its rate of change.

For an ordinary number $a$, the equation $dA/dt = aA$ has the solution $A(t) = e^{at}A(0)$: exponential growth. The exponential can be written as a series, $e^{at} = 1 + at + \tfrac12 (at)^2 + \dots$ The same series makes sense with an operator in place of the number, where "squared" means "apply it twice". So the solution of $dA/dt = (\text{operator})A$ can be written in the same form, with the operator in the exponent. More in the [toolbox](maths.html#operators).
</div>

It is convenient to define the **Liouville operator** $iL$ by $iL\,A = \{A,H\}$, so that $\dot A = iL\,A$ with the formal solution

$$
A(t) = e^{iLt}A(0).
$$

<div class="legend" markdown="1">
- $iL$: the Liouville operator, the rule "take the Poisson bracket with $H$". Treat $iL$ as one symbol. The $i$ is the square root of $-1$ (see the toolbox on [complex numbers](maths.html#complex)) and is there by a convention taken from quantum mechanics. You never compute with it here. This $L$ is not the Lagrangian.
- $A(0)$: the value of the observable at the starting state.
- $A(t)$: its value after the system has moved for a time $t$.
- $e^{iLt}$: the **propagator**, the operator that advances the system by a time $t$. It is defined by the series in the box above.
</div>

"Formal solution" means that the expression is correct but cannot be evaluated directly for a real system. Its use is as a starting point: Module 4 replaces $e^{iLt}$ by an approximation that can be computed, and that approximation is the integrator.

For the Cartesian Hamiltonian,

$$
iL = \underbrace{\sum_i \frac{\mathbf p_i}{m_i}\cdot\frac{\partial}{\partial \mathbf r_i}}_{iL_r} + \underbrace{\sum_i \mathbf F_i\cdot\frac{\partial}{\partial \mathbf p_i}}_{iL_p}.
$$

<div class="legend" markdown="1">
- $\mathbf p_i/m_i$: the velocity of atom $i$.
- $\partial/\partial\mathbf r_i$: "take the gradient with respect to the position of atom $i$". It is a derivative waiting for a function to act on.
- $\mathbf F_i$: the force on atom $i$.
- $\partial/\partial\mathbf p_i$: the same for the momentum of atom $i$.
- $iL_r$: the name of the first part. It gives the change of an observable caused by the positions moving at their velocities.
- $iL_p$: the name of the second part. It gives the change caused by the momenta changing under the forces.
- The braces underneath only attach the two names. They are not part of the formula.
</div>

This is the Poisson bracket of the previous formula with $\partial H/\partial\mathbf p_i = \mathbf p_i/m_i$ and $-\partial H/\partial\mathbf r_i = \mathbf F_i$ filled in. Keep this splitting in mind. In Module 4 the velocity Verlet algorithm falls out of it in two lines. The reason it is useful: each part on its own can be solved exactly. With $iL_r$ alone, the atoms move in straight lines at constant velocity (the drift). With $iL_p$ alone, the positions stand still and each momentum changes by force times time (the kick). The integrator alternates the two.

## Conservation laws

<div data-videos="HLr5ZeQUrBk PuDproV-17s ojEwHlyty4Q"></div>

A conserved quantity is one whose value never changes during the motion. Conserved quantities are the first thing to check in a simulation, because a quantity that should be constant and is not points to an error. Since $dA/dt = \{A,H\}$, a quantity $A$ is conserved when $\{A,H\}=0$.

Each conservation law comes from a symmetry of $H$ (Noether's theorem). A **symmetry** is a change you can make to the whole system that leaves $H$ exactly as it was. For example, shift every atom by the same amount in the same direction. No distance between atoms changes, so $U$ does not change, and neither does $K$. The theorem says that this symmetry is the reason the total momentum is conserved.

| Symmetry of $H$ | Conserved quantity | In an MD simulation |
|---|---|---|
| No explicit time dependence | Energy $H$ | Conserved in NVE up to integration error. Not conserved with a thermostat (but an extended energy often is). |
| Translation of all particles | Total linear momentum $\mathbf P$ | Conserved with periodic boundaries. Codes set it to zero at the start and remove any numerical drift ("centre-of-mass motion removal"). |
| Rotation of all particles | Total angular momentum $\mathbf L$ | **Not** conserved with periodic boundaries, because a cubic box is not rotationally symmetric. Conserved in vacuum or droplet simulations. |

<div class="legend" markdown="1">
- $\mathbf P = \sum_i \mathbf p_i$: the total linear momentum, the sum of the momenta of all atoms.
- $\mathbf L = \sum_i \mathbf r_i\times\mathbf p_i$: the total angular momentum, a measure of how much the system as a whole is rotating about the origin. The $\times$ is the [cross product](maths.html#cross-product) of two vectors. This $\mathbf L$ is not the Lagrangian.
- NVE: a simulation with constant number of atoms $N$, volume $V$ and energy $E$, that is, one without a thermostat or barostat (Module 3).
- Periodic boundaries: the simulation box is surrounded by copies of itself, so an atom that leaves through one face comes back in through the opposite one (Module 7).
</div>

The number of conserved quantities affects the number of degrees of freedom used to compute the temperature (Module 3): $3N - 3$ in a periodic box with no constraints. The reason is that the three components of the total momentum are held at zero, which removes three of the $3N$ independent ways the atoms can move.

## Liouville's theorem

<div data-videos="MFqA1nePCNg ddKRdrf9iqI XiFEXVWNlpg 8w4az6IQsNc lQIbcV6dQzw"></div>

So far we followed one system. Now imagine very many copies of it, each started from slightly different positions and momenta. In phase space they form a cloud of points. As time passes each point follows its own trajectory and the cloud changes shape.

Liouville's theorem says that the cloud can be deformed but not compressed or expanded: the volume it occupies in phase space stays the same. Think of a drop of ink stirred into water. It is drawn out into long thin threads, yet the amount of ink is what it was.

There are two reasons to care. Statistical mechanics assigns probabilities to regions of phase space, and those probabilities would not be stable if the motion squeezed or inflated the regions. And the theorem names a property that a numerical integrator should share with the true motion.

Consider not one system but a cloud of systems with slightly different initial conditions, described by a density $\rho(\Gamma,t)$ in phase space. The density says how many of the copies are found, at time $t$, in a small region around the point $\Gamma$, per unit volume of that region. The cloud moves with "velocity" $\dot\Gamma = (\dot q,\dot p)$: at each point of phase space, Hamilton's equations give the rates of change of all coordinates and momenta, and together these rates say where the point moves next.

<div class="box maths" markdown="1">
**Maths you need here: the divergence.** Take any flow, such as water in a river, with a velocity at each place. The **divergence** of the flow at a point measures whether the flow is spreading out from that point (positive), closing in on it (negative) or neither (zero). You compute it by adding up, for every direction, the derivative of that component of the velocity with respect to its own coordinate.

In one dimension: if the velocity is $v(x) = ax$ with $a > 0$, points further from the origin move faster, so a blob of points gets stretched. The divergence is $dv/dx = a$, positive. A flow whose divergence is zero everywhere is called **incompressible**: any blob keeps its volume. More in the [toolbox](maths.html#divergence).
</div>

The divergence of this velocity field is

$$
\nabla_\Gamma\cdot\dot\Gamma = \sum_k \left(\frac{\partial \dot q_k}{\partial q_k} + \frac{\partial \dot p_k}{\partial p_k}\right)
= \sum_k \left(\frac{\partial^2 H}{\partial q_k\partial p_k} - \frac{\partial^2 H}{\partial p_k\partial q_k}\right) = 0 .
$$

<div class="legend" markdown="1">
- $\nabla_\Gamma\cdot$: the divergence in phase space. The "directions" are all the coordinates $q_k$ and all the momenta $p_k$.
- $\dot\Gamma$: the velocity of a point in phase space, made of all the $\dot q_k$ and $\dot p_k$.
- $\sum_k$: a sum over all degrees of freedom, $k = 1,\dots,n$.
- $H$: the Hamiltonian.
- $\partial\dot q_k/\partial q_k$: how the rate of change of coordinate $k$ varies when that coordinate itself is varied. Likewise for $\partial\dot p_k/\partial p_k$.
- $\dfrac{\partial^2 H}{\partial q_k\partial p_k}$: a second partial derivative. Differentiate $H$ with respect to $p_k$, then differentiate the result with respect to $q_k$.
</div>

The steps: the first equality is the definition of the divergence. The second uses Hamilton's equations, $\dot q_k = \partial H/\partial p_k$ and $\dot p_k = -\partial H/\partial q_k$. The last uses the fact that for a smooth function the order of two partial derivatives does not matter, so the two terms in each bracket are equal and cancel.

The flow in phase space is **incompressible**. A blob of initial conditions changes shape, often into something very stretched and folded, but its volume stays the same. Combining this with conservation of the number of systems (copies are neither created nor destroyed) gives the Liouville equation

$$
\frac{\partial\rho}{\partial t} = -\{\rho,H\} = -iL\rho, \qquad\text{equivalently}\qquad \frac{d\rho}{dt}=0 \text{ along a trajectory.}
$$

<div class="legend" markdown="1">
- $\rho$: the density of copies in phase space, a function of the point $\Gamma$ and the time $t$.
- $\partial\rho/\partial t$: the rate of change of the density at a fixed point of phase space, as if you stood still and watched the cloud flow past.
- $\{\rho,H\}$: the Poisson bracket of the density with the Hamiltonian.
- $iL$: the Liouville operator.
- $d\rho/dt$ along a trajectory: the rate of change of the density seen while moving with one of the copies.
</div>

The second form is the easier one to remember: travelling with the flow, you see the density around you stay the same for ever.

Where the first form comes from. At a fixed point of phase space the density changes only because the flow carries copies past it, at the rate $-\sum_k(\dot q_k\,\partial\rho/\partial q_k + \dot p_k\,\partial\rho/\partial p_k)$. No other term appears, because an incompressible flow does not pile copies up or thin them out. Replace $\dot q_k$ and $\dot p_k$ using Hamilton's equations and the sum becomes the Poisson bracket, which gives $\partial\rho/\partial t = -\{\rho,H\}$.

Two consequences matter for simulation:

1. **Any density that depends on $\Gamma$ only through $H$ is stationary**, since then $\{\rho(H),H\}=0$. The microcanonical density $\delta(H-E)$ and the canonical density $e^{-\beta H}$ are both of this kind. This is why Hamiltonian dynamics is compatible with the equilibrium ensembles.
2. **A good integrator should also preserve the Hamiltonian structure of phase space.** Integrators that do are called symplectic. They preserve phase-space volume, and they preserve more than that (the sum of the oriented areas $dq_k\,dp_k$), and it is this stronger property that gives them a conserved "shadow" energy (Module 4). Integrators without it (for example forward Euler or the classical explicit Runge-Kutta methods) make the cloud grow or shrink steadily, which shows up as an energy drift.

Some words in these two points need explaining.

*Stationary* means "does not change in time". A stationary density describes equilibrium: the copies keep moving, but the cloud as a whole looks the same at all times. The bracket vanishes because of the chain rule: $\{\rho(H),H\} = \rho'(H)\,\{H,H\}$, where $\rho'$ is the derivative of $\rho$ with respect to its argument, and $\{H,H\}=0$.

*The two densities* are the subject of Module 3. $\delta(H-E)$ uses the [Dirac delta](maths.html#delta), an infinitely narrow peak: it is zero unless its argument is zero, and the area under it is 1. It describes copies that all have exactly the energy $E$. In $e^{-\beta H}$, $\beta = 1/k_BT$, where $T$ is the temperature and $k_B$ the Boltzmann constant. It describes copies at a fixed temperature, where states of high energy are exponentially rarer. An *ensemble* is the name for such a collection of copies.

*Symplectic* is the technical word for "keeps the special structure that Hamilton's equations give to phase space". To picture the oriented areas, take a small two-dimensional patch of the cloud and look at its shadow on each $(q_k,p_k)$ plane, one plane per degree of freedom. The oriented area is the area of that shadow, with a plus or a minus sign that depends on which way round the edge of the patch runs in that plane. A symplectic integrator keeps the sum of these areas over all the planes constant, for every such patch. You do not need the precise definition, only the consequence in Module 4.

*Forward Euler* is the simplest possible integrator: it computes the new positions and the new velocities both from the old values. The demo below does not use it: it shows a cloud of starting points that keeps its area under Hamilton's equations and loses area when you switch on friction. The integrator demo of [Module 4](04-integrators.html) compares forward Euler with velocity Verlet.

<div class="widget" data-widget="liouville"></div>

## Time reversibility

<div data-videos="sg15UClUY48"></div>

Film two billiard balls colliding and run the film backwards. The reversed film shows a collision that could equally well have happened: nothing in it breaks the laws of motion. The same is true of atoms moving under conservative forces.

Hamilton's equations are symmetric under $t\to -t$, $\mathbf p \to -\mathbf p$. That is, if you replace the time by minus the time and every momentum by minus itself, you get the same equations back. Check it on $\dot q_k = \partial H/\partial p_k$: reversing time changes the sign of the left side, reversing $p_k$ changes the sign of the right side, and the two changes cancel. In $\dot p_k = -\partial H/\partial q_k$ the left side changes sign twice and the right side not at all. (This needs $H$ to be the same for $\mathbf p$ and $-\mathbf p$, which it is, because the momenta enter as $\mathbf p^2$.)

If you stop a simulation, flip all velocities and continue, an exact solution retraces its path. Velocity Verlet has the same symmetry in exact arithmetic. In practice round-off error and chaos destroy the retracing after a few hundred steps, but the symmetry of the algorithm still protects it from systematic drift. (Round-off error is the small error made because a computer stores numbers with about 16 digits. Chaos is explained in the last section.) It also matters for Monte Carlo schemes that use MD moves (hybrid Monte Carlo), which need a reversible, volume-preserving integrator to satisfy detailed balance. Detailed balance is the condition, met again in Module 14, that at equilibrium every move happens as often as its reverse.

## Small oscillations and normal modes

Near the bottom of any smooth valley, the ground looks like a parabola. So a molecule close to an energy minimum behaves like a set of masses joined by springs, whatever the true shape of $U$ further away. This section turns that statement into vibration frequencies. They matter in MD because the fastest vibration decides how long a time step can be.

<div class="box maths" markdown="1">
**Maths you need here: the Taylor expansion.** Close to a point $x_0$, a smooth function can be approximated by a polynomial built from its derivatives at that point:

$$
f(x_0 + \Delta) \approx f(x_0) + f'(x_0)\,\Delta + \tfrac12 f''(x_0)\,\Delta^2 .
$$

Here $\Delta$ is a small step away from $x_0$, $f'$ is the slope and $f''$ the curvature (the derivative of the slope). At a minimum the slope is zero, so the first term that changes with $\Delta$ is the quadratic one. That term is the energy of a spring, $\tfrac12 k\Delta^2$, with stiffness $k = f''(x_0)$. More in the [toolbox](maths.html#taylor).
</div>

Near a minimum $\mathbf r_0$, expand $U$ to second order:

$$
U(\mathbf r) \approx U(\mathbf r_0) + \tfrac12 \sum_{ab} H_{ab}\,\Delta r_a \Delta r_b,\qquad H_{ab} = \frac{\partial^2 U}{\partial r_a\partial r_b}\bigg|_{\mathbf r_0}.
$$

<div class="legend" markdown="1">
- $\mathbf r$: all $3N$ atomic coordinates, written as one long list.
- $\mathbf r_0$: their values at the energy minimum.
- $a$, $b$: labels that run over the $3N$ coordinates (not over atoms).
- $\Delta r_a$: the displacement of coordinate $a$ from its value at the minimum.
- $\sum_{ab}$: a double sum. $a$ and $b$ each run over all $3N$ coordinates, so every combination appears, including $a = b$ and both orders, $ab$ and $ba$.
- $H_{ab}$: the **Hessian**, a table (matrix) with $3N$ rows and $3N$ columns holding all second derivatives of $U$ at the minimum. The vertical bar means "evaluated at $\mathbf r_0$".
</div>

There is no term with a single $\Delta r_a$ because at a minimum all first derivatives of $U$, the forces, are zero. A diagonal entry $H_{aa}$ is the stiffness for moving coordinate $a$ alone. An off-diagonal entry $H_{ab}$ says how much moving coordinate $b$ changes the force along coordinate $a$: it is the coupling between the two.

$H_{ab}$ is the Hessian (not the Hamiltonian). Newton's law for coordinate $a$ in this quadratic energy is $m_a\,\Delta\ddot r_a = -\sum_b H_{ab}\,\Delta r_b$, where $m_a$ is the mass of the atom that coordinate $a$ belongs to. The masses are a nuisance because they differ from atom to atom. They can be absorbed into the coordinates. In mass-weighted coordinates $\tilde r_a = \sqrt{m_a}\,\Delta r_a$, the equations of motion are $\ddot{\tilde{\mathbf r}} = -\tilde{\mathbf H}\tilde{\mathbf r}$ with $\tilde H_{ab} = H_{ab}/\sqrt{m_a m_b}$.

<div class="legend" markdown="1">
- $\tilde r_a$: the mass-weighted displacement of coordinate $a$. The tilde marks "mass-weighted".
- $\tilde{\mathbf r}$: the list of all $3N$ of them.
- $\tilde{\mathbf H}$: the mass-weighted Hessian matrix, with entries $\tilde H_{ab}$.
- $\tilde{\mathbf H}\tilde{\mathbf r}$: the matrix multiplied by the list, which gives a new list whose entry $a$ is $\sum_b \tilde H_{ab}\tilde r_b$.
</div>

The step in full. Put $\Delta r_a = \tilde r_a/\sqrt{m_a}$ and $\Delta r_b = \tilde r_b/\sqrt{m_b}$ into Newton's law above. The left side becomes $\sqrt{m_a}\,\ddot{\tilde r}_a$ and the right side $-\sum_b H_{ab}\,\tilde r_b/\sqrt{m_b}$. Divide both sides by $\sqrt{m_a}$ and you get $\ddot{\tilde r}_a = -\sum_b \tilde H_{ab}\,\tilde r_b$ with $\tilde H_{ab} = H_{ab}/\sqrt{m_a m_b}$.

<div class="box maths" markdown="1">
**Maths you need here: eigenvalues and eigenvectors.** A matrix multiplied by a vector gives another vector, usually pointing in a different direction. For certain special vectors the direction is kept and the vector is only multiplied by a number. Such a vector is an **eigenvector** of the matrix, and the number is its **eigenvalue**. "Diagonalising" a matrix means finding all of them, which every numerical library can do. More in the [toolbox](maths.html#eigen).
</div>

Diagonalising $\tilde{\mathbf H}$ gives eigenvalues $\omega_k^2$ and eigenvectors, the **normal modes**: independent harmonic oscillators with frequency $\omega_k$. Here $k$ labels the modes, and $\omega_k$ is the angular frequency of mode $k$. Each eigenvector is a pattern of motion in which all atoms swing in step at one frequency, such as the symmetric stretch of a water molecule. Along an eigenvector the equation of motion reduces to that of a single spring, with $\omega_k^2$ in the place of stiffness over mass, and any small vibration of the molecule is a sum of such patterns, each going on as if the others were not there.

Why this matters here:

- the highest $\omega_k$ sets the largest stable time step (Module 4): for one harmonic bond between masses $m_1$ and $m_2$, $\omega = \sqrt{k/\mu}$ with reduced mass $\mu = m_1m_2/(m_1+m_2)$. A light hydrogen gives a small $\mu$ and a high frequency;
- the lowest-frequency modes are the collective motions, and normal-mode analysis and elastic network models use them directly;
- the harmonic approximation gives a formula for vibrational entropy that is used in some end-point free-energy methods.

<div class="legend" markdown="1">
- $\omega$: the angular frequency of the bond vibration, in radians per unit of time. The period of one oscillation is $2\pi/\omega$.
- $k$: here the spring constant (stiffness) of the bond.
- $m_1$, $m_2$: the masses of the two bonded atoms.
- $\mu$: the **reduced mass**, the effective mass of the relative motion of the two atoms. It is always smaller than the lighter of the two masses.
</div>

<div class="box key" markdown="1">
**Worked example: the period of a C-H stretch.** With $k \approx 2.8\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ (a typical force-field value in the convention $U=\tfrac12 k(r-r_0)^2$) and $\mu = 12\times1/13 = 0.923$ u, the angular frequency is $\omega = \sqrt{k/\mu} = \sqrt{2.8\times10^5/0.923}\ \text{ps}^{-1} \approx 551\ \text{ps}^{-1}$. The period is $2\pi/\omega \approx 0.0114$ ps $= 11.4$ fs. Ten steps per period means a time step near 1 fs.

In the formula for $U$, $r$ is the length of the bond and $r_0$ is its length at the energy minimum. Two remarks on the arithmetic. The reduced mass uses 12 u for carbon and 1 u for hydrogen. And the units work out without any conversion factor, because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$. Dividing kJ mol$^{-1}$ nm$^{-2}$ by u therefore leaves ps$^{-2}$, and the square root is in ps$^{-1}$. This is why this course uses nm, ps, u and kJ/mol together (see the [primer](physics.html#units)). Programs that work in ångström and kcal/mol need a conversion factor in this formula.
</div>

## Chaos, and why MD still works

Weather forecasts fail after a week or two because a tiny uncertainty in today's weather grows until it dominates. Atoms in a liquid behave the same way, on a time scale of picoseconds instead of days.

Many-particle systems are chaotic: two trajectories that start a tiny distance $\delta_0$ apart separate as $\delta(t)\approx\delta_0 e^{\lambda t}$, where $\lambda$ is the largest Lyapunov exponent.

<div class="legend" markdown="1">
- $\delta_0$: the distance in phase space between two trajectories at the start.
- $\delta(t)$: their distance after a time $t$.
- $\lambda$: the largest **Lyapunov exponent**, the rate of the exponential growth, in units of one over time. After a time $1/\lambda$ the distance has grown by a factor $e \approx 2.7$.
- $e^{\lambda t}$: the exponential function. It multiplies by the same factor in every equal interval of time.
</div>

For a liquid, $1/\lambda$ is of the order of a picosecond. Round-off error at the 16th digit therefore grows to order one within a few tens of picoseconds. The arithmetic: an error of relative size $10^{-16}$ has to grow by a factor $10^{16}$, which takes $t = \ln(10^{16})/\lambda \approx 37/\lambda$, about 37 ps if $1/\lambda$ is 1 ps. Two consequences:

- A simulated trajectory is **not** the true trajectory from those initial conditions beyond a few picoseconds. Running the same input on two machines, or on a different number of processors, gives different trajectories.
- This does not matter for what MD is used for. We want statistical properties, and a numerical trajectory stays close to *some* true trajectory of a slightly modified Hamiltonian (the "shadow" Hamiltonian of Module 4). Averages over long trajectories are reproducible even though individual trajectories are not.

In practice, chaos is useful: starting copies of a system with different random velocities gives runs whose fast motions are statistically independent within a short time. Copies started from the same structure still share its conformational basin, so for slow motions independent runs should also start from different structures. (A conformational basin is one valley of the energy landscape, for example one folded shape of a protein. Getting out of it can take far longer than the simulation.)

## Check yourself

<details markdown="1"><summary>1. Show that the total momentum is conserved when all forces are pair forces.</summary>
$\dot{\mathbf P} = \sum_i \mathbf F_i = \sum_i\sum_{j\ne i}\mathbf F_{ij}$. Each pair appears twice, as $\mathbf F_{ij}$ and $\mathbf F_{ji} = -\mathbf F_{ij}$, so the sum is zero.
</details>

<details markdown="1"><summary>2. Write Hamilton's equations for the one-dimensional harmonic oscillator and solve them.</summary>
$H = p^2/2m + \tfrac12 m\omega^2x^2$. $\dot x = p/m$, $\dot p = -m\omega^2 x$. So $\ddot x = -\omega^2x$ and $x(t) = x_0\cos\omega t + (p_0/m\omega)\sin\omega t$, $p(t) = p_0\cos\omega t - m\omega x_0\sin\omega t$. Here $x_0$ and $p_0$ are the position and the momentum at $t = 0$. In the $(x,p)$ plane this is an ellipse traversed clockwise.
</details>

<details markdown="1"><summary>3. Why is angular momentum not conserved in a periodic box?</summary>
Conservation of angular momentum follows from invariance under rotation. A periodic lattice of cubic boxes is invariant only under a few discrete rotations. Equivalently, when a particle leaves through one face and re-enters through the opposite one, its position vector jumps while its momentum does not, so $\mathbf r\times\mathbf p$ jumps.
</details>

<details markdown="1"><summary>4. A friction force $-\gamma \mathbf p$ is added to $\dot{\mathbf p}$. What happens to phase-space volume?</summary>
The divergence becomes $\sum_k \partial(-\gamma p_k)/\partial p_k = -n\gamma$ for $n$ degrees of freedom, so volume contracts as $e^{-n\gamma t}$. Here $\gamma$ is the friction coefficient, in units of one over time. Friction alone cools the system to zero temperature. A thermostat must add something that compensates: random kicks in Langevin dynamics, or a friction coefficient that changes sign in Nosé-Hoover dynamics (Module 8).
</details>

## Exercises

1. Derive the equations of motion of two atoms connected by a harmonic bond using the Lagrangian in centre-of-mass and relative coordinates. Show that the relative motion is an oscillator with the reduced mass.
2. For the double pendulum, write the Lagrangian. (You do not need to solve it.) Simulate it numerically with any integrator and plot the distance between two runs whose initial angles differ by $10^{-9}$ radians, on a logarithmic axis. Estimate the Lyapunov exponent from the slope.
3. Build the mass-weighted Hessian of a linear triatomic molecule with two equal springs (a model of CO$_2$ in one dimension) and find its three normal modes. Which one has zero frequency, and why?
4. Prove that $\{H,H\}=0$ and that $\{\rho(H),H\}=0$ for any differentiable function $\rho$. (The text gives the argument in words. Write it out with the sums, for any number of coordinates.)

## Read

{{READ}}
