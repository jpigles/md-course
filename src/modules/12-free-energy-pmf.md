---
num: 12
title: Free energy I, potentials of mean force, umbrella sampling, WHAM and MBAR
short: PMF, umbrella, WHAM
part: Part IV · Free energy and sampling
hours: 9
summary: Compute a free-energy profile along a coordinate with umbrella sampling, derive the WHAM and MBAR equations that combine the windows, and turn a profile into a binding constant.
videos: 12
papers: H
tags: free-energy
---

<div class="box goal" markdown="1">
#### After this module you can

- define the potential of mean force and handle the Jacobian of a radial coordinate;
- explain why a biasing potential helps and how its effect is removed exactly;
- derive the WHAM equations and state what MBAR does differently;
- choose window spacing and spring constants, and diagnose poor overlap and hysteresis;
- convert a PMF along a separation distance into $K_d$ with the correct standard state.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Many questions put to a simulation are questions about populations. How much of the time is the ligand bound? How much less likely is the top of a barrier than the bottom of a well, and so how rare is a crossing? The quantity that answers them is a **free energy**. This module computes it along a path, for example as a function of the distance between a protein and its ligand while the ligand leaves the binding site.

A plain simulation cannot do this, because it almost never visits the unlikely parts of the path. The method of this module, umbrella sampling, holds the simulation in each part of the path in turn and afterwards removes the effect of the holding exactly.

The module has five layers:

1. **What is measured.** Free energy, the potential of mean force along one coordinate, and why a plain trajectory cannot measure it.
2. **The trick.** Umbrella sampling: add a known extra energy that keeps the system in place, sample, and remove the effect of that energy afterwards.
3. **The book-keeping.** Each simulation gives one piece of the profile at an unknown height. WHAM and MBAR are the two standard ways to join the pieces.
4. **The practice.** How stiff a spring, how many simulations, where to start them, how to check the result and how to put an error bar on it.
5. **The use.** Turning a profile along a distance into a binding constant that can be compared with experiment.

The sections on WHAM and MBAR carry the most algebra. On a first reading it is enough to follow what each equation says in words and the algorithm that solves it. The derivations can wait for a second reading.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The notation below appears in this module for the first time or is used heavily. The general conventions are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\xi$ | The Greek letter xi. The collective variable: one number computed from a configuration. $\xi(\mathbf r)$ with brackets is the rule that computes it, $\xi$ alone is one value of it. |
| $\beta$ | Shorthand for $1/k_BT$. $\beta U$ is an energy measured in units of $k_BT$, a pure number. |
| $\ln$ | The natural logarithm, the inverse of the exponential: $\ln e^x = x$. |
| $\langle A\rangle$ | The equilibrium average of the quantity $A$ in the real system, without any bias. |
| $\langle A\rangle_i$ | With a subscript $i$: the average of $A$ in the biased simulation number $i$. (A subscript that is a coordinate, as in $\langle F_x\rangle_x$, means an average at a fixed value of that coordinate.) |
| $\int d\mathbf r$ | An integral over all atomic coordinates: add up over every possible configuration. |
| $\delta(x)$ | The Dirac delta function: it keeps only the cases where $x = 0$. |
| superscript $b$ | "Biased": a quantity measured in a simulation that contains the extra energy term. |
| $W'$ | A prime is a derivative with respect to the argument: $W'(\xi) = dW/d\xi$, the slope of $W$. |
| $\hat P$ | A hat marks an estimate obtained from data. |
| $\propto$ | "Is proportional to": equal up to a constant factor. |
| $[\text{L}]$ | Square brackets around the name of a molecule: its concentration. |
| $^\circ$ | A small circle marks a standard-state quantity, defined at a concentration of 1 mol/L. |
| a frame around a formula | A result to remember. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which meaning applies each time.

- $W(\xi)$ is the potential of mean force. $W_n$, with a frame label, is a statistical weight in the MBAR section. Lowercase $w_i$ is the bias potential of simulation $i$.
- For a distance, Module 3 wrote the corrected profile as lowercase $w(r)$ and the uncorrected one as capital $W(r)$. Here lowercase $w$ is taken by the bias, and capital $W(r)$ stands for the corrected profile.
- $k$ is the spring constant of the bias. $k_B$ is the Boltzmann constant. In the MBAR section $k$ is also a label that numbers the simulations.
- $n_i(\xi)$ is a number of counts in the WHAM section. In the MBAR section $n$ numbers the saved frames. $N_i$ and $N$ are numbers of samples, not numbers of atoms.
- $\mathbf r$ in bold is the list of all atomic coordinates. $r$ in ordinary type is one distance.
- $P$ is a probability, and upright $\text{P}$ is the protein. $F_i$ is a free energy, not a force. $S$ is the number of simulations, except in the formula $A = \langle E\rangle-TS$, where it is the entropy. $C$ is a free constant, and $C^\circ$ is the standard concentration.
- $A$ is the Helmholtz free energy in $\Delta A$ and in $A = \langle E\rangle-TS$, the name of a state in $P_A$ and in the subscript of $\Delta A_{A\to B}$, and any measured quantity in $\langle A\rangle$ and $A(\mathbf x_n)$.
- $\delta(\dots)$ with brackets is the Dirac delta function. In $\delta P$ and $\delta W$ the same letter marks a small error of $P$ or of $W$.
- Free energies appear under five letters: $\Delta A$ (between two states, as in Module 3), $W(\xi)$ (along a coordinate), $F_i$ (the cost of switching on a bias), $f_i$ (the same in units of $k_BT$) and $\Delta G^\circ$ (of binding, at the standard concentration).
</div>

## Potential energy and free energy

The **potential energy** $U(\mathbf r)$ is a property of one arrangement of the atoms. Give the force field one set of coordinates $\mathbf r$ (all the atomic positions together) and it returns one number (Modules 2 and 5).

At a temperature $T$ the system does not sit in the arrangement of lowest energy. It moves through very many arrangements, and Module 3 gave the rule for how often each is visited: the probability of an arrangement is proportional to its **Boltzmann factor** $e^{-U/k_BT}$. Here $k_B$ is the Boltzmann constant, and $k_BT$ is the natural unit of thermal energy, 2.494 kJ/mol at 300 K. An arrangement that is $k_BT$ higher in energy than another is visited $e^{-1} = 0.37$ times as often.

The questions we ask are almost never about one arrangement. "Bound" is an enormous set of arrangements: every position of every water molecule and every wobble of every side chain, as long as the ligand sits in its site. Such a set is called a **state** (Module 3 called it a macrostate). The probability of a state is the sum of the probabilities of all its arrangements. So a state can be highly populated for two different reasons: its arrangements have low energy, or there are very many of them.

The **free energy** is the quantity that puts both reasons into one number. It is defined so that states obey the same exponential rule as single arrangements:

$$
\frac{P_B}{P_A} = e^{-\beta\,\Delta A_{A\to B}},\qquad \Delta A_{A\to B} = -k_BT\ln\frac{P_B}{P_A} .
$$

<div class="legend" markdown="1">
- $P_A$, $P_B$: the probabilities of finding the system in state A and in state B at equilibrium. In a long simulation they are the fractions of the frames that fall in each state.
- $\Delta A_{A\to B}$: the free-energy difference between the two states, B minus A, in kJ/mol. Negative means that B is the more populated state. (This is the Helmholtz free energy of Module 3.)
- $\beta$: shorthand for $1/k_BT$.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature in kelvin.
- $e^{\dots}$ and $\ln$: the exponential function and the natural logarithm, which undo each other ([toolbox](maths.html#exp-log)).
</div>

Read it like this. The second formula is the first one solved for $\Delta A$: take the logarithm of both sides and multiply by $-k_BT$. A free-energy difference is a ratio of populations, written on a logarithmic scale and given the unit of an energy.

Some numbers to keep in mind. Each factor of 10 in population is worth $k_BT\ln10 = 2.494\times2.303 = 5.74$ kJ/mol at 300 K (1.37 kcal/mol). A factor of 100 is worth twice that, 11.5 kJ/mol, and a factor of 1,000 three times that, 17.2 kJ/mol. In the other direction, a difference of one $k_BT$ is a factor of $e = 2.7$ in population.

That is the sense in which free energy decides populations: it is the population, in other units. An experiment that measures what fraction of a protein is bound, or folded, measures a free energy. It does not measure a potential energy.

The two can differ a great deal. In thermodynamic terms the free energy is $A = \langle E\rangle - TS$ (Module 3): the average energy, minus the temperature times the **entropy** $S$, and the entropy measures how many arrangements the state contains. Module 3 worked an example in which a state of higher energy was favoured 18 to 1 because it consisted of 1,000 conformations. The [physics primer](physics.html#thermodynamics) has more on entropy and free energy.

## The potential of mean force, again

<div data-videos="pjT7waGUGDI LCKtsR1ijsA upLHN5z9TEg"></div>

The last section compared two states. Often you want more: the free energy at every point along a path between them. How deep is the bound well, where is the barrier, and how high is it?

To ask that, you first need a number that says where the system is along the path. Such a number is a **collective variable**: any function $\xi(\mathbf r)$ (the Greek letter xi) that takes all the atomic coordinates and returns one number. The distance between the centre of mass of a ligand and the centre of mass of its binding site is one example. An angle, or the fraction of native contacts, is another.

It is called collective because its value depends on many atoms together. When the variable is chosen to measure the progress of a process, such as unbinding, it is also called a **reaction coordinate**.

Then ask of a long equilibrium simulation: what fraction of the time does $\xi$ take each value? The answer is a probability distribution, $P(\xi)$. The **potential of mean force** (PMF) is this distribution written as a free energy, by the rule of the last section. Where $\xi$ is found often, the PMF is low. Where $\xi$ is found rarely, it is high.

From Module 3: for a coordinate $\xi(\mathbf r)$, called a **collective variable** (CV) or reaction coordinate,

$$
P(\xi) = \frac{\int d\mathbf r\,\delta\big(\xi(\mathbf r)-\xi\big)e^{-\beta U(\mathbf r)}}{\int d\mathbf r\,e^{-\beta U(\mathbf r)}},\qquad W(\xi) = -k_BT\ln P(\xi)+C .
$$

<div class="legend" markdown="1">
- $\mathbf r$: all the atomic coordinates of one configuration (three numbers per atom), written as one list.
- $\xi(\mathbf r)$: the collective variable, a rule that computes one number from a configuration.
- $\xi$ (without brackets): one particular value of that number, the place on the axis where you ask for the probability.
- $U(\mathbf r)$: the potential energy of the configuration.
- $\beta = 1/k_BT$, so $e^{-\beta U(\mathbf r)}$ is the Boltzmann factor of the configuration.
- $\int d\mathbf r$: an integral over all coordinates. Add up what follows over every possible configuration ([toolbox](maths.html#integral)).
- $\delta(\dots)$: the Dirac delta function. It is zero unless its argument is zero, so it keeps only the configurations whose collective variable equals $\xi$ (see the box below).
- $P(\xi)$: the probability density of the collective variable at equilibrium. $P(\xi)\,d\xi$ is the probability of finding it between $\xi$ and $\xi+d\xi$.
- $W(\xi)$: the potential of mean force, in kJ/mol.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- $\ln$: the natural logarithm.
- $C$: a constant that you may choose freely (explained below).
</div>

<div class="box maths" markdown="1">
**Maths you need here: a probability density, and the delta function that selects.** A coordinate such as a distance can take any value in a range, so the probability of one exact value is zero. What is defined is the probability of an interval. The **probability density** $P(\xi)$ is the probability of a small interval divided by its width.

In practice it is a histogram. Cut the axis into bins of width $\Delta\xi$, count the frames in each bin, and divide by the total number of frames and by $\Delta\xi$. Example: 2,000 of 100,000 frames fall in a bin that is 0.05 nm wide, so there $P = (2000/100000)/0.05 = 0.4$ nm$^{-1}$. A density has the unit of one over the unit of $\xi$, and its integral over the whole axis is 1. More in the [toolbox](maths.html#probability).

The **Dirac delta** $\delta(x)$ is the mathematical way to write "keep only the cases where $x=0$". It is zero everywhere except at $x=0$ and has a total area of 1, so that $\int f(x)\,\delta(x-a)\,dx = f(a)$: the integral picks out the value of $f$ at the point $a$. In the formula for $P(\xi)$ it does the job of the histogram bin. Of all configurations, only those with $\xi(\mathbf r)=\xi$ are counted. More in the [toolbox](maths.html#delta).
</div>

Read it like this. The numerator adds up the Boltzmann factors of all configurations that have the chosen value of $\xi$. The denominator adds up the Boltzmann factors of all configurations. The ratio is the share of the total that belongs to this value of $\xi$. Everything other than $\xi$ (the solvent, the side chains, the rest of the protein) has been summed over, which is what "integrating out" means.

So $W(\xi)$ is the energy landscape that is left after averaging over everything else. For the single variable $\xi$ it plays the role that $U$ plays for the full set of coordinates: the probability of a value of $\xi$ is proportional to $e^{-\beta W(\xi)}$. But $W$ is a free energy. A region of $\xi$ can be low in $W$ because the energy is low there, or because many arrangements of the other atoms are compatible with it. In the words of Module 3, its barriers and wells contain the entropy of all the other degrees of freedom (the other independent coordinates of the system), including the solvent.

**The constant $C$.** Only differences of $W$ between two values of $\xi$ have a meaning, as with any free energy. Changing the unit of $\xi$ multiplies the density $P$ by a constant and so shifts $W$ everywhere by the same amount. Using the probability of a bin (the density times the bin width) in place of the density, as the WHAM section does, has the same effect. You fix $C$ by a convention. Usually the lowest point of the profile, or its flat part at large separation, is set to zero.

**The name.** "Potential of mean force" says that the slope of $W$ gives an average force, in the same way that the slope of $U$ gives the force (Module 2). For a Cartesian-like coordinate, $-dW/d\xi$ is the force along $\xi$, averaged over all configurations that share that value of $\xi$.

<details markdown="1"><summary>Optional: why the slope of the PMF is the mean force</summary>
Take the simplest case. Let $\xi$ be one Cartesian coordinate $x$ of one atom, and let $\mathbf y$ stand for all the other coordinates. The delta function then only fixes $x$, and

$$
P(x) = \frac{1}{Z}\int d\mathbf y\;e^{-\beta U(x,\mathbf y)},\qquad Z = \int dx\,d\mathbf y\;e^{-\beta U(x,\mathbf y)} .
$$

Differentiate $W(x) = -k_BT\ln P(x)+C$ with respect to $x$. The [chain rule](maths.html#chain-rule) gives $dW/dx = -k_BT\,(dP/dx)/P$. Inside the integral, the derivative of $e^{-\beta U}$ with respect to $x$ is $-\beta\,(\partial U/\partial x)\,e^{-\beta U}$. The product $k_BT\,\beta$ is 1, and $Z$ cancels between $dP/dx$ and $P$:

$$
\frac{dW}{dx} = \frac{\int d\mathbf y\;\dfrac{\partial U}{\partial x}\,e^{-\beta U(x,\mathbf y)}}{\int d\mathbf y\;e^{-\beta U(x,\mathbf y)}} = \left\langle\frac{\partial U}{\partial x}\right\rangle_x .
$$

The right-hand side is the average of $\partial U/\partial x$ over the other coordinates, with Boltzmann weights, at a fixed value of $x$. The force on the coordinate is $F_x = -\partial U/\partial x$, so this says $-dW/dx = \langle F_x\rangle_x$: minus the slope of the PMF is the mean force. For a coordinate that is not Cartesian, such as a distance, an extra geometric term appears. The subsection on the Jacobian below treats the most important case.
</details>

### Why a plain simulation cannot measure it

The straightforward estimate is a histogram of $\xi$ from a long trajectory. It fails wherever $P(\xi)$ is small. A region that is $10\,k_BT$ above the minimum is visited with relative probability $e^{-10}=4.5\times10^{-5}$: the top of a barrier, which is exactly the region of interest, is almost never sampled, and the system rarely crosses to sample the other side.

Put numbers on a typical case. A barrier of 40 kJ/mol is $40/2.494 = 16.04$ times $k_BT$ at 300 K. Compared with a bin at the minimum, a bin of the same width at the top of the barrier is visited with relative probability $e^{-16.04} = 1.1\times10^{-7}$: about once for every nine million visits to the minimum.

A trajectory of 1 microsecond saved every 10 ps has 100,000 frames. Even if every one of them lay in the bin at the minimum, you would expect $100{,}000\times1.1\times10^{-7} = 0.011$ frames at the top of the barrier. You would need about a hundred such trajectories to see a single one.

A histogram also has to be filled well enough to be trusted. A bin that holds $n$ independent frames has a statistical error of about $\sqrt n$ in its count, so a relative error of $1/\sqrt n$ in $P$. The derivative of $\ln P$ is $1/P$, so a small error $\delta P$ in $P$ changes $W = -k_BT\ln P$ by $k_BT\,\delta P/P$.

Together: $\delta W\approx k_BT/\sqrt n$. With 100 independent frames in a bin the error is $0.1\,k_BT$, or 0.25 kJ/mol. With one frame it is as large as $k_BT$ itself.

So a plain trajectory gives the profile well at the bottom of the wells, where it is least interesting, and not at all near the barrier. Umbrella sampling repairs this. First, one more property of the PMF that causes confusion in practice.

### The Jacobian of a distance

Suppose the collective variable is the distance $r$ between two particles, and suppose the particles do not interact at all. You might expect a flat profile, since no force prefers any distance. A histogram of $r$ is not flat, because there are more ways to be 2 nm apart than to be 1 nm apart.

The picture: fix the first particle and ask where the second can be. All positions at a distance between $r$ and $r+dr$ form a thin spherical shell of radius $r$ and thickness $dr$. Its volume is the area of the sphere, $4\pi r^2$, times the thickness. A shell at 2 nm has four times the volume of a shell of the same thickness at 1 nm, so a particle that is equally likely to be anywhere is four times as likely to be found in it.

For a distance $r$ between two particles in three dimensions, even with no interaction at all the probability density grows as $4\pi r^2$, because there is more volume at larger $r$. The physically meaningful PMF, which is flat for non-interacting particles, removes this factor:

$$
W(r) = -k_BT\ln\frac{P(r)}{4\pi r^2} + C = -k_BT\ln P(r) + 2k_BT\ln r + C' .
$$

<div class="legend" markdown="1">
- $r$: the distance between the two particles (or between two centres of mass), in nm. It is one number, in ordinary type, not the list of all coordinates $\mathbf r$.
- $P(r)$: the probability density of that distance, as a histogram of $r$ from a trajectory gives it.
- $4\pi r^2$: the area of a sphere of radius $r$. Multiplied by a small thickness $dr$ it is the volume of the shell of positions at distance $r$.
- $P(r)/4\pi r^2$: the probability per unit volume, in place of the probability per unit distance.
- $W(r)$: the potential of mean force along the distance, with the volume factor removed.
- $2k_BT\ln r$: the same correction written as a term that is added. At 300 K, $2k_BT = 4.99$ kJ/mol.
- $C$, $C'$: two free constants. They differ by $k_BT\ln4\pi$, as the steps below show.
</div>

<div class="box maths" markdown="1">
**Maths you need here: three rules for logarithms.** The logarithm turns products into sums and powers into factors:

$$
\ln(ab) = \ln a+\ln b,\qquad \ln\frac{a}{b} = \ln a-\ln b,\qquad \ln(a^n) = n\ln a .
$$

Example: $\ln(4\pi r^2) = \ln4\pi+\ln(r^2) = \ln4\pi+2\ln r$. The third rule is where the factor 2 in $2k_BT\ln r$ comes from: it is the power of $r$ in the area of a sphere. More in the [toolbox](maths.html#exp-log).
</div>

The two forms of the formula say the same thing, and the step between them uses only these rules. Start from the first form and split the logarithm of the ratio:

$$
-k_BT\ln\frac{P(r)}{4\pi r^2} = -k_BT\ln P(r)+k_BT\ln(4\pi r^2) = -k_BT\ln P(r)+k_BT\ln4\pi+2k_BT\ln r .
$$

<div class="legend" markdown="1">
- First step: the logarithm of a ratio is a difference of logarithms, and the minus sign in front turns $-\ln(4\pi r^2)$ into a plus.
- Second step: $\ln(4\pi r^2) = \ln4\pi+2\ln r$.
- $k_BT\ln4\pi$: a number that does not depend on $r$ (6.3 kJ/mol at 300 K). It is absorbed into the constant: $C' = C+k_BT\ln4\pi$.
- Other symbols: as in the list above.
</div>

(The logarithm of a length depends on the unit of length. Going from nm to another unit multiplies $r$ by a fixed number and so adds a constant to $\ln r$, which again disappears into $C'$.)

<div class="box maths" markdown="1">
**Maths you need here: the volume element, and the word "Jacobian".** In Cartesian coordinates a small box has the volume $dx\,dy\,dz$, the same everywhere. Describe the same point by its distance $r$ from the origin and two angles for the direction, and equal steps in $r$ and in the angles no longer mark out equal volumes: the piece is larger far from the origin. The factor that converts steps in the new coordinates into volume is called the **Jacobian** of the change of coordinates.

For these spherical coordinates the piece has the volume $r^2\sin\theta\,dr\,d\theta\,d\phi$, where $\theta$ and $\phi$ are the two angles. Adding up over all directions gives $4\pi r^2\,dr$, the shell of the text. So "the Jacobian of a distance" means the factor $4\pi r^2$, or in the PMF the term $2k_BT\ln r$. Integrals over space are in the [toolbox](maths.html#integral).
</div>

Read it like this. Take two particles that do not interact, at 300 K. The uncorrected profile $-k_BT\ln P(r)$ is lower at 2 nm than at 1 nm by $2k_BT\ln2 = 3.46$ kJ/mol, and lower at 3 nm than at 1 nm by $2k_BT\ln3 = 5.48$ kJ/mol, although no force acts. It looks like a repulsion that never ends. Adding $2k_BT\ln r$ cancels this and leaves the flat line that "no interaction" should give.

Two profiles along a distance are therefore in use, and Module 3 met both. Mind the letters: Module 3 wrote the corrected profile as lowercase $w(r)$ and gave capital $W(r)$ to the uncorrected one. In this module capital $W(r)$ is the corrected profile, because lowercase $w$ is needed for the bias.

The uncorrected one, $-k_BT\ln P(r)$, answers "how likely is each distance", volume included. The corrected one, $W(r)$ above, describes the effective interaction between the two partners: it becomes constant at large separation, and it is the one that the binding-constant formula at the end of this module needs. An analysis that starts from a histogram of $r$ produces the uncorrected profile first. The term $2k_BT\ln r$ is added afterwards, by you or by the program. This holds for the umbrella sampling, WHAM and MBAR analyses of the following sections too: for a distance they return $-k_BT\ln P(r)$, the uncorrected profile.

Check which convention your software uses. Many tools output $-k_BT\ln P(r)$ without the correction, and a PMF along a distance that keeps falling as $-2k_BT\ln r$ at large separation is the signature.

## Umbrella sampling

<div data-videos="1tMd68ankiA LVxFGBxgrLo c-dKO66Sx9A"></div>

The difficulty is now defined. The simulation spends its time where $P(\xi)$ is large, and the profile is wanted where $P(\xi)$ is small. Running longer does not help within any time you can afford.

The way out is to change the rules of the simulation on purpose. Add an extra energy term, of your own design, that makes the unlikely region comfortable. The simulation then samples that region well. It samples the wrong distribution, because the extra term is not part of the real system. But you know the extra term exactly, so you can calculate what the distribution would have been without it.

A picture for the usual form of the method. A ball on a steep hillside rolls to the valley and stays there. Tie the ball with a spring to a peg on the slope, and it stays near the peg and jiggles. Move the peg to a series of places and you have inspected the whole hillside. How the ball sits on its spring at each place, pulled a little downhill, tells you the slope there.

<div class="box maths" markdown="1">
**Maths you need here: reweighting.** You can compute an average for one probability distribution from samples drawn from a different one, if you know the ratio of the two. Give each sample the weight (probability you want) divided by (probability you sampled from), and take the weighted average.

Example. You want the mean of a fair die, which is 3.5. You only have a loaded die that shows a six half of the time and each other face one time in ten. Its plain mean is $0.5\times6+0.1\times(1+2+3+4+5) = 4.5$, which is wrong.

Now weight each throw. A six gets the weight $(1/6)/(1/2) = 1/3$, and any other face gets $(1/6)/(1/10) = 5/3$. The weighted mean is $0.5\times\tfrac13\times6+0.1\times\tfrac53\times(1+2+3+4+5) = 1+2.5 = 3.5$: the fair value, obtained from the loaded die.

In a simulation the loaded die is the system with an extra energy term $w$. Its configurations appear with a probability proportional to $e^{-\beta(U+w)}$, where the real system has $e^{-\beta U}$. The ratio, the probability you want divided by the probability you sampled from, is proportional to $e^{+\beta w}$, and that is the weight that undoes the bias. The condition is the same as for the die: every outcome that matters must turn up in the sample. A loaded die that never shows a one cannot tell you anything about ones.
</div>

Umbrella sampling was introduced by [Torrie and Valleau (1977)](cite:torrie1977) for Monte Carlo estimates of free-energy differences: they sampled with a non-Boltzmann weight that widened the range of configurations visited, and recovered unbiased averages exactly by reweighting. The form used in molecular dynamics today, with a harmonic restraint along a coordinate, came later.

Three terms in these sentences. Monte Carlo is the other way to sample configurations, by random trial moves in place of equations of motion (Module 3). A "non-Boltzmann weight" means that configurations were visited with a probability other than $e^{-\beta U}$. A "harmonic restraint" is a spring, as in the next formula.

Add a **bias potential** $w_i(\xi)$ that holds the system near a chosen value $\xi_i$, most often a harmonic spring:

$$
U_i^{b}(\mathbf r) = U(\mathbf r)+w_i\big(\xi(\mathbf r)\big),\qquad w_i(\xi) = \tfrac12k\,(\xi-\xi_i)^2 .
$$

<div class="legend" markdown="1">
- $i$: the label of one simulation. Each simulation has its own bias.
- $U(\mathbf r)$: the potential energy of the real system, from the force field.
- $w_i(\xi)$: the bias potential of simulation $i$, an extra energy that depends on the configuration only through the value of the collective variable. It is lowercase, and it is not the PMF $W$.
- $U_i^{b}(\mathbf r)$: the total potential energy used in simulation $i$. The superscript $b$ stands for "biased".
- $\xi_i$: the centre of the spring, the value of $\xi$ at which the bias is zero. You choose it.
- $k$: the spring constant (stiffness), which you also choose. If $\xi$ is a distance in nm, $k$ is in kJ mol$^{-1}$ nm$^{-2}$. It is not the Boltzmann constant $k_B$.
- $\tfrac12k\,(\xi-\xi_i)^2$: the energy of a spring that is stretched by $\xi-\xi_i$ ([primer](physics.html#oscillator)).
- $\mathbf r$, $\xi(\mathbf r)$, $\xi$: the configuration, the rule that computes the collective variable from it, and one value of the collective variable, as in the lists above.
</div>

Read it like this. The bias costs nothing at $\xi=\xi_i$ and grows with the square of the distance from it. Say $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$. At 0.05 nm from the centre the bias is $\tfrac12\times1000\times0.05^2 = 1.25$ kJ/mol, half of $k_BT$, and at 0.1 nm it is 5 kJ/mol, twice $k_BT$.

Thermal motion therefore carries the system a few hundredths of a nanometre from the centre and seldom much further. A larger $k$ holds it more tightly. At every step the MD program adds the force of this spring, $-k(\xi-\xi_i)$ along $\xi$, to the forces of the force field.

Run one simulation, a **window**, for each of a series of centres $\xi_1,\dots,\xi_S$ that span the range of interest. Each window samples its neighbourhood thoroughly, including regions of high free energy.

Here $S$ is the number of windows. A window whose centre lies at the top of a barrier, with a spring that is stiff enough, spends all of its time near the top of the barrier, because the spring stops it from sliding down either side. What plain MD saw once in millions of frames, this window sees in every frame.

### Removing the bias from one window

Each window samples a distorted distribution. This subsection shows what the distortion is and how to undo it. It is the central derivation of the module, and it takes four short steps.

**The bias can be removed exactly.** The biased distribution in window $i$ is

$$
P_i^{b}(\xi) = \frac{\int d\mathbf r\,\delta(\xi(\mathbf r)-\xi)\,e^{-\beta[U+w_i(\xi)]}}{\int d\mathbf r\,e^{-\beta[U+w_i]}}
= \frac{e^{-\beta w_i(\xi)}\,P(\xi)}{\langle e^{-\beta w_i}\rangle},
$$

because the bias depends on $\mathbf r$ only through $\xi$ and can be taken out of the integral.

<div class="legend" markdown="1">
- $P_i^{b}(\xi)$: the probability density of $\xi$ in window $i$, the one that the biased simulation samples. Its histogram is what you measure.
- $P(\xi)$: the probability density of $\xi$ in the real, unbiased system. This is what you want.
- $e^{-\beta[U+w_i]}$: the Boltzmann factor of a configuration in the biased simulation, with the total energy $U+w_i$ in the exponent.
- $\langle e^{-\beta w_i}\rangle$: the average of $e^{-\beta w_i(\xi(\mathbf r))}$ over the unbiased equilibrium distribution. Angle brackets without a subscript always mean an average in the real system. It is one number per window.
- $\int d\mathbf r$, $\delta$, $\beta$, $U$, $w_i$: as in the lists above.
</div>

The first expression is the definition of a probability density from the previous section, with $U$ replaced by the biased energy $U+w_i$. The second expression is what it reduces to. The steps:

1. *Numerator: take the bias out.* The delta function keeps only configurations with $\xi(\mathbf r)=\xi$. For all of those the bias has the same value, $w_i(\xi)$. A factor that is the same for every term of a sum can be written in front of the sum, so the numerator is $e^{-\beta w_i(\xi)}\int d\mathbf r\,\delta(\xi(\mathbf r)-\xi)\,e^{-\beta U}$.
2. *Numerator: recognise $P(\xi)$.* Write $Z = \int d\mathbf r\,e^{-\beta U}$ for the sum of all unbiased Boltzmann factors. By the definition of $P(\xi)$, the integral that is left equals $Z\,P(\xi)$. The numerator is $e^{-\beta w_i(\xi)}\,Z\,P(\xi)$.
3. *Denominator: recognise an average.* The average of any quantity $A$ in the unbiased system is $\langle A\rangle = \int d\mathbf r\,A\,e^{-\beta U}/Z$. With $A = e^{-\beta w_i}$ this reads $\int d\mathbf r\,e^{-\beta w_i}e^{-\beta U} = Z\,\langle e^{-\beta w_i}\rangle$. The left side is the denominator, because $e^{-\beta[U+w_i]} = e^{-\beta U}e^{-\beta w_i}$.
4. *Divide.* $Z$ appears above and below and cancels, which leaves the second expression.

Read it like this. The window sees the true distribution multiplied by $e^{-\beta w_i(\xi)}$, a factor that is 1 at the centre of the spring and falls off on both sides, and divided by a constant that makes the total probability 1 again. In terms of energies: $P(\xi)$ is proportional to $e^{-\beta W(\xi)}$, so the window samples $\xi$ as if its landscape were $W(\xi)+w_i(\xi)$, the true profile plus the spring. A spring that is stiff enough gives that sum a minimum near $\xi_i$ wherever $\xi_i$ lies, even on a slope or on top of a barrier.

Now turn the relation round, so that the unknown $P(\xi)$ is expressed by the measured $P_i^{b}(\xi)$. Take the logarithm of both sides. A product becomes a sum, and the factor in the denominator gets a minus sign:

$$
\ln P_i^{b}(\xi) = -\beta w_i(\xi)+\ln P(\xi)-\ln\big\langle e^{-\beta w_i}\big\rangle .
$$

<div class="legend" markdown="1">
- $-\beta w_i(\xi)$: the logarithm of the factor $e^{-\beta w_i(\xi)}$, because $\ln e^x = x$.
- Other symbols: as in the list above.
</div>

Multiply every term by $-k_BT$ (remember that $k_BT\,\beta = 1$) and move terms until $-k_BT\ln P(\xi)$ stands alone on the left. That term is the PMF $W(\xi)$, apart from its free constant.

Solving for the unbiased PMF:

$$
\boxed{W(\xi) = -k_BT\ln P_i^{b}(\xi) - w_i(\xi) + F_i},\qquad F_i = -k_BT\ln\big\langle e^{-\beta w_i}\big\rangle .
$$

<div class="legend" markdown="1">
- $W(\xi)$: the unbiased PMF, the result.
- $-k_BT\ln P_i^{b}(\xi)$: the PMF that the biased window appears to have. You get it from the histogram of $\xi$ in window $i$.
- $w_i(\xi)$: the bias, which you know because you chose it.
- $F_i$: a constant for window $i$, in kJ/mol, defined by the second formula. It does not depend on $\xi$.
- $\langle e^{-\beta w_i}\rangle$: the unbiased average of the factor $e^{-\beta w_i}$, as above.
- The frame around the first formula marks a result to remember.
- $k_BT$, $\ln$, $\beta$: the thermal energy, the natural logarithm and $1/k_BT$, as in the lists above.
</div>

Read it like this. Measure the histogram of the window, turn it into an apparent free energy with $-k_BT\ln$, and subtract the spring energy that you added. What remains is the true profile, raised or lowered by a constant $F_i$. The shape of $W$ inside the window is recovered exactly. Its height is not.

Within one window everything on the right is known except the constant $F_i$, the free energy of adding bias $i$ to the system. Each window therefore gives a piece of $W(\xi)$ with an unknown vertical offset. The pieces must be joined, and the joining is where the statistics matter.

### The unknown constant of each window

A formula for $F_i$ stands above, so why is it unknown? Because the formula asks for an average over the *unbiased* system, and the unbiased system is the one that cannot be sampled. $F_i$ depends on the whole of $P(\xi)$, which is the unknown.

Its meaning. Write $Z_i = \int d\mathbf r\,e^{-\beta[U+w_i]}$ for the sum of the Boltzmann factors of the biased system. Step 3 of the derivation showed that $\langle e^{-\beta w_i}\rangle = Z_i/Z$, so

$$
F_i = -k_BT\ln\frac{Z_i}{Z} .
$$

<div class="legend" markdown="1">
- $Z$: the configurational integral of the real system, $\int d\mathbf r\,e^{-\beta U}$, the sum of the Boltzmann factors of all configurations.
- $Z_i$: the same sum for the system with bias $i$ switched on.
- $F_i$: the free-energy difference between the system with bias $i$ and the system without it. Here $F$ is a free energy, not a force.
- $k_BT$, $\ln$: the thermal energy and the natural logarithm, as before.
</div>

This has the form of the free-energy difference between two states from the start of the module, with "bias on" and "bias off" as the two states. The spring energy is never negative, so $e^{-\beta w_i}$ is never larger than 1 and $F_i$ is zero or positive: switching on a restraint always costs free energy. It costs little when the spring sits where the system likes to be anyway, and much when it sits in an unlikely place. As a rough illustration, if a bias confines the system to about one sixteenth of a range that it would otherwise visit evenly, then $\langle e^{-\beta w_i}\rangle$ is about $1/16$ and $F_i = k_BT\ln16 = 6.9$ kJ/mol.

**How the offsets get fixed.** Two neighbouring windows $i$ and $j$ describe the same function $W(\xi)$. Wherever both have data, the two pieces must agree, and that requirement determines the difference of their constants. Write the framed formula for both windows at the same $\xi$ and subtract one from the other:

$$
F_j-F_i = w_j(\xi)-w_i(\xi)+k_BT\ln\frac{P_j^{b}(\xi)}{P_i^{b}(\xi)} .
$$

<div class="legend" markdown="1">
- $i$, $j$: two windows whose histograms both cover the value $\xi$.
- $P_i^{b}(\xi)$, $P_j^{b}(\xi)$: the two measured (biased) probability densities at that $\xi$.
- $w_i(\xi)$, $w_j(\xi)$: the two spring energies at that $\xi$.
- $F_j-F_i$: the difference of the two unknown constants. With perfect data it comes out the same for every $\xi$ in the overlap.
- $k_BT$, $\ln$: the thermal energy and the natural logarithm, as before.
</div>

<div class="box key" markdown="1">
**Worked example: one shared bin.** Windows 1 and 2 both have samples in the bin at $\xi^*$. There the spring of window 1 costs $w_1 = 4$ kJ/mol and the spring of window 2 costs $w_2 = 1$ kJ/mol. Window 1 has 2 % of its samples in this bin, and window 2 has 10 %. (The bin is the same for both, so the ratio of the densities is the ratio of these fractions.) At 300 K,

$F_2-F_1 = 1-4+2.494\ln(0.10/0.02) = -3+4.01 = 1.01$ kJ/mol.

Relative to the piece from window 1, the piece from window 2 has to be raised by 1.01 kJ/mol for the two to meet at $\xi^*$.
</div>

With real data every bin of the overlap gives a slightly different answer, because the counts are noisy. Which bin to believe, and what to do when three or more windows overlap at once, is the subject of the next section.

The demo below runs both approaches on the same toy problem with the same total number of steps: one particle in the double well $U(x) = h\,(x^2-1)^2$, with energies in units of $k_BT$. "Run plain MD" shows the histogram of an unbiased run and the profile it gives. "Run umbrella + WHAM" shows one histogram per window and the joined profile. Raise the barrier $h$ and compare how much of the range each method covers.

<div class="widget" data-widget="umbrella"></div>

## WHAM: joining the windows optimally

<div data-videos="V1RCMp4wM2k"></div>

After the simulations you have $S$ histograms. Each gives a piece of the profile that is good near its own centre and noisy in its tails, at an unknown height. In an overlap region two or more windows give an estimate of the same thing. WHAM answers two questions at once: how to average the estimates where windows overlap, and what the heights $F_i$ are.

The principle behind the averaging is ordinary good practice with measurements: trust each estimate according to its precision. A window with 5,000 samples in a bin knows that bin better than a window with 5 samples in it.

The weighted histogram analysis method ([Kumar et al. 1992](cite:kumar1992)). Bin $\xi$. Let $n_i(\xi)$ be the number of samples from window $i$ in the bin at $\xi$ and $N_i$ the total number of samples in window $i$. Each window gives its own estimate of the unbiased distribution, $P(\xi)\approx\frac{n_i(\xi)}{N_i}e^{+\beta[w_i(\xi)-F_i]}$.

"Bin $\xi$" means: cut the range of $\xi$ into small intervals of equal width (bins) and count the samples of each window in each bin. A sample is one saved frame. From here to the end of this section, $P(\xi)$ stands for the probability of the *bin* at $\xi$, that is, the density times the bin width, and $w_i(\xi)$ for the bias at the centre of that bin. For the PMF this changes nothing except the free constant.

The single-window estimate is the result of the last section, written with counts. The fraction $n_i(\xi)/N_i$ of the samples of window $i$ that fall in the bin estimates the biased probability $P_i^{b}(\xi)$. The definition of $F_i$ gives $\langle e^{-\beta w_i}\rangle = e^{-\beta F_i}$, so the relation $P_i^{b} = e^{-\beta w_i}P/\langle e^{-\beta w_i}\rangle$ becomes $P_i^{b}(\xi) = e^{-\beta[w_i(\xi)-F_i]}\,P(\xi)$. Dividing by the exponential gives the estimate in the text.

<div class="box maths" markdown="1">
**Maths you need here: counting errors and the weighted average.** Two facts from statistics.

*Counts scatter by their square root.* If events happen independently and you expect $\bar n$ of them, the number you observe varies from one repeat to the next with a variance of about $\bar n$, so with a standard deviation of $\sqrt{\bar n}$. (The **variance** is the mean squared deviation from the average, and the standard deviation is its square root.) Expect 100 counts in a bin and you will see 100 give or take 10, a relative error of 10 %. Expect 10,000 and the relative error is 1 %.

*Average with weights of one over the variance.* Suppose two independent measurements of the same quantity give $x_1$ with variance $s_1^2$ and $x_2$ with variance $s_2^2$. Any combination $p\,x_1+(1-p)\,x_2$ estimates the quantity, and its variance is $p^2s_1^2+(1-p)^2s_2^2$. Setting the derivative with respect to $p$ to zero, $2p\,s_1^2-2(1-p)\,s_2^2 = 0$, gives the best choice: $p$ proportional to $1/s_1^2$ and $1-p$ proportional to $1/s_2^2$. In general, the combination with the smallest variance weights each measurement by one over its variance, and the variance of the result is one over the sum of those weights.

Example: $10\pm1$ and $14\pm2$. The weights are $1/1^2 = 1$ and $1/2^2 = 0.25$, so the best estimate is $(1\times10+0.25\times14)/1.25 = 10.8$, with variance $1/1.25 = 0.8$ and standard deviation 0.89. The result lies closer to the more precise measurement and is more precise than either. More in the [toolbox](maths.html#averages).
</div>

Combine them as a weighted average with weights chosen to minimise the statistical variance of the result. The answer is

$$
\boxed{P(\xi) = \frac{\sum_{i=1}^{S}n_i(\xi)}{\sum_{i=1}^{S}N_i\,e^{-\beta[w_i(\xi)-F_i]}}}
\qquad\qquad
\boxed{e^{-\beta F_i} = \sum_{\xi}P(\xi)\,e^{-\beta w_i(\xi)}}
$$

<div class="legend" markdown="1">
- $\xi$: here the label of one bin of the histogram.
- $i$: the label of a window, from 1 to $S$. $S$ is the number of windows.
- $\sum_{i=1}^{S}$: a sum over all windows.
- $n_i(\xi)$: the number of samples of window $i$ that fall in the bin at $\xi$.
- $N_i$: the total number of samples of window $i$.
- $w_i(\xi)$: the bias energy of window $i$ at the centre of the bin.
- $F_i$: the free-energy constant of window $i$ from the previous section.
- $e^{-\beta[w_i(\xi)-F_i]}$: the factor by which bias $i$ changes the probability of the bin, that is, the biased probability divided by the unbiased one.
- $P(\xi)$: the best estimate of the unbiased probability of the bin, from all windows together.
- $\sum_\xi$: a sum over all bins.
- $\beta = 1/k_BT$.
</div>

The first equation has a simple reading: the numerator is the total number of counts observed in the bin, and the denominator is the total number of counts *expected* there if $P(\xi)$ were 1, summed over windows.

In more detail: window $i$ has $N_i$ samples, and each of them lands in the bin with the biased probability $e^{-\beta[w_i(\xi)-F_i]}\,P(\xi)$. So window $i$ is expected to contribute $N_i\,e^{-\beta[w_i(\xi)-F_i]}\,P(\xi)$ counts, and all windows together $P(\xi)\sum_iN_i\,e^{-\beta[w_i(\xi)-F_i]}$. Set this equal to the number observed, $\sum_in_i(\xi)$, and solve for $P(\xi)$: that is the first equation. A window whose spring is far from the bin has a tiny exponential there. It expects no counts, sees none, and adds almost nothing to either sum.

The second is just the definition of $F_i$.

Recall $F_i = -k_BT\ln\langle e^{-\beta w_i}\rangle$, so that $e^{-\beta F_i} = \langle e^{-\beta w_i}\rangle$. The average of a quantity that depends only on $\xi$ is the sum over the bins of (probability of the bin) times (value in the bin), and that is the right-hand side. It requires $P$ to be normalised: its values must add up to 1 over the bins.

### Where the first equation comes from

The counting argument above already gives the first equation. The route named in the text, a weighted average with the smallest variance, leads to the same place and shows what "optimally" means. It takes five steps, with the $F_i$ treated as known numbers. That is a simplification: the $F_i$ are estimated from the same counts, so the argument shows that the weights are the best ones for given $F_i$ and says nothing about the error of the $F_i$ themselves.

1. *Abbreviate.* Write $c_i(\xi) = e^{-\beta[w_i(\xi)-F_i]}$. The estimate of $P(\xi)$ from window $i$ alone is then $\hat P_i(\xi) = n_i(\xi)/(N_i\,c_i(\xi))$.
2. *The error of a count.* Window $i$ expects $N_ic_iP$ counts in the bin. By the counting rule in the box, the variance of $n_i$ is about that same number, $N_ic_iP$.
3. *The error of the estimate.* Dividing a quantity by a constant divides its variance by the square of the constant. So the variance of $\hat P_i$ is $N_ic_iP/(N_ic_i)^2 = P/(N_ic_i)$.
4. *The weights.* One over the variance is $N_ic_i/P$. The factor $1/P$ is the same for every window and cancels from a weighted average, so the weight of window $i$ is $p_i = N_ic_i$. Each window is weighted by the number of counts it expects in this bin.
5. *The weighted average.*

$$
P(\xi) = \frac{\sum_ip_i\,\hat P_i(\xi)}{\sum_ip_i} = \frac{\sum_iN_ic_i(\xi)\,\dfrac{n_i(\xi)}{N_ic_i(\xi)}}{\sum_iN_ic_i(\xi)} = \frac{\sum_in_i(\xi)}{\sum_iN_i\,c_i(\xi)} .
$$

<div class="legend" markdown="1">
- $c_i(\xi) = e^{-\beta[w_i(\xi)-F_i]}$: an abbreviation used only in this derivation.
- $\hat P_i(\xi) = n_i(\xi)/(N_ic_i(\xi))$: the estimate of $P(\xi)$ from window $i$ alone. The hat marks an estimate from data.
- $p_i = N_ic_i(\xi)$: the weight given to window $i$ in this bin.
- $\sum_i$: a sum over all windows.
- Other symbols: as in the list above.
</div>

In the middle expression $N_ic_i$ cancels inside each term of the numerator. The result is the first WHAM equation.

The rule in the box also gives the error of the result. Its variance is one over the sum of the weights $N_ic_i/P$, which is $P/\sum_iN_ic_i$. The first WHAM equation says that $\sum_iN_ic_i = \sum_in_i/P$, so the variance is $P^2/\sum_in_i$ and the relative error of $P$ is one over the square root of the total number of counts in the bin. The rule $\delta W\approx k_BT/\sqrt n$ from the section on the PMF therefore describes how much the joined profile scatters from one bin to the next, with $n$ the number of independent counts that all windows together put in the bin.

This is not the whole error. The $F_i$ were treated as known, but they are estimated from the overlaps and each carries an error of its own. These errors add up along the chain of windows, so the height of one end of the profile relative to the other is less certain than the counting rule says. The bootstrap described under "Checks and error bars" gives an error bar that contains both parts.

### Solving the two equations

The two are coupled, so they are solved by iteration: start with all $F_i=0$, compute $P$, update the $F_i$, and repeat until they stop changing (to $10^{-6}\,k_BT$ or better; convergence can be slow, and stopping early is a known source of error).

"Coupled" means that each equation needs the answer of the other. The first gives $P$ if the $F_i$ are known, and the second gives the $F_i$ if $P$ is known. Neither can be solved alone. A solution is a set of numbers that is **self-consistent**: put the $F_i$ into the first equation, put the resulting $P$ into the second, and the same $F_i$ come back.

<div class="box maths" markdown="1">
**Maths you need here: solving an equation by iteration.** Some equations have the unknown on both sides and cannot be rearranged into "unknown = formula". A common way to solve them is to guess, put the guess into the right-hand side, take the result as the next guess, and repeat until the number stops changing.

Example: $x = \tfrac12(x+2/x)$ is satisfied by $x = \sqrt2$. Start from $x = 1$. The right-hand side gives 1.5, then 1.41667, then 1.41422, then 1.41421, and it stays there. A value that reproduces itself is called a fixed point. How fast such a scheme converges depends on the equation.
</div>

Written as an algorithm:

1. From the trajectories, build the table of counts $n_i(\xi)$, with one row per window and one column per bin, and the totals $N_i$. Compute the table of bias energies $w_i(\xi)$ at the bin centres.
2. Set every $F_i = 0$.
3. For every bin, compute $P(\xi)$ from the first equation with the present $F_i$.
4. For every window, compute a new $F_i = -k_BT\ln\sum_\xi P(\xi)\,e^{-\beta w_i(\xi)}$ from the second equation with that $P$.
5. Find the largest change of any $F_i$ since the previous round. If it is above the tolerance, go back to step 3.
6. Report $W(\xi) = -k_BT\ln P(\xi)$, shifted so that its lowest point (or its plateau, the flat part at large separation) is zero. If $\xi$ is a distance $r$, this is the uncorrected profile: add $2k_BT\ln r$ first, as in the subsection on the Jacobian. Without that term the profile has no flat part.

Why a loose tolerance is dangerous. The relative height of two distant windows is passed along the chain of overlaps between them, and each round moves it only part of the way. With many windows and little overlap the $F_i$ keep creeping for a great many rounds, each change small. A loop that stops when the changes look small can leave a profile that is still tilted.

The two equations fix $P$ and the $F_i$ only up to one common constant. Add the same amount $a$ to every $F_i$ and multiply $P$ by $e^{-\beta a}$, and both equations still hold. This is the free constant $C$ of the PMF again. A convention removes the freedom, for example normalising $P$ or setting one of the $F_i$ to zero.

The same equations follow from maximising the likelihood of the observed histograms.

The **likelihood** is the probability of obtaining exactly the counts that were observed, regarded as a function of the unknowns $P(\xi)$ and $F_i$. Maximising it means choosing the unknowns under which the data you have would be the most probable. Two different principles, smallest variance and largest likelihood, lead to the same equations. Exercise 5 asks you for the second derivation.

### What the data must provide

Requirements:

- **Overlap.** Neighbouring windows must sample common bins. Where two windows share no bins, nothing in the data fixes their relative offset.
- **Uncorrelated counts.** The derivation assumes independent samples. With correlated data the estimate is still valid but the weights are no longer optimal, and error estimates must account for the correlation (below).

On overlap: the formula for $F_j-F_i$ in the previous section needs a value of $\xi$ at which both histograms are well filled. If there is none, the equations still return numbers, but the numbers rest on nothing (Check yourself 3).

On correlation: frames saved close together in time resemble each other, so 1,000 frames can carry the information of far fewer independent samples. Module 11 measured this with the statistical inefficiency $g$, the number of successive frames that are worth one independent sample. "Still valid" means that with enough data the estimate goes to the right answer. The counting error, however, must be computed with the number of independent samples, $n/g$, and not with the number of frames.

## MBAR: the binless limit

<div data-videos="5tKnjRdVz3E fhMjOYvnGcY"></div>

WHAM needs bins, and bins force a compromise. Wide bins blur the profile, because the bias is treated as constant across each bin. Narrow bins hold few counts and are noisy.

The noise of narrow bins spoils the profile, bin by bin. It does not spoil the constants $F_i$, because each $F_i$ is a sum over all bins. MBAR is what the WHAM equations for the $F_i$ become when the bins are made so narrow that each holds one sample at most. The profile is then built from the weights of the single frames, as shown below.

Nothing is histogrammed. Each saved frame is used individually, and the method returns a weight for every frame that says how much the frame counts in the real, unbiased system.

The multistate Bennett acceptance ratio ([Shirts and Chodera 2008](cite:shirts2008)) removes the histogram. Let $u_k(\mathbf x) = \beta[U(\mathbf x)+w_k(\xi(\mathbf x))]$ be the reduced potential of state $k$, and pool all samples $\mathbf x_n$ from all windows, $n=1,\dots,N$. The dimensionless free energies $f_i=\beta F_i$ satisfy

$$
f_i = -\ln\sum_{n=1}^{N}\frac{e^{-u_i(\mathbf x_n)}}{\sum_{k=1}^{S}N_k\,e^{f_k-u_k(\mathbf x_n)}} .
$$

<div class="legend" markdown="1">
- $\mathbf x$: one configuration, the same thing that was written $\mathbf r$ above.
- $\mathbf x_n$: the configuration of saved frame number $n$.
- $n$: here the label of one frame in the pooled list, from 1 to $N$. (In the WHAM section $n_i(\xi)$ was a count.)
- $N$: the total number of frames from all windows, $N = \sum_kN_k$.
- $k$ and $i$: labels of states, from 1 to $S$. For umbrella sampling a state is one window, that is, the system with one particular bias. This $k$ is a label, not the spring constant.
- $N_k$: the number of frames that were generated in state $k$.
- $u_k(\mathbf x)$: the **reduced potential** of state $k$, the total energy of configuration $\mathbf x$ in window $k$ divided by $k_BT$. A pure number. $e^{-u_k}$ is the Boltzmann factor.
- $f_i$: the free energy of state $i$ divided by $k_BT$, also a pure number. At 300 K, $F_i$ in kJ/mol is 2.494 times $f_i$.
- $\ln$, $\sum$: the natural logarithm and a sum.
</div>

Read it like this. "Reduced" and "dimensionless" both mean "measured in units of $k_BT$": an energy of 5 kJ/mol at 300 K is $5/2.494 = 2.0$ in reduced units.

"Pool" means: put the frames of all windows into one list. The equation never asks which window a frame came from. It asks, for every frame, what the energy of that frame *would be* in every window. For umbrella sampling this only requires the value of $\xi$ in the frame and the springs.

The unknowns appear on both sides: $f_i$ on the left, and all the $f_k$ inside the sum on the right. So this is again a self-consistent set of equations, one per window, and it is solved numerically in the same spirit as WHAM. As with WHAM, only differences between the $f_i$ are determined.

This is the WHAM equation with bins of zero width, one per sample.

To see it, put the first WHAM equation into the second, so that $P$ disappears:

$$
e^{-\beta F_i} = \sum_{\xi}\frac{\big[\sum_jn_j(\xi)\big]\,e^{-\beta w_i(\xi)}}{\sum_kN_k\,e^{-\beta[w_k(\xi)-F_k]}} .
$$

<div class="legend" markdown="1">
- $\sum_jn_j(\xi)$: the total number of samples in the bin at $\xi$, from all windows.
- $j$, $k$: labels of windows inside the two inner sums. They are different letters because the two sums run independently of each other and of $i$.
- Other symbols: as in the list under the WHAM equations.
</div>

Now shrink the bins until each contains one sample or none. Empty bins contribute nothing. A bin with one sample, frame $n$ with collective variable $\xi_n$, contributes its term once. The sum over bins becomes a sum over frames:

$$
e^{-\beta F_i} = \sum_{n=1}^{N}\frac{e^{-\beta w_i(\xi_n)}}{\sum_kN_k\,e^{-\beta[w_k(\xi_n)-F_k]}} .
$$

<div class="legend" markdown="1">
- $\xi_n$: the value of the collective variable in frame $n$.
- $w_i(\xi_n)$: the bias energy that frame $n$ would have in window $i$.
- Other symbols: as above.
</div>

Compare with the MBAR equation. Its exponential form is $e^{-f_i} = \sum_ne^{-u_i(\mathbf x_n)}/\sum_kN_ke^{f_k-u_k(\mathbf x_n)}$. Insert $u_k = \beta U+\beta w_k$. Every term of the fraction, above and below, then contains the same factor $e^{-\beta U(\mathbf x_n)}$, which cancels.

What is left is the equation above, with $f = \beta F$. For umbrella sampling the two methods are the same estimate, with and without bins.

<details markdown="1"><summary>Optional: one way to see where the MBAR equation comes from</summary>
In state $k$ a configuration $\mathbf x$ turns up with the probability density $p_k(\mathbf x) = e^{-u_k(\mathbf x)}/Z_k$, where $Z_k = \int d\mathbf x\,e^{-u_k(\mathbf x)}$ is the sum of all Boltzmann factors of that state. The dimensionless free energy is $f_k = -\ln Z_k$, so $p_k(\mathbf x) = e^{f_k-u_k(\mathbf x)}$. (This $f_k$ differs from $\beta F_k$ of the main text by a constant that is the same for every state. Only differences between the $f_k$ are determined, so the constant has no effect.)

The pooled list holds $N_k$ frames from each state. Treat a frame picked at random from the list as drawn from the mixture of the states, which has the density

$$
p_{\text{mix}}(\mathbf x) = \sum_k\frac{N_k}{N}\,p_k(\mathbf x) = \frac1N\sum_kN_k\,e^{f_k-u_k(\mathbf x)} .
$$

Now reweight, as with the loaded die. For any function $g$, the integral $\int d\mathbf x\,g(\mathbf x)$ equals $\int d\mathbf x\,p_{\text{mix}}(\mathbf x)\,[g(\mathbf x)/p_{\text{mix}}(\mathbf x)]$, and that is the average of $g/p_{\text{mix}}$ over frames drawn from the mixture. With $g = e^{-u_i}$ the integral is $Z_i$:

$$
Z_i\approx\frac1N\sum_{n=1}^{N}\frac{e^{-u_i(\mathbf x_n)}}{p_{\text{mix}}(\mathbf x_n)} = \sum_{n=1}^{N}\frac{e^{-u_i(\mathbf x_n)}}{\sum_kN_k\,e^{f_k-u_k(\mathbf x_n)}} .
$$

Taking $-\ln$ of both sides gives the MBAR equation. The denominator is $N$ times the density with which frame $n$ turns up in the pooled data. A frame from a region that the windows together sampled heavily gets a small weight, and a frame from a thinly sampled region gets a large one.

Take this as a way to understand the equation and not as its derivation. That a fixed number of frames came from each state, in place of random draws from the mixture, does no harm: with the true $f_k$ in the denominator the sum on the right still equals $Z_i$ on average. What the argument leaves out is that the $f_k$ are not known. They are the unknowns of the same set of equations, so the argument shows that the equations are consistent, and it does not show that their solution is the best estimate the data allow.
</details>

Its advantages: no binning error; in the limit of many samples, the lowest variance of any estimator of its family, with an analytical uncertainty that assumes uncorrelated samples; and each sample gets a weight

$$
W_n = \frac{e^{-u_0(\mathbf x_n)}}{\sum_kN_k\,e^{f_k-u_k(\mathbf x_n)}}
$$

for the unbiased state $u_0=\beta U$ (normalise the $W_n$ to sum to 1), so that the unbiased average of **any** observable, including a PMF along a different coordinate, is $\langle A\rangle = \sum_nW_nA(\mathbf x_n)$.

<div class="legend" markdown="1">
- $W_n$: the weight of frame $n$ in the unbiased system, a pure number. This $W$ with a frame label is not the PMF $W(\xi)$.
- $u_0(\mathbf x_n) = \beta U(\mathbf x_n)$: the reduced potential of frame $n$ without any bias. State 0 is the real system, in which no simulation was run.
- The denominator: the same sum as in the equation for $f_i$, with the converged values of the $f_k$.
- $A(\mathbf x_n)$: the value of any observable in frame $n$, for example a distance or a number of contacts.
- $\langle A\rangle$: the average of $A$ in the unbiased system.
- $\sum_n$: a sum over all frames of the pooled list.
</div>

Some words in that sentence need explaining.

An **estimator** is a recipe that turns data into a number, here frames into free energies. Its **variance** says how much the number would scatter if you repeated the whole set of simulations. Lower is better. The claim of lowest variance is made within a defined class of estimators, and for the limit of many samples.

**Binning error** is the error that WHAM makes by treating the bias as constant across a bin. An **analytical uncertainty** is an error bar that comes from a formula evaluated on the same data, with no need to repeat the run. The formula assumes that the frames are statistically independent. If they are not, the error bar is too small.

For umbrella sampling the weight takes a simple form. Insert $u_0 = \beta U$ and $u_k = \beta U+\beta w_k$ into $W_n$, and the factor $e^{-\beta U(\mathbf x_n)}$ cancels as before:

$$
W_n\propto\frac{1}{\sum_kN_k\,e^{f_k-\beta w_k(\xi_n)}} .
$$

<div class="legend" markdown="1">
- $\propto$: "proportional to". The missing constant is fixed by making the weights add up to 1.
- $\xi_n$: the collective variable in frame $n$.
- $\beta w_k(\xi_n)$: the bias energy that frame $n$ would have in window $k$, in units of $k_BT$.
- Other symbols: as above.
</div>

Read it like this. The weight of a frame depends only on where the frame is along $\xi$. The denominator is the one of the first WHAM equation: the number of frames that the windows together were expected to collect near $\xi_n$, per unit of true probability. It is large where the springs made the simulations oversample and small where they undersampled. Dividing by it puts every region back to its true share.

To get the PMF along $\xi$, make a histogram of the $\xi_n$ in which each frame counts $W_n$ in place of 1, and take $-k_BT\ln$ of it. To get the PMF along another coordinate, do the same with that coordinate and the same weights. This works as far as the pooled frames cover the range of the other coordinate.

MBAR also handles states that differ in temperature or in the Hamiltonian (Module 13). The `pymbar` package implements it. Feed it decorrelated samples.

The Hamiltonian is the energy function of a system (Module 2). Simulations with different energy functions include umbrella windows, as here, and the alchemical states of Module 13. "Decorrelated" refers to the statistical inefficiency $g$ of Module 11: keeping one frame out of every $g$ gives a set of nearly independent samples, which is what the error formula assumes.

## Designing an umbrella sampling calculation

<div data-videos="J7F2aguxTXs A3SxYkoKlnM dvo6noErrbc"></div>

The relation that removes the bias is exact, and WHAM and MBAR are sound ways to join the windows. Whether the result is right depends on choices made before the simulations start and on checks made after them. This section goes through both in the order in which you meet them.

### Choosing the coordinate

**The coordinate.** It must distinguish the states of interest and, ideally, follow the slowest motion. For binding, the distance between the centres of mass of the two binding sites is the standard choice. For folding or coupled folding and binding, the fraction of native contacts $Q$ is common.

The centre of mass of a group of atoms is their mass-weighted average position. $Q$ is the fraction of the contacts present in a reference structure that are formed in a frame (Module 11), a number between 0 and 1.

The method assumes that all coordinates *orthogonal* to $\xi$ equilibrate within each window. If a slow motion is not captured by $\xi$ (a side chain that must flip, a loop that must open, a rotation of the ligand), neighbouring windows sit in different states of that hidden variable and the PMF is wrong, typically showing up as a dependence on the starting configurations.

"Orthogonal to $\xi$" means every way in which the system can move while $\xi$ stays the same. "Equilibrate" means that the window visits all of those arrangements with their Boltzmann probabilities during the run. The derivation needed this. $P_i^{b}(\xi)$ was defined as an integral over *all* configurations with a given $\xi$, and the histogram of a window that is stuck in a part of them estimates something else. The spring helps the system along $\xi$ and along nothing else.

### Spring constant and window spacing

Two numbers define the set of windows: the stiffness $k$ and the distance $\Delta\xi$ between neighbouring centres. They are tied together by the requirement that neighbouring histograms overlap.

<div class="box maths" markdown="1">
**Maths you need here: the Gaussian.** The bell-shaped curve

$$
p(x) = \frac{1}{\sqrt{2\pi}\,\sigma}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

is the Gaussian or normal distribution. $\exp(a)$ is another way to write $e^a$. $x$ is the variable, $\mu$ is the centre of the curve (the mean) and $\sigma$ its width (the standard deviation). About 68 % of the probability lies within one $\sigma$ of the centre and about 95 % within two. At a distance $\sigma$ from the centre the curve has fallen to $e^{-1/2} = 0.61$ of its peak, at $2\sigma$ to $e^{-2} = 0.14$, and at $3\sigma$ to $e^{-4.5} = 0.011$.

The thing to recognise: whenever a probability is the exponential of minus something quadratic in $x$, it is a Gaussian, and you can read $\sigma$ from the coefficient of the square. More in the [toolbox](maths.html#gaussian).
</div>

**Spring constant and spacing.** In a window where the PMF is locally flat, $\xi$ has a Gaussian distribution of width $\sigma=\sqrt{k_BT/k}$.

Where this comes from. The window samples $\xi$ with a probability proportional to $e^{-\beta[W(\xi)+w_i(\xi)]}$. If $W$ is constant across the window, only the spring is left: $P_i^{b}(\xi)\propto e^{-\beta k(\xi-\xi_i)^2/2}$. Compare the exponent with that of the Gaussian in the box, $-(x-\mu)^2/2\sigma^2$. The centre is $\xi_i$, and $1/\sigma^2 = \beta k$, so $\sigma^2 = k_BT/k$.

A stiffer spring gives a narrower histogram, but the width falls only as the square root: four times the stiffness halves the width.

For good overlap, space the centres about one to two $\sigma$ apart:

$$
\Delta\xi\approx(1\text{ to }2)\sqrt{\frac{k_BT}{k}} .
$$

<div class="legend" markdown="1">
- $\Delta\xi$: the distance between the centres of two neighbouring windows, $\xi_{i+1}-\xi_i$.
- $k$: the spring constant of the bias.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- $\sqrt{k_BT/k}$: the width $\sigma$ of the histogram of one window on a flat profile.
- "(1 to 2)": a factor between 1 and 2. This is a rule of thumb.
- $\approx$: "approximately equal to".
</div>

Read it like this. Two neighbouring histograms of width $\sigma$ whose centres are a distance $d$ apart cross midway between the centres, where each has fallen to $e^{-d^2/8\sigma^2}$ of its peak. For $d=\sigma$ that is 0.88, and for $d=2\sigma$ it is 0.61: both windows have plenty of samples in the region between them. For $d=4\sigma$ it is 0.14. For $d=6\sigma$ it is 0.011, and the offset between the two windows then rests on a handful of frames in two tails.

Where the PMF is steep, the window does not sit at its centre: the mean is displaced to $\langle\xi\rangle_i\approx\xi_i - W'(\xi_i)/k$.

Here $\langle\xi\rangle_i$ is the average of $\xi$ in window $i$ (the subscript says that the average is taken in the biased simulation), and $W'(\xi_i)$ is the slope $dW/d\xi$ of the PMF at the centre of the spring, in kJ mol$^{-1}$ nm$^{-1}$ for a distance. The derivation: near the centre, replace the PMF by a straight line, $W(\xi)\approx W(\xi_i)+W'(\xi_i)\,(\xi-\xi_i)$, which is a [Taylor expansion](maths.html#taylor) to first order. The window then samples the landscape $W'(\xi_i)\,(\xi-\xi_i)+\tfrac12k\,(\xi-\xi_i)^2$ plus a constant. Its minimum is where the derivative is zero: $W'(\xi_i)+k\,(\xi-\xi_i) = 0$, so $\xi = \xi_i-W'(\xi_i)/k$.

The histogram keeps its Gaussian shape and its width and moves downhill by the slope divided by the stiffness. This is the spring balance of the hillside picture. The spring stretches until its pull, $k$ times the stretch, equals the push of the slope.

A weak spring on a steep slope slides away from the region it was meant to sample, leaving a gap. Stiffer springs need more windows. Example: $k$ = 1,000 kJ mol$^{-1}$ nm$^{-2}$ gives $\sigma=0.05$ nm, so windows every 0.05 to 0.1 nm, and 20 to 40 windows for a 2 nm path.

The arithmetic: $\sigma = \sqrt{2.494/1000} = 0.0499$ nm, and 2 nm divided by 0.1 nm or by 0.05 nm gives 20 or 40 windows. On a slope of, say, 100 kJ mol$^{-1}$ nm$^{-1}$ this spring lets the window slide by $100/1000 = 0.1$ nm, which is two widths.

So the choice is a compromise. A soft spring gives wide histograms and few windows, but slides on slopes. A stiff spring stays in place, but needs many windows. Nothing requires the same $k$ and the same spacing everywhere: you can use a stiffer spring and closer centres only where the profile is steep (Check yourself 2).

### Starting configurations

**Starting configurations.** Each window needs a starting structure near its centre. They are usually taken from a steered MD run that pulls the system along $\xi$ (Module 14). Pulling fast distorts the structure, and windows then start from unrelaxed configurations: discard the beginning of each window, and where possible generate starting structures in both directions.

In **steered MD** the same kind of spring is attached to $\xi$, and its centre is moved at a constant speed from one end of the path to the other, so that it drags the system along. Frames saved on the way give structures at every value of $\xi$. When the pull is faster than the system can adjust, the structures it leaves behind carry strain: the protein and the solvent have not caught up with the ligand. "Discard the beginning" means leaving the first part of each window out of the analysis, as equilibration (Module 10). "Both directions" means one pull that separates the partners and one that brings them together.

The work done by the moving spring can in principle be converted into a free energy with the Jarzynski equality (Module 13). At practical pulling speeds that estimate does not converge (Module 14). This is why the pull serves here only to produce starting structures, and the free energy comes from the windows.

### Checks and error bars

**Checks.**

1. Plot all histograms: every part of the range must be covered by at least two windows.
2. Split each window in halves, or in several time blocks, and compute the PMF from each. Systematic change with time means the windows are still relaxing.
3. Run in both directions (association and dissociation). The difference is **hysteresis**, and is an honest lower bound on the error.
4. Error bars by bootstrap over decorrelated blocks or, better, over complete independent repeats. Bootstrapping individual frames ignores the correlation and gives error bars that are far too small.

What each check does:

- *Check 1* is the overlap requirement as a picture. Draw the $S$ histograms on one axis. A place where neighbouring curves do not cross well above zero is a gap, and WHAM will bridge it without telling you.
- *Check 2* tests convergence in time. If the PMF from the first half of every window differs in a systematic way from the PMF from the second half, the windows were still relaxing from their starting structures. Discard more of the beginning, or extend the runs.
- *Check 3.* **Hysteresis** means that a result depends on the direction from which the system arrived. If windows started from a pulling-apart run and windows started from a pushing-together run give different profiles, at least one set has not equilibrated its orthogonal coordinates. Both sets can also share an error that the comparison does not show, which is why the difference is a lower bound.
- *Check 4* needs the box below.

<div class="box maths" markdown="1">
**Maths you need here: the bootstrap.** It is a way to get an error bar from the data you have when no formula for the error is available. Treat your $M$ independent pieces of data as a stand-in for all the data you might have collected. Draw $M$ pieces from them at random *with replacement*, so that some are picked twice and some not at all, and repeat the whole analysis on this resampled set. Do that a few hundred times. The spread (standard deviation) of the results is the error estimate.

The method stands or falls with the word "independent": the pieces that you resample must be independent of each other. The standard error and its estimation are in the [toolbox](maths.html#averages).
</div>

For umbrella sampling the pieces are blocks of the trajectory of each window, each block longer than the correlation time (Module 11), or whole repeats of the calculation started from different structures. Single frames are not independent pieces. Neighbouring frames are nearly copies of each other, so resampling them reproduces almost the same histogram every time, and the spread comes out far too small. The counting rule $\delta W\approx k_BT/\sqrt n$ fails for the same reason when $n$ is a number of frames and not a number of independent samples.

### Two related techniques

**Umbrella integration** is an alternative to WHAM: from the mean and variance of $\xi$ in each window, estimate the mean force, $\partial W/\partial\xi\approx k_BT(\xi-\langle\xi\rangle_i)/\sigma_i^2 - k(\xi-\xi_i)$, and integrate numerically. It needs no iteration and makes noise easy to see.

Here $\langle\xi\rangle_i$ and $\sigma_i^2$ are the mean and the variance of $\xi$ measured in window $i$, and $\partial W/\partial\xi$ is the slope of the PMF. The formula comes from the framed result of the umbrella section, $W = -k_BT\ln P_i^{b}-w_i+F_i$, differentiated with respect to $\xi$:

- The constant $F_i$ has zero derivative and disappears. This is why no iteration is needed.
- The spring gives $dw_i/d\xi = k\,(\xi-\xi_i)$.
- For the histogram, assume a Gaussian with the measured mean and variance, so that $\ln P_i^{b} = -(\xi-\langle\xi\rangle_i)^2/2\sigma_i^2$ plus a constant. Its derivative is $-(\xi-\langle\xi\rangle_i)/\sigma_i^2$, and multiplying by $-k_BT$ gives the first term of the formula.

"Integrate numerically" means adding up slope times step along $\xi$, which recovers $W$ from its slope ([toolbox](maths.html#integral)). The measured $\sigma_i$ is close to the flat-profile value $\sqrt{k_BT/k}$ but not equal to it, because the curvature of the PMF changes the width.

**Replica exchange between windows** (Module 14) lets configurations move between neighbouring windows and helps the orthogonal degrees of freedom relax.

All windows run at the same time, and at intervals neighbouring windows try to swap their current configurations. A swap is accepted with a probability that leaves the distribution of every window correct (Module 14 gives the rule). A structure that has found, say, the flipped side chain in one window can then travel to the others.

## From a PMF to a binding constant

<div data-videos="z2C6siB6Qqo iLw7acCoCrs"></div>

An experiment on binding does not report a profile. It reports one number: a dissociation constant $K_d$, or a standard binding free energy $\Delta G^\circ$. This section turns the profile into that number. The conversion is short. The depth of the well alone is not the answer, and the section shows what else enters.

<div class="box physics" markdown="1">
**Physics you need here: the equilibrium constant.** A protein P and a ligand L bind and separate all the time: $\text{P}+\text{L}\rightleftharpoons\text{PL}$. At equilibrium the concentrations satisfy the law of mass action,

$$
K_a = \frac{[\text{PL}]}{[\text{P}][\text{L}]},\qquad K_d = \frac{1}{K_a} = \frac{[\text{P}][\text{L}]}{[\text{PL}]} .
$$

Square brackets mean concentration: $[\text{L}]$ is the concentration of free ligand, $[\text{P}]$ of free protein and $[\text{PL}]$ of the complex. $K_a$ is the **association constant** and $K_d$ the **dissociation constant**.

Rearranged, $[\text{PL}]/[\text{P}] = [\text{L}]/K_d$: the ratio of occupied to empty protein equals the free ligand concentration measured in units of $K_d$. So $K_d$ is the free ligand concentration at which half of the protein is occupied, and a smaller $K_d$ means tighter binding. $K_d$ is a concentration, so $K_a$ has the unit of one over a concentration, which is a volume per molecule (or litres per mole). More in the [primer](physics.html#equilibrium).
</div>

Let $W(r)$ be the PMF along the separation of two molecules, **with** the Jacobian removed, shifted so that $W\to0$ at large $r$ where the molecules do not interact. The equilibrium constant for association is the ratio of the bound-state configurational integral to that of the two free molecules at unit concentration:

$$
K_a = 4\pi\int_{0}^{r_b}r^2\,e^{-\beta W(r)}\,dr ,\qquad K_d=\frac{1}{K_a},
$$

where $r_b$ marks the end of the bound region.

<div class="legend" markdown="1">
- $W(r)$: the PMF along the separation $r$, with the Jacobian removed and with its zero at large $r$. Inside the binding well it is negative.
- $e^{-\beta W(r)}$: the factor by which the ligand is more likely to be found at the distance $r$ than it would be without any interaction. It is 1 far away and very large in the well.
- $4\pi r^2\,dr$: the volume of the shell of positions between $r$ and $r+dr$.
- $\int_0^{r_b}\dots\,dr$: add up the contributions of all shells from the centre out to $r_b$.
- $r_b$: the distance up to which the pair counts as bound. You choose it at the outer edge of the well.
- $K_a$: the association constant, here in nm$^3$ (per molecule).
- $K_d$: the dissociation constant, here in nm$^{-3}$ (molecules per nm$^3$).
- $\beta = 1/k_BT$.
</div>

### Where the formula comes from

Take one protein in a solution of ligand that is dilute enough for the ligand molecules not to meet each other. Far from the protein the ligand has a uniform number density $[\text{L}]$, in molecules per nm$^3$. Near the protein the interaction changes the density. With the Jacobian removed and the zero at large distance, $e^{-\beta W(r)}$ is the factor by which it is changed: the local density at the distance $r$ is $[\text{L}]\,e^{-\beta W(r)}$.

The average number of ligand molecules in the bound region is the density added up over the volume of that region, shell by shell:

$$
\text{average number of ligands within } r_b = [\text{L}]\times4\pi\int_{0}^{r_b}r^2\,e^{-\beta W(r)}\,dr = [\text{L}]\,K_a .
$$

<div class="legend" markdown="1">
- $[\text{L}]$: the number density of free ligand far from the protein, in molecules per nm$^3$.
- $[\text{L}]\,e^{-\beta W(r)}$: the local ligand density at the distance $r$ from the protein.
- Other symbols: as in the list above.
</div>

When this number is much smaller than 1, it is the fraction of the proteins that have a ligand in the site, divided by the fraction that have none (which is then nearly 1). The law of mass action writes the same ratio as $[\text{PL}]/[\text{P}] = K_a[\text{L}]$. The two agree if $K_a$ is the integral. That is the meaning of the sentence about configurational integrals: the integral measures the weighted volume available to the bound ligand, and a free ligand at unit concentration has unit volume to itself.

Read it like this. $K_a$ is a volume. With no interaction at all ($W=0$ everywhere) the integral would be $\tfrac43\pi r_b^3$, the plain volume of the sphere, and the number of ligands inside would be concentration times volume. The interaction multiplies the volume of every shell by $e^{-\beta W}$, a huge number in the well. So $K_a$ is the volume of bulk solution that holds, on average, as much ligand as the binding site does.

The choice of $r_b$ hardly matters for a deep well. Moving it outwards adds shells in which $e^{-\beta W}\approx1$, that is, a few nm$^3$ of ordinary volume, to a number that the worked example below puts at hundreds of millions of nm$^3$.

### The standard concentration, and why it must appear

$K_a$ has units of volume, nm$^3$ per molecule. To get the usual molar units, divide by the volume per molecule at 1 mol/L, $V^\circ = 1/C^\circ = 1.661$ nm$^3$:

$$
\Delta G^\circ_{bind} = -k_BT\ln\frac{K_a}{V^\circ} = -k_BT\ln\big(K_aC^\circ\big),\qquad K_d\,[\text{M}] = \frac{V^\circ}{K_a} .
$$

<div class="legend" markdown="1">
- $C^\circ$: the **standard concentration**, 1 mol/L (written 1 M), which is 0.6022 molecules per nm$^3$. The small circle marks a standard-state quantity.
- $V^\circ = 1/C^\circ$: the volume per molecule at the standard concentration, 1.661 nm$^3$.
- $K_a/V^\circ = K_aC^\circ$: the association constant as a pure number. It is also its value in litres per mole.
- $\Delta G^\circ_{bind}$: the **standard binding free energy**, in kJ/mol: the free-energy change on binding when free protein, free ligand and complex are all at the standard concentration. The more negative, the tighter the binding.
- $K_d\,[\text{M}]$: the dissociation constant expressed in mol/L. Here the square brackets give the unit. They are not a concentration.
- $k_BT$, $\ln$: as before.
</div>

Where 0.6022 comes from. One mole is $6.022\times10^{23}$ molecules. One litre is a cube with edges of 0.1 m, which is $10^8$ nm, so it holds $10^{24}$ nm$^3$. A 1 M solution therefore has $6.022\times10^{23}/10^{24} = 0.6022$ molecules per nm$^3$, and each molecule has $1/0.6022 = 1.661$ nm$^3$ to itself, a cube with edges of 1.18 nm.

Why a concentration must appear at all. A logarithm can only be taken of a pure number, and $K_a$ is a volume, so something with the unit of volume has to divide it.

The division has a physical meaning. How favourable binding is depends on what the free ligand gives up. In a dilute solution each free ligand has a large volume to wander in and loses all of it on binding. In a concentrated solution it had less to lose. The free energy of binding therefore depends on the concentration of the free partners, and one number can be quoted only for an agreed reference concentration. Chemistry has agreed on 1 M.

Read it like this. $\Delta G^\circ = -k_BT\ln(K_a/V^\circ)$ compares two volumes: the effective volume $K_a$ of the bound state, and the 1.661 nm$^3$ that a free molecule has at 1 M. A different reference would shift every binding free energy by the same amount. With 1 mM in place of 1 M each free molecule has 1,000 times more volume, and all values become more positive by $k_BT\ln1000 = 17.2$ kJ/mol. A "binding free energy" quoted without its standard state is therefore not a defined number.

The same formula in terms of $K_d$ in mol/L is $\Delta G^\circ = k_BT\ln(K_d/1\,\text{M})$, because $K_aC^\circ$ is one over $K_d$ in molar units. Each factor of 10 in $K_d$ is worth 5.74 kJ/mol at 300 K. A binder with $K_d = 10^{-9}$ M (1 nM) has $\Delta G^\circ = 9\times(-5.74) = -51.7$ kJ/mol.

The letter $G$ is the Gibbs free energy, the free energy for a system at constant pressure, which is how experiments are done. $A$ is the Helmholtz free energy, for constant volume. For binding in a liquid at 1 bar the two differ by the pressure times the change of volume, and even a volume change of a full 1 nm$^3$ would contribute only 0.06 kJ/mol. The [primer](physics.html#thermodynamics) explains the two.

<div class="box key" markdown="1">
**Worked example.** A PMF has a well of depth 50 kJ/mol and width 0.1 nm centred at $r$ = 1.0 nm. At 300 K, $\beta\times50 = 20.05$, so $K_a\approx4\pi(1.0)^2(0.1)\,e^{20.05} = 1.257\times5.1\times10^{8} = 6.4\times10^{8}$ nm$^3$. Then $K_d = 1.661/6.4\times10^8 = 2.6\times10^{-9}$ M, about 3 nM, and $\Delta G^\circ = -2.494\ln(3.9\times10^8) = -49.3$ kJ/mol.

Notice that the well depth (50) and $\Delta G^\circ$ (49.3) are not the same quantity: $\Delta G^\circ$ contains the width of the well and the standard volume. A narrower well of the same depth binds more weakly.

The steps.

1. *The model.* The well is treated as a square well: $W = -50$ kJ/mol for $r$ between 0.95 and 1.05 nm, and zero elsewhere.
2. *The exponent.* $\beta\times50 = 50/2.494 = 20.05$. $W$ is negative in the well, so $e^{-\beta W} = e^{+20.05} = 5.1\times10^{8}$ there.
3. *The integral.* Across the narrow well $r^2$ is nearly constant at $(1.0)^2$ nm$^2$, so the integral is the integrand times the width. $4\pi\times1.0^2\times0.1 = 1.257$ nm$^3$ is the volume of the shell, and it is multiplied by $5.1\times10^{8}$. The part of the range where $W=0$ adds a few nm$^3$ at most and is neglected.
4. *The units.* $K_d$ in mol/L is $V^\circ/K_a$, and $K_aC^\circ = 6.4\times10^{8}/1.661 = 3.9\times10^{8}$.
5. *Where the 0.7 kJ/mol went.* $\Delta G^\circ = -k_BT\ln(e^{20.05}\times1.257/1.661) = -50-2.494\ln(1.257/1.661) = -50+0.70$ kJ/mol. The first term is the depth. The second compares the volume of the bound shell, 1.257 nm$^3$, with the standard volume. Here the two volumes happen to be similar, so the correction is small. A well ten times narrower would lose a further $k_BT\ln10 = 5.74$ kJ/mol.
</div>

Three complications in real systems:

- **The coordinate is one of six.** Two rigid molecules have six relative degrees of freedom: one distance, two angles for the direction, three for the orientation. The simple formula assumes that at each $r$ the simulation samples all orientations and lateral positions correctly. For a protein-protein or protein-peptide complex that is rarely true once the partners separate. The rigorous route ([Woo and Roux 2005](cite:woo2005); [Gumbart, Roux and Chipot 2013](cite:gumbart2013)) adds three kinds of restraint: on the ligand's conformation (RMSD to its bound structure), on its orientation (three angles), and on the direction of the separation vector (two angles that keep the ligand on an axis). It computes the PMF along $r$ with them in place, and adds the free energies of imposing each restraint in the bound state and releasing it in bulk. (The paper describes the same cycle in the binding direction: restrain the free ligand, bring it in, release the restraints in the site.) The bulk terms for direction and orientation need no simulation, because in an isotropic solvent they reduce to integrals of the restraint's Boltzmann factor over angles. The same terms in the bound state do need a simulation (free energy perturbation in the paper). The conformational (RMSD) restraint has to be computed by simulation, for the bound and for the free molecule.
- **Other coordinates need their own standard-state treatment.** If the CV is not a distance, for example $Q$ or an RMSD, the "unbound" end of the profile does not correspond to a defined concentration. The free-energy difference between the two basins of such a profile is a property of *that simulation box*: it depends on the box volume. You must relate the unbound state to a volume to obtain $K_d$, for example through the box volume or a separate distance-based calculation.
- **Finite box.** The PMF must reach its plateau inside the box. With charged partners and slowly decaying interactions this can require a long path.

Some words in these three points need explaining.

*Six degrees of freedom.* To place one rigid body relative to another you need six numbers. Three say where its centre is: the distance $r$ and two angles for the direction in which it lies, like latitude and longitude. Three more say how it is turned about its own centre.

The PMF along $r$ treats the other five as part of "everything else", and the formula for $K_a$ is right only if every window sampled them fully. In the bound state that is easy, because the site holds the ligand in one orientation. At large $r$ the ligand must tumble through all orientations and wander over the whole sphere of directions, which can take far longer than a window lasts.

*Restraints and their free energies.* A **restraint** is an extra energy term that holds some quantity near a chosen value, as the umbrella spring does for $\xi$. The route in the first point holds the troublesome coordinates in place with restraints, so that each window has little left to sample, and then corrects for having done so. The correction is of the same kind as the constant $F_i$ earlier: switching a restraint on or off changes the free energy, and each such change is computed and added.

All the steps together form a second path from the free partners to the complex, beside the direct one in which the ligand binds without help. Two paths between the same end states close a loop, a **thermodynamic cycle**. Free energy depends only on the end states, so both paths give the same difference, and you may compute along whichever is easiest.

*Smaller terms.* The RMSD (root-mean-square deviation) measures how far a structure is from a reference structure, here how far the shape of the ligand is from its bound shape (Module 11). Bulk means far from the protein, in plain solvent. Isotropic means "the same in every direction": in bulk solvent no direction and no orientation is preferred, so the free energy of an angular restraint there is an integral over angles that can be done on paper. Free energy perturbation is a method of Module 13 for the free-energy difference between two energy functions.

*The box volume in the second point.* Put one pair of molecules in a box of volume $V$ and call everything outside the bound region "unbound". The ligand is found at each point with a probability proportional to $e^{-\beta W}$. Added up over the bound region this gives $K_a$, and over the rest of the box, where $W=0$, it gives nearly $V$. So the ratio of the bound to the unbound population is $K_a/V$, when $V$ is much larger than the bound region.

A basin is a well of the profile together with all the arrangements that belong to it. The free-energy difference between the two basins, bound minus unbound, is then $-k_BT\ln(K_a/V)$ (minus $k_BT$ times the logarithm of the ratio of their populations), and it changes when the box changes: doubling the box doubles the unbound population and shifts the difference by $k_BT\ln2 = 1.7$ kJ/mol.

Comparing with $\Delta G^\circ = -k_BT\ln(K_a/V^\circ)$ gives the correction for this simplest case: $\Delta G^\circ$ is the basin difference minus $k_BT\ln(V/V^\circ)$. For a box of 500 nm$^3$ that is $2.494\ln(500/1.661) = 14.2$ kJ/mol. The estimate assumes that the "unbound" basin of the profile contains every unbound arrangement in the box and nothing else.

*Plateau.* The flat part of the profile at large separation, where the molecules no longer feel each other. The zero of $W$ is set there, so the profile must reach it. If the box is too small for the interaction to die away, there is no plateau and no zero.

A PMF also gives a barrier along $\xi$. That barrier is not an activation free energy in the kinetic sense unless $\xi$ is a good reaction coordinate. Module 16 explains what is needed for rates.

An activation free energy is the barrier height that controls how fast a process happens. With a poorly chosen coordinate, arrangements from before and after the real bottleneck can share the same value of $\xi$, and the profile along $\xi$ then does not show the bottleneck.

## Check yourself

<details markdown="1"><summary>1. Why can the bias be factored out of the integral in the derivation?</summary>
Because $w_i$ depends on the configuration only through $\xi(\mathbf r)$, and the delta function fixes $\xi(\mathbf r)=\xi$. Inside the integral $e^{-\beta w_i(\xi(\mathbf r))}$ is therefore the constant $e^{-\beta w_i(\xi)}$.
</details>

<details markdown="1"><summary>2. You use k = 500 kJ mol⁻¹ nm⁻² at 300 K. What window spacing would you choose? The PMF has a slope of 300 kJ mol⁻¹ nm⁻¹ in one region; where does a window centred there actually sit?</summary>
$\sigma=\sqrt{2.494/500} = 0.071$ nm, so centres every 0.07 to 0.14 nm. On the slope the mean is displaced by $W'/k = 300/500 = 0.6$ nm downhill, far outside the window's nominal position. That spring is much too weak for this region: increase $k$ there (and add windows).

Here $\sigma$ is the width of the histogram of one window, $k$ the spring constant and $W'$ the slope of the PMF.
</details>

<details markdown="1"><summary>3. Two neighbouring windows have histograms that do not overlap. What does WHAM return?</summary>
A number, with no warning. The relative offset $F_{i+1}-F_i$ is not determined by any data, so the result depends on numerical noise and the starting guess. The profile will show a meaningless step at the gap.

($F_i$ and $F_{i+1}$ are the free-energy constants of the two windows.)
</details>

<details markdown="1"><summary>4. A PMF along the centre-of-mass distance has a well depth of 60 kJ/mol. A colleague reports "ΔG = −60 kJ/mol". What is missing?</summary>
The integral over the bound-state volume and the standard-state concentration, $K_a = 4\pi\int r^2e^{-\beta W}dr$ and $\Delta G^\circ = -k_BT\ln(K_aC^\circ)$. Also whether the Jacobian was removed, whether orientations were sampled or restrained, and an error estimate.

($K_a$ is the association constant, $W$ the PMF along the distance $r$, and $C^\circ$ the standard concentration of 1 M.)
</details>

<details markdown="1"><summary>5. At 300 K, state B is ten times more populated than state A. What is the free-energy difference? What is it for a factor of 1,000?</summary>
$\Delta A_{A\to B} = -k_BT\ln(P_B/P_A) = -2.494\ln10 = -5.74$ kJ/mol: B is lower by 5.74 kJ/mol. For a factor of 1,000 it is three times as much, $-17.2$ kJ/mol, because $\ln1000 = 3\ln10$.
</details>

<details markdown="1"><summary>6. A program gives a profile along the distance between two particles that is 5.5 kJ/mol lower at 3 nm than at 1 nm, at 300 K. Do the particles repel each other?</summary>
Not necessarily. Two particles with no interaction at all give an uncorrected profile $-k_BT\ln P(r)$ that falls by $2k_BT\ln3 = 2\times2.494\times1.099 = 5.48$ kJ/mol between 1 and 3 nm, only because the shell at 3 nm has nine times the volume. The program has most likely not removed the Jacobian. Add $2k_BT\ln r$ and see whether the profile becomes flat.
</details>

<details markdown="1"><summary>7. A calculation gives an association constant of 1,000 nm³. What are the dissociation constant in mol/L and ΔG° at 300 K?</summary>
$K_d = V^\circ/K_a = 1.661/1000 = 1.66\times10^{-3}$ M, about 1.7 mM. $\Delta G^\circ = -k_BT\ln(K_a/V^\circ) = -2.494\ln(602) = -2.494\times6.40 = -16.0$ kJ/mol. ($V^\circ = 1.661$ nm$^3$ is the volume per molecule at 1 M.)
</details>

## Exercises

1. In the demo above, find the smallest number of windows that still gives an RMS error below 0.3 $k_BT$ at $h=10$ with $k=40$. Explain the failure when there are fewer.
2. Write your own WHAM in Python (20 lines) for the one-dimensional double well, generating the data with overdamped Langevin dynamics. Compare with the exact potential.
3. Analyse the same data with `pymbar` and compare the free energies of the windows and the error estimates with your WHAM.
4. For the worked example, recompute $K_d$ if the well is 45 kJ/mol deep, and if it is 50 kJ/mol deep but 0.3 nm wide. Which matters more?
5. Derive the WHAM equations by maximising the likelihood of observing the histograms $\{n_i(\xi)\}$ given $P(\xi)$ and the $F_i$.

## Read

{{READ}}

## Key papers

{{PAPERS}}
