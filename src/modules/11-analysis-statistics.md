---
num: 11
title: Analysing trajectories and putting error bars on the results
short: Analysis and statistics
part: Part III · Practice
hours: 8
summary: Compute the standard structural and dynamical observables, and above all estimate their statistical uncertainty from correlated data.
videos: 11
tags: analysis-errors
---

<div class="box goal" markdown="1">
#### After this module you can

- compute RMSD, RMSF, radius of gyration, radial distribution functions, hydrogen bonds and contacts, and say what each means;
- get a diffusion coefficient from the mean squared displacement and correct it for box size;
- compute an autocorrelation time, the number of independent samples and a standard error by block averaging;
- decide how much of a trajectory to discard as equilibration;
- run a principal component analysis and avoid its best-known pitfall.
</div>

## Watch first

{{WATCH}}

## Before any analysis

Two bookkeeping steps come first. **Make molecules whole and centre the solute**: periodic wrapping splits molecules across the box in the raw trajectory, and distances computed on such frames are wrong. **Remove overall rotation and translation** by least-squares fitting each frame to a reference when you want internal motion. The tools are `gmx trjconv`, MDAnalysis transformations, or `cpptraj autoimage`.

## Structural observables

**RMSD**, the root mean square deviation from a reference structure after optimal superposition:

$$
\mathrm{RMSD}(t) = \min_{\mathbf R,\mathbf t}\sqrt{\frac1N\sum_{i=1}^N\big|\mathbf R\,\mathbf r_i(t)+\mathbf t-\mathbf r_i^{ref}\big|^2}.
$$

The optimal rotation $\mathbf R$ comes from the singular value decomposition of the $3\times3$ covariance matrix of the two centred coordinate sets (the Kabsch algorithm). RMSD compresses 3N coordinates into one number: two very different structures can have the same RMSD from the reference. A plateau in RMSD shows the structure stopped drifting away from the start. It does not show that sampling has converged.

**RMSF**, the fluctuation of each atom about its mean position, $\mathrm{RMSF}_i = \sqrt{\langle|\mathbf r_i-\langle\mathbf r_i\rangle|^2\rangle}$. It shows which parts are flexible, and compares with crystallographic B-factors through $B_i = \tfrac{8\pi^2}{3}\mathrm{RMSF}_i^2$.

**Radius of gyration**, the overall size:

$$
R_g^2 = \frac{\sum_im_i|\mathbf r_i-\mathbf r_{cm}|^2}{\sum_im_i}.
$$

The main observable for disordered proteins, directly comparable with SAXS.

**Contacts and hydrogen bonds.** A contact is usually a pair of heavy atoms closer than 0.45 nm, or C$\alpha$ atoms closer than 0.8 nm. A hydrogen bond is counted by geometry: donor-acceptor distance below 0.35 nm and hydrogen-donor-acceptor angle below 30°. The **fraction of native contacts** $Q$ is the fraction of contacts present in a reference structure that are formed in a frame, and is the standard coordinate for folding and binding.

**Solvent-accessible surface area**, **secondary structure** (DSSP), and specific distances and dihedral angles complete the usual set.

### Radial distribution function

For particles of types A and B, $g_{AB}(r)$ is the density of B at distance $r$ from an A, divided by the bulk density of B:

$$
g_{AB}(r) = \frac{\langle n_B(r,r+dr)\rangle}{4\pi r^2\,dr\;\rho_B}.
$$

It tends to 1 at large $r$. Peaks are solvation shells. The integral up to the first minimum gives the coordination number, $n = 4\pi\rho_B\int_0^{r_{min}}g(r)\,r^2dr$. And $w(r) = -k_BT\ln g(r)$ is the potential of mean force between the two species (Module 3). $g(r)$ is measured by X-ray and neutron scattering, which makes it a primary test of water and ion models.

## Dynamical observables

**Diffusion.** The mean squared displacement grows linearly at long times (Einstein relation):

$$
\mathrm{MSD}(t) = \big\langle|\mathbf r(t_0+t)-\mathbf r(t_0)|^2\big\rangle \;\to\; 6Dt .
$$

Fit the linear part, not the short-time ballistic part. Equivalently, by the Green-Kubo relation, $D = \tfrac13\int_0^\infty\langle\mathbf v(0)\cdot\mathbf v(t)\rangle\,dt$. Use unwrapped coordinates.

Diffusion in a periodic box is slowed by hydrodynamic interaction with the periodic images. For a cubic box of edge $L$ and solvent viscosity $\eta$ (Yeh and Hummer 2004):

$$
D_\infty = D_{PBC} + \frac{2.837\,k_BT}{6\pi\eta L}.
$$

For water in a 3 nm box the correction is more than 10 %.

**Time correlation functions.** For any observable, $C_{AA}(t)=\langle\delta A(0)\,\delta A(t)\rangle$ with $\delta A = A-\langle A\rangle$. Their decay gives relaxation times, and their integrals give transport coefficients. The rotational correlation function of N-H bond vectors gives NMR order parameters $S^2$.

## Statistical error: the part most often done wrong

A trajectory of $N$ frames is not $N$ independent measurements. Frames close in time are similar. The quantity that tells you how similar is the normalised autocorrelation function

$$
c(t) = \frac{\langle\delta A(0)\,\delta A(t)\rangle}{\langle\delta A^2\rangle},
$$

which starts at 1 and decays to 0. Its integral is the **integrated autocorrelation time** $\tau_{int}=\int_0^\infty c(t)\,dt$. With frames saved every $\Delta t_s$, define the **statistical inefficiency**

$$
g = 1+\frac{2\tau_{int}}{\Delta t_s},\qquad N_{eff} = \frac{N}{g},\qquad
\boxed{\mathrm{SE}(\bar A) = \frac{\sigma_A}{\sqrt{N_{eff}}}\approx\sigma_A\sqrt{\frac{2\tau_{int}}{T_{sim}}}}
$$

The last form shows what matters: the error depends on the simulated time in units of the correlation time, not on how many frames you saved. A 100 ns trajectory of an observable with $\tau_{int}$ = 10 ns contains about five independent samples, whether you stored 1,000 frames or 1,000,000.

### Block averaging

The practical method (Flyvbjerg and Petersen 1989). Cut the series into $M$ consecutive blocks, average within each block, and treat the block averages as independent:

$$
\mathrm{SE}_{block} = \frac{s(\text{block means})}{\sqrt M}.
$$

Repeat for increasing block length. While blocks are shorter than the correlation time, the estimate rises. When it reaches a plateau, the blocks are independent and the plateau value is the standard error. **If there is no plateau before you run out of blocks, the simulation is too short to give an error estimate**, and the mean itself cannot be trusted.

```python
import numpy as np

def block_average(a, n_blocks_list=(5, 10, 20, 40, 80, 160)):
    """Standard error of the mean of a correlated series, for several block counts."""
    a = np.asarray(a, float)
    out = []
    for nb in n_blocks_list:
        m = len(a) // nb                         # samples per block
        means = a[: m * nb].reshape(nb, m).mean(axis=1)
        out.append((m, means.std(ddof=1) / np.sqrt(nb)))
    return out                                    # list of (block length, standard error)

def statistical_inefficiency(a):
    """g = 1 + 2 tau / dt, summing the autocorrelation function up to its first zero."""
    a = np.asarray(a, float) - np.mean(a)
    n, var, g = len(a), np.var(a), 1.0
    for t in range(1, n // 2):
        c = np.dot(a[:-t], a[t:]) / ((n - t) * var)
        if c <= 0.0:
            break
        g += 2.0 * c * (1.0 - t / n)
    return g
```

### Independent repeats

The most reliable error bar comes from several independent simulations: compute the observable in each, and report the mean and the standard error across runs. Repeats also catch something no single-trajectory analysis can: a run that is trapped in a different state. If three runs give 12.1, 12.3 and 17.8, you have learned that there are at least two long-lived states and that none of the runs has sampled the transition between them.

### Equilibration: what to discard

The start of a production run still remembers its preparation. Including it biases the average. Discarding too much wastes data. A principled choice (Chodera 2016): for each candidate cut-off time $t_0$, compute the number of effectively independent samples $N_{eff}(t_0)$ in the remainder, and choose the $t_0$ that maximises it. In practice also look at the time series, and check that the result does not change when you discard twice as much.

<div class="box warn" markdown="1">
**You cannot prove convergence.** Every test above detects correlation on time scales shorter than the trajectory. A process slower than the trajectory is invisible: all observables look flat and well converged within one state. Protect yourself with independent repeats from *different* starting structures, with physical knowledge of what the slow processes are likely to be, and by stating clearly what the simulation length can and cannot support.
</div>

## Collective motions: principal component analysis

After fitting to a reference, build the covariance matrix of atomic positions,

$$
C_{ab} = \big\langle(x_a-\langle x_a\rangle)(x_b-\langle x_b\rangle)\big\rangle,
$$

and diagonalise it. The eigenvectors with the largest eigenvalues are the directions of largest fluctuation, and a handful usually account for most of the motion ("essential dynamics"). Projecting the trajectory on the first two gives a map of the conformations visited.

The pitfall: a random walk in high dimensions, that is an unconverged simulation, produces first principal components that look like smooth half-cosines in time, and a projection that looks like a meaningful U-shaped pathway. Hess (2000, 2002) showed this and proposed the cosine content as a test. If your first component is a cosine of period twice the trajectory length, you are looking at diffusion, not at a functional motion.

Time-lagged independent component analysis (TICA, Module 16) is the related method that finds the *slowest* rather than the largest motions.

## Free-energy surfaces from histograms

If a trajectory samples the equilibrium distribution, the free energy along any coordinate is $F(\xi) = -k_BT\ln P(\xi)$, from a histogram. This is only valid where transitions between the regions have been sampled many times. A beautiful two-dimensional free-energy map made from a single trajectory that crossed the barrier once is a picture of one trajectory. Modules 12 and 14 give the methods for the case that matters.

## Comparing with experiment

| Experiment | What to compute |
|---|---|
| NMR scalar couplings $^3J$ | Karplus relation $J(\phi) = A\cos^2\theta+B\cos\theta+C$ averaged over the trajectory |
| NMR relaxation, order parameters $S^2$ | Long-time limit of the bond-vector rotational correlation function |
| NMR chemical shifts | Empirical predictors (SPARTA+, SHIFTX2) applied per frame, then averaged |
| NOE distances | $\langle r^{-6}\rangle^{-1/6}$, which is dominated by the shortest distances |
| SAXS | Scattering curve per frame (CRYSOL, Pepsi-SAXS), then averaged; or $R_g$ |
| FRET efficiency | Average of $1/[1+(r/R_0)^6]$ over the distance distribution |
| Crystallographic B-factors | RMSF (remembering that crystals also contain static disorder) |

Average the **observable**, not the structure: experimental signals are non-linear in the coordinates.

## Tools

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms

u = mda.Universe("md.tpr", "md.xtc")            # topology + trajectory
ref = mda.Universe("md.tpr", "npt.gro")          # reference structure
R = rms.RMSD(u, ref, select="backbone").run()    # fit and compute per frame
time_ps, rmsd_A = R.results.rmsd[:, 1], R.results.rmsd[:, 2]

ca = u.select_atoms("name CA")
rg = [ca.radius_of_gyration() for ts in u.trajectory]
```

MDAnalysis and MDTraj are the two general Python libraries. The GROMACS tools (`gmx rms`, `rmsf`, `gyrate`, `rdf`, `hbond`, `msd`, `energy`, `analyze -ee` for block averaging) and AMBER's `cpptraj` cover the standard analyses. VMD, PyMOL, ChimeraX and NGLview display trajectories: always watch the trajectory before trusting any number computed from it.

## Check yourself

<details markdown="1"><summary>1. A 200 ns trajectory was saved every 10 ps. The radius of gyration has a standard deviation of 0.10 nm and an integrated autocorrelation time of 5 ns. What is the standard error of its mean?</summary>
$N = 20{,}000$ frames, $g = 1+2\times5000/10 = 1001$, $N_{eff}\approx20$. SE $=0.10/\sqrt{20} = 0.022$ nm. The naive $0.10/\sqrt{20000} = 0.0007$ nm is too small by a factor of 32.
</details>

<details markdown="1"><summary>2. The backbone RMSD levels off at 0.2 nm after 20 ns. Is the simulation converged?</summary>
It shows only that the distance from the starting structure stopped increasing. Many different conformations lie at 0.2 nm from the start, and slow transitions between them, or to states further away, may not have occurred. Check observables relevant to your question, their block-averaged errors, and independent repeats.
</details>

<details markdown="1"><summary>3. Why should you compute a NOE-derived distance as ⟨r⁻⁶⟩^(−1/6) and not as ⟨r⟩?</summary>
The NOE intensity is proportional to $r^{-6}$, and the experiment averages the intensity. Two protons that are close for 10 % of the time give a strong NOE even if their mean distance is large.
</details>

<details markdown="1"><summary>4. Block averaging gives standard errors of 0.8, 1.5, 2.6 and 3.9 kJ/mol for blocks of 1, 5, 20 and 50 ns in a 200 ns run. What do you conclude?</summary>
There is no plateau: the error estimate is still growing at the longest block length for which you have a few blocks. The correlation time is comparable with or longer than the run, and neither the mean nor its error is reliable. Run longer or use enhanced sampling.
</details>

## Exercises

1. For the simulation from Module 10, compute backbone RMSD, per-residue RMSF and radius of gyration. Compare RMSF with the B-factors in the PDB file.
2. Compute the oxygen-oxygen radial distribution function of the water and the coordination number of the first shell. Compare the peak positions with the experimental values (first peak near 0.28 nm).
3. Apply `block_average` and `statistical_inefficiency` to the potential energy, the radius of gyration and one side-chain dihedral angle. Which converges fastest, and why?
4. Generate a 1,000-dimensional random walk of 10,000 steps, run PCA on it, and plot the projections on the first three components against time. Compare with cosines.
5. Compute the diffusion coefficient of water from your trajectory, apply the finite-size correction, and compare with experiment.

## Read

{{READ}}
