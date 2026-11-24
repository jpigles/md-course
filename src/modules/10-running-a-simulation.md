---
num: 10
title: Running a simulation from a PDB file to a production trajectory
short: Running a simulation
part: Part III · Practice
hours: 8
summary: Carry out the full workflow (prepare, solvate, neutralise, minimise, equilibrate, produce) in GROMACS and in OpenMM, knowing what every step and every setting is for.
videos: 10
papers: M
tags: practical-setup
---

<div class="box goal" markdown="1">
#### After this module you can

- prepare a structure: missing atoms, protonation states, termini, disulfides;
- build a solvated, neutral system at a chosen salt concentration and compute how many ions it needs;
- explain what energy minimisation and each equilibration stage do;
- read and write a GROMACS `.mdp` file and an OpenMM script line by line;
- recognise the common failures and list what a methods section must report.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

The earlier modules took an MD program apart: the force field ([Module 5](05-force-field-form.html), [Module 6](06-force-field-parameters.html)), the periodic box and the electrostatics ([Module 7](07-boundaries-electrostatics.html)), the thermostat and the barostat ([Module 8](08-thermostats-barostats.html)), the constraints ([Module 9](09-constraints.html)) and the integrator that moves the atoms ([Module 4](04-integrators.html)). This module puts the parts together. You start from a file of atomic coordinates taken from a database, and you end with a trajectory that can be analysed.

There is no new theory here and there are no derivations. What the module adds is the reason for each step of the standard recipe. A recipe followed without its reasons works until something unusual happens, and then you cannot tell which step failed. So for every step the text answers the same three questions:

1. What is physically being done to the system?
2. What goes wrong if the step is skipped?
3. How do you tell that it worked?

The module has four layers:

1. **Build the system** (steps 1 to 4). Turn an experimental structure into a complete, chemically sensible model in a box of salt water.
2. **Relax it** (steps 5 to 7). Remove the damage done by building, then bring the system to the temperature and the density of the experiment.
3. **Run and plan** (step 8 and the planning section). The production run, with every line of its input explained, in two programs: GROMACS and OpenMM.
4. **Diagnose and report.** The common failures, and what a reader needs in order to repeat your work.

The commands and input files are shown exactly as you would type them. After each block, a table explains every option and names the module in which the idea behind it was introduced. The few formulas are arithmetic: how many ions, how large a box, how many steps.

<div class="box key" markdown="1">
**Run it yourself.** Two notebooks for Google Colab run this whole workflow on a real protein, hen egg-white lysozyme (PDB entry 1AKI), on a free GPU. One uses the GROMACS commands and the five parameter files of this lesson, exactly as printed here. The other uses OpenMM. Each downloads the structure, builds the box with water and ions, minimises, equilibrates with the protein restrained, runs 1 ns of production and analyses the trajectory (RMSD, radius of gyration, flexibility of each residue, an error bar, a movie). They need a Google account and nothing installed on your computer.

<a class="btn" href="https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_gromacs.ipynb" target="_blank" rel="noopener">Open the GROMACS notebook in Colab</a> <a class="btn" href="https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb" target="_blank" rel="noopener">Open the OpenMM notebook in Colab</a>

Both notebooks are files in the repository of this course (see them on GitHub: [GROMACS](https://github.com/jpigles/md-course/blob/main/notebooks/md_lysozyme_gromacs.ipynb), [OpenMM](https://github.com/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb)). Both were run from start to finish on Colab with a T4 GPU on 24 November 2026. The GROMACS notebook took about twelve minutes: two to install GROMACS, under seven for the 1 ns production run (about 210 ns per day). The OpenMM notebook took under ten minutes, of which 4.5 for the production run (about 320 ns per day).
</div>

### How to read the commands and the files

GROMACS is a collection of command-line tools. Each one is started by typing `gmx`, then the name of the tool, then its options. OpenMM is a Python library: you write a short script and run it. The conventions below are enough to read every block in this module.

| You see | It means |
|---|---|
| `gmx editconf -d 1.2` | Run the GROMACS tool called `editconf`. An option starts with a dash and is followed by its value: here the option `-d` gets the value 1.2. An option without a value, such as `-ignh`, switches something on. |
| `-f`, `-o`, `-p` | Wherever they appear in this module, `-f` is an input file (the structure, or for `gmx grompp` the parameter file), `-o` is the file that is written, and `-p` is the topology. The other letters change from tool to tool. |
| `# text` | A comment in a shell or Python block. The computer ignores it. |
| `; text` | A comment in a GROMACS input file. |
| `name = value` | One setting in a GROMACS parameter file. |
| `a && b` | Shell syntax: run command `a`, then run command `b` only if `a` ended without an error. |
| `125_000` | In Python, the number 125000. The underscore only makes long numbers easier to read. |
| `2.4 * unit.nanometer` | In OpenMM every quantity carries its unit. This is 2.4 nm. |

The workflow passes the system from one file to the next. These are the file types you will meet:

| File | What it holds |
|---|---|
| `.pdb` | A **structure file** in the format of the Protein Data Bank: one line per atom, with the name of the atom, the residue it belongs to and its three coordinates. |
| `.gro` | The GROMACS structure file: the coordinates of every atom, and the size and shape of the box. |
| `.top` | The **topology**: which atoms the system contains, which are bonded to which, and the force-field parameters of each atom (type, charge, mass). It contains no coordinates ([Module 6](06-force-field-parameters.html)). |
| `.mdp` | The run parameters: a list of `name = value` settings that say what kind of run to do. |
| `.tpr` | The run input file. One tool packs structure, topology and parameters into this single file, and the simulation engine reads it. |
| `.cpt` | A **checkpoint**: the complete state of a run at one instant, from which the run can be continued. |

<div class="box warn" markdown="1">
**Names that mean two things in this module.** The option `-c` means "centre the solute" in `gmx editconf` and "the file with the starting coordinates" in `gmx grompp`. The setting `nsteps` is the largest number of steps allowed in a minimisation and the exact number of steps taken in an MD run. Among the symbols, $k$ is the spring constant of a restraint, while $k_B$ is the Boltzmann constant. $c$ is a concentration, and has nothing to do with the speed of light. $h$ is the step length of the minimiser: it is neither a time step nor Planck's constant. $T$ is a temperature and $t$ is a time. The letter $N$ with a subscript counts different things each time: ion pairs, water molecules, frames, degrees of freedom.

The letter $e$ is the charge of a proton where a net charge is given "in units of $e$", and the number 2.718 in $e^{-t/\tau}$. The word "padding" is the distance from the solute to the box face in the text and in `gmx editconf -d`, and the distance from the solute to its nearest periodic copy, twice as much, in the `padding` argument of OpenMM.
</div>

### How to read the formulas

Every displayed formula in this course is followed by a list that says what each letter in it means. The notation below is new in this module. The general conventions (bold letters for vectors, bars for lengths, angle brackets for averages) are in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| mol/L, M, mM | A concentration: moles of a substance per litre of solution. M is short for mol/L, and 1 mM is 0.001 mol/L. |
| $N_A$ | Avogadro's number, $6.022\times10^{23}$: the number of particles in one mole. |
| $a\leftarrow b$ | "Replace $a$ by $b$." An update that the program carries out, not an equation to be solved. |
| $\vert\mathbf F\vert_{max}$ | The largest force on any single atom at this moment. |
| $\max(a,b)$ | The larger of the two numbers $a$ and $b$. |
| $\approx$ | "Is approximately equal to." |

## The workflow at a glance

<div data-videos="EFtbEkuJ9tk ZKNUR5Uz2r0 HPk5SiEqFIM _CYsaBhAEeA"></div>

An MD program needs three things before it can take one step: the position of every atom, a rule that gives the force on every atom, and the conditions of the run (temperature, pressure, length). Steps 1 to 4 of the table produce the positions and the rule. Steps 5 to 8 are four runs of the same engine under different conditions, each starting where the one before stopped. Step 9 is the subject of [Module 11](11-analysis-statistics.html).

| Step | What you do | Why | Module |
|---|---|---|---|
| 1 | Get and clean the structure | The model must be chemically complete and sensible | this one |
| 2 | Choose force field and water model | They define the physics | 5, 6 |
| 3 | Define the box, add water | Bulk-like environment | 7 |
| 4 | Add ions | Neutral system, physiological ionic strength | 7 |
| 5 | Energy minimisation | Remove clashes that would make the first step explode | this one |
| 6 | NVT equilibration with restraints | Bring the solvent to temperature around a fixed solute | 8 |
| 7 | NPT equilibration | Bring the density to its equilibrium value | 8 |
| 8 | Production | Collect data | 4, 8, 9 |
| 9 | Checks and analysis | Decide whether the data mean anything | 11 |

The order follows from what each step needs. Water cannot be added before the box exists. Ions cannot be counted before the charge of the solute is known, and that charge is fixed by the protonation states of step 1 and the force field of step 2. Heating a system that still has overlapping atoms makes it fly apart, so minimisation comes before any dynamics. And a barostat acting on a system that is not yet at its temperature rescales the box violently, so the constant-volume stage comes before the constant-pressure one.

Several words of the table are used in the rest of the module:

- The **solute** is the molecule you want to study: the protein, with anything bound to it. The **solvent** is what is added around it, that is, water and ions.
- A **force field** is the formula and the list of parameters that give the potential energy $U$ for any arrangement of the atoms ([Module 5](05-force-field-form.html)). A **water model** is the force-field description of one water molecule: its geometry, its charges and its Lennard-Jones parameters ([Module 6](06-force-field-parameters.html)).
- The **box** is the volume that is simulated. It is periodic: surrounded on all sides by copies of itself, so that there is no surface ([Module 7](07-boundaries-electrostatics.html)). "Bulk-like" means "as in the middle of a large volume of liquid, far from any wall".
- A **clash** is a pair of atoms that sit closer together than two real atoms can. **Energy minimisation** moves the atoms downhill in potential energy until the forces are small. A run "explodes" when atoms receive forces so large that they fly apart and the program stops.
- **Equilibration** is the first part of a simulation, during which the system loses the memory of how it was built. Its data are not used for results.
- **Production** is the run whose data you keep and analyse.
- **Restraints** are extra springs, added to the force field for a while, that hold chosen atoms near chosen positions. The "fixed solute" of step 6 is a solute held by such springs. It is not frozen.

<div class="box physics" markdown="1">
**Physics you need here: NVE, NVT and NPT.** The letters name what is held fixed during a run. $N$ is the number of atoms, $V$ the volume of the box, $T$ the temperature, $P$ the pressure and $E$ the total energy.

- **NVE**: nothing is controlled. The atoms follow Newton's law and the total energy stays constant ([Module 2](02-classical-mechanics.html)).
- **NVT**: the box is fixed and a **thermostat** is switched on. A thermostat is an addition to the equations of motion that feeds kinetic energy into the atoms or takes it out, so that the temperature fluctuates around a target value.
- **NPT**: thermostat and **barostat** are both on. A barostat changes the size of the box, and moves the atoms with it, so that the pressure fluctuates around a target value. The volume is then free to find its own value.

In statistical mechanics each of these is called an *ensemble* ([Module 3](03-statistical-mechanics.html)). Experiments in a test tube are done at fixed temperature and pressure, so production runs are usually NPT. The algorithms are the subject of [Module 8](08-thermostats-barostats.html). For what temperature and pressure mean for a collection of atoms, see the primer on [temperature](physics.html#temperature) and on [pressure](physics.html#pressure).
</div>

## Step 1: the starting structure

<div data-videos="YQ8eRyScuyk RvvSvC8YyVo"></div>

*What is done.* You turn a file from a structure database into a complete and chemically correct model: every atom present, every chemical choice made.

*If it is skipped.* The tools of step 2 stop with an error when an atom they expect is missing. Or, worse, they build something that runs but is a different molecule from the one you meant, for example with a charge where the real protein has none. No later step repairs that.

*How to tell that it worked.* Step 2 builds the topology without errors, the net charge of the model is the whole number you expect from your choices, and the structure looks right in a molecular viewer.

A **structure file** lists atoms, one per line: the name of the atom, the residue it belongs to (a residue is one amino acid of the chain), the chain, and three coordinates. The usual format is PDB, named after the Protein Data Bank, the public archive of experimentally determined structures. Each entry has a four-character code, such as 1AKI for the lysozyme of exercise 1. Such a file records where an experiment found atoms. It was not written as the input of a simulation, and this step closes the gap between the two.

A simulation can only be as good as its starting model. Go through this list every time. Each of the seven items is given first in its short form and then explained.

**Source.** A crystal or cryo-EM structure, an NMR model, or a prediction (AlphaFold and similar). For a predicted complex, the interface may be wrong in ways that MD will not repair on accessible time scales.

The three experimental methods give different things. X-ray crystallography gives the positions of the heavier atoms (carbon, nitrogen, oxygen, sulfur) of molecules packed in a crystal. Cryo-electron microscopy (cryo-EM) builds a three-dimensional map from many images of frozen molecules. NMR measures distances between atoms in solution and gives a bundle of models that all agree with the data: start from one of them, or from several in separate runs. A prediction is computed from the amino-acid sequence and is not a measurement.

The warning about predicted complexes is about time scales. An *interface* is the surface where the two molecules of a complex touch. If the prediction has placed one partner wrongly, correcting it means rearranging the whole interface. That is a slow, collective motion, which takes far longer than the nanoseconds to microseconds that a simulation covers ([Module 1](01-what-is-md.html)). The run then shows a complex that looks stable and is wrong.

**Missing atoms and residues.** Crystal structures lack hydrogens and often lack flexible loops and side chains. Build missing side chains (PDBFixer, MODELLER, Swiss-PdbViewer, CHARMM-GUI). For a missing loop either model it or cap the chain ends, and say which.

Hydrogen has a single electron, and X-rays are scattered by electrons, so hydrogens are invisible in most crystal structures. That is no problem: the tools of step 2 add every hydrogen from the known chemistry of each residue. A loop or a side chain is missing for another reason. It was moving or disordered in the crystal, so no definite position could be recorded. The force field cannot leave atoms out: it describes each residue by a template with a fixed list of atoms ([Module 6](06-force-field-parameters.html)), and a residue with atoms missing does not match its template.

A missing loop leaves the chain in two pieces. If you do nothing, each piece gets a charged end where the real protein has an ordinary peptide bond. The two honest choices are to model the loop (its conformation is then a guess) or to *cap* the two loose ends with small neutral groups, as described under Termini below. "Say which" means: write it in your methods section.

**Alternate conformations.** Keep one (usually the A conformer).

In a well-resolved crystal a side chain is sometimes seen in two positions, because different copies of the protein in the crystal have it in different places. The file then lists the same atoms twice, labelled A and B. A simulated molecule has each atom once, so one set has to be chosen. If the two positions differ in a region that matters for your question, that is a reason for a second simulation.

**Termini.** Decide between charged termini (NH$_3^+$, COO$^-$) and neutral caps (acetyl, N-methylamide). A fragment cut from a longer protein should be capped, otherwise you create charges that do not exist in the real molecule.

A protein chain has two ends. The N-terminus ends in an amino group and the C-terminus in a carboxyl group. In water at neutral pH the amino group carries an extra proton and a charge of $+1$, and the carboxyl group has lost its proton and has a charge of $-1$. That is the right model for the true ends of a complete protein. When you simulate only a fragment, say residues 50 to 120 of a larger protein, its ends are artificial: in the real molecule the chain continues there with an uncharged peptide bond.

A **cap** is a small neutral group that imitates the continuing chain. The acetyl group (CH$_3$-CO-) goes on the N-terminal side and the N-methylamide group (-NH-CH$_3$) on the C-terminal side.

**Disulfide bonds.** Make sure they are declared in the topology.

A disulfide bond is a covalent bond between the sulfur atoms of two cysteine residues, which can be far apart in the sequence. The structure file shows the two sulfur atoms close together, about 0.2 nm apart, but the simulation knows only the bonds that are listed in the topology. In a classical force field that list is fixed when the system is built and never changes during the run ([Module 5](05-force-field-form.html)). A disulfide that is not declared is therefore two separate cysteines for the whole simulation, and nothing holds them together. After step 2, check that the bond is in the topology.

**Protonation states.** The force field needs one fixed protonation state per residue.

Several amino-acid side chains can bind or release a proton, the nucleus of a hydrogen atom, written H$^+$. The **protonation state** of a residue says whether the proton is on or off, and so whether the side chain is charged. In reality protons hop on and off all the time. In a classical force field they cannot, because bonds are never made or broken during a run. So you choose one state for each residue before the run, and the residue keeps it.

<div class="box physics" markdown="1">
**Physics you need here: pH, pK$_a$ and the fraction protonated.** The pH measures how many free protons the solution contains: the lower the pH, the more protons, and the more acidic the solution. Each group that can bind a proton has a pK$_a$, the pH at which it carries the proton exactly half of the time. Below its pK$_a$ a group is mostly protonated, above it mostly deprotonated. The fraction of the time it carries the proton is

$$
f_{prot} = \frac{1}{1 + 10^{\,\mathrm{pH} - \mathrm{p}K_a}} .
$$

Here $f_{prot}$ is the fraction protonated, a number between 0 and 1. The exponent is the difference between the pH of the solution and the pK$_a$ of the group. Each unit of that difference changes the ratio of the two forms by a factor of 10.

Three examples at pH 7, with round pK$_a$ values chosen for illustration:

- A carboxylic acid such as the Asp side chain, with a pK$_a$ of 4: $f_{prot} = 1/(1+10^{3}) = 0.001$. It is deprotonated and carries a charge of $-1$.
- An amine such as the Lys side chain, with a pK$_a$ of 10.5: $f_{prot} = 1/(1+10^{-3.5}) = 0.9997$. It is protonated and carries a charge of $+1$.
- A histidine with a pK$_a$ of 6.5: $f_{prot} = 1/(1+10^{0.5}) = 0.24$. With a pK$_a$ of 6 the result is $1/(1+10^{1}) = 0.09$. Neither form can be neglected, which is why histidine needs a decision.

How an equilibrium of this kind is related to a free energy is explained in the [primer](physics.html#equilibrium).
</div>

At pH 7, Asp and Glu are deprotonated, Lys and Arg protonated. These four are several units away from their pK$_a$ at pH 7, so the choice is safe unless the surroundings shift the pK$_a$ strongly. Asp and Glu then carry a charge of $-1$ each, and Lys and Arg a charge of $+1$ each.

**Histidine** (pK$_a$ near 6 to 6.5) is the difficult one: it can be neutral with the proton on N$\delta$ (HID) or N$\varepsilon$ (HIE), or doubly protonated and positive (HIP). The histidine side chain ends in a five-membered ring with two nitrogen atoms, called N$\delta$ and N$\varepsilon$ after their positions along the side chain. Either nitrogen can carry a hydrogen, or both can. That gives three states: two neutral ones that differ only in which nitrogen has the hydrogen, and a positive one with both.

HID, HIE and HIP are the residue names used for the three states in AMBER-family force fields. With a pK$_a$ so close to 7, the charged form is present a sizeable part of the time: 24 % or 9 % in the two examples of the box. The surroundings in the protein can push the balance either way.

Choose by inspecting hydrogen-bond partners or with a pK$_a$ predictor (PROPKA, H++). A hydrogen bond needs a donor, an N-H or O-H group, and an acceptor, an N or O atom that does not carry that hydrogen. Look at what sits next to each ring nitrogen in the structure. A nitrogen that faces an acceptor, such as a backbone C=O group, should carry the hydrogen. A nitrogen that faces a donor should not.

A pK$_a$ predictor is a program that estimates the pK$_a$ of every such group from the structure around it, so that you can apply the formula of the box residue by residue.

Buried Asp, Glu, Lys and Cys can also have shifted pK$_a$ values. A charge is stabilised by water, whose molecules turn their dipoles towards it ([primer](physics.html#electrostatics)). In the dry interior of a protein that stabilisation is missing, so a buried group tends to prefer its neutral form: the pK$_a$ of a buried acid goes up and that of a buried base goes down. A nearby charge of the opposite sign does the reverse and stabilises the charged form (Check yourself 4 is an example).

If the science depends on pH, plan simulations in each relevant protonation state. A standard simulation has no pH setting. The pH enters only through the protonation states chosen at this step. So "the same protein at pH 5 and at pH 7" means two systems that differ in their protonation states, each built and simulated separately.

**Ligands, cofactors, ions, structural waters.** Keep those that matter and get parameters for anything non-standard from a compatible general force field (Module 6). Metal sites need special care.

A structure file often contains more than the protein. A *ligand* is a small molecule bound to it, such as a drug or a substrate. A *cofactor* is a non-protein group that the protein needs for its function, such as a haem group. *Structural waters* are water molecules seen at fixed positions in the crystal, often buried in the protein and hydrogen-bonded to it. Crystals also contain molecules that are present only because they were in the crystallisation solution, and those are removed.

A protein force field has templates for the standard amino acids and none for a drug molecule. The parameters of such a molecule come from a *general force field*, built to be combined with one particular protein force field ([Module 6](06-force-field-parameters.html)). Metal ions are difficult for another reason: a metal ion bound in a protein polarises its neighbours and partly shares electrons with them, and a model of fixed point charges describes that poorly ([Module 5](05-force-field-form.html) lists what fixed charges leave out).

## Steps 2 to 4: topology, box, water, ions

<div data-videos="8oGZn1NdvbY Kbq6Gf9m2T8 GRH81ABCq54 nKYrzrwaRmc zCTGd5xYwoQ"></div>

*What is done.* Four operations, each by one tool. The force field is applied to the structure, which gives the topology (step 2). A periodic box is defined around the molecule and filled with water (step 3). Some of the water molecules are replaced by ions (step 4).

*If it is skipped.* Without a topology there are no forces at all. Without water the protein is in a vacuum, where nothing weakens the attraction between its charged groups, and the structure distorts. Without ions, a charged solute leaves a net charge in the box, and the Ewald method of [Module 7](07-boundaries-electrostatics.html) then adds an artificial background charge that distorts the results.

*How to tell that it worked.* Each tool ends without an error and the final system has zero net charge. The numbers of water molecules and ions agree with your own estimate (the formulas are below). A viewer shows the solute in the middle of a box of water, with ions scattered through it.

Three words first.

- **Topology.** The structure file says where the atoms are. The topology says what they are: the type, the charge and the mass of each atom, and the lists of bonds, angles and torsions between them. The tool that writes it matches every residue of your structure to a template of the force field ([Module 6](06-force-field-parameters.html)). It adds the hydrogens at the same time, because the template says how many each atom has.
- **To solvate** is to surround the solute with solvent. Here every water molecule is present as three atoms ("explicit" water).
- **To neutralise** is to add ions until the charges of all atoms in the box add up to zero.

With GROMACS (a force field that ships with every version is used here; current ones such as ff14SB, ff19SB and CHARMM36m are available as ports):

```bash
# topology: applies the force field, adds hydrogens
gmx pdb2gmx -f protein.pdb -o processed.gro -p topol.top -ff amber99sb-ildn -water tip3p -ignh

# rhombic dodecahedron with at least 1.2 nm between the solute and the box faces
gmx editconf -f processed.gro -o boxed.gro -c -d 1.2 -bt dodecahedron

# fill with water (spc216.gro is a generic equilibrated 3-site water box)
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top

# replace water molecules by ions: neutralise, then add 150 mM NaCl
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15
```

A force field "ships with" the program when its parameter files are installed together with it. A "port" is a conversion of the parameter files of a force field into the file format of another program, here GROMACS.

### The five commands, option by option

| Command or option | What it does | Module |
|---|---|---|
| `gmx pdb2gmx` | Step 2. Applies the force field to the structure and adds the hydrogens. | [6](06-force-field-parameters.html) |
| `-f protein.pdb` | The cleaned structure of step 1. | |
| `-o processed.gro` | The structure that is written, now with all its hydrogens. | |
| `-p topol.top` | The topology that is written. The later commands that take `-p topol.top` read this file or update it. | [6](06-force-field-parameters.html) |
| `-ff amber99sb-ildn` | The force field. | [5](05-force-field-form.html), [6](06-force-field-parameters.html) |
| `-water tip3p` | The water model: TIP3P, a model with three sites, one on each atom. | [6](06-force-field-parameters.html) |
| `-ignh` | Ignore the hydrogens that are already in the input file. Every hydrogen is then one that the tool places itself. | |
| `gmx editconf` | Step 3, first half. Defines the box. | [7](07-boundaries-electrostatics.html) |
| `-f processed.gro`, `-o boxed.gro` | The structure that is read, and the same structure written with a box around it. | |
| `-c` | Put the solute in the centre of the box. | |
| `-d 1.2` | The padding: at least 1.2 nm between the solute and the faces of the box. | [7](07-boundaries-electrostatics.html) |
| `-bt dodecahedron` | The box type, a rhombic dodecahedron. Of the three box shapes of Module 7 it needs the least volume: 29 % less than a cube for the same distance between copies. | [7](07-boundaries-electrostatics.html) |
| `gmx solvate` | Step 3, second half. Fills the box with water. | |
| `-cp boxed.gro` | The solute in its box. | |
| `-cs spc216.gro` | The water to fill it with. | [6](06-force-field-parameters.html) |
| `-o solvated.gro`, `-p topol.top` | The solvated structure that is written, and the topology, which is updated with the water that was added. | |
| `gmx grompp` | Packs parameters (`-f`), structure (`-c`) and topology (`-p`) into a run input file (`-o`). It is here only because the next tool takes a `.tpr` file as its input. No simulation is run from `ions.tpr`. | |
| `gmx genion` | Step 4. Replaces water molecules by ions. | [7](07-boundaries-electrostatics.html) |
| `-s ions.tpr` | The system to which the ions are added. | |
| `-o ions.gro`, `-p topol.top` | The structure with ions that is written, and the topology, updated again. | |
| `-pname NA`, `-nname CL` | The names of the positive and the negative ion: sodium and chloride. | |
| `-neutral` | Add the ions needed to bring the net charge of the box to zero. | [7](07-boundaries-electrostatics.html) |
| `-conc 0.15` | Add salt up to a concentration of 0.15 mol/L. | this section |

The file `ions.mdp` has one job: to let `gmx grompp` build the `.tpr` file that `gmx genion` needs. No run is made from it. It is the minimisation file `em.mdp` of Step 5 with one change, `coulombtype = Cut-off`:

```
; ions.mdp : only used to build ions.tpr for gmx genion, never run
integrator    = steep
emtol         = 1000.0
emstep        = 0.01
nsteps        = 50000
cutoff-scheme = Verlet
coulombtype   = Cut-off     ; plain cutoff: the box still has a net charge at this point
rcoulomb      = 1.0
rvdw          = 1.0
```

The reason for the change: with `coulombtype = PME` and a solute that still has a net charge, `gmx grompp` gives a warning about the net charge, and a warning stops it from writing the output. In the test described further down, on a protein with a net charge of $+8\,e$, `em.mdp` at this step gave "You are using Ewald electrostatics in a system with net charge" and then "Too many warnings (1)", and no `.tpr` file was written. Neutralising the box is what the next command is for, so at this one step a plain cutoff is used. The other lines are explained with `em.mdp` in Step 5.

With `ions.mdp`, `gmx grompp` prints two notes and carries on: one says that the system has a non-zero total charge, the other that a plain Coulomb cutoff might produce artefacts. Both are expected here. A note is information, and only a warning or an error stops the program.

When `gmx genion` runs, it prints the list of groups, asks "Select a group" and waits. Choose the group of the water molecules, which GROMACS calls `SOL`. Afterwards the last lines of `topol.top` list the ions that were added. In the test they were 26 `NA` and 34 `CL`: eight more chloride ions than sodium ions, which cancels the charge of $+8\,e$.

(How these files were tested is stated in the box under "The equilibration input files".)

### How large is the box?

The box decides the cost of everything that follows, because most of the atoms in it are water ([Module 6](06-force-field-parameters.html) puts water at 80 to 90 % of the atoms). Two numbers fix its size: the largest dimension of the solute and the **padding**, the layer of solvent you leave between the solute and the box face.

The solute tumbles during the run, so its longest dimension can point in any direction. The box must leave the padding on both sides of that dimension:

$$
d_{image} = D + 2\,d_{pad}, \qquad V_{box} = f\,d_{image}^{3} .
$$

<div class="legend" markdown="1">
- $D$: the largest dimension of the solute, the longest distance between two of its atoms, in nm.
- $d_{pad}$: the padding, in nm. It is the value given to `-d`.
- $d_{image}$: the image distance, the distance from any point of the box to its nearest copy in a neighbouring box, in nm.
- $V_{box}$: the volume of the box, in nm$^3$.
- $f$: a number that depends on the shape of the box. It is 1 for a cube, 0.77 for a truncated octahedron and 0.71 for a rhombic dodecahedron (the table of [Module 7](07-boundaries-electrostatics.html)).
- The exponent 3: the image distance cubed.
</div>

Read it like this. The solute and its nearest copy are separated by at least $2\,d_{pad}$ of solvent. That gap must stay larger than the cutoff of the interactions (the distance, about 1 nm, beyond which the program no longer computes the interaction of two atoms pair by pair, [Module 7](07-boundaries-electrostatics.html)), or the solute feels its own copy, which is an artefact of the box and exists in no experiment. Module 7 gives the practical rule: 1.0 to 1.2 nm of solvent on each side. The volume grows with the *cube* of the image distance, so a little more padding costs a lot of water.

A worked number. Take a small protein with $D = 4$ nm (a round value for illustration) and $d_{pad} = 1.2$ nm. Then $d_{image} = 4 + 2\times1.2 = 6.4$ nm. A cubic box has $6.4^3 = 262$ nm$^3$, and a rhombic dodecahedron has $0.71\times262 = 186$ nm$^3$. Raising the padding to 1.4 nm gives $d_{image} = 6.8$ nm and a volume 20 % larger, because $(6.8/6.4)^3 = 1.20$.

The number of water molecules follows from the volume that is left for them. Liquid water has 33.4 molecules per nm$^3$ ([Module 1](01-what-is-md.html)):

$$
N_{water} \approx 33.4\ \text{nm}^{-3}\times\left(V_{box} - V_{solute}\right) .
$$

<div class="legend" markdown="1">
- $N_{water}$: the number of water molecules in the box. Each one is three atoms.
- 33.4 nm$^{-3}$: the number of molecules in one cubic nanometre of liquid water.
- $V_{box}$: the volume of the box, in nm$^3$.
- $V_{solute}$: the volume taken up by the solute itself, in nm$^3$.
- $\approx$: an estimate. The real count depends on how the water packs against the solute.
</div>

In the example, say the protein fills 30 nm$^3$. The dodecahedron then holds about $33.4\times(186-30) = 5{,}200$ water molecules, which is 15,600 atoms. The cube would hold $33.4\times(262-30) = 7{,}700$ molecules, or 23,100 atoms. The choice of box shape alone removes a third of the water.

### What solvating does

A solvation tool does not build liquid water molecule by molecule. It starts from a small box of water that was simulated beforehand until it had the structure of the liquid. That is what "equilibrated" means in the comment of the command block. Copies of this small box are stacked until they cover your box, and every water molecule that would overlap the solute or stick out of the box is left out.

"3-site" means that the water molecule has three interaction sites, one on each atom. "Generic" means that the stored positions are not tied to one particular three-site model. The parameters come from the water model you chose in step 2. The starting positions are close enough for any of them, and the equilibration of steps 6 and 7 corrects the rest.

The result is a box of water that has never seen this solute. Next to the protein there are small gaps, some molecules are a little too close to it, and none is oriented towards its charged and polar groups. Steps 5 to 7 exist to repair this.

### Counter-ions, salt and ionic strength

Step 4 adds ions for two separate reasons.

**To neutralise.** Add up the charges of all atoms of the solute and you get its net charge, a whole number such as $-6$ or $+3$ in units of the proton charge $e$. A periodic box with a net charge is a problem, because every one of its infinitely many copies carries the same charge. The Ewald method then silently spreads the opposite charge evenly over the whole box, and that artificial background distorts pressure and free energies (the warning box of [Module 7](07-boundaries-electrostatics.html)). A real solution is neutral, so the right repair is the physical one: add as many ions of the opposite sign as the solute has net charges. These are the **counter-ions**.

**To have salt.** A protein in a cell or in a buffer is surrounded by dissolved salt. The ions gather around charges of the opposite sign and weaken the electrostatic forces between charged groups at a distance. This is called screening ([primer](physics.html#electrostatics)). Without salt, charged groups attract and repel each other more strongly and over longer distances than they do in the experiment you want to compare with.

The quantity that measures how strongly a salt solution screens is the **ionic strength**:

$$
I = \tfrac12\sum_i c_i\,z_i^{2} .
$$

<div class="legend" markdown="1">
- $I$: the ionic strength, in mol/L.
- $\sum_i$: a sum over the kinds of ion in the solution. For table salt there are two kinds, Na$^+$ and Cl$^-$.
- $c_i$: the concentration of ion kind $i$, in mol/L.
- $z_i$: the charge number of that ion: $+1$ for Na$^+$, $-1$ for Cl$^-$, $+2$ for Ca$^{2+}$. It is squared, so the sign drops out and a doubly charged ion counts four times.
- $\tfrac12$: a convention. It makes $I$ equal to the salt concentration for a salt such as NaCl.
</div>

Read it like this. For 0.15 mol/L of NaCl there is 0.15 mol/L of Na$^+$ and 0.15 mol/L of Cl$^-$, so $I = \tfrac12(0.15\times1 + 0.15\times1) = 0.15$ mol/L. For a salt of two singly charged ions the ionic strength and the concentration are the same number, which is why this module uses the two words for the same thing. They differ for other salts: 0.10 mol/L of CaCl$_2$ has 0.10 mol/L of Ca$^{2+}$ and 0.20 mol/L of Cl$^-$, and $I = \tfrac12(0.10\times4 + 0.20\times1) = 0.30$ mol/L. "Physiological" in the workflow table means about 0.15 mol/L.

### From a concentration to a number of ions

A concentration says how many moles there are in a litre. A simulation needs a number of ions in a box measured in nm$^3$. The conversion takes two facts. One mole is $N_A = 6.022\times10^{23}$ particles, and one litre is a cube of 0.1 m, or $10^8$ nm, on each side, which makes $10^{24}$ nm$^3$. A concentration of 1 mol/L is therefore $6.022\times10^{23}/10^{24} = 0.6022$ particles per nm$^3$, and

$$
N_{s} = 0.6022\;c\;V .
$$

<div class="legend" markdown="1">
- $N_s$: the number of ion pairs of salt to add. One pair is one Na$^+$ and one Cl$^-$.
- $c$: the salt concentration you want, in mol/L.
- $V$: the volume of the box, in nm$^3$.
- 0.6022: Avogadro's number times the number of litres in one nm$^3$, that is, $6.022\times10^{23}\times10^{-24}$. Its unit is nm$^{-3}$ per mol/L.
</div>

The counter-ions come on top of the salt:

$$
N_{\text{Na}} = N_s + \max(0,\,-Q), \qquad N_{\text{Cl}} = N_s + \max(0,\,Q) .
$$

<div class="legend" markdown="1">
- $N_{\text{Na}}$, $N_{\text{Cl}}$: the numbers of sodium and chloride ions in the finished box.
- $Q$: the net charge of the solute in units of $e$, a whole number. It is negative for a solute with more negative than positive groups.
- $\max(0,x)$: the larger of 0 and $x$. It equals $x$ when $x$ is positive and 0 otherwise.
- $N_s$: the number of ion pairs of salt, from the formula above.
</div>

Read it like this. A solute with $Q = -6$ gets 6 extra Na$^+$ and no extra Cl$^-$. The total charge of the box is then $-6 + (N_s + 6) - N_s = 0$. A solute with $Q = +3$ gets 3 extra Cl$^-$.

A worked number, for the example box of 186 nm$^3$ at 0.15 mol/L: $N_s = 0.6022\times0.15\times186 = 16.8$, so 17 pairs. If that protein has $Q = -6$, the box gets 23 Na$^+$ and 17 Cl$^-$.

**How many ions?** A concentration of 0.15 mol/L is $0.15\times0.6022 = 0.0903$ ion pairs per nm$^3$. A box of 500 nm$^3$ needs 45 Na$^+$ and 45 Cl$^-$, plus counter-ions for the net charge of the solute. Equivalently, one ion pair per $55.5/0.15 = 370$ water molecules. In small boxes the number of ions is small, so the realised concentration is coarse-grained: one ion pair more or less in a 100 nm$^3$ box changes it by 17 mM.

Three remarks on this paragraph.

*The first route* is the formula above: $0.0903\times500 = 45.2$, rounded to 45 pairs.

*The second route* counts water molecules instead of volume. A litre of water weighs about 1,000 g and a mole of water weighs 18 g, so water is a 55.5 mol/L solution of itself. A salt concentration of 0.15 mol/L then means 0.15 ion pairs for every 55.5 water molecules, which is one pair per 370.

The two routes do not give quite the same number. For the 5,200 water molecules of the example box, the second gives $5{,}200/370 = 14$ pairs, and the first gave 17. The first counts the volume of the solute as if it were solution. That is the remark at the end of the answer to Check yourself 1.

So the word "equivalently" holds for the solution itself: 0.0903 pairs per nm$^3$ and one pair per 370 water molecules are the same statement, because $33.4/0.0903 = 370$. The two counts differ only when the first is multiplied by a volume that includes the solute. The option `-conc` of `gmx genion` follows the first route: its documentation says that the number of ions is computed from the volume of the box.

*Coarse-grained* means here that the concentration can only change in steps, because you cannot add half an ion. A box of 100 nm$^3$ needs $0.0903\times100 = 9.03$ pairs. With 9 pairs the concentration is 149 mM, with 10 pairs it is 166 mM, and nothing in between is possible.

Make these estimates before you build, and compare them with what the tools report. If the numbers are far apart, look for the reason before going on: a wrong box type, a wrong padding, or a net charge you did not expect.

The calculator below does the arithmetic for numbers that you choose. It uses the rules of this section: the box volume from the size of the solute and the padding, 33.4 water molecules per nm$^3$, and 0.0602 ion pairs per nm$^3$ for each 100 mM of salt. It applies the last rule to the volume of the water, $V_{box} - V_{solute}$, as the second route does. For the example of this section (a longest dimension of 4 nm, a padding of 1.2 nm, a protein of 25 kDa) it therefore shows 14 ion pairs, where the formula with the whole box volume gave 17.

<div class="widget" data-widget="syscalc"></div>

## Step 5: energy minimisation

<div data-videos="OCcxxddYrDg WvkSCxLqkxY AyFXfAhwVBQ Y_IAolv3ZZg"></div>

*What is done.* Every atom is moved a small distance, again and again, in the direction that lowers the potential energy, until no atom feels a large force. No velocities and no time are involved.

*If it is skipped.* The first MD step throws the overlapping atoms apart at enormous speed, and the run stops with an error within a few steps.

*How to tell that it worked.* The potential energy has fallen and levelled off, and the largest force on any atom is below the limit you set.

The freshly built system has overlapping atoms: water placed too close to the protein, hydrogens added in idealised positions. The Lennard-Jones repulsion there is enormous, and the first MD step would give those atoms huge velocities. Minimisation moves the system downhill to the nearest local minimum of $U$.

The three sentences of that paragraph are explained in turn.

### Why there are overlaps, and why they are fatal

The water came from a pre-built box and was not arranged around this protein. The hydrogens were placed with standard bond lengths and angles ("idealised positions"), without regard to what else is nearby. So here and there two atoms sit closer than two real atoms can.

Two atoms repel each other when their electron clouds overlap. The Lennard-Jones term of the force field describes this with an energy that grows as $1/r^{12}$ when the distance $r$ between the atoms shrinks ([Module 5](05-force-field-form.html)). A twelfth power is very steep. Bring two atoms to half their distance and this energy is multiplied by $2^{12} = 4096$. The force, which is the slope of the energy, grows faster still.

Now see what such a force does in one time step. An atom that starts at rest and feels a constant force $F$ moves, during a time $\Delta t$, a distance

$$
\Delta x \approx \tfrac12\,\frac{F}{m}\,\Delta t^{2} .
$$

<div class="legend" markdown="1">
- $\Delta x$: the distance the atom moves during one time step, in nm.
- $F$: the force on the atom, in kJ mol$^{-1}$ nm$^{-1}$.
- $m$: the mass of the atom, in atomic mass units (u). Hydrogen is about 1 u.
- $F/m$: the acceleration of the atom (Newton's second law, [Module 2](02-classical-mechanics.html)). It comes out in nm ps$^{-2}$ without any conversion factor, because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$.
- $\Delta t$: the time step, in ps. A step of 2 fs is 0.002 ps.
- $\tfrac12$ and the square: the rule for motion at constant acceleration. The velocity grows in proportion to the time, and the distance covered is the average velocity times the time.
- $\approx$: an estimate. It ignores the velocity the atom already has and the change of the force during the step.
</div>

Read it like this, for a hydrogen atom ($m = 1$ u) and a step of 2 fs. With a force of 1,000 kJ mol$^{-1}$ nm$^{-1}$ the atom moves $\tfrac12\times1000\times0.002^2 = 0.002$ nm. That is the same size as the 0.003 nm it moves in one step from its thermal velocity at 300 K, so the integrator can handle it.

With a force one hundred times larger, which a bad overlap can produce, the atom moves 0.2 nm in one step. That is twice the length of a bond to hydrogen. The atom lands on top of other atoms, the forces there are larger again, and the next step is worse. This runaway is what "explode" means.

### Downhill, and where it stops

The potential energy $U$ is a function of all the coordinates. Module 2 pictured it as a landscape of hills and valleys, with the force on the system pointing downhill. A **local minimum** is the bottom of one valley: every small move away from it raises the energy, and all forces are zero there. The **global minimum** is the bottom of the deepest valley of all.

A minimiser behaves like a ball that rolls downhill with so much friction that it stops in the first hollow it meets. It never climbs over a ridge, so where it stops depends on where it started. The energy of a protein in water has an enormous number of local minima, and the minimiser finds the one nearest to the structure you built. For removing clashes nothing more is needed.

<div class="box maths" markdown="1">
**Maths you need here: the gradient, and what "downhill" means with many atoms.** $U$ depends on the three coordinates of every atom. The **gradient** of $U$ is the list of its slopes with respect to each coordinate in turn, the others held fixed. As a vector it points in the direction in which $U$ rises fastest. The force is minus the gradient, so the force points in the direction in which $U$ falls fastest. Moving every atom a short distance along its own force therefore lowers $U$.

A small example with two coordinates: $U = x^2 + 4y^2$ at the point $(1, 1)$, where $U = 5$. The slopes are $2x = 2$ and $8y = 8$, so the force is $(-2, -8)$. Divide by the largest component, 8, and take a step of length 0.1: the point moves by $(-0.025, -0.1)$ to $(0.975, 0.9)$. There $U = 0.975^2 + 4\times0.9^2 = 4.19$, lower than before. More in the [toolbox](maths.html#gradient).
</div>

### The two families of minimiser

**Steepest descent.** Move every atom along its force: $\mathbf r\leftarrow\mathbf r + h\,\mathbf F/|\mathbf F|_{max}$, increasing the step $h$ after a successful step and decreasing it after a failed one. Robust far from a minimum, slow close to it. The right choice for removing clashes.

Written for one atom, the update is

$$
\mathbf r_i \leftarrow \mathbf r_i + h\,\frac{\mathbf F_i}{|\mathbf F|_{max}} .
$$

<div class="legend" markdown="1">
- $\mathbf r_i$: the position of atom $i$, a vector, in nm. The formula in the sentence above leaves out the label $i$ and means "for every atom".
- $\leftarrow$: replace what is on the left by what is on the right.
- $\mathbf F_i$: the force on atom $i$, a vector. It is minus the gradient of $U$ with respect to the position of that atom.
- $|\mathbf F|_{max}$: the size of the largest force on any atom at this moment. The bars mean "length of the vector".
- $h$: the step length, in nm. It is the distance moved by the atom with the largest force. Its first value is the setting `emstep`.
</div>

Read it like this. Dividing by the largest force turns the forces into relative sizes between 0 and 1. The atom with the largest force moves exactly a distance $h$. An atom that feels a tenth of that force moves $h/10$, and each atom moves in the direction of its own force. With `emstep = 0.01` the worst atom moves 0.01 nm in the first step, about a tenth of a bond length.

A step is *successful* when the potential energy comes out lower. The next step is then tried with a larger $h$. A step has *failed* when the energy went up: the atoms moved too far and climbed the opposite wall of the valley. The step is then discarded, and a shorter one is tried from the same place. Because of this test the method cannot run away, which is what "robust" means.

It is slow near a minimum because the bottom of a valley is usually long and narrow. The steepest direction then points across the valley, and the path zigzags from wall to wall and makes little progress along the floor.

**Conjugate gradient and L-BFGS.** Use information from previous steps to choose better directions. Faster near a minimum. Needed when you want a tightly converged minimum, for example before normal-mode analysis.

Both methods remember the forces of earlier steps. From the way the force changed between steps they estimate the curvature of the valley, and they aim along its floor. Normal-mode analysis ([Module 2](02-classical-mechanics.html)) describes the vibrations of a molecule by expanding $U$ to second order around a minimum, and that expansion assumes that the forces are zero to high accuracy. Starting an MD run needs no such accuracy.

### When to stop, and what minimisation is not

Convergence criterion: the maximum force on any atom below about 1,000 kJ mol$^{-1}$ nm$^{-1}$ is enough to start MD. Minimisation does not find the global minimum and does not "relax" the structure in any thermodynamic sense: it is a 0 K operation that only removes strain.

A *convergence criterion* is the rule that decides when the minimiser may stop. The estimate above shows why this value is enough: at 1,000 kJ mol$^{-1}$ nm$^{-1}$ the force moves even the lightest atom no further in one step than its thermal motion does.

"A 0 K operation" needs a word. Temperature measures the kinetic energy of the atoms ([Module 3](03-statistical-mechanics.html)). A minimiser has no velocities, so its result is a system without thermal motion, which is a system at absolute zero. *Strain* means the local distortions left by building: overlaps, stretched bonds, bent angles.

A real protein at 300 K is never at a minimum of $U$. It moves all the time between a huge number of minima. Which shapes it prefers is decided by the free energy, which also counts how many arrangements are available ([primer](physics.html#thermodynamics)). A minimised structure therefore says nothing about which conformation is stable.

### The input file, line by line

```
; em.mdp
integrator    = steep
emtol         = 1000.0      ; stop when the largest force is below this (kJ/mol/nm)
emstep        = 0.01        ; initial step (nm)
nsteps        = 50000
cutoff-scheme = Verlet
coulombtype   = PME
rcoulomb      = 1.0
rvdw          = 1.0
```

| Line | What it means | Module |
|---|---|---|
| `integrator = steep` | Do a steepest-descent minimisation. The setting is called `integrator` because the same line chooses the MD algorithm in the other input files. | this section |
| `emtol = 1000.0` | The convergence criterion: stop when the largest force on any atom is below 1,000 kJ mol$^{-1}$ nm$^{-1}$. | this section |
| `emstep = 0.01` | The first value of the step length $h$: 0.01 nm. | this section |
| `nsteps = 50000` | The largest number of steps allowed. The run ends earlier if `emtol` is reached. | this section |
| `cutoff-scheme = Verlet` | Keep a buffered list of neighbouring atoms, so that not every pair of atoms has to be tested at every step. | [7](07-boundaries-electrostatics.html) |
| `coulombtype = PME` | Compute the electrostatic forces with particle-mesh Ewald, which includes all periodic copies of the box. | [7](07-boundaries-electrostatics.html) |
| `rcoulomb = 1.0` | The cutoff of the short-range (real-space) part of the Ewald sum: 1.0 nm. | [7](07-boundaries-electrostatics.html) |
| `rvdw = 1.0` | The cutoff of the Lennard-Jones interaction: 1.0 nm. | [7](07-boundaries-electrostatics.html) |

The last four lines say how the forces are computed, and they have the same values as in the production file of step 8. The minimiser should go downhill on the same energy that the MD run will use.

Check two things afterwards. First, plot the potential energy against the step number (exercise 1): it should fall steeply and then level off. In a box that is mostly water the final value is a large negative number, because the attraction between the water molecules outweighs everything else.

Second, find out why the run stopped. If the largest force fell below `emtol`, the minimisation converged. If the run stopped for another reason, for example because it used up `nsteps`, the largest force may still be far above the limit. Then look at the atom that carries it, because that is where the structure has a problem.

## Steps 6 and 7: equilibration

<div data-videos="WU_8wdSSZC8 3T5-m-FNR8Y"></div>

*What is done.* Two short MD runs. The first gives the atoms velocities and brings the system to the target temperature in a box of fixed size. The second lets the size of the box change until the density is right. In both, springs hold the solute near its starting structure.

*If it is skipped.* A production run started straight from the minimised structure spends its first part far from equilibrium: cold, at the wrong density, with water that has not adapted to the solute. In the mild case the first part of your data is biased. In the bad case the barostat reacts to a meaningless pressure and deforms the box, or the unsettled solvent pushes the solute out of shape.

*How to tell that it worked.* The temperature and the density, plotted against time, have each reached a plateau and fluctuate around it.

The minimised system is at 0 K with a density that is slightly wrong and water that is not adapted to the solute. Equilibration brings it to the target temperature and pressure without damaging the structure you prepared.

That sentence names three defects.

- *At 0 K.* The minimised structure has positions and no velocities.
- *A density that is slightly wrong.* Water molecules were left out wherever they would have overlapped the solute, which leaves thin gaps. And the pre-built water was not prepared with your water model at your temperature. The box holds slightly too few molecules for its volume.
- *Water that is not adapted to the solute.* Near a protein, water molecules turn towards charged groups and form hydrogen bonds with polar ones. The pre-built water was arranged as in pure water.

A system is at **equilibrium** when the averages of its properties (temperature, density, energy) no longer change with time. The properties still fluctuate from instant to instant.

### Holding the solute in place

**Position restraints.** During equilibration the heavy atoms of the solute are tied to their starting positions with harmonic springs, $U_{restr} = \tfrac12k|\mathbf r-\mathbf r_{ref}|^2$ with $k$ = 1,000 kJ mol$^{-1}$ nm$^{-2}$ (fluctuations of about 0.05 nm). The solvent relaxes around the solute while the solute keeps its shape.

<div class="legend" markdown="1">
- $U_{restr}$: the restraint energy of one atom, in kJ/mol. It is added to the force-field energy $U$ for as long as the restraints are on.
- $\mathbf r$: the present position of the atom.
- $\mathbf r_{ref}$: its reference position, the point the spring pulls it towards. It is the position the atom has in the reference structure given to the run.
- $|\mathbf r-\mathbf r_{ref}|$: the distance between the two, in nm. The bars mean "length of the vector".
- $k$: the spring constant, the stiffness of the spring, in kJ mol$^{-1}$ nm$^{-2}$.
- $\tfrac12$ and the square: the energy of a harmonic spring, as in [Module 2](02-classical-mechanics.html). Twice the displacement costs four times the energy.
</div>

Read the formula like this, with $k = 1{,}000$ kJ mol$^{-1}$ nm$^{-2}$. An atom 0.05 nm from its reference position has a restraint energy of $\tfrac12\times1000\times0.05^2 = 1.25$ kJ/mol, half of the thermal energy $k_BT = 2.494$ kJ/mol at 300 K. At 0.1 nm the energy is 5 kJ/mol, twice $k_BT$. At 0.2 nm it is 20 kJ/mol, eight times $k_BT$. So an atom moves freely over a few hundredths of a nanometre and is held firmly beyond that.

The "fluctuations of about 0.05 nm" can be computed. For an atom held only by this spring, the typical displacement along one direction is

$$
\sqrt{\langle \Delta x^{2}\rangle} = \sqrt{\frac{k_BT}{k}} .
$$

<div class="legend" markdown="1">
- $\Delta x$: the displacement of the atom from its reference position along one direction ($x$, $y$ or $z$), in nm.
- $\langle\ \rangle$: an average over time.
- $\sqrt{\langle\Delta x^2\rangle}$: the root-mean-square displacement, the typical size of the fluctuation.
- $k_B$: the Boltzmann constant, 0.0083145 kJ mol$^{-1}$ K$^{-1}$.
- $T$: the temperature, in K. At 300 K, $k_BT = 2.494$ kJ/mol.
- $k$: the spring constant of the restraint.
</div>

The formula comes from equipartition ([Module 3](03-statistical-mechanics.html), and in words in the [primer](physics.html#temperature)). Every term of the energy that is a square, such as $\tfrac12k\,\Delta x^2$, holds on average $\tfrac12k_BT$. Setting $\tfrac12k\langle\Delta x^2\rangle = \tfrac12k_BT$ and dividing both sides by $\tfrac12k$ gives $\langle\Delta x^2\rangle = k_BT/k$. With $k = 1{,}000$ the result is $\sqrt{2.494/1000} = 0.050$ nm. A stiffer spring gives smaller fluctuations, and a higher temperature larger ones.

What the restraints are for: in the first picoseconds the water is far from equilibrium and pushes on the solute unevenly. The springs keep the solute in the shape you prepared while the water settles around it. They act on the *heavy atoms*, which are all atoms except hydrogen, and they are removed before production.

Do not confuse a restraint with a constraint ([Module 9](09-constraints.html)). A constraint fixes a bond length exactly and removes that motion from the system. A restraint is an extra energy term: the atom still moves, and the spring pulls it back.

### The two stages

**NVT stage (about 100 ps).** Velocities are drawn from the Maxwell-Boltzmann distribution, the thermostat takes the system to 300 K at fixed volume. Check: the temperature reaches the target and fluctuates about it.

The **Maxwell-Boltzmann distribution** says how fast atoms move at a given temperature ([Module 3](03-statistical-mechanics.html)). Each of the three velocity components of an atom is a random number from a bell-shaped (Gaussian) distribution centred on zero, with a width of $\sqrt{k_BT/m}$, where $m$ is the mass of the atom. At 300 K that width is about 1.6 nm/ps for hydrogen and 0.46 nm/ps for carbon. "Drawn" means that the program produces random numbers with this distribution and uses them as starting velocities. Different random numbers give a different, equally valid start (see Repeats in the planning section).

The thermostat still has work to do after that. The atoms start at the bottom of a valley of $U$. As soon as they move they climb its walls, and kinetic energy turns into potential energy. For a system of ideal springs exactly half is converted, so without a thermostat the temperature would fall towards 150 K. The thermostat supplies the difference over the first picoseconds.

How large should the fluctuations of the temperature be? Module 3 gives the standard deviation of the instantaneous temperature:

$$
\sigma_T = T\,\sqrt{\frac{2}{N_{df}}} .
$$

<div class="legend" markdown="1">
- $\sigma_T$: the standard deviation of the instantaneous temperature, in K. It is the typical distance of the temperature from its average at any moment.
- $T$: the target temperature, in K.
- $N_{df}$: the number of degrees of freedom, the number of independent ways the atoms can move. It is three per atom, minus one for each constraint, minus three ([Module 9](09-constraints.html)).
</div>

Read it like this. For a system with, say, $N_{df} = 60{,}000$ at 300 K, $\sigma_T = 300\times\sqrt{2/60000} = 1.7$ K. The plot should show a noisy line around 300 K that moves up and down by a kelvin or two. A larger system gives a quieter line. A perfectly flat line is a sign of a wrong thermostat setting, as Module 8 explains.

**NPT stage (100 ps to a few ns).** The barostat is switched on and the box volume adjusts. Check: the density rises to a plateau, close to 1,000 kg/m$^3$ for a dilute aqueous system (the exact value depends on the water model). For membranes, large complexes or anything built by hand, extend this stage and release the restraints gradually (for example 1,000, then 100, then 10 kJ mol$^{-1}$ nm$^{-2}$).

The density is the mass in the box divided by the volume of the box. The number of atoms is fixed, so the density can change only through the volume. The box starts a little too large for the water it holds, the barostat shrinks it, and the density rises until it stops at the value that the force field gives at 1 bar. A *dilute aqueous system* is one that is mostly water. In the units of MD, 1 u/nm$^3$ is 1.6605 kg/m$^3$, so pure water with 33.4 molecules of 18.015 u in each nm$^3$ has $33.4\times18.015\times1.6605 = 999$ kg/m$^3$.

The check uses the density and not the pressure for a reason given in Module 8. Water is nearly incompressible, so a tiny change of volume is a large change of pressure, and the instantaneous pressure of a small box swings by several hundred bar from step to step. The pressure is a noisy gauge. The density settles much faster.

Releasing the restraints gradually has a plain meaning in terms of the fluctuation formula above. With $k$ = 1,000, 100 and 10 kJ mol$^{-1}$ nm$^{-2}$ the typical displacement per direction is 0.05, 0.16 and 0.50 nm. Each stage lets the atoms move about three times further than the one before ($\sqrt{10} = 3.2$), so the solute is handed over to the force field in steps.

Why NVT first and NPT second is the subject of Check yourself 2. In short: the pressure is computed from the kinetic energy and from the *virial*, a sum over pairs of atoms of the force between them times their distance ([Module 8](08-thermostats-barostats.html)). Right after minimisation the first part is zero and the second reflects a strained, freshly built structure. A barostat that acts on such a pressure changes the box for the wrong reason.

### The four runs as commands

```bash
gmx grompp -f em.mdp  -c ions.gro -p topol.top -o em.tpr                     && gmx mdrun -deffnm em
gmx grompp -f nvt.mdp -c em.gro  -r em.gro  -p topol.top -o nvt.tpr          && gmx mdrun -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr && gmx mdrun -deffnm npt
gmx grompp -f md.mdp  -c npt.gro -t npt.cpt -p topol.top -o md.tpr           && gmx mdrun -deffnm md
```

The four lines are minimisation, NVT, NPT and production, and they have the same pattern: pack the input, then run it.

| Part | What it does |
|---|---|
| `gmx grompp ... -o nvt.tpr` | Pack the parameters (`-f`), the starting structure (`-c`) and the topology (`-p`) into the run input file `nvt.tpr`. |
| `gmx mdrun -deffnm nvt` | Run it. `mdrun` is the simulation engine. `-deffnm nvt` gives all its files the base name `nvt`: it reads `nvt.tpr` and writes, among others, the final structure `nvt.gro` and the checkpoint `nvt.cpt`. |
| `-c em.gro` | Start from the last structure of the stage before. Each line starts where the previous one ended. |
| `-r em.gro` | The reference positions $\mathbf r_{ref}$ of the position restraints. The option is present in the two equilibration lines and absent from the production line, where the solute is free. |
| `-t nvt.cpt` | Also read the checkpoint of the stage before, which holds the velocities. The NPT run and the production run continue the motion. They do not draw new velocities. |
| `&&` | Start the run only if `gmx grompp` reported no error. |

To look at what a run produced, use `gmx energy`. For example, `gmx energy -f nvt.edr -o temperature.xvg` reads the energy file of the NVT run (`nvt.edr`, written by `mdrun`), lists the quantities stored in it, asks which one you want (temperature, pressure, density, potential energy and others) and writes it as a table against time. These are the plots behind the checks of the two stages.

### The equilibration input files

The files `nvt.mdp` and `npt.mdp` differ from the production file of the next section in four ways. Both runs are short, and both have the position restraints on. The NVT file has no barostat and asks for new velocities. The NPT file has the barostat on and continues from the NVT checkpoint. Here they are in full. Every line that also occurs in `md.mdp` has the same value there and is explained in the next section, so only the lines that differ are explained here.

<div class="box key" markdown="1">
**How these files were tested.** The five parameter files of this module (`ions.mdp`, `em.mdp`, `nvt.mdp`, `npt.mdp`, `md.mdp`) were taken from this page as printed and passed through `gmx grompp` of GROMACS 2026.1, after the build commands of Steps 2 to 4, on hen egg-white lysozyme (PDB entry 1AKI, 129 residues, net charge $+8\,e$, crystal water removed). All five were accepted without a warning, and each produced its `.tpr` file.

The files were then run for real. The GROMACS notebook linked at the top of this module takes them from this page and runs every stage with `gmx mdrun` (GROMACS 2026.3 on a GPU): the minimisation, 100 ps at constant volume, 100 ps at constant pressure and a production run. Only one line was changed for that run: `nsteps` in `md.mdp`, from 100 ns to 1 ns. Every stage finished without a warning or an error. The minimisation converged in 773 steps, the temperature held at 300 K, and the density settled near 1,015 kg/m$^3$.

With `nvt.mdp` and `npt.mdp`, `gmx grompp` prints one note: removing the centre-of-mass motion while position restraints are on "might cause artifacts", which it calls usually negligible when a macromolecule is equilibrated. That note is expected. If you see a warning or an error with your own system, read it: it names the setting it objects to.
</div>

```
; nvt.mdp : equilibration at constant volume, 100 ps, solute restrained
define                  = -DPOSRES      ; switch on the position restraints of posre.itp

integrator              = md            ; leap-frog (Module 4)
dt                      = 0.002         ; 2 fs, needs constrained bonds to H
nsteps                  = 50000         ; 50,000 x 2 fs = 100 ps

nstxout-compressed      = 5000          ; write positions every 10 ps
nstenergy               = 500           ; write energies every 1 ps (for the temperature plot)
nstlog                  = 500

continuation            = no            ; first MD run: bring the bonds to H to their fixed lengths
constraint-algorithm    = lincs         ; Module 9
constraints             = h-bonds
lincs-iter              = 1
lincs-order             = 4

cutoff-scheme           = Verlet        ; buffered neighbour list (Module 7)
rvdw                    = 1.0           ; Lennard-Jones cutoff (nm)
vdw-modifier            = Potential-shift
DispCorr                = EnerPres      ; tail correction for energy and pressure

coulombtype             = PME           ; particle-mesh Ewald (Module 7)
rcoulomb                = 1.0
pme-order               = 4
fourierspacing          = 0.12

tcoupl                  = V-rescale     ; stochastic velocity rescaling (Module 8)
tc-grps                 = Protein Non-Protein
tau-t                   = 0.1  0.1      ; ps
ref-t                   = 300  300      ; K

pcoupl                  = no            ; no barostat: the box is fixed (NVT)

pbc                     = xyz
gen-vel                 = yes           ; draw velocities from the Maxwell-Boltzmann distribution
gen-temp                = 300           ; at this temperature (K)
gen-seed                = -1            ; seed of the random numbers; -1 = a new seed at every gmx grompp
```

| Line of `nvt.mdp` | What it means | In `md.mdp` |
|---|---|---|
| `define = -DPOSRES` | Switch on the position restraints: the topology then includes the file `posre.itp`. | absent |
| `nsteps = 50000` | 50,000 steps of 2 fs: 100 ps. | longer |
| `nstenergy = 500`, `nstlog = 500` | Write the energies every 1 ps, so that the temperature plot has 100 points. | every 10 ps |
| `continuation = no` | This is the first MD run. The minimisation was done without constraints, so the program first brings the bonds to hydrogen to their fixed lengths. | `yes` |
| `pcoupl = no` | No barostat: the box keeps its size. This one line stands in the place of the pressure lines of `md.mdp`. | `C-rescale` |
| `gen-vel = yes` | Draw new velocities. | `no` |
| `gen-temp = 300` | The temperature, in K, of the Maxwell-Boltzmann distribution from which they are drawn. | absent |
| `gen-seed = -1` | The seed of the random numbers. With $-1$ the program picks a new seed each time `gmx grompp` is run. A whole number of your choice makes the start reproducible. | absent |

```
; npt.mdp : equilibration at constant pressure, 100 ps, solute restrained
define                  = -DPOSRES      ; position restraints still on

integrator              = md            ; leap-frog (Module 4)
dt                      = 0.002         ; 2 fs, needs constrained bonds to H
nsteps                  = 50000         ; 50,000 x 2 fs = 100 ps

nstxout-compressed      = 5000          ; write positions every 10 ps
nstenergy               = 500           ; write energies every 1 ps (for the density plot)
nstlog                  = 500

continuation            = yes           ; continue from the NVT equilibration
constraint-algorithm    = lincs         ; Module 9
constraints             = h-bonds
lincs-iter              = 1
lincs-order             = 4

cutoff-scheme           = Verlet        ; buffered neighbour list (Module 7)
rvdw                    = 1.0           ; Lennard-Jones cutoff (nm)
vdw-modifier            = Potential-shift
DispCorr                = EnerPres      ; tail correction for energy and pressure

coulombtype             = PME           ; particle-mesh Ewald (Module 7)
rcoulomb                = 1.0
pme-order               = 4
fourierspacing          = 0.12

tcoupl                  = V-rescale     ; stochastic velocity rescaling (Module 8)
tc-grps                 = Protein Non-Protein
tau-t                   = 0.1  0.1      ; ps
ref-t                   = 300  300      ; K

pcoupl                  = C-rescale     ; stochastic cell rescaling (Module 8)
pcoupltype              = isotropic
tau-p                   = 2.0           ; ps
ref-p                   = 1.0           ; bar
compressibility         = 4.5e-5        ; of water, bar^-1
refcoord-scaling        = all           ; the reference positions of the restraints follow the box

pbc                     = xyz
gen-vel                 = no            ; velocities come from the NVT checkpoint
```

| Line of `npt.mdp` | What it means | Compared with `nvt.mdp` |
|---|---|---|
| `continuation = yes` | The run continues the NVT run. The bonds to hydrogen already have their fixed lengths. | was `no` |
| `pcoupl = C-rescale` and the four lines after it | The barostat is on, with the same settings as in `md.mdp`. | was `pcoupl = no` |
| `refcoord-scaling = all` | When the barostat rescales the box, the reference positions of the restraints are rescaled with it. With the default, `no`, the reference positions stay where they were while the box changes around them, and the documentation warns that the pressure may then be ill defined. In the test, `gmx grompp` refused the file with `no`: "You are using pressure coupling with absolute position restraints, this will give artifacts. Use the refcoord_scaling option." | new |
| `gen-vel = no` | Do not draw velocities again. They are read from `nvt.cpt`, which is given with `-t`. | was `yes` |

**Where the restraints come from.** In GROMACS the restraints are prepared at step 2. Besides the topology, `gmx pdb2gmx` writes a file `posre.itp` with the list of restrained atoms and the spring constant, 1,000 kJ mol$^{-1}$ nm$^{-2}$ unless you ask for another value. The topology includes that file only when the name `POSRES` is defined, so the restraints are off unless the parameter file contains the line `define = -DPOSRES`. That line is in `nvt.mdp` and `npt.mdp` and absent from `md.mdp`. The reference positions are the coordinates of the file given to `gmx grompp` with `-r`.

**Where the velocities and the seed are set.** The velocities are drawn once, by `gmx grompp`, when it builds `nvt.tpr`. Three lines of `nvt.mdp` control this: `gen-vel`, `gen-temp` and `gen-seed`. The NPT and production files have `gen-vel = no` and take their velocities from the checkpoint given with `-t`. So a repeat with new velocities (Exercise 2) starts at the NVT stage: give `gen-seed` a different whole number for each repeat, and run NVT, NPT and production once for each. In OpenMM the same is done with a second argument of `setVelocitiesToTemperature`, a random seed: `sim.context.setVelocitiesToTemperature(300 * unit.kelvin, 1)`, then with `2`, then with `3`, gives three reproducible repeats.

**Continuing a run that was interrupted.** The command is `gmx mdrun -deffnm md -cpi md.cpt`. The option `-cpi` continues from the state stored in the checkpoint. If no checkpoint file is found, the program starts from the first step, so the same command can be used for the first job and for every later one.

## Step 8: production, an annotated input file

<div data-videos="P9pyJmbK3tM xS4r2bLATvo IArpsQsZ95U sSVME8caRCM"></div>

*What is done.* The same kind of run as the NPT equilibration, without restraints and much longer. From here on the data are kept. The run must be done under exactly the conditions you will report, because every setting below is part of the model.

*How to tell that it worked.* The run reaches its last step, or stops at the time limit of the job and continues from its checkpoint. Temperature and density stay on the plateaus reached during equilibration. The molecule looks intact when you watch the trajectory. Whether the *results* can be trusted is a different question, the one of [Module 11](11-analysis-statistics.html).

Every line below refers to a module of this course. Settings are for an AMBER-family force field; a CHARMM force field needs `rvdw = 1.2`, `rvdw-switch = 1.0`, `vdw-modifier = Force-switch`, `rcoulomb = 1.2` and, following the GROMACS recommendation for CHARMM36, `DispCorr = no`.

The second sentence is a reminder that the cutoff settings belong to the force field. The parameters of a force field were fitted with one particular treatment of the Lennard-Jones interaction near the cutoff, and they are only valid with that treatment. Module 7 gives the example: CHARMM force fields were parameterised with a force switch from 1.0 to 1.2 nm.

```
; md.mdp : production, NPT, 100 ns
integrator              = md            ; leap-frog (Module 4)
dt                      = 0.002         ; 2 fs, needs constrained bonds to H
nsteps                  = 50000000      ; 50,000,000 x 2 fs = 100 ns

nstxout-compressed      = 5000          ; write positions every 10 ps
nstenergy               = 5000          ; write energies every 10 ps
nstlog                  = 5000

continuation            = yes           ; continue from the NPT equilibration
constraint-algorithm    = lincs         ; Module 9
constraints             = h-bonds
lincs-iter              = 1
lincs-order             = 4

cutoff-scheme           = Verlet        ; buffered neighbour list (Module 7)
rvdw                    = 1.0           ; Lennard-Jones cutoff (nm)
vdw-modifier            = Potential-shift
DispCorr                = EnerPres      ; tail correction for energy and pressure

coulombtype             = PME           ; particle-mesh Ewald (Module 7)
rcoulomb                = 1.0
pme-order               = 4
fourierspacing          = 0.12

tcoupl                  = V-rescale     ; stochastic velocity rescaling (Module 8)
tc-grps                 = Protein Non-Protein
tau-t                   = 0.1  0.1      ; ps
ref-t                   = 300  300      ; K

pcoupl                  = C-rescale     ; stochastic cell rescaling (Module 8)
pcoupltype              = isotropic
tau-p                   = 2.0           ; ps
ref-p                   = 1.0           ; bar
compressibility         = 4.5e-5        ; of water, bar^-1

pbc                     = xyz
gen-vel                 = no            ; velocities come from the checkpoint
```

The file has eight groups of lines, separated by empty lines. They are taken one at a time below.

### How long the run is

The first group fixes the length of the run. The simulated time is the number of steps times the length of one step:

$$
t_{sim} = n_{steps}\times\Delta t .
$$

<div class="legend" markdown="1">
- $t_{sim}$: the simulated time, the stretch of time in the life of the molecule that the run covers.
- $n_{steps}$: the number of integration steps, the setting `nsteps`.
- $\Delta t$: the time step, the setting `dt`, in ps.
</div>

Read it like this. $50{,}000{,}000\times2$ fs $= 100{,}000{,}000$ fs, which is 100 ns. Turned around, the number of steps for a wanted length is $n_{steps} = t_{sim}/\Delta t$: an equilibration stage of 100 ps at 2 fs per step is 50,000 steps. The same product gives every output interval of the file: 5,000 steps of 2 fs are 10,000 fs, or 10 ps.

| Line | What it means | Module |
|---|---|---|
| `integrator = md` | Run molecular dynamics with the leap-frog algorithm. At every step it computes the forces, uses them to update the velocities, and uses the new velocities to update the positions. | [4](04-integrators.html) |
| `dt = 0.002` | The time step: 0.002 ps, or 2 fs. A step should be 10 to 20 times shorter than the period of the fastest motion in the system. With the bonds to hydrogen held rigid (the `constraints` line below) that period is about 20 fs, which allows 2 fs. | [4](04-integrators.html), [9](09-constraints.html) |
| `nsteps = 50000000` | The number of steps. | this section |

### What is written to disk

A **trajectory** is the record of the run: the positions of the atoms, saved at regular intervals. Each saved set of positions is called a **frame**. The run computes 50 million sets of positions and keeps one in every 5,000, so the trajectory has $50{,}000{,}000/5{,}000 = 10{,}000$ frames.

| Line | What it means | Module |
|---|---|---|
| `nstxout-compressed = 5000` | Every 5,000 steps (10 ps), write the positions of the atoms to the trajectory file. "Compressed" means that they are stored with reduced precision, which saves disk space. | this section |
| `nstenergy = 5000` | Every 10 ps, write the energies and the related quantities (temperature, pressure, density) to the energy file. The plots of exercise 1 are made from them. | [8](08-thermostats-barostats.html) |
| `nstlog = 5000` | Every 10 ps, write the energies to the log file, a text file that records the progress of the run. | this section |

**Trajectory formats** differ in three ways: what they store for each frame (positions only, or velocities and forces as well), how precisely they store it, and which programs can read them. The two that appear in this module both store positions: the compressed GROMACS trajectory written by `nstxout-compressed`, and the DCD file written by the OpenMM script below. Positions at reduced precision are all that structural analysis needs. They are not enough to continue a run. That is the job of the checkpoint, which holds the complete state at full precision.

### Continuation and constraints

| Line | What it means | Module |
|---|---|---|
| `continuation = yes` | This run continues an earlier one. The starting structure comes with velocities and already has its constrained bonds at the right lengths, so the program must not adjust it before the first step. | this section |
| `constraint-algorithm = lincs` | The algorithm that keeps the constrained bonds at their fixed lengths: LINCS. | [9](09-constraints.html) |
| `constraints = h-bonds` | Which bonds are held at fixed length: every bond that involves a hydrogen atom. These bonds have the fastest vibrations in the system, with a period near 10 fs. Removing them is what allows the 2 fs step. | [9](09-constraints.html) |
| `lincs-iter = 1` | The number of final correction steps in LINCS. | [9](09-constraints.html) |
| `lincs-order = 4` | The order of the series that LINCS uses in place of a matrix inversion: the highest power of the coupling matrix that is kept. | [9](09-constraints.html) |

### Lennard-Jones interactions

| Line | What it means | Module |
|---|---|---|
| `cutoff-scheme = Verlet` | Keep a buffered list of neighbouring atoms, so that not every pair has to be tested at every step. | [7](07-boundaries-electrostatics.html) |
| `rvdw = 1.0` | Compute the Lennard-Jones interaction only for pairs of atoms closer than 1.0 nm. | [7](07-boundaries-electrostatics.html) |
| `vdw-modifier = Potential-shift` | Shift the Lennard-Jones energy by a constant so that it is exactly zero at the cutoff. The energy then has no jump when a pair crosses the cutoff. | [7](07-boundaries-electrostatics.html) |
| `DispCorr = EnerPres` | Add the average effect of the attraction that was cut off beyond 1.0 nm to the energy and to the pressure. Without this correction the density comes out too low. | [7](07-boundaries-electrostatics.html) |

### Electrostatics

| Line | What it means | Module |
|---|---|---|
| `coulombtype = PME` | Particle-mesh Ewald. The Coulomb interaction with all periodic copies is split into a short-range part, computed pair by pair, and a smooth long-range part, computed on a grid. | [7](07-boundaries-electrostatics.html) |
| `rcoulomb = 1.0` | The cutoff of the short-range part, in nm. Nothing is thrown away beyond it: the rest of the interaction is in the grid part. | [7](07-boundaries-electrostatics.html) |
| `pme-order = 4` | The order of the interpolation that spreads each charge over the grid points near it. | [7](07-boundaries-electrostatics.html) |
| `fourierspacing = 0.12` | The largest spacing allowed between grid points, in nm. A finer grid is more accurate and slower. | [7](07-boundaries-electrostatics.html) |

### Temperature

| Line | What it means | Module |
|---|---|---|
| `tcoupl = V-rescale` | The thermostat: stochastic velocity rescaling. It gives the kinetic energy the correct distribution and disturbs the motion very little. | [8](08-thermostats-barostats.html) |
| `tc-grps = Protein Non-Protein` | Two groups of atoms, each with its own thermostat: the protein, and everything else (water and ions). Neither group can then stay warmer or colder than the target while the average looks right. Module 8 adds the condition that each group must be large. | [8](08-thermostats-barostats.html) |
| `tau-t = 0.1  0.1` | The coupling time of each group, in ps: how quickly a deviation of the temperature is removed. One value for each group. | [8](08-thermostats-barostats.html) |
| `ref-t = 300  300` | The target temperature of each group, in K. | [8](08-thermostats-barostats.html) |

A **coupling time** $\tau$ has a concrete meaning for a thermostat or barostat of this kind. A deviation of the average from its target decays as $e^{-t/\tau}$, where $t$ is the time that has passed and $e = 2.718$ is the base of the exponential function ([toolbox](maths.html#exp-log)). After one coupling time about 37 % of it is left ($e^{-1} = 0.37$). A short coupling time corrects fast and interferes more with the natural motion.

### Pressure

| Line | What it means | Module |
|---|---|---|
| `pcoupl = C-rescale` | The barostat: stochastic cell rescaling. | [8](08-thermostats-barostats.html) |
| `pcoupltype = isotropic` | One scale factor for all three directions of the box. The box changes its size and keeps its shape, which is right for a protein in water. | [8](08-thermostats-barostats.html) |
| `tau-p = 2.0` | The coupling time of the barostat, in ps. | [8](08-thermostats-barostats.html) |
| `ref-p = 1.0` | The target pressure, in bar. | [8](08-thermostats-barostats.html) |
| `compressibility = 4.5e-5` | The compressibility of water, in bar$^{-1}$: the relative change of volume per bar of pressure. The barostat uses it to turn a difference in pressure into a change of the box volume. | [8](08-thermostats-barostats.html) |

### Box and velocities

| Line | What it means | Module |
|---|---|---|
| `pbc = xyz` | Periodic boundary conditions in all three directions. | [7](07-boundaries-electrostatics.html) |
| `gen-vel = no` | Do not draw new velocities. They are read from the checkpoint of the NPT stage, so the motion continues without a break. | this section |

### The same workflow in OpenMM

<div data-videos="hbQ_dfgWPc8 AlWsbbdUNC0 yLnjbjtRgdg 71snkHHku1c"></div>

To run this for real, open the [OpenMM notebook](https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb) named at the top of this module. It runs the script below on lysozyme, one step at a time, with the restrained equilibration of steps 6 and 7 added and an analysis of the result.

OpenMM runs the same steps from one Python script. There are no intermediate files: the structure, the topology and the settings are Python objects in memory. Read the script in four parts: build the system (steps 1 to 4), choose the physics (what the `.mdp` file did), minimise and equilibrate (steps 5 to 7), and produce (step 8).

```python
import openmm as mm
from openmm import app, unit

pdb = app.PDBFile("protein.pdb")
ff = app.ForceField("amber14-all.xml", "amber14/tip3pfb.xml")

model = app.Modeller(pdb.topology, pdb.positions)
model.addHydrogens(ff, pH=7.0)
# In OpenMM, padding is the guaranteed distance between the solute and its nearest
# periodic copy, so 2.4 nm here builds the same box as "gmx editconf -d 1.2".
model.addSolvent(ff, padding=2.4 * unit.nanometer,
                 ionicStrength=0.15 * unit.molar, boxShape="dodecahedron")

system = ff.createSystem(model.topology,
                         nonbondedMethod=app.PME,
                         nonbondedCutoff=1.0 * unit.nanometer,
                         constraints=app.HBonds,          # Module 9
                         hydrogenMass=4 * unit.amu)       # HMR, allows 4 fs
system.addForce(mm.MonteCarloBarostat(1 * unit.bar, 300 * unit.kelvin))

integrator = mm.LangevinMiddleIntegrator(300 * unit.kelvin,     # Module 8
                                         1 / unit.picosecond,   # friction
                                         0.004 * unit.picoseconds)
sim = app.Simulation(model.topology, system, integrator)
sim.context.setPositions(model.positions)

sim.minimizeEnergy()
sim.context.setVelocitiesToTemperature(300 * unit.kelvin)
sim.step(125_000)                                        # 500 ps equilibration

sim.reporters.append(app.DCDReporter("traj.dcd", 2500))  # every 10 ps
sim.reporters.append(app.StateDataReporter("log.csv", 2500, step=True,
                     potentialEnergy=True, temperature=True, density=True, speed=True))
sim.reporters.append(app.CheckpointReporter("state.chk", 250_000))
sim.step(25_000_000)                                     # 100 ns
```

**Part 1: build the system.**

| Line | What it does | In the GROMACS version | Module |
|---|---|---|---|
| `import ...` | Load the library. `mm` is the engine, `app` holds the tools that read files and build systems, `unit` holds the units. | | |
| `app.PDBFile("protein.pdb")` | Read the cleaned structure file of step 1. | `-f protein.pdb` | |
| `app.ForceField(...)` | Load the force field. The first file holds the parameters of the solute, the second those of the water model and of the ions. | `-ff`, `-water` | [5](05-force-field-form.html), [6](06-force-field-parameters.html) |
| `app.Modeller(...)` | Make a model that can be edited: its topology (which atoms and bonds) and its positions. | | |
| `model.addHydrogens(ff, pH=7.0)` | Add the hydrogens. The pH decides the protonation state that each residue gets. This is the protonation decision of step 1, made by the program for the pH you give. The cases that needed thought in step 1 still need your check. | `gmx pdb2gmx` | this module |
| `model.addSolvent(...)` | Steps 3 and 4 in one call: build a rhombic dodecahedron, fill it with water, add the counter-ions that neutralise the solute, and add salt for an ionic strength of 0.15 mol/L. | `gmx editconf`, `gmx solvate`, `gmx genion` | [7](07-boundaries-electrostatics.html) |

The comment in the script about the padding compares two ways of measuring the same box. In the notation of the box-size formula, the GROMACS option `-d` is the distance from the solute to the box face, $d_{pad}$. The OpenMM argument `padding` is the distance from the solute to its nearest copy, $2\,d_{pad}$. So `padding=2.4` nm and `-d 1.2` describe the same box, with one difference of detail: for the size of the solute GROMACS takes the largest distance between two of its atoms, and OpenMM takes the diameter of a sphere that encloses it, which can be a little larger.

**Part 2: choose the physics.**

| Line | What it does | In the GROMACS version | Module |
|---|---|---|---|
| `ff.createSystem(...)` | Apply the force field to the model. The result, `system`, is the topology in OpenMM's form: every atom with its parameters, and every force that acts. | `gmx pdb2gmx`, and the `.mdp` lines below | [6](06-force-field-parameters.html) |
| `nonbondedMethod=app.PME` | Electrostatics with particle-mesh Ewald. | `coulombtype = PME` | [7](07-boundaries-electrostatics.html) |
| `nonbondedCutoff=1.0 * unit.nanometer` | The cutoff of the direct, pair-by-pair interactions: 1.0 nm. | `rcoulomb`, `rvdw` | [7](07-boundaries-electrostatics.html) |
| `constraints=app.HBonds` | Hold every bond to a hydrogen at fixed length. | `constraints = h-bonds` | [9](09-constraints.html) |
| `hydrogenMass=4 * unit.amu` | Hydrogen mass repartitioning (HMR). Each hydrogen bonded to a heavy atom gets a mass of 4 u, and the extra mass is taken from that atom. The hydrogens of rigid water molecules keep their mass. The fastest remaining motions become slower, which allows a step of 4 fs. | not used | [9](09-constraints.html) |
| `mm.MonteCarloBarostat(1 * unit.bar, 300 * unit.kelvin)` | The barostat. Every few steps it proposes a random change of the volume and accepts or rejects it. The first number is the target pressure. The temperature is needed for the acceptance rule. | `pcoupl`, `ref-p` | [8](08-thermostats-barostats.html) |
| `mm.LangevinMiddleIntegrator(...)` | Integrator and thermostat in one. Langevin dynamics adds a friction force and a random force to every atom. The three numbers are the target temperature (300 K), the friction coefficient (1 ps$^{-1}$) and the time step (0.004 ps, or 4 fs). | `integrator`, `tcoupl`, `ref-t`, `dt` | [4](04-integrators.html), [8](08-thermostats-barostats.html) |
| `app.Simulation(...)` | Tie topology, system and integrator together into one object that can run. | `gmx grompp` | |
| `sim.context.setPositions(model.positions)` | Give the starting coordinates. | `-c` | |

**Part 3: minimise and equilibrate.**

| Line | What it does | In the GROMACS version | Module |
|---|---|---|---|
| `sim.minimizeEnergy()` | Step 5, energy minimisation. | the `em` line | this module |
| `sim.context.setVelocitiesToTemperature(300 * unit.kelvin)` | Draw velocities from the Maxwell-Boltzmann distribution at 300 K. | the NVT stage | [3](03-statistical-mechanics.html) |
| `sim.step(125_000)` | Run 125,000 steps. At 4 fs per step that is 500,000 fs, or 500 ps. Nothing is written yet, because no reporter has been attached. | the `nvt` and `npt` lines | |

**Part 4: produce.** A *reporter* is an object that writes something to a file at regular intervals.

| Line | What it does | In the GROMACS version | Module |
|---|---|---|---|
| `app.DCDReporter("traj.dcd", 2500)` | From now on, write the positions to a trajectory file every 2,500 steps. At 4 fs per step that is 10 ps. | `nstxout-compressed` | this module |
| `app.StateDataReporter("log.csv", 2500, ...)` | Every 10 ps, add a line to a table with the quantities that are switched on: the step number, the potential energy, the temperature, the density and the speed of the run. | `nstenergy`, `nstlog` | [8](08-thermostats-barostats.html) |
| `app.CheckpointReporter("state.chk", 250_000)` | Every 250,000 steps, which is 1 ns, save a checkpoint from which the run can be continued. | the `.cpt` file | this module |
| `sim.step(25_000_000)` | Run 25,000,000 steps. At 4 fs per step that is 100 ns, with $25{,}000{,}000/2{,}500 = 10{,}000$ frames. | `nsteps` | |

The two versions do the same workflow with different, equally defensible choices (the protocol table of [Module 8](08-thermostats-barostats.html) lists both). The OpenMM script uses a 4 fs step with heavier hydrogens where the GROMACS file uses 2 fs. It uses a Langevin thermostat and a Monte Carlo barostat where the GROMACS file uses velocity rescaling and cell rescaling. Its equilibration is one stage of 500 ps with the barostat on from the start. The two versions also load different force-field and water-model files (compare `-ff amber99sb-ildn -water tip3p` with the two file names in the script), so they do not simulate exactly the same model.

Read the script as a second, shorter example of the workflow, and not as a line-by-line translation of the GROMACS files. A run made with one is not a repeat of a run made with the other.

This short script skips the restrained equilibration stages. For real work add position restraints with a `CustomExternalForce` for the first stage and remove them before production.

A `CustomExternalForce` is OpenMM's way to add an energy term that depends on the position of each atom separately, through a formula that you write. The restraint energy of the equilibration section, a spring between each heavy atom and its reference position, is such a term. In a periodic box the OpenMM documentation advises writing the formula with its function `periodicdistance`, because the position that the formula receives can be that of any periodic copy of the atom.

## Planning: length, repeats, output, cost

<div data-videos="EsKsPEdYksE F-SsbOw2YrM"></div>

A production run costs days of computer time. Before you start one, decide four things: how long to run, how many times, what to write to disk, and how to split the run into jobs. A test run of five minutes answers the practical ones.

**How long?** Long enough to see the slowest process relevant to your question many times, which you often do not know in advance. Start by listing the time scales (Module 1) and deciding what you can and cannot claim.

A simulation reports only on events that happen during it, and to say how often something happens you must see it many times. One opening of a loop in 100 ns shows that the loop can open. It does not tell you how often it does. If the process you care about is slower than your run, the run describes the fluctuations around the starting structure and nothing more, and that is then the only claim you can make.

**Repeats.** Three to five independent runs from different initial velocities are worth more than one run of the same total length: they give an honest error bar (Module 11). To find out whether the result depends on the starting structure, start some of the runs from different conformations.

A **repeat**, also called a **replica**, is another simulation of the same system that differs only in its starting velocities. A computer has no true randomness. Its "random" numbers are a fixed sequence computed from a starting number, the **seed** ([toolbox](maths.html#random-numbers)). The same seed gives the same velocities, and a different seed gives a different and equally valid set. Because the motion of many atoms is chaotic ([Module 2](02-classical-mechanics.html)), two runs that differ only in their velocities are on different paths within picoseconds.

One run gives one answer and no measure of how much that answer owes to chance. Several runs give several answers, and their spread is the error bar. For $n$ independent runs,

$$
\mathrm{SE} = \frac{s}{\sqrt{n}} .
$$

<div class="legend" markdown="1">
- $\mathrm{SE}$: the standard error of the mean, the uncertainty of the average over the runs.
- $s$: the standard deviation of the $n$ results, a measure of how much the runs differ from each other. It is computed with $n-1$ in the denominator ([toolbox](maths.html#averages)), which is what gives 0.04 nm in the example below.
- $n$: the number of independent runs.
</div>

Read it like this. Say three runs give an average radius of gyration (a measure of the overall size of the molecule, [Module 11](11-analysis-statistics.html)) of 1.52, 1.48 and 1.56 nm (invented numbers). The mean is 1.52 nm, the standard deviation is 0.04 nm, and the standard error is $0.04/\sqrt3 = 0.023$ nm, so you report $1.52\pm0.02$ nm. With one run you would have had one of the three numbers and no idea of the 0.04. More in the [toolbox](maths.html#averages) and in [Module 11](11-analysis-statistics.html).

Repeats from one structure share that structure. If the molecule has a second shape that it reaches only once in a microsecond, five short repeats will most likely all miss it, and their small spread will look reassuring. That is the reason for the last sentence of the item: start some runs from different conformations.

**Output frequency.** Saving every 10 to 100 ps is enough for most structural analysis. Saving more often than the correlation time of your observable only fills disks. If you do not need the water, save only the solute (`compressed-x-grps` in GROMACS).

The *correlation time* of a quantity is the time over which it keeps a memory of its value ([Module 11](11-analysis-statistics.html)). Two frames closer together than that carry nearly the same information. The number of frames and the disk space follow from

$$
N_{frames} = \frac{t_{sim}}{t_{out}}, \qquad \text{size} \approx N_{frames}\times N_{atoms}\times 12\ \text{bytes} .
$$

<div class="legend" markdown="1">
- $N_{frames}$: the number of frames in the trajectory.
- $t_{sim}$: the simulated time.
- $t_{out}$: the time between two saved frames, in the same unit as $t_{sim}$.
- $N_{atoms}$: the number of atoms that are saved in each frame.
- 12 bytes: three coordinates of 4 bytes each, the size of one atom in an uncompressed frame. Compressed formats need less.
- size: the disk space taken by the trajectory, in bytes ($10^9$ bytes are 1 GB).
- $\approx$: an estimate. Each frame also holds a few more numbers, such as the time and the box.
</div>

Read it like this. A run of 100 ns saved every 10 ps has $100{,}000/10 = 10{,}000$ frames. With 50,000 atoms (a round number) that is $10{,}000\times50{,}000\times12 = 6\times10^9$ bytes, or 6 GB. Halving the interval doubles the size. Saving only a solute of 5,000 atoms takes 0.6 GB: most of the atoms are water, which is why leaving the water out saves so much.

**Benchmark first.** Run 5 minutes and read the performance in ns/day from the log before submitting a long job. Size the job's time limit from the measured speed.

The speed of a run is given in **ns/day**: nanoseconds of simulated time per day of real time. It depends on the number of atoms, on the hardware and on the settings, and it cannot be guessed. The real time that a run needs is

$$
t_{wall} = \frac{t_{sim}}{S} .
$$

<div class="legend" markdown="1">
- $t_{wall}$: the real time the run takes, in days. It is called wall-clock time, the time that passes on the clock on the wall.
- $t_{sim}$: the simulated time, in ns.
- $S$: the speed, in ns/day.
</div>

Read it like this. Say the test gives 80 ns/day (an invented value). A run of 100 ns then takes $100/80 = 1.25$ days, or 30 hours. On a cluster that allows 24 hours per job, one job delivers 80 ns, so the run needs two jobs. The five-minute test itself covers $80\times5/1440 = 0.28$ ns (a day has 1,440 minutes), which is about 139,000 steps of 2 fs and enough for a steady reading.

**Checkpoints.** Long runs must be restartable: `gmx mdrun -cpi` continues exactly from the last checkpoint, and OpenMM's checkpoint reporter does the same. Chain short jobs if the cluster favours them.

Jobs end before the run is finished for ordinary reasons: the time limit is reached, or a machine fails. A **checkpoint** holds everything needed to go on as if nothing had happened: positions, velocities, the box, and the internal variables of the thermostat and the barostat, all at full precision. A trajectory frame cannot do this, because it holds positions only, at reduced precision. `-cpi` is the option of `gmx mdrun` that tells it to continue from a checkpoint. To *chain* jobs is to submit several short jobs one after the other, each continuing from the checkpoint that the one before left.

In OpenMM the reporter only writes the file. To continue, a new script builds the same `Simulation` object and loads the checkpoint with `sim.loadCheckpoint("state.chk")` before it calls `sim.step`. The OpenMM documentation sets two limits. The continued run is meant to be identical to an uninterrupted one, but this is not guaranteed. And a checkpoint can be read only on the same hardware and with the same OpenMM version that wrote it.

## What goes wrong

Most failed runs fail in one of a few ways, and the error message names the symptom, not the cause. Some words of the table need a definition first.

- A **LINCS warning** is printed when a constrained bond has rotated by more than 30° in one step ([Module 9](09-constraints.html)). Bonds do not turn that fast in a healthy run.
- "Particle moved more than the cutoff" says that an atom travelled an impossibly long way in a single step.
- **NaN** stands for "not a number". It is what a computer returns for a calculation that has no answer, such as zero divided by zero. Once one coordinate is NaN, every energy is. These first three symptoms are the same event seen at different moments: the explosion described in step 5.
- A **vacuum bubble** is a region of the box without water. Under a barostat the box shrinks quickly to close it.
- **RMSD** is the root-mean-square deviation: a typical distance between the atoms now and the same atoms in a reference structure (the square root of the average of the squared distances), after the two structures have been laid on top of each other ([Module 11](11-analysis-statistics.html)). An RMSD that "levels off" has stopped growing.

| Symptom | Likely cause | Fix |
|---|---|---|
| Crash in the first steps, "LINCS warning", "particle moved more than the cutoff", NaN energies | Clashes left after minimisation, missing atoms, wrong topology, time step too large for the system state | Inspect the named atoms; minimise further; start with a smaller time step and restraints |
| "System has non-zero total charge" | Ions not added or miscounted | Neutralise with `genion -neutral` |
| Protein appears torn apart in the viewer | Molecules wrapped across the periodic box, a display artefact | `gmx trjconv -pbc mol -center` or the equivalent in MDAnalysis |
| Density far from 1,000 kg/m$^3$, box collapsing or exploding | Barostat too aggressive on an unequilibrated system, vacuum bubbles | Longer NVT, gentler barostat (stochastic cell rescaling), check solvation |
| Protein interacts with its own image | Box too small for the conformations sampled | Larger box; monitor with `gmx mindist -pi` |
| Ligand or ion flies away immediately | Wrong protonation or charges, missing restraints during equilibration | Recheck parameters and protonation |
| Structure drifts steadily, RMSD never levels off | Could be real (wrong starting model), a force-field problem, or wrong protonation | Compare repeats and force fields; check against experiment |

### Periodic images in the output

The third row puzzles almost everyone once. The simulation box is surrounded by copies of itself, and an atom that leaves through one face comes back in through the opposite face ([Module 7](07-boundaries-electrostatics.html)). A program can store each atom at its position inside the one central box. A protein that has drifted across a face is then written with some of its atoms at one side of the box and the rest at the other side. A viewer that draws the bonds shows long lines across the box, or a protein in two pieces.

Nothing is wrong with the simulation. With periodic boundaries each atom interacts with the nearest copy of every other atom, so for the forces the molecule was whole all the time. The repair is made on the trajectory file after the run.

The command in the table rewrites the trajectory molecule by molecule. The option `-pbc mol` puts the centre of mass of every molecule inside the box, so that a molecule is moved as a whole, and `-center` puts the group you choose, here the protein, in the middle of the box. Written out with its files the command is, for example, `gmx trjconv -s md.tpr -f md.xtc -o md_centred.xtc -pbc mol -center`: `-pbc mol` requires the run input file (`-s`). If a molecule still appears broken, the documentation offers `-pbc whole`, which only makes broken molecules whole.

The fifth row is the opposite case, a real problem that looks harmless. If the box is too small, the solute comes within the cutoff of its own copy and feels it. The command in that row reports the shortest distance between the solute and its periodic images during the run. That distance must stay larger than the cutoff ([Module 7](07-boundaries-electrostatics.html)).

### How to use the table

Work backwards through the workflow. A crash in production usually comes from the equilibration, and a crash in equilibration usually from the building. Look at the structure in a viewer before you change a setting: a clash, a missing atom or a hole in the water is often visible at once. And do not make the warning go away by loosening the setting that printed it. Module 9 makes the point for LINCS: the algorithm is reporting the problem and is rarely its cause.

## What to report

A reader must be able to repeat your simulation. State: source and preparation of the structure, protonation states and how they were chosen; force field, water model and ion parameters with versions; box shape and size, number of atoms, salt concentration; minimisation and equilibration protocol; integrator and time step, constraints, mass repartitioning; cutoffs, long-range electrostatics and dispersion treatment; thermostat and barostat with coupling constants; length and number of repeats, what was discarded as equilibration; software and version; where the input files and trajectories can be obtained.

The list follows the workflow: step 1, then steps 2 to 4, then steps 5 to 7, then the production input file line by line, then the planning. If you kept your input files, writing it is short work. Some of its words:

- *Ion parameters* are the force-field parameters of the ions, which are specific to the water model ([Module 6](06-force-field-parameters.html)).
- *Mass repartitioning* is the hydrogen mass repartitioning of [Module 9](09-constraints.html).
- The *dispersion treatment* is what is done about the Lennard-Jones attraction beyond the cutoff, the `DispCorr` line.
- *Coupling constants* are the coupling times `tau-t` and `tau-p`.
- *Discarded as equilibration* refers to the first part of the production run, which you leave out of the analysis if the quantity you measure was still drifting there ([Module 11](11-analysis-statistics.html)).

All of this is needed because the settings are part of the model. Two simulations of the same protein with different water models, cutoffs or thermostats are two different models. A reader who cannot tell which one you ran cannot compare your result with anything.

## Check yourself

<details markdown="1"><summary>1. Your solvated box is 7 × 7 × 7 nm and the protein has a net charge of −6. How many Na⁺ and Cl⁻ for 150 mM?</summary>
Volume 343 nm$^3$ gives $343\times0.0903 = 31$ ion pairs. Add 6 extra Na$^+$ to neutralise: 37 Na$^+$ and 31 Cl$^-$. (Strictly, the volume available to the solvent is slightly smaller than the box.)

In the symbols of this module: $N_s = 0.6022\,c\,V$ with $c = 0.15$ mol/L and $V = 343$ nm$^3$, then $N_{\text{Na}} = N_s + 6$ and $N_{\text{Cl}} = N_s$ because the net charge is $Q = -6$.
</details>

<details markdown="1"><summary>2. Why equilibrate at constant volume before switching on the barostat?</summary>
Right after minimisation the kinetic energy is zero and the virial is unrepresentative, so the instantaneous pressure is far from equilibrium. A barostat acting on that would rescale the box violently. Bringing the system to temperature first makes the pressure meaningful.

(The virial is the part of the pressure that comes from the forces: a sum over pairs of atoms of the force between them times their distance. "Unrepresentative" means that it reflects the strained, freshly built structure and says little about the liquid at 300 K.)
</details>

<details markdown="1"><summary>3. What does the energy minimiser not do?</summary>
It does not cross barriers, does not find the global minimum, does not include entropy or temperature, and does not validate the structure. It only moves the system to the nearest local minimum.
</details>

<details markdown="1"><summary>4. A histidine sits next to an aspartate in your binding interface. Which protonation state would you consider?</summary>
The doubly protonated, positively charged form (HIP) is stabilised by the nearby negative charge, which raises the histidine pK$_a$. Run a pK$_a$ prediction, and if the result is near the experimental pH, simulate both states.

(A higher pK$_a$ means that the group holds its proton up to a higher pH. With the formula of step 1, a histidine whose pK$_a$ is raised from 6.5 to 7.5 is protonated 76 % of the time at pH 7 instead of 24 %.)
</details>

<details markdown="1"><summary>5. You want a run of 250 ns with a time step of 4 fs and one frame every 20 ps. Which numbers do you set, and how many frames do you get?</summary>
Use $n_{steps} = t_{sim}/\Delta t$ with both times in ps. The run needs $250{,}000/0.004 = 62{,}500{,}000$ steps. One frame every 20 ps is one frame every $20/0.004 = 5{,}000$ steps. The trajectory has $250{,}000/20 = 12{,}500$ frames. A step of 4 fs needs hydrogen mass repartitioning as well as constrained bonds to hydrogen (Module 9).
</details>

<details markdown="1"><summary>6. In the viewer, half of your protein is at the left edge of the box and the other half at the right edge. Has the simulation failed?</summary>
No. The box is periodic, and the atoms were stored at their positions inside one box. The protein has drifted across a face, so the file shows it in two parts. For the forces it was whole all the time, because each atom interacts with the nearest copy of its neighbours. Rewrite the trajectory so that molecules are in one piece before you analyse it or look at it.
</details>

<details markdown="1"><summary>7. Why can a run be continued exactly from a checkpoint and not from the last frame of the trajectory?</summary>
A frame holds positions only, at reduced precision. To continue the same motion the program also needs the velocities and the internal variables of the thermostat and the barostat, at full precision. The checkpoint holds all of these. Starting from a frame with newly drawn velocities is possible and gives a valid simulation. It is then a new start.
</details>

## Exercises

1. Do the complete workflow for a small protein of your choice (lysozyme, PDB 1AKI, is the classic tutorial case). Plot potential energy during minimisation, temperature during NVT, and density during NPT.
2. Repeat the production run three times with different random seeds for the initial velocities. Overlay the backbone RMSD traces.
3. Run a 100 ps NVE simulation from your equilibrated system (thermostat and barostat off) and measure the energy drift. Repeat with a 4 fs time step without mass repartitioning and describe what happens.
4. Write the methods paragraph for your simulation following the list above, in fewer than 200 words.

## Read

{{READ}}

## Key papers

{{PAPERS}}
