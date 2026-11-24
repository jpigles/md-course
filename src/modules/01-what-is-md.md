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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

These are playlists for the whole course. If you want to follow one, start it here. You do not need to finish it now: watch the first one or two lectures to get the overall picture, then come back to the same playlist as you move through the modules.

## The plan of this module

This module is the map of the course. It says what a molecular dynamics simulation computes, shows the complete algorithm once, and lists what the method leaves out. Very little is derived here. Each idea comes back in a later module with its full derivation, and the text says which one.

The module has four layers:

1. **The idea and the algorithm.** What goes into a simulation, what comes out, and the loop that every MD program runs. The loop is given three times: as formulas, in words, and as a short program that you can run.
2. **The approximations.** Which physics the method keeps, which it drops, and what this rules out.
3. **The numbers.** Units, time scales and cost: what a simulation can reach and what it cannot.
4. **The results.** How a number is obtained from a trajectory, and the three kinds of error it carries.

A short history sits between layers 3 and 4.

You do not need to be a physicist to follow the course. Two background pages explain from zero what the lessons use: the [maths toolbox](maths.html) (derivatives, vectors, sums, probability) and the [physics primer](physics.html) (force, energy, temperature, charge). When a lesson uses a tool for the first time, it explains the tool in a box and links to the section of these pages that covers it.

### How to read the formulas

Every displayed formula in this course is followed by a list that says what each letter in it means (for a formula inside a box, the sentences around it do this). This is the first lesson, so the table below collects the conventions that all later lessons use. Each one is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $x$, $m$, $t$ | A letter in italics stands for one number: here a coordinate, a mass, a time. |
| $\mathbf r_i$ | A letter in bold is a **vector**: a quantity with a direction, stored as three numbers. $\mathbf r_i = (x_i, y_i, z_i)$ is the position of atom $i$. |
| $i$, $j$ | Labels (indices) that number the atoms, from 1 to $N$. $N$ is the number of atoms. A subscript $i$ or $j$ attaches a quantity to one atom: $m_i$ is the mass of atom $i$. Other subscripts are part of a name, as in $k_B$, or mark one particular value, as in $x_0$. |
| $U(\mathbf r_1,\dots,\mathbf r_N)$ | A **function**: a rule that gives one number for each choice of the things in the brackets. The dots mean "and so on, up to". |
| $x(t)$ | The value of $x$ at the time $t$. $x(t+\Delta t)$ is its value a little later. |
| $\Delta t$ | A capital Greek delta means "a step in" or "a change of". $\Delta t$ is the time step and is one symbol. It is not $\Delta$ times $t$. |
| $dx/dt$ | The **derivative** of $x$ with respect to time: how fast $x$ is changing at this instant. |
| $d^2x/dt^2$ | The second derivative: how fast that rate of change is itself changing. |
| $\dot x$, $\ddot x$ | From Module 2 on, a dot over a letter is a shorter way to write $dx/dt$, and two dots mean $d^2x/dt^2$. |
| $\partial U/\partial x$ | A **partial derivative**: the slope of $U$ when only $x$ changes and every other variable is held fixed. |
| $\nabla_i U$ | The **gradient**: the three partial derivatives of $U$ with respect to $x_i$, $y_i$ and $z_i$, collected in one vector. |
| $\sum_i$ | Add up the expression that follows for every value of $i$. For three atoms, $\sum_i m_i = m_1 + m_2 + m_3$. |
| $\langle A\rangle$, $\bar A$ | Two kinds of average of a quantity $A$. They are explained in the last section. |
| $\approx$, $\ll$ | "Is approximately equal to" and "is much smaller than". |
| $5\times10^{8}$, $10^{-4}$ | Powers of ten: 500,000,000 and 0.0001. |
| kJ mol$^{-1}$ nm$^{-2}$ | In a unit, a negative power means "per": kilojoules per mole per square nanometre. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** Physics has more quantities than the alphabet has letters, so some letters are used twice.

- Small $t$ is the time and capital $T$ the temperature.
- Bold $\mathbf r$ is a position and italic $r$ a distance between two atoms.
- Capital $U$ is the potential energy of the whole system, small $u(r)$ is the energy of one pair of atoms, and the upright u is a unit of mass.
- $k_B$ is the Boltzmann constant, while $k$ alone is the stiffness of a spring.
- $N$ is the number of atoms, while $N_A$ is Avogadro's number.
- $\varepsilon$ is the depth of the Lennard-Jones attraction, while $\varepsilon_0$ is a constant of electricity.
- Capital $K$ is the total kinetic energy in the formula for the temperature and a binding constant in the section on units. The upright K is the kelvin, the unit of temperature.
- Small $e$ is the elementary charge when it stands in a unit. In $e^{-14}$ it is the number 2.718..., the base of the natural logarithm.
- In the Python program the names follow programming habits. `x` holds all coordinates of all atoms, `u` is the potential energy and `k` the kinetic energy. `T` is the temperature, `L` the box length and `n` the number of atoms along one edge of the starting lattice.
</div>

## The idea in one paragraph

<div data-videos="dEmAnuO8RhQ GcGClviieOU O3YgILmo5V8 GUASx0_NyEE"></div>

This section answers the first question: what does a simulation compute? It computes how a set of atoms moves, given a rule for how the atoms push and pull on each other. Apart from the starting structure, it uses no knowledge of what the molecule looks like or is supposed to do. Whatever you see in the result, a protein that stays folded or a ligand that leaves its pocket, follows from the forces and from the starting point.

The picture to hold is this: every atom is a small ball with a mass. The balls attract and repel each other, a little like balls joined by springs. (The comparison is loose: a spring joins two chosen balls, while in a simulation every atom also feels every other atom nearby.) You place the balls, give each one a push, and let go. The computer works out where each ball is a tiny moment later, then a tiny moment after that, many millions of times.

Physics says the same thing in its own words. Two symbols are needed first: $N$ is the number of atoms, and $\mathbf r_i$ (in bold, because it is a vector of three coordinates) is the position of atom number $i$.

A molecular dynamics (MD) simulation takes a set of particles, a rule that gives the potential energy $U(\mathbf r_1,\dots,\mathbf r_N)$ for any arrangement of them, and Newton's second law. It then moves the particles forward in time in very small steps. The output is a **trajectory**: the positions and velocities of every particle at each saved step. Everything else you will ever report from MD (a free energy, a diffusion constant, an RMSD plot, a binding affinity) is a statistic computed from one or more trajectories.

The words of that paragraph, one at a time:

- **Particles.** Usually one particle is one atom. (In the coarse-grained models of Module 15, one particle stands for a group of atoms.) Each particle has a mass and a position.
- **Potential energy.** $U(\mathbf r_1,\dots,\mathbf r_N)$ is a single number, an energy, that belongs to one arrangement of all the atoms. The brackets list what it depends on: the $N$ positions and nothing else. It is low for a comfortable arrangement (bonds at their preferred lengths, no atoms overlapping) and high for a strained one. The formula used to compute it is called the **force field**, and the forces follow from it: each atom is pushed in the direction that lowers $U$ fastest.
- **Newton's second law.** Acceleration equals force divided by mass. It turns the forces into motion, and the next section writes it out.
- **Very small steps.** The step in time is called the **time step**. It is about one femtosecond, $10^{-15}$ s, a millionth of a billionth of a second. The section on time scales explains why it must be so short.
- **Trajectory.** Think of a film. Each frame holds the positions (and often the velocities) of all atoms at one instant. The program saves a frame only every so many steps, and you choose how many, because saving every step would fill the disk with frames that are nearly identical.
- **Statistic.** A number computed from many frames, most often an average. One frame tells you little, because the atoms never stop moving. The collection of frames tells you what the molecule does typically and how much it varies.

The four examples in the brackets belong to later modules. A **free energy** is the quantity that says which of two states is more probable, and by how much (Module 12). A **diffusion constant** says how fast a molecule wanders through a liquid (Module 11). An **RMSD** (root-mean-square deviation) measures how far the atoms of one frame are from the same atoms in a reference structure (Module 11). A **binding affinity** says how strongly two molecules hold on to each other (Modules 12 and 13).

The same paragraph also tells you what a simulation cannot do. It cannot be better than its energy rule: if the force field is wrong about an interaction, the trajectory is wrong about it too. It cannot show what happens on times longer than the trajectory. And it cannot show anything that the model does not contain, such as a chemical bond breaking. The later sections take these limits one at a time.

There are three ingredients, and the course follows them:

| Ingredient | Question it answers | Modules |
|---|---|---|
| Equations of motion and how to integrate them | How do the particles move, and how do we step forward in time without the error growing? | 2, 4, 8, 9 |
| The force field $U(\mathbf r)$ | What are the forces between atoms? | 5, 6, 7, 15, 17 |
| Statistical mechanics | Why does a trajectory tell us about thermodynamics, and how many samples do we need? | 3, 11, 12, 13, 14, 16 |

Some words in the table need a first explanation. In $U(\mathbf r)$, the bold $\mathbf r$ without a label stands for the positions of all atoms together.

**Equations of motion** are the equations that say how positions and velocities change in time. Newton's second law is one way to write them. To **integrate** them means to compute the positions at later times from the rates of change now, one step after another. The part of an MD program that does this is called the **integrator**. Each step makes a small error, and a good integrator is one whose small errors do not pile up.

**Statistical mechanics** is the theory that connects the motion of single atoms to the properties you can measure on a sample of matter, such as temperature, pressure and free energy. **Thermodynamics** is the study of those measurable properties and of the relations between them. A **sample**, in the table, is one observed state of the system, for example one saved frame. The question "how many samples do we need?" comes back in the last section of this module and in Module 11.

## The algorithm

<div data-videos="IlwC3PSyZ0Q QiZk_uT-40E AtExb5EprvE NItXk8epkNM TEg1Nx4yGjc gQ1YPzcHZqo"></div>

The question of this section: you know where every atom is now and how it is moving. Where is everything a moment later? The answer takes four lines of arithmetic per atom, repeated at every step. First comes the law of motion, then the recipe that turns it into steps.

<div class="box maths" markdown="1">
**Maths you need here: velocity and acceleration as derivatives.** Let $x(t)$ be the position of a particle along a line at the time $t$. Its **velocity** is the derivative $v = dx/dt$: the distance it covers per unit of time, measured at this instant. Its **acceleration** is the derivative of the velocity, $a = dv/dt = d^2x/dt^2$: how fast the velocity is changing. The notation $d^2x/dt^2$ is read "the second derivative of $x$ with respect to $t$": the 2 means "differentiate twice", and nothing is squared.

Example: a particle at $x(t) = 3t^2$ (in nm, with $t$ in ps) has the velocity $dx/dt = 6t$ and the acceleration $d^2x/dt^2 = 6$ nm/ps$^2$. At $t = 2$ ps it is at 12 nm and moves at 12 nm/ps, and its velocity grows by 6 nm/ps in every picosecond. For a position in space, $\mathbf r = (x, y, z)$, each of the three components is differentiated separately. More in the [toolbox](maths.html#derivative).
</div>

For particle $i$ with mass $m_i$ and position $\mathbf r_i$, Newton's second law is

$$
m_i \frac{d^2 \mathbf r_i}{dt^2} = \mathbf F_i = -\frac{\partial U}{\partial \mathbf r_i}.
$$

<div class="legend" markdown="1">
- $i$: the label of one particle, from 1 to $N$. The law holds for each particle separately.
- $m_i$: the mass of particle $i$. MD programs use the atomic mass unit, u: hydrogen is about 1 u, carbon about 12 u.
- $\mathbf r_i$: the position of particle $i$, a vector $(x_i, y_i, z_i)$, in nanometres.
- $t$: the time, in picoseconds.
- $d^2\mathbf r_i/dt^2$: the acceleration of particle $i$, the rate at which its velocity is changing (see the box above).
- $\mathbf F_i$: the total force on particle $i$ from all the other particles, a vector. In MD units a force is given in kJ mol$^{-1}$ nm$^{-1}$, an energy per distance.
- $U$: the potential energy, a function of all the positions.
- $\partial U/\partial \mathbf r_i$: the **gradient** of $U$ with respect to the position of particle $i$. It is the vector of the three slopes $(\partial U/\partial x_i,\ \partial U/\partial y_i,\ \partial U/\partial z_i)$, explained in the box below. Other lessons write it $\nabla_i U$.
- The minus sign: the force points in the direction in which $U$ falls fastest, that is, downhill.
</div>

<div class="box maths" markdown="1">
**Maths you need here: the slope of a function of many variables.** For a function of one variable, the derivative is the slope of its graph. The potential energy depends on $3N$ variables, the three coordinates of every atom, so it has one slope for each of them.

A **partial derivative**, written $\partial U/\partial x_1$ with a curly $\partial$, is the slope of $U$ when you change only $x_1$ and hold every other coordinate still. You compute it like an ordinary derivative and treat all other variables as constants. The **gradient** with respect to the position of one atom is the vector made of its three partial derivatives. It points in the direction in which $U$ rises fastest when that atom is moved.

Example: two atoms on a line, at $x_1$ and $x_2$, joined by a spring of stiffness $k$ whose relaxed length is $b$. The energy is $U = \tfrac12 k\,(x_2 - x_1 - b)^2$. Differentiating with respect to $x_1$ gives $\partial U/\partial x_1 = -k\,(x_2 - x_1 - b)$, where the minus sign comes from the $-x_1$ inside the bracket (the chain rule: differentiate the square, then multiply by the derivative of what is inside the bracket, which is $-1$ here; see the [toolbox](maths.html#chain-rule)). Differentiating with respect to $x_2$ gives $\partial U/\partial x_2 = +k\,(x_2 - x_1 - b)$. The forces are minus these slopes: $F_1 = +k\,(x_2 - x_1 - b)$ and $F_2 = -k\,(x_2 - x_1 - b)$.

Take, as an illustration, $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$, $b = 0.10$ nm, $x_1 = 0$ and $x_2 = 0.11$ nm. The spring is stretched by 0.01 nm, the energy is $\tfrac12\times1000\times0.01^2 = 0.05$ kJ/mol, and the forces are $F_1 = +10$ and $F_2 = -10$ kJ mol$^{-1}$ nm$^{-1}$. Atom 1 is pulled to the right and atom 2 to the left: a stretched spring pulls its two ends together. More in the toolbox on [partial derivatives](maths.html#partial-derivative) and on [the gradient](maths.html#gradient).
</div>

**Read it like this.** Mass times acceleration equals force. Turned round: acceleration equals force divided by mass, so the same force changes the velocity of a heavy atom less than that of a light one. The second equals sign says where the force comes from: it is minus the slope of the potential energy. The whole chain is: the positions give $U$, the slopes of $U$ give the forces, the forces give the accelerations, and the accelerations say how the motion changes. More in the primer on [motion and force](physics.html#newton) and on [energy](physics.html#energy).

Because $\mathbf r_i$ and $\mathbf F_i$ are vectors, the law is three equations per atom, one for each of $x$, $y$ and $z$, and $3N$ equations in all. They are tied together, because the force on one atom depends on where all the others are.

In general there is no closed-form solution for three or more interacting particles, so we solve it numerically.

A **closed-form solution** would be a formula that gives the position of every atom at any later time directly. A single mass on a spring, let go at rest, has one: $x(t) = x_0\cos\omega t$, where $x_0$ is the starting position, $\cos$ is the cosine function and $\omega$ sets how fast the mass swings. For many atoms that push on each other no such formula exists. To solve **numerically** means to compute numbers in place of a formula: advance the positions by a small step in time, then by another, and accept a small error at each step.

<div class="box maths" markdown="1">
**Maths you need here: solving an equation of motion step by step.** An equation that contains derivatives of the unknown quantity, such as Newton's law, is a **differential equation**. It does not tell you the position. It tells you how the position is changing, and to get the position you must add up the changes.

A numerical method rests on one idea: over a short enough time $\Delta t$, a rate of change is nearly constant. So

$$
x(t+\Delta t) \approx x(t) + v(t)\,\Delta t, \qquad v(t+\Delta t) \approx v(t) + a(t)\,\Delta t .
$$

In words: the new position is the old position plus the velocity times the time step, and the new velocity is the old velocity plus the acceleration times the time step. Here $x$ is a position, $v$ a velocity, $a = F/m$ an acceleration, and $\approx$ means "approximately equal to".

Example: a car that moves at 20 m/s is about $20\times0.1 = 2$ m further on after 0.1 s, almost regardless of what the driver does with the pedals during that tenth of a second. Over 10 s the same estimate could be badly wrong. The shorter the step, the smaller the error of each step, and the more steps you need. More in the [toolbox](maths.html#ode).
</div>

The two formulas in the box, used as they stand, are the simplest possible method, called forward Euler. Its energy drifts steadily (Module 2 says why), which makes it unsuitable for MD. MD programs use a better arrangement of the same two ideas.

The most common scheme, velocity Verlet (derived in Module 4), is:

$$
\begin{aligned}
\mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) &= \mathbf v_i(t) + \frac{\Delta t}{2 m_i}\,\mathbf F_i(t) \\
\mathbf r_i(t+\Delta t) &= \mathbf r_i(t) + \Delta t\,\mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) \\
\mathbf F_i(t+\Delta t) &= -\nabla_i U\big(\mathbf r(t+\Delta t)\big) \\
\mathbf v_i(t+\Delta t) &= \mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right) + \frac{\Delta t}{2 m_i}\,\mathbf F_i(t+\Delta t)
\end{aligned}
$$

<div class="legend" markdown="1">
- $i$: the label of one particle, from 1 to $N$, as in Newton's law above. The four lines are carried out for every particle.
- $t$: the present time. $t+\Delta t$ is the time one step later, and $t+\tfrac{\Delta t}{2}$ the time half a step later.
- $\Delta t$: the time step, typically 0.001 to 0.002 ps (1 to 2 fs).
- $\mathbf r_i(t)$: the position of particle $i$ at the time $t$, in nm.
- $\mathbf v_i(t)$: the velocity of particle $i$ at the time $t$, a vector, in nm/ps. $\mathbf v_i\!\left(t+\tfrac{\Delta t}{2}\right)$ is its velocity in the middle of the step.
- $\mathbf F_i(t)$: the force on particle $i$, computed from the positions at the time $t$.
- $m_i$: the mass of particle $i$. $\mathbf F_i/m_i$ is its acceleration, so $\frac{\Delta t}{2m_i}\mathbf F_i$ is the change of its velocity during half a step.
- $\mathbf r(t+\Delta t)$, bold and without a label: the positions of all particles at the new time.
- $U\big(\mathbf r(t+\Delta t)\big)$: the potential energy of the new arrangement.
- $\nabla_i$: the gradient with respect to the position of particle $i$. $-\nabla_i U$ is the same thing as $-\partial U/\partial\mathbf r_i$ in Newton's law above.
</div>

In words:

1. Give every atom a position (from a structure) and a velocity (random, from the Maxwell-Boltzmann distribution at the target temperature).
2. Compute the force on every atom from the force field.
3. Use the forces to update the velocities by half a step.
4. Use the velocities to update the positions by a full step.
5. Compute the forces at the new positions and finish the velocity update.
6. Every so often, write positions and energies to disk. Go to 3.

**Read it like this**, with the list next to the four formula lines. Line 1 is step 3, the *half kick*: every velocity changes by its acceleration times half a time step, using the forces at the present positions. Line 2 is step 4, the *drift*: every position moves by its velocity times a full time step. The velocity used is the one in the middle of the step, which is a good estimate of the average velocity during the step. Lines 3 and 4 are step 5: the atoms have moved, so the forces are computed again, and the *second half kick* finishes the velocity update with the new forces.

The other steps are not in the formulas. Step 1 happens once, at the start. Step 2 is the force calculation of line 3, done once before the first pass. Step 6 closes the loop.

Lines 1 and 4 together are the velocity formula of the box on solving step by step, cut into two halves, and line 2 is the position formula. The reason for the two halves is that the force changes during the step. The first half of the velocity change uses the force at the start of the step and the second half uses the force at the end, so the step treats its beginning and its end alike. Module 4 shows why this arrangement, unlike forward Euler, does not let the total energy drift over millions of steps.

What happens when the symbols change: a larger $\Delta t$ moves the atoms further per step, so the same simulated time needs fewer steps. But each step makes a larger error, and above a certain limit the scheme fails altogether. A larger mass $m_i$ gives a smaller change of velocity for the same force.

<div class="box key" markdown="1">
**Worked example: one step by hand.** One particle on a line, held by a spring: $U = \tfrac12 kx^2$, so the force is $F = -kx$. Illustration values: mass $m = 10$ u, stiffness $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$, time step $\Delta t = 0.01$ ps. The particle starts at $x = 0.1$ nm, at rest ($v = 0$).

1. *Force now.* $F = -1000\times0.1 = -100$ kJ mol$^{-1}$ nm$^{-1}$.
2. *Half kick.* $v = 0 + \dfrac{0.01}{2\times10}\times(-100) = -0.05$ nm/ps.
3. *Drift.* $x = 0.1 + 0.01\times(-0.05) = 0.0995$ nm.
4. *New force.* $F = -1000\times0.0995 = -99.5$ kJ mol$^{-1}$ nm$^{-1}$.
5. *Second half kick.* $v = -0.05 + \dfrac{0.01}{2\times10}\times(-99.5) = -0.09975$ nm/ps.

The exact solution for a spring gives $x = 0.0995004$ nm and $v = -0.09983$ nm/ps after 0.01 ps, so one step is off by less than one part in a thousand. The total energy was $\tfrac12 kx^2 = 5$ kJ/mol at the start. After the step it is $\tfrac12 mv^2 + \tfrac12 kx^2 = 0.04975 + 4.95013 = 4.99988$ kJ/mol.

No conversion factor was needed: a force in kJ mol$^{-1}$ nm$^{-1}$ divided by a mass in u is an acceleration in nm/ps$^2$. The section on units explains why.
</div>

Two things in step 1 of the list in words are new.

*A position from a structure.* The starting positions come from an experimental structure (from X-ray crystallography, cryo-electron microscopy or NMR) or from a predicted model. Module 10 covers how to prepare them.

*A velocity from the Maxwell-Boltzmann distribution.* A structure from an experiment contains positions and no velocities, so the program has to invent them. It does so at random, in the way the next box describes.

<div class="box physics" markdown="1">
**Physics you need here: temperature and the Maxwell-Boltzmann distribution.** The atoms of a liquid or a gas never stand still. **Temperature** measures how vigorously they move: at the absolute temperature $T$ (in kelvin), the average kinetic energy of an atom is $\tfrac32 k_BT$. Here $k_B$ is the Boltzmann constant, the number that converts a temperature into an energy, and the kinetic energy of an atom of mass $m$ and speed $v$ is $\tfrac12 mv^2$.

This is an average. At any instant some atoms are slow and a few are very fast. The **Maxwell-Boltzmann distribution** says how the velocities are spread: each of the three components $v_x$, $v_y$, $v_z$ of the velocity of an atom is a random number from a bell-shaped (Gaussian) distribution, centred on zero, with the width (standard deviation) $\sqrt{k_BT/m}$. For a carbon atom at 300 K, with $k_BT = 2.494$ kJ/mol and $m = 12$ u, the width is $\sqrt{2.494/12} = 0.456$ nm/ps, which is 456 m/s. A hydrogen atom is twelve times lighter and moves about $\sqrt{12}\approx3.5$ times faster.

So "give every atom a random velocity at 300 K" means: for every atom, draw three Gaussian random numbers with the width that belongs to its mass. Module 3 derives the distribution. More in the primer on [temperature](physics.html#temperature) and in the toolbox on [the Gaussian](maths.html#gaussian) and on [random numbers](maths.html#random-numbers).
</div>

Step 5, the force calculation, takes most of the computer time (the pair interactions alone take more than half). The rest of the "engine" part of this course (cutoffs, neighbour lists, particle-mesh Ewald, constraints) exists to make that step cheaper or to allow a larger $\Delta t$.

The reason step 5 is so much more expensive than the others: steps 3 and 4 need one multiplication and one addition per coordinate. Step 5 needs, for every atom, one contribution from every other atom close enough to push or pull on it, and there are several hundred of those (the count is done in the section on time and length scales). A **pair interaction** is one such contribution: a part of the energy that depends on the distance between two atoms.

| Line of the loop | Work per step | For 100,000 atoms |
|---|---|---|
| Half kick (twice per step) | one multiplication and one addition per coordinate | $3\times10^5$ coordinates, twice |
| Drift | one multiplication and one addition per coordinate | $3\times10^5$ coordinates |
| Forces | a distance, an energy and a force for every pair within reach, plus the long-range electrostatics | about $2\times10^7$ pairs |
| Writing a frame | only every so many steps | depends on how often you save |

The four words in the brackets (cutoffs, neighbour lists, particle-mesh Ewald, constraints) are explained in later modules. For now:

- a **cutoff** is a distance beyond which pair interactions are not computed one by one (Module 7);
- a **neighbour list** is a stored list, for each atom, of the atoms within reach, so that the program does not have to test all pairs at every step (Module 7);
- **particle-mesh Ewald** is a method that computes the long-range part of the electrostatic interactions, the part that reaches beyond the cutoff, on a grid (Module 7);
- **constraints** hold chosen bond lengths fixed, which removes the fastest vibrations and allows a larger time step (Module 9).

The simulation below runs this loop in your browser, for 49 particles in two dimensions. Press Start and watch the plot. Leave the thermostat off (a thermostat is an extra part of the algorithm that holds the temperature at a set value, Module 8). Kinetic and potential energy then move in opposite directions while the total stays nearly flat. Then raise $\Delta t$ with the slider and see what happens to the total energy.

<div class="widget" data-widget="md2d"></div>

### The same thing in 35 lines of Python

<div data-videos="kvJ1siWcBfM"></div>

Read this code line by line. It is a complete simulation of a Lennard-Jones fluid (a good model of liquid argon) in reduced units. Every production MD program is this loop with a more elaborate force routine.

Three ideas are needed before the code can be read: the Lennard-Jones potential, reduced units and the periodic box. Each has a box below. After the code, every line is explained. On a first reading the essential part is the loop, the last nine lines of the program. The force routine can wait for a second reading.

<div class="box physics" markdown="1">
**Physics you need here: the Lennard-Jones potential.** Two atoms with no charge and no chemical bond between them, such as two argon atoms, still interact. When they come very close they repel strongly, because their electron clouds overlap. A little further apart they attract weakly. The Lennard-Jones (LJ) formula is the usual simple model of both effects:

$$
u(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right].
$$

Here $r$ is the distance between the two atoms and $u(r)$ is the energy of the pair. $\sigma$ (sigma) is a length that sets the size of the atoms, and $\varepsilon$ (epsilon) is an energy that sets the strength of the attraction. The term with the power 12 is the repulsion. It is huge at short distance and dies off fast. The term with the power 6 and the minus sign is the attraction.

Three values fix the shape. At $r = \sigma$ the two terms cancel and $u = 0$. At $r = 2^{1/6}\sigma\approx1.12\,\sigma$ the energy has its minimum, $u = -\varepsilon$: this is the distance the pair prefers. At $r = 2.5\,\sigma$ the energy is only $-0.016\,\varepsilon$, so pairs further apart than that contribute little, and the program below leaves them out.

Module 5 treats this potential in full. More in the [primer](physics.html#intermolecular).
</div>

<div class="box physics" markdown="1">
**Physics you need here: reduced units.** When all atoms are alike, you can measure every length in units of $\sigma$, every energy in units of $\varepsilon$ and every mass in units of the mass $m$ of one atom. The Boltzmann constant $k_B$ is set to 1. In these **reduced units** $\sigma = \varepsilon = m = k_B = 1$, and the Lennard-Jones formula becomes $u(r) = 4\,(r^{-12} - r^{-6})$, with no parameter left to look up.

All other quantities follow. A temperature of 1.0 means $k_BT = \varepsilon$: the thermal energy equals the depth of the attraction. A density of 0.8 means 0.8 atoms in a volume $\sigma^3$. The unit of time is $\sigma\sqrt{m/\varepsilon}$, and a time step of 0.004 is 0.004 of that unit.

The advantage is that one simulation describes every Lennard-Jones substance at once. To get nanometres and kJ/mol for a particular substance, you multiply by its $\sigma$ and $\varepsilon$.
</div>

<div class="box physics" markdown="1">
**Physics you need here: the periodic box and the minimum image.** The program simulates 125 atoms. In a box with walls, most of them would sit next to a wall, and the walls would dominate everything you measure. The standard remedy is the **periodic box**: imagine the box surrounded on all sides by exact copies of itself, like tiles on a floor. An atom that leaves through one face comes back in through the opposite face, so the number of atoms stays the same and there is no surface anywhere.

An atom close to one face now has neighbours on the other side of that face: the copies of the atoms near the opposite face. The **minimum-image convention** says that for each pair of atoms you use the nearest of all the copies. In one dimension, with a box of length $L = 5$: two atoms at $x = 4.6$ and $x = 0.4$ are 4.2 apart inside the box, but a copy of the second atom sits at $0.4 + 5 = 5.4$, only 0.8 away. The rule "subtract the box length times the rounded value of the difference divided by the box length" finds this: $4.2/5 = 0.84$ rounds to 1, and $4.2 - 5\times1 = -0.8$. Module 7 covers periodic boundaries in full.
</div>

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

**What the arrays hold.** `x` is a table with $N$ rows and 3 columns: row $i$ holds the $x$, $y$ and $z$ coordinates of atom $i$. `v` and `f` have the same shape and hold the velocities and the forces. `L` is the edge length of the cubic box.

**The force routine, `lj_forces`.** It returns the force on every atom and the total potential energy.

- `d = x[:, None, :] - x[None, :, :]` builds a table with $N\times N\times3$ entries. Entry `d[i, j]` is the vector $\mathbf r_i - \mathbf r_j$, which points from atom $j$ to atom $i$. (Each `None` adds an axis to the array, and NumPy then subtracts the rows of `x` from each other in all combinations.)
- `d -= L * np.round(d / L)` applies the minimum-image convention of the box above to each component of each pair vector.
- `r2 = (d ** 2).sum(-1)` adds the squares of the three components. By Pythagoras' theorem this is the squared distance $r^2$ of each pair, an $N\times N$ table.
- `np.fill_diagonal(r2, np.inf)` deals with the entries `r2[i, i]`, the distance of each atom from itself, which is zero. Dividing by zero would give nonsense. Setting these entries to infinity puts them outside the cutoff, so an atom never interacts with itself.
- `inside = r2 < rc ** 2` is a table of True and False: True for the pairs closer than the cutoff `rc`, which is 2.5. Comparing squared distances avoids computing a square root.
- `inv6 = np.where(inside, 1.0 / r2 ** 3, 0.0)` is $1/r^6$ for the pairs inside the cutoff, computed as $1/(r^2)^3$, and zero for all others.
- `shift = 4 * (rc ** -12 - rc ** -6)` is the Lennard-Jones energy at the cutoff distance, $-0.0163$. Subtracting it from every pair energy makes the pair energy exactly zero at the cutoff. Without the shift, the energy of a pair would jump by 0.0163 each time the pair crossed the cutoff distance, and the total energy would not be conserved.
- `u = 0.5 * np.sum(...)` adds up $4\,(r^{-12} - r^{-6})$ minus the shift over all pairs inside the cutoff. `inv6 ** 2` is $r^{-12}$. The table contains every pair twice, as $(i,j)$ and as $(j,i)$, and the factor 0.5 corrects for that.
- `f = (24 * (2 * inv6 ** 2 - inv6) / r2)[:, :, None] * d` is the force on atom $i$ from atom $j$, for all pairs at once. The formula is derived below.
- `return f.sum(axis=1), u` adds up, for each atom $i$, the forces from all atoms $j$. The result is the total force on each atom, a table with $N$ rows and 3 columns like `x`.

The force line comes from the rule that a force is minus the slope of the energy. For a pair energy $u(r)$, the force on atom $i$ from atom $j$ acts along the line between the two atoms (Module 2 derives this):

$$
\mathbf F_{ij} = -\frac{du}{dr}\,\frac{\mathbf r_{ij}}{r} = \frac{24}{r^{2}}\left(\frac{2}{r^{12}} - \frac{1}{r^{6}}\right)\mathbf r_{ij} .
$$

<div class="legend" markdown="1">
- $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$.
- $r$: the distance between the two atoms.
- $u(r)$: the Lennard-Jones pair energy, which in reduced units is $4\,(r^{-12} - r^{-6})$.
- $du/dr$: the slope of the pair energy with respect to the distance.
- $\mathbf r_{ij} = \mathbf r_i - \mathbf r_j$: the vector from atom $j$ to atom $i$, the entry `d[i, j]` of the program.
- $\mathbf r_{ij}/r$: that vector divided by its own length. This leaves a vector of length 1 that only gives the direction.
</div>

The steps. The derivative of $r^{-12}$ is $-12\,r^{-13}$ and that of $r^{-6}$ is $-6\,r^{-7}$ (the power rule), so $du/dr = 4\,(-12\,r^{-13} + 6\,r^{-7}) = -24\,(2\,r^{-13} - r^{-7})$. Changing the sign and dividing by $r$ gives $24\,(2\,r^{-14} - r^{-8})$, which is the same as $(24/r^2)(2\,r^{-12} - r^{-6})$. In the program $r^{-6}$ is `inv6`, $r^{-12}$ is `inv6 ** 2` and $r^2$ is `r2`.

**Read it like this.** When the bracket is positive (short distance, the repulsion wins) the force on $i$ points along $\mathbf r_{ij}$, away from $j$. When it is negative the force points towards $j$. The sign changes at $r = 2^{1/6}$, the minimum of the energy, where the force is zero.

The shift does not appear in the force, because it is a constant and a constant has zero slope. One flaw remains. At the cutoff the size of the force is 0.039 in reduced units, small but not zero, and beyond the cutoff the force is exactly zero. This small jump in the force comes back below.

**The set-up.**

- `rng = np.random.default_rng(0)` creates a random-number generator. The 0 is the seed: with the same seed the program draws the same "random" numbers every time, so a run can be repeated exactly.
- `n, rho, T, dt = 5, 0.8, 1.0, 0.004` sets the number of atoms along one edge of the starting lattice, the density, the temperature and the time step, all in reduced units. `N = n ** 3` is the number of atoms, 125.
- `L = (N / rho) ** (1 / 3)` is the box edge. A density is a number divided by a volume, $\rho = N/L^3$, so $L = (N/\rho)^{1/3} = (125/0.8)^{1/3} = 5.39$. Half of that is 2.69, which is larger than the cutoff of 2.5, as the minimum-image convention requires.
- `g = (np.arange(n) + 0.5) * L / n` is a list of five evenly spaced coordinates: 0.54, 1.62, 2.69, 3.77 and 4.85. The spacing is $L/n = 1.08$.
- `x = np.array(np.meshgrid(g, g, g)).reshape(3, -1).T` forms all $5\times5\times5$ combinations of these values, one per atom, so the atoms start on a regular cubic lattice. A lattice makes sure that no two atoms start almost on top of each other, which would give an enormous force.
- `v = rng.normal(0.0, np.sqrt(T), (N, 3))` draws the velocities from the Maxwell-Boltzmann distribution: Gaussian random numbers with mean 0 and width $\sqrt{k_BT/m}$, which is $\sqrt{T}$ in reduced units.
- `v -= v.mean(axis=0)` subtracts the average velocity from every atom. The total momentum (mass times velocity, added up over all atoms) is then zero, so the liquid as a whole does not drift through the box.

**The loop.**

- `f, u = lj_forces(x, L)` computes the forces once before the loop starts (step 2 of the list in words).
- `for step in range(2001):` repeats the indented lines 2,001 times.
- `v += 0.5 * dt * f` is the half kick, $\frac{\Delta t}{2m}\mathbf F$ with $m = 1$.
- `x += dt * v` is the drift.
- `x %= L` wraps the positions: an atom that has left the box through one face is put back in through the opposite face. The `%` operator gives the remainder after division by `L`.
- `f, u = lj_forces(x, L)` computes the forces at the new positions. This one line takes nearly all of the run time.
- `v += 0.5 * dt * f` is the second half kick.
- `if step % 200 == 0:` is true at every 200th step. Then `k = 0.5 * (v ** 2).sum()` is the total kinetic energy, $\sum_i \tfrac12 m v_i^2$ with $m = 1$, where $v_i$ is the speed of atom $i$. The `print` line reports the step number, the temperature and the total energy per atom, `(k + u) / N`.

The temperature is computed from the kinetic energy. At the temperature $T$, every independent direction of motion holds on average a kinetic energy of $\tfrac12 k_BT$ (this is the "$\tfrac32 k_BT$ per atom" of the box on temperature, counted per direction). With $3N-3$ independent directions, the total kinetic energy is on average $K = \tfrac12(3N-3)\,k_BT$. Solving for $T$ gives the temperature of one frame:

$$
T = \frac{2K}{(3N-3)\,k_B} .
$$

<div class="legend" markdown="1">
- $T$: the instantaneous temperature, the temperature computed from the velocities of one frame.
- $K$: the total kinetic energy of all atoms, `k` in the program.
- $N$: the number of atoms, so $3N$ is the number of velocity components.
- $3N-3$: the number of independent directions of motion (degrees of freedom). Three are subtracted because the three components of the total momentum were set to zero and stay zero, so the $3N$ velocity components are not all independent (Module 2).
- $k_B$: the Boltzmann constant. It equals 1 in reduced units, which is why it does not appear in the program.
</div>

The force routine works through all $N\times N$ entries of the pair table at every step, 15,625 of them. That is fine for 125 atoms. For 100,000 atoms the table would have $10^{10}$ entries, and this is where the cutoffs and neighbour lists of Module 7 come in.

When you run the program it prints eleven lines. On the computer used to check this lesson the first three were:

```text
step     0  T = 1.018  E/N = -3.28873
step   200  T = 0.858  E/N = -3.28829
step   400  T = 0.974  E/N = -3.28823
```

Your digits may differ a little, and more so in the later lines, because tiny rounding differences between computers grow quickly in a system like this (Module 2 explains why). The pattern should be the same.

The total energy per particle printed in the last column should stay constant to about three decimal places (it wanders by a few $10^{-4}$, mostly because of the finite time step and a little because the force still has a small jump at the cutoff), while the temperature changes by several percent. The temperature does not stay at its starting value of 1.0: as the lattice melts, kinetic and potential energy are exchanged, and the temperature settles a little lower and keeps fluctuating. That is equilibration, which you will meet again in Module 10.

Three remarks on this paragraph.

*Why the energy should be constant.* The loop has no thermostat, so nothing adds or removes energy. Module 2 proves that Newton's law, with forces that come from a potential energy, keeps the sum of kinetic and potential energy constant. A constant total energy is therefore the first test that an MD program is correct.

*The small jump at the cutoff.* The shift made the energy continuous at the cutoff, but the size of the force still drops from 0.039 to zero there, as computed above. Each time a pair crosses the cutoff distance the integration makes a small extra error. In a run as short as this one that error is the smaller part: most of the wander in the fourth decimal place comes from the size of the time step (Module 4). On the computer used to check this lesson, halving `dt` to 0.002 made the wander nearly four times smaller, and removing the jump (with a force that is shifted to reach zero at the cutoff) changed it by a tenth or less. The error from the jump builds up slowly and shows in runs about ten times longer.

*Why the temperature changes.* At the start the atoms sit on a perfect lattice, where the forces on each atom cancel and the potential energy is low. The random velocities break the lattice up. As it melts, the potential energy rises and the kinetic energy falls by the same amount, because the total is fixed. The temperature is proportional to the kinetic energy, so it falls below 1.0 and then fluctuates as the two forms of energy keep trading.

In the run quoted above the printed temperatures lie between 0.858 and 1.018, so single values are up to 14 percent below 1.0. The "several percent" of the paragraph above is the typical swing: from about step 100 on, the temperature stays near 0.96 with a standard deviation of about 5 percent. The largest change falls before the second printed line: after about 15 steps the temperature is down at about 0.53, and by about step 60 it is back up at about 1.17.

**Equilibration** is this first phase of a run, in which the system forgets its artificial starting arrangement.

## Which physics is kept, and which is dropped

<div data-videos="4uloreO4qHA qnDkRUaz57g"></div>

Atoms are not balls. An atom is a heavy nucleus surrounded by light electrons, and both obey quantum mechanics, the theory of matter on the smallest scales. This section explains why a simulation may still treat atoms as balls that follow Newton's law. Two approximations lead from the full description to the simple one, and each has a price. On a first reading, keep the two prices: bonds cannot break, and hydrogen is the atom for which the picture of a classical ball is least safe.

<div class="box physics" markdown="1">
**Physics you need here: quantum mechanics in five sentences.** In quantum mechanics a particle does not have one definite position. It is described by a **wave function**, a function of position whose squared size gives the probability of finding the particle near each place. The **Schrödinger equation** is the law that says how the wave function changes in time, so it plays the part that Newton's law plays for classical particles. The states in which a system can remain unchanged have definite energies, and the one with the lowest energy is called the **ground state**. Solving the equation exactly for all the electrons and nuclei of a protein in water is out of reach, because the cost grows steeply with the number of particles.

More in the [primer](physics.html#quantum).
</div>

The exact description of a molecule is the time-dependent Schrödinger equation for all nuclei and electrons. MD makes two approximations to get from there to Newton's law.

("Time-dependent" names the form of the equation that follows the wave function as it changes in time. A particle is called **classical** when it can be treated as a point with a definite position and velocity that obeys Newton's law.)

**1. Born-Oppenheimer.** Electrons are about 1,800 times lighter than a proton, so they adjust almost instantly to the nuclear positions. For a given arrangement of nuclei the electrons sit in their ground state, and the electronic ground-state energy as a function of nuclear positions is the potential energy surface $U(\mathbf r)$. In classical MD we do not solve for the electrons at all: we replace $U(\mathbf r)$ by a cheap fitted formula, the **force field**. Consequence: bonds cannot break or form, and electrons cannot polarise (in standard force fields).

Step by step:

- *The separation of speeds.* A proton is the nucleus of a hydrogen atom, the lightest nucleus there is. Electrons are so much lighter that they move much faster than any nucleus. Picture a swarm of flies around a walking cow: wherever the cow goes, the swarm has already rearranged itself around it. (Electrons form a smeared-out cloud and are not little flies. The comparison is only about the speeds.)
- *The ground state.* For each arrangement of the nuclei, the electrons settle into their state of lowest energy. Because they are so fast, they are taken to be in that state at every moment of the nuclear motion.
- *The potential energy surface.* Do this for every possible arrangement of the nuclei and you have one energy for each arrangement. That is a function of the nuclear positions, written $U(\mathbf r)$, where the bold $\mathbf r$ stands for all the positions together. It is called a surface because for two coordinates you could draw it as a landscape of hills and valleys. The nuclei move on this landscape and its slopes push them downhill.
- *The force field.* Computing $U$ from the electrons at every step is far too slow for a protein. A force field is a formula made of simple terms (springs for bonds and angles, a Lennard-Jones term and an electric term for pairs of atoms) whose parameters were adjusted until the formula reproduced reference data. That adjusting is what "fitted" means. Module 5 gives the formula and Module 6 says where the parameters come from.
- *The consequence.* The list of bonds is part of the input, and each bond is a spring whose energy keeps rising as you stretch it, so a bond can never break and a new one can never form. To **polarise** means that the electron cloud of a molecule shifts when a charge comes near. A standard force field gives every atom a fixed charge that never changes, so it lacks this response. More in the primer on [dipoles and polarisation](physics.html#dipoles).

The first approximation removed the electrons. The nuclei are left, and they too are quantum particles. The second approximation treats each nucleus as a point with a definite position and velocity. Quantum mechanics provides a length that tells you when this is allowed.

**2. Classical nuclei.** A particle behaves classically when its thermal de Broglie wavelength

$$
\Lambda = \frac{h}{\sqrt{2\pi m k_B T}}
$$

is small compared with the distances over which the potential changes.

<div class="legend" markdown="1">
- $\Lambda$ (capital Greek lambda): the thermal de Broglie wavelength, a length. It is roughly the size of the region over which quantum mechanics smears out a particle of mass $m$ at the temperature $T$.
- $h$: Planck's constant, the constant of nature that sets the scale of quantum effects. $h = 6.626\times10^{-34}$ J s, which is 0.399 kJ mol$^{-1}$ ps in MD units.
- $m$: the mass of the particle.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the absolute temperature, in kelvin.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- $\pi$: the number 3.14159...
- $\sqrt{\ \ }$: the square root of everything under the bar.
</div>

**Read it like this.** If the smeared-out region is much smaller than the distance over which the forces change, the particle may be treated as a point. A larger mass or a higher temperature makes $\Lambda$ smaller, so heavy and hot means classical. Because of the square root, a particle that is four times heavier has half the wavelength.

<div class="box key" markdown="1">
**Worked example: hydrogen at 300 K, in MD units.** With $h = 0.399$ kJ mol$^{-1}$ ps, $m = 1.008$ u and $k_BT = 2.494$ kJ/mol, the quantity under the square root is $2\pi\times1.008\times2.494 = 15.80$, and its square root is 3.974. So $\Lambda = 0.399/3.974 = 0.100$ nm, which is 1.0 Å. The result comes out in nm without any conversion, because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$.

Carbon is about 12 times heavier, so its wavelength is smaller by the factor $\sqrt{12/1.008} = 3.45$, and $1.0/3.45 = 0.29$ Å.
</div>

At 300 K this gives $\Lambda \approx 1.0$ Å for hydrogen and $0.29$ Å for carbon, while interatomic distances are 1 to 4 Å. Heavy atoms are safely classical. Hydrogen is borderline.

(1 Å, one ångström, is 0.1 nm.) For carbon the smearing is a small fraction of the distance to the neighbouring atoms. For hydrogen it is as large as the shortest distances between atoms, which is why hydrogen is the atom for which the classical picture is least safe.

There is a second way to test whether a motion is classical. It looks at vibrations and needs one more piece of quantum mechanics.

<div class="box physics" markdown="1">
**Physics you need here: the energy steps of a vibration, and the unit cm$^{-1}$.** A classical spring can hold any amount of energy. A quantum vibration cannot. Its energy can only take values on a ladder with equally spaced steps, and the size of one step, the **vibrational quantum**, is $\hbar\omega$. Here $\omega$ is the angular frequency of the vibration ($2\pi$ times the number of oscillations per unit of time) and $\hbar$, read "h-bar", is Planck's constant divided by $2\pi$. The bottom of the ladder is the ground state.

Whether the steps matter depends on how they compare with the thermal energy $k_BT$, the typical amount of energy that the surroundings hand to a molecule or take from it. If a step is much smaller than $k_BT$, the vibration moves up and down many steps all the time and the ladder acts like a smooth ramp: the classical picture is fine. If a step is much larger than $k_BT$, the surroundings almost never supply enough for even one step, and the vibration stays at the bottom.

Spectroscopists give vibrational frequencies as **wavenumbers** in cm$^{-1}$: the number of waves of the matching infrared light that fit into one centimetre. The wavenumber is proportional to the frequency, and so to the quantum $\hbar\omega$, which lets it serve as a unit of energy. On this scale $k_BT$ at 300 K is 208 cm$^{-1}$. More in the primer on [waves and frequencies](physics.html#waves).
</div>

A second test is to compare the vibrational quantum $\hbar\omega$ with the thermal energy $k_BT$ (208 cm$^{-1}$ at 300 K). A C-H stretch at about 3,000 cm$^{-1}$ has $\hbar\omega \approx 14\,k_BT$: in reality it sits in its quantum ground state and does not exchange energy with its surroundings. A classical spring with the same frequency would hold a full $k_BT$ of energy. This is one physical reason why it is acceptable, even preferable, to freeze bonds to hydrogen with constraints (Module 9). Slow, soft motions (torsions, diffusion, domain motions) have $\hbar\omega \ll k_BT$ and are well described classically.

The numbers: a C-H stretch is the vibration in which the bond between a carbon and a hydrogen atom gets longer and shorter. $3000/208\approx14$, so one step of its ladder costs about 14 times the thermal energy. The fraction of such bonds that sit one step up is about $e^{-14}$, less than one in a million (here $e\approx2.718$ is the base of the natural logarithm, and this exponential rule is the Boltzmann factor of Module 3). The real bond therefore stays in its ground state and takes no part in the exchange of thermal energy.

A classical spring behaves differently. In classical mechanics every vibration holds on average $\tfrac12 k_BT$ of kinetic energy and $\tfrac12 k_BT$ of potential energy, whatever its frequency (the equipartition theorem, Module 3). A classical C-H spring therefore carries and exchanges energy that the real bond does not. Holding the bond length fixed removes this false energy. It also removes the fastest vibration in the system, which allows a longer time step.

At the other end, a **torsion** is a rotation about a bond, and a **domain motion** is the movement of one folded part of a protein relative to another. These motions are slow, so their $\omega$ is small and their quantum is far below $k_BT$ (the sign $\ll$ means "much smaller than"). For them the ladder is a ramp.

<div class="box key" markdown="1">
**What MD cannot do without extra methods:** chemical reactions (needs QM/MM or reactive force fields), proton transfer and changes in protonation state (needs constant-pH methods), electronic excitation, and nuclear tunnelling.
</div>

The terms in this box:

- In a **chemical reaction** bonds break and form. **QM/MM** treats a small region, for example the active site of an enzyme, with quantum mechanics (QM) and the rest with a force field (molecular mechanics, MM). A **reactive force field** is one whose formula allows bonds to change.
- The **protonation state** of a group such as a carboxylic acid or a histidine side chain says whether it carries its proton, and so what charge it has. In standard MD you decide it at set-up and it never changes. **Constant-pH methods** let it change during the run, according to a chosen pH.
- An **electronic excitation** lifts an electron to a state of higher energy, for example when a molecule absorbs light. A force field describes the electronic ground state only.
- **Nuclear tunnelling** is a light nucleus, usually a proton, passing through an energy barrier that it does not have the energy to climb over. It is a quantum effect with no classical counterpart.

## Units and the numbers worth memorising

An MD program does arithmetic on numbers and does not know what they stand for. Give it a distance in ångström where it expects nanometres and it runs without complaint and returns nonsense. This section lists the units, explains why they fit together, and gives a few numbers that let you check a result in your head.

The units and their sizes:

- **nanometre (nm)**: $10^{-9}$ m. A bond between two carbon atoms is about 0.15 nm long. The older unit **ångström (Å)** is 0.1 nm.
- **picosecond (ps)**: $10^{-12}$ s. A **femtosecond (fs)** is $10^{-15}$ s, so 1 ps is 1,000 fs.
- **atomic mass unit (u)**: $1.66054\times10^{-27}$ kg, close to the mass of one hydrogen atom. It is also called the dalton (Da).
- **kJ/mol**: an energy per mole of molecules. A mole is $6.02214\times10^{23}$ molecules (Avogadro's number, $N_A$), so 1 kJ/mol is $1.66\times10^{-21}$ J for a single molecule. Energies are given per mole because chemistry measures them that way and because the numbers have a convenient size.
- **kcal/mol**: the same with the kilocalorie, 1 kcal = 4.184 kJ.
- **elementary charge ($e$)**: the charge of one proton. An electron has the charge $-1\,e$.
- **kelvin (K)**: the unit of absolute temperature. 300 K is about 27 °C.

More in the primer on [units](physics.html#units).

Most biomolecular codes use one of two unit systems. GROMACS uses nm, ps, atomic mass units (u), kJ/mol and elementary charges. These are consistent: 1 u nm$^2$ ps$^{-2}$ = 1 kJ/mol, so no conversion factors appear in Newton's law. AMBER, CHARMM and NAMD use Å and kcal/mol. With Å, u and kcal/mol the consistent time unit is about 48.9 fs, so these programs convert internally, and you give the time step in ps (AMBER, CHARMM) or in fs (NAMD).

GROMACS, AMBER, CHARMM and NAMD are MD programs ("codes"). **Consistent** means that the units fit together without extra factors.

Newton's law says that a force is a mass times an acceleration, and a force is also an energy divided by a distance. So an energy must be a mass times a length squared divided by a time squared. In a consistent system the units obey that same relation with the factor 1. Here is the check for the GROMACS units:

$$
\begin{aligned}
1\ \text{u}\,\text{nm}^2\,\text{ps}^{-2} &= 1.66054\times10^{-27}\ \text{kg}\times\frac{(10^{-9}\ \text{m})^2}{(10^{-12}\ \text{s})^2} = 1.66054\times10^{-21}\ \text{J} \\
1.66054\times10^{-21}\ \text{J}\times N_A &= 1.66054\times10^{-21}\ \text{J}\times6.02214\times10^{23}\ \text{mol}^{-1} = 1000\ \text{J/mol} = 1\ \text{kJ/mol}
\end{aligned}
$$

<div class="legend" markdown="1">
- u, nm, ps: the atomic mass unit, the nanometre and the picosecond.
- kg, m, s, J: the kilogram, the metre, the second and the joule. 1 J is 1 kg m$^2$ s$^{-2}$.
- $N_A$: Avogadro's number, $6.02214\times10^{23}$ per mole. Multiplying an energy per molecule by it gives the energy per mole.
</div>

The first line computes the energy for one particle. The second converts it to a mole of particles. The worked example in the algorithm section relied on this: a force of $-100$ kJ mol$^{-1}$ nm$^{-1}$ on a mass of 10 u gave an acceleration of $-10$ nm/ps$^2$ with no conversion.

With Å, u and kcal/mol the same check fails. 1 kcal/mol is 4.184 kJ/mol, which is 4.184 u nm$^2$ ps$^{-2}$, and since 1 nm$^2$ is 100 Å$^2$ this is 418.4 u Å$^2$ ps$^{-2}$. The factor is 418.4 where it should be 1. It becomes 1 only if time is measured in a unit of $1/\sqrt{418.4}$ ps, which is 0.0489 ps or 48.9 fs. That is the "consistent time unit" of the paragraph above. Nobody wants to type time steps in units of 48.9 fs, so these programs accept ps or fs and convert.

| Quantity | Value |
|---|---|
| $k_B$ | 0.0083145 kJ mol$^{-1}$ K$^{-1}$ = 0.0019872 kcal mol$^{-1}$ K$^{-1}$ |
| $k_BT$ at 300 K | 2.494 kJ/mol = 0.596 kcal/mol |
| 1 kcal/mol | 4.184 kJ/mol |
| Coulomb constant $1/(4\pi\varepsilon_0)$ | 138.935 kJ mol$^{-1}$ nm $e^{-2}$ = 332.06 kcal mol$^{-1}$ Å $e^{-2}$ |
| Typical time step | 1 fs (flexible bonds), 2 fs (bonds to H constrained), 4 fs (with hydrogen mass repartitioning) |
| Factor of 10 in a binding constant at 298 K | $RT\ln 10$ = 5.71 kJ/mol = 1.36 kcal/mol |
| Number density of water | 33.4 molecules per nm$^3$, about 100 atoms per nm$^3$ |

What each line of the table is for:

- **$k_B$**, the Boltzmann constant, converts a temperature into an energy. With energies per mole it has the same value as the gas constant $R$ of chemistry, because $R = N_A k_B$ and "per mole" has already multiplied by $N_A$.
- **$k_BT$**, the thermal energy, is the yardstick for every energy in this course: $0.0083145\times300 = 2.494$ kJ/mol. An energy difference much smaller than $k_BT$ is washed out by thermal motion. A barrier many times $k_BT$ high is rarely crossed. More in the primer on [temperature](physics.html#temperature).
- **1 kcal/mol = 4.184 kJ/mol.** You will need this conversion often, because both units are in use.
- **The Coulomb constant** gives the electric energy of two charges in vacuum: $138.935\,q_1q_2/r$ kJ/mol, for charges $q_1$ and $q_2$ in units of $e$ at a distance $r$ in nm. Two charges of $+1\,e$ at 1 nm repel each other with an energy of 138.9 kJ/mol, about 56 times $k_BT$. The symbol $\varepsilon_0$ is the vacuum permittivity, the constant of nature that sets the strength of electric forces. It has nothing to do with the Lennard-Jones $\varepsilon$. More in the primer on [charge and Coulomb's law](physics.html#electrostatics).
- **The time step.** The next section explains the values. *Flexible bonds* means that all bonds are free to vibrate. *Constrained* means that the lengths of the bonds to hydrogen are held fixed (Module 9). *Hydrogen mass repartitioning* moves part of the mass of a heavy atom to the hydrogens attached to it, which slows the fastest remaining motions (Module 9).
- **$RT\ln 10$.** A binding constant $K$ and the binding free energy $\Delta G$ are related by $\Delta G = -RT\ln K$, where $R$ is the gas constant, $T$ the temperature and $\ln$ the natural logarithm. Multiply $K$ by 10 and $\Delta G$ becomes more negative by $RT\ln 10 = 0.0083145\times298\times2.303 = 5.71$ kJ/mol. Read in the other direction: an error of 5.71 kJ/mol (1.36 kcal/mol) in a computed binding free energy is a factor of 10 in the affinity. (298 K is 25 °C, the usual reference temperature in chemistry.) More in the primer on [equilibrium constants](physics.html#equilibrium) and in the toolbox on [logarithms](maths.html#exp-log).
- **The density of water.** Liquid water has 33.4 molecules in every cubic nanometre, and each molecule has three atoms. Most of a simulation box is water, so this number gives the size of a system at once: a cubic box with an edge of 8 nm has a volume of 512 nm$^3$ and holds about 51,000 atoms.

## Time and length scales

<div data-videos="_TiQYNWJwYg ryJFDd0dF44"></div>

This section answers two questions. Why is the time step a femtosecond? And how much time can a simulation cover? The distance between the two answers is the main practical limit of MD.

The time step must resolve the fastest motion in the system, and the fastest motion is a bond vibration with a period of about 10 fs.

To **resolve** a motion means to take enough steps during one cycle of it to follow its shape. Think of drawing the motion of a swing from photographs: with ten photographs per swing you can trace it, with one photograph per swing you see nothing of it. For the integrator the matter is more serious than a poor drawing.

Each step assumes that the force hardly changes during the step. If a bond goes through a large part of its vibration in one step, the update overshoots, the next step overshoots more, and the energy grows without limit. The rule of thumb is ten or more steps per period of the fastest motion.

Why bond vibrations are so fast: the **period** of a vibration is the time for one full cycle. For a mass $m$ on a spring of stiffness $k$ it is $2\pi\sqrt{m/k}$ (see the primer on [the harmonic oscillator](physics.html#oscillator)), so a light mass on a stiff spring swings fast. Atoms are extremely light and chemical bonds are stiff, and the result is a period near 10 fs for bonds to hydrogen, the lightest atom (Module 2 computes 11.4 fs for a C-H bond). Ten steps per period then give a time step of 1 fs. With the bonds to hydrogen held fixed, the fastest remaining motions are slower, and 2 fs is possible.

Everything interesting in biology is slower by many orders of magnitude:

| Process | Typical time | Steps at 2 fs |
|---|---|---|
| Bond stretch (C-H) | 10 fs | 5 |
| Water reorientation, hydrogen-bond lifetime | 1 to 10 ps | $5\times10^2$ to $5\times10^3$ |
| Side-chain rotamer flips at the surface | 10 ps to 1 ns | $5\times10^3$ to $5\times10^5$ |
| Loop motions, helix formation | 1 ns to 1 µs | $5\times10^5$ to $5\times10^8$ |
| Fast protein folding, small-ligand binding | 1 µs to 1 ms | $5\times10^8$ to $5\times10^{11}$ |
| Unbinding of a nanomolar complex | seconds to hours | $5\times10^{14}$ or more |

An order of magnitude is a factor of ten. The last column is the time divided by the time step: 1 ns is $10^{-9}$ s, and $10^{-9}/(2\times10^{-15}) = 5\times10^{5}$ steps. The primer has a longer table of [time and length scales](physics.html#time-scales). Some words in the first column:

- *Water reorientation* is a water molecule turning to point in a new direction. A *hydrogen-bond lifetime* is how long one hydrogen bond between two molecules lasts before it breaks.
- A *rotamer* is one of the few preferred shapes of an amino-acid side chain. A flip is a jump from one rotamer to another.
- A *loop* is a flexible stretch of the protein chain between helices and strands.
- A *ligand* is a small molecule that binds to a protein.
- A *nanomolar complex* is a pair of molecules that bind tightly. Its dissociation constant, the concentration of free partner at which half of the binding sites are occupied, is about $10^{-9}$ mol/L.

A single GPU today gives roughly 100 to 1,000 ns per day for a solvated protein of 50,000 to 100,000 atoms (the exact figure depends on the hardware, the system and the settings, so measure it for your own system). That is about $5\times10^8$ steps per day at best: one microsecond per day.

A GPU (graphics processing unit) is the kind of processor these programs run on. *Solvated* means surrounded by water. At 100 atoms per nm$^3$, a system of 50,000 to 100,000 atoms fills a cubic box with an edge of about 8 to 10 nm. The arithmetic of the second sentence: 1,000 ns is $10^{-6}$ s, and $10^{-6}/(2\times10^{-15}) = 5\times10^{8}$ steps. A day has 86,400 seconds, so the computer completes about 6,000 passes of the loop every second.

The special-purpose machine Anton reached one millisecond for a small protein in 2010. Seconds are far outside the range of direct simulation, and this gap is the reason Modules 12 to 16 exist: free-energy methods, enhanced sampling, coarse-graining and kinetic models are all ways to answer questions about slow processes without simulating them directly.

At one microsecond per day, a millisecond takes 1,000 days, almost three years, and one second takes a million days, about 2,700 years. Running longer will not reach the last row of the table. The four approaches named above, in one line each:

- **free-energy methods** (Modules 12 and 13) compute how probable two states are relative to each other, without waiting for the system to go from one to the other by itself;
- **enhanced sampling** (Module 14) changes the simulation so that rare events happen more often, and corrects for the change afterwards;
- **coarse-graining** (Module 15) replaces groups of atoms by single particles, so that there is less to compute and the time step can be longer;
- **kinetic models** (Module 16) combine many short simulations into one model of a slow process.

Cost per step is set by the number of pair interactions. With about 100 atoms per nm$^3$ and a 1 nm cutoff, each atom has $\tfrac{4}{3}\pi (1\,\text{nm})^3 \times 100 \approx 420$ neighbours. A 100,000-atom system therefore evaluates about $2\times10^7$ pair interactions per step (each pair counted once), plus the long-range electrostatics.

The arithmetic: a sphere of radius $r$ has the volume $\tfrac43\pi r^3$. With $r = 1$ nm that is 4.19 nm$^3$, and at 100 atoms per nm$^3$ it contains about 420 atoms. These are the **neighbours** of the atom at the centre, the atoms within its cutoff. For 100,000 atoms that makes $100{,}000\times420$ combinations of an atom and a neighbour. Each pair appears twice in this count, once from each of its two atoms, so the number of distinct pairs is half of it, $2.1\times10^7$.

**Long-range electrostatics** is the electric interaction between charges that are further apart than the cutoff. It cannot be left out and is computed separately (Module 7). Combined with the 6,000 steps per second from above, the pair count means that the GPU evaluates more than $10^{11}$ pair interactions every second.

## A short history

<div data-videos="PGqCeSjNuTY eNuV8pYd-is SgH_GcFhQf8"></div>

The list below shows how the pieces of the algorithm arrived one at a time. First came the idea of following particles on a computer, then smooth forces, then a way to cut the cost, then water and a protein, and in the same year as the protein a method that later allowed a longer time step. You do not need the dates. What is worth keeping is the order, and how small and how short the first simulations were compared with the numbers of the previous section. The words that have not been explained yet are collected after the list.

- **1957, [Alder and Wainwright](cite:alder1957).** The first published molecular dynamics simulation: 32 and 108 hard spheres, followed collision by collision. The pressure showed two branches, which pointed to a fluid-solid transition. The method is described in full in [Alder and Wainwright (1959)](cite:alder1959).
- **1964, [Rahman](cite:rahman1964).** 864 argon atoms with a Lennard-Jones potential, a continuous interaction in place of hard spheres and square wells. The pair distribution function agreed well with experiment, and the self-diffusion constant came out within about 20 percent of the measured value.
- **1967, [Verlet](cite:verlet1967).** 864 Lennard-Jones particles, integrated with the simple position recursion that now carries his name, and a table of neighbours, rebuilt every few steps, that cut the cost about tenfold. Velocity Verlet and today's buffered neighbour lists descend from both.
- **1971, [Rahman and Stillinger](cite:rahman1971).** Liquid water, 216 molecules.
- **1977, [McCammon, Gelin and Karplus](cite:mccammon1977).** First protein simulation: the 58-residue inhibitor BPTI, without solvent apart from four buried water molecules and with hydrogens merged into the heavy atoms, for less than 10 ps. The lasting result was qualitative: the interior of a protein is fluid-like, not rigid.
- **1977, [Ryckaert, Ciccotti and Berendsen](cite:ryckaert1977).** SHAKE: an iterative way to keep bond lengths (and, in the paper, angles) fixed at every step. Freezing the fastest motions is what later allowed 2 fs time steps; the paper itself kept the usual step.
- **1980s.** Thermostats and barostats (Andersen, Berendsen, Nosé, Hoover, Parrinello and Rahman), free-energy perturbation applied to biomolecules, the first AMBER, CHARMM, GROMOS and OPLS force fields.
- **1993 to 1995.** Particle-mesh Ewald makes proper long-range electrostatics affordable.
- **2010 to 2011, [Shaw and co-workers](cite:shaw2010).** Millisecond simulation of BPTI and reversible folding of twelve small proteins on Anton.
- **2013.** Nobel Prize in Chemistry to Karplus, Levitt and Warshel for multiscale models of complex chemical systems.
- **Since about 2015.** GPUs make microsecond simulations routine; machine-learned potentials and generative models of ensembles appear (Module 17).

Words used in the list:

- **Hard spheres** are particles that do not interact at all until they touch, and then bounce off each other like billiard balls. There is no smooth force to integrate, so the simulation jumps from one collision to the next. A **square well** adds an attraction: the energy of a pair is lower by a fixed amount whenever the two spheres are closer than a fixed distance. A **continuous interaction** is a pair energy that changes smoothly with distance, such as the Lennard-Jones formula.
- A **branch** is one continuous piece of a curve. A **fluid-solid transition** is freezing or melting.
- The **pair distribution function** (also called the radial distribution function) says how often two atoms are found at a given distance from each other, compared with a completely random arrangement. The **self-diffusion constant** says how fast an atom wanders away from its starting point through the liquid. Both are covered in Module 11.
- A **recursion** is a rule that produces each new value from the ones before it. Verlet's rule gives the next positions from the present and the previous positions (Module 4). The **table of neighbours** is the neighbour list of the algorithm section.
- A **residue** is one amino acid of a protein chain. **Solvent** is the water around the molecule. "Hydrogens merged into the heavy atoms" means that a heavy atom and the hydrogens bonded to it were treated as one particle. A **qualitative** result is a statement about the kind of behaviour, as opposed to a number.
- **Iterative** means repeating a correction until the answer is good enough.
- A **thermostat** is an algorithm that holds the temperature at a set value, and a **barostat** does the same for the pressure (Module 8). **Free-energy perturbation** is a method that computes the free-energy difference between two systems (Module 13).
- **AMBER, CHARMM, GROMOS and OPLS** are families of force fields. AMBER and CHARMM are also the names of MD programs, as in the section on units.
- **Reversible folding** means that a protein folds and unfolds repeatedly within one simulation.
- A **multiscale model** describes different parts of a system at different levels of detail, for example one part with quantum mechanics and the rest with a force field.
- A **machine-learned potential** is an energy function that a machine-learning model, for example a neural network, has learned from reference calculations. A **generative model of ensembles** produces sets of conformations directly, without stepping through time (Module 17).

## What you get out, and the three kinds of error

<div data-videos="XrLfl_b4X5k 4zhx74oR_dM"></div>

A trajectory is a long list of coordinates, and nobody reads it directly. This section says what kinds of number you can extract from it, how an average over frames is related to what an experiment measures, and what can make the number wrong.

MD gives three classes of result:

- **Structure**: average geometries, distributions of distances and angles, radial distribution functions, the ensemble of conformations.
- **Thermodynamics**: averages and fluctuations (energy, density, heat capacity) and, with extra work, free-energy differences.
- **Dynamics**: diffusion constants, relaxation times, rates. These depend on the thermostat and the model more than structural averages do.

Some words in this list:

- A **distribution** of a quantity is the record of how often each value occurs over the frames, usually shown as a histogram. A **conformation** is one three-dimensional shape of a molecule.
- A **fluctuation** is the amount by which a quantity varies around its average. The **heat capacity** is the energy needed to warm the system by one degree. Module 3 shows that it can be computed from the size of the energy fluctuations.
- A **relaxation time** is the time a system needs to settle after a disturbance. A **rate** is the number of events of some kind, such as unbinding, per unit of time.
- The remark on the thermostat: a thermostat (Module 8) changes the velocities to hold the temperature. This can leave the averages correct and still alter how fast things happen, so quantities that depend on timing need more care. The same holds for the model: a force field can give good average structures and still get the speed of a motion wrong.

### From frames to a number: averages and sampling

An experiment on a solution measures a huge number of molecules at the same moment, and each of them is in a different conformation at that moment. The instrument reports the average over all of them. The collection of all the states the system can be in, each with its probability, is called an **ensemble**. The average over it is the **ensemble average**:

$$
\langle A\rangle = \sum_{s} P_s\,A_s .
$$

<div class="legend" markdown="1">
- $A$: any quantity that can be computed from one frame, such as a distance, an angle or an energy. Such a quantity is called an observable.
- $s$: a label that runs over all the states the system can be in. A state is one arrangement of all the atoms, together with their velocities when $A$ depends on them.
- $A_s$: the value of $A$ in state $s$.
- $P_s$: the probability of state $s$, a number between 0 and 1. All the $P_s$ add up to 1. At a fixed temperature, states of low energy are more probable (the Boltzmann distribution, Module 3).
- $\sum_s$: the sum over all states.
- $\langle\ \ \rangle$: angle brackets mean "ensemble average".
</div>

**Read it like this.** Every state contributes its value of $A$, weighted by how probable the state is. For atoms the states form a continuous range, and the sum becomes an integral (Module 3). The idea is the same.

A simulation does something different. It has one copy of the system and follows it in time. What it gives is the **time average** over the saved frames:

$$
\bar A = \frac{1}{M}\sum_{n=1}^{M} A(t_n) .
$$

<div class="legend" markdown="1">
- $M$: the number of saved frames.
- $n$: the label of one frame, from 1 to $M$ (not the `n` of the Python program).
- $t_n$: the time at which frame $n$ was saved.
- $A(t_n)$: the value of $A$ computed from frame $n$.
- $\frac{1}{M}\sum_{n=1}^{M}$: add up the $M$ values and divide by their number. This is the ordinary mean.
- $\bar A$: a bar over a letter means "time average over the trajectory".
</div>

The two averages are equal if the simulated system spends, in each state, a fraction of the time equal to the probability $P_s$ of that state. A system that does this, given enough time, is called **ergodic**, and for such a system $\bar A$ approaches $\langle A\rangle$ as the trajectory gets longer. Module 3 states this as the ergodic hypothesis. The words "given enough time" carry the weight: nothing guarantees that the time you can afford is enough.

**Sampling** is the name for collecting states in this way. Each saved frame is one sample of the ensemble. Good sampling means that the trajectory has visited all the states that matter, in the right proportions. Poor sampling means that it has not had the time. More in the toolbox on [probability](maths.html#probability) and on [averages](maths.html#averages).

<div class="box key" markdown="1">
**Worked example: a side chain with two rotamers.** In rotamer 1 a certain distance is 0.4 nm, and in rotamer 2 it is 0.8 nm. Suppose, as an illustration, that the probabilities are $P_1 = 0.75$ and $P_2 = 0.25$. The ensemble average of the distance is $0.75\times0.4 + 0.25\times0.8 = 0.5$ nm.

A long trajectory with 1,000 frames, 750 of them in rotamer 1 and 250 in rotamer 2, gives the time average $(750\times0.4 + 250\times0.8)/1000 = 0.5$ nm, the same number.

Now suppose that a flip between the rotamers happens about once per microsecond, and that your trajectory is 100 ns long and starts in rotamer 1. Most probably it never leaves. All frames are in rotamer 1 and the time average is 0.4 nm. The result is wrong by 0.1 nm, and nothing in the trajectory warns you: the run finished without an error and the distance looks stable.
</div>

### The three kinds of error

Every number from MD carries three kinds of error, and it helps to keep them apart:

1. **Model error (accuracy of the force field).** The energy function is an approximation. More sampling does not fix this. You detect it by comparing with experiment.
2. **Sampling error (precision).** The trajectory is finite, and consecutive frames are correlated. You detect it with repeats from different starting velocities, block averaging and convergence checks (Module 11).
3. **Set-up and implementation error.** Wrong protonation state, a box that is too small, a thermostat that distorts the ensemble, a cutoff that is inconsistent with the force field. You avoid it by knowing what every setting does, which is the purpose of Modules 7 to 10.

The words in brackets after the first two come from the theory of measurement. **Accuracy** is how close a result is to the true value. **Precision** is how closely repeated measurements agree with each other.

Think of a kitchen scale. A scale that always shows 50 g too much is precise and not accurate: weigh the flour ten times and you get the same wrong number ten times. That is model error, and repeating the simulation does not reveal it. A scale whose display jumps around the right value is accurate on average and not precise, and weighing many times and averaging helps. That is sampling error.

The other terms of the list:

- *Consecutive frames are correlated.* Two frames saved a few picoseconds apart show almost the same conformation, so the second adds little new information. What counts is the number of independent samples, which can be far smaller than the number of frames. The statistical error falls as one over the square root of that number, so halving the error costs four times the simulation time (Module 11).
- *Repeats* are runs of the same system started with different random velocities. *Block averaging* cuts a trajectory into blocks, averages each block and looks at how much the block averages differ. A *convergence check* asks whether the running average still changes as the trajectory gets longer.
- *A box that is too small* lets a molecule interact with its own periodic copy. *A thermostat that distorts the ensemble* holds the temperature but visits the states with the wrong probabilities (Module 8). *A cutoff that is inconsistent with the force field* is a cutoff treatment different from the one used when the parameters were fitted, which changes the model (Modules 6 and 7).

A common mistake is to treat a single long trajectory as "the answer". It is one sample path of a chaotic system. Change the initial velocities and you get a different path with the same statistics, if and only if both runs are long enough.

A **chaotic** system is one in which a tiny difference at the start grows quickly, so that two runs that begin almost alike soon follow entirely different paths (Module 2). A **sample path** is one of the many possible histories of the system. "The same statistics" means the same averages and distributions.

"If and only if" joins two statements: runs that are long enough agree, and runs that are too short cannot be relied on to agree. Read backwards, the first statement gives the test you can use: runs that disagree are not long enough. Agreement proves less, because two short runs can both be stuck in the same state, as in the rotamer example above. The practical rule follows: run several repeats and compare them before you believe any one of them.

## Check yourself

<details markdown="1"><summary>1. Why is the time step about 1 to 2 fs, and what would happen at 10 fs?</summary>
The integrator must take roughly ten or more steps per period of the fastest motion. Bonds to hydrogen vibrate with a period near 10 fs, so unconstrained simulations use 1 fs. With those bonds constrained, the next fastest motions allow 2 fs. At 10 fs the integration of bond and angle vibrations is unstable: energy grows without bound within a few steps and the program stops with an error (in GROMACS usually a LINCS or SETTLE warning).

"Unstable" means that the error of one step makes the error of the next step larger. LINCS and SETTLE are algorithms that hold bond lengths fixed (Module 9).
</details>

<details markdown="1"><summary>2. You double the number of atoms. How does the cost per step change?</summary>
With a cutoff and a neighbour list the number of pairs within the cutoff grows linearly with $N$, so the short-range cost doubles. Particle-mesh Ewald scales as $N\log N$. Without a cutoff the cost would grow as $N^2$.

Here $N$ is the number of atoms. "Grows linearly" means that doubling $N$ doubles the cost. $N\log N$ grows only slightly faster than that. $N^2$ means that doubling $N$ multiplies the cost by four.
</details>

<details markdown="1"><summary>3. A colleague says a 500 ns simulation "shows the binder stays bound, so the affinity is high". What is wrong?</summary>
A complex with a micromolar dissociation constant typically has a residence time of milliseconds or longer, which is thousands of times the simulated time. Both a weak and a strong binder will stay bound for 500 ns. Staying bound only rules out very unstable poses. Affinity is a free-energy difference and needs the methods of Modules 12 and 13.

The dissociation constant is the concentration of free partner at which half of the binding sites are occupied: the smaller it is, the tighter the binding. Micromolar means $10^{-6}$ mol/L. The residence time is the average time a complex stays together before it falls apart. A pose is one way of placing the binder on its target.
</details>

<details markdown="1"><summary>4. Which approximation makes it impossible for a standard force field to describe an enzyme reaction?</summary>
The fixed bonding topology that replaces the electronic problem. The list of bonds is an input, and the bond term is a spring that cannot break.

The bonding topology is the list that says which atoms are bonded to which.
</details>

<details markdown="1"><summary>5. In one pass of the velocity Verlet loop, which line needs the forces at the new positions, and how many force calculations does one pass cost?</summary>
The second half kick. The atoms moved in the drift, and the forces depend on the positions, so the old forces no longer apply. One pass costs one force calculation: the forces computed for the second half kick are kept and used again for the first half kick of the next pass.
</details>

<details markdown="1"><summary>6. A cubic box of water has an edge of 4 nm. About how many atoms does it hold, and how many pair interactions lie within a 1 nm cutoff?</summary>
The volume is $4^3 = 64$ nm$^3$. At about 100 atoms per nm$^3$ that is 6,400 atoms (about 2,100 water molecules). Each atom has about 420 neighbours within 1 nm, and each pair is counted once, so there are $6400\times420/2\approx1.3\times10^6$ pair interactions per step.
</details>

<details markdown="1"><summary>7. The average distance between two domains is 1.20 nm in one 200 ns run and 1.55 nm in a second run that started with different velocities. Which kind of error is this?</summary>
Sampling error. Both runs use the same model and the same set-up, so the difference can only come from their finite length: the system has slow motions that 200 ns does not cover. You need more or longer runs, or an enhanced-sampling method (Module 14). The model error cannot be judged until the sampling error is under control.
</details>

## Exercises

1. Run the Python code above. Plot total, kinetic and potential energy against time. Then increase `dt` to 0.01 and 0.02 and describe what happens to the total energy.
2. Compute the thermal de Broglie wavelength for deuterium and for oxygen at 300 K.
3. A system has 80,000 atoms and runs at 250 ns/day with a 2 fs step. How many pair forces per second is the GPU evaluating, assuming 420 neighbours per atom? How long would 1 ms take?
4. Use the live simulation above with the thermostat on. Find the temperature below which the fluid condenses into a droplet. Why is there no sharp transition in such a small system?

Hints. For exercise 2, follow the worked example for hydrogen and change the mass (deuterium is hydrogen with a nucleus twice as heavy, about 2 u). For exercise 3, follow the arithmetic at the end of the section on time and length scales.

## Read

{{READ}}

## Key papers

{{PAPERS}}
