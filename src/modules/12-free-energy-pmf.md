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

## Watch first

{{WATCH}}

## The potential of mean force, again

<div data-videos="pjT7waGUGDI LCKtsR1ijsA upLHN5z9TEg"></div>

From Module 3: for a coordinate $\xi(\mathbf r)$, called a **collective variable** (CV) or reaction coordinate,

$$
P(\xi) = \frac{\int d\mathbf r\,\delta\big(\xi(\mathbf r)-\xi\big)e^{-\beta U(\mathbf r)}}{\int d\mathbf r\,e^{-\beta U(\mathbf r)}},\qquad W(\xi) = -k_BT\ln P(\xi)+C .
$$

The straightforward estimate is a histogram of $\xi$ from a long trajectory. It fails wherever $P(\xi)$ is small. A region that is $10\,k_BT$ above the minimum is visited with relative probability $e^{-10}=4.5\times10^{-5}$: the top of a barrier, which is exactly the region of interest, is almost never sampled, and the system rarely crosses to sample the other side.

### The Jacobian of a distance

For a distance $r$ between two particles in three dimensions, even with no interaction at all the probability density grows as $4\pi r^2$, because there is more volume at larger $r$. The physically meaningful PMF, which is flat for non-interacting particles, removes this factor:

$$
W(r) = -k_BT\ln\frac{P(r)}{4\pi r^2} + C = -k_BT\ln P(r) + 2k_BT\ln r + C' .
$$

Check which convention your software uses. Many tools output $-k_BT\ln P(r)$ without the correction, and a PMF along a distance that keeps falling as $-2k_BT\ln r$ at large separation is the signature.

## Umbrella sampling

<div data-videos="1tMd68ankiA LVxFGBxgrLo c-dKO66Sx9A"></div>

[Torrie and Valleau (1977)](cite:torrie1977). Add a **bias potential** $w_i(\xi)$ that holds the system near a chosen value $\xi_i$, most often a harmonic spring:

$$
U_i^{b}(\mathbf r) = U(\mathbf r)+w_i\big(\xi(\mathbf r)\big),\qquad w_i(\xi) = \tfrac12k\,(\xi-\xi_i)^2 .
$$

Run one simulation, a **window**, for each of a series of centres $\xi_1,\dots,\xi_S$ that span the range of interest. Each window samples its neighbourhood thoroughly, including regions of high free energy.

**The bias can be removed exactly.** The biased distribution in window $i$ is

$$
P_i^{b}(\xi) = \frac{\int d\mathbf r\,\delta(\xi(\mathbf r)-\xi)\,e^{-\beta[U+w_i(\xi)]}}{\int d\mathbf r\,e^{-\beta[U+w_i]}}
= \frac{e^{-\beta w_i(\xi)}\,P(\xi)}{\langle e^{-\beta w_i}\rangle},
$$

because the bias depends on $\mathbf r$ only through $\xi$ and can be taken out of the integral. Solving for the unbiased PMF:

$$
\boxed{W(\xi) = -k_BT\ln P_i^{b}(\xi) - w_i(\xi) + F_i},\qquad F_i = -k_BT\ln\big\langle e^{-\beta w_i}\big\rangle .
$$

Within one window everything on the right is known except the constant $F_i$, the free energy of adding bias $i$ to the system. Each window therefore gives a piece of $W(\xi)$ with an unknown vertical offset. The pieces must be joined, and the joining is where the statistics matter.

<div class="widget" data-widget="umbrella"></div>

## WHAM: joining the windows optimally

<div data-videos="V1RCMp4wM2k"></div>

The weighted histogram analysis method ([Kumar et al. 1992](cite:kumar1992)). Bin $\xi$. Let $n_i(\xi)$ be the number of samples from window $i$ in the bin at $\xi$ and $N_i$ the total number of samples in window $i$. Each window gives its own estimate of the unbiased distribution, $P(\xi)\approx\frac{n_i(\xi)}{N_i}e^{+\beta[w_i(\xi)-F_i]}$. Combine them as a weighted average with weights chosen to minimise the statistical variance of the result. The answer is

$$
\boxed{P(\xi) = \frac{\sum_{i=1}^{S}n_i(\xi)}{\sum_{i=1}^{S}N_i\,e^{-\beta[w_i(\xi)-F_i]}}}
\qquad\qquad
\boxed{e^{-\beta F_i} = \sum_{\xi}P(\xi)\,e^{-\beta w_i(\xi)}}
$$

The first equation has a simple reading: the numerator is the total number of counts observed in the bin, and the denominator is the total number of counts *expected* there if $P(\xi)$ were 1, summed over windows. The second is just the definition of $F_i$. The two are coupled, so they are solved by iteration: start with all $F_i=0$, compute $P$, update the $F_i$, and repeat until they stop changing (to $10^{-6}\,k_BT$ or better; convergence can be slow, and stopping early is a known source of error). The same equations follow from maximising the likelihood of the observed histograms.

Requirements:

- **Overlap.** Neighbouring windows must sample common bins. Where two windows share no bins, nothing in the data fixes their relative offset.
- **Uncorrelated counts.** The derivation assumes independent samples. With correlated data the estimate is still valid but the weights are no longer optimal, and error estimates must account for the correlation (below).

## MBAR: the binless limit

<div data-videos="5tKnjRdVz3E fhMjOYvnGcY"></div>

The multistate Bennett acceptance ratio ([Shirts and Chodera 2008](cite:shirts2008)) removes the histogram. Let $u_k(\mathbf x) = \beta[U(\mathbf x)+w_k(\xi(\mathbf x))]$ be the reduced potential of state $k$, and pool all samples $\mathbf x_n$ from all windows, $n=1,\dots,N$. The dimensionless free energies $f_i=\beta F_i$ satisfy

$$
f_i = -\ln\sum_{n=1}^{N}\frac{e^{-u_i(\mathbf x_n)}}{\sum_{k=1}^{S}N_k\,e^{f_k-u_k(\mathbf x_n)}} .
$$

This is the WHAM equation with bins of zero width, one per sample. Its advantages: no binning error; in the limit of many samples, the lowest variance of any estimator of its family, with an analytical uncertainty that assumes uncorrelated samples; and each sample gets a weight

$$
W_n = \frac{e^{-u_0(\mathbf x_n)}}{\sum_kN_k\,e^{f_k-u_k(\mathbf x_n)}}
$$

for the unbiased state $u_0=\beta U$ (normalise the $W_n$ to sum to 1), so that the unbiased average of **any** observable, including a PMF along a different coordinate, is $\langle A\rangle = \sum_nW_nA(\mathbf x_n)$. MBAR also handles states that differ in temperature or in the Hamiltonian (Module 13). The `pymbar` package implements it. Feed it decorrelated samples.

## Designing an umbrella sampling calculation

<div data-videos="J7F2aguxTXs A3SxYkoKlnM dvo6noErrbc"></div>

**The coordinate.** It must distinguish the states of interest and, ideally, follow the slowest motion. For binding, the distance between the centres of mass of the two binding sites is the standard choice. For folding or coupled folding and binding, the fraction of native contacts $Q$ is common. The method assumes that all coordinates *orthogonal* to $\xi$ equilibrate within each window. If a slow motion is not captured by $\xi$ (a side chain that must flip, a loop that must open, a rotation of the ligand), neighbouring windows sit in different states of that hidden variable and the PMF is wrong, typically showing up as a dependence on the starting configurations.

**Spring constant and spacing.** In a window where the PMF is locally flat, $\xi$ has a Gaussian distribution of width $\sigma=\sqrt{k_BT/k}$. For good overlap, space the centres about one to two $\sigma$ apart:

$$
\Delta\xi\approx(1\text{ to }2)\sqrt{\frac{k_BT}{k}} .
$$

Where the PMF is steep, the window does not sit at its centre: the mean is displaced to $\langle\xi\rangle_i\approx\xi_i - W'(\xi_i)/k$. A weak spring on a steep slope slides away from the region it was meant to sample, leaving a gap. Stiffer springs need more windows. Example: $k$ = 1,000 kJ mol$^{-1}$ nm$^{-2}$ gives $\sigma=0.05$ nm, so windows every 0.05 to 0.1 nm, and 20 to 40 windows for a 2 nm path.

**Starting configurations.** Each window needs a starting structure near its centre. They are usually taken from a steered MD run that pulls the system along $\xi$ (Module 14). Pulling fast distorts the structure, and windows then start from unrelaxed configurations: discard the beginning of each window, and where possible generate starting structures in both directions.

**Checks.**

1. Plot all histograms: every part of the range must be covered by at least two windows.
2. Split each window in halves, or in several time blocks, and compute the PMF from each. Systematic change with time means the windows are still relaxing.
3. Run in both directions (association and dissociation). The difference is **hysteresis**, and is an honest lower bound on the error.
4. Error bars by bootstrap over decorrelated blocks or, better, over complete independent repeats. Bootstrapping individual frames ignores the correlation and gives error bars that are far too small.

**Umbrella integration** is an alternative to WHAM: from the mean and variance of $\xi$ in each window, estimate the mean force, $\partial W/\partial\xi\approx k_BT(\xi-\langle\xi\rangle_i)/\sigma_i^2 - k(\xi-\xi_i)$, and integrate numerically. It needs no iteration and makes noise easy to see.

**Replica exchange between windows** (Module 14) lets configurations move between neighbouring windows and helps the orthogonal degrees of freedom relax.

## From a PMF to a binding constant

<div data-videos="z2C6siB6Qqo iLw7acCoCrs"></div>

Let $W(r)$ be the PMF along the separation of two molecules, **with** the Jacobian removed, shifted so that $W\to0$ at large $r$ where the molecules do not interact. The equilibrium constant for association is the ratio of the bound-state configurational integral to that of the two free molecules at unit concentration:

$$
K_a = 4\pi\int_{0}^{r_b}r^2\,e^{-\beta W(r)}\,dr ,\qquad K_d=\frac{1}{K_a},
$$

where $r_b$ marks the end of the bound region. $K_a$ has units of volume, nm$^3$ per molecule. To get the usual molar units, divide by the volume per molecule at 1 mol/L, $V^\circ = 1/C^\circ = 1.661$ nm$^3$:

$$
\Delta G^\circ_{bind} = -k_BT\ln\frac{K_a}{V^\circ} = -k_BT\ln\big(K_aC^\circ\big),\qquad K_d\,[\text{M}] = \frac{V^\circ}{K_a} .
$$

<div class="box key" markdown="1">
**Worked example.** A PMF has a well of depth 50 kJ/mol and width 0.1 nm centred at $r$ = 1.0 nm. At 300 K, $\beta\times50 = 20.05$, so $K_a\approx4\pi(1.0)^2(0.1)\,e^{20.05} = 1.257\times5.1\times10^{8} = 6.4\times10^{8}$ nm$^3$. Then $K_d = 1.661/6.4\times10^8 = 2.6\times10^{-9}$ M, about 3 nM, and $\Delta G^\circ = -2.494\ln(3.9\times10^8) = -49.3$ kJ/mol.

Notice that the well depth (50) and $\Delta G^\circ$ (49.3) are not the same quantity: $\Delta G^\circ$ contains the width of the well and the standard volume. A narrower well of the same depth binds more weakly.
</div>

Three complications in real systems:

- **The coordinate is one of six.** Two rigid molecules have six relative degrees of freedom: one distance, two angles for the direction, three for the orientation. The simple formula assumes that at each $r$ the simulation samples all orientations and lateral positions correctly. For a protein-protein or protein-peptide complex that is rarely true once the partners separate. The rigorous route ([Woo and Roux 2005](cite:woo2005); [Gumbart, Roux and Chipot 2013](cite:gumbart2013)) adds three kinds of restraint: on the ligand's conformation (RMSD to its bound structure), on its orientation (three angles), and on the direction of the separation vector (two angles that keep the ligand on an axis). It computes the PMF along $r$ with them in place, and adds the free energies of imposing each restraint in the bound state and releasing it in bulk. (The paper describes the same cycle in the binding direction: restrain the free ligand, bring it in, release the restraints in the site.) The bulk terms for direction and orientation need no simulation, because in an isotropic solvent they reduce to integrals of the restraint's Boltzmann factor over angles. The same terms in the bound state do need a simulation (free energy perturbation in the paper). The conformational (RMSD) restraint has to be computed by simulation, for the bound and for the free molecule.
- **Other coordinates need their own standard-state treatment.** If the CV is not a distance, for example $Q$ or an RMSD, the "unbound" end of the profile does not correspond to a defined concentration. The free-energy difference between the two basins of such a profile is a property of *that simulation box*: it depends on the box volume. You must relate the unbound state to a volume to obtain $K_d$, for example through the box volume or a separate distance-based calculation.
- **Finite box.** The PMF must reach its plateau inside the box. With charged partners and slowly decaying interactions this can require a long path.

A PMF also gives a barrier along $\xi$. That barrier is not an activation free energy in the kinetic sense unless $\xi$ is a good reaction coordinate. Module 16 explains what is needed for rates.

## Check yourself

<details markdown="1"><summary>1. Why can the bias be factored out of the integral in the derivation?</summary>
Because $w_i$ depends on the configuration only through $\xi(\mathbf r)$, and the delta function fixes $\xi(\mathbf r)=\xi$. Inside the integral $e^{-\beta w_i(\xi(\mathbf r))}$ is therefore the constant $e^{-\beta w_i(\xi)}$.
</details>

<details markdown="1"><summary>2. You use k = 500 kJ mol⁻¹ nm⁻² at 300 K. What window spacing would you choose? The PMF has a slope of 300 kJ mol⁻¹ nm⁻¹ in one region; where does a window centred there actually sit?</summary>
$\sigma=\sqrt{2.494/500} = 0.071$ nm, so centres every 0.07 to 0.14 nm. On the slope the mean is displaced by $W'/k = 300/500 = 0.6$ nm downhill, far outside the window's nominal position. That spring is much too weak for this region: increase $k$ there (and add windows).
</details>

<details markdown="1"><summary>3. Two neighbouring windows have histograms that do not overlap. What does WHAM return?</summary>
A number, with no warning. The relative offset $F_{i+1}-F_i$ is not determined by any data, so the result depends on numerical noise and the starting guess. The profile will show a meaningless step at the gap.
</details>

<details markdown="1"><summary>4. A PMF along the centre-of-mass distance has a well depth of 60 kJ/mol. A colleague reports "ΔG = −60 kJ/mol". What is missing?</summary>
The integral over the bound-state volume and the standard-state concentration, $K_a = 4\pi\int r^2e^{-\beta W}dr$ and $\Delta G^\circ = -k_BT\ln(K_aC^\circ)$. Also whether the Jacobian was removed, whether orientations were sampled or restrained, and an error estimate.
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
