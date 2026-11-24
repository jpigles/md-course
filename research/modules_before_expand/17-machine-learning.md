---
num: 17
title: Machine learning in molecular simulation
short: Machine-learned potentials
part: Part V · Beyond all-atom
hours: 7
summary: Understand how neural-network potentials are built and trained, how machine learning is used for coarse-graining and for generating equilibrium ensembles directly, and how to judge these tools with the statistics from the rest of the course.
videos: 16
papers: L
tags: ml-potentials
---

<div class="box goal" markdown="1">
#### After this module you can

- state the learning problem for an interatomic potential and the symmetries it must respect;
- describe descriptor-based (Behler-Parrinello, ANI) and message-passing (SchNet, NequIP, MACE) architectures;
- write the energy-and-force loss and explain why forces are the richer training signal;
- explain machine-learned coarse-graining as force matching with a neural network;
- explain what Boltzmann generators and diffusion-based ensemble emulators produce, and what they do not.
</div>

## Watch first

{{WATCH}}

## Where the classical force field falls short

<div data-videos="LInWiab7q6Q"></div>

Modules 5 and 6 described an energy function with a fixed, simple form. Its accuracy is limited by that form: no polarisation, no reactivity, a few thousand parameters shared across all chemistry. Quantum chemistry gives accurate energies and forces for any arrangement of atoms, but its cost grows steeply with system size, and even density functional theory is many orders of magnitude slower than a force field.

A **machine-learned interatomic potential** (MLIP) is a flexible function, usually a neural network, trained to reproduce quantum-mechanical energies and forces. The aim is quantum accuracy at a cost within a few orders of magnitude of a force field.

## The learning problem

<div data-videos="tWeBrPTrSDE 8DPSLDUsqbA"></div>

Find a function $E_\theta(\mathbf r_1,\dots,\mathbf r_N;Z_1,\dots,Z_N)$ of atomic positions and element types such that $E_\theta\approx E_{QM}$, with forces obtained by differentiation, $\mathbf F_i=-\partial E_\theta/\partial\mathbf r_i$, so that the force field is conservative by construction (automatic differentiation makes this free).

**Symmetries.** The energy must not change when the whole molecule is translated or rotated, or when two atoms of the same element are exchanged. Forces must rotate with the molecule (equivariance). A model that has to learn these from data wastes capacity and generalises poorly, so they are built into the architecture.

**Locality.** To scale to large systems and to transfer between molecules, almost all models write the energy as a sum of atomic contributions that depend only on the neighbourhood within a cutoff $r_c$ (typically 0.4 to 0.6 nm):

$$
E=\sum_{i=1}^{N}E_i\big(\{\mathbf r_j-\mathbf r_i,\ Z_j\}_{r_{ij}<r_c}\big).
$$

Cost is then linear in $N$. The weak point is anything beyond the cutoff: electrostatics and dispersion at long range are missing unless added explicitly.

## Architectures

### Descriptors plus a network

[Behler and Parrinello (2007)](cite:behler2007) introduced the template. Describe each atom's environment by a vector of **symmetry functions** that are invariant by construction, for example a radial function

$$
G_i^{rad}=\sum_{j\ne i}e^{-\eta\,(r_{ij}-r_s)^2}\,f_c(r_{ij}),
$$

for a set of widths $\eta$ and shifts $r_s$ (ANI uses one narrow $\eta$ and many evenly spaced $r_s$), where $f_c$ goes smoothly to zero at the cutoff, plus angular functions built from triples of atoms. Feed the vector to a small neural network that outputs $E_i$, the same network for every atom of one element (the 2007 paper treated only silicon, so a single network served all atoms). **ANI** ([Smith, Isayev and Roitberg 2017](cite:smith2017)) used a heavily modified version of this design, with neighbours resolved by element and shifted angular functions, for organic molecules made of H, C, N and O, trained on about 17 million conformations. Gaussian approximation potentials use related local-environment descriptors (the bispectrum originally, later SOAP) with kernel regression in place of a network.

### Message passing

Let the network learn the descriptors. Treat atoms as nodes of a graph, with edges between neighbours within the cutoff. Each atom carries a feature vector $\mathbf h_i$, updated in several rounds using messages from its neighbours:

$$
\mathbf h_i^{(t+1)}=\mathcal U\Big(\mathbf h_i^{(t)},\ \sum_{j\in\mathcal N(i)}\mathcal M\big(\mathbf h_i^{(t)},\mathbf h_j^{(t)},\mathbf r_{ij}\big)\Big),\qquad E=\sum_i\mathcal R\big(\mathbf h_i^{(T)}\big).
$$

**SchNet** ([Schütt et al. 2018](cite:schutt2018)) is the simplest case: the message from atom $j$ is its feature vector multiplied, element by element, by a learned function of the distance, so the features stay invariant. (SchNet itself used a cutoff only for crystals. Some later models, MACE among them, read the energy out from every layer and add the contributions.) After $T$ rounds an atom has received information from up to $T\times r_c$ away.

### Equivariant networks

<div data-videos="ZR1NTBPBDOo I9Y2le9e74A"></div>

Distances alone discard directional information, which then has to be recovered from many-body combinations. **Equivariant** networks carry features that are vectors and higher-rank tensors and that rotate with the molecule. Messages are built from spherical harmonics of the direction $\hat{\mathbf r}_{ij}$ and combined with tensor products that respect the rules for adding angular momenta. **NequIP** ([Batzner et al. 2022](cite:batzner2022)) showed that this gives high accuracy from far less training data: on water and ice it reached lower force errors with 133 training structures than an earlier neural network trained on 133,500, and on small molecules it matched or beat kernel methods, which were already data-efficient. **MACE** ([Batatia et al. 2022](cite:batatia2022)) builds higher body-order messages in each layer, which allows fewer layers and faster evaluation. These are the current standard, together with related designs (Allegro, which is strictly local and parallelises well).

## Training

<div data-videos="106sdeDF1oc"></div>

The loss combines energies and forces over a set of reference configurations:

$$
\mathcal L(\theta)=w_E\sum_{c}\big(E_\theta^{(c)}-E_{QM}^{(c)}\big)^2+w_F\sum_{c}\sum_{i=1}^{N_c}\big|\mathbf F_{\theta,i}^{(c)}-\mathbf F_{QM,i}^{(c)}\big|^2 .
$$

Each configuration supplies one energy but $3N$ force components, so forces carry most of the information and are usually weighted most.

**Data matter more than architecture.** A model is reliable only for the kinds of configurations it was trained on. Outside them it does not degrade gracefully: it can predict a deep, unphysical energy minimum and the simulation falls into it. Remedies:

- **Active learning.** Run MD with the current model, detect configurations where the model is uncertain (typically where an ensemble of models disagree), compute those with quantum chemistry, add them and retrain.
- **Stability tests.** A low error on a test set of forces does not guarantee stable dynamics. Always run long simulations and check distributions and conservation of energy.

**Cost and reach.** Even the fastest learned potentials are one to three orders of magnitude slower than a classical force field for the same system ([Unke et al. 2021](cite:unke2021)), and the accurate equivariant networks sit at the slow end. That limits routine use to small systems or short times, or to a hybrid in which only a region of interest (a ligand) is treated by the learned potential and the rest by a force field (ML/MM): with a 53-atom learned region the OpenMM developers report a slowdown of only 3 to 5 times ([Eastman et al. 2024](cite:eastman2024)). General-purpose pretrained models for organic and biological chemistry exist (the ANI family, AIMNet2, MACE-OFF and others). OpenMM ships ANI-1ccx and ANI-2x and runs other PyTorch models through a plug-in; LAMMPS runs several others.

**Long range.** Strictly local models miss electrostatics beyond the cutoff. Approaches include predicting atomic partial charges and adding an explicit Coulomb term (with an empirical dispersion correction), and learning a correction on top of a physical baseline.

<div class="widget" data-widget="nnfit"></div>

## Machine-learned coarse-graining

Module 15 showed that the ideal coarse-grained potential is the many-body PMF, and that force matching finds it in principle. Pair potentials are too restrictive to represent it. A neural network is not.

**CGnet** ([Wang et al. 2019](cite:wang2019b)) trains a network $U_\theta(\mathbf R)$ on atomistic trajectories by minimising the force-matching loss

$$
\mathcal L(\theta)=\Big\langle\big|-\nabla_{\mathbf R}U_\theta\big(\mathbf M(\mathbf r)\big)-\mathbf M_F\,\mathbf f(\mathbf r)\big|^2\Big\rangle,
$$

where $\mathbf M_F\,\mathbf f$ is the atomistic force projected on the coarse-grained sites. The instantaneous projected force is extremely noisy, since it fluctuates around the mean force, so a large amount of data is needed. A simple physical prior (bonded terms and a repulsion; in Majewski et al. also a term that fixes chirality) is added so that the model behaves sensibly in regions without data. [Majewski et al. (2023)](cite:majewski2023) trained one model on twelve small fast-folding proteins. It recovered the native structure of ten of them and of a few helical mutants, and its authors state that it should not be expected to work for other sequences. Transfer to proteins outside the training set came later, from training on far more diverse data (Module 18). The state-dependence problem of Module 15 remains: the learned free energy is for the temperature and conditions of the training data.

## Generating ensembles without running dynamics

MD produces equilibrium samples one correlated step at a time, and is slow because of barriers. Generative models try to draw independent samples from the Boltzmann distribution directly.

### Boltzmann generators

<div data-videos="WuXJRswYIaA JZjeFBH0Jl4"></div>

[Noé et al. (2019)](cite:noe2019). Train an invertible network (a normalising flow) $\mathbf x=f_\theta(\mathbf z)$ that maps a simple Gaussian variable $\mathbf z$ to molecular configurations. It is trained in two ways at once: by energy (a loss that needs only $U$ and pushes generated configurations towards low energy while keeping them spread out) and by example (maximum likelihood on a few known configurations of each state of interest). Training by energy alone collapses onto the most stable state. Because the map is invertible, the probability density of each generated configuration is known exactly:

$$
p_X(\mathbf x)=p_Z\big(f_\theta^{-1}(\mathbf x)\big)\,\left|\det\frac{\partial f_\theta^{-1}}{\partial\mathbf x}\right| .
$$

The generated distribution is only approximately Boltzmann, but since $p_X$ is known, each sample can be given the importance weight

$$
w(\mathbf x)\propto\frac{e^{-\beta U(\mathbf x)}}{p_X(\mathbf x)},
$$

and reweighted averages are then exact in principle, including free-energy differences between states that MD would rarely connect. In practice the weights are usable only when the model overlaps well with the target, the same overlap condition as in free-energy perturbation (Module 13).

### Diffusion and flow-matching emulators

<div data-videos="LStKhWcL0VE zaZAAWUISGE oZZumtlUXag"></div>

A newer family trains a diffusion or flow-matching model to output protein conformations for a given sequence, as structure-prediction networks output one structure. Training data are structures from the PDB and predicted-structure databases, large collections of MD trajectories, and in some cases experimental stabilities used to adjust the relative weights of folded and unfolded states. **BioEmu** ([Lewis et al. 2025](cite:lewis2025)) is a prominent example, and AlphaFlow and Distributional Graphormer are related systems. They generate thousands of statistically independent conformations in about a GPU-hour (the figure the BioEmu authors give), far less than the MD needed to sample the same ensemble.

What to keep in mind:

- They are **emulators**: the samples follow the distribution the model learned, with no exact reweighting to a physical energy function. Their errors are model errors of a new kind and must be measured against experiment or converged MD for the property you care about.
- They give **ensembles, not dynamics**: no time axis, so no rates or pathways.
- Most are trained on single chains under one set of conditions. Complexes, ligands, mutations far from the training distribution, pH and temperature dependence are active research questions, and performance there has to be tested, not assumed.

### Other uses

Learned collective variables for enhanced sampling (Module 14), VAMPnets for kinetic models (Module 16), differentiable simulation engines that allow force-field parameters to be optimised through the trajectory, and surrogate models that predict the outcome of a free-energy calculation.

## How to evaluate any of these tools

The standards of the rest of this course apply unchanged:

1. **What is the reference?** A learned potential is at best as good as its training data: the quantum method for an MLIP, the atomistic force field for a learned coarse-grained model, the trajectory set for an emulator.
2. **Is the test out of distribution?** Performance on molecules or proteins similar to the training set says little about new ones.
3. **Are the statistics sound?** Independent repeats, uncertainty estimates, convergence (Module 11).
4. **Does it reproduce an observable, not just a loss value?** Densities, radial distribution functions, free-energy differences, experimental data.
5. **What is the cost, counted honestly**, including training and data generation?

## Check yourself

<details markdown="1"><summary>1. Why are forces obtained as the gradient of a learned energy instead of being predicted directly by the network?</summary>
A force field that is the gradient of a scalar energy is conservative: the work around any closed path is zero and energy is conserved in MD. Directly predicted forces are generally not the gradient of any function, and simulations with them gain or lose energy. (Some recent models do predict forces directly for speed and accept this.)
</details>

<details markdown="1"><summary>2. A model reaches a very low force error on its test set but the MD simulation explodes after 50 ps. How can both be true?</summary>
The test set comes from the same distribution as the training set. During MD the system drifted into configurations outside it (a slightly compressed bond, an unusual contact), where the model extrapolates without constraint. Test error measures interpolation. Stability requires coverage, which active learning supplies.
</details>

<details markdown="1"><summary>3. What makes a Boltzmann generator "exact" where a diffusion-based emulator is not?</summary>
The Boltzmann generator provides the probability density of every sample it draws, and a physical energy function $U$ is available, so each sample can be reweighted by $e^{-\beta U}/p_X$. An emulator trained on data has no target energy function to reweight against and, depending on the model type, no cheap exact density.
</details>

<details markdown="1"><summary>4. Why is the training signal in force-matching coarse-graining so noisy?</summary>
For a fixed coarse-grained configuration $\mathbf R$, many atomistic configurations (different solvent positions, side-chain orientations) map to it, each with a different instantaneous force. The target is their average, the mean force, but each training example supplies one instantaneous value that scatters around the mean force. This scatter is an irreducible noise term: the loss never reaches zero, and a lot of data is needed to average it out.
</details>

## Exercises

1. Fit a small neural network to the energy of a one-dimensional double well from 20 samples. Compare the predicted forces from differentiating the network with the exact ones, inside and outside the range of the training data.
2. Using a pretrained general-purpose potential available in OpenMM-ML, run a short gas-phase simulation of a small neutral molecule made of elements the model supports, and compare the distribution of one dihedral angle with the same simulation using GAFF2 or OpenFF.
3. For a one-dimensional double well, train a model on samples from overdamped Langevin dynamics by force matching with added noise on the forces. How does the error in the learned free energy scale with the number of samples?
4. Generate an ensemble for a small protein with an ensemble emulator and for the same protein with MD. Compare per-residue RMSF, radius of gyration and secondary-structure content, with error bars on the MD values. Where do they disagree, and which do you believe?

## Read

{{READ}}

## Key papers

{{PAPERS}}
