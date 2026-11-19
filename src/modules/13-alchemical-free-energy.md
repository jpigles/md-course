---
num: 13
title: Free energy II, alchemical methods and non-equilibrium work
short: Alchemical free energy
part: Part IV · Free energy and sampling
hours: 8
summary: Derive free-energy perturbation, thermodynamic integration and the Bennett acceptance ratio, set up thermodynamic cycles for relative and absolute binding free energies, and understand the Jarzynski and Crooks relations.
videos: 17
papers: H
tags: free-energy
---

<div class="box goal" markdown="1">
#### After this module you can

- derive the Zwanzig formula, the thermodynamic integration formula and the BAR equation;
- explain why intermediate states and soft-core potentials are needed;
- draw the thermodynamic cycle for a relative binding free energy, including a mutation in a protein binder;
- describe the double-decoupling route to an absolute binding free energy and the role of restraints;
- state the Jarzynski and Crooks relations and what they imply for pulling simulations.
</div>

## Watch first

{{WATCH}}

## The idea

<div data-videos="ypg1doAqVPM ov0mMvR3wrM a2axeq_E3RQ"></div>

Module 12 computed free energy along a physical path. For many questions a physical path is too slow to sample: unbinding, or changing one residue into another. Free energy is a state function, so any path between the two end states gives the same difference, including a path with no physical counterpart in which one molecule is gradually turned into another or made to vanish. Because atoms change identity, such paths are called **alchemical**.

The quantity is always

$$
\Delta A_{A\to B} = -k_BT\ln\frac{Q_B}{Q_A} = -k_BT\ln\frac{\int e^{-\beta U_B(\mathbf r)}d\mathbf r}{\int e^{-\beta U_A(\mathbf r)}d\mathbf r} .
$$

## Free-energy perturbation

<div data-videos="D_We9YYxpkM bMvzvlqVqzU"></div>

Multiply and divide the integrand of the numerator by $e^{-\beta U_A}$:

$$
\frac{Q_B}{Q_A} = \frac{\int e^{-\beta(U_B-U_A)}\,e^{-\beta U_A}d\mathbf r}{\int e^{-\beta U_A}d\mathbf r} = \big\langle e^{-\beta\Delta U}\big\rangle_A ,\qquad \Delta U = U_B-U_A .
$$

$$
\boxed{\Delta A_{A\to B} = -k_BT\ln\big\langle e^{-\beta\Delta U}\big\rangle_A}
$$

This is the free-energy perturbation formula of [Zwanzig (1954)](cite:zwanzig1954). Simulate state A, and for each saved configuration evaluate what the energy would be in state B. The formula is exact. Its practical problem is that the average is dominated by configurations where $\Delta U$ is very negative, that is, configurations typical of B. If A rarely visits them, the estimate is biased and converges extremely slowly. Expanding in cumulants shows the scale:

$$
\Delta A = \langle\Delta U\rangle_A - \frac{\beta}{2}\,\sigma^2_{\Delta U} + \dots
$$

The method works when the standard deviation of $\Delta U$ is no more than 1 to 2 $k_BT$. By Jensen's inequality, $\Delta A\le\langle\Delta U\rangle_A$ always.

### Intermediate states

To keep the perturbation small, connect A and B through a chain of intermediate Hamiltonians indexed by a **coupling parameter** $\lambda\in[0,1]$, for example

$$
U(\lambda) = (1-\lambda)\,U_A+\lambda\,U_B ,
$$

and add up the steps: $\Delta A = \sum_k\Delta A_{\lambda_k\to\lambda_{k+1}}$. Typical calculations use 10 to 40 or more values of $\lambda$, each a separate simulation.

## Thermodynamic integration

<div data-videos="iCzHM5Lb_m8"></div>

Treat $A(\lambda) = -k_BT\ln Q(\lambda)$ as a function of $\lambda$ and differentiate:

$$
\frac{dA}{d\lambda} = -\frac{k_BT}{Q}\frac{\partial Q}{\partial\lambda} = \frac{\int\frac{\partial U}{\partial\lambda}\,e^{-\beta U(\lambda)}d\mathbf r}{\int e^{-\beta U(\lambda)}d\mathbf r} = \left\langle\frac{\partial U}{\partial\lambda}\right\rangle_\lambda .
$$

$$
\boxed{\Delta A = \int_0^1\left\langle\frac{\partial U}{\partial\lambda}\right\rangle_\lambda d\lambda}
$$

This is thermodynamic integration, which goes back to [Kirkwood (1935)](cite:kirkwood1935). Compute the average of $\partial U/\partial\lambda$ at each $\lambda$ and integrate numerically (the trapezoid rule is the usual recommendation, because it works with any spacing of the $\lambda$ values). TI has no exponential average and is robust, but it has a quadrature error that depends on how smooth the integrand is, and it needs enough $\lambda$ points where the curve bends.

## The Bennett acceptance ratio

FEP uses samples from one end only. With samples from both A and B, [Bennett (1976)](cite:bennett1976) asked for the estimator with the lowest variance. Start from an identity that holds for any function $f$ satisfying $f(x)/f(-x)=e^{-x}$; the Fermi function $f(x)=1/(1+e^{x})$ is the optimal choice:

$$
\frac{Q_B}{Q_A}=\frac{\big\langle f\big(\beta(\Delta U-C)\big)\big\rangle_A}{\big\langle f\big(-\beta(\Delta U-C)\big)\big\rangle_B}\,e^{-\beta C} .
$$

The variance is smallest when the constant is $C=\Delta A+k_BT\ln(N_B/N_A)$. With equal numbers of samples this gives the BAR equation, solved for $\Delta A$ by iteration:

$$
\boxed{\sum_{n\in A}\frac{1}{1+e^{\beta(\Delta U_n-\Delta A)}} = \sum_{n\in B}\frac{1}{1+e^{-\beta(\Delta U_n-\Delta A)}}}
$$

Each configuration from A is weighted by how plausible it would be as a member of B and the reverse. BAR needs only that the two distributions of $\Delta U$ overlap, and is far more efficient than one-sided FEP. **MBAR** (Module 12) generalises it to all $\lambda$ states at once and is the current standard estimator. Its by-product, the **overlap matrix** between states, is the main diagnostic: adjacent states should have off-diagonal overlap of at least about 0.03.

<div class="widget" data-widget="fep"></div>

## Making atoms appear and disappear: soft-core potentials

With linear scaling, a disappearing atom at $\lambda$ close to 1 is nearly non-interacting, so other atoms can sit right on top of it, where its $r^{-12}$ repulsion, though scaled by a small factor, is still infinite. $\langle\partial U/\partial\lambda\rangle$ diverges at the end point. The fix ([Beutler et al. 1994](cite:beutler1994)) is a **soft-core** Lennard-Jones potential in which $\lambda$ also shifts the distance. A widely used form (the GROMACS variant with `sc-power = 1`; the original paper uses different powers of $\lambda$) is:

$$
U_{sc}(r,\lambda) = 4\varepsilon\,(1-\lambda)\left[\frac{1}{\big(\alpha\lambda+(r/\sigma)^6\big)^2}-\frac{1}{\alpha\lambda+(r/\sigma)^6}\right].
$$

At $\lambda=0$ it is the normal potential. As $\lambda\to1$ the singularity at $r=0$ is removed and the interaction fades smoothly. A common and safe protocol turns off the charges first with linear scaling, then the Lennard-Jones interactions with soft-core, so that a bare charge is never left without its repulsive core. Softening both together in a single stage is also used and can be cheaper; neither has been shown to be clearly better ([Mey et al. 2020](cite:mey2020)).

## Thermodynamic cycles

Alchemical changes are useful because of cycles.

### Relative binding free energy

<div data-videos="iweSKUD2YBI WhUEc5YMT2Q HSh4AzzhGKM LJOmgrwncY0 rgN9noKQoVg"></div>

Which of two ligands A and B binds a protein more strongly? The physical processes are the two binding events (horizontal arrows). The alchemical processes turn A into B, once in the binding site and once free in solution (vertical arrows):

```
                 ΔG_bind(A)
   P + A  ───────────────────────►  P·A
     │                               │
     │ ΔG_free(A→B)                  │ ΔG_complex(A→B)
     ▼                               ▼
   P + B  ───────────────────────►  P·B
                 ΔG_bind(B)
```

Going round the cycle must give zero, so

$$
\Delta\Delta G_{bind} = \Delta G_{bind}(B)-\Delta G_{bind}(A) = \Delta G_{complex}(A\to B)-\Delta G_{free}(A\to B) .
$$

Neither vertical leg involves binding or unbinding, and when A and B are similar, each is a small perturbation. For congeneric small molecules, well-run calculations reach root-mean-square errors of about 1 to 2 kcal/mol (4 to 8 kJ/mol) against experiment in favourable cases ([Wang et al. 2015](cite:wang2015); [Mey et al. 2020](cite:mey2020)).

**Mutations in a protein or peptide binder** use the same cycle: "A→B" is the mutation of one residue, done once in the complex and once in the free binder. The result is $\Delta\Delta G_{bind}$ of the mutation. Complications: the free binder may change conformation or become disordered (the free leg then needs far more sampling than the bound leg); mutations that change the net charge need corrections for the finite periodic box, or a co-alchemical ion that changes in the opposite sense; and large changes in side-chain size need time for the surroundings to rearrange.

### Absolute binding free energy

<div data-videos="LPYzLZ1WmG4"></div>

To get $\Delta G^\circ_{bind}$ of one ligand, make it vanish. In **double decoupling** the ligand's interactions with its surroundings are switched off twice, in the binding site and in bulk solvent:

$$
\Delta G^\circ_{bind} = \Delta G_{decouple}^{solvent}-\Delta G_{decouple}^{site}-\Delta G_{restr}^\circ ,
$$

where $\Delta G_{restr}^\circ$ is the free energy of *releasing* the decoupled ligand from its restraints into the standard volume (formula below). It is negative, so subtracting it makes the computed binding less favourable. Its size depends on the restraints you chose, and the restrained decoupling work in the site changes by the opposite amount, so only the sum of the two has a physical meaning. It is therefore not, by itself, the translational and rotational entropy that the ligand loses on binding ([Gilson et al. 1997](cite:gilson1997)). The complete formula of that paper has two more terms on the right-hand side. One is a symmetry term, $+k_BT\ln[\sigma_{PL}/(\sigma_P\sigma_L)]$, with $\sigma$ the symmetry numbers of complex, protein and ligand: a ligand with $\sigma_L$ equivalent orientations, restrained to one of them in an asymmetric site, binds more strongly than computed by $k_BT\ln\sigma_L$. The other is a pressure-volume term, which is negligible at 1 bar.

A decoupled ligand is an ideal-gas molecule. Without restraints it would wander through the whole box, so the end state would depend on the box volume and the result would have no defined standard state. The original "double annihilation" method had this flaw: it had no standard-state term, and Gilson et al. estimate that published values were too favourable by about 12 to 16 kJ/mol. Such runs also converge very slowly ([Gilson et al. 1997](cite:gilson1997)). So the ligand is held by **restraints** to the protein while it is decoupled. [Boresch et al. (2003)](cite:boresch2003) use one distance, two angles and three dihedrals between three atoms of the ligand and three of the protein, which fixes all six relative degrees of freedom. The free energy of releasing a non-interacting ligand from these restraints into the standard volume $V^\circ$ is analytical:

$$
\Delta G_{restr}^\circ = -k_BT\ln\left[\frac{8\pi^2V^\circ\sqrt{K_rK_{\theta_A}K_{\theta_B}K_{\phi_A}K_{\phi_B}K_{\phi_C}}}{r_0^2\,\sin\theta_{A,0}\,\sin\theta_{B,0}\,(2\pi k_BT)^3}\right],
$$

with $K$ the force constants and $r_0$, $\theta_{A,0}$, $\theta_{B,0}$ the reference values. For typical restraints the argument of the logarithm is about $10^5$, so $\Delta G_{restr}^\circ\approx-28$ kJ/mol ($-6.8$ kcal/mol). Sign conventions for this term differ between papers and programs (some report the free energy of *imposing* the restraints, which is the same number with the opposite sign and then enters with a plus), so check which direction your software reports. Absolute calculations are harder than relative ones: the errors of two large numbers do not cancel, and the protein must relax between the bound and the empty state.

## Non-equilibrium work relations

<div data-videos="nI3pHiPbxeg NeGjghk0im4 LXcQx6Bu3OQ gsq3irAz8Ok"></div>

Change $\lambda$ from 0 to 1 in a finite time and record the work $W=\int_0^1(\partial U/\partial\lambda)\,d\lambda$ along the trajectory. The second law says $\langle W\rangle\ge\Delta A$, with equality only for an infinitely slow change. [Jarzynski (1997)](cite:jarzynski1997) showed there is an exact equality for any switching speed:

$$
\boxed{\big\langle e^{-\beta W}\big\rangle = e^{-\beta\Delta A}}
$$

where the average is over many repetitions started from equilibrium in state A. The second law follows from Jensen's inequality. [Crooks (1999)](cite:crooks1999) gave the underlying relation between the work distributions of the forward process and its reverse:

$$
\frac{P_F(W)}{P_R(-W)} = e^{\beta(W-\Delta A)} .
$$

The two distributions cross at $W=\Delta A$. In practice the Jarzynski average has the same weakness as FEP: it is dominated by rare trajectories with unusually low work. It is reliable only when the spread $\sigma_W$ of the work values is of the order of $k_BT$ (for a Gaussian work distribution the dissipated work $\langle W\rangle-\Delta A$ equals $\sigma_W^2/2k_BT$). Using both directions with the Crooks relation (which leads to BAR applied to work values) is much better. Fast non-equilibrium switching between two equilibrium ensembles is the basis of some protein-mutation workflows (for example pmx), and the same relations apply to steered MD run with a stochastic thermostat from equilibrated starting points (Module 14).

## End-point methods

<div data-videos="Hy-Cc7nn2MY"></div>

MM/PBSA and MM/GBSA estimate binding free energy from MD snapshots, usually of the complex alone (the single-trajectory protocol, in which receptor and ligand are cut out of the same frames) and sometimes from separate simulations of complex, receptor and ligand: $\Delta G\approx\langle\Delta E_{MM}\rangle+\langle\Delta G_{solv}\rangle-T\Delta S$, where the solvation term comes from a continuum model (Module 15) and the entropy from a normal-mode or similar estimate. They are much cheaper than alchemical or PMF methods because they need no intermediate states. They are also much less reliable: the terms are large and nearly cancel, the entropy is crude, and results depend on the dielectric constant chosen. They can rank related compounds in favourable cases and should not be read as absolute free energies. Linear interaction energy (LIE) is another method in this class.

## Good practice

<div data-videos="cQQM1DTLR5g id5D_9PC1mA fxPNNVkSIWo zodHyKUyUbM"></div>

- Equilibrate each $\lambda$ window and discard the equilibration (Module 11).
- Use Hamiltonian replica exchange between $\lambda$ windows (Module 14).
- Inspect the overlap matrix and add windows where overlap is poor.
- Check convergence by computing $\Delta A$ from the first $x$ % and from the last $x$ % of the data as a function of $x$ (forward and reverse plots).
- For networks of relative calculations, check cycle closure: the sum around any closed loop should be zero within error.
- Report the estimator, the number of windows, the simulation time per window and the uncertainty with its method.
- Validate the whole protocol on a system with a known answer first. Hydration free energies of small molecules are the standard test.

Software: `alchemlyb` and `pymbar` for analysis; GROMACS, AMBER, OpenMM, NAMD and CHARMM all run the simulations; `pmx`, OpenFE, Perses and FEP+ automate set-up. The LiveCoMS review by [Mey et al. (2020)](cite:mey2020) is the reference for practice.

## Check yourself

<details markdown="1"><summary>1. Why is one-sided FEP from A to B biased when the perturbation is large?</summary>
The exponential average is dominated by configurations with low $U_B$, which are rare in the A ensemble. With a finite sample they are missed, the average of $e^{-\beta\Delta U}$ is underestimated, and $\Delta A$ is overestimated. The result looks converged because the missing configurations simply never appear.
</details>

<details markdown="1"><summary>2. In the relative binding cycle, why do you not need to simulate binding?</summary>
Free energy is a state function. The difference of the two horizontal legs equals the difference of the two vertical legs, and the vertical legs are alchemical changes at fixed binding state.
</details>

<details markdown="1"><summary>3. You pull a ligand out of its site 20 times and get a mean work of 180 kJ/mol with a standard deviation of 25 kJ/mol. Can you apply Jarzynski's equality directly?</summary>
Not usefully. A standard deviation of 25 kJ/mol is 10 $k_BT$. For a Gaussian work distribution the estimate would be $\langle W\rangle-\beta\sigma^2/2 = 180-125 = 55$ kJ/mol, but that value depends entirely on a tail that 20 samples do not contain. Pull more slowly, or use the pulling only to generate umbrella windows.
</details>

<details markdown="1"><summary>4. Why are charges turned off before Lennard-Jones interactions when decoupling a molecule?</summary>
If the Lennard-Jones core were removed first, oppositely charged atoms of the environment could approach a bare charge to zero distance, giving an infinitely negative Coulomb energy.
</details>

## Exercises

1. For two one-dimensional harmonic oscillators with force constants $k_A$ and $k_B$, compute $\Delta A$ analytically. Then estimate it by FEP in both directions, by TI and by BAR from sampled data, for $k_B/k_A$ = 1.5 and 20. Which estimators fail in which case?
2. Derive the second-order cumulant formula $\Delta A\approx\langle\Delta U\rangle-\tfrac{\beta}{2}\sigma^2$ and show it is exact when $\Delta U$ is Gaussian.
3. Compute the hydration free energy of methane or ethanol by decoupling it in water, following a published tutorial (for example the GROMACS free-energy tutorial). Analyse with `alchemlyb` using TI, BAR and MBAR, and compare with experiment.
4. Draw the thermodynamic cycle for the effect of a His to Ala mutation in a binder on its affinity for a target. List what could make the free-binder leg harder to converge than the complex leg.

## Read

{{READ}}

## Key papers

{{PAPERS}}
