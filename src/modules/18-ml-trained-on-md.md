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

## The plan of this module

Modules 1 to 17 taught how a molecular dynamics (MD) simulation is run and how its output is analysed. This module is about what happens when that output is given to a machine-learning (ML) program as teaching material. Such programs are offered, often under the label "AI" (artificial intelligence), as faster force fields, as replacements for long simulations, and as predictors of flexibility or binding. The module reports what the papers show that they can do, and what has not been shown.

Some words in the box above may be new. A preprint is a version of a paper made public before it has been through peer review, and arXiv and bioRxiv are two servers that host preprints. Crossref is a registry of published papers. A model card is a short description that the authors of a model publish with it.

The evidence is dense: tables of data sets and models, and one number after another. A statement such as "correlates 0.85 with MD on 82 held-out proteins" tells you something only if you know what was correlated, what "held-out" means and what value would count as good. So the module alternates between two kinds of text:

1. **Background sections** explain the ideas from zero: the vocabulary of machine learning, the three levels at which a model can agree with a simulation, and how generative models work.
2. **Evidence sections** keep the statements that were checked against the papers, each with its citation: the four kinds of model, the data sets, one section per kind, the list of what a model needs and the list of what has not been shown. Around the checked statements, added paragraphs explain the words they use.

On a first reading the essential parts are the vocabulary, the four kinds, the three levels of agreement and the two lists at the end. The formulas in "Generative models from zero" can be skipped the first time, as long as you keep the picture that goes with each one. No statement in the evidence sections depends on following the algebra.

Three sections have a strip of lectures under their heading. The lesson is written to be complete without them. They are a second explanation of the same material, for when you want to hear it from a lecturer.

The module uses ideas from earlier modules, and repeats each one in a sentence or a box at the place where it is needed: populations and free energy (Module 3), fluctuations and error bars (Module 11), coarse-graining and force matching (Module 15), Markov state models (Module 16), and neural-network potentials and Boltzmann generators (Module 17).

### How to read the formulas

This module has few formulas, and all of them are in the background sections. Each displayed formula is followed by a list that says what every letter in it means. The notation below is all you need. Each item is explained at more length in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $x$ | One **configuration**: the full list of coordinates of all the atoms (or beads) of a system at one instant. In the small examples it is a single number. |
| $p(x)$ | A **probability density**: how probable it is to find the system at, or very near, the configuration $x$. A larger $p$ means "visited more often". See the [toolbox](maths.html#probability). |
| $p(x\mid y)$ | The vertical bar is read "given": the probability density of $x$ when $y$ is known. |
| $\propto$ | "Is proportional to": equal up to a constant factor that is the same for every $x$. |
| $\ln$ | The natural logarithm, the inverse of the exponential function $e^{(\ )}$. See the [toolbox](maths.html#exp-log). |
| $\langle A\rangle$ | The average of the quantity $A$. |
| $k_BT$ | The thermal energy: the Boltzmann constant times the temperature, 2.494 kJ/mol at 300 K. |
| a subscript $\theta$, as in $v_\theta$ | "This function is a neural network." The letter $\theta$ (theta) stands for all its adjustable parameters together. |

<div class="box warn" markdown="1">
**Words and letters that mean two things in this module.**

- **Weight.** (1) One of the adjustable numbers of a neural network. (2) A statistical weight: a number that says how much one configuration counts in an average (the Boltzmann weight, an importance weight). (3) The share of the training examples that comes from one data set.
- **Model.** Usually a machine-learning model. Sometimes a physical model: a force field, a Markov state model, an elastic network model.
- **Prior.** Knowledge a model has before it sees the data of interest. Either a network that was already trained on something else, or energy terms written down by hand.
- **Flow.** In "normalising flow" and "flow matching" it is a transformation of random numbers. No liquid flows and no time passes.
- **Sample.** As a verb, to draw one random configuration. As a noun, the configuration drawn. "Sampling" in the MD sense is how thoroughly a simulation has visited its states.
- **Replica.** Here an independent repeat of a simulation, not a member of a replica-exchange ladder (Module 14).
- $t$ is physical time, except in the flow-matching formula, where it is a progress variable from 0 to 1. $T$ is always the temperature.
- $p$ is always a probability or a population here, never a momentum.
- The subscript of $x$ changes meaning. In the noising formula $x_0$ is the training frame and $x_k$ the frame after $k$ noising steps. In flow matching $x_0$ is the noise and $x_1$ the training frame. In $p(x_{t+\tau}\mid x_t)$ the subscript is a physical time.
- $A$ in $\langle A\rangle$ and $A(x)$ is any quantity computed from a configuration, while A and B in running text are the names of two states. $b$ is a parameter of the straight line $y = ax + b$ in the vocabulary section and the amount of noise per step in the noising formula.
</div>

## The vocabulary of machine learning, from zero

Every paper behind this module describes its model with the same dozen words: model, parameter, label, loss, training set, test set, pretraining, benchmark, baseline, ablation. This section defines them once. One small example is used throughout: a program that takes the structure of a protein and returns, for each residue, how much that residue moves in a simulation.

### Model, parameters, label, loss

A **model** is a function with adjustable numbers in it. The straight line $y = ax + b$ is a model: $x$ is the input, $y$ is the output, and $a$ and $b$ are two adjustable numbers, its **parameters**. A neural network is the same kind of object with millions of parameters, built by chaining many simple operations (Module 17). The parameters of a network are also called its **weights**.

**Training** means choosing the parameters so that the outputs of the model come close to known right answers. Each known right answer is a **label**, and one input together with its label is one **training example**. In the flexibility example, the input is a structure and the label is the flexibility of each residue, measured in an MD trajectory of that protein. This is the sense in which such a model is "trained on MD": the simulation supplied the right answers.

The **loss** is one number that measures how far the outputs are from the labels over all the examples, for instance the average squared difference. Training is a search for the parameters that make the loss small. The computer does it in many small steps, and each step changes every parameter a little in the direction that lowers the loss.

<div class="box maths" markdown="1">
**Maths you need here: fitting by least squares, the smallest case.** Take the model $y = ax$, with one parameter $a$, and three training examples $(x, y)$: $(1,\ 2.1)$, $(2,\ 3.9)$ and $(3,\ 6.0)$. The loss is the sum of the squared differences between output and label:

$$
L(a) = (1a - 2.1)^2 + (2a - 3.9)^2 + (3a - 6.0)^2 .
$$

The loss is smallest where its slope with respect to $a$ is zero. Working that out gives $a = (\text{sum of } x\,y)/(\text{sum of } x^2) = (2.1 + 7.8 + 18.0)/(1 + 4 + 9) = 27.9/14 = 1.99$. The model has "learned" that $y$ is about twice $x$. The loss at this value is 0.019 and not zero, because the three points do not lie exactly on one line: that remainder is the noise of the labels.

A neural network is trained in the same spirit, with millions of parameters in the place of one. There is then no formula for the best values, so the minimum is approached step by step. More in the [toolbox](maths.html#fitting).
</div>

### Training set, validation set, test set

A student who has seen the exam questions in advance can score well without understanding anything. A model can do the same. With enough parameters it can store the training examples and return their labels, and fail on everything else. This is **overfitting**. To detect it, the data are divided into three parts before training starts:

- the **training set**: the examples the parameters are fitted to (the exercises with solutions);
- the **validation set**: examples that are not fitted, used during development to decide when to stop training and which version of the model to keep (the mock exam);
- the **test set**: examples used once, at the end, to report how good the model is (the final exam).

The validation set has to be separate from the test set because every decision taken by looking at a score adapts the model a little to those examples. After many such decisions the validation score is too optimistic, and only the untouched test set gives an honest number. Examples that are kept away from training are called **held-out**. The loss computed on each part has the matching name: training loss, validation loss, test loss.

A model **generalises** when it does well on examples it was not trained on. Two expressions describe how far a new example is from the training data. It is **in distribution** if it resembles them: another natural protein of ordinary size, for a model trained on natural proteins of ordinary size. It is **out of distribution** if it does not: a designed protein, a complex, a much larger system.

In this module a model is called **transferable** when it works on a molecule that was not in its training set at all, without being trained again. A model trained on simulations of one protein and used on that same protein is not transferable, however accurate it is.

### Data leakage, and why the split is done by sequence identity

The test set is an honest exam only if its questions are new. For proteins that is harder to arrange than it sounds, because proteins come in families. Two members of a family (two **homologues**) descend from a common ancestor, and they have related sequences, nearly the same fold and similar motions. If one member is in the training set and another in the test set, the exam contains a question that was almost among the exercises. The model can answer it from memory.

This is **data leakage**: information about the test answers reaches the model through the training data. In a **random split** each protein is sent to the training set or to the test set by chance. A random split leaks whenever the data set contains families, and sets of natural proteins usually do.

The remedy is to split by similarity. **Sequence identity** is the percentage of aligned positions at which two sequences have the same amino acid. The proteins are first grouped into clusters whose members are more identical to each other than a chosen threshold, say 30 % (an illustration: papers choose different values). Then whole clusters are sent to one side or the other, so that no test protein has a relative above the threshold in the training set.

The same idea applies to small molecules (split by chemical similarity) and to time. Two frames taken a few picoseconds apart in one trajectory are nearly the same configuration, so the frames of one trajectory must not be divided at random between training and test.

The consequence for reading papers: a score obtained on a random split says how the model does on close relatives of what it has seen. Treat it as an upper estimate of what you will get on a new protein.

### Pretraining and fine-tuning

Training can be done in stages, on different data. In **pretraining** the model is trained on a large, general data set. In **fine-tuning** the training continues on a smaller and more specific data set, starting from the parameters that the first stage produced. A physician is trained in the same way: general medicine first, then a speciality, which is learned faster because of what came before.

The reason is the amount of data. There are far more known structures and sequences than there are long simulations. A model that has first learned what proteins look like from the large collection has less left to learn from the small one: how they move. A training recipe such as "AlphaFold weights, then PDB, then ATLAS", which you will meet in the table of generators, has three such stages.

In that recipe, "AlphaFold weights" means the parameters of the already trained AlphaFold structure-prediction network, taken as the starting point. The PDB is the Protein Data Bank, the public archive of experimentally determined structures, and ATLAS is one of the MD data sets described below.

What the model carries over from an earlier stage is one meaning of the word **prior**: knowledge it has before it sees the data of interest. The other meaning, a physical energy term fixed in advance, appears in Kind 1.

### Benchmark, metric, baseline, ceiling, ablation

These five words describe how a model is judged.

- A **benchmark** is an agreed exam: a fixed set of test systems, a reference answer for each (from experiment or from long MD), and a rule for scoring. Its value is that different models are compared on the same questions.
- A **metric** is the number that the scoring rule produces: a correlation coefficient, an average error in ångström or in kcal/mol, the percentage of known states that the model found. A metric squeezes a whole comparison into one number, so something is always lost. Each metric quoted in this module is explained where it first appears.
- A **baseline** is a simple or cheap method scored on the same benchmark. It shows how much of the score is easy to get. A model that reaches 0.60 looks different once you know that a method which ignores half of the problem reaches 0.52 (this pair of numbers appears in Kind 3).
- A **ceiling** is the best score that still means something. The reference has noise of its own: two independent simulations of the same protein do not agree perfectly. A model cannot meaningfully agree with one simulation better than a second simulation does.
- An **ablation** removes one ingredient (a data set, an input, a training stage), trains the model again and measures again. The change in the score is the contribution of that ingredient. Without an ablation, a claim that "X helps" is not supported, however good the final model is.

## Four kinds of model, told apart by their label

A simulation writes a **trajectory**: a list of **frames**, each frame being the coordinates of all the atoms at one instant. If asked, it also writes the velocities and the forces on every atom at those instants. "A model trained on MD" is a model for which some of this output served as training material. That says little by itself, because very different tasks can be set:

- **Learn a potential.** The model outputs an energy for any arrangement of the atoms, and forces with it. You still run a simulation, with the learned energy function in the place of the force field.
- **Generate conformations.** The model outputs plausible three-dimensional structures of a molecule, several different ones for the same sequence, without running a simulation.
- **Predict an ensemble.** The same, with a stronger promise: each conformation appears as often as it would in a long simulation. (An ensemble, in the sense of Module 3, is the collection of configurations that a system visits at equilibrium, each with its probability.)
- **Emulate the dynamics step by step.** The model takes the configuration now and outputs a configuration a moment later, where the "moment" is far longer than an MD time step. Repeating this gives a trajectory with a time axis.
- **Predict a property.** The model outputs one number or a few numbers per protein or per residue, such as a flexibility or a binding affinity.

One question sorts these five tasks into four kinds of model.

"Trained on MD" covers four different things. The useful question is: **what was the training label?**

| Kind | Label taken from the simulation | What the model outputs | Example |
|---|---|---|---|
| 1. Learned coarse-grained force field | The **forces** on the atoms, projected onto beads | An energy function for coarse-grained MD | CGnet, CGSchNet |
| 2. Ensemble or trajectory generator | The **frames** themselves (coordinates), sometimes ordered in time | Conformations, without running MD | AlphaFlow, BioEmu |
| 3. Predictor that uses MD as a feature or a label | A **summary** of the trajectory (flexibility, contact occupancy) | Something else: flexibility, affinity, a structure | Flexpert, Dynaformer, Boltz-2 |
| 4. Atomistic potential trained on quantum chemistry | **Quantum energies and forces** of configurations that MD supplied | An all-atom energy function | ANI, MACE-OFF |

Kind 4 is not trained on MD in the strict sense: classical or semi-empirical MD only supplies the configurations, and quantum chemistry labels them. It is included because it is what most people mean by a "machine-learned force field" (Module 17).

### Reading the table of kinds

The label is the useful question because it fixes two things. It fixes what the model can know: a model that was shown forces can be good at forces, and nothing in its training tells it how long a process takes. And it fixes what the simulation must have saved, which matters when you plan a data set.

Row by row:

- **Kind 1.** A coarse-grained model replaces groups of atoms by single particles called beads (Module 15). "Projected onto beads" means that the forces on the atoms of a group are combined into one force on its bead. The model does the first task, learning a potential, for the beads.
- **Kind 2.** The label is the frame itself. The model is shown conformations and learns to produce more of the same kind (the second and third tasks). If the order of the frames in time is also given, it can learn how one frame follows another (the fourth task).
- **Kind 3.** A summary is a number, or a small table of numbers, computed from the whole trajectory. Flexibility is how much each residue moves about its average position (the root-mean-square fluctuation, RMSF, of Module 11). Contact occupancy is the fraction of frames in which two given groups touch. The model does the fifth task. MD enters as a **label** (the model is trained to output the summary) or as a **feature** (the summary is given to the model as an extra input, to help it predict something else).
- **Kind 4.** Quantum chemistry computes the energy of an arrangement of atoms from the behaviour of its electrons, far more accurately and far more slowly than a force field (Module 17). Semi-empirical MD is MD with forces from a simplified and faster quantum method. The model does the first task for all the atoms.

The names in the last column are names of published models. You do not need to know what the letters in them stand for.

The numbers 1 to 4 follow the table. The sections below take the two potentials first (Kinds 1 and 4), then the generators (Kind 2), then the predictors (Kind 3).

## The data sets

A model can be no better than its data, so start here.

An MD data set, in the sense of this module, is a collection of trajectories of many different molecules, all run with one protocol and published so that others can train models on them. The table below has one row per data set. Its columns:

- **Systems**: how many different molecules or complexes were simulated. A chain is one protein molecule. A domain is a compact part of a chain that folds by itself, and CATH is a database that sorts such domains by their fold (the letters stand for Class, Architecture, Topology, Homologous superfamily). A protein-ligand complex is a protein with a small molecule bound to it.
- **Total time**: the simulated time added up over all systems and all runs. The units are the millisecond (ms), the microsecond (µs) and the nanosecond (ns): 1 ms = 1,000 µs = 1,000,000 ns.
- **Per system**: the length of one run and the number of runs. Replicas are independent runs of the same system (Module 11).
- **Force field, temperature**: the energy function and water model used (Modules 5 and 6), and the temperature. CHARMM36m, CHARMM22\* and ff14SB are protein force fields, TIP3P is a water model, and GAFF2 is a force field for small organic molecules.
- **Stores**: what was written to disk for each frame.
- **Used by**: models that appear later in this module.

Check the first row to see how the columns fit together: 1,390 chains × 3 runs × 100 ns = 417,000 ns, which is 0.417 ms, the "about 0.42 ms" of the table.

Some entries need a word. GPCRmd collects simulations of G-protein-coupled receptors (GPCRs), a large family of receptors that sit in the cell membrane. The "fast folders" are small proteins that fold and unfold within the length of the simulation, so that one trajectory shows both states and several passages between them. "On request" means that the trajectories are not in a public archive.

"MM/PBSA terms" are the energy components of the end-point binding estimate of Module 13 (the letters stand for molecular mechanics, Poisson-Boltzmann, surface area). "Amber family" means force fields of the line to which ff14SB belongs (Module 6). DiG is the Distributional Graphormer named in Module 17. The other entries of the last column are names of models.

| Data set | Systems | Total time | Per system | Force field, temperature | Stores | Used by |
|---|---|---|---|---|---|---|
| ATLAS ([Vander Meersche et al. 2024](cite:atlas)) | 1,390 protein chains | about 0.42 ms | 3 × 100 ns | CHARMM36m, TIP3P, 300 K | Coordinates | AlphaFlow, MDGen, aSAM, BBFlow, Boltz-2, flexibility predictors |
| mdCATH ([Mirarchi et al. 2024](cite:mdcath)) | 5,398 CATH domains | 62.6 ms | up to 500 ns × 5 replicas × 5 temperatures | CHARMM22\*, TIP3P, 320 to 450 K | Coordinates **and forces** | aSAMt, Boltz-2, learned force fields |
| MISATO ([Siebenmorgen et al. 2024](cite:misato_2024)) | 16,972 protein-ligand complexes | over 0.17 ms | 10 ns (8 ns stored) | ff14SB, GAFF2, 300 K | Coordinates, energy terms | Boltz-2, affinity models |
| PLAS-20k ([Korlepara et al. 2024](cite:plas20k_2024)) | 19,500 protein-ligand complexes | about 0.39 ms | 5 × 4 ns | ff14SB, GAFF2, 300 K | Coordinates, MM/PBSA terms | Affinity models |
| GPCRmd ([Rodríguez-Espigares et al. 2020](cite:gpcrmd2020)) | 191 systems at first release; 615 simulations on the platform | 0.41 ms, the total of the 615 simulations | 3 × 500 ns | see its protocol | Coordinates | DiG |
| D. E. Shaw fast folders | 12 small proteins | 8.2 ms | long trajectories, each with about ten folding events | CHARMM22\*, protein-specific temperatures | Coordinates, on request | ITO, BioEmu, tests of many models |
| BioEmu corpus ([Lewis et al. 2025](cite:lewis2025)) | 24,062 systems | 172 ms | varies | Amber family, about 300 K | Frames | BioEmu |
| Dynamic PDB ([Liu et al. 2024](cite:dynamicpdb2024)) | 12,643 chains | about 12.6 ms | 1 µs | ff14SB, 300 K | Coordinates, velocities **and forces** | Trajectory models |

Three things to notice. Almost every set is of **single chains or protein-ligand complexes**: there is no large public MD set of protein-protein complexes. Most runs are **short**, 10 to 500 ns, so they describe fluctuations around the starting structure. And only two sets store **forces**, which matters for the first kind of model.

"Fluctuations around the starting structure" are the small motions of a folded protein that stays folded: side chains turning, loops shifting, the whole structure breathing. A run of this length is usually too short for the protein to unfold or to move to a very different shape, so the data say little about such events.

### Why the amount, length, diversity and force field of the simulations limit a model

Four properties of a data set decide what a model trained on it can know. The total time in the table mixes the first three, so it has to be taken apart.

**Amount.** Labels taken from a simulation are noisy, and an average over noisy data becomes sharper only as the number of independent data grows (Module 11). Frames that are close in time are nearly copies of each other. A thousand frames from one nanosecond therefore carry less information than a thousand frames spread over a microsecond.

**Length of each run.** A run of a given length carries no information about events that take much longer. Suppose a protein changes shape about once per millisecond (an illustration). A 100 ns run is one ten-thousandth of that time, so it almost certainly shows one shape only, and a model trained on it cannot know that the other exists.

Length also limits what can be said about populations. To learn that a protein spends 80 % of its time in one state and 20 % in another, a run must pass between the two many times. A run that crosses once shows that both states exist, and nothing about the ratio.

**Diversity.** A transferable model has to learn how behaviour depends on sequence or structure, and it learns that from examples of different sequences. Twelve proteins simulated for a very long time are still twelve examples. The table shows how differently a total can be spent: the fast-folder set puts 8.2 ms into 12 proteins, about 0.68 ms each on average, while ATLAS gives each of its 1,390 chains 0.3 µs, about 2,300 times less.

**Force field.** The labels describe what the force field does. They describe the real molecule only as far as the force field is right (Module 6). A model that reproduces its training simulations perfectly reproduces their errors too, and more training data of the same kind cannot remove them.

A fifth property is simpler: **what was stored**. A label that was not written to disk cannot be learned from.

## Three levels of agreement: states, populations, rates

Papers say that a model "reproduces MD" or "agrees with MD". The phrase covers three claims of increasing strength, and the evidence sections keep them apart. A fourth question, whether the model agrees with experiment, is of a different kind and comes at the end of this section.

### Level 1: which conformations exist

The weakest claim is about coverage: the model produces the shapes that the simulation visited, such as folded and unfolded, or open and closed. Nothing is claimed about how often each occurs. A group of conformations that resemble each other and interconvert quickly is called a **state** or a **basin**, one valley of the energy landscape (Module 2).

### Level 2: how populated each one is

The second claim is about the **distribution**: each conformation appears with the right probability. This is what "thermodynamics" means in this module, because populations and free energies are two ways of writing the same information.

<div class="box physics" markdown="1">
**Physics you need here: the Boltzmann distribution.** Module 3 showed that a system held at a fixed temperature does not visit all its configurations equally often. Configurations of low energy are visited more often, by a rule that contains only the energy and the temperature. The rule is the formula below. A correct MD simulation at constant temperature that runs long enough visits configurations with exactly these frequencies, and that is the reference for level 2. More in the primer, on [temperature](physics.html#temperature) and on [free energy](physics.html#thermodynamics).
</div>

$$
p(x) \propto e^{-U(x)/k_BT} .
$$

<div class="legend" markdown="1">
- $x$: one configuration, the coordinates of all the atoms.
- $p(x)$: the probability density of finding the system at configuration $x$ at equilibrium.
- $\propto$: "is proportional to". The missing constant factor is the same for every $x$. It is fixed by the condition that all the probabilities add up to 1.
- $e$: the base of the exponential function, about 2.718.
- $U(x)$: the potential energy of configuration $x$, in kJ/mol.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature, in kelvin.
- $k_BT$: the thermal energy, 2.494 kJ/mol at 300 K. It is the yardstick against which an energy counts as small or large.
- The minus sign: higher energy, lower probability.
</div>

The right-hand side, $e^{-U(x)/k_BT}$, is called the **Boltzmann weight** (or Boltzmann factor) of the configuration.

**Read it like this.** Only the ratio of the energy to $k_BT$ matters. A configuration that lies one $k_BT$ higher in energy than another (2.494 kJ/mol at 300 K) is visited $e^{-1} = 0.37$ times as often. One that lies 5.74 kJ/mol higher is visited 10 times less often, and each further 5.74 kJ/mol costs another factor of 10. Raising the temperature makes $k_BT$ larger, so the same energy difference counts for less, and configurations of high energy become more common.

A state is a whole region of configurations, so its population is the sum of $p(x)$ over that region. Two states A and B with populations $p_A$ and $p_B$ differ in **free energy** by

$$
\Delta G_{AB} = G_B - G_A = -k_BT\,\ln\frac{p_B}{p_A} .
$$

<div class="legend" markdown="1">
- $p_A$, $p_B$: the populations of states A and B, the fractions of the time that the system spends in each.
- $G_A$, $G_B$: the free energies of the two states.
- $\Delta G_{AB}$: the free-energy difference, B minus A, in the units of $k_BT$ (kJ/mol here).
- $\ln$: the natural logarithm.
- $k_BT$: the thermal energy, as in the list above.
</div>

**Read it like this.** The less populated state has the higher free energy, and equal populations give $\Delta G_{AB} = 0$. Populations of 80 % and 20 % give $\Delta G_{AB} = -k_BT\ln(0.2/0.8) = k_BT\ln 4$, which is 3.5 kJ/mol at 300 K (3.4 kJ/mol at 298 K). The free energy is used here, and not the energy, because a state that contains many configurations is visited more often than one that contains few, at equal energy (Module 3).

Read backwards, the formula turns an error in a free energy into an error in populations. An error of 0.9 kcal/mol is 3.8 kJ/mol (1 kcal = 4.184 kJ), about 1.5 times $k_BT$, and it changes the ratio $p_B/p_A$ by a factor $e^{1.5}$, about 4.5. Keep this conversion in mind for the table of generators.

### Level 3: how fast the molecule moves between them

The strongest claim is about **kinetics**: rates, waiting times and pathways. Populations do not contain this information. Take all the frames of a trajectory and shuffle them like a pack of cards. Every count of "how often" is unchanged, so levels 1 and 2 can still be learned from the shuffled pack. The order in time is gone, and with it everything about "how fast".

The physical reason is in Module 16. Populations depend on the free-energy difference between two states, and rates depend on the height of the barrier between them. Two proteins can have the same populations and rates that differ by orders of magnitude (an order of magnitude is a factor of 10). A model can therefore be right at level 2 and know nothing at level 3.

To learn kinetics, a model needs frames in their order in time, saved at short intervals, and its predictions have to be tested against rates.

### Agreeing with MD, or agreeing with experiment

All three levels compare the model with the simulations it was trained on, or with other simulations of the same kind. Such a comparison says how well the model learned. Whether the result is true of the real molecule is a second question, and its answer also depends on the force field.

Think of two steps in a chain. The model differs from MD by some amount, and MD differs from experiment by some other amount. A model that matches MD perfectly lands exactly where the force field lands, errors included. The evidence gives both distances for one model (point 5 of the list in Kind 2), and they are far apart.

So whenever a paper reports agreement, look first for the reference: MD of the same kind as the training data, longer or better MD, or a measurement. A model can also be given experimental data during training, which is one way to correct what the simulations get wrong. One model in Kind 2 does this.

## Kind 1: learned coarse-grained force fields

<div data-videos="106sdeDF1oc"></div>

This kind does the first task, learning a potential, for a simplified representation of a protein. The attraction is speed: with far fewer particles and no water, each new sample of a protein's shape should cost much less than in all-atom MD. The section is about what it takes to train such a model. Its first lesson is that the label is much harder to use than it looks.

<div class="box physics" markdown="1">
**Physics you need here: coarse-graining and force matching (Module 15).** A coarse-grained (CG) model replaces groups of atoms by single particles called **beads**, for example one bead per amino acid. Everything else (the remaining atoms of the protein, the water) no longer appears. The beads must then feel the *average* effect of what was removed. The energy function that does this exactly is the **potential of mean force**: a free energy, written as a function of the bead positions. Minus its slope gives the **mean force** on each bead, which is the atomistic force averaged over all the arrangements of the removed atoms that fit the same bead positions.

**Force matching** finds this energy function from an all-atom simulation. For every saved frame, combine the forces on the atoms of each group into one force on its bead. Then adjust the CG energy function until the forces it predicts are as close as possible to those bead forces, on average over all frames. Module 15 showed that the best possible result of this fit is the mean force.
</div>

The idea is the force matching of Module 15 with a neural network as the energy function ([Wang et al. 2019](cite:wang2019b)). Its history is a lesson in what the label demands.

### Why the label is so noisy

Fix the beads in one arrangement. The water and the side chains can be in a great many arrangements around them, and in each one the force on a bead is different. The label you want is the average over all of these, the mean force. The label that a frame gives you is the force for the single arrangement that the atoms happened to be in at that instant. It is one draw from a wide scatter.

Averaging is the only cure, and it works slowly. If one label scatters around the true value with a standard deviation $\sigma$, the average of $n$ independent labels still has an uncertainty of

$$
\sigma_{\text{mean}} = \frac{\sigma}{\sqrt{n}} .
$$

<div class="legend" markdown="1">
- $\sigma$ (sigma): the standard deviation of a single label, the typical size of its scatter around the true value. Here it is the noise of the instantaneous force.
- $n$: the number of independent labels that are averaged.
- $\sigma_{\text{mean}}$: the uncertainty that remains in their average (the standard error of Module 11).
- $\sqrt{n}$: the square root of $n$. Four times as many labels make the average only twice as sharp.
</div>

**Read it like this.** Say the noise is 10 times as large as the mean force you want to learn (an illustration). To know the mean force to within a tenth of its size, the noise must come down from 10 to 0.1, a factor of 100, and that takes $n = 100^2 = 10{,}000$ independent labels for one arrangement of the beads. More in the [toolbox](maths.html#averages).

A network does not average frame by frame: it shares information between similar arrangements. The square root is still the reason why the amount of data in the next paragraph is so large. It is also the reason why lowering $\sigma$ pays so well: half the noise needs a quarter of the labels.

**The label is noisy, and that sets the amount of data.** For one coarse-grained configuration there are many atomistic ones, each with a different force, so the projected force scatters widely around the mean force the model must learn. The noise can be an order of magnitude larger than the signal ([Krämer et al. 2023](cite:kramer2023_optimalforce)). Plain force matching needs of the order of a million force-labelled frames, about 190 µs of MD, for a single miniprotein. Most of the progress since 2023 is in reducing that noise:

| Idea | Gain in data efficiency | Source |
|---|---|---|
| Better way of projecting forces onto beads | about 3 times | [Krämer et al. 2023](cite:kramer2023_optimalforce) |
| Forces generated by a flow model trained on the frames | about 70 times, for chignolin | [Köhler et al. 2023](cite:kohler2023_flowmatching) |
| Forces combined with a denoising objective | up to about 100 times | [Durumeric et al. 2026](cite:durumeric2026_forcesnoise) |
| Mean forces from constrained simulations | 375 times fewer labels for the same test loss | [Park et al. 2026](cite:park2026_meanforce) |

In that paragraph the "signal" is the mean force and the "noise" is the scatter of the instantaneous force around it. A force-labelled frame is a frame saved together with its forces. A miniprotein is a very small protein, and chignolin, named in the table and again below, is one of the smallest that are used as test cases.

**Data efficiency** is how little training data a method needs for a given quality of result. A gain of 70 times means, roughly, the same quality from 70 times less data. The exact measure differs from paper to paper, and the last row of the table states its own.

The four rows use ideas that are explained elsewhere in this module, so here is the idea of each in a sentence or two.

- *Row 1.* There is more than one valid way to combine atomic forces into a bead force, and some ways scatter less than others.
- *Row 2.* A flow model is a generative model (see "Generative models from zero"). Trained on frames alone, it gives a smooth estimate of how probable each arrangement is. The Boltzmann formula read backwards turns a probability into an energy, and an energy has forces.
- *Row 3.* A denoising objective is the training task of a diffusion model, explained in the same section: remove noise that was added to the frames on purpose. It is a second source of information next to the forces.
- *Row 4.* In a constrained simulation the beads are held in place while everything else moves. The force averaged over such a run is already a mean force, so most of the noise is gone before training starts.

**Forces must be saved during the run.** Training sets for these models store the instantaneous forces on the protein atoms ([Majewski et al. 2023](cite:majewski2023); [Charron et al. 2025](cite:charron2025)). The D. E. Shaw trajectories and ATLAS have none, which is why mdCATH advertises its forces as a distinguishing feature.

An MD program computes the force on every atom at every step, because it needs the forces to move the atoms (Module 4). It writes to disk only what the input file asks for (Module 10), and many published trajectories contain coordinates only, as the table of data sets shows. The **instantaneous force** is the force at the instant of a saved frame, as opposed to a force averaged over time. The first "Check yourself" question says what it takes to recover forces that were not saved.

**Diversity of systems matters more than converged sampling of each.** A model trained on converged folding simulations of 12 fast-folding proteins could not stabilise proteins outside that set, and its authors say it should not be expected to ([Majewski et al. 2023](cite:majewski2023)). A model trained on simulations of about 50 CATH domains that only sample their folded state, plus 1,245 umbrella-sampled dimer systems that show it what close contacts cost, folds proteins it never saw ([Charron et al. 2025](cite:charron2025)). The comparison is not clean, since resolution and architecture also differ, but volume still counts: with 10 % or 50 % of the same data, no folded test protein was stable.

Some words in that paragraph. Sampling is **converged** when the simulation has visited every relevant state so many times that the averages no longer change with more simulation (Module 11). To **stabilise** a protein means that a simulation run with the learned model keeps the protein folded. **Umbrella sampling** (Module 12) holds two molecules at a chosen distance with a spring-like restraint, one distance after another, so that the data also contain distances that an ordinary simulation rarely visits. A dimer is a pair of molecules, and the "close contacts" are such rarely visited distances, where two groups are pressed together and the energy rises steeply.

**Resolution** is the number of beads per residue, and **architecture** is the type of network. The second model "folds proteins it never saw", so it is transferable in the sense of the vocabulary section. The last sentence of the paragraph describes a data-scaling test: train the same model on a part of the data and see what is lost.

**A physics prior is needed.** Without simple bonded and repulsive terms, the network explores regions where it has no data and the simulation produces unphysical structures or explodes. The network learns a many-body correction on top of the prior, and pair potentials alone cannot fold even chignolin ([Wang et al. 2019](cite:wang2019b)).

Here **prior** has its second meaning: energy terms that are written down by hand before training and are not learned. The bonded terms are springs that keep neighbouring beads at sensible distances and angles (the bond and angle terms of Module 5). The repulsive term is a steeply rising energy that stops two beads from sitting on top of each other.

The need for them follows from where the data come from. A simulation visits configurations of low energy and almost never those of high energy, so the training frames contain no example of two overlapping beads. Nothing tells the network that such a configuration is costly. In a region without data a network can return any value, including a very low energy, and a simulation that wanders there stays there. "Explodes" means that the coordinates grow without limit and the run stops.

A **pair potential** is an energy that is a sum of terms, each of which depends on one distance between two beads. A **many-body** term depends on the positions of three or more beads at once and cannot be written as such a sum (Module 15). The last sentence of the paragraph says that many-body terms are needed for folding, even for the smallest test protein.

**Low test error does not mean a good model.** In both coarse-grained and atomistic work, validation loss fails to predict whether a simulation is stable or gives the right free energies; models have to be chosen by running them ([Majewski et al. 2023](cite:majewski2023); [Fu et al. 2023](cite:fu2023forces)).

The validation loss measures the error of the forces on frames that resemble the training frames. A simulation asks a different question: where does the model go when it follows its own forces for millions of steps? Small errors add up, and the simulation can leave the region that the data covered. "The right free energies" means the right populations, level 2 of the previous section. "Chosen by running them" means that each of several trained models is used in a simulation, and the one whose simulation behaves best is kept.

**Limits that the papers state themselves.** The model is valid only at the temperature it was trained at. It gives thermodynamics, not kinetics: coarse-grained time is not physical time. Per step it is slower than classical all-atom MD on the same hardware, by one to two orders of magnitude in one report; the gain, where it has been quantified, is 42 to 1,144 times fewer steps per independent sample for four small proteins ([Charron et al. 2025](cite:charron2025)). And the training data of the transferable model contain no protein-protein complexes.

The first two limits have their reasons in Module 15. The temperature: the CG energy function is a free energy. It contains the entropy of the removed atoms, and that contribution changes with temperature, so a function fitted at one temperature is wrong at another. The time: removing atoms removes friction, so the beads move faster than the real groups would, by a factor that differs from one process to another. The model can therefore be right at levels 1 and 2 and still say nothing reliable at level 3.

The speed comparison has two parts that must be kept apart. "Per step" compares the cost of one time step: one step of the network model costs more computer time than one step of all-atom MD, by a factor of 10 to 100 in the report quoted. "Steps per independent sample" counts how many steps a simulation needs before it reaches a configuration that is unrelated to the one it started from (Module 11). The CG model needs far fewer. Whether the exchange is favourable depends on both numbers.

## Kind 4: atomistic potentials trained on quantum chemistry

<div data-videos="tWeBrPTrSDE I9Y2le9e74A ZR1NTBPBDOo"></div>

This kind also learns a potential, for all the atoms and with a different source of labels. The energies and forces come from quantum chemistry, which computes them from the electrons and is far more accurate and far slower than a force field. A simulation has only the job of proposing which arrangements of atoms (**configurations**) to compute. A cheap method chooses the questions, an expensive one answers them, and the network learns the answers.

These were introduced in Module 17. What the papers add:

- **Where the configurations come from.** Classical MD at 300 and 500 K for the SPICE set behind MACE-OFF ([Kovács et al. 2025](cite:maceoff_2025)); semi-empirical MD and metadynamics for AIMNet2 ([Anstine et al. 2025](cite:aimnet2_2025)); short restrained classical MD of fragments of PDB structures for the biomolecular part of OMol25 ([Levine et al. 2025](cite:omol25)).
- **Speed.** Every measurement in the papers read puts these models below classical MD in steps per day: 4 to 70 times slower in most measurements, depending on the model and the test, and more in some ([Kovács et al. 2025](cite:maceoff_2025); [Zaverkin et al. 2025](cite:zaverkin2025)).
- **Stability.** Failures appear suddenly, sometimes after hundreds of picoseconds of apparently healthy dynamics, and a force error below 1 meV/Å did not prevent one model from failing after 25 ps ([Fu et al. 2023](cite:fu2023forces)). Published protein demonstrations are short: one to two nanoseconds for crambin with MACE-OFF, at most 10 ns in AI2BMD ([Wang et al. 2024](cite:ai2bmd2024)).
- **Long-range interactions and solvent** are mostly delegated to a classical model or left out. OMol25 calls binding free energies out of scope.
- **Read the method behind a headline.** AI2BMD's agreement with experimental folding free energies and melting temperatures was obtained by re-evaluating conformations sampled with a classical force field, not from ensembles the learned potential sampled itself.

### The five points, explained

**Where the configurations come from.** A network can be trusted only near configurations of the kind it was trained on (Module 17), so the training set must cover what a later simulation will meet. Classical MD at 500 K supplies geometries that are more distorted than those at 300 K. **Semi-empirical** methods are simplified, fast versions of quantum chemistry. **Metadynamics** (Module 14) pushes a system away from configurations it has already visited, which produces unusual geometries.

In a **restrained** simulation some atoms are tied to chosen positions by springs. PDB structures are entries of the Protein Data Bank. SPICE, AIMNet2 and OMol25 are names of data sets or models.

**Speed.** "Steps per day" is the number of time steps a program completes in a day on a given computer. Multiplied by the time step, it gives the nanoseconds per day of Module 10.

**Stability.** A simulation is stable while it keeps producing physically sensible structures. The **force error** is the average difference between the forces of the model and the reference forces that served as its labels, on test configurations. Its unit here is the millielectronvolt per ångström (1 Å = 0.1 nm): 1 meV/Å is 0.965 kJ mol$^{-1}$ nm$^{-1}$. A picosecond (ps) is a thousandth of a nanosecond. Crambin is a protein, and AI2BMD is the name of a model.

**Long-range interactions and solvent.** Most of these networks compute the energy of an atom from its neighbours within a short cutoff distance (Module 17), while electrostatic interactions reach much further (Module 7). "Delegated to a classical model" means that the long-range part, or the water, is handled by an ordinary force field. "Out of scope" means that the authors did not test it: they write that computing a binding free energy is beyond the scope of their evaluation of the potentials.

**Read the method behind a headline.** There are two ways to get a free energy from a potential. One is to run a simulation with that potential and count populations. The other is to take conformations that a different potential produced, and to compute their energies again with the new one. The second way tests the energies that the model assigns to conformations which something else found. It does not test whether the model, left to run, would find those conformations and stay in them.

A **folding free energy** is the free-energy difference between the folded and the unfolded state of a protein, in the sense of the formula for two states above. A **melting temperature** is the temperature at which half of the molecules are unfolded.

A related and more modest use of machine learning is to assign the parameters of an ordinary classical force field from quantum data ([Takaba et al. 2024](cite:espaloma03); [Seute et al. 2025](cite:grappa2025)). The result runs at classical speed. So far only the bonded terms are learned; the Lennard-Jones parameters and the charge model, which govern binding, are inherited.

The **bonded terms** are the springs for bonds, angles and torsions (Module 5). The Lennard-Jones parameters set the size of each atom and how strongly it attracts its neighbours, and the charge model sets the partial charges (Modules 5 and 6). Two molecules that bind touch each other only through these non-bonded terms, which is why the paragraph says that they govern binding. "Inherited" means taken unchanged from an existing force field.

## Generative models from zero

Kind 2, and two rows of the table in Kind 1, rest on generative models. This section explains what they are and how the types named in this module work: diffusion models, flow matching, normalising flows and Boltzmann generators. Each type gets one picture and one small formula. On a first reading the pictures are enough.

### What "generative" means

A predictor returns one answer for one input. Give a structure-prediction network a sequence and it returns one structure. A **generative model** returns a different answer each time it is asked, and the answers taken together follow a probability distribution. Ask it a thousand times for a conformation of the same sequence and you receive a thousand conformations. That set is the model's ensemble.

A die is the smallest generative model: it generates the numbers 1 to 6. A loaded die generates the same numbers with other frequencies. Training a generative model amounts to loading the die until its frequencies match those of the training data. For a protein the "faces" are conformations, and there are infinitely many of them, so the frequencies cannot be stored in a table. The model has to learn a rule, and the rule must give sensible answers for sequences that were not in the training data.

A computer can produce simple random numbers at almost no cost, for instance numbers that follow a Gaussian (bell-shaped) distribution ([toolbox](maths.html#random-numbers)). All the methods below turn a list of such numbers, called **noise**, into a conformation. They differ in how the transformation is built and trained. To **sample** is to carry out the transformation once and obtain one conformation.

A model is **conditioned on** something when that thing is given to it as an input and its samples depend on it. A model conditioned on the sequence produces conformations of that sequence. One conditioned on a starting structure produces conformations near that structure, and one conditioned on a temperature produces the ensemble for the temperature requested. In symbols, $p(x\mid y)$ is the distribution of the conformations $x$ given the input $y$.

### Diffusion: add noise step by step, learn to remove it

Take a sharp photograph and add a little random grain to it, again and again. After enough steps nothing of the picture is left, only grain. Destroying a picture in this way needs no skill. A **diffusion model** is a network trained to undo one step: given a grainy picture, return a slightly less grainy one. To generate a new picture, start from pure grain and apply the network many times.

For a protein the "picture" is the list of atomic coordinates, and the grain is a small random displacement of every atom. One noising step, written for a single coordinate in units chosen so that the data have a spread of about 1, is

$$
x_k = \sqrt{1-b}\;x_{k-1} + \sqrt{b}\;\varepsilon_k .
$$

<div class="legend" markdown="1">
- $x_k$: the value of the coordinate after $k$ noising steps. $x_0$ is the value in the training frame.
- $k$: the number of the step, from 1 to the last step.
- $b$: a small number between 0 and 1 that sets how much noise one step adds. In practice it changes from step to step, and the list of its values is called the noise schedule.
- $\varepsilon_k$ (epsilon): a fresh random number for this step, drawn from a Gaussian distribution with mean 0 and standard deviation 1.
- $\sqrt{1-b}$: a factor a little below 1 that shrinks the old value.
- $\sqrt{b}$: the factor that scales the new noise. The two square roots are chosen so that the overall spread stays the same: if the values of $x_{k-1}$ have variance 1, those of $x_k$ have variance $(1-b)\times 1 + b\times 1 = 1$.
</div>

**Read it like this.** Each step keeps most of the old value and mixes in a little noise. With $b = 0.1$ and $x_0 = 2.0$, the first step gives $x_1 = 0.949\times 2.0 + 0.316\,\varepsilon_1 = 1.90 + 0.316\,\varepsilon_1$. After $k$ steps the original value has been multiplied by $(1-b)^{k/2}$. For 50 steps that is $0.9^{25} = 0.07$: 7 % of the frame is left and the rest is noise.

Training needs no label beyond the frame. Take a frame, add noise up to a randomly chosen step $k$, and ask the network what noise was added. The right answer is known, because you added the noise yourself. This is why the label of Kind 2 is "the frames themselves". Generation runs the other way: draw pure noise, let the network estimate the noise in it, remove a part of that estimate, and repeat down to step 0.

Many small steps are used because each one is an easy task. Removing a little noise means moving every atom slightly towards where atoms in such surroundings are usually found. Removing all the noise at once would mean producing a correct protein structure from nothing in one stroke.

### The score: an arrow towards higher probability

What the denoising network learns has a name and a plain meaning. The **score** of a distribution is the slope of the logarithm of its probability density:

$$
s(x) = \frac{d}{dx}\ln p(x) .
$$

<div class="legend" markdown="1">
- $x$: one coordinate. In the real case $x$ is all the coordinates and the derivative becomes a [gradient](maths.html#gradient), one slope per coordinate.
- $p(x)$: the probability density of the data at $x$.
- $\ln$: the natural logarithm.
- $\dfrac{d}{dx}$: the derivative with respect to $x$, the slope.
- $s(x)$: the score. Its sign says in which direction the data become more probable, and its size says how quickly.
</div>

**Read it like this.** The score is an arrow attached to every point, and it points uphill on the probability. For a Gaussian distribution centred at 0 with standard deviation 1, $\ln p(x) = -x^2/2$ plus a constant, so $s(x) = -x$. At $x = 2$ the score is $-2$: move to the left, towards the centre, where the data are. At the centre it is 0. It can be shown that the best possible denoising step moves a noisy point along the score of the noised data, which is why diffusion models are also called score-based models.

For a simulator the score is an old acquaintance. Put the Boltzmann distribution $p(x)\propto e^{-U(x)/k_BT}$ into the definition. The logarithm of $p$ is $-U(x)/k_BT$ plus a constant, and its slope is

$$
s(x) = -\frac{1}{k_BT}\frac{dU}{dx} = \frac{F(x)}{k_BT} .
$$

<div class="legend" markdown="1">
- $U(x)$: the potential energy.
- $F(x) = -dU/dx$: the force (Module 2).
- $k_BT$: the thermal energy.
- Other symbols: as in the list above.
</div>

For frames that follow the Boltzmann distribution, the score is the force divided by $k_BT$. Both point towards where the system prefers to be. For frames of beads, where the distribution is set by the potential of mean force, the same algebra gives the mean force divided by $k_BT$.

This link is used twice in the table of Kind 1. A model that has learned the probability density of equilibrium frames carries information about forces without having been shown any (second row). And a denoising task and a force-matching task can inform the same energy function (third row).

### Flow matching: learn a velocity

A diffusion model removes noise in many random steps. **Flow matching** reaches the same goal with a different object. Picture leaves on a river: each leaf is carried along by the velocity of the water at the place where it is. A flow-matching model is a network that gives such a velocity for every point and every moment. A sample of noise is placed in the "river" and carried by it until it has become a conformation:

$$
\frac{dx}{dt} = v_\theta(x,t), \qquad t \text{ from } 0 \text{ to } 1 .
$$

<div class="legend" markdown="1">
- $x$: the point being carried. At $t = 0$ it is a sample of noise, at $t = 1$ a generated conformation.
- $t$: a progress variable that runs from 0 to 1. It is not physical time, and the path is not a trajectory of the molecule.
- $dx/dt$: the rate at which the point moves as $t$ advances.
- $v_\theta(x,t)$: the velocity that the network gives for a point at $x$ when the progress is $t$.
- $\theta$ (theta): all the adjustable parameters of the network.
</div>

**Read it like this.** This is the statement "velocity is the change of position per unit of time", and a computer solves it in small steps, as an integrator does in Module 4. The name comes from the training. Pair each training frame $x_1$ with a sample of noise $x_0$, and join the two by a straight line, $x_t = (1-t)\,x_0 + t\,x_1$ (the simplest choice of path). A point that travels along this line from $t = 0$ to $t = 1$ has the constant velocity $x_1 - x_0$. The network is trained to match these velocities, on average over many pairs.

A small example: the noise $x_0 = 3$ and the data point $x_1 = 1$ give the velocity $-2$, and at $t = 0.25$ the point is at $0.75\times 3 + 0.25\times 1 = 2.5$. Once the starting noise is chosen, the path is fixed, so all the randomness of the samples comes from the starting point. Diffusion and flow matching are close relatives, and the choice between them does not change how you should read a paper's evidence.

### Normalising flows: an invertible transformation with a known density

A **normalising flow** is a third way to turn noise into data. It is one function, $x = f_\theta(z)$, built so that it can be run backwards: from every $x$ you can recover the $z$ it came from. Picture a sheet of rubber with a simple pattern of dots printed on it. Stretch it in some places and squeeze it in others, and the dots end up in a complicated pattern. Because you know how much each patch was stretched, you know how dense the dots are everywhere.

That knowledge is what sets this type apart. For one coordinate,

$$
p_X(x) = p_Z(z)\,\left|\frac{dz}{dx}\right| , \qquad x = f_\theta(z) .
$$

<div class="legend" markdown="1">
- $z$: the noise, a number drawn from a simple distribution such as a Gaussian.
- $x$: the generated value, obtained from $z$ by the function $f_\theta$.
- $f_\theta$: the network, an invertible function with parameters $\theta$.
- $p_Z(z)$: the probability density of the noise at $z$. It is known, because you chose the distribution.
- $p_X(x)$: the probability density of the generated values at $x$. This is what the formula delivers.
- $dz/dx$: how much $z$ changes per unit change of $x$, the inverse of the local stretching. The vertical bars take the absolute value.
</div>

**Read it like this.** Where the function stretches (a small range of $z$ is spread over a large range of $x$), the density goes down by the stretching factor, because the same amount of probability covers more ground. Example: $x = 2z$ with Gaussian noise. The point $z = 0.5$, where $p_Z = 0.352$, goes to $x = 1$, and $dz/dx = 1/2$, so $p_X(1) = 0.176$. In many dimensions the factor becomes the determinant in the formula of Module 17.

The name has two parts. "Flow", because the function is built as a chain of simple invertible steps through which the numbers pass. "Normalising", because run backwards it turns the data into a normal (Gaussian) distribution. A model trained by flow matching can be run backwards too, by following the velocity in reverse, so in principle it also has a density. Computing that density costs much more than drawing the sample.

### Boltzmann generators, and reweighting to the Boltzmann distribution

Every model so far learns the distribution of its training data. Its samples are as good as that learning, and nothing corrects them afterwards. A **Boltzmann generator** (Module 17) has two more things: a physical energy function $U(x)$ for the molecule, and a model whose sample density is known, such as a normalising flow. With both in hand the samples can be corrected.

The correction is called **reweighting**. The model generates the configuration $x$ with the density $p_{\text{model}}(x)$. The Boltzmann distribution requires a density proportional to $e^{-U(x)/k_BT}$. Give each sample a weight equal to the ratio of the two, and use weighted averages:

$$
w(x) = \frac{e^{-U(x)/k_BT}}{p_{\text{model}}(x)} , \qquad \langle A\rangle \approx \frac{\sum_{n} w(x_n)\,A(x_n)}{\sum_{n} w(x_n)} .
$$

<div class="legend" markdown="1">
- $x_n$: the $n$-th configuration generated by the model. The label $n$ runs from 1 to the number of samples.
- $p_{\text{model}}(x)$: the probability density with which the model generates $x$.
- $e^{-U(x)/k_BT}$: the Boltzmann weight of $x$, from the section on the levels of agreement.
- $w(x)$: the **importance weight** of the sample. A weight larger than those of the other samples means that the model produces this configuration too rarely, and a smaller one that it produces it too often.
- $A(x)$: any quantity computed from one configuration, such as a distance, or the number 1 if $x$ is folded and 0 if it is not.
- $\langle A\rangle$: the average of $A$ in the Boltzmann distribution.
- $\sum_n$: a sum over all the samples.
- $\approx$: the two sides agree better and better as the number of samples grows.
</div>

**Read it like this.** A configuration that the model produces twice as often as it should gets half the weight, and the two effects cancel. A constant factor common to all the weights cancels between the numerator and the denominator of the average, so the Boltzmann weight does not have to be normalised. Module 17 wrote the same weight with $\beta = 1/k_BT$ and with $p_X$ for the density of the model.

<div class="box key" markdown="1">
**Worked example: reweighting two states.** A model generates state A in half of its samples and state B in the other half. The Boltzmann populations are 80 % and 20 %. The weights are $w_A = 0.8/0.5 = 1.6$ and $w_B = 0.2/0.5 = 0.4$. Of 1,000 samples, the 500 in A carry a total weight of $500\times 1.6 = 800$ and the 500 in B carry $500\times 0.4 = 200$. The weighted fraction in A is $800/(800+200) = 0.8$, as it should be.

Now let the model be badly wrong: it generates B once in 1,000 samples. That one sample gets the weight $0.2/0.001 = 200$, and each of the other 999 gets $0.8/0.999 = 0.80$, a total of 800. The weighted fraction of B is $200/(200+800) = 0.2$, the right value, but it rests on a single sample. Another batch of 1,000 samples may contain no B at all, or two, and the answer would then be 0 or 0.33.
</div>

The second half of the example is the "overlap" condition of Modules 13 and 17. Reweighting is exact in principle. It works in practice only when the model already produces every important configuration reasonably often.

In the table of Kind 2, "samples with exact weights" refers to this. The word reweighting is also used in this module for a related correction: the frames of short simulations are given weights so that the populations of their states match a better estimate, taken from a Markov state model or from experiment.

### Emulating the dynamics step by step

The models above produce conformations with no order in time. One more type asks a different question: given the configuration now, where is the system a time $\tau$ later? The answer is again a distribution, because many futures are possible. It is written $p(x_{t+\tau}\mid x_t)$: the probability density of the configuration $x_{t+\tau}$ at the time $t+\tau$, given the configuration $x_t$ at the time $t$.

Here $t$ is physical time and $\tau$ (tau) is the length of the jump. Any of the generative techniques above can be trained to sample from this distribution.

The training examples are pairs of frames separated by $\tau$ in one trajectory, so the frames must be stored in their order in time. The jump $\tau$ is chosen far longer than an MD time step, and that is the source of the saving. Chaining jumps gives a trajectory with a time axis, from which rates can be read.

Module 16 met the same object in a simpler form: the transition matrix of a Markov state model is the table of these probabilities for a small number of discrete states. As there, the hard part is the slow processes. If the training trajectories contain few passages over a barrier, the model has few examples of the jumps that determine the rate.

## Kind 2: models that generate ensembles

<div data-videos="zaZAAWUISGE LStKhWcL0VE JZjeFBH0Jl4"></div>

These models do the second, third and fourth tasks: they produce conformations directly, with no simulation at the time of use. Such a model is often called an **emulator**, because it imitates the output of MD without doing what MD does. The table has one row per model or family of models.

Read each row with three questions from the earlier sections. What was the model trained on, and in which stages? At which level does the evidence test it: states, populations or rates? And is the reference MD or experiment?

| Model | Trained on | Output | Main evidence | Stated limit |
|---|---|---|---|---|
| AlphaFlow ([Jing et al. 2024](cite:alphaflow2024)) | AlphaFold weights, then PDB, then ATLAS (1,265 proteins × 300 frames) | All-atom ensembles | Per-residue flexibility correlates 0.85 with MD on 82 held-out proteins | Nothing slower than the 100 ns of ATLAS |
| BioEmu ([Lewis et al. 2025](cite:lewis2025)) | Predicted structures, then 172 ms of MD, then about 776,000 measured stabilities | Backbone ensembles for one chain | Free-energy error near 0.9 kcal/mol on 17 held-out domains | Single chains, one temperature, no ligands |
| aSAMt ([Janson et al. 2025](cite:asam2025)) | mdCATH, all five temperatures | Heavy-atom ensembles at a chosen temperature | Approaches held-out MD replicas on 90 test domains | Does not reproduce the Boltzmann weights of MD |
| BBFlow ([Wolf et al. 2025](cite:bbflow2025)) | ATLAS only, conditioned on a starting structure | Backbone ensembles | Flexibility correlation 0.90 on ATLAS, 0.84 on designed proteins | Cannot reach states far from the starting structure |
| idpSAM ([Janson and Feig 2024](cite:idpsam2024)) | Implicit-solvent ensembles of 3,259 disordered regions | C$\alpha$ ensembles of disordered peptides | Matches its training force field closely | Inherits that force field's error against experiment |
| Timewarp, ITO, MDGen ([Klein et al. 2023](cite:timewarp2023); [Schreiner et al. 2023](cite:ito2023); [Jing et al. 2024](cite:mdgen2024)) | Time-ordered trajectories of peptides or a few small proteins | Large time steps or whole trajectories | Kinetics of unseen tetrapeptides; folding times within about a factor of 3 for four mini-proteins | Not shown for proteins of ordinary size |
| Boltzmann generators ([Noé et al. 2019](cite:noe2019); [Klein and Noé 2024](cite:tbg2024)) | An energy function plus a few samples | Samples with exact weights | Transfer across dipeptides | Has not scaled beyond small systems |

### Reading the table of generators

The numbers in the fourth column are metrics. The one that appears most often is a correlation.

<div class="box maths" markdown="1">
**Maths you need here: the correlation coefficient.** Take two lists of numbers of the same length, for example the flexibility of each residue from the model and from MD. The **correlation coefficient** $r$ is one number between $-1$ and $+1$ that says how well the two lists rise and fall together. $r = 1$: plotted against each other, the pairs of values lie exactly on a rising straight line. $r = 0$: no straight-line relation. $r = -1$: they lie exactly on a falling straight line.

A small example: $x = (1, 2, 3, 4)$ and $y = (1, 3, 2, 4)$. Both lists have the mean 2.5. The deviations from the mean are $(-1.5, -0.5, 0.5, 1.5)$ and $(-1.5, 0.5, -0.5, 1.5)$. Multiply them pair by pair and add: $2.25 - 0.25 - 0.25 + 2.25 = 4$.

Then divide by the square root of the product of the two sums of squared deviations, $\sqrt{5\times 5} = 5$. The result is $r = 4/5 = 0.8$. The two middle values of $y$ are in the wrong order, and that lowers the coefficient from 1 to 0.8.

Three cautions. A correlation ignores scale: if a model predicts every flexibility ten times too large, $r$ is still 1, which is why some results are quoted as an error in ångström instead. It comes in two variants, Pearson (computed from the values, as above) and Spearman (computed from the rank order), and numbers from different papers can be compared only if the variant and the test set are the same. And a value has to be judged against a baseline and a ceiling. More in the [toolbox](maths.html#averages).
</div>

**The column "Trained on".** A list joined by "then" is a sequence of pretraining and fine-tuning stages. "Predicted structures" are structures computed by a structure-prediction network, as opposed to experimental ones. A "measured stability" is an experimental value of the free-energy difference between the folded and the unfolded state of a protein. "1,265 proteins × 300 frames" is 379,500 training frames. "Implicit-solvent" simulations replace the water by a formula for its average effect (Module 15), and a disordered region is a stretch of protein without a stable fold.

**The column "Output".** "All-atom" means every atom, and "heavy-atom" every atom except hydrogen. "Backbone" means only the atoms of the main chain, without side chains, and "C$\alpha$" means a single point per residue, its central carbon atom. A coarser output is easier to learn and says less: the side-chain contacts of a binding interface, for example, cannot be seen in a backbone ensemble.

**The column "Main evidence".** "Held-out" systems were kept out of training. "Per-residue flexibility correlates 0.85 with MD" means: compute the flexibility of every residue from the model's ensemble and from the MD trajectories, and take the correlation coefficient of the two lists. "Free-energy error near 0.9 kcal/mol" is the typical difference between a free-energy difference computed from the model's populations and its reference value. By the conversion of the section on levels of agreement, that is 3.8 kJ/mol, or a factor of about 4.5 in a ratio of populations.

"Approaches held-out MD replicas" uses a ceiling: the model's ensemble is compared with an MD run, and the result is set against how well a second, independent MD run agrees with the first. "Kinetics" and "folding times" are tests at level 3. A folding time is the average time a protein takes to go from the unfolded to the folded state. In the rate formulas of Module 16, an error of a factor of 3 in a rate corresponds to an error of $k_BT\ln 3 = 2.7$ kJ/mol in a barrier height. Dipeptides and tetrapeptides are very small peptides.

**The column "Stated limit".** "Does not reproduce the Boltzmann weights of MD" is a failure at level 2: the states are there, with the wrong populations. "Inherits that force field's error against experiment" is the difference between agreeing with MD and agreeing with experiment. "Has not scaled" means that the method has not been made to work for large molecules.

What the evidence across these papers says:

1. **A structure prior is needed.** Removing the PDB stage from AlphaFlow lowered its agreement with MD (a correlation of 0.48 fell to 0.29). BioEmu found that pretraining on predicted structures chosen to show several conformations per sequence beat pretraining on the PDB.
2. **MD adds what static structures lack.** A model trained on PDB structures alone matches the distributions of only about 0.1 to 1 µs of MD on the fast folders ([Lu et al. 2024](cite:str2str2024)), and a PDB-trained model makes disordered proteins too compact until it is fine-tuned on simulated ensembles.
3. **The number of different systems drives transfer.** idpSAM is poor below about 500 training sequences and improves sharply up to about 1,000. BioEmu's free-energy error falls as its training domains go from 1 % to 10 % to 100 %.
4. **Short MD teaches which states exist, not how populated they are.** aSAMt finds the right basins of the fast folders but not their free energies, because 500 ns runs contain few transitions. BioEmu corrects its training frames with Markov models or with measured stabilities for this reason.
5. **A model inherits the force field of its data.** idpSAM reproduces its training simulations (radius of gyration within 0.06 nm) and therefore their error against experiment (0.70 nm). aSAMt's melting temperatures are about 130 K too high.
6. **Knowing the starting structure carries most of the short-time signal.** With the structure as input, a model trained from scratch on ATLAS matches one built on AlphaFold.
7. **Rare and distant states are the common failure.** BioEmu finds only 49 % of the "apo" forms of cryptic pockets. Models trained on 100 ns data miss conformations that the longer reference runs visit.

### The seven points, explained

**Point 1, the structure prior.** This is the first meaning of prior: what the model knew about protein structure before it saw any simulation. "Removing the PDB stage" is an ablation of one training stage. The second sentence compares two choices of pretraining data.

**Point 2, static structures.** A PDB entry is one snapshot of a protein, or a few. The model trained only on such snapshots produced ensembles that resemble what MD explores in 0.1 to 1 µs. The fast-folder trajectories are far longer than that: 8.2 ms for 12 proteins in the table of data sets. "Too compact" means that the chain is, on average, more tightly balled up than it should be.

**Point 3, transfer.** Both sentences describe data-scaling experiments: train the same model on a part of the data, and follow the test result as the part grows. "Transfer" is performance on sequences outside the training set.

**Point 4, states and populations.** This is the difference between level 1 and level 2. "Basins" are states, and "free energies" are their populations. A **transition** is one passage from one state to another. A ratio of populations estimated from a handful of passages is mostly chance, as the section on data sets explained.

A **Markov state model** (Module 16) is one way out. It counts the jumps between small states in many short trajectories, and computes from those counts the populations that a very long simulation would give. Those populations are then used to reweight the frames. Measured stabilities serve the same purpose with numbers from experiment.

**Point 5, the inherited force field.** The **radius of gyration** is the root-mean-square distance of the atoms from the centre of the molecule, a measure of its overall size (Module 11). The two numbers are the two distances of the section on levels of agreement: 0.06 nm separates the model from its training simulations, and 0.70 nm separates those simulations, and therefore the model, from experiment. The melting temperature was defined in Kind 4.

**Point 6, the starting structure.** "From scratch" means starting from random parameters, with no pretraining. "Built on AlphaFold" means fine-tuned from the AlphaFold weights. The "short-time signal" is the fluctuation around the starting structure that 100 ns runs contain.

**Point 7, rare and distant states.** "Apo" is the form of a protein without a bound ligand, and "holo" is the form with it. A **cryptic pocket** is a binding pocket that cannot be seen in the usual structure of the protein and appears only in some of its conformations. "Finds 49 %" is a coverage metric, at level 1: the percentage of the known target conformations that turn up among the samples of the model. The second sentence is the length limit of the data-set section at work: what a 100 ns run never visits, the model never sees.

<div class="box warn" markdown="1">
**If you design proteins, read this one twice.** On 50 computationally designed proteins, the two models that rely on evolutionary information predicted unstable conformations: flexibility errors of 4.2 Å (BioEmu) and 4.8 Å (AlphaFlow without a template), against 0.26 Å for the structure-conditioned BBFlow ([Wolf et al. 2025](cite:bbflow2025)). Designed sequences have no homologues, so a model that learned from families has little to go on. Flexibility predictors built on protein language models show the same drop on designed backbones ([Viliuga et al. 2026](cite:backflip2)). Test any such tool on designs before trusting it on yours.
</div>

The reasoning of this box rests on where two of the models get their information. **Evolutionary information** is what can be read from the family of a protein. A **multiple sequence alignment** (MSA) lines up the sequences of many homologues, so that each column shows which amino acids evolution has accepted at one position. A network can infer a great deal about the three-dimensional structure from the patterns in such an alignment. A **protein language model** has absorbed similar patterns from very large collections of sequences.

A designed protein has a sequence produced by a design program and not by evolution. It has no family, so its alignment has a single row and carries no such patterns. A **template** is a known three-dimensional structure given to a model as an extra input, and a **structure-conditioned** model receives the structure itself as its input, so it does not depend on a family.

A flexibility error is the typical difference between the flexibility of a residue in the model's ensemble and in the reference. The errors are in ångström (1 Å = 0.1 nm): 4.2 Å is 0.42 nm and 0.26 Å is 0.026 nm, a ratio of 16. This is a test out of distribution, in the sense of the vocabulary section. Designed proteins differ from the natural proteins that the models were trained on, and a good score on natural proteins did not carry over.

## Kind 3: MD as a feature or a label for something else

In this kind the simulation is one ingredient of a model that predicts something else. It can enter in four ways, and the four paragraphs below show all of them:

- as a **label**: the model is trained to output a quantity that was computed from MD, such as a flexibility;
- as a **feature**: a quantity computed from MD is given to the model as an input, next to the structure or the sequence, to help it predict something measured in the laboratory;
- as an **extra training target**: the main job of the model is something else, and it is asked to predict an MD quantity as well, in the hope that this teaches it something useful;
- as **pretraining** data: the model is first trained on a task that uses simulation frames, and is then fine-tuned for its main job.

The question to ask each time is the one that an ablation answers. How much better is the model with the MD ingredient than without it?

**Flexibility.** This is the clearest case where MD data add information. The same network scores 0.76 to 0.78 against MD flexibility when trained on MD, and 0.47 to 0.56 when trained on crystallographic B-factors ([Kouba et al. 2025](cite:flexpert)). Two cautions: two MD replicas of the same protein agree only to about 0.88, which is the ceiling, and a parameter-free elastic network model already reaches 0.76 to 0.79. The headroom for learning is about a tenth (0.09 to 0.12 between the elastic network and the ceiling).

Read the scores in that paragraph on a scale where 1 is perfect agreement, like the correlation coefficient. **Crystallographic B-factors** are numbers attached to each atom of a crystal structure that say how smeared out the atom appears in the experiment. They reflect motion, and also disorder that is frozen into the crystal (Module 11).

An **elastic network model** replaces the protein by beads joined by springs wherever two residues are close in the structure, and computes the flexibility from the vibrations of that network (the normal modes of Module 2). "Parameter-free" means that nothing in it was fitted to MD data. It plays the part of the baseline, and the agreement between two replicas plays the part of the ceiling.

**Binding affinity of small molecules.** When the same model is trained with and without the MD ingredient, the gain in correlation with experiment is small: +0.03 ([Min et al. 2024](cite:dynaformer_2024)), +0.06 ([Wu et al. 2022](cite:protmd_2022)), and +0.02 to +0.03 with none at all on a random split ([Poziemski et al. 2026](cite:mdts_2026)). That last study also found that features from 20 ns of MD worked better than from 200 ns, and that a model given no information about the protein reached 0.52 where the full model reached 0.60. Most published numbers in this area report no such control.

**Binding affinity** is how strongly a small molecule (the ligand) holds on to its protein. It is measured as a dissociation constant or, which is the same information, as a binding free energy (Module 3, and the [primer](physics.html#equilibrium)). "Correlation with experiment" is the correlation coefficient between predicted and measured affinities over the test complexes. "The MD ingredient" is whatever the simulations contributed to the model, as input features or as pretraining data. The three gains quoted are results of ablations: the same model, with and without.

Two comparisons in the paragraph deserve attention. The random split, defined in the vocabulary section, is the easiest exam, and on it the third study found no gain at all. And a model that was told nothing about the protein reached 0.52 where the full model reached 0.60, so a large part of the score did not need any information about the protein. A **control** is a comparison of this kind, designed to rule out a simpler explanation of a good score.

<div class="box maths" markdown="1">
**Maths you need here: how sure is a correlation coefficient?** A correlation computed from a finite test set would come out a little different on another test set of the same size. For a coefficient $r$ computed from $n$ independent pairs, a rough size of this uncertainty is $(1-r^2)/\sqrt{n}$. Example: $r = 0.6$ from $n = 300$ test complexes (an illustration) gives $(1-0.36)/\sqrt{300} = 0.037$. A gain of 0.03 is then about as large as the uncertainty of each of the two coefficients.

When two models are scored on the same test set, part of their error is shared, and the comparison can be sharper than this estimate suggests. The proper tool is therefore a paired test. One common form: recompute both coefficients on many random resamplings of the test set (a bootstrap), and look at the spread of their difference. More in the [toolbox](maths.html#averages).
</div>

**Structure prediction.** Boltz-2 mixes three MD sets into its training with small weights, supervises on distance distributions and on B-factors computed from MD, and adds a switch asking for "MD-like" output ([Passaro et al. 2025](cite:boltz2)). The measured effect is better agreement with MD flexibility. Its authors report no model trained without MD, so there is no evidence that MD improved its structures or its affinity predictions.

Three expressions need a word. In "mixes three MD sets into its training with small weights", a weight is the share of the training examples that comes from each source, so MD frames are a small part of what the model sees. "Supervises on" means "is trained to reproduce". A distance distribution is, for a pair of residues, the histogram of their distance over a trajectory.

B-factors can be computed from MD because the B-factor and the RMSF are linked by a formula given in Module 11. The "switch" is a conditioning input: a flag with which the user asks for output that resembles simulation frames. The last sentence of the paragraph is about a missing ablation. With no version of the model trained without MD, the contribution of MD to the other outputs cannot be read off.

**Protein-protein affinity.** One study uses MD flexibility as an extra training target for protein-protein and protein-peptide affinity and gains 0.07 in correlation, with trajectories available for only 383 of about 12,000 complexes ([Bogdanova et al. 2026](cite:hybindnn)). In the same model, removing the protein language model costs about thirty times more, measured as the rise in the mean squared error of the predicted affinities (about 46, against 1.51 for removing the MD target).

An extra training target works like this: the model predicts the affinity and, from the same internal representation, the flexibility computed from MD. Learning the second is hoped to improve the first. A **protein language model** is a network trained on very large collections of protein sequences, with no structures, to predict amino acids that were hidden from it. Its internal numbers for a sequence, called an **embedding**, are used as input features by other models.

The paragraph compares two ablations in the same model: one removes the MD target, the other removes the language-model input. The two costs are compared in the mean squared error, which is the average squared difference between predicted and measured affinity. The factor of thirty is not a factor on the 0.07 of correlation. Trajectories existed for 383 of about 12,000 complexes, which is about 3 %.

## What a model needs, in one list

This list turns the evidence into advice for someone who plans to produce simulation data for training. Each point follows from results quoted in the sections above.

1. **Decide the label before you simulate.** Forces for a force field (write them out during the run). Frames for a generator. A trajectory summary for a predictor. Time-ordered frames at short intervals if kinetics is the goal.
2. **Many different systems, before long simulations of a few.** Every data-scaling result above points the same way.
3. **Enough sampling per system for the claim you want.** Fluctuations need about 100 ns. Populations need many transitions, or reweighting with a Markov model or with experimental data.
4. **Deliberate coverage of what equilibrium runs rarely visit.** Close contacts, distorted geometries, high temperatures. Without them, models have no reason to avoid those regions.
5. **A prior that carries the physics you already know.** Simple bonded and repulsive terms for a force field, a structure-prediction model for a generator, conservative forces for any potential.
6. **One consistent protocol, written down.** The model will reproduce the force field, temperature and conditions of its data, including their errors, and will not transfer to other conditions.
7. **Evaluation that could fail.** Run the model and look at observables, not only at the loss. Compare with the agreement between two MD replicas, and with a cheap baseline (an elastic network, a ligand-only model). Split the data by sequence similarity. Test on the kind of protein you will use it for.
8. **An ablation.** If you claim that MD helps, train the same model without it.

A few words in the list have not been defined yet.

- *Point 1.* "Time-ordered frames at short intervals" are pairs of frames separated by a known, short time, which is what a step-by-step emulator learns from.
- *Point 3.* The "claim" is the level of agreement you want to assert: states, populations or rates.
- *Point 5.* **Conservative forces** are forces that are minus the slope of an energy function (Module 2). A network that outputs forces directly, without an energy, can produce forces that are not of this type, and a simulation run with them gains or loses energy (Module 17).
- *Point 6.* A **protocol** is the complete recipe of the simulations: force field, water model, temperature, pressure, salt, time step, and what was saved and how often (Module 10).
- *Point 7.* An **observable** is a quantity computed from a simulation that has a physical meaning and can be compared with a reference: a radius of gyration, the distribution of a distance, a free-energy difference. A test "could fail" when a poor model would score visibly worse on it than a good one. That is the case for a test against a baseline, below a known ceiling, on proteins unrelated to the training set. A ligand-only model is the control met in Kind 3: an affinity model that is given no information about the protein.

## What has not been shown

"Not shown" means here that no paper among those read reports the test. It does not mean that the thing cannot be done. The list matters because the uses that many readers have in mind, protein-protein binding and designed proteins, are in it.

As of the papers read:

- No learned force field or atomistic potential has been trained on, or tested for, **protein-protein binding thermodynamics**.
- No ensemble generator has been validated for **complexes**. BioEmu's first version is single-chain; a second version announced in October 2026 lists complexes and ligands in its description, but no paper or evaluation was found.
- **Kinetics** have been tested only for peptides and four mini-proteins.
- No paper separates the effect of total simulation time from the number of systems, for proteins.
- None of the affinity studies read reports a statistical test on the difference between a model with and without MD.
- Claims that MD lets a model "learn the entropy of binding" are made in several papers and tested in none.

Some words in the list. **Binding thermodynamics** is the binding free energy together with its split into an energy part and an entropy part ([primer](physics.html#thermodynamics)). "Validated" means tested against a reference on systems that were kept out of training. To separate total simulation time from the number of systems, one would have to vary one of them while holding the other fixed, which is the ablation idea applied to a data set.

A **statistical test** on a difference asks whether the difference is larger than what chance alone would produce with a test set of that size (see the box on the uncertainty of a correlation). The **entropy of binding** is the part of the binding free energy that comes from the change, on binding, in the number of configurations open to the two partners and to the water. A claim that a model has learned it needs a test in which that entropy is known.

## Check yourself

<details markdown="1"><summary>1. A colleague wants to train a coarse-grained force field from the ATLAS trajectories. What is the first obstacle?</summary>
ATLAS stores coordinates only. Force matching needs the forces on the atoms for each frame. They would have to be recomputed from the saved coordinates with the original force field, which needs the coordinates at full precision and a second pass over all the data. mdCATH stores forces and avoids this.
</details>

<details markdown="1"><summary>2. An emulator trained on 100 ns trajectories gives two conformations of your protein with populations of 80 % and 20 %. Can you report a free-energy difference of 3.4 kJ/mol?</summary>
Not on that basis. The arithmetic is right ($k_BT\ln(0.8/0.2)$ is 3.4 kJ/mol, with the two populations 0.8 and 0.2 and the thermal energy $k_BT = 2.48$ kJ/mol at 298 K), and the populations that go into it are not established. Runs of that length contain few or no transitions between distinct conformations, so the frequencies in the training data reflect where the simulations started, and the model reproduces them. The model can tell you that both states are plausible. Populations need MD with many transitions, a Markov model, or experimental data.
</details>

<details markdown="1"><summary>3. A paper reports that adding MD features raised the correlation with measured affinities from 0.50 to 0.64. Name three things to check.</summary>
Whether anything else was added at the same time (in one such case quantum-chemical charges were added together with the MD features). Whether the test proteins are dissimilar to the training proteins. What a model with no protein information scores on the same test, and whether any uncertainty is given for the difference.
</details>

<details markdown="1"><summary>4. Why might an emulator that works well on natural proteins fail on a designed binder?</summary>
Models that take a multiple sequence alignment or language-model embedding as input learned from families of related natural sequences. A designed sequence has no relatives, so that input carries little information. On 50 designed proteins such models predicted unstable conformations while a model conditioned on the designed structure stayed accurate.
</details>

<details markdown="1"><summary>5. A paper divides the frames of its trajectories at random into a training set and a test set, and reports a low test loss. Why does that say little about a new protein?</summary>
Neighbouring frames of one trajectory are nearly the same configuration, so almost every test frame has a near copy in the training set. This is data leakage, and the low test loss shows only that the model can reproduce what it has seen. The same proteins are also on both sides of the split. An honest test keeps whole proteins out of training, and keeps out their relatives as well by splitting on sequence identity.
</details>

<details markdown="1"><summary>6. A generator produces state A in 90 % of its samples and state B in 10 %. The Boltzmann populations are 60 % and 40 %. Which weights correct the samples, and what must be known to compute such weights for a real model?</summary>
The weight is the wanted probability divided by the probability with which the model generates the sample: $w_A = 0.6/0.9 = 0.67$ and $w_B = 0.4/0.1 = 4$. Check with 1,000 samples: $900\times 0.67 = 600$ and $100\times 4 = 400$, which is 60 % and 40 % of the total weight. For a real model two things must be known for every sample: its energy $U(x)$, for the Boltzmann weight, and the density $p_{\text{model}}(x)$ with which the model produces it. A Boltzmann generator has both. An emulator trained on frames alone has no energy function to reweight against.
</details>

<details markdown="1"><summary>7. The frames of a long trajectory are shuffled at random before a model is trained on them. Which of the three levels of agreement can the model still learn?</summary>
Levels 1 and 2. The shuffled frames still show which conformations exist and how often each one occurs. Level 3 is lost: rates and pathways are contained in the order of the frames in time, and shuffling destroys it.
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
