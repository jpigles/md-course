---
num: 16
title: Kinetics, from rate theory to Markov state models
short: Kinetics and Markov models
part: Part V · Beyond all-atom
hours: 7
summary: Relate free-energy barriers to rates with transition state and Kramers theory, understand the committor, and build and validate a Markov state model from many short trajectories.
videos: 15
papers: K
tags: msm-kinetics
---

<div class="box goal" markdown="1">
#### After this module you can

- relate $K_d$ to $k_{on}$ and $k_{off}$ and estimate what MD can observe directly;
- write the transition state theory and Kramers rate expressions and say what each assumes;
- define the committor and explain why a barrier on an arbitrary coordinate is not an activation free energy;
- build a Markov state model: features, dimensionality reduction, clustering, transition matrix;
- validate it with implied time scales and the Chapman-Kolmogorov test.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Modules 12 to 14 computed free energies. A free energy tells you how much of each state there is at equilibrium: how much of a protein is folded, how much of a ligand is bound. It does not tell you how long it takes to go from one state to the other. That second question belongs to **kinetics**, the study of rates. It decides how long a drug stays on its target, how fast a protein folds, and whether a simulation of a given length can see an event at all.

The module has four layers:

1. **Rates.** What a rate constant is, how two rate constants fix the equilibrium populations, and what the kinetics of binding means for a simulation.
2. **From a barrier to a rate.** Transition state theory, then Kramers theory, which adds the friction of the solvent, and the mean first-passage time.
3. **The committor.** A number that says how far a configuration has progressed from one state to the other, and a test of whether the coordinate you chose describes the process.
4. **Markov state models.** A method that needs no coordinate chosen in advance. You cut the configurations into many small states, count the jumps between them in many short trajectories, and read the slow processes from a table of jump probabilities.

Layers 2 and 3 are what you need to read a paper that quotes a barrier or a rate. Layer 4 is the one you will use on your own trajectories. On a first reading you can skip the blocks marked "Optional" and the part on the mean first-passage time.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter means. The notation below first appears in this module. The general conventions (bold letters, dots for time derivatives, sums) are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $k_{AB}$ | A **rate constant**: the probability per unit time of a jump from state A to state B. Read the subscript from left to right: from A, to B. |
| $P_A$ | The **population** of state A: the fraction of all molecules (or of all simulation time) found in A. A number between 0 and 1. |
| $P_A^{eq}$ | The same at equilibrium, when the populations have stopped changing. |
| $\beta$ | Shorthand for $1/k_BT$, where $k_B$ is the Boltzmann constant and $T$ the temperature. At 300 K, $k_BT = 2.494$ kJ/mol. |
| $\ddagger$ | The double dagger marks a quantity taken at the top of a barrier. $\Delta W^\ddagger$ is the height of the barrier. |
| $\langle\dots\rangle_{\xi^\ddagger}$ | An average of the quantity between the brackets, taken only over the configurations that sit at the barrier top. |
| $P(a\mid b)$ | A **conditional probability**: the probability of $a$, given that $b$ is true. |
| $T_{ij}$ | The entry in row $i$ and column $j$ of the table (matrix) $\mathbf T$. Here it is the probability of going from state $i$ to state $j$. |
| $\mathbf p^T$ | A superscript $T$ on a list of numbers means that the list is written as a row. |
| $\mathbf T^k$ | The matrix $\mathbf T$ multiplied by itself $k$ times. |
| $\hat T$ | A hat marks an **estimate** computed from data, as opposed to the true value. |
| $\gg$, $\ll$ | "Much larger than" and "much smaller than". |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which meaning applies each time.

- $k$ with a subscript ($k_{AB}$, $k_{on}$, $k_{TST}$) is a rate constant, and so is a plain $k$ in the sections on rates and rate theory. $k_B$ is the Boltzmann constant. In the sections on Markov models, a plain $k$ counts lag times, as in $k\tau$, or is a label in a sum.
- $T$ in $k_BT$ is the temperature. $\mathbf T$ and $T_{ij}$ are the transition matrix. A superscript $T$, as in $\mathbf p^T$, turns a column into a row.
- $\tau$ is the lag time of a Markov model. $\tau(a\to b)$ is a mean first-passage time.
- $t$ is the time. $t_i$ with a subscript is the implied time scale of process number $i$.
- $P_A$ is a population and $P(\dots)$ a probability. An upright $\text{P}$ is the protein in $\text{P}+\text{L}$. $\mathbf p$ is a list of populations, and $p_B$ is the committor.
- $\pi$ is the number 3.14159 in $2\pi$. $\pi_i$ and $\boldsymbol\pi$ are the stationary distribution of a Markov model.
- $\lambda$ is an eigenvalue of the transition matrix. In the TICA step of the pipeline it is an eigenvalue of a different matrix problem.
- $C_{ij}$ is a number of counted transitions. $C_{ab}(\tau)$ in the TICA step is a covariance.
- $i$ and $j$ label states in $T_{ij}$ and $\pi_i$. In $\lambda_i$ and $t_i$ the label $i$ numbers the eigenvalues.
- $x$, $a$ and $b$: in the mean first-passage time, $x$ is a position along the coordinate and $a$ and $b$ are the start and the end. In the TICA step, $x_a$ is the value of feature number $a$. A bold $\mathbf x$ is a whole configuration. In the check of the moderate-friction formula, $x$ is short for $\gamma/2\omega_b$.
- $y$ is the variable of the inner integral in the mean first-passage time. In the TICA step it is a combination of features.
</div>

## Thermodynamics is not kinetics

<div data-videos="rFavri_VYfk balC-1gTQro hRpUif7C4Ek NOHVd_VgAD0"></div>

Picture two valleys separated by a mountain pass, and a crowd of hikers who wander at random. In the long run more hikers are found in the deeper valley, and how many more depends only on the two valleys. How often a hiker gets from one valley to the other depends on the pass. Raise the pass and the traffic drops, while the long-run numbers in the two valleys stay what they were.

Molecules behave in the same way. **Thermodynamics** is about the long-run numbers: the equilibrium populations of the states, which are fixed by their free energies (Module 3). **Kinetics** is about the traffic: how many jumps happen per unit time, which is fixed by the barrier between the states. This section makes the statement exact for the smallest case, two states.

<div class="box physics" markdown="1">
**Physics you need here: the rate constant and the waiting time.** Take many copies of a molecule, all in state A, and suppose that each copy can jump to state B. The **rate constant** $k$ is the probability per unit time that one copy jumps. Its unit is one over time, for example s$^{-1}$ or µs$^{-1}$. In a short time $dt$, a copy that is still in A jumps with probability $k\,dt$.

Let $S(t)$ be the fraction of copies that have not jumped yet at time $t$. During the next short time $dt$ a fraction $k\,dt$ of them jumps, so $S$ changes by $dS = -k\,S\,dt$. Dividing by $dt$:

$$
\frac{dS}{dt} = -k\,S, \qquad\text{with the solution}\qquad S(t) = e^{-kt} .
$$

The left part is a [differential equation](maths.html#ode): it gives the rate of change of $S$ in terms of $S$ itself. The right part is its solution, an [exponential decay](maths.html#exp-log) that starts at $S(0)=1$. You can check it by differentiating: the derivative of $e^{-kt}$ with respect to $t$ is $-k\,e^{-kt}$, which is $-k\,S$. A process whose rate is proportional to the first power of the amount present is called **first-order**.

Three consequences. The waiting time before the jump is random, and short waits are the most likely. The mean waiting time is $1/k$ (the average of $t$ weighted by the probability $k\,e^{-kt}\,dt$ of jumping between $t$ and $t+dt$). The time after which half of the copies have jumped is $\ln 2/k\approx0.69/k$. Example: with $k = 2$ µs$^{-1}$ the mean wait is 0.5 µs, half of the copies have jumped after 0.35 µs, and after 1 µs a fraction $e^{-2} = 0.14$ is still waiting.
</div>

Now let the copies jump in both directions. For two states A and B with rate constants $k_{AB}$ and $k_{BA}$,

$$
\frac{dP_A}{dt}=-k_{AB}P_A+k_{BA}P_B,\qquad\frac{P_B^{eq}}{P_A^{eq}}=\frac{k_{AB}}{k_{BA}}=e^{-\beta\Delta G_{AB}} .
$$

<div class="legend" markdown="1">
- $P_A$, $P_B$: the populations of A and B at time $t$, the fractions of all copies found in each state. They add up to 1.
- $dP_A/dt$: the rate at which the population of A changes.
- $k_{AB}$: the rate constant for jumps from A to B, in 1/time.
- $k_{BA}$: the rate constant for jumps from B to A.
- $-k_{AB}P_A$: the loss of A, the copies that leave A per unit time.
- $+k_{BA}P_B$: the gain of A, the copies that arrive from B per unit time.
- $P_A^{eq}$, $P_B^{eq}$: the populations at equilibrium, when they no longer change.
- $\beta$: $1/k_BT$, with $k_BT = 2.494$ kJ/mol at 300 K.
- $\Delta G_{AB}$: the free energy of B minus the free energy of A. It is positive when B is the less populated state.
- $e^{-\beta\Delta G_{AB}}$: the Boltzmann factor of that free-energy difference.
</div>

The first formula is a balance sheet for state A: what leaves, with a minus sign, and what arrives, with a plus sign. The second formula follows from it in two steps. At equilibrium the populations stop changing, so set $dP_A/dt=0$. That gives $k_{AB}P_A^{eq}=k_{BA}P_B^{eq}$: per unit time, as many copies go from A to B as come back. Divide both sides by $k_{BA}P_A^{eq}$ and you have $P_B^{eq}/P_A^{eq}=k_{AB}/k_{BA}$.

The last equality is the statistical mechanics of Module 3: the ratio of two equilibrium populations is the Boltzmann factor of their free-energy difference. A Boltzmann factor is $e^{-\beta E}$ for an energy $E$: the higher the energy, the smaller the factor. The ratio $P_B^{eq}/P_A^{eq}$ is called the **equilibrium constant** (see the [primer](physics.html#equilibrium)). So the equilibrium constant is the ratio of the two rate constants.

The free-energy difference fixes only the *ratio* of the rates. Multiply both rate constants by a thousand and every jump happens a thousand times more often, yet the ratio, the populations and $\Delta G_{AB}$ stay what they were.

The populations relax with the single rate $k_{AB}+k_{BA}$. To see why, use $P_B = 1-P_A$ in the balance sheet. Collecting the terms that contain $P_A$ gives $-(k_{AB}+k_{BA})P_A+k_{BA}$, and taking the factor $-(k_{AB}+k_{BA})$ out of both terms gives the form on the right:

$$
\frac{dP_A}{dt}=-k_{AB}P_A+k_{BA}(1-P_A)=-(k_{AB}+k_{BA})\,\big(P_A-P_A^{eq}\big),\qquad P_A^{eq}=\frac{k_{BA}}{k_{AB}+k_{BA}} .
$$

<div class="legend" markdown="1">
- $1-P_A$: the population of B, because the two populations add up to 1.
- $P_A-P_A^{eq}$: the distance of the population of A from its equilibrium value.
- $k_{AB}+k_{BA}$: the **relaxation rate**, in 1/time.
- Other symbols: as in the list above.
</div>

This is the equation of the box above, with the distance from equilibrium in the place of $S$ and $k_{AB}+k_{BA}$ in the place of $k$. Its solution is therefore an exponential decay of that distance:

$$
P_A(t)=P_A^{eq}+\big(P_A(0)-P_A^{eq}\big)\,e^{-(k_{AB}+k_{BA})\,t} .
$$

<div class="legend" markdown="1">
- $P_A(0)$: the population of A at the start.
- $P_A(t)$: the population of A after a time $t$.
- $e^{-(k_{AB}+k_{BA})t}$: a factor that starts at 1 and falls towards 0. It has dropped to $1/e\approx0.37$ after the **relaxation time** $1/(k_{AB}+k_{BA})$.
- Other symbols: as in the lists above.
</div>

Read it like this. Whatever the starting populations, the distance from equilibrium shrinks by the same factor in every equal interval of time. The rate of this approach is the *sum* of the two rate constants, so equilibrium is reached faster than either jump alone would suggest. An experiment or a simulation that watches populations relax therefore measures the sum. To get $k_{AB}$ and $k_{BA}$ separately you also need their ratio, which is the equilibrium constant.

<div class="box key" markdown="1">
**Worked example: the same populations at two speeds.** Say $k_{AB}=1$ µs$^{-1}$ and $k_{BA}=9$ µs$^{-1}$ (round numbers, for illustration). Then $P_B^{eq}/P_A^{eq}=1/9$, so $P_A^{eq}=0.9$ and $P_B^{eq}=0.1$. At 300 K, $\Delta G_{AB}=-k_BT\ln(1/9)=2.494\times2.197=5.48$ kJ/mol. The relaxation rate is $1+9=10$ µs$^{-1}$ and the relaxation time is 0.1 µs. Starting with every copy in A, $P_A(t)=0.9+0.1\,e^{-10t}$ with $t$ in µs: 0.937 after 0.1 µs and 0.905 after 0.3 µs.

A second molecule has $k_{AB}=0.001$ µs$^{-1}$ and $k_{BA}=0.009$ µs$^{-1}$. The ratio is the same, so the populations and $\Delta G_{AB}$ are the same, but the relaxation time is 100 µs. A measurement of populations cannot tell the two molecules apart. A simulation can: the expected number of A-to-B jumps in a run of length $t_{sim}$ is $P_A^{eq}\,k_{AB}\,t_{sim}$. In 10 µs that is $0.9\times1\times10=9$ jumps for the first molecule and $0.009$ for the second, which means that the run will almost certainly show none.
</div>

### Binding: on-rates, off-rates and what a simulation can see

Binding adds one complication: two molecules must meet before they can form a complex. For binding, $\text{P}+\text{L}\rightleftharpoons\text{PL}$:

$$
K_d=\frac{k_{off}}{k_{on}},\qquad\text{residence time}=\frac{1}{k_{off}} .
$$

<div class="legend" markdown="1">
- $\text{P}$, $\text{L}$, $\text{PL}$: the free protein, the free ligand and the complex. The double arrow $\rightleftharpoons$ says that the reaction runs in both directions.
- $k_{on}$: the **association rate constant**. The number of complexes formed per unit time and volume is $k_{on}[\text{P}][\text{L}]$, where square brackets are concentrations. Two concentrations are multiplied, so the unit of $k_{on}$ is M$^{-1}$s$^{-1}$ (M means mol per litre).
- $k_{off}$: the **dissociation rate constant**, the probability per unit time that one complex falls apart, in s$^{-1}$. It is a first-order rate constant like $k$ in the box above.
- $K_d$: the **dissociation constant**, $[\text{P}][\text{L}]/[\text{PL}]$ at equilibrium, a concentration. It is the concentration of free ligand at which half of the protein is bound. A small $K_d$ means tight binding (Module 3).
- Residence time: the mean lifetime of one complex.
</div>

Both relations follow from what you have seen. At equilibrium, complexes form as fast as they fall apart: $k_{on}[\text{P}][\text{L}]=k_{off}[\text{PL}]$. Divide both sides by $k_{on}[\text{PL}]$ and the left side becomes $[\text{P}][\text{L}]/[\text{PL}]$, which is $K_d$. For the residence time, one complex falls apart with probability $k_{off}$ per unit time, so by the box above its mean waiting time is $1/k_{off}$.

Read it like this. $K_d$ is thermodynamics: it is a ratio, and it does not say whether a binder is tight because it binds fast or because it leaves slowly. The two rate constants are kinetics, and they answer different questions. $k_{on}$ says how quickly a free ligand finds its site. $k_{off}$ says how long it stays there.

Association rates of proteins are typically $10^5$ to $10^7$ M$^{-1}$s$^{-1}$, bounded above by diffusion at about $10^9$ to $10^{10}$. For a 10 nM complex with $k_{on}=10^6$ M$^{-1}$s$^{-1}$, $k_{off}=10^{-2}$ s$^{-1}$: the complex lives for 100 seconds on average. Two complexes with the same $K_d$ can differ by orders of magnitude in residence time, and for drug efficacy residence time often matters more.

Three remarks on this paragraph. The diffusion bound exists because the two partners must first find each other by random motion through the water, and no binding step can be faster than these encounters. The arithmetic of the example is $k_{off}=K_d\,k_{on}=10^{-8}\ \text{M}\times10^{6}\ \text{M}^{-1}\text{s}^{-1}=10^{-2}$ s$^{-1}$, and the residence time is $1/k_{off}=100$ s.

For the last sentence of the paragraph, take two complexes with $K_d=10$ nM. One has $k_{on}=10^7$ M$^{-1}$s$^{-1}$ and $k_{off}=10^{-1}$ s$^{-1}$, and lives 10 s. The other has $k_{on}=10^5$ M$^{-1}$s$^{-1}$ and $k_{off}=10^{-3}$ s$^{-1}$, and lives 1,000 s, about 17 minutes.

**What MD can observe directly.** An event with rate constant $k$ happens about $k\,t_{sim}$ times in a simulation of length $t_{sim}$ that spends its time in the starting state. To estimate a rate by counting you want at least some ten events, so $k$ must be larger than about $10/t_{sim}$. For a 1 µs trajectory that means $k>10^7$ s$^{-1}$. The complex above, with $k_{off}=10^{-2}$ s$^{-1}$, misses this by nine orders of magnitude.

Association is slow too, for a different reason. In a simulation box of $10\times10\times10$ nm (an illustration) that holds one protein and one ligand, the ligand concentration is one molecule per 1,000 nm$^3$. With 1 M $=0.6022$ molecules per nm$^3$ (Module 3) this is $1/(1000\times0.6022)=1.7\times10^{-3}$ M, or 1.7 mM, a high concentration. Even so, with $k_{on}=10^6$ M$^{-1}$s$^{-1}$ the binding rate is $k_{on}[\text{L}]=1.7\times10^{3}$ s$^{-1}$, a mean waiting time of 0.6 ms.

So the kinetics of binding is out of reach of plain simulation in most cases. The rest of this module gives the two ways around the problem. Rate theories compute a rate from a free-energy barrier, which the methods of Modules 12 and 14 can provide. Markov state models assemble long time scales from many short trajectories.

## Transition state theory

<div data-videos="c-dKO66Sx9A"></div>

The two-state picture took the rate constants as given. Transition state theory (TST) computes one from the free-energy profile along a coordinate. Its idea fits in one sentence: the rate is the probability that a reactant is found at the top of the barrier, times the speed at which it moves through the top. The top of the barrier is called the **transition state**, which gives the theory its name.

Three terms from earlier modules are needed:

- A **collective variable** $\xi$ (Greek xi) is a single number, computed from the atomic positions, that measures the progress of the process. An example is the distance between a ligand and its binding site (Modules 12 and 14).
- The **potential of mean force** (PMF) $W(\xi)$ is the free energy as a function of $\xi$, defined by $W(\xi)=-k_BT\ln P(\xi)+\text{const}$, where $P(\xi)$ is the equilibrium [probability density](maths.html#probability) of $\xi$ (Modules 3 and 12). Its wells are the stable states and the hill between two wells is the barrier.
- **Configuration space** is the set of all possible arrangements of the atoms: positions only, without the velocities.

Divide configuration space into reactant and product by a surface at the top of the barrier, at $\xi=\xi^\ddagger$. Every configuration with $\xi$ below $\xi^\ddagger$ is then called reactant (state A) and every configuration above it product (state B). The border, all configurations with exactly $\xi=\xi^\ddagger$, is the **dividing surface**.

TST assumes that every trajectory crossing the surface towards products goes on to become product, and that reactants are in equilibrium. The first assumption says that nobody turns back after the top. The second says that the configurations inside A occur with their Boltzmann probabilities, including the rare ones near the top, although some copies keep leaving. A **flux** is a number of crossings per unit time. The rate is the equilibrium flux through the surface:

$$
k_{TST}=\tfrac12\big\langle|\dot\xi|\big\rangle_{\xi^\ddagger}\;\frac{e^{-\beta W(\xi^\ddagger)}}{\int_{A}e^{-\beta W(\xi)}d\xi} .
$$

<div class="legend" markdown="1">
- $k_{TST}$: the TST estimate of the rate constant from reactant to product, in 1/time.
- $\xi$: the collective variable. $\xi^\ddagger$ is its value at the top of the barrier.
- $\dot\xi$: the time derivative of $\xi$, the velocity along the coordinate. The bars in $|\dot\xi|$ take the absolute value: the speed, without its direction.
- $\langle\dots\rangle_{\xi^\ddagger}$: an average over equilibrium configurations that sit on the dividing surface.
- $\tfrac12$: at the top, half of the copies are moving towards the product and half are moving back. Only the first half counts.
- $W(\xi)$: the potential of mean force, an energy in kJ/mol.
- $\beta$: $1/k_BT$.
- $e^{-\beta W(\xi^\ddagger)}$: the Boltzmann factor at the barrier top. It is small when the top is high.
- $\int_A\dots d\xi$: an [integral](maths.html#integral) over the reactant region, all values of $\xi$ below $\xi^\ddagger$. It adds up the Boltzmann factors of all reactant positions.
</div>

Read it like this. The fraction on the right is a probability density: the chance, per unit length of $\xi$, that a copy which is somewhere in A is found at the top. Multiplying a probability per unit length by a speed (length per time) gives a probability per unit time, which is a rate constant.

Each part of the formula can be read on its own. A higher barrier makes the numerator exponentially smaller. A wider well makes the denominator larger and the rate smaller, because the reactant has more places to be that are not the top. A faster coordinate makes the first factor larger.

<details markdown="1"><summary>Optional: where the factor in front comes from</summary>
Call the fraction $\rho^\ddagger$. Among the reactant copies, the fraction found in a thin strip of width $d\xi$ at the top is $\rho^\ddagger\,d\xi$.

A copy that moves to the right with velocity $\dot\xi>0$ crosses the surface during the next short time $dt$ if it is closer to the surface than the distance it travels, $\dot\xi\,dt$. The fraction of copies in that strip is $\rho^\ddagger\,\dot\xi\,dt$.

Copies have different velocities, so average over them, counting only the positive ones. If $p(\dot\xi)$ is the probability density of the velocity, the fraction of copies that cross in $dt$ is

$$
\rho^\ddagger\,dt\int_0^\infty\dot\xi\;p(\dot\xi)\,d\dot\xi=\rho^\ddagger\,dt\;\tfrac12\big\langle|\dot\xi|\big\rangle .
$$

The equality holds because the distribution of velocities is symmetric: as many copies move left as right, so the integral over positive velocities is half of the average of $|\dot\xi|$ over all velocities. Dividing by $dt$ gives the crossings per unit time per reactant copy, which is the formula for $k_{TST}$.
</details>

The general formula becomes much shorter when the well has a simple shape. "Harmonic" means that near its minimum the PMF is a parabola, $W\approx W_{min}+\tfrac12m\omega_0^2(\xi-\xi_0)^2$, like the energy of a mass $m$ on a spring (Module 2 and the [primer](physics.html#oscillator)). Here $\xi_0$ is the position of the minimum, $W_{min}$ the free energy there, and $m$ the mass that moves along $\xi$.

For a one-dimensional harmonic well with frequency $\omega_0$ and barrier $\Delta W^\ddagger$ this becomes

$$
k_{TST}=\frac{\omega_0}{2\pi}\,e^{-\beta\Delta W^\ddagger},
$$

and in the form used by chemists (Eyring), $k=\dfrac{k_BT}{h}e^{-\beta\Delta G^\ddagger}$, with $k_BT/h=6.25\times10^{12}$ s$^{-1}$ at 300 K.

<div class="legend" markdown="1">
- $\omega_0$: the angular frequency of the oscillation in the reactant well, in radians per unit time.
- $\omega_0/2\pi$: the ordinary frequency, the number of full oscillations per unit time. Here $\pi$ is the number 3.14159.
- $\Delta W^\ddagger$: the barrier height, $W(\xi^\ddagger)-W_{min}$, measured from the bottom of the well.
- $e^{-\beta\Delta W^\ddagger}$: the Boltzmann factor of the barrier, a number between 0 and 1.
- $h$: Planck's constant, $6.626\times10^{-34}$ J s, a constant of quantum mechanics.
- $k_BT/h$: a frequency that depends only on the temperature, about 6 per picosecond at 300 K.
- $\Delta G^\ddagger$: the **activation free energy** of Eyring's form: the free energy of the system held at the top of the barrier minus the free energy of the whole reactant state. It is not the same number as $\Delta W^\ddagger$ (see below).
- $k$: the rate constant in Eyring's form, in 1/time. $k_B$ is the Boltzmann constant and $T$ the temperature.
- $k_{TST}$, $\beta$: as in the list above.
</div>

Read it like this. The system knocks at the barrier $\omega_0/2\pi$ times per unit time, once per oscillation in the well. Each attempt succeeds with probability $e^{-\beta\Delta W^\ddagger}$. The rate is attempts times success probability.

<div class="box key" markdown="1">
**Worked example: how strongly the rate depends on the barrier.** Say the oscillation in the well has a period of 1 ps, so $\omega_0/2\pi=10^{12}$ s$^{-1}$ (an illustration).

- Barrier of $5\,k_BT$ (12.5 kJ/mol at 300 K): $e^{-5}=6.7\times10^{-3}$, so $k=6.7\times10^{9}$ s$^{-1}$. One crossing per 0.15 ns.
- Barrier of $10\,k_BT$ (24.9 kJ/mol): $e^{-10}=4.5\times10^{-5}$, so $k=4.5\times10^{7}$ s$^{-1}$. One crossing per 22 ns.
- Barrier of $20\,k_BT$ (49.9 kJ/mol): $e^{-20}=2.1\times10^{-9}$, so $k=2.1\times10^{3}$ s$^{-1}$. One crossing per 0.5 ms.

Every extra $k_BT$ of barrier divides the rate by $e\approx2.7$. Every extra $k_BT\ln10=5.7$ kJ/mol divides it by ten. An error of 6 kJ/mol in a computed barrier is therefore an error of a factor ten in the rate.
</div>

<details markdown="1"><summary>Optional: from the general formula to the harmonic one</summary>
Two ingredients are needed, and both are [Gaussian integrals](maths.html#gaussian).

*The speed at the top.* At temperature $T$ the velocity along $\xi$ follows the Maxwell-Boltzmann distribution (Module 3): a Gaussian with mean zero and variance $k_BT/m$. For a Gaussian with standard deviation $\sigma$ the mean absolute value is $\sigma\sqrt{2/\pi}$. So $\langle|\dot\xi|\rangle=\sqrt{2k_BT/\pi m}$.

*The integral over the well.* With the parabola for $W$, the Boltzmann factor $e^{-\beta W}$ is a Gaussian in $\xi$ centred on the minimum. Almost all of its area lies near the minimum, so the integral over A can be extended over all $\xi$. The standard result $\int_{-\infty}^{\infty}e^{-ax^2}dx=\sqrt{\pi/a}$ with $a=\beta m\omega_0^2/2$ gives

$$
\int_Ae^{-\beta W(\xi)}d\xi\approx e^{-\beta W_{min}}\sqrt{\frac{2\pi k_BT}{m\,\omega_0^2}} .
$$

*Put them together.* Insert both into the general formula and use $W(\xi^\ddagger)-W_{min}=\Delta W^\ddagger$:

$$
k_{TST}=\frac12\sqrt{\frac{2k_BT}{\pi m}}\;\sqrt{\frac{m\,\omega_0^2}{2\pi k_BT}}\;e^{-\beta\Delta W^\ddagger}=\frac12\,\frac{\omega_0}{\pi}\,e^{-\beta\Delta W^\ddagger}=\frac{\omega_0}{2\pi}\,e^{-\beta\Delta W^\ddagger} .
$$

Under the two square roots, $k_BT$ and $m$ cancel and $\omega_0^2/\pi^2$ is left. Neither the mass nor the temperature survives in the factor in front.
</details>

Eyring's form is the same transition-state-theory rate with a different bookkeeping. Its factor in front, $k_BT/h$, is the same for every reaction, and everything that is specific to the reaction, the width of the well included, is put into $\Delta G^\ddagger$. For the one-dimensional harmonic well, setting the two forms equal gives $\Delta G^\ddagger=\Delta W^\ddagger+k_BT\ln\big(k_BT/h\nu_0\big)$, where $\nu_0=\omega_0/2\pi$ is the frequency in the well. For a well period of 1 ps at 300 K the extra term is $k_BT\ln6.25=4.6$ kJ/mol, and for a softer well with a period of 10 ps it is $k_BT\ln62.5=10.3$ kJ/mol.

So a barrier read from a PMF is not yet an activation free energy in Eyring's sense: the term for the width of the well is missing. If you put $\Delta W^\ddagger$ into Eyring's form unchanged, the rate comes out too high by the factor $k_BT/h\nu_0$, about 6 and about 60 in the two examples. With a barrier from a PMF, use $\omega_0/2\pi$ as the factor in front, or add the extra term to the barrier first. This is where the curvature of the well enters the first answer to "Check yourself" 2. As a number to remember: with $\Delta G^\ddagger=30$ kJ/mol at 300 K, $e^{-30/2.494}=6.0\times10^{-6}$ and Eyring's form gives $k=3.7\times10^{7}$ s$^{-1}$.

### Recrossing and the transmission coefficient

TST is an **upper bound**. Real trajectories recross the surface: they are knocked back by the solvent. The exact rate is $k=\kappa\,k_{TST}$ with a **transmission coefficient** $\kappa\le1$ that can be computed by launching short trajectories from the dividing surface (the reactive-flux, or Bennett-Chandler, method).

Here $\kappa$ (Greek kappa) is a pure number between 0 and 1, $k_{TST}$ is the TST rate constant of the formulas above, and $k$ is the true rate constant.

The picture is this. A copy arrives at the top and moves towards the product. TST counts it as a reaction at that instant.

In water, the next collision may reverse its velocity and send it back into the reactant well, or it may cross the top several times before it settles on one side. Each of these crossings was counted by TST, and only some of them belong to a completed reaction. TST can therefore only count too many crossings, never too few, which is why it is an upper bound. With $\kappa=0.1$, the true rate is a tenth of the TST rate.

The reactive-flux method measures $\kappa$ directly. You prepare many configurations on the dividing surface, give each one random velocities for the temperature, and follow each for a short time, until it has settled in A or in B. Then you compare the flow that ended in B with the flow that TST assumed. The trajectories can be short because they start at the top, the place that a free simulation almost never visits.

## Kramers theory

The harmonic TST formula contains the well and the barrier and nothing else. The solvent is absent from it. Yet a coordinate of a protein in water is pushed around by collisions all the time. Kramers theory puts the solvent back as friction, and asks how the rate depends on the strength of that friction.

<div class="box physics" markdown="1">
**Physics you need here: friction and Brownian motion.** A particle of mass $m$ that moves through a solvent with velocity $v$ feels a drag force $-m\gamma v$ that opposes the motion, and random kicks from the collisions with solvent molecules. Motion of this kind is called **Brownian motion**, and this description of it is the Langevin model of Module 8. With no other force, the drag makes the average velocity decay as $e^{-\gamma t}$. The **friction rate** $\gamma$ (Greek gamma) therefore has the unit 1/time, and $1/\gamma$ is the time after which the particle has forgotten its velocity.

When $\gamma$ is large, the particle forgets its velocity almost at once and its path is a random walk. The regime is called **overdamped** or diffusive. When $\gamma$ is small, the particle flies and oscillates almost as it would in vacuum, and the regime is called underdamped.

How fast a random walk spreads is measured by the **diffusion coefficient** $D$, in length squared per time: along one coordinate, the mean squared displacement after a time $t$ is $2Dt$. Friction and diffusion are tied together by $D=k_BT/m\gamma$: more friction, slower spreading. More in the [primer](physics.html#diffusion).
</div>

[Kramers (1940)](cite:kramers1940) treated barrier crossing as Brownian motion of a particle in a potential with friction $\gamma$. With angular well frequency $\omega_0$ and angular barrier frequency $\omega_b$ (each $\sqrt{|W''|/m}$, taken at the minimum and at the barrier top), friction rate $\gamma$ (in 1/time, as in Module 8) and barrier height $\Delta W^\ddagger$, the high-friction result is

$$
k_{Kramers}=\frac{\omega_0\,\omega_b}{2\pi\gamma}\,e^{-\beta\Delta W^\ddagger}\qquad(\gamma\gg\omega_b).
$$

<div class="legend" markdown="1">
- $k_{Kramers}$: the rate constant for crossing the barrier, in 1/time.
- $W''$: the second derivative of $W$ with respect to the coordinate, its [curvature](maths.html#derivative). It is positive at the minimum and negative at the barrier top, which is why the absolute value is taken.
- $m$: the mass that moves along the coordinate.
- $\omega_0$: the angular frequency of oscillation in the well, $\sqrt{W''_{min}/m}$. A stiff, narrow well has a large $\omega_0$.
- $\omega_b$: the angular barrier frequency, $\sqrt{|W''_{top}|/m}$. It measures how sharply the barrier top is curved. A particle without friction, released next to the top, slides away from it roughly as $e^{\omega_bt}$.
- $\gamma$: the friction rate, in 1/time.
- $\Delta W^\ddagger$: the barrier height. $\beta=1/k_BT$. In $2\pi$, $\pi$ is the number 3.14159.
- $(\gamma\gg\omega_b)$: the condition under which the formula holds. The velocity is forgotten, after a time $1/\gamma$, long before the particle could slide off the top, which takes a time of about $1/\omega_b$.
</div>

Read it like this. Compare with the harmonic TST formula: the Boltzmann factor and $\omega_0/2\pi$ are the same, and there is one new factor, $\omega_b/\gamma$. That factor is the transmission coefficient $\kappa$ of the previous section, and under the condition $\gamma\gg\omega_b$ it is much smaller than 1. With $\gamma=10\,\omega_b$ the rate is a tenth of the TST rate. Double the friction and the rate halves.

The rate is inversely proportional to friction: in the overdamped regime that applies to conformational changes of proteins in water, crossing the barrier top is a slow diffusion and the system recrosses many times. At very low friction the rate falls again, now in proportion to $\gamma$, because the particle cannot gain or lose energy fast enough. The rate therefore has a maximum at an intermediate friction, the "Kramers turnover" ([Hänggi, Talkner and Borkovec 1990](cite:hanggi1990)). For moderate friction Kramers' formula is $k=\kappa\,k_{TST}$ with $\kappa=\sqrt{1+(\gamma/2\omega_b)^2}-\gamma/2\omega_b$, which reduces to the high-friction result when $\gamma\gg\omega_b$.

The two limits are easier to remember as pictures.

| Friction | Picture | What limits the rate | How the rate changes with $\gamma$ |
|---|---|---|---|
| High, $\gamma\gg\omega_b$ | A ball pushed through honey | Diffusing across the flat region at the top, with many recrossings | Falls as $1/\gamma$ |
| Intermediate | Between the two | Little: the rate is at its maximum, nearest to the TST value and still below it | Almost flat |
| Very low | A ball on an almost frictionless track | Collecting enough energy to reach the top, and getting rid of it afterwards | Rises in proportion to $\gamma$ |

The low-friction row needs a few more words. To cross, the particle needs an energy above the barrier top, and the only source of energy is the solvent. When the coupling to the solvent is weak, a particle in the well waits a long time for that energy. Once it has it, it flies over the top, bounces off the far wall and flies back, because it loses energy as slowly as it gained it. It is not trapped in the product well until the solvent has taken the energy away.

The formula for moderate friction can be checked in both directions. Write $x=\gamma/2\omega_b$. For large $x$, $\sqrt{1+x^2}=x\sqrt{1+1/x^2}\approx x+1/2x$ (a [Taylor expansion](maths.html#taylor) of the square root), so $\kappa\approx1/2x=\omega_b/\gamma$, the high-friction factor. For example $x=5$ gives $\kappa=\sqrt{26}-5=0.099$, against $\omega_b/\gamma=0.1$.

For small $x$, $\kappa$ approaches 1, which is TST: $x=0.05$ gives $\kappa=0.95$. This formula does not contain the fall of the rate at very low friction, which needs a separate treatment.

Two lessons for simulation. First, anything that changes the effective friction (the thermostat's $\gamma$, a water model that is too fluid, a coarse-grained or implicit-solvent model) changes the rates without changing the free energies. The direction depends on the regime: more friction lowers the rate when the motion is overdamped and raises it at very weak friction. Second, the prefactor is not universal: it depends on the curvature and on the diffusion coefficient along the coordinate (with $D=k_BT/m\gamma$ the high-friction formula reads $k=D\sqrt{W''_{min}\,|W''_{top}|}\;e^{-\beta\Delta W^\ddagger}/2\pi k_BT$), so a barrier height alone does not give a rate.

Why the free energies do not change: equilibrium populations are given by Boltzmann factors of the energy, and friction does not appear in them. Friction only decides how fast the system moves between configurations. Two warnings of earlier modules have this origin. A Langevin thermostat adds its friction to that of the solvent and slows the dynamics (Module 8), and time in a coarse-grained model, which has lost part of the friction, has no simple relation to real time (Module 15). The "prefactor" is everything in front of the exponential.

The formula in brackets is the Kramers formula rewritten. Two substitutions are needed. From the definitions, $\omega_0\omega_b=\sqrt{W''_{min}/m}\,\sqrt{|W''_{top}|/m}=\sqrt{W''_{min}|W''_{top}|}/m$. And from $D=k_BT/m\gamma$, $1/m\gamma=D/k_BT$. Together:

$$
k=\frac{\omega_0\,\omega_b}{2\pi\gamma}\,e^{-\beta\Delta W^\ddagger}=\frac{D\,\sqrt{W''_{min}\,|W''_{top}|}}{2\pi\,k_BT}\;e^{-\beta\Delta W^\ddagger} .
$$

<div class="legend" markdown="1">
- $D$: the diffusion coefficient along the coordinate, for example in nm$^2$/ps when the coordinate is a distance.
- $W''_{min}$: the curvature of the PMF at the bottom of the well, in kJ mol$^{-1}$ nm$^{-2}$ for a distance.
- $W''_{top}$: the curvature at the barrier top, a negative number. The bars take its absolute value.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- Other symbols: as in the list above.
</div>

This form is the practical one, because it contains only quantities that a simulation can measure: two curvatures and a barrier height from the PMF, and a diffusion coefficient from the motion along the coordinate. The mass has dropped out. Example with round numbers: $D=0.001$ nm$^2$/ps, both curvatures 500 kJ mol$^{-1}$ nm$^{-2}$ and a barrier of $5\,k_BT$ give $k=0.001\times500\times e^{-5}/(2\pi\times2.494)=2.1\times10^{-4}$ ps$^{-1}$, one crossing per 4.7 ns. Halve $D$ and the rate halves, with the same PMF.

### The mean first-passage time

Start a trajectory at position $a$ and stop the clock the first time it reaches position $b$. The time on the clock is a **first-passage time**. It is different in every run, and its average over many runs is the **mean first-passage time**. It is the most direct definition of "how long does it take", and for diffusion along one coordinate it can be written down without approximating the shape of $W$.

For diffusive motion along a coordinate with free energy $W(x)$ and position-dependent diffusion coefficient $D(x)$, the mean first-passage time from $a$ to $b$ is exact:

$$
\tau(a\to b)=\int_a^b\frac{e^{\beta W(x)}}{D(x)}\left[\int_{-\infty}^{x}e^{-\beta W(y)}dy\right]dx .
$$

<div class="legend" markdown="1">
- $\tau(a\to b)$: the mean first-passage time from $a$ to $b$, a time. This $\tau$ is not the lag time of the later sections.
- $x$: a position along the coordinate between $a$ and $b$, the variable of the outer integral.
- $y$: a position to the left of $x$, the variable of the inner integral.
- $W(x)$: the free-energy profile (the PMF) along the coordinate. $\beta=1/k_BT$.
- $D(x)$: the diffusion coefficient, which may differ from place to place.
- $e^{\beta W(x)}$: an exponential with a *positive* sign. It is large where $W$ is high, at the barrier.
- $\int_{-\infty}^{x}e^{-\beta W(y)}dy$: the sum of the Boltzmann factors of all positions to the left of $x$, a measure of the population found there.
- $-\infty$: there is no exit on the left. The profile $W$ must rise there, so that the inner integral is finite.
</div>

Read it like this. "Exact" refers to the model of diffusive motion on a profile $W$: no parabola and no high barrier is assumed. The outer integrand is largest near the barrier top, where $e^{\beta W}$ is large, so the top dominates the passage time. At the top, the inner integral is the whole population of the starting well. A deep, wide well and a high, flat top both make the time long, and so does slow diffusion at the top.

Two checks with numbers. For a flat profile with a wall at $x=0$, constant $D$ and a target at distance $L$, the formula gives $\tau=\int_0^L(x/D)\,dx=L^2/2D$: with $L=1$ nm and $D=1$ nm$^2$/ns, 0.5 ns. For the double well $W(x)=5\,k_BT\,(x^2-1)^2$, with its minima at $x=\pm1$ and with $D=1$ in the units of the example, evaluating the two integrals numerically gives $\tau(-1\to1)=36.5$, while the inverse of the Kramers rate is 33.0. The two differ by about 10%, the price of replacing the well and the top by parabolas. For a barrier of $8\,k_BT$ the difference shrinks to 6%.

<details markdown="1"><summary>Optional: how the Kramers rate comes out of this integral</summary>
Take a constant $D$ and a barrier of several $k_BT$, and let $b$ lie well beyond the top.

*The outer integral.* Near the top, at $x^\ddagger$, the profile is an upside-down parabola, $W\approx W^\ddagger-\tfrac12|W''_{top}|(x-x^\ddagger)^2$. So $e^{\beta W}$ is a Gaussian peak centred on the top, and its area is $e^{\beta W^\ddagger}\sqrt{2\pi k_BT/|W''_{top}|}$.

*The inner integral.* For $x$ near the top it covers the whole well. With a parabola for the well, as in the TST section, it equals $e^{-\beta W_{min}}\sqrt{2\pi k_BT/W''_{min}}$, and it hardly changes while $x$ moves across the narrow peak.

*The product.*

$$
\tau\approx\frac{1}{D}\,\sqrt{\frac{2\pi k_BT}{|W''_{top}|}}\,\sqrt{\frac{2\pi k_BT}{W''_{min}}}\;e^{\beta(W^\ddagger-W_{min})}=\frac{2\pi\,k_BT}{D\sqrt{W''_{min}|W''_{top}|}}\;e^{\beta\Delta W^\ddagger} ,
$$

which is $1/k$ for the Kramers rate in its diffusion form. If $b$ is placed exactly at the top, the outer integral covers only half of the Gaussian peak and the result is half as large. A particle that has reached the top falls back as often as it goes on, so reaching the top takes half the time of a full transition. Exercise 1 uses this.
</details>

## The committor and what makes a good reaction coordinate

<div data-videos="ziRedoLEb2o"></div>

The rate formulas above need a coordinate with a well and a barrier top. A protein offers many candidate coordinates, and a convenient one need not describe the process well. This section gives the standard by which a coordinate is judged.

Start with a question about one configuration: if the system is released here, where does it go first, back to A or on to B? Rain on a mountain ridge is the picture. A drop that falls on one side of the ridge ends in one valley, a drop on the other side ends in the other valley, and the ridge line is where both outcomes are equally likely. The picture fails in one respect. Water runs downhill along a fixed path, while a molecule is kicked at random, so for a molecule the answer is a probability that changes gradually from 0 to 1.

For any configuration $\mathbf x$, the **committor** $p_B(\mathbf x)$ is the probability that a trajectory started from $\mathbf x$ with random Maxwell-Boltzmann velocities reaches state B before state A. It is 0 in A, 1 in B, and the true **transition state ensemble** is the set of configurations with $p_B=\tfrac12$.

<div class="legend" markdown="1">
- $\mathbf x$: one configuration, the positions of all atoms. Bold, because it is a list of many numbers.
- A, B: the two states, each a region of configuration space, for example "bound" and "unbound".
- $p_B(\mathbf x)$: the committor of configuration $\mathbf x$, a number between 0 and 1. The subscript B names the state that is to be reached first. This $p$ is not a momentum.
- Random Maxwell-Boltzmann velocities: velocities drawn at random from the distribution that belongs to the temperature (Module 3). The positions are the same in every trial and only the velocities differ.
- Transition state ensemble: an ensemble is a collection of configurations. This one collects the configurations from which both outcomes are equally likely.
</div>

The definition is also the recipe for computing it. Take the configuration, draw random velocities, and run until the trajectory reaches A or B. Repeat $N$ times. If $n_B$ of the runs ended in B, then $p_B\approx n_B/N$.

The statistical error of such a fraction is $\sqrt{p_B(1-p_B)/N}$: for $p_B=\tfrac12$ and $N=200$ runs it is 0.035. For a configuration near the top each run is short, because it ends as soon as a state is reached, but a few hundred runs are needed for every configuration, which makes the committor expensive.

The committor is the ideal reaction coordinate: it says exactly how far a configuration has progressed. A collective variable $\xi$ is a good reaction coordinate to the extent that the committor is a function of it, $p_B(\mathbf x)\approx g\big(\xi(\mathbf x)\big)$ with $g$ monotonic, so that every surface of constant $\xi$ is a surface of constant committor.

Three words in the last sentence need unpacking. $\xi(\mathbf x)$ is the value of the collective variable in configuration $\mathbf x$. $g$ is some function of one variable, and "monotonic" means that it never turns round: it only goes up as $\xi$ goes up (or only goes down, when B lies at small values of $\xi$). A "surface of constant $\xi$" is the set of all configurations that share one value of $\xi$. So the sentence says: once you know $\xi$, you know the committor, and nothing else about the configuration matters.

The test: collect configurations at the barrier top of your PMF, shoot many short trajectories from each, and histogram their committor values. A peak near $\tfrac12$ means $\xi$ captures the mechanism. A bimodal histogram with peaks near 0 and 1 means that the configurations at the "barrier top" already belong to one side or the other: an important coordinate is missing, the barrier in the PMF is lower than the true one, and a rate computed from it will be too high.

"Bimodal" means with two peaks. An example shows how this happens. Suppose that a ligand can leave its site only after a loop of the protein has opened, and that the opening of the loop is the difficult step. You compute the PMF along the distance between the ligand and the site, which is the convenient coordinate.

At the distance where your PMF has its maximum you will find two kinds of configurations: some with the loop closed, which fall back to the bound state, and some with the loop open, which go on to the unbound state. Configurations with the loop half open, the real bottleneck, are rare at every distance.

The PMF along the distance averages over the loop. Its maximum is made of the two common kinds of configurations and hides the rare half-open ones, so it lies lower than the barrier that the system has to cross. A lower barrier in a rate formula gives a higher rate.

This is why barrier heights read from a PMF along a convenient coordinate should not be quoted as activation free energies without such a check.

<details markdown="1"><summary>Optional: the committor along one coordinate</summary>
For diffusion along a single coordinate with a constant diffusion coefficient, with state A at $x=a$ and state B at $x=b$, the committor has a closed form. It is a standard result, given here without its derivation:

$$
p_B(x)=\frac{\int_a^xe^{\beta W(y)}dy}{\int_a^be^{\beta W(y)}dy} .
$$

Here $W$ is the free-energy profile, $\beta=1/k_BT$, and $y$ is the variable of integration. The integrand $e^{\beta W}$ is large near the barrier top, so the committor rises from 0 to 1 almost entirely in the region of the top.

For the double well $W(x)=5\,k_BT\,(x^2-1)^2$ with $a=-1$ and $b=1$, numerical integration gives $p_B=0.50$ at $x=0$, 0.80 at $x=0.2$ and 0.97 at $x=0.5$, and by symmetry 0.20 and 0.03 on the other side. A simulation agrees: of 4,000 Brownian trajectories started at $x=0.2$, a fraction 0.805 reached $x=1$ first. Nearly all of the change takes place where $W$ lies within about $2\,k_BT$ of the top. The transition state is a narrow region.
</details>

## Markov state models

<div data-videos="xNjQatR2rRU 0pB3pUXULmo YXppP_QTut8"></div>

Rate theory needs one coordinate, one barrier, and evidence that the coordinate is a good one. A protein has many states, many barriers and no coordinate that is known to be good. A Markov state model (MSM) avoids the choice.

The alternative to choosing a coordinate in advance: describe the dynamics as jumps between many small states, and estimate the jump probabilities from simulation. An MSM turns many short trajectories, which can be run in parallel and started from different points, into a model of long-time kinetics.

The sections below take this in steps: a Markov chain in the smallest example, the definition of the model, how it is estimated from trajectories, what its eigenvalues mean, the full pipeline for a protein, how the model is validated, how to sample for it, and what goes wrong.

### A Markov chain in a small example

Think of a board game in which your next square depends only on the square you are on now and on the dice. How you reached the square does not matter. A process with this property is a **Markov chain**, and the property is called **memoryless**, or Markovian.

Take a molecule with two states, 1 and 2, and look at it once every nanosecond. Suppose that a molecule seen in state 1 is found in state 2 at the next look with probability 0.1, and that a molecule seen in state 2 is found in state 1 with probability 0.3 (numbers chosen for illustration). The four possibilities fit in a table, the **transition matrix**:

$$
\mathbf T=\begin{pmatrix}T_{11}&T_{12}\\ T_{21}&T_{22}\end{pmatrix}=\begin{pmatrix}0.9&0.1\\ 0.3&0.7\end{pmatrix} .
$$

<div class="legend" markdown="1">
- $\mathbf T$: the transition matrix, a table of probabilities.
- $T_{ij}$: the probability of being in state $j$ at the next look, given state $i$ now. The first label is the row and says where the molecule comes from. The second is the column and says where it goes.
- Row 1, $(0.9,\ 0.1)$: a molecule in state 1 stays with probability 0.9 and moves to state 2 with probability 0.1.
- Row 2, $(0.3,\ 0.7)$: a molecule in state 2 moves to state 1 with probability 0.3 and stays with probability 0.7.
- Every row adds up to 1, because the molecule has to be somewhere at the next look.
</div>

Now follow a large number of copies. Let $p_1$ and $p_2$ be the fractions of copies in the two states. After one step, state 1 holds the copies that were in 1 and stayed, plus the copies that were in 2 and moved: $p_1'=p_1T_{11}+p_2T_{21}$. In the same way $p_2'=p_1T_{12}+p_2T_{22}$. The prime marks the value one step later.

<div class="box maths" markdown="1">
**Maths you need here: a row of numbers times a matrix.** The two sums above are one operation, "multiply the row $\mathbf p^T=(p_1,\ p_2)$ by the matrix $\mathbf T$", written $\mathbf p^T\mathbf T$. The rule: entry $j$ of the result is $\sum_ip_iT_{ij}$. Go down column $j$ of the matrix, multiply each entry by the matching entry of the row, and add. Example: $(1,\ 0)\,\mathbf T=(1\times0.9+0\times0.3,\ \ 1\times0.1+0\times0.7)=(0.9,\ 0.1)$.

Two steps in a row are one multiplication by the matrix product $\mathbf T\,\mathbf T=\mathbf T^2$. Entry $(i,j)$ of a product of two matrices is $\sum_kT_{ik}T_{kj}$: the probability of going from $i$ to some state $k$ in the first step and from $k$ to $j$ in the second, added up over all intermediate states $k$. For the matrix above,

$$
\mathbf T^2=\begin{pmatrix}0.9\times0.9+0.1\times0.3&0.9\times0.1+0.1\times0.7\\0.3\times0.9+0.7\times0.3&0.3\times0.1+0.7\times0.7\end{pmatrix}=\begin{pmatrix}0.84&0.16\\0.48&0.52\end{pmatrix} .
$$

More in the [toolbox](maths.html#matrices).
</div>

Start with every copy in state 1 and apply the matrix again and again:

| Step | Time (ns) | $p_1$ | $p_2$ | $p_1-0.75$ |
|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0.25 |
| 1 | 1 | 0.9 | 0.1 | 0.15 |
| 2 | 2 | 0.84 | 0.16 | 0.09 |
| 3 | 3 | 0.804 | 0.196 | 0.054 |
| 4 | 4 | 0.782 | 0.218 | 0.032 |
| 8 | 8 | 0.754 | 0.246 | 0.004 |

Two things happen, and the rest of this part of the module is built on them.

**The populations settle.** They approach $(0.75,\ 0.25)$ and stay there. Check: $(0.75,\ 0.25)\,\mathbf T=(0.675+0.075,\ \ 0.075+0.175)=(0.75,\ 0.25)$. A set of populations that one step leaves unchanged is the **stationary distribution** of the chain, written $\boldsymbol\pi$. It is the equilibrium of the model. At that point the two flows balance: $0.75\times0.1=0.075$ of all copies go from 1 to 2 in a step, and $0.25\times0.3=0.075$ come back.

**The distance from equilibrium shrinks by a constant factor.** The last column reads 0.25, 0.15, 0.09, 0.054: each number is 0.6 times the one before. A constant factor per step is an exponential decay, the relaxation of the two-state rate equation seen at regular intervals. The factor is $1-T_{12}-T_{21}=1-0.1-0.3=0.6$, and the section on eigenvalues turns it into a relaxation time.

<details markdown="1"><summary>Optional: why the factor is 1 − T₁₂ − T₂₁</summary>
Use $p_2=1-p_1$ in the rule for one step: $p_1'=p_1T_{11}+(1-p_1)T_{21}=p_1(T_{11}-T_{21})+T_{21}$. The stationary value $\pi_1$ obeys the same rule and does not change: $\pi_1=\pi_1(T_{11}-T_{21})+T_{21}$. Subtract the second equation from the first:

$$
p_1'-\pi_1=(T_{11}-T_{21})\,(p_1-\pi_1)=(1-T_{12}-T_{21})\,(p_1-\pi_1) ,
$$

where the last step uses $T_{11}=1-T_{12}$. Solving the equation for $\pi_1$ gives $\pi_1=T_{21}/(T_{12}+T_{21})=0.3/0.4=0.75$. Compare with the rate equation of the first section, where $P_A^{eq}=k_{BA}/(k_{AB}+k_{BA})$: the same structure, with jump probabilities in the place of rate constants.
</details>

### The model

<div data-videos="kKC4ccoUHGU gSR2xp2NFIc"></div>

A Markov state model is a chain of this kind whose states are made from simulation frames. Each state is a region of configuration space, and every frame of every trajectory falls into exactly one of them. How the regions are made is the subject of "The pipeline" below. For now, take them as given.

Partition configuration space into $n$ discrete states. Choose a **lag time** $\tau$. The model is the transition probability matrix

$$
T_{ij}(\tau)=P\big(\text{in state }j\text{ at }t+\tau\ \big|\ \text{in state }i\text{ at }t\big),
$$

and the assumption is that the process is **Markovian** at lag $\tau$: the next state depends only on the current state, not on the history.

<div class="legend" markdown="1">
- $n$: the number of states, in practice 100 to 1,000 (see "The pipeline" below).
- $i$, $j$: the labels of two states, each from 1 to $n$.
- $\tau$: the **lag time**, the interval between "now" and "later", for example 1 ns or 10 ns. You choose it. It is a multiple of the interval at which frames were saved, and far longer than the time step of the integrator.
- $t$: any time along a trajectory.
- $T_{ij}(\tau)$: the probability of finding the system in state $j$ at time $t+\tau$, given that it is in state $i$ at time $t$. The matrix depends on $\tau$: with a longer lag the system has more time to move, and the numbers change.
- $P(\dots\mid\dots)$: a [conditional probability](maths.html#probability). The vertical bar reads "given that".
</div>

Then the model assumes that the populations evolve as $\mathbf p^T(t+k\tau)=\mathbf p^T(t)\,\mathbf T^k(\tau)$. The assumption is never exactly true for a discretised process, because the position inside a state is lost. The error shrinks when the states are fine, above all near barriers where the slow processes change fastest, and when $\tau$ is long enough that the system forgets within one lag time where inside a state it was.

<div class="legend" markdown="1">
- $\mathbf p(t)$: the populations of the $n$ states at time $t$, a list of $n$ numbers that add up to 1. $\mathbf p^T$ is the same list written as a row.
- $k$: a whole number, the number of lag times that pass. It is not a rate constant here.
- $\mathbf T^k(\tau)$: the matrix for lag $\tau$ multiplied by itself $k$ times.
</div>

Read the formula like this: to predict the populations after a time $k\tau$, apply the one-step matrix $k$ times. The table of the small example did exactly this.

Why can the assumption not be exactly true? A state is a region and has an inside. Think of a copy that has entered state $i$ a moment ago. It sits close to the border that it crossed and is more likely to go back than a copy that has been in state $i$ for a long time and sits in the middle. The future of a copy then depends on where it came from, which is memory.

A "discretised process" is the sequence of state labels, in which the exact position has been thrown away.

Two things reduce this memory, and they are the two named in the paragraph above. If a state is small, the border and the middle are almost the same place. If the lag time is long, a copy has wandered all over its state before the next look, and where it entered no longer matters.

Fine states matter most near barriers. "Where the slow processes change fastest" is short for: where the right eigenvector of a slow process (see "What the eigenvalues mean" below), which is nearly constant inside each well, changes from its value in one well to its value in the other. That happens at the barrier, which is also where the future of a configuration changes fastest with position. In a one-dimensional double well with a barrier of $5\,k_BT$, the committor goes from 0.03 to 0.97 across the top of the barrier (the optional block of the previous section has the numbers). A single state that covers the whole top mixes configurations with opposite futures.

### Estimation

<div data-videos="pVl7TPFuHwk"></div>

Nobody gives you the transition matrix. You estimate it from the trajectories by counting. Once the states are defined, every trajectory becomes a list of state labels, one label per saved frame. This list is called a **discrete trajectory**.

Count transitions at lag $\tau$ along all trajectories: $C_{ij}$ is the number of times the system was in $i$ at time $t$ and in $j$ at $t+\tau$. The simplest estimate of the transition matrix is the row-normalised count matrix,

$$
\hat T_{ij}=\frac{C_{ij}}{\sum_kC_{ik}} .
$$

<div class="legend" markdown="1">
- $C_{ij}$: the number of counted transitions from state $i$ to state $j$ at lag $\tau$. The table of all of them is the **count matrix**.
- $\sum_kC_{ik}$: the sum of row $i$ of the count matrix, the total number of times the system was seen in state $i$ at the start of a pair. Here $k$ is a label that runs over all states.
- $\hat T_{ij}$: the estimate of $T_{ij}$: of all the times the system was seen in $i$, the fraction in which it was in $j$ one lag time later. The hat marks an estimate from data.
</div>

<div class="box key" markdown="1">
**Worked example: counting by hand.** A trajectory was saved every 1 ns and reads A A B A A A B B A A, ten frames. At a lag of 1 ns, compare every frame with the next one. That gives nine pairs: A to A four times, A to B twice, B to A twice, B to B once. Row A has $4+2=6$ counts, so $\hat T_{AA}=4/6=0.67$ and $\hat T_{AB}=2/6=0.33$. Row B has 3 counts, so $\hat T_{BA}=0.67$ and $\hat T_{BB}=0.33$.

At a lag of 2 ns, compare every frame with the frame two places later. That gives eight pairs: A to B three times, B to A three times, A to A twice and B to B never. Every frame is used as a starting point, so the pairs overlap. Nine counts are far too few for any conclusion. A real model needs many thousands of frames.
</div>

In Python the count takes a few lines:

```python
import numpy as np

def count_matrix(states, lag, n):
    """states: one state label (0 to n-1) per frame. lag: in frames."""
    C = np.zeros((n, n))
    for a, b in zip(states[:-lag], states[lag:]):
        C[a, b] += 1
    return C

C = count_matrix(states, lag=1, n=3)        # states: your discrete trajectory
T_hat = C / C.sum(axis=1, keepdims=True)    # divide every row by its sum
```

<div class="box key" markdown="1">
**Worked example: an estimate against a known answer.** To judge an estimate you need a case in which the truth is known. Take a chain with three states and a lag time of 1 ns (numbers chosen for illustration):

$$
\mathbf T=\begin{pmatrix}0.90&0.10&0\\0.20&0.79&0.01\\0&0.01&0.99\end{pmatrix} .
$$

States 1 and 2 exchange often. State 3 is reached only from state 2, and rarely. The stationary distribution is $\boldsymbol\pi=(0.5,\ 0.25,\ 0.25)$, which you can check by multiplying it with the matrix.

One trajectory of 10,000 steps (10 µs of "simulation"), generated from this matrix with random numbers, gave these counts at a lag of one step, and this estimate (a second run, with other random numbers, gives somewhat different counts):

$$
\mathbf C=\begin{pmatrix}4410&492&0\\491&1975&21\\0&20&2590\end{pmatrix},\qquad\hat{\mathbf T}=\begin{pmatrix}0.900&0.100&0\\0.197&0.794&0.008\\0&0.008&0.992\end{pmatrix} .
$$

The entries that rest on hundreds or thousands of counts are right to two decimals. The exchange between states 2 and 3 rests on 21 and 20 counts. The relative uncertainty of a count of $N$ random events is about $1/\sqrt N$, which is 22% for 21 events, and the estimates 0.008 against the true 0.01 are off by that order. The precision of a transition probability depends on how many times that transition was seen. The total length of the simulation does not decide it.
</div>

At equilibrium the dynamics obey detailed balance, $\pi_iT_{ij}=\pi_jT_{ji}$, and current practice is to restrict the model to the largest connected set of states and to use a maximum-likelihood estimator that enforces detailed balance. Bayesian estimators sample the distribution of transition matrices compatible with the counts and give error bars for everything derived from the model.

These two sentences contain four ideas.

**Detailed balance.** $\pi_i$ is the equilibrium population of state $i$, and $\pi_iT_{ij}$ is the fraction of all copies that jump from $i$ to $j$ during one lag time: the population of $i$ times the probability of the jump. Detailed balance says that this flow equals the flow in the opposite direction, for every pair of states separately. The reason is the time reversibility of Module 2. A film of a system at equilibrium looks equally plausible when it runs backwards, so every jump must be as frequent as its reverse. Both examples above obey it: $0.75\times0.1=0.25\times0.3$ in the two-state chain, and $0.5\times0.10=0.25\times0.20$ and $0.25\times0.01=0.25\times0.01$ in the three-state chain.

**Why enforce it.** Counts from a finite amount of data do not, as a rule, satisfy detailed balance exactly, least of all when they come from many short trajectories. Building it into the estimate uses a fact that is known in advance, which reduces the noise. It also guarantees that all eigenvalues of the matrix are ordinary real numbers, which the next section needs.

**The largest connected set.** A set of states is connected when every state in it can be reached from every other one, and back, along transitions that were observed. A state that trajectories entered and never left, or left and never entered again, cannot be given an equilibrium population relative to the others. Such states are removed before the estimate.

**Maximum likelihood, and the Bayesian alternative.** The maximum-likelihood estimate is the matrix under which the observed counts are most probable. Without extra conditions it is the row-normalised count matrix above. With detailed balance as a condition there is no closed formula, and the software finds the matrix by iteration.

A Bayesian estimator produces many matrices, each compatible with the counts, and they differ more from each other where the counts are few. You compute your quantity of interest, a population or a time scale, from each of them. The spread of the results is its error bar.

### What the eigenvalues mean

<div data-videos="opx_wViFlTs"></div>

A transition matrix with 500 states holds 250,000 numbers, and nobody can read a process from them directly. The eigenvalues and eigenvectors of the matrix sort the same information into a short list: the equilibrium populations, and a few slow processes, each with its time scale.

<div class="box maths" markdown="1">
**Maths you need here: eigenvectors of a transition matrix.** Module 2 introduced eigenvectors: special vectors that a matrix only multiplies by a number, the eigenvalue. A transition matrix acts on a row of populations, $\mathbf p^T\mathbf T$, so the vectors of interest here are rows with $\mathbf l^T\mathbf T=\lambda\,\mathbf l^T$. They are called **left eigenvectors**. In words, $\mathbf l$ is a pattern of populations that one step of the chain leaves unchanged in shape and multiplies by the number $\lambda$. "Diagonalising" the matrix means finding all its eigenvalues and eigenvectors, which a numerical library does in one call.

Example, with the two-state matrix of the small example. $(0.75,\ 0.25)\,\mathbf T=(0.75,\ 0.25)$: an eigenvector with eigenvalue 1. And $(1,\ -1)\,\mathbf T=(0.9-0.3,\ \ 0.1-0.7)=(0.6,\ -0.6)$: an eigenvector with eigenvalue 0.6.

A matrix also has **right eigenvectors**, columns $\mathbf r$ with $\mathbf T\,\mathbf r=\lambda\,\mathbf r$, for the same eigenvalues. With detailed balance the two kinds carry the same information: the entry of $\mathbf l$ for a state is the entry of $\mathbf r$ for that state times the equilibrium population of the state. More in the [toolbox](maths.html#eigen).
</div>

Diagonalise $\mathbf T$. The eigenvalues satisfy $1=\lambda_1>\lambda_2\ge\lambda_3\ge\dots$

- The left eigenvector with $\lambda_1=1$ is the **stationary distribution** $\boldsymbol\pi$: the equilibrium populations of the states, and so the free energies $F_i=-k_BT\ln\pi_i$, obtained from short trajectories that never individually sampled equilibrium.
- Each further eigenvector describes a **relaxation process**, an exchange of population between the regions where it is positive and negative, decaying with the **implied time scale**

$$
t_i=-\frac{\tau}{\ln|\lambda_i(\tau)|} .
$$

<div class="legend" markdown="1">
- $\lambda_i(\tau)$: eigenvalue number $i$ of the transition matrix that was estimated at lag $\tau$. The eigenvalues are numbered from the largest, $\lambda_1=1$, downwards. Here the label $i$ numbers processes, not states.
- $|\dots|$: the absolute value. An eigenvalue of a fast process can come out negative, and the bars keep the logarithm defined.
- $\ln$: the natural [logarithm](maths.html#exp-log). It is negative for a number between 0 and 1, so the minus sign in front makes $t_i$ positive.
- $\tau$: the lag time.
- $t_i$: the implied time scale of process $i$, for $i\ge2$, in the same unit as $\tau$.
- $\boldsymbol\pi$ (in the list above the formula): the stationary distribution, the list of the equilibrium populations $\pi_i$ of all states.
- $F_i$: the free energy of state $i$. $k_BT$ is 2.494 kJ/mol at 300 K.
</div>

A gap in the spectrum (a few slow processes well separated from the rest) indicates metastable states.

The "spectrum" is the list of eigenvalues. A **metastable** state is one in which the system stays for a long time before it leaves. The paragraphs below take the three statements in turn.

**The first eigenvector: populations and free energies.** The stationary distribution is the row of populations that a step leaves unchanged, $\boldsymbol\pi^T\mathbf T=\boldsymbol\pi^T$. That is the eigenvector equation with eigenvalue 1. No eigenvalue can be larger than 1, because a pattern of populations cannot grow without limit when the total is fixed at 1. The relation $F_i=-k_BT\ln\pi_i$ is the same link between a population and a free energy as in the PMF. In the three-state chain above, $\boldsymbol\pi=(0.5,\ 0.25,\ 0.25)$, so state 2 lies $k_BT\ln2=1.73$ kJ/mol above state 1.

The remark about short trajectories is the reason the method exists. To estimate $T_{ij}$ you only need to know what happens during one lag time after the system was in state $i$. Trajectories can therefore be short and can start anywhere. The matrix then says where the populations would settle if you waited long enough, although no single trajectory waited that long.

**The other eigenvectors: where the formula comes from.** Three steps. First, the starting populations can be written as the stationary distribution plus a mixture of the other left eigenvectors, which is always possible for a matrix with detailed balance:

$$
\mathbf p^T(0)=\boldsymbol\pi^T+\sum_{i\ge2}c_i\,\mathbf l_i^T .
$$

<div class="legend" markdown="1">
- $\mathbf p(0)$: the populations of all states at the start.
- $\boldsymbol\pi$: the stationary distribution, which is the first left eigenvector.
- $\mathbf l_i$: left eigenvector number $i$. Its entries add up to zero for $i\ge2$, so adding it moves population between states and leaves the total unchanged.
- $c_i$: a number that says how strongly process $i$ is present in the starting populations.
- $\sum_{i\ge2}$: a sum over all eigenvectors except the first.
</div>

Second, apply the matrix $k$ times. Each application leaves $\boldsymbol\pi$ unchanged and multiplies every $\mathbf l_i$ by its eigenvalue, so after $k$ steps each term carries the factor $\lambda_i^k$. Third, write that factor as an exponential, with the rule $a^k=e^{k\ln a}$:

$$
\mathbf p^T(k\tau)=\boldsymbol\pi^T+\sum_{i\ge2}c_i\,\lambda_i^k\,\mathbf l_i^T,\qquad\lambda_i^k=e^{k\ln\lambda_i}=e^{-k\tau/t_i}\quad\text{with}\quad t_i=-\frac{\tau}{\ln\lambda_i} .
$$

<div class="legend" markdown="1">
- $k$: the number of steps taken, a whole number.
- $k\tau$: the time that has passed.
- $\lambda_i^k$: the eigenvalue raised to the power $k$.
- $e^{-k\tau/t_i}$: an exponential decay in the elapsed time $k\tau$, with time constant $t_i$.
- Other symbols: as in the lists above.
</div>

The last equality is only a definition of $t_i$, chosen so that $k\ln\lambda_i$ equals $-k\tau/t_i$. With it, every process decays as $e^{-t/t_i}$, where $t=k\tau$ is the elapsed time. This is the form of the two-state relaxation of the first section, $e^{-(k_{AB}+k_{BA})t}$. So an eigenvalue is a decay factor per lag time, and the implied time scale is the same information expressed as a time.

The positive and negative entries of an eigenvector say where the population moves. States with a positive entry hold too much population while the process is present and states with a negative entry too little, or the other way round, depending on the sign of $c_i$. As the term decays, population flows from one group to the other.

Read the formula like this. An eigenvalue close to 1 means a slow process, because little of the pattern is lost in one lag time. In the two-state example, $\lambda_2=0.6$ at $\tau=1$ ns gives $t_2=-1/\ln0.6=1.96$ ns. The table agrees: after two steps the distance from equilibrium had fallen from 0.25 to 0.09, a factor 0.36, close to $1/e=0.37$.

For an eigenvalue near 1 a useful approximation is $t_i\approx\tau/(1-\lambda_i)$: $\lambda=0.99$ gives about $100\,\tau$. The same example shows how sensitive slow time scales are: 0.99 gives $99.5\,\tau$ and 0.98 gives $49.5\,\tau$, so an error of 0.01 in the eigenvalue is a factor two in the time.

The word "implied" is a reminder that nobody watched the relaxation happen. The time scale is implied by a matrix that was estimated at a short lag.

**From a relaxation time to rate constants.** Take the two-state system of the first section, with rate constants $k_{AB}$ and $k_{BA}$, and look at it once every $\tau$. The distance from equilibrium decays as $e^{-(k_{AB}+k_{BA})t}$, so the factor per lag time is $\lambda_2=e^{-(k_{AB}+k_{BA})\tau}$. Insert this in the formula: $t_2=-\tau/\ln\lambda_2=1/(k_{AB}+k_{BA})$.

Two conclusions follow. The implied time scale of a two-state system is its relaxation time, the inverse of the *sum* of the two rate constants. And $\tau$ has cancelled: with the example rates of 1 and 9 µs$^{-1}$, a lag of 0.01 µs gives $\lambda_2=e^{-0.1}=0.905$ and a lag of 0.05 µs gives $\lambda_2=e^{-0.5}=0.607$, and both give $t_2=0.1$ µs.

To get the two rate constants separately, combine the relaxation time with the populations. From $k_{AB}+k_{BA}=1/t_2$ and $k_{AB}/k_{BA}=\pi_B/\pi_A$ it follows that $k_{AB}=\pi_B/t_2$ and $k_{BA}=\pi_A/t_2$. For the two-state chain of the small example, with $\boldsymbol\pi=(0.75,\ 0.25)$ and $t_2=1.96$ ns, the rate constant from 1 to 2 is $0.25/1.96=0.13$ ns$^{-1}$ and the one from 2 to 1 is $0.75/1.96=0.38$ ns$^{-1}$.

<div class="box key" markdown="1">
**Worked example: the three-state chain.** For the matrix of the estimation example, with $\tau=1$ ns, a numerical library gives:

- $\lambda_1=1$, left eigenvector $(0.5,\ 0.25,\ 0.25)$: the stationary distribution.
- $\lambda_2=0.987$, left eigenvector proportional to $(-0.70,\ -0.30,\ +1.00)$, implied time scale $-1/\ln0.987=76$ ns.
- $\lambda_3=0.693$, left eigenvector proportional to $(+0.97,\ -1.00,\ +0.03)$, implied time scale $-1/\ln0.693=2.7$ ns.

Process 2 has one sign on states 1 and 2 and the other sign on state 3. It is the exchange between the pair $\{1,2\}$ and state 3, and it is slow. Process 3 has opposite signs on states 1 and 2 and almost nothing on state 3. It is the exchange between 1 and 2, and it is 28 times faster.

That factor is the gap in the spectrum. On times longer than a few nanoseconds, states 1 and 2 behave as one state, and the chain has two metastable states: $\{1,2\}$ with population 0.75 and $\{3\}$ with population 0.25.

You can watch both processes by starting with every copy in state 1 and applying the matrix. After 20 steps the populations are $(0.640,\ 0.311,\ 0.049)$: states 1 and 2 already stand in their equilibrium ratio of two to one, and state 3 is still almost empty. After 100 steps they are $(0.549,\ 0.271,\ 0.180)$, and after 400 steps $(0.501,\ 0.250,\ 0.249)$.
</div>

The numbers of the example come from these lines, which you can reuse for your own matrix:

```python
import numpy as np

T = np.array([[0.90, 0.10, 0.00],
              [0.20, 0.79, 0.01],
              [0.00, 0.01, 0.99]])
tau = 1.0                                  # lag time in ns

evals, left = np.linalg.eig(T.T)           # eigenvectors of the transpose = left eigenvectors of T
order = np.argsort(-evals.real)            # largest eigenvalue first
evals, left = evals.real[order], left.real[:, order]

pi = left[:, 0] / left[:, 0].sum()         # stationary distribution, normalised to sum 1
print(np.round(evals, 3))                  # [1.    0.987 0.693]
print(np.round(pi, 3))                     # [0.5  0.25 0.25]
print(np.round(-tau / np.log(evals[1:]), 2))   # [76.24  2.73]  implied time scales in ns
```

### The pipeline

<div data-videos="A3AUWXqqONc QHQBVmVq-Vo u4ec4EYsgkQ jXMaCSSOSgg CNYreswqJAQ"></div>

So far the states were given. For a protein you have to make them, from frames that each hold the coordinates of thousands of atoms. The list below is the map of the whole procedure. The paragraphs after it take the steps one at a time.

1. **Featurise.** Convert each frame into internal coordinates that do not depend on overall rotation: backbone dihedrals, distances between residues, contacts.
2. **Reduce dimension with TICA.** Time-lagged independent component analysis finds the linear combinations of features that decorrelate most slowly, by solving the generalised eigenvalue problem
   $$\mathbf C(\tau)\,\mathbf v=\lambda\,\mathbf C(0)\,\mathbf v,\qquad C_{ab}(\tau)=\big\langle\delta x_a(t)\,\delta x_b(t+\tau)\big\rangle .$$
   Compare with PCA (Module 11), which finds directions of largest variance: large and slow are not the same thing.
3. **Cluster** the frames in the reduced space into 100 to 1,000 microstates (k-means or similar).
4. **Estimate** $\mathbf T(\tau)$ for a range of lag times.
5. **Validate** (below), then choose the lag time.
6. **Coarse-grain** the microstates into a few metastable macrostates (PCCA+, or a hidden Markov model) for interpretation.
7. **Extract** populations, rates, mean first-passage times, and with transition path theory the committor, the reactive flux and the dominant pathways between two states.

The formula in step 2 uses these symbols.

<div class="legend" markdown="1">
- $x_a(t)$: the value of feature number $a$ in the frame at time $t$. The labels $a$ and $b$ run over the features.
- $\delta x_a(t)$: the deviation of that feature from its mean over all frames, $x_a(t)-\langle x_a\rangle$.
- $\langle\dots\rangle$: an average over all frames of all trajectories.
- $C_{ab}(\tau)$: the **time-lagged covariance** of features $a$ and $b$: the average of the deviation of $a$ now times the deviation of $b$ one lag time later. Here $\tau$ is a lag time chosen for this step.
- $\mathbf C(\tau)$: the matrix of all $C_{ab}(\tau)$. $\mathbf C(0)$ is the same at lag zero, the ordinary covariance matrix that PCA uses.
- $\mathbf v$: a list of weights, one per feature. It defines one combination of the features, $y=\sum_av_a\,\delta x_a$.
- $\lambda$: the eigenvalue that belongs to $\mathbf v$. It is the autocorrelation of the combination $y$ at lag $\tau$, a number near 1 for a slow combination and near 0 for a fast one. It is not an eigenvalue of the transition matrix.
</div>

**Step 1, features.** Cartesian coordinates change when the whole protein rotates or drifts, which says nothing about its shape. Features are numbers that depend on the shape alone: dihedral angles, distances between residues, and contacts (1 if two residues touch, 0 if they do not). Each frame becomes a list of hundreds or thousands of such numbers. No later step can repair this choice, because the model can only contain motions that the features can see.

**Step 2, TICA.** A list of a thousand features is too long to cluster well, and most of the features carry fast, local noise. The aim of this step is to keep a handful of combinations of features that carry the slow motions.

<div class="box maths" markdown="1">
**Maths you need here: covariance, autocorrelation and the generalised eigenvalue problem.** The **covariance** of two quantities is the average of the product of their deviations from their means. It is positive when the two tend to be above their means at the same time. The covariance of a quantity with itself is its **variance**, the square of its standard deviation (see the [toolbox](maths.html#averages)).

A *time-lagged* covariance compares one quantity now with another one a time $\tau$ later. For a single quantity $y$, the ratio $\langle\delta y(t)\,\delta y(t+\tau)\rangle/\langle\delta y^2\rangle$ is its **autocorrelation** at lag $\tau$ (Module 11). It is 1 if $y$ has not changed at all after $\tau$ and 0 if it has forgotten its value. A slow quantity has a high autocorrelation.

An ordinary eigenvalue problem reads $\mathbf A\mathbf v=\lambda\mathbf v$. A *generalised* one has a second matrix on the right-hand side, $\mathbf A\mathbf v=\lambda\mathbf B\mathbf v$, and libraries solve it in the same way. In TICA the eigenvalue has a direct meaning. Multiply the equation from the left by the row $\mathbf v^T$: the left side becomes $\langle\delta y(t)\,\delta y(t+\tau)\rangle$ for the combination $y=\sum_av_a\,\delta x_a$, and the right side becomes $\lambda\langle\delta y^2\rangle$. So $\lambda$ is the autocorrelation of $y$, and the eigenvector with the largest $\lambda$ is the slowest combination that the features allow.

A tiny example with two features that are not correlated with each other. Feature 1 has variance 4 and autocorrelation 0.1 at the chosen lag. Feature 2 has variance 1 and autocorrelation 0.9. Then $\mathbf C(0)$ has 4 and 1 on its diagonal, $\mathbf C(\tau)$ has $4\times0.1=0.4$ and $1\times0.9=0.9$, and the two eigenvalues are 0.1 and 0.9.

PCA ranks feature 1 first, because its variance is larger. TICA ranks feature 2 first, because it is slower.
</div>

The comparison with PCA in the list is easier to keep with a picture. A floppy loop at the surface moves a long way and does so within picoseconds. A side chain that blocks a binding site may move by a fraction of a nanometre once in a microsecond. PCA puts the loop first. For kinetics the side chain is the motion that counts, and TICA puts it first.

After this step every frame is described by a few numbers, its values along the slowest TICA components.

**Step 3, clustering.** The frames are now points in a space of a few dimensions, and clustering groups nearby points. The k-means method does it as follows: place a chosen number of centres among the points, assign every frame to its nearest centre, move each centre to the mean of the frames assigned to it, and repeat until nothing changes. Each centre with its frames is one **microstate**, and each frame receives the label of its microstate.

The number of microstates is a compromise. More of them means smaller states and a better Markov assumption. It also means fewer counts per transition and more statistical noise.

**Steps 4 and 5** are the estimation of the previous section, repeated for several lag times, and the validation of the next section.

**Step 6, coarse-graining.** A model with 500 microstates gives good numbers and no picture. If the spectrum has a gap after, say, the third eigenvalue, the system has three metastable states, and the microstates can be grouped into three **macrostates**. PCCA+ reads the grouping from the right eigenvectors of the slow processes: microstates with nearly the same entries there exchange quickly with each other and are put together. In the three-state chain the right eigenvector of the slow process is proportional to $(-0.35,\ -0.30,\ 1.00)$. States 1 and 2 have nearly the same entry and form one macrostate.

A hidden Markov model reaches the same goal in another way: it assumes a small number of hidden states with memoryless jumps between them, each of which produces the observed microstates with certain probabilities. "For interpretation" is meant literally. In the pipeline above, the time scales were computed and validated on the microstate model in steps 4 and 5, and the macrostates are for pictures and for words.

**Step 7, extracting results.** The population of a macrostate is the sum of $\pi_i$ over its microstates. Rates between macrostates and mean first-passage times follow from the matrix by solving sets of linear equations. **Transition path theory** (TPT) goes further. You name a start set A and a target set B of states, for example unbound and bound, and TPT answers three questions from the matrix alone, with no new simulation.

*What is the committor of every state?* The committor of a state is the average of the committors of the states it jumps to, weighted by the jump probabilities:

$$
q_i=\sum_jT_{ij}\,q_j\quad\text{for every state }i\text{ outside A and B},\qquad q_i=0\ \text{in A},\qquad q_i=1\ \text{in B}.
$$

<div class="legend" markdown="1">
- $q_i$: the committor of microstate $i$, the probability of reaching B before A when starting from $i$. It is the quantity $p_B$ of the committor section, for a state in place of a configuration.
- $T_{ij}$: the transition matrix of the model.
- $\sum_j$: a sum over all states $j$ that can be reached from $i$, including $i$ itself.
</div>

This is one linear equation per state, and a library solves the whole set. In the three-state chain with A $=\{1\}$ and B $=\{3\}$ there is one unknown, $q_2=T_{21}\times0+T_{22}\,q_2+T_{23}\times1$, so $q_2=T_{23}/(1-T_{22})=0.01/0.21=0.048$. From state 2 the system reaches state 3 before state 1 in fewer than 5% of the cases. State 2 lies on the side of state 1, as the eigenvectors said.

*Where does the traffic pass?* The **reactive flux** between two states is the number of transitions per unit time made by trajectories that are on their way from A to B. Trajectories that leave A and return to it are not counted.

*Which routes matter?* The reactive flux can be split into **pathways**, chains of states that lead from A to B, each with its share of the total. Statements such as "most binding events pass through this intermediate" come from this analysis.

The variational principle (VAMP) gives a score that measures how well a choice of features and states captures the slow dynamics, so that modelling choices can be compared objectively by cross-validation. Neural networks trained on this score (VAMPnets) merge steps 1 to 3.

The idea behind the score returns under "Validation" below: a poor description can make the slow processes look faster than they are, and apart from statistical noise it cannot make them look slower. Of several descriptions of the same data at the same lag time, the one in which the slow processes come out slowest is therefore the closest to the truth, and the score measures this. **Cross-validation** protects against rewarding noise: the model is built on one part of the trajectories and scored on another part that it has not seen. A VAMPnet is a neural network that takes the coordinates of a frame and returns its state directly, so that features, dimension reduction and clustering are learned together.

### Validation

<div data-videos="aO_DmbqHWYs"></div>

A Markov state model always produces numbers. Whether they mean anything depends on the Markov assumption, on the states and on the amount of data, and each of these can be tested. The three checks are listed first and explained after the list.

- **Implied time scales against lag time.** Compute $t_i(\tau)$ for increasing $\tau$. If the model is Markovian, a true relaxation time does not depend on the lag used to measure it. Choose the smallest $\tau$ at which the slow time scales have levelled off. Levelling off is necessary but not sufficient for a Markovian model, so it guides the choice of $\tau$ and does not validate the model; the Chapman-Kolmogorov test below does. Time scales that keep rising with $\tau$ mean the discretisation is too coarse: discretisation error always underestimates the slow time scales, which approach their true values from below. Too little data is a separate, statistical problem. No process faster than $\tau$ can be resolved.
- **Chapman-Kolmogorov test.** Check that $\mathbf T(k\tau)\approx\mathbf T(\tau)^k$: the model estimated at lag $\tau$ must predict, within error, the transition probabilities estimated directly from the data at longer lags.
- **Connectivity and statistics.** Every state kept must be reversibly connected to the rest, with transitions observed in both directions more than a few times. A state entered once and never left makes the model meaningless for that state.

**Implied time scales.** The two-state calculation in the section on eigenvalues showed why a true relaxation time does not depend on the lag: $\tau$ cancels. A model with memory behaves differently. At a short lag it sees fast returns across the borders of its states and reports a relaxation that is too fast. At longer lags these returns matter less and the reported time scale rises.

So you estimate the matrix at many lag times, compute $t_i=-\tau/\ln|\lambda_i(\tau)|$ for each, and plot the slow time scales against $\tau$. "Discretisation" is the cutting of configuration space into states, and its error is the memory described under "The model".

A worked example makes this concrete. Take the three-state chain as the truth, with its slow time scale of 76.2 ns, and suppose that your clustering produced only two states. In the good case the border lies where it should, $\{1,2\}$ against $\{3\}$. In the bad case it lies between states 1 and 2, giving $\{1\}$ against $\{2,3\}$. The table shows the implied time scale of each two-state model, computed exactly, that is, as if there were unlimited data.

| Lag $\tau$ (ns) | Good states (ns) | Bad states (ns) |
|---|---|---|
| 1 | 74.5 | 4.5 |
| 2 | 74.8 | 4.8 |
| 5 | 75.3 | 6.1 |
| 10 | 75.7 | 9.2 |
| 20 | 75.9 | 15.7 |
| 50 | 76.1 | 30.0 |
| 100 | 76.2 | 43.1 |
| 200 | 76.2 | 55.0 |

Both columns start below the true 76.2 ns and rise towards it, as the first bullet says. With good states the error is 2% at the shortest lag and the curve is flat. With bad states the model is 17 times too fast at a lag of 1 ns, and at 200 ns it is still 28% short and still rising. More data would not help, because the table already assumes unlimited data. Only better states would.

**The Chapman-Kolmogorov test.** For a memoryless chain, $k$ steps of length $\tau$ are the same as one step of length $k\tau$. That is the Chapman-Kolmogorov equation, $\mathbf T(k\tau)=\mathbf T(\tau)^k$, and the box on matrix products showed a case: $\mathbf T^2$ holds the probabilities for two steps.

The test compares the two sides, each obtained in its own way. The right side is the model: estimate the matrix at lag $\tau$ and raise it to the power $k$. The left side is the data: count pairs of frames a time $k\tau$ apart and normalise the rows. The comparison is usually shown for a few metastable sets, as the probability of being in a set after a time $k\tau$ when starting in it, with error bars from a Bayesian estimator. "Within error" means that the two curves agree inside those bars.

In the worked example, the model with bad states, estimated at a lag of 1 ns, predicts that a copy that starts in $\{1\}$ is found there 10 ns later with probability 0.55. Counting directly gives 0.67. After 20 ns the numbers are 0.51 and 0.64. The model fails.

With good states, the probability of being found in $\{1,2\}$ after 20 ns is 0.941 from the model and 0.942 from direct counting. The model passes.

Why are flat time scales not enough? They show that the eigenvalues estimated at different lags agree with each other. The Chapman-Kolmogorov test compares whole matrices, which also contain the eigenvectors, that is, where the population goes. It is the stronger test.

**No process faster than $\tau$.** The model looks at the system once per lag time. A process that relaxes in much less than $\tau$ is over between two looks, and its eigenvalue $e^{-\tau/t_i}$ is close to zero and lost in the noise.

The lag time is therefore a compromise. A short lag keeps the fast processes and risks memory. A long lag is safer for the Markov assumption, loses the fast processes and leaves fewer independent counts. The rule in the first bullet, the smallest lag at which the slow time scales are flat, is that compromise.

**Too little data.** This error is of a different kind. It is random, it can go in either direction, and more data cures it. Go back to the three-state chain with correct states and a correct lag, and estimate the slow time scale from one trajectory of 10,000 steps.

The trajectory of the estimation example gives 97 ns. In eight more repeats with different random numbers the estimate ranged from 63 to 105 ns, against the true 76 ns, and each trajectory contained between 19 and 28 transitions from state 2 to state 3. The fast time scale, which rests on thousands of transitions, ranged only from 2.6 to 3.0 ns. With trajectories of 1,000 steps there were between zero and three transitions to state 3, and one trajectory never reached it. A model built from that trajectory has two states and no slow process at all.

**Connectivity and statistics.** The last experiment is the reason for the third bullet. A transition seen once has a relative uncertainty of 100%. A state that was entered and never left has no measured exit probability, so its population and every time scale that involves it are undefined. Count the transitions in both directions for every state you keep. Error bars from a Bayesian estimator, or from repeating the analysis with part of the trajectories left out, tell you whether a time scale is known to 10% or to a factor of three.

The demo below builds a model from a particle that diffuses in a potential with three wells. Its left plot is the implied-time-scale plot of this section, and its right plot compares the stationary distribution of the model with the exact Boltzmann populations. The demo enforces detailed balance in the simplest way: it replaces $C_{ij}$ and $C_{ji}$ by their average before the rows are normalised.

This shortcut is not the maximum-likelihood estimator of the section on estimation. It treats every observed jump as if its reverse had been observed too, which is justified only when the trajectories as a whole sample equilibrium. The stationary distribution of the matrix it gives is then practically the fraction of frames found in each state. For the one long trajectory of the demo that is acceptable. For many short trajectories started away from equilibrium it gives wrong populations, and the freedom to start trajectories where you like (next section) is lost.

<div class="widget" data-widget="msm"></div>

### Sampling for a Markov model

<div data-videos="B8uo60u9TqI Fuai8_MSxaw HfTdS-kgG70"></div>

A single trajectory long enough to cross every barrier many times is what a Markov model lets you avoid. A road map can be drawn from many short trips, provided that together they cover every road in both directions. It does not need one driver who visits the whole country.

Because only local equilibrium within states is needed, the data can be many short trajectories from distributed computing or many GPUs. **Adaptive sampling** runs in rounds: build a preliminary model, start new trajectories from states that are poorly sampled or newly discovered, and repeat (doing this fully automatically and reliably for complex systems is still an open problem). Markov models have been used to describe protein folding at millisecond time scales and the binding and unbinding of ligands and of protein partners, including dissociation events that no single trajectory spans.

"Local equilibrium within states" is the precise condition. To estimate row $i$ of the matrix you need trajectories that pass through state $i$, and while they are inside it they must visit its configurations with their Boltzmann weights. A short trajectory reaches this condition quickly when the state is small.

What you do not need is the right *number* of trajectories in each state. Normalising each row divides that number out, so you may start many more trajectories in a rare state than its population would justify. "Poorly sampled" means few counts in a row or in a transition, and adaptive sampling sends the next round of trajectories there.

Limits: the model is only as good as the features (a slow motion that the features cannot see is absent from the model), rare states remain statistically weak, and the result depends on modelling choices, which is why the validation steps are not optional. The underlying trajectories must come from dynamics whose kinetics you are prepared to defend (Module 8).

The last sentence points back to Kramers theory. A Markov model reports the kinetics of the trajectories it was given. If they were run with a thermostat of strong friction, or with a coarse-grained model, the time scales of the model are those of that dynamics.

### Three ways to get a wrong model

| What went wrong | What you see | What to do |
|---|---|---|
| Too little data | Wide error bars. Time scales and populations change when part of the trajectories is left out. States with transitions in one direction only. | More trajectories, started in the weakly sampled states. Fewer and larger states where the counts are thin. |
| Poor features or poor states | Slow time scales keep rising with the lag time, and the Chapman-Kolmogorov test fails. In the worst case nothing shows it, because the missing motion is invisible to the features. | Add features that describe the missing motion and compare feature sets by their VAMP score. Use finer states near the transitions. Compare predictions with experiment. |
| Lag time too short | The time scales at the chosen lag lie below their plateau, and the model predicts kinetics that are too fast. | A longer lag time, at the price of losing the faster processes. |

The first row is a statistical error: random, in either direction, and cured by data. The second and third rows are systematic errors: they make slow processes look too fast, and more data of the same kind does not remove them. The worst case in the second row cannot be detected from inside the model, because validation only tests whether the model is consistent with the trajectories as the features describe them.

## Check yourself

<details markdown="1"><summary>1. A complex has K_d = 1 nM and k_on = 10⁶ M⁻¹s⁻¹. What is its residence time? How long would you have to simulate to see it dissociate ten times?</summary>
$k_{off}=K_d\,k_{on}=10^{-9}\times10^6=10^{-3}$ s$^{-1}$, a residence time of 1,000 s. Ten events would take about $10^4$ seconds of simulated time, some $10^{10}$ times longer than a 1 µs trajectory.
</details>

<details markdown="1"><summary>2. Your PMF along a distance has a 30 kJ/mol barrier. Using k = (k_BT/h) exp(−βΔG‡) you get a rate. Give two reasons it may be wrong by orders of magnitude.</summary>
(1) The prefactor $k_BT/h$ is the transition-state-theory value, an upper bound. In solution the motion over the barrier is diffusive and the prefactor depends on friction and curvature, often being $10^2$ to $10^4$ times smaller. (2) The distance may not be the reaction coordinate: if another slow variable is involved, the true barrier is higher than the one seen in the projection, and the transmission coefficient is small.
</details>

<details markdown="1"><summary>3. At lag time 10 ns the second eigenvalue of a Markov model is 0.95. What is the slowest relaxation time?</summary>
$t_2=-10/\ln0.95=195$ ns.
</details>

<details markdown="1"><summary>4. The implied time scale of the slowest process rises from 200 ns at τ = 1 ns to 2 µs at τ = 50 ns and is still rising. What should you do?</summary>
The model is not Markovian at these lags with this state definition. Improve the features and the discretisation (the states mix configurations on both sides of a barrier), and collect more data. Do not report the rate. The new data are for the finer states, which each need enough counted transitions. More data with the same states would not stop the rise, which is a discretisation error (see "Validation").
</details>

<details markdown="1"><summary>5. Two states exchange with k_AB = 2 µs⁻¹ and k_BA = 6 µs⁻¹. What are the equilibrium populations, the free-energy difference at 300 K and the relaxation time?</summary>
$P_B^{eq}/P_A^{eq}=k_{AB}/k_{BA}=1/3$, so $P_A^{eq}=0.75$ and $P_B^{eq}=0.25$. $\Delta G_{AB}=-k_BT\ln(1/3)=2.494\times1.099=2.74$ kJ/mol, where $\Delta G_{AB}$ is the free energy of B minus that of A. The relaxation rate is $k_{AB}+k_{BA}=8$ µs$^{-1}$, so the relaxation time is $0.125$ µs, or 125 ns. It is shorter than both mean waiting times, $1/k_{AB}=500$ ns and $1/k_{BA}=167$ ns.
</details>

<details markdown="1"><summary>6. A two-state Markov model at a lag time of 5 ns has T₁₂ = 0.02 and T₂₁ = 0.06. Find the stationary distribution, the implied time scale and the two rate constants.</summary>
$\pi_1=T_{21}/(T_{12}+T_{21})=0.06/0.08=0.75$ and $\pi_2=0.25$. The second eigenvalue is $\lambda_2=1-T_{12}-T_{21}=0.92$, so $t_2=-5/\ln0.92=60$ ns. The rate constants are $\pi_2/t_2=0.25/60=0.0042$ ns$^{-1}$ from state 1 to state 2 and $\pi_1/t_2=0.75/60=0.0125$ ns$^{-1}$ from state 2 to state 1. They are close to $T_{12}/\tau=0.004$ and $T_{21}/\tau=0.012$ ns$^{-1}$, because the lag time is much shorter than the relaxation time.
</details>

<details markdown="1"><summary>7. A discrete trajectory saved every 1 ns reads 1 1 2 2 2 1 1 1 2 1. Build the count matrix and the transition matrix at a lag of 1 ns. Why should you not trust the result?</summary>
The nine pairs of neighbouring frames give $C_{11}=3$, $C_{12}=2$, $C_{21}=2$ and $C_{22}=2$. Dividing each row by its sum, $\hat T_{11}=0.6$, $\hat T_{12}=0.4$, $\hat T_{21}=0.5$ and $\hat T_{22}=0.5$. Each kind of transition was seen only two or three times, so every entry has a relative uncertainty of the order of $1/\sqrt2$, about 70%.
</details>

## Exercises

1. Simulate overdamped Langevin dynamics on the one-dimensional double well for several barrier heights. Measure the mean time between crossings and compare with the Kramers formula and with the mean first-passage time integral. Count well-to-well transitions, not crossings of the barrier top: the mean first-passage time to the top itself is half the inverse rate.
2. For the same system, pick points at $x=0$ and compute the committor by shooting 200 short trajectories. Then compute it for points at $x=0.3$.
3. Discretise your double-well trajectory into 20 bins, build $\mathbf T(\tau)$ for several lag times with NumPy, and plot the implied time scales. Compare the slowest with the crossing time from exercise 1.
4. Work through the alanine dipeptide tutorial of PyEMMA or deeptime: features, TICA, clustering, implied time scales, Chapman-Kolmogorov test, PCCA+. Report the populations and exchange times of the main basins.

## Read

{{READ}}

## Key papers

{{PAPERS}}

