---
num: 3
title: Statistical mechanics, the link between a trajectory and a measurement
short: Statistical mechanics
part: Part I · Foundations
hours: 8
summary: Derive the Boltzmann distribution, connect partition functions to free energies, and understand why a time average over an MD trajectory equals a thermodynamic average.
videos: 3
tags: stat-mech
---

<div class="box goal" markdown="1">
#### After this module you can

- define a microstate, a macrostate and an ensemble, and say which ensemble a given simulation samples;
- derive the canonical distribution $P\propto e^{-\beta H}$ from a system in contact with a heat bath;
- compute averages and fluctuations from a partition function, and the temperature and pressure from a trajectory;
- explain what a free energy is and why it is harder to compute than an energy;
- define the potential of mean force and write a binding constant as a ratio of partition functions.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Module 2 ended with a trajectory: the positions and momenta of all atoms, step after step. An experiment reports something else: a temperature, a pressure, a heat capacity, a binding constant. Statistical mechanics is the set of rules that turns the first into the second. Almost every number you extract from a simulation is obtained with a formula from this module. The exceptions are the numbers that say how fast something happens, which need more care (see the section on time averages).

The central idea fits in three sentences. A system at a fixed temperature does not sit in one state. It moves through an enormous number of states and visits each with a known probability. What you measure is an average over them.

The module builds this in four layers:

1. **States and probabilities.** What a microstate, a macrostate and an ensemble are, and why a state of energy $E$ has a probability proportional to $e^{-E/k_BT}$, the Boltzmann factor.
2. **The partition function.** The sum of all Boltzmann factors, and how the energy, the pressure, the entropy and their fluctuations follow from it. This layer also gives the formulas an MD program uses to print the temperature and the pressure.
3. **Time averages.** Why averaging over the frames of one trajectory gives the same result as averaging over all states, and when it does not.
4. **Free energy.** The quantity that decides which state is more populated, the potential of mean force along a coordinate, and the binding constant.

The module uses a small set of mathematical tools again and again: exponentials and logarithms, integrals over many variables, Gaussian integrals, averages. Each one is explained in a box at the place where it is first needed. On a first reading you can skip the blocks marked "Optional" without losing the thread.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The table below collects the notation that appears for the first time in this module. Notation from Module 2 (bold letters for vectors, $\sum$, partial derivatives, the dot product) is used in the same way here. All of it is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\langle A\rangle$ | Angle brackets: the **average** of $A$ over all states, each state weighted by its probability. |
| $\propto$ | "Is proportional to": equal up to a constant factor that is not written out. |
| $\approx$ | "Is approximately equal to." |
| $\ll$ | "Is much smaller than." |
| $e^{x}$, $\ln x$ | The exponential function and the natural logarithm. Each undoes the other. |
| $\int d\mathbf r^N\,d\mathbf p^N$ or $\int d\Gamma$ | An integral over all positions and all momenta of the $N$ atoms: "add up over every microstate". |
| $\prod_i$ | Multiply the expression that follows for every value of $i$. It is the counterpart of $\sum_i$ for products. |
| $N!$ | "$N$ factorial", the product $N\times(N-1)\times\dots\times2\times1$. |
| $\delta(x)$ | The Dirac delta function, which is zero unless $x = 0$. |
| $\Delta X$ | A difference: the value of $X$ in the final state minus its value in the initial state. |
| $E_{tot}$, $T_{inst}$, $N_{df}$ | A subscript made of letters is a shortened word. It says which energy, temperature or number is meant: total, instantaneous, degrees of freedom. |
| $[\text{X}]$ | The concentration of the molecule X. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The usual names collide here more than anywhere else in the course.

- $P$ is a probability or a probability density in $P(s)$, $P(\Gamma)$, $P(\xi)$ and $P_A$. It is the pressure in "NPT", in $PV$ and in the virial equation. In the last section it is also the name of a protein.
- $A$ is the Helmholtz free energy in $A = -k_BT\ln Q$ and in $\Delta A$. It is any observable in $\langle A\rangle$ and $A(\Gamma)$. And "A" and "B" are the names of two states.
- $\Delta$ in front of a letter means "difference". In the table of ensembles it is once the name of a partition function. In the box on the Taylor expansion and in the step $\Delta = -E_s$ after it, $\Delta$ alone is a small step.
- $\delta(x)$ is the Dirac delta function. In $\delta V$ the same letter means "deviation from the average".
- $K$ is the kinetic energy. $K_a$ and $K_d$ are binding constants.
- $M$ is the number of saved frames of a trajectory. In one Optional block it is an exponent, and an upright M after a number is the unit mol per litre.
- L is the ligand. In one Optional block $L$ is the edge of the box.
- $s$ labels a microstate in $E_s$ and $P(s)$, and once a species of molecule in $N_s$. Capital $S$ is the entropy.
- $W(\xi)$ and $w(r)$ are two different potentials of mean force.

The lists under the formulas say which meaning applies each time.
</div>

## Microstates, macrostates, ensembles

<div data-videos="lKyrJhN8MFY tcTmOEk8cc4 lLhUpB6oOr8 5LALoxDs0ic HDl63ZSFVwM D1RzvXDXyqA zyId5iqW6Ig"></div>

A simulation knows where every atom is. An experiment does not: a thermometer reads one number and a pressure gauge another. This section sets up the words for these two levels of description, the complete one (every atom) and the coarse one (a few numbers), and for the probabilities that connect them.

A small example first. Throw two dice. The complete description is what each die shows, for example (2, 5). The coarse description is the sum, 7. There are 36 complete outcomes and all are equally likely, but the sums are not: six outcomes give a sum of 7, namely (1,6), (2,5), (3,4), (4,3), (5,2) and (6,1), and only one gives a sum of 2.

So a sum of 7 is six times more probable than a sum of 2, for no other reason than that more complete outcomes lie behind it. Statistical mechanics is this counting argument applied to atoms. The comparison has one limit that matters. All outcomes of the dice are equally likely, while the complete states of a molecule at a fixed temperature are not: their probabilities depend on their energy. The next section derives how.

A **microstate** is one point in phase space, $\Gamma=(\mathbf r,\mathbf p)$: every position and momentum. A **macrostate** is what an experiment controls or measures: number of particles $N$, volume $V$, energy $E$, temperature $T$, pressure $P$. An enormous number of microstates is compatible with one macrostate. An **ensemble** is the probability distribution over microstates that corresponds to a macrostate.

<div class="legend" markdown="1">
- $\Gamma$ (capital Greek gamma): one microstate, the complete list of positions and momenta, $6N$ numbers in all. **Phase space** is the space of all such lists (Module 2).
- $\mathbf r$: the positions of all atoms, three numbers per atom, in nm.
- $\mathbf p$: the momenta of all atoms. The momentum of an atom is its mass times its velocity.
- $N$: the number of particles (atoms).
- $V$: the volume of the simulation box, in nm$^3$.
- $E$: the total energy, kinetic plus potential, in kJ/mol.
- $T$: the temperature, in kelvin (K).
- $P$: the pressure, in bar.
</div>

In the dice example a microstate is the pair of faces and a macrostate is the sum. For a glass of water, a microstate is where each molecule is and how it moves at one instant, and the macrostate is "this many molecules, in this volume, at 25 °C". You can shift or turn any one molecule a little without changing the macrostate. That is why the number of microstates behind one macrostate is enormous.

### Why probabilities, and what an ensemble is

The motion of the atoms follows Newton's laws and leaves nothing to chance. Probability enters because of what a measurement is. A system at room temperature is in a different microstate from one femtosecond to the next, and a measurement lasts enormously longer than that.

What the instrument reports is an average over all the microstates the system went through. To predict such an average you do not need the order in which the microstates were visited. You need to know how often each one occurs, and that is its probability.

The word **ensemble** comes from a way of picturing this probability. Imagine a very large number of copies of your system: the same molecules, the same box, the same temperature, but each copy set up independently of the others, so each is in its own microstate. This imagined collection is the ensemble. The fraction of the copies that are in a given microstate is the probability of that microstate. So "an ensemble" and "a probability distribution over microstates" are two ways of saying the same thing.

A system is at **equilibrium** when this probability distribution no longer changes with time. Every formula in this module is for a system at equilibrium.

The copies are a device for thinking, and nobody builds them. Whether one system followed through time visits its microstates with the same frequencies is a separate question, which the section on time averages takes up. Module 2 used the same picture: the cloud of points in phase space of Liouville's theorem is an ensemble.

<div class="box maths" markdown="1">
**Maths you need here: probability and probability density.** A **probability** is a number between 0 and 1 that says how often something happens: 0.25 means a quarter of the time. The probabilities of all possible outcomes add up to 1. This condition is called **normalisation**.

That works when the outcomes can be listed, like the faces of a die. A position is different. It can take any value in a continuous range, and the probability of finding an atom at *exactly* $x = 0.3$ nm, to infinitely many digits, is zero. What you can ask for is the probability of finding it in a small interval.

A **probability density** $P(x)$ is defined so that $P(x)\,dx$ is the probability of finding $x$ between $x$ and $x+dx$, where $dx$ is the width of a very small interval. The probability of a larger interval is the area under the curve $P(x)$ over that interval, which is an integral. Normalisation then reads $\int P(x)\,dx = 1$.

Example: an atom is equally likely to be anywhere between $x = 0$ and $x = 0.5$ nm. The density is constant and the total area must be 1, so $P = 1/0.5 = 2$ nm$^{-1}$. The probability of finding the atom between 0.1 and 0.2 nm is $2\ \text{nm}^{-1}\times0.1\ \text{nm} = 0.2$. Two things to see here: a density has a unit (one over the unit of $x$), and its value can be larger than 1. Only the area is a probability.

Positions and momenta are continuous, so for classical atoms "the probability of a microstate" is a density of this kind. The derivation in the next section treats the microstates as a list that can be numbered, which keeps the algebra short. The step to continuous variables comes after it. More in the [toolbox](maths.html#probability).
</div>

### The four ensembles

Which probability distribution is the right one depends on what is held fixed, that is, on how the system is connected to its surroundings. Four cases cover almost everything, and the table lists them. Do not try to absorb the formulas in the third and fourth columns now. The paragraphs after the table say what each column and each row means, and the rest of the module derives the formulas.

| Ensemble | Fixed | Probability density of a microstate | Thermodynamic potential | MD realisation |
|---|---|---|---|---|
| Microcanonical (NVE) | $N,V,E$ | $\propto \delta(H(\Gamma)-E)$ | Entropy $S = k_B\ln\Omega$ | Plain Newtonian MD |
| Canonical (NVT) | $N,V,T$ | $\propto e^{-\beta H(\Gamma)}$ | Helmholtz $A = -k_BT\ln Q$ | MD with a thermostat |
| Isothermal-isobaric (NPT) | $N,P,T$ | $\propto e^{-\beta (H(\Gamma)+PV)}$ | Gibbs $G = -k_BT\ln\Delta$ | Thermostat and barostat |
| Grand canonical (µVT) | $\mu,V,T$ | $\propto e^{-\beta (H-\mu N)}$ | $-PV$ | Monte Carlo insertion moves |

Here $\beta = 1/k_BT$. Most biomolecular simulation is NPT, matching a test tube at 1 bar.

<div class="legend" markdown="1">
- $N$, $V$, $E$, $T$, $P$: number of particles, volume, total energy, temperature and pressure, as above. In this table $P$ is the pressure.
- $\mu$ (Greek mu): the **chemical potential**, the change in the free energy of the system when one particle is added to it. Fixing $\mu$ means that the system can exchange particles with a reservoir.
- $H(\Gamma)$: the Hamiltonian, which is the total energy (kinetic plus potential) of the microstate $\Gamma$ (Module 2).
- $\propto$: "is proportional to". The density equals the expression times a constant that is the same for all microstates. Normalisation fixes the constant.
- $\delta(\ )$: the Dirac delta function, explained in the box below.
- $e^{-\beta H(\Gamma)}$: the **Boltzmann factor** of the microstate. $e$ is the number 2.718..., and $e^{-x}$ gets smaller as $x$ grows.
- $\beta$ (Greek beta): shorthand for $1/k_BT$.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$. See the physics box below.
- $\Omega$ (capital Greek omega): the number of microstates that have the given $N$, $V$ and $E$.
- $\ln$: the natural logarithm.
- $S$, $A$, $G$: the entropy, the Helmholtz free energy and the Gibbs free energy. All three are explained later in this module.
- $Q$, $\Delta$: the normalising constants, called partition functions, of the NVT and of the NPT density. Here $\Delta$ is the name of one quantity and does not mean "difference".
- $-PV$: minus the pressure times the volume.
</div>

**The columns.** "Fixed" lists what the set-up of the experiment or of the simulation holds constant. Everything else fluctuates. "Probability density of a microstate" says how likely each microstate is, up to a constant.

The "thermodynamic potential" is the single quantity from which the other thermodynamic properties of that ensemble follow by taking derivatives. In the first three rows you can see that it is a constant times the logarithm of a count or of a normalising constant. "MD realisation" says how to make a simulation sample that ensemble.

**The rows.**

- *Microcanonical (NVE).* The system is isolated: nothing goes in or out, so its energy is fixed. The delta function says that the microstates with energy exactly $E$ are all equally likely and all others have probability zero. This is what Newton's equations alone produce, because they conserve the energy (Module 2).
- *Canonical (NVT).* The system can exchange heat with surroundings that are held at the temperature $T$. Its energy is no longer fixed. It fluctuates around an average. A microstate of energy $H$ has a probability proportional to $e^{-\beta H}$: the higher the energy, the rarer the microstate. In MD a **thermostat** plays the part of the surroundings. It is an algorithm that adds and removes kinetic energy so that the temperature stays close to the target (Module 8).
- *Isothermal-isobaric (NPT).* In addition the volume can change, as if the box had a piston pushed in with the pressure $P$. A microstate now includes the volume of the box. The extra term $PV$ in the exponent makes large volumes less likely, the more so the higher the pressure. In MD a **barostat** changes the size of the box (Module 8).
- *Grand canonical (µVT).* The volume is fixed but particles can enter and leave. This is rare in MD, because inserting an atom in the middle of a trajectory is awkward. It is done with Monte Carlo moves: random trial insertions and deletions that are accepted or rejected by a rule.

<div class="box maths" markdown="1">
**Maths you need here: the Dirac delta function.** Picture a peak at $x = 0$ that is made narrower and taller while the area under it stays equal to 1. The limit of this process is $\delta(x)$. It is zero for every $x$ except $x = 0$. Its job is to pick out one value. Inside an integral it does this:

$$
\int f(x)\,\delta(x-a)\,dx = f(a) .
$$

Here $f$ is any smooth function and $a$ is a fixed number. Only the point where the argument of the delta is zero, $x = a$, contributes. Example: $\int x^2\,\delta(x-3)\,dx = 3^2 = 9$.

In the table, $\delta(H(\Gamma)-E)$ is zero unless the energy $H(\Gamma)$ of the microstate equals $E$. It says "the microstates with energy exactly $E$, all with the same weight, and no others". The delta function returns in the last part of this module, where it picks out all configurations that share one value of a distance. More in the [toolbox](maths.html#delta).
</div>

<div class="box physics" markdown="1">
**Physics you need here: the Boltzmann constant and the energy $k_BT$.** Temperature is measured in kelvin and energy in kJ/mol. The Boltzmann constant $k_B$ converts one into the other: $k_B = 0.0083145$ kJ mol$^{-1}$ K$^{-1}$. (Per mole, as here, it is the same number as the gas constant $R$ of chemistry.) The product $k_BT$ is an energy. At 300 K, $k_BT = 0.0083145\times300 = 2.494$ kJ/mol, or 0.596 kcal/mol.

$k_BT$ is the size of the energy that thermal motion hands to, and takes from, each part of a molecule all the time. It is the yardstick for every energy in this course. An energy difference of 1 $k_BT$ matters little, because thermal motion overcomes it constantly. A difference of 20 $k_BT$ (about 50 kJ/mol at 300 K) is rarely overcome.

The symbol $\beta = 1/k_BT$ has the unit of one over energy, so the product $\beta E$ is a pure number: the energy $E$ counted in units of $k_BT$. For example, 10 kJ/mol at 300 K is $\beta E = 10/2.494 = 4.01$. Whenever you see $e^{-\beta E}$, read "$e$ to the power of minus the energy in units of $k_BT$". More in the primer, under [temperature](physics.html#temperature) and [units](physics.html#units).
</div>

## Where the Boltzmann factor comes from

<div data-videos="_6AFgt2gkr0 tDKjLzbXYQI aFEovHmSvQk J-qTchJh4Ok EmM1jOV1uSY rhFkYjaM5kE SmmGDn8OnTA"></div>

The table states that at a fixed temperature a microstate of energy $E$ has a probability proportional to $e^{-\beta E}$. Every average that a simulation at constant temperature produces is weighted by this factor, so it is worth seeing where it comes from. The argument uses only counting.

The idea in words. Put a small system (a protein, say) in contact with a huge reservoir of surrounding molecules, the **heat bath**, and let the two exchange energy. The total energy is fixed. Every bit of energy that the small system holds is energy that the bath does not have, and a bath with less energy can arrange itself in fewer ways. So the microstates of the small system that hold much energy are improbable, because they leave the bath with few options.

Why an exponential? Suppose, as an illustration, that the number of ways to arrange the bath doubles for every unit of energy it receives. If the small system takes one unit, the bath has half as many arrangements. If it takes two units, a quarter. Three units, an eighth.

Each extra unit costs the same *factor*, and a quantity that falls by a constant factor for each equal step is an exponential. The derivation below makes this exact. If it is heavy on a first reading, keep this picture and the framed result at the end of the derivation, and come back to the steps later.

**Postulate (equal a priori probabilities).** For an isolated system with energy $E$, all accessible microstates are equally likely. The number of them is $\Omega(N,V,E)$, and Boltzmann's entropy is $S = k_B\ln\Omega$.

In $\Omega(N,V,E)$ the brackets list what the count depends on: the number of particles, the volume and the energy. Three words in the postulate need explaining. An **isolated** system exchanges neither energy nor particles with anything else. The **accessible** microstates are those compatible with the fixed values of $N$, $V$ and $E$.

A **postulate** is a starting assumption. It is not derived from anything more basic, and it is accepted because what follows from it agrees with experiment. You make the same assumption about a fair die: with no reason to prefer one face, you give all six the same probability. Here each of the $\Omega$ microstates gets the probability $1/\Omega$.

<div class="box physics" markdown="1">
**Physics you need here: entropy.** Boltzmann's formula $S = k_B\ln\Omega$ defines the entropy $S$ as a measure of the number of microstates $\Omega$ that lie behind a macrostate. Many microstates, high entropy. For the two dice, the macrostate "sum 7" has $\Omega = 6$ and "sum 2" has $\Omega = 1$.

Why the logarithm and not $\Omega$ itself? Because counts multiply and logarithms add. If one system has $\Omega_1$ microstates and a second, independent one has $\Omega_2$, then together they have $\Omega_1\Omega_2$, since each microstate of the first can go with each microstate of the second. The logarithm turns the product into a sum, $\ln(\Omega_1\Omega_2) = \ln\Omega_1 + \ln\Omega_2$.

So the entropy of two systems is the sum of their entropies, in the same way as their energies and their volumes add. The logarithm also tames the size of $\Omega$, which for any sample you can see is too large to write down: its number of digits is itself of the order of the number of molecules.

The constant $k_B$ only sets the unit, energy per kelvin, so that temperature times entropy, $TS$, is an energy. An example to keep in mind: a state that consists of 1,000 equally likely conformations has an entropy that is higher by $k_B\ln1000$ than a state that is a single conformation. At 300 K this is worth $T\Delta S = 2.494\times6.908 = 17.2$ kJ/mol. More in the [primer](physics.html#thermodynamics).
</div>

<div class="box maths" markdown="1">
**Maths you need here: the exponential and the logarithm.** The exponential function $e^x$, also written $\exp(x)$, is the number $e = 2.718\ldots$ raised to the power $x$. Its main rule: adding in the exponent is multiplying outside, $e^{a+b} = e^a e^b$. So $e^{-x}$ falls by the same factor each time $x$ grows by 1: $e^{-1} = 0.368$, $e^{-2} = 0.135$, $e^{-3} = 0.050$.

The natural logarithm $\ln$ undoes the exponential: $\ln(e^x) = x$ and $e^{\ln y} = y$. It is defined for positive numbers only. Its rules mirror those of the exponential. For positive numbers $a$ and $b$ and any number $n$:

$$
\ln(ab) = \ln a + \ln b,\qquad \ln\frac{a}{b} = \ln a - \ln b,\qquad \ln(a^n) = n\ln a,\qquad \ln 1 = 0 .
$$

Example: $\ln 1000 = \ln(10^3) = 3\ln 10 = 3\times2.303 = 6.908$. Two habits save time. To remove a logarithm from an equation, take the exponential of both sides. And "$y$ is proportional to $e^{-x}$" is the same statement as "$\ln y$ plotted against $x$ is a straight line with slope $-1$". More in the [toolbox](maths.html#exp-log).
</div>

Now take a small system in thermal contact with a very large bath. "Thermal contact" means that the two can exchange energy as heat, but no particles. Together they are isolated with total energy $E_{tot}$.

Apply the postulate to the two together. A microstate of the combined system is a pair: one microstate of the small system and one of the bath. All such pairs with total energy $E_{tot}$ are equally likely. Now fix the small system in one particular microstate, call it $s$, with energy $E_s$. The bath is left with the energy $E_{tot}-E_s$, and it can be in any of its own microstates that have this energy.

The number of those is $\Omega_{bath}(E_{tot}-E_s)$. So this many of the equally likely pairs have the small system in the microstate $s$. The probability that the small system is in one particular microstate with energy $E_s$ is proportional to the number of bath microstates that go with it:

$$
P(\text{microstate } s) \propto \Omega_{bath}(E_{tot}-E_s).
$$

<div class="legend" markdown="1">
- $s$: the label of one microstate of the small system. Think of the microstates as numbered $s = 1, 2, 3, \dots$
- $P(\text{microstate } s)$: the probability of finding the small system in the microstate $s$. Here $P$ is a probability, not a pressure.
- $\propto$: "is proportional to".
- $E_{tot}$: the total energy of the small system and the bath together. It is fixed.
- $E_s$: the energy of the small system when it is in the microstate $s$.
- $E_{tot}-E_s$: the energy left for the bath.
- $\Omega_{bath}(E)$: the number of microstates of the bath when the bath has the energy $E$.
</div>

What remains is to find out how fast $\Omega_{bath}$ falls when energy is taken from the bath.

<div class="box maths" markdown="1">
**Maths you need here: a first-order Taylor expansion.** Close to a point $x_0$, a smooth function is nearly a straight line through that point, with the slope it has there:

$$
f(x_0+\Delta) \approx f(x_0) + f'(x_0)\,\Delta .
$$

Here $\Delta$ is a small step away from $x_0$, and $f'(x_0)$ is the slope (the derivative) of $f$ at $x_0$. "First order" means that only the term with $\Delta$ to the power 1 is kept. Example: $\ln(1+\Delta)\approx\Delta$ for small $\Delta$, because $\ln 1 = 0$ and the slope of $\ln x$ at $x = 1$ is 1. For $\Delta = 0.01$ the exact value is 0.00995. More in the [toolbox](maths.html#taylor).
</div>

The function to expand is $\ln\Omega_{bath}$, the point $x_0$ is $E_{tot}$, and the step is $\Delta = -E_s$: the bath has a little less than the total energy. The step is small because the bath is huge, so the energy of the small system is a tiny fraction of the total. Expand the logarithm, which varies slowly, to first order in $E_s \ll E_{tot}$:

$$
\ln\Omega_{bath}(E_{tot}-E_s) \approx \ln\Omega_{bath}(E_{tot}) - E_s \frac{\partial\ln\Omega_{bath}}{\partial E}.
$$

<div class="legend" markdown="1">
- $\ln\Omega_{bath}(E)$: the logarithm of the number of bath microstates at the bath energy $E$.
- $\approx$: "is approximately equal to". The error becomes negligible when the bath is very large.
- $\partial\ln\Omega_{bath}/\partial E$: the slope of $\ln\Omega_{bath}$ with respect to the energy of the bath, taken at $E = E_{tot}$, with the volume and the number of particles of the bath held fixed. (A partial derivative, Module 2.)
- The minus sign: it comes from the step $\Delta = -E_s$.
- Other symbols: as in the list above.
</div>

<details markdown="1"><summary>Optional: why the logarithm is expanded and not the count itself</summary>
$\Omega_{bath}$ changes far too fast for a straight line to follow it. As an illustration, suppose it grows as a high power of the energy, $\Omega_{bath}\propto E^M$, with $M$ of the order of the number of atoms in the bath.

A straight-line approximation to $\Omega_{bath}$ itself gives $\Omega_{bath}(E_{tot})\,(1 - ME_s/E_{tot})$. This turns negative as soon as $E_s$ exceeds $E_{tot}/M$, which is roughly the energy of one atom, and a negative count is nonsense. The logarithm, $M\ln E$, changes gently, and its straight-line approximation is accurate whenever the bath is much larger than the small system.
</details>

Thermodynamics defines temperature by $1/T = \partial S/\partial E$, so $\partial\ln\Omega_{bath}/\partial E = 1/k_BT = \beta$.

This definition looks strange if you think of temperature as "how hot something is". It says that temperature measures how much the entropy of a body rises when you give it a little energy, at fixed volume and number of particles. For a cold body the gain is large ($1/T$ is large): a little energy opens up many new microstates. For a hot body the gain is small.

When a hot and a cold body touch, energy flows from hot to cold, because the number of microstates of the cold body is multiplied by more than that of the hot body is divided by, so the number for the two together goes up. The flow stops when both have the same $\partial S/\partial E$, that is, the same temperature.

The second half of the sentence inserts $S = k_B\ln\Omega$. The slope of $\ln\Omega_{bath}$ is $(1/k_B)\,\partial S/\partial E = 1/k_BT$, and this is what $\beta$ stands for. Three short steps finish the derivation.

**Step 1, insert the slope.** The expansion becomes

$$
\ln\Omega_{bath}(E_{tot}-E_s) \approx \ln\Omega_{bath}(E_{tot}) - \beta E_s .
$$

<div class="legend" markdown="1">
- $\beta$: $1/k_BT$, where $T$ is the temperature of the bath.
- $\beta E_s$: the energy of the microstate $s$ in units of $k_BT$, a pure number.
- Other symbols: as in the list above.
</div>

**Step 2, take the exponential of both sides.** This removes the logarithm on the left. On the right, the rule $e^{a+b} = e^ae^b$ splits the result into two factors:

$$
\Omega_{bath}(E_{tot}-E_s) \approx \Omega_{bath}(E_{tot})\;e^{-\beta E_s} .
$$

<div class="legend" markdown="1">
- $\Omega_{bath}(E_{tot})$: the number of bath microstates if the bath had all the energy. It is one fixed number, the same for every $s$.
- $e^{-\beta E_s}$: the only factor that depends on the microstate $s$.
- Other symbols: as in the list above.
</div>

The probability of $s$ is proportional to the left side, and on the right side only the second factor depends on $s$. So $P(s) \propto e^{-\beta E_s}$.

**Step 3, normalise.** Write $P(s) = c\,e^{-\beta E_s}$ with an unknown constant $c$. The probabilities of all microstates must add up to 1, so $c\sum_s e^{-\beta E_s} = 1$ and $c = 1/\sum_s e^{-\beta E_s}$. The sum is given the name $Q$.

Therefore

$$
\boxed{P(s) = \frac{e^{-\beta E_s}}{Q},\qquad Q=\sum_s e^{-\beta E_s}}
$$

<div class="legend" markdown="1">
- $P(s)$: the probability that the small system is in the microstate $s$.
- $E_s$: the energy of the microstate $s$.
- $\beta$: $1/k_BT$. At 300 K, $k_BT = 2.494$ kJ/mol.
- $e^{-\beta E_s}$: the **Boltzmann factor** of the microstate $s$, a number between 0 and 1 when the energy is counted from the lowest microstate.
- $\sum_s$: a sum over all microstates of the small system.
- $Q$: the sum of the Boltzmann factors of all microstates. Dividing by it makes the probabilities add up to 1.
- The frame around the formula only marks it as the main result of this section.
</div>

Read it like this. The probability of a microstate depends only on its energy, counted in units of $k_BT$. A microstate with a higher energy is always less probable than one with a lower energy. By how much is fixed by the ratio of the two probabilities, in which $Q$ cancels:

$$
\frac{P(s_2)}{P(s_1)} = e^{-\beta(E_2-E_1)} .
$$

<div class="legend" markdown="1">
- $s_1$, $s_2$: two microstates of the same system.
- $E_1$, $E_2$: their energies.
- $E_2-E_1$: the energy difference. Only the difference matters, so the zero of energy can be put anywhere.
- Other symbols: as in the list above.
</div>

At 300 K, a microstate that lies 2.494 kJ/mol (1 $k_BT$) above another is $e^{-1} = 0.37$ times as probable. One that lies 10 kJ/mol higher is $e^{-4.01} = 0.018$ times as probable. Raise the temperature and $\beta$ gets smaller, so the same energy difference counts for less and the high-energy microstates become more populated. Lower it towards zero and only the microstate of lowest energy survives.

<div class="box key" markdown="1">
**Worked example: three microstates.** A toy system has three microstates with the energies 0, 2.494 and 4.988 kJ/mol. At 300 K that is 0, 1 and 2 in units of $k_BT$. The Boltzmann factors are $e^{0} = 1$, $e^{-1} = 0.368$ and $e^{-2} = 0.135$.

The partition function is their sum, $Q = 1 + 0.368 + 0.135 = 1.503$. The probabilities are the factors divided by $Q$: 0.665, 0.245 and 0.090. They add up to 1, as they must.
</div>

This is the canonical (Boltzmann) distribution, and $Q$ is the **partition function**. The only property of the bath that survives is its temperature.

The last sentence is what makes the result usable. The bath could be water, a gas or a block of metal, and the small system cannot tell the difference. All that reaches it is one number, $T$. This is also why a thermostat algorithm, which is nothing like a real bath, can stand in for one (Module 8).

One warning before going on. The formula gives the probability of one *microstate*. The probability that the system has a certain *energy* is a different thing: it is proportional to the Boltzmann factor times the number of microstates that have that energy.

Per microstate, low energy wins. But there are usually far more microstates at higher energy. The competition between these two effects is the subject of the section on free energy.

### The classical partition function

<div data-videos="UxJCRnNJCPw 34OuWjAwI8w RT_v0PhXP5E"></div>

The derivation above numbered the microstates and summed over them. For atoms that follow classical mechanics the microstates cannot be numbered, because positions and momenta are continuous. The sum over microstates becomes an integral over all positions and all momenta, that is, over phase space. This subsection writes that integral down and then does half of it exactly. The result is one of the most useful facts of the course: the masses of the atoms do not affect which structures are populated.

<div class="box maths" markdown="1">
**Maths you need here: an integral over many variables.** An ordinary integral $\int f(x)\,dx$ adds up the values of $f$ over all $x$, each multiplied by the width $dx$ of a small step. It is the continuous version of a sum. With two variables, $\int\!\!\int f(x,y)\,dx\,dy$ does the same over a plane: cut the plane into small rectangles of area $dx\,dy$, multiply the value of $f$ in each rectangle by that area, and add.

The symbol $\int d\mathbf r^N\,d\mathbf p^N$ is the same idea with $6N$ variables: the three position components and the three momentum components of each of the $N$ atoms. Read it as "add up over every possible microstate". Each position runs over the inside of the box and each momentum component from $-\infty$ to $+\infty$. In this notation the $d\ldots$ stands directly after the integral sign and the function to be integrated comes after it. That is only a different order of writing.

Nobody computes such an integral by brute force. One rule makes parts of it easy: when the function is a product of a part that depends only on $x$ and a part that depends only on $y$, the double integral is the product of two single integrals. Example:

$$
\int_0^2\!dx\int_0^3\!dy\;x\,y = \left(\int_0^2 x\,dx\right)\left(\int_0^3 y\,dy\right) = 2\times4.5 = 9 .
$$

More in the [toolbox](maths.html#integral).
</div>

For classical particles the sum over states becomes an integral over phase space:

$$
Q(N,V,T) = \frac{1}{N!\,h^{3N}}\int d\mathbf r^N\,d\mathbf p^N\; e^{-\beta H(\mathbf r,\mathbf p)} .
$$

<div class="legend" markdown="1">
- $Q(N,V,T)$: the canonical partition function. The brackets list what it depends on: the number of particles, the volume and the temperature.
- $\int d\mathbf r^N\,d\mathbf p^N$: the integral over all positions and all momenta of the $N$ atoms, $6N$ variables in all (see the box above).
- $H(\mathbf r,\mathbf p)$: the Hamiltonian, the total energy of the microstate with the positions $\mathbf r$ and the momenta $\mathbf p$.
- $e^{-\beta H}$: the Boltzmann factor of that microstate, with $\beta = 1/k_BT$.
- $h$: Planck's constant, the basic constant of quantum mechanics. Its value is $6.626\times10^{-34}$ J s, which is 0.399 kJ mol$^{-1}$ ps in MD units.
- $h^{3N}$: one factor $h$ for each of the $3N$ pairs made of a position component and its momentum component.
- $N!$: "$N$ factorial", the product $N\times(N-1)\times\dots\times2\times1$. It is the number of different orders in which $N$ objects can be put. For example $3! = 6$.
</div>

The factor $h^{3N}$ makes $Q$ dimensionless and matches the quantum count of states. The $N!$ corrects for identical particles.

Neither factor will trouble you in practice. Both are constants that do not depend on the microstate. They cancel in the probability of a microstate, in every average, and in every free-energy difference between two states of the same system. They matter only for absolute entropies and absolute free energies.

<details markdown="1"><summary>Optional: what the factors $h^{3N}$ and $N!$ do</summary>
*The factor $h^{3N}$.* A sum over numbered microstates is a pure number. The integral is not: each pair $dx\,dp$ carries the unit of length times momentum. Planck's constant has exactly that unit, so dividing by one $h$ per pair leaves a pure number. ("Dimensionless" means "without a unit".) The physical picture is that quantum mechanics does not allow a position and its momentum to be specified more finely than a cell of area $h$ in the $(x,p)$ plane. Dividing the volume of phase space by $h^{3N}$ counts these cells, so the integral becomes a count of states again.

*The factor $N!$.* Take two water molecules and exchange them: put molecule 1 where molecule 2 was, with its momentum, and the reverse. Nothing physical has changed, because the two are identical. But the integral runs over the positions of molecule 1 and of molecule 2 separately, so it counts the two arrangements as different points of phase space.

For $N$ identical molecules every physical state is counted $N!$ times, once for each way of handing out the labels. The division by $N!$ removes the overcount. More on factorials in the [toolbox](maths.html#combinatorics).
</details>

Now the integral itself. The Hamiltonian of Module 2 is a sum of two parts: the kinetic energy, which contains only momenta, and the potential energy $U$, which contains only positions. Because $e^{a+b} = e^ae^b$, the Boltzmann factor is then a product:

$$
e^{-\beta H(\mathbf r,\mathbf p)} = e^{-\beta\sum_i \mathbf p_i^2/2m_i}\;\times\;e^{-\beta U(\mathbf r)} .
$$

<div class="legend" markdown="1">
- $\mathbf p_i$: the momentum of atom $i$, a vector with three components.
- $\mathbf p_i^2$: shorthand for $\mathbf p_i\cdot\mathbf p_i = p_{ix}^2+p_{iy}^2+p_{iz}^2$.
- $m_i$: the mass of atom $i$, in u.
- $\sum_i \mathbf p_i^2/2m_i$: the total kinetic energy.
- $U(\mathbf r)$: the potential energy, a function of the positions only.
- Other symbols: as in the list above.
</div>

One factor depends only on the momenta and the other only on the positions. By the rule in the box, the integral splits into a momentum integral times a position integral. The momentum factor splits further, into one factor for each atom and each component $x$, $y$, $z$, and every one of them has the form $e^{-\beta p^2/2m}$. This is a bell-shaped curve, a Gaussian, and its integral is known.

<div class="box maths" markdown="1">
**Maths you need here: Gaussian integrals.** The function $e^{-ax^2}$, with $a$ a positive constant, is the bell curve. It equals 1 at $x = 0$ and falls off symmetrically on both sides, faster for larger $a$. It is called a Gaussian. Two integrals over the whole line, from $-\infty$ to $+\infty$, are used again and again:

$$
\int_{-\infty}^{\infty} e^{-ax^2}\,dx = \sqrt{\frac{\pi}{a}},\qquad
\int_{-\infty}^{\infty} x^2\,e^{-ax^2}\,dx = \frac{1}{2a}\sqrt{\frac{\pi}{a}} .
$$

Example: for $a = 1$ the first one is $\sqrt\pi = 1.772$. Dividing the second by the first gives the average of $x^2$ under a Gaussian weight, which is $1/(2a)$.

A probability density proportional to $e^{-x^2/2\sigma^2}$ is called a Gaussian (or normal) distribution with standard deviation $\sigma$ (Greek sigma). Comparing the exponents, $a = 1/(2\sigma^2)$, so the average of $x^2$ is $\sigma^2$. This average is called the variance. More in the [toolbox](maths.html#gaussian).
</div>

Apply the first result with $x = p$ and $a = \beta/2m$. One momentum component gives $\sqrt{\pi\times2m/\beta} = \sqrt{2\pi mk_BT}$. An atom has three components, so its momentum integral is this to the power 3, which is the left half of the next line. With $H = \sum \mathbf p_i^2/2m_i + U(\mathbf r)$ the momentum integrals are Gaussian and can be done exactly:

$$
\int d\mathbf p\,e^{-\beta \mathbf p^2/2m} = (2\pi m k_BT)^{3/2}
\quad\Longrightarrow\quad
Q = \frac{1}{N!\,\Lambda^{3N}}\underbrace{\int d\mathbf r^N e^{-\beta U(\mathbf r)}}_{Z},\qquad \Lambda = \frac{h}{\sqrt{2\pi mk_BT}}.
$$

<div class="legend" markdown="1">
- $\int d\mathbf p$: the integral over the three momentum components of one atom, each from $-\infty$ to $+\infty$.
- $\mathbf p^2$: $p_x^2+p_y^2+p_z^2$ for that atom.
- $m$: the mass of the atom. The line is written for atoms that all have the same mass.
- $(2\pi mk_BT)^{3/2}$: the result for one atom, the third power of $\sqrt{2\pi mk_BT}$.
- $\Longrightarrow$: "from which it follows that".
- $Z$: the **configurational integral**, the integral of $e^{-\beta U}$ over the positions of all atoms. Its unit is a volume to the power $N$.
- The brace underneath only attaches the name $Z$ to the integral. It is not part of the formula.
- $\Lambda$ (capital Greek lambda): the **thermal de Broglie wavelength**, a length that collects $h$, the mass and the temperature. For a carbon atom (12 u) at 300 K it is about 0.03 nm.
- $N!$, $h$, $\beta$, $U(\mathbf r)$: as in the lists above.
</div>

The right half follows by collecting factors. There are $N$ atoms, so the momentum integrals give $(2\pi mk_BT)^{3N/2}$ in all. Together with the $1/h^{3N}$ in front, this is $\big(\sqrt{2\pi mk_BT}/h\big)^{3N} = 1/\Lambda^{3N}$. What remains is the integral over the positions, which gets the name $Z$.

For an ideal gas, where $U = 0$, the function under the integral is 1 and each atom contributes the volume of the box, so $Z = V^N$. All the effects of the interactions are in the difference between $Z$ and $V^N$.

$Z$ is the **configurational integral**. (The formula is written for identical particles of one mass. With several species, each atom contributes its own $\Lambda_i^3$ and each species $s$ its own $N_s!$: $Q = Z/\big[\prod_sN_s!\,\prod_i\Lambda_i^3\big]$. Nothing below depends on this.) This factorisation has a practical meaning: in classical statistical mechanics, **the distribution of positions does not depend on the masses**, and the momenta always follow the Maxwell-Boltzmann distribution regardless of the forces. All the difficulty, and all the chemistry, is in $Z$. It is also why hydrogen mass repartitioning (Module 9) does not change equilibrium properties.

In the bracketed remark, $\prod$ is the product sign, $s$ labels a species, that is, a kind of molecule (it is not a microstate here), $N_s$ is the number of molecules of that species, and $\Lambda_i$ is $\Lambda$ computed with the mass of atom $i$.

To see why the positions do not feel the masses, ask for the probability density of the positions alone, whatever the momenta are. Integrate the full density, which is proportional to $e^{-\beta H}$, over all momenta. The momentum integral gives the same constant for every arrangement of the atoms. It cancels against the same constant in the normalisation, and what is left is

$$
P(\mathbf r) = \frac{e^{-\beta U(\mathbf r)}}{Z} .
$$

<div class="legend" markdown="1">
- $\mathbf r$: one arrangement (configuration) of all the atoms, $3N$ coordinates.
- $P(\mathbf r)$: the probability density of finding the atoms in that arrangement. Here $P$ is a probability density, not a pressure.
- $U(\mathbf r)$: the potential energy of the arrangement.
- $Z$: the configurational integral, which normalises the density.
</div>

No mass appears in this formula. The masses sit only in the momentum factor, which has been integrated away. Making every hydrogen three times heavier changes how fast a molecule moves. It does not change which structures the molecule visits or how often. Hydrogen mass repartitioning, a technique of Module 9 that makes the hydrogen atoms heavier so that a longer time step can be used, relies on this.

The momentum factor, for its part, contains no forces. $e^{-\beta p^2/2m}$ is the same Gaussian whether the atom sits inside a protein or in a dilute gas. That Gaussian is the **Maxwell-Boltzmann distribution**, which the section on equipartition below writes out.

## From the partition function to thermodynamics

<div data-videos="_ErxZOHwtaA AhNHsYpemII bW30Rj6w8VI"></div>

$Q$ looks like a mere normalising constant, the number you divide by so that the probabilities add up to 1. This section shows that it holds the whole thermodynamics of the system. Here is why a normalising constant can carry so much. $Q$ is the sum of the Boltzmann factors of all microstates, so it depends on the temperature (through $\beta$) and on the volume and the number of particles (through the energies $E_s$).

Change the temperature slightly, and each term of the sum changes by an amount proportional to its energy, so the change of $Q$ records the average energy. Change the volume slightly, and the change of $Q$ records how the energies respond to the volume, which is the pressure. $Q$ as a function of $T$, $V$ and $N$ is a compact record of the system, and derivatives read it out.

On a first reading, the essential parts of this section are the four relations, what each of them means, and the statement that fluctuations give the heat capacity. The step-by-step checks can wait. First, one piece of notation.

<div class="box maths" markdown="1">
**Maths you need here: mean, variance and the angle brackets.** The **mean** (average) of a quantity $A$ that has the value $A_s$ in the microstate $s$ is the sum of the values, each weighted by its probability:

$$
\langle A\rangle = \sum_s A_s\,P(s) .
$$

Angle brackets $\langle\ \rangle$ always mean such an average. The **variance** measures how far the values spread around the mean. It is the mean of the squared deviation, $\langle (A-\langle A\rangle)^2\rangle$. Multiplying out the square shows that it equals $\langle A^2\rangle - \langle A\rangle^2$, "the mean of the square minus the square of the mean". Its square root is the **standard deviation**, which has the same unit as $A$ and is the typical size of a fluctuation.

Example, with the three microstates of the worked example above (energies 0, 2.494 and 4.988 kJ/mol, probabilities 0.665, 0.245 and 0.090). The mean energy is $\langle E\rangle = 0.245\times2.494 + 0.090\times4.988 = 1.06$ kJ/mol. The mean of the square is $\langle E^2\rangle = 0.245\times2.494^2 + 0.090\times4.988^2 = 3.76$ (kJ/mol)$^2$. The variance is $3.76 - 1.06^2 = 2.64$ (kJ/mol)$^2$, and the standard deviation is its square root, 1.62 kJ/mol. More in the [toolbox](maths.html#averages).
</div>

Everything follows from $Q$:

$$
A = -k_BT\ln Q,\qquad
\langle E\rangle = -\frac{\partial \ln Q}{\partial\beta},\qquad
P = k_BT\frac{\partial\ln Q}{\partial V},\qquad
S = -\frac{\partial A}{\partial T}.
$$

<div class="legend" markdown="1">
- $Q$: the canonical partition function, a function of $N$, $V$ and $T$.
- $A$: the **Helmholtz free energy**, in kJ/mol. Here $A$ is not an observable.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- $\langle E\rangle$: the average total energy of the system.
- $\partial/\partial\beta$: the derivative with respect to $\beta = 1/k_BT$, with $N$ and $V$ held fixed.
- $P$: the pressure. Here $P$ is not a probability.
- $\partial/\partial V$: the derivative with respect to the volume, with $N$ and $T$ held fixed.
- $S$: the entropy.
- $\partial A/\partial T$: the derivative of the free energy with respect to the temperature, with $N$ and $V$ held fixed.
</div>

The four relations, one at a time.

**The free energy, $A = -k_BT\ln Q$.** This is the bridge between counting and thermodynamics. For now, take it as the definition of the Helmholtz free energy $A$. The section on free energy below explains what $A$ measures.

Two things can be read off at once. $A$ is an energy, because $\ln Q$ is a pure number and $k_BT$ is an energy. And the minus sign means that more accessible microstates give a larger $Q$ and a lower free energy.

**The average energy.** Check the second one: $-\partial_\beta \ln Q = \frac{1}{Q}\sum_s E_s e^{-\beta E_s} = \langle E\rangle$.

Here $\partial_\beta$ is a short way of writing $\partial/\partial\beta$. Step by step: the derivative of $\ln Q$ is $1/Q$ times the derivative of $Q$ ([chain rule](maths.html#chain-rule)). $Q$ is a sum of terms $e^{-\beta E_s}$, and the derivative of each term with respect to $\beta$ is $-E_s\,e^{-\beta E_s}$. The two minus signs cancel. What is left, $\sum_s E_s\,e^{-\beta E_s}/Q$, is $\sum_s E_s P(s)$, which is the definition of the mean energy.

Why differentiate with respect to $\beta$ and not $T$? Only because the algebra is shorter. To convert at any time, use $\beta = 1/k_BT$, which gives $d\beta/dT = -1/k_BT^2$.

**The pressure.** Thermodynamics defines the pressure as the rate at which the free energy falls when the volume grows at constant temperature, $P = -\partial A/\partial V$. (A gas pushes its container outwards because expanding lowers its free energy.) Inserting $A = -k_BT\ln Q$ gives the third relation. A quick check with the ideal gas: without interactions $Z = V^N$, so $\ln Q = N\ln V$ plus terms that do not contain $V$. The derivative of $N\ln V$ with respect to $V$ is $N/V$, so $P = Nk_BT/V$, which is the ideal gas law.

**The entropy.** $S = -\partial A/\partial T$ is also a relation from thermodynamics: the entropy is the rate at which the free energy falls when the temperature rises, at fixed $N$ and $V$. Is this the same entropy as Boltzmann's $k_B\ln\Omega$?

Test it on the simplest case, a system with $\Omega$ microstates that all have the same energy $E_0$. Then $Q = \Omega\,e^{-\beta E_0}$, and with the rules for logarithms $A = -k_BT\ln\Omega + E_0$. Differentiating with respect to $T$ gives $S = k_B\ln\Omega$. It is the same.

<details markdown="1"><summary>Optional: check that $A = \langle E\rangle - TS$</summary>
The section on free energy uses the form $A = \langle E\rangle - TS$. It follows from the relations above. Start from $A = -k_BT\ln Q$ and differentiate with respect to $T$ using the product rule:

$$
\frac{\partial A}{\partial T} = -k_B\ln Q - k_BT\,\frac{\partial\ln Q}{\partial T} .
$$

The first term is $A/T$. For the second, use the chain rule with $d\beta/dT = -1/k_BT^2$ and the result $\partial\ln Q/\partial\beta = -\langle E\rangle$:

$$
\frac{\partial\ln Q}{\partial T} = \frac{\partial\ln Q}{\partial\beta}\,\frac{d\beta}{dT} = \frac{\langle E\rangle}{k_BT^2} .
$$

So $\partial A/\partial T = A/T - \langle E\rangle/T$. Since $S = -\partial A/\partial T$, this reads $-S = (A - \langle E\rangle)/T$. Multiply by $T$ and rearrange: $A = \langle E\rangle - TS$.
</details>

### Fluctuations and the heat capacity

The energy of a system at constant temperature is not constant. It fluctuates around $\langle E\rangle$, because energy keeps passing to and from the surroundings. The size of these fluctuations carries information: it gives the heat capacity.

Differentiating once more gives the fluctuations:

$$
\frac{\partial^2\ln Q}{\partial\beta^2} = \langle E^2\rangle - \langle E\rangle^2
\quad\Longrightarrow\quad
C_V = \frac{\partial \langle E\rangle}{\partial T} = \frac{\langle E^2\rangle-\langle E\rangle^2}{k_BT^2}.
$$

<div class="legend" markdown="1">
- $\partial^2\ln Q/\partial\beta^2$: the second derivative of $\ln Q$ with respect to $\beta$: differentiate, then differentiate the result again.
- $\langle E^2\rangle$: the average of the square of the energy.
- $\langle E\rangle^2$: the square of the average energy.
- $\langle E^2\rangle - \langle E\rangle^2$: the variance of the energy, the square of the typical size of an energy fluctuation.
- $C_V$: the **heat capacity at constant volume**, the energy needed to raise the temperature by one kelvin while the volume is fixed, in kJ mol$^{-1}$ K$^{-1}$.
- $\partial\langle E\rangle/\partial T$: the definition of $C_V$, the rate at which the average energy rises with the temperature.
- $k_BT^2$: the Boltzmann constant times the square of the temperature.
- $\Longrightarrow$: "from which it follows that".
</div>

The left part, step by step. From above, $\partial\ln Q/\partial\beta = (1/Q)\,\partial Q/\partial\beta$. Differentiate this product once more with the product rule:

$$
\frac{\partial^2\ln Q}{\partial\beta^2} = \frac{1}{Q}\frac{\partial^2Q}{\partial\beta^2} - \frac{1}{Q^2}\left(\frac{\partial Q}{\partial\beta}\right)^2 .
$$

<div class="legend" markdown="1">
- $\partial^2Q/\partial\beta^2$: the second derivative of $Q$ with respect to $\beta$.
- $(\partial Q/\partial\beta)^2$: the square of the first derivative.
- Other symbols: as in the list above.
</div>

In the first term, differentiating $e^{-\beta E_s}$ twice brings down $E_s^2$, so the term is $\sum_sE_s^2\,e^{-\beta E_s}/Q = \langle E^2\rangle$. The second term is the square of $(1/Q)\,\partial Q/\partial\beta$, which is $-\langle E\rangle$. Together they give $\langle E^2\rangle - \langle E\rangle^2$, the variance of the energy.

The right part. Since $\langle E\rangle = -\partial\ln Q/\partial\beta$, the left side is also $-\partial\langle E\rangle/\partial\beta$. Convert to a derivative with respect to $T$ with the chain rule: $\partial\langle E\rangle/\partial T = (\partial\langle E\rangle/\partial\beta)\,(d\beta/dT)$. The first factor is minus the variance and the second is $-1/k_BT^2$. The two minus signs cancel, which gives the formula for $C_V$.

Read it like this. The heat capacity says how much energy the system takes up per kelvin. The formula says that you can obtain it without changing the temperature at all: run one simulation at one temperature, record the total energy, and compute its variance. A system whose energy fluctuates widely has many microstates within reach at nearby energies, and such a system soaks up much energy when heated. An illustration with round numbers: if the total energy of a simulated box has a standard deviation of 500 kJ/mol at 300 K, then $C_V = 500^2/(0.0083145\times300^2) = 334$ kJ mol$^{-1}$ K$^{-1}$.

The formula holds for the canonical ensemble. In an NVE run the total energy does not fluctuate at all, and with a thermostat the result is right only if the thermostat produces the correct canonical fluctuations (Module 8).

This is a general pattern: **response functions are fluctuations**. The heat capacity is the variance of the energy, the compressibility is the variance of the volume ($\langle\delta V^2\rangle = k_BT\,V\kappa_T$ in NPT), and the dielectric constant is the variance of the total dipole moment. Relative fluctuations scale as $1/\sqrt N$: for a macroscopic sample they are invisible, for a simulation box of $10^5$ atoms they are a fraction of a percent, and for the instantaneous pressure they are large (Module 8).

<div class="legend" markdown="1">
- Response function: a number that says how strongly a system reacts when a condition is changed. The heat capacity is the response of the energy to the temperature.
- $\kappa_T$ (Greek kappa): the **isothermal compressibility**, the fraction by which the volume shrinks per unit of added pressure at constant temperature. It is the response of the volume to the pressure.
- $\delta V$: the deviation of the volume from its average at one instant, $V - \langle V\rangle$. This $\delta$ is not the Dirac delta.
- $\langle\delta V^2\rangle$: the average of the squared deviation, which is the variance of the volume.
- $V$ on the right side: the average volume of the box.
- Dielectric constant: the factor by which a material weakens the electric forces between charges inside it ([primer](physics.html#electrostatics)). It is the response of the material to an electric field.
- Total dipole moment: a vector that measures how far the positive and the negative charge in the box are separated, the sum of charge times position over all atoms ([primer](physics.html#dipoles)).
- $N$: the number of atoms.
- Relative fluctuation: the standard deviation divided by the mean.
</div>

Where does the $1/\sqrt N$ come from? The energy of a large system is a sum of $N$ contributions that are roughly independent of each other. For such a sum the means add, so the mean grows as $N$. The variances add too, so the variance grows as $N$ and the standard deviation as $\sqrt N$. The ratio of standard deviation to mean therefore falls as $\sqrt N/N = 1/\sqrt N$.

For $N = 10^5$ this is 0.003, a fraction of a percent. For a sample with $10^{23}$ atoms it is about $3\times10^{-12}$, far below what any instrument can see.

## Equipartition and temperature

<div data-videos="KthbNCxnj2g b8n1k3Iob0Q uoieTQ3Qb3M MCRHXHskWnE"></div>

A simulation has no thermometer. It has positions and velocities. So what does the program mean when it prints "300 K"? The answer is that temperature is a measure of the average kinetic energy per degree of freedom. This section derives that statement, which is called equipartition, and then the formula that every MD code uses.

Two terms first. A **degree of freedom** (Module 2) is one independent way in which the system can move, described by one number. Each atom has three for its motion: the $x$, $y$ and $z$ components of its momentum.

A term is **quadratic** in a variable when it is a constant times the square of that variable. The kinetic energy of one momentum component, $p_x^2/2m$, is quadratic in $p_x$, with the constant $a = 1/2m$. The energy of a spring, $\tfrac12kx^2$, is quadratic in the stretch $x$, with $a = k/2$.

For any degree of freedom that appears in $H$ as a quadratic term $a x^2$,

$$
\langle a x^2\rangle = \frac{\int a x^2 e^{-\beta a x^2}dx}{\int e^{-\beta a x^2}dx} = \frac{1}{2}k_BT .
$$

<div class="legend" markdown="1">
- $x$: the variable of one degree of freedom. It can be a momentum component or the stretch of a spring. It is not necessarily a position.
- $a$: a positive constant, $1/2m$ for a momentum component and $k/2$ for a spring of stiffness $k$.
- $ax^2$: the energy stored in this degree of freedom.
- $\langle ax^2\rangle$: its average in the canonical ensemble.
- $e^{-\beta ax^2}$: the Boltzmann factor of this term alone.
- $\int\dots dx$: an integral over all values of $x$, from $-\infty$ to $+\infty$.
- The fraction: the numerator adds up "energy times weight", the denominator adds up the weights. Dividing by the total weight makes an average, as dividing by $Q$ did before.
- $\tfrac12k_BT$: half the thermal energy, 1.247 kJ/mol at 300 K.
</div>

Where the fraction comes from. The average of any quantity is the integral of that quantity times the Boltzmann factor $e^{-\beta H}$ over all of phase space, divided by the same integral without the quantity. $H$ is a sum of terms, so $e^{-\beta H}$ is a product of factors, and one of them is $e^{-\beta ax^2}$. All the other factors do not contain $x$, so they appear in the numerator and in the denominator and cancel. Only the integrals over $x$ remain.

How to evaluate it. Both integrals are Gaussian integrals from the box above, with $\beta a$ in the place of $a$:

$$
\int_{-\infty}^{\infty} a x^2\,e^{-\beta a x^2}\,dx = a\cdot\frac{1}{2\beta a}\sqrt{\frac{\pi}{\beta a}} = \frac{1}{2\beta}\sqrt{\frac{\pi}{\beta a}},
\qquad
\int_{-\infty}^{\infty} e^{-\beta a x^2}\,dx = \sqrt{\frac{\pi}{\beta a}} .
$$

<div class="legend" markdown="1">
- $\int_{-\infty}^{\infty}$: the integral over the whole line.
- $\pi$: the number 3.14159...
- $\beta a$: the constant that multiplies $x^2$ in the exponent.
- Other symbols: as in the list above.
</div>

Divide the first by the second. The square roots cancel and $1/(2\beta) = \tfrac12k_BT$ is left.

Read it like this. The constant $a$ has dropped out. A heavy atom and a light one, a stiff spring and a soft one: each quadratic degree of freedom holds $\tfrac12k_BT$ on average, which is 1.247 kJ/mol at 300 K. Thermal energy is shared out in equal parts, and that is what "equipartition" means. A heavy atom has the same average kinetic energy as a light one and therefore moves more slowly.

Two limits. The result holds for classical mechanics only (Exercise 1 looks at where quantum mechanics changes it). And it holds for quadratic terms only. The potential energy of a torsion angle or of a non-bonded contact is not quadratic, and its average is in general not $\tfrac12k_BT$. The kinetic energy is always quadratic in the momenta, so for the kinetic energy the result is safe.

### The temperature of a simulation

Each momentum component contributes $\tfrac12k_BT$ of kinetic energy, so $\langle K\rangle = \tfrac12 N_{df}k_BT$. MD codes turn this around to *define* the instantaneous temperature:

$$
T_{inst} = \frac{2K}{N_{df}k_B},\qquad N_{df} = 3N - N_{constraints} - 3 .
$$

<div class="legend" markdown="1">
- $T_{inst}$: the **instantaneous temperature**, the number the program computes at one time step, in K.
- $K$: the total kinetic energy at that time step, $\sum_i \tfrac12 m_iv_i^2$, in kJ/mol. Here $K$ is not a binding constant.
- $\langle K\rangle$ (in the sentence above): the average of $K$ over the ensemble.
- $N_{df}$: the number of degrees of freedom that carry kinetic energy.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $N$: the number of atoms. $3N$ is the number of momentum components.
- $N_{constraints}$: the number of constraints, for example bond lengths that are held rigid (Module 9). Each constraint removes one independent way of moving.
- The last 3: the three components of the total momentum (see below).
</div>

"Turning it around" means solving for $T$. From $\langle K\rangle = \tfrac12N_{df}k_BT$ you get $T = 2\langle K\rangle/(N_{df}k_B)$. The program applies this formula to the kinetic energy of a single time step, without the average, and calls the result $T_{inst}$. Only the average of $T_{inst}$ over many steps is the temperature.

Example: 1,000 atoms without constraints have $N_{df} = 3000 - 3 = 2997$. At 300 K their average kinetic energy is $\tfrac12\times2997\times2.494 = 3737$ kJ/mol. If at some step the kinetic energy happens to be 3800 kJ/mol, the program prints $T_{inst} = 2\times3800/(2997\times0.0083145) = 305.0$ K.

The 3 accounts for the conserved total momentum in a periodic box. $T_{inst}$ fluctuates even at perfect equilibrium, with relative standard deviation $\sqrt{2/N_{df}}$ in the canonical ensemble. For 100 atoms that is 8 %, for 100,000 atoms 0.26 %.

On the first sentence: Module 2 showed that the total momentum of all atoms is conserved in a periodic box, and the program keeps it at zero. Its three components are therefore not free to take up thermal energy, and three of the $3N$ momentum components do not count. On the second: "relative standard deviation" is the standard deviation divided by the mean. For 100 atoms at 300 K, 8 % means that $T_{inst}$ wanders by about 25 K around 300 K, and this is correct behaviour. For 100,000 atoms the wandering is below 1 K.

<details markdown="1"><summary>Optional: where $\sqrt{2/N_{df}}$ comes from</summary>
In the canonical ensemble the kinetic energy behaves as a sum of $N_{df}$ independent terms of the form $p^2/2m$, and each $p$ is a Gaussian random variable. For a Gaussian variable $x$ with mean zero and variance $\sigma^2$, the mean of $x^2$ is $\sigma^2$ and the mean of $x^4$ is $3\sigma^4$. The variance of $x^2$ is therefore $3\sigma^4 - \sigma^4 = 2\sigma^4$, twice the square of its mean. Each kinetic term has the mean $\tfrac12k_BT$, so its variance is $2\times(\tfrac12k_BT)^2 = \tfrac12(k_BT)^2$.

Means and variances of independent terms add. The sum $K$ has the mean $\tfrac12N_{df}k_BT$ and the variance $\tfrac12N_{df}(k_BT)^2$. Its standard deviation is $\sqrt{N_{df}/2}\;k_BT$. Dividing by the mean gives $\sqrt{N_{df}/2}\,\big/\,(N_{df}/2) = \sqrt{2/N_{df}}$. $T_{inst}$ is proportional to $K$, so it has the same relative standard deviation.
</details>

### The distribution of velocities

The velocity of each atom follows the Maxwell-Boltzmann distribution: each Cartesian component is Gaussian with variance $k_BT/m$. Initial velocities are drawn from it.

This follows from the momentum part of the Boltzmann factor. ("Cartesian component" means the $x$, $y$ or $z$ part of the velocity.) For one component, $e^{-\beta p_x^2/2m}$ with $p_x = mv_x$ becomes $e^{-mv_x^2/2k_BT}$. Compare this with the Gaussian $e^{-x^2/2\sigma^2}$ of the maths box: the variance is $\sigma^2 = k_BT/m$. With its normalising constant, the probability density of one velocity component is

$$
P(v_x) = \sqrt{\frac{m}{2\pi k_BT}}\;e^{-m v_x^2/2k_BT} .
$$

<div class="legend" markdown="1">
- $v_x$: the $x$ component of the velocity of one atom, in nm/ps. The same formula holds for $v_y$ and $v_z$.
- $P(v_x)$: the probability density of $v_x$. $P(v_x)\,dv_x$ is the probability of finding the component between $v_x$ and $v_x+dv_x$. Here $P$ is not a pressure.
- $m$: the mass of the atom.
- $k_BT$: the thermal energy.
- The square root in front: the normalising constant, which makes the area under the curve equal to 1.
</div>

Read it like this. The curve is centred on zero: an atom is as likely to move to the left as to the right. Its width is the standard deviation $\sqrt{k_BT/m}$. For a carbon atom (12 u) at 300 K that is $\sqrt{2.494/12} = 0.456$ nm/ps, or 456 m/s.

For a hydrogen atom (1 u) it is 1.58 nm/ps. Light atoms are faster, in agreement with equipartition: $\tfrac12m\langle v_x^2\rangle = \tfrac12m\,(k_BT/m) = \tfrac12k_BT$ for both.

The units work out without a conversion factor because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$. "Drawn from it" means that at the start of a run the program gives each velocity component of each atom a Gaussian [random number](maths.html#random-numbers) with this standard deviation.

## Pressure and the virial

<div data-videos="2BJYXuZZK3c jny9W7NtlK4"></div>

Pressure is the force that a fluid exerts on each unit of area of the wall of its container. A simulation box with periodic boundaries has no walls (Module 7): an atom that leaves through one face comes back in through the opposite one. So the program needs a formula that gives the pressure from what happens inside the box: the positions, the velocities and the forces. That formula is the virial equation.

<div class="box physics" markdown="1">
**Physics you need here: pressure.** In a gas, the pressure on a wall comes from molecules that hit the wall and bounce back. Each bounce gives the wall a small push. More molecules per volume, or faster molecules, give more pushes and harder ones. For molecules that do not interact with each other this leads to the ideal gas law, $PV = Nk_BT$: the pressure $P$ is the number of molecules per volume, $N/V$, times the thermal energy $k_BT$.

In a liquid the molecules also pull and push on each other all the time, and these forces change the pressure. Pressure is an energy per volume. In MD units, 1 kJ mol$^{-1}$ nm$^{-3}$ is 16.6 bar, and 1 bar is close to the pressure of the atmosphere. More in the [primer](physics.html#pressure).
</div>

Using $P = k_BT\,\partial\ln Q/\partial V$ and scaling the coordinates with the box gives the **virial equation**:

$$
P = \frac{N k_BT}{V} + \frac{1}{3V}\Big\langle \sum_i \mathbf r_i\cdot\mathbf F_i\Big\rangle
= \frac{1}{3V}\Big\langle 2K + \sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}\Big\rangle .
$$

<div class="legend" markdown="1">
- $P$: the pressure. In MD units it comes out in kJ mol$^{-1}$ nm$^{-3}$. Multiply by 16.6 to get bar.
- $N$: the number of atoms. $V$: the volume of the box. $k_BT$: the thermal energy.
- $\langle\ \rangle$: the average over the ensemble, in practice over the frames of the trajectory.
- $\sum_i$: a sum over all atoms.
- $\mathbf r_i$: the position of atom $i$. $\mathbf F_i$: the total force on atom $i$.
- $\mathbf r_i\cdot\mathbf F_i$: the dot product of the two vectors, $x_iF_{ix}+y_iF_{iy}+z_iF_{iz}$, a single number.
- $K$: the total kinetic energy.
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once.
- $\mathbf r_{ij} = \mathbf r_i-\mathbf r_j$: the vector that points from atom $j$ to atom $i$.
- $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$ (Module 2).
- The factor 3 in $1/3V$: the number of dimensions of space.
</div>

The first term is the ideal-gas pressure. The second, the virial, is the contribution of the interactions: attractive forces lower the pressure, repulsive ones raise it. The pair form on the right is the one to use with periodic boundaries.

Read it like this. Look at one pair in the form on the right. $\mathbf r_{ij}$ points from $j$ to $i$. If the pair repels, the force on $i$ points away from $j$, along $\mathbf r_{ij}$, and the dot product is positive: the pressure goes up. If the pair attracts, the force on $i$ points towards $j$, against $\mathbf r_{ij}$, the dot product is negative, and the pressure goes down.

This matches intuition. Molecules that push each other apart push harder on the walls, and molecules that hold on to each other push less.

An illustration with round numbers. At 100 atoms per nm$^3$, which is about the density of a liquid, and 300 K, the first term is $100\times2.494 = 249$ kJ mol$^{-1}$ nm$^{-3}$, about 4,100 bar. For the total to come out at 1 bar, the virial term must cancel this almost exactly. The pressure of a liquid is a small difference between two large numbers, which helps to explain why the instantaneous pressure fluctuates so strongly (Module 8).

**From the first form to the second.** Two steps. *The kinetic term.* By equipartition the average kinetic energy is $\langle K\rangle = \tfrac32Nk_BT$, three momentum components per atom. This is for atoms without constraints, and it leaves out the three degrees of freedom of the total momentum, a negligible correction when $N$ is large. So $Nk_BT = \tfrac13\langle 2K\rangle$.

*The pair term.* When all forces are pair forces, $\mathbf F_i = \sum_{j\ne i}\mathbf F_{ij}$ (Module 2). Each pair then appears twice in $\sum_i\mathbf r_i\cdot\mathbf F_i$, once as $\mathbf r_i\cdot\mathbf F_{ij}$ and once as $\mathbf r_j\cdot\mathbf F_{ji}$. By Newton's third law $\mathbf F_{ji} = -\mathbf F_{ij}$, so the two add up to $(\mathbf r_i-\mathbf r_j)\cdot\mathbf F_{ij} = \mathbf r_{ij}\cdot\mathbf F_{ij}$.

*Where these two steps need care.* With constraints, $\langle 2K\rangle$ is $N_{df}k_BT$, which can be well below $3Nk_BT$ (one sixth lower in the first "Check yourself" question). The first form, with $N$ counted in atoms, then no longer holds. The second form still does, if the forces that keep the constraints satisfied are counted among the pair forces. Angle and torsion terms (Module 5) act on three or four atoms at once and are not pair forces, but the forces of each such term add up to zero, so they can be written with relative positions in the same way.

**Why the pair form with periodic boundaries.** In a periodic box an atom has no unique position: $\mathbf r_i$ and $\mathbf r_i$ shifted by one box length describe the same atom, and the product $\mathbf r_i\cdot\mathbf F_i$ would change with the choice. The vector $\mathbf r_{ij}$ from an atom to the nearest copy of its partner has no such ambiguity.

<details markdown="1"><summary>Optional: where the virial equation comes from</summary>
Of the factors of $Q$, only the configurational integral $Z$ depends on the volume, so $P = k_BT\,\partial\ln Z/\partial V$. The volume enters $Z$ in two ways: through the limits of the integral (each atom is integrated over the box) and through $U$, because in a bigger box the atoms are further apart. "Scaling the coordinates with the box" makes both visible. Take a cubic box of edge $L$, so that $V = L^3$, and write each position as $\mathbf r_i = L\,\mathbf u_i$, where every component of the scaled position $\mathbf u_i$ runs from 0 to 1. Each $d\mathbf r_i$ becomes $L^3\,d\mathbf u_i = V\,d\mathbf u_i$, and

$$
Z = V^N\int d\mathbf u^N\,e^{-\beta U(L\mathbf u)} .
$$

Now the limits of the integral are fixed. Take the logarithm, $\ln Z = N\ln V + \ln\int d\mathbf u^N e^{-\beta U}$, and differentiate with respect to $V$. The first term gives $N/V$. The second gives the average of $-\beta\,\partial U/\partial V$, by the same steps as for $\langle E\rangle$ in the previous section:

$$
\frac{\partial\ln Z}{\partial V} = \frac{N}{V} - \beta\left\langle\frac{\partial U}{\partial V}\right\rangle .
$$

To find $\partial U/\partial V$, use the chain rule: $U$ changes because every atom moves when the box grows while its $\mathbf u_i$ stays fixed. Since $L = V^{1/3}$, the derivative is $dL/dV = L/3V$, and so $\partial\mathbf r_i/\partial V = \mathbf u_i\,L/3V = \mathbf r_i/3V$. With $\nabla_iU = -\mathbf F_i$ (the gradient of $U$ with respect to the position of atom $i$ is minus the force on that atom, Module 2),

$$
\frac{\partial U}{\partial V} = \sum_i\nabla_iU\cdot\frac{\partial\mathbf r_i}{\partial V} = -\frac{1}{3V}\sum_i\mathbf r_i\cdot\mathbf F_i .
$$

Insert this and multiply by $k_BT$, remembering that $k_BT\,\beta = 1$. The result is $P = Nk_BT/V + \frac{1}{3V}\langle\sum_i\mathbf r_i\cdot\mathbf F_i\rangle$, the first form of the virial equation.
</details>

## Why a time average equals an ensemble average

<div data-videos="rBni87N8cBs WneHzwWh0Ws Iq9ZxMRbpmc"></div>

All the averages so far were averages over an ensemble: over every microstate, each weighted by its probability. A simulation does not produce that. It produces one system, followed through time. This section says when the two give the same number. That they do is the assumption behind every result of MD.

A picture of the two kinds of average. You want to know what fraction of their time the people of a city spend at work. You could photograph the whole city at one instant and count: an average over the ensemble of people. Or you could follow one person for a year and add up the hours: a time average.

The two agree if that one person, over the year, goes through all the situations that occur in the population, in the same proportions. They disagree if the person you follow never leaves one district during your year, and that is the way in which MD fails, as described below.

An experiment measures a time average over a huge number of molecules. Statistical mechanics gives the ensemble average

$$
\langle A\rangle = \int d\Gamma\,A(\Gamma)\,P(\Gamma).
$$

<div class="legend" markdown="1">
- $A$: any **observable**, a quantity that can be computed from one microstate, such as a distance, an energy or the radius of a protein. Here $A$ is not the free energy.
- $A(\Gamma)$: the value of the observable in the microstate $\Gamma$.
- $P(\Gamma)$: the probability density of the microstate $\Gamma$. In the canonical ensemble it is $e^{-\beta H(\Gamma)}$ divided by the integral of $e^{-\beta H}$ over all microstates.
- $\int d\Gamma$: the integral over all microstates, the same as $\int d\mathbf r^N\,d\mathbf p^N$.
- $\langle A\rangle$: the ensemble average of $A$.
</div>

In words: go through all microstates, multiply the value of $A$ in each by the probability of that microstate, and add. It is the continuous version of $\langle A\rangle = \sum_s A_sP(s)$.

MD computes a time average along one trajectory. The **ergodic hypothesis** says the two agree for an infinitely long trajectory:

$$
\langle A\rangle = \lim_{\tau\to\infty}\frac{1}{\tau}\int_0^{\tau}A(\Gamma(t))\,dt \;\approx\; \frac{1}{M}\sum_{n=1}^{M}A(\Gamma(t_n)).
$$

<div class="legend" markdown="1">
- $\Gamma(t)$: the microstate of the simulated system at the time $t$. This function of time is the trajectory.
- $A(\Gamma(t))$: the value of the observable at the time $t$.
- $\tau$ (Greek tau): the length of the trajectory.
- $\frac{1}{\tau}\int_0^{\tau}\dots dt$: the time average. Add up the values of $A$ along the trajectory and divide by its length.
- $\lim_{\tau\to\infty}$: the limit in which the trajectory becomes infinitely long.
- $M$: the number of saved frames (snapshots) of the trajectory.
- $t_n$: the time of frame number $n$, with $n$ running from 1 to $M$.
- $\frac{1}{M}\sum_{n=1}^{M}$: the mean over the frames.
- $\approx$: "is approximately equal to", because $M$ is finite.
</div>

Read it like this. The first equals sign is the hypothesis. The part after the sign $\approx$ is what you compute in practice. A simulation saves a finite number $M$ of frames, and the integral over time becomes a sum over the frames divided by their number:

```python
import numpy as np
# A_frames[n] is the value of the observable in frame n of the trajectory
A_mean = np.mean(A_frames)   # the estimate of <A>
```

No Boltzmann factor appears in the sum over frames. None is needed, because the weight is already in the trajectory: the dynamics visits each region of phase space in proportion to its probability, so microstates of low energy turn up among the frames more often. Multiplying each frame by $e^{-\beta H}$ would count the weight twice.

This is the single most important equation for using MD, and its weak point is the word "infinitely". A system with high barriers is ergodic in principle but not on the time scale you can afford. If your protein has two conformations separated by a barrier that is crossed once per millisecond, a microsecond trajectory samples one of them and the "average" is wrong, with no warning. Module 11 covers how to detect this and Module 14 how to fight it.

Three words in this paragraph need a definition. A system is **ergodic** when one trajectory, given enough time, visits every accessible region of phase space with the frequency that the ensemble assigns to it. A **barrier** is a region of high energy that lies between two regions of low energy. By the Boltzmann factor the system is rarely found on top of it, so it rarely crosses. And "hypothesis" is the honest word: for realistic systems ergodicity cannot be proved, and it is assumed.

Note what is *not* required: the trajectory does not need to be the true physical trajectory. Any dynamics that visits microstates with the right probability gives correct equilibrium averages. That is why thermostats that perturb the dynamics, Monte Carlo moves, and replica exchange are all legitimate for thermodynamics, while kinetic quantities need more care.

The methods named here all change how the system moves from one microstate to the next. A thermostat alters the velocities (Module 8). A Monte Carlo move changes the configuration at random and is accepted or rejected by a rule built to give the Boltzmann distribution. Replica exchange swaps configurations between copies of the system that run under different conditions, most often at different temperatures (Module 14). When they are built correctly, none of them changes how often each microstate is visited, so averages come out right.

**Kinetic quantities** are those that answer "how fast?": rate constants, diffusion coefficients, relaxation times. They depend on the true motion, and a method that alters the motion can distort them.

The demo below shows this section in one picture. One particle moves in a one-dimensional potential under thermal noise. The histogram of the positions it has visited is drawn together with the exact Boltzmann density $e^{-U/k_BT}/Z$. At a high temperature the histogram converges to the exact curve. At a low temperature the particle stays trapped in one well and the histogram is wrong, although nothing in it looks unusual.

<div class="widget" data-widget="boltzmann"></div>

## Free energy

<div data-videos="3XyGqsgBpIM Lq8GwTlJ9Z8 BznPadIkfKM mg9JWntdfyE"></div>

Which of two states is more populated: bound or unbound, folded or unfolded? The lowest energy does not decide it, and the largest number of microstates does not decide it either. A combination of the two decides it, and that combination is the free energy. This section gives the formula you will use most in practice: a free-energy difference is $-k_BT$ times the logarithm of a ratio of populations. The two subsections apply the same idea to a continuous coordinate and to binding.

<div class="box physics" markdown="1">
**Physics you need here: free energy.** A ball rolls to the place of lowest energy and stays there. A molecule at a finite temperature does not, because thermal motion keeps kicking it out. It spends most of its time where the compromise between low energy and a large number of microstates (high entropy) is best. The **Helmholtz free energy** $A = E - TS$ is the quantity that measures this compromise: a system at fixed $N$, $V$ and $T$ settles in the macrostate with the lowest $A$.

Low energy lowers $A$, high entropy lowers $A$, and the temperature sets the exchange rate between the two. At low temperature energy wins, at high temperature entropy wins.

At fixed pressure instead of fixed volume, the corresponding quantity is the **Gibbs free energy** $G = A + PV$. For processes in a liquid at 1 bar the two differ very little. 1 bar is 0.0602 kJ mol$^{-1}$ nm$^{-3}$, so a volume change of 0.1 nm$^3$ contributes $P\Delta V = 0.006$ kJ/mol. This is why the module can work with $A$ while experiments report $\Delta G$. More in the [primer](physics.html#thermodynamics).
</div>

The Helmholtz free energy $A = -k_BT\ln Q = \langle E\rangle - TS$ counts states, weighted by their Boltzmann factors.

"Counts states" can be made concrete. If every Boltzmann factor were 1, $Q = \sum_s e^{-\beta E_s}$ would be the number of microstates. With the factors in place, each microstate counts for less the higher its energy. So $Q$ is the effective number of microstates that the system can reach at this temperature, and $A$ is $-k_BT$ times the logarithm of that number. The second form, $\langle E\rangle - TS$, is derived in the optional block of the section on thermodynamics above.

The most useful form of this statement is about the relative probability of two **macrostates** A and B (two regions of configuration space, for example "bound" and "unbound", or "folded" and "unfolded"):

$$
\frac{P_B}{P_A} = \frac{\int_B e^{-\beta U}d\mathbf r}{\int_A e^{-\beta U}d\mathbf r} = \frac{Z_B}{Z_A} = e^{-\beta\,\Delta A_{A\to B}},
\qquad \Delta A = -k_BT\ln\frac{Z_B}{Z_A}.
$$

<div class="legend" markdown="1">
- A, B (as labels): the names of two macrostates. Each is a region of **configuration space**, the space of all arrangements of the atoms, without the momenta.
- $P_A$, $P_B$: the probabilities of finding the system in region A and in region B. They are also called the populations of the two states. Here $P$ is not a pressure.
- $\int_A \dots d\mathbf r$: an integral over all configurations that belong to region A. $\int_B$ likewise.
- $e^{-\beta U}$: the Boltzmann factor of a configuration with the potential energy $U$.
- $Z_A$, $Z_B$: names for the two integrals. Each is the part of the configurational integral $Z$ that comes from one region.
- $\Delta A_{A\to B}$: the Helmholtz free energy of state B minus that of state A. The arrow reads "going from A to B". In $\Delta A$ the letter $A$ is the free energy. In the subscript, A and B are the states.
- $\ln$: the natural logarithm.
</div>

The chain of equalities, link by link.

*First link.* The probability density of a configuration is $e^{-\beta U}/Z$. The probability of a macrostate is the integral of this density over all configurations that belong to it, so $P_A = Z_A/Z$ and $P_B = Z_B/Z$. In the ratio the total $Z$ cancels. The momenta can be left out because, as shown above, they contribute the same factor to every configuration.

*Second link.* Give each macrostate a free energy in the same way as the whole system: $-k_BT\ln Z_A$ for A and $-k_BT\ln Z_B$ for B. (The factors $N!$ and $\Lambda$ are the same for both and drop out of the difference.) The difference is $\Delta A = -k_BT\ln Z_B + k_BT\ln Z_A = -k_BT\ln(Z_B/Z_A)$, by the rule for the logarithm of a ratio. That is the formula on the right.

*Third link.* Divide that formula by $-k_BT$ and take the exponential of both sides: $Z_B/Z_A = e^{-\beta\Delta A}$.

Combine the first and the last member of the chain:

$$
\Delta A_{A\to B} = -k_BT\,\ln\frac{P_B}{P_A} .
$$

<div class="legend" markdown="1">
- $P_B/P_A$: the ratio of the populations of the two states, a pure number.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- Other symbols: as in the list above.
</div>

Read it like this. A free-energy difference is a ratio of populations, written on a logarithmic scale in units of $k_BT$. If you can count how often a simulation is in A and how often in B, you have their free-energy difference.

Numbers for 300 K: equal populations mean $\Delta A = 0$. A ratio of 10 to 1 in favour of B means $\Delta A = -2.494\times\ln10 = -5.7$ kJ/mol, or $-1.4$ kcal/mol. A ratio of 100 to 1 means $-11.5$ kJ/mol, and every further factor of 10 adds another $-5.7$ kJ/mol.

<div class="box key" markdown="1">
**Energy against entropy, a two-state example.** State A is one conformation with energy 0. State B has energy $+10$ kJ/mol but consists of 1,000 conformations of equal energy. At 300 K, $Z_A = 1$ and $Z_B = 1000\,e^{-10/2.494} = 18.1$, so $\Delta A = -2.494\ln 18.1 = -7.2$ kJ/mol: B is favoured 18 to 1 although its energy is higher. The entropy term is $-T\Delta S = -k_BT\ln 1000 = -17.2$ kJ/mol. Looking at energies of single structures, which is what most scoring functions do, would get the sign wrong.

The steps. The conformations form a list here, so each $Z$ is a sum of Boltzmann factors instead of an integral. State A has one conformation with the factor $e^{0} = 1$, so $Z_A = 1$.

Each conformation of B has the factor $e^{-10/2.494} = e^{-4.01} = 0.0181$: taken alone, it is 55 times less probable than A. But there are 1,000 of them, so $Z_B = 1000\times0.0181 = 18.1$. The populations are $1/(1+18.1)$, which is 5 %, for A and $18.1/(1+18.1)$, which is 95 %, for B.

The same result split into energy and entropy with $\Delta A = \Delta E - T\Delta S$. The energy term is $\Delta E = +10$ kJ/mol, against B. The entropy difference is $\Delta S = k_B\ln(1000/1)$, so $-T\Delta S = -2.494\times6.908 = -17.2$ kJ/mol, in favour of B. The sum is $10 - 17.2 = -7.2$ kJ/mol.

A scoring function is a formula that gives one structure a score, for example to estimate how well a ligand binds. It sees the $+10$ and misses the $-17.2$.
</div>

**Why free energies are hard.** An average like $\langle U\rangle$ is dominated by the configurations the simulation visits most. The free energy is different. One can write

$$
e^{+\beta A_{config}} \propto \frac{1}{Z} = \frac{\langle e^{+\beta U}\rangle}{V^N},
$$

an average dominated by the *high*-energy configurations that a Boltzmann-weighted simulation almost never visits.

<div class="legend" markdown="1">
- $A_{config}$: the configurational part of the free energy, $-k_BT\ln Z$. It is the part that depends on the interactions.
- $e^{+\beta A_{config}}$: by that definition this is $1/Z$.
- $\propto$: "is proportional to". With the definition of $A_{config}$ given here the two sides are equal. The weaker sign covers other conventions, which put a constant factor such as $V^N$ into the definition.
- $Z$: the configurational integral.
- $\langle e^{+\beta U}\rangle$: the average of the quantity $e^{+\beta U}$ over the configurations of a canonical simulation. Mind the plus sign in the exponent.
- $U$: the potential energy of a configuration.
- $V^N$: the volume of the box to the power $N$, the number of atoms.
</div>

Where the right-hand side comes from. Write out the average of $e^{+\beta U}$: it is the integral of that quantity times the probability density $e^{-\beta U}/Z$ of the configurations.

$$
\langle e^{+\beta U}\rangle = \frac{1}{Z}\int d\mathbf r^N\,e^{+\beta U}\,e^{-\beta U} = \frac{1}{Z}\int d\mathbf r^N\,1 = \frac{V^N}{Z} .
$$

<div class="legend" markdown="1">
- $\int d\mathbf r^N$: the integral over the positions of all $N$ atoms, each over the box.
- $e^{+\beta U}\,e^{-\beta U}$: the two exponentials multiply to $e^0 = 1$.
- $\int d\mathbf r^N\,1$: the integral of the number 1. Each atom contributes the volume $V$ of the box, which gives $V^N$.
- Other symbols: as in the list above.
</div>

Dividing both sides by $V^N$ gives $1/Z = \langle e^{+\beta U}\rangle/V^N$.

Read it like this. In principle you could get $Z$, and with it the absolute free energy, by averaging $e^{+\beta U}$ over a trajectory. In practice that average does not converge.

$e^{+\beta U}$ is astronomically large for configurations of high energy, for example two atoms on top of each other, and the simulation visits such configurations with a probability that is astronomically small. In the exact average the huge value and the tiny probability multiply to the same contribution for every configuration. Almost all configurations are of this high-energy kind, and a real run never sees them, so almost all of the average is missing.

Compare this with $\langle U\rangle$, where the configurations that contribute most are also the most probable ones, so the trajectory samples what matters.

Absolute free energies are therefore out of reach, and practical methods compute *differences* between states that are made to overlap (Modules 12 and 13).

Two states **overlap** when a simulation of one also visits configurations that are typical of the other. Only then can the two be compared within one calculation. When the states of interest do not overlap, the methods of Modules 12 and 13 put a chain of intermediate states between them, each of which overlaps with the next.

### The potential of mean force

<div data-videos="pjT7waGUGDI"></div>

The two-state formula needs you to decide in advance what "A" and "B" are. It is often more informative to keep one continuous coordinate and ask for the free energy at every value of it, for example as a function of the distance between a ligand and its pocket. That function is the potential of mean force. The recipe is the two-state formula applied to every bin of a histogram: count how often the coordinate has each value, take the logarithm, multiply by $-k_BT$.

Often we care about one coordinate $\xi(\mathbf r)$, a distance, an angle, or a fraction of native contacts, and want the free energy as a function of it. Its probability density is obtained by integrating out everything else:

$$
P(\xi') = \frac{1}{Z}\int d\mathbf r\;\delta\big(\xi(\mathbf r)-\xi'\big)\,e^{-\beta U(\mathbf r)},
\qquad
W(\xi') = -k_BT\ln P(\xi') + \text{const}.
$$

<div class="legend" markdown="1">
- $\xi$ (Greek xi): one number computed from the positions of many atoms. Such a coordinate is called a **collective variable** or a reaction coordinate (Module 12).
- $\xi(\mathbf r)$: the rule that computes the coordinate from the configuration $\mathbf r$.
- $\xi'$: one particular value of the coordinate, the value at which you ask for the density. The prime only separates the value from the rule.
- $P(\xi')$: the probability density of the coordinate. $P(\xi')\,d\xi$ is the fraction of the time that the coordinate spends between $\xi'$ and $\xi'+d\xi$. Here $P$ is not a pressure.
- $\delta\big(\xi(\mathbf r)-\xi'\big)$: the Dirac delta function. It is zero unless the configuration $\mathbf r$ has the coordinate value $\xi'$.
- $\int d\mathbf r$: the integral over all configurations.
- $e^{-\beta U(\mathbf r)}/Z$: the probability density of the configuration $\mathbf r$.
- $W(\xi')$: the potential of mean force at the value $\xi'$, in kJ/mol.
- const: a constant that can be chosen freely (see below).
</div>

Two of the examples in the first sentence need a word. A "fraction of native contacts" is the fraction of the atom pairs touching in the folded structure that are also touching in the present configuration. And "integrating out everything else" means: add up the probabilities of all configurations that share the same value of $\xi$, whatever the other degrees of freedom are doing. The delta function does the selecting (see the box in the first section).

In practice you never evaluate this integral. You take a trajectory, compute $\xi$ for every frame and make a histogram. The height of a bin, divided by the number of frames and by the width of the bin, is the estimate of $P$ at that value.

*The constant.* $P(\xi')$ has a unit (one over the unit of $\xi$), and the logarithm of a quantity with a unit is defined only up to an added constant: changing the unit of length from nm to Å shifts all of $W$ by the same amount. This does no harm, because only differences of $W$ between two values of $\xi$ have a meaning. The usual choice puts $W = 0$ at the lowest point of the curve or, when the curve becomes flat at large separation, on that flat part.

Read it like this. Where the coordinate is found often, $W$ is low: the wells of $W$ are the populated states. Where it is found rarely, $W$ is high: these are the barriers. If a distance is found near 0.5 nm a hundred times more often than near 0.8 nm, then $W(0.8) - W(0.5) = k_BT\ln100 = 11.5$ kJ/mol at 300 K.

$W(\xi)$ is the **potential of mean force (PMF)**. The name comes from the fact that, for a Cartesian-like coordinate, its slope is the average force along $\xi$: $-dW/d\xi = \langle F_\xi\rangle_\xi$. Its barriers and wells are free energies: they contain the entropy of all the other degrees of freedom, including the solvent.

<div class="legend" markdown="1">
- $dW/d\xi$: the slope of the PMF.
- $F_\xi$: the force along the coordinate $\xi$ in one configuration.
- $\langle\ \rangle_\xi$: an average over all configurations in which the coordinate has the value $\xi$, with all other degrees of freedom free.
- Cartesian-like coordinate: a coordinate measured along a straight line, such as the $x$ position of an atom.
</div>

The last sentence deserves attention. A point on the curve $W(\xi)$ is not one structure. It stands for all configurations that share this value of $\xi$, including every arrangement of the water. A well can be deep because the energy is low there, or because very many arrangements exist there. $W$ alone does not say which.

<details markdown="1"><summary>Optional: why the slope of $W$ is the mean force</summary>
Take the simplest case: $\xi$ is the $x$ coordinate of atom 1. The delta function then fixes $x_1 = x'$, and the integral runs over all the other coordinates, written $\mathbf r_{rest}$:

$$
P(x') = \frac{1}{Z}\int d\mathbf r_{rest}\;e^{-\beta U(x',\mathbf r_{rest})} .
$$

Differentiate $W = -k_BT\ln P$ with respect to $x'$. The derivative of $\ln P$ is $(1/P)\,dP/dx'$ (chain rule), and the derivative of $e^{-\beta U}$ with respect to $x'$ is $-\beta\,(\partial U/\partial x_1)\,e^{-\beta U}$:

$$
-\frac{dW}{dx'} = \frac{k_BT}{P}\frac{dP}{dx'} = \frac{\int d\mathbf r_{rest}\,\left(-\dfrac{\partial U}{\partial x_1}\right)e^{-\beta U}}{\int d\mathbf r_{rest}\,e^{-\beta U}} .
$$

The product $k_BT\,\beta = 1$ has dropped out, and so has $1/Z$. The right side is the average of $-\partial U/\partial x_1$, which is the force on atom 1 along $x$, over all arrangements of the other atoms while atom 1 is held at $x'$. So $W$ is the potential whose slope gives the *mean* force, which explains the name.
</details>

For a curvilinear coordinate there is an extra geometric (Jacobian) term. The important case is a distance $r$: the volume available grows as $4\pi r^2$, so $P(r)\propto r^2 g(r)$, where $g(r)$ is the pair distribution function. Two "PMFs" along a distance are therefore in use, and they differ by $2k_BT\ln r$:

$$
w(r) = -k_BT\ln g(r)\qquad\text{and}\qquad W(r) = -k_BT\ln P(r) = w(r) - 2k_BT\ln r + \text{const}.
$$

<div class="legend" markdown="1">
- $r$: the distance between two particles, in nm.
- $g(r)$: the pair distribution function, explained in the box below.
- $w(r)$: the PMF computed from $g(r)$. It is zero wherever $g = 1$.
- $P(r)$: the probability density of the distance. $P(r)\,dr$ is the probability that the distance lies between $r$ and $r+dr$.
- $W(r)$: the PMF computed from the plain histogram of the distance.
- $2k_BT\ln r$: the geometric (Jacobian) term, the difference between the two.
- const: a constant that can be chosen freely.
</div>

The words first. A **curvilinear** coordinate is one that is not measured along a straight line: a distance, an angle. The **Jacobian** is the factor that says how much volume of configuration space belongs to one unit of the coordinate.

For a distance the picture is simple. All points at a distance between $r$ and $r+dr$ from a centre form a spherical shell. The area of a sphere is $4\pi r^2$, so the volume of the shell is $4\pi r^2\,dr$, and it grows with $r$. Two particles are found at a large distance more often than at a small one for the plain reason that there is more room out there.

<div class="box physics" markdown="1">
**Physics you need here: the pair distribution function $g(r)$.** Sit on one particle and look at the others around it. Count how many of them lie in a thin spherical shell between the distances $r$ and $r+dr$, and average the count over time and over all the particles you could sit on. Then divide by the number you would expect if the particles were spread evenly with their average density $\rho$ (Greek rho, particles per nm$^3$). That number is $\rho\times4\pi r^2\,dr$, the density times the volume of the shell. The ratio is $g(r)$.

So $g(r)$ compares the real structure with a structureless one. $g = 1$ means "as many neighbours as in an even spread". $g > 1$ means that this distance is preferred, $g < 1$ that it is avoided.

In a liquid, $g(r) = 0$ at very short distances, because two atoms cannot overlap. It has a peak at the distance of the nearest neighbours and tends to 1 at large distances, where the particles no longer feel each other. It is also called the radial distribution function. Module 11 shows how to compute it from a trajectory.
</div>

Where the formula comes from. The number of partners in a shell is proportional to $g(r)$ times the volume of the shell, so $P(r)\propto r^2g(r)$. Take $-k_BT\ln$ of both sides. The logarithm of a product is a sum, and $\ln r^2 = 2\ln r$, so $-k_BT\ln P(r) = -k_BT\ln g(r) - 2k_BT\ln r + \text{const}$. The first term on the right is $w(r)$.

Read it like this. For two particles that do not interact at all, $g = 1$ and $w = 0$ at every distance, as you would wish for "no interaction". But $W(r) = -2k_BT\ln r$ still falls as $r$ grows: large distances are more populated because the shells are bigger.

That fall is an effect of entropy. No force between the particles is involved. Between $r = 1$ and $r = 2$ nm the term changes by $2k_BT\ln2 = 3.5$ kJ/mol at 300 K, which is not small next to the effects one looks for.

$w(r)$ is the one whose slope is exactly the mean force between the two particles and which goes to zero at large separation. Always check which of the two a paper or a program reports (Module 12).

One more warning about the letters. Module 12 writes capital $W(r)$ for the profile with the geometric term removed, that is, for the $w(r)$ of this module, because there the small letter is needed for something else.

### Binding constants

<div data-videos="Srj-ZqBzNv4"></div>

The number that an experiment reports for binding is a binding constant. This subsection connects it to the PMF, and with that to something a simulation can compute.

<div class="box physics" markdown="1">
**Physics you need here: the binding constant.** A protein P and a ligand L in solution keep meeting, sticking together and coming apart: $\text{P} + \text{L}\rightleftharpoons \text{PL}$. The double arrow means that both directions go on all the time. At equilibrium the concentrations no longer change. Square brackets denote a concentration, the number of molecules (or of moles) per volume. $[\text{PL}]$ is the concentration of the complex.

The **association constant** $K_a = [\text{PL}]/([\text{P}][\text{L}])$ is large when binding is strong. Its unit is one over a concentration, which is a volume: litres per mole, or nm$^3$ per molecule. Its inverse, the **dissociation constant** $K_d = 1/K_a$, is a concentration, and it is the number experiments usually report.

Its meaning: when the concentration of free ligand equals $K_d$, half of the protein molecules carry a ligand. A small $K_d$ (nanomolar) is tight binding, a large one (millimolar) is weak binding. More in the [primer](physics.html#equilibrium).
</div>

For $\text{P} + \text{L}\rightleftharpoons \text{PL}$, the association constant is a ratio of partition functions. If $w(r) = -k_BT\ln g_{PL}(r)$ is the radial PMF along the separation of the two partners (the $g(r)$-type PMF defined above, with $w\to0$ at large distance), then to a good approximation

$$
K_a = \frac{[\text{PL}]}{[\text{P}][\text{L}]} = 4\pi\int_{bound} r^2\,e^{-\beta w(r)}\,dr,
\qquad
\Delta G^\circ_{bind} = -k_BT\ln\big(K_a C^\circ\big),\qquad K_d = 1/K_a .
$$

<div class="legend" markdown="1">
- P, L, PL: the protein, the ligand and their complex. Here P is the name of a molecule, not a pressure or a probability.
- $[\ ]$: the concentration of the molecule named inside, in molecules per nm$^3$ or in mol/L.
- $K_a$: the association constant, a volume. $K_d$: the dissociation constant, a concentration.
- $r$: the distance between the protein and the ligand.
- $g_{PL}(r)$: the pair distribution function of the ligand around the protein.
- $w(r)$: the PMF computed from $g_{PL}(r)$, which goes to zero ($w\to0$) at large distance.
- $e^{-\beta w(r)}$: equal to $g_{PL}(r)$. It says how much more likely the ligand is at the distance $r$ than it would be without any interaction.
- $4\pi r^2\,dr$: the volume of the spherical shell at the distance $r$.
- $\int_{bound}$: the integral over the distances that count as "bound", from zero to a limit a little beyond the well of $w$.
- $\Delta G^\circ_{bind}$: the standard free energy of binding. The small circle marks the standard concentration.
- $C^\circ$: the standard concentration, 1 mol/L.
</div>

Read it like this. The integral is a volume. If protein and ligand did not interact ($w = 0$), it would be the plain volume of the region you call "bound". The attraction multiplies each shell of that region by $e^{-\beta w}$, which is larger than 1 where $w$ is negative. So $K_a$ is an effective volume: the bound region, enlarged by the Boltzmann factor of the attraction.

It is a ratio of partition functions in this sense. The integral is the configurational integral of the ligand over the bound region. And $1/C^\circ$, the volume per molecule at the standard concentration, plays the part of the configurational integral of a free ligand. The product $K_aC^\circ$ is the ratio of the two. The words "to a good approximation" cover the conditions under which the formula holds, which Module 12 states.

<div class="box key" markdown="1">
**Worked example: a square-well PMF (an illustration with round numbers).** Suppose $w(r) = -25$ kJ/mol at all distances below 0.5 nm and zero beyond, and call everything below 0.5 nm "bound". Inside the well $e^{-\beta w} = e^{25/2.494} = 22{,}560$. This is a constant, so it can be taken out of the integral. What remains is $4\pi\int_0^{0.5}r^2\,dr = \tfrac43\pi\,(0.5)^3 = 0.524$ nm$^3$, the volume of a sphere of radius 0.5 nm. So $K_a = 0.524\times22{,}560 = 11{,}800$ nm$^3$.

Multiply by $C^\circ = 0.6022$ nm$^{-3}$ to get the pure number $K_aC^\circ = 7{,}110$. This is also $K_a$ in litres per mole. Then $\Delta G^\circ_{bind} = -2.494\times\ln 7110 = -22.1$ kJ/mol, and $K_d = 1/7110$ mol/L, which is $1.4\times10^{-4}$ M or 140 µM.

The binding free energy, $-22.1$ kJ/mol, is weaker than the depth of the well, $-25$ kJ/mol. The difference, $-k_BT\ln(0.524\times0.6022) = +2.9$ kJ/mol, is the price of confining the ligand to 0.524 nm$^3$ when at 1 M it would have 1.66 nm$^3$ to itself. It is an entropy term, and it depends on the standard concentration.
</div>

$C^\circ = 1$ M $= 0.6022$ molecules per nm$^3$ is the standard concentration. It must appear because $K_a$ has units of volume: the "free energy of binding" is only defined relative to a reference concentration. Module 12 develops this fully.

The conversion: 1 M is one mole per litre. A litre is $10^{24}$ nm$^3$ and a mole is $6.022\times10^{23}$ molecules, so 1 M is 0.6022 molecules per nm$^3$, and each molecule has $1/0.6022 = 1.66$ nm$^3$ to itself. The reason $C^\circ$ must appear: a logarithm needs a pure number, and $K_a$ is a volume. Multiplying by a concentration removes the unit. A different choice of that concentration would shift $\Delta G^\circ$ by a constant, so a binding free energy always means "relative to 1 M".

## Check yourself

<details markdown="1"><summary>1. In a canonical simulation of 30,000 atoms with all bonds to hydrogen constrained (15,000 constraints), what is the expected standard deviation of the instantaneous temperature at 300 K?</summary>
$N_{df} = 90{,}000 - 15{,}000 - 3 = 74{,}997$. $\sigma_T = 300\sqrt{2/74997} = 1.55$ K. A temperature trace that fluctuates by ±1.5 K is correct. One that is flat means the thermostat is suppressing fluctuations.

Symbols: $N_{df}$ is the number of degrees of freedom, $3N$ minus the constraints minus 3. $\sigma_T$ is the standard deviation of the instantaneous temperature, equal to $T\sqrt{2/N_{df}}$.
</details>

<details markdown="1"><summary>2. Two conformations differ in free energy by 2 kcal/mol at 300 K. What are their populations?</summary>
$e^{-2/0.596} = 0.035$, so 96.6 % and 3.4 %.

The steps: 0.596 kcal/mol is $k_BT$ at 300 K. $e^{-\Delta A/k_BT} = 0.035$ is the population of the higher state divided by that of the lower one. The two populations must add up to 1, so they are $1/(1+0.035) = 0.966$ and $0.035/(1+0.035) = 0.034$.
</details>

<details markdown="1"><summary>3. Does the equilibrium distribution of a dihedral angle change if you triple the mass of every hydrogen?</summary>
No. The configurational distribution $e^{-\beta U(\mathbf r)}/Z$ contains no masses. Only dynamical properties change. (With rigid constraints there is a small mass-dependent correction, which is negligible for bond constraints.)

Symbols: $U(\mathbf r)$ is the potential energy of the configuration $\mathbf r$, $\beta = 1/k_BT$, and $Z$ is the configurational integral. "Dynamical properties" are those that involve time, such as vibration frequencies and diffusion.
</details>

<details markdown="1"><summary>4. Why can you not get an absolute entropy by averaging something over a trajectory?</summary>
Entropy is $-k_B\int P\ln P$: it depends on the value of the probability density itself, including the normalisation $Z$, which is the volume of all accessible configuration space. A trajectory gives you samples from $P$ but not the value of $Z$.

Symbols: $P$ is the probability density of the configurations, $e^{-\beta U}/Z$, and the integral runs over all configurations. More exactly, $Z$ is the volume of configuration space with every configuration weighted by its Boltzmann factor $e^{-\beta U}$. It is the plain volume $V^N$ only when $U = 0$. The formula $-k_B\int P\ln P$ is the general definition of entropy for a probability density. When $\Omega$ microstates are equally likely, each with the probability $1/\Omega$, it reduces to Boltzmann's $k_B\ln\Omega$.
</details>

<details markdown="1"><summary>5. At 300 K one microstate lies 5 kJ/mol above another. What is the ratio of their probabilities? And at 600 K?</summary>
The ratio is the Boltzmann factor of the energy difference, $e^{-\Delta E/k_BT}$. At 300 K, $k_BT = 2.494$ kJ/mol and the ratio is $e^{-5/2.494} = 0.135$. At 600 K, $k_BT = 4.988$ kJ/mol and the ratio is $e^{-5/4.988} = 0.367$. The same energy difference counts for less at the higher temperature.
</details>

<details markdown="1"><summary>6. You average an observable over the frames of an NVT trajectory. Should you multiply each frame by its Boltzmann factor first?</summary>
No. The trajectory already visits the microstates in proportion to their Boltzmann factors, so low-energy microstates appear among the frames more often. The plain mean over the frames, $\frac{1}{M}\sum_n A(\Gamma(t_n))$ with $M$ the number of frames, is the estimate of $\langle A\rangle$. Weighting again would count the Boltzmann factor twice.
</details>

<details markdown="1"><summary>7. In a histogram of a distance with equal bin widths, the bin at 0.4 nm holds 50 times more frames than the bin at 0.7 nm. What is the difference in the PMF between the two distances at 300 K, for $W(r)$ and for $w(r)$?</summary>
For the histogram PMF, $W(0.7) - W(0.4) = k_BT\ln 50 = 2.494\times3.912 = 9.76$ kJ/mol. For the PMF based on $g(r)$, use $w(r) = W(r) + 2k_BT\ln r + \text{const}$. The geometric term adds $2k_BT\ln(0.7/0.4) = 2.79$ kJ/mol, so $w(0.7) - w(0.4) = 9.76 + 2.79 = 12.55$ kJ/mol. The shell at 0.7 nm is about three times bigger than the shell at 0.4 nm, so per unit of volume the larger distance is even less populated than the raw histogram suggests.
</details>

## Exercises

1. For a one-dimensional harmonic oscillator, compute $Q$ classically. Derive $\langle E\rangle = k_BT$ and $C_V = k_B$. Compare with the quantum result and find the temperature below which they differ by more than 10 % for a 3,000 cm$^{-1}$ vibration.
2. Take the energies printed by the Python simulation of Module 1 with a Langevin thermostat added (you will write it in Module 8) and estimate $C_V$ from the energy fluctuations.
3. Derive the virial equation for an ideal gas ($\mathbf F=0$ in the bulk) and check it gives $PV = Nk_BT$.
4. A PMF has a square well of depth 40 kJ/mol between $r=0.9$ and $1.1$ nm and is zero outside. Compute $K_a$, $K_d$ in molar units and $\Delta G^\circ$ at 300 K. Then widen the well to 0.8 to 1.2 nm and explain the change in terms of entropy.

## Read

{{READ}}
