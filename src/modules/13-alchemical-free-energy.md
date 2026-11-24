---
num: 13
title: Free energy II, alchemical methods and non-equilibrium work
short: Alchemical free energy
part: Part IV · Free energy and sampling
hours: 8
summary: Derive free-energy perturbation, thermodynamic integration and the Bennett acceptance ratio, set up thermodynamic cycles for relative and absolute binding free energies, and understand the Jarzynski and Crooks relations.
videos: 17
papers: H
tags: free-energy
---

<div class="box goal" markdown="1">
#### After this module you can

- derive the Zwanzig formula, the thermodynamic integration formula and the BAR equation;
- explain why intermediate states and soft-core potentials are needed;
- draw the thermodynamic cycle for a relative binding free energy, including a mutation in a protein binder;
- describe the double-decoupling route to an absolute binding free energy and the role of restraints;
- state the Jarzynski and Crooks relations and what they imply for pulling simulations.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Two questions come up all the time in molecular design: whether adding a methyl group to a ligand makes it bind more tightly, and whether replacing one residue of a protein binder weakens it. Both ask for a difference in binding free energy. Neither can be answered by watching molecules bind and unbind in a simulation, because that takes far longer than a simulation lasts.

The methods of this module answer them by another route. Inside the computer, one molecule is changed into another, or made to vanish, in small steps. No real molecule could follow such a path. The first section explains why the answer is still correct.

The module has five layers:

1. **The idea.** Why a free-energy difference does not depend on the path, and what that allows.
2. **Three ways to compute it.** Free-energy perturbation (FEP), thermodynamic integration (TI) and the Bennett acceptance ratio (BAR), each derived step by step. They are three ways to process the same simulations.
3. **Making the path behave.** Intermediate states, and soft-core potentials for atoms that appear or disappear.
4. **Thermodynamic cycles.** How alchemical changes are combined into quantities that an experiment measures: hydration, relative binding and absolute binding free energies.
5. **Relatives and practice.** Non-equilibrium switching (the Jarzynski and Crooks relations), the cheap end-point methods, how to check a calculation, and what accuracy to expect.

On a first reading the essential parts are the idea, the FEP formula and the reason it fails, the picture behind TI, the relative binding cycle, and the list of good practice. The derivation of the BAR identity and the derivation of the restraint formula are in blocks marked "Optional" and can wait.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The conventions below first appear in this module. The general ones are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\Delta U$, $\Delta A$, $\Delta G$ | A capital delta in front of a quantity is a **difference**: its value in the final state minus its value in the initial state. |
| $\Delta A_{A\to B}$ | The subscript gives the direction, from state A to state B. A negative value means that B is the more favourable state. Reversing the direction changes the sign. |
| $\Delta\Delta G$ | A difference between two differences, for example the binding free energy of ligand B minus that of ligand A. |
| $\langle X\rangle_A$ | The **average** of the quantity $X$ over the configurations that a simulation of state A visits. The subscript says which state was simulated. |
| $\lambda$ | The **coupling parameter**: a number between 0 and 1 that you choose. It says how far the system has been changed from one end state ($\lambda=0$) to the other ($\lambda=1$). |
| $\partial U/\partial\lambda$ | A partial derivative: how fast the potential energy changes when $\lambda$ changes and all atoms stay where they are. |
| $\beta$ | Shorthand for $1/k_BT$. At 300 K, $k_BT=2.494$ kJ/mol, so $\beta=0.401$ mol/kJ. |
| $\ln$ | The natural logarithm, the inverse of the exponential function $e^x$ ([toolbox](maths.html#exp-log)). |
| $G^\circ$, $V^\circ$ | A small circle marks the **standard state**, the agreed reference concentration of 1 mol/L. |
| A formula in a frame | A result to remember. The lines before it are the steps that lead to it. |

Energies are in kJ/mol. The literature on binding often uses kcal/mol, and 1 kcal is 4.184 kJ. The yardstick for every energy in this module is the thermal energy $k_BT$, which is 2.494 kJ/mol or 0.596 kcal/mol at 300 K ([primer](physics.html#units)).

<div class="box warn" markdown="1">
**Letters that mean two things in this module.**

- $A$ is the Helmholtz free energy, and A is also the name of the first of two states (B is the second). In $\Delta A_{A\to B}$ the large $A$ is the free energy and the small letters underneath are the states. In the binding cycles, A and B are two ligands.
- $A$ and $G$ are two free energies, for constant volume and for constant pressure. The first section says when each is used.
- $\sigma$ is a standard deviation in $\sigma_{\Delta U}$ and $\sigma_W$, the size parameter of the Lennard-Jones potential in the section on soft-core potentials, and a symmetry number in the section on absolute binding.
- $K$ with a subscript such as $K_r$ is the force constant of a restraint. $K_d$ is a dissociation constant.
- $P$ is the protein in the cycle diagrams, the pressure in $U+PV$, and a probability density in $P_A(\Delta U)$ and $P_F(W)$.
- $W$ is the work done in a switching simulation. In Module 12 the same letter was the potential of mean force.
- $N$ is the number of atoms in the list under the first formula. Everywhere else it counts saved frames, as do $N_A$ and $N_B$.
- $n$ labels a saved frame. In the sentence about the original soft-core paper, $\lambda^n$, it is a power of $\lambda$.
- $C$ is the freely chosen constant of the Bennett identity, an energy. $C^\circ$ is the standard concentration, 1 mol/L.
- $k_B$ is the Boltzmann constant. In Exercise 1, $k_A$ and $k_B$ are the force constants of two springs.
- "Forward" and "reverse" mean the directions A to B and B to A, except in the convergence plots of the last section, where they refer to the first and the last part of the data.
</div>

## The idea

<div data-videos="ypg1doAqVPM ov0mMvR3wrM a2axeq_E3RQ"></div>

The difference in altitude between two towns is one fixed number. You can measure it along the main road, along a footpath, or along a straight tunnel that nobody has dug, and you get the same answer. Free energy behaves like altitude. This module rests on that one fact.

Module 12 computed free energy along a physical path. For many questions a physical path is too slow to sample: unbinding, or changing one residue into another. Free energy is a state function, so any path between the two end states gives the same difference, including a path with no physical counterpart in which one molecule is gradually turned into another or made to vanish. Because atoms change identity, such paths are called **alchemical**.

Four terms in this paragraph need a closer look.

A **state**, in this module, is a complete description of what is simulated: which atoms are present, with which force-field parameters, at which temperature and volume. In practice a state is a potential-energy function $U(\mathbf r)$, the rule that gives an energy to every arrangement $\mathbf r$ of the atoms (Module 5). State A can be "the protein with ligand A in water" and state B "the same box with ligand B in the place of A". A state covers all the structures that the system visits, each with its probability. A single structure is only one member of it.

A **state function** is a quantity whose value is fixed by the state alone, whatever happened before. Altitude is a state function of your position. The distance you walked to get there is not. The formula below shows why free energy is one: it contains a property of state A, a property of state B, and nothing about any route between them.

A **physical path** is a sequence of states that real molecules pass through, for example a ligand at 0.5 nm from its site, then at 0.6 nm, then at 0.7 nm. Module 12 used such a path, with the distance as the coordinate. An **alchemical path** is a sequence of invented energy functions. The first is $U_A$, the last is $U_B$, and those in between describe a molecule that is partly A and partly B. The computer can simulate them because a simulation only needs an energy function, and you are free to write any energy function you like.

<div class="box physics" markdown="1">
**Physics you need here: the partition function and the free energy.** This is a reminder of [Module 3](03-statistical-mechanics.html).

A **configuration** is one arrangement of all the atoms. At temperature $T$, a configuration with potential energy $U$ occurs with a probability proportional to its **Boltzmann factor** $e^{-U/k_BT}$, where $k_B$ is the Boltzmann constant. Low energies are likely, high energies are exponentially rare.

The **partition function** $Q$ of a state is the sum of the Boltzmann factors of all its configurations. Because positions are continuous, the sum is an integral. A large $Q$ means that the state has many configurations of low energy.

The **Helmholtz free energy** is $A = -k_BT\ln Q$. The minus sign gives a state with more low-energy configurations a lower free energy. Of two states, the one with the lower free energy is the more probable: the ratio of their probabilities is $e^{-\Delta A/k_BT}$.

The smallest example is one particle that moves freely on a line of length $L$, with $U=0$ everywhere on it. Every position has the Boltzmann factor 1, so $Q$ is proportional to $L$. Doubling the length doubles $Q$ and changes the free energy by $-k_BT\ln 2 = -1.73$ kJ/mol at 300 K. No energy changed. The particle only gained room, and free energy counts that. More in the [primer](physics.html#thermodynamics).
</div>

The quantity is always

$$
\Delta A_{A\to B} = -k_BT\ln\frac{Q_B}{Q_A} = -k_BT\ln\frac{\int e^{-\beta U_B(\mathbf r)}d\mathbf r}{\int e^{-\beta U_A(\mathbf r)}d\mathbf r} .
$$

<div class="legend" markdown="1">
- $\Delta A_{A\to B}$: the Helmholtz free energy of state B minus that of state A, in kJ/mol.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature in kelvin. $k_BT$ is about 2.5 kJ/mol at 300 K.
- $\ln$: the natural logarithm.
- $Q_A$, $Q_B$: the partition functions of state A and state B.
- $\mathbf r$: the positions of all $N$ atoms, a list of $3N$ numbers. One value of $\mathbf r$ is one configuration.
- $U_A(\mathbf r)$, $U_B(\mathbf r)$: the potential energy of the configuration $\mathbf r$, computed with the energy function of state A or of state B.
- $\beta$: shorthand for $1/k_BT$.
- $e^{-\beta U}$: the Boltzmann factor of a configuration.
- $\int\dots d\mathbf r$: an integral over all configurations, that is, a sum over every possible arrangement of the atoms ([toolbox](maths.html#integral)).
</div>

The first equality is the definition $A=-k_BT\ln Q$ applied to both states: $\Delta A = A_B-A_A = -k_BT\ln Q_B+k_BT\ln Q_A$, and a difference of two logarithms is the logarithm of the ratio ([toolbox](maths.html#exp-log)).

The second equality writes the two partition functions out. In Module 3, $Q$ also contained integrals over the momenta and constant factors in front. When the atoms keep their masses, these are identical in A and B and cancel in the ratio. What is left is the integral over positions, which Module 3 called the configurational integral. (If masses change too, as when a hydrogen becomes a carbon, the momentum integrals give a factor that depends only on the masses and the temperature. It is the same in every environment, so it cancels in the cycles used later.)

**Read it like this.** $Q_B/Q_A$ says how much more Boltzmann-weighted room state B offers than state A. If the ratio is 10, then $\Delta A = -k_BT\ln 10 = -5.74$ kJ/mol at 300 K, and B is ten times more probable than A. Every further factor of 10 adds another $-5.74$ kJ/mol ($-1.37$ kcal/mol). A ratio below 1 gives a positive $\Delta A$: B is the less favourable state.

Neither $Q_A$ nor $Q_B$ can be computed on its own for a real system (Module 3 explains why). The ratio can, provided the two states share enough of their important configurations. Each method in this module is a way to estimate this ratio from simulations.

**$A$ or $G$?** The formulas are written for a box of fixed volume and give the Helmholtz free energy $A$. Experiments are done at fixed pressure, where the matching quantity is the Gibbs free energy $G$ (Module 3). Simulations at constant pressure use the same formulas with the energy $U$ replaced by $U+PV$, where $P$ is the pressure and $V$ the volume of the box, and the result is $\Delta G$. For changes in liquid water at 1 bar the two numbers are nearly the same. This module writes $\Delta A$ in the derivations and $\Delta G$ where it compares with experiment.

**What you give up.** The intermediate states are not real, so an alchemical calculation says nothing about how a ligand gets into its site or how long that takes. It gives one number, the free-energy difference between the two end states. Those end states are real, and they must be sampled properly.

## Free-energy perturbation

<div data-videos="D_We9YYxpkM bMvzvlqVqzU"></div>

Suppose you have a simulation of state A. Free-energy perturbation (FEP) gets the free energy of state B from it without ever simulating B. Take each saved frame of the A simulation and ask what its energy would be if the system were suddenly B. Frames that B would like count for more, frames that B would dislike count for less. The name says that B is treated as a small disturbance, a perturbation, of A.

<div class="box maths" markdown="1">
**Maths you need here: the average over an ensemble.** The **ensemble** of state A is the collection of all its configurations, each with its Boltzmann probability (Module 3). The average of any quantity $X(\mathbf r)$ over this ensemble is written $\langle X\rangle_A$ and is defined as

$$
\langle X\rangle_A = \frac{\int X(\mathbf r)\,e^{-\beta U_A(\mathbf r)}\,d\mathbf r}{\int e^{-\beta U_A(\mathbf r)}\,d\mathbf r} .
$$

The Boltzmann factor of a configuration divided by the integral in the denominator is the probability density of that configuration. So the formula says: add up $X$ over all configurations, each weighted by its probability.

A simulation of state A visits configurations with these probabilities. In practice the average is therefore the ordinary mean over the $N$ saved frames, $\langle X\rangle_A\approx\frac1N\sum_n X(\mathbf r_n)$, where $\mathbf r_n$ is the configuration in frame $n$. Three frames with $X$ equal to 2, 4 and 9 give $\langle X\rangle = 5$. More in the toolbox: [probability densities](maths.html#probability) and [averages](maths.html#averages).
</div>

The derivation has three steps. It starts from the ratio $Q_B/Q_A$ of the previous section.

**Step 1, a factor of one.** The numerator of the ratio contains $e^{-\beta U_B}$ and the denominator $e^{-\beta U_A}$. To turn the ratio into an average over A, the numerator must contain $e^{-\beta U_A}$ too. Multiply and divide the integrand of the numerator by $e^{-\beta U_A}$:

$$
\frac{Q_B}{Q_A} = \frac{\int e^{-\beta(U_B-U_A)}\,e^{-\beta U_A}d\mathbf r}{\int e^{-\beta U_A}d\mathbf r} = \big\langle e^{-\beta\Delta U}\big\rangle_A ,\qquad \Delta U = U_B-U_A .
$$

<div class="legend" markdown="1">
- $\Delta U$: the energy difference $U_B(\mathbf r)-U_A(\mathbf r)$ of one and the same configuration, computed with the two energy functions. It is positive when the configuration is less comfortable in B than in A.
- $\big\langle\dots\big\rangle_A$: the average over the configurations of state A (see the box above).
- $e^{-\beta\Delta U}$: a weight. It is larger than 1 for a configuration that B likes better than A, and smaller than 1 otherwise.
- Other symbols: as in the list above.
</div>

In symbols, $e^{-\beta U_B} = e^{-\beta U_B}\,e^{+\beta U_A}\,e^{-\beta U_A} = e^{-\beta(U_B-U_A)}\,e^{-\beta U_A}$. Nothing has changed, because $e^{+\beta U_A}e^{-\beta U_A}=1$, and exponents add when exponentials are multiplied. That is the first equality.

**Step 2, recognise an average.** Compare the middle expression with the definition in the box. It is that definition with $X = e^{-\beta\Delta U}$. That gives the second equality.

**Step 3, take the logarithm.** Put the result into $\Delta A=-k_BT\ln(Q_B/Q_A)$:

$$
\boxed{\Delta A_{A\to B} = -k_BT\ln\big\langle e^{-\beta\Delta U}\big\rangle_A}
$$

<div class="legend" markdown="1">
- $\Delta A_{A\to B}$: the free energy of B minus that of A.
- $\big\langle e^{-\beta\Delta U}\big\rangle_A$: the average of the weight $e^{-\beta\Delta U}$ over the frames of a simulation of state A.
- $-k_BT\ln$: turns the average weight back into an energy.
- The frame: a result to remember.
</div>

This is the free-energy perturbation formula of [Zwanzig (1954)](cite:zwanzig1954). Simulate state A, and for each saved configuration evaluate what the energy would be in state B. The formula is exact.

**Read it like this.** The recipe has three steps.

1. Run a simulation with the energy function $U_A$ and save $N$ frames.
2. For every frame $n$, compute the energy of the same coordinates twice, once with $U_A$ and once with $U_B$. The difference is $\Delta U_n$. No new dynamics is run for this. It is a re-evaluation of stored frames.
3. Compute $e^{-\beta\Delta U_n}$ for every frame, take the mean, take the logarithm and multiply by $-k_BT$.

A small example at 300 K, where $k_BT=2.494$ kJ/mol. Three frames have $\Delta U$ equal to 0, 2 and 4 kJ/mol. Their weights $e^{-\beta\Delta U}$ are 1.000, 0.449 and 0.201, with mean 0.550. So $\Delta A = -2.494\times\ln 0.550 = 1.49$ kJ/mol.

The plain mean of $\Delta U$ is 2 kJ/mol. The free energy is lower than that, because the frame with the lowest $\Delta U$ has the largest weight and counts most.

*Exact* means that no approximation was made in the derivation. With infinitely many frames the formula gives the right answer for any two states, however different. The difficulty is that a simulation has a finite number of frames.

### Why FEP fails when the two states overlap poorly

Its practical problem is that the average is dominated by configurations where $\Delta U$ is very negative, that is, configurations typical of B. If A rarely visits them, the estimate is biased and converges extremely slowly.

Here is how strongly one frame can dominate. Measure energies in units of $k_BT$. Suppose 999 of 1,000 frames have $\Delta U=+5\,k_BT$ and one frame has $\Delta U=-5\,k_BT$. The 999 frames together contribute $999\times e^{-5}=6.7$ to the sum of the weights. The single frame contributes $e^{+5}=148$.

The estimate with that frame is $\Delta A=-k_BT\ln(155.1/1000)=1.9\,k_BT$, and without it the estimate would be $5\,k_BT$. One frame in a thousand moves the answer by $3.1\,k_BT$, which is 7.8 kJ/mol at 300 K.

Now imagine that such frames occur once in 100,000 frames and your run has 1,000. Most likely it contains none of them. The estimate is then too high, and nothing in the data warns you, because the frames that matter are absent. This is what **biased** means: the error does not average out, it pushes the result in one direction (here, too high). *Converges slowly* means that a longer run helps only once the rare frames begin to appear.

The word for what is missing is **overlap**. Two states overlap when the configurations that are important for B are visited reasonably often in a simulation of A. Overlap decides whether any of the methods in this module works, and it comes back in every section.

How small must the perturbation be? Expanding in cumulants shows the scale:

$$
\Delta A = \langle\Delta U\rangle_A - \frac{\beta}{2}\,\sigma^2_{\Delta U} + \dots
$$

<div class="legend" markdown="1">
- $\Delta A$: the free-energy difference from A to B, as in the framed formula above.
- $\langle\Delta U\rangle_A$: the mean of $\Delta U$ over the frames of state A.
- $\sigma^2_{\Delta U}$: the **variance** of $\Delta U$ over the same frames, the mean of the squared deviation from the mean. Its square root $\sigma_{\Delta U}$ is the **standard deviation**, the width of the distribution of $\Delta U$ ([toolbox](maths.html#averages)). Here $\sigma$ is not the Lennard-Jones parameter.
- $\beta/2$: half of $1/k_BT$.
- The dots: further terms that depend on finer details of the distribution of $\Delta U$, such as its asymmetry.
- **Cumulants** are a standard series of numbers that describe a distribution. The first is the mean and the second is the variance.
</div>

**Read it like this.** The first term is the average energy cost of switching the energy function from A to B with the atoms frozen where the A simulation put them. The second term lowers it, and it grows with the square of the width of the distribution of $\Delta U$. A width of $1\,k_BT$ lowers $\Delta A$ by $0.5\,k_BT$. A width of $4\,k_BT$ lowers it by $8\,k_BT$, and a correction that large cannot be trusted from a finite sample.

<details markdown="1"><summary>Optional: where the first two terms come from</summary>
Write $m=\langle\Delta U\rangle_A$ for the mean and $\delta=\Delta U-m$ for the deviation of one frame from the mean. Then $\langle e^{-\beta\Delta U}\rangle_A = e^{-\beta m}\,\langle e^{-\beta\delta}\rangle_A$, because $e^{-\beta m}$ is the same for every frame and can be taken out of the average.

For small $\beta\delta$, use the [Taylor expansion](maths.html#taylor) $e^{-x}\approx1-x+\tfrac12x^2$ with $x=\beta\delta$, and average term by term. The average of $\delta$ is zero by its definition. The average of $\delta^2$ is the variance $\sigma^2_{\Delta U}$. So

$$
\big\langle e^{-\beta\delta}\big\rangle_A \approx 1+\tfrac12\beta^2\sigma^2_{\Delta U} .
$$

Take the logarithm, using $\ln(1+y)\approx y$ for small $y$: $\ln\langle e^{-\beta\Delta U}\rangle_A\approx-\beta m+\tfrac12\beta^2\sigma^2_{\Delta U}$. Multiply by $-k_BT=-1/\beta$ to get $\Delta A\approx m-\tfrac{\beta}{2}\sigma^2_{\Delta U}$. Exercise 2 asks you to do this with more care.
</details>

The method works when the standard deviation of $\Delta U$ is no more than 1 to 2 $k_BT$.

The reason can be made precise when the values of $\Delta U$ follow a [Gaussian](maths.html#gaussian) (bell-shaped) distribution with mean $m$ and standard deviation $\sigma$. Multiply the bell curve $e^{-(\Delta U-m)^2/2\sigma^2}$ by the weight $e^{-\beta\Delta U}$ and complete the square in the exponent. The product is a bell curve of the same width, centred at $m-\beta\sigma^2$. The frames that contribute most to the exponential average are therefore those with $\Delta U$ near $m-\beta\sigma^2$, which lies $\beta\sigma$ standard deviations below the mean.

For $\sigma=1\,k_BT$ that is one standard deviation below the mean, and 16 % of the frames lie at or beyond it. For $\sigma=2\,k_BT$ it is 2.3 % of the frames. For $\sigma=4\,k_BT$ it is 0.003 %, about one frame in 30,000.

By Jensen's inequality, $\Delta A\le\langle\Delta U\rangle_A$ always.

<div class="box maths" markdown="1">
**Maths you need here: Jensen's inequality.** A function is **convex** if its graph curves upward, like a bowl. $e^{-x}$ is convex. For a convex function, the average of the function is never smaller than the function of the average.

Example with two values, $x=0$ and $x=2$. The average of $e^{-x}$ is $(1+0.135)/2=0.568$. The function at the average, $x=1$, is $e^{-1}=0.368$, which is smaller.

Applied here: $\langle e^{-\beta\Delta U}\rangle_A\ge e^{-\beta\langle\Delta U\rangle_A}$. Take the logarithm of both sides and multiply by $-k_BT$. Multiplying by a negative number turns the inequality round, and the result is $\Delta A\le\langle\Delta U\rangle_A$.
</div>

In physical terms, $\langle\Delta U\rangle_A$ is the cost of switching to B without letting the atoms respond. When they are allowed to relax into the arrangements that B prefers, the free energy can only go down.

**Two directions.** Nothing in the derivation singles out A. Exchange the roles of the two states and you get the same formula for a simulation of B: $\Delta A_{B\to A}=-k_BT\ln\langle e^{+\beta\Delta U}\rangle_B$. The sign in the exponent has changed because the energy difference seen from B is $U_A-U_B=-\Delta U$. Since $\Delta A_{A\to B}=-\Delta A_{B\to A}$, this is a second estimate of the same number. The run from A is called the forward direction and the run from B the reverse direction.

With perfect sampling the two directions agree. With poor overlap the forward estimate of $\Delta A_{A\to B}$ comes out too high and the reverse estimate too low. The gap between them is called the **hysteresis**, and a large one is a warning. The Bennett method below combines the two directions into one better estimate.

### Intermediate states

If A and B are too different for one step, take several. Insert states between them, close enough that each neighbouring pair overlaps well.

To keep the perturbation small, connect A and B through a chain of intermediate Hamiltonians indexed by a **coupling parameter** $\lambda\in[0,1]$, for example

$$
U(\lambda) = (1-\lambda)\,U_A+\lambda\,U_B ,
$$

and add up the steps: $\Delta A = \sum_k\Delta A_{\lambda_k\to\lambda_{k+1}}$. Typical calculations use 10 to 40 or more values of $\lambda$, each a separate simulation.

<div class="legend" markdown="1">
- $\lambda$: the coupling parameter, a pure number that you set. It is a control knob of the calculation and not a physical quantity such as a temperature.
- $\lambda\in[0,1]$: "$\lambda$ lies between 0 and 1, both ends included".
- $U(\lambda)$: the potential-energy function of the intermediate state. It also depends on the positions of the atoms, which are not written.
- $U_A$, $U_B$: the potential-energy functions of the two end states.
- $(1-\lambda)$ and $\lambda$: the two mixing weights. They add up to 1.
- $k$: a label that numbers the chosen values of $\lambda$ in increasing order. $\lambda_k$ is value number $k$.
- $\sum_k$: add up over all steps from one value of $\lambda$ to the next.
- $\Delta A_{\lambda_k\to\lambda_{k+1}}$: the free-energy difference between two neighbouring values of $\lambda$.
</div>

*Hamiltonian* is the name from Module 2 for the function that gives the total energy of a system, kinetic plus potential. In this field the word is used loosely for "the energy function that defines a state", because the kinetic part is not what changes. A **hybrid Hamiltonian** is an energy function between those of A and B.

**Read it like this.** At $\lambda=0$ the formula gives $U_A$, at $\lambda=1$ it gives $U_B$, and at $\lambda=0.5$ every configuration gets the mean of its two energies. Take an atom whose partial charge is $-0.5\,e$ in A and 0 in B. Its Coulomb energy with the unchanged atoms is proportional to its charge, so under this mixing rule the atom behaves at $\lambda=0.3$ as if it carried $-0.35\,e$. No such atom exists in chemistry. The simulation runs all the same, because the program only needs a rule that turns positions into an energy.

Adding up the steps is allowed because free energy is a state function: $A(\lambda_2)-A(\lambda_0)=[A(\lambda_1)-A(\lambda_0)]+[A(\lambda_2)-A(\lambda_1)]$, and so on along the chain. The simulation at one value of $\lambda$ is called a **window**.

Why the chain helps: with the linear mixing above, the energy difference between two neighbouring windows is $U(\lambda_{k+1})-U(\lambda_k)=(\lambda_{k+1}-\lambda_k)(U_B-U_A)$. Twenty equal steps (21 windows) make each difference twenty times smaller than the full $U_B-U_A$, and its standard deviation shrinks roughly in proportion. A perturbation with a spread of $20\,k_BT$, hopeless in one step, becomes twenty steps with a spread near $1\,k_BT$ each.

The windows do not have to be equally spaced. Put them closer together where the system changes fastest with $\lambda$. The overlap matrix described below shows where that is. The linear rule is only one example of a path. It fails when atoms appear or disappear, and the section on soft-core potentials replaces it there.

## Thermodynamic integration

<div data-videos="iCzHM5Lb_m8"></div>

FEP compares neighbouring states. Thermodynamic integration (TI) measures a slope. Think of the altitude picture again: you can find the height difference between two towns by measuring how steep the road is at many points and adding up slope times distance. Here the road is the coupling parameter $\lambda$ and the altitude is the free energy $A(\lambda)$. The slope $dA/d\lambda$ turns out to be an ordinary average that a simulation at fixed $\lambda$ can measure.

<div class="box maths" markdown="1">
**Maths you need here: differentiating a logarithm and an integral.** Two rules are used.

*The derivative of a logarithm.* $\dfrac{d}{dx}\ln f(x)=\dfrac{1}{f}\dfrac{df}{dx}$, by the [chain rule](maths.html#chain-rule). Example: $\frac{d}{dx}\ln(x^2)=\frac{1}{x^2}\,2x=\frac2x$.

*The derivative of an integral with respect to a parameter.* If the integrand depends on a parameter $\lambda$ that is not the variable of integration, you may differentiate inside the integral: $\frac{d}{d\lambda}\int g(x,\lambda)\,dx=\int\frac{\partial g}{\partial\lambda}\,dx$. An integral is a sum, and the derivative of a sum is the sum of the derivatives. Example: for $g = e^{-\lambda x}$, $\partial g/\partial\lambda = -x\,e^{-\lambda x}$, again by the chain rule.

The symbol $\partial$ marks a [partial derivative](maths.html#partial-derivative): only $\lambda$ changes, and the positions of the atoms are held fixed.
</div>

Treat $A(\lambda) = -k_BT\ln Q(\lambda)$ as a function of $\lambda$ and differentiate:

$$
\frac{dA}{d\lambda} = -\frac{k_BT}{Q}\frac{\partial Q}{\partial\lambda} = \frac{\int\frac{\partial U}{\partial\lambda}\,e^{-\beta U(\lambda)}d\mathbf r}{\int e^{-\beta U(\lambda)}d\mathbf r} = \left\langle\frac{\partial U}{\partial\lambda}\right\rangle_\lambda .
$$

<div class="legend" markdown="1">
- $A(\lambda)$: the free energy of the intermediate state with coupling parameter $\lambda$.
- $dA/d\lambda$: the slope of the free energy along $\lambda$. Because $\lambda$ has no unit, the slope is an energy, in kJ/mol.
- $Q$, short for $Q(\lambda)$: the partition function of that intermediate state, $\int e^{-\beta U(\mathbf r,\lambda)}d\mathbf r$ up to constant factors.
- $U(\lambda)$: the potential-energy function at this $\lambda$. It depends on the positions $\mathbf r$ as well.
- $\partial U/\partial\lambda$: how fast the energy of one fixed configuration changes when $\lambda$ is changed. It is a function of the positions, and it has a value in every frame.
- $\left\langle\dots\right\rangle_\lambda$: the average over the configurations of a simulation run at this value of $\lambda$.
- $k_B$, $T$, $\beta$, $\mathbf r$, $\int\dots d\mathbf r$: as before.
</div>

The line contains three steps.

**Step 1, the logarithm.** The first rule of the box, applied to $A=-k_BT\ln Q$, gives $dA/d\lambda=-(k_BT/Q)\,\partial Q/\partial\lambda$. Any constant factor in front of the integral in $Q$ cancels between $1/Q$ and $\partial Q/\partial\lambda$.

**Step 2, the integral.** The second rule of the box gives

$$
\frac{\partial Q}{\partial\lambda} = \int\left(-\beta\,\frac{\partial U}{\partial\lambda}\right)e^{-\beta U(\mathbf r,\lambda)}\,d\mathbf r .
$$

<div class="legend" markdown="1">
- $-\beta\,\partial U/\partial\lambda$: the factor that the chain rule brings down from the exponent when $e^{-\beta U}$ is differentiated with respect to $\lambda$.
- Other symbols: as in the list above.
</div>

Multiply this by $-k_BT/Q$. The two minus signs give a plus, and $k_BT\times\beta=1$. What remains is the middle expression of the first line.

**Step 3, recognise an average.** The middle expression is the definition of an ensemble average (the box in the previous section) with $X=\partial U/\partial\lambda$, taken in the state whose energy function is $U(\lambda)$.

So the slope of the free energy along $\lambda$ is the average, over a simulation run at that $\lambda$, of how fast the energy function changes with $\lambda$. To get the whole difference, add up the slopes. The integral of a derivative is the difference of the function between the two ends, $A(1)-A(0)=\int_0^1(dA/d\lambda)\,d\lambda$, so

$$
\boxed{\Delta A = \int_0^1\left\langle\frac{\partial U}{\partial\lambda}\right\rangle_\lambda d\lambda}
$$

<div class="legend" markdown="1">
- $\Delta A$: the free energy at $\lambda=1$ (state B) minus that at $\lambda=0$ (state A).
- $\int_0^1\dots d\lambda$: the integral over $\lambda$ from 0 to 1, that is, the area under the curve of the averages plotted against $\lambda$.
- $\left\langle\partial U/\partial\lambda\right\rangle_\lambda$: the average slope measured in the simulation at $\lambda$, in kJ/mol.
</div>

This is thermodynamic integration. It goes back to [Kirkwood (1935)](cite:kirkwood1935), who switched on the interaction of one molecule with the rest of a fluid through a coupling parameter and wrote its chemical potential as an integral of the mean interaction energy over that parameter. (The **chemical potential** is the free-energy change when one molecule is added to a system.)

**What $\partial U/\partial\lambda$ is in practice.** With the linear mixing rule $U(\lambda)=(1-\lambda)U_A+\lambda U_B$, the derivative is $\partial U/\partial\lambda=U_B-U_A=\Delta U$, the same energy difference that FEP uses. For other mixing rules, such as the soft-core form below, it is a different function of the positions. The simulation program evaluates it during the run, along with the forces.

**Read it like this.** Run one simulation per window. In each, average $\partial U/\partial\lambda$ over the frames. Plot the averages against $\lambda$ and compute the area under the curve. With linear mixing the first point of the curve, at $\lambda=0$, is $\langle\Delta U\rangle_A$, the first term of the cumulant formula of the previous section.

From there the curve can only fall when the mixing is linear. Its slope is then $-\beta$ times the variance of $\Delta U$ in that window, and a variance is never negative. The stronger the fluctuations of $\Delta U$, the faster the curve bends, and the more windows you need there.

<div class="box maths" markdown="1">
**Maths you need here: the trapezoid rule.** An integral is the area under a curve ([toolbox](maths.html#integral)). When the curve is known only at a few points, join neighbouring points by straight lines and add up the areas of the trapezoids underneath. Each trapezoid has the area "width times the mean of its two heights".

Example: the averages are 30, 10 and $-2$ kJ/mol at $\lambda$ equal to 0, 0.5 and 1. The first trapezoid gives $0.5\times(30+10)/2=10$ and the second $0.5\times(10-2)/2=2$, so $\Delta A\approx12$ kJ/mol. Computing an integral from a few points in this way is called **quadrature**, and the error it makes is the quadrature error.
</div>

Compute the average of $\partial U/\partial\lambda$ at each $\lambda$ and integrate numerically (the trapezoid rule is the usual recommendation, because it works with any spacing of the $\lambda$ values). TI has no exponential average and is robust, but it has a quadrature error that depends on how smooth the integrand is, and it needs enough $\lambda$ points where the curve bends.

"No exponential average" means that no single frame can dominate. Each window contributes a plain mean, and its statistical error can be found with the block averaging of Module 11.

The weakness lies elsewhere. Straight lines between the points miss the area where the true curve bends between them, and more sampling in the existing windows does not repair that. The remedy is more windows in the curved part. A sharp bend or a spike in the curve near an end point is the mark of the end-point problem treated below.

## The Bennett acceptance ratio

Forward FEP uses only the frames of A and relies on some of them looking like B. Reverse FEP uses only the frames of B. The Bennett acceptance ratio (BAR) uses both sets at once and gives the most weight to the frames that both states visit, the overlap region. With a chain of windows you always have simulations of both members of every neighbouring pair, so BAR needs no extra simulations.

Two words first. An **estimator** is a recipe that turns data into an estimate of a quantity. Forward FEP, reverse FEP and BAR are three estimators of the same $\Delta A$. Repeat a calculation several times with different random starting velocities and an estimator gives a slightly different number each time. The spread of those numbers is measured by its **variance** ([toolbox](maths.html#averages)), and a good estimator has a small one.

FEP uses samples from one end only. With samples from both A and B, [Bennett (1976)](cite:bennett1976) asked for the estimator with the lowest variance, and showed that the one below is optimal for large samples. Start from an identity that holds for any function $f$ satisfying $f(x)/f(-x)=e^{-x}$; the Fermi function $f(x)=1/(1+e^{x})$ is the optimal choice:

$$
\frac{Q_B}{Q_A}=\frac{\big\langle f\big(\beta(\Delta U-C)\big)\big\rangle_A}{\big\langle f\big(-\beta(\Delta U-C)\big)\big\rangle_B}\,e^{-\beta C} .
$$

<div class="legend" markdown="1">
- $Q_B/Q_A$: the ratio of partition functions, equal to $e^{-\beta\Delta A}$.
- $f$: any function with the stated property. From here on it is the Fermi function.
- $x$: the argument of $f$, a pure number.
- $\Delta U$: $U_B-U_A$ of one configuration, as in FEP.
- $C$: a constant with the unit of energy that you may choose freely. The identity holds for every $C$, but the statistical error of the result depends on the choice.
- $\beta(\Delta U-C)$: the energy difference, shifted by $C$ and expressed in units of $k_BT$.
- $\langle\dots\rangle_A$, $\langle\dots\rangle_B$: averages over the frames of the simulation of A and of the simulation of B.
- $e^{-\beta C}$: a factor that compensates for the shift by $C$.
</div>

**The Fermi function.** $f(x)=1/(1+e^{x})$ is a smooth step. It is close to 1 when $x$ is very negative, exactly $\tfrac12$ at $x=0$, and close to 0 when $x$ is very positive. It satisfies the condition: $f(-x)=1/(1+e^{-x})=e^{x}/(e^{x}+1)$, so $f(x)/f(-x)=1/e^{x}=e^{-x}$. What matters most here is that it never exceeds 1.

<details markdown="1"><summary>Optional: where the identity comes from</summary>
Write $x=\beta(\Delta U-C)=\beta(U_B-U_A-C)$. The condition on $f$ says $f(x)=f(-x)\,e^{-x}$. Multiply both sides by the Boltzmann factor of state A:

$$
f(x)\,e^{-\beta U_A} = f(-x)\,e^{-\beta(U_B-U_A-C)}\,e^{-\beta U_A} = f(-x)\,e^{-\beta U_B}\,e^{\beta C} .
$$

In the last step the two factors with $U_A$ cancelled. Now integrate both sides over all configurations. On the left, $\int f(x)\,e^{-\beta U_A}d\mathbf r$ is $Q_A$ times the average of $f(x)$ in state A, by the definition of the average. On the right, the integral is $e^{\beta C}$ times $Q_B$ times the average of $f(-x)$ in state B. So

$$
Q_A\,\big\langle f(x)\big\rangle_A = e^{\beta C}\,Q_B\,\big\langle f(-x)\big\rangle_B .
$$

Divide both sides by $Q_A\,\langle f(-x)\rangle_B\,e^{\beta C}$ and you have the identity.
</details>

Bennett then asked which value of $C$ gives the smallest variance. Write $N_A$ and $N_B$ for the numbers of frames from the simulations of A and of B. The variance is smallest when the constant is $C=\Delta A+k_BT\ln(N_B/N_A)$. With equal numbers of samples this gives the BAR equation, solved for $\Delta A$ by iteration:

$$
\boxed{\sum_{n\in A}\frac{1}{1+e^{\beta(\Delta U_n-\Delta A)}} = \sum_{n\in B}\frac{1}{1+e^{-\beta(\Delta U_n-\Delta A)}}}
$$

<div class="legend" markdown="1">
- $n$: the label of one saved frame.
- $\sum_{n\in A}$: a sum over all frames of the simulation of state A. $\sum_{n\in B}$: the same for the simulation of state B.
- $\Delta U_n$: the energy difference $U_B-U_A$ of frame $n$. It is $U_B-U_A$ on both sides, also for the frames that come from B.
- $\Delta A$: the free-energy difference from A to B. It is the unknown.
- $1/(1+e^{\dots})$: the Fermi function. Each term is a number between 0 and 1.
- $\beta$: $1/k_BT$.
</div>

How the framed equation follows from the identity. Take $-k_BT\ln$ of both sides of the identity. The left side becomes $\Delta A$, and the factor $e^{-\beta C}$ becomes $+C$:

$$
\Delta A = -k_BT\ln\frac{\big\langle f\big(\beta(\Delta U-C)\big)\big\rangle_A}{\big\langle f\big(-\beta(\Delta U-C)\big)\big\rangle_B} + C .
$$

<div class="legend" markdown="1">
- $+C$: what the factor $e^{-\beta C}$ of the identity becomes when $-k_BT\ln$ is applied to it.
- Other symbols: as in the list under the identity.
</div>

With $N_A=N_B$ the best constant is $C=\Delta A$, because $\ln 1=0$. Put $C=\Delta A$ into this line. $\Delta A$ then stands on both sides and cancels, so the logarithm must be zero, which means that the two averages are equal. An average is a sum divided by the number of frames, and the numbers of frames are equal, so the two sums are equal. Writing out the Fermi function gives the framed equation.

*Solved by iteration* means the following. The unknown $\Delta A$ appears on both sides and cannot be isolated with algebra. So guess a value, compute both sums, and adjust the guess. When the guess is raised, every term on the left grows and every term on the right shrinks, so there is exactly one value at which the two sums are equal. A computer finds it in a few tens of steps.

Each configuration from A is weighted by how plausible it would be as a member of B and the reverse. BAR needs only that the two distributions of $\Delta U$ overlap, and is far more efficient than one-sided FEP.

**Read it like this.** Pool the frames of both simulations and pick one. Suppose all you know about it is its value of $\Delta U$. With equal numbers of frames, the probability that it came from the B simulation is $1/(1+e^{\beta(\Delta U-\Delta A)})$, the term on the left. The probability that it came from the A simulation is the term on the right.

So the left side counts how many of the frames from A could pass for frames of B, and the right side counts how many of the frames from B could pass for frames of A. BAR chooses $\Delta A$ so that the two counts are equal.

Because every term lies between 0 and 1, no single frame can take over the sum, which is what happened with the exponential average of FEP.

### Overlap decides the precision

Make two histograms of $\Delta U=U_B-U_A$: one from the frames of the A simulation and one from the frames of the B simulation. Call the two distributions $P_A(\Delta U)$ and $P_B(\Delta U)$. The histogram from B lies at lower values, because the configurations that B prefers have a low energy in B. The two are tied together by an exact relation:

$$
\frac{P_B(\Delta U)}{P_A(\Delta U)} = e^{-\beta(\Delta U-\Delta A)} .
$$

<div class="legend" markdown="1">
- $P_A(\Delta U)$: the probability density of finding the value $\Delta U$ among the frames of state A. The area under it is 1 ([toolbox](maths.html#probability)).
- $P_B(\Delta U)$: the same for the frames of state B. The quantity on the axis is still $U_B-U_A$.
- $\Delta A$: the free-energy difference from A to B.
- $\beta$: $1/k_BT$.
</div>

It follows from the same factor-of-one step as the FEP formula. Among the configurations with one given value of $\Delta U$, each is more probable in B than in A by the same factor, $e^{-\beta\Delta U}\,Q_A/Q_B$, and $Q_A/Q_B=e^{+\beta\Delta A}$.

**Read it like this.** At $\Delta U=\Delta A$ the right side is 1, so the two histograms cross exactly at the free-energy difference. Finding $\Delta A$ means finding that crossing point. If the histograms overlap, many frames from both runs lie near the crossing and it is located precisely. If they are far apart, the crossing lies in the empty region between them, where neither run has frames, and its position has to be guessed from the thin tails.

Forward FEP guesses it from the lower tail of the A histogram alone, and reverse FEP from the upper tail of the B histogram alone. BAR uses both tails, which is why it needs less overlap than FEP. It still fails when there is none. This is the reason for intermediate states, said once more: they are chosen so that the histograms of each neighbouring pair of windows overlap.

**From two states to many.** A chain of windows gives many neighbouring pairs. BAR can be applied to each pair in turn and the results added. But a frame from window 5 also carries information about windows 3, 4, 6 and 7, and pairwise BAR ignores it. **MBAR** (Module 12) generalises it to all $\lambda$ states at once and is the current standard estimator. Its by-product, the **overlap matrix** between states, is the main diagnostic: adjacent states should have off-diagonal overlap of at least about 0.03.

MBAR stands for multistate Bennett acceptance ratio. In words: take every saved frame from every window and compute its energy with the energy function of every window. Then solve one set of coupled equations, with one unknown free energy per window, in which each frame is weighted by how plausible it is in each state. With two states the equations reduce to BAR. They are written out in [Module 12](12-free-energy-pmf.html), where the states were umbrella windows, and they are the same here with the $\lambda$ windows as states.

The overlap matrix is a table with one row and one column per window. The entry in row $i$ and column $j$ estimates the probability that a frame sampled in window $i$ would be taken for a frame of window $j$, judged by its energies. Each row adds up to 1. The entries next to the diagonal are the overlaps between neighbouring windows, and they are the ones to check.

If one of them is close to zero, the chain is broken at that place, and the total $\Delta A$ cannot be trusted however good the other windows are. The repair is an extra window between the two.

The demo below shows all of this on the smallest possible system. States A and B are two springs, for which the exact $\Delta A$ is known. It draws the two histograms of $\Delta U$ and compares FEP from A, FEP from B and BAR.

<div class="widget" data-widget="fep"></div>

## Making atoms appear and disappear: soft-core potentials

Many alchemical changes remove atoms or create them: a hydrogen becomes a methyl group, a side chain shrinks, a whole ligand vanishes. The linear mixing rule breaks down for these, at the end of the path where the atom is almost gone. This section explains why, and gives the standard repair.

<div class="box physics" markdown="1">
**Physics you need here: the two non-bonded energies of a pair of atoms.** This is a reminder of [Module 5](05-force-field-form.html). Two atoms that are not bonded to each other interact in two ways.

The **Lennard-Jones** energy is $U_{LJ}(r)=4\varepsilon\big[(\sigma/r)^{12}-(\sigma/r)^{6}\big]$, where $r$ is the distance between the two atoms. The term with the power 12 is a steep repulsion that keeps atoms from overlapping, and the term with the power 6 is a weak attraction. $\sigma$ is the distance at which the energy passes through zero, roughly the contact distance of the pair, and $\varepsilon$ is the depth of the attractive well. As $r$ goes to zero the energy grows without limit. This is the **repulsive core** of the atom.

The **Coulomb** energy of two partial charges $q_i$ and $q_j$ is $U_C(r)=q_iq_j/(4\pi\epsilon_0r)$, with $1/(4\pi\epsilon_0)=138.935$ kJ mol$^{-1}$ nm $e^{-2}$. Charges of $+0.4\,e$ and $-0.4\,e$ at 0.3 nm have an energy of $-74$ kJ/mol. For opposite charges the energy falls without limit as $r$ goes to zero. In a normal simulation this never happens, because the repulsive cores stop the atoms long before. More in the primer: [forces between molecules](physics.html#intermolecular) and [Coulomb's law](physics.html#electrostatics).
</div>

### The end-point catastrophe

With linear scaling, a disappearing atom at $\lambda$ close to 1 is nearly non-interacting, so other atoms can sit right on top of it, where its $r^{-12}$ repulsion, though scaled by a small factor, is still infinite. $\langle\partial U/\partial\lambda\rangle$ diverges at the end point.

In this section $\lambda=0$ is the state in which the atom is fully present and $\lambda=1$ the state in which it is gone. Linear scaling means that its Lennard-Jones energy with every other atom is multiplied by $(1-\lambda)$.

The trouble is that a small number times infinity is still infinity. At $\lambda=0.99$ the energy is multiplied by 0.01, but at the centre of the atom it is still infinite, so a wall remains. It has only moved inwards.

Take $\varepsilon=0.5$ kJ/mol as an illustration. The distance at which the scaled repulsion $(1-\lambda)\,4\varepsilon(\sigma/r)^{12}$ equals $k_BT$ at 300 K is $0.98\,\sigma$ at $\lambda=0$, $0.67\,\sigma$ at $\lambda=0.99$ and $0.46\,\sigma$ at $\lambda=0.9999$. The wall shrinks very slowly, as the twelfth root of $(1-\lambda)$, and then vanishes all at once at $\lambda=1$.

Now look at what TI measures. With linear scaling, $\partial U/\partial\lambda=-U_{LJ}(r)$, the full, unscaled energy with the opposite sign. As $\lambda$ approaches 1, neighbouring atoms come closer to the centre, where the unscaled energy is enormous. Its average grows without limit, which is the meaning of "diverges". The TI curve shoots off at the end, and no placement of windows makes the trapezoid rule accurate there.

FEP and BAR suffer in their own way. The windows closest to the end overlap poorly with the end state, because in the end state other atoms sit inside a region that is still forbidden a short step before. The whole effect is called the **end-point catastrophe**.

The fix ([Beutler et al. 1994](cite:beutler1994)) is a **soft-core** Lennard-Jones potential in which $\lambda$ also shifts the distance. A widely used form (the GROMACS variant with `sc-power = 1`) is given below. The original paper runs $\lambda$ the other way, uses a prefactor $\lambda^n$ and a shift proportional to $\alpha(1-\lambda)^2$, and softens the Coulomb term in the same way:

$$
U_{sc}(r,\lambda) = 4\varepsilon\,(1-\lambda)\left[\frac{1}{\big(\alpha\lambda+(r/\sigma)^6\big)^2}-\frac{1}{\alpha\lambda+(r/\sigma)^6}\right].
$$

<div class="legend" markdown="1">
- $U_{sc}(r,\lambda)$: the soft-core Lennard-Jones energy of one pair, the disappearing atom and one atom of its surroundings.
- $r$: the distance between the two atoms.
- $\lambda$: the coupling parameter. Here 0 means fully present and 1 means gone.
- $\varepsilon$, $\sigma$: the Lennard-Jones well depth and size of the pair (see the box above). Here $\sigma$ is not a standard deviation.
- $4\varepsilon\,(1-\lambda)$: the ordinary Lennard-Jones prefactor, scaled down linearly as before.
- $\alpha$: the soft-core parameter, a positive pure number that you choose (say, 0.5). It sets how strongly the core is softened.
- $\alpha\lambda+(r/\sigma)^6$: the expression that takes the place of $(r/\sigma)^6$ in the normal potential. The added $\alpha\lambda$ keeps it away from zero when $r$ is zero.
- The square bracket: its first term is the repulsion (it replaces $(\sigma/r)^{12}$) and its second term the attraction (it replaces $(\sigma/r)^{6}$).
</div>

At $\lambda=0$ it is the normal potential. As $\lambda\to1$ the singularity at $r=0$ is removed and the interaction fades smoothly. (A **singularity** is a point where a function becomes infinite.)

**Read it like this.** Write the normal potential as $4\varepsilon\,[1/x^2-1/x]$ with $x=(r/\sigma)^6$. The soft-core form is the same expression with $x$ replaced by $x+\alpha\lambda$, and with the prefactor $4\varepsilon$ scaled down to $4\varepsilon\,(1-\lambda)$. The pair behaves as if the two atoms were always a little further apart than they are. Even at $r=0$ the effective $x$ is $\alpha\lambda$, which is larger than zero, so the energy stays finite.

Numbers for $\alpha=0.5$ and $\varepsilon=0.5$ kJ/mol, both chosen as illustrations. At $\lambda=0.5$ an atom that sits exactly on top of the disappearing one ($r=0$) has the energy $24\,\varepsilon=12$ kJ/mol, about $4.8\,k_BT$: a hill that is climbed now and then. At $\lambda=0.9$ it is $1.1\,\varepsilon=0.5$ kJ/mol, less than $k_BT$. At $\lambda=1$ it is zero. The wall has become a hill that sinks gradually, so neighbouring windows overlap and $\langle\partial U/\partial\lambda\rangle$ stays finite.

### Charges first, then Lennard-Jones

A disappearing atom has a partial charge as well as a Lennard-Jones core, and the order in which the two are removed matters.

A common and safe protocol turns off the charges first with linear scaling, then the Lennard-Jones interactions with soft-core, so that a bare charge is never left without its repulsive core. Softening both together in a single stage is also used and can be cheaper; neither has been shown to be clearly better ([Mey et al. 2020](cite:mey2020)).

The reason is the Coulomb energy in the box above. Between opposite charges it falls without limit as the distance goes to zero, and the only thing that prevents this in a force field is the repulsive core. Remove or soften the core while the charge is still there, and an oppositely charged atom of the surroundings can fall onto it. The energy becomes hugely negative and the simulation fails.

So the change is done in two stages, each with its own set of windows. In stage 1 the charges of the disappearing atoms are scaled to zero while their Lennard-Jones cores are intact. Linear scaling is safe here, because the cores keep other atoms away from the places where the Coulomb energy is singular. In stage 2 the uncharged atoms are removed with the soft-core potential.

The total free energy is the sum of the two stages, again because free energy is a state function. When atoms appear instead, the order is reversed: first the cores, then the charges.

*Softening both together* means that the Coulomb term is given a soft-core form too, so that it stays finite at $r=0$ and one stage is enough.

## Thermodynamic cycles

Alchemical changes are useful because of cycles.

On its own, an alchemical free energy is a number that nobody can measure. "The free energy of turning ligand A into ligand B in water" corresponds to no experiment. A **thermodynamic cycle** combines alchemical steps with physical ones in a closed loop of states. Because free energy is a state function, the changes around a closed loop add up to zero, in the same way that a walk that returns to its starting point ends at the altitude where it began. That one equation lets you replace a step that is hard to simulate by steps that are easier.

Each side of the loop is called a **leg**. In the three cycles below, the physical legs are the ones an experiment measures and the alchemical legs are the ones you simulate.

### The simplest cycle: a hydration free energy

The **hydration free energy** $\Delta G_{hyd}$ of a molecule is the free-energy change when it is moved from the gas phase into water. Simulating a molecule that crosses from a gas into a liquid is slow. The alchemical route switches off the interactions between the molecule and the water instead. This is called **decoupling**: the molecule keeps its bonds, its angles and the interactions among its own atoms, but the water no longer feels it and it no longer feels the water.

The cycle has four corners. M is the molecule and M_off the decoupled molecule:

```
                          ΔG_hyd
   M (gas)  ──────────────────────────────►  M (in water)
     │                                          │
     │ 0                                        │ ΔG_decouple(water)
     ▼                                          ▼
   M_off (gas)  ◄──────────────────────────  M_off (in water)
                            0
```

The four legs:

- **Top, physical.** Transfer of the molecule from gas to water, $\Delta G_{hyd}$. This is what the experiment measures.
- **Right, alchemical.** Decoupling the molecule in water, $\Delta G_{decouple}^{water}$. This is the only leg that is simulated.
- **Bottom.** Moving the decoupled molecule out of the water into the gas. It does not interact with the water, so this costs nothing.
- **Left.** Decoupling the molecule in the gas. There are no surroundings to decouple from, so this is zero too.

Go round the loop clockwise from the top left. The top and the right leg are followed along their arrows and count with a plus sign. The bottom leg is zero. The left leg is followed against its arrow, counts with a minus sign, and is zero as well. So $\Delta G_{hyd}+\Delta G_{decouple}^{water}+0-0=0$, which gives

$$
\Delta G_{hyd} = -\Delta G_{decouple}^{water} .
$$

<div class="legend" markdown="1">
- $\Delta G_{hyd}$: the hydration free energy, for the transfer from gas to water. It is negative for a molecule that prefers water.
- $\Delta G_{decouple}^{water}$: the free energy of switching off the interactions between the molecule and the water, in a box of water. It is computed from a chain of $\lambda$ windows with TI, BAR or MBAR.
- The minus sign: hydration is the reverse of decoupling.
</div>

Decoupling a polar molecule from water removes favourable interactions, so $\Delta G_{decouple}^{water}$ is positive and the hydration free energy is negative. If the windows add up to, say, $+20$ kJ/mol, then $\Delta G_{hyd}=-20$ kJ/mol.

Two details. First, the bottom leg is zero only if the decoupled molecule has the same concentration in the gas as in the water. The number you get is therefore the free energy of transfer between gas and solution at equal concentrations, and you should check that the experimental value you compare with uses the same convention. Second, if a protocol also switches off the non-bonded interactions inside the molecule, the left leg is no longer zero and has to be computed in a separate simulation of the molecule alone.

### Relative binding free energy

<div data-videos="iweSKUD2YBI WhUEc5YMT2Q HSh4AzzhGKM LJOmgrwncY0 rgN9noKQoVg"></div>

Which of two ligands A and B binds a protein more strongly? The physical processes are the two binding events (horizontal arrows). The alchemical processes turn A into B, once in the binding site and once free in solution (vertical arrows):

```
                 ΔG_bind(A)
   P + A  ───────────────────────►  P·A
     │                               │
     │ ΔG_free(A→B)                  │ ΔG_complex(A→B)
     ▼                               ▼
   P + B  ───────────────────────►  P·B
                 ΔG_bind(B)
```

The four corners are four states. Top left: the protein P and ligand A, both in water and far apart. Top right: the complex P·A in water. Bottom left and bottom right: the same with ligand B. The four legs:

- **Top, physical.** A binds, with free energy $\Delta G_{bind}(A)$.
- **Bottom, physical.** B binds, with free energy $\Delta G_{bind}(B)$.
- **Left, alchemical.** A is changed into B while free in water, $\Delta G_{free}(A\to B)$. The protein takes no part, so this simulation contains only the ligand and water.
- **Right, alchemical.** A is changed into B inside the binding site, $\Delta G_{complex}(A\to B)$.

Going round the cycle must give zero, so

$$
\Delta\Delta G_{bind} = \Delta G_{bind}(B)-\Delta G_{bind}(A) = \Delta G_{complex}(A\to B)-\Delta G_{free}(A\to B) .
$$

<div class="legend" markdown="1">
- $\Delta\Delta G_{bind}$: the **relative binding free energy**, that of B minus that of A. A negative value means that B binds more strongly.
- $\Delta G_{bind}(A)$, $\Delta G_{bind}(B)$: the binding free energies of the two ligands, each for the step from unbound to bound.
- $\Delta G_{complex}(A\to B)$: the free energy of the alchemical change of A into B in the complex.
- $\Delta G_{free}(A\to B)$: the free energy of the same change for the free ligand in water.
- In the diagram, P is the protein, A and B are the ligands, and P·A is the complex.
</div>

In full: start at the top left and go round clockwise. The top leg gives $+\Delta G_{bind}(A)$ and the right leg $+\Delta G_{complex}(A\to B)$. The bottom leg and the left leg are followed against their arrows and give $-\Delta G_{bind}(B)$ and $-\Delta G_{free}(A\to B)$. The sum is zero. Move the two binding terms to one side and you have the formula.

**Read it like this.** The change of A into B is made twice, in two environments. If it is more favourable in the binding site than in water, the site prefers B, and B is the stronger binder. Example: $\Delta G_{complex}=-30$ kJ/mol and $\Delta G_{free}=-25$ kJ/mol give $\Delta\Delta G_{bind}=-5$ kJ/mol. The two alchemical numbers have no meaning on their own. Their difference does.

To turn $\Delta\Delta G$ into a ratio of affinities, use the relation between the binding free energy and the dissociation constant $K_d$ from Module 12. It gives $\Delta\Delta G_{bind}=k_BT\ln[K_d(B)/K_d(A)]$. For $-5$ kJ/mol at 300 K the ratio is $e^{-5/2.494}=0.13$. The $K_d$ of B is 7.4 times lower, so B binds 7.4 times more tightly.

Neither vertical leg involves binding or unbinding, and when A and B are similar, each is a small perturbation. For congeneric small molecules, well-run calculations reach root-mean-square errors of about 1 to 2 kcal/mol (4 to 8 kJ/mol) against experiment in favourable cases ([Wang et al. 2015](cite:wang2015); [Mey et al. 2020](cite:mey2020)).

*Congeneric* molecules share the same core and differ in a few atoms, for example a series of compounds with different groups on one ring. The *root-mean-square error* is the square root of the mean of the squared differences between computed and measured values over a set of ligand pairs. It is a typical size of the error. At 300 K an error of 1 kcal/mol corresponds to a factor of 5 in $K_d$, and 2 kcal/mol to a factor of about 29.

No standard concentration appears in a relative calculation. Both binding events refer to the same standard state, and its contribution cancels in the difference. This is one reason why relative calculations are easier than absolute ones.

**Mutations in a protein or peptide binder** use the same cycle: "A→B" is the mutation of one residue, done once in the complex and once in the free binder. The result is $\Delta\Delta G_{bind}$ of the mutation. Complications: the free binder may change conformation or become disordered (the free leg then needs far more sampling than the bound leg); mutations that change the net charge need corrections for the finite periodic box, or a co-alchemical ion that changes in the opposite sense; and large changes in side-chain size need time for the surroundings to rearrange.

Written out as a cycle, with "wt" (wild type) for the original binder and "mut" for the mutant: the top leg is the binding of the wt binder to its target, and the bottom leg the binding of the mutant. The right leg is the mutation of the residue inside the complex, and the left leg the same mutation in the free binder in water. Then $\Delta\Delta G_{bind}=\Delta G_{complex}(\text{wt}\to\text{mut})-\Delta G_{free}(\text{wt}\to\text{mut})$. A positive value means that the mutation weakens binding.

The three complications, one at a time.

*The free binder.* In the complex the binder is held in one shape by its partner. Free in water it may be flexible or disordered, and the mutation may shift the balance between its shapes. The free leg must sample all of them with the right weights at every $\lambda$, which can take far longer than the bound leg.

*A change of net charge.* Replacing aspartate (charge $-1$) by alanine (charge 0) changes the net charge of the box by $+1$. With periodic boundaries and Ewald electrostatics (Module 7), a charged group interacts with its own periodic copies and with a uniform background charge that the method adds to keep the box neutral. These contributions depend on the size of the box and on what else is in it. They differ between the box of the complex and the box of the free binder, so they do not cancel in the cycle.

One remedy is a correction term computed afterwards. The other is to keep the net charge of the box constant. While the residue goes from $-1$ to 0, an ion elsewhere in the box is changed alchemically in the opposite sense, for example a sodium ion (charge $+1$) into a neutral water molecule. That ion is the co-alchemical ion.

*A change of size.* When a small side chain becomes a large one, room has to be made: water leaves and neighbouring side chains move. When a large one becomes small, water has to enter the cavity. If these rearrangements are slower than the simulation in each window, the result depends on the starting structure.

### Single and dual topology

How is "A is changed into B" set up in practice? A **topology** is the list of the atoms of a molecule with their parameters and bonds (Module 6). There are two ways to build a molecule that is A at one end of the path and B at the other.

- **Single topology.** There is one set of atoms. Atoms that A and B have in common are matched, and each matched atom changes its charge and its Lennard-Jones parameters gradually from the values in A to the values in B. An atom that exists in only one of the two molecules becomes a **dummy atom** at the other end: it stays bonded to the molecule but has no charge and no Lennard-Jones interaction.
- **Dual topology.** The parts in which A and B differ are both present for the whole calculation, and they do not interact with each other. As $\lambda$ goes from 0 to 1, the part that belongs to A is switched off and the part that belongs to B is switched on.

Single topology changes fewer atoms, which makes the perturbation smaller. It needs a sensible matching of atoms. Dual topology needs no matching, but more atoms appear and disappear, so more of the path depends on soft-core potentials. The two can be mixed: match the common core and let only the atoms that differ appear and disappear.

Dummy atoms are still bonded to the molecule, so their bonded energy terms are present in the calculation. They are present in both alchemical legs of the cycle. They contribute the same amount to each and cancel in the difference, provided the dummy atoms are attached in a way that does not distort the real part of the molecule.

### Absolute binding free energy

<div data-videos="LPYzLZ1WmG4"></div>

A relative calculation says that B binds seven times more tightly than A. It does not say how tightly either of them binds. For that you need the **absolute** (or standard) binding free energy $\Delta G^\circ_{bind}$, the number that corresponds to a measured dissociation constant: $\Delta G^\circ_{bind}=k_BT\ln(K_d/C^\circ)$, with $C^\circ=1$ mol/L the standard concentration (Module 12). A $K_d$ of 1 nM corresponds to $-51.7$ kJ/mol ($-12.4$ kcal/mol) at 300 K.

<div class="box physics" markdown="1">
**Physics you need here: the standard state.** A free ligand in solution can be anywhere. The more dilute the solution, the more volume each ligand has to itself, the more freedom it loses on binding, and the weaker the binding appears. A binding free energy is therefore defined only for an agreed concentration of the free partners. The convention is 1 mol/L, which is one molecule per $V^\circ=1.661$ nm$^3$. The superscript $^\circ$ marks quantities that refer to this convention.

A simulation box has some other volume. Every absolute calculation must therefore contain a step that refers the free ligand to $V^\circ$. More in the [primer](physics.html#equilibrium) and in Module 12.
</div>

To get $\Delta G^\circ_{bind}$ of one ligand, make it vanish.

This is the trick of the hydration cycle, used twice. A ligand that has been decoupled does not care where it is, so taking it from the solvent to the binding site costs nothing except some bookkeeping about the room it has. The cycle has four corners. P is the protein, L the ligand and L_off the decoupled ligand:

```
                               ΔG°_bind
   P + L (both in water)  ──────────────────────►  P·L
     │                                               │
     │ ΔG_decouple(solvent)                          │ ΔG_decouple(site)
     ▼                                               ▼
   P + L_off (free, in the  ◄────────────────────  P·L_off (held in the
       standard volume)          ΔG°_restr              site by restraints)
```

The four legs:

- **Top, physical.** Binding at the standard concentration, $\Delta G^\circ_{bind}$. This is what the experiment measures.
- **Left, alchemical.** Decoupling the ligand in a box of water without the protein, $\Delta G_{decouple}^{solvent}$. It is the same kind of simulation as for a hydration free energy.
- **Right, alchemical.** In the complex, restraints that hold the ligand in the site are switched on, and the ligand is then decoupled from the protein and the water. The free energy of both together is $\Delta G_{decouple}^{site}$.
- **Bottom.** The decoupled ligand is released from the restraints into the standard volume, $\Delta G_{restr}^\circ$. This leg needs no simulation. Why restraints are needed, and the formula for this leg, come below.

In **double decoupling** the ligand's interactions with its surroundings are switched off twice, in the binding site and in bulk solvent:

$$
\Delta G^\circ_{bind} = \Delta G_{decouple}^{solvent}-\Delta G_{decouple}^{site}-\Delta G_{restr}^\circ ,
$$

where $\Delta G_{restr}^\circ$ is the free energy of *releasing* the decoupled ligand from its restraints into the standard volume (formula below).

<div class="legend" markdown="1">
- $\Delta G^\circ_{bind}$: the standard binding free energy, for free protein and free ligand at 1 mol/L going to the complex. More negative means tighter binding.
- $\Delta G_{decouple}^{solvent}$: the free energy of switching off the interactions of the ligand with its surroundings when it is alone in water. It is positive for a ligand that interacts favourably with water.
- $\Delta G_{decouple}^{site}$: the same in the binding site, including the switching on of the restraints. For a ligand that binds, it is larger than the solvent term.
- $\Delta G_{restr}^\circ$: the free energy of releasing the decoupled ligand from the restraints into the standard volume. It is negative.
- The two minus signs: the right and the bottom leg of the cycle are followed against the direction of binding.
</div>

How the formula follows from the cycle: start at the top left and go round clockwise. The top leg gives $+\Delta G^\circ_{bind}$, the right leg $+\Delta G_{decouple}^{site}$, and the bottom leg, followed along its arrow, $+\Delta G_{restr}^\circ$. The left leg is followed against its arrow and gives $-\Delta G_{decouple}^{solvent}$. The sum is zero, and solving for $\Delta G^\circ_{bind}$ gives the formula.

An illustration with invented numbers: $\Delta G_{decouple}^{solvent}=+60$ kJ/mol, $\Delta G_{decouple}^{site}=+125$ kJ/mol and $\Delta G_{restr}^\circ=-28.7$ kJ/mol give $\Delta G^\circ_{bind}=60-125+28.7=-36.3$ kJ/mol. The answer is a small difference between large numbers.

Now back to the restraint term $\Delta G_{restr}^\circ$. It is negative, so subtracting it makes the computed binding less favourable. Its size depends on the restraints you chose, and the restrained decoupling work in the site changes by the opposite amount, so only the sum of the two has a physical meaning. It is therefore not, by itself, the translational and rotational entropy that the ligand loses on binding ([Gilson et al. 1997](cite:gilson1997)).

The complete formula of that paper has two more terms on the right-hand side. One is a symmetry term, $+k_BT\ln[\sigma_{PL}/(\sigma_P\sigma_L)]$, with $\sigma$ the symmetry numbers of complex, protein and ligand: a ligand with $\sigma_L$ equivalent orientations, restrained to one of them in an asymmetric site, binds more strongly than computed by $k_BT\ln\sigma_L$. The other is a pressure-volume term, which is negligible at 1 bar.

A **symmetry number** counts the orientations of a molecule that cannot be told apart. A molecule that looks the same after a half turn about one axis has $\sigma=2$, and a molecule without symmetry has $\sigma=1$. A symmetric ligand can sit in the site in $\sigma_L$ equivalent ways, but the restraints hold it in one of them, so the simulation counts only one. For $\sigma_L=2$ the correction is $k_BT\ln2=1.7$ kJ/mol at 300 K. The pressure-volume term is the work done against the outside pressure when the volume of the solution changes on binding.

The sign of the restraint term and its dependence on the restraints both come from counting room. Release gives the ligand more room, and more room means a lower free energy (the particle on a line in the first section), so the term is negative. Tighter restraints make the bottom leg more negative. They also make the right leg larger by the same amount, because that leg ends with the ligand held more tightly. The binding free energy does not depend on the restraints, as long as every leg is converged.

### Restraints: why the ligand must be held

A decoupled ligand is an ideal-gas molecule. Without restraints it would wander through the whole box, so the end state would depend on the box volume and the result would have no defined standard state. The original "double annihilation" method had this flaw: it had no standard-state term, and Gilson et al. estimate that published values were too favourable by about 12 to 16 kJ/mol. Such runs also converge very slowly ([Gilson et al. 1997](cite:gilson1997)).

An **ideal-gas molecule** is a molecule that interacts with nothing. A fully decoupled ligand is one: it passes through water and protein as if they were not there.

Two things go wrong without restraints. The first is a matter of definition. The coupled ligand stays in the site, held by its interactions, while the decoupled ligand roams the whole simulation box. The free energy of that end state contains the box volume (more room, lower free energy), so the answer would change with the size of the box you happened to build.

The second is practical. In the windows where the ligand is almost decoupled it drifts out of the site, and in a finite run it rarely finds its way back, so those windows do not sample what they should.

The decoupling in bulk solvent needs no restraint. There the coupled ligand roams the whole box too, the volume appears at both ends of the leg, and it cancels.

So the ligand is held by **restraints** to the protein while it is decoupled. [Boresch et al. (2003)](cite:boresch2003) use one distance, two angles and three dihedrals between three atoms of the ligand and three of the protein, which fixes all six relative degrees of freedom.

A **restraint** is an extra energy term that you add to keep a coordinate near a chosen value. Here it is a harmonic spring, $\tfrac12K(\zeta-\zeta_0)^2$, where $\zeta$ stands for the restrained coordinate, $\zeta_0$ for its reference value and $K$ for the force constant. Module 12 used the same device for umbrella windows.

**Six degrees of freedom.** A **degree of freedom** is an independent way in which something can move (Module 2). Treat the ligand for a moment as a rigid object. To say where it is relative to the protein you need three numbers for its position and three for its orientation, six in all. If all six are restrained, the decoupled ligand can only tremble around one pose. The six numbers are built from three atoms of the protein, call them p1, p2 and p3, and three atoms of the ligand, l1, l2 and l3:

- one **distance** $r$, between p1 and l1;
- two **angles** $\theta_A$ and $\theta_B$, for example p2-p1-l1 and p1-l1-l2;
- three **dihedrals** $\phi_A$, $\phi_B$ and $\phi_C$, for example p3-p2-p1-l1, p2-p1-l1-l2 and p1-l1-l2-l3.

The distance, the first angle and the first dihedral fix where the atom l1 is. The other three fix how the ligand is turned. (A dihedral is the angle of rotation about the middle bond of four atoms in a row, Module 5.)

The free energy of releasing a non-interacting ligand from these restraints into the standard volume $V^\circ$ is analytical:

$$
\Delta G_{restr}^\circ = -k_BT\ln\left[\frac{8\pi^2V^\circ\sqrt{K_rK_{\theta_A}K_{\theta_B}K_{\phi_A}K_{\phi_B}K_{\phi_C}}}{r_0^2\,\sin\theta_{A,0}\,\sin\theta_{B,0}\,(2\pi k_BT)^3}\right],
$$

with $K$ the force constants and $r_0$, $\theta_{A,0}$, $\theta_{B,0}$ the reference values.

<div class="legend" markdown="1">
- $\Delta G_{restr}^\circ$: the free energy of releasing the decoupled ligand from its six restraints into the standard volume. It is negative.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- The square bracket: the room available to the free ligand divided by the room that the restraints leave it. It is a pure number, far larger than 1.
- $8\pi^2$: the measure of all orientations of a rigid object, $4\pi$ for the direction of an axis times $2\pi$ for the rotation about it.
- $V^\circ$: the standard volume, 1.661 nm$^3$ per molecule.
- $K_r$: the force constant of the distance restraint, in kJ mol$^{-1}$ nm$^{-2}$.
- $K_{\theta_A}$, $K_{\theta_B}$, $K_{\phi_A}$, $K_{\phi_B}$, $K_{\phi_C}$: the force constants of the two angle restraints and the three dihedral restraints, in kJ mol$^{-1}$ rad$^{-2}$.
- The square-root sign: it covers the product of the six force constants.
- $r_0$: the reference value of the distance, in nm.
- $\theta_{A,0}$, $\theta_{B,0}$: the reference values of the two angles. $\sin$ is the sine function.
- $(2\pi k_BT)^3$: one factor $\sqrt{2\pi k_BT}$ for each of the six restraints. $\pi=3.14159$.
</div>

*Analytical* means that it is given by a formula and needs no simulation. That is possible because the decoupled ligand feels nothing but the six springs, and the partition function of a spring is an integral that can be done by hand.

**Read it like this.** The top of the fraction, $8\pi^2V^\circ$, measures the room of a free ligand at the standard concentration: $V^\circ$ for where it can be and $8\pi^2$ for how it can be turned. The rest measures the room that the springs leave. A spring with force constant $K$ lets its coordinate spread over a width of $\sqrt{2\pi k_BT/K}$, so a stiffer spring leaves less room. Larger force constants therefore make the bracket larger and $\Delta G_{restr}^\circ$ more negative. The factors $r_0^2\sin\theta_{A,0}\sin\theta_{B,0}$ convert the spreads in distance and angles into a volume, in the same way as the volume element $r^2\sin\theta$ of spherical coordinates.

For typical restraints the argument of the logarithm is about $10^5$, so $\Delta G_{restr}^\circ\approx-28$ kJ/mol ($-6.8$ kcal/mol). It grows in size with the force constants: Boresch et al. tabulate $-6.3$ to $-10.4$ kcal/mol ($-26$ to $-43$ kJ/mol) for force constants from 5 to 50 kcal/mol per Å$^2$ or rad$^2$.

<div class="box key" markdown="1">
**Worked example: the restraint term for round numbers.** Take all six force constants equal to 10 kcal/mol per Å$^2$ or per rad$^2$. In MD units the distance restraint has $K_r=4184$ kJ mol$^{-1}$ nm$^{-2}$ (1 Å$^{-2}$ is 100 nm$^{-2}$), and the five angular restraints have 41.84 kJ mol$^{-1}$ rad$^{-2}$ each. Take $r_0=0.5$ nm, both reference angles equal to $90^\circ$ (so both sines are 1), and $T=300$ K.

1. *The square root.* $\sqrt{4184\times41.84^5}=7.32\times10^5$.
2. *The numerator.* $8\pi^2\times1.661=131.1$, and $131.1\times7.32\times10^5=9.6\times10^7$.
3. *The denominator.* $2\pi k_BT=15.67$ kJ/mol, its cube is 3850, and $0.5^2\times3850\approx962$.
4. *The bracket.* $9.6\times10^7/962=1.0\times10^5$.
5. *The result.* $\Delta G_{restr}^\circ=-2.494\times\ln(1.0\times10^5)=-28.7$ kJ/mol, which is $-6.9$ kcal/mol. This is the typical size quoted above.

The sentence before this box gives about $-28$ kJ/mol ($-6.8$ kcal/mol) for a bracket of $10^5$. That is the same quantity at 298 K, where $k_BT=2.478$ kJ/mol: $-2.478\times\ln10^5=-28.5$ kJ/mol, which is $-6.8$ kcal/mol. For the same bracket, going from 298 K to 300 K changes the result by 0.2 kJ/mol, so the two statements agree.

The units cancel: the numerator has nm$^3$ times (kJ/mol)$^3$ nm$^{-1}$, the denominator nm$^2$ times (kJ/mol)$^3$. A radian counts as a pure number.
</div>

<details markdown="1"><summary>Optional: where the restraint formula comes from</summary>
The release changes the decoupled ligand from "held by six springs" to "free in the volume $V^\circ$". Its free energy is $-k_BT\ln(Z_{free}/Z_{restr})$, where each $Z$ is the integral of the Boltzmann factor over the six numbers that give the position and the orientation of the ligand relative to the protein.

*The free ligand.* It feels no energy, so the Boltzmann factor is 1. The integral over positions gives the volume $V^\circ$, and the integral over orientations gives $8\pi^2$. So $Z_{free}=8\pi^2V^\circ$.

*The restrained ligand.* In the six coordinates of the list above, the volume element is $r^2\sin\theta_A\sin\theta_B\,dr\,d\theta_A\,d\theta_B\,d\phi_A\,d\phi_B\,d\phi_C$. If the springs are stiff, the coordinates stay close to their reference values and the factor $r^2\sin\theta_A\sin\theta_B$ can be replaced by its value there, $r_0^2\sin\theta_{A,0}\sin\theta_{B,0}$. What remains is one integral per spring, and each is a [Gaussian integral](maths.html#gaussian):

$$
\int e^{-K(\zeta-\zeta_0)^2/2k_BT}\,d\zeta = \sqrt{\frac{2\pi k_BT}{K}} .
$$

The product of the six is $(2\pi k_BT)^3$ divided by the square root of the product of the six force constants. So

$$
Z_{restr} = r_0^2\sin\theta_{A,0}\sin\theta_{B,0}\,\frac{(2\pi k_BT)^3}{\sqrt{K_rK_{\theta_A}K_{\theta_B}K_{\phi_A}K_{\phi_B}K_{\phi_C}}} .
$$

Dividing $Z_{free}$ by $Z_{restr}$ gives the bracket of the formula.
</details>

The formula assumes restraint energies of the form $\tfrac12K(\zeta-\zeta_0)^2$; a program that writes $K(\zeta-\zeta_0)^2$ needs $2K$ in it. Sign conventions for this term differ between papers and programs (some report the free energy of *imposing* the restraints, which is the same number with the opposite sign and then enters with a plus), so check which direction your software reports.

The factor of 2 is worth a number. If all six force constants are entered a factor 2 too small, each square root in the product is off by $\sqrt2$, the bracket is off by $2^3=8$, and the result is wrong by $k_BT\ln8=5.2$ kJ/mol at 300 K.

Absolute calculations are harder than relative ones: the errors of two large numbers do not cancel, and the protein must relax between the bound and the empty state.

In a relative calculation a few atoms change, and the two legs share most of their errors. In an absolute calculation the whole ligand disappears, both decoupling free energies are large (60 and 125 kJ/mol in the illustration above), and an error of a few per cent in either is as large as the differences you care about. The end state of the site leg is also a different protein: the site without its ligand fills with water, and side chains or loops may move. That relaxation can be slow, and it has to happen within the windows.

## Non-equilibrium work relations

<div data-videos="nI3pHiPbxeg NeGjghk0im4 LXcQx6Bu3OQ gsq3irAz8Ok"></div>

All the methods so far let every window come to equilibrium. This section asks what happens if you do not wait: change $\lambda$ from 0 to 1 during one short simulation, and repeat that many times. The system cannot keep up with the changing energy function, and each repetition gives a different result. Two exact relations show that the equilibrium free-energy difference can still be recovered from these hurried runs.

Each run is described by one number, the **work** $W$. In mechanics, work is the energy that you transfer to a system by acting on it from outside ([primer](physics.html#energy)). Here "acting from outside" means changing $\lambda$. At each time step $\lambda$ is raised by a small amount $d\lambda$. The atoms have had no time to move, so the energy changes by $(\partial U/\partial\lambda)\,d\lambda$, and the work is the sum of these changes over the run.

The work differs from one repetition to the next. Its mean over the repetitions is written $\langle W\rangle$.

Change $\lambda$ from 0 to 1 in a finite time and record the work $W=\int_0^1(\partial U/\partial\lambda)\,d\lambda$ along the trajectory. The second law says $\langle W\rangle\ge\Delta A$, with equality only for an infinitely slow change. [Jarzynski (1997)](cite:jarzynski1997) showed there is an exact equality for any switching speed:

$$
\boxed{\big\langle e^{-\beta W}\big\rangle = e^{-\beta\Delta A}}
$$

where the average is over many repetitions started from equilibrium in state A.

<div class="legend" markdown="1">
- $W$: the work done in one switching run, in kJ/mol. It differs from run to run.
- $\big\langle\dots\big\rangle$: here the mean over many runs, each started from a different configuration taken from an equilibrium simulation of state A. It is not an average over the frames of one run.
- $\Delta A$: the equilibrium free-energy difference between state B ($\lambda=1$) and state A ($\lambda=0$).
- $\beta$: $1/k_BT$.
</div>

The integral for $W$ looks like the TI formula, with one difference. TI uses the equilibrium average of $\partial U/\partial\lambda$ at each $\lambda$. Here the values come from a single trajectory that is not at equilibrium with the current $\lambda$, and nothing is averaged.

The **second law** of thermodynamics, in the form needed here, says that changing a system at constant temperature costs on average at least the free-energy difference ([primer](physics.html#thermodynamics)). The work beyond $\Delta A$ is the **dissipated work**. It ends up as heat in the thermostat. Stirring honey is the everyday picture: stir fast and you work much harder than when you stir slowly, and the extra effort warms the honey.

**Read it like this.** Compare with the FEP formula, written as $e^{-\beta\Delta A}=\langle e^{-\beta\Delta U}\rangle_A$. Jarzynski's equality has the same form with the work in the place of $\Delta U$, and FEP is its limiting case. Switch infinitely fast, in a single step: the atoms do not move at all, the work is $U_B-U_A=\Delta U$ of the starting configuration, and the equality becomes the Zwanzig formula. Switch infinitely slowly: the system stays at equilibrium, every run gives the same work $W=\Delta A$, and the calculation is TI. The same equation covers every speed between these two limits.

The second law follows from Jensen's inequality. The step is the same as for FEP: $e^{-\beta\Delta A}=\langle e^{-\beta W}\rangle\ge e^{-\beta\langle W\rangle}$, and taking $-k_BT\ln$ of both sides gives $\Delta A\le\langle W\rangle$. The second law is a statement about the average. Single runs can have $W<\Delta A$, and the equality depends on them.

[Crooks (1999)](cite:crooks1999) gave the underlying relation between the work distributions of the forward process and its reverse:

$$
\frac{P_F(W)}{P_R(-W)} = e^{\beta(W-\Delta A)} .
$$

<div class="legend" markdown="1">
- $P_F(W)$: the probability density of obtaining the work $W$ in the forward process, in which $\lambda$ goes from 0 to 1 starting from equilibrium in state A.
- $P_R(-W)$: the probability density of obtaining the work $-W$ in the reverse process, in which $\lambda$ goes from 1 to 0 along the same schedule run backwards, starting from equilibrium in state B.
- The minus sign in $-W$: a reverse run that exactly undid a forward run would give back the work, that is, $-W$.
- $\Delta A$: the free-energy difference from A to B.
- $\beta$: $1/k_BT$.
</div>

The two distributions cross at $W=\Delta A$.

**Read it like this.** Put $W=\Delta A$ into the formula: the exponent is zero and the two densities are equal. So if you plot the histogram of the forward work values and the histogram of minus the reverse work values, they cross at the free-energy difference. This is the picture of the two histograms of $\Delta U$ in the section on BAR, which is the special case of infinitely fast switching. For $W>\Delta A$ the forward density $P_F(W)$ is the larger of the two, and for $W<\Delta A$ it is the smaller, by the factor $e^{\beta(W-\Delta A)}$. Forward runs with $W<\Delta A$ exist and need not be rare: the second law limits only the mean of $W$.

Jarzynski's equality follows from the Crooks relation in two lines. Multiply both sides by $P_R(-W)\,e^{-\beta W}$ to get $P_F(W)\,e^{-\beta W}=P_R(-W)\,e^{-\beta\Delta A}$. Integrate both sides over all values of $W$. The left side is the average of $e^{-\beta W}$ over forward runs. On the right, $e^{-\beta\Delta A}$ is a constant and the integral of a probability density is 1.

In practice the Jarzynski average has the same weakness as FEP: it is dominated by rare trajectories with unusually low work. It is reliable only when the spread $\sigma_W$ of the work values is of the order of $k_BT$ (for a Gaussian work distribution the dissipated work $\langle W\rangle-\Delta A$ equals $\sigma_W^2/2k_BT$). Using both directions with the Crooks relation (which leads to BAR applied to work values) is much better.

Here $\sigma_W$ is the standard deviation of the work over the repetitions. The statement in brackets is the cumulant formula of the FEP section with $W$ in the place of $\Delta U$: $\Delta A=\langle W\rangle-\tfrac{\beta}{2}\sigma_W^2$, which is exact for a Gaussian.

Two numbers at 300 K. A spread of 5 kJ/mol ($2\,k_BT$) means 5 kJ/mol of dissipated work. A spread of 25 kJ/mol ($10\,k_BT$) means 125 kJ/mol. In the second case the runs that dominate the average lie 10 standard deviations below the mean work, and the chance of seeing one is about $10^{-23}$.

"BAR applied to work values" means this. In the BAR equation, the forward work values take the place of $\Delta U$ for the frames from A, and minus the reverse work values take the place of $\Delta U$ for the frames from B.

Fast non-equilibrium switching between two equilibrium ensembles is the basis of some protein-mutation workflows (for example pmx), and the same relations apply to steered MD run with a stochastic thermostat from equilibrated starting points (Module 14).

A switching workflow of this kind has three parts. Run one ordinary equilibrium simulation of state A and one of state B. From snapshots of the first, start many short runs in which $\lambda$ goes from 0 to 1, and from snapshots of the second, runs in which it goes from 1 to 0. Record the work of each run and apply the Crooks relation.

In steered MD (Module 14) a spring attached to a moving point pulls on part of the system, for example on a ligand in its site. The position of the moving point plays the part of $\lambda$, and the work is the force of the spring times the displacement of the moving point, added up over the run. A stochastic thermostat is one that acts through random kicks (Module 8).

## End-point methods

<div data-videos="Hy-Cc7nn2MY"></div>

Alchemical calculations are expensive: tens of windows, each a simulation. End-point methods are the cheap alternative. They simulate only the real states at the two ends, usually only the complex, and estimate the binding free energy from the energies of the saved snapshots with the help of a simplified model of the water. They are fast, and you need to know how far to trust them.

MM/PBSA and MM/GBSA estimate binding free energy from MD snapshots, usually of the complex alone (the single-trajectory protocol, in which receptor and ligand are cut out of the same frames) and sometimes from separate simulations of complex, receptor and ligand: $\Delta G\approx\langle\Delta E_{MM}\rangle+\langle\Delta G_{solv}\rangle-T\Delta S$, where the solvation term comes from a continuum model (Module 15) and the entropy from a normal-mode or similar estimate. They are much cheaper than alchemical or PMF methods because they need no intermediate states. They are also much less reliable: the terms are large and nearly cancel, the entropy is crude, and results depend on the dielectric constant chosen. They can rank related compounds in favourable cases and should not be read as absolute free energies. Linear interaction energy (LIE) is another method in this class.

<div class="legend" markdown="1">
- $\Delta G$: the estimated binding free energy.
- $\Delta E_{MM}$: the force-field energy of the complex minus the force-field energies of receptor and ligand, without any solvent. MM stands for molecular mechanics, another name for a force field.
- $\Delta G_{solv}$: the solvation free energy of the complex minus those of receptor and ligand, each computed from a continuum model.
- $\langle\dots\rangle$: the mean over the snapshots.
- $T$: the temperature. $\Delta S$: the change of the entropy of the solutes on binding. Binding restricts motion, so $\Delta S$ is negative and $-T\Delta S$ opposes binding.
</div>

The names spell out the recipe. PB (Poisson-Boltzmann) and GB (generalised Born) are two continuum models for the electrostatic part of the solvation free energy. SA stands for a term proportional to the solvent-accessible surface area, which accounts for the non-polar part. A **continuum model** replaces the water molecules by a uniform medium, described by its **dielectric constant**. This is the factor by which the medium weakens the interaction between charges, about 80 for water ([primer](physics.html#electrostatics)).

In the single-trajectory protocol only the complex is simulated. For each snapshot the energy of the complex is computed, then the ligand is deleted and the energy of the receptor is computed, and then the same is done for the ligand alone. Receptor and ligand therefore have exactly the shape they have in the complex, and any energy of changing shape on binding is left out.

The normal-mode estimate of the entropy treats the molecule as a set of harmonic vibrations around one energy minimum (Module 2). Slow, large motions between several minima are outside it.

Why "large and nearly cancel" matters: suppose, as an illustration, $\langle\Delta E_{MM}\rangle=-400$ kJ/mol and $\langle\Delta G_{solv}\rangle=+360$ kJ/mol. Their sum is $-40$ kJ/mol. An error of 2 % in each term is 8 and 7 kJ/mol, as large as the differences between ligands that you want to resolve. The cancellation has a physical reason. Charged and polar groups that attract each other in the complex were attracted to water before binding, so most of what is gained in direct interaction is paid back in lost solvation.

The dielectric constant enters for the water, where its value is known, and for the interior of the protein, where it is a parameter of the model that the user sets. The computed electrostatic terms change with that choice.

LIE estimates the binding free energy from the average interaction energy between the ligand and its surroundings, once in the complex and once free in water, scaled by empirical coefficients.

## Good practice

<div data-videos="cQQM1DTLR5g id5D_9PC1mA fxPNNVkSIWo zodHyKUyUbM"></div>

An alchemical calculation always returns a number. The checks below are how you find out whether to believe it.

- Equilibrate each $\lambda$ window and discard the equilibration (Module 11).
- Use Hamiltonian replica exchange between $\lambda$ windows (Module 14).
- Inspect the overlap matrix and add windows where overlap is poor.
- Check convergence by computing $\Delta A$ from the first $x$ % and from the last $x$ % of the data as a function of $x$ (forward and reverse plots).
- For networks of relative calculations, check cycle closure: the sum around any closed loop should be zero within error.
- Report the estimator, the number of windows, the simulation time per window and the uncertainty with its method.
- Validate the whole protocol on a system with a known answer first. Hydration free energies of small molecules are the standard test.

Software: `alchemlyb` and `pymbar` for analysis; GROMACS, AMBER, OpenMM, NAMD and CHARMM all run the simulations; `pmx`, OpenFE, Perses and FEP+ automate set-up. The LiveCoMS review by [Mey et al. (2020)](cite:mey2020) is the reference for practice.

### What each check is for

**Equilibration.** Every window is a different system, and its starting structure usually comes from another window or from an end state. The first part of each run is the relaxation to the new energy function. All the formulas of this module assume equilibrium, so that part is thrown away.

**Hamiltonian replica exchange.** At intervals, neighbouring windows try to swap their configurations, with an acceptance rule that keeps every window at its correct equilibrium distribution (Module 14). A configuration can then travel along $\lambda$. A rearrangement that is easy in the middle of the path, where the changing atoms interact weakly, reaches the end states, where it would be slow.

**The overlap matrix.** See the section on BAR. A value near zero next to the diagonal marks a pair of windows that are too far apart.

**Forward and reverse plots.** Here "forward" and "reverse" refer to time. The forward curve is $\Delta A$ computed from the first $x$ % of every window's data, and the reverse curve from the last $x$ %. At $x=100$ the two use all the data and coincide. If the calculation has converged, both curves reach that final value early and then stay flat within their error bars. A curve that is still drifting near the end means that the early data were not at equilibrium or that the runs are too short.

**Cycle closure.** Take three ligands and compute the three relative binding free energies A to B, B to C and C to A. Free energy is a state function, so the exact values add up to zero.

Suppose the computed values are $-3.1$, $+1.4$ and $+2.5$ kJ/mol. They add up to $+0.8$ kJ/mol. If each has an independent uncertainty of 0.5 kJ/mol, the uncertainty of the sum is $\sqrt3\times0.5=0.9$ kJ/mol, and the cycle closes within error. A sum of 5 kJ/mol would tell you that at least one of the three is wrong, though not which one.

**Hysteresis.** Compute the same change in both directions, from A to B and from B to A. The two results should be equal with opposite signs. The difference is the hysteresis introduced in the FEP section.

Cycle closure and hysteresis test sampling only. An error of the force field is the same along every path, so it closes every cycle perfectly and shows no hysteresis. Passing these checks is necessary and does not prove that the number agrees with experiment.

**Validation.** A hydration free energy uses the whole machinery (decoupling, soft-core potentials, the charge and Lennard-Jones stages, the estimator) on a system that is small, converges fast and has a measured answer. If your protocol fails there, it will not work on a protein.

### What accuracy to expect

Two kinds of error must be kept apart. The **statistical uncertainty** is the error bar that the estimator reports, or better, the spread between independent repeats started from different structures (Module 11). It says how reproducible the number is. The **systematic error** is everything that repeating does not reveal: an imperfect force field, a wrong protonation state, a wrong binding pose, or a slow motion that none of the runs sampled.

For relative binding free energies of similar small molecules, the figure quoted above is a root-mean-square error of 1 to 2 kcal/mol against experiment in favourable cases. As computed there, that is a factor of 5 to 29 in $K_d$. A useful yardstick: a factor of 10 in $K_d$ is 5.7 kJ/mol or 1.4 kcal/mol at 300 K. A predicted difference well below that between two ligands is within the noise of the method.

Absolute binding free energies are harder, for the reasons given in their section. End-point methods are useful for ranking related compounds at best. A small error bar does not mean a small error, because the error bar measures only the statistical part.

## Check yourself

<details markdown="1"><summary>1. Why is one-sided FEP from A to B biased when the perturbation is large?</summary>
The exponential average is dominated by configurations with low $U_B$, which are rare in the A ensemble. With a finite sample they are missed, the average of $e^{-\beta\Delta U}$ is underestimated, and $\Delta A$ is overestimated. The result looks converged because the missing configurations simply never appear.
</details>

<details markdown="1"><summary>2. In the relative binding cycle, why do you not need to simulate binding?</summary>
Free energy is a state function. The difference of the two horizontal legs equals the difference of the two vertical legs, and the vertical legs are alchemical changes at fixed binding state.
</details>

<details markdown="1"><summary>3. You pull a ligand out of its site 20 times and get a mean work of 180 kJ/mol with a standard deviation of 25 kJ/mol. Can you apply Jarzynski's equality directly?</summary>
Not usefully. A standard deviation of 25 kJ/mol is 10 $k_BT$. For a Gaussian work distribution the estimate would be $\langle W\rangle-\beta\sigma^2/2 = 180-125 = 55$ kJ/mol, but that value depends entirely on a tail that 20 samples do not contain.

Here $\langle W\rangle$ is the mean work, $\sigma$ its standard deviation and $\beta=1/k_BT$ with $k_BT=2.494$ kJ/mol at 300 K, so $\beta\sigma^2/2=25^2/(2\times2.494)=125$ kJ/mol.

Pull more slowly, or use the pulling only to generate umbrella windows.
</details>

<details markdown="1"><summary>4. Why are charges turned off before Lennard-Jones interactions when decoupling a molecule?</summary>
If the Lennard-Jones core were removed first, oppositely charged atoms of the environment could approach a bare charge to zero distance, giving an infinitely negative Coulomb energy.
</details>

<details markdown="1"><summary>5. Why may the free energy be computed along a path that no real molecule could follow?</summary>
Because free energy is a state function. $\Delta A=-k_BT\ln(Q_B/Q_A)$ contains the partition functions of the two end states and nothing about a path. Any chain of intermediate energy functions that starts at $U_A$ and ends at $U_B$ gives the same sum, so you are free to pick a chain whose neighbouring states overlap well.
</details>

<details markdown="1"><summary>6. Three windows give averages of $\partial U/\partial\lambda$ of 40, 12 and 2 kJ/mol at $\lambda$ = 0, 0.5 and 1. Estimate $\Delta A$ by thermodynamic integration. What would you do next?</summary>
The trapezoid rule gives $0.5\times(40+12)/2+0.5\times(12+2)/2=13+3.5=16.5$ kJ/mol. The curve falls steeply between the first two points and is nearly flat between the last two, so it bends. If the true curve is bowl-shaped between the points, as these three values suggest, the straight lines lie above it and the trapezoid rule overestimates the area. Add windows between $\lambda=0$ and 0.5 and see whether the result changes.
</details>

<details markdown="1"><summary>7. A relative calculation gives $\Delta G_{complex}(A\to B)=-12.0$ kJ/mol and $\Delta G_{free}(A\to B)=-8.0$ kJ/mol. Which ligand binds more strongly, and by what factor do the dissociation constants differ at 300 K?</summary>
$\Delta\Delta G_{bind}=-12.0-(-8.0)=-4.0$ kJ/mol, so B binds more strongly. The ratio is $K_d(B)/K_d(A)=e^{\Delta\Delta G/k_BT}=e^{-4.0/2.494}=0.20$: the dissociation constant of B is five times lower. A difference of 4 kJ/mol is about 1 kcal/mol, the size of the typical error of such calculations, so this prediction is not a safe one.
</details>

## Exercises

1. For two one-dimensional harmonic oscillators with force constants $k_A$ and $k_B$, compute $\Delta A$ analytically. Then estimate it by FEP in both directions, by TI and by BAR from sampled data, for $k_B/k_A$ = 1.5 and 20. Which estimators fail in which case?
2. Derive the second-order cumulant formula $\Delta A\approx\langle\Delta U\rangle-\tfrac{\beta}{2}\sigma^2$ and show it is exact when $\Delta U$ is Gaussian.
3. Compute the hydration free energy of methane or ethanol by decoupling it in water, following a published tutorial (for example the GROMACS free-energy tutorial). Analyse with `alchemlyb` using TI, BAR and MBAR, and compare with experiment.
4. Draw the thermodynamic cycle for the effect of a His to Ala mutation in a binder on its affinity for a target. List what could make the free-binder leg harder to converge than the complex leg.

## Read

{{READ}}

## Key papers

{{PAPERS}}
