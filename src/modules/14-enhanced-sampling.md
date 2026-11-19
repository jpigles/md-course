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

## Watch first

{{WATCH}}

## The problem in one formula

The rate of crossing a free-energy barrier $\Delta F^\ddagger$ is roughly

$$
k\approx k_0\,e^{-\beta\Delta F^\ddagger},
$$

with a prefactor $k_0$ of about $10^{9}$ to $10^{12}$ s$^{-1}$ for molecular motions in solution. Each additional 5.7 kJ/mol (at 300 K) makes the event ten times rarer. A barrier of 40 kJ/mol gives waiting times of microseconds to milliseconds, and 60 kJ/mol gives milliseconds to seconds. Plain MD spends almost all its time vibrating inside one basin.

Enhanced sampling methods change the simulation so that barriers are crossed often, in a way that still allows the unbiased equilibrium distribution to be recovered. They fall into three families:

| Family | What is changed | Examples | Needs collective variables? |
|---|---|---|---|
| Bias along chosen coordinates | A potential is added as a function of a few CVs | Umbrella sampling, metadynamics, adaptive biasing force, steered MD | Yes |
| Tempering | Temperature or the whole Hamiltonian is scaled, usually across exchanging replicas | Temperature replica exchange, REST2, Hamiltonian replica exchange, simulated tempering, accelerated MD | No (or only loosely) |
| Trajectory ensembles | Many unbiased trajectories are managed so that rare ones are kept | Weighted ensemble, milestoning, transition path sampling, adaptive sampling with Markov models | A progress coordinate |

## Collective variables

A collective variable $s(\mathbf r)$ is a function of the coordinates that describes the process in few dimensions: a distance, an angle, a coordination number, an RMSD, the fraction of native contacts, a path variable. A good CV:

1. **distinguishes** the initial, final and intermediate states;
2. **includes the slow motions**. Any slow motion not in the CV set is not accelerated, and the bias then pushes the system over the wrong ridge, producing hysteresis and wrong free energies;
3. is **few in number**: the cost of filling a free-energy landscape grows exponentially with the number of CVs, and two or three is the practical limit for most CV-based methods.

Finding good CVs is the hard part of this whole subject. Machine-learning approaches (time-lagged independent components, autoencoders, classifiers trained on end states) are increasingly used to propose them from preliminary simulations.

## Replica exchange (parallel tempering)

Run $M$ copies of the system at temperatures $T_1<T_2<\dots<T_M$ simultaneously. The hot replicas cross barriers easily. At intervals, attempt to **swap configurations** between neighbouring temperatures, so that structures found at high temperature can reach the temperature of interest.

**The acceptance rule.** The joint probability of replica $i$ holding configuration $\mathbf x$ and replica $j$ holding $\mathbf x'$ is proportional to $e^{-\beta_iU(\mathbf x)}e^{-\beta_jU(\mathbf x')}$. After the swap it is $e^{-\beta_iU(\mathbf x')}e^{-\beta_jU(\mathbf x)}$. Detailed balance with the Metropolis criterion requires accepting with the ratio of the two:

$$
\boxed{P_{acc} = \min\Big\{1,\ \exp\big[(\beta_i-\beta_j)\,\big(U(\mathbf x)-U(\mathbf x')\big)\big]\Big\}}
$$

Sanity check: if $i$ is the colder replica ($\beta_i>\beta_j$) and currently holds the configuration of higher energy ($U(\mathbf x)>U(\mathbf x')$), the exponent is positive and the swap is always accepted. The low-energy configuration moves to the cold replica, as it should. After an accepted swap, velocities are rescaled by $\sqrt{T_{new}/T_{old}}$. Each temperature samples its own canonical ensemble exactly, so the lowest-temperature replica gives unbiased averages directly.

**How many replicas.** Swaps are accepted only if the potential-energy distributions of neighbouring temperatures overlap. The mean energy grows in proportion to the number of degrees of freedom $N_{df}$ while the width of the distribution grows as $\sqrt{N_{df}}$, so the temperature spacing must shrink as $1/\sqrt{N_{df}}$ and

$$
M\propto\sqrt{N_{df}}\;\ln\frac{T_{max}}{T_{min}} .
$$

A geometric ladder, $T_k = T_{min}(T_{max}/T_{min})^{k/(M-1)}$, gives roughly uniform acceptance when the heat capacity is constant; aim for 20 to 30 %. A small protein in explicit water (30,000 atoms) spanning 300 to 450 K needs of the order of 50 to 60 replicas, most of the effort going into heating water. That cost motivates the next method.

**REST2** (replica exchange with solute tempering; Wang, Friesner and Berne 2011). All replicas run at the same temperature $T_0$, but the potential energy is scaled so that only the solute is effectively heated:

$$
U_m = \lambda_m\,U_{pp}+\sqrt{\lambda_m}\,U_{pw}+U_{ww},\qquad\lambda_m = \frac{T_0}{T_m}\le1,
$$

with solute-solute (pp), solute-water (pw) and water-water (ww) terms. The solute sees an effective temperature $T_m$ while the water stays cold. Since only the solute's degrees of freedom enter the exchange criterion, a handful to a dozen replicas suffice.

**Hamiltonian replica exchange.** In general the replicas can differ in any parameter of the Hamiltonian: the $\lambda$ of an alchemical transformation, or the centre of an umbrella window. For two replicas with bias potentials $w_i$ and $w_j$ at the same temperature, holding $\mathbf x_i$ and $\mathbf x_j$:

$$
P_{acc} = \min\Big\{1,\ \exp\big(-\beta\big[w_i(\mathbf x_j)+w_j(\mathbf x_i)-w_i(\mathbf x_i)-w_j(\mathbf x_j)\big]\big)\Big\} .
$$

The bracket is the energy after the swap minus the energy before. Exchanges between umbrella windows let a configuration diffuse along the reaction coordinate and help the orthogonal degrees of freedom to relax, which reduces the hysteresis problem of Module 12 at no extra cost.

A limit to remember: tempering helps with *enthalpic* barriers. A barrier that is entropic, a narrow path that must be found, is not lowered by heating.

## Metadynamics

Laio and Parrinello (2002). Instead of fixing the bias in advance, build it during the run. At regular intervals deposit a small Gaussian hill at the current value of the CVs:

$$
V(s,t) = \sum_{t'<t}w\,\exp\left(-\frac{\big(s-s(t')\big)^2}{2\sigma^2}\right).
$$

The accumulated hills push the system away from where it has already been. Wells are filled, the system spills over the lowest barrier into the next well, and eventually the whole landscape along $s$ is flat. At that point the bias is the negative of the free energy, $V(s,t\to\infty)\approx-F(s)+C$.

In this original form the bias never converges: hills keep being added and $V$ fluctuates around $-F$ with an error set by the hill height. **Well-tempered metadynamics** (Barducci, Bussi and Parrinello 2008) lets the hill height decrease where bias has already accumulated:

$$
w(t') = w_0\,\exp\left(-\frac{V\big(s(t'),t'\big)}{k_B\,\Delta T}\right),
\qquad
V(s,t\to\infty) = -\frac{\Delta T}{T+\Delta T}\,F(s)+C .
$$

The bias converges smoothly to a fraction of $-F$, and the CVs are sampled as if at the higher temperature $T+\Delta T$. The **bias factor** $\gamma=(T+\Delta T)/T$ is the main parameter: $\gamma=1$ is unbiased MD, $\gamma\to\infty$ is standard metadynamics, and typical values are 5 to 20, chosen so that the highest relevant barrier divided by $\gamma$ is a few $k_BT$. The free energy is $F(s)=-\frac{\gamma}{\gamma-1}V(s)$, and other observables can be recovered by reweighting each frame with $e^{\beta[V(s,t)-c(t)]}$.

Practical choices: the Gaussian width $\sigma$ should be about the standard deviation of the CV in an unbiased basin; hills every 1 ps or so; initial height around 1 kJ/mol. **Convergence** means the system has gone back and forth between the basins many times and the free-energy difference between them has stopped changing. One crossing each way is not convergence. Variants: multiple walkers (several simulations sharing one bias), bias-exchange and parallel-tempering metadynamics, and on-the-fly probability enhanced sampling (OPES). The standard implementation is the PLUMED library, which plugs into GROMACS, AMBER, NAMD, LAMMPS and OpenMM.

**Adaptive biasing force** (Darve and Pohorille 2001) is the force-based relative: accumulate a running estimate of the mean force $-dF/ds$ in bins along the CV, and apply its negative. Once the estimate is good the system diffuses freely along $s$, and $F$ is the integral of the estimated mean force.

## Steered MD

Attach a harmonic spring to a CV and move its centre at constant speed $v$:

$$
U_{pull}(t) = \tfrac12k\big[s(\mathbf r)-s_0-vt\big]^2 .
$$

This imitates an atomic-force-microscope or optical-tweezer experiment, at pulling speeds millions of times faster (0.1 to 10 nm/ns against micrometres per second). It is used to explore unbinding and unfolding pathways, to generate starting structures for umbrella windows, and to compare forces between related systems.

Getting a free energy from it uses Jarzynski's equality (Module 13) with the accumulated work $W=\int F_{pull}\,v\,dt$. At practical speeds the process is far from equilibrium and most of the work is dissipated, so the exponential average does not converge. Rupture forces and work values depend on the pulling speed, roughly logarithmically, and comparisons are only meaningful at equal speed and spring constant.

## Accelerated MD

Hamelberg, Mongan and McCammon (2004). Raise the bottoms of all wells without choosing CVs. When the potential energy $V$ is below a threshold $E$, add a boost:

$$
\Delta V(\mathbf r) = \frac{\big(E-V(\mathbf r)\big)^2}{\alpha+E-V(\mathbf r)}\quad\text{for }V<E,\qquad\Delta V=0\text{ otherwise}.
$$

Barriers shrink and transitions speed up by orders of magnitude. Recovering unbiased averages needs the weights $e^{\beta\Delta V}$, and because $\Delta V$ is tens to hundreds of $k_BT$ for a solvated protein, those weights are dominated by a few frames: the reweighted result is very noisy. **Gaussian accelerated MD** uses a harmonic boost whose distribution is close to Gaussian, so the reweighting factor can be approximated by a second-order cumulant expansion. These methods are good for exploration; treat their free energies with caution.

## Weighted ensemble

Huber and Kim (1996). No bias on the potential at all. Divide a progress coordinate into bins. Run many short unbiased trajectories ("walkers"), each carrying a statistical weight. After each short interval, **split** walkers in bins that have too few (the copies share the weight) and **merge** walkers in bins that have too many (the survivor takes the combined weight). Computer time is thereby concentrated on rare regions, while the total weight flowing from one state to another remains statistically exact.

Because the dynamics are unbiased, the method gives **rates** and pathways as well as populations, which bias-based methods do not give directly. The costs are many trajectories, correlated walkers, and slow relaxation to steady state. WESTPA is the usual software. Milestoning, forward flux sampling and transition path sampling are related methods that also work with ensembles of unbiased trajectory fragments.

## Choosing

| Situation | Reasonable first choice |
|---|---|
| Free energy along a coordinate you trust (a binding distance, one dihedral) | Umbrella sampling with exchange between windows, or well-tempered metadynamics |
| Conformational ensemble of a peptide or a disordered region, no obvious CV | REST2, or temperature replica exchange for small systems |
| Alchemical free energies | Hamiltonian replica exchange in $\lambda$ |
| Exploring an unknown mechanism | Steered MD or Gaussian accelerated MD for a first look, then a rigorous method on the pathway found |
| Rates and mechanisms | Weighted ensemble, or many unbiased trajectories with a Markov state model (Module 16) |
| The slow variable is unknown | Preliminary simulations plus data-driven CV discovery, then a CV-based method |

The same validation applies to all of them: the final answer must not depend on the starting structure, on which half of the data you analyse, or on a second independent run.

## Check yourself

<details markdown="1"><summary>1. Why does the number of replicas in temperature replica exchange grow with system size?</summary>
The swap probability depends on the overlap of the potential-energy distributions at neighbouring temperatures. Their separation grows as $N_{df}\,\Delta T$ and their width as $\sqrt{N_{df}}$, so the temperature spacing giving constant overlap shrinks as $1/\sqrt{N_{df}}$.
</details>

<details markdown="1"><summary>2. In well-tempered metadynamics with bias factor 10 at 300 K, the converged bias between two basins differs by 18 kJ/mol. What is the free-energy difference?</summary>
$F=-\frac{\gamma}{\gamma-1}V$, so the difference is $18\times10/9 = 20$ kJ/mol, with the opposite sign to the bias difference: the basin with more accumulated bias is the lower one.
</details>

<details markdown="1"><summary>3. A metadynamics run shows the system leaving the bound state once and never returning. Can you report the binding free energy?</summary>
No. The depth of the bound well can be estimated only when the system has visited both states repeatedly under a nearly stationary bias. A single exit tells you roughly how much bias was needed to escape. That is not a free energy, and it says nothing about the free energy of the unbound state relative to the bound one.
</details>

<details markdown="1"><summary>4. Why do weighted ensemble simulations give rates while metadynamics does not, at least not directly?</summary>
Weighted ensemble trajectories follow the unmodified dynamics, and the splitting and merging only redistribute statistical weight, so the flux of weight into the target state is the true rate. In metadynamics the forces themselves are altered, so the time axis is no longer physical. (Rates can be recovered under extra assumptions when no bias is deposited on the transition state: "infrequent metadynamics".)
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
