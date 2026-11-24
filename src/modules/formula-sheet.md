---
title: Formula sheet
short: Formula sheet
summary: The equations of the course on one page, with the module where each is derived.
---

This page collects the main equations of the course, grouped by topic, with the module where each one is derived. Under every block of formulas a list says in words what each formula computes and then what every letter in it stands for. Unless a list says otherwise, lengths are in nm, times in ps, masses in u (atomic mass units), energies in kJ/mol, charges in units of the elementary charge $e$ and temperatures in K. Lengths, times, masses and energies in these units fit together without conversion factors, because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$.

<div class="box warn" markdown="1">
**Letters that mean more than one thing on this page.** There are more quantities than letters, so the same letter is used again in another section with another meaning. The list under each block says which meaning applies there. The main cases:

| Letter | Meanings on this page |
|---|---|
| $\lambda$ | velocity scaling factor (Berendsen thermostat); Lagrange multiplier $\lambda_k$ (constraints); coupling parameter from 0 to 1 (thermodynamic integration); eigenvalue (Markov models, TICA); Debye length $\lambda_D$ |
| $\sigma$ | Lennard-Jones distance; constraint function $\sigma_k$; standard deviation ($\sigma_T$, and $\sigma$ in the formula for the standard error); native contact distance $\sigma_{ij}$ in a Gō model |
| $k$ | force constant ($k_b$, $k_\theta$, $k_n$, umbrella spring); wave vector $\mathbf k$ (Ewald); a counting label (constraints, states, lags); rate constant ($k_{on}$, $k_{off}$, $k_{TST}$). $k_B$ is always the Boltzmann constant |
| $g$ | radial distribution function $g(r)$; SHAKE correction $g$; statistical inefficiency $g_{stat}$ |
| $w$, $W$ | umbrella bias $w_i(\xi)$; hill height $w$ (metadynamics); loss weights $w_E$, $w_F$; importance weight $w(\mathbf x)$; potential of mean force $W(\xi)$; work $W$ (Jarzynski, Crooks) |
| $\gamma$ | friction rate (Langevin, Kramers); bias factor (metadynamics) |
| $\xi$ | collective variable; vector of random numbers $\boldsymbol\xi$ (O step, Brownian dynamics); thermostat variable (Nosé-Hoover) |
| $T$ | temperature; total simulated time $T_{sim}$; transition matrix $\mathbf T$ |
| $P$ | probability; pressure |
| $Q$ | partition function; thermostat "mass" (Nosé-Hoover) |
| $\rho$ | density of copies in phase space (Liouville); number density of particles |
| $\eta$ | random force $\boldsymbol\eta$ (Langevin); viscosity |
| $\varepsilon$ | Lennard-Jones well depth; contact energy (Gō model); permittivity of vacuum $\varepsilon_0$; dielectric constants $\varepsilon_r$, $\varepsilon_{in}$, $\varepsilon_{out}$ |
| $K$ | kinetic energy; force constant in AMBER and CHARMM files; equilibrium constants $K_a$, $K_d$ |
| $A$ | Helmholtz free energy; the name of a state (A and B) |
| $N$ | number of atoms; number of saved frames or samples |
| $F$ | force $\mathbf F$; free energy ($F_i$ of a window, $F(s)$ along a collective variable) |
| $C$ | count matrix $C_{ij}$; covariance matrix $\mathbf C(\tau)$; heat capacity $C_V$; standard concentration $C^\circ$ |
| $V$ | volume; metadynamics bias $V(s,t)$ |
| $M$ | number of replicas; mapping $\mathbf M(\mathbf r)$ from atoms to beads. An upright M in a unit, as in M$^{-1}$ s$^{-1}$, is mol/L |
| $R$ | bead coordinates $\mathbf R$; Born radius $R_i$; gas constant in $RT\ln10$ |
| $i$ | a label for atoms, windows or states; the imaginary unit in $iL$ and in $e^{i\mathbf k\cdot\mathbf r_j}$ |
| $L$ | box edge length; Liouville operator $iL$; loss $\mathcal L$ |
| $\theta$ | bond angle; the parameters of a neural network |
| $\delta$ | deviation from the mean ($\delta E$, $\delta V$); phase $\delta_n$ of a torsion; Dirac delta function $\delta(\ )$ |
| $\tau$ | coupling time $\tau_T$; autocorrelation time $\tau_{int}$; lag time of a Markov model |
| $q$ | a generalised coordinate (Hamilton's equations); a charge $q_i$ |
| $s$ | collective variable (metadynamics); bond vectors $\mathbf s$, $\mathbf s'$ (SHAKE) |
| $n$ | multiplicity of a torsion term; shift $\mathbf n$ to a periodic copy and whole numbers $n_x$, $n_y$, $n_z$ (Ewald); number of particles in a shell $n(r,r+dr)$; counts $n_i(\xi)$ in a histogram bin (WHAM); the label of a sample (MBAR) |
| $u$ | energy of one pair $u(r)$ (pair force); atomistic potential energy $u(\mathbf r)$ (coarse-graining); reduced potential $u_i(\mathbf x)$ (MBAR). An upright u after a number is the atomic mass unit |
| $p$ | momentum ($\mathbf p_i$, $p$); probability density $p_X(\mathbf x)$ of a generator (machine learning) |
| $v$ | velocity $\mathbf v$; eigenvector $\mathbf v$ (TICA) |
| $S$ | structure factor $S(\mathbf k)$ (Ewald); the number of umbrella windows or states (WHAM, MBAR) |
| $e$ | the number 2.718, the base of the natural logarithm, in every exponential such as $e^{-\beta H}$; the elementary charge where it appears in a unit (kJ mol$^{-1}$ nm $e^{-2}$) |
</div>

## Constants and conversions

| Quantity | Value |
|---|---|
| $k_B$ | 0.0083145 kJ mol$^{-1}$ K$^{-1}$ = 0.0019872 kcal mol$^{-1}$ K$^{-1}$ |
| $k_BT$ at 300 K | 2.494 kJ/mol = 0.596 kcal/mol |
| $RT\ln10$ at 298 K | 5.71 kJ/mol = 1.36 kcal/mol |
| $1/(4\pi\varepsilon_0)$ | 138.935 kJ mol$^{-1}$ nm $e^{-2}$ |
| Standard volume $V^\circ=1/C^\circ$ | 1.661 nm$^3$ per molecule at 1 mol/L |
| Debye length in water at 25 °C | $0.304/\sqrt{I[\text{M}]}$ nm |
| Harmonic constant, AMBER/CHARMM to GROMACS | $k=2K$; kcal mol$^{-1}$ Å$^{-2}$ × 418.4 = kJ mol$^{-1}$ nm$^{-2}$ |

<div class="legend" markdown="1">
- $k_B$: the Boltzmann constant. It converts a temperature into an energy. This course counts energies per mole of molecules, so the value is per mole and is the same number as the gas constant $R$. It appears wherever a temperature does: in $k_BT$, in $\beta=1/k_BT$ and in the instantaneous temperature.
- $k_BT$ at 300 K: the thermal energy at room temperature ($T$ is the absolute temperature in K). It is the yardstick for every energy on this page: a barrier or a well depth is large or small compared with $k_BT$.
- $RT\ln10$ at 298 K: the free-energy difference that corresponds to a factor of 10 in a binding constant or in a ratio of two populations. $R$ is the gas constant (equal to $k_B$ in per-mole units) and $\ln10=2.303$. With $\Delta G^\circ=-k_BT\ln(K_aC^\circ)$, a binder that is 10 times tighter has a $\Delta G^\circ$ that is 5.71 kJ/mol more negative. This row is for 298 K, the row above for 300 K.
- $1/(4\pi\varepsilon_0)$: the Coulomb constant. $\varepsilon_0$ is the permittivity of vacuum. Multiply $q_iq_j/r$ by it, with the charges in units of $e$ and the distance in nm, to get a Coulomb energy in kJ/mol. It is used in the force field, in the Ewald sum and in the Debye-Hückel and generalised Born formulas.
- $C^\circ$ and $V^\circ$: $C^\circ$ is the standard concentration, 1 mol/L, which is 0.6022 molecules per nm$^3$. $V^\circ=1/C^\circ$ is the volume that one molecule has to itself at that concentration. The small circle marks the standard state. They turn an association constant in nm$^3$ into molar units and into $\Delta G^\circ$ (free-energy section).
- Debye length: the distance over which dissolved salt screens an electrostatic interaction, written $\lambda_D$ in the coarse-graining section. $I$ is the ionic strength of the solution (Module 15). For a salt of singly charged ions such as NaCl it equals the salt concentration. $I[\text{M}]$ means its value in mol/L, entered as a plain number. At 0.15 mol/L the Debye length is 0.79 nm.
- $k=2K$: two ways of writing the energy of a spring. GROMACS writes $\tfrac12k(x-x_0)^2$, and AMBER and CHARMM parameter files write $K(x-x_0)^2$ with no half, so $k=2K$. For a bond length, the factor 418.4 is 4.184 (kcal to kJ) times 100 (Å$^{-2}$ to nm$^{-2}$). For an angle constant in kcal mol$^{-1}$ rad$^{-2}$ only the 4.184 applies, because radians are not converted. Example: $K=310$ kcal mol$^{-1}$ Å$^{-2}$ becomes $k=2\times310\times418.4=259{,}408$ kJ mol$^{-1}$ nm$^{-2}$.
</div>

## Mechanics (Module 2)

$$
m_i\ddot{\mathbf r}_i=\mathbf F_i=-\nabla_iU\qquad
H=\sum_i\frac{\mathbf p_i^2}{2m_i}+U(\mathbf r)\qquad
\dot q=\frac{\partial H}{\partial p},\ \ \dot p=-\frac{\partial H}{\partial q}
$$

<div class="legend" markdown="1">
- First formula: Newton's second law with a conservative force. Mass times acceleration equals the force, and the force is minus the slope of the potential energy.
- Second formula: the Hamiltonian, which is the total energy (kinetic plus potential) written with momenta.
- Third formula (a pair of equations): Hamilton's equations, the same motion written as two first-order equations.
- $i$: the label of one atom, from 1 to $N$ (the number of atoms). $\sum_i$ means "add up over all atoms".
- $m_i$: the mass of atom $i$, in u.
- $\mathbf r_i$: the position of atom $i$, a vector $(x_i,y_i,z_i)$ in nm. $\mathbf r$ without a label means all positions together.
- $\ddot{\mathbf r}_i$: the acceleration of atom $i$. Each dot is one derivative with respect to time.
- $\mathbf F_i$: the total force on atom $i$, in kJ mol$^{-1}$ nm$^{-1}$.
- $U$: the potential energy, a function of all positions, in kJ/mol.
- $\nabla_i$: the gradient with respect to the position of atom $i$, that is the three slopes $(\partial/\partial x_i,\partial/\partial y_i,\partial/\partial z_i)$. The minus sign makes the force point towards lower energy.
- $H$: the Hamiltonian, in kJ/mol.
- $\mathbf p_i$: the momentum of atom $i$, equal to $m_i\dot{\mathbf r}_i$ (mass times velocity). $\mathbf p_i^2$ is short for $\mathbf p_i\cdot\mathbf p_i$, and $\mathbf p_i^2/2m_i$ is the kinetic energy of atom $i$.
- $q$, $p$: one coordinate and the momentum that belongs to it. There is one such pair of equations for every degree of freedom (Module 2 writes $q_k$, $p_k$). Here $q$ is not a charge and $p$ is not a probability.
- $\dot q$, $\dot p$: their rates of change in time.
- $\partial H/\partial p$, $\partial H/\partial q$: partial derivatives, the slope of $H$ when only that one variable changes.
</div>

$$
\text{Pair force: }\mathbf F_i=-\frac{du}{dr}\frac{\mathbf r_{ij}}{r_{ij}}\qquad
\text{Liouville: }\nabla_\Gamma\cdot\dot\Gamma=0,\ \ \frac{\partial\rho}{\partial t}=-\{\rho,H\}
$$

<div class="legend" markdown="1">
- Pair force: the force on atom $i$ from one other atom $j$ when the energy of the pair depends only on their distance. The total force on atom $i$ is the sum of this expression over all partners $j$. In Module 2 and in the virial equation of the next section the force from one partner is written $\mathbf F_{ij}$.
- Liouville, first formula: the flow of points in phase space is incompressible, so a cloud of starting conditions keeps its volume.
- Liouville, second formula: the Liouville equation, which says how a density of copies of the system changes in time.
- $u$: the energy of one pair of atoms as a function of their distance $r$, for example the Lennard-Jones function. $du/dr$ is its slope, taken at the present distance $r_{ij}$.
- $r_{ij}$ (not bold): the distance between atoms $i$ and $j$.
- $\mathbf r_{ij}$ (bold): the vector $\mathbf r_i-\mathbf r_j$, which points from $j$ to $i$. Divided by its length $r_{ij}$ it is a vector of length 1 that gives only the direction.
- $\Gamma$ (capital gamma): one point in phase space, that is one complete set of positions and momenta of all atoms, $6N$ numbers.
- $\dot\Gamma$: the rate of change of that point, made of all the $\dot q$ and $\dot p$ of Hamilton's equations.
- $\nabla_\Gamma\cdot$: the divergence in phase space. It measures whether the flow spreads out (positive) or closes in (negative). Zero means neither.
- $\rho$ (rho): here the density of copies of the system in phase space, a function of $\Gamma$ and of the time $t$. It is not the number density of particles used in the sections on boundaries and on analysis.
- $\partial\rho/\partial t$: the rate of change of that density at a fixed point of phase space.
- $\{\rho,H\}$: the Poisson bracket, short for $\sum_k\big(\frac{\partial\rho}{\partial q_k}\frac{\partial H}{\partial p_k}-\frac{\partial\rho}{\partial p_k}\frac{\partial H}{\partial q_k}\big)$, where $k$ runs over all degrees of freedom. $H$ is the Hamiltonian.
</div>

## Statistical mechanics (Module 3)

$$
P(\Gamma)=\frac{e^{-\beta H(\Gamma)}}{Q}\qquad
Q=\frac{1}{N!\,\Lambda^{3N}}\int e^{-\beta U(\mathbf r)}d\mathbf r\qquad
A=-k_BT\ln Q
$$

<div class="legend" markdown="1">
- First formula: the canonical (Boltzmann) distribution, the probability of one microstate at a fixed temperature.
- Second formula: the classical partition function after the integrals over the momenta have been done.
- Third formula: the Helmholtz free energy from the partition function.
- $\Gamma$: one microstate, a point in phase space (all positions and all momenta).
- $P(\Gamma)$: the probability of the microstate $\Gamma$ when the number of particles, the volume and the temperature are fixed. Here $P$ is a probability, not the pressure. It is a probability per counted state, a pure number: $Q$ counts one state for each cell of volume $h^{3N}$ in phase space ($h$ is Planck's constant, 0.399 kJ mol$^{-1}$ ps) and counts the $N!$ exchanges of identical particles as one state. The probability density per unit volume of phase space, which Module 3 uses for averages, is $e^{-\beta H}/(N!\,h^{3N}Q)$. That is $e^{-\beta H}$ divided by its integral over all positions and momenta.
- $H(\Gamma)$: the Hamiltonian, the total energy of that microstate.
- $\beta$ (beta): short for $1/k_BT$, with $k_B$ the Boltzmann constant and $T$ the temperature in K. At 300 K, $1/\beta=2.494$ kJ/mol.
- $e^{-\beta H}$: the Boltzmann factor. A state whose energy is higher by $k_BT$ is less likely by a factor $e\approx2.7$.
- $Q$: the partition function, the sum of the Boltzmann factors of all microstates. Dividing by it makes the probabilities add up to 1. It is a pure number. Here $Q$ is not the thermostat "mass" of Module 8.
- $N$: the number of particles. $N!$ is the factorial $N(N-1)\cdots1$, which corrects for counting the same arrangement of identical particles more than once.
- $\Lambda$ (capital lambda): the thermal de Broglie wavelength, $h/\sqrt{2\pi mk_BT}$, a length ($h$ is Planck's constant and $m$ the mass of a particle). It is what remains of the integrals over the momenta: one factor $1/\Lambda$ for each of the $3N$ momentum components. The formula for $Q$ is written for $N$ identical particles of one mass.
- $\int e^{-\beta U(\mathbf r)}d\mathbf r$: the configurational integral, called $Z$ in Module 3. The integral runs over all positions of all atoms ($3N$ variables).
- $U(\mathbf r)$: the potential energy of the configuration $\mathbf r$.
- $A$: the Helmholtz free energy, in kJ/mol. Here $A$ is not the name of a state.
- $\ln$: the natural logarithm.
</div>

$$
T_{inst}=\frac{2K}{N_{df}k_B}\qquad\frac{\sigma_T}{T}=\sqrt{\frac{2}{N_{df}}}\qquad
C_V=\frac{\langle\delta E^2\rangle}{k_BT^2}\qquad\langle\delta V^2\rangle=k_BT\,V\kappa_T
$$

<div class="legend" markdown="1">
- First formula: the instantaneous temperature, computed from the kinetic energy of one frame.
- Second formula: how much that temperature fluctuates in a correct constant-temperature simulation.
- Third formula: the heat capacity from the fluctuations of the energy.
- Fourth formula: the fluctuations of the volume at constant pressure, which are set by the compressibility.
- $T_{inst}$: the temperature of one frame, in K.
- $K$: the total kinetic energy, $\sum_i\tfrac12m_iv_i^2$ with $v_i$ the speed of atom $i$, in kJ/mol. Here $K$ is not a force constant or an equilibrium constant.
- $N_{df}$: the number of degrees of freedom, $3N-N_c-3$ (see the section on constraints).
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $\sigma_T$: the standard deviation of $T_{inst}$ along the run. Here $\sigma$ is a standard deviation, not a Lennard-Jones distance. $T$ is the temperature of the simulation, which is the mean of $T_{inst}$. For 100,000 atoms without constraints the ratio is 0.26 %.
- $C_V$: the heat capacity at constant volume, the energy needed to raise the temperature by one kelvin, in kJ mol$^{-1}$ K$^{-1}$.
- $E$: the total energy. $\delta E=E-\langle E\rangle$ is its deviation from the mean, so $\langle\delta E^2\rangle$ is the variance of the energy in a constant-temperature (NVT) simulation.
- $\langle\ \rangle$: the average over the ensemble, in practice over the frames of a trajectory.
- $V$: the volume of the box. $\langle\delta V^2\rangle$ is the variance of the volume in a constant-pressure (NPT) simulation. On the right-hand side $V$ is the mean volume.
- $\kappa_T$ (kappa): the isothermal compressibility, the relative decrease of the volume per unit of added pressure at constant temperature. For water it is $4.5\times10^{-5}$ bar$^{-1}$, which is $7.47\times10^{-4}$ nm$^3$ mol kJ$^{-1}$ in the units of this page (1 bar is 0.0602 kJ mol$^{-1}$ nm$^{-3}$).
</div>

$$
P=\frac{1}{3V}\Big\langle2K+\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}\Big\rangle\qquad
\frac{P_B}{P_A}=e^{-\beta\Delta A_{AB}}\qquad
W(\xi)=-k_BT\ln P(\xi)
$$

<div class="legend" markdown="1">
- First formula: the virial equation for the pressure.
- Second formula: the relative probability of two macrostates, which defines their free-energy difference.
- Third formula: the potential of mean force along a chosen coordinate.
- $P$ (first formula): the pressure. With $K$ in kJ/mol and $V$ in nm$^3$ it comes out in kJ mol$^{-1}$ nm$^{-3}$, and 1 kJ mol$^{-1}$ nm$^{-3}$ is 16.6 bar. $P_A$, $P_B$ and $P(\xi)$ in the other two formulas are probabilities.
- $V$: the volume of the box.
- $K$: the total kinetic energy. The term $2K/3V$ is the ideal-gas part of the pressure.
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once.
- $\mathbf r_{ij}$: the vector from atom $j$ to atom $i$. $\mathbf F_{ij}$: the force on atom $i$ caused by atom $j$. The dot between them is the dot product, which gives a single number.
- $\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}$: the virial term, the contribution of the interactions. Attractive forces make it negative and lower the pressure, repulsive forces raise it.
- $\langle\ \rangle$: the average over the trajectory.
- $P_A$, $P_B$: the probabilities of finding the system in macrostate A or in macrostate B, for example "unbound" and "bound".
- $\Delta A_{AB}$: the Helmholtz free energy of B minus that of A, in kJ/mol. The letter $A$ is the free energy, and the subscripts A and B are the names of the states.
- $\beta$: $1/k_BT$.
- $\xi$ (xi): a chosen coordinate computed from the atomic positions, such as a distance or an angle. In this formula it is not a random number or a thermostat variable.
- $P(\xi)$: the probability density of finding the value $\xi$ at equilibrium, whatever all the other coordinates are doing.
- $W(\xi)$: the potential of mean force, the free energy as a function of $\xi$, in kJ/mol. It is defined up to an added constant. Here $W$ is not work. When $\xi$ is a distance $r$, this $W$ still contains the geometric (Jacobian) term $-2k_BT\ln r$. The formula for $K_a$ in the free-energy section needs the profile with that term removed, which Module 3 writes $w(r)$ and Module 12 writes $W(r)$.
</div>

## Integrators (Module 4)

$$
\mathbf v\leftarrow\mathbf v+\tfrac{\Delta t}{2m}\mathbf F;\quad\mathbf r\leftarrow\mathbf r+\Delta t\,\mathbf v;\quad\mathbf F\leftarrow\mathbf F(\mathbf r);\quad\mathbf v\leftarrow\mathbf v+\tfrac{\Delta t}{2m}\mathbf F
$$

<div class="legend" markdown="1">
- The whole line: one step of the velocity Verlet algorithm. Four operations are done in this order for every atom: half kick, drift, new forces, half kick.
- $\leftarrow$: "is replaced by". Compute the right-hand side with the present values and store the result in the variable on the left, like `=` in a program.
- $\mathbf v$: the velocity of an atom, in nm/ps.
- $\mathbf r$: its position, in nm.
- $\mathbf F$: the force on it. $\mathbf F/m$ is its acceleration.
- $m$: its mass, in u.
- $\Delta t$: the time step, usually 1 to 4 fs (0.001 to 0.004 ps) in an atomistic simulation.
- $\tfrac{\Delta t}{2m}\mathbf F$: the change of the velocity during half a time step (the "half kick").
- $\Delta t\,\mathbf v$: the distance moved in one time step at the present velocity (the "drift").
- $\mathbf F(\mathbf r)$: the forces computed again from the new positions. This is the one force calculation of the step.
</div>

$$
e^{iL\Delta t}\approx e^{iL_p\Delta t/2}e^{iL_r\Delta t}e^{iL_p\Delta t/2}\qquad
\text{stability: }\omega\Delta t<2\qquad
\tilde H=H+O(\Delta t^2)
$$

<div class="legend" markdown="1">
- First formula: the splitting of the exact time-step operation into three pieces that can each be applied exactly. Read from right to left it is velocity Verlet: half kick, drift, half kick.
- Second formula: the stability limit of the time step.
- Third formula: the shadow Hamiltonian that the numerical trajectory conserves.
- $iL$: the Liouville operator, the rule that gives the rate of change of any quantity along the motion. Treat $iL$ as one symbol. The $i$ is the imaginary unit and is there by convention. This $L$ is not a box length.
- $e^{iL\Delta t}$: the propagator, the operation "advance the whole system by one time step $\Delta t$".
- $iL_r$: the part of $iL$ that moves the positions at fixed velocities. $e^{iL_r\Delta t}$ is a drift over a full step.
- $iL_p$: the part that changes the velocities (momenta) under the forces at fixed positions. $e^{iL_p\Delta t/2}$ is a kick over half a step.
- $\approx$: the two sides differ by a term of order $\Delta t^3$ in one step.
- $\omega$ (omega): the angular frequency of the fastest vibration in the system, in radians per ps. Its period is $2\pi/\omega$, so the condition says that $\Delta t$ must be shorter than the period divided by $\pi$.
- $H$: the true Hamiltonian (the total energy). $\tilde H$: the shadow Hamiltonian, a slightly different energy function, which velocity Verlet conserves.
- $O(\Delta t^2)$: a term whose size is proportional to $\Delta t^2$. Halve the time step and it becomes four times smaller.
</div>

## Force field (Modules 5 and 6)

$$
U=\sum_{b}\tfrac12k_b(r-r_0)^2+\sum_{a}\tfrac12k_\theta(\theta-\theta_0)^2+\sum_{d}\sum_nk_n[1+\cos(n\phi-\delta_n)]
+\sum_{i<j}\left\{4\varepsilon_{ij}\left[\left(\tfrac{\sigma_{ij}}{r}\right)^{12}-\left(\tfrac{\sigma_{ij}}{r}\right)^{6}\right]+\frac{q_iq_j}{4\pi\varepsilon_0r}\right\}
$$

<div class="legend" markdown="1">
- The whole formula: the potential energy of a classical additive force field, as a sum of bond, angle, torsion, Lennard-Jones and Coulomb terms. It is shortened: Module 5 has one more bonded sum, over the improper dihedrals, which keep four atoms in a plane. Module 5 derives every term, and Module 6 explains how the numbers in them ($k_b$, $k_\theta$, $k_n$, $\sigma_{ij}$, $\varepsilon_{ij}$, $q_i$) are chosen.
- $U$: the total potential energy, in kJ/mol.
- $\sum_b$, $\sum_a$, $\sum_d$: sums over all bonds, all angles and all proper dihedrals (torsions) listed in the topology.
- $r$ (first sum): the present length of the bond. $r_0$: its reference length, in nm. $k_b$: the bond force constant, in kJ mol$^{-1}$ nm$^{-2}$ (a few times $10^5$ for covalent bonds).
- $\theta$ (theta): the present angle between two bonds that share an atom. $\theta_0$: its reference value. $k_\theta$: the angle force constant, typically 300 to 700 kJ mol$^{-1}$ rad$^{-2}$, so $\theta-\theta_0$ must be in radians. Here $\theta$ is an angle, not the parameters of a neural network.
- $\tfrac12$: the convention of GROMACS. AMBER and CHARMM parameter files leave it out (see the constants table).
- $\phi$ (phi): the dihedral angle of four atoms bonded in a row, the angle between the plane of the first three and the plane of the last three.
- $n$: the multiplicity of a torsion term, the number of minima in a full turn (1, 2, 3, sometimes 4 or 6). $\sum_n$ adds the terms of one dihedral.
- $k_n$: the force constant of the term with multiplicity $n$, in kJ/mol. It is half the barrier height of that term. Module 5 writes it $k_{\phi,n}$.
- $\delta_n$: the phase of that term, 0 or 180° in most force fields. Here $\delta$ is not a delta function.
- $\sum_{i<j}$: a sum over all pairs of non-bonded atoms, each pair once. Atoms one or two bonds apart are left out, and pairs three bonds apart are scaled in some force fields.
- $r$ (last sum): the distance between atoms $i$ and $j$, written $r_{ij}$ in Module 5.
- $\varepsilon_{ij}$ (epsilon): the depth of the Lennard-Jones well for this pair, typically 0.1 to 1 kJ/mol.
- $\sigma_{ij}$ (sigma): the distance at which the Lennard-Jones energy of the pair is zero, the "size" of the pair, in nm.
- The term with the power 12 is the repulsion at short distance. The term with the power 6 is the dispersion attraction.
- $q_i$, $q_j$: the partial charges of the two atoms, in units of the elementary charge $e$.
- $\varepsilon_0$: the permittivity of vacuum, with $1/(4\pi\varepsilon_0)=138.935$ kJ mol$^{-1}$ nm $e^{-2}$. It is a different quantity from the well depth $\varepsilon_{ij}$.
</div>

$$
r_{min}=2^{1/6}\sigma\qquad
\text{Lorentz-Berthelot: }\sigma_{ij}=\tfrac12(\sigma_i+\sigma_j),\ \varepsilon_{ij}=\sqrt{\varepsilon_i\varepsilon_j}\qquad
\text{harmonic fluctuation: }\sqrt{k_BT/k}
$$

<div class="legend" markdown="1">
- First formula: the distance at which the Lennard-Jones energy has its minimum.
- Lorentz-Berthelot: the combining rules, which build the parameters of a pair from the parameters of the two atom types.
- Harmonic fluctuation: the size of the thermal fluctuation of a coordinate held by a harmonic spring.
- $r_{min}$: the distance of the Lennard-Jones minimum, where the energy is $-\varepsilon$ and the force is zero. $2^{1/6}\approx1.122$.
- $\sigma$: the Lennard-Jones distance, where the energy crosses zero.
- $\sigma_i$, $\varepsilon_i$: the Lennard-Jones parameters stored for the atom type of atom $i$. $\sigma_{ij}$, $\varepsilon_{ij}$: the parameters used for the pair of atoms $i$ and $j$.
- $\tfrac12(\sigma_i+\sigma_j)$: the arithmetic mean of the two distances. $\sqrt{\varepsilon_i\varepsilon_j}$: the geometric mean of the two well depths.
- $k$: here the force constant of a harmonic term $\tfrac12k(x-x_0)^2$, for example $k_b$ or $k_\theta$.
- $k_B$, $T$: the Boltzmann constant and the temperature. $k_BT=2.494$ kJ/mol at 300 K.
- $\sqrt{k_BT/k}$: the standard deviation of the coordinate $x$ at the temperature $T$. For a bond with $k_b=2.6\times10^5$ kJ mol$^{-1}$ nm$^{-2}$ it is 0.003 nm at 300 K.
</div>

## Boundaries and electrostatics (Module 7)

$$
\Delta x\leftarrow\Delta x-L\,\mathrm{round}(\Delta x/L)\qquad r_c\le L/2\qquad
U_{tail}=\tfrac83\pi N\rho\varepsilon\sigma^3\left[\tfrac13\left(\tfrac{\sigma}{r_c}\right)^9-\left(\tfrac{\sigma}{r_c}\right)^3\right]
$$

<div class="legend" markdown="1">
- First formula: the minimum-image convention. It replaces a separation by the separation to the nearest periodic copy. The form given is for a rectangular box.
- Second formula: the largest cutoff that is consistent with it.
- Third formula: the tail correction, the Lennard-Jones energy that a cutoff leaves out.
- $\Delta x$: the $x$ component of the separation between two particles. The same operation is applied to $y$ and $z$.
- $\leftarrow$: "is replaced by".
- $L$: the length of the box edge along that direction, in nm. In the second formula it is the shortest edge. Here $L$ is not the Liouville operator.
- $\mathrm{round}(\ )$: round to the nearest whole number. It counts by how many box lengths the separation is off.
- $r_c$: the cutoff distance beyond which pair interactions are not computed, usually 0.9 to 1.2 nm.
- $U_{tail}$: the correction to the total energy, in kJ/mol. It assumes that the liquid is uniform beyond $r_c$.
- $N$: the number of particles. $\rho$ (rho): their number density, in particles per nm$^3$. Here $\rho$ is not the phase-space density of Module 2.
- $\varepsilon$, $\sigma$: the Lennard-Jones well depth and distance of the particles.
- The square bracket: the first term comes from the repulsion and the second from the attraction. For a cutoff larger than $\sigma$ the second is the larger one, so $U_{tail}$ is negative.
</div>

$$
U_{Ewald}=\frac{1}{4\pi\varepsilon_0}\left[\frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\frac{\mathrm{erfc}(\alpha|\mathbf r_{ij}+\mathbf n|)}{|\mathbf r_{ij}+\mathbf n|}+\frac{2\pi}{V}\sum_{\mathbf k\ne0}\frac{e^{-k^2/4\alpha^2}}{k^2}|S(\mathbf k)|^2-\frac{\alpha}{\sqrt\pi}\sum_iq_i^2\right],\qquad S(\mathbf k)=\sum_jq_je^{i\mathbf k\cdot\mathbf r_j}
$$

<div class="legend" markdown="1">
- First formula: the Ewald sum, the electrostatic energy of all charges in the box and in all its periodic copies. The three terms in the square bracket are the real-space term, the reciprocal-space term and the self term. For molecules, Module 7 adds a correction for the pairs that the force field excludes (atoms one or two bonds apart).
- Second formula: the structure factor, which is used in the reciprocal-space term.
- $1/(4\pi\varepsilon_0)$: the Coulomb constant, 138.935 kJ mol$^{-1}$ nm $e^{-2}$.
- $q_i$, $q_j$: the charges of atoms $i$ and $j$, in units of $e$.
- $\mathbf n$: a vector that points from the box to one of its periodic copies (a whole number of box edges along each axis). $\mathbf n=0$ is the box itself. Here $n$ is not a multiplicity.
- $\sum_{\mathbf n}{}^{'}\sum_{i,j}$: a sum over all copies and over all pairs of atoms. The prime means: leave out $i=j$ when $\mathbf n=0$, so that no charge interacts with itself. The $\tfrac12$ in front corrects for counting each pair twice.
- $\mathbf r_{ij}$: the vector between atoms $i$ and $j$ in the box. $|\mathbf r_{ij}+\mathbf n|$: the distance between atom $j$ and the image of atom $i$ in the copy of the box shifted by $\mathbf n$. The bars mean "length of the vector".
- $\mathrm{erfc}$: the complementary error function. $\mathrm{erfc}(x)$ falls from 1 at $x=0$ to nearly 0 for $x$ above about 3, which makes the first term short-ranged.
- $\alpha$ (alpha): the Ewald splitting parameter, in nm$^{-1}$. It sets the width of the Gaussian charge clouds and so how the work is divided between the first two terms. The total does not depend on it.
- $V$: the volume of the box.
- $\mathbf k$ (bold): a wave vector of the periodic box, $2\pi(n_x/L_x,n_y/L_y,n_z/L_z)$ with whole numbers $n_x$, $n_y$, $n_z$ and box edges $L_x$, $L_y$, $L_z$. $k$ (not bold) is its length, in nm$^{-1}$. $\sum_{\mathbf k\ne0}$ runs over all wave vectors except zero. Here $k$ is not a force constant.
- $e^{-k^2/4\alpha^2}$: a Gaussian factor that makes the sum over $\mathbf k$ converge after a modest number of terms.
- $S(\mathbf k)$: the structure factor, a complex number that describes how the charges are arranged at the wavelength that belongs to $\mathbf k$. $|S(\mathbf k)|^2$ is its squared absolute value, a real number.
- $e^{i\mathbf k\cdot\mathbf r_j}$: a complex exponential. In the exponent $i$ is the imaginary unit ($i^2=-1$), not an atom label. $\mathbf k\cdot\mathbf r_j$ is the dot product of the wave vector with the position of atom $j$.
- $-\frac{\alpha}{\sqrt\pi}\sum_iq_i^2$: the self term. It removes the interaction of each charge with its own Gaussian cloud, which the reciprocal-space term contains.
</div>

## Thermostats and barostats (Module 8)

$$
\text{Berendsen: }\lambda^2=1+\frac{\Delta t}{\tau_T}\left(\frac{T_0}{T}-1\right)\qquad
\text{Langevin: }m\dot{\mathbf v}=\mathbf F-\gamma m\mathbf v+\sqrt{2\gamma mk_BT}\,\boldsymbol\eta
$$

<div class="legend" markdown="1">
- Berendsen: the factor by which all velocities are multiplied at each step so that the temperature relaxes towards its target.
- Langevin: the equation of motion of an atom with a friction force and a random force added to the force from the potential.
- $\lambda$ (lambda): here the velocity scaling factor, a pure number close to 1. The formula gives its square. It is not a Lagrange multiplier, a coupling parameter or an eigenvalue.
- $\Delta t$: the time step.
- $\tau_T$ (tau): the coupling time constant, in ps. A larger $\tau_T$ means a weaker and slower coupling.
- $T_0$: the target temperature. $T$ (Berendsen): the instantaneous temperature at this step, written $T_{inst}$ in the statistical mechanics section.
- $m$: the mass of the atom. $\mathbf v$: its velocity. $\dot{\mathbf v}$: its acceleration.
- $\mathbf F$: the force on the atom from the potential energy.
- $\gamma$ (gamma): here the friction rate, in ps$^{-1}$ (Module 8 calls it the friction coefficient). $-\gamma m\mathbf v$ is a friction force that opposes the motion. In explicit solvent $\gamma$ is 0.1 to 1 ps$^{-1}$. It is not the bias factor of metadynamics.
- $\boldsymbol\eta$ (eta, bold): here a random force term, Gaussian white noise. Each of its components has mean zero and is uncorrelated with the other components and with its own value at any other time. It is not a viscosity.
- $\sqrt{2\gamma mk_BT}$: the strength of the random force. It is tied to the friction so that the system settles at the temperature $T$.
- $k_B$, $T$ (Langevin): the Boltzmann constant and the temperature that the thermostat is set to.
</div>

$$
\text{O step: }\mathbf v\leftarrow e^{-\gamma\Delta t}\mathbf v+\sqrt{\tfrac{k_BT}{m}(1-e^{-2\gamma\Delta t})}\,\boldsymbol\xi\qquad
\text{Brownian: }d\mathbf r=\frac{D}{k_BT}\mathbf F\,dt+\sqrt{2D\,dt}\,\boldsymbol\xi
$$

<div class="legend" markdown="1">
- O step: the exact solution of the friction-plus-noise part of Langevin dynamics over one time step. Integrators such as BAOAB use it as one of their sub-steps.
- Brownian: the equation of Brownian (overdamped Langevin) dynamics, the limit of high friction. Positions are moved directly and velocities do not appear.
- $\mathbf v$: the velocity of an atom. $\leftarrow$: "is replaced by".
- $\gamma$: the friction rate, in ps$^{-1}$. $\Delta t$: the time step.
- $e^{-\gamma\Delta t}$: the fraction of the old velocity that survives the friction during one step. With $\gamma=1$ ps$^{-1}$ and $\Delta t=0.002$ ps it is 0.998.
- $k_BT/m$: the variance of one velocity component at the temperature $T$ (the Maxwell-Boltzmann distribution), with $m$ the mass of the atom. The factor $1-e^{-2\gamma\Delta t}$ is the share of this variance that the friction removes in one step, so the noise puts back what was lost.
- $\boldsymbol\xi$ (xi, bold): here a vector of three independent random numbers, each drawn from a Gaussian with mean 0 and variance 1, new for every atom at every step. It is not a collective variable.
- $d\mathbf r$: the displacement of the atom during the small time $dt$.
- $\mathbf F$: the force on the atom.
- $D$: the diffusion coefficient of the atom, $D=k_BT/m\gamma$, in nm$^2$/ps. $D/k_BT$ is the mobility, the velocity per unit of force.
- $\sqrt{2D\,dt}$: the size of the random displacement along each axis during $dt$.
</div>

$$
\text{Nosé-Hoover: }\dot{\mathbf p}_i=\mathbf F_i-\xi\mathbf p_i,\ \ \dot\xi=\frac1Q\Big(\sum_i\frac{\mathbf p_i^2}{m_i}-N_{df}k_BT_0\Big)
$$

<div class="legend" markdown="1">
- The two formulas: the Nosé-Hoover equations of motion. The first is Newton's law with an extra friction term. The second says how the friction variable responds to the kinetic energy.
- $\mathbf p_i$: the momentum of atom $i$. $\dot{\mathbf p}_i$: its rate of change. $\mathbf F_i$: the force on atom $i$. $m_i$: its mass.
- $\xi$ (xi): here the thermostat variable, a friction coefficient in ps$^{-1}$ that is itself a variable of the simulation. When the system is too hot it grows, and the friction cools the system. When the system is too cold it becomes negative and heats the system. It is not a collective variable or a random number.
- $\dot\xi$: its rate of change.
- $\sum_i\mathbf p_i^2/m_i$: twice the kinetic energy at this instant.
- $N_{df}k_BT_0$: twice the kinetic energy that the system should have on average at the target temperature $T_0$, with $N_{df}$ the number of degrees of freedom and $k_B$ the Boltzmann constant.
- $Q$: here the "mass" of the thermostat, an energy times a time squared (kJ mol$^{-1}$ ps$^2$) and not a real mass. It sets how fast $\xi$ responds: $Q=N_{df}k_BT_0\,\tau_T^2$ with $\tau_T$ the coupling time. It is not the partition function.
</div>

$$
\text{Monte Carlo barostat: }P_{acc}=\min\{1,\exp[-\beta(\Delta U+P_0\Delta V)+N_{mol}\ln(V'/V)]\}
$$

<div class="legend" markdown="1">
- The formula: the probability of accepting a trial change of the box volume in a Monte Carlo barostat.
- $P_{acc}$: the acceptance probability, between 0 and 1. $P_0$, with the subscript 0, is a pressure.
- $\min\{1,x\}$: the smaller of 1 and $x$, so that the probability never exceeds 1.
- $\exp[\ ]$: the exponential function, $e$ to the power of the bracket.
- $\beta$: $1/k_BT$.
- $V$: the present volume. $V'$: the trial volume, which must be drawn uniformly in $V$ for this formula (the old volume plus a random number spread evenly between a negative and a positive limit). $\Delta V=V'-V$.
- $\Delta U$: the change of the potential energy when the box and the positions of the molecules are scaled to the trial volume.
- $P_0$: the target pressure. $P_0\Delta V$ is the work done against it (1 bar nm$^3$ is 0.0602 kJ/mol).
- $N_{mol}$: the number of centres that are scaled independently. It is the number of molecules when each molecule is moved as a rigid body.
- $\ln(V'/V)$: the natural logarithm of the ratio of the two volumes. With the factor $N_{mol}$ it accounts for the larger number of positions available to the molecules in a larger box.
</div>

## Constraints (Module 9)

$$
\sigma_k=|\mathbf r_{ij}|^2-d_k^2=0\qquad m_i\ddot{\mathbf r}_i=\mathbf F_i-\sum_k\lambda_k\nabla_i\sigma_k\qquad
g\approx\frac{|\mathbf s'|^2-d^2}{2(m_i^{-1}+m_j^{-1})\,\mathbf s\cdot\mathbf s'}\qquad N_{df}=3N-N_c-3
$$

<div class="legend" markdown="1">
- First formula: a bond constraint written as an equation that must hold at all times.
- Second formula: Newton's law with the constraint forces added.
- Third formula: the SHAKE correction for one constraint.
- Fourth formula: the number of degrees of freedom that remain.
- $k$: here the label of one constraint. $\sum_k$ adds up over all constraints. It is not a force constant.
- $\sigma_k$: here the constraint function of constraint $k$. It is zero when the bond has its prescribed length. It is not a Lennard-Jones distance or a standard deviation.
- $\mathbf r_{ij}$: the vector $\mathbf r_i-\mathbf r_j$ between the two atoms of the constrained bond. $|\mathbf r_{ij}|^2$: its length squared.
- $d_k$: the prescribed length of bond $k$, in nm ($d$ in the third formula, where there is only one bond).
- $m_i$, $\ddot{\mathbf r}_i$, $\mathbf F_i$: the mass of atom $i$, its acceleration and the force on it from the force field.
- $\lambda_k$: here the Lagrange multiplier of constraint $k$, an unknown number that is determined at every step so that the constraint holds. It is not a coupling parameter or an eigenvalue.
- $\nabla_i\sigma_k$: the gradient of the constraint function with respect to the position of atom $i$. For a bond it is $2\mathbf r_{ij}$, so the constraint force $-\lambda_k\nabla_i\sigma_k$ acts along the bond.
- $g$: here the size of the SHAKE correction for one constraint, $g=2\lambda\Delta t^2$ with $\Delta t$ the time step. Its unit is a mass (u), so $g/m_i$ is a pure number. The corrected positions are $\mathbf r_i=\mathbf r_i'-(g/m_i)\,\mathbf s$ and $\mathbf r_j=\mathbf r_j'+(g/m_j)\,\mathbf s$, where the primes mark the positions after the unconstrained step. It is not $g(r)$ or the statistical inefficiency.
- $\mathbf s$: the bond vector at the start of the step, of length $d$. $\mathbf s'$: the bond vector after the unconstrained step. $\mathbf s\cdot\mathbf s'$: their dot product. Here $\mathbf s$ is not a collective variable.
- $m_i^{-1}+m_j^{-1}$: the sum of the inverse masses of the two atoms, $1/m_i+1/m_j$.
- $\approx$: the formula neglects a small term in $g^2$. SHAKE therefore applies it repeatedly until all bond lengths are correct within a tolerance.
- $N_{df}$: the number of degrees of freedom used to compute the temperature. $N$: the number of atoms. $N_c$: the number of constraints. The last 3 accounts for the conserved total momentum in a periodic box.
</div>

## Analysis and errors (Module 11)

$$
g(r)=\frac{\langle n(r,r+dr)\rangle}{4\pi r^2dr\,\rho}\qquad\mathrm{MSD}(t)\to6Dt\qquad
D_\infty=D_{PBC}+\frac{2.837\,k_BT}{6\pi\eta L}
$$

<div class="legend" markdown="1">
- First formula: the radial distribution function, the density of particles at a distance $r$ from a chosen particle divided by the bulk density.
- Second formula: the Einstein relation, which gives the diffusion coefficient from the mean squared displacement.
- Third formula: the correction of a diffusion coefficient for the finite size of a periodic box.
- $g(r)$: here the radial distribution function, a pure number that tends to 1 at large $r$. It is not the SHAKE correction or the statistical inefficiency.
- $r$: the distance from the central particle. $dr$: the thickness of a thin shell.
- $n(r,r+dr)$: the number of particles found in the shell between $r$ and $r+dr$ around one central particle.
- $\langle\ \rangle$: the average over all central particles and all frames.
- $4\pi r^2dr$: the volume of that shell.
- $\rho$: the bulk number density of the particles that are counted, in particles per nm$^3$.
- $\mathrm{MSD}(t)$: the mean squared displacement, the average of the squared distance that a particle has moved after a time $t$, in nm$^2$.
- $\to$: "approaches at long times".
- $D$: the diffusion coefficient, in nm$^2$/ps. The 6 is 2 times the 3 dimensions of space.
- $D_{PBC}$: the diffusion coefficient measured in the periodic box. $D_\infty$: its value for an infinitely large system.
- 2.837: a pure number that belongs to the cubic arrangement of the periodic copies. The formula holds for a cubic box only.
- $k_BT$: the thermal energy.
- $\eta$ (eta): here the viscosity of the solvent. It is not the random force of Langevin dynamics. This formula needs care with units. Module 11 evaluates it in SI units: $k_BT=4.14\times10^{-21}$ J at 300 K, $\eta$ in Pa s and $L$ in m, which gives $D$ in m$^2$/s. With $k_BT$ in kJ/mol, $L$ in nm and $D$ in nm$^2$/ps, the viscosity must be entered in kJ mol$^{-1}$ nm$^{-3}$ ps. 1 mPa s, about the viscosity of water at room temperature, is 602.2 of these units.
- $L$: the edge length of the cubic box.
</div>

$$
g_{stat}=1+2\sum_{k\ge1}c(k\Delta t_s)=1+\frac{2\tau_{int}}{\Delta t_s}\qquad N_{eff}=\frac{N}{g_{stat}}\qquad\mathrm{SE}=\frac{\sigma}{\sqrt{N_{eff}}}\approx\sigma\sqrt{\frac{2\tau_{int}}{T_{sim}}}
$$

<div class="legend" markdown="1">
- First formula: the statistical inefficiency, the number of saved frames that are worth one independent sample.
- Second formula: the effective number of independent samples.
- Third formula: the standard error of the mean of a correlated time series.
- $g_{stat}$: the statistical inefficiency, a pure number. Module 11 writes it $g$. It is not the radial distribution function $g(r)$.
- $c(t)$: the normalised autocorrelation function of the observable. It is 1 at $t=0$ and decays to 0 as the observable loses the memory of its earlier value.
- $\Delta t_s$: the time between saved frames (not the time step $\Delta t$ of the integrator).
- $k$: here a counting label, the number of frames between two samples. $\sum_{k\ge1}$ adds up over all lags $k\Delta t_s$.
- $\tau_{int}$ (tau): the integrated autocorrelation time, in the same unit as $\Delta t_s$. It is $\Delta t_s$ times the sum over the lags, which is the area under the curve $c(t)$.
- $N$: here the number of saved frames, not the number of atoms.
- $N_{eff}$: the number of effectively independent samples.
- $\mathrm{SE}$: the standard error of the mean of the observable. The second form, after $\approx$, holds when $\tau_{int}$ is much longer than $\Delta t_s$.
- $\sigma$: here the standard deviation of the observable over the trajectory.
- $T_{sim}$: the total simulated time, $N\Delta t_s$. It is a time, not a temperature. A 100 ns run of an observable with $\tau_{int}=10$ ns holds about five independent samples.
</div>

## Free energy (Modules 12 and 13)

$$
W(\xi)=-k_BT\ln P_i^b(\xi)-w_i(\xi)+F_i\qquad
\text{WHAM: }P(\xi)=\frac{\sum_in_i(\xi)}{\sum_iN_ie^{-\beta[w_i(\xi)-F_i]}},\ \ e^{-\beta F_i}=\sum_\xi P(\xi)e^{-\beta w_i(\xi)}
$$

<div class="legend" markdown="1">
- First formula: the unbiased potential of mean force recovered from one umbrella window.
- WHAM, first formula: the best estimate of the unbiased distribution from all windows together.
- WHAM, second formula: the free energy of each window. Each of the two WHAM equations contains the unknown of the other, so they are solved by iteration.
- $\xi$ (xi): the collective variable, the coordinate along which the profile is computed (for example a distance in nm).
- $W(\xi)$: the potential of mean force, in kJ/mol.
- $i$: the label of a window, from 1 to $S$ (the number of windows). $\sum_i$ adds up over the windows.
- $P_i^b(\xi)$: the distribution of $\xi$ observed in window $i$. The superscript $b$ means "biased".
- $w_i(\xi)$: here the bias potential of window $i$, usually a spring $\tfrac12k(\xi-\xi_i)^2$ centred at $\xi_i$. It is not a hill height or a weight.
- $F_i$: the free energy of adding bias $i$ to the system, one constant for each window, in kJ/mol. Here $F$ is not a force.
- $P(\xi)$: the unbiased probability of the bin at $\xi$.
- $n_i(\xi)$: the number of samples from window $i$ that fall in the bin at $\xi$.
- $N_i$: the total number of samples in window $i$.
- $k_B$, $T$, $\beta$: the Boltzmann constant, the temperature, and $\beta=1/k_BT$.
- $\sum_\xi$: a sum over all bins of the histogram.
</div>

$$
\text{MBAR: }f_i=-\ln\sum_{n}\frac{e^{-u_i(\mathbf x_n)}}{\sum_kN_ke^{f_k-u_k(\mathbf x_n)}}\qquad
\text{window width: }\sqrt{k_BT/k}
$$

<div class="legend" markdown="1">
- MBAR: the equations for the free energies of all states (windows) at once, without a histogram. The unknowns appear on both sides, so they are solved by iteration.
- Window width: the width of the distribution of $\xi$ in one umbrella window, which sets the spacing of the windows.
- $f_i$: the free energy of state $i$ divided by $k_BT$, $f_i=\beta F_i$, a pure number.
- $n$: here the label of one sample. $\sum_n$ runs over all samples from all windows pooled together, $n=1,\dots,N$.
- $\mathbf x_n$: the configuration (all atomic positions) of sample $n$.
- $u_i(\mathbf x)$: the reduced potential of state $i$, $\beta[U(\mathbf x)+w_i(\xi(\mathbf x))]$. It is the energy that the configuration would have in window $i$, bias included, divided by $k_BT$.
- $k$ (in the sum of the MBAR formula): a label that runs over all states, $k=1,\dots,S$. $N_k$: the number of samples drawn from state $k$. $f_k$, $u_k$: the free energy and the reduced potential of state $k$, defined as $f_i$ and $u_i$.
- $k$ (in the window width): the spring constant of the umbrella bias, in kJ/mol per squared unit of $\xi$.
- $\sqrt{k_BT/k}$: the standard deviation of $\xi$ in a window where the potential of mean force is locally flat. With $k=1{,}000$ kJ mol$^{-1}$ nm$^{-2}$ at 300 K it is 0.05 nm.
</div>

$$
K_a=4\pi\int_{bound}r^2e^{-\beta W(r)}dr\ \ \big(W(r\to\infty)=0,\ \text{Jacobian removed}\big)\qquad\Delta G^\circ=-k_BT\ln(K_aC^\circ)\qquad K_d=1/K_a
$$

<div class="legend" markdown="1">
- First formula: the association constant from a potential of mean force along the separation of the two partners.
- Second formula: the standard free energy of binding.
- Third formula: the dissociation constant.
- $K_a$: the association constant. From this formula it comes out as a volume, in nm$^3$ per molecule. Here $K$ is not a kinetic energy.
- $r$: the distance between the two partners, in nm.
- $\int_{bound}\dots dr$: an integral over the distances that count as bound, from 0 to the end of the bound region.
- $4\pi r^2$: the area of a sphere of radius $r$. It counts the positions available at that distance.
- $W(r)$: the potential of mean force along $r$, in kJ/mol. The bracket gives two conditions. It is shifted so that it is zero at large separation. And the Jacobian is removed: the profile is $-k_BT\ln[P(r)/4\pi r^2]$, which is flat where the partners do not interact. It is the $W(\xi)$ of the earlier blocks, taken along $\xi=r$, with $2k_BT\ln r$ added. Module 3 writes this profile $w(r)$.
- $\beta$: $1/k_BT$.
- $C^\circ$: the standard concentration, 1 mol/L, equal to 0.6022 molecules per nm$^3$. $K_aC^\circ$ is a pure number.
- $\Delta G^\circ$: the standard free energy of binding, in kJ/mol. The circle marks the standard state. $G$ is the Gibbs free energy, for constant pressure. $A$ in the other formulas is the Helmholtz free energy, for constant volume. For binding in a liquid at 1 bar the two differ by a negligible amount (Module 12).
- $K_d$: the dissociation constant. In molar units it is $1.661/K_a$ with $K_a$ in nm$^3$.
</div>

$$
\text{FEP: }\Delta A=-k_BT\ln\langle e^{-\beta\Delta U}\rangle_A\qquad
\text{TI: }\Delta A=\int_0^1\Big\langle\frac{\partial U}{\partial\lambda}\Big\rangle_\lambda d\lambda\qquad
\text{BAR: }\sum_{A}\frac{1}{1+e^{\beta(\Delta U-\Delta A)}}=\sum_{B}\frac{1}{1+e^{-\beta(\Delta U-\Delta A)}}
$$

<div class="legend" markdown="1">
- FEP: free-energy perturbation (the Zwanzig formula). It gives the free-energy difference between two states A and B from a simulation of A alone.
- TI: thermodynamic integration. It gives the same difference as an integral along a path of intermediate states.
- BAR: the Bennett acceptance ratio. It is an equation for the same difference that uses simulations of both A and B and is solved for $\Delta A$ by iteration.
- $\Delta A$: the Helmholtz free energy of state B minus that of state A, in kJ/mol.
- A, B (as a subscript and under the sums): the names of the two states, for example two ligands.
- $\Delta U$: the potential energy that a configuration would have in state B minus its energy in state A, $U_B-U_A$, computed for the same atomic positions.
- $\langle\ \rangle_A$: the average over the configurations sampled in a simulation of state A.
- $\beta$: $1/k_BT$.
- $\lambda$ (lambda): here the coupling parameter, a number that goes from 0 (state A) to 1 (state B) and labels the intermediate states. It is not a Lagrange multiplier, an eigenvalue or a scaling factor.
- $U$ (in TI): the potential energy at the given $\lambda$, for example $(1-\lambda)U_A+\lambda U_B$. $\partial U/\partial\lambda$: its slope with respect to $\lambda$ at fixed atomic positions.
- $\langle\ \rangle_\lambda$: the average over a simulation run at that value of $\lambda$.
- $\int_0^1\dots d\lambda$: the integral over $\lambda$ from 0 to 1, in practice a numerical sum over the simulated values of $\lambda$.
- $\sum_A$, $\sum_B$: sums over the configurations sampled in state A and in state B. The formula is for equal numbers of each.
- $\dfrac{1}{1+e^{x}}$: the Fermi function. It weights each configuration by how plausible it would be as a member of the other state.
</div>

$$
\text{Jarzynski: }\langle e^{-\beta W}\rangle=e^{-\beta\Delta A}\qquad\text{Crooks: }\frac{P_F(W)}{P_R(-W)}=e^{\beta(W-\Delta A)}\qquad
\Delta\Delta G_{bind}=\Delta G_{complex}^{A\to B}-\Delta G_{free}^{A\to B}\qquad
\Delta G^\circ_{bind}=\Delta G_{decouple}^{solvent}-\Delta G_{decouple}^{site}-\Delta G_{restr}^{\circ,\,release}
$$

<div class="legend" markdown="1">
- Jarzynski: an exact relation between the work of many fast, non-equilibrium switches from A to B and the equilibrium free-energy difference.
- Crooks: the relation between the distributions of the work in the forward process and in the reverse process.
- Third formula: a relative binding free energy from a thermodynamic cycle.
- Fourth formula: an absolute binding free energy by double decoupling.
- $W$: here the work done on the system during one switch, in kJ/mol. It is not a potential of mean force.
- $\langle\ \rangle$: the average over many repetitions of the switch, each started from equilibrium in state A.
- $\Delta A$: the free energy of state B minus that of state A.
- $\beta$: $1/k_BT$.
- $P_F(W)$: the probability density of obtaining the work $W$ in the forward process (A to B). $P_R(-W)$: the probability density of obtaining the work $-W$ in the reverse process (B to A).
- $\Delta\Delta G_{bind}$: the binding free energy of B minus that of A, $\Delta G_{bind}(B)-\Delta G_{bind}(A)$. A negative value means that B binds more strongly.
- $\Delta G_{complex}^{A\to B}$: the free energy of changing A into B alchemically in the complex. $\Delta G_{free}^{A\to B}$: the same change for the free molecule in solution.
- $\Delta G^\circ_{bind}$: the standard binding free energy of one ligand.
- $\Delta G_{decouple}^{solvent}$: the free energy of switching off the interactions of the ligand with its surroundings in bulk solvent. $\Delta G_{decouple}^{site}$: the same in the binding site, with the ligand held by restraints. It includes the free energy of switching these restraints on.
- $\Delta G_{restr}^{\circ,\,release}$: the free energy of releasing the decoupled ligand from its restraints into the standard volume $V^\circ$. It is negative.
</div>

## Enhanced sampling (Module 14)

$$
\text{Replica exchange: }P_{acc}=\min\{1,\exp[(\beta_i-\beta_j)(U_i-U_j)]\}\qquad M\propto\sqrt{N_{df}}
$$

<div class="legend" markdown="1">
- Replica exchange: the probability of accepting a swap of configurations between two replicas at different temperatures.
- Second formula: how the number of replicas needed grows with the size of the system, for a fixed range of temperatures. It is shortened: Module 14 gives $M\propto\sqrt{N_{df}}\,\ln(T_{max}/T_{min})$, with $T_{min}$ and $T_{max}$ the lowest and the highest temperature of the ladder.
- $P_{acc}$: the acceptance probability. $\min\{1,x\}$: the smaller of 1 and $x$.
- $i$, $j$: the labels of the two replicas.
- $\beta_i$, $\beta_j$: $1/k_BT_i$ and $1/k_BT_j$, with $T_i$ and $T_j$ the temperatures of the two replicas.
- $U_i$, $U_j$: the potential energies of the configurations that replicas $i$ and $j$ hold before the swap, written $U(\mathbf x)$ and $U(\mathbf x')$ in Module 14. Both are computed with the same energy function.
- $M$: here the number of replicas. It is not a mapping.
- $\propto$: "is proportional to".
- $N_{df}$: the number of degrees of freedom of the system.
</div>

$$
\text{Well-tempered metadynamics: }w=w_0e^{-V(s,t)/k_B\Delta T},\ \ F(s)=-\frac{\gamma}{\gamma-1}V(s),\ \ \gamma=\frac{T+\Delta T}{T}
$$

<div class="legend" markdown="1">
- First formula: the height of the hill that is deposited at the time $t$ in well-tempered metadynamics. It shrinks where bias has already been added.
- Second formula: the free energy from the converged bias.
- Third formula: the definition of the bias factor.
- $s$: the collective variable (called $\xi$ in the free-energy section). Here $s$ is not a bond vector.
- $t$: the time.
- $V(s,t)$: here the bias potential built up so far, as a function of $s$, in kJ/mol. In the first formula it is taken at the present value of $s$. It is not a volume. $V(s)$ in the second formula is the bias at the end of a converged run.
- $w$: here the height of the Gaussian hill that is added now, in kJ/mol. $w_0$: the initial height, around 1 kJ/mol. It is not an umbrella bias or a weight.
- $k_B$: the Boltzmann constant.
- $T$: the temperature of the simulation. $\Delta T$: a parameter with the unit of a temperature. The collective variable is sampled as if at the temperature $T+\Delta T$.
- $\gamma$ (gamma): here the bias factor, a pure number, typically 5 to 20. It is not a friction rate.
- $F(s)$: the free energy as a function of $s$, in kJ/mol, up to an added constant. Here $F$ is not a force.
</div>

## Coarse-graining (Module 15)

$$
U_{CG}(\mathbf R)=-k_BT\ln\int d\mathbf r\,\delta(\mathbf M(\mathbf r)-\mathbf R)e^{-\beta u(\mathbf r)}\qquad
\text{Gō contact: }\varepsilon\left[5\left(\tfrac{\sigma_{ij}}{r}\right)^{12}-6\left(\tfrac{\sigma_{ij}}{r}\right)^{10}\right]
$$

<div class="legend" markdown="1">
- First formula: the ideal coarse-grained potential, the many-body potential of mean force of the beads.
- Gō contact: the energy of one native contact in a C$\alpha$ structure-based (Gō) model.
- $\mathbf R$: the coarse-grained coordinates, the positions of all beads. Here $R$ is not a Born radius.
- $\mathbf r$: the atomistic coordinates, the positions of all atoms.
- $\mathbf M(\mathbf r)$: the mapping, the rule that computes the bead positions from the atom positions (for example the centre of mass of each group). It is not a number of replicas.
- $\delta(\ )$: the Dirac delta function. It keeps only the atomistic configurations that map exactly onto the bead positions $\mathbf R$. Here $\delta$ is not a phase.
- $\int d\mathbf r$: the integral over all atomistic configurations.
- $u(\mathbf r)$: the atomistic potential energy. $\beta$: $1/k_BT$.
- $U_{CG}(\mathbf R)$: the coarse-grained potential, in kJ/mol, defined up to an added constant. It is a free energy, so it depends on the temperature.
- $\varepsilon$ (Gō contact): the strength of one native contact. The depth of the well is $-\varepsilon$.
- $\sigma_{ij}$: here the distance between residues $i$ and $j$ in the native structure. The minimum of the contact energy is exactly at $r=\sigma_{ij}$. This differs from the Lennard-Jones $\sigma$, where the energy is zero.
- $r$: the present distance between beads $i$ and $j$.
</div>

$$
U_{DH}=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_rr}e^{-r/\lambda_D}\qquad
\Delta G_{GB}=-\frac{1}{8\pi\varepsilon_0}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right)\sum_{i,j}\frac{q_iq_j}{\sqrt{r_{ij}^2+R_iR_je^{-r_{ij}^2/4R_iR_j}}}
$$

<div class="legend" markdown="1">
- First formula: the Debye-Hückel energy of two charges in a salt solution, a Coulomb energy that is weakened by the solvent and screened by the ions.
- Second formula: the generalised Born estimate of the polar part of the solvation free energy of a solute (called $\Delta G_{pol}$ in Module 15).
- $q_i$, $q_j$: the charges, in units of $e$. $r$: their distance, in nm.
- $\varepsilon_0$: the permittivity of vacuum, with $1/(4\pi\varepsilon_0)=138.935$ kJ mol$^{-1}$ nm $e^{-2}$.
- $\varepsilon_r$: the relative dielectric constant of the solvent, a pure number (about 78 for water at 25 °C). It weakens the interaction by that factor.
- $\lambda_D$: here the Debye length, in nm, the distance over which the ions screen the interaction. In water at 25 °C it is $0.304/\sqrt I$ nm with the ionic strength $I$ in mol/L. It is not a coupling parameter or an eigenvalue.
- $e^{-r/\lambda_D}$: the screening factor. Here $e$ is the base of the natural logarithm, not the elementary charge.
- $\varepsilon_{in}$, $\varepsilon_{out}$: the dielectric constants inside the solute and of the solvent outside.
- $\sum_{i,j}$: a sum over all ordered pairs of atoms. It includes each atom with itself ($i=j$), and every pair of different atoms appears twice, as $(i,j)$ and as $(j,i)$. That is why the factor in front has $8\pi$ where Coulomb's law has $4\pi$.
- $r_{ij}$: the distance between atoms $i$ and $j$.
- $R_i$, $R_j$: the Born radii of the two atoms, in nm. The Born radius of an atom measures how deeply it is buried in the solute. Here $R$ is not a bead coordinate.
- The square root: the function called $f_{GB}$ in Module 15. It equals $R_i$ for $i=j$ and tends to $r_{ij}$ when the two atoms are far apart.
</div>

## Kinetics (Module 16)

$$
K_d=\frac{k_{off}}{k_{on}}\qquad k_{TST}=\frac{\omega_0}{2\pi}e^{-\beta\Delta W^\ddagger}\qquad
k_{Kramers}=\frac{\omega_0\omega_b}{2\pi\gamma}e^{-\beta\Delta W^\ddagger}
$$

<div class="legend" markdown="1">
- First formula: the dissociation constant as the ratio of the two rate constants of binding.
- Second formula: the rate of escape from a harmonic well according to transition state theory.
- Third formula: the Kramers rate for the same escape at high friction.
- $K_d$: the dissociation constant, in mol/L.
- $k_{off}$: the rate constant of dissociation, in s$^{-1}$. $1/k_{off}$ is the residence time. $k_{on}$: the rate constant of association, in M$^{-1}$ s$^{-1}$. Here $k$ is a rate constant, not a force constant.
- $k_{TST}$, $k_{Kramers}$: the rate of crossing the barrier, in crossings per unit of time.
- $\omega_0$ (omega): the angular frequency of the oscillation in the well. $\omega_0/2\pi$ is the number of oscillations per unit of time.
- $\omega_b$: the angular frequency that belongs to the curvature at the top of the barrier. Both frequencies are $\sqrt{|W''|/m}$, with $W''$ the curvature (second derivative) of the profile at the minimum or at the top and $m$ the mass that moves along the coordinate.
- $\Delta W^\ddagger$: the height of the barrier, the potential of mean force at the top minus its value at the minimum, in kJ/mol. The double dagger marks the transition state.
- $\beta$: $1/k_BT$.
- $\gamma$ (gamma): here the friction rate, in 1/time, as in Langevin dynamics. The formula holds when $\gamma$ is much larger than $\omega_b$. It is not the bias factor of metadynamics.
</div>

$$
\hat T_{ij}(\tau)=\frac{C_{ij}}{\sum_kC_{ik}}\qquad t_i=-\frac{\tau}{\ln|\lambda_i(\tau)|}\qquad\mathbf T(k\tau)\approx\mathbf T(\tau)^k\qquad
\mathbf C(\tau)\mathbf v=\lambda\,\mathbf C(0)\mathbf v
$$

<div class="legend" markdown="1">
- First formula: the estimate of the transition matrix of a Markov state model from counted transitions.
- Second formula: the implied time scale of a relaxation process.
- Third formula: the Chapman-Kolmogorov test.
- Fourth formula: the eigenvalue problem that TICA (time-lagged independent component analysis) solves.
- $\tau$ (tau): the lag time, the time interval over which transitions are counted.
- $i$, $j$, $k$: labels of the discrete states in the first formula. In the second formula $i$ numbers the eigenvalues. In the third formula $k$ is a whole number of lag times.
- $C_{ij}$: the number of times the system was seen in state $i$ and, one lag time later, in state $j$. $\sum_kC_{ik}$: all transitions counted out of state $i$.
- $\hat T_{ij}(\tau)$: the estimated probability of being in state $j$ a time $\tau$ after being in state $i$. The hat marks an estimate from data. Here $T$ is not a temperature.
- $\mathbf T(\tau)$ (bold): the whole matrix of these probabilities. $\mathbf T(\tau)^k$: the matrix multiplied by itself $k$ times. $\mathbf T(k\tau)$: the matrix estimated directly from the data at the longer lag $k\tau$. The test asks whether the two agree within the statistical error.
- $\lambda_i(\tau)$: here the eigenvalue number $i$ of $\mathbf T(\tau)$. The largest is $\lambda_1=1$ and the others are smaller. The bars take the absolute value. It is not a coupling parameter.
- $t_i$: the implied time scale of process $i$, the time over which that process relaxes. With $\tau=10$ ns and $\lambda_2=0.95$ it is 195 ns.
- $\mathbf C(\tau)$ (bold, fourth formula): the time-lagged covariance matrix of the features, with entries $\langle\delta x_a(t)\,\delta x_b(t+\tau)\rangle$, where $\delta x_a$ is the deviation of feature $a$ from its mean. $\mathbf C(0)$: the ordinary covariance matrix. This $\mathbf C$ is not the count matrix $C_{ij}$.
- $\mathbf v$: here an eigenvector, a combination of features that defines one TICA component. It is not a velocity.
- $\lambda$ (fourth formula): the eigenvalue that belongs to $\mathbf v$. The combinations with the largest eigenvalues are the ones that decorrelate most slowly.
</div>

## Machine learning (Module 17)

$$
E=\sum_iE_i(\text{environment within }r_c),\ \ \mathbf F_i=-\frac{\partial E}{\partial\mathbf r_i}\qquad
\mathcal L=w_E\sum(E_\theta-E_{QM})^2+w_F\sum|\mathbf F_\theta-\mathbf F_{QM}|^2\qquad
w(\mathbf x)\propto\frac{e^{-\beta U(\mathbf x)}}{p_X(\mathbf x)}
$$

<div class="legend" markdown="1">
- First formula (two equations): the energy of a machine-learned potential as a sum of atomic contributions, and the force as minus its gradient.
- Second formula: the loss that is minimised during training.
- Third formula: the importance weight of a configuration produced by a Boltzmann generator.
- $E$: the total potential energy predicted by the model.
- $E_i$: the contribution of atom $i$. It depends only on the positions and the elements of the atoms closer than $r_c$.
- $r_c$: the cutoff of the model, typically 0.4 to 0.6 nm.
- $\mathbf F_i$: the force on atom $i$. $\partial E/\partial\mathbf r_i$: the gradient of the energy with respect to the position of atom $i$.
- $\mathcal L$: the loss, the number that training makes as small as possible. It is not the Liouville operator.
- $\theta$ (theta): here all the adjustable parameters of the model. It is not an angle. $E_\theta$, $\mathbf F_\theta$: the energy and a force predicted by the model with the parameters $\theta$.
- $E_{QM}$, $\mathbf F_{QM}$: the reference energy and force from a quantum-mechanical calculation.
- The first $\sum$ runs over the reference configurations. The second runs over the configurations and over the atoms of each.
- $|\ |^2$: the squared length of the difference between the two force vectors.
- $w_E$, $w_F$: here the weights of the energy part and of the force part of the loss, set when the training is prepared.
- $w(\mathbf x)$: here the importance weight of the generated configuration $\mathbf x$, used when averages are computed.
- $\propto$: "is proportional to".
- $U(\mathbf x)$: the potential energy of that configuration. $\beta$: $1/k_BT$.
- $p_X(\mathbf x)$: the probability density with which the generator produces the configuration $\mathbf x$.
</div>
