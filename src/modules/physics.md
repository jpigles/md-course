---
title: Physics primer
short: Physics primer
summary: The physics that the lessons build on, explained from zero in sixteen short sections that you can read in order or open one at a time from a link in a lesson.
---

This page explains the physics that the eighteen lessons build on. It starts from zero. You need no physics beyond what you remember from school. The mathematics is on a separate page, the [maths toolbox](maths.html#notation), and this page links to it wherever a tool is needed.

There are two ways to use the page. You can read it once from top to bottom before Module 1, because the sections build on each other. Or you can arrive from a link in a lesson, read the one section you need, and go back with the back button of your browser.

Every section has the same five parts in the same order: the idea in plain words, the notation (with a list under every formula that says what each symbol means), one or two worked examples with numbers that you can check by hand, the lessons that use the idea, and a common mistake.

All numbers are in the units of the course: nanometres, picoseconds, atomic mass units and kJ/mol. The first section explains them.

<div class="box warn" markdown="1">
**Letters that mean two things on this page.** Physics has more quantities than letters. The lists under the formulas say which meaning is used each time. The collisions to watch for:

- $T$ is the temperature. $T_{period}$ is the time of one oscillation.
- $k$ is a spring constant in the first half of the page and the wave number $2\pi/\lambda$ in the last section. $k_B$ is Boltzmann's constant. Capital $K$ is the kinetic energy, and in one section an equilibrium constant. An upright K after a number is the unit kelvin.
- $E$ is an energy. Bold $\mathbf E$ is the electric field.
- $P$ is the pressure. $P_A$ with a label is a probability. Small bold $\mathbf p$ and capital bold $\mathbf P$ are momenta.
- $\mu$ is the reduced mass of two atoms. Bold $\boldsymbol\mu$ is a dipole moment.
- $\varepsilon$ alone is the depth of a Lennard-Jones well. $\varepsilon_0$ and $\varepsilon_r$ belong to electrostatics.
- $H$ is the enthalpy here. In Module 2 it is the Hamiltonian.
- $Q$ is heat here. In Module 3 it is the partition function.
- $\nu$ (Greek nu) is a frequency. $v$ (Latin) is a velocity. They look alike in print.
- $\lambda$ is a wavelength. $\lambda_D$ is the Debye length. Capital $\Lambda$ is the thermal wavelength of a particle.
- $\rho$ is the number of molecules per volume in the section on pressure and the charge per volume in Poisson's equation.
- $A$ is the Helmholtz free energy. In the section on pressure it is an area, and as a subscript it is the name of a state.
- $e$ is the elementary charge when it stands in a unit or in a charge. In a power such as $e^{-x}$ it is the number 2.718.
- $R$ is the gas constant in $RT$ and the radius of a sphere in the section on diffusion. Bold $\mathbf R$ is the centre of mass.
</div>

**The sections**

1. [Units used in MD](#units)
2. [Motion, velocity, acceleration, force](#newton)
3. [Work, kinetic and potential energy](#energy)
4. [Momentum and angular momentum](#momentum)
5. [The harmonic oscillator](#oscillator)
6. [Temperature and thermal energy](#temperature)
7. [Pressure and volume](#pressure)
8. [Heat, entropy and free energy](#thermodynamics)
9. [Equilibrium constants and free energy](#equilibrium)
10. [Charge and Coulomb's law](#electrostatics)
11. [Dipoles and polarisation](#dipoles)
12. [Why atoms can be treated as classical balls](#quantum)
13. [Forces between molecules](#intermolecular)
14. [Diffusion, friction and viscosity](#diffusion)
15. [Time and length scales of molecules](#time-scales)
16. [Waves and frequencies](#waves)

## Units used in MD {#units}

A protein is a few nanometres across, one of its carbon atoms weighs $2\times10^{-26}$ kg, and its bonds vibrate once every $10^{-14}$ s. In metres, kilograms, seconds and joules, every number in a simulation would carry a large power of ten. MD programs therefore use units of the size of atoms and molecules. This course uses the following set throughout.

| Quantity | Unit | In SI units | A scale to remember |
|---|---|---|---|
| Length | nanometre, nm | $10^{-9}$ m | A bond is 0.1 to 0.15 nm long. 1 nm = 10 Å (ångström). |
| Time | picosecond, ps | $10^{-12}$ s | 1 ps = 1,000 fs (femtoseconds). A time step is 1 to 4 fs. |
| Mass | atomic mass unit, u | $1.66054\times10^{-27}$ kg | Hydrogen is about 1 u, carbon 12 u, oxygen 16 u. |
| Energy | kJ/mol | $1.66054\times10^{-21}$ J for one molecule | The thermal energy at 300 K is 2.494 kJ/mol. |
| Charge | elementary charge, $e$ | $1.602177\times10^{-19}$ C | A proton has $+1\,e$, an electron $-1\,e$. |
| Temperature | kelvin, K | K | 0 °C is 273.15 K. Body temperature is 310 K. |
| Pressure | bar | $10^5$ Pa | The atmosphere at sea level is 1.013 bar. |

The mass in u of a molecule is the same number as its molar mass in g/mol: water is 18 u and 18 g/mol. Biochemists call the same unit the dalton (Da), so a protein of 20 kDa has a mass of 20,000 u. Many papers and some programs use ångström for length and kcal/mol for energy. The conversion table below covers both.

**Energies are "per mole".** Chemists measure energies for a mole of molecules, because a mole is an amount that you can weigh. A mole is $N_A = 6.02214\times10^{23}$ molecules (Avogadro's number). An energy of 1 kJ/mol means: if every molecule in a mole did this, the total would be 1 kJ. For one molecule it is

$$
1\ \text{kJ/mol} = \frac{1000\ \text{J}}{N_A} = 1.66054\times10^{-21}\ \text{J for one molecule}.
$$

<div class="legend" markdown="1">
- kJ/mol: kilojoule per mole, the energy unit of this course.
- J: joule, the SI unit of energy. 1 kJ is 1,000 J.
- $N_A$: Avogadro's number, $6.02214\times10^{23}$ per mole, the number of molecules in one mole.
</div>

So "kJ/mol" in MD is a unit for the energy of one molecule or one interaction, scaled to a convenient size. It does not mean that the simulation contains a mole of anything. When a program prints a total potential energy of $-300{,}000$ kJ/mol for a box of water, it means $-300{,}000\times1.66054\times10^{-21}$ J for that one box.

**Why these units fit together.** Kinetic energy is one half of mass times velocity squared (see [Work, kinetic and potential energy](#energy)). In MD units a mass times a velocity squared is in u nm$^2$ ps$^{-2}$. Convert each factor to SI units:

$$
1\ \text{u}\,\text{nm}^2\,\text{ps}^{-2} = 1.66054\times10^{-27}\ \text{kg}\times\frac{(10^{-9}\ \text{m})^2}{(10^{-12}\ \text{s})^2} = 1.66054\times10^{-21}\ \text{J} = 1\ \text{kJ/mol}.
$$

<div class="legend" markdown="1">
- u: the atomic mass unit, $1.66054\times10^{-27}$ kg.
- nm, ps: nanometre and picosecond.
- kg, m, s, J: the SI units kilogram, metre, second and joule. One joule is 1 kg m$^2$ s$^{-2}$.
- The last step uses the formula above: $1.66054\times10^{-21}$ J for one molecule is 1 kJ/mol.
</div>

The two numbers agree because the atomic mass unit is one gram per mole divided by Avogadro's number, and the powers of ten in nm and ps cancel the rest. The consequence is that no conversion factor appears in Newton's law or in the kinetic energy. With masses in u, lengths in nm and times in ps, energies come out in kJ/mol, forces in kJ mol$^{-1}$ nm$^{-1}$, velocities in nm/ps and accelerations in nm ps$^{-2}$.

**Conversions.**

| This | equals |
|---|---|
| 1 nm | 10 Å |
| 1 ps | 1,000 fs |
| 1 kcal/mol | 4.184 kJ/mol |
| 1 kJ/mol | 0.2390 kcal/mol |
| 1 eV for one molecule (electronvolt) | 96.485 kJ/mol |
| 1 kcal mol$^{-1}$ Å$^{-2}$ (a spring constant) | 418.4 kJ mol$^{-1}$ nm$^{-2}$ |
| 1 kJ mol$^{-1}$ nm$^{-1}$ (a force) | 1.6605 pN (piconewton) |
| 1 nm/ps (a velocity) | 1,000 m/s |
| 1 kJ mol$^{-1}$ nm$^{-3}$ (a pressure) | 16.605 bar |
| 1 atm (atmosphere) | 1.01325 bar |
| 1 M (mol per litre, a concentration) | 0.6022 molecules per nm$^3$ |
| 1 D (debye, a dipole moment) | 0.02082 $e$ nm |
| 1 V (volt, an electric potential) | 96.485 kJ mol$^{-1}$ $e^{-1}$ |
| 1 cm$^{-1}$ (a wavenumber, as an energy) | 0.011963 kJ/mol |

**Constants in MD units.**

| Constant | Symbol | Value |
|---|---|---|
| Boltzmann's constant | $k_B$ | 0.0083145 kJ mol$^{-1}$ K$^{-1}$, which is $1.380649\times10^{-23}$ J/K for one molecule |
| Avogadro's number | $N_A$ | $6.02214\times10^{23}$ mol$^{-1}$ |
| Coulomb constant | $1/(4\pi\varepsilon_0)$ | 138.935 kJ mol$^{-1}$ nm $e^{-2}$, which is 332.06 kcal mol$^{-1}$ Å $e^{-2}$ |
| Planck's constant | $h$ | 0.399031 kJ mol$^{-1}$ ps, which is $6.62607\times10^{-34}$ J s |
| Speed of light | $c$ | 299,792 nm/ps, which is $2.99792\times10^{8}$ m/s |

**The thermal energy.** The one number worth knowing by heart is the product of Boltzmann's constant and the temperature:

$$
k_BT = 0.0083145\ \text{kJ mol}^{-1}\,\text{K}^{-1}\times 300\ \text{K} = 2.494\ \text{kJ/mol} = 0.596\ \text{kcal/mol}.
$$

<div class="legend" markdown="1">
- $k_B$: Boltzmann's constant. It converts a temperature into an energy.
- $T$: the temperature in kelvin, here 300 K (27 °C).
- $k_BT$: the thermal energy, the typical energy that random thermal motion gives to one molecule. See [Temperature and thermal energy](#temperature).
</div>

Chemistry books call the per-mole value of $k_B$ the gas constant, $R = N_Ak_B = 8.3145$ J mol$^{-1}$ K$^{-1}$. With energies in kJ/mol the two are the same number, and the lessons write $k_B$ throughout.

<div class="box key" markdown="1">
**Worked example: three conversions.**

1. *A free energy from a paper.* A binding free energy of $-10$ kcal/mol is $-10\times4.184 = -41.84$ kJ/mol. In units of the thermal energy at 300 K it is $-41.84/2.494 = -16.8\ k_BT$.
2. *A kinetic energy with no conversion factor.* A carbon atom (12 u) moves at 0.5 nm/ps. Its kinetic energy is $\tfrac12\times12\times0.5^2 = 1.5$ kJ/mol. The same in SI units: $\tfrac12\times(12\times1.66054\times10^{-27}\ \text{kg})\times(500\ \text{m/s})^2 = 2.49\times10^{-21}$ J, and multiplying by $N_A$ gives 1,500 J/mol, which is 1.5 kJ/mol.
3. *A spring constant.* 300 kcal mol$^{-1}$ Å$^{-2}$ is $300\times4.184\times100 = 125{,}520$ kJ mol$^{-1}$ nm$^{-2}$. The factor 100 appears because 1 Å$^{-2}$ is 100 nm$^{-2}$.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: the table of numbers worth memorising.
- [Module 2](02-classical-mechanics.html), Classical mechanics: the period of a bond vibration computed with no conversion factor.
- [Module 5](05-force-field-form.html), The form of a force field: every parameter has a unit, and force fields differ in their unit systems.
- [Module 10](10-running-a-simulation.html), Running a simulation: every number in an input file is in these units.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the standard concentration of 1 M as a volume per molecule.

<div class="box warn" markdown="1">
**A common mistake.** Mixing kJ with kcal, or nm with Å. An energy that is wrong by the factor 4.184 looks plausible, but energies enter probabilities through an exponential, so the populations computed from it are badly wrong. Spring constants are the usual trap: the factor between kcal mol$^{-1}$ Å$^{-2}$ and kJ mol$^{-1}$ nm$^{-2}$ is 418.4, because the length is squared. A second mistake is to put a temperature in °C into a formula. Every formula on this page needs kelvin.
</div>

## Motion, velocity, acceleration, force {#newton}

To describe motion you need three quantities, and each is the rate of change of the one before. The **position** says where an atom is. The **velocity** says how fast and in which direction the position is changing. The **acceleration** says how fast and in which direction the velocity is changing. In a car, the speedometer shows the size of the velocity, and you feel the acceleration in your back when the car speeds up, brakes or turns.

All three are [vectors](maths.html#vectors): each has a size and a direction and is stored as three numbers, one for each of $x$, $y$ and $z$. "Rate of change" is the [derivative](maths.html#derivative) with respect to time.

$$
\mathbf v = \frac{d\mathbf r}{dt} = \dot{\mathbf r}, \qquad \mathbf a = \frac{d\mathbf v}{dt} = \ddot{\mathbf r}.
$$

<div class="legend" markdown="1">
- $\mathbf r$: the position of the atom, a vector $(x, y, z)$, in nm.
- $t$: the time, in ps.
- $\mathbf v$: the velocity, in nm/ps. Its size, without the direction, is the **speed**.
- $\mathbf a$: the acceleration, in nm ps$^{-2}$.
- $d/dt$: the derivative with respect to time, "how fast this changes".
- The dots: a shorter way of writing the same thing. One dot is one time derivative, two dots are two.
</div>

What makes the velocity change is a **force**, a push or a pull. Newton's three laws say how.

1. **No force, no change.** An atom on which no force acts keeps its velocity. If it is at rest it stays at rest. If it moves, it goes on in a straight line at constant speed.
2. **A force changes the velocity.** The acceleration is the force divided by the mass. The same force changes the velocity of a heavy atom less than that of a light one.
3. **Forces come in pairs.** If atom A pushes atom B, then B pushes A with a force of the same size in the opposite direction.

The second law as a formula:

$$
m\,\mathbf a = \mathbf F .
$$

<div class="legend" markdown="1">
- $m$: the mass of the atom, in u.
- $\mathbf a$: its acceleration.
- $\mathbf F$: the total force on the atom, a vector, in kJ mol$^{-1}$ nm$^{-1}$. One such unit is 1.66 pN.
</div>

Read it as "acceleration equals force divided by mass". The force gives the acceleration, the acceleration changes the velocity, and the velocity changes the position. When the force is constant, this chain can be worked out exactly. Along one direction $x$:

$$
v(t) = v_0 + a\,t, \qquad x(t) = x_0 + v_0\,t + \tfrac12 a\,t^2 .
$$

<div class="legend" markdown="1">
- $x_0$, $v_0$: the position and the velocity at time zero.
- $a$: the constant acceleration, $F/m$.
- $t$: the time that has passed.
- $v(t)$, $x(t)$: the velocity and the position at time $t$.
</div>

The velocity grows in proportion to the time, and the position gets an extra term that grows with the time squared. Between atoms the force is never constant for long, because it changes as the atoms move. An MD program therefore uses formulas of this kind over one very short time step, computes the forces again, and repeats ([Module 4](04-integrators.html)).

<div class="box key" markdown="1">
**Worked example: one time step of one atom.** A carbon atom, $m = 12$ u, feels a force of 1,200 kJ mol$^{-1}$ nm$^{-1}$ along $x$ (an illustration). Its acceleration is $a = F/m = 1200/12 = 100$ nm ps$^{-2}$.

Follow it for one time step of 1 fs, which is 0.001 ps. The velocity changes by $a\,t = 100\times0.001 = 0.1$ nm/ps. If the atom started at rest it moves $\tfrac12 a t^2 = \tfrac12\times100\times0.001^2 = 5\times10^{-5}$ nm.

Compare this with thermal motion. At 300 K a carbon atom has a typical speed of 0.46 nm/ps along any one direction (see [Temperature and thermal energy](#temperature)). In 1 fs that velocity carries it $0.46\times0.001 = 4.6\times10^{-4}$ nm, about nine times farther than the force does. So within one step an atom mostly continues in a straight line, and the force bends its path a little. The effect of the forces builds up over many steps.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: the algorithm is Newton's second law applied again and again.
- [Module 2](02-classical-mechanics.html), Classical mechanics: Newton's law, and the same law rewritten by Lagrange and Hamilton.
- [Module 4](04-integrators.html), Integrators: how to turn accelerations into steps without losing accuracy.
- [Module 5](05-force-field-form.html), The form of a force field: where the force on each atom comes from.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: extra terms that are added to Newton's law to control the temperature.

<div class="box warn" markdown="1">
**A common mistake.** Thinking that a force is needed to keep something moving. Everyday experience suggests it, because a bicycle stops when you stop pedalling. But the bicycle stops because friction, a force, slows it down. Without any force an atom keeps its velocity for ever. A force is needed to *change* a velocity.

Also keep velocity and speed apart: an atom that goes round a circle at constant speed is accelerating all the time, because the direction of its velocity changes.
</div>

## Work, kinetic and potential energy {#energy}

Energy is a quantity that keeps its total while it passes from one form to another. Lift a shopping bag onto a table and you transfer energy from your arm to the bag. Push it off the table and that stored energy turns into energy of motion. Physics gives each of the three steps a name: the transfer is **work**, the stored energy is **potential energy**, and the energy of motion is **kinetic energy**.

**Work** is how a force transfers energy. It is the force multiplied by the distance moved in the direction of the force.

$$
W = F\,\Delta x \quad\text{(constant force)},\qquad W = \int_{x_1}^{x_2} F(x)\,dx \quad\text{(a force that changes along the way)}.
$$

<div class="legend" markdown="1">
- $W$: the work done by the force, an energy, in kJ/mol.
- $F$: the force along the direction of motion. A force at right angles to the motion does no work.
- $\Delta x$: the distance moved. The Greek capital delta, $\Delta$, means "change of".
- $x_1$, $x_2$: the positions where the motion starts and ends.
- $\int$: the [integral](maths.html#integral). It adds up force times distance over many small pieces of the path, each of length $dx$, and is the area under the curve of $F$ against $x$.
</div>

**Kinetic energy** is the energy that a mass has because it moves.

$$
K = \tfrac12 m v^2 .
$$

<div class="legend" markdown="1">
- $K$: the kinetic energy, in kJ/mol.
- $m$: the mass, in u.
- $v$: the speed, in nm/ps. For a velocity vector, $v^2 = v_x^2 + v_y^2 + v_z^2$.
</div>

The two are linked: the work done on a particle by the total force equals the change of its kinetic energy. You can check this for a constant force with the formulas of [the previous section](#newton). From $v = v_0 + at$ and $\Delta x = v_0t + \tfrac12at^2$ it follows that $v^2 = v_0^2 + 2a\,\Delta x$. Multiply by $\tfrac12m$ and use $ma = F$: $\tfrac12mv^2 - \tfrac12mv_0^2 = F\,\Delta x$.

**Potential energy** is energy stored in the arrangement of the atoms. It exists when the work that the force does between two points is the same whatever the route. All force-field forces are of this kind ([Module 2](02-classical-mechanics.html) calls them conservative). The work can then be written as the difference of a function $U$ of position.

$$
F = -\frac{dU}{dx}, \qquad U(x_2) - U(x_1) = -\int_{x_1}^{x_2} F(x)\,dx .
$$

<div class="legend" markdown="1">
- $U$: the potential energy, a function of the position, in kJ/mol.
- $dU/dx$: the [derivative](maths.html#derivative) of $U$, the slope of the curve of $U$ against $x$.
- The first minus sign: the force points downhill, towards lower $U$.
- The second formula: when the force does positive work, the potential energy falls by the same amount.
- $F$, $x$, $x_1$, $x_2$, $\int$: the force, the position, the two end points and the integral, as in the list for work above.
</div>

With many atoms, $U$ depends on all the positions, and the force on atom $i$ is minus the [gradient](maths.html#gradient) of $U$ with respect to the position of that atom ([Module 2](02-classical-mechanics.html)). Because the work that the force does is taken out of $U$ and put into $K$, the sum of the two does not change:

$$
E = K + U = \text{constant}.
$$

<div class="legend" markdown="1">
- $E$: the total energy.
- $K$: the kinetic energy of all atoms added together.
- $U$: the potential energy.
</div>

This is the **conservation of energy**. It holds when nothing outside the system pushes on it or exchanges heat with it.

**Energy landscapes.** Plot $U$ against the coordinates and you get a landscape of hills and valleys. A valley is a stable arrangement, because every small displacement is pushed back. A pass between two valleys is a **barrier**: the system needs at least that much energy to get from one valley to the other. With $N$ atoms there are $3N$ coordinates, so the landscape cannot be drawn. In practice people draw the energy along one or two chosen coordinates, such as a distance or a torsion angle.

<div class="box key" markdown="1">
**Worked example: a ball on a spring.** A spring has the potential energy $U = \tfrac12kx^2$, with $k = 100$ kJ mol$^{-1}$ nm$^{-2}$ (an illustration). An atom of mass 12 u is held at $x = 0.1$ nm and released from rest.

- At the start: $U = \tfrac12\times100\times0.1^2 = 0.5$ kJ/mol and $K = 0$, so $E = 0.5$ kJ/mol.
- Half-way, at $x = 0.05$ nm: $U = \tfrac12\times100\times0.05^2 = 0.125$ kJ/mol, so $K = 0.5 - 0.125 = 0.375$ kJ/mol. The speed is $v = \sqrt{2K/m} = \sqrt{2\times0.375/12} = 0.25$ nm/ps.
- At the bottom, $x = 0$: $U = 0$ and $K = 0.5$ kJ/mol, so $v = \sqrt{2\times0.5/12} = 0.29$ nm/ps.

Half-way in distance the atom already has three quarters of its final kinetic energy, because the spring force is largest at the start.

**Worked example: work.** A constant force of 100 kJ mol$^{-1}$ nm$^{-1}$ moves an atom by 0.02 nm along the force. The work is $100\times0.02 = 2$ kJ/mol, a little less than the thermal energy at 300 K.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the proof that the total energy is conserved, and the first test of any MD program.
- [Module 4](04-integrators.html), Integrators: the drift of the total energy measures the quality of an integrator.
- [Module 5](05-force-field-form.html), The form of a force field: the potential energy written term by term.
- [Module 10](10-running-a-simulation.html), Running a simulation: energy minimisation walks downhill on $U$ before the dynamics starts.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: the work done when a system is changed at a finite speed.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: barriers, and the work of pulling a molecule.

<div class="box warn" markdown="1">
**A common mistake.** Reading a meaning into the absolute value of a potential energy. Only differences of $U$ and its slopes have physical meaning. You can add any constant to $U$ and no force changes. So the potential energies of two different systems, or of the same molecule in two force fields, cannot be compared.

A second mistake is to treat the lowest potential energy as the most probable state. At a finite temperature the number of arrangements counts as well (see [Heat, entropy and free energy](#thermodynamics)).
</div>

## Momentum and angular momentum {#momentum}

The **momentum** of an atom is its mass times its velocity. It measures how hard the atom is to stop: a lorry and a bicycle at the same speed have very different momenta. Newton's second law can be read as "a force changes the momentum", and the third law then says that when two atoms push on each other, what one gains in momentum the other loses. The total is unchanged.

$$
\mathbf p = m\,\mathbf v, \qquad \frac{d\mathbf p}{dt} = \mathbf F, \qquad \mathbf P = \sum_i m_i\mathbf v_i .
$$

<div class="legend" markdown="1">
- $\mathbf p$: the momentum of one atom, a vector, in u nm/ps.
- $m$, $\mathbf v$: its mass and its velocity.
- $\mathbf F$: the total force on the atom. The middle formula is Newton's second law, because $d\mathbf p/dt = m\,\mathbf a$.
- $\mathbf P$: the total momentum of the system.
- $\sum_i$: a sum over all atoms, labelled by $i$.
</div>

The total momentum can be assigned to a single point that carries the whole mass, the **centre of mass**. It is the average position of the atoms, with each atom weighted by its mass.

$$
\mathbf R = \frac{1}{M}\sum_i m_i\,\mathbf r_i, \qquad M = \sum_i m_i, \qquad \mathbf P = M\,\dot{\mathbf R}.
$$

<div class="legend" markdown="1">
- $\mathbf R$: the position of the centre of mass.
- $M$: the total mass.
- $m_i$, $\mathbf r_i$: the mass and the position of atom $i$.
- $\dot{\mathbf R}$: the velocity of the centre of mass.
- $\mathbf P$, $\sum_i$: the total momentum and the sum over all atoms, as in the list above.
</div>

The centre of mass moves as if the whole mass sat there and only the forces from outside acted on it. The forces between the atoms of the system cancel in pairs and cannot move it. A molecule that tumbles and vibrates as it flies through empty space still has a centre of mass that travels in a straight line.

**Rotation** has its own versions of momentum and force. The **angular momentum** measures how much an atom is moving around a chosen point. The **torque** is the turning effect of a force. A door shows the idea: the same push turns the door more easily when you apply it far from the hinge.

$$
\mathbf L = \mathbf r\times\mathbf p, \qquad \boldsymbol\tau = \mathbf r\times\mathbf F, \qquad \frac{d\mathbf L}{dt} = \boldsymbol\tau .
$$

<div class="legend" markdown="1">
- $\mathbf L$: the angular momentum of the atom about the origin, in u nm$^2$ ps$^{-1}$.
- $\mathbf r$: the position of the atom, measured from the origin you chose.
- $\times$: the [cross product](maths.html#cross-product). It gives a vector at right angles to both factors. Its size is largest when the two factors are perpendicular and zero when they are parallel.
- $\boldsymbol\tau$ (Greek tau, bold): the torque.
- $\mathbf p$, $\mathbf F$: the momentum of the atom and the force on it, as in the first list of this section.
- The last formula: a torque changes the angular momentum, in the same way that a force changes the momentum.
</div>

For an atom that moves on a circle of radius $r$ at speed $v$, with the origin at the centre of the circle, the position and the momentum are perpendicular, so the size of the angular momentum is $L = m\,r\,v$. It points along the axis of the circle. An atom of 16 u on a circle of radius 0.1 nm at 0.5 nm/ps has $L = 16\times0.1\times0.5 = 0.8$ u nm$^2$ ps$^{-1}$.

When no force acts from outside, the total momentum is conserved. When no torque acts from outside, the total angular momentum is conserved.

<div class="box key" markdown="1">
**Worked example: a centre of mass.** A carbon atom (12 u) sits at $x = 0$ and an oxygen atom (16 u) at $x = 0.113$ nm (a round bond length for an illustration). The centre of mass is at $X = (12\times0 + 16\times0.113)/28 = 0.0646$ nm. It lies closer to the heavier atom: 0.065 nm from the carbon and 0.048 nm from the oxygen.

**Worked example: a collision.** An atom of 1 u moving at 2 nm/ps hits an atom of 16 u at rest, and the two stick together. The momentum before is $1\times2 = 2$ u nm/ps. Afterwards the pair has mass 17 u, so its velocity is $2/17 = 0.118$ nm/ps.

The kinetic energy before was $\tfrac12\times1\times2^2 = 2$ kJ/mol. The kinetic energy of the pair moving together is $\tfrac12\times17\times0.118^2 = 0.12$ kJ/mol. The missing 1.88 kJ/mol went into the vibration of the new pair. Momentum is conserved in every collision. The kinetic energy of the overall motion is not.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: momenta in Hamilton's equations, and which of the two totals a periodic box conserves.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the conserved total momentum removes three degrees of freedom from the temperature.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: programs remove the motion of the centre of mass.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the overall translation and rotation of a molecule are removed before its internal motion is analysed.
- [Module 15](15-coarse-grained.html), Coarse-grained models: a group of atoms is replaced by one particle, often placed at the centre of mass of the group.

<div class="box warn" markdown="1">
**A common mistake.** Confusing momentum with kinetic energy. Both are built from the mass and the velocity, but momentum is a vector and kinetic energy is a number that is never negative. Two equal atoms that fly apart at the same speed have a total momentum of zero and a total kinetic energy that is not zero. A second point: an angular momentum always refers to an origin. If you change the origin, its value changes.
</div>

## The harmonic oscillator {#oscillator}

Hang a weight on a spring, pull it down and let go. It moves up and down around its rest position in a steady rhythm. This is a **harmonic oscillator**: a mass that is pulled back towards a rest position by a force proportional to how far it has been moved. A child on a swing and a ball that rolls back and forth in a bowl behave in the same way for small swings, and so does a chemical bond.

$$
F = -k\,x, \qquad U = \tfrac12 k\,x^2, \qquad m\,\ddot x = -k\,x .
$$

<div class="legend" markdown="1">
- $x$: the displacement from the rest position, in nm. For a bond it is the bond length minus its rest length.
- $k$: the **spring constant** or stiffness, in kJ mol$^{-1}$ nm$^{-2}$. A large $k$ is a stiff spring.
- $F$: the restoring force. The minus sign says that it points against the displacement.
- $U$: the potential energy of the spring, a parabola. Its slope gives the force, $F = -dU/dx$.
- $m$: the mass. $\ddot x$: its acceleration. The third formula is Newton's second law for this force.
</div>

The third formula is a [differential equation](maths.html#ode): it says that the acceleration is always proportional to the displacement and opposite to it. Its solution is a cosine.

$$
x(t) = x_{\max}\cos(\omega t + \varphi), \qquad \omega = \sqrt{\frac{k}{m}} .
$$

<div class="legend" markdown="1">
- $x_{\max}$: the **amplitude**, the largest displacement reached.
- $\cos$: the cosine function. It swings between $+1$ and $-1$ and repeats each time its argument has grown by $2\pi$.
- $\omega$ (Greek omega): the **angular frequency**, in radians per ps. It says how fast the argument of the cosine grows.
- $\varphi$ (Greek phi): the phase, which says where in its cycle the oscillator is at $t = 0$.
- $k$, $m$: the spring constant and the mass, as in the list above. With $k$ in kJ mol$^{-1}$ nm$^{-2}$ and $m$ in u, the square root is in ps$^{-1}$.
- $t$: the time.
</div>

You can check the solution. Differentiating the cosine twice gives $\ddot x = -\omega^2x$. Put this into Newton's law: $-m\omega^2x = -kx$, which holds at all times if $\omega^2 = k/m$.

$$
T_{period} = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}}, \qquad \nu = \frac{1}{T_{period}} = \frac{\omega}{2\pi} .
$$

<div class="legend" markdown="1">
- $T_{period}$: the **period**, the time of one full oscillation. It is not a temperature.
- $\nu$ (Greek nu): the **frequency**, the number of oscillations per unit of time, in ps$^{-1}$. One ps$^{-1}$ is $10^{12}$ Hz (hertz, oscillations per second).
- $2\pi$: one full turn of the cosine, in radians.
- $\omega$, $m$, $k$: the angular frequency, the mass and the spring constant, as in the lists above.
</div>

Read it like this. A stiffer spring oscillates faster and a heavier mass oscillates more slowly. Because of the square root, four times the stiffness halves the period. The amplitude does not appear in the formula: a small swing and a large swing take the same time. That is special to the parabola and is only approximately true for real bonds.

The total energy of the oscillator is $E = \tfrac12mv^2 + \tfrac12kx^2 = \tfrac12kx_{\max}^2$. The last form holds because at the largest displacement the mass stands still for an instant, so all the energy is potential there. It passes from potential to kinetic and back twice in every period, as in the worked example of the section on [energy](#energy).

**Two atoms on one spring.** When two atoms are joined by a spring, both move. The bond length then oscillates with $\omega = \sqrt{k/\mu}$, where $\mu = m_1m_2/(m_1+m_2)$ is the **reduced mass** of the two atoms with masses $m_1$ and $m_2$ ([Module 2](02-classical-mechanics.html)). The reduced mass is always smaller than the lighter of the two masses. For a hydrogen bonded to a heavy atom it is close to 1 u.

**Why it is everywhere.** Near the bottom of any smooth valley of the potential energy, the curve looks like a parabola. This follows from the [Taylor expansion](maths.html#taylor): at a minimum the slope is zero, so the first term that matters is the quadratic one, with $k$ equal to the curvature of $U$ at the minimum. So any system close to a stable arrangement behaves like a set of harmonic oscillators. That is why force fields describe bonds and angles as springs, and why the harmonic oscillator is the standard test case for integrators and thermostats.

<div class="box key" markdown="1">
**Worked example: a stiff bond.** Take a bond between an oxygen (16 u) and a hydrogen (1 u) with $k = 4.5\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ (a round value for an illustration). The reduced mass is $\mu = 16\times1/(16+1) = 0.9412$ u. Then $\omega = \sqrt{4.5\times10^5/0.9412} = 691$ ps$^{-1}$. The period is $2\pi/691 = 0.0091$ ps, which is 9.1 fs, and the frequency is $\nu = 691/2\pi = 110$ ps$^{-1}$. The units need no conversion: kJ mol$^{-1}$ nm$^{-2}$ divided by u is ps$^{-2}$ (see [Units](#units)).

**Worked example: a soft spring.** A carbon atom (12 u) on a spring with $k = 100$ kJ mol$^{-1}$ nm$^{-2}$, fixed at the other end: $\omega = \sqrt{100/12} = 2.89$ ps$^{-1}$ and the period is $2\pi\sqrt{12/100} = 2.18$ ps. Compared with the bond above, the stiffness is 4,500 times smaller and the mass 12.75 times larger, so the period is $\sqrt{4500\times12.75} = 240$ times longer.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the vibrations of a molecule as a set of independent oscillators (normal modes).
- [Module 4](04-integrators.html), Integrators: the fastest oscillation in the system limits the time step.
- [Module 5](05-force-field-form.html), The form of a force field: bonds and angles are harmonic springs.
- [Module 9](09-constraints.html), Constraints: the fastest oscillators are frozen so that the time step can be longer.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: umbrella sampling holds a coordinate with a harmonic spring.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: the frequencies of a well and of a barrier top appear in the formulas for rates.

<div class="box warn" markdown="1">
**A common mistake.** Confusing the angular frequency $\omega$ with the frequency $\nu$. They differ by the factor $2\pi \approx 6.28$. The bond in the example has $\omega = 691$ ps$^{-1}$ but oscillates 110 times per picosecond, not 691 times. Before you use a "frequency" from a paper, check which of the two is meant.

A second point: a harmonic spring never breaks, however far you stretch it. A real bond does, so the spring is a good model only for small displacements.
</div>

## Temperature and thermal energy {#temperature}

The atoms of any material move all the time, even in a solid that looks still. In a liquid they jostle, collide and change direction many times in a picosecond. **Temperature** measures how much kinetic energy this random motion carries on average. In a hot cup of tea the water molecules move faster than in a cold one.

When two objects touch, their atoms collide at the surface and exchange kinetic energy. Energy flows from the side with more kinetic energy per atom to the side with less, until the averages are equal. Two objects at the same temperature are two objects for which this flow has stopped.

$$
\left\langle \tfrac12 m v_x^2 \right\rangle = \tfrac12 k_BT .
$$

<div class="legend" markdown="1">
- $m$: the mass of an atom.
- $v_x$: the $x$ component of its velocity.
- $\langle\ \rangle$: the [average](maths.html#averages), over a long time or over many atoms.
- $k_B$: Boltzmann's constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature in kelvin.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K.
</div>

The same holds for the $y$ and $z$ components. One atom therefore has $\tfrac32k_BT$ of kinetic energy on average, and for $N$ atoms

$$
\langle K\rangle = \tfrac32 N k_BT , \qquad \sqrt{\langle v^2\rangle} = \sqrt{\frac{3k_BT}{m}} .
$$

<div class="legend" markdown="1">
- $K$: the total kinetic energy of the system.
- $N$: the number of atoms, each free to move in three directions.
- $\sqrt{\langle v^2\rangle}$: the root-mean-square speed, the typical speed of an atom of mass $m$. It follows from $\langle\tfrac12mv^2\rangle = \tfrac32k_BT$.
- Other symbols: as in the list above.
</div>

Read it like this. All atoms have the same average kinetic energy, whatever their mass, so light atoms are faster than heavy ones. The typical speed grows with the square root of the temperature: to double the speed you must multiply the temperature (in kelvin) by four.

The single velocities are spread around these typical values. Each component of the velocity of an atom, for example $v_x$, follows a [Gaussian](maths.html#gaussian) distribution with mean zero and standard deviation $\sqrt{k_BT/m}$. This is the **Maxwell-Boltzmann distribution** ([Module 3](03-statistical-mechanics.html)). The "typical speed along one direction" quoted on this page is this standard deviation.

**Equipartition.** The rule is more general. Every term in the energy that is a constant times the square of a velocity or of a coordinate holds $\tfrac12k_BT$ on average. Each velocity component gives such a term, $\tfrac12mv_x^2$, and so does a harmonic spring, $\tfrac12kx^2$. The thermal energy is shared equally between all these terms, which is what the word **equipartition** means. Each independent way in which a system can move is called a **degree of freedom**.

For a spring the rule gives the typical displacement at once: $\langle\tfrac12kx^2\rangle = \tfrac12k_BT$ means $\sqrt{\langle x^2\rangle} = \sqrt{k_BT/k}$. For the soft spring of the last section, $k = 100$ kJ mol$^{-1}$ nm$^{-2}$, this is $\sqrt{2.494/100} = 0.16$ nm. [Module 3](03-statistical-mechanics.html) proves the rule. It belongs to classical physics and fails for very stiff vibrations such as bond stretches (see [Why atoms can be treated as classical balls](#quantum)).

**The yardstick.** The thermal energy is the scale against which every other energy in the course is judged. In a system at temperature $T$, a state with a higher energy is less probable, by a factor that depends only on the energy difference divided by $k_BT$.

$$
\frac{P_2}{P_1} = e^{-(E_2 - E_1)/k_BT}, \qquad \beta = \frac{1}{k_BT} .
$$

<div class="legend" markdown="1">
- $P_1$, $P_2$: the probabilities of finding the system in state 1 and in state 2. A state is here one definite arrangement of the atoms (a microstate, see [Heat, entropy and free energy](#thermodynamics)). Here $P$ is not a pressure.
- $E_1$, $E_2$: the energies of the two states.
- $e^{-\dots}$: the [exponential function](maths.html#exp-log). The factor is called the **Boltzmann factor**.
- $\beta$ (Greek beta): a shorthand used in all the lessons. At 300 K, $\beta = 1/2.494 = 0.401$ mol/kJ. With it the factor reads $e^{-\beta(E_2-E_1)}$.
</div>

| Energy difference | In kJ/mol at 300 K | Boltzmann factor |
|---|---|---|
| $1\,k_BT$ | 2.5 | 0.37 |
| $2.3\,k_BT$ | 5.7 | 0.10 |
| $5\,k_BT$ | 12.5 | 0.0067 |
| $10\,k_BT$ | 24.9 | $4.5\times10^{-5}$ |
| $20\,k_BT$ | 49.9 | $2.1\times10^{-9}$ |

A difference well below $k_BT$ hardly matters. A difference of many $k_BT$ makes the upper state very rare. [Module 3](03-statistical-mechanics.html) derives the Boltzmann factor.

<div class="box key" markdown="1">
**Worked example: how fast are molecules?** A water molecule at 300 K, with $m = 18.015$ u, has a typical speed of $\sqrt{3\times2.494/18.015} = 0.644$ nm/ps, which is 644 m/s. Along one direction the typical speed is $\sqrt{2.494/18.015} = 0.372$ nm/ps. A hydrogen atom (1.008 u) has $\sqrt{3\times2.494/1.008} = 2.72$ nm/ps and a carbon atom (12.011 u) has 0.79 nm/ps. Both have the same average kinetic energy, and the hydrogen is about 3.5 times faster.

**Worked example: the temperature of a simulation.** A system of 1,000 atoms has 2,997 degrees of freedom (three per atom, minus three for the conserved total momentum). At one instant its kinetic energy is 3,700 kJ/mol. Each degree of freedom should hold $\tfrac12k_BT$, so $T = 2K/(2997\,k_B) = 2\times3700/(2997\times0.0083145) = 297$ K.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: $k_BT$ is among the numbers to memorise.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the Boltzmann factor and equipartition are derived, and the temperature of a simulation is defined.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: how a program holds the temperature.
- [Module 10](10-running-a-simulation.html), Running a simulation: starting velocities are drawn for the chosen temperature.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: copies of the system at higher temperatures cross barriers more often.
- [Module 15](15-coarse-grained.html), Coarse-grained models: what temperature means when atoms have been merged.

<div class="box warn" markdown="1">
**A common mistake.** Giving a temperature to one atom or to one instant. Temperature is defined through an average. The value that a program computes from the kinetic energy at one step goes up and down around the target even in a perfect simulation, and the smaller the system, the larger these swings ([Module 3](03-statistical-mechanics.html) gives the formula). A trace of the temperature that wanders by a few kelvin is correct.
</div>

## Pressure and volume {#pressure}

The molecules of a gas or a liquid hit the walls of their container all the time. Each hit is a small push. Over the enormous number of hits on every part of the wall, the pushes add up to a steady force. **Pressure** is that force divided by the area of the wall. A bicycle tyre is hard because the air inside is denser than the air outside, so more molecules hit the rubber from the inside.

$$
P = \frac{F}{A} .
$$

<div class="legend" markdown="1">
- $P$: the pressure.
- $F$: the force on the wall, at right angles to it.
- $A$: the area of the wall.
</div>

The SI unit is the pascal, 1 Pa = 1 N/m$^2$, and 1 bar is $10^5$ Pa. In MD units a force divided by an area is in kJ mol$^{-1}$ nm$^{-3}$, and one such unit is 16.6 bar.

For a gas whose molecules do not interact with each other, an **ideal gas**, the pressure follows from the number of molecules, the volume and the temperature alone.

$$
P\,V = N\,k_BT \qquad\text{or}\qquad P = \rho\,k_BT .
$$

<div class="legend" markdown="1">
- $V$: the volume of the container, in nm$^3$.
- $N$: the number of molecules.
- $\rho$ (Greek rho): the number density $N/V$, in molecules per nm$^3$.
- $P$: the pressure, as above. With $V$ in nm$^3$ and $k_BT$ in kJ/mol it comes out in kJ mol$^{-1}$ nm$^{-3}$. Multiply by 16.605 to get bar.
- $k_BT$: the thermal energy.
</div>

Read it like this. More molecules in the same volume give more hits. A higher temperature gives faster molecules, which hit more often and harder. A larger volume gives each molecule a longer way between two hits on the wall. Chemistry books write the same law as $PV = nRT$, with $n$ the amount in moles and $R$ the gas constant.

**Liquids.** In a liquid the molecules are in contact, and the forces between them change the pressure. Attractions hold the molecules together and lower the pressure. Repulsions push them apart and raise it. [Module 3](03-statistical-mechanics.html) writes the pressure as the ideal-gas term plus a term from the forces, called the virial. In a liquid at 1 bar both terms are very large and they almost cancel (first worked example below).

**Compressibility.** How much does the volume shrink when the pressure rises?

$$
\kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial P}\right)_T .
$$

<div class="legend" markdown="1">
- $\kappa_T$ (Greek kappa): the **isothermal compressibility**, in bar$^{-1}$. It is the fraction by which the volume shrinks for each bar of added pressure.
- $\partial V/\partial P$: the [partial derivative](maths.html#partial-derivative) of the volume with respect to the pressure.
- The subscript $T$ on the bracket: the temperature is held fixed while the pressure changes.
- The minus sign: the volume falls when the pressure rises, so the sign makes $\kappa_T$ positive.
</div>

Water is hard to compress: $\kappa_T = 4.5\times10^{-5}$ bar$^{-1}$ near room temperature. For an ideal gas, $V = Nk_BT/P$ gives $\partial V/\partial P = -V/P$ and so $\kappa_T = 1/P$, which is 1 bar$^{-1}$ at 1 bar. A gas at 1 bar is 22,000 times easier to compress than water.

<div class="box key" markdown="1">
**Worked example: a gas and a liquid.** At 1 bar and 300 K the volume for each molecule of an ideal gas is $V/N = k_BT/P$. In MD units 1 bar is $1/16.605 = 0.06022$ kJ mol$^{-1}$ nm$^{-3}$, so $V/N = 2.494/0.06022 = 41.4$ nm$^3$, a cube with an edge of 3.5 nm. Liquid water has 33.4 molecules per nm$^3$, which is 0.030 nm$^3$ for each molecule, about 1,400 times less.

Now put the density of liquid water into the ideal-gas law: $\rho k_BT = 33.4\times2.494 = 83.3$ kJ mol$^{-1}$ nm$^{-3}$, which is $83.3\times16.605 = 1{,}383$ bar. The real pressure is 1 bar. So the forces between the molecules contribute about $-1{,}382$ bar. Two large numbers almost cancel, and a small change in the distances between molecules changes the balance by many bar.

**Worked example: compressing water.** Raising the pressure by 100 bar shrinks water by $100\times4.5\times10^{-5} = 0.0045$, which is 0.45 %. Turned around: a change of the volume by 0.1 % goes with a change of the pressure by $0.001/(4.5\times10^{-5}) = 22$ bar.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the pressure of a simulation from the forces between atoms (the virial).
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the correction to the pressure for interactions beyond the cutoff.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: how a program holds the pressure, and why the compressibility is one of its settings.
- [Module 10](10-running-a-simulation.html), Running a simulation: equilibration at constant pressure, judged by the density.

<div class="box warn" markdown="1">
**A common mistake.** Expecting the pressure printed at each step to be close to 1 bar. The two worked examples show why it cannot be: the pressure of a liquid is a small difference between large terms, and water hardly compresses. In a box of a few nanometres the instantaneous pressure swings by hundreds of bar, and this is correct. Judge the average over a long stretch, and judge equilibration by the density ([Module 8](08-thermostats-barostats.html)).
</div>

## Heat, entropy and free energy {#thermodynamics}

Thermodynamics is the bookkeeping of energy for a **system** that exchanges energy with its **surroundings**. In a simulation the system is everything in the box. The surroundings are an imagined large reservoir, the **heat bath**, that holds the temperature fixed. This section introduces heat, work, entropy, enthalpy and free energy. The last one decides what a molecule does at a given temperature, and several lessons are about computing it.

**The first law: energy is conserved.** The energy of the system can change in two ways. **Work** is energy transferred by a force that moves something in an ordered way: a piston is pushed in, or a molecule is pulled by one end. **Heat** is energy transferred by the random collisions of atoms at the boundary between system and surroundings.

$$
\Delta E = Q + W .
$$

<div class="legend" markdown="1">
- $E$: the **internal energy** of the system, the kinetic plus the potential energy of all its atoms.
- $\Delta$: "change of": the value at the end minus the value at the start.
- $Q$: the heat that flows into the system. It is negative when heat flows out. Here $Q$ is not the partition function of Module 3.
- $W$: the work done on the system. It is negative when the system does work on the surroundings.
</div>

**The second law: which way things go.** A hot cup of tea cools to room temperature and never warms up again by itself. A drop of ink spreads through a glass of water and never gathers again. The reverse processes would conserve energy, so the first law does not forbid them. What forbids them is a matter of counting.

Throw 100 coins. "All heads" can happen in one way. "Fifty heads and fifty tails" can happen in about $10^{29}$ ways, because that is the number of ways to choose which fifty coins show heads ([counting](maths.html#combinatorics)). Every single arrangement is equally likely, so you will practically always find about half heads, because nearly all arrangements look like that.

Atoms behave like the coins. One detailed arrangement, with every position and every velocity given, is a **microstate**. What you see on a large scale ("the ink is spread out", "the protein is unfolded") is a **macrostate**, and it contains very many microstates. A system left to itself ends up in the macrostate with the most microstates, because that is where almost all the possibilities are. **Entropy** measures that number.

$$
S = k_B\ln\Omega .
$$

<div class="legend" markdown="1">
- $S$: the entropy of a macrostate, in kJ mol$^{-1}$ K$^{-1}$.
- $\Omega$ (Greek capital omega): the number of microstates that belong to the macrostate.
- $\ln$: the [natural logarithm](maths.html#exp-log). It turns products into sums. Two independent systems have $\Omega_1\Omega_2$ microstates together, and their entropies add: $S_1 + S_2$.
- $k_B$: Boltzmann's constant. It gives the entropy its unit, so that $T$ times $S$ is an energy.
</div>

The second law says: the total entropy of a system and its surroundings never decreases. It grows until the macrostate with the most microstates is reached. That state is **equilibrium**.

Entropy is connected with heat. When heat $Q$ flows slowly into a body at temperature $T$, the entropy of the body rises by $Q/T$: more energy can be shared out among the atoms in more ways. The same heat adds more entropy to a cold body than it removes from a hot one, because it is divided by a smaller $T$. That is why heat flows from hot to cold.

**Free energy: the second law for a system at constant temperature.** A simulated system is not isolated. It exchanges heat with the bath. The second law applies to the system and the bath together, but it can be rewritten as a statement about the system alone.

Let the system change at constant volume, with no work done. Its energy changes by $\Delta E$ and its entropy by $\Delta S$. The energy came from the bath as heat, so the bath lost the heat $\Delta E$, and its entropy changed by $-\Delta E/T$.

The total entropy change is $\Delta S - \Delta E/T$, and the second law says that it cannot be negative. Multiply by $-T$, which turns "not negative" into "not positive": $\Delta E - T\Delta S \le 0$. This combination has a name.

$$
A = E - TS, \qquad \Delta A = \Delta E - T\,\Delta S \le 0 .
$$

<div class="legend" markdown="1">
- $A$: the **Helmholtz free energy**, in kJ/mol. Some books write $F$.
- $E$: the internal energy of the system.
- $T$: the temperature of the bath, held fixed.
- $S$: the entropy of the system.
- $\le 0$: at constant temperature and volume the system can only move to states of lower $A$. Equilibrium is the state of lowest $A$.
</div>

Read it like this. The free energy falls when the energy falls or when the entropy rises. A state can win by having a low energy (strong, favourable interactions) or by having a high entropy (many arrangements). The temperature sets the exchange rate between the two: at low temperature the energy decides, at high temperature the entropy decides.

A protein unfolds when it is heated for this reason. The unfolded chain has a higher energy but far more conformations.

**Work and free energy.** The same argument covers a change that is driven from outside, for example by pulling on a molecule. Let the work $W$ be done on the system while it stays in contact with the bath. By the first law the heat that the system takes from the bath is $\Delta E - W$, so the entropy of the bath changes by $-(\Delta E - W)/T$. The total entropy change, $\Delta S - (\Delta E - W)/T$, cannot be negative, which gives $W \ge \Delta E - T\,\Delta S = \Delta A$.

So the free-energy difference is the smallest amount of work that the change can cost. The work equals $\Delta A$ only when the change is made infinitely slowly. A faster change costs more, and the extra work ends up as heat in the bath. For a system as small as one molecule the work differs from one repetition to the next, and the rule holds for the average ([Module 13](13-alchemical-free-energy.html)).

**Constant pressure: enthalpy and the Gibbs free energy.** Most experiments are done at constant pressure, not at constant volume. The system can then expand, and to do so it must push the surroundings back, which costs the energy $P\,\Delta V$. Two more quantities take this into account.

$$
H = E + PV, \qquad G = H - TS .
$$

<div class="legend" markdown="1">
- $H$: the **enthalpy**. At constant pressure, the heat that flows into the system equals $\Delta H$. Here $H$ is not the Hamiltonian of Module 2.
- $P$, $V$: the pressure and the volume of the system.
- $G$: the **Gibbs free energy**. At constant temperature and pressure the system moves to lower $G$, and equilibrium is the state of lowest $G$.
- $E$, $T$, $S$: as in the list above.
</div>

For a liquid at 1 bar the term $PV$ is tiny. One water molecule takes up 0.030 nm$^3$, so $PV = 0.06022\times0.030 = 0.0018$ kJ/mol for each molecule, a thousand times less than $k_BT$. In solution $\Delta G$ and $\Delta A$ are therefore almost the same number, and so are $\Delta H$ and $\Delta E$. The difference matters when a gas is formed. When a liquid evaporates, each molecule gains the volume $k_BT/P$ of a gas molecule, so $P\,\Delta V \approx k_BT = 2.5$ kJ/mol at 300 K.

| Symbol | Name | Definition | What it is for |
|---|---|---|---|
| $E$ | internal energy | kinetic plus potential energy | conserved in an isolated system |
| $H$ | enthalpy | $E + PV$ | heat exchanged at constant pressure |
| $A$ | Helmholtz free energy | $E - TS$ | lowest at equilibrium at constant volume and temperature |
| $G$ | Gibbs free energy | $H - TS$ | lowest at equilibrium at constant pressure and temperature |

**Free energy and probability.** A free-energy difference between two macrostates tells you how much more often the system is found in one than in the other.

$$
\frac{P_B}{P_A} = e^{-\Delta A/k_BT}, \qquad \Delta A = A_B - A_A .
$$

<div class="legend" markdown="1">
- The subscripts $A$ and $B$: the names of two macrostates, for example "folded" and "unfolded", or "bound" and "unbound".
- $P_A$, $P_B$: the probabilities of finding the system in each. Here $P$ is not a pressure.
- $A_A$, $A_B$: the Helmholtz free energies of the two macrostates. The large $A$ is the free energy and the subscript is the name of the state. At constant pressure, use $G$ in place of the free energy $A$.
- $k_BT$: the thermal energy.
</div>

This is the Boltzmann factor of the section on [temperature](#temperature), with the free energy in the place of the energy. The entropy enters because a macrostate with more microstates is found more often. If each of the $\Omega$ microstates of a macrostate has the same energy $E$, the probability of the macrostate is proportional to $\Omega\,e^{-E/k_BT}$. Because $\Omega = e^{S/k_B}$, this is $e^{-(E-TS)/k_BT}$, the Boltzmann factor of the free energy $A = E - TS$. [Module 3](03-statistical-mechanics.html) derives the formula in general.

The formula also says how to read the rule that a system moves to lower $A$. For a glass of water, the free-energy differences between macrostates are enormous compared with $k_BT$, so the macrostate of lowest free energy is found practically always. For a single molecule the differences are a few $k_BT$. The molecule then visits both states again and again, and the one with the higher free energy less often.

<div class="box key" markdown="1">
**Worked example: energy against entropy.** A molecule has two macrostates at 300 K. State A is one conformation with energy 0. State B consists of 1,000 conformations, each with energy $+10$ kJ/mol.

- Energy: $\Delta E = +10$ kJ/mol. It favours A.
- Entropy: $\Delta S = k_B\ln(1000/1) = 0.0083145\times6.9078 = 0.05743$ kJ mol$^{-1}$ K$^{-1}$, so $T\Delta S = 300\times0.05743 = 17.23$ kJ/mol. It favours B.
- Free energy: $\Delta A = 10 - 17.23 = -7.23$ kJ/mol. B wins.
- Populations: $P_B/P_A = e^{7.23/2.494} = 18$. The molecule is found in B 18 times more often than in A, although every conformation of B has a higher energy than A.

The balance changes with temperature. $\Delta A = 0$ when $T = \Delta E/\Delta S = 10/0.05743 = 174$ K. Below 174 K state A is the more populated one, above it state B. [Module 3](03-statistical-mechanics.html) does the same calculation in another way.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: entropy and free energy from the count of states, and the link to probabilities.
- [Module 6](06-force-field-parameters.html), Force-field parameters: heats of vaporisation and free energies of solvation as data for fitting.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: constant volume or constant pressure, and which free energy belongs to each.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: free-energy surfaces from histograms of a trajectory.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the free energy along a coordinate.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: free-energy differences between two molecules, and the link between work and free energy.
- [Module 15](15-coarse-grained.html), Coarse-grained models: why the interaction between merged particles is a free energy.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: the free energy of a barrier and the rate of crossing it.

<div class="box warn" markdown="1">
**A common mistake.** Taking the structure with the lowest potential energy for the most populated one. The example shows that it need not be. Populations follow the free energy, which includes the number of arrangements, and that number includes the arrangements of the water around the molecule. A second trap is the word "disorder" for entropy. It is a count of microstates, and a state can look ordered to the eye and still have the larger count.
</div>

## Equilibrium constants and free energy {#equilibrium}

A molecule that can exist in two forms, A and B, keeps switching between them. At **equilibrium** the switches from A to B happen as often as those from B to A. The fraction of molecules in each form then stays constant, although every single molecule goes on switching. The ratio of the two fractions is the **equilibrium constant**. It is what an experiment measures, and it is a free-energy difference in another form.

$$
K = \frac{[\text{B}]}{[\text{A}]} = e^{-\Delta G/k_BT}, \qquad \Delta G = -k_BT\ln K .
$$

<div class="legend" markdown="1">
- $[\text{A}]$, $[\text{B}]$: the concentrations of the two forms at equilibrium. Square brackets mean "concentration of", in mol per litre (M).
- $K$: the equilibrium constant. For this reaction it is a pure number. Here $K$ is not the kinetic energy.
- $\Delta G$: the Gibbs free energy of form B minus that of form A, with both at the same concentration (chemistry books write $\Delta G^\circ$). A negative value means that B is favoured. It is not the $\Delta G$ of the statement "at equilibrium $\Delta G = 0$", which is the free-energy change at the concentrations actually present.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K. Chemistry books write $RT$, which is the same number for a mole.
- $\ln$: the natural logarithm, the inverse of the exponential.
</div>

This is the probability formula of the [last section](#thermodynamics), because the ratio of the concentrations is the ratio of the probabilities $P_B/P_A$. Read it like this. When $\Delta G = 0$, $K = 1$ and the two forms are equally populated. Each factor of 10 in $K$ corresponds to $k_BT\ln10 = 5.74$ kJ/mol (1.37 kcal/mol) at 300 K. At 298 K, the temperature used in [Module 1](01-what-is-md.html), it is 5.71 kJ/mol (1.36 kcal/mol).

| $\Delta G$ in kJ/mol at 300 K | $K$ | Fraction in form B |
|---|---|---|
| 0 | 1 | 50 % |
| $-2.5$ (one $k_BT$) | 2.7 | 73 % |
| $-5.7$ | 10 | 91 % |
| $-11.5$ | 100 | 99 % |
| $-20$ | 3,000 | 99.97 % |

**Binding.** When two molecules join, a protein P and a ligand L forming the complex PL, there are two constants in use, and one is the inverse of the other.

$$
K_a = \frac{[\text{PL}]}{[\text{P}][\text{L}]}, \qquad K_d = \frac{1}{K_a} = \frac{[\text{P}][\text{L}]}{[\text{PL}]} .
$$

<div class="legend" markdown="1">
- $[\text{P}]$, $[\text{L}]$: the concentrations of free protein and free ligand at equilibrium.
- $[\text{PL}]$: the concentration of the complex.
- $K_a$: the **association constant**. Its unit is M$^{-1}$.
- $K_d$: the **dissociation constant**. Its unit is M. A small $K_d$ means tight binding.
</div>

The dissociation constant has a direct meaning. Solve its definition for the complex, $[\text{PL}] = [\text{P}][\text{L}]/K_d$, and put this into the fraction of the protein that carries a ligand. Then divide the top and the bottom by $[\text{P}]$ and multiply both by $K_d$:

$$
\text{fraction bound} = \frac{[\text{PL}]}{[\text{P}] + [\text{PL}]} = \frac{[\text{L}]}{[\text{L}] + K_d} .
$$

<div class="legend" markdown="1">
- $[\text{L}]$: the concentration of free ligand.
- $K_d$: the dissociation constant.
- Other symbols: as in the list above.
</div>

When $[\text{L}] = K_d$ the fraction is one half. So $K_d$ is the concentration of free ligand at which half of the protein is occupied. With $K_d = 1$ nM and 10 nM of free ligand, the occupied fraction is $10/(10+1) = 0.91$.

**The standard state.** For the reaction between A and B, $K$ was a pure number. $K_a$ has a unit, and the logarithm of a quantity with a unit is not defined. It must first be multiplied by a reference concentration.

$$
\Delta G^\circ_{bind} = -k_BT\ln\big(K_a C^\circ\big) = k_BT\ln\frac{K_d}{C^\circ}, \qquad C^\circ = 1\ \text{M} .
$$

<div class="legend" markdown="1">
- $\Delta G^\circ_{bind}$: the **standard free energy of binding**. The small circle means "with every species at the standard concentration".
- $C^\circ$: the **standard concentration**, 1 mol per litre by convention. In MD units it is 0.6022 molecules per nm$^3$, or one molecule in every 1.661 nm$^3$ (the standard volume $V^\circ$ of [Module 12](12-free-energy-pmf.html)).
- $K_aC^\circ$ and $K_d/C^\circ$: pure numbers, so the logarithm can be taken.
- $k_BT$, $\ln$, $K_a$, $K_d$: as in the lists above. The second form follows from $K_a = 1/K_d$ and $\ln(1/x) = -\ln x$.
</div>

There is physics behind this. A free ligand can be anywhere in the volume that the solution offers to each molecule, and that volume depends on the concentration. Binding takes this freedom away. The more dilute the solution, the more freedom is lost and the less favourable binding is.

A "free energy of binding" therefore means nothing until the concentration is stated, and the convention is 1 M. Another convention would shift every $\Delta G^\circ$ by the same constant, so differences between two ligands do not depend on it.

Binding constants are also linked to rates: $K_d = k_{off}/k_{on}$, where $k_{on}$ is the rate constant for binding and $k_{off}$ the one for unbinding ([Module 16](16-kinetics-msm.html)).

<div class="box key" markdown="1">
**Worked example: from a dissociation constant to a free energy.** A complex has $K_d = 1$ nM, which is $10^{-9}$ M. At 300 K, $\Delta G^\circ = 2.494\times\ln(10^{-9}) = 2.494\times(-20.72) = -51.7$ kJ/mol, or $-12.4$ kcal/mol. For $K_d = 1$ µM the result is $2.494\times(-13.82) = -34.5$ kJ/mol. The two differ by three factors of ten, and $3\times5.74 = 17.2$ kJ/mol.

The convention matters. If the standard concentration were 1 mM, the 1 nM complex would have $\Delta G^\circ = 2.494\times\ln(10^{-9}/10^{-3}) = -34.5$ kJ/mol. It is the same complex, and the number differs by $k_BT\ln1000 = 17.2$ kJ/mol.

**Worked example: the concentration in a simulation box.** One ligand in a cubic box with an edge of 5 nm has $1/125 = 0.008$ molecules per nm$^3$. Divide by 0.6022 to get mol per litre: 0.0133 M, or 13 mM. That is far above the $K_d$ of most complexes of interest. A simulation of one protein and one ligand is therefore not at the standard concentration, and [Module 12](12-free-energy-pmf.html) shows how to convert.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: the free energy that corresponds to a factor of ten in a binding constant.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the binding constant written with the tools of statistical mechanics.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: from a free-energy profile to $K_d$, with the correct standard state.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: binding free energies computed by transforming molecules.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: $K_d$ as a ratio of two rates.

<div class="box warn" markdown="1">
**A common mistake.** Reporting the depth of a free-energy well, or a free-energy difference measured in one simulation box, as "the binding free energy". The depth of a well is not a free energy of binding, and a difference measured in one box depends on the size of that box. Only the reference to 1 M gives a number that can be compared with experiment ([Module 12](12-free-energy-pmf.html)). Two smaller traps: the sign (binding has a negative $\Delta G^\circ$ when $K_d$ is below 1 M, and dissociation has the opposite sign), and the logarithm ($\ln K = 2.303\times\log_{10}K$).
</div>

## Charge and Coulomb's law {#electrostatics}

**Charge** is a property of matter, like mass. Unlike mass it comes in two kinds, positive and negative. Two charges of the same kind repel each other, and two of opposite kinds attract.

In an atom the nucleus is positive and the electrons are negative. A proton carries the charge $+e$ and an electron $-e$, where $e$ is the elementary charge. An **ion** is an atom or a molecule with unequal numbers of the two. Almost everything that atoms do to each other comes from electric forces between their nuclei and their electrons.

Coulomb's law gives the energy of two point charges.

$$
U(r) = \frac{q_1q_2}{4\pi\varepsilon_0\,r} = 138.935\ \frac{q_1q_2}{r}\ \text{kJ/mol}\qquad(q \text{ in } e,\ r \text{ in nm}).
$$

<div class="legend" markdown="1">
- $q_1$, $q_2$: the two charges, in units of $e$. They can be fractions (see [Dipoles and polarisation](#dipoles)).
- $r$: the distance between the charges, in nm.
- $\varepsilon_0$ (Greek epsilon, with a zero): the vacuum permittivity, a constant of nature that fixes how strong electric forces are in SI units.
- $4\pi$: a geometric factor that belongs to the SI definition of $\varepsilon_0$.
- $1/(4\pi\varepsilon_0)$: the Coulomb constant. In MD units it is 138.935 kJ mol$^{-1}$ nm $e^{-2}$.
- $U$: the energy of the pair, counted as zero when the charges are infinitely far apart.
</div>

The force is minus the slope of this energy.

$$
F(r) = -\frac{dU}{dr} = \frac{q_1q_2}{4\pi\varepsilon_0\,r^2} .
$$

<div class="legend" markdown="1">
- $F$: the force along the line that joins the two charges. A positive value pushes them apart, a negative value pulls them together.
- $dU/dr$: the derivative of $U$ with respect to the distance. The derivative of $1/r$ is $-1/r^2$.
- Other symbols: as in the list above.
</div>

Read it like this. For two charges of the same sign the product $q_1q_2$ is positive, the energy is positive and falls when they move apart, so they repel. For opposite signs everything is reversed.

The energy decays slowly: at twice the distance it is still one half. Compare the attraction between two neutral atoms (the Lennard-Jones attraction of the section on [forces between molecules](#intermolecular)), which falls to 1/64 at twice the distance. This slow decay is the reason why electrostatics needs special methods in a simulation ([Module 7](07-boundaries-electrostatics.html)).

**Potential and field.** It is often useful to describe what a set of charges does to the space around it, before saying which charge will feel it. The **electrostatic potential** at a point is the energy that a test charge of $+1\,e$ would have there. The **electric field** is the force that the test charge would feel.

$$
\phi(\mathbf r) = \sum_j \frac{q_j}{4\pi\varepsilon_0\,\vert\mathbf r - \mathbf r_j\vert}, \qquad U = q\,\phi(\mathbf r), \qquad \mathbf E = -\nabla\phi, \qquad \mathbf F = q\,\mathbf E .
$$

<div class="legend" markdown="1">
- $\phi(\mathbf r)$ (Greek phi): the electrostatic potential at the point $\mathbf r$, in kJ mol$^{-1}$ $e^{-1}$. One volt is 96.485 of these units.
- $\sum_j$: a sum over the charges $q_j$ that create the potential, at the positions $\mathbf r_j$. The potentials of several charges add.
- $\vert\mathbf r - \mathbf r_j\vert$: the distance from charge $j$ to the point. The bars mean "length of the vector".
- $q$: a charge placed at the point, and $U$ its energy there.
- $\mathbf E$ (bold): the electric field at the point, a vector. It is a force for each unit of charge, not an energy.
- $\nabla$: the [gradient](maths.html#gradient). The field points in the direction in which the potential falls fastest.
- $\mathbf F$: the force on the charge $q$.
</div>

For a continuous cloud of charge the same relation between charge and potential is written as Poisson's equation, $\nabla^2\phi = -\rho/\varepsilon_0$, where $\rho$ is the charge density (charge in each unit of volume) and $\nabla^2$ is the Laplacian ([toolbox](maths.html#divergence)). Module 7 writes it as $\nabla^2\phi = -4\pi\rho$, which is the same equation in units where the Coulomb constant $1/(4\pi\varepsilon_0)$ is set to 1, so that $1/\varepsilon_0 = 4\pi$. In those units a point charge $q$ creates the potential $q/r$, and every energy is multiplied by 138.935 at the end to get kJ/mol. One consequence of Poisson's equation is used there: seen from outside, a round cloud of total charge $q$ creates the same potential as a point charge $q$ at its centre.

**The dielectric constant.** Put two ions in water instead of in vacuum. Water molecules are small dipoles (next section). Around a positive ion they turn their negative side towards it, and around a negative ion their positive side. These turned molecules create a field of their own that opposes the field of the ion.

From a distance each ion therefore looks as if it carried a smaller charge. At distances that are large compared with a water molecule, the result is Coulomb's law divided by a number.

$$
U(r) = \frac{q_1q_2}{4\pi\varepsilon_0\varepsilon_r\,r} .
$$

<div class="legend" markdown="1">
- $\varepsilon_r$: the **dielectric constant** (relative permittivity) of the medium, a pure number. It is 1 in vacuum, about 2 in a non-polar liquid such as an oil, and about 78 in water at 25 °C (78.4 to three digits, the value used in the arithmetic below; some lessons round it to 80).
- Other symbols: as in the first list of this section.
</div>

The dielectric constant is a property of the bulk liquid, an average over very many molecules. It describes charges that are several molecular diameters apart. It is not accurate for two ions in contact, and it has no single value inside a protein. In a simulation with explicit water the formula is used with $\varepsilon_r = 1$, because the water molecules are present and do the screening themselves ([Module 5](05-force-field-form.html)). A dielectric constant larger than 1 appears when the water is simplified or left out ([Module 15](15-coarse-grained.html)), and in the reaction-field method for the liquid beyond the cutoff ([Module 7](07-boundaries-electrostatics.html)).

**A single charge in a dielectric.** A dielectric also lowers the energy of a single charge, because the molecules that have turned towards the charge are attracted to it. For an ion of charge $q$ and radius $R$ that is moved from vacuum into the medium, the free energy changes by $-\tfrac12\,q^2(1-1/\varepsilon_r)/(4\pi\varepsilon_0R)$. This is the Born formula of [Module 15](15-coarse-grained.html). For a unit charge of radius 0.2 nm in water it gives $-\tfrac12\times(138.935/0.2)\times(1-1/78.4) = -343$ kJ/mol, more than a hundred times $k_BT$. This is why charged groups stay in contact with water, and why burying one in the interior of a protein or a membrane costs so much.

A useful length follows from comparing Coulomb's law with the thermal energy. The **Bjerrum length** is the distance at which two unit charges have an interaction energy of exactly $k_BT$.

$$
\ell_B = \frac{e^2}{4\pi\varepsilon_0\varepsilon_r\,k_BT} .
$$

<div class="legend" markdown="1">
- $\ell_B$: the Bjerrum length, in nm.
- $e^2/(4\pi\varepsilon_0)$: the Coulomb constant times one unit charge squared, 138.935 kJ mol$^{-1}$ nm.
- $\varepsilon_r$: the dielectric constant of the medium.
- $k_BT$: the thermal energy.
</div>

In vacuum at 300 K it is $138.935/2.494 = 55.7$ nm. In water at 25 °C, where $k_BT = 2.479$ kJ/mol, it is $138.935/(78.4\times2.479) = 0.71$ nm. Two unit charges in water that are farther apart than 0.7 nm interact with less than the thermal energy.

**Screening by salt.** Dissolved ions are free to move. Near a positive charge, negative ions are a little more common than average and positive ions a little rarer. This cloud of ions cancels the charge further, and beyond a certain distance almost completely. For weak interactions the result is Coulomb's law with an extra factor that decays exponentially.

$$
U(r) = \frac{q_1q_2}{4\pi\varepsilon_0\varepsilon_r\,r}\,e^{-r/\lambda_D}, \qquad \lambda_D \approx \frac{0.304}{\sqrt{I}}\ \text{nm} .
$$

<div class="legend" markdown="1">
- $\lambda_D$: the **Debye length**, the distance over which the cloud of ions screens a charge.
- $e^{-r/\lambda_D}$: an exponential decay. At $r = \lambda_D$ the interaction is down to 37 % of its value without salt, at $r = 3\lambda_D$ to 5 %. Here $e$ is the number 2.718, not the elementary charge.
- $I$: the **ionic strength** in mol per litre. For a salt such as NaCl it is equal to the salt concentration.
- 0.304: the value for water at 25 °C. [Module 15](15-coarse-grained.html) gives the full formula. For 0.15 M it quotes 0.79 nm. To three digits the value is 0.785 nm.
- Other symbols: as in the lists above.
</div>

| Ionic strength | Debye length |
|---|---|
| 1 M | 0.30 nm |
| 0.15 M (about the salt concentration in the body) | 0.785 nm |
| 0.01 M | 3.0 nm |
| 0.001 M | 9.6 nm |

<div class="box key" markdown="1">
**Worked example: vacuum against water.** A charge of $+1\,e$ and a charge of $-1\,e$ are 0.3 nm apart. In vacuum, $U = 138.935\times(+1)\times(-1)/0.3 = -463$ kJ/mol, which is $-186\ k_BT$ at 300 K. With the dielectric constant of water, $-463/78 = -5.9$ kJ/mol, or $-2.4\ k_BT$. (At contact the second number is only a rough estimate, as explained above.) Water turns an interaction that nothing thermal could break into one that breaks all the time.

The force between the two charges in vacuum has the size $138.935/0.3^2 = 1{,}544$ kJ mol$^{-1}$ nm$^{-1}$, which is $1{,}544\times1.6605 \approx 2{,}560$ pN. The potential 0.3 nm from the positive charge is $138.935/0.3 = 463$ kJ mol$^{-1}$ $e^{-1}$, which is $463/96.485 = 4.8$ V.

**Worked example: salt.** Two charges of $+1\,e$ are 1 nm apart in water at 25 °C with 0.15 M salt. Without salt, $U = 138.935/(78.4\times1) = 1.77$ kJ/mol. The Debye length is $0.304/\sqrt{0.15} = 0.785$ nm, and the factor is $e^{-1/0.785} = 0.28$. So $U = 1.77\times0.28 = 0.50$ kJ/mol, one fifth of $k_BT$.
</div>

**Where the course uses it.**

- [Module 5](05-force-field-form.html), The form of a force field: the Coulomb term, and why it contains no dielectric constant.
- [Module 6](06-force-field-parameters.html), Force-field parameters: charges are chosen to reproduce the electrostatic potential around a molecule.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: why the Coulomb energy cannot be cut off, and the Ewald sum that treats it correctly.
- [Module 10](10-running-a-simulation.html), Running a simulation: ions are added to make the box neutral.
- [Module 15](15-coarse-grained.html), Coarse-grained models: screened Coulomb interactions and other models that replace the water by a dielectric constant.

<div class="box warn" markdown="1">
**A common mistake.** Dividing the Coulomb energy by 78 in a simulation that contains explicit water. That counts the screening twice. A second mistake is to conclude from screening that electrostatics is short-ranged and can be cut off. Screening is produced by all the other charges as they respond, and they can only produce it if their own interactions are computed at full range.
</div>

## Dipoles and polarisation {#dipoles}

Atoms of different elements pull on the electrons they share with different strength. In a water molecule the oxygen pulls harder than the hydrogens. The oxygen side of the molecule is therefore slightly negative and the hydrogen side slightly positive, although the molecule as a whole is neutral. A molecule with a positive and a negative side is a **dipole**, and such a molecule is called **polar** (a molecule without such sides, for example a hydrocarbon, is **non-polar**). A force field represents this uneven distribution by giving each atom a **partial charge**, a fraction of $e$, usually placed at its nucleus.

The **dipole moment** measures how much charge is separated and how far.

$$
\boldsymbol\mu = \sum_i q_i\,\mathbf r_i .
$$

<div class="legend" markdown="1">
- $\boldsymbol\mu$ (Greek mu, bold): the dipole moment of the molecule, a vector. It points from the negative side to the positive side.
- $q_i$, $\mathbf r_i$: the partial charge and the position of atom $i$.
- $\sum_i$: a sum over the atoms of the molecule.
- Unit: $e$ nm, or the debye (D). 1 D is 0.02082 $e$ nm, and 1 $e$ nm is 48.03 D.
</div>

The simplest case is two charges $+q$ and $-q$ a distance $d$ apart. Then the size of the dipole moment is $\mu = q\,d$. One elementary charge separated by 0.1 nm gives 0.1 $e$ nm, which is 4.8 D. For a neutral molecule the dipole moment does not depend on where you put the origin, because shifting all positions by the same vector adds that vector times the total charge, which is zero.

An electric field turns a dipole. The energy of a dipole in a field is

$$
U = -\boldsymbol\mu\cdot\mathbf E = -\mu\,E\cos\theta .
$$

<div class="legend" markdown="1">
- $\boldsymbol\mu\cdot\mathbf E$: the [dot product](maths.html#dot-product) of the dipole moment and the electric field.
- $\mu$, $E$: the sizes of the two vectors. Here $E$ is the size of the field, not an energy.
- $\theta$ (Greek theta): the angle between the dipole and the field.
- The energy is lowest when the dipole points along the field ($\theta = 0$) and highest when it points against it.
</div>

A field therefore lines dipoles up, and thermal motion works against this. The result is a partial alignment, and this is how water screens charges (see [the dielectric constant](#electrostatics)).

Seen from far away, the two sides of a dipole almost cancel. Its interactions therefore fall off faster with distance than those of a net charge.

| Pair | Energy falls off as | Reason |
|---|---|---|
| charge and charge | $1/r$ | Coulomb's law |
| charge and dipole | $1/r^2$ | the two sides of the dipole nearly cancel |
| dipole and dipole, in fixed orientations | $1/r^3$ | the cancellation happens on both sides |

You can check the middle row by adding up Coulomb's law for the single charges. Put a charge of $+1\,e$ at the origin, and build a dipole from $-0.5\,e$ and $+0.5\,e$ that are 0.1 nm apart, with its centre at a distance $r$ and its negative end towards the charge. At $r = 0.3$ nm the energy is $138.935\times(-0.5/0.25 + 0.5/0.35) = -79.4$ kJ/mol. At $r = 0.6$ nm it is $138.935\times(-0.5/0.55 + 0.5/0.65) = -19.4$ kJ/mol. Twice the distance leaves about a quarter of the energy, where two net charges would keep one half.

**Polarisation.** The charges in a molecule are not rigidly fixed. An electric field pushes the electron cloud one way and the nuclei the other way. This creates an additional dipole, the **induced dipole**, which lasts as long as the field does.

$$
\boldsymbol\mu_{ind} = \alpha\,\mathbf E .
$$

<div class="legend" markdown="1">
- $\boldsymbol\mu_{ind}$: the induced dipole moment.
- $\alpha$ (Greek alpha): the **polarisability** of the molecule. It says how easily its electron cloud is shifted.
- $\mathbf E$: the electric field at the molecule.
- Tables usually list the polarisability volume $\alpha' = \alpha/(4\pi\varepsilon_0)$, in nm$^3$ or Å$^3$. It is of the order of 0.001 nm$^3$ (1 Å$^3$) for a small molecule and grows with the size of the molecule.
</div>

The induced dipole lowers the energy by $\tfrac12\alpha E^2$. A liquid thus responds to a field in two ways. Its molecules turn, which takes time, and their electron clouds shift, which is immediate.

A force field with fixed partial charges contains the first response, because the molecules in the simulation can turn. It does not contain the second, because the charges never change ([Module 5](05-force-field-form.html)). Polarisable force fields add it ([Module 6](06-force-field-parameters.html)).

<div class="box key" markdown="1">
**Worked example: the dipole moment of a water-like molecule.** Take a charge of $-0.8\,e$ on the oxygen and $+0.4\,e$ on each hydrogen, O-H distances of 0.1 nm and an H-O-H angle of 104.5° (round values for an illustration). Put the oxygen at the origin, so that it contributes nothing to the sum. Each hydrogen lies $0.1\times\cos(52.25^\circ) = 0.0612$ nm along the axis of symmetry (52.25° is half of the angle), and the sideways parts of the two hydrogens cancel. So $\mu = 2\times0.4\times0.0612 = 0.0490$ $e$ nm, which is $0.0490/0.02082 = 2.35$ D. Module 5 lists the dipole moments of real water models.

**Worked example: an induced dipole.** A molecule with $\alpha' = 0.0015$ nm$^3$ (an illustration) is 0.3 nm from a charge of $+1\,e$. The field of a point charge is $E = q/(4\pi\varepsilon_0r^2)$ and $\alpha = 4\pi\varepsilon_0\alpha'$, so the factors $4\pi\varepsilon_0$ cancel and the formula above becomes $\mu_{ind} = \alpha'q/r^2 = 0.0015\times1/0.3^2 = 0.0167$ $e$ nm, which is 0.80 D, a third of the permanent dipole in the first example. The energy gained is $\tfrac12\alpha E^2$, which in these units is $\tfrac12\times138.935\times\alpha'q^2/r^4 = \tfrac12\times138.935\times0.0015/0.3^4 = 12.9$ kJ/mol. Close to an ion, polarisation is not a small effect.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the dielectric constant of a liquid from the fluctuations of its total dipole moment.
- [Module 5](05-force-field-form.html), The form of a force field: partial charges, and the missing response of the electron clouds.
- [Module 6](06-force-field-parameters.html), Force-field parameters: how partial charges are chosen, and polarisable force fields.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the reaction-field method, which treats the liquid beyond the cutoff as a medium that can be polarised.

<div class="box warn" markdown="1">
**A common mistake.** Thinking that a neutral molecule has no electrostatic interactions. Water is neutral, and its interactions are mostly electrostatic. A second point: partial charges are parameters of a model and cannot be measured. Different sets of charges can describe the same molecule almost equally well. What can be measured or computed without ambiguity is the dipole moment and the electrostatic potential around the molecule.
</div>

## Why atoms can be treated as classical balls {#quantum}

An atom is a small, heavy nucleus with light electrons around it. Electrons do not behave like tiny balls. They obey quantum mechanics: each electron is spread out as a cloud, and chemistry (bonds, lone pairs, partial charges) is the shape and the energy of these clouds.

The exact equation for all the electrons and nuclei of a protein in water is far beyond any computer. MD gets round it in three steps. Each step is an approximation, and it is worth knowing what each one gives up. ([Module 1](01-what-is-md.html) counts steps 1 and 2 together as its first approximation, and step 3 as its second.)

**Step 1: separate the electrons from the nuclei.** A proton is 1,836 times heavier than an electron, and other nuclei are heavier still. The electrons therefore move much faster than the nuclei and rearrange almost instantly when the nuclei move. Picture slow lorries (the nuclei) with a swarm of flies (the electrons) around them: wherever the lorries are, the swarm has already adapted.

So for each arrangement of the nuclei the electrons have one definite lowest energy. That energy, as a function of the positions of all nuclei, is the potential energy $U(\mathbf r)$ in which the nuclei move. This is the **Born-Oppenheimer approximation**.

**Step 2: replace the electronic energy by a formula.** Computing the energy of the electrons for one arrangement of the nuclei is the business of quantum chemistry, and it is far too slow to repeat at every step for a hundred thousand atoms. A **force field** is a cheap formula with fitted parameters that imitates $U(\mathbf r)$: springs for bonds and angles, periodic terms for rotations about bonds, a Lennard-Jones term, and Coulomb's law between partial charges ([Module 5](05-force-field-form.html)). The electrons no longer appear. Their effect is stored in the parameters.

**Step 3: move the nuclei with Newton's law.** Nuclei are quantum objects too, but they are much heavier than electrons. Two tests say whether the classical description is good enough. The first compares the quantum blur of a particle with the distances that matter.

$$
\Lambda = \frac{h}{\sqrt{2\pi m k_BT}} .
$$

<div class="legend" markdown="1">
- $\Lambda$ (Greek capital lambda): the **thermal de Broglie wavelength**, the size of the quantum blur in the position of a particle at temperature $T$.
- $h$: Planck's constant, $6.62607\times10^{-34}$ J s, or 0.399031 kJ mol$^{-1}$ ps. It sets the scale of all quantum effects.
- $m$: the mass of the particle.
- $k_BT$: the thermal energy.
</div>

A particle behaves classically when $\Lambda$ is small compared with the distances over which the forces on it change. Between atoms these distances are 0.1 to 0.4 nm.

| Particle | Mass | $\Lambda$ at 300 K |
|---|---|---|
| Electron | 0.00055 u | 4.3 nm |
| Hydrogen | 1.008 u | 0.10 nm |
| Carbon | 12.011 u | 0.029 nm |
| Oxygen | 15.999 u | 0.025 nm |

The blur of an electron is many times larger than an atom, so electrons are never classical. Carbon and oxygen are safely classical. Hydrogen is a borderline case.

The second test looks at vibrations. A quantum oscillator cannot have any energy it likes. Its energy comes in steps.

$$
E_n = \left(n + \tfrac12\right)\hbar\omega, \qquad n = 0, 1, 2, \dots
$$

<div class="legend" markdown="1">
- $E_n$: the allowed energies of a quantum harmonic oscillator.
- $n$: the number of the level. $n = 0$ is the lowest.
- $\hbar$ ("h-bar"): Planck's constant divided by $2\pi$, 0.0635078 kJ mol$^{-1}$ ps.
- $\omega$: the angular frequency of the [oscillator](#oscillator), in ps$^{-1}$.
- $\hbar\omega$: the distance between two neighbouring levels, the **vibrational quantum**.
- $\tfrac12\hbar\omega$: the **zero-point energy**, which remains even in the lowest level. A quantum oscillator is never completely at rest.
</div>

Compare $\hbar\omega$ with $k_BT$. If $\hbar\omega$ is much smaller than $k_BT$, the steps are tiny on the thermal scale, the energy looks continuous, and the classical description is good. If $\hbar\omega$ is much larger than $k_BT$, the oscillator sits in its lowest level and cannot take up or give off thermal energy. A classical spring with the same frequency would hold $k_BT$ of energy and exchange it freely, which is wrong.

<div class="box key" markdown="1">
**Worked example: a stiff and a soft vibration.** The C-H stretch of Module 2 has $\omega = 551$ ps$^{-1}$. Its quantum is $\hbar\omega = 0.0635\times551 = 35.0$ kJ/mol, which is $35.0/2.494 = 14\ k_BT$ at 300 K. The first excited level is populated $e^{-14} = 8\times10^{-7}$ times as often as the lowest one. This vibration is frozen in its lowest level, which is one reason why bonds to hydrogen can be replaced by rigid constraints ([Module 9](09-constraints.html)).

The soft spring in the section on [the harmonic oscillator](#oscillator) had $\omega = 2.89$ ps$^{-1}$. Its quantum is $0.0635\times2.89 = 0.18$ kJ/mol, or $0.07\ k_BT$. Slow, soft motions are classical.

**Worked example: the thermal wavelength of hydrogen.** In SI units, $m = 1.008\times1.66054\times10^{-27} = 1.6738\times10^{-27}$ kg and $k_BT = 1.380649\times10^{-23}\times300 = 4.1419\times10^{-21}$ J. Then $2\pi mk_BT = 4.356\times10^{-47}$, its square root is $6.600\times10^{-24}$, and $\Lambda = 6.626\times10^{-34}/(6.600\times10^{-24}) = 1.00\times10^{-10}$ m, which is 0.10 nm.
</div>

**Where the classical picture fails.**

- **Chemical reactions.** When a bond breaks or forms, the electrons rearrange. An ordinary force field has a fixed list of bonds.
- **Excited electrons.** Absorption of light, fluorescence and photochemistry need electrons in states other than the lowest one.
- **Transfer of protons and electrons.** Light particles can also pass through a barrier that they do not have the energy to climb. This is called tunnelling.
- **Stiff vibrations.** Their zero-point energy and their failure to take up heat are missing from a classical simulation.
- **The response of the electron clouds** to their surroundings, unless the force field includes polarisation (see [Dipoles and polarisation](#dipoles)).

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: which physics MD keeps and which it drops.
- [Module 5](05-force-field-form.html), The form of a force field: the formula that replaces the energy of the electrons.
- [Module 6](06-force-field-parameters.html), Force-field parameters: parameters fitted to quantum-chemical calculations and to experiments.
- [Module 9](09-constraints.html), Constraints: freezing the bonds to hydrogen.
- [Module 17](17-machine-learning.html), Machine-learned potentials: a learned replacement for the energy of the electrons, trained on quantum-chemical calculations.

<div class="box warn" markdown="1">
**A common mistake.** Saying that classical MD "contains no quantum mechanics". The quantum behaviour of the electrons is what creates $U(\mathbf r)$, and the force field carries it in its parameters. What is classical is the motion of the nuclei. The opposite mistake is to expect an ordinary simulation to show a reaction, a change of protonation or a shift of charge. The formula has no way to produce them.
</div>

## Forces between molecules {#intermolecular}

The atoms inside a molecule are held together by covalent bonds, and these do not break in an MD simulation. Everything else is decided by the much weaker forces between atoms that are not bonded to each other: why water is a liquid, why a protein folds, why a drug stays on its target. There are only a few kinds. All of them have an electric origin, and a force field describes them with two formulas, the Lennard-Jones function and Coulomb's law.

**Repulsion.** Push two atoms together and their electron clouds begin to overlap. Quantum mechanics does not allow two electrons to be in the same state in the same place (the Pauli principle), so the energy rises very steeply. This is what gives an atom its size and what makes matter hard to compress.

**Dispersion.** Two atoms attract each other weakly even when neither has a charge or a dipole. The electron cloud of an atom fluctuates, so at any instant it is slightly lopsided: the atom has a momentary dipole. The field of that dipole polarises the neighbouring atom (see [Dipoles and polarisation](#dipoles)), and the two dipoles attract. The energy of this attraction falls off as $1/r^6$. It acts between all atoms and is stronger for atoms with more electrons.

The dispersion attraction is also called the London force or the van der Waals attraction. The Lennard-Jones function combines repulsion and dispersion, and the term it forms in a force field is often called the van der Waals term.

$$
U_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right].
$$

<div class="legend" markdown="1">
- $U_{LJ}$: the Lennard-Jones energy of one pair of atoms, in kJ/mol. It is zero when the atoms are far apart.
- 4: a number chosen so that the depth of the well is exactly $\varepsilon$.
- $r$: the distance between the two atoms, in nm.
- $\varepsilon$ (Greek epsilon, without a subscript): the depth of the energy well, in kJ/mol. It is not the permittivity $\varepsilon_0$ of electrostatics.
- $\sigma$ (Greek sigma): the distance at which the energy is zero, roughly the diameter of an atom.
- $(\sigma/r)^{12}$: the repulsion, a conveniently steep function.
- $-(\sigma/r)^{6}$: the dispersion attraction.
</div>

The curve is very high at short distance, crosses zero at $r = \sigma$, has its minimum of depth $-\varepsilon$ at $r = 2^{1/6}\sigma = 1.12\,\sigma$, and rises back towards zero at large distance ([Module 5](05-force-field-form.html)).

**Electrostatic forces.** Charges and partial charges interact through Coulomb's law. This one formula covers the interactions between ions, between an ion and a polar molecule, and between two polar molecules (see [Charge and Coulomb's law](#electrostatics) and [Dipoles and polarisation](#dipoles)).

**The hydrogen bond.** A hydrogen bound to a nitrogen or an oxygen carries a positive partial charge. Because a hydrogen atom is small, a negatively charged oxygen or nitrogen of another group can come very close to it. The result is a strong attraction with a preferred direction, the hydrogen bond. It is strongest when the three atoms (the atom that carries the hydrogen, the hydrogen, and the atom that accepts it) lie nearly on a line. It is mostly electrostatic.

For two water molecules in the gas phase a hydrogen bond is worth about 20 kJ/mol, which is 8 $k_BT$ at 300 K. In liquid water the balance is different: a group that loses one hydrogen bond usually finds another partner, so the net free-energy changes are much smaller. A force field has no separate term for hydrogen bonds. They arise from the Coulomb and Lennard-Jones terms ([Module 5](05-force-field-form.html)).

**The hydrophobic effect.** Oil and water do not mix. The reason is not a strong attraction between oil molecules: the dispersion attraction between oil and water is about as strong as between oil and oil. The reason lies in the water.

Water molecules form hydrogen bonds with each other, and a non-polar molecule cannot take part. The water around it keeps its hydrogen bonds by arranging itself around the intruder, but it has fewer ways of doing so, and its entropy falls (see [Heat, entropy and free energy](#thermodynamics)). This is the picture for small non-polar molecules at room temperature.

When two non-polar groups come together, the surface that they show to the water shrinks, some water is released, and the free energy falls. This looks like an attraction between the two groups. It is a free-energy effect of the solvent, so you will not find it as a term in the potential energy function. It appears by itself in a simulation with explicit water. Models without water molecules must add it by hand ([Module 15](15-coarse-grained.html)).

| Interaction | Origin | Falls off as | Typical size | In a force field |
|---|---|---|---|---|
| Repulsion | overlap of electron clouds | very steeply | sets the size of atoms | Lennard-Jones, first term |
| Dispersion | fluctuating electron clouds | $1/r^6$ | 0.1 to 1 kJ/mol for one pair of atoms | Lennard-Jones, second term |
| Charge with charge | Coulomb's law | $1/r$ | hundreds of kJ/mol in vacuum at contact | Coulomb term |
| Charge with dipole, dipole with dipole | Coulomb's law between partial charges | $1/r^2$, $1/r^3$ | tens of kJ/mol at contact | Coulomb term |
| Hydrogen bond | mostly electrostatic | short-ranged, directional | about 20 kJ/mol in the gas phase | Coulomb and Lennard-Jones terms together |
| Hydrophobic effect | hydrogen bonds between water molecules | | grows with the non-polar surface | none: it comes from the explicit water |

<div class="box key" markdown="1">
**Worked example: the Lennard-Jones energy at five distances.** Take $\varepsilon = 0.5$ kJ/mol and $\sigma = 0.34$ nm (round values for an illustration).

| $r$ in nm | $(\sigma/r)^{12}$ | $(\sigma/r)^{6}$ | $U_{LJ}$ in kJ/mol |
|---|---|---|---|
| 0.30 | 4.490 | 2.119 | $+4.74$ |
| 0.34 | 1 | 1 | 0 |
| 0.3816 (the minimum, $2^{1/6}\sigma$) | 0.250 | 0.500 | $-0.50$ |
| 0.50 | 0.0098 | 0.0989 | $-0.178$ |
| 1.00 | $2.4\times10^{-6}$ | 0.0015 | $-0.0031$ |

First row: $4\times0.5\times(4.490 - 2.119) = 4.74$ kJ/mol. Moving the atoms 0.04 nm closer than $\sigma$ already costs 1.9 $k_BT$, so atoms rarely come closer than that. The minimum, at $r = 2^{1/6}\times0.34 = 0.382$ nm, is only 0.2 $k_BT$ deep: one contact is weak. At 1 nm one pair contributes 0.6 % of the well depth, but the number of pairs at that distance is large, which is why the cutoff needs a correction ([Module 7](07-boundaries-electrostatics.html)).

**Worked example: three sizes on the thermal scale.** At 300 K: one dispersion contact of 0.5 kJ/mol is 0.2 $k_BT$. One hydrogen bond between two water molecules in the gas phase, 20 kJ/mol, is 8 $k_BT$. Two opposite unit charges 0.3 nm apart in vacuum, 463 kJ/mol, are 186 $k_BT$.
</div>

**Where the course uses it.**

- [Module 5](05-force-field-form.html), The form of a force field: the Lennard-Jones and Coulomb terms, and the absence of a hydrogen-bond term.
- [Module 6](06-force-field-parameters.html), Force-field parameters: how the strengths of these interactions are fitted, and the balance between protein-water and protein-protein attraction.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: where the short-range interactions can be cut off.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: softening the repulsive wall when atoms are made to appear or disappear.
- [Module 15](15-coarse-grained.html), Coarse-grained models: effective interactions that include the effect of the water.

<div class="box warn" markdown="1">
**A common mistake.** Looking for the hydrogen bond or the hydrophobic effect as a term of the energy function. Neither is there. Both emerge from the terms that are. A second mistake is to dismiss dispersion because one contact is only a fraction of $k_BT$. A side chain buried in a protein has dozens of such contacts, and their sum is not small.
</div>

## Diffusion, friction and viscosity {#diffusion}

A molecule in a liquid is surrounded by neighbours that hit it from all sides, many times in each picosecond. Every hit changes its direction. Its path is a **random walk**, like that of a person who takes each step in a new random direction.

After many steps the walker has on average gone nowhere, because steps to the left and to the right cancel. But the typical distance from the starting point keeps growing, slowly. This spreading is **diffusion**.

$$
\left\langle \vert\mathbf r(t) - \mathbf r(0)\vert^2 \right\rangle = 6\,D\,t .
$$

<div class="legend" markdown="1">
- $\mathbf r(0)$, $\mathbf r(t)$: the position of the molecule at the start and after a time $t$.
- $\vert\ \ \vert^2$: the squared length of the vector, here the squared distance travelled.
- $\langle\ \rangle$: the average over many molecules or over many starting times. The left side is called the **mean squared displacement** (MSD).
- $D$: the **diffusion constant**, in nm$^2$/ps. One nm$^2$/ps is $10^{-6}$ m$^2$/s, or 0.01 cm$^2$/s.
- 6: two for each of the three directions. Along one direction alone, $\langle(\Delta x)^2\rangle = 2Dt$.
</div>

Read it like this. The *squared* distance grows in proportion to the time, so the distance grows with the square root of the time. Four times the time gives twice the distance, and to go ten times farther takes a hundred times longer. Diffusion is fast over the size of a molecule and slow over large distances.

The formula holds for times that are long compared with the time between two collisions. Over a small fraction of a picosecond a molecule still flies straight, and the squared distance grows with the square of the time. This early part is called ballistic.

**Friction.** Drag an object through a liquid and the liquid resists. For slow motion the resisting force is proportional to the velocity.

$$
\mathbf F_{drag} = -\zeta\,\mathbf v, \qquad D = \frac{k_BT}{\zeta} .
$$

<div class="legend" markdown="1">
- $\mathbf F_{drag}$: the friction force. The minus sign says that it points against the velocity.
- $\zeta$ (Greek zeta): the **friction coefficient**, in u/ps.
- $\mathbf v$: the velocity of the object through the liquid.
- $D$: the diffusion constant of the same object.
- $k_BT$: the thermal energy.
</div>

The second formula is the **Einstein relation**. The collisions that slow down a moving molecule are the same collisions that kick a resting molecule around. Friction and diffusion are therefore two sides of one thing: strong friction means slow diffusion. In a Langevin thermostat the friction is given as a rate $\gamma = \zeta/m$, in ps$^{-1}$, where $m$ is the mass of the atom ([Module 8](08-thermostats-barostats.html)). Then $D = k_BT/(m\gamma)$.

**Viscosity.** The property of the liquid that sets the friction is its **viscosity**: how strongly it resists flowing. Honey has a high viscosity, water a low one. For a sphere that is much larger than the molecules of the liquid:

$$
\zeta = 6\pi\eta R, \qquad D = \frac{k_BT}{6\pi\eta R} .
$$

<div class="legend" markdown="1">
- $\eta$ (Greek eta): the viscosity of the liquid. For water at 25 °C it is $0.89\times10^{-3}$ Pa s.
- $R$: the radius of the sphere.
- $6\pi$: a number that comes from the flow of the liquid around a sphere.
- The second formula is the **Stokes-Einstein relation**. It follows from putting the first formula into the Einstein relation.
</div>

Read it like this. A larger particle diffuses more slowly, and so does any particle in a more viscous liquid. For a protein the formula works well. For a molecule as small as the solvent it gives only a rough estimate.

<div class="box key" markdown="1">
**Worked example: how far does a water molecule get?** The measured diffusion constant of water at 25 °C is $2.3\times10^{-9}$ m$^2$/s, which is $2.3\times10^{-3}$ nm$^2$/ps. The typical distance after a time $t$ is $\sqrt{6Dt}$.

- After 1 ps: $\sqrt{6\times0.0023\times1} = 0.12$ nm, less than the diameter of the molecule.
- After 1 ns: $\sqrt{6\times0.0023\times1000} = 3.7$ nm.
- After 100 ns: $\sqrt{6\times0.0023\times10^5} = 37$ nm. A hundred times the time, ten times the distance.

**Worked example: a protein.** Treat a protein as a sphere of radius 2 nm in water at 25 °C. In SI units, $k_BT = 1.380649\times10^{-23}\times298.15 = 4.116\times10^{-21}$ J and $6\pi\eta R = 6\pi\times0.89\times10^{-3}\times2\times10^{-9} = 3.355\times10^{-11}$ kg/s. So $D = 4.116\times10^{-21}/(3.355\times10^{-11}) = 1.23\times10^{-10}$ m$^2$/s, which is $1.23\times10^{-4}$ nm$^2$/ps, 19 times slower than water.

To move by its own diameter, 4 nm, the protein needs $t = 4^2/(6\times1.23\times10^{-4}) = 21{,}700$ ps, about 22 ns. To cross a cell of 10 µm ($10^4$ nm) it needs $(10^4)^2/(6\times1.23\times10^{-4}) = 1.4\times10^{11}$ ps, which is 0.14 s.
</div>

**Where the course uses it.**

- [Module 4](04-integrators.html), Integrators: integrators for equations of motion that contain friction and random forces.
- [Module 6](06-force-field-parameters.html), Force-field parameters: water models differ in their diffusion constant and viscosity, and this changes the speed of everything dissolved in them.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: the Langevin thermostat, which adds friction and random kicks.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the diffusion constant from the mean squared displacement in a trajectory.
- [Module 15](15-coarse-grained.html), Coarse-grained models: without explicit water the friction must be chosen, and it sets the time scale.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: crossing a barrier against friction.

<div class="box warn" markdown="1">
**A common mistake.** Reading the diffusion constant from the first picosecond of the mean squared displacement, where the motion is still ballistic. Fit the straight part at longer times. A second mistake is to compute displacements from coordinates that have been wrapped back into the periodic box, which makes molecules appear to jump ([Module 11](11-analysis-statistics.html)). A note on vocabulary: the "diffusion models" of Modules 17 and 18 are machine-learning methods that borrow the mathematics of random walks. They do not simulate the diffusion of molecules.
</div>

## Time and length scales of molecules {#time-scales}

A simulation advances in steps of a few femtoseconds. The processes that a biologist cares about take from nanoseconds to seconds. Whether MD can answer a question depends first of all on where the process sits between these two ends. This section is a map of the sizes and the times.

**Prefixes.**

| Prefix | Factor | As a time | Number of 2 fs steps |
|---|---|---|---|
| milli (m) | $10^{-3}$ | 1 ms | $5\times10^{11}$ |
| micro (µ) | $10^{-6}$ | 1 µs | $5\times10^{8}$ |
| nano (n) | $10^{-9}$ | 1 ns | $5\times10^{5}$ |
| pico (p) | $10^{-12}$ | 1 ps | 500 |
| femto (f) | $10^{-15}$ | 1 fs | half a step |

**Lengths.**

| Object | Size |
|---|---|
| C-H bond | 0.11 nm |
| C-C single bond | 0.15 nm |
| Hydrogen bond between two water molecules, O to O | 0.28 nm |
| Diameter of a water molecule | about 0.3 nm |
| Distance between neighbouring C$\alpha$ atoms in a protein | 0.38 nm |
| $\alpha$-helix | 0.15 nm along the axis for each residue, 0.54 nm for each turn |
| Debye length at 0.15 M salt | 0.8 nm |
| Usual cutoff for short-range interactions | about 1 nm |
| DNA double helix | 2 nm wide, 0.34 nm for each base pair |
| Small folded protein (about 100 residues) | 3 to 4 nm across |
| Lipid bilayer | about 4 nm thick |
| Simulation box for one protein in water | 5 to 15 nm along each edge |
| Ribosome | about 25 nm |

**Times.** The table is the one of [Module 1](01-what-is-md.html).

| Process | Typical time | Steps at 2 fs |
|---|---|---|
| Bond stretch (C-H) | 10 fs | 5 |
| Water reorientation, hydrogen-bond lifetime | 1 to 10 ps | $5\times10^2$ to $5\times10^3$ |
| Side-chain rotamer flips at the surface | 10 ps to 1 ns | $5\times10^3$ to $5\times10^5$ |
| Loop motions, helix formation | 1 ns to 1 µs | $5\times10^5$ to $5\times10^8$ |
| Fast protein folding, small-ligand binding | 1 µs to 1 ms | $5\times10^8$ to $5\times10^{11}$ |
| Unbinding of a nanomolar complex | seconds to hours | $5\times10^{14}$ or more |

**Why the gap is so wide.** There are two reasons. The first is that the time step is tied to the fastest motion in the system. A bond vibration has a period of about 10 fs (see [The harmonic oscillator](#oscillator)), and the step must be several times shorter, however slow the process you are interested in.

The second reason is that slow processes are slow because they must cross a free-energy barrier. The molecule moves about in one valley and runs against the barrier again and again. Only the rare attempts that happen to have enough energy get over it. The fraction of such attempts is a Boltzmann factor (see [Temperature and thermal energy](#temperature)).

$$
\text{rate} \approx \nu_0\,e^{-\Delta G^\ddagger/k_BT} .
$$

<div class="legend" markdown="1">
- rate: the number of crossings in each unit of time. Its inverse is the average waiting time for one crossing.
- $\nu_0$: the attempt frequency, the number of attempts in each unit of time. The examples below take one attempt per picosecond as an illustration. [Module 16](16-kinetics-msm.html) explains what sets it.
- $\Delta G^\ddagger$: the height of the free-energy barrier above the valley. The double dagger marks the top of a barrier.
- $k_BT$: the thermal energy.
</div>

Because the barrier sits in an exponent, the waiting time is extremely sensitive to it. At 300 K every additional 5.74 kJ/mol makes the process ten times slower.

<div class="box key" markdown="1">
**Worked example: barrier heights and waiting times.** With $\nu_0 = 10^{12}$ per second (one attempt per picosecond) and $T = 300$ K:

| Barrier | In $k_BT$ | Rate | Waiting time |
|---|---|---|---|
| 10 kJ/mol | 4 | $1.8\times10^{10}$ s$^{-1}$ | 55 ps |
| 30 kJ/mol | 12 | $6.0\times10^{6}$ s$^{-1}$ | 170 ns |
| 50 kJ/mol | 20 | $2.0\times10^{3}$ s$^{-1}$ | 0.5 ms |
| 70 kJ/mol | 28 | 0.65 s$^{-1}$ | 1.5 s |

First row: $10^{12}\times e^{-10/2.494} = 10^{12}\times0.0181 = 1.81\times10^{10}$ s$^{-1}$, and $1/(1.81\times10^{10}\ \text{s}^{-1}) = 5.5\times10^{-11}$ s, which is 55 ps. A barrier seven times higher gives a waiting time that is longer by a factor of $3\times10^{10}$.

**Worked example: how many steps, how many atoms?** One microsecond at 2 fs for each step is $10^{-6}/(2\times10^{-15}) = 5\times10^8$ steps. On a computer that produces 100 ns per day (an illustration) that takes 10 days.

Liquid water has 33.4 molecules per nm$^3$, about 100 atoms. A cubic box with an edge of 5 nm has a volume of 125 nm$^3$ and holds about 4,200 water molecules, 12,500 atoms. With an edge of 10 nm it holds 33,400 molecules, 100,000 atoms. Doubling the edge multiplies the number of atoms by eight.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: the same table, and what a step costs.
- [Module 4](04-integrators.html), Integrators: how long a time step can be.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: how large the box and the cutoff must be.
- [Module 9](09-constraints.html), Constraints: longer steps by freezing the fastest motions.
- [Module 10](10-running-a-simulation.html), Running a simulation: planning the length and the number of repeats.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: deciding whether a run was long enough.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: methods that make barrier crossings more frequent.
- [Module 15](15-coarse-grained.html), Coarse-grained models: larger systems and longer times by merging atoms.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: rates from simulations.

<div class="box warn" markdown="1">
**A common mistake.** Calling a run "long" because of its number of steps. A run of 500 ns is 250 million steps, and it is still shorter than a single event of a process that happens once in a microsecond. Compare the length of the run with the slowest process that matters for your question. And one observed transition is one event. It does not give a rate.
</div>

## Waves and frequencies {#waves}

Throw a stone into a pond and rings spread over the water. At one fixed place the surface goes up and down in time. At one fixed moment crests and troughs alternate in space. A **wave** is a pattern that repeats both in time and in space. Light, X-rays and sound are waves.

Waves matter for MD in two ways. The experiments that test a simulation, spectroscopy and scattering, are described in the language of waves. And in a periodic simulation box, any function that repeats with the box can be built as a sum of waves that fit into the box ([Fourier series](maths.html#fourier)).

$$
y(x,t) = y_{\max}\cos(kx - \omega t), \qquad k = \frac{2\pi}{\lambda}, \qquad \omega = \frac{2\pi}{T_{period}} = 2\pi\nu .
$$

<div class="legend" markdown="1">
- $y$: the quantity that oscillates. For the pond it is the height of the water. For light it is the electric field.
- $y_{\max}$: the amplitude, the largest value of $y$.
- $x$, $t$: the position along the direction of travel, and the time.
- $\lambda$ (Greek lambda): the **wavelength**, the distance from one crest to the next.
- $k$: the **wave number**, in radians per nm. It says how fast the wave repeats in space. Here $k$ is not a spring constant. In three dimensions it becomes a vector $\mathbf k$, the wave vector, that points in the direction of travel.
- $T_{period}$: the period, the time between two crests passing a fixed place.
- $\nu$ (Greek nu): the **frequency**, the number of crests that pass in each unit of time.
- $\omega$: the angular frequency, in radians per unit of time.
</div>

The wave number does for space what the angular frequency does for time. A crest is a place where $kx - \omega t = 0$, that is $x = (\omega/k)\,t$. So a crest travels at the speed

$$
v = \frac{\omega}{k} = \lambda\,\nu .
$$

<div class="legend" markdown="1">
- $v$ (Latin letter): the speed of the wave.
- $\omega$, $k$: its angular frequency and its wave number, as in the list above.
- $\lambda$, $\nu$ (Greek letters): its wavelength and its frequency.
- For light in vacuum the speed is always $c = 2.998\times10^{8}$ m/s, so a long wavelength means a low frequency.
</div>

**Spectroscopy.** A bond with partial charges on its two atoms is a small dipole, and when the bond vibrates the dipole oscillates. It absorbs light whose frequency matches its own. An infrared spectrum therefore shows the vibration frequencies of a molecule. Spectroscopists do not quote the frequency itself. They quote the **wavenumber** of the light.

$$
\tilde\nu = \frac{1}{\lambda} = \frac{\nu}{c}, \qquad E = h\nu = hc\,\tilde\nu .
$$

<div class="legend" markdown="1">
- $\tilde\nu$ ("nu tilde"): the wavenumber, the number of wavelengths that fit into one centimetre. Its unit is cm$^{-1}$.
- $\lambda$: the wavelength of the light, in cm in this formula.
- $c$: the speed of light, $2.998\times10^{10}$ cm/s.
- $E$: the energy of one quantum of light of this frequency (one photon).
- $h$: Planck's constant.
</div>

Three conversions follow. A vibration with wavenumber $\tilde\nu$ has the frequency $\nu = c\,\tilde\nu$. Its period in femtoseconds is 33,356 divided by the wavenumber in cm$^{-1}$. Its quantum of energy is 0.011963 kJ/mol times the wavenumber in cm$^{-1}$. On this scale the thermal energy at 300 K corresponds to 208.5 cm$^{-1}$.

| Wavenumber | Period | Quantum in $k_BT$ at 300 K | Example (typical value) |
|---|---|---|---|
| 3,000 cm$^{-1}$ | 11 fs | 14 | stretch of a C-H bond |
| 1,650 cm$^{-1}$ | 20 fs | 7.9 | C=O stretch of the peptide group |
| 200 cm$^{-1}$ | 170 fs | 0.96 | a soft vibration of low frequency |
| 1 cm$^{-1}$ | 33 ps | 0.005 | |

<div class="box key" markdown="1">
**Worked example: wavenumber, period and angular frequency.** A vibration at 3,000 cm$^{-1}$ has $\nu = 2.998\times10^{10}\times3000 = 8.99\times10^{13}$ s$^{-1}$, which is 89.9 ps$^{-1}$. The period is $1/89.9 = 0.0111$ ps, or 11.1 fs, and $\omega = 2\pi\times89.9 = 565$ ps$^{-1}$. The light that it absorbs has a wavelength of $1/3000$ cm, which is 3.33 µm, in the infrared. One quantum is $0.011963\times3000 = 35.9$ kJ/mol, or 14.4 $k_BT$ at 300 K.

The other way round: the C-H stretch of Module 2 has $\omega = 551$ ps$^{-1}$. Then $\nu = 551/2\pi = 87.7$ ps$^{-1}$, which is $8.77\times10^{13}$ s$^{-1}$, and $\tilde\nu = 8.77\times10^{13}/(2.998\times10^{10}) = 2{,}925$ cm$^{-1}$.

**Worked example: waves in a box.** In a cubic box with an edge of $L = 5$ nm, the waves that fit a whole number of times have the wavelengths $L$, $L/2$, $L/3$ and so on. Their wave numbers are $2\pi/5 = 1.26$ nm$^{-1}$ and its multiples. These are the wave vectors of "reciprocal space" in [Module 7](07-boundaries-electrostatics.html). A structure that repeats every 0.3 nm, such as neighbouring molecules in a liquid, corresponds to $k = 2\pi/0.3 = 21$ nm$^{-1}$.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: vibration frequencies in cm$^{-1}$ compared with the thermal energy.
- [Module 2](02-classical-mechanics.html), Classical mechanics: the frequencies of the normal modes of a molecule.
- [Module 4](04-integrators.html), Integrators: from the period of the fastest vibration to the time step.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the Ewald sum adds up waves in reciprocal space.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: comparing a simulation with scattering experiments.

<div class="box warn" markdown="1">
**A common mistake.** Mixing up the three ways of stating how fast something oscillates: the frequency $\nu$, the angular frequency $\omega = 2\pi\nu$, and the wavenumber $\tilde\nu = \nu/c$. Check the unit: a value in ps$^{-1}$ can be either of the first two, and cm$^{-1}$ is always the third. A related trap is that the spectroscopist's wavenumber, $1/\lambda$, has no factor $2\pi$, while the wave number $k = 2\pi/\lambda$ of this section has one.
</div>
