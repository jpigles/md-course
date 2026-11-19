---
num: 18
title: Machine-learning models trained on MD data, the state of the art
short: ML trained on MD: state of the art
part: Part V · Beyond all-atom
hours: 7
summary: Know what the current models were actually trained on, what each kind of model needs from a simulation data set to work, and what has and has not been demonstrated, with every claim tied to the paper it comes from.
papers: N
tags: ml-potentials
---

<div class="box goal" markdown="1">
#### After this module you can

- sort any "AI for MD" model into one of four kinds by asking what its training label is;
- name the main MD data sets, with their size, force field and what they store;
- state, with numbers, what the evidence says a model needs: which labels, how many systems, how much sampling, which priors;
- list what has not been shown, in particular for protein-protein binding and for designed proteins;
- plan a simulation data set that a model could later be trained on.
</div>

<div class="box key" markdown="1">
**How this module was written.** Unlike Modules 1 to 17, this one was written from the papers themselves. About 75 papers and data-set descriptions were located and their identity checked against Crossref, arXiv or bioRxiv; 33 were read in full, 38 in part (main text, methods and the data appendices), and 4 only as an abstract or a model card. Every number below comes from one of them and carries its citation. Where a paper was read as a preprint, the published version may differ. The field moves quickly: this is the state in November 2026.
</div>

## Four kinds of model, told apart by their label

"Trained on MD" covers four different things. The useful question is: **what was the training label?**

| Kind | Label taken from the simulation | What the model outputs | Example |
|---|---|---|---|
| 1. Learned coarse-grained force field | The **forces** on the atoms, projected onto beads | An energy function for coarse-grained MD | CGnet, CGSchNet |
| 2. Ensemble or trajectory generator | The **frames** themselves (coordinates), sometimes ordered in time | Conformations, without running MD | AlphaFlow, BioEmu |
| 3. Predictor that uses MD as a feature or a label | A **summary** of the trajectory (flexibility, contact occupancy) | Something else: flexibility, affinity, a structure | Flexpert, Dynaformer, Boltz-2 |
| 4. Atomistic potential trained on quantum chemistry | **Quantum energies and forces** of configurations that MD supplied | An all-atom energy function | ANI, MACE-OFF |

Kind 4 is not trained on MD in the strict sense: classical or semi-empirical MD only supplies the configurations, and quantum chemistry labels them. It is included because it is what most people mean by a "machine-learned force field" (Module 17).

## The data sets

A model can be no better than its data, so start here.

| Data set | Systems | Total time | Per system | Force field, temperature | Stores | Used by |
|---|---|---|---|---|---|---|
| ATLAS ([Vander Meersche et al. 2024](cite:atlas)) | 1,390 protein chains | about 0.42 ms | 3 × 100 ns | CHARMM36m, TIP3P, 300 K | Coordinates | AlphaFlow, MDGen, aSAM, BBFlow, Boltz-2, flexibility predictors |
| mdCATH ([Mirarchi et al. 2024](cite:mdcath)) | 5,398 CATH domains | 62.6 ms | up to 500 ns × 5 replicas × 5 temperatures | CHARMM22\*, TIP3P, 320 to 450 K | Coordinates **and forces** | aSAMt, Boltz-2, learned force fields |
| MISATO ([Siebenmorgen et al. 2024](cite:misato_2024)) | 16,972 protein-ligand complexes | over 0.17 ms | 10 ns (8 ns stored) | ff14SB, GAFF2, 300 K | Coordinates, energy terms | Boltz-2, affinity models |
| PLAS-20k ([Korlepara et al. 2024](cite:plas20k_2024)) | 19,500 protein-ligand complexes | about 0.39 ms | 5 × 4 ns | ff14SB, GAFF2, 300 K | Coordinates, MM/PBSA terms | Affinity models |
| GPCRmd ([Rodríguez-Espigares et al. 2020](cite:gpcrmd2020)) | 191 systems at first release | 0.41 ms | 3 × 500 ns | see its protocol | Coordinates | DiG |
| D. E. Shaw fast folders | 12 small proteins | 8.2 ms | long trajectories, each with about ten folding events | CHARMM22\*, protein-specific temperatures | Coordinates, on request | ITO, BioEmu, tests of many models |
| BioEmu corpus ([Lewis et al. 2025](cite:lewis2025)) | 24,062 systems | 172 ms | varies | Amber family, about 300 K | Frames | BioEmu |
| Dynamic PDB ([Liu et al. 2024](cite:dynamicpdb2024)) | 12,643 chains | about 12.6 ms | 1 µs | ff14SB, 300 K | Coordinates, velocities **and forces** | Trajectory models |

Three things to notice. Almost every set is of **single chains or protein-ligand complexes**: there is no large public MD set of protein-protein complexes. Most runs are **short**, 10 to 500 ns, so they describe fluctuations around the starting structure. And only two sets store **forces**, which matters for the first kind of model.

## Kind 1: learned coarse-grained force fields

<div data-videos="106sdeDF1oc"></div>

The idea is the force matching of Module 15 with a neural network as the energy function ([Wang et al. 2019](cite:wang2019b)). Its history is a lesson in what the label demands.

**The label is noisy, and that sets the amount of data.** For one coarse-grained configuration there are many atomistic ones, each with a different force, so the projected force scatters widely around the mean force the model must learn. The noise can be an order of magnitude larger than the signal ([Krämer et al. 2023](cite:kramer2023_optimalforce)). Plain force matching needs of the order of a million force-labelled frames, about 190 µs of MD, for a single miniprotein. Most of the progress since 2023 is in reducing that noise:

| Idea | Gain in data efficiency | Source |
|---|---|---|
| Better way of projecting forces onto beads | about 3 times | [Krämer et al. 2023](cite:kramer2023_optimalforce) |
| Forces generated by a flow model trained on the frames | about 70 times, for chignolin | [Köhler et al. 2023](cite:kohler2023_flowmatching) |
| Forces combined with a denoising objective | up to about 100 times | [Durumeric et al. 2026](cite:durumeric2026_forcesnoise) |
| Mean forces from constrained simulations | 375 times fewer labels for the same test loss | [Park et al. 2026](cite:park2026_meanforce) |

**Forces must be saved during the run.** Training sets for these models store the instantaneous forces on the protein atoms ([Majewski et al. 2023](cite:majewski2023); [Charron et al. 2025](cite:charron2025)). The D. E. Shaw trajectories and ATLAS have none, which is why mdCATH advertises its forces as a distinguishing feature.

**Diversity of systems matters more than converged sampling of each.** A model trained on converged folding simulations of 12 fast-folding proteins could not stabilise proteins outside that set, and its authors say it should not be expected to ([Majewski et al. 2023](cite:majewski2023)). A model trained on simulations of about 50 CATH domains that only sample their folded state, plus 1,245 umbrella-sampled dimer systems that show it what close contacts cost, folds proteins it never saw ([Charron et al. 2025](cite:charron2025)). The comparison is not clean, since resolution and architecture also differ, but volume still counts: with 10 % or 50 % of the same data, no folded test protein was stable.

**A physics prior is needed.** Without simple bonded and repulsive terms, the network explores regions where it has no data and the simulation produces unphysical structures or explodes. The network learns a many-body correction on top of the prior, and pair potentials alone cannot fold even chignolin ([Wang et al. 2019](cite:wang2019b)).

**Low test error does not mean a good model.** In both coarse-grained and atomistic work, validation loss fails to predict whether a simulation is stable or gives the right free energies; models have to be chosen by running them ([Majewski et al. 2023](cite:majewski2023); [Fu et al. 2023](cite:fu2023forces)).

**Limits that the papers state themselves.** The model is valid only at the temperature it was trained at. It gives thermodynamics, not kinetics: coarse-grained time is not physical time. Per step it is slower than classical all-atom MD on the same hardware, by one to two orders of magnitude in one report; the gain, where it has been quantified, is 42 to 1,144 times fewer steps per independent sample for four small proteins ([Charron et al. 2025](cite:charron2025)). And the training data of the transferable model contain no protein-protein complexes.

## Kind 4: atomistic potentials trained on quantum chemistry

<div data-videos="tWeBrPTrSDE I9Y2le9e74A ZR1NTBPBDOo"></div>

These were introduced in Module 17. What the papers add:

- **Where the configurations come from.** Classical MD at 300 and 500 K for the SPICE set behind MACE-OFF ([Kovács et al. 2025](cite:maceoff_2025)); semi-empirical MD and metadynamics for AIMNet2 ([Anstine et al. 2025](cite:aimnet2_2025)); short restrained classical MD of fragments of PDB structures for the biomolecular part of OMol25 ([Levine et al. 2025](cite:omol25)).
- **Speed.** Every measurement in the papers read puts these models below classical MD in steps per day: 4 to 70 times slower in most measurements, depending on the model and the test, and more in some ([Kovács et al. 2025](cite:maceoff_2025); [Zaverkin et al. 2025](cite:zaverkin2025)).
- **Stability.** Failures appear suddenly, sometimes after hundreds of picoseconds of apparently healthy dynamics, and a force error below 1 meV/Å did not prevent one model from failing after 25 ps ([Fu et al. 2023](cite:fu2023forces)). Published protein demonstrations are short: one to two nanoseconds for crambin with MACE-OFF, at most 10 ns in AI2BMD ([Wang et al. 2024](cite:ai2bmd2024)).
- **Long-range interactions and solvent** are mostly delegated to a classical model or left out. OMol25 calls binding free energies out of scope.
- **Read the method behind a headline.** AI2BMD's agreement with experimental folding free energies and melting temperatures was obtained by re-evaluating conformations sampled with a classical force field, not from ensembles the learned potential sampled itself.

A related and more modest use of machine learning is to assign the parameters of an ordinary classical force field from quantum data ([Takaba et al. 2024](cite:espaloma03); [Seute et al. 2025](cite:grappa2025)). The result runs at classical speed. So far only the bonded terms are learned; the Lennard-Jones parameters and the charge model, which govern binding, are inherited.

## Kind 2: models that generate ensembles

<div data-videos="zaZAAWUISGE LStKhWcL0VE JZjeFBH0Jl4"></div>

| Model | Trained on | Output | Main evidence | Stated limit |
|---|---|---|---|---|
| AlphaFlow ([Jing et al. 2024](cite:alphaflow2024)) | AlphaFold weights, then PDB, then ATLAS (1,265 proteins × 300 frames) | All-atom ensembles | Per-residue flexibility correlates 0.85 with MD on 82 held-out proteins | Nothing slower than the 100 ns of ATLAS |
| BioEmu ([Lewis et al. 2025](cite:lewis2025)) | Predicted structures, then 172 ms of MD, then about 776,000 measured stabilities | Backbone ensembles for one chain | Free-energy error near 0.9 kcal/mol on 17 held-out domains | Single chains, one temperature, no ligands |
| aSAMt ([Janson et al. 2025](cite:asam2025)) | mdCATH, all five temperatures | Heavy-atom ensembles at a chosen temperature | Approaches held-out MD replicas on 90 test domains | Does not reproduce the Boltzmann weights of MD |
| BBFlow ([Wolf et al. 2025](cite:bbflow2025)) | ATLAS only, conditioned on a starting structure | Backbone ensembles | Flexibility correlation 0.90 on ATLAS, 0.84 on designed proteins | Cannot reach states far from the starting structure |
| idpSAM ([Janson and Feig 2024](cite:idpsam2024)) | Implicit-solvent ensembles of 3,259 disordered regions | C$\alpha$ ensembles of disordered peptides | Matches its training force field closely | Inherits that force field's error against experiment |
| Timewarp, ITO, MDGen ([Klein et al. 2023](cite:timewarp2023); [Schreiner et al. 2023](cite:ito2023); [Jing et al. 2024](cite:mdgen2024)) | Time-ordered trajectories of peptides or a few small proteins | Large time steps or whole trajectories | Kinetics of unseen tetrapeptides; folding times within about a factor of 3 for four mini-proteins | Not shown for proteins of ordinary size |
| Boltzmann generators ([Noé et al. 2019](cite:noe2019); [Klein and Noé 2024](cite:tbg2024)) | An energy function plus a few samples | Samples with exact weights | Transfer across dipeptides | Has not scaled beyond small systems |

What the evidence across these papers says:

1. **A structure prior is needed.** Removing the PDB stage from AlphaFlow lowered its agreement with MD (a correlation of 0.48 fell to 0.29). BioEmu found that pretraining on predicted structures chosen to show several conformations per sequence beat pretraining on the PDB.
2. **MD adds what static structures lack.** A model trained on PDB structures alone matches the distributions of only about 0.1 to 1 µs of MD on the fast folders ([Lu et al. 2024](cite:str2str2024)), and a PDB-trained model makes disordered proteins too compact until it is fine-tuned on simulated ensembles.
3. **The number of different systems drives transfer.** idpSAM is poor below about 500 training sequences and improves sharply up to about 1,000. BioEmu's free-energy error falls as its training domains go from 1 % to 10 % to 100 %.
4. **Short MD teaches which states exist, not how populated they are.** aSAMt finds the right basins of the fast folders but not their free energies, because 500 ns runs contain few transitions. BioEmu corrects its training frames with Markov models or with measured stabilities for this reason.
5. **A model inherits the force field of its data.** idpSAM reproduces its training simulations (radius of gyration within 0.06 nm) and therefore their error against experiment (0.70 nm). aSAMt's melting temperatures are about 130 K too high.
6. **Knowing the starting structure carries most of the short-time signal.** With the structure as input, a model trained from scratch on ATLAS matches one built on AlphaFold.
7. **Rare and distant states are the common failure.** BioEmu finds only 49 % of the open "apo" forms of cryptic pockets. Models trained on 100 ns data miss conformations that the longer reference runs visit.

<div class="box warn" markdown="1">
**If you design proteins, read this one twice.** On 50 computationally designed proteins, the two models that rely on evolutionary information predicted unstable conformations: flexibility errors of 4.2 Å (BioEmu) and 4.8 Å (AlphaFlow without a template), against 0.26 Å for the structure-conditioned BBFlow ([Wolf et al. 2025](cite:bbflow2025)). Designed sequences have no homologues, so a model that learned from families has little to go on. Flexibility predictors built on protein language models show the same drop on designed backbones ([Viliuga et al. 2026](cite:backflip2)). Test any such tool on designs before trusting it on yours.
</div>

## Kind 3: MD as a feature or a label for something else

**Flexibility.** This is the clearest case where MD data add information. The same network scores 0.76 to 0.78 against MD flexibility when trained on MD, and 0.47 to 0.56 when trained on crystallographic B-factors ([Kouba et al. 2025](cite:flexpert)). Two cautions: two MD replicas of the same protein agree only to about 0.88, which is the ceiling, and a parameter-free elastic network model already reaches 0.76 to 0.79. The headroom for learning is a few hundredths.

**Binding affinity of small molecules.** When the same model is trained with and without the MD ingredient, the gain in correlation with experiment is small: +0.03 ([Min et al. 2024](cite:dynaformer_2024)), +0.06 ([Wu et al. 2022](cite:protmd_2022)), and +0.02 to +0.03 with none at all on a random split ([Poziemski et al. 2026](cite:mdts_2026)). That last study also found that features from 20 ns of MD worked better than from 200 ns, and that a model given no information about the protein reached 0.52 where the full model reached 0.60. Most published numbers in this area report no such control.

**Structure prediction.** Boltz-2 mixes three MD sets into its training with small weights, supervises on distance distributions and on B-factors computed from MD, and adds a switch asking for "MD-like" output ([Passaro et al. 2025](cite:boltz2)). The measured effect is better agreement with MD flexibility. Its authors report no model trained without MD, so there is no evidence that MD improved its structures or its affinity predictions.

**Protein-protein affinity.** One study uses MD flexibility as an extra training target for protein-protein and protein-peptide affinity and gains 0.07 in correlation, with trajectories available for only 383 of about 12,000 complexes ([Bogdanova et al. 2026](cite:hybindnn)). In the same model, removing the protein language model costs about thirty times more.

## What a model needs, in one list

1. **Decide the label before you simulate.** Forces for a force field (write them out during the run). Frames for a generator. A trajectory summary for a predictor. Time-ordered frames at short intervals if kinetics is the goal.
2. **Many different systems, before long simulations of a few.** Every data-scaling result above points the same way.
3. **Enough sampling per system for the claim you want.** Fluctuations need about 100 ns. Populations need many transitions, or reweighting with a Markov model or with experimental data.
4. **Deliberate coverage of what equilibrium runs rarely visit.** Close contacts, distorted geometries, high temperatures. Without them, models have no reason to avoid those regions.
5. **A prior that carries the physics you already know.** Simple bonded and repulsive terms for a force field, a structure-prediction model for a generator, conservative forces for any potential.
6. **One consistent protocol, written down.** The model will reproduce the force field, temperature and conditions of its data, including their errors, and will not transfer to other conditions.
7. **Evaluation that could fail.** Run the model and look at observables, not only at the loss. Compare with the agreement between two MD replicas, and with a cheap baseline (an elastic network, a ligand-only model). Split the data by sequence similarity. Test on the kind of protein you will use it for.
8. **An ablation.** If you claim that MD helps, train the same model without it.

## What has not been shown

As of the papers read:

- No learned force field or atomistic potential has been trained on, or tested for, **protein-protein binding thermodynamics**.
- No ensemble generator has been validated for **complexes**. BioEmu's first version is single-chain; a second version announced in October 2026 lists complexes and ligands in its description, but no paper or evaluation was found.
- **Kinetics** have been tested only for peptides and four mini-proteins.
- No paper separates the effect of total simulation time from the number of systems, for proteins.
- None of the affinity studies read reports a statistical test on the difference between a model with and without MD.
- Claims that MD lets a model "learn the entropy of binding" are made in several papers and tested in none.

## Check yourself

<details markdown="1"><summary>1. A colleague wants to train a coarse-grained force field from the ATLAS trajectories. What is the first obstacle?</summary>
ATLAS stores coordinates only. Force matching needs the forces on the atoms for each frame. They would have to be recomputed from the saved coordinates with the original force field, which needs the coordinates at full precision and a second pass over all the data. mdCATH stores forces and avoids this.
</details>

<details markdown="1"><summary>2. An emulator trained on 100 ns trajectories gives two conformations of your protein with populations of 80 % and 20 %. Can you report a free-energy difference of 3.4 kJ/mol?</summary>
Not on that basis. Runs of that length contain few or no transitions between distinct conformations, so the frequencies in the training data reflect where the simulations started, and the model reproduces them. The model can tell you that both states are plausible. Populations need MD with many transitions, a Markov model, or experimental data.
</details>

<details markdown="1"><summary>3. A paper reports that adding MD features raised the correlation with measured affinities from 0.50 to 0.64. Name three things to check.</summary>
Whether anything else was added at the same time (in one such case quantum-chemical charges were added together with the MD features). Whether the test proteins are dissimilar to the training proteins. What a model with no protein information scores on the same test, and whether any uncertainty is given for the difference.
</details>

<details markdown="1"><summary>4. Why might an emulator that works well on natural proteins fail on a designed binder?</summary>
Models that take a multiple sequence alignment or language-model embedding as input learned from families of related natural sequences. A designed sequence has no relatives, so that input carries little information. On 50 designed proteins such models predicted unstable conformations while a model conditioned on the designed structure stayed accurate.
</details>

## Exercises

1. Download the metadata of mdCATH and of ATLAS. For each, plot the distribution of chain lengths and count how many systems are complexes. What does that say about using them for interfaces?
2. Take the force-matching exercise of Module 17 (a double well with noise added to the forces). Measure how the error of the learned free energy falls with the number of samples for three noise levels, and relate the result to the table of data-efficiency gains above.
3. Choose one model from the table of generators, find its paper through the reference list below, and fill in for yourself: number of training systems, total simulated time, force field, what was held out, and the one limitation its authors stress most.
4. Write a one-page plan for an MD data set intended to train a predictor of whether a designed protein-protein interface holds together. Use the eight-point list: state the label, the number and diversity of complexes, the simulation length and repeats, what you will store, the split, the baseline and the ablation.

## Read

{{READ}}

## The papers behind this module

{{PAPERS}}
