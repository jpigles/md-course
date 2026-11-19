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

## Watch first

{{WATCH}}

## Thermodynamics is not kinetics

<div data-videos="rFavri_VYfk balC-1gTQro hRpUif7C4Ek NOHVd_VgAD0"></div>

For two states A and B with rate constants $k_{AB}$ and $k_{BA}$,

$$
\frac{dP_A}{dt}=-k_{AB}P_A+k_{BA}P_B,\qquad\frac{P_B^{eq}}{P_A^{eq}}=\frac{k_{AB}}{k_{BA}}=e^{-\beta\Delta G_{AB}} .
$$

The free-energy difference fixes only the *ratio* of the rates. The populations relax with the single rate $k_{AB}+k_{BA}$. For binding, $\text{P}+\text{L}\rightleftharpoons\text{PL}$:

$$
K_d=\frac{k_{off}}{k_{on}},\qquad\text{residence time}=\frac{1}{k_{off}} .
$$

Association rates of proteins are typically $10^5$ to $10^7$ M$^{-1}$s$^{-1}$, bounded above by diffusion at about $10^9$ to $10^{10}$. For a 10 nM complex with $k_{on}=10^6$ M$^{-1}$s$^{-1}$, $k_{off}=10^{-2}$ s$^{-1}$: the complex lives for 100 seconds on average. Two complexes with the same $K_d$ can differ by orders of magnitude in residence time, and for drug efficacy residence time often matters more.

## Transition state theory

<div data-videos="c-dKO66Sx9A"></div>

Divide configuration space into reactant and product by a surface at the top of the barrier, at $\xi=\xi^\ddagger$. TST assumes that every trajectory crossing the surface towards products goes on to become product, and that reactants are in equilibrium. The rate is the equilibrium flux through the surface:

$$
k_{TST}=\tfrac12\big\langle|\dot\xi|\big\rangle_{\xi^\ddagger}\;\frac{e^{-\beta W(\xi^\ddagger)}}{\int_{A}e^{-\beta W(\xi)}d\xi} .
$$

For a one-dimensional harmonic well with frequency $\omega_0$ and barrier $\Delta W^\ddagger$ this becomes

$$
k_{TST}=\frac{\omega_0}{2\pi}\,e^{-\beta\Delta W^\ddagger},
$$

and in the form used by chemists (Eyring), $k=\dfrac{k_BT}{h}e^{-\beta\Delta G^\ddagger}$, with $k_BT/h=6.2\times10^{12}$ s$^{-1}$ at 300 K.

TST is an **upper bound**. Real trajectories recross the surface: they are knocked back by the solvent. The exact rate is $k=\kappa\,k_{TST}$ with a **transmission coefficient** $\kappa\le1$ that can be computed by launching short trajectories from the dividing surface (the reactive-flux, or Bennett-Chandler, method).

## Kramers theory

[Kramers (1940)](cite:kramers1940) treated barrier crossing as Brownian motion of a particle in a potential with friction $\gamma$. With well frequency $\omega_0$, barrier frequency $\omega_b$ (from the negative curvature at the top) and barrier height $\Delta W^\ddagger$, the high-friction result is

$$
k_{Kramers}=\frac{\omega_0\,\omega_b}{2\pi\gamma}\,e^{-\beta\Delta W^\ddagger}\qquad(\gamma\gg\omega_b).
$$

The rate is inversely proportional to friction: in the overdamped regime that applies to conformational changes of proteins in water, crossing the barrier top is a slow diffusion and the system recrosses many times. At very low friction the rate falls again because the particle cannot gain or lose energy fast enough, giving the "Kramers turnover" in between.

Two lessons for simulation. First, anything that changes the effective friction (the thermostat's $\gamma$, a water model that is too fluid, a coarse-grained or implicit-solvent model) changes the rates without changing the free energies. Second, the prefactor is not universal: it depends on the curvature and on the diffusion coefficient along the coordinate, so a barrier height alone does not give a rate.

For diffusive motion along a coordinate with free energy $W(x)$ and position-dependent diffusion coefficient $D(x)$, the mean first-passage time from $a$ to $b$ is exact:

$$
\tau(a\to b)=\int_a^b\frac{e^{\beta W(x)}}{D(x)}\left[\int_{-\infty}^{x}e^{-\beta W(y)}dy\right]dx .
$$

## The committor and what makes a good reaction coordinate

<div data-videos="ziRedoLEb2o"></div>

For any configuration $\mathbf x$, the **committor** $p_B(\mathbf x)$ is the probability that a trajectory started from $\mathbf x$ with random Maxwell-Boltzmann velocities reaches state B before state A. It is 0 in A, 1 in B, and the true **transition state ensemble** is the set of configurations with $p_B=\tfrac12$.

The committor is the ideal reaction coordinate: it says exactly how far a configuration has progressed. A collective variable $\xi$ is a good reaction coordinate to the extent that the committor is a function of it, $p_B(\mathbf x)\approx g\big(\xi(\mathbf x)\big)$ with $g$ monotonic, so that every surface of constant $\xi$ is a surface of constant committor. The test: collect configurations at the barrier top of your PMF, shoot many short trajectories from each, and histogram their committor values. A peak near $\tfrac12$ means $\xi$ captures the mechanism. A bimodal histogram with peaks near 0 and 1 means that the configurations at the "barrier top" already belong to one side or the other: an important coordinate is missing, the barrier in the PMF is lower than the true one, and a rate computed from it will be too high.

This is why barrier heights read from a PMF along a convenient coordinate should not be quoted as activation free energies without such a check.

## Markov state models

<div data-videos="xNjQatR2rRU 0pB3pUXULmo YXppP_QTut8"></div>

The alternative to choosing a coordinate in advance: describe the dynamics as jumps between many small states, and estimate the jump probabilities from simulation. An MSM turns many short trajectories, which can be run in parallel and started from different points, into a model of long-time kinetics.

### The model

<div data-videos="kKC4ccoUHGU gSR2xp2NFIc"></div>

Partition configuration space into $n$ discrete states. Choose a **lag time** $\tau$. The model is the transition probability matrix

$$
T_{ij}(\tau)=P\big(\text{in state }j\text{ at }t+\tau\ \big|\ \text{in state }i\text{ at }t\big),
$$

and the assumption is that the process is **Markovian** at lag $\tau$: the next state depends only on the current state, not on the history. Then the populations evolve as $\mathbf p^T(t+k\tau)=\mathbf p^T(t)\,\mathbf T^k(\tau)$. The assumption holds when the states are small enough, and $\tau$ long enough, that the system forgets within one lag time where inside a state it was.

### Estimation

<div data-videos="pVl7TPFuHwk"></div>

Count transitions at lag $\tau$ along all trajectories: $C_{ij}$ is the number of times the system was in $i$ at time $t$ and in $j$ at $t+\tau$. The simplest estimate of the transition matrix is the row-normalised count matrix,

$$
\hat T_{ij}=\frac{C_{ij}}{\sum_kC_{ik}} .
$$

At equilibrium the dynamics obey detailed balance, $\pi_iT_{ij}=\pi_jT_{ji}$, and current practice is to restrict the model to the largest connected set of states and to use a maximum-likelihood estimator that enforces detailed balance. Bayesian estimators sample the distribution of transition matrices compatible with the counts and give error bars for everything derived from the model.

### What the eigenvalues mean

<div data-videos="opx_wViFlTs"></div>

Diagonalise $\mathbf T$. The eigenvalues satisfy $1=\lambda_1>\lambda_2\ge\lambda_3\ge\dots$

- The left eigenvector with $\lambda_1=1$ is the **stationary distribution** $\boldsymbol\pi$: the equilibrium populations of the states, and so the free energies $F_i=-k_BT\ln\pi_i$, obtained from short trajectories that never individually sampled equilibrium.
- Each further eigenvector describes a **relaxation process**, an exchange of population between the regions where it is positive and negative, decaying with the **implied time scale**

$$
t_i=-\frac{\tau}{\ln|\lambda_i(\tau)|} .
$$

A gap in the spectrum (a few slow processes well separated from the rest) indicates metastable states.

### The pipeline

<div data-videos="A3AUWXqqONc QHQBVmVq-Vo u4ec4EYsgkQ jXMaCSSOSgg CNYreswqJAQ"></div>

1. **Featurise.** Convert each frame into internal coordinates that do not depend on overall rotation: backbone dihedrals, distances between residues, contacts.
2. **Reduce dimension with TICA.** Time-lagged independent component analysis finds the linear combinations of features that decorrelate most slowly, by solving the generalised eigenvalue problem
   $$\mathbf C(\tau)\,\mathbf v=\lambda\,\mathbf C(0)\,\mathbf v,\qquad C_{ab}(\tau)=\big\langle\delta x_a(t)\,\delta x_b(t+\tau)\big\rangle .$$
   Compare with PCA (Module 11), which finds directions of largest variance: large and slow are not the same thing.
3. **Cluster** the frames in the reduced space into 100 to 1,000 microstates (k-means or similar).
4. **Estimate** $\mathbf T(\tau)$ for a range of lag times.
5. **Validate** (below), then choose the lag time.
6. **Coarse-grain** the microstates into a few metastable macrostates (PCCA+, or a hidden Markov model) for interpretation.
7. **Extract** populations, rates, mean first-passage times, and with transition path theory the committor, the reactive flux and the dominant pathways between two states.

The variational principle (VAMP) gives a score that measures how well a choice of features and states captures the slow dynamics, so that modelling choices can be compared objectively by cross-validation. Neural networks trained on this score (VAMPnets) merge steps 1 to 3.

### Validation

<div data-videos="aO_DmbqHWYs"></div>

- **Implied time scales against lag time.** Compute $t_i(\tau)$ for increasing $\tau$. If the model is Markovian, a true relaxation time does not depend on the lag used to measure it. Choose the smallest $\tau$ at which the slow time scales have levelled off. Time scales that keep rising with $\tau$ mean the discretisation is too coarse or the data insufficient. No process faster than $\tau$ can be resolved.
- **Chapman-Kolmogorov test.** Check that $\mathbf T(k\tau)\approx\mathbf T(\tau)^k$: the model estimated at lag $\tau$ must predict, within error, the transition probabilities estimated directly from the data at longer lags.
- **Connectivity and statistics.** Every state kept must be reversibly connected to the rest, with transitions observed in both directions more than a few times. A state entered once and never left makes the model meaningless for that state.

<div class="widget" data-widget="msm"></div>

### Sampling for a Markov model

<div data-videos="B8uo60u9TqI Fuai8_MSxaw HfTdS-kgG70"></div>

Because only local equilibrium within states is needed, the data can be many short trajectories from distributed computing or many GPUs. **Adaptive sampling** runs in rounds: build a preliminary model, start new trajectories from states that are poorly sampled or newly discovered, and repeat (doing this fully automatically and reliably for complex systems is still an open problem). Markov models have been used to describe protein folding at millisecond time scales and the binding and unbinding of ligands and of protein partners, including dissociation events that no single trajectory spans.

Limits: the model is only as good as the features (a slow motion that the features cannot see is absent from the model), rare states remain statistically weak, and the result depends on modelling choices, which is why the validation steps are not optional. The underlying trajectories must come from dynamics whose kinetics you are prepared to defend (Module 8).

## Check yourself

<details markdown="1"><summary>1. A complex has K_d = 1 nM and k_on = 10⁶ M⁻¹s⁻¹. What is its residence time? How long would you have to simulate to see it dissociate ten times?</summary>
$k_{off}=K_d\,k_{on}=10^{-9}\times10^6=10^{-3}$ s$^{-1}$, a residence time of 1,000 s. Ten events would take about $10^4$ seconds of simulated time, some $10^{10}$ times longer than a 1 µs trajectory.
</details>

<details markdown="1"><summary>2. Your PMF along a distance has a 30 kJ/mol barrier. Using k = (k_BT/h) exp(−βΔG‡) you get a rate. Give two reasons it may be wrong by orders of magnitude.</summary>
(1) The prefactor $k_BT/h$ is a gas-phase estimate. In solution the motion over the barrier is diffusive and the prefactor depends on friction and curvature, often being $10^2$ to $10^4$ times smaller. (2) The distance may not be the reaction coordinate: if another slow variable is involved, the true barrier is higher than the one seen in the projection, and the transmission coefficient is small.
</details>

<details markdown="1"><summary>3. At lag time 10 ns the second eigenvalue of a Markov model is 0.95. What is the slowest relaxation time?</summary>
$t_2=-10/\ln0.95=195$ ns.
</details>

<details markdown="1"><summary>4. The implied time scale of the slowest process rises from 200 ns at τ = 1 ns to 2 µs at τ = 50 ns and is still rising. What should you do?</summary>
The model is not Markovian at these lags with this state definition. Improve the features and the discretisation (the states mix configurations on both sides of a barrier), and collect more data. Do not report the rate.
</details>

## Exercises

1. Simulate overdamped Langevin dynamics on the one-dimensional double well for several barrier heights. Measure the mean time between crossings and compare with the Kramers formula and with the mean first-passage time integral.
2. For the same system, pick points at $x=0$ and compute the committor by shooting 200 short trajectories. Then compute it for points at $x=0.3$.
3. Discretise your double-well trajectory into 20 bins, build $\mathbf T(\tau)$ for several lag times with NumPy, and plot the implied time scales. Compare the slowest with the crossing time from exercise 1.
4. Work through the alanine dipeptide tutorial of PyEMMA or deeptime: features, TICA, clustering, implied time scales, Chapman-Kolmogorov test, PCCA+. Report the populations and exchange times of the main basins.

## Read

{{READ}}

## Key papers

{{PAPERS}}
