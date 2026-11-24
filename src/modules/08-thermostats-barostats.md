---
num: 8
title: Thermostats and barostats, controlling temperature and pressure
short: Thermostats and barostats
part: Part II · The engine
hours: 7
summary: Understand how each thermostat and barostat modifies the equations of motion, which of them sample the correct ensemble, and which to use for equilibration and for production.
videos: 8
papers: D
tags: thermostats-barostats
---

<div class="box goal" markdown="1">
#### After this module you can

- compute temperature and pressure from a trajectory and say how much they should fluctuate;
- write the equations of the Berendsen, velocity-rescale, Andersen, Langevin and Nosé-Hoover thermostats;
- show that Langevin dynamics and Nosé-Hoover dynamics have the canonical distribution as their stationary state;
- explain Berendsen, Parrinello-Rahman, Monte Carlo and stochastic cell rescaling barostats;
- choose a defensible combination and coupling time for your own simulation.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

A simulation that follows Newton's law and nothing else keeps its total energy fixed. A sample in a laboratory does not. It sits in a tube at the temperature of the room and under the pressure of the air, and it trades heat and volume with its surroundings all the time. A **thermostat** and a **barostat** are the parts of an MD program that stand in for those surroundings. The thermostat changes the velocities of the atoms so that the system behaves as if it touched something at a fixed temperature, and the barostat changes the size of the box so that the system behaves as if a fixed pressure pushed on it.

There are many thermostats and barostats, and they differ in two ways that matter to you. Some produce the correct statistics and some do not. Some leave the natural motion of the atoms almost untouched and some change it strongly. This module goes through them one at a time, so that you can read the methods section of a paper, or write your own, and know what each choice does.

The module has four layers:

1. **What "the right temperature" means.** The temperature of a simulation is computed from the velocities. It goes up and down from step to step, and the size and the shape of that fluctuation are known exactly.
2. **Five thermostats.** Each one comes first as a picture and then as equations: rescaling all velocities (Berendsen, stochastic velocity rescaling), random collisions (Andersen), friction plus random kicks (Langevin), and one extra variable that brakes and pushes the atoms (Nosé-Hoover).
3. **Pressure and the barostats.** How the pressure is computed, why it is so noisy, and the barostats, which repeat the ideas of the thermostats with the volume of the box in the place of the kinetic energy.
4. **A protocol.** Which combination to use for equilibration, which for production, and how to choose the coupling times.

On a first reading you can skip the two proofs (the box "Why that amplitude" and the part headed "Proof that this is canonical") and every block marked "Optional". Do not skip the picture at the start of each thermostat and barostat, the summary tables or the protocol.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The conventions below appear for the first time in this module, or are used so often here that a reminder helps. More in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $T_0$, $P_0$ | A subscript 0 marks the **target** value, the one you ask for in the input file, for example 300 K and 1 bar. |
| $T_{inst}$, $P_{inst}$ | "inst" is short for **instantaneous**: the value computed from the positions and velocities of one single time step. |
| $\langle A\rangle$ | Angle brackets: the **average** of $A$, over a long run or over many repetitions. |
| $\delta A$ | The deviation of $A$ from its average at this instant, $A - \langle A\rangle$. (This is not the delta function.) |
| $\Delta t$ and $dt$ | $\Delta t$ is the time step of the simulation, a definite number such as 2 fs. $dt$ is an interval so short that it is treated as going to zero. |
| $dK = \dots\,dt + \dots\,dW$ | An equation written with small changes: "in the short time $dt$, $K$ changes by this much". |
| $dW$ | **Wiener noise**: a new random number for every interval $dt$, with mean zero and variance $dt$. Explained in the section on stochastic velocity rescaling. |
| $\boldsymbol\xi\sim\mathcal N(0,1)$ | "$\boldsymbol\xi$ is drawn from a Gaussian (normal) distribution with mean 0 and variance 1." |
| $\leftarrow$ | Assignment, as in a program: replace the quantity on the left by the value on the right. |
| $\propto$ | "Is proportional to": equal up to a constant factor. |
| $\Longrightarrow$ | "From which it follows that." |
| $\tau_T$, $\tau_P$ | A **coupling time** (Greek tau): how long the thermostat or the barostat takes to act, in picoseconds. |
| $\beta$ | Shorthand for $1/(k_BT)$, where $k_B$ is the Boltzmann constant and $T$ the temperature. At 300 K, $k_BT = 2.494$ kJ/mol. |

<div class="box warn" markdown="1">
**Letters that mean two things in this module.** The lists under the formulas say which meaning applies each time.

- $P$ is the pressure, except in $P(K)$ and $P(v_x)$, which are probability densities, and in $P_{acc}$, an acceptance probability.
- $\xi$ (Greek xi) is the Nosé-Hoover thermostat variable. The bold $\boldsymbol\xi$ in the Langevin and Brownian formulas is a set of Gaussian random numbers. Capital $\Xi$ is the virial.
- $W$ is the "mass" of the piston in Andersen's barostat. It has nothing to do with the Wiener noise $dW$.
- $H$ is the Hamiltonian, the total energy written as a function of positions and momenta (Module 2). Only in the label $(N,P,H)$ does it stand for the enthalpy.
- $K$ is the kinetic energy, $\bar K$ its target value, and bold $\mathbf K$ the kinetic-energy tensor.
- $\delta V$ is a deviation from the average, $\delta_{ab}$ is the Kronecker delta and $\delta(t-t')$ the Dirac delta.
- $\lambda$ and $\mu$ are scale factors here. In Module 2, $\lambda$ was the Lyapunov exponent and $\mu$ the reduced mass.
- $Q$ is the "mass" of the Nosé-Hoover thermostat here. In Module 3 it was the partition function.
- $\nu$ is the Greek letter nu, a collision frequency. It is not the letter v of a velocity.
</div>

## Why control temperature at all

<div data-videos="5LALoxDs0ic"></div>

Put a cup of hot coffee on a table. It cools to the temperature of the room and then stays there. The room does not get noticeably warmer, because it is so much larger than the cup. A body like the room, large enough to give or take heat without changing its own temperature, is called a **heat bath**. Every laboratory sample has one: the buffer around a protein, the wall of the tube, the air.

A simulation box has no surroundings. With periodic boundaries (Module 7) the box is surrounded only by copies of itself, and nothing outside it can give or take energy. Such a system is called isolated, and Module 2 showed that its total energy stays constant. A thermostat is an algorithm that plays the part of the missing heat bath.

<div class="box physics" markdown="1">
**Physics you need here: the three ensembles.** Fix a few large-scale properties of a system, for example the number of atoms, the volume and the temperature. Very many different arrangements of positions and velocities are compatible with them. An **ensemble** (Module 3) is the rule that says how probable each of these microscopic states is. Which rule applies depends on what is held fixed:

- **NVE, the microcanonical ensemble.** The number of atoms $N$, the volume $V$ and the total energy $E$ are fixed. This is an isolated system. Every state with the energy $E$ is equally probable.
- **NVT, the canonical ensemble.** $N$, $V$ and the temperature $T$ are fixed. The system exchanges heat with a bath, so its energy goes up and down. A state with total energy $H$ has a probability proportional to $e^{-\beta H}$, the Boltzmann factor, with $\beta = 1/(k_BT)$. States of high energy are exponentially rarer.
- **NPT, the isothermal-isobaric ensemble.** $N$, the pressure $P$ and $T$ are fixed. The volume also goes up and down, as if one wall of the box were a movable piston. A state has a probability proportional to $e^{-\beta(H+PV)}$.

A simulation **samples** an ensemble when the states it visits along the trajectory turn up with the frequencies that the ensemble prescribes. Averages over the trajectory are then the averages of that ensemble. This property is what the whole module is about. More on heat and temperature in the [primer](physics.html#thermodynamics).
</div>

Newtonian MD conserves energy and samples the microcanonical (NVE) ensemble. We usually want the canonical (NVT) or isothermal-isobaric (NPT) ensemble because:

- experiments are done at fixed temperature and pressure;
- numerical errors (integration, cutoffs, constraints) add or remove energy slowly, and without a thermostat the temperature drifts;
- non-equilibrium procedures (pulling, alchemical changes, equilibration from a poor start) put work into the system that has to be removed.

The second and third reasons need a word. No program solves Newton's equations exactly. The time step is finite (Module 4), forces are cut off or approximated beyond some distance (Module 7), and bond constraints are solved only to a tolerance (Module 9). Each of these changes the energy by a tiny amount at every step, and over millions of steps the amounts add up.

*Work* is energy that you put into the system from outside by forcing it to change. Pulling two molecules apart (Module 12) does work, and so does switching an interaction off gradually (the "alchemical" changes of Module 13). A starting structure with atoms too close together releases energy in the same way as it relaxes. All of this energy ends up as heat. In an experiment the heat bath carries it away, and in a simulation the thermostat must.

### Temperature in a simulation: a number that fluctuates

There is no thermometer in a simulation. The program computes the temperature from the velocities of the atoms. Temperature measures the average kinetic energy (energy of motion) per degree of freedom, where a **degree of freedom** is one independent way in which the system can move. By the equipartition theorem of Module 3, each degree of freedom carries $\tfrac12k_BT$ of kinetic energy on average, so the average kinetic energy of the whole system is $\langle K\rangle = \tfrac12N_{df}k_BT$. The program turns this relation around and uses the kinetic energy of the present step to define an **instantaneous temperature**:

$$
T_{inst} = \frac{2K}{N_{df}\,k_B},\qquad K = \sum_i \tfrac12 m_i\mathbf v_i^2 .
$$

<div class="legend" markdown="1">
- $T_{inst}$: the instantaneous temperature, in kelvin. It is computed anew at every step.
- $K$: the total kinetic energy at this step, in kJ/mol.
- $\sum_i$: a sum over all atoms $i$.
- $m_i$, $\mathbf v_i$: the mass and the velocity of atom $i$. $\mathbf v_i^2$ is the speed squared, $v_{ix}^2+v_{iy}^2+v_{iz}^2$.
- $N_{df}$: the number of degrees of freedom. For $N$ atoms in a periodic box it is $3N$ minus the number of constraints minus 3 (Module 3). For a solvated protein it is tens or hundreds of thousands.
- $k_B$: the Boltzmann constant, $0.0083145$ kJ mol$^{-1}$ K$^{-1}$. It converts a temperature into an energy.
</div>

Read it like this: add up the kinetic energy, divide by the number of degrees of freedom to get the share of each, and divide by $\tfrac12k_B$ to turn that share into kelvin. If every atom moved 1 % faster, $K$ and $T_{inst}$ would both be 2 % higher, because the velocities enter squared. More on temperature as kinetic energy in the [primer](physics.html#temperature).

The atoms speed up and slow down all the time as they climb and descend each other's potential energy, and a heat bath gives and takes energy in random portions. So $K$, and with it $T_{inst}$, changes from step to step. To say by how much, we need three words from statistics.

<div class="box maths" markdown="1">
**Maths you need here: mean, variance, standard deviation and probability density.** Take five readings of a temperature: 298, 301, 300, 302 and 299 K.

- The **mean** is their sum divided by their number: $1500/5 = 300$ K.
- The deviations from the mean are $-2$, $1$, $0$, $2$ and $-1$ K. The **variance** is the mean of the squared deviations: $(4+1+0+4+1)/5 = 2$ K$^2$.
- The **standard deviation** is the square root of the variance, $1.4$ K. It has the unit of the quantity itself and tells you the typical distance of a reading from the mean.
- The **relative** standard deviation is the standard deviation divided by the mean: $1.4/300 = 0.0047$, or 0.47 %.

For a quantity $x$ that can take any value, the **probability density** $P(x)$ says how the readings are spread: $P(x)\,dx$ is the probability of finding a value between $x$ and $x+dx$. In practice it is the histogram of very many readings, drawn with narrow bins and scaled so that its total area is 1. More in the toolbox: [densities](maths.html#probability), [mean and variance](maths.html#averages).
</div>

From Module 3, the instantaneous temperature is $T_{inst} = 2K/(N_{df}k_B)$, and in the canonical ensemble it must fluctuate with relative standard deviation $\sqrt{2/N_{df}}$.

Put numbers in. A small system of 100 atoms has $N_{df} = 297$, and $\sqrt{2/297} = 0.082$: at 300 K the temperature should wander by about 25 K around the mean. A solvated protein with $N_{df} = 60{,}000$ (a round number for illustration) has $\sqrt{2/60{,}000} = 0.0058$, which is 1.7 K at 300 K. The fluctuation gets smaller as the system gets larger, because the ups and downs of many independent atoms partly cancel, but it is never zero.

A thermostat's job is to make the *distribution* of kinetic energy correct, not to pin $T_{inst}$ to a number. More precisely, the kinetic energy must follow a gamma distribution:

$$
P(K)\propto K^{N_{df}/2-1}\,e^{-\beta K}.
$$

<div class="legend" markdown="1">
- $P(K)$: the probability density of the kinetic energy (see the box above). Here $P$ is not the pressure.
- $\propto$: proportional to. The constant in front, which makes the total probability 1, is left out.
- $K$: the total kinetic energy.
- $N_{df}$: the number of degrees of freedom, so the exponent $N_{df}/2-1$ is a large number for a real system.
- $e^{-\beta K}$: the Boltzmann factor for the kinetic energy.
- $\beta$: $1/(k_BT_0)$, with $T_0$ the temperature of the heat bath.
</div>

Read it like this. The formula is a product of two factors that pull in opposite directions. The first, $K^{N_{df}/2-1}$, rises with $K$: it counts in how many ways the atoms can share out a kinetic energy $K$ among their velocities, and there are more ways when there is more energy to share. The second, $e^{-\beta K}$, falls with $K$: the bath gives up large amounts of energy only rarely. The product is a single hump, and this hump is called a **gamma distribution**.

Three numbers describe the hump, and all follow from the formula:

- its mean is $\tfrac12N_{df}k_BT_0$, the equipartition value;
- its variance is $\tfrac12N_{df}(k_BT_0)^2$;
- so its relative standard deviation is $\sqrt{\tfrac12N_{df}}\,k_BT_0$ divided by $\tfrac12N_{df}k_BT_0$, which is $\sqrt{2/N_{df}}$.

Because $T_{inst}$ is $K$ multiplied by a constant, it has the same relative standard deviation. That is where the $\sqrt{2/N_{df}}$ of Module 3 comes from.

<details markdown="1"><summary>Optional: where the factor $K^{N_{df}/2-1}$ comes from</summary>
In the canonical ensemble each velocity component is an independent Gaussian random number (the Maxwell-Boltzmann distribution, Module 3). The probability of a whole set of velocities is proportional to $e^{-\beta K}$, and it depends on the velocities only through $K$. To get the probability of a value of $K$, multiply by the amount of "velocity space" that has this $K$.

Take two degrees of freedom and equal masses: $K = \tfrac12m(v_x^2+v_y^2)$. All points with the same $K$ lie on a circle of radius $v = \sqrt{2K/m}$ in the $(v_x,v_y)$ plane. The points with kinetic energy between $K$ and $K+dK$ fill a thin ring of area $2\pi v\,dv$. Since $dK = mv\,dv$, the area is $(2\pi/m)\,dK$, which does not depend on $K$. So $P(K)\propto e^{-\beta K}$, and indeed $N_{df}/2-1 = 0$.

With three degrees of freedom the ring becomes a spherical shell of volume $4\pi v^2\,dv$. Now $v\propto\sqrt K$ and $dv\propto dK/\sqrt K$, so the volume is proportional to $K\cdot K^{-1/2}\,dK = K^{1/2}\,dK$, and $N_{df}/2-1 = \tfrac12$. In $N_{df}$ dimensions the shell has a volume proportional to $v^{N_{df}-1}\,dv$, which gives $K^{(N_{df}-1)/2}\cdot K^{-1/2} = K^{N_{df}/2-1}$. Different masses change only the constant in front.
</details>

### What "samples the canonical ensemble" asks of a thermostat

The phrase appears in every section that follows, so here is what it means in practice. A thermostat samples the canonical ensemble if a long run visits each state, positions and velocities together, with a frequency proportional to $e^{-\beta H}$. One consequence that you can test is the histogram of the kinetic energy: it must be the gamma distribution above. Three cases are possible:

- The histogram is a single spike. The kinetic energy is pinned to one value. This is the wrong ensemble, however good the flat temperature plot looks.
- The histogram has the right mean but is too narrow. The fluctuations are suppressed. Still the wrong ensemble.
- The histogram is the gamma distribution. This is necessary for a correct thermostat. The thermostats labelled "canonical" below also leave the distribution of the positions correct.

Why care, if the mean is right in all three cases? First, some quantities are computed from fluctuations: Module 3 showed that the heat capacity is the variance of the energy. Second, a thermostat that distorts the fluctuations can move energy between different motions of the molecule in ways that do not happen in reality. The Berendsen thermostat below does both.

## Thermostats

<div data-videos="l-uZaSvlycY ey1tv0yoyGc HiZ7gvtmDbk pCm2i6kQs4E X3K5A96-U4E"></div>

The temperature is computed from the velocities, so every thermostat works by changing velocities. The five thermostats of this section do it in four different ways:

- **Rescaling.** At every step, multiply all velocities by one common factor close to 1. Berendsen and stochastic velocity rescaling.
- **Collisions.** Now and then, give one atom a completely new random velocity. Andersen.
- **Friction and noise.** At every step, slow every atom down a little and give it a small random kick. Langevin.
- **A feedback variable.** One extra variable brakes all atoms when the system is too hot and pushes them when it is too cold. Nosé-Hoover.

Two pairs of words classify them. A thermostat is **global** if it looks at the kinetic energy of the whole system and treats all atoms alike (rescaling, Nosé-Hoover), and **local** if it acts on each atom separately (Andersen, Langevin). It is **stochastic** if it uses random numbers (stochastic velocity rescaling, Andersen, Langevin) and **deterministic** if it does not (Berendsen, Nosé-Hoover), so that the same start always gives the same trajectory.

For each thermostat, ask three questions. Does it sample the canonical ensemble? How much does it disturb the natural motion of the atoms? And how does it approach the target temperature, smoothly or with oscillations?

### Simple velocity scaling, and Berendsen

The crudest method multiplies all velocities each step by $\lambda=\sqrt{T_0/T_{inst}}$. This fixes the kinetic energy exactly, which is the wrong distribution.

Here $\lambda$ (Greek lambda) is a pure number, $T_0$ is the target temperature and $T_{inst}$ the instantaneous temperature before the scaling. The square root is there because the kinetic energy contains the velocities squared. Multiplying every velocity by $\lambda$ multiplies $K$, and so $T_{inst}$, by $\lambda^2$, and $\lambda^2T_{inst} = T_0$.

For example, if $T_{inst}$ is 310 K and the target is 300 K, then $\lambda = \sqrt{300/310} = 0.984$: every atom is slowed by 1.6 % and the temperature is exactly 300 K again. Done at every step, this gives a temperature plot that is a flat line and a histogram of $K$ that is a spike, the first of the three cases above. The method is also called isokinetic scaling ("iso" means "equal").

Berendsen's idea is to do the same thing gently. Think of the coffee cup again. It does not jump to room temperature. It loses heat at a rate proportional to how much hotter it is than the room, fast at first and then ever more slowly. The **Berendsen** thermostat ([1984](cite:berendsen1984)) relaxes the temperature towards the target with a time constant $\tau_T$, as if the system were weakly coupled to a bath:

$$
\frac{dT}{dt} = \frac{T_0-T}{\tau_T}
\qquad\Longrightarrow\qquad
\lambda^2 = 1+\frac{\Delta t}{\tau_T}\left(\frac{T_0}{T_{inst}}-1\right).
$$

<div class="legend" markdown="1">
- $T$: the temperature of the system at this moment. It is the same quantity that is written $T_{inst}$ on the right.
- $T_0$: the target temperature, the temperature of the imagined bath.
- $dT/dt$: the rate at which the temperature changes, in kelvin per picosecond.
- $\tau_T$: the **coupling time** or time constant of the thermostat, in picoseconds. It is the time in which the gap to the target shrinks to 37 % of its size.
- $\Longrightarrow$: the formula on the right follows from the one on the left. The steps are given below.
- $\lambda$: the factor by which every velocity is multiplied at this step. $\lambda^2$ is the factor by which the kinetic energy and the temperature change.
- $\Delta t$: the time step of the simulation.
</div>

<div class="box maths" markdown="1">
**Maths you need here: a first-order differential equation and exponential relaxation.** A differential equation states how fast something changes, and solving it means finding how the thing itself depends on time. The equation

$$
\frac{dy}{dt} = \frac{y_0-y}{\tau}
$$

says: $y$ moves towards the value $y_0$ at a rate proportional to its distance from $y_0$. The constant $\tau$ (Greek tau) is a time. If $y$ has the value $y(0)$ at the time $t = 0$, the solution is

$$
y(t) = y_0 + \big(y(0)-y_0\big)\,e^{-t/\tau} .
$$

Check it by differentiating: the derivative of $e^{-t/\tau}$ is $-e^{-t/\tau}/\tau$, so $dy/dt = -(y(0)-y_0)e^{-t/\tau}/\tau = -(y-y_0)/\tau$, which is the equation. The gap to the target shrinks by the same factor in every equal interval of time: to 37 % after a time $\tau$ ($e^{-1} = 0.37$), to 14 % after $2\tau$ and to 5 % after $3\tau$. Example: start at 310 K with a target of 300 K and $\tau = 0.1$ ps. After 0.1 ps the temperature is $300 + 10\times0.37 = 303.7$ K, and after 0.3 ps it is 300.5 K.

The equation is called **first-order** because only the first derivative $dy/dt$ appears. A first-order relaxation approaches its target from one side and never overshoots. More in the [toolbox](maths.html#ode).
</div>

**From the left formula to the right one.** The left formula says how much the temperature should change in one time step: $\Delta T = (\Delta t/\tau_T)(T_0-T_{inst})$. The thermostat can only change the temperature by scaling the velocities, and a scale factor $\lambda$ changes the temperature from $T_{inst}$ to $\lambda^2T_{inst}$, a change of $(\lambda^2-1)\,T_{inst}$. Set the two changes equal:

$$
(\lambda^2-1)\,T_{inst} = \frac{\Delta t}{\tau_T}\,(T_0-T_{inst}) .
$$

<div class="legend" markdown="1">
- $(\lambda^2-1)\,T_{inst}$: the change of temperature that the scaling produces.
- $(\Delta t/\tau_T)(T_0-T_{inst})$: the change of temperature that the relaxation equation asks for in one step.
- Other symbols: as in the list above.
</div>

Divide both sides by $T_{inst}$ and add 1, and you have the formula for $\lambda^2$.

Read it like this. If the system is too hot, $T_0/T_{inst}$ is smaller than 1, the bracket is negative, $\lambda$ is smaller than 1 and all atoms are slowed. If it is too cold they are sped up. The ratio $\Delta t/\tau_T$ is the fraction of the gap that is closed in one step.

A number: with $\Delta t = 0.002$ ps, $\tau_T = 0.1$ ps, $T_{inst} = 310$ K and $T_0 = 300$ K, the formula gives $\lambda^2 = 1 + 0.02\times(300/310-1) = 0.99935$. The new temperature is $310\times0.99935 = 309.8$ K: one step removed 0.2 K, which is 2 % of the 10 K gap.

Two limits are worth seeing. If you set $\tau_T$ equal to $\Delta t$, the formula becomes $\lambda^2 = T_0/T_{inst}$, the crude scaling of the first paragraph. If you make $\tau_T$ very long, $\lambda$ goes to 1 and the thermostat does nothing: you are back in NVE.

It is stable and brings a system to the target temperature quickly and smoothly. It does **not** generate the canonical ensemble (the 1984 paper did not claim that it does, and the point was settled later): it suppresses the fluctuations of the kinetic energy, and in doing so it slowly transfers energy from high-frequency internal motions into low-frequency ones. The extreme case is the "flying ice cube", where kinetic energy ends up in the translation of the whole system. If you use it at all, use it for equilibration only: current best-practice guides ([Braun et al. 2018](cite:braun2018)) recommend a thermostat that samples the correct ensemble even there.

Why does it suppress the fluctuations? A real heat bath does two things. It pulls the kinetic energy back towards the average, and it also knocks it away from the average at random, by the irregular arrival of energy. The Berendsen formula contains only the pull.

Whenever $K$ is above its target the thermostat pushes it down, whenever it is below the thermostat pushes it up, and the thermostat never pushes it away. What is left of the fluctuation comes from the exchange between kinetic and potential energy alone. The histogram of $K$ comes out narrower than the gamma distribution, the second of the three cases above, and the shorter $\tau_T$ the narrower it is.

The name "flying ice cube" describes the extreme case of this transfer of energy. At equilibrium every degree of freedom should hold the same average kinetic energy, $\tfrac12k_BT$ (equipartition, Module 3). That includes the fast internal vibrations of bonds and angles (the high-frequency motions) and the slow motions of whole molecules and of the whole system (the low-frequency ones). With this thermostat, energy leaks over a long run from the first group to the second.

In the extreme case the molecules hardly vibrate, as if frozen, while the system as a whole drifts through the box. The thermostat does not notice, because it looks only at the total kinetic energy, and the total is still what it should be.

Two words from the paragraph on the properties of this thermostat are used throughout the module. **Equilibration** is the first part of a simulation, in which the system relaxes from its artificial starting structure to the target temperature and density. Its data are thrown away. **Production** is the part that you analyse.

### Stochastic velocity rescaling

The Berendsen thermostat has half of a heat bath: the pull towards the target. The other half is missing: the random give and take of energy. Stochastic velocity rescaling adds it. All velocities are still multiplied by one common factor at each step, but the factor now contains a random number, chosen so that the kinetic energy wanders up and down exactly as it would in contact with a real bath.

To write this down we need an equation that contains randomness.

<div class="box maths" markdown="1">
**Maths you need here: an equation with noise.** An ordinary differential equation such as $dK/dt = a$ can also be written $dK = a\,dt$: in the short time $dt$, $K$ changes by $a\,dt$. Written that way, a random term can be added:

$$
dK = a\,dt + b\,dW .
$$

This is a **stochastic differential equation** ("stochastic" means "containing randomness"). The term $a\,dt$ is the systematic change, called the drift. The term $b\,dW$ is a random kick, and $b$ is its amplitude.

$dW$ is called **Wiener noise**. For each short interval $dt$ it is a new random number, drawn from a Gaussian (bell-shaped) distribution with mean zero and variance $dt$, and independent of the numbers drawn in all other intervals. On a computer with a time step $\Delta t$ you generate it as $\sqrt{\Delta t}$ times a Gaussian random number of variance 1.

Why is the variance $dt$, so that the typical size is $\sqrt{dt}$ and not $dt$? Independent random kicks add up like the steps of a walker who chooses the direction of each step at random. After $n$ steps the walker is typically $\sqrt n$ steps from the start, not $n$, because it is the variances of independent steps that add.

With $a = 0$ and $b = 1$ the equation describes a quantity whose variance after a time $t$ is exactly $t$. For example, 100 kicks with $\Delta t = 0.01$ have a variance of 0.01 each, and their sum has variance $100\times0.01 = 1$, the same as a single kick with $\Delta t = 1$. So the result does not depend on how finely you cut the time. More in the [toolbox](maths.html#random-numbers).
</div>

[Bussi, Donadio and Parrinello (2007)](cite:bussi2007b) kept the idea of a global rescaling but made the target kinetic energy itself a random variable with the correct canonical distribution. The kinetic energy follows

$$
dK = \left(\bar K - K\right)\frac{dt}{\tau_T} + 2\sqrt{\frac{K\bar K}{N_{df}\,\tau_T}}\;dW,\qquad \bar K = \tfrac12N_{df}k_BT_0,
$$

where $dW$ is a Wiener noise.

<div class="legend" markdown="1">
- $dK$: the change of the kinetic energy during the short time $dt$.
- $K$: the kinetic energy at this moment.
- $\bar K$: the target kinetic energy, the average that $K$ must have at the temperature $T_0$. The bar marks "target average".
- $N_{df}$, $k_B$, $T_0$: the number of degrees of freedom, the Boltzmann constant and the target temperature.
- $\tau_T$: the coupling time of the thermostat, in picoseconds.
- $dW$: Wiener noise, a random number with mean zero and variance $dt$ (see the box above).
- $2\sqrt{K\bar K/(N_{df}\tau_T)}$: the amplitude of the noise, which sets how far a random number moves $K$.
</div>

The equation is for the kinetic energy, and the velocities follow from it. At each step the program computes the new value of $K$ and then multiplies every velocity by the square root of (new $K$ divided by old $K$).

The first term is Berendsen. The second supplies exactly the fluctuations Berendsen removes. To see the first statement, multiply Berendsen's equation $dT/dt = (T_0-T)/\tau_T$ on both sides by $\tfrac12N_{df}k_B$, which turns each temperature into the corresponding kinetic energy:

$$
\frac{dK}{dt} = \frac{\bar K-K}{\tau_T} .
$$

<div class="legend" markdown="1">
- $dK/dt$: the rate of change of the kinetic energy when only the first term acts.
- Other symbols: as in the list above.
</div>

Read the second term like this. The random kick is larger when $\tau_T$ is short, because a strongly coupled bath exchanges energy quickly. Compared with $\bar K$ itself, one kick has a relative size of about $2\sqrt{\Delta t/(N_{df}\tau_T)}$. With $N_{df} = 60{,}000$, $\tau_T = 0.1$ ps and $\Delta t = 0.002$ ps this is 0.0012: each step moves the temperature at random by about a tenth of a percent, a third of a kelvin. The pull of the first term keeps these kicks from adding up without limit, and the balance between the two gives a standard deviation of $\sqrt{2/N_{df}}$, here 0.58 %.

<details markdown="1"><summary>Optional: check that the noise has the right size</summary>
*The mean.* Average both sides of the equation. The random term averages to zero, which leaves $d\langle K\rangle = (\bar K-\langle K\rangle)\,dt/\tau_T$. The mean relaxes exponentially to $\bar K$, as with Berendsen.

*The variance.* We need the change of $K^2$. For a small change, $d(K^2) = (K+dK)^2-K^2 = 2K\,dK + (dK)^2$. In ordinary calculus the last term is dropped because it is of the order $dt^2$. Here it stays, because $dK$ contains $dW$ and the square of $dW$ is $dt$ on average. Keeping the terms of order $dt$ gives $(dK)^2 = 4K\bar K\,dt/(N_{df}\tau_T)$.

Now average. The random term of $2K\,dK$ averages to zero again, and

$$
\frac{d\langle K^2\rangle}{dt} = \frac{2\bar K\langle K\rangle-2\langle K^2\rangle}{\tau_T} + \frac{4\bar K\langle K\rangle}{N_{df}\,\tau_T} .
$$

Once the system has settled, the left side is zero and $\langle K\rangle = \bar K$. Multiply by $\tau_T/2$ and rearrange:

$$
\langle K^2\rangle-\bar K^2 = \frac{2\bar K^2}{N_{df}} .
$$

The left side is the variance of $K$. Dividing by $\bar K^2$ and taking the square root gives the relative standard deviation $\sqrt{2/N_{df}}$, the canonical value. With $\bar K = \tfrac12N_{df}k_BT_0$ the variance is $\tfrac12N_{df}(k_BT_0)^2$, as it should be.
</details>

The result samples the canonical ensemble and has first-order (non-oscillating) relaxation. Because it acts on all velocities with one scale factor, it leaves constraints and the centre-of-mass motion untouched, and with a coupling time that is not too short (0.1 ps or more) it disturbs the dynamics very little. It also has an energy-like quantity that should stay nearly constant along a run: a drift in it means the time step is too large. This is `tcoupl = V-rescale` in GROMACS and a good default.

Several phrases in this paragraph carry a physical statement:

- *First-order relaxation.* The average of $K$ obeys the first-order equation of the maths box in the Berendsen section, so a system that starts too hot slides to the target without overshooting.
- *Constraints.* A constraint (Module 9) holds a bond at a fixed length, which means that the two atoms have no velocity relative to each other along the bond. If both velocities are multiplied by the same number, that relative velocity is still zero.
- *Centre-of-mass motion.* The velocity of the system as a whole is set to zero at the start (Module 2). Zero multiplied by any factor is zero. (If it were not zero, the common factor would rescale it together with all other velocities and keep its direction. "Untouched" is exact for the usual case of zero total momentum.)
- *Disturbs the dynamics very little.* The direction of every velocity is kept. Only the common scale of the speeds changes. In the example above the kinetic energy changes by about a tenth of a percent per step, and the speeds by half of that.
- *An energy-like quantity.* The thermostat gives and takes energy, so the total energy is no longer constant. But the program can keep a running sum of all the energy the thermostat has added. The total energy minus that sum would stay exactly constant if the integration were exact, so it can be watched in the same way as the total energy of an NVE run.

### Andersen

Picture the atoms of your system flying through a thin gas of invisible bath particles. Now and then one atom is hit. After the hit it has forgotten how it was moving and leaves with a new velocity that is typical for the temperature of the bath. All other atoms continue undisturbed. That is the whole method.

<div class="box physics" markdown="1">
**Physics you need here: the Maxwell-Boltzmann distribution.** At temperature $T$, each Cartesian component of the velocity of an atom of mass $m$ is a random number with a Gaussian distribution (the bell curve), with mean zero and variance $k_BT/m$ (Module 3):

$$
P(v_x)\propto\exp\left(-\frac{m v_x^2}{2k_BT}\right).
$$

The exponent is the kinetic energy $\tfrac12mv_x^2$ of that component divided by $k_BT$, so this is a Boltzmann factor. The typical speed along one axis is the standard deviation $\sqrt{k_BT/m}$. For a water molecule ($m = 18$ u) at 300 K it is $\sqrt{2.494/18} = 0.37$ nm/ps, or 370 m/s. Heavy atoms are slower and light atoms faster.

"A fresh draw from the Maxwell-Boltzmann distribution" means: generate three Gaussian random numbers of variance 1 and multiply each by $\sqrt{k_BT/m}$. More in the toolbox: [the Gaussian](maths.html#gaussian), [random numbers](maths.html#random-numbers).
</div>

At random times, with collision frequency $\nu$, a particle's velocity is replaced by a fresh draw from the Maxwell-Boltzmann distribution. [Andersen (1980)](cite:andersen1980) showed that this samples the canonical ensemble, provided the collisions let the system reach all of its configurations. The averages do not depend on $\nu$, but the dynamics do: the collisions decorrelate velocities, so diffusion and other dynamical properties are altered. It is useful when dynamics do not matter.

The **collision frequency** $\nu$ (Greek nu) is the average number of collisions that one particle suffers per unit of time, in ps$^{-1}$. In a time step $\Delta t$ each particle is hit with probability $\nu\,\Delta t$. As an illustration, take $\nu = 1$ ps$^{-1}$ and $\Delta t = 0.002$ ps. Each atom then has a chance of 0.002 of being hit in a given step, so in a system of 10,000 atoms about 20 atoms receive new velocities at every step, and each atom is hit about once per picosecond.

Why this gives the canonical ensemble, in words. Right after a collision the velocity of the atom has the canonical distribution by construction. Between collisions the atoms follow Newton's equations, and Module 2 showed that this motion leaves the canonical density $e^{-\beta H}$ unchanged. So neither of the two ingredients disturbs a canonical distribution once it is there, and the collisions push any other distribution towards it. The condition in Andersen's statement is the same as the ergodicity of Module 3: the motion, collisions included, must be able to take the system through all of its states.

The sentence about averages and dynamics separates two kinds of result. An **average** (the mean energy, the density, the distribution of a distance) depends only on which states are visited and how often. A **dynamical property** (a diffusion constant, a rate, a relaxation time) depends on the order in which they are visited and on how long it takes.

"Decorrelate" means "make forget": after a collision the new velocity of an atom has nothing to do with the old one. Diffusion depends on how long an atom keeps moving in one direction, so frequent collisions cut it down. With an Andersen thermostat you can trust the averages and you cannot trust anything that has a time in it.

### Langevin dynamics

<div data-videos="AzCzDYLimvc jonJHFcYTso"></div>

Look at a grain of pollen in water under a microscope and you see it jitter without rest. The water molecules around it, far too small to see, do two things to it. They hit it from all sides at random, which keeps it moving. And they resist its motion: a grain that moves to the right runs into more molecules on its right side, and they slow it down. The random hits and the drag have the same cause, the collisions with the water.

Langevin dynamics gives every atom of the simulation such an invisible fluid. The fluid itself is not simulated. Only its two effects are put into the equation of motion. Add a friction force and a random force to each particle:

$$
m\,\dot{\mathbf v} = \mathbf F(\mathbf r) - \gamma m\,\mathbf v + \sqrt{2\gamma m k_BT}\;\boldsymbol\eta(t),\qquad \langle\eta_a(t)\,\eta_b(t')\rangle = \delta_{ab}\,\delta(t-t').
$$

<div class="legend" markdown="1">
- $m$: the mass of the particle, here one atom. The equation holds for each atom separately.
- $\mathbf v$: its velocity. $\dot{\mathbf v}$ is its acceleration.
- $\mathbf F(\mathbf r)$: the force from the force field, which depends on the positions $\mathbf r$ of the atoms. With this term alone the equation is Newton's law.
- $\gamma$ (Greek gamma): the **friction coefficient**, in ps$^{-1}$. It is a rate: $1/\gamma$ is the time in which friction alone would reduce the velocity to 37 % of its value. You choose it in the input file.
- $-\gamma m\,\mathbf v$: the friction force. It points against the velocity and grows with the speed.
- $k_B$, $T$: the Boltzmann constant and the target temperature (called $T_0$ in the other sections).
- $\boldsymbol\eta(t)$ (Greek eta, bold): the **random force** before its amplitude is put in. It is a vector of three random functions of time, one for each of $x$, $y$ and $z$, each with mean zero.
- $\sqrt{2\gamma mk_BT}$: the amplitude of the random force.
- $\langle\ \rangle$: the average over many repetitions with different random numbers.
- $a$, $b$: labels for the components $x$, $y$, $z$, so $\eta_a$ is component $a$ of the random force. $t$ and $t'$ are two moments in time.
- $\delta_{ab}$: the Kronecker delta, which is 1 if $a$ and $b$ are the same component and 0 otherwise.
- $\delta(t-t')$: the Dirac delta, which is zero unless the two times are equal.
</div>

<div class="box maths" markdown="1">
**Maths you need here: white noise.** The second formula describes the random force. It contains two delta symbols, explained in the [toolbox](maths.html#delta), and says three things.

1. $\delta_{ab}$: the random force along $x$ has nothing to do with the one along $y$ or $z$. In the same way the random forces on different atoms are independent.
2. $\delta(t-t')$ is zero for two different times: the random force at one instant has nothing to do with the random force at any other instant. The noise has no memory. Noise of this kind is called **white noise**.
3. The delta function is infinitely high at $t = t'$, with an area of 1. This fixes the strength: added up over a short time $dt$, the noise gives a random number with variance $dt$. That number is the Wiener noise of the previous section, $\eta(t)\,dt = dW$.

A program never needs $\eta(t)$ itself. It needs the effect of the noise over one time step, and that is an ordinary Gaussian random number.
</div>

The friction removes energy and the noise adds it. The two are tied together by the **fluctuation-dissipation theorem**: the noise amplitude must be $\sqrt{2\gamma mk_BT}$ for the system to settle at temperature $T$.

To see why two terms are needed, switch them on one at a time, with no force from the force field.

- *Friction alone.* The equation is $\dot v = -\gamma v$, with the solution $v(t) = v(0)\,e^{-\gamma t}$. Every velocity decays to zero and the system cools to absolute zero. With $\gamma = 1$ ps$^{-1}$ a velocity falls to 37 % in 1 ps.
- *Noise alone.* Every atom receives random kicks that nothing takes away. The velocity performs a random walk, its variance grows in proportion to the time, and the system heats up without limit.
- *Both.* The faster an atom moves, the more the friction takes from it, while the kicks arrive at the same rate whatever the speed. So there is a speed at which gains and losses balance, and the kinetic energy settles there.

"Dissipation" is the loss of energy of motion to heat, which is what friction does. "Fluctuation" is the noise. The theorem says that the two are not independent: for a bath at temperature $T$, a stronger friction must come with a stronger noise, in the ratio that the amplitude $\sqrt{2\gamma mk_BT}$ expresses. A hotter bath kicks harder for the same friction.

It helps to divide the equation by $m$ and to write it in the form of the noise box, for one component $v$ of the velocity of one atom:

$$
dv = \frac{F}{m}\,dt - \gamma v\,dt + \sqrt{\frac{2\gamma k_BT}{m}}\;dW .
$$

<div class="legend" markdown="1">
- $dv$: the change of the velocity component during the short time $dt$.
- $F$: the same component of the force from the force field.
- $dW$: Wiener noise, the random number of variance $dt$ that $\eta(t)\,dt$ stands for.
- $\sqrt{2\gamma k_BT/m}$: the noise amplitude for the velocity, which is the amplitude for the force divided by $m$.
- Other symbols: as in the list above.
</div>

The box that follows shows where the amplitude comes from. It can be skipped on a first reading.

<div class="box key" markdown="1">
**Why that amplitude.** Take one velocity component with no force: $dv = -\gamma v\,dt + \sigma\,dW$. Here $\sigma$ (Greek sigma) is the noise amplitude for the velocity, which we pretend not to know yet. This is an Ornstein-Uhlenbeck process with solution

$$
v(t) = v(0)\,e^{-\gamma t} + \sigma\int_0^te^{-\gamma(t-s)}dW(s).
$$

"Ornstein-Uhlenbeck process" is the name for any quantity that is pulled back towards zero at a rate proportional to its own value while noise kicks it about. The solution has two parts. The first is the starting velocity, decaying by friction. The second adds up all the kicks received between time 0 and time $t$: the integral sign with $dW(s)$ means "sum over the kicks", and $s$ is the time at which a kick arrived. A kick that arrived at time $s$ has itself been decaying ever since, for a time $t-s$, which is the factor $e^{-\gamma(t-s)}$.

Its mean decays to zero and its variance tends to $\sigma^2/2\gamma$. The mean first: the kicks average to zero, so only the first part is left, and it decays. For the variance, use the rule that the variances of independent random numbers add. The kick of the interval $ds$ has variance $ds$, and it is multiplied by $\sigma e^{-\gamma(t-s)}$, so it contributes $\sigma^2e^{-2\gamma(t-s)}\,ds$:

$$
\text{variance of } v(t) = \sigma^2\int_0^te^{-2\gamma(t-s)}\,ds = \frac{\sigma^2}{2\gamma}\left(1-e^{-2\gamma t}\right).
$$

For times much longer than $1/\gamma$ the exponential is gone and the variance is $\sigma^2/2\gamma$. More noise makes it larger and more friction makes it smaller, as the three cases above suggested.

The Maxwell-Boltzmann distribution requires a variance of $k_BT/m$, so $\sigma^2 = 2\gamma k_BT/m$. Multiply $\sigma$ by $m$ to return from velocity to force, and you have the amplitude $\sqrt{2\gamma mk_BT}$ of the Langevin equation.

The last statement of this box is about the full equation, with forces, and uses three terms. $\rho$ is the density of a cloud of copies of the system in phase space, as in Module 2. The Fokker-Planck equation says how such a density changes in time when the motion contains friction and noise, and is the counterpart of the Liouville equation of Module 2. A stationary solution is a density that does not change in time.

With forces present, one can check that $\rho\propto e^{-\beta H}$ is the stationary solution of the corresponding Fokker-Planck equation: the Hamiltonian part of the flow leaves $e^{-\beta H}$ unchanged (Liouville, Module 2), and the friction and noise terms cancel each other exactly for a Maxwell-Boltzmann distribution of velocities.
</div>

The exact solution over one time step is what integrators use for the "O" step (Module 4):

$$
\mathbf v \leftarrow e^{-\gamma\Delta t}\,\mathbf v + \sqrt{\frac{k_BT}{m}\left(1-e^{-2\gamma\Delta t}\right)}\;\boldsymbol\xi,\qquad \boldsymbol\xi\sim\mathcal N(0,1).
$$

<div class="legend" markdown="1">
- $\leftarrow$: "is replaced by". The $\mathbf v$ on the right is the velocity of one atom before this part of the step, and the $\mathbf v$ on the left is its velocity after it.
- $\Delta t$: the time step.
- $e^{-\gamma\Delta t}$: the fraction of the old velocity that survives the friction during one step.
- $k_BT/m$: the variance that each velocity component must have at temperature $T$.
- $\sqrt{(k_BT/m)(1-e^{-2\gamma\Delta t})}$: the size of the random velocity that is added.
- $\boldsymbol\xi$ (bold): three independent Gaussian random numbers, drawn anew for every atom at every step. This is not the Nosé-Hoover variable $\xi$ of the next section.
- $\sim\mathcal N(0,1)$: "drawn from the normal (Gaussian) distribution with mean 0 and variance 1".
- $\gamma$, $m$, $k_B$, $T$: the friction coefficient, the mass of the atom, the Boltzmann constant and the target temperature, as in the Langevin equation.
</div>

The formula is the solution in the box, read for a time $\Delta t$. The first part of the solution is $e^{-\gamma\Delta t}$ times the old velocity. The second part is a sum of Gaussian kicks, so it is itself a Gaussian random number, and its variance is the one computed in the box with $t = \Delta t$ and $\sigma^2/2\gamma = k_BT/m$. In Module 4 a time step with a Langevin thermostat is split into pieces named by letters: B for the kick by the forces, A for the drift of the positions, and O for this friction-plus-noise part (the O comes from Ornstein-Uhlenbeck).

Read it like this: keep a fraction of the old velocity and replace the rest by a random velocity of the right temperature. With $\gamma = 1$ ps$^{-1}$ and $\Delta t = 0.002$ ps, $e^{-\gamma\Delta t} = 0.998$ and $\sqrt{1-e^{-2\gamma\Delta t}} = 0.063$. Each step keeps 99.8 % of the velocity and adds a random part that is 6.3 % of the typical thermal velocity $\sqrt{k_BT/m}$. If $\gamma\,\Delta t$ is made very large, nothing of the old velocity is kept and every atom receives a fresh Maxwell-Boltzmann velocity at every step, which is an Andersen thermostat that hits every atom every time. You can also check that the step does not change a correct distribution: if the old velocity has variance $k_BT/m$, the new one has variance $e^{-2\gamma\Delta t}\,k_BT/m + (1-e^{-2\gamma\Delta t})\,k_BT/m = k_BT/m$.

Properties: canonical, local (each particle is thermostatted, so it also equilibrates poorly coupled parts of the system), and very robust. The cost is that momentum is not conserved and dynamics are slowed: the friction adds to the natural friction of the solvent. For explicit solvent $\gamma$ = 0.1 to 1 ps$^{-1}$ is a mild perturbation. For implicit-solvent and coarse-grained models there is no solvent friction, and $\gamma$ becomes a parameter that sets the time scale: with low friction the dynamics are much faster than in reality, which helps sampling but means simulated time has no physical meaning.

Some of these properties need unpacking.

- *Local, and poorly coupled parts.* A global thermostat controls only the total kinetic energy. If one part of the system exchanges energy with the rest only slowly, it can stay too hot or too cold for a long time while the total is correct. A local thermostat sets the temperature of every atom, wherever it is.
- *Momentum is not conserved.* In Module 2 the total momentum was conserved because every force on one atom was matched by an opposite force on another (Newton's third law). The random force and the friction force on an atom have no partner, so the total momentum of the system changes at random.
- *Explicit solvent* means that the water molecules are present as atoms. They already slow the solute down by real collisions, and a small $\gamma$ adds little to that.
- *Implicit-solvent* models replace the water by a formula for its average effect, and *coarse-grained* models merge groups of atoms into single beads (Module 15). In both, the collisions that would slow the molecule down are missing, and the only friction is the $\gamma$ that you choose. The populations of the states remain correct for any $\gamma$. The clock does not.

In the limit of high friction the inertial term can be dropped, giving **Brownian (overdamped Langevin) dynamics**:

$$
d\mathbf r = \frac{D}{k_BT}\,\mathbf F\,dt + \sqrt{2D\,dt}\;\boldsymbol\xi,\qquad D = \frac{k_BT}{m\gamma}.
$$

<div class="legend" markdown="1">
- $d\mathbf r$: the change of the position of one particle during the short time $dt$.
- $\mathbf F$: the force on the particle from the force field.
- $D$: the **diffusion constant** of the particle, in nm$^2$/ps. It measures how fast the particle spreads by random motion.
- $D/(k_BT)$: the mobility, the drift velocity per unit of force. It equals $1/(m\gamma)$.
- $\sqrt{2D\,dt}\;\boldsymbol\xi$: a random displacement. $\boldsymbol\xi$ is a set of three Gaussian random numbers of variance 1, as in the O step.
- $m$, $\gamma$, $k_BT$: the mass, the friction coefficient and the thermal energy, as before.
</div>

The "inertial term" is the left side of the Langevin equation, mass times acceleration. A heavy ball rolling on a table has inertia: it keeps moving after you stop pushing. A ball in honey does not. It moves only while it is pushed and stops at once when the push ends. That is the overdamped limit, and "Brownian" refers to the jitter of the pollen grain.

The steps from the Langevin equation: set the left side $m\dot{\mathbf v}$ to zero and solve what remains for the velocity, which gives $\mathbf v = \mathbf F/(m\gamma) + \sqrt{2k_BT/(m\gamma)}\,\boldsymbol\eta(t)$. Multiply by $dt$ to get the displacement $d\mathbf r = \mathbf v\,dt$, and replace $\boldsymbol\eta\,dt$ by $dW$, which a program generates as $\sqrt{dt}$ times a Gaussian number of variance 1. Writing $D$ for $k_BT/(m\gamma)$ gives the formula, since $1/(m\gamma) = D/(k_BT)$. The relation $D = k_BT/(m\gamma)$ is known as the Einstein relation. More in the [primer](physics.html#diffusion).

Read it like this. There is no velocity in the equation any more: the position is moved directly. The first term slides the particle along the force, the faster the smaller the friction. The second is a random step whose size grows as the square root of the time.

Without any force, the variances of the random steps add up, and after a time $t$ the displacement along each axis has a variance of $2Dt$. This spreading is diffusion, and $D$ measures its speed. As an illustration, a bead of 100 u with $\gamma = 10$ ps$^{-1}$ at 300 K has $D = 2.494/(100\times10) = 0.0025$ nm$^2$/ps.

The umbrella-sampling demo in Module 12 uses this equation.

### Nosé-Hoover

A deterministic alternative. Langevin dynamics uses a fixed friction coefficient $\gamma$ and makes up for the energy it removes with random kicks. The Nosé-Hoover thermostat has no random numbers at all. Its friction coefficient is not fixed: it changes in time, it can become negative, and a negative friction accelerates the atoms. A feedback rule steers it.

Think of adjusting a shower whose temperature reacts with a delay. The water is too cold, so you turn the tap towards hot and keep turning while it stays cold. By the time the water is right, the tap is too far, and the water goes on to become too hot. You turn back, overshoot again, and the temperature swings around the value you wanted. The Nosé-Hoover thermostat behaves like this.

Add one extra dynamical variable, a friction coefficient $\xi$ that responds to the kinetic energy:

$$
\dot{\mathbf r}_i = \frac{\mathbf p_i}{m_i},\qquad
\dot{\mathbf p}_i = \mathbf F_i - \xi\,\mathbf p_i,\qquad
\dot\xi = \frac{1}{Q}\left(\sum_i\frac{\mathbf p_i^2}{m_i} - N_{df}k_BT_0\right).
$$

<div class="legend" markdown="1">
- $\mathbf r_i$, $\mathbf p_i$, $m_i$: the position, the momentum (mass times velocity) and the mass of atom $i$. A dot is a time derivative.
- $\mathbf F_i$: the force on atom $i$ from the force field.
- $\xi$ (Greek xi): the thermostat variable, a friction coefficient in ps$^{-1}$. There is one $\xi$ for the whole system. It plays the role of $\gamma$ in Langevin dynamics but changes in time and can have either sign.
- $-\xi\,\mathbf p_i$: the thermostat force on atom $i$. For positive $\xi$ it is a brake, for negative $\xi$ a push along the direction of motion.
- $\dot\xi$: the rate at which the friction coefficient changes.
- $Q$: the thermostat "mass", in units of energy times time squared (kJ mol$^{-1}$ ps$^2$). It is not a real mass.
- $\sum_i\mathbf p_i^2/m_i$: twice the present kinetic energy, $2K$.
- $N_{df}k_BT_0$: twice the target kinetic energy, $2\bar K$, with $N_{df}$ the number of degrees of freedom, $k_B$ the Boltzmann constant and $T_0$ the target temperature.
</div>

A "dynamical variable" is a quantity with its own equation of motion, which the program advances in time together with the positions and momenta. The first equation is the ordinary one: the position changes at the velocity. The second is Newton's law with the thermostat force added. The third is the feedback rule. With $2K$ and $2\bar K$ for the two terms in the bracket it reads

$$
\dot\xi = \frac{2}{Q}\left(K-\bar K\right).
$$

<div class="legend" markdown="1">
- $K$: the present kinetic energy.
- $\bar K$: the target kinetic energy, $\tfrac12N_{df}k_BT_0$.
- Other symbols: as in the list above.
</div>

When the system is too hot the bracket is positive, $\xi$ grows and the friction cools the system. When it is too cold, $\xi$ becomes negative and heats it. The "mass" $Q$ sets the response time: $Q = N_{df}k_BT_0\,\tau_T^2$, where $\tau_T$ is the period of the temperature oscillations up to a numerical factor. [Martyna, Klein and Tuckerman (1992)](cite:martyna1992) suggest $\tau_T = 1/\omega$, with $\omega$ a characteristic frequency of the system, and call it a rough estimate.

(In this course $\omega$ denotes an angular frequency, $2\pi$ divided by the period of a vibration, as in Module 2.)

The important point is in the wording "grows". The excess of kinetic energy does not set the friction. It sets the *rate of change* of the friction. As long as the system is too hot, $\xi$ keeps rising, and when the temperature reaches the target, $\xi$ is at its largest and goes on cooling. This is the tap that has been turned too far.

$Q$ is called a mass because it stands where a mass stands in "acceleration equals force divided by mass". A large $Q$ makes $\xi$ respond slowly and gives slow, gentle swings. A small $Q$ gives fast ones. The name also has a history: the method started from an extended Lagrangian in which the thermostat variable has a fictitious mass and a kinetic energy (Module 2).

In practice you set the time $\tau_T$ (see the practical points below), and $Q$ follows from it. Putting the formula $Q = N_{df}k_BT_0\,\tau_T^2$ into the feedback rule shows what $\tau_T$ does:

$$
\dot\xi = \frac{1}{\tau_T^2}\left(\frac{T_{inst}}{T_0}-1\right).
$$

<div class="legend" markdown="1">
- $\tau_T$: the time constant of the thermostat, in picoseconds.
- $T_{inst}/T_0-1$: the relative error of the temperature, for example 0.01 if the system is 1 % too hot.
- Other symbols: as in the lists above.
</div>

To get this, write $K-\bar K = \tfrac12N_{df}k_B(T_{inst}-T_0)$ and divide by $Q = N_{df}k_BT_0\tau_T^2$. The factors $N_{df}k_B$ cancel. Read it like this: the same temperature error changes $\xi$ a hundred times more slowly if $\tau_T$ is ten times longer.

<details markdown="1"><summary>Optional: why the temperature oscillates, and with what period</summary>
Take the simplest case, in which the kinetic energy changes only because of the thermostat. From $\dot{\mathbf p}_i = -\xi\,\mathbf p_i$ each momentum shrinks at the rate $\xi$, and the kinetic energy, which contains the momenta squared, shrinks at twice that rate: $\dot K = -2\xi K$. Close to the target, replace $K$ on the right by $\bar K$, so that $\dot K\approx-2\bar K\xi$. Now differentiate the feedback rule $\dot\xi = 2(K-\bar K)/Q$ once more in time and insert this:

$$
\ddot\xi = \frac{2\dot K}{Q} = -\frac{4\bar K}{Q}\,\xi = -\frac{2}{\tau_T^2}\,\xi .
$$

The last step used $\bar K = \tfrac12N_{df}k_BT_0$ and $Q = N_{df}k_BT_0\tau_T^2$. This is the equation of a harmonic oscillator, $\ddot x = -\omega^2x$ (Module 2), with angular frequency $\sqrt2/\tau_T$. Its period is $2\pi\tau_T/\sqrt2$, about $4.4\,\tau_T$. In a real system kinetic energy also passes into and out of the potential energy, which changes the number in front. That is the "numerical factor" of the text.

Two first-order equations, one for $K$ and one for $\xi$, have combined into one second-order equation, and a second-order equation can oscillate. Berendsen and stochastic velocity rescaling have a single first-order equation for $K$ and cannot.
</details>

The rest of this section proves that these equations sample the canonical ensemble, and then lists two weaknesses. The proof can be skipped on a first reading. It has three steps and uses Liouville's theorem of Module 2.

Recall the setting of that theorem: imagine a cloud of copies of the system, each a point in **phase space**, the space of all positions and momenta. Here the thermostat variable $\xi$ is one more coordinate of that space. The copies move, and the cloud flows.

**Proof that this is canonical.** The flow is no longer incompressible. Its divergence is

$$
\sum_i\frac{\partial\dot{\mathbf p}_i}{\partial\mathbf p_i} = -N_{df}\,\xi .
$$

<div class="legend" markdown="1">
- $\partial\dot{\mathbf p}_i/\partial\mathbf p_i$: for each component of the momentum of atom $i$, the derivative of its rate of change with respect to that same component, added over the components.
- $\sum_i$: the sum over all atoms. Together with the previous item this is a sum over all independent momentum components, of which there are $N_{df}$.
- $\xi$: the thermostat variable.
</div>

*Step 1: how fast the cloud is compressed.* The **divergence** of a flow measures whether it spreads out (positive) or closes in (negative). You compute it by differentiating the rate of change of every coordinate with respect to that coordinate and adding up ([toolbox](maths.html#divergence)). In Module 2 the sum was zero: Hamilton's equations give an **incompressible** flow, one in which a cloud keeps its volume.

Now go through the three Nosé-Hoover equations. $\dot{\mathbf r}_i = \mathbf p_i/m_i$ does not contain $\mathbf r_i$, and $\dot\xi$ does not contain $\xi$, so neither contributes. In $\dot{\mathbf p}_i = \mathbf F_i-\xi\,\mathbf p_i$ the force depends on positions only, and the derivative of $-\xi p$ with respect to $p$ is $-\xi$. Each independent momentum component therefore contributes $-\xi$, and there are $N_{df}$ of them. With a positive $\xi$ all momenta are being shrunk towards zero, and the cloud contracts.

A remark on the count. Read as a plain sum over all atoms, the left side of the formula would be $-3N\xi$. Constraints and the fixed centre of mass take away components that cannot change independently, and the $N_{df}$ of Module 3 is the number that is left. The proof works only with this count, which is why the same $N_{df}$ stands in the feedback rule.

*Step 2: what that means for the density.* The generalised Liouville equation for a density $f(\mathbf r,\mathbf p,\xi)$ then requires $d\ln f/dt = +N_{df}\,\xi$ along a trajectory. The density $f$ is the number of copies per unit volume of phase space around a given point. If a piece of the cloud shrinks, the same copies are packed into less space and the density there goes up, at a relative rate equal to minus the divergence. A relative rate of change, $(1/f)\,df/dt$, is the same thing as the rate of change of the logarithm, $d\ln f/dt$. So a density that does not change as a whole must have the following property: as you travel with one copy, the value of $\ln f$ at the place where you are rises at the rate $N_{df}\,\xi$.

*Step 3: test a guess.* Try $f\propto\exp\left[-\beta\left(H+\tfrac12Q\xi^2\right)\right]$:

$$
\frac{d\ln f}{dt} = -\beta\left(\dot H + Q\xi\dot\xi\right)
= -\beta\left(-\xi\sum_i\frac{\mathbf p_i^2}{m_i} + \xi\sum_i\frac{\mathbf p_i^2}{m_i} - \xi N_{df}k_BT_0\right) = N_{df}\,\xi .\quad\checkmark
$$

<div class="legend" markdown="1">
- $f$: the guessed density. Its logarithm is $-\beta(H+\tfrac12Q\xi^2)$ plus a constant.
- $\beta$: $1/(k_BT_0)$.
- $H$: the Hamiltonian of the atoms, kinetic plus potential energy.
- $\dot H$: the rate of change of the energy of the atoms. It is the first term in the second bracket.
- $Q\xi\dot\xi$: the time derivative of $\tfrac12Q\xi^2$, by the chain rule. It gives the second and third terms of the second bracket.
- $\checkmark$: the result is what step 2 required.
- Other symbols: as in the list under the Nosé-Hoover equations.
</div>

The line has three equalities. The first takes the time derivative of $\ln f$. The second inserts two things, described next. The third uses that the two sums cancel and that $\beta k_BT_0 = 1$.

The first thing inserted is $\dot H$: by the [chain rule](maths.html#chain-rule), as in the energy proof of Module 2, $\dot H = \sum_i(\mathbf p_i/m_i)\cdot\dot{\mathbf p}_i - \sum_i\mathbf F_i\cdot\dot{\mathbf r}_i$. Insert the equations of motion, and the two terms with $\mathbf F_i$ cancel, leaving $\dot H = -\xi\sum_i\mathbf p_i^2/m_i$: the thermostat force removes energy when $\xi$ is positive. The second thing inserted is $Q\xi\dot\xi$, which by the feedback rule equals $\xi$ times the bracket of that rule.

So $e^{-\beta H}$ times a Gaussian in $\xi$ is stationary. The dynamics are smooth and time-reversible and conserve an extended energy.

The guessed density is a product, $e^{-\beta H}\times e^{-\beta Q\xi^2/2}$. The first factor is the canonical distribution for the atoms, which is what we wanted. The second is a Gaussian distribution of the thermostat variable with mean zero and variance $k_BT_0/Q$. In a long run $\xi$ swings around zero: on average the thermostat neither brakes nor pushes.

The last sentence names three properties:

- *Smooth.* There are no random numbers and no sudden jumps. All velocities change continuously.
- *Time-reversible.* If you reverse all momenta and the sign of $\xi$ and run on, the system retraces its path, as in Module 2.
- *An extended energy.* The energy $H$ of the atoms is not conserved, because the thermostat gives and takes energy. But the following quantity is:

$$
E_{ext} = H + \tfrac12Q\xi^2 + N_{df}k_BT_0\int_0^t\xi(t')\,dt' .
$$

<div class="legend" markdown="1">
- $E_{ext}$: the extended energy, in kJ/mol. It keeps its starting value during the whole run.
- $H$: the energy of the atoms, kinetic plus potential.
- $\tfrac12Q\xi^2$: the "kinetic energy" of the thermostat variable.
- $\int_0^t\xi(t')\,dt'$: the friction coefficient added up over the time from the start of the run to now. $t'$ is the time variable of the sum.
- $N_{df}k_BT_0$: twice the target kinetic energy.
</div>

To check it, differentiate the three terms with respect to time. They give $-\xi\sum_i\mathbf p_i^2/m_i$, then $\xi\left(\sum_i\mathbf p_i^2/m_i-N_{df}k_BT_0\right)$, then $N_{df}k_BT_0\,\xi$, and the sum is zero. The second and third terms together are the energy that the thermostat has taken out of the atoms so far. The use of $E_{ext}$ is the same as that of the total energy in an NVE run: a steady drift in it means that the time step is too long.

Two caveats. The proof shows the canonical density is *a* stationary state, not that the dynamics reach it: for small or stiff systems (a single harmonic oscillator is the textbook case) Nosé-Hoover is not ergodic. **Nosé-Hoover chains** ([Martyna, Klein and Tuckerman 1992](cite:martyna1992)), where the thermostat variable is itself thermostatted by a second, and so on, restore the canonical distribution in the test cases where one thermostat fails (a harmonic oscillator needed two thermostats, a free particle three). This was shown numerically, not proved. And the temperature approaches its target with oscillations, so it is a poor choice for equilibrating a system that starts far from the target.

The first caveat is about the difference between "can stay" and "gets there". The proof shows that a cloud of copies with the canonical density keeps that density. It does not show that one single trajectory visits all states with the right frequencies, which is what **ergodic** means (Module 3) and what a simulation needs. A "stiff" system is one dominated by fast, almost perfectly harmonic vibrations that exchange little energy with each other. In such a system the motion of the atoms and the swing of $\xi$ can stay regular, without the irregular changes of $\xi$ that a large system produces, and the trajectory keeps to a small part of the states.

A chain repairs this by treating the thermostat variable like one more degree of freedom. The Gaussian found above means that the "kinetic energy" $\tfrac12Q\xi^2$ should average $\tfrac12k_BT_0$, the equipartition value. A second thermostat variable watches that quantity and acts as a friction on $\xi$, a third can watch the second, and so on. The added variables are there to make $\xi$ itself fluctuate as its Gaussian distribution requires, which a single thermostat does not ensure.

### Summary of thermostats

The table collects the answers to the three questions asked at the start of this section. "Canonical?" asks whether the thermostat samples the canonical ensemble. "Perturbs dynamics" asks how much it changes the natural motion, which matters if you want diffusion constants, rates or time scales.

| Thermostat | Canonical? | Perturbs dynamics | Good for |
|---|---|---|---|
| Berendsen | No | Little | Fast, smooth equilibration only |
| Stochastic velocity rescaling | Yes | Very little | Equilibration and production |
| Andersen | Yes | Strongly | Sampling when dynamics are irrelevant |
| Langevin | Yes | Depends on $\gamma$ | Implicit solvent, coarse-grained models, free-energy calculations, GPU codes |
| Nosé-Hoover (chains) | Yes | Little | Production of well-equilibrated systems |

**Practical points.** Use $\tau_T$ of 0.1 to 1 ps for velocity rescaling and Nosé-Hoover, and $\gamma\approx1$ ps$^{-1}$ for Langevin in explicit solvent. Thermostat the protein and the solvent as separate groups only if each group is large; coupling very small groups separately creates artefacts. Remove centre-of-mass motion.

*What the coupling time means.* For Berendsen and stochastic velocity rescaling, $\tau_T$ is the time of the exponential approach to the target when nothing but the thermostat changes the kinetic energy: after $3\tau_T$ the gap is then down to 5 %. In a real system the approach is slower (about twice as slow when the motions are harmonic vibrations), because kinetic energy that the thermostat removes is partly replaced from the potential energy. For Nosé-Hoover $\tau_T$ sets the period of the swings.

For Langevin, $1/\gamma$ is the time after which an atom has forgotten its velocity. The kinetic energy, which contains the velocities squared, is brought to its target twice as fast, with the time constant $1/(2\gamma)$. So $\gamma\approx1$ ps$^{-1}$ acts like a coupling time of about 0.5 ps. The last section of the module says how to choose these times.

*Groups.* A global thermostat computes one $T_{inst}$ from a set of atoms. Programs let you define several sets, for example protein and solvent, each with its own thermostat. The limit on the size of a group comes from the formula $\sqrt{2/N_{df}}$. A ligand of 10 atoms has about 30 degrees of freedom, so its own temperature naturally fluctuates by $\sqrt{2/30} = 26$ %, which is 77 K at 300 K. A thermostat that works on so noisy a number acts strongly on very few atoms.

*Centre-of-mass motion.* The system as a whole should not travel through the box. Programs set the common velocity to zero at the start and remove any numerical drift of it (Module 2), so that kinetic energy cannot collect in the translation of the whole system.

The demo below runs a toy system of 24 independent oscillators at a target temperature of 1, in arbitrary units, so $N_{df} = 24$ and the correct relative fluctuation is $\sqrt{2/24} = 0.29$. The left plot shows $T_{inst}$ against time. The right plot shows the histogram of $T_{inst}$ and, drawn over it, the gamma distribution that a correct thermostat must reproduce. Choose a thermostat and a coupling time and compare the two curves. With no thermostat the histogram is whatever the starting velocities gave, because these oscillators cannot exchange energy with each other.

<div class="widget" data-widget="thermostats"></div>

## Pressure

Pressure is force per unit of area. Blow up a balloon: the gas molecules inside hit the skin from within and push it outwards, and the pressure is the push on each square centimetre. A simulation box with periodic boundaries has no walls to push on. Pressure is defined there with an imaginary surface drawn through the liquid: how hard does the material on one side push on the material on the other?

Two things carry that push. First, atoms fly across the surface and take their momentum with them. This part depends only on how fast the atoms move, so on the kinetic energy, and in an ideal gas it is all there is. Second, atoms on one side exert forces on atoms on the other side. Repulsion between them adds to the push and raises the pressure, and attraction pulls the two sides together and lowers it.

The formula of this section has one term for each. The unit used in MD is the bar, which is $10^5$ Pa and close to the pressure of the atmosphere. More in the [primer](physics.html#pressure).

The instantaneous pressure comes from the virial (Module 3):

$$
P_{inst} = \frac{2}{3V}\left(K - \Xi\right),\qquad \Xi = -\frac12\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}.
$$

<div class="legend" markdown="1">
- $P_{inst}$: the instantaneous pressure, computed from the positions, velocities and forces of one time step.
- $V$: the volume of the box, in nm$^3$.
- $K$: the total kinetic energy.
- $\Xi$ (capital Greek xi): the **virial**, a single number with the unit of energy that sums up the forces between the atoms.
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once.
- $\mathbf r_{ij}$: the vector from atom $j$ to atom $i$, $\mathbf r_i-\mathbf r_j$.
- $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$.
- $\mathbf r_{ij}\cdot\mathbf F_{ij}$: their dot product, which is the distance between the two atoms times the part of the force along the line that joins them. It is positive when the two atoms repel and negative when they attract.
- $2/(3V)$: the factor that turns an energy into a pressure. The 3 is the number of dimensions of space.
</div>

Read it like this. The term $2K/(3V)$ is the kinetic part. To check it, take an ideal gas: there are no forces, so $\Xi = 0$, and the kinetic energy is $\tfrac32Nk_BT$ for $N$ atoms, so $P = Nk_BT/V$, the ideal gas law.

The term $-2\Xi/(3V)$ is the part from the forces. A repelling pair has a positive $\mathbf r_{ij}\cdot\mathbf F_{ij}$, which makes $\Xi$ more negative, and because $\Xi$ enters with a minus sign the pressure goes up. An attracting pair lowers it.

The units: with $K$ and $\Xi$ in kJ/mol and $V$ in nm$^3$, the pressure comes out in kJ mol$^{-1}$ nm$^{-3}$, and 1 kJ mol$^{-1}$ nm$^{-3}$ is 16.6 bar ([units](physics.html#units)).

In a liquid the two parts almost cancel. Liquid water has 33.4 molecules per nm$^3$ (Module 1). An ideal gas of molecules at that density and 300 K would have a pressure of $33.4\times2.494 = 83.3$ kJ mol$^{-1}$ nm$^{-3}$, which is about 1,400 bar, while real water at that density is at 1 bar. The forces between the molecules therefore take away nearly all of the kinetic part, and the pressure you read is a small difference between two large numbers. This is the first reason why it is so noisy.

In an anisotropic system it is a tensor $\mathbf P = \frac{2}{V}(\mathbf K-\boldsymbol\Xi)$.

<div class="box maths" markdown="1">
**Maths you need here: the pressure as a table of nine numbers.** One number is enough for the pressure of a liquid at rest, because a liquid pushes equally in all directions. An **anisotropic** system is one whose directions are not equivalent. A membrane is the main example: the direction across the bilayer is different from the two directions within it. A crystal is another. The pressure of such a system needs a table with 3 rows and 3 columns, called a **tensor** and written in bold.

The entry $P_{ab}$, where $a$ and $b$ are each one of $x$, $y$, $z$, is the force along $a$ per unit area on a surface that faces the direction $b$. The three diagonal entries $P_{xx}$, $P_{yy}$ and $P_{zz}$ are the ordinary pressures on the faces of the box perpendicular to $x$, $y$ and $z$. The other entries are sideways (shear) stresses.

The formula is the one above with tables in the place of numbers: $K_{ab} = \tfrac12\sum_im_iv_{ia}v_{ib}$ and $\Xi_{ab} = -\tfrac12\sum_{i<j}r_{ij,a}F_{ij,b}$, where $v_{ia}$ is component $a$ of the velocity of atom $i$, and likewise for $r_{ij,a}$ and $F_{ij,b}$. The diagonal entries of $\mathbf K$ add up to the kinetic energy $K$ and those of $\boldsymbol\Xi$ to the virial $\Xi$. So the average of the three diagonal pressures, $(P_{xx}+P_{yy}+P_{zz})/3$, is the $P_{inst}$ of the formula above. This average over three directions is why the scalar formula has $2/(3V)$ where the tensor formula has $2/V$. More on tables of numbers in the [toolbox](maths.html#matrices).
</div>

<div class="box physics" markdown="1">
**Physics you need here: compressibility.** Squeeze a material and its volume gets smaller. The **isothermal compressibility** $\kappa_T$ (Greek kappa; "isothermal" means "at constant temperature") says by how much:

$$
\kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial P}\right)_T .
$$

Here $\partial V/\partial P$ is the change of volume per unit change of pressure, and the subscript $T$ says that the temperature is held fixed. Dividing by $V$ turns it into a relative change. The minus sign makes $\kappa_T$ positive, since the volume falls when the pressure rises. For small changes the definition reads $\Delta V/V = -\kappa_T\,\Delta P$. The unit of $\kappa_T$ is one over a pressure.

Water has $\kappa_T = 4.5\times10^{-5}$ bar$^{-1}$: it loses 0.0045 % of its volume for each additional bar. An ideal gas has $\kappa_T = 1/P$, which is 1 bar$^{-1}$ at 1 bar, about twenty thousand times more. Now turn the relation around: $\Delta P = -(\Delta V/V)/\kappa_T$. A material that is hard to compress answers a tiny change of volume with a large change of pressure. More in the [primer](physics.html#pressure).
</div>

**The pressure fluctuates enormously.** Water is nearly incompressible, $\kappa_T = 4.5\times10^{-5}$ bar$^{-1}$, so a relative volume fluctuation of only 0.1 % corresponds to a pressure change of about 20 bar. In a box of a few nanometres, instantaneous pressures swing by several hundred bar from step to step. This is physical. A pressure of "1.0 ± 250 bar" is normal: judge the average over a long window, and judge equilibration by the **density**, which converges much faster.

The arithmetic of the first sentence, with the relation in the box: a relative volume change of 0.1 % is 0.001, and $0.001/(4.5\times10^{-5}\ \text{bar}^{-1}) = 22$ bar. Three things together make the instantaneous pressure so restless:

- the liquid is stiff, so the small changes of the distances between neighbouring molecules that happen at every step change the forces a great deal;
- the pressure is a small difference between two large numbers, as shown above;
- a simulation box holds few molecules, and relative fluctuations grow as the number of molecules falls (Module 3).

In "1.0 ± 250 bar" the number after the ± sign is the standard deviation of the instantaneous values. It does not say that the average is uncertain by 250 bar: the uncertainty of an average shrinks as you average over a longer time (Module 11). The **density** is the mass in the box divided by its volume, and since the mass is fixed it follows the volume. The volume is a property of the whole box that changes slowly and smoothly. Its plot settles to a plateau that you can recognise by eye, which is what "converges" means here.

In the NPT ensemble the volume fluctuates as

$$
\langle\delta V^2\rangle = k_BT\,\langle V\rangle\,\kappa_T ,
$$

and a correct barostat must reproduce this.

<div class="legend" markdown="1">
- $\delta V$: the deviation of the volume from its average at one instant, $V-\langle V\rangle$.
- $\langle\delta V^2\rangle$: the average of the squared deviation, which is the variance of the volume, in nm$^6$.
- $\langle V\rangle$: the average volume of the box.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
- $\kappa_T$: the isothermal compressibility of the material in the box.
</div>

Read it like this. The volume of the box in an NPT simulation is not a fixed number. It breathes, and the formula says by how much. A more compressible material breathes more, and so does a hotter one. The variance grows in proportion to the volume, so the standard deviation grows as $\sqrt{\langle V\rangle}$ and the relative fluctuation falls as $1/\sqrt{\langle V\rangle}$: large boxes are steadier.

A number, for a cubic box of water with an edge of 4 nm, so $\langle V\rangle = 64$ nm$^3$. First convert the compressibility to MD units: 1 bar is 0.0602 kJ mol$^{-1}$ nm$^{-3}$, so $\kappa_T = 4.5\times10^{-5}/0.0602 = 7.47\times10^{-4}$ nm$^3$ mol kJ$^{-1}$. Then $\langle\delta V^2\rangle = 2.494\times64\times7.47\times10^{-4} = 0.119$ nm$^6$, and the standard deviation is 0.35 nm$^3$, about 0.5 % of the volume.

The formula is one more case of the rule of Module 3 that response functions are fluctuations. Turned around, $\kappa_T = \langle\delta V^2\rangle/(k_BT\langle V\rangle)$, it lets you measure the compressibility of your model from the volume record of an NPT run. This only works if the barostat produces the right fluctuations, which is the question to ask of every barostat below.

## Barostats

<div data-videos="rGOyUWV0fX0"></div>

All barostats change the volume by scaling the box and the particle coordinates. They differ in how the scaling factor is determined.

Scaling works like enlarging a photograph. Every edge of the box and every coordinate is multiplied by the same factor, a number very close to 1. All distances between molecules change by that factor, and the volume changes by its cube. A slightly larger box means molecules slightly further apart, weaker repulsion and a lower pressure.

A useful picture for the whole section is a cylinder closed by a piston. The pressure of the system pushes the piston out, and the outside pressure $P_0$ pushes it in. A barostat is a rule for moving the piston. The rules repeat the ideas of the thermostats, with the volume in the place of the kinetic energy and the pressure in the place of the temperature:

| Idea | Thermostat | Barostat |
|---|---|---|
| First-order relaxation towards the target | Berendsen | Berendsen |
| The same, with noise of the right size added | Stochastic velocity rescaling | Stochastic cell rescaling |
| An extra variable with a "mass" | Nosé-Hoover | Andersen, Parrinello-Rahman, MTTK |
| Random trial changes that are accepted or rejected | none in this module | Monte Carlo barostat |

### Berendsen

First-order relaxation of the pressure, the analogue of the Berendsen thermostat:

$$
\frac{dP}{dt}=\frac{P_0-P}{\tau_P}\qquad\Longrightarrow\qquad
\mu = \left[1-\frac{\kappa_T\,\Delta t}{\tau_P}\,(P_0-P_{inst})\right]^{1/3},
$$

with coordinates and box edges scaled by $\mu$ each step.

<div class="legend" markdown="1">
- $P$: the pressure of the system at this moment, the quantity written $P_{inst}$ on the right.
- $P_0$: the target pressure, for example 1 bar.
- $dP/dt$: the rate at which the pressure changes.
- $\tau_P$: the coupling time of the barostat, in picoseconds.
- $\mu$ (Greek mu): the factor by which every box edge and every coordinate is multiplied at this step.
- $\kappa_T$: the isothermal compressibility. You give the program a value, usually that of water.
- $\Delta t$: the time step.
- The exponent $1/3$: a cube root. The square bracket is the factor for the volume, and the volume is the cube of a length.
</div>

**From the left formula to the right one.** The steps are the same as for the thermostat, with one more link in the chain.

*Step 1.* The left formula says how much the pressure should change in one time step: $\Delta P = (\Delta t/\tau_P)(P_0-P_{inst})$.

*Step 2.* A barostat can change the pressure only by changing the volume. The compressibility says which change of volume gives the wanted change of pressure: $\Delta V/V = -\kappa_T\,\Delta P$.

*Step 3.* Put step 1 into step 2:

$$
\frac{\Delta V}{V} = -\frac{\kappa_T\,\Delta t}{\tau_P}\,(P_0-P_{inst}) .
$$

<div class="legend" markdown="1">
- $\Delta V/V$: the relative change of the volume in one step.
- Other symbols: as in the list above.
</div>

*Step 4.* Scaling all lengths by $\mu$ turns the volume $V$ into $\mu^3V$. The new volume must be $V+\Delta V$, so $\mu^3 = 1+\Delta V/V$. Taking the cube root gives the formula for $\mu$.

Read it like this. If the pressure is too high, $P_0-P_{inst}$ is negative, the bracket is larger than 1, and the box grows, which lowers the pressure.

A number: take $\kappa_T = 4.5\times10^{-5}$ bar$^{-1}$, $\Delta t = 0.002$ ps, $\tau_P = 1$ ps and a pressure of 201 bar with a target of 1 bar. The bracket is $1+4.5\times10^{-5}\times0.002\times200 = 1.000018$ and $\mu = 1.000006$. Each edge of the box grows by six millionths in this step. That looks like nothing, but there are 500 steps in a picosecond.

Only the ratio $\kappa_T/\tau_P$ appears in the formula. If the compressibility you typed is twice the true one, the box relaxes twice as fast as $\tau_P$ says, and nothing else changes. In particular the pressure at which the box settles does not depend on it.

Robust and non-oscillating, but it gives the wrong volume fluctuations, so it does not sample NPT. Equilibration only.

The reason is the same as for the thermostat. The formula contains only the pull towards the target and no noise term of the right size, so the variance of the volume is not the $k_BT\langle V\rangle\kappa_T$ that the NPT ensemble requires. In the tests of the stochastic cell rescaling paper (two sections below) it came out too small.

### Extended-system barostats: Andersen, Parrinello-Rahman, MTTK

Give the piston of the picture above a mass. A piston with mass does not jump to the position where the pressures balance. It is accelerated by the difference between the two pressures, gathers speed, passes the balance point and swings back, like a weight on a spring.

An "extended system" is the original system plus one or more extra variables of this kind that have their own equations of motion. The Nosé-Hoover thermostat was one example, with the variable $\xi$ and the mass $Q$. Here the extra variable is the volume.

[Andersen (1980)](cite:andersen1980) made the volume a dynamical variable with a fictitious mass $W$ and a "kinetic energy", driven by the imbalance between internal and external pressure:

$$
W\,\ddot V = P_{inst}-P_0 .
$$

<div class="legend" markdown="1">
- $V$: the volume of the box, now a variable that the program moves in time like a coordinate.
- $\ddot V$: the second time derivative of the volume, its "acceleration".
- $W$: the "mass" of the piston. It is not a real mass: its unit is a pressure times a time squared divided by a volume. You choose it, directly or through a coupling time $\tau_P$.
- $P_{inst}$: the instantaneous pressure of the system, the internal pressure.
- $P_0$: the target pressure, the external pressure.
</div>

Read it like Newton's law, mass times acceleration equals force. If the pressure inside is higher than outside, the volume is accelerated outwards. When the two pressures are equal the acceleration is zero, but the volume is still moving, so it overshoots. A small $W$ gives a light piston and fast oscillations of the box, a large $W$ a heavy piston and slow ones.

The "kinetic energy" of the piston is $\tfrac12W\dot V^2$, by analogy with $\tfrac12mv^2$. "Fictitious" says that this mass and this energy belong to the method and not to the molecules.

On its own this piston samples the constant-enthalpy ensemble $(N,P,H)$; Andersen obtained NPT by adding the stochastic collisions of his thermostat.

The **enthalpy** is the energy of the system plus the pressure times its volume ([primer](physics.html#thermodynamics)). In the label $(N,P,H)$ the letter $H$ stands for it.

Here is why it is the conserved quantity. Atoms plus piston are an isolated system: nothing in the equation supplies or removes heat. When the box grows by a small volume, the atoms push the piston out against the outside pressure and lose the energy $P_0$ times that volume. So the energy of the atoms alone is not constant, but the energy plus $P_0V$ is, apart from the small kinetic energy of the piston. To hold the temperature fixed as well, a thermostat has to be added, and the two together give NPT.

[Parrinello and Rahman (1981)](cite:parrinello1981), building on their 1980 letter, generalised the piston to the full box matrix $\mathbf h$, so that the box can change shape as well as size. They needed this for structural transitions in crystals, and it is also what anisotropic systems such as membranes require. Their equations too must be combined with a thermostat to give NPT.

A simulation box is defined by three edge vectors. Write them as the columns of a table with 3 rows and 3 columns and you have the **box matrix** $\mathbf h$. It holds the lengths of the three edges and the angles between them, and the volume of the box is its determinant ([toolbox](maths.html#matrices)).

Andersen's piston moves one number, the volume, so the box keeps its shape. In the Parrinello-Rahman method every entry of $\mathbf h$ has an equation of motion of the piston type, driven by the difference between the pressure tensor and the target pressure. The box can then become longer in one direction and shorter in another, or tilt. A structural transition in a crystal is a change from one crystal structure to another, which changes the shape of the repeating cell, and a box of fixed shape would not allow it.

[Martyna, Tobias and Klein (1994)](cite:martyna1994), and later the same authors with Tuckerman (MTTK), derived extended-system equations that generate the exact NPT ensemble, provided the dynamics is ergodic (Hoover's earlier constant-pressure equations did not give exactly that ensemble). Parrinello-Rahman, the form most used in GROMACS, gives correct averages for a well-equilibrated system, but its volume fluctuations are not guaranteed to be exactly those of NPT: use MTTK, stochastic cell rescaling or a Monte Carlo barostat when the fluctuations themselves matter.

"Ergodic" has the meaning it had for Nosé-Hoover: one long trajectory must visit all states with the right frequencies. "When the fluctuations themselves matter" covers every result that is computed from the size of the volume fluctuations and not from an average. The compressibility obtained from $\langle\delta V^2\rangle$ is the example of the previous section.

Like Nosé-Hoover, all these methods are second-order: far from equilibrium the box oscillates and can become unstable. Do not start an NPT run with Parrinello-Rahman from an unequilibrated density.

"Second-order" means that the equation contains a second time derivative, here $\ddot V$. Such an equation has inertia and can overshoot, while a first-order one (Berendsen) cannot. If the density at the start is far from its final value, the pressure difference is huge, the piston is accelerated hard, and the box swings with a large amplitude. In a bad case the swing grows until the simulation crashes.

### Stochastic cell rescaling

[Bernetti and Bussi (2020)](cite:bernetti2020) did for pressure what velocity rescaling did for temperature: Berendsen's first-order relaxation plus a noise term of exactly the right size,

$$
d\varepsilon = -\frac{\kappa_T}{\tau_P}\left(P_0-P_{inst}\right)dt + \sqrt{\frac{2k_BT\,\kappa_T}{V\,\tau_P}}\;dW,\qquad \varepsilon = \ln\frac{V}{V_0}.
$$

<div class="legend" markdown="1">
- $\varepsilon$ (Greek epsilon): the natural logarithm of the volume divided by a fixed reference volume $V_0$. It is a pure number. It is not the Lennard-Jones $\varepsilon$ of Module 5.
- $d\varepsilon$: the change of $\varepsilon$ in the short time $dt$. Because the derivative of $\ln V$ is $1/V$, it is to first order $dV/V$, the relative change of the volume. With noise the two differ by a small term of order $dt$ (from the square of $dW$), and the equation is exact as written, for $\varepsilon$.
- $\kappa_T$, $\tau_P$: the compressibility and the coupling time of the barostat.
- $P_0$, $P_{inst}$: the target pressure and the instantaneous pressure.
- $k_BT$: the thermal energy at the temperature of the thermostat.
- $V$: the present volume of the box.
- $dW$: Wiener noise, a random number with mean zero and variance $dt$.
- $\sqrt{2k_BT\kappa_T/(V\tau_P)}$: the amplitude of the noise.
</div>

Read it like this. The first term is the Berendsen barostat: step 3 of its derivation was $\Delta V/V = -(\kappa_T\Delta t/\tau_P)(P_0-P_{inst})$, and $\Delta V/V$ is the change of $\varepsilon$. The second term is a random relative change of the volume. Its amplitude is larger for a more compressible and for a hotter system, and smaller for a larger box, in the same way as the fluctuation formula $\langle\delta V^2\rangle = k_BT\langle V\rangle\kappa_T$.

<details markdown="1"><summary>Optional: check that the noise has the right size</summary>
Suppose the pressure answers a change of volume through the compressibility alone. When $\varepsilon$ is above its average by $\delta\varepsilon$ (the box is too large by that fraction), the pressure is below the target: $P_{inst}-P_0 = -\delta\varepsilon/\kappa_T$. Put this into the first term. The compressibility cancels and the term becomes $-(\delta\varepsilon/\tau_P)\,dt$, so

$$
d(\delta\varepsilon) = -\frac{\delta\varepsilon}{\tau_P}\,dt + \sqrt{\frac{2k_BT\,\kappa_T}{V\,\tau_P}}\;dW .
$$

This is the Ornstein-Uhlenbeck process of the box "Why that amplitude", with $1/\tau_P$ in the place of $\gamma$ and the square root in the place of $\sigma$. Its variance is $\sigma^2/2\gamma$, which here is $k_BT\kappa_T/V$. For small changes $\delta V = V\,\delta\varepsilon$, so the variance of the volume is $V^2$ times that, $k_BTV\kappa_T$: the NPT formula. The coupling time has cancelled. It decides how fast the volume fluctuates, not by how much.
</details>

It samples the correct NPT ensemble, does not oscillate, and can be used from the start of equilibration through production, provided the coupling time $\tau_P$ is not too short and the pressure coupling is applied often enough (the original paper found errors with very small $\tau_P$ and with coupling only every ten steps or more). In GROMACS it is `pcoupl = C-rescale`.

It does not oscillate because the equation is first-order, like Berendsen's. "Applied often enough" refers to a way of saving time: a program may compute the pressure and rescale the box only every so many steps and not at each one.

### Monte Carlo barostat

The barostats so far compute the pressure and let it move the box. The Monte Carlo barostat never computes a pressure. It works by trial and error: change the volume by a small random amount, look at what that did to the energy, and then decide whether to keep the change.

<div class="box maths" markdown="1">
**Maths you need here: a Monte Carlo move.** Monte Carlo is the name for methods that use random numbers to sample a probability distribution. One move has three parts:

1. *Propose* a random change of the state.
2. *Compute* the ratio of the probability of the new state to that of the old one.
3. *Accept* the change with a probability equal to that ratio, or with certainty if the ratio is larger than 1. If the change is not accepted, put the old state back.

This rule is the Metropolis criterion, which returns in Module 14. Changes towards more probable states are always taken and changes towards less probable states only sometimes. Over many moves each state is then visited in proportion to its probability, provided a change and its reverse are proposed equally often, as they are here. On a computer, "accept with probability 0.37" means: draw a random number spread evenly between 0 and 1, and accept if it is smaller than 0.37.
</div>

Every few steps, propose a random volume change $V\to V'$, scale the coordinates of molecular centres, and accept with probability

$$
P_{acc} = \min\left\{1,\ \exp\left[-\beta\left(\Delta U + P_0\,\Delta V\right) + N_{mol}\ln\frac{V'}{V}\right]\right\},
$$

where $N_{mol}$ is the number of independently scaled centres (molecules, when each molecule is moved as a rigid body) and the trial volume is drawn uniformly in $V$.

<div class="legend" markdown="1">
- $P_{acc}$: the acceptance probability, a number between 0 and 1. Here $P$ is not a pressure.
- $\min\{1,\ x\}$: the smaller of 1 and $x$. It keeps the probability from exceeding 1.
- $\exp[\dots]$: the exponential function, $e$ to the power of the bracket.
- $V$, $V'$: the volume before the trial change and after it.
- $\Delta V$: the change of volume, $V'-V$.
- $\Delta U$: the change of the potential energy caused by the scaling, new minus old.
- $P_0$: the target pressure.
- $\beta$: $1/(k_BT)$.
- $N_{mol}$: the number of centres that were scaled, normally the number of molecules.
- $\ln(V'/V)$: the natural logarithm of the ratio of the two volumes, positive for an expansion.
</div>

Where the three terms come from. Describe a state by the volume $V$ and by the positions of the centres measured as fractions of the box edges, which the scaling leaves unchanged. In the NPT ensemble such a state has a probability proportional to $V^{N_{mol}}e^{-\beta(U+P_0V)}$. The exponential is the Boltzmann factor of the NPT ensemble from the first section, with the potential energy $U$ in the place of $H$ because the velocities are not touched by the move. The factor $V^{N_{mol}}$ counts places: each of the $N_{mol}$ centres can be anywhere in the box, so a larger box offers more arrangements.

The ratio of new to old probability is $(V'/V)^{N_{mol}}e^{-\beta(\Delta U+P_0\Delta V)}$. Writing the first factor as $\exp[N_{mol}\ln(V'/V)]$ puts everything into one exponent ([toolbox](maths.html#exp-log)), and the Metropolis rule gives the formula.

Read it like this, term by term:

- $\Delta U$: if the scaling pushes molecules into each other, the energy rises and the move is less likely to be accepted.
- $P_0\,\Delta V$: an expansion costs work against the outside pressure. The unit conversion is 1 bar $\times$ 1 nm$^3$ = 0.0602 kJ/mol.
- $N_{mol}\ln(V'/V)$: an expansion gives every molecule more room, which favours it.

A check with an ideal gas, where $\Delta U = 0$. For a small change, $\ln(V'/V)\approx\Delta V/V$, so the exponent is $\Delta V\,(N_{mol}/V-\beta P_0)$. It vanishes when $P_0 = N_{mol}k_BT/V$, the ideal gas law. If the box is smaller than that, expansions are favoured, and if it is larger, contractions are. The volume settles where the pressure of the gas equals $P_0$, although no pressure was ever computed.

Some phrases of the text. "Scale the coordinates of molecular centres" means that each molecule is moved as a whole: its centre is scaled, and its bond lengths and angles stay as they are. That is why $N_{mol}$ counts molecules and not atoms. "Drawn uniformly in $V$" means that the trial volume is the old volume plus a random number spread evenly between a negative and a positive limit. The limit is chosen so that neither nearly all nor nearly none of the trials are accepted.

It needs no virial, which is convenient for GPU codes and unusual potentials, and it samples NPT exactly. This is OpenMM's `MonteCarloBarostat` and an option in AMBER. The barostat does not use the instantaneous pressure, though OpenMM can compute it on request (`computeCurrentPressure`).

"Needs no virial" refers to the sum $\Xi$ of the pressure formula, which requires the forces pair by pair. The Monte Carlo move needs two numbers only, the potential energy before the scaling and after it.

### Coupling types

A barostat can treat the three directions of the box alike or separately. The choice depends on the system.

- **Isotropic**: one scale factor. Proteins in water.
- **Semi-isotropic**: $x$ and $y$ coupled together, $z$ separately. Membranes, where area and thickness must adjust independently.
- **Anisotropic**: full tensor. Crystals. In a liquid it lets the box deform without limit, so avoid it.

*Isotropic* means "the same in all directions". The box keeps its shape and changes only its size, and the barostat uses the single number $P_{inst}$.

*Semi-isotropic* coupling is for a membrane lying in the $xy$ plane. One scale factor acts on $x$ and $y$ together and is driven by the average of $P_{xx}$ and $P_{yy}$. A second one acts on $z$ and is driven by $P_{zz}$. The area of the box is set by how the lipids pack side by side, and its height by the thickness of the bilayer and of the water layer. With a single factor for all three directions the area could change only together with the height, and the bilayer could not find its own area per lipid.

*Anisotropic* coupling lets every entry of the box matrix respond to the pressure tensor, so the shape of the box is free. A crystal resists a change of shape, which holds the box in place. A liquid does not resist a slow change of shape at all. Nothing brings the box back, the random changes add up, and the box can become very long and thin.

## A defensible protocol

"Defensible" means that a referee who knows the subject would accept your choices. A simulation is run in stages, and the stages ask different things of the thermostat and the barostat. Early on, the system is far from where it should be and the only requirement is to get there without a crash. Later the data are kept, and the ensemble must be right.

| Stage | Thermostat | Barostat |
|---|---|---|
| Heating and first equilibration (NVT), 100 ps | Velocity rescaling or Langevin, $\tau_T$ = 0.1 ps | none |
| Density equilibration (NPT), 100 ps to 1 ns | same | Stochastic cell rescaling (or Berendsen), $\tau_P$ = 1 to 2 ps |
| Production (NPT) | Velocity rescaling, Langevin or Nosé-Hoover chains | Stochastic cell rescaling, Parrinello-Rahman ($\tau_P$ = 2 to 5 ps) or Monte Carlo |

State the thermostat, barostat and coupling constants in your methods section. They are part of the model.

### Why the stages come in this order

A freshly built system is artificial. The water was placed by a program, the density is only roughly right, and the velocities were drawn at random. Because the pressure is so sensitive to small changes of distance, the pressure of such a system can be wrong by a very large amount.

- **Stage 1, constant volume.** The box is held fixed and only the thermostat acts. The atoms find sensible local arrangements and the temperature reaches its target. A barostat switched on at this point would react to pressures that mean nothing yet.
- **Stage 2, the barostat is switched on.** The box size adjusts until the density stops drifting. The start may still be far from the target, so a first-order barostat is used, one that cannot oscillate. Judge this stage by the density plot.
- **Stage 3, production.** Temperature and density have settled. Every thermostat in this row samples the canonical ensemble, and with it the barostats of this row give NPT, with the caveat about the fluctuations of Parrinello-Rahman.

### How to choose the coupling times

1. **Many time steps.** A coupling time must be much longer than the time step, so that the thermostat or barostat acts a little at each step. With $\Delta t = 2$ fs, $\tau_T = 0.1$ ps is 50 steps.
2. **Temperature.** Stay within the range given above, 0.1 to 1 ps. A shorter time intervenes more strongly in the motion of the atoms. A much longer one reacts too slowly to the heat that has to be removed.
3. **Pressure.** In the table the coupling time for the pressure is ten or more times longer than that for the temperature. The instantaneous pressure is far noisier than the instantaneous temperature, and a barostat with a short $\tau_P$ would move the box in answer to noise of hundreds of bar. With a long $\tau_P$ it answers the average over many steps. A short $\tau_P$ also means a light piston and fast swings of the box in the second-order barostats, and the stochastic cell rescaling paper found errors with very small values.
4. **Run for many coupling times.** In a first-order relaxation the gap to the target is down to 5 % of its starting size after three coupling times. With $\tau_P = 2$ ps, a stage of 100 ps is 50 coupling times.
5. **The compressibility.** The first-order barostats need a value of $\kappa_T$. Only the ratio $\kappa_T/\tau_P$ enters, so an inexact value changes the speed of the relaxation and nothing else.

### Which combinations are safe

The rules below repeat what the sections above established.

- During equilibration the data are discarded, so the requirement is stability. First-order methods approach the target without oscillating: Berendsen, stochastic velocity rescaling and Langevin for the temperature, Berendsen and stochastic cell rescaling for the pressure.
- Second-order methods (Nosé-Hoover, Parrinello-Rahman, MTTK) oscillate when started far from the target. Switch to them only when temperature and density have settled.
- Production needs a thermostat that samples the canonical ensemble together with a barostat that gives NPT. Both Berendsen methods fail this test.
- An extended-system barostat always needs a thermostat beside it. Alone it conserves the enthalpy and does not hold the temperature.
- If you want dynamical properties, avoid Andersen, and with Langevin keep $\gamma$ small.

| Pair | Equilibration from a rough start | Production |
|---|---|---|
| Berendsen thermostat with Berendsen barostat | Stable and smooth, but the best-practice guides prefer a thermostat that samples the correct ensemble even here | No: the fluctuations of kinetic energy and volume are wrong |
| Stochastic velocity rescaling with stochastic cell rescaling | Yes, under the conditions given in the section on stochastic cell rescaling | Yes, under the same conditions |
| Langevin with a Monte Carlo barostat | Langevin is very robust. The protocol above uses the Monte Carlo barostat in production only | Yes. The friction slows the dynamics |
| Nosé-Hoover chains with Parrinello-Rahman or MTTK | No: both oscillate far from the target | Yes, for a well-equilibrated system. With Parrinello-Rahman the volume fluctuations are not guaranteed to be exactly those of NPT |

## Check yourself

<details markdown="1"><summary>1. Your temperature plot is a perfectly flat line at 300.00 K. Is that good?</summary>
No. The instantaneous temperature must fluctuate with standard deviation $T\sqrt{2/N_{df}}$. (Here $T$ is the target temperature and $N_{df}$ the number of degrees of freedom of the system.) A flat line means the kinetic energy is being pinned (isokinetic scaling or an extremely short Berendsen time constant), which is not the canonical ensemble.
</details>

<details markdown="1"><summary>2. Why is the Berendsen thermostat acceptable for equilibration but not for production?</summary>
During equilibration the goal is to reach the target state quickly and stably, and the ensemble is irrelevant because the data are discarded. In production the distribution of kinetic energy is too narrow, so fluctuation-based properties are wrong, and energy is redistributed unphysically between degrees of freedom over long times.
</details>

<details markdown="1"><summary>3. In an implicit-solvent Langevin simulation you lower γ from 50 ps⁻¹ to 1 ps⁻¹ and conformational transitions become ten times faster. Did the free-energy landscape change?</summary>
No. The stationary distribution of Langevin dynamics is $e^{-\beta H}$ for every $\gamma>0$ (exactly for the continuous equations; an integrator with a finite time step samples a slightly different distribution, with an error that depends on $\Delta t$ and hardly on $\gamma$). (Here $\gamma$ is the friction coefficient, $H$ the total energy, $\beta = 1/(k_BT)$ and $\Delta t$ the time step. The free-energy landscape is the set of populations of the different shapes of the molecule, expressed as free energies, as in Module 12.) Only the kinetics changed. Populations are comparable between the two runs; rates and times are not.
</details>

<details markdown="1"><summary>4. The average pressure over 100 ps is −14 bar with a target of 1 bar. Is the barostat broken?</summary>
Not necessarily. With fluctuations of a few hundred bar and a correlation time of the order of a picosecond, the standard error of a 100 ps average is tens of bar. (The correlation time is the time after which two readings of the pressure are independent of each other, and the standard error is the uncertainty of an average, as in Module 11. In 100 ps there are of the order of 100 independent readings, and the standard deviation divided by $\sqrt{100}$ is a tenth of a few hundred bar.) Check the density instead and average the pressure over nanoseconds.
</details>

<details markdown="1"><summary>5. A system has 30,000 degrees of freedom and a target of 300 K. What standard deviation of the temperature do you expect? And for the 10 atoms of a ligand taken alone?</summary>
For the system, $300\times\sqrt{2/30{,}000} = 2.4$ K. The ligand has about 30 degrees of freedom, so the temperature computed from its atoms alone fluctuates by $300\times\sqrt{2/30} = 77$ K. Both numbers are correct behaviour. The second shows why a very small group should not have its own thermostat.
</details>

<details markdown="1"><summary>6. Why can a thermostat not consist of friction alone, and what does the noise in Langevin dynamics add?</summary>
Friction alone removes kinetic energy at every step: each velocity decays as $e^{-\gamma t}$, with $\gamma$ the friction coefficient, and the system cools towards absolute zero. The noise feeds energy in at a rate that does not depend on the speed. The two balance at one value of the kinetic energy, and with the amplitude $\sqrt{2\gamma mk_BT}$ (the fluctuation-dissipation theorem) that value corresponds to the temperature $T$.
</details>

<details markdown="1"><summary>7. A Berendsen barostat sees an instantaneous pressure of 301 bar with a target of 1 bar. Does the box grow or shrink, and by how much in one step, for a compressibility of 4.5 × 10⁻⁵ bar⁻¹, a time step of 2 fs and a coupling time of 1 ps?</summary>
It grows, because the pressure inside is too high. The bracket of the formula is $1-4.5\times10^{-5}\times0.002\times(1-301) = 1.000027$, which is the factor for the volume. The cube root is $\mu = 1.000009$: every edge of the box becomes longer by nine millionths.
</details>

## Exercises

1. Add a Langevin thermostat (BAOAB) to the Python code of Module 1. Verify that the average temperature matches the target and that the kinetic energy histogram matches the gamma distribution (up to an error of order $\Delta t^2$, which shrinks as you reduce the time step).
2. Simulate a single harmonic oscillator with a Nosé-Hoover thermostat and plot the $(x,p)$ points visited. Compare with the Gaussian you expect. Then add a second thermostat in a chain and repeat.
3. Add a Berendsen thermostat to the same code and compare the variance of the kinetic energy with the canonical value $\tfrac12N_{df}(k_BT)^2$ for several values of $\tau_T$.
4. From an NPT simulation of water, compute the isothermal compressibility from the volume fluctuations, once with a Berendsen barostat and once with stochastic cell rescaling. Compare with the experimental $4.5\times10^{-5}$ bar$^{-1}$ and with the value of your water model itself (TIP3P gives about $6\times10^{-5}$ bar$^{-1}$).

Notes on the notation of the exercises:

- Exercise 1. BAOAB is the order of the pieces of one time step, with B, A and O as explained under the O step above (Module 4). "An error of order $\Delta t^2$" is an error that falls by a factor of four when the time step $\Delta t$ is halved.
- Exercise 2. $(x,p)$ are the position and the momentum of the oscillator.
- Exercise 3. $N_{df}$ is the number of degrees of freedom, $k_BT$ the thermal energy and $\tau_T$ the coupling time.
- Exercise 4. Use $\kappa_T = \langle\delta V^2\rangle/(k_BT\langle V\rangle)$ from the section on pressure. TIP3P is a water model (Module 6).

## Read

{{READ}}

## Key papers

{{PAPERS}}
