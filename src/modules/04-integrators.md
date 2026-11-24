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

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

An MD program knows, at one instant, where every atom is and how fast it moves. From the positions it computes the force on every atom (Modules 5 to 7). The **integrator** is the short piece of code that turns "positions, velocities and forces now" into "positions and velocities a moment later". It is applied millions of times in a row, so small faults in it add up, and its properties decide whether a long run can be trusted.

The module has four parts, in this order:

1. **The rule.** The Verlet rule and its two rewritings, velocity Verlet and leap-frog. They are derived step by step from a Taylor expansion and shown to give the same positions.
2. **Why such a simple rule is so good.** A second derivation, from the Liouville operator of Module 2, shows that the rule can be run backwards, keeps the volume of phase space, and conserves a "shadow" energy. This is the most abstract part.
3. **How large the time step can be.** The fastest vibration in the system sets a hard limit, and the usual choices of 1, 2 and 4 fs follow from it.
4. **What else there is.** Higher-order methods, several time steps at once, and integrators with random forces.

If you are short of time, read "The problem", "Verlet from Taylor series" with its subsections and "How large can the time step be?". They are enough to choose a time step and to test it. The Liouville section explains why the method behaves so well and can wait for a second reading.

One small example runs through the whole module: a mass on a spring, with numbers that you can check on a calculator.

<div class="box physics" markdown="1">
**Physics you need here: the harmonic oscillator.** A mass $m$ on a spring of stiffness $k$ feels the force $F = -kx$, where $x$ is its displacement from the rest position. Its acceleration is $a = F/m = -\omega^2x$ with $\omega = \sqrt{k/m}$. The exact motion is a cosine wave. Started at $x_0$ with no velocity, it is $x(t) = x_0\cos\omega t$ and $v(t) = -\omega x_0\sin\omega t$. The number $\omega$ is the **angular frequency**, in radians per unit of time, and one full oscillation takes the **period** $T_{period} = 2\pi/\omega$. The energy $\tfrac12mv^2 + \tfrac12kx^2$ is constant.

Every bond in a molecule behaves like this near its rest length (Module 2). That makes the oscillator the natural test of an integrator: the exact answer is known, so the numerical answer can be compared with it. In the examples below $m = 1$ and $\omega = 1$, so the period is $2\pi\approx6.28$ time units and the acceleration is $a = -x$. More in the [primer](physics.html#oscillator).
</div>

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The notation below first appears in this module. The general conventions (bold letters for vectors, dots for time derivatives, the sum sign) are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\Delta t$ | The **time step**: the small interval of time by which the simulation advances at each step. Typically 1 to 4 fs, where 1 fs is $10^{-15}$ s or 0.001 ps. |
| $\mathbf r(t)$, $\mathbf v(t)$, $\mathbf a(t)$ | Position, velocity and acceleration at the time $t$. The bracket says "at which time". It is not a multiplication. $\mathbf r(t+\Delta t)$ is the position one step later and $\mathbf r(t-\Delta t)$ the position one step earlier. |
| $t+\tfrac{\Delta t}{2}$ | A **half step**: the instant halfway between two steps. |
| $O(\Delta t^4)$ | "Terms of the size of $\Delta t^4$ and smaller, which are left out." Explained in a box below. |
| $x_n$ | The value of $x$ after $n$ steps, that is, at the time $n\,\Delta t$. |
| $x'$, $v'$ | In the formulas for one step, a prime marks the value *after* the step. |
| $e^{iL\Delta t}$ | The **propagator** of Module 2: the operation "advance the system by a time $\Delta t$". |
| $\tilde H$ | The "shadow" version of the Hamiltonian $H$. |
| A formula in a frame | A result to remember. |

<div class="box warn" markdown="1">
**Letters and words that mean two things in this module.**

- $O$ is the order symbol in $O(\Delta t^4)$, and the name of the friction-and-noise step in "BAOAB" (last section).
- $i$ is the label of an atom in sums such as $\sum_i$, and the imaginary unit ($i^2 = -1$) in $iL$ and in $e^{i\theta n}$.
- $n$ counts steps in $x_n$. In the section on multiple time steps it is the number of short steps inside one long step.
- $T_{period}$ is the period of an oscillation. $T$ in $k_BT$ is the temperature. In the answer to question 2 of "Check yourself", a bare $T$ is the period.
- $\Delta t$ (capital delta) is the time step. $\delta t$ (small delta) is the shorter, inner time step of the multiple-time-step scheme.
- $A$ and $B$ are any two operators in the maths boxes and in Exercise 4. In the Liouville section, $A$ alone is also any quantity that depends on the state, as in $dA/dt = iL\,A$. In the last section A and B are the names of the drift and the kick.
- $\mathbf b$ (bold, small) is the third time derivative of the position.
- A prime in $x'$ means "after one step". In the maths boxes the derivative of a function is written out as $df/dt$ to avoid confusion.
- A tilde in $\tilde H$ marks the shadow Hamiltonian. In Module 2 a tilde marked mass-weighted coordinates, and in $\tilde\nu$ it marks a wavenumber.
- "Order" has two uses. A *second-order method* has an error proportional to $\Delta t^2$. In Module 2, a *first-order equation* was one that contains only first derivatives. In this module "order" always has the first meaning.
</div>

## The problem

<div data-videos="dOpKIWFDW0s _CTZDDFaE5A"></div>

Newton's law (Module 2) says that the force on an atom fixes its acceleration, $\mathbf a = \mathbf F/m$. The acceleration is how fast the velocity of the atom is changing at this instant, and the velocity in turn is how fast the position is changing. So the law gives rates of change, and the positions themselves have to be worked out from them. An equation of this kind is called a differential equation. To "integrate the equations of motion" means to add up all these changes and obtain the positions and velocities as functions of time.

<div class="box maths" markdown="1">
**Maths you need here: a differential equation, and what "integrating" it means.** An ordinary equation such as $2x = 6$ asks for a number. A **differential equation** asks for a whole function, and the clue it gives is the rate at which that function changes. The simplest case is $dx/dt = v$ with a constant $v$: "the position changes at the rate $v$". Its solution is $x(t) = x(0) + vt$. You can check it by differentiating: the derivative of $x(0) + vt$ with respect to $t$ is $v$.

To **integrate** (or solve) a differential equation is to find the function from its rate of change. The starting values, here $x(0)$, must be given, because a rate of change says nothing about where the motion began. Newton's law contains the acceleration, the second derivative of the position, so it needs two starting values for every coordinate: a position and a velocity. The letters ODE stand for "ordinary differential equation", which means that there is one independent variable, here the time. More in the [toolbox](maths.html#ode).
</div>

For a single spring the adding up can be done with pen and paper, and the result is the cosine of the box in the plan section. For a protein in water it cannot be done. The force on each atom depends on the positions of thousands of other atoms, all of which are moving, and the forces are not simple functions of the positions (Module 5). No formula for the result exists.

What remains is to advance in small steps. Assume that during a very short time $\Delta t$ the forces change little, use them to move the atoms a little, compute the forces again, and repeat. The short time $\Delta t$ is the **time step**. Each step makes a small error, because the forces do change during the step. The whole subject of this module is how to choose the rule for one step so that these errors do no harm over a long run.

Some notation first. Write $t$ for the present time, $\mathbf r(t)$ for the positions of all atoms at that time, and $\mathbf v(t)$ for their velocities. Then $\mathbf r(t+\Delta t)$ and $\mathbf v(t+\Delta t)$ are the positions and velocities one time step later.

We need $\mathbf r(t+\Delta t)$ and $\mathbf v(t+\Delta t)$ from $\mathbf r(t)$, $\mathbf v(t)$ and the forces. What makes MD different from most numerical ODE problems:

- the force evaluation is by far the most expensive part, so a method should need **one force evaluation per step**;
- we integrate for $10^7$ to $10^{10}$ steps, so **long-time stability** matters more than the accuracy of any single step;
- the system is chaotic, so reproducing the exact trajectory is impossible anyway (Module 2). What we need is correct statistics.

Some words in this list need a comment.

A **force evaluation** is one pass over all interacting atoms that yields the force on every atom. It takes most of the computer time of a step (Module 1). The cost of an integration method is therefore counted in force evaluations, and a method that needs two per step costs twice as much.

The numbers of steps are large because the steps are short. With a time step of 2 fs, $10^7$ steps cover 20 ns and $10^{10}$ steps cover 20 µs. **Long-time stability** means that the errors of all these steps do not build up without limit. A method can be very accurate in each single step and still fail this test, as the section on higher-order methods shows.

**Chaotic** (Module 2) means that two trajectories which start almost at the same point move apart exponentially fast. After a few picoseconds the computed trajectory is no longer the true trajectory from the given starting point, whatever the method. **Correct statistics** means that averages over the trajectory (Module 3) come out right: the mean energy, the distribution of a distance, how often a conformation occurs. That is what MD is used for, and it is a different requirement from following one trajectory accurately.

### The simplest rule, forward Euler, and why it fails

Before the good method, look at the most direct one. It shows what can go wrong. **Forward Euler** takes the velocity and the acceleration at the start of the step and pretends that they stay constant during the step:

$$
\mathbf r(t+\Delta t) = \mathbf r(t) + \mathbf v(t)\,\Delta t,\qquad \mathbf v(t+\Delta t) = \mathbf v(t) + \mathbf a(t)\,\Delta t .
$$

<div class="legend" markdown="1">
- $t$: the present time.
- $\Delta t$: the time step.
- $\mathbf r(t)$, $\mathbf v(t)$: the positions and velocities of the atoms now. The formula holds for every atom and for each of its three coordinates.
- $\mathbf a(t)$: the accelerations now, $\mathbf F/m$, with the forces computed at the present positions.
- $\mathbf r(t+\Delta t)$, $\mathbf v(t+\Delta t)$: the positions and velocities one step later, which the rule computes.
</div>

Read it as "new position = old position + velocity × time" and "new velocity = old velocity + acceleration × time". Try it on the oscillator of the plan section ($a = -x$), started at $x = 1$, $v = 0$, with $\Delta t = 0.5$. The energy is $E = \tfrac12v^2 + \tfrac12x^2$ and should stay at 0.5.

| Step | $x$ | $v$ | Energy |
|---|---|---|---|
| 0 | 1 | 0 | 0.5 |
| 1 | 1 | $-0.5$ | 0.625 |
| 2 | 0.75 | $-1$ | 0.781 |
| 3 | 0.25 | $-1.375$ | 0.977 |

The energy grows by a quarter at every step. This is no accident of the numbers chosen. Write $x'$ and $v'$ for the values after one step, so that $x' = x + v\,\Delta t$ and $v' = v - \omega^2x\,\Delta t$, and compute the new energy:

$$
E' = \tfrac12\left(v - \omega^2x\,\Delta t\right)^2 + \tfrac12\omega^2\left(x + v\,\Delta t\right)^2 = \left(1+\omega^2\Delta t^2\right)E .
$$

<div class="legend" markdown="1">
- $x$, $v$: position and velocity of the oscillator before the step.
- $\omega$: its angular frequency. The acceleration is $a = -\omega^2x$.
- $E = \tfrac12v^2 + \tfrac12\omega^2x^2$: the energy before the step, for a mass of 1.
- $E'$: the energy after the step, the same expression with $x'$ and $v'$.
- $\Delta t$: the time step.
</div>

The step between the two forms: multiply out the two squares. The mixed terms are $-\omega^2xv\,\Delta t$ from the first square and $+\omega^2xv\,\Delta t$ from the second, and they cancel. What is left is $\tfrac12v^2 + \tfrac12\omega^2x^2$ plus the same expression multiplied by $\omega^2\Delta t^2$.

So every Euler step multiplies the energy by a number larger than 1, for any time step. A smaller step slows the growth and does not stop it. With $\omega\Delta t = 0.01$ the factor is 1.0001 per step, which looks harmless. After $10^6$ steps, a short MD run, the energy has grown by $1.0001^{10^6}\approx 3\times10^{43}$.

The reason is geometric. On a curved path the direction of motion changes during the step. Euler keeps going in the direction that was right at the start of the step, so it always leaves the curve on the outside. For the oscillator this turns the closed orbit into an outward spiral. The methods below avoid this by using the velocity from the *middle* of the step.

## Verlet from Taylor series

<div data-videos="g55QvpAev0I qT8pxV53FA4 ld5VABtBkF0"></div>

This section derives the rule on which all the integrators of this module are built. The idea is to write down two predictions, one for the position a short time ahead and one for the position a short time back, and to add them. The largest errors of the two predictions have opposite signs and cancel. The tool for making predictions over a short time is the Taylor expansion.

<div class="box maths" markdown="1">
**Maths you need here: the Taylor expansion in time.** Module 2 used the Taylor expansion to approximate the energy near a minimum. Here the same tool predicts the near future. If you know a smooth function $f$ at a time $t$, and its derivatives at that time, then a short time $\Delta t$ later

$$
f(t+\Delta t) = f(t) + \frac{df}{dt}\,\Delta t + \frac12\frac{d^2f}{dt^2}\,\Delta t^2 + \frac16\frac{d^3f}{dt^3}\,\Delta t^3 + \dots
$$

All derivatives are taken at the time $t$. The first two terms say "keep going at the present rate". The third corrects for the fact that the rate itself is changing, the fourth for the change of that change, and so on. The numbers $\tfrac12$ and $\tfrac16$ are $1/(1\cdot2)$ and $1/(1\cdot2\cdot3)$. The next one would be $\tfrac1{24}$.

Example. Take $f(t) = \cos t$ at $t = 0$. There $f = 1$, $df/dt = -\sin 0 = 0$ and $d^2f/dt^2 = -\cos 0 = -1$. The first three terms give $\cos(0.1)\approx 1 + 0 - \tfrac12(0.1)^2 = 0.995$. The true value is $0.9950042$. More in the [toolbox](maths.html#taylor).
</div>

<div class="box maths" markdown="1">
**Maths you need here: the order symbol.** A Taylor series has to be cut off somewhere, and the terms that are left out are the error. $O(\Delta t^4)$, read "of order $\Delta t$ to the fourth", stands for all of them together and says how large they are: roughly a constant times $\Delta t^4$, where the constant does not depend on $\Delta t$. The notation does not give the constant. What it tells you is how the error reacts when you change the step. For an error of order $\Delta t^4$, halving the step divides the error by $2^4 = 16$.

Example. In the box above, $1 - \tfrac12\Delta t^2$ approximates $\cos\Delta t$ with an error of order $\Delta t^4$, because the first term left out is $\tfrac1{24}\Delta t^4$. With $\Delta t = 0.1$ the error is $4.2\times10^{-6}$. With $\Delta t = 0.05$ it is $2.6\times10^{-7}$, which is 16 times smaller. More in the [toolbox](maths.html#taylor).
</div>

For the position of an atom, the first derivative is the velocity and the second is the acceleration. Expand the position forward and backward in time:

$$
\begin{aligned}
\mathbf r(t+\Delta t) &= \mathbf r(t) + \mathbf v(t)\Delta t + \tfrac12\mathbf a(t)\Delta t^2 + \tfrac16\mathbf b(t)\Delta t^3 + O(\Delta t^4)\\
\mathbf r(t-\Delta t) &= \mathbf r(t) - \mathbf v(t)\Delta t + \tfrac12\mathbf a(t)\Delta t^2 - \tfrac16\mathbf b(t)\Delta t^3 + O(\Delta t^4)
\end{aligned}
$$

<div class="legend" markdown="1">
- $t$: the present time. $\Delta t$: the time step.
- $\mathbf r(t)$: the position of an atom now. The formula holds for every atom and each coordinate.
- $\mathbf r(t+\Delta t)$: its position one step in the future. $\mathbf r(t-\Delta t)$: its position one step in the past.
- $\mathbf v(t)$: its velocity now, the first time derivative of the position.
- $\mathbf a(t)$: its acceleration now, the second time derivative of the position.
- $\mathbf b(t)$: the third time derivative of the position, that is, the rate at which the acceleration is changing.
- $\tfrac12$, $\tfrac16$: the fixed numbers of the Taylor expansion (see the box).
- $O(\Delta t^4)$: all the remaining terms, which contain $\Delta t^4$ or higher powers.
</div>

The second line is the first with $\Delta t$ replaced by $-\Delta t$. The odd powers, $\Delta t$ and $\Delta t^3$, change sign. The even powers do not.

Here $\mathbf b$ is the third time derivative of the position. Add the two lines. The odd terms cancel:

$$
\mathbf r(t+\Delta t) + \mathbf r(t-\Delta t) = 2\mathbf r(t) + \mathbf a(t)\,\Delta t^2 + O(\Delta t^4) .
$$

<div class="legend" markdown="1">
- All symbols: as in the list above. The left side is the sum of the position one step ahead and the position one step back.
</div>

The terms with $\mathbf v$ and with $\mathbf b$ appear once with a plus sign and once with a minus sign, and drop out. The terms with $\mathbf r(t)$ appear twice. So do the terms with $\mathbf a$, and $\tfrac12 + \tfrac12 = 1$. Now subtract $\mathbf r(t-\Delta t)$ from both sides:

$$
\boxed{\mathbf r(t+\Delta t) = 2\mathbf r(t) - \mathbf r(t-\Delta t) + \mathbf a(t)\,\Delta t^2 + O(\Delta t^4)},\qquad \mathbf a = \mathbf F/m .
$$

<div class="legend" markdown="1">
- $\mathbf F$: the force on the atom, computed from the positions at the time $t$.
- $m$: the mass of the atom.
- The frame: this is the rule to remember.
- Other symbols: as in the list above.
</div>

This is the original **Verlet** algorithm (1967). The error of one step is $O(\Delta t^4)$, and the accumulated error over a fixed time is $O(\Delta t^2)$: a second-order method. Velocities do not appear. If needed they come from the difference $\mathbf v(t) = [\mathbf r(t+\Delta t)-\mathbf r(t-\Delta t)]/2\Delta t$, one step late.

**Read it like this.** Rearrange the right side as $\mathbf r(t) + [\mathbf r(t) - \mathbf r(t-\Delta t)] + \mathbf a(t)\Delta t^2$. The square bracket is the displacement of the atom during the last step. So the rule says: repeat the last displacement, then correct it by the acceleration times $\Delta t^2$. With no force the atom repeats the same displacement for ever, which is motion in a straight line at constant speed. The force enters once, at the present positions, so the method needs one force evaluation per step.

In numbers, for the oscillator ($a = -x$, $\Delta t = 0.5$): suppose the previous position was 0.875 and the present position is 1. The acceleration is $-1$, and the new position is $2\times1 - 0.875 + (-1)\times0.25 = 0.875$. One step on, the acceleration is $-0.875$ and the new position is $2\times0.875 - 1 + (-0.875)\times0.25 = 0.53125$. The exact values are $\cos 0.5 = 0.8776$ and $\cos 1 = 0.5403$.

**The velocity formula.** It comes from subtracting the two Taylor lines instead of adding them. Then the even terms cancel, and what is left is $\mathbf r(t+\Delta t) - \mathbf r(t-\Delta t) = 2\mathbf v(t)\Delta t$ plus a term $\tfrac13\mathbf b(t)\Delta t^3$ and smaller ones. Dividing by $2\Delta t$ gives the formula in the text, with an error of order $\Delta t^2$.

"One step late" means that the velocity at the time $t$ needs the position at $t+\Delta t$. You know how fast the atoms were moving only after you have moved them on. That is awkward, because the kinetic energy and the temperature are computed from the velocities.

**The first step.** The rule needs two earlier positions, and at the start of a simulation there is only one set of positions, with velocities. The missing "previous" position is built from them with a Taylor expansion backwards, $\mathbf r(-\Delta t) = \mathbf r(0) - \mathbf v(0)\Delta t + \tfrac12\mathbf a(0)\Delta t^2$. For the oscillator started at rest at $x = 1$ this is $1 - 0 - 0.125 = 0.875$, the value used above.

### Local error and global error

The text above gave two different powers for the error of the Verlet rule, $\Delta t^4$ and $\Delta t^2$. Both are right, because they answer different questions.

The **local error** is the error made in one step that starts from exact values. The **global error** is the error that has built up at a fixed time, say after 10 ps, when many steps have been made. The global error is the one that matters. It is larger, because a shorter step means more steps: reaching a fixed time $t_{end}$ takes $t_{end}/\Delta t$ steps.

For most methods one power of $\Delta t$ is lost on the way. A local error of order $\Delta t^{p+1}$, where $p$ is a whole number, made $t_{end}/\Delta t$ times, gives a global error of order $\Delta t^p$. The **order** of a method is the power in its global error. Forward Euler has a local error of order $\Delta t^2$ (the first Taylor term that it leaves out) and a global error of order $\Delta t$. It is a first-order method.

The Verlet rule loses two powers. It stores no velocity: the velocity is hidden in the difference of two successive positions, divided by $\Delta t$. An error of the size $\Delta t^4$ in one position is therefore the same as an error of the size $\Delta t^3$ in the hidden velocity. Over $t_{end}/\Delta t$ steps these velocity errors add up to the size $\Delta t^2$. A velocity that is wrong by that much for a fixed time gives a position that is wrong by the order $\Delta t^2$.

The table shows all of this for the oscillator with $\omega = 1$, started at $x = 1$ with $v = 0$, where the exact position is $\cos t$. The second column is the error of one Verlet step from exact earlier positions. The other two are the errors in the position at the time $t = 10$.

| $\Delta t$ | One Verlet step | Verlet at $t = 10$ | Forward Euler at $t = 10$ |
|---|---|---|---|
| 0.2 | $-1.3\times10^{-4}$ | $9.2\times10^{-3}$ | $-1.57$ |
| 0.1 | $-8.3\times10^{-6}$ | $2.3\times10^{-3}$ | $-0.57$ |
| 0.05 | $-5.2\times10^{-7}$ | $5.7\times10^{-4}$ | $-0.24$ |
| 0.025 | $-3.3\times10^{-8}$ | $1.4\times10^{-4}$ | $-0.11$ |

Each time the step is halved, the one-step error of Verlet falls by a factor of 16 and its error at a fixed time by a factor of 4. The error of forward Euler falls by a factor between 2 and 3, which approaches 2 as the step gets smaller. Halving the step also doubles the number of force evaluations. A second-order method buys a fourfold gain in accuracy for a twofold cost.

### Velocity Verlet

<div data-videos="ii-N61PeeQU 1kER3-3x8VI"></div>

The Verlet rule has three practical weaknesses. The velocities arrive one step late. The start needs a constructed "previous" position. And the rule adds a very small number, $\mathbf a\,\Delta t^2$, to a combination of two much larger ones, which wastes digits of the computer's arithmetic (see the part on round-off below).

Velocity Verlet produces exactly the same positions and has none of these weaknesses. It stores the positions and the velocities at the same instant.

The form used in practice carries positions and velocities at the same time ([Swope, Andersen, Berens and Wilson, 1982](cite:swope1982)):

$$
\begin{aligned}
\mathbf v(t+\tfrac{\Delta t}{2}) &= \mathbf v(t) + \tfrac{\Delta t}{2}\,\mathbf a(t) &&\text{half kick}\\
\mathbf r(t+\Delta t) &= \mathbf r(t) + \Delta t\,\mathbf v(t+\tfrac{\Delta t}{2}) &&\text{drift}\\
\mathbf v(t+\Delta t) &= \mathbf v(t+\tfrac{\Delta t}{2}) + \tfrac{\Delta t}{2}\,\mathbf a(t+\Delta t) &&\text{half kick}
\end{aligned}
$$

<div class="legend" markdown="1">
- $\mathbf v(t+\tfrac{\Delta t}{2})$: the velocity at the **half step**, the instant halfway between $t$ and $t+\Delta t$. It is an intermediate value, used in the second line and replaced in the third.
- $\mathbf a(t)$: the acceleration at the start of the step, $\mathbf F/m$ with the forces computed at the positions $\mathbf r(t)$.
- $\mathbf a(t+\Delta t)$: the acceleration at the end of the step, from the forces at the new positions $\mathbf r(t+\Delta t)$.
- $\tfrac{\Delta t}{2}$: half a time step.
- "half kick", "drift": the names of the three operations. They are labels and not part of the formulas.
- Other symbols: as in the lists above.
</div>

A **kick** changes the velocities with the forces and leaves the positions alone. A **drift** moves the positions with the velocities and leaves the velocities alone. (Both names were introduced in Module 2.) One step is three operations in a row:

1. *Half kick.* Advance the velocities by half a step with the present forces.
2. *Drift.* Move the positions by a full step with these half-step velocities.
3. *Half kick.* Compute the forces at the new positions and advance the velocities by the second half of the step.

Compare this with forward Euler, which moved the positions with the velocity from the *start* of the step. Velocity Verlet moves them with the velocity from the *middle* of the step, which is a much better estimate of the average velocity during the step. The velocities are treated in the same spirit: half of their change uses the forces at the start and half uses the forces at the end.

The forces are computed once per step, in operation 3. The acceleration $\mathbf a(t+\Delta t)$ found there is kept, and serves as $\mathbf a(t)$ in operation 1 of the next step. In Python the whole step is four lines:

```python
v += 0.5 * dt * a      # half kick with the forces already known
x += dt * v            # drift
a = force(x) / m       # the one force evaluation of this step
v += 0.5 * dt * a      # half kick with the new forces
```

Here `force(x)` stands for whatever routine computes the forces from the positions.

**A shorter way to write it.** Insert the first line of the scheme into the second, and the first into the third. The half-step velocity disappears:

$$
\begin{aligned}
\mathbf r(t+\Delta t) &= \mathbf r(t) + \mathbf v(t)\,\Delta t + \tfrac12\mathbf a(t)\,\Delta t^2\\
\mathbf v(t+\Delta t) &= \mathbf v(t) + \tfrac12\left[\mathbf a(t) + \mathbf a(t+\Delta t)\right]\Delta t
\end{aligned}
$$

<div class="legend" markdown="1">
- $\tfrac12[\mathbf a(t) + \mathbf a(t+\Delta t)]$: the average of the acceleration at the start and at the end of the step.
- Other symbols: as in the list above.
</div>

Read the first line as the Taylor expansion of the position, kept up to the acceleration term. Forward Euler stopped one term earlier. Read the second line as "the velocity changes by the average acceleration times the time".

To see that it is the same algorithm, write the drift for two consecutive steps and subtract: you get $\mathbf r(t+\Delta t) - 2\mathbf r(t)+\mathbf r(t-\Delta t) = \Delta t\,[\mathbf v(t+\tfrac{\Delta t}{2}) - \mathbf v(t-\tfrac{\Delta t}{2})] = \mathbf a(t)\Delta t^2$.

Step by step:

$$
\begin{aligned}
\mathbf r(t+\Delta t) - \mathbf r(t) &= \Delta t\,\mathbf v(t+\tfrac{\Delta t}{2}) &&\text{drift of the step from } t \text{ to } t+\Delta t\\
\mathbf r(t) - \mathbf r(t-\Delta t) &= \Delta t\,\mathbf v(t-\tfrac{\Delta t}{2}) &&\text{drift of the step before}\\
\mathbf v(t+\tfrac{\Delta t}{2}) - \mathbf v(t-\tfrac{\Delta t}{2}) &= \tfrac{\Delta t}{2}\,\mathbf a(t) + \tfrac{\Delta t}{2}\,\mathbf a(t) = \Delta t\,\mathbf a(t) &&\text{the two half kicks at the time } t
\end{aligned}
$$

<div class="legend" markdown="1">
- $\mathbf v(t-\tfrac{\Delta t}{2})$: the half-step velocity of the previous step, halfway between $t-\Delta t$ and $t$.
- Other symbols: as in the lists above.
</div>

Subtract the second line from the first. The left side becomes $\mathbf r(t+\Delta t) - 2\mathbf r(t) + \mathbf r(t-\Delta t)$ and the right side becomes $\Delta t$ times the difference of the two half-step velocities. The third line gives that difference. Between the instants $t-\tfrac{\Delta t}{2}$ and $t+\tfrac{\Delta t}{2}$ the velocity receives two half kicks, the last operation of the earlier step and the first operation of the present one, and both use the same acceleration $\mathbf a(t)$. The result, $\mathbf a(t)\Delta t^2$, is the Verlet rule.

The velocities agree as well. The two half kicks at the time $t$ put $\mathbf v(t)$ exactly in the middle between the two half-step velocities, and the sum of the two drift lines is $\mathbf r(t+\Delta t) - \mathbf r(t-\Delta t) = \Delta t\,[\mathbf v(t+\tfrac{\Delta t}{2}) + \mathbf v(t-\tfrac{\Delta t}{2})] = 2\Delta t\,\mathbf v(t)$. So the velocity of velocity Verlet is the velocity formula of the Verlet rule. The difference is that it is available at once.

<div class="box key" markdown="1">
**Worked example: three velocity Verlet steps by hand.** The oscillator with $m = 1$ and $\omega = 1$, so $a = -x$. Start at $x = 1$, $v = 0$. Time step $\Delta t = 0.5$, which is about 12.6 steps per period.

*Step 1.* The acceleration at the start is $a = -1$.

1. Half kick: $v = 0 + 0.25\times(-1) = -0.25$.
2. Drift: $x = 1 + 0.5\times(-0.25) = 0.875$.
3. New acceleration $a = -0.875$. Half kick: $v = -0.25 + 0.25\times(-0.875) = -0.46875$.

*Step 2.* Half kick: $v = -0.46875 + 0.25\times(-0.875) = -0.6875$. Drift: $x = 0.875 + 0.5\times(-0.6875) = 0.53125$. New acceleration $-0.53125$. Half kick: $v = -0.6875 + 0.25\times(-0.53125) = -0.82031$.

*Step 3.* Half kick: $v = -0.82031 + 0.25\times(-0.53125) = -0.95313$. Drift: $x = 0.53125 + 0.5\times(-0.95313) = 0.05469$. New acceleration $-0.05469$. Half kick: $v = -0.95313 + 0.25\times(-0.05469) = -0.96680$.

| Step | Time | $x$ | $v$ | Exact $x$ | Exact $v$ | Energy $\tfrac12v^2+\tfrac12x^2$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 | 0 | 0.5000 |
| 1 | 0.5 | 0.87500 | $-0.46875$ | 0.87758 | $-0.47943$ | 0.4927 |
| 2 | 1.0 | 0.53125 | $-0.82031$ | 0.54030 | $-0.84147$ | 0.4776 |
| 3 | 1.5 | 0.05469 | $-0.96680$ | 0.07074 | $-0.99749$ | 0.4688 |

The positions are those of the Verlet rule in the section above. The energy is not exactly constant. It dips while $x$ moves towards zero, and it comes back up towards 0.5 whenever $x$ approaches $+1$ or $-1$ again: it oscillates. Compare forward Euler with the same step, where the energy went 0.625, 0.781, 0.977 and kept rising.

For a feeling of the scale: the C-H stretch of Module 2 has $\omega\approx551$ ps$^{-1}$, so $\omega\Delta t = 0.5$ corresponds to $\Delta t = 0.5/551$ ps, about 0.9 fs.
</div>

### Leap-frog

<div data-videos="pVudb6-_FaM"></div>

Velocity Verlet touches the velocities twice in a row: the half kick that ends one step is followed at once by the half kick that begins the next, with the same forces. Leap-frog joins the two into one full kick. It is the same calculation with less bookkeeping.

Merge the second half kick of one step with the first half kick of the next:

$$
\mathbf v(t+\tfrac{\Delta t}{2}) = \mathbf v(t-\tfrac{\Delta t}{2}) + \Delta t\,\mathbf a(t),\qquad
\mathbf r(t+\Delta t) = \mathbf r(t) + \Delta t\,\mathbf v(t+\tfrac{\Delta t}{2}).
$$

<div class="legend" markdown="1">
- $\mathbf v(t-\tfrac{\Delta t}{2})$: the velocity half a step before the time $t$, which was stored at the previous step.
- $\mathbf v(t+\tfrac{\Delta t}{2})$: the velocity half a step after the time $t$, which is stored for the next step.
- $\mathbf a(t)$: the acceleration at the time $t$, from the forces at the positions $\mathbf r(t)$.
- $\mathbf r(t)$, $\mathbf r(t+\Delta t)$: the positions at the start and at the end of the step.
- $\Delta t$: the time step.
</div>

The first formula is the third line of the step-by-step derivation above: two half kicks with the same acceleration make one full kick. The second formula is the drift, unchanged. The velocity at the time $t$ itself is never computed.

Positions live on integer steps and velocities on half steps, "leaping" over each other. This is the default `integrator = md` in GROMACS. The trajectory of positions is identical to velocity Verlet. The only difference is bookkeeping: kinetic energy at time $t$ must be estimated from the two neighbouring half-step velocities, which slightly changes the reported temperature and how thermostats and barostats are coupled.

The table shows what the three schemes store for the oscillator of the worked example ($\Delta t = 0.5$). To start leap-frog from $x = 1$, $v = 0$, the velocity is first moved back by half a kick, to $v(-0.25) = 0 - 0.25\times(-1) = 0.25$.

| Time | 0 | 0.25 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 |
|---|---|---|---|---|---|---|---|
| Verlet, $x$ | 1 | | 0.87500 | | 0.53125 | | 0.05469 |
| Velocity Verlet, $x$ | 1 | | 0.87500 | | 0.53125 | | 0.05469 |
| Velocity Verlet, $v$ | 0 | | $-0.46875$ | | $-0.82031$ | | $-0.96680$ |
| Leap-frog, $x$ | 1 | | 0.87500 | | 0.53125 | | 0.05469 |
| Leap-frog, $v$ | | $-0.25$ | | $-0.6875$ | | $-0.95313$ | |

The three rows of positions are the same numbers. The leap-frog velocities are the half-step velocities of the worked example.

The bookkeeping point in numbers. At the time 0.5 leap-frog knows the velocities $-0.25$ (before) and $-0.6875$ (after). Their average is $-0.46875$, the velocity Verlet value, with kinetic energy $\tfrac12\times0.46875^2 = 0.110$. The average of the two kinetic energies is $\tfrac12(0.0313 + 0.2363) = 0.134$. The two estimates differ by $\tfrac18ma^2\Delta t^2$ for each coordinate, where $m$ is the mass and $a$ the acceleration at that time: a term of order $\Delta t^2$.

The temperature is computed from the kinetic energy (Module 3), and thermostats and barostats (Module 8) act on the temperature and the pressure. The choice of estimate therefore shows up in both.

## Velocity Verlet from the Liouville operator

<div data-videos="5OZO5GPuSJY Uyg9asVcMOc"></div>

The Taylor derivation gave the rule. It did not explain why the energy in the worked example swings back to its starting value, while with forward Euler it grows without limit. This section derives velocity Verlet a second time, in a way that shows where the good behaviour comes from. The idea is to cut the motion into two parts that can each be carried out exactly, and to alternate them.

This is the most abstract section of the module. On a first reading three statements are enough. Velocity Verlet is "half kick, drift, half kick". Each of the three pieces is the exact motion of a simpler system. For that reason the method can be run backwards, keeps the volume of phase space, and conserves an energy very close to the true one.

<div class="box physics" markdown="1">
**Physics you need here: three ideas from Module 2.**

- **Phase space.** The complete state of the system is the list of all positions and all momenta. Module 2 called this list $\Gamma$, one point in phase space. This module uses velocities in the place of momenta. Nothing changes by that, because the momentum of an atom is its mass times its velocity, $\mathbf p_i = m_i\mathbf v_i$.
- **The Hamiltonian** $H = K + U$ is the total energy, kinetic plus potential, written as a function of the state.
- **The Liouville operator** $iL$ is the rule that gives the rate of change of any quantity $A$ that depends on the state: $dA/dt = iL\,A$. From it Module 2 built the **propagator** $e^{iLt}$, the operation "advance the system by a time $t$". The propagator is exact, and for a real system it cannot be computed. An integrator is an approximation to $e^{iL\Delta t}$ that can be computed.
</div>

The Taylor derivation hides *why* the method is so good. The operator derivation ([Tuckerman, Berne and Martyna, 1992](cite:tuckerman1992)) shows it. From Module 2, the state evolves as $\Gamma(t) = e^{iLt}\Gamma(0)$ with

$$
iL = iL_r + iL_p,\qquad iL_r = \sum_i \mathbf v_i\cdot\frac{\partial}{\partial\mathbf r_i},\qquad iL_p = \sum_i \frac{\mathbf F_i}{m_i}\cdot\frac{\partial}{\partial\mathbf v_i}.
$$

<div class="legend" markdown="1">
- $\Gamma(0)$, $\Gamma(t)$: the state of the system (all positions and velocities) at the start and after a time $t$.
- $e^{iLt}$: the propagator, "advance by a time $t$".
- $iL$: the Liouville operator. Treat it as one symbol. The $i$ is the imaginary unit, kept by a convention from quantum mechanics, and $L$ is not the Lagrangian.
- $iL_r$: the position part of $iL$. It describes the change of the positions at the present velocities.
- $iL_p$: the momentum part. It describes the change of the velocities under the present forces. Module 2 wrote it as $\sum_i\mathbf F_i\cdot\partial/\partial\mathbf p_i$, which is the same thing because $\mathbf p_i = m_i\mathbf v_i$.
- $\sum_i$: a sum over all atoms $i$.
- $\mathbf v_i$, $\mathbf F_i$, $m_i$: the velocity of atom $i$, the force on it, and its mass.
- $\partial/\partial\mathbf r_i$, $\partial/\partial\mathbf v_i$: derivatives waiting for a function to act on. They ask "how does the function change when the position (or the velocity) of atom $i$ is changed?"
- The dot between a vector and a derivative: a dot product, the sum over the $x$, $y$ and $z$ components.
</div>

Read it like this. Apply $iL$ to any quantity $A$ and you get $\sum_i\mathbf v_i\cdot\partial A/\partial\mathbf r_i + \sum_i(\mathbf F_i/m_i)\cdot\partial A/\partial\mathbf v_i$. This is the chain rule: $A$ changes because the positions change, at the rate $\mathbf v_i$, and because the velocities change, at the rate $\mathbf F_i/m_i$. The first sum is $iL_r\,A$ and the second is $iL_p\,A$. For one particle on a line, $iL$ applied to $x$ gives $v$ and applied to $v$ gives $F/m$, which is Newton's law.

<div class="box maths" markdown="1">
**Maths you need here: the exponential of a derivative is a shift.** An **operator** is a rule that turns one function into another, for example "differentiate with respect to $x$", written $\partial/\partial x$. Module 2 defined the exponential of an operator by the same series as for a number, $e^{a} = 1 + a + \tfrac12a^2 + \tfrac16a^3 + \dots$, where the square of an operator means "apply it twice".

Put the operator $c\,\partial/\partial x$ in the exponent, with $c$ a constant, and apply the series to a function $f(x)$:

$$
e^{c\,\partial/\partial x}f(x) = f(x) + c\,\frac{\partial f}{\partial x} + \frac12c^2\frac{\partial^2 f}{\partial x^2} + \dots = f(x+c).
$$

The middle expression is the Taylor expansion of $f$ around $x$ with the step $c$, and that is $f(x+c)$. So this operator evaluates the function at a shifted place. Example with $f(x) = x^2$: the series gives $x^2 + c\cdot2x + \tfrac12c^2\cdot2 = x^2 + 2cx + c^2 = (x+c)^2$. It stops there because all higher derivatives of $x^2$ are zero. More in the [toolbox](maths.html#operators).
</div>

Each piece alone is trivial to apply exactly. Because $e^{c\,\partial/\partial x}f(x) = f(x+c)$ (Taylor's theorem), $e^{iL_r\Delta t}$ shifts every position by $\mathbf v\Delta t$ with velocities fixed (a drift), and $e^{iL_p\Delta t}$ shifts every velocity by $\mathbf F\Delta t/m$ with positions fixed (a kick).

In more detail. In $e^{iL_r\Delta t}$ the exponent is $\Delta t\sum_i\mathbf v_i\cdot\partial/\partial\mathbf r_i$. It has the form of the box, with the shift $c = \mathbf v_i\Delta t$ for the position of atom $i$. The velocities count as constants here, because $iL_r$ contains no derivative with respect to a velocity and so does not change them. The result is $\mathbf r_i\to\mathbf r_i + \mathbf v_i\Delta t$: flight in a straight line, as if all forces were switched off.

In $e^{iL_p\Delta t}$ the roles are exchanged. The shift is $c = \mathbf F_i\Delta t/m_i$ for the velocity of atom $i$. It is a constant because the forces depend only on the positions, which this operator does not move. The result is $\mathbf v_i\to\mathbf v_i + \mathbf F_i\Delta t/m_i$: the velocities change as if the atoms were held in place.

Neither piece is the true motion. In the true motion the atoms move and feel forces at the same time, and the forces change as the atoms move. The question is how to combine the two exact pieces into a good approximation of the true motion.

<div class="box maths" markdown="1">
**Maths you need here: operations that do not commute.** Two operations **commute** when the order in which you apply them makes no difference. "Add 3" and "add 5" commute. "Add 3" and "multiply by 2" do not: starting from 1, add and then multiply gives $(1+3)\times2 = 8$, multiply and then add gives $1\times2+3 = 5$.

For two operators $A$ and $B$, the difference between the two orders has a name, the **commutator**:

$$
[A,B] = AB - BA .
$$

$AB$ means "apply $B$ first, then $A$", because the operator written next to the function acts on it first. If the commutator is zero, the operators commute.

For ordinary numbers $e^{a+b} = e^ae^b$. For operators this rule can be relied on only when they commute. When they do not, $e^{A+B}$ ("do both at the same time") and $e^Ae^B$ ("do one, then the other") are different, and the size of the difference is set by the commutator. More in the [toolbox](maths.html#operators).
</div>

The two operators do not commute, so $e^{(iL_r+iL_p)\Delta t} \ne e^{iL_r\Delta t}e^{iL_p\Delta t}$. The symmetric **Trotter (Strang) splitting** is accurate to second order:

$$
e^{iL\Delta t} = e^{iL_p\Delta t/2}\;e^{iL_r\Delta t}\;e^{iL_p\Delta t/2} + O(\Delta t^3).
$$

<div class="legend" markdown="1">
- $e^{iL\Delta t}$: the exact propagator for one time step. This is what we want and cannot compute.
- $e^{iL_p\Delta t/2}$: a kick over half a time step.
- $e^{iL_r\Delta t}$: a drift over a full time step.
- Writing the three next to each other: apply them one after the other.
- $O(\Delta t^3)$: the error of one step, of order $\Delta t^3$.
- $\ne$ (in the sentence above): "is not equal to".
</div>

The drift and the kick do not commute because each one changes what the other one uses. The drift moves the positions, on which the forces depend. The kick changes the velocities, on which the drift depends. The oscillator shows it in two lines. Start at $x = 1$, $v = 0$, with $a = -x$ and $\Delta t = 0.5$.

- Drift first, then kick: the drift gives $x = 1 + 0.5\times0 = 1$, then the kick gives $v = 0 + 0.5\times(-1) = -0.5$. Result: $x = 1$, $v = -0.5$.
- Kick first, then drift: the kick gives $v = -0.5$, then the drift gives $x = 1 + 0.5\times(-0.5) = 0.75$. Result: $x = 0.75$, $v = -0.5$.

The exact answer is $x = 0.8776$, $v = -0.4794$. The two orders miss the exact position on opposite sides, by $+0.12$ and by $-0.13$. The symmetric splitting, with half a kick before the drift and half a kick after it, gave $x = 0.875$, $v = -0.46875$ in the worked example. The two one-sided errors nearly cancel.

Read from right to left: half kick, drift, half kick. That is velocity Verlet. The derivation gives three properties for free. (Tuckerman, Berne and Martyna state the first, reversibility. The other two are standard results for integrators built from exact flows and are not discussed in their paper.)

Why from right to left: in a product of operators the one written last, on the right, stands next to the state and acts first, in the same way that in $\sin(\cos x)$ the cosine is applied first. Here the product is symmetric, so it reads the same in both directions. Its three factors are the three lines of the velocity Verlet scheme.

"Accurate to second order" refers to the global error. The term $O(\Delta t^3)$ is the error of one step in the positions and velocities together. One power is lost over a fixed time, as explained in the section on local and global error, which leaves $\Delta t^2$. This agrees with the Taylor derivation, as it must, because the algorithm is the same.

<details markdown="1"><summary>Optional: why the symmetric product is better than the simple one</summary>
Write $A = iL_p\Delta t$ and $B = iL_r\Delta t$, so that each is proportional to $\Delta t$. Expand every exponential with $e^{X} = 1 + X + \tfrac12X^2 + \dots$ and keep the order of the factors, because $A$ and $B$ do not commute. The exact propagator is

$$
e^{A+B} = 1 + (A+B) + \tfrac12\left(A^2 + AB + BA + B^2\right) + \dots
$$

The simple product is

$$
e^{A}e^{B} = \left(1 + A + \tfrac12A^2\right)\left(1 + B + \tfrac12B^2\right) + \dots = 1 + (A+B) + \tfrac12\left(A^2 + 2AB + B^2\right) + \dots
$$

The two differ already in the terms with two factors: $\tfrac12(2AB) - \tfrac12(AB+BA) = \tfrac12(AB-BA) = \tfrac12[A,B]$. Two factors mean $\Delta t^2$. So the simple product has a one-step error of order $\Delta t^2$ and is a first-order method.

Now the symmetric product, to the same accuracy:

$$
e^{A/2}e^{B}e^{A/2} = \left(1 + \tfrac12A + \tfrac18A^2\right)\left(1 + B + \tfrac12B^2\right)\left(1 + \tfrac12A + \tfrac18A^2\right) + \dots
$$

Collect the terms with two factors. $A^2$ appears as $\tfrac18A^2$ from each of the two outer brackets and as $\tfrac14A^2$ from the product $\tfrac12A\cdot\tfrac12A$, together $\tfrac12A^2$. $AB$ appears once, as $\tfrac12AB$, with the $A$ taken from the left bracket. $BA$ appears once, as $\tfrac12BA$, with the $A$ taken from the right bracket. $B^2$ appears as $\tfrac12B^2$.

The sum is $\tfrac12(A^2 + AB + BA + B^2)$, exactly as in $e^{A+B}$. The commutator has cancelled, and the first disagreement comes with three factors, at the order $\Delta t^3$. Exercise 4 asks you to find those terms.
</details>

**1. Time-reversible.** The product is symmetric, so applying it with $-\Delta t$ exactly undoes a step.

Here is why. A kick with a negative time undoes the kick with the positive time, because the positions, and therefore the forces, are the same in both. A drift with a negative time undoes a drift in the same way.

Now follow a forward step, "half kick, drift, half kick", by a step with $-\Delta t$. The last half kick of the forward step meets the first half kick of the backward step, and the two cancel. That brings the two drifts next to each other, and they cancel. Then the two remaining half kicks cancel. Nothing is left, and the system is back where it started.

The cancellation works only because the sequence is the same read forwards and backwards. In numbers: the worked example went from $x = 1$, $v = 0$ to $x = 0.875$, $v = -0.46875$ in one step. A further step from there with $\Delta t = -0.5$ returns $x = 1$, $v = 0$ exactly.

Module 2 described the same property in another way: stop, reverse all velocities, continue with the usual positive step, and the system retraces its path. The two descriptions are equivalent. Forward Euler does not have the property. Its first step went from $x = 1$, $v = 0$ to $x = 1$, $v = -0.5$, and an Euler step with $\Delta t = -0.5$ from there lands on $x = 1.25$, $v = 0$.

**2. Symplectic.** A drift is the exact flow of the Hamiltonian $K$ alone, and a kick is the exact flow of $U$ alone. Each is therefore a symplectic map, and a composition of symplectic maps is symplectic. One visible consequence: a drift changes $\mathbf r$ by a function of $\mathbf v$ only, and a kick changes $\mathbf v$ by a function of $\mathbf r$ only, so each is a shear in phase space with Jacobian determinant exactly 1, and the numerical map preserves phase-space volume exactly, as the true dynamics does (Liouville's theorem). Symplectic is the stronger property: every symplectic map preserves volume, but not every volume-preserving map is symplectic.

The words of this paragraph, one at a time.

A **map** is a rule that takes each point of phase space to another point. One step of an integrator is a map: a state goes in and a state comes out. The **flow** of a Hamiltonian over a time $\Delta t$ is the map that takes every state to the state it reaches after that time under Hamilton's equations (Module 2). The true motion is the flow of the full Hamiltonian $H = K + U$, where $K$ is the kinetic and $U$ the potential energy.

*The exact flows of $K$ alone and of $U$ alone.* Imagine a system whose energy is only kinetic. With no forces, Hamilton's equations make every atom fly in a straight line, and after a time $\Delta t$ its position is $\mathbf r_i + \mathbf v_i\Delta t$, exactly: the drift. Now imagine a system whose energy is only the potential energy. Its positions do not change, and each momentum changes by $\mathbf F_i\Delta t$, exactly: the kick. Neither system exists in nature, but each piece of the integrator is a true Hamiltonian motion with no approximation in it.

**Symplectic** (Module 2) is the name for maps that keep the special structure which Hamilton's equations give to phase space. Every flow of a Hamiltonian is symplectic. Applying one symplectic map after another (a *composition*) gives a symplectic map again. So "half kick, drift, half kick" is symplectic, for any time step and any force field.

<div class="box maths" markdown="1">
**Maths you need here: a linear map, its matrix and its determinant.** One step of an integrator takes a state $(x, v)$ to a new state $(x', v')$. The map is **linear** when the new values are sums of multiples of the old ones:

$$
x' = M_{11}\,x + M_{12}\,v,\qquad v' = M_{21}\,x + M_{22}\,v .
$$

The four numbers are collected in a table, the **matrix** of the map, and the two equations are written in one line as

$$
\begin{pmatrix}x'\\ v'\end{pmatrix} = \begin{pmatrix} M_{11} & M_{12}\\ M_{21} & M_{22}\end{pmatrix}\begin{pmatrix}x\\ v\end{pmatrix}.
$$

The first row of the matrix gives $x'$ and the second row gives $v'$. The **determinant** of the matrix is the number $M_{11}M_{22} - M_{12}M_{21}$. Its meaning is geometric: the map multiplies every area in the $(x, v)$ plane by this number. A determinant of 1 means that areas are kept. Example: a drift is $x' = x + v\,\Delta t$, $v' = v$, so the matrix has the entries 1, $\Delta t$, 0, 1 and the determinant is $1\times1 - \Delta t\times0 = 1$.

For a map that is not linear, the same role is played by the matrix of the four partial derivatives $\partial x'/\partial x$, $\partial x'/\partial v$, $\partial v'/\partial x$ and $\partial v'/\partial v$, called the **Jacobian matrix**. Its determinant, the Jacobian determinant, is the factor by which the map multiplies a small area around a given point. More in the [toolbox](maths.html#matrices).
</div>

*Shear and volume.* The part of the symplectic property that can be pictured is the conservation of volume. For one particle on a line, phase space is the $(x, v)$ plane. A drift moves every point sideways by $v\,\Delta t$, so points higher up move further. A square of starting states becomes a slanted parallelogram with the same base and the same height, and so with the same area, like a deck of cards pushed sideways. Such a map is called a **shear**.

A kick is a shear in the other direction. It moves every point up or down by an amount that depends on $x$ only. In the language of the box, the Jacobian matrix of a drift has the entries 1, $\Delta t$, 0, 1, and that of a kick has the entries 1, 0, $\Delta t\,(da/dx)$, 1, where $da/dx$ is the slope of the acceleration as a function of the position. Both determinants are exactly 1, whatever the force.

Liouville's theorem (Module 2) says that the true motion keeps the volume of any cloud of states in phase space. The numerical map does the same, exactly, at every step. Forward Euler does not. For the oscillator its matrix has the entries 1, $\Delta t$, $-\omega^2\Delta t$, 1 and the determinant $1 + \omega^2\Delta t^2$, so every step inflates areas. This is the outward spiral again.

On the last sentence of the paragraph: for one particle on a line, keeping the area and being symplectic are the same thing. With more degrees of freedom (independent coordinates: $3N$ for $N$ atoms), symplectic asks for more than keeping the total volume. Module 2 described the extra as the sum of the oriented areas in each coordinate-momentum plane. This extra is what leads to the third property.

**3. A conserved shadow Hamiltonian.** Each sub-step is the exact flow of a Hamiltonian ($K$ or $U$ alone). The Baker-Campbell-Hausdorff formula then shows that the product is the exact flow of a nearby Hamiltonian

$$
\tilde H = H + \Delta t^2\,H_2 + \Delta t^4\,H_4+\dots
$$

<div class="legend" markdown="1">
- $\tilde H$: the **shadow Hamiltonian**, the energy function that the numerical trajectory conserves.
- $H$: the true Hamiltonian, $K + U$, the energy you asked the program to conserve.
- $\Delta t$: the time step.
- $H_2$, $H_4$: correction functions. Like $H$, they are functions of the positions and velocities, with a value at every state. They are fixed by the masses and the force field and do not depend on $\Delta t$.
- The dots: further terms with $\Delta t^6$, $\Delta t^8$ and so on. Only even powers appear, because the splitting is symmetric.
</div>

The numerical trajectory conserves $\tilde H$, not $H$ (up to effects that are exponentially small for small $\Delta t$). Since $\tilde H - H = O(\Delta t^2)$ and is bounded, the true energy **oscillates** around a constant with amplitude $\propto\Delta t^2$ and does not drift. A non-symplectic method has no such protection.

In plain words: the numerical trajectory is the exact trajectory of a slightly different system. That system has an energy of its own, $\tilde H$, and the numerical trajectory conserves it. The energy that the program reports is $H$, which is $\tilde H$ minus $\Delta t^2H_2$ and the smaller terms. Along the numerical trajectory $\tilde H$ stays constant, while $H_2$ takes different values as the atoms move, within a limited range. So the reported energy wobbles inside a band whose width is proportional to $\Delta t^2$ (the sign $\propto$ means "proportional to"), and the band does not move.

The **Baker-Campbell-Hausdorff formula** comes from the mathematics of operators. It answers this question: if $e^Ae^B$ is not $e^{A+B}$, which single exponent $C$ gives $e^Ae^B = e^C$? The answer is a series, $C = A + B + \tfrac12[A,B] + \dots$, in which every further term is built from commutators. Applied to the three factors of the splitting, it says that one velocity Verlet step is the exact propagator of a modified Liouville operator. Because the pieces are flows of Hamiltonians, the modified operator belongs to a Hamiltonian as well, and that Hamiltonian is $\tilde H$.

The remark in brackets is small print. For a general system the series does not have to add up to a finite function. Cut off at a suitable term, it gives a quantity that is conserved up to a remainder which shrinks faster than any power of $\Delta t$ as the step is reduced. For small steps that remainder is far smaller than the $\Delta t^2$ wobble.

"No such protection" is what forward Euler showed. Nothing ties its energy to a conserved quantity, and its errors, all of the same sign, add up step after step.

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

The symbols in the box: $x$ and $v$ are the position and the velocity before the step, $x'$ and $v'$ those after it. The mass is 1, $\omega$ is the angular frequency of the oscillator and $\Delta t$ the time step. The matrix notation is explained in the maths box above.

**Where the matrix comes from.** Carry out the three lines of velocity Verlet with the acceleration $a = -\omega^2x$:

$$
\begin{aligned}
v_{1/2} &= v - \tfrac12\omega^2\Delta t\,x\\
x' &= x + \Delta t\,v_{1/2} = \left(1-\tfrac12\omega^2\Delta t^2\right)x + \Delta t\,v\\
v' &= v_{1/2} - \tfrac12\omega^2\Delta t\,x' = -\omega^2\Delta t\left(1-\tfrac14\omega^2\Delta t^2\right)x + \left(1-\tfrac12\omega^2\Delta t^2\right)v
\end{aligned}
$$

<div class="legend" markdown="1">
- $x$, $v$: position and velocity before the step.
- $v_{1/2}$: the velocity at the half step, after the first half kick.
- $x'$, $v'$: position and velocity after the step.
- $\omega$: the angular frequency of the oscillator.
- $\Delta t$: the time step.
</div>

The first line is the half kick. The second is the drift, with the first line inserted. The third is the second half kick with the new position: insert $v_{1/2}$ and $x'$, and collect the terms with $x$ and the terms with $v$. The numbers in front of $x$ and $v$ in the last two lines are the four entries of the matrix.

**In numbers.** With $\omega = 1$ and $\Delta t = 0.5$ the matrix has the entries 0.875, 0.5, $-0.46875$, 0.875. Applied to the state $x = 1$, $v = 0$ it gives $x' = 0.875$, $v' = -0.46875$, the first step of the worked example. Its determinant is $0.875\times0.875 - 0.5\times(-0.46875) = 0.765625 + 0.234375 = 1$.

The shadow Hamiltonian is $\tilde H = \tfrac12v^2 + \tfrac12\times0.9375\,x^2$. At the start it is $0.46875$. After step 1 it is $\tfrac12\times0.46875^2 + \tfrac12\times0.9375\times0.875^2 = 0.10986 + 0.35889 = 0.46875$. After step 2 it is $0.33646 + 0.13229 = 0.46875$. It does not change, while the true energy in the table of the worked example does.

**The softer spring and the limit.** The spring constant of the oscillator is $\omega^2$ (for a mass of 1). In $\tilde H$ it is multiplied by the bracket $1-\tfrac14\omega^2\Delta t^2$, which is smaller than 1: a softer spring. The true energy and the shadow energy differ by $\tfrac18\omega^4\Delta t^2x^2$. This is the wobble of the previous paragraphs, proportional to $\Delta t^2$, largest when $x$ is largest and zero when $x = 0$. In the worked example it is $0.03125\,x^2$, which is why the energy moved between 0.46875 and 0.5.

When $\omega\Delta t$ is larger than 2 the bracket is negative. Then $\tilde H$ is $\tfrac12v^2$ *minus* a multiple of $x^2$, and conserving it no longer keeps the motion in bounds: $x$ and $v$ can both grow without limit while their combination stays constant. That is the instability of the next section.

<div class="widget" data-widget="integrators"></div>

The demo runs forward Euler, velocity Verlet and the fourth-order Runge-Kutta method (explained in a later section) on this oscillator, started at $x = 1$, $v = 0$, with a slider for the time step. Its default step is 0.5, the step of the worked example. With that step the Verlet energy stays between 0.9375 and 1 times the exact energy, however long the run, and the Euler energy grows by the factor 1.25 at every step. Move the slider beyond 2 to see velocity Verlet fail as well.

## How large can the time step be?

A longer time step means fewer force evaluations for the same simulated time, so you want the longest step that works. There is a hard upper limit. Above it the positions grow without bound within a few steps. For a harmonic oscillator the limit can be computed exactly, and this section does so.

The picture behind the limit is this. The integrator sees the motion only at separate instants, one per step. To follow an oscillation it needs several of these instants in every period, as a film needs several frames per turn of a wheel to show which way the wheel turns.

The calculation uses the Verlet rule for the oscillator. Write $x_n$ for the position after $n$ steps. With the acceleration $a = -\omega^2x_n$, the rule $x_{n+1} = 2x_n - x_{n-1} + a\,\Delta t^2$ becomes the recursion quoted below. The method is to try a solution that oscillates steadily, and to ask when such a solution exists. A steady oscillation is easiest to write with a complex exponential.

<div class="box maths" markdown="1">
**Maths you need here: the complex exponential.** The imaginary unit $i$ is a number defined by $i^2 = -1$. Euler's formula connects the exponential function with the sine and the cosine:

$$
e^{i\theta} = \cos\theta + i\sin\theta .
$$

For a real angle $\theta$ this is a point on a circle of radius 1, at the angle $\theta$. Raising it to the power $n$ turns it further round the circle, $e^{i\theta n} = \cos n\theta + i\sin n\theta$, and it never leaves the circle. So $x_n = e^{i\theta n}$ is a compact way to write "an oscillation that advances by the angle $\theta$ at every step and neither grows nor dies out". Two facts are used below. Multiplying powers adds the exponents, $e^{i\theta(n+1)} = e^{i\theta}e^{i\theta n}$. And

$$
e^{i\theta} + e^{-i\theta} = 2\cos\theta ,
$$

because the two sine terms cancel. The actual position of the oscillator is the real part, $\cos n\theta$. The complex form is used because it makes the algebra shorter. More in the [toolbox](maths.html#complex).
</div>

Insert $x_n = e^{i\theta n}$ into the Verlet recursion for the harmonic oscillator, $x_{n+1} - 2x_n + x_{n-1} = -\omega^2\Delta t^2 x_n$:

$$
\cos\theta = 1 - \tfrac12\omega^2\Delta t^2 .
$$

<div class="legend" markdown="1">
- $x_n$: the position of the oscillator after $n$ steps. $x_{n+1}$ and $x_{n-1}$ are the positions one step later and one step earlier.
- $\theta$: the angle, in radians, by which the numerical oscillation advances in one step. A full oscillation is $2\pi$.
- $i$: the imaginary unit (here it is not the label of an atom).
- $\omega$: the true angular frequency of the oscillator.
- $\Delta t$: the time step.
- $\cos$: the cosine function.
</div>

The steps. Inserting the trial solution gives $e^{i\theta(n+1)} - 2e^{i\theta n} + e^{i\theta(n-1)} = -\omega^2\Delta t^2e^{i\theta n}$. Divide both sides by $e^{i\theta n}$, which leaves $e^{i\theta} - 2 + e^{-i\theta} = -\omega^2\Delta t^2$. By the second formula of the box the left side is $2\cos\theta - 2$. Divide by 2 and move the 1 to the right side.

Read the result like this. The product $\omega\Delta t$ is the angle through which the *true* oscillation turns during one step, and $\theta$ is the angle through which the *numerical* one turns. For a small angle $\cos\theta\approx1-\tfrac12\theta^2$ (the Taylor expansion of the cosine), so for a small step the formula says $\theta\approx\omega\Delta t$: the numerical oscillation keeps pace with the true one.

A real $\theta$ (a bounded oscillation) exists only if

$$
\boxed{\omega\,\Delta t < 2\qquad\Longleftrightarrow\qquad \Delta t < \frac{T_{period}}{\pi}}
$$

<div class="legend" markdown="1">
- $\omega\,\Delta t$: the angle, in radians, through which the true oscillation turns in one time step. It has no unit.
- $\Longleftrightarrow$: "is the same statement as".
- $T_{period}$: the period of the oscillation, $2\pi/\omega$.
- $\pi$: the number 3.14159...
- The frame: the result to remember.
</div>

Where the condition comes from: the cosine of a real angle lies between $-1$ and 1. The right side of the formula for $\cos\theta$ is never above 1, so the only danger is that it falls below $-1$. The condition $1 - \tfrac12\omega^2\Delta t^2 > -1$ is $\omega^2\Delta t^2 < 4$, which is $\omega\Delta t < 2$. For the second form insert $\omega = 2\pi/T_{period}$ and divide by $2\pi$, which gives $\Delta t/T_{period} < 1/\pi$.

In words: the method needs more than $\pi\approx3.14$ steps per period, or it fails. (Exactly at $\omega\Delta t = 2$ the amplitude can still grow, in proportion to the number of steps, so the limit itself is excluded.)

Beyond this the solution grows exponentially. Below it, the numerical frequency is $\omega_{num} = \theta/\Delta t \approx \omega\,(1 + \omega^2\Delta t^2/24)$: slightly too fast.

<div class="legend" markdown="1">
- $\omega_{num}$: the angular frequency of the numerical oscillation. The oscillation advances by the angle $\theta$ in the time $\Delta t$, so its frequency is $\theta/\Delta t$.
- $\omega$: the true angular frequency.
- $\approx$: "is approximately". The formula keeps the first correction and drops smaller ones.
</div>

*Beyond the limit, in numbers.* Take $\omega\Delta t = 2.1$, only 5 % above the limit, and start at $x = 1$, $v = 0$. The positions after successive steps are $-1.2$, $1.9$, $-3.4$, $6.3$, $-11.7$, $21.9$. The sign alternates and the size grows by a factor that settles at 1.88 per step. After ten steps the position is 272. When no real $\theta$ exists, the solution has the form of a number larger than 1 in size raised to the power $n$, and that is exponential growth.

*Below the limit, in numbers.* With $\omega\Delta t = 0.5$ the numerical frequency is $1.011\,\omega$, about 1 % too fast. With $\omega\Delta t = 0.1$ it is $1.0004\,\omega$. A step five times shorter makes the error about 25 times smaller, as a term with $\Delta t^2$ should.

One possible confusion: the box in the previous section said that the conserved quantity $\tilde H$ has a *softer* spring, which suggests a slower oscillation, and here the numerical oscillation is *faster*. Both statements are correct, because the function in the box is conserved by the numerical motion but does not, by itself, generate that motion. If it did, the frequency would be $\omega\sqrt{1-\tfrac14\omega^2\Delta t^2}$, which is too slow, and the true value is too fast.

The Hamiltonian whose exact motion the numerical points follow is the function in the box multiplied by a constant slightly larger than 1. The constant is $1+\tfrac16\omega^2\Delta t^2$ plus terms of order $\Delta t^4$ (1.044 for $\omega\Delta t = 0.5$). A constant in front of a Hamiltonian changes neither the orbits nor what is conserved, and it makes the motion along the orbits faster by that factor. Multiplied out to the order $\Delta t^2$, the product is $\tfrac12\left(1+\tfrac16\omega^2\Delta t^2\right)v^2 + \tfrac12\omega^2\left(1-\tfrac1{12}\omega^2\Delta t^2\right)x^2$: a slightly softer spring together with a slightly lighter mass. The lighter mass wins, and the frequency is $\omega\,(1+\omega^2\Delta t^2/24)$, as found above.

<details markdown="1"><summary>Optional: where the factor 1/24 comes from</summary>
Use the identity $1 - \cos\theta = 2\sin^2(\theta/2)$. The formula $\cos\theta = 1 - \tfrac12\omega^2\Delta t^2$ becomes $2\sin^2(\theta/2) = \tfrac12\omega^2\Delta t^2$, that is,

$$
\sin\frac{\theta}{2} = \frac{\omega\,\Delta t}{2} .
$$

This form shows the stability limit once more: a sine cannot be larger than 1, so $\omega\Delta t$ cannot be larger than 2. For a small number $u$, the angle whose sine is $u$ is $u + \tfrac16u^3 + \dots$ (a Taylor expansion). With $u = \omega\Delta t/2$ this gives $\theta/2\approx\omega\Delta t/2 + (\omega\Delta t)^3/48$, and so $\theta\approx\omega\Delta t\,[1 + (\omega\Delta t)^2/24]$. Dividing by $\Delta t$ gives the numerical frequency.
</details>

### Why the fastest vibration decides

All atoms are advanced with the same time step. A molecule near an energy minimum moves as a sum of normal modes, each one an independent harmonic oscillator with its own frequency (Module 2). The condition $\omega\Delta t < 2$ must hold for every one of them, and the mode with the highest frequency breaks it first. So the fastest vibration in the system sets the limit for everything.

If the condition fails for a single mode, the amplitude of that mode grows at every step. The bond in question stretches further and further, the forces become huge, and the energy spreads to the neighbouring atoms. This is what is meant when a simulation is said to "blow up".

The motions that interest you (a loop that opens, a ligand that leaves) take nanoseconds or longer and could be followed with far longer steps. They do not count. The price is set by the fastest motion present, whether you care about it or not. This is why so much effort goes into removing or slowing the fastest motions, as the table below shows.

The fastest motions in a biomolecule are the stretching vibrations of bonds to hydrogen. Hydrogen is the lightest atom, and Module 2 showed that a small reduced mass gives a high frequency. For the C-H stretch computed there, $\omega\approx551$ ps$^{-1}$ and the period is 11.4 fs, so the stability limit is $2/\omega = 3.6$ fs.

### From the limit to the time steps used in practice

The limit says where the method breaks down. The time steps in actual use are several times shorter, and the table below lists them. Its first row gives a vibration frequency in the unit used by spectroscopists.

<div class="box physics" markdown="1">
**Physics you need here: wavenumbers.** Spectroscopists give the frequency of a vibration as a **wavenumber** $\tilde\nu$ in cm$^{-1}$: the number of wavelengths of the matching infrared light that fit into one centimetre. The frequency is the speed of light times the wavenumber, $\nu = c\tilde\nu$, and the period is $1/\nu$. With $c = 2.998\times10^{10}$ cm/s, a vibration at 3,000 cm$^{-1}$ has the period $1/(2.998\times10^{10}\times3000)$ s $= 1.11\times10^{-14}$ s, about 11 fs. A higher wavenumber means a faster vibration. More in the [primer](physics.html#waves).
</div>

Stability is not accuracy. Real potentials are anharmonic, and energy must also flow correctly between modes, so in practice one uses 10 to 20 steps per period of the fastest motion:

| Fastest motion left in the system | Period | Usual $\Delta t$ |
|---|---|---|
| Bonds to hydrogen (X-H stretch, about 3,000 cm$^{-1}$) | 11 fs | 0.5 to 1 fs |
| Heavy-atom bonds and angles involving H, after constraining X-H bonds | about 20 fs | 2 fs |
| After hydrogen mass repartitioning (H mass about 3 to 4 u) or virtual-site hydrogens | about 30 to 40 fs | 4 fs |
| Coarse-grained beads (Martini) | hundreds of fs | 20 fs |

*Anharmonic* means "not exactly a parabola". The limit above was derived for a perfect spring, and real bonds, and still more the collisions between atoms, are not perfect springs. *Energy must flow between modes*: in a real molecule the vibrations exchange energy with each other, and the simulation has to reproduce this exchange to distribute the energy correctly.

Both need a margin below the hard limit. Stability alone asks for a little more than 3 steps per period. The 10 to 20 steps used in practice are a margin of a factor of about 3 to 6.

How to read the table. The second column is the period of the fastest motion that is still present, and the third is the time step in common use. Dividing one by the other gives the number of steps per period: 11 to 22 in the first row, about 10 in the second, 7.5 to 10 in the third. The third row sits at the lower end of the "10 to 20" quoted above the table, or slightly below it. The range is a rule of thumb and not a strict bound.

- *First row.* All bonds are free to vibrate. X stands for any heavy atom, such as C, N or O.
- *Second row.* The lengths of the bonds to hydrogen are held fixed by a constraint algorithm (Module 9). A bond of fixed length cannot vibrate, so this motion is gone, and the next fastest one sets the step.
- *Third row.* Hydrogen mass repartitioning makes each hydrogen heavier and the atom it is bonded to lighter by the same amount, which slows the remaining motions of the hydrogens. Virtual-site hydrogens are not integrated at all: their positions are rebuilt at every step from the neighbouring heavy atoms. Both are explained in Module 9.
- *Fourth row.* In a coarse-grained model such as Martini (Module 15) one bead stands for several atoms. The bonds between hydrogens and heavy atoms do not exist in the model, and the fastest motions that remain are much slower.

**How to test your own choice.** Run NVE (no thermostat) for a few hundred picoseconds and measure the drift of the total energy. Express it per atom, in units of $k_BT$ per nanosecond, and compare it with what the developers of your MD program consider acceptable: the designers of the GROMACS pair-list scheme, for example, accept about 0.1 $k_BT$ per nanosecond per atom ([Páll and Hess 2013](cite:pall2013)), which is harmless once a thermostat is on. The fluctuation of the energy should fall by a factor of four when you halve the time step. If it does not, something other than the integrator (a cutoff discontinuity, loose constraint tolerance, neighbour-list buffer) is the source.

### Energy drift and energy fluctuation

The test in the paragraph above rests on the difference between two things that you can see in a plot of the total energy against time.

- A **fluctuation** is a rapid wobble of the energy around a constant level. Velocity Verlet must show one: the numerical trajectory conserves the shadow Hamiltonian $\tilde H$, and the true energy differs from it by an amount of order $\Delta t^2$ that changes as the atoms move. The wobble does not grow with the length of the run.
- A **drift** is a slow, steady change of the level itself. It adds up in proportion to the simulated time. A run with a drift slowly heats up or cools down, and it no longer samples the system at one energy.

To separate the two, fit a straight line to the total energy as a function of time. The slope of the line is the drift. The standard deviation of what is left after subtracting the line is the fluctuation.

*NVE* (Module 3) is a run with a fixed number of atoms, volume and energy, which means no thermostat and no barostat. The test has to be run this way, because a thermostat adds and removes energy on purpose and would hide a drift. This is also why a small drift is "harmless once a thermostat is on": the thermostat takes the surplus out as fast as it appears.

*The units.* The total energy grows with the size of the system, so the drift is divided by the number of atoms. It is compared with $k_BT$, the natural scale of thermal energy (Module 3), where $k_B$ is the Boltzmann constant and $T$ the temperature: 2.494 kJ/mol at 300 K. An example with invented numbers: in a system of 30,000 atoms the total energy rises by 50 kJ/mol in 500 ps. Per atom and per nanosecond this is $50/(30{,}000\times0.5) = 0.0033$ kJ/mol, or $0.0033/2.494 = 0.0013$ in units of $k_BT$, far below 0.1.

*The factor of four.* The fluctuation that comes from the integrator is proportional to $\Delta t^2$, so half the step gives a quarter of the fluctuation. The oscillator shows it. Over 30 periods the standard deviation of its energy is 0.01104 with $\Delta t = 0.5$, 0.00276 with $\Delta t = 0.25$ and 0.00069 with $\Delta t = 0.125$: a factor of 4.0 each time.

If your system does not show this factor, part of the energy error has another origin, one that does not follow the $\Delta t^2$ rule. The paragraph names three:

- A *cutoff discontinuity*. Pair interactions are switched off beyond a cutoff distance (Module 7). If the energy jumps there, every pair that crosses the cutoff changes the total energy a little.
- A *loose constraint tolerance*. Constraint algorithms (Module 9) fix the bond lengths only up to a chosen accuracy.
- A *neighbour-list buffer* that is too small. The list of nearby pairs is rebuilt only every few steps (Module 7), and pairs that come within the cutoff between two rebuilds are missed.

### Round-off error

There is a second kind of error, which has nothing to do with the size of the time step. A computer stores a number with a limited count of significant digits: about 7 in **single precision** and about 16 in **double precision**. Whatever does not fit is rounded away. In single precision $1 + 10^{-8}$ is stored as exactly 1, so that this addition has no effect at all.

This matters for integrators because every step adds a small change to a large number. Take an invented case of realistic size: an atom at the coordinate 5 nm, with an acceleration of 83 nm ps$^{-2}$ (a force of 1,000 kJ mol$^{-1}$ nm$^{-1}$ on a mass of 12 u) and a step of 0.002 ps. The Verlet term $a\,\Delta t^2$ is $3.3\times10^{-4}$ nm. In single precision, neighbouring numbers near 5 are $4.8\times10^{-7}$ nm apart, so this term is added with only about three correct digits.

The Verlet rule has a second problem of this kind. Its velocity is hidden in the difference of two positions that are almost equal, and the difference of two nearly equal numbers has few correct digits left. Velocity Verlet and leap-frog store the velocity in a variable of its own, with its full set of digits.

Round-off errors are tiny, but they are made at every step and in every coordinate. Three consequences:

- They break the exact reversibility of the algorithm. A real program does not retrace its path when the velocities are reversed (Module 2).
- Together with chaos they make trajectories irreproducible in detail from one machine to another (Module 2).
- They can produce a slow energy drift that does not depend on $\Delta t$ in the way the integrator's error does. A shorter step does not help, because more steps mean more rounding. The remedy is more digits: double precision throughout, or **mixed precision**, which uses double precision for the few operations that are most sensitive to rounding and single precision for the rest.

## Why not a higher-order method?

<div data-videos="zLnIWwvfuo4"></div>

Velocity Verlet is a second-order method: its error at a fixed time falls by a factor of 4 when the step is halved. Methods of fourth and higher order exist, whose error falls by a factor of 16 or more. It seems natural to use one of them and to take longer steps. This section explains why that does not pay in MD. The candidates are these.

- **Runge-Kutta 4** needs four force evaluations per step. For the same cost you could take four Verlet steps. It is not symplectic: the energy drifts monotonically, as the demo shows.
- **Gear predictor-corrector** methods use one force evaluation and are more accurate than Verlet at small $\Delta t$, but they are neither reversible nor symplectic and drift at the step sizes used in practice. They were common in the 1970s and 1980s and have disappeared from biomolecular codes.
- **Higher-order symplectic** methods (Forest-Ruth, Yoshida) exist but need several force evaluations and do not allow a larger step for stiff molecular systems.

The stiffness of bond vibrations limits $\Delta t$ by stability, not by accuracy, so a higher order buys nothing.

What the names mean:

- A **Runge-Kutta** method computes the forces at several trial points inside one step and combines the results. The classical fourth-order version, RK4, uses four trial points, and so four force evaluations.
- A **predictor-corrector** method stores the acceleration and some higher time derivatives. It predicts the new positions with a Taylor expansion, computes the forces there, and uses the difference between the predicted and the computed acceleration to correct the prediction.
- **Forest-Ruth** and **Yoshida** are the names of splitting methods that chain more kicks and drifts, of specially chosen lengths, inside one step, so that more error terms cancel.

*Monotonically* means always in the same direction. The energy only goes down, or only up, and the change adds up over the run. On the oscillator with $\Delta t = 0.5$, each RK4 step multiplies the energy by 0.99979. That looks harmless. After 30 periods (377 steps) the energy has fallen to 0.924 of its starting value, and it keeps falling.

Velocity Verlet with the same step is less accurate in each single step, and its energy stays between 0.9375 and 1 of the starting value for as long as you run.

A system is called **stiff** when it contains motions on very different time scales and the fastest one dictates the step, although the interest is in the slow ones. A protein is stiff in this sense. Its bonds vibrate in about 10 fs, and the motions of interest take nanoseconds or more.

The sentence after the list carries the argument. The step is capped at a fraction of the fastest period by *stability*, the hard limit of the previous section. A method of higher order improves the *accuracy* at a given step, and accuracy was not what limited the step.

## Multiple time steps

<div data-videos="CRbC_-iGnZM"></div>

The time step is short because of the bonded vibrations. The force evaluation is expensive because of the many non-bonded pairs and the long-range electrostatics. The two facts concern different forces. Multiple-time-step integration uses this: it recomputes the fast-changing, cheap forces at every short step, and the slowly changing, expensive forces less often.

Two terms in the next paragraph. *Bonded forces* come from bonds, angles and torsions (Module 5). *Reciprocal-space electrostatics* is the smooth, long-range part of the electrostatic forces, which the particle-mesh Ewald method (PME) computes on a grid (Module 7).

Forces differ in how fast they change. Bonded forces change on the 10 fs scale, short-range non-bonded forces on the 100 fs scale, and the long-range (reciprocal-space) electrostatics more slowly still. Split $iL_p = iL_p^{fast} + iL_p^{slow}$ and nest the Trotter splitting (r-RESPA):

$$
e^{iL\Delta t} \approx e^{iL_p^{slow}\Delta t/2}\Big[e^{iL_p^{fast}\delta t/2}\,e^{iL_r\delta t}\,e^{iL_p^{fast}\delta t/2}\Big]^{n}e^{iL_p^{slow}\Delta t/2},\qquad \delta t = \Delta t/n .
$$

<div class="legend" markdown="1">
- $e^{iL\Delta t}$: the exact propagator for one outer time step, as in the earlier section.
- $\Delta t$: the **outer** (long) time step, at which the slow forces are applied.
- $\delta t$ (small Greek delta): the **inner** (short) time step, equal to $\Delta t/n$.
- $n$: the number of inner steps in one outer step, a whole number such as 2 or 4. Here $n$ is not a step counter.
- $iL_p^{fast}$: the kick operator that contains only the fast forces, for example the bonded ones.
- $iL_p^{slow}$: the kick operator that contains only the slow forces. The two together are the $iL_p$ of the earlier section.
- $iL_r$: the drift operator, as before.
- $e^{iL_p^{slow}\Delta t/2}$: a half kick with the slow forces over half an outer step.
- $[\ \dots\ ]^{n}$: apply the content of the square bracket $n$ times in a row.
- $\approx$: "is approximately".
</div>

Read it from the outside in. The square bracket is one velocity Verlet step of the length $\delta t$ that uses only the fast forces. One outer step is then:

1. a half kick with the slow forces, over $\Delta t/2$;
2. $n$ short velocity Verlet steps with the fast forces only;
3. a half kick with the slow forces at the new positions, over $\Delta t/2$.

An example with round numbers: $\Delta t = 4$ fs and $n = 2$, so $\delta t = 2$ fs. In 4 fs of simulated time the fast forces are computed twice and the slow forces once. Plain velocity Verlet with a step of 2 fs would compute all forces twice. The name r-RESPA stands for "reversible reference system propagator algorithm".

The cheap fast forces are evaluated every inner step, the expensive slow forces once per outer step. The scheme stays reversible and symplectic. Tuckerman, Berne and Martyna showed the reversibility, and showed on Lennard-Jones test systems that the scheme is more stable at large steps than the earlier, non-reversible RESPA. The resonance limit described next was worked out later. The catch is **resonance**: the slow force is applied as periodic impulses, and when the outer step approaches half the period of the fastest motion the impulses pump energy into it. With constrained bonds to hydrogen this limits the outer step to about 4 to 5 fs. GROMACS, NAMD, OpenMM and Desmond all offer some version of this (for example evaluating PME every second or third step).

The scheme stays reversible and symplectic for the reasons given in the Liouville section. The product reads the same forwards and backwards, and every factor in it is an exact kick or an exact drift. (A Lennard-Jones test system is a set of particles that interact through the Lennard-Jones potential of Module 5, a standard simple model of a liquid.)

**Resonance in plain words.** Push a child on a swing at random moments and little happens. Push in step with the swing and every push adds to the motion. Resonance is this build-up, which occurs when a periodic push matches the rhythm of an oscillation.

In the multiple-time-step scheme the slow force acts only at the ends of the outer steps, as a sudden kick once every $\Delta t$. That is the meaning of "periodic impulses". Between the kicks the fast vibrations run freely. The kick depends on the positions of the atoms, so it depends on where each vibration is in its cycle at that moment.

After half a period a vibration has reversed both its displacement and its velocity. A kick that arrives then is reversed too, since for a small vibration the change of the slow force is proportional to the displacement. It therefore acts on the reversed motion as the previous kick acted on the original motion, and the small effects of successive kicks add up where otherwise they would average out. Half a period is the shortest interval at which this happens. This is why the limit is stated as half the period of the fastest motion.

This rule places the resonance of one ideal oscillator. It does not by itself give the 4 to 5 fs quoted above: half of the "about 20 fs" in the table of time steps is about 10 fs. The lower figure used in practice is stated here without a derivation.

<div class="box key" markdown="1">
**Worked example: resonance in a toy model.** Take one oscillator pulled by two springs: a fast one with $\omega = 1$ (force $-x$) and a weak one with the force $-0.1\,x$, which plays the part of the slow force. Together they give an oscillation with the period $2\pi/\sqrt{1.1} = 5.99$, so half a period is 3.0. Integrate with the scheme above: the fast force in 20 inner steps per outer step, the weak force only in the two outer half kicks. Start at $x = 1$, $v = 0$ and follow 100 outer steps.

| Outer step $\Delta t$ | Largest position reached |
|---|---|
| 2.0 | 1.0 |
| 2.5 | 1.0 |
| 3.0 | $1.6\times10^{6}$ |

With an outer step of 2.0 or 2.5 the oscillation keeps its size. With 3.0, half the period, every outer step multiplies the amplitude by about 1.16. The growth appears for outer steps between about 2.86 and 3.14. Shorter inner steps do not remove it, because the cause is the timing of the outer kicks.
</div>

## Stochastic integrators

So far the equations of motion were Newton's, with nothing random in them. Many simulations add a thermostat to hold the temperature (Module 8), and one widely used thermostat, the Langevin thermostat, changes the equations of motion themselves. The integrator then has to handle a random term. The splitting idea of this module carries over.

<div class="box physics" markdown="1">
**Physics you need here: friction and random force.** A Langevin thermostat treats each atom as if it moved through a fluid of much smaller, invisible particles. The fluid does two things. It slows the atom down with a **friction** force $-\gamma m\mathbf v$, opposite to the velocity $\mathbf v$ and proportional to it, where $m$ is the mass of the atom and $\gamma$ the friction coefficient, in units of one over time. And it hits the atom with many small pushes in random directions, the **random force**. Friction removes kinetic energy and the random pushes add it. The size of the random force is chosen so that the two balance at the wanted temperature. The details are in Module 8. More in the [primer](physics.html#diffusion).
</div>

With a Langevin thermostat (Module 8) the equations of motion gain a friction term and a random force. The same splitting idea applies, with three pieces: B (kick), A (drift), O (the friction-plus-noise part, which can be solved exactly). [Leimkuhler and Matthews](cite:leimkuhler2012) showed that the ordering **BAOAB** cancels the leading $\Delta t^2$ error in averages of functions of the positions. At high friction its configurational error is up to two orders of magnitude smaller than that of the alternatives at the same $\Delta t$; at low friction the methods behave similarly. OpenMM's `LangevinMiddleIntegrator` uses a closely related "middle" discretisation with the same advantage.

*The letters.* A is the drift and B is the kick of the earlier sections, under new names. O acts on the velocities only. With the positions held fixed, friction shrinks each velocity and the random force adds a random amount to it. For this piece alone the result after a time $\Delta t$ is known exactly: the old velocity is multiplied by $e^{-\gamma\Delta t}$, and a random number is added whose typical size is set by the temperature, the mass, $\gamma$ and $\Delta t$.

*The name.* A splitting method is named by its pieces in the order in which they are applied. BAOAB is: half kick, half drift, the full O step, half drift, half kick. Take the O step out, and the two half drifts join into one full drift: what is left is the "half kick, drift, half kick" of velocity Verlet. The same five pieces can be put in other orders, and such orderings are among the "alternatives" of the paragraph above.

*Configurational.* A quantity that depends on the positions only, and not on the velocities, is called configurational: the potential energy, a distance between two atoms, the radius of a protein. Most of what is computed from MD is of this kind. The average of such a quantity over a simulation with a finite step is slightly wrong, with a leading error proportional to $\Delta t^2$. The statement of the paragraph is that for BAOAB the main part of this term cancels: what is left of it shrinks as the friction $\gamma$ grows, so the error falls as $\Delta t^4$ at high friction, and an error proportional to $\Delta t^2$ remains at low friction, as for the alternatives. "Two orders of magnitude" means a factor of 100.

*High and low friction* refer to the size of $\gamma$. At high friction the fluid dominates and the atoms lose the memory of their velocity quickly. At low friction the motion is close to Newton's.

## Check yourself

<details markdown="1"><summary>1. Why does the energy in velocity Verlet oscillate but not drift?</summary>
Because the algorithm is the exact solution of a slightly different Hamiltonian $\tilde H = H + O(\Delta t^2)$. $\tilde H$ is conserved, so $H = \tilde H - O(\Delta t^2)$ varies only by a bounded amount.

Here $H$ is the true Hamiltonian (the energy the program reports), $\tilde H$ the shadow Hamiltonian, and $O(\Delta t^2)$ a difference that is proportional to the square of the time step.
</details>

<details markdown="1"><summary>2. A flexible water model has an O-H stretch at 3,500 cm⁻¹. What is the largest stable time step, and what would you use?</summary>
Period $= 1/(c\tilde\nu) = 1/(2.998\times10^{10}\,\text{cm/s}\times3500\,\text{cm}^{-1}) = 9.5$ fs. Stability limit $T/\pi = 3.0$ fs. For accuracy use 0.5 fs (19 steps per period).

Here $c$ is the speed of light, $\tilde\nu$ the wavenumber of the vibration (see the box on wavenumbers) and $T$ the period.
</details>

<details markdown="1"><summary>3. Positions from leap-frog and velocity Verlet are identical. Why can the reported temperatures differ?</summary>
Leap-frog has velocities at half steps. The kinetic energy at step $t$ is computed as the average of the kinetic energies at $t\pm\Delta t/2$ (or from averaged velocities), which differs from the velocity Verlet on-step value by a term of order $\Delta t^2$.

The sign $\pm$ stands for the two instants half a step before and half a step after the time $t$. The two estimates named in the answer do not behave in the same way. The average of the two half-step kinetic energies is larger than the velocity Verlet value by $\tfrac18ma^2\Delta t^2$ for each coordinate, where $m$ is the mass and $a$ the acceleration at the time $t$. This is the term of order $\Delta t^2$. The kinetic energy from the averaged velocities shows no difference in the plain scheme of this module (no thermostat, no constraints), because there the average of the two half-step velocities is exactly the velocity Verlet velocity at the time $t$.

The numbers for the oscillator are in the leap-frog section.
</details>

<details markdown="1"><summary>4. Your NVE test shows the energy rising linearly, and halving Δt does not change the slope. What do you suspect?</summary>
Not the integrator, whose error scales with $\Delta t^2$. Likely causes: a truncated potential with a jump at the cutoff, a neighbour list updated too rarely (particles enter the cutoff unnoticed), too loose a constraint tolerance, or single-precision arithmetic (the OpenMM developers measured a clear drift in single precision for a system of only 24,000 atoms, which mixed precision removed).
</details>

<details markdown="1"><summary>5. Do one velocity Verlet step by hand: the oscillator with a = −x, started at x = 1, v = 0, with Δt = 0.2.</summary>
The acceleration at the start is $-1$. Half kick: $v = 0 + 0.1\times(-1) = -0.1$. Drift: $x = 1 + 0.2\times(-0.1) = 0.98$. The new acceleration is $-0.98$. Half kick: $v = -0.1 + 0.1\times(-0.98) = -0.198$. The exact values are $\cos 0.2 = 0.98007$ and $-\sin 0.2 = -0.19867$.
</details>

<details markdown="1"><summary>6. You halve the time step of a second-order method. What happens to the error at a fixed simulated time, and to the cost?</summary>
The error falls by a factor of $2^2 = 4$. The cost doubles, because twice as many steps, and so twice as many force evaluations, are needed to reach the same time. For a first-order method such as forward Euler the error would fall only by a factor of 2 for the same doubling of the cost.
</details>

<details markdown="1"><summary>7. Start at x = 1, v = 0 with a = −x and Δt = 0.1. Apply a full drift and then a full kick. Then do it in the other order. What do you find?</summary>
Drift, then kick: $x = 1 + 0.1\times0 = 1$, then $v = 0 + 0.1\times(-1) = -0.1$. Kick, then drift: $v = -0.1$, then $x = 1 + 0.1\times(-0.1) = 0.99$. The two results differ by 0.01 in the position, which is $\Delta t^2$. The drift and the kick do not commute, and this is why a simple "one, then the other" splitting has a one-step error of order $\Delta t^2$.
</details>

## Exercises

1. Starting from the 2×2 matrix in the box above, verify that its determinant is 1 and that $\tilde H$ is conserved. Compute its eigenvalues and show they leave the unit circle when $\omega\Delta t>2$.
2. Implement forward Euler, velocity Verlet and RK4 for the pendulum $\ddot\theta = -\sin\theta$ with large amplitude (anharmonic). Plot energy against time for 1,000 periods.
3. In the Python code from Module 1, run with $\Delta t$ = 0.001, 0.002, 0.004 and 0.008. Measure the standard deviation of the total energy and show on a log-log plot that it scales as $\Delta t^2$.
4. Show by a Taylor expansion that $e^{A/2}e^{B}e^{A/2} = e^{A+B+O(3)}$, where the leading error terms are the double commutators $[B,[B,A]]$ and $[A,[A,B]]$.

Notes on the notation in the exercises:

- *Exercise 1.* The box is the one with the exact result for the harmonic oscillator. Eigenvalues are explained in the [toolbox](maths.html#eigen). Here they are complex numbers, and "the unit circle" is the set of complex numbers of size 1. An eigenvalue outside it means that the map makes some state grow at every step.
- *Exercise 2.* $\theta$ is the angle of the pendulum and $\ddot\theta$ its second time derivative.
- *Exercise 3.* A log-log plot has logarithmic scales on both axes, so that a quantity proportional to $\Delta t^2$ appears as a straight line of slope 2.
- *Exercise 4.* $A$ and $B$ are any two operators, $[A,B] = AB - BA$ is their commutator, $[B,[B,A]]$ is the commutator of $B$ with the commutator $[B,A]$, and $O(3)$ stands for terms with three or more factors of $A$ and $B$.

## Read

{{READ}}

## Key papers

{{PAPERS}}
