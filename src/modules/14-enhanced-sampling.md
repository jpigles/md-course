---
num: 14
title: Enhanced sampling, getting over barriers
short: Enhanced sampling
part: Part IV · Free energy and sampling
hours: 8
summary: Understand the main families of enhanced sampling (replica exchange, metadynamics, adaptive biasing, accelerated and steered MD, weighted ensemble), derive their key equations, and choose between them.
videos: 13
papers: I
tags: enhanced-sampling
---

<div class="box goal" markdown="1">
#### After this module you can

- classify an enhanced-sampling method by what it modifies: the potential along chosen coordinates, the temperature or Hamiltonian, or the ensemble of trajectories;
- derive the replica-exchange acceptance rule and estimate how many replicas a system needs;
- explain how metadynamics builds its bias and what well-tempering changes;
- say what steered MD and accelerated MD can and cannot give;
- list the properties of a good collective variable.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

A molecular dynamics run follows every atom, femtosecond by femtosecond, and that is also its limit. The events you usually care about (a loop that opens, a ligand that leaves its pocket, a peptide that folds) are **rare events**. The system waits for a long time in one shape and then changes quickly. A plain simulation spends almost its whole budget on the waiting, and often the event never comes.

This module is about methods that shorten the waiting. Each one changes the simulation on purpose and then corrects for the change, so that the result still describes the real system. Together they are called **enhanced sampling**. "Sampling" means collecting configurations (snapshots of all atomic positions) with the probabilities they have at equilibrium. Every average and every free energy is computed from such a collection (Module 3).

The module has four layers:

1. **The problem.** How long you would wait for a barrier of a given height, and the three kinds of cure.
2. **The vocabulary.** Collective variables: the one or two coordinates along which most methods act.
3. **The methods, one at a time.** Replica exchange, metadynamics and the adaptive biasing force, steered MD, accelerated MD, weighted ensemble and adaptive sampling. For each: the idea in words, the central formula with every symbol defined, what it gives and what it costs.
4. **Judgement.** Which method fits which problem, how to tell that a run has converged, and what information about the real motion is lost.

On a first reading the essential parts are the first section, replica exchange up to the boxed acceptance rule, and metadynamics up to the well-tempered formula. The blocks marked "Optional" and the estimate of the number of replicas can wait for a second reading.

### How to read the formulas

Every displayed formula in the main text is followed by a list that says what each letter in it means. Inside the boxes the surrounding sentences do that job. The notation below appears for the first time in this module or is used heavily in it. The general conventions are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\beta$ | Shorthand for $1/k_BT$, where $k_B$ is the Boltzmann constant and $T$ the temperature. At 300 K, $k_BT = 2.494$ kJ/mol and $\beta = 0.401$ mol/kJ. A product such as $\beta U$ is an energy counted in units of $k_BT$. |
| $\ddagger$ | A double dagger marks a quantity taken at the top of a barrier. $\Delta F^\ddagger$ is the height of a free-energy barrier. |
| $s$, $s(\mathbf r)$ | A **collective variable**: one number computed from the atomic positions $\mathbf r$, for example a distance. |
| $\mathbf x$, $\mathbf x'$ | A configuration: the positions of all atoms of one copy of the system. The prime marks a second, different configuration. It is not a derivative. |
| $\min\{a,\ b\}$ | The smaller of the two numbers $a$ and $b$. |
| $\propto$ | "Is proportional to": the two sides are equal up to a constant factor that is not written. |
| $t\to\infty$ | "As the time $t$ grows without limit": the value that is approached in a very long run. |
| $\sum_{t'<t}$ | A sum over all earlier times $t'$ at which something was done (here: a hill was added). |
| $\langle A\rangle$ | The average of the quantity $A$ over the configurations of an equilibrium simulation. |
| $\exp(x)$ | The same as $e^{x}$, the exponential function. It is written this way when the exponent is long. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The methods come from different groups and each kept its own notation.

- $k$ is a rate (crossings per second) in the first section, a label in the temperature ladder $T_k$, and a spring constant in steered MD. $k_B$ is always the Boltzmann constant.
- $V$ is the bias potential $V(s,t)$ in the metadynamics section and the potential energy $V(\mathbf r)$ in the accelerated MD section. Everywhere else the potential energy is $U$.
- $w$ is the height of a hill in metadynamics. $w_i$ with a label is the bias potential of replica $i$ in Hamiltonian replica exchange.
- $\Delta T$ is the gap between two neighbouring temperatures in replica exchange. In well-tempered metadynamics it is a parameter that sets how fast the hills shrink.
- $F$ is a free energy. $F_{pull}$ is a force.
- $\sigma$ is the width of a hill in metadynamics and a standard deviation elsewhere.
- $\lambda_m$ is the scaling factor of REST2. The plain $\lambda$ is the alchemical parameter of Module 13.
- $W$ is a work in steered MD. (Module 12 used $W$ for the potential of mean force, which this module calls $F$.)
- $C$ is a constant without importance in the free-energy and bias formulas. In the part on the number of replicas it is the heat capacity.
- $E$ is an energy in $F = E-TS$ and the threshold energy in accelerated MD.
- $n$ counts the steps of the temperature ladder, labels a second replica in the REST2 exchange, and numbers the saved frames in the reweighting formulas.

The lists under the formulas say which meaning applies each time.
</div>

## The problem in one formula

<div data-videos="PkTCrc0P_Xs 9JiorFETCTo EwGZ39PS1qk"></div>

This section answers one question: how long must a simulation run before an interesting event happens once? The answer decides whether plain MD is enough or whether you need the methods of this module.

Picture the energy of a molecule as a terrain of valleys and mountain passes (an energy landscape, [primer](physics.html#energy)). A valley is called a **basin**: a family of similar shapes, for example "loop closed" or "ligand bound". To go from one basin to another the system has to climb over a pass, the **barrier**. The climb is paid for by random pushes from the surrounding atoms, and a push large enough for a high pass is rare.

The picture is drawn in two dimensions, and that is where it can mislead. The real terrain has thousands of dimensions, and a pass can be hard to cross because it is high or because it is narrow and hard to find. Both cases appear below.

<div class="box physics" markdown="1">
**Physics you need here: free energy along a coordinate.** Module 3 defined a free energy as a function of one chosen coordinate $s$, such as a distance or an angle. Count how often an equilibrium simulation finds the system at each value of $s$. That gives a probability density $P(s)$ (the fraction of the frames per unit of $s$, Module 3), and the free energy along $s$ is

$$
F(s) = -k_BT\ln P(s) + C .
$$

Here $k_B$ is the Boltzmann constant, $T$ the temperature, $\ln$ the natural logarithm and $C$ a constant that does not matter, because only differences of $F$ are used. The product $k_BT$ is the typical size of a thermal push ([primer](physics.html#temperature)): 2.494 kJ/mol at 300 K. Where the system is often found, $P$ is large and $F$ is low: a basin. Where it is almost never found, $F$ is high: a barrier.

Two remarks. $F(s)$ is a *free* energy and not the potential energy: it already contains the effect of all the other coordinates, water included, through the count of how many configurations share the same $s$. And Modules 3 and 12 call the same function the potential of mean force and write it $W(\xi)$. More in the [primer](physics.html#thermodynamics).
</div>

The height of the barrier, measured from the bottom of the basin the system starts in, is written $\Delta F^\ddagger$. The rate of crossing a free-energy barrier $\Delta F^\ddagger$ is roughly

$$
k\approx k_0\,e^{-\beta\Delta F^\ddagger},
$$

with a prefactor $k_0$ of about $10^{9}$ to $10^{12}$ s$^{-1}$ for molecular motions in solution.

<div class="legend" markdown="1">
- $k$: the **rate** of crossing: the average number of crossings per second while the system sits in the starting basin. Its unit is s$^{-1}$.
- $\approx$: "is roughly equal to". The formula gives an order of magnitude, not three digits.
- $k_0$: the **prefactor**, also called the attempt frequency: how many times per second the system arrives at the foot of the barrier and tries.
- $e$: the base of the exponential function, 2.718. For positive $x$, $e^{-x}$ is a number between 0 and 1 that shrinks fast as $x$ grows.
- $\beta$: shorthand for $1/k_BT$. At 300 K, $\beta = 1/2.494 = 0.401$ mol/kJ.
- $\Delta F^\ddagger$: the height of the free-energy barrier above the bottom of the starting basin, in kJ/mol. $\Delta$ means "difference", and the double dagger marks the top of the barrier.
- $\beta\Delta F^\ddagger$: the barrier height counted in units of $k_BT$. It is a pure number.
</div>

Read it like this. The rate is a product of two factors: the number of attempts per second, $k_0$, and the fraction of attempts that succeed, $e^{-\beta\Delta F^\ddagger}$. The second factor is the Boltzmann factor of Module 3, often called the Arrhenius factor when it appears in a rate. It is the probability of finding the system at the top of the barrier relative to the bottom of the basin. A higher barrier or a lower temperature makes the exponent more negative and the rate smaller.

The quantity you feel in practice is the **mean waiting time**, $1/k$. If crossings happen at a rate of 1,000 per second, you wait on average one thousandth of a second for the next one. The waiting is random, so a single wait can be several times shorter or longer than the mean.

<div class="box maths" markdown="1">
**Maths you need here: the exponential and the logarithm.** The exponential function turns sums into products: $e^{a+b} = e^{a}\,e^{b}$. So adding a fixed amount to the barrier multiplies the rate by a fixed factor, whatever the barrier was before. The natural logarithm $\ln$ undoes the exponential: $\ln(e^{x}) = x$.

Use this to find the extra barrier height $\Delta$ that makes the rate ten times smaller. The condition is $e^{-\beta\Delta} = 1/10$. Take the logarithm of both sides: $-\beta\Delta = -\ln 10$. Multiply both sides by $-k_BT$: $\Delta = k_BT\ln 10 = 2.494\times2.303 = 5.74$ kJ/mol at 300 K. More in the [toolbox](maths.html#exp-log).
</div>

Each additional 5.7 kJ/mol (at 300 K) makes the event ten times rarer. The table works this out at 300 K for the two ends of the range of $k_0$. The first two columns are the barrier in kJ/mol and in units of $k_BT$.

| $\Delta F^\ddagger$ (kJ/mol) | $\beta\Delta F^\ddagger$ | $e^{-\beta\Delta F^\ddagger}$ | Mean wait if $k_0 = 10^{12}$ s$^{-1}$ | Mean wait if $k_0 = 10^{9}$ s$^{-1}$ |
|---|---|---|---|---|
| 10 | 4.0 | $1.8\times10^{-2}$ | 55 ps | 55 ns |
| 20 | 8.0 | $3.3\times10^{-4}$ | 3.0 ns | 3.0 µs |
| 30 | 12.0 | $6.0\times10^{-6}$ | 0.17 µs | 0.17 ms |
| 40 | 16.0 | $1.1\times10^{-7}$ | 9.2 µs | 9.2 ms |
| 50 | 20.0 | $2.0\times10^{-9}$ | 0.51 ms | 0.51 s |
| 60 | 24.1 | $3.6\times10^{-11}$ | 28 ms | 28 s |

A barrier of 40 kJ/mol gives waiting times of microseconds to milliseconds, and 60 kJ/mol gives tens of milliseconds to tens of seconds. The [primer](physics.html#time-scales) has a table of the time scales of molecular motions for comparison.

<div class="box key" markdown="1">
**Worked example: one row of the table.** Take $\Delta F^\ddagger = 40$ kJ/mol at 300 K.

1. *Barrier in units of $k_BT$.* $\beta\Delta F^\ddagger = 40/2.494 = 16.04$.
2. *Fraction of successful attempts.* $e^{-16.04} = 1.1\times10^{-7}$: about one attempt in nine million.
3. *Rate.* With $k_0 = 10^{12}$ s$^{-1}$, $k = 10^{12}\times1.1\times10^{-7} = 1.1\times10^{5}$ s$^{-1}$.
4. *Mean waiting time.* $1/k = 9.2\times10^{-6}$ s $= 9.2$ µs. With $k_0 = 10^{9}$ s$^{-1}$ it is a thousand times longer, 9.2 ms.

Now compare with what you can simulate. Say your budget is 1 µs (an illustration). Even with the fastest prefactor, the expected number of crossings in the whole run is $10^{-6}\ \text{s}\times1.1\times10^{5}\ \text{s}^{-1} = 0.11$. Most such runs would never see the event.
</div>

Plain MD spends almost all its time vibrating inside one basin. This is a problem for averages and not only for watching events. Module 3 showed that a time average along a trajectory equals the equilibrium average only if the trajectory is long enough to visit every important basin, and to visit each one many times. A run that stays in one basin reports the properties of that basin with small error bars and no warning that another basin exists. That is the **sampling problem**.

### Three ways out

Keep the terrain in mind. When the pass is too high for the walker, there are three things you can do.

1. **Raise the temperature.** A hotter system receives larger random pushes. In the formula, $\beta$ becomes smaller, so the same barrier counts for fewer units of $k_BT$. A barrier that is 40 kJ/mol of pure energy is crossed about 200 times more often at 450 K than at 300 K ($e^{-10.69}$ against $e^{-16.04}$, with the same prefactor). The price is that a hot simulation samples the hot system, where the shapes have other populations. The tempering methods run hot and cold copies together and pass structures between them.
2. **Change the terrain.** Add an extra energy term, a **bias**, that fills the valleys or lowers the passes, so that the system moves over a flatter terrain. Because you know exactly what you added, you can remove its effect from the results afterwards. Umbrella sampling, metadynamics, the adaptive biasing force and accelerated MD work this way. Steered MD is a rougher relative: it drags the system over the pass with a moving spring.
3. **Leave the terrain alone and manage many walkers.** Run many short, unmodified trajectories. Stop some of those that wander where many others already are, and start extra copies of the few that have made progress up the pass. Weighted ensemble and adaptive sampling work this way.

The first two change the temperature or the forces, so the motion you watch is no longer the real motion in time. The third keeps the real motion and pays with a large number of trajectories. This difference decides which methods can give rates, and the last two sections come back to it.

<div class="box maths" markdown="1">
**Maths you need here: reweighting.** A biased simulation visits configurations with the wrong frequencies, but they are wrong by a known factor, and a known factor can be divided out.

Add a bias energy $V_b$ to the potential energy $U$. The probability of a configuration was proportional to $e^{-\beta U}$. It is now proportional to $e^{-\beta(U+V_b)} = e^{-\beta U}\,e^{-\beta V_b}$. So each configuration is visited too rarely by the factor $e^{-\beta V_b}$ (or too often, where $V_b$ is negative). To undo this, count each saved frame with the **weight** $e^{+\beta V_b}$, using the bias energy that frame had, and take a weighted average:

$$
\langle A\rangle = \frac{\sum_n A_n\,e^{\beta V_{b,n}}}{\sum_n e^{\beta V_{b,n}}} .
$$

Here $n$ numbers the saved frames, $A_n$ is the value of the quantity $A$ in frame $n$, $V_{b,n}$ is the bias energy of frame $n$, and $\langle A\rangle$ is the average in the system without bias.

A two-state example. In the real system, a "closed" state holds 99 % of the population and an "open" state holds 1 %. You add a bias of $+11.46$ kJ/mol to every closed configuration and none to the open ones. At 300 K, $e^{-\beta\times11.46} = 1/99$, so the biased run spends half its time in each state: say 500 closed frames and 500 open frames.

Now reweight. Each closed frame gets the weight $e^{+\beta\times11.46} = 99$ and each open frame the weight 1. The weighted fraction of open frames is $500/(500\times99+500) = 0.01$, the true 1 %. The biased run moved between the two states easily and still returned the right populations.

One warning for later: this works well only while the weights are of similar size. If a few frames carry almost all the weight, the average rests on those few frames. More on averages in the [toolbox](maths.html#averages).
</div>

Enhanced sampling methods change the simulation so that barriers are crossed often, in a way that still allows the unbiased equilibrium distribution, or at least a free-energy difference, to be recovered. They fall into five families (the classification follows the review of [Hénin et al. 2022](cite:henin2022)):

| Family | What is changed | Examples | Needs collective variables? |
|---|---|---|---|
| Bias along chosen coordinates | A potential is added as a function of a few CVs, fixed in advance or built up during the run | Umbrella sampling, metadynamics, adaptive biasing force | Yes |
| Boost of the potential energy | The potential energy, or a part of it such as the dihedral terms, is raised wherever it is low | Accelerated MD, Gaussian accelerated MD | No |
| Tempering | Temperature or part of the Hamiltonian is scaled, usually across exchanging replicas | Temperature replica exchange, REST2, Hamiltonian replica exchange, simulated tempering | No |
| Driving out of equilibrium | The system is pulled along a coordinate in a finite time. It does not sample an equilibrium ensemble; free energies come from averaging the work | Steered MD, non-equilibrium switching | Yes |
| Trajectory ensembles | Many unbiased trajectories are managed so that rare ones are kept | Weighted ensemble, milestoning, transition path sampling, adaptive sampling with Markov models | A progress coordinate |

Some words in the table need a line each.

- *Unbiased equilibrium distribution*: the probabilities that the configurations have in the real, unmodified system at the temperature of interest. "Unbiased" means "as if nothing had been added".
- *CV*: collective variable, the subject of the next section.
- *Hamiltonian* (Module 2): the function that gives the total energy of the system. "Part of the Hamiltonian is scaled" means that some of the energy terms are multiplied by a factor.
- *Replica*: one of several copies of the system that are simulated side by side.
- *Simulated tempering*: a single copy whose temperature moves up and down a list of temperatures in a random walk during the run, in place of several copies that exchange.
- *Equilibrium ensemble* (Module 3): the collection of configurations, each with its Boltzmann probability, that a system at fixed temperature visits. A system that is being dragged does not have time to settle into it.
- *Non-equilibrium switching*: changing a parameter of the energy function in a finite time and recording the work, as in Module 13.
- *Progress coordinate*: a coordinate that measures how far a trajectory has advanced. It is used only to sort trajectories. No force is derived from it.

The five rows fit the three pictures. Rows one, two and four change the terrain (with a bias along chosen coordinates, with a boost everywhere, or by dragging). Row three raises the temperature, or imitates a higher temperature by scaling energies. Row five manages many walkers.

## Collective variables

<div data-videos="TYz9W8d54zM"></div>

Most methods of this module do not act on all the atomic coordinates. They act on one or two numbers computed from the coordinates, chosen by you. This section says what such a number is and what separates a useful choice from a harmful one.

The idea is the one behind any map. A protein in water has tens of thousands of coordinates or more, and nobody can draw, or fill with bias, a function of that many variables. So you describe the process by a number that changes as the process advances: for unbinding, the distance between the ligand and its pocket. The rest of the system is left to adjust by itself.

The standard name for such a number is **collective variable**, CV for short, because it depends on many atoms together. In symbols, $\mathbf r$ stands for the positions of all atoms and $s(\mathbf r)$ is a recipe that turns those positions into one number.

The usual choices are these:

- a **distance** between two atoms, or between the centres of mass of two groups of atoms;
- an **angle** or a **dihedral angle**, the twist around a bond (Module 5), such as the backbone angles $\phi$ and $\psi$ of a peptide;
- a **coordination number**: how many atoms of one kind lie within a chosen distance of a given atom or group. It is computed with a smooth counting function so that it changes gradually, because a bias force needs a slope;
- an **RMSD** (root-mean-square deviation, Module 11): the typical distance of the atoms from their places in a reference structure, after the two structures have been superposed;
- the **fraction of native contacts** $Q$: of all the pairs of atoms or residues that touch in the reference (native) structure, the fraction that also touch now. It runs from 0 (none formed) to 1 (all formed);
- a **path variable**: the position of the present structure along a chosen series of structures that leads from the starting state to the final state, like the kilometre mark along a road.

A collective variable $s(\mathbf r)$ is a function of the coordinates that describes the process in few dimensions: a distance, an angle, a coordination number, an RMSD, the fraction of native contacts, a path variable. A good CV:

1. **distinguishes** the initial, final and intermediate states;
2. **includes the slow motions**. Any slow motion not in the CV set is not accelerated, and the bias then pushes the system over the wrong ridge, producing hysteresis and wrong free energies;
3. is **few in number**: the cost of filling a free-energy landscape grows exponentially with the number of CVs, and three or four is the practical limit for most CV-based methods.

**Property 1.** If two states give the same value of $s$, the method cannot tell them apart, and neither can your free-energy profile. The distance between the two ends of a peptide, for example, can be the same in a folded hairpin and in a disordered compact coil. A profile along that distance mixes the two.

**Property 2** is the one that fails most often. A "slow motion" is any change that takes long to happen by itself.

Suppose a ligand can leave its pocket only after a side chain has swung out of the way, and suppose you chose the ligand-pocket distance as the only CV. The side-chain rotation is slow and is not in $s$. The bias pushes the ligand outward while the gate is still closed, and the ligand is forced out through the wall of the pocket, at an energy cost that the real process never pays. That is "the wrong ridge": a pass that exists on your one-dimensional map and is not the pass the real system uses.

**Hysteresis** means that the result depends on the direction or the history of the run: pushing the system from A to B gives one profile, and from B to A another. At equilibrium the answer cannot depend on the direction. Hysteresis therefore shows that some slow motion was left behind. The motions that are not described by the CV are called the **orthogonal degrees of freedom**, and every CV-based method assumes that they keep up.

**Property 3** is arithmetic. Suppose you need 20 points along each CV to draw the free energy. One CV needs 20 points, two CVs need $20^2 = 400$, three need 8,000 and four need 160,000. Each point has to be visited many times before its free energy is known, so the computer time grows by the same factors.

Finding good CVs is the hard part of this whole subject. Machine-learning approaches (time-lagged independent components, autoencoders, classifiers trained on end states) are increasingly used to propose them from preliminary simulations. In words: time-lagged independent components are the combinations of input coordinates that change most slowly in time (Module 16). An autoencoder is a neural network that compresses each structure into a few numbers and expands it again, so those few numbers must carry the main differences between structures. A classifier trained on end states is a model that has learned to tell structures of state A from structures of state B, and its output, which runs from "like A" to "like B", is used as the CV.

## Replica exchange (parallel tempering)

<div data-videos="qITm4laxhtk ktkmgiFJSGQ 5upvgbp_elI 5w6rRqq2Dhg"></div>

This is the first cure: raise the temperature. The difficulty is to use heat without ending up with the properties of a hot system. Replica exchange solves it by running several temperatures at once and letting structures travel between them.

A **replica** is one complete, independent copy of the simulated system: the same molecules and the same force field, with its own positions and velocities, running as its own simulation. Replicas do not interact. No atom of one replica feels a force from an atom of another. The only contact between them is the swap move described below.

Run $M$ copies of the system at temperatures $T_1<T_2<\dots<T_M$ simultaneously. The hot replicas cross barriers easily. At intervals, attempt to **swap configurations** between neighbouring temperatures, so that structures found at high temperature can reach the temperature of interest.

<div class="legend" markdown="1">
- $M$: the number of replicas.
- $T_1$: the lowest temperature, usually the one you care about (for example 300 K).
- $T_M$: the highest temperature, chosen hot enough for the barriers to be crossed quickly.
- $T_1<T_2<\dots<T_M$: the temperatures in rising order. The list is called the **temperature ladder**, and each temperature is a rung.
</div>

Think of the ladder as a relay. A structure that crossed a barrier at 450 K is handed down, one rung at a time, until it arrives at 300 K. A structure that was stuck at 300 K is handed up, is shaken loose at the top, and comes down again somewhere else. The swap has to follow a rule, or the cold simulation would fill up with hot structures that do not belong there. The rule is an accept-or-reject test, and deriving it needs one new idea.

<div class="box physics" markdown="1">
**Physics you need here: detailed balance and the Metropolis rule.** Suppose you want a procedure that visits states $a$, $b$, ... with given target probabilities $\pi(a)$, $\pi(b)$, ... (for us, Boltzmann probabilities). The procedure makes random moves from one state to another. It keeps the target probabilities stable if it obeys **detailed balance**: for every pair of states, the flow from $a$ to $b$ equals the flow from $b$ to $a$,

$$
\pi(a)\,P(a\to b) = \pi(b)\,P(b\to a) .
$$

Here $P(a\to b)$ is the probability that the procedure, being in $a$, moves to $b$. The left side is "how often you are in $a$" times "how often you then go to $b$". If the flows cancel pair by pair, no state gains or loses probability, so a collection of systems that has the target distribution keeps it.

The **Metropolis rule** is the standard way to obey detailed balance. Propose moves in such a way that proposing $a\to b$ is as likely as proposing $b\to a$. Then accept a proposal with probability $\min\{1,\ \pi(b)/\pi(a)\}$: always, if $b$ is at least as probable as $a$, and otherwise with a probability equal to the ratio. In a program you draw a random number between 0 and 1 and accept if it is smaller than the ratio.

A check with two states, $\pi(a) = 0.8$ and $\pi(b) = 0.2$. The move $a\to b$ is accepted with probability $0.2/0.8 = 0.25$, and the move $b\to a$ always. The flow from $a$ to $b$ is $0.8\times0.25 = 0.2$. The flow from $b$ to $a$ is $0.2\times1 = 0.2$. They are equal. More on probabilities in the [toolbox](maths.html#probability).
</div>

Take two replicas, $i$ and $j$, and treat the pair as one large system whose "state" says which configuration sits at which temperature. Two facts are needed. At equilibrium, a system at temperature $T$ is found in configuration $\mathbf x$ with a probability proportional to the Boltzmann factor $e^{-\beta U(\mathbf x)}$ (Module 3), where $U(\mathbf x)$ is the potential energy of that configuration and $\beta = 1/k_BT$. And the two replicas are independent, so the probability of finding both in given configurations is the product of the two separate probabilities. The rule then follows in three steps: the probability before the swap, the probability after it, and their ratio.

**The acceptance rule.** The joint probability of replica $i$ holding configuration $\mathbf x$ and replica $j$ holding $\mathbf x'$ is proportional to $e^{-\beta_iU(\mathbf x)}e^{-\beta_jU(\mathbf x')}$. After the swap it is $e^{-\beta_iU(\mathbf x')}e^{-\beta_jU(\mathbf x)}$. (The swap exchanges the two configurations and leaves the temperatures where they are, so each $\beta$ now multiplies the energy of the other configuration.)

For the third step, divide the second expression by the first. A ratio of exponentials is the exponential of the difference of the exponents:

$$
\frac{e^{-\beta_iU(\mathbf x')}\,e^{-\beta_jU(\mathbf x)}}{e^{-\beta_iU(\mathbf x)}\,e^{-\beta_jU(\mathbf x')}}
= \exp\big[-\beta_iU(\mathbf x')-\beta_jU(\mathbf x)+\beta_iU(\mathbf x)+\beta_jU(\mathbf x')\big].
$$

<div class="legend" markdown="1">
- $i$, $j$: the labels of the two replicas, two rungs of the ladder.
- $\mathbf x$, $\mathbf x'$: the configurations (all atomic positions) held by replica $i$ and by replica $j$ before the swap.
- $U(\mathbf x)$: the potential energy of configuration $\mathbf x$, in kJ/mol. All replicas use the same energy function $U$.
- $\beta_i = 1/k_BT_i$: the inverse temperature of replica $i$. A colder replica has a larger $\beta$.
- The fraction on the left: the probability of the arrangement after the swap (top) divided by the probability before it (bottom).
- $\exp[\dots]$: the exponential function, another way of writing $e$ to the power of the bracket.
</div>

Now tidy the exponent. Collect the two terms that contain $\beta_i$ and the two that contain $\beta_j$: the exponent is $\beta_i\big(U(\mathbf x)-U(\mathbf x')\big)-\beta_j\big(U(\mathbf x)-U(\mathbf x')\big) = (\beta_i-\beta_j)\big(U(\mathbf x)-U(\mathbf x')\big)$. This ratio plays the part of $\pi(b)/\pi(a)$ in the box. A swap is proposed as often in one direction as in the other, so the Metropolis rule applies. Detailed balance with the Metropolis criterion requires accepting with the ratio of the two:

$$
\boxed{P_{acc} = \min\Big\{1,\ \exp\big[(\beta_i-\beta_j)\,\big(U(\mathbf x)-U(\mathbf x')\big)\big]\Big\}}
$$

<div class="legend" markdown="1">
- $P_{acc}$: the probability with which the proposed swap is accepted, a number between 0 and 1.
- $\min\{1,\ \dots\}$: the smaller of 1 and the number that follows. A probability cannot be larger than 1.
- $\beta_i-\beta_j$: the difference of the two inverse temperatures. It is positive when $i$ is the colder replica.
- $U(\mathbf x)-U(\mathbf x')$: the energy of the configuration now held by $i$ minus the energy of the configuration now held by $j$.
- The frame around the formula marks it as a main result.
- Other symbols: as in the list above.
</div>

Read it like this. Only two numbers enter: the difference of the inverse temperatures and the difference of the potential energies. Both are already known in a running simulation, so a swap attempt costs almost nothing. No velocities appear and no new forces are needed.

Sanity check: if $i$ is the colder replica ($\beta_i>\beta_j$) and currently holds the configuration of higher energy ($U(\mathbf x)>U(\mathbf x')$), the exponent is positive and the swap is always accepted. The low-energy configuration moves to the cold replica, as it should. In the opposite case, where the cold replica already holds the configuration of lower energy, the exponent is negative and the swap is accepted only some of the time.

A numerical example: replica $i$ runs at 300 K and replica $j$ at 310 K, so $\beta_i = 0.4009$ mol/kJ, $\beta_j = 0.3880$ mol/kJ and $\beta_i-\beta_j = 0.0129$ mol/kJ. If the cold replica holds the configuration that is lower in energy by 50 kJ/mol, then $U(\mathbf x)-U(\mathbf x') = -50$ kJ/mol, the exponent is $0.0129\times(-50) = -0.65$ and $P_{acc} = e^{-0.65} = 0.52$. If it is lower by 200 kJ/mol, the exponent is $-2.59$ and $P_{acc} = 0.075$. The wider the energy gap between the two configurations, the smaller the chance of a swap. The number of replicas a system needs follows from this fact.

After an accepted swap, velocities are rescaled by $\sqrt{T_{new}/T_{old}}$. Here $T_{old}$ is the temperature the configuration came from and $T_{new}$ the temperature it now runs at. The reason: the configuration arrives with the velocities of its old temperature, and the kinetic energy is proportional to the square of the velocities and, on average, to the temperature (Module 3). Multiplying every velocity by $\sqrt{T_{new}/T_{old}}$ multiplies the kinetic energy by $T_{new}/T_{old}$, which puts it at the level of the new temperature at once. This rescaling is also why only the potential energy appears in the rule: with it, the kinetic-energy parts of the Boltzmann factors are the same before and after the swap, and they cancel from the ratio.

Each temperature samples its own canonical ensemble exactly, so the lowest-temperature replica gives unbiased averages directly. The **canonical ensemble** (Module 3) is the collection of configurations with Boltzmann probabilities at one fixed temperature, which is what a thermostatted simulation samples. "Exactly" means that the swap rule adds no error of its own. The frames collected at 300 K can be analysed as they are, with no reweighting.

### Replicas, temperatures, and what the hot ones tell you

The output can be sorted in two ways. Sorted by temperature, you get everything that was simulated at, say, 300 K: this is what you analyse. Sorted by replica, you follow one copy of the system as it wanders up and down the ladder: this is what you inspect to see whether the method works. (Exchanging the configurations of two temperatures, or the temperatures of two running copies, is the same move described in two ways.)

The word "replica" is used in both senses in this lesson. In the derivation above, and in "the hot replicas", it means the simulation that runs at one temperature, whichever configuration it holds at the moment. In "sorted by replica" and in the next paragraph it means one continuous copy of the system, which changes its temperature at every accepted swap.

A healthy run shows every replica travelling from the bottom of the ladder to the top and back, many times. A replica that stays in the lower half never benefits from the heat, however good the acceptance looks.

What you may conclude from the hot replicas:

- Each of them is a correct equilibrium simulation of the model at its own temperature. Averages taken at 400 K are averages of the model at 400 K.
- They are a source of new structures for the cold replicas. That is their purpose.
- Their data can be combined with the cold data by MBAR (Module 12), which accepts states that differ in temperature, to reduce the statistical error.

What you may not conclude:

- The populations seen at a high temperature are not the populations at the temperature of interest. A helix that is mostly formed at 300 K can be mostly melted at 450 K. Only the frames collected at 300 K, or a proper reweighting, tell you about 300 K.
- The time order means nothing. After sorting by temperature, the frames at 300 K are pieces of different replicas joined end to end, with a jump at every accepted swap. Sorting by replica does not help, because then the temperature changes along the way. Durations, rates and the order of events are lost.
- Whether the model describes the real molecule well at 450 K is a separate question. The method does not need the hot replicas to be realistic. It only needs them to move.

### How many replicas

The ladder must be fine enough for swaps to be accepted, and every rung costs a full simulation. This part explains why large systems need many rungs. On a first reading the picture of the overlapping bells, the formula and the worked example are enough. The four steps in between show where the formula comes from.

At a given temperature the potential energy of the system is not one number. It fluctuates from frame to frame around a mean value. Make a histogram of it and you get a bell-shaped curve with a centre (the mean energy at that temperature) and a width (the standard deviation, the typical size of the fluctuations). A hotter replica has its bell at higher energy.

Now look at the acceptance rule again. A swap is accepted easily only when the energy of the cold replica's configuration is not far below the energy of the hot replica's configuration. That happens often only if the two bells overlap, so that a typical energy of one replica is also a plausible energy of the other. If the bells are far apart, the gap is large every time, the exponent is large and negative, and nearly every swap is refused.

**How many replicas.** Swaps are accepted only if the potential-energy distributions of neighbouring temperatures overlap. The mean energy grows in proportion to the number of degrees of freedom $N_{df}$ while the width of the distribution grows as $\sqrt{N_{df}}$, so the temperature spacing must shrink as $1/\sqrt{N_{df}}$ and

$$
M\propto\sqrt{N_{df}}\;\ln\frac{T_{max}}{T_{min}} .
$$

<div class="legend" markdown="1">
- $M$: the number of replicas.
- $\propto$: "is proportional to". The formula says how $M$ scales. It does not give the number itself, because the constant in front depends on the acceptance you aim for and on the heat capacity of the system.
- $N_{df}$: the number of **degrees of freedom**, the number of independent ways in which the atoms can move. It is about three per atom, minus the constraints (Module 3).
- $\sqrt{N_{df}}$: its square root. A system with four times as many atoms has twice this value.
- $T_{min}$, $T_{max}$: the lowest and the highest temperature of the ladder.
- $\ln$: the natural logarithm. It grows slowly: for 300 to 450 K, $\ln(450/300) = 0.405$.
</div>

<div class="box maths" markdown="1">
**Maths you need here: mean, standard deviation, and the square-root rule.** The **mean** of a fluctuating quantity is its average value. The **standard deviation** $\sigma$ measures how far single values typically lie from the mean. Its square, $\sigma^2$, is called the variance.

When a quantity is a sum of $N$ independent contributions of similar size, its mean grows in proportion to $N$ and its standard deviation only as $\sqrt N$. Example: toss $N$ coins and count the heads. For $N = 100$ you expect 50, give or take 5 (the standard deviation is $\sqrt N/2$). For $N = 10{,}000$ you expect 5,000, give or take 50. The count grew 100 times and its spread only 10 times.

The energy of a large system behaves in the same way, because it is a sum of contributions from many atoms. More in the [toolbox](maths.html#averages).
</div>

Here is where the two scalings come from, in four steps.

*Step 1, the distance between the bells.* The energy needed to warm the system by one kelvin is its **heat capacity** $C$. (Only the potential energy enters the swap rule, so $C$ here is the part of the heat capacity that comes from the potential energy.) Two replicas whose temperatures differ by $\Delta T$ have mean energies that differ by $C\,\Delta T$. Every degree of freedom takes its share of the heat, so $C$ is proportional to $N_{df}$.

*Step 2, the width of a bell.* The energy is a sum of very many contributions, so by the square-root rule its standard deviation grows as $\sqrt{N_{df}}$. Module 3 gave the exact relation for the total energy, and the same relation holds for the potential energy with its own part of the heat capacity: the variance is $k_BT^2C$. The standard deviation is the square root of that, $\sqrt{k_BT^2C}$.

*Step 3, the ratio.* The overlap is set by the distance between the bells measured in units of their width:

$$
\frac{\text{distance between the means}}{\text{width}} = \frac{C\,\Delta T}{\sqrt{k_BT^2C}} = \sqrt{\frac{C}{k_B}}\;\frac{\Delta T}{T} .
$$

<div class="legend" markdown="1">
- $C$: the heat capacity (potential-energy part), in kJ mol$^{-1}$ K$^{-1}$. It is proportional to $N_{df}$.
- $\Delta T$: the difference between two neighbouring temperatures of the ladder, in K.
- $T$: the temperature of the colder of the two, in K.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $\sqrt{k_BT^2C}$: the standard deviation of the potential energy at temperature $T$.
- $C/k_B$: the heat capacity as a pure number. It is of the order of the number of degrees of freedom.
- The second equality: $C/\sqrt{C} = \sqrt{C}$, and $\sqrt{k_BT^2} = T\sqrt{k_B}$.
</div>

To keep the same overlap when the system grows, this ratio has to stay the same. Since $\sqrt{C/k_B}$ grows as $\sqrt{N_{df}}$, the relative spacing $\Delta T/T$ has to shrink as $1/\sqrt{N_{df}}$.

*Step 4, counting the rungs.* If every step multiplies the temperature by the same factor $1+\Delta T/T$, then $n$ steps multiply it by $(1+\Delta T/T)^n$. To reach $T_{max}$ from $T_{min}$ you need $(1+\Delta T/T)^n = T_{max}/T_{min}$. Take the logarithm of both sides and use $\ln(1+x)\approx x$ for small $x$: $n\approx\ln(T_{max}/T_{min})\,/\,(\Delta T/T)$. With $\Delta T/T$ proportional to $1/\sqrt{N_{df}}$, the number of steps, and so the number of replicas $M = n+1$, is proportional to $\sqrt{N_{df}}\,\ln(T_{max}/T_{min})$. That is the formula above.

<details markdown="1"><summary>Optional: from the overlap to an acceptance percentage</summary>
The ratio of step 3 can be turned into a number. Assume that the two energy distributions are Gaussian bells of the same width $\sigma$, with centres a distance $d$ apart, and that $d$ and $\sigma$ are related as in steps 1 and 2. Averaging the acceptance rule over the two bells is a Gaussian integral. Its result is

$$
\text{average acceptance} = \operatorname{erfc}\left(\frac{d}{2\sigma}\right),
$$

where erfc is the complementary error function: $\operatorname{erfc}(z)$ is the probability that a Gaussian number lies further than $z\sqrt2$ standard deviations from its mean, on either side ([toolbox](maths.html#gaussian)). It is 1 at $z = 0$ and falls quickly. Some values:

| $d/\sigma$ | 0.5 | 1 | 1.5 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| average acceptance | 72 % | 48 % | 29 % | 16 % | 3.4 % | 0.5 % |

So an acceptance of 20 to 30 % corresponds to bells whose centres are about 1.5 to 1.8 widths apart. The model is rough (real distributions are not exactly Gaussian, and their widths differ a little between neighbours), but it shows how fast the acceptance collapses when the rungs are too far apart.
</details>

<div class="box key" markdown="1">
**Worked example: a ladder for a small system, and for one four times larger.** The numbers are an illustration. Take $N_{df} = 10{,}000$ and suppose the potential-energy part of the heat capacity is $\tfrac12k_B$ per degree of freedom, the value for a collection of springs (real liquids differ). Then $C/k_B = 5{,}000$ and $\sqrt{C/k_B} = 70.7$.

1. *Choose the overlap.* Aim for a ratio of 1.5 in step 3, which the optional block above translates into an acceptance near 29 %.
2. *Spacing.* $\Delta T/T = 1.5/70.7 = 0.021$: each rung is 2.1 % hotter than the one below, which is 6.4 K at 300 K.
3. *Number of rungs from 300 to 400 K.* $n = \ln(400/300)/\ln(1.021) = 0.288/0.021 = 13.7$, so 14 steps and 15 replicas.

Now make the system four times larger, $N_{df} = 40{,}000$. The spacing halves to 1.06 %, the number of steps doubles to 28, and you need 29 replicas. Each replica also costs four times more to run, so the whole calculation costs about eight times more.
</div>

A geometric ladder, $T_k = T_{min}(T_{max}/T_{min})^{k/(M-1)}$, gives roughly uniform acceptance when the heat capacity is constant; aim for roughly equal acceptance between all neighbouring pairs, commonly 20 to 30 % (the original eight-replica peptide simulation had about 15 %, and its authors considered anything above 10 % sufficient).

<div class="legend" markdown="1">
- $T_k$: the temperature of rung $k$.
- $k$: the label of the rung. In this formula it runs from 0 to $M-1$, so that $T_0 = T_{min}$ and $T_{M-1} = T_{max}$. (The list at the start of the section was numbered from 1 to $M$. Only the numbering differs: with that numbering the same ladder is written $T_k = T_{min}(T_{max}/T_{min})^{(k-1)/(M-1)}$, with $k$ from 1 to $M$.)
- $T_{max}/T_{min}$: the ratio of the highest to the lowest temperature.
- The exponent $k/(M-1)$: the fraction of the ladder that has been climbed at rung $k$, from 0 at the bottom to 1 at the top.
</div>

"Geometric" means that each temperature is the one below it multiplied by the same factor, $(T_{max}/T_{min})^{1/(M-1)}$. For four replicas between 300 and 450 K the factor is $1.5^{1/3} = 1.145$ and the ladder is 300, 343, 393 and 450 K. The gaps grow (43, 50 and 57 K) while the ratio stays the same.

Step 3 shows why this is the natural choice: the overlap depends on $\Delta T/T$, the relative spacing, and on $C$. "When the heat capacity is constant" means when $C$ is the same at all temperatures of the ladder. Where $C$ is larger, the same step also shows that the rungs must be closer.

The reason for aiming at equal acceptance: a structure travels along the ladder by a chain of accepted swaps, and the pair with the lowest acceptance is the bottleneck of the whole chain. The usual target is a compromise. With a much lower acceptance the structures hardly travel. With a much higher one the rungs are closer than they need to be, and replicas are spent for nothing.

A small protein in explicit water (30,000 atoms) spanning 300 to 450 K needs of the order of 50 to 60 replicas, most of the effort going into heating water. That cost motivates the next method.

"Explicit water" means that the water molecules are simulated atom by atom. They are counted in $N_{df}$ like any other atoms, so the ladder is set by the water although the barriers you care about are in the protein. The estimate of the worked example, applied to a system of this size, gives a number of the same order. Exercise 3 asks you to do it.

**REST2** (replica exchange with solute tempering; [Wang, Friesner and Berne 2011](cite:wang2011)). The idea in words: the protein or peptide (the **solute**) is what is stuck, and the water around it is not. So heat the solute only. Two parts of one box cannot stay at two temperatures at equilibrium, because heat flows from the hot part to the cold one, but there is another way to the same effect. The Boltzmann factor contains only the product $\beta U = U/k_BT$. Dividing an energy by 2 changes this product exactly as doubling the temperature would.

All replicas run at the same temperature $T_0$, but the potential energy is scaled so that only the solute is effectively heated:

$$
U_m = \lambda_m\,U_{pp}+\sqrt{\lambda_m}\,U_{pw}+U_{ww},\qquad\lambda_m = \frac{T_0}{T_m}\le1,
$$

with solute-solute (pp), solute-water (pw) and water-water (ww) terms.

<div class="legend" markdown="1">
- $U_m$: the potential-energy function used by replica $m$.
- $m$: the label of the replica.
- $U_{pp}$: the solute-solute energy, all interactions among the atoms of the solute (p for protein).
- $U_{pw}$: the solute-water energy, all interactions between a solute atom and a water atom.
- $U_{ww}$: the water-water energy.
- $\lambda_m$: the scaling factor of replica $m$, a pure number between 0 and 1. The replica with $\lambda_m = 1$ is the real system. This is not the alchemical $\lambda$ of Module 13.
- $\sqrt{\lambda_m}$: its square root, the factor applied to the solute-water energy.
- $T_0$: the real temperature of every replica, the one the thermostat holds.
- $T_m$: the effective temperature of the solute in replica $m$. It is a label that you choose to fix $\lambda_m$. No thermostat is set to it.
- $\le$: "smaller than or equal to".
</div>

Read it like this, for $T_0 = 300$ K and $T_m = 600$ K, so $\lambda_m = 0.5$. The solute-solute energy is halved. Its Boltzmann factor is $e^{-\beta_0\lambda_mU_{pp}} = e^{-U_{pp}/k_BT_m}$ with $\beta_0 = 1/k_BT_0$, the same as for the unscaled energy at 600 K. The solute-water energy is multiplied by $\sqrt{0.5} = 0.71$, which corresponds to an intermediate temperature of $\sqrt{T_0T_m} = 424$ K. The water-water energy is untouched and stays at 300 K.

The solute sees an effective temperature $T_m$ while the water stays cold. The water-water energy cancels from the exchange criterion, leaving only the solute-solute and solute-water energies, so the number of replicas grows with the number of degrees of freedom of the solute, not with the number of water molecules. A handful to a dozen replicas suffice for peptides and small proteins. The cancellation is shown below, after the general exchange rule. The saving follows from the square-root argument: the energies that enter the swap test now belong to the solute and its contacts with water, and no longer to the whole box.

In practice only the solute's dihedral terms, charges and Lennard-Jones well depths are scaled: scaling its bonds and angles does not help ([Wang, Friesner and Berne 2011](cite:wang2011)). These are the force-field terms of Module 5.

The charge scaling shows where the square root in the formula comes from. An electrostatic energy is proportional to the product of two charges. Multiply every solute charge by $\sqrt{\lambda_m}$: a pair of solute atoms then has its energy multiplied by $\sqrt{\lambda_m}\times\sqrt{\lambda_m} = \lambda_m$, and a solute-water pair by $\sqrt{\lambda_m}$ only, because the water charge is unchanged. The Lennard-Jones well depths behave in the same way under the combination rule of Module 5, in which the well depth of a pair of atoms $i$ and $j$ is $\sqrt{\varepsilon_i\varepsilon_j}$, when the well depth $\varepsilon_i$ of each solute atom is multiplied by $\lambda_m$.

Temperature is only one way to make replicas differ. The general idea is to give each replica a slightly different energy function and to exchange configurations between neighbours. The Hamiltonian (Module 2) is the function that gives the total energy, which explains the name of the general method. REST2 is one case of it.

**Hamiltonian replica exchange.** In general the replicas can differ in any parameter of the Hamiltonian: the $\lambda$ of an alchemical transformation, or the centre of an umbrella window. (An alchemical $\lambda$ is the parameter of Module 13 that gradually turns one molecule into another. An umbrella window is one of the simulations of Module 12, in which a spring holds a coordinate near a chosen centre.)

The rule is derived as before. Let every replica have the same temperature and the energy function $U+w_i$, where $w_i$ is the extra term of replica $i$. Before the swap the joint probability is proportional to $e^{-\beta[U(\mathbf x_i)+w_i(\mathbf x_i)]}\,e^{-\beta[U(\mathbf x_j)+w_j(\mathbf x_j)]}$. After the swap, replica $i$ holds $\mathbf x_j$ and replica $j$ holds $\mathbf x_i$, and it is proportional to $e^{-\beta[U(\mathbf x_j)+w_i(\mathbf x_j)]}\,e^{-\beta[U(\mathbf x_i)+w_j(\mathbf x_i)]}$.

Divide the second by the first. The common energy $U(\mathbf x_i)+U(\mathbf x_j)$ appears in both and cancels, and only the extra terms remain. For two replicas with bias potentials $w_i$ and $w_j$ at the same temperature, holding $\mathbf x_i$ and $\mathbf x_j$:

$$
P_{acc} = \min\Big\{1,\ \exp\big(-\beta\big[w_i(\mathbf x_j)+w_j(\mathbf x_i)-w_i(\mathbf x_i)-w_j(\mathbf x_j)\big]\big)\Big\} .
$$

<div class="legend" markdown="1">
- $P_{acc}$: the probability of accepting the swap.
- $\beta$: $1/k_BT$, the same for both replicas.
- $w_i$, $w_j$: the **bias potentials** of replicas $i$ and $j$, the extra energy terms that make each replica different from the others. For umbrella windows, $w_i = \tfrac12k(\xi-\xi_i)^2$, a spring of stiffness $k$ that holds the coordinate $\xi$ near the centre $\xi_i$. (This $w$ is not the hill height of metadynamics.)
- $\mathbf x_i$, $\mathbf x_j$: the configurations held by replica $i$ and by replica $j$ before the swap.
- $w_i(\mathbf x_j)$: the bias of replica $i$ evaluated on the configuration of replica $j$: the extra energy replica $i$ would have if it received that configuration.
- $\min\{1,\ \dots\}$: the smaller of 1 and the number that follows.
</div>

The bracket is the energy after the swap minus the energy before. If the swap lowers the total bias energy, it is always accepted. If it raises it, it is accepted with the Boltzmann factor of the increase.

A numerical example with two umbrella windows at 300 K. Both springs have $k = 1{,}000$ kJ mol$^{-1}$ nm$^{-2}$, with centres at 1.00 and 1.05 nm. Replica $i$ holds a configuration with $\xi = 1.01$ nm and replica $j$ one with $\xi = 1.04$ nm.

Before the swap the bias energies are $500\times0.01^2 = 0.05$ kJ/mol each. After it, each configuration sits 0.04 nm from its new centre and costs $500\times0.04^2 = 0.8$ kJ/mol. The bracket is $0.8+0.8-0.05-0.05 = 1.5$ kJ/mol, so $P_{acc} = e^{-1.5/2.494} = 0.55$. Windows whose centres are much further apart than the width of their distributions would almost never exchange.

Back to REST2, where two replicas $m$ and $n$ differ in the whole energy function, $U_m$ against $U_n$. The same derivation gives the same bracket with $U_m$ and $U_n$ in the places of $w_i$ and $w_j$: energy after the swap minus energy before. The water-water energy $U_{ww}$ enters $U_m$ and $U_n$ with the same factor 1. In the bracket it therefore appears once with a plus sign and once with a minus sign for each of the two configurations, and drops out. Only the terms that are scaled differently in the two replicas remain, the solute-solute and the solute-water energies, which is the cancellation stated above.

Exchanges between umbrella windows let a configuration diffuse along the reaction coordinate and help the orthogonal degrees of freedom to relax, which reduces the hysteresis problem of Module 12 at no extra cost. "Diffuse along the reaction coordinate" means that, through a chain of accepted swaps, a configuration can travel from window to window instead of staying where it was started. A configuration that is stuck in a bad arrangement of the other coordinates can then be replaced by a better one from a neighbouring window. "At no extra cost" holds because the windows have to be run anyway, and the swap test needs only bias energies.

A limit to remember: tempering helps with *enthalpic* barriers. A barrier that is entropic, a narrow path that must be found, is not lowered by heating.

<div class="box physics" markdown="1">
**Physics you need here: enthalpic and entropic barriers.** A free energy has two parts, $F = E - TS$ (Module 3): the energy $E$ and the entropy $S$, which counts how many configurations are available. A barrier can be high for either reason. (Enthalpy is the energy plus a pressure-volume term that is negligible for a liquid at 1 bar, so "enthalpic" can be read as "energetic" here.)

A barrier is **enthalpic** when the system must pay energy to pass, for example by breaking hydrogen bonds. The chance of having that energy is $e^{-\Delta E^\ddagger/k_BT}$, where $\Delta E^\ddagger$ is the energy needed, and it rises steeply with temperature. For $\Delta E^\ddagger = 40$ kJ/mol it is $e^{-16.0}$ at 300 K and $e^{-10.7}$ at 450 K, about 200 times larger.

A barrier is **entropic** when no energy is needed but the way through is narrow: of all the configurations in the basin, only a tiny fraction lies at the entrance of the path. The chance of being there is a ratio of two counts of configurations, and a ratio of counts does not depend on the temperature. If one configuration in nine million is at the entrance, that is so at 300 K and at 450 K. Think of a large hall with one small door: the share of the floor that lies in front of the door does not change when the people inside move faster. More in the [primer](physics.html#thermodynamics).
</div>

## Metadynamics

<div data-videos="QP5F83g1G0E b8aViZKaKFs bZZggbV2r5E BYvsNThvXlk"></div>

This is the second cure: change the terrain. Umbrella sampling (Module 12) also adds a bias, but there you decide in advance where the springs go. Metadynamics builds its bias while it runs, out of the history of the run. Wherever the system has been, a little extra energy is left behind, so that the system is pushed to go somewhere new.

One picture carries the idea. A walker in a valley drops a shovel of sand at their feet at regular intervals. The floor rises where the walker spends time. In the end the valleys are full, the walker roams everywhere, and the amount of sand at each place tells you how deep the valley was there.

The picture needs one correction. The sand is not dropped in real space. It is dropped along the collective variable $s$, so the bias is a function of $s$ alone, and the "walker" is the whole system.

<div class="box maths" markdown="1">
**Maths you need here: the Gaussian as a bump.** The function

$$
g(s) = w\,\exp\left(-\frac{(s-s_c)^2}{2\sigma^2}\right)
$$

is a smooth bump centred at $s = s_c$. Its **height** is $w$: that is its value at the centre, where the exponent is zero and $\exp(0) = 1$. Its **width** is $\sigma$. One $\sigma$ away from the centre the bump has fallen to $e^{-1/2} = 0.61$ of its height, two $\sigma$ away to $e^{-2} = 0.14$, and three $\sigma$ away to $e^{-4.5} = 0.011$.

The same function describes the normal distribution of statistics. Here it is used only as a shape: a small pile with no edges, whose slope, and so the force it produces, is finite everywhere. More in the [toolbox](maths.html#gaussian).
</div>

[Laio and Parrinello (2002)](cite:laio2002) introduced the idea of a history-dependent bias made of Gaussians (in their paper it acts on a coarse-grained dynamics of the CVs driven by mean forces). In the form used today the bias is added directly to an MD run. Instead of fixing the bias in advance, build it during the run: at regular intervals deposit a small Gaussian hill at the current value of the CVs:

$$
V(s,t) = \sum_{t'<t}w\,\exp\left(-\frac{\big(s-s(t')\big)^2}{2\sigma^2}\right).
$$

<div class="legend" markdown="1">
- $V(s,t)$: the **bias potential**: the extra energy that is added, at time $t$, to any configuration whose CV has the value $s$. Its unit is kJ/mol. In this section $V$ is the bias, not the potential energy of the system, which is $U$.
- $s$: the value of the collective variable at which you ask for the bias. With two CVs, $s$ stands for the pair of values and each hill is a bump in two dimensions.
- $t$: the present simulation time.
- $t'$: an earlier time at which a hill was deposited. Hills are deposited at a fixed interval, the **deposition stride** (written $\tau_G$ in this lesson), so $t' = \tau_G, 2\tau_G, 3\tau_G, \dots$ The stride does not appear as a letter in the formula. It is hidden in the list of times.
- $\sum_{t'<t}$: the sum over all hills deposited before the present time.
- $s(t')$: the value the CV had at the time $t'$. It is the centre of that hill.
- $w$: the **height** of each hill, in kJ/mol.
- $\sigma$: the **width** of each hill, in the unit of the CV (nm for a distance, radians for an angle).
- $\exp(\dots)$: the Gaussian bump of the box above, with centre $s(t')$.
</div>

"History-dependent" means that the bias at any moment depends on where the system has been before. A "mean force" is a force averaged over all the other coordinates. It returns below, in the adaptive biasing force.

Read the formula like this. With a hill every 1 ps, the sum has 1,000 terms after 1 ns. To get the bias at some value $s$, go through all the hills and add up what each one contributes at $s$. Hills whose centres lie within a few $\sigma$ of $s$ count, and the others contribute almost nothing. Three numbers are yours to choose: the height $w$, the width $\sigma$ and the stride $\tau_G$.

The simulation runs on the total energy $U+V$. The bias reaches the atoms through the [chain rule](maths.html#chain-rule): the extra force on atom $i$ is $-(\partial V/\partial s)\,\nabla_i s$. The first factor is the slope of the pile along $s$, and $\nabla_i s$ is the [gradient](maths.html#gradient) of the CV with respect to the position of atom $i$ (Module 2), which says how moving that atom changes $s$. The force points down the slope of the pile, away from where hills have accumulated.

The accumulated hills push the system away from where it has already been. Wells are filled, the system spills over the lowest barrier into the next well, and eventually the whole landscape along $s$ is flat. At that point the bias is the negative of the free energy, $V(s,t\to\infty)\approx-F(s)+C$. In this short formula, $t\to\infty$ means "after a very long run", $F(s)$ is the free energy along the CV as defined in the first section, and $C$ is a constant, the same for all $s$, that drops out of every free-energy difference.

### Why the bias ends up as minus the free energy

The statement follows from three observations.

1. *What the system feels.* Along $s$, the unbiased system moves on the free energy $F(s)$. With the bias it moves on $F(s)+V(s,t)$. If the bias changes slowly, the system is found at $s$ with a probability proportional to $e^{-\beta[F(s)+V(s,t)]}$: most often where $F+V$ is lowest.
2. *Where the hills go.* Hills are dropped where the system is. So the bias grows fastest where $F+V$ is lowest. The lowest places are raised first, which is a self-correcting process: any dip in $F+V$ attracts the system and is filled.
3. *When it stops changing shape.* Once $F+V$ has the same value everywhere, the system visits all values of $s$ equally often, hills fall evenly, and $V$ rises by the same amount everywhere. The sum $F+V$ stays flat.

A flat sum means $F(s)+V(s,t) = \text{constant}$, which is $V = -F+C$. The constant keeps growing as hills are added, and constants do not matter. The argument also shows why the result is a *free* energy. Hills are placed according to how often the system is at each $s$, and "how often" already counts all the other coordinates, which is how $F(s)$ was defined.

In this original form the bias never converges: hills keep being added and $V$ fluctuates around $-F$ with an error that grows with the rate at which bias is deposited (as the square root of the hill height divided by the deposition interval). In the notation above, the rate of deposition is $w/\tau_G$, an energy per unit of time, and the error grows as $\sqrt{w/\tau_G}$. This is a trade. Large or frequent hills fill the wells quickly and leave a rough bias. Hills four times smaller take four times longer to fill the same well and halve the error, because $\sqrt{1/4} = 1/2$.

**Well-tempered metadynamics** ([Barducci, Bussi and Parrinello 2008](cite:barducci2008)) lets the hill height decrease where bias has already accumulated:

$$
w(t') = w_0\,\exp\left(-\frac{V\big(s(t'),t'\big)}{k_B\,\Delta T}\right),
\qquad
V(s,t\to\infty) = -\frac{\Delta T}{T+\Delta T}\,F(s)+C .
$$

<div class="legend" markdown="1">
- $w(t')$: the height of the hill deposited at time $t'$. It is no longer the same for all hills.
- $w_0$: the **initial hill height**: the height of a hill that lands where there is no bias yet.
- $V\big(s(t'),t'\big)$: the bias that is already present, at the time $t'$, at the place where the system is and where the new hill will land.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $\Delta T$: a parameter with the unit of temperature, chosen by you. It sets the energy scale $k_B\,\Delta T$ on which the hills shrink. It is not a gap between two temperatures and no thermostat is set to it.
- $T$: the temperature of the simulation, the one the thermostat holds.
- $F(s)$: the free energy along the CV.
- $\dfrac{\Delta T}{T+\Delta T}$: a number between 0 and 1: the fraction of the free energy that the bias compensates in the end.
- $t\to\infty$: after a very long run.
- $C$: a number that is the same for all $s$ but not fixed in time. It keeps rising as hills are added, ever more slowly (roughly as the logarithm of the time). What converges is the shape of the bias: the differences of $V$ between values of $s$.
</div>

Read the first formula like this. Where there is no bias yet, the exponent is zero and the hill has its full height $w_0$. Where the bias has reached $k_B\,\Delta T$, new hills have shrunk to $e^{-1} = 0.37$ of $w_0$. An example at 300 K with $w_0 = 1$ kJ/mol and $\Delta T = 2{,}700$ K, so that $k_B\,\Delta T = 22.4$ kJ/mol: where 10 kJ/mol of bias has accumulated the next hill is 0.64 kJ/mol high, at 20 kJ/mol it is 0.41, and at 45 kJ/mol it is 0.13. The bias keeps growing, but ever more slowly, so it settles instead of fluctuating.

The second formula says where it settles: at a fixed fraction of $-F$. In the example the fraction is $2{,}700/3{,}000 = 0.9$. (In the notation introduced below, this example has the bias factor $\gamma = 10$.)

### Where the fraction comes from

The argument is the one used above, with one new ingredient: the height of a hill now depends on the place. At a given $s$ the bias grows at a rate equal to the height of a new hill there, times how often the system is there to receive one:

$$
\text{growth rate of the bias at }s\ \propto\ \underbrace{e^{-V(s,t)/k_B\Delta T}}_{\text{height of a new hill}}\times\underbrace{e^{-[F(s)+V(s,t)]/k_BT}}_{\text{how often the system is at }s} .
$$

<div class="legend" markdown="1">
- $\propto$: "is proportional to". The constant factors $w_0$ and $1/\tau_G$ are left out because they are the same at every $s$.
- The first factor: the hill-height rule of the well-tempered formula.
- The second factor: the Boltzmann probability of finding the system at $s$ when it moves on $F+V$ at the temperature $T$.
- The braces underneath only attach the two descriptions. They are not part of the formula.
- Other symbols: as in the list above.
</div>

The shape of the bias stops changing when it grows at the same rate at every $s$, that is, when the product on the right no longer depends on $s$. Three lines of algebra turn this condition into the result:

$$
\begin{aligned}
-\frac{V(s)}{k_B\,\Delta T}-\frac{F(s)+V(s)}{k_BT} &= \text{constant}\\
V(s)\left(\frac{1}{\Delta T}+\frac{1}{T}\right) &= -\frac{F(s)}{T}+\text{constant}\\
V(s) &= -\frac{\Delta T}{T+\Delta T}\,F(s)+C .
\end{aligned}
$$

<div class="legend" markdown="1">
- $V(s)$: the bias at the end of a long run, written without the time.
- "constant": any number that is the same for all values of $s$. It changes from line to line and is called $C$ in the last one.
- Other symbols: as in the lists above.
</div>

Line 1 takes the logarithm of the product: the logarithm of a product is the sum of the logarithms, and the logarithm of an exponential is its exponent. Line 2 multiplies both sides by $-k_B$, collects the two terms that contain $V$, and moves the term with $F$ to the right. Line 3 uses $1/\Delta T+1/T = (T+\Delta T)/(T\,\Delta T)$ and divides both sides by it. As before the process corrects itself: where the product is larger than elsewhere, the bias grows faster, and that lowers the product there.

The bias converges smoothly to a fraction of $-F$, and the CVs are sampled as if at the higher temperature $T+\Delta T$. The second half of the sentence follows from the first. What the system feels along $s$ at the end is $F+V = F-\frac{\Delta T}{T+\Delta T}F = \frac{T}{T+\Delta T}F$. Its Boltzmann factor at the real temperature is $e^{-\frac{T}{T+\Delta T}F/k_BT} = e^{-F/k_B(T+\Delta T)}$, which is the Boltzmann factor of the full $F$ at the temperature $T+\Delta T$. Only the CVs are "hot" in this sense: all other coordinates stay at $T$, which is the difference from replica exchange, where everything is heated.

The **bias factor** $\gamma=(T+\Delta T)/T$ is the main parameter: $\gamma=1$ is unbiased MD, $\gamma\to\infty$ is standard metadynamics, and typical values are 5 to 20, chosen so that the highest relevant barrier divided by $\gamma$ is a few $k_BT$. The free energy is $F(s)=-\frac{\gamma}{\gamma-1}V(s)$, and other observables can be recovered by reweighting each frame with $e^{\beta[V(s,t)-c(t)]}$.

<div class="legend" markdown="1">
- $\gamma$: the **bias factor**, a pure number of 1 or more. It is the ratio of the temperature at which the CVs appear to be sampled to the real temperature. (In Modules 8 and 16 the same letter is a friction.)
- $T$, $\Delta T$: the real temperature and the well-tempered parameter, as above.
- $\gamma\to\infty$: the limit of a very large bias factor.
- $V(s)$: the bias at the end of the run.
- $\beta$: $1/k_BT$ at the real temperature.
- $V(s,t)$: the bias that a frame saved at time $t$, with CV value $s$, was feeling.
- $c(t)$: an energy that depends on the time and not on the configuration. It is explained below.
</div>

The three statements about $\gamma$ can be checked one by one. With $\gamma = 1$, $\Delta T = 0$, and the converged bias $-\frac{\Delta T}{T+\Delta T}F$ is zero: no bias, plain MD. With $\gamma\to\infty$, $\Delta T\to\infty$: the exponent of the hill-height rule is zero, every hill has the height $w_0$, and you are back to the original method. In between, the system moves on $F/\gamma$: every barrier along $s$ is divided by $\gamma$. For a barrier of 50 kJ/mol at 300 K:

| Bias factor $\gamma$ | Fraction of $F$ compensated, $(\gamma-1)/\gamma$ | The 50 kJ/mol barrier becomes |
|---|---|---|
| 5 | 0.80 | 10 kJ/mol, or 4.0 $k_BT$ |
| 10 | 0.90 | 5 kJ/mol, or 2.0 $k_BT$ |
| 20 | 0.95 | 2.5 kJ/mol, or 1.0 $k_BT$ |

The formula for the free energy is the converged bias turned around. The fraction $\Delta T/(T+\Delta T)$ equals $1-T/(T+\Delta T) = 1-1/\gamma = (\gamma-1)/\gamma$. So $V = -\frac{\gamma-1}{\gamma}F$, and dividing by the fraction gives $F = -\frac{\gamma}{\gamma-1}V$. With $\gamma = 10$, the free energy is the bias times $-10/9$.

**Reweighting** is the tool of the maths box in the first section, applied to a bias that changes in time. A frame saved at time $t$ carried the bias energy $V(s,t)$, so its weight contains $e^{\beta V(s,t)}$. The term $c(t)$ is needed because the bias as a whole keeps rising during the run. Without it, late frames would receive larger weights than early ones for no physical reason. With these weights you can compute the average of any quantity, and the free energy along a coordinate that was not biased.

<details markdown="1"><summary>Optional: where the offset c(t) comes from</summary>
At time $t$ the system moves on the energy $U+V(s,t)$. If the bias changes slowly, the configurations at that time have the probabilities $e^{-\beta[U+V(s,t)]}/Z_V(t)$. Here $Z_V(t)$ is the normalisation: the sum of $e^{-\beta[U+V]}$ over all configurations, which makes the probabilities add up to 1. In the unbiased system the probabilities are $e^{-\beta U}/Z_0$, with $Z_0$ the sum of $e^{-\beta U}$ over all configurations. The weight that converts a biased frame into an unbiased one is the ratio of the two probabilities:

$$
\frac{e^{-\beta U}/Z_0}{e^{-\beta[U+V(s,t)]}/Z_V(t)} = e^{\beta V(s,t)}\,\frac{Z_V(t)}{Z_0} = e^{\beta[V(s,t)-c(t)]},
\qquad
c(t) = -k_BT\ln\frac{Z_V(t)}{Z_0} .
$$

The first equality cancels $e^{-\beta U}$. The second writes the ratio of the two normalisations as an exponential, which defines $c(t)$. Both sums can be done along the CV alone, because the bias depends on the configuration only through $s$: $Z_0$ is proportional to $\int e^{-\beta F(s)}\,ds$ and $Z_V(t)$ to $\int e^{-\beta[F(s)+V(s,t)]}\,ds$, with the same constant in front. So $c(t)$ can be computed from the free-energy estimate and the bias. A check: if the bias were the same number $V_0$ at every $s$, then $Z_V = e^{-\beta V_0}Z_0$, $c = V_0$, and every weight would be 1: a uniform bias changes nothing, as it should.
</details>

Practical choices: the Gaussian width $\sigma$ should be about the standard deviation of the CV in an unbiased basin; hills every 1 ps or so; initial height around 1 kJ/mol. The reasons are these.

- *Width.* Run a short plain simulation inside one basin and compute the standard deviation of the CV. Hills much wider than that cannot follow the shape of the basin and smear out its features. Hills much narrower need many more depositions to fill the same well and leave a rough surface.
- *Stride.* After a hill has been added, the system needs time to respond to it. Hills that follow each other too closely pile up under a system that has not yet moved.
- *Height.* At 300 K, 1 kJ/mol is 0.4 $k_BT$: each hill is a gentle push, small against the thermal energy.

**Convergence** means the system has gone back and forth between the basins many times and the free-energy difference between them has stopped changing. One crossing each way is not convergence. The first crossing shows only that the first well has been filled far enough for the system to get over the pass. At that moment the second well contains no bias, and nothing is known about its depth. The estimate $F = -\frac{\gamma}{\gamma-1}V$ becomes meaningful when both wells are filled and the system keeps moving between them, so that the bias is topped up evenly on both sides.

A practical check: compute the free-energy difference between the two basins from the bias at regular times during the run, and plot it against time. (The free energy of a basin is obtained by adding up $e^{-\beta F(s)}$ over the values of $s$ that belong to it and taking $-k_BT\ln$ of the sum, as for the macrostates of Module 3.) In a converged run the curve settles around a constant value.

Variants: multiple walkers (several simulations sharing one bias), bias-exchange and parallel-tempering metadynamics, and on-the-fly probability enhanced sampling (OPES). The standard implementation is the PLUMED library, which plugs into GROMACS, AMBER, NAMD, LAMMPS and other MD programs (its manual has the current list). In words: bias-exchange runs several replicas that each bias a different CV and exchange configurations. Parallel-tempering metadynamics runs metadynamics inside the replicas of a temperature ladder. OPES, as its name says, builds the bias from an estimate of the probability distribution of the CVs that is updated during the run.

**Adaptive biasing force** ([Darve and Pohorille 2001](cite:darve2001)) is the force-based relative: accumulate a running estimate of the mean force $-dF/ds$ in bins along the CV, and apply its negative. Once the estimate is good the system diffuses freely along $s$, and $F$ is the integral of the estimated mean force. The quantity averaged in each bin is the instantaneous force along the coordinate plus a geometric (Jacobian) correction. The 2001 paper derives this formula; the adaptive algorithm itself appeared in a later paper by the same authors.

Unpacked, this says the following.

- The **mean force** $-dF/ds$ is the slope of the free energy along $s$ with a minus sign. It is the average force that pushes the system along $s$ when the CV has that value (Module 3). Metadynamics estimates $F$ by piling up energy. This method estimates the slope of $F$ by averaging forces.
- *Bins* are small intervals into which the range of $s$ is divided. Each bin keeps its own running average.
- *Apply its negative*: add a force that is equal and opposite to the average. Along $s$ the system then feels no net force on average. It wanders back and forth as on flat ground, which is what "diffuses freely" means.
- *$F$ is the integral*: the free energy is recovered by adding up slope times bin width from one end of the range, $F(s) = F(s_0)-\int_{s_0}^{s}(\text{mean force})\,ds'$, where $s_0$ is the starting end and $s'$ runs from $s_0$ to $s$ ([toolbox](maths.html#integral)). Example: a mean force of $-20$ kJ mol$^{-1}$ nm$^{-1}$ over a stretch of 0.1 nm raises $F$ by $20\times0.1 = 2$ kJ/mol.
- The *Jacobian correction* is a geometric term. Module 12 met it for a distance: there is more room at larger separation, which produces an apparent outward push that is not caused by any interaction. It has to be included for the integral to give the free energy.

The demo below runs well-tempered metadynamics on one particle in a double well, with energies in units of $k_BT$. Its sliders are the quantities defined in this section: the barrier height, the bias factor $\gamma$, the initial hill height $w_0$ and the hill width $\sigma$. It draws the exact energy, the estimate $-\frac{\gamma}{\gamma-1}V$ read from the bias, and the sum of energy and bias that the particle feels at that moment.

<div class="widget" data-widget="metad"></div>

## Steered MD

<div data-videos="RJMQ70K8UmA"></div>

This is the roughest way to change the terrain: do not wait for the system to find the pass, drag it over. Steered MD ties one end of an imaginary spring to a collective variable, for example the distance between a ligand and its pocket, and moves the other end at a steady speed. The system follows, as a sledge follows a rope.

Attach a harmonic spring to a CV and move its centre at constant speed $v$:

$$
U_{pull}(t) = \tfrac12k\big[s(\mathbf r)-s_0-vt\big]^2 .
$$

<div class="legend" markdown="1">
- $U_{pull}(t)$: the energy of the spring at time $t$, in kJ/mol. It is added to the potential energy of the system.
- $k$: the **spring constant**, the stiffness of the spring, in kJ mol$^{-1}$ nm$^{-2}$ when the CV is a distance. In this section $k$ is not a rate.
- $s(\mathbf r)$: the present value of the collective variable.
- $s_0$: the position of the centre of the spring at $t = 0$, usually the value of the CV in the starting structure.
- $v$: the **pulling speed**, in nm/ps or nm/ns.
- $t$: the time since the pulling started.
- $s_0+vt$: where the centre of the spring is at time $t$.
- $\tfrac12k[\dots]^2$: the energy of a spring stretched by the amount in the brackets (Module 2, [primer](physics.html#oscillator)). "Harmonic" is the name for this quadratic form.
</div>

Read it like this. The centre of the spring moves ahead at the speed $v$ whatever the system does. When the CV lags behind the centre, the spring is stretched and pulls the system forward with the force $F_{pull} = k\,[s_0+vt-s(\mathbf r)]$, the stiffness times the lag. A stiff spring keeps the CV close to its centre. A soft one lets the CV fall behind and then jump.

Example: with $k = 1{,}000$ kJ mol$^{-1}$ nm$^{-2}$ and a lag of 0.05 nm, the force is $1{,}000\times0.05 = 50$ kJ mol$^{-1}$ nm$^{-1}$ (83 pN, since 1 kJ mol$^{-1}$ nm$^{-1}$ is 1.66 pN) and the spring stores $\tfrac12\times1{,}000\times0.05^2 = 1.25$ kJ/mol.

This imitates an atomic-force-microscope or optical-tweezer experiment, at pulling speeds millions of times faster (0.1 to 10 nm/ns against micrometres per second). It is used to explore unbinding and unfolding pathways, to generate starting structures for umbrella windows, and to compare forces between related systems.

In those experiments a single molecule is held between a surface and a fine lever, or between beads held by laser light, and is stretched while the force is recorded. For the comparison of speeds, 1 nm/ns is 1 m/s, so the simulation pulls at 0.1 to 10 m/s and the experiment at about $10^{-6}$ m/s.

Getting a free energy from it uses Jarzynski's equality (Module 13) with the accumulated work $W=\int F_{pull}\,v\,dt$. At practical speeds the process is far from equilibrium and most of the work is dissipated, so the exponential average does not converge. Rupture forces and work values depend on the pulling speed (in force spectroscopy the rupture force rises roughly linearly with the logarithm of the loading rate), and comparisons are only meaningful at equal speed and spring constant.

<div class="legend" markdown="1">
- $W$: the **work** done on the system by the moving spring during one pull, in kJ/mol. (Not the potential of mean force of Module 12.)
- $F_{pull}$: the force of the spring on the system at each instant, as given above.
- $v\,dt$: the small distance the centre of the spring moves in the short time $dt$.
- $\int\dots dt$: the sum of force times distance over all the short time intervals of the pull ([toolbox](maths.html#integral)).
</div>

Each sentence of that paragraph packs an idea.

*Jarzynski's equality.* Repeat the pull many times from different equilibrium starting structures and record the work $W$ of each. Module 13 gave the exact relation $\langle e^{-\beta W}\rangle = e^{-\beta\Delta F}$. Here $\langle\ \rangle$ is the average over the repeated pulls and $\Delta F$ is the free-energy difference between the end and the start of the pull (Module 13 wrote it $\Delta A$).

*Dissipated work.* Pull infinitely slowly and the work equals $\Delta F$. Pull fast and you spend more, because the system is dragged through the water before it can adjust, and the extra work turns into heat. That extra part is the dissipated work. It is the molecular version of stirring honey quickly.

*The exponential average does not converge.* The average of $e^{-\beta W}$ is dominated by the pulls with unusually small work, and those are rare. For work values with a bell-shaped (Gaussian) distribution of standard deviation $\sigma_W$, the pulls that carry the average lie $\sigma_W/k_BT$ standard deviations below the mean work. With $\sigma_W = 3\,k_BT$ that is 3 standard deviations, about one pull in 740. With $\sigma_W = 5\,k_BT$ it is one pull in 3.5 million. When most of the work is dissipated the spread is large, and the pulls that matter do not occur in any sample you can afford.

*Rupture force and loading rate.* The rupture force is the peak force at which the complex gives way. The loading rate is how fast the applied force grows, the spring constant times the pulling speed, $kv$. Both the rupture force and the work depend on how fast you pull, so two systems can be compared only when they were pulled in the same way.

## Accelerated MD

<div data-videos="cc_5q6Od6XU f4faPQU58oA SbtqjZk80Qc"></div>

This method changes the terrain without a map. No collective variable is chosen. The rule looks only at the potential energy of the present configuration: if it is low, the system is probably deep in some well, and the energy is raised by an amount that is larger the deeper the system sits.

[Hamelberg, Mongan and McCammon (2004)](cite:hamelberg2004). Raise the bottoms of all wells without choosing CVs. When the potential energy $V$ is below a threshold $E$, add a boost:

$$
\Delta V(\mathbf r) = \frac{\big(E-V(\mathbf r)\big)^2}{\alpha+E-V(\mathbf r)}\quad\text{for }V<E,\qquad\Delta V=0\text{ otherwise}.
$$

<div class="legend" markdown="1">
- $V(\mathbf r)$: the potential energy of the configuration $\mathbf r$, or the part of it that is boosted (for example the dihedral terms), in kJ/mol. In this section $V$ is not the bias of metadynamics.
- $\mathbf r$: the positions of all atoms.
- $E$: the **threshold energy**, chosen by you. Configurations whose energy is above $E$ are left alone.
- $\Delta V(\mathbf r)$: the **boost**, the extra energy added to the configuration. It is never negative. The simulation runs on $V+\Delta V$.
- $E-V(\mathbf r)$: how far the configuration lies below the threshold.
- $\alpha$: a tuning parameter with the unit of energy, chosen by you. It sets how strongly the wells are flattened.
- "for $V<E$" and "otherwise": the rule has two cases, below and above the threshold.
</div>

Read it like this, with numbers. Take $\alpha = 20$ kJ/mol. A well bottom that lies 40 kJ/mol below the threshold is raised by $40^2/(20+40) = 26.7$ kJ/mol. A barrier top that lies 10 kJ/mol below the threshold is raised by $10^2/(20+10) = 3.3$ kJ/mol. The barrier between them was 30 kJ/mol and is now $30-26.7+3.3 = 6.7$ kJ/mol.

The parameter $\alpha$ sets the strength. With a large $\alpha$ of 200 kJ/mol the two boosts are 6.7 and 0.5 kJ/mol, and the barrier is still 23.8 kJ/mol. With $\alpha$ close to zero the boost approaches $E-V$, and everything below the threshold is lifted to the threshold itself: a flat plain on which the system has lost all sense of where the wells were. The boost always grows more slowly than the depth below the threshold, so minima stay minima and passes stay passes. Only the differences are compressed.

The wells are raised, so barriers shrink and escapes become faster (the 2004 paper applied the boost to the dihedral terms of small peptides in implicit solvent). Implicit solvent means that the water is represented by a continuous medium and not by molecules (Module 15).

Recovering unbiased averages needs the weights $e^{\beta\Delta V}$, and because $\Delta V$ can be tens to hundreds of $k_BT$ for a solvated protein, those weights are dominated by a few frames: the reweighted result is very noisy. This is reweighting as in the first section, with the boost as the bias. The trouble is the size of the exponent. If the boost of two frames differs by 10 $k_BT$, their weights differ by a factor of $e^{10} = 22{,}000$: one frame counts as much as 22,000 others.

The boost is computed from the potential energy of the whole system, which fluctuates by amounts that grow with the size of the system (the square-root rule again). So the weights vary enormously from frame to frame, for reasons that have nothing to do with the barrier you care about. Metadynamics does not have this problem to the same degree, because its bias is a function of one or two CVs and is no larger than the free-energy differences along them.

**Gaussian accelerated MD** uses a harmonic boost whose distribution is close to Gaussian, so the reweighting factor can be approximated by a second-order cumulant expansion. These methods are good for exploration; treat their free energies with caution. "Harmonic" means quadratic: the boost grows as the square of the distance $E-V$ below the threshold, like the energy of a spring. "Its distribution" is the histogram of the boost values over the frames of the run.

<div class="box maths" markdown="1">
**Maths you need here: the cumulant expansion.** The noisy quantity in reweighting is an average of an exponential, $\langle e^{x}\rangle$, with $x = \beta\Delta V$. A few large values of $x$ dominate it. The cumulant expansion writes its logarithm in terms of quantities that are easy to estimate:

$$
\ln\langle e^{x}\rangle = \langle x\rangle+\tfrac12\sigma_x^2+\dots
$$

Here $\langle x\rangle$ is the mean of $x$, and $\sigma_x^2 = \langle x^2\rangle-\langle x\rangle^2$ is its variance. The dots stand for terms built from higher powers of the deviations from the mean. If $x$ has exactly a Gaussian distribution, all those terms are zero and the first two are the whole answer. "Second order" means stopping after the variance term.

Example: if $\beta\Delta V$ has a mean of 20 and a standard deviation of 2, then $\ln\langle e^{\beta\Delta V}\rangle = 20+\tfrac12\times2^2 = 22$. The mean and the variance are computed from all frames and not from a few extreme ones, so the estimate is far less noisy. Its accuracy rests on the boost really being Gaussian. More in the toolbox: [mean and variance](maths.html#averages), [the Gaussian](maths.html#gaussian).
</div>

## Weighted ensemble

<div data-videos="EMZu-n4WCH0 ShtrAD-tT7c ziRedoLEb2o"></div>

This is the third cure: leave the terrain alone and manage many walkers. The forces are never touched. What is changed is the bookkeeping: which trajectories are continued, which are stopped, and how much probability each one stands for.

[Huber and Kim (1996)](cite:huber1996) introduced the method for Brownian dynamics of two model proteins (rigid spheres that diffuse and associate), not for all-atom MD. No bias on the potential at all. Divide a progress coordinate into bins. Run many short unbiased trajectories ("walkers"), each carrying a statistical weight. After each short interval (in the original paper, after every Brownian time step), **split** walkers in bins that have too few (the copies share the weight) and **merge** walkers in bins that have too many (the survivor takes the combined weight). Computer time is thereby concentrated on rare regions, while the total weight flowing from one state to another remains statistically exact.

Some words first. Brownian dynamics (Module 8) moves particles by random steps plus a drift along the force, with the solvent present only as friction and noise. A progress coordinate measures how far a walker has advanced, for example the distance between the two partners, and is cut into intervals called bins. The **statistical weight** of a walker is the share of the total probability that it stands for. The weights of all walkers add up to 1 at all times.

An example with invented numbers. Start 10 walkers in the first bin, each with the weight 0.1, and decide to keep 4 walkers in every occupied bin.

- *Split.* One walker steps into the second bin, which was empty, and is replaced by 4 copies with the weight $0.1/4 = 0.025$ each. The copies continue with different random numbers (the random steps of Brownian dynamics, or the random kicks of a stochastic thermostat in MD), so they soon follow different paths. Without some randomness, identical copies would stay identical and nothing would be gained. When one of them reaches the third bin it is split again, into 4 walkers of weight 0.00625.
- *Merge.* Suppose a crowded bin holds, among others, two walkers with the weights 0.3 and 0.1. One of them is stopped and the other continues with the weight 0.4. The survivor has to be picked at random, with the probabilities 0.75 and 0.25 that are in proportion to the weights. Then each of the two possible futures still carries, on average, the weight it had: $0.75\times0.4 = 0.3$ and $0.25\times0.4 = 0.1$.

After a few rounds the bins near the top of the barrier are full of walkers, each of which stands for a very small probability. A region that a single trajectory would reach once in millions of attempts is populated by walkers of tiny weight, without anyone waiting for it. The result stays exact because splitting and merging never change the forces, never change the total weight, and never change the average weight that travels along each path. The weight that arrives anywhere is, on average, what unmodified dynamics would deliver.

Because the dynamics are unbiased, the method gives **rates** (from the flux of weight into the target state once a steady state has been reached; in the original method each walker that arrives is put back in the starting state, and the steady flux is the inverse of the mean first-passage time) and pathways, which bias-based methods do not give directly. It is less well suited to equilibrium populations. The costs are many trajectories, correlated walkers, and slow relaxation to steady state. WESTPA is the usual software. Milestoning, forward flux sampling and transition path sampling are related methods that also work with ensembles of unbiased trajectory fragments.

The terms of that paragraph:

- The **flux** is the weight that arrives in the target state per unit of time.
- A **steady state** is reached when the flux no longer changes with time, because the distribution of walkers over the bins has settled. Before that, the measured flux is still drifting and does not give the rate.
- The **mean first-passage time** is the average time a trajectory that starts in the initial state needs to reach the target for the first time. Its inverse is the rate. Example: if a weight of $10^{-6}$ arrives per nanosecond, the rate is $10^{-6}$ ns$^{-1}$ $= 10^{3}$ s$^{-1}$ and the mean first-passage time is 1 ms, although no walker ran for longer than a short interval.
- **Correlated walkers**: copies made by splitting share their past. A hundred walkers that descend from one parent are not a hundred independent observations, so error bars have to come from independent runs.

### Adaptive sampling

Adaptive sampling, the last entry of the table in the first section, follows the same strategy with looser bookkeeping. Run a batch of short unbiased trajectories. Look at where they went and find the places where sampling is thin: states visited only a few times, or newly discovered. Start the next batch from those places, and repeat. Computer time flows to the frontier, as in weighted ensemble, but the trajectories carry no weights.

Starting points chosen in this way are not drawn from the equilibrium distribution, so a plain average over all frames would be wrong. The correction is made in the analysis, by a Markov state model (Module 16). Such a model counts transitions between small states over a short time. A count "from state $i$ to state $j$" says what happens *after* the system is in $i$, and that does not depend on how often trajectories were started in $i$.

From the transition probabilities the model then computes the equilibrium populations and the rates. The condition is that the trajectories are in local equilibrium within each state, and Module 16 explains how to test the model.

## Choosing

<div data-videos="st5XKYuJHQE"></div>

Three things narrow the choice before you look at the table. The first is whether you know a coordinate you trust: if you do, a CV-based method is the natural choice. The second is whether you need populations and free energies, or rates and mechanisms: only methods built on unbiased trajectories give rates directly. The third is the size of the part of the system that has to be heated or biased, which decides whether a tempering method is affordable.

| Situation | Reasonable first choice |
|---|---|
| Free energy along a coordinate you trust (a binding distance, one dihedral) | Umbrella sampling with exchange between windows, or well-tempered metadynamics |
| Conformational ensemble of a peptide or a disordered region, no obvious CV | REST2, or temperature replica exchange for small systems |
| Alchemical free energies | Hamiltonian replica exchange in $\lambda$ |
| Exploring an unknown mechanism | Steered MD or Gaussian accelerated MD for a first look, then a rigorous method on the pathway found |
| Rates and mechanisms | Weighted ensemble, or many unbiased trajectories with a Markov state model (Module 16) |
| The slow variable is unknown | Preliminary simulations plus data-driven CV discovery, then a CV-based method |

The same validation applies to all of them: the final answer must not depend on the starting structure, on which half of the data you analyse, or on a second independent run.

## Checking convergence

An enhanced-sampling run that has not converged can deliver a smooth, plausible free-energy profile that is wrong, and nothing in the output says so. "Converged" means that running longer would not change the answer beyond its error bar. The three tests at the end of the previous section apply to every method. Each method also has its own signs.

| Method | What to look at | Sign of trouble |
|---|---|---|
| Temperature replica exchange, REST2 | The path of each replica along the ladder. The acceptance of each neighbouring pair. Averages at the lowest rung from the first and the second half of the run. | A replica that never travels the whole ladder. One pair with a much lower acceptance than the others. Two halves that disagree. |
| Umbrella sampling with exchange | The histograms of all windows and the profile from the two halves, as in Module 12. | Gaps between histograms. A profile that depends on the direction in which the windows were prepared. |
| Metadynamics | The CV against time. The free-energy difference between the basins against time. The height of the new hills (well-tempered). | Few crossings. A free-energy difference that keeps drifting. A CV that gets stuck again after the wells were filled, which points to a slow motion outside the CV. |
| Accelerated MD | The spread of the boost over the frames, and the effective number of frames (below). | A handful of frames carry nearly all the weight. |
| Weighted ensemble | The flux into the target state against time. | A flux that is still rising, or that jumps each time a single heavy walker arrives. |

For every method that reweights, one number summarises how many frames really count. If frame $n$ has the weight $g_n$, the **effective number of frames** is

$$
N_{eff} = \frac{\big(\sum_ng_n\big)^2}{\sum_ng_n^2} .
$$

<div class="legend" markdown="1">
- $N_{eff}$: the effective number of frames: the number of equally weighted frames that would give an average of the same statistical quality.
- $n$: the label of a saved frame, from 1 to the total number of frames.
- $g_n$: the weight of frame $n$, for example $e^{\beta\Delta V}$ in accelerated MD.
- $\sum_n$: the sum over all saved frames.
</div>

Read it like this: if all $N$ weights are equal ($N$ is the number of frames), the formula gives $N_{eff} = N$. If one frame outweighs all the others together, it gives a number close to 1. Example: 999 frames of weight 1 and one frame of weight 1,000 give $N_{eff} = 1{,}999^2/(999+1{,}000^2) = 4.0$. A thousand frames were saved, and the average rests on about four. Error bars then come, as always, from blocks or from independent runs (Module 11).

## What is lost: the time axis

Every method that changes the temperature or the forces gives up the real motion in time. Equilibrium averages survive this. Module 3 made the point: any procedure that visits configurations with the right probabilities gives correct averages, whatever the order of the visits. Rates do not survive it, because a rate is a statement about how long things take.

| Method | Populations and free energies | Rates, durations, order of events |
|---|---|---|
| Plain MD | Yes, if the run is long enough | Yes |
| Replica exchange (temperature, REST2, Hamiltonian) | Yes, from the unmodified replica | No. Swaps cut the trajectories into pieces, and time in a heated or scaled replica is not real time |
| Umbrella sampling, metadynamics, adaptive biasing force | Yes, along the CVs, and for other quantities by reweighting | No. The forces are altered |
| Accelerated MD | In principle, by reweighting, with large noise | No |
| Steered MD | Only through averages of the work, which rarely converge | No. The speed is imposed by you |
| Weighted ensemble | Less well suited | Yes. The trajectories are unbiased |
| Adaptive sampling with a Markov model | Yes, from the model (Module 16) | Yes, from the model, once it has passed its validation tests |

Two cautions follow. A pathway seen under a bias is a suggestion and not yet a mechanism: the system was pushed along the CV you chose, and the real process may go another way. And a barrier height read from a free-energy profile is not enough for a rate, even with the formula of the first section. The CV must be a good reaction coordinate (one along which the transition really proceeds, so that the top of the profile is the true bottleneck), and the prefactor must be known as well (Module 16).

## Check yourself

<details markdown="1"><summary>1. Why does the number of replicas in temperature replica exchange grow with system size?</summary>
The swap probability depends on the overlap of the potential-energy distributions at neighbouring temperatures. Their separation grows as $N_{df}\,\Delta T$ and their width as $\sqrt{N_{df}}$, so the temperature spacing giving constant overlap shrinks as $1/\sqrt{N_{df}}$. (Here $N_{df}$ is the number of degrees of freedom and $\Delta T$ the difference between two neighbouring temperatures.)
</details>

<details markdown="1"><summary>2. In well-tempered metadynamics with bias factor 10 at 300 K, the converged bias between two basins differs by 18 kJ/mol. What is the free-energy difference?</summary>
$F=-\frac{\gamma}{\gamma-1}V$, so the difference is $18\times10/9 = 20$ kJ/mol, with the opposite sign to the bias difference: the basin with more accumulated bias is the lower one. (Here $\gamma$ is the bias factor, $V$ the converged bias and $F$ the free energy along the CV.)
</details>

<details markdown="1"><summary>3. A metadynamics run shows the system leaving the bound state once and never returning. Can you report the binding free energy?</summary>
No. The depth of the bound well can be estimated only when the system has visited both states repeatedly under a nearly stationary bias. A single exit tells you roughly how much bias was needed to escape. That is not a free energy, and it says nothing about the free energy of the unbound state relative to the bound one.
</details>

<details markdown="1"><summary>4. Why do weighted ensemble simulations give rates while metadynamics does not, at least not directly?</summary>
Weighted ensemble trajectories follow the unmodified dynamics, and the splitting and merging only redistribute statistical weight, so the steady-state flux of weight into the target state is the true rate. In metadynamics the forces themselves are altered, so the time axis is no longer physical. (Rates can be recovered under extra assumptions when no bias is deposited on the transition state: "infrequent metadynamics".)
</details>

<details markdown="1"><summary>5. A conformational change has a free-energy barrier of 30 kJ/mol at 300 K. With a prefactor of 10¹⁰ s⁻¹, what is the mean waiting time, and how many crossings do you expect in a simulation of 1 µs?</summary>
The barrier in units of $k_BT$ is $30/2.494 = 12.03$, and $e^{-12.03} = 6.0\times10^{-6}$. The rate is $k = 10^{10}\times6.0\times10^{-6} = 6.0\times10^{4}$ s$^{-1}$, so the mean waiting time is $1/k = 17$ µs. In 1 µs you expect $10^{-6}\times6.0\times10^{4} = 0.06$ crossings: most such runs see none.
</details>

<details markdown="1"><summary>6. Two replicas run at 300 K and 320 K. The cold one holds a configuration whose potential energy is 40 kJ/mol lower than that of the hot one. With what probability is a swap accepted? And if the cold one held the configuration of higher energy?</summary>
$\beta_i-\beta_j = \frac{1}{k_B}\left(\frac{1}{300}-\frac{1}{320}\right) = 0.0251$ mol/kJ, with $i$ the cold replica. In the first case $U(\mathbf x)-U(\mathbf x') = -40$ kJ/mol, the exponent is $0.0251\times(-40) = -1.0$ and $P_{acc} = e^{-1.0} = 0.37$. In the second case the exponent is positive and the swap is always accepted.
</details>

<details markdown="1"><summary>7. A colleague analyses the 450 K replica of a replica-exchange run and reports the populations of folded and unfolded peptide found there as the result of the study, which is about 300 K. What is wrong?</summary>
The 450 K replica samples the equilibrium of the model at 450 K, where the populations are different. The hot replicas exist to supply the cold one with new structures. The populations at 300 K come from the frames collected at 300 K (or from a reweighting of all temperatures with MBAR). Time information is not available from either.
</details>

## Exercises

1. Implement temperature replica exchange for the one-dimensional double well of Module 12 with four temperatures. Plot the trajectory of each replica through temperature space and compare the sampled distribution at the lowest temperature with the exact one.
2. Implement well-tempered metadynamics for the same double well. Plot the estimated free energy every 10,000 steps and the free-energy difference between the wells against time.
3. Estimate the number of replicas needed for temperature replica exchange between 300 and 450 K for a system with 60,000 degrees of freedom and for one with 600 (a peptide in implicit solvent), using an online temperature generator or the scaling argument above.
4. Do the first PLUMED masterclass exercise on metadynamics of alanine dipeptide, with $\phi$ and $\psi$ as CVs. Then repeat using only $\psi$ and explain what goes wrong.

## Read

{{READ}}

## Key papers

{{PAPERS}}
