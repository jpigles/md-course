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

## Watch first

{{WATCH}}

## The workflow at a glance

<div data-videos="EFtbEkuJ9tk ZKNUR5Uz2r0 HPk5SiEqFIM _CYsaBhAEeA"></div>

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

## Step 1: the starting structure

<div data-videos="YQ8eRyScuyk RvvSvC8YyVo"></div>

A simulation can only be as good as its starting model. Go through this list every time.

- **Source.** A crystal or cryo-EM structure, an NMR model, or a prediction (AlphaFold and similar). For a predicted complex, the interface may be wrong in ways that MD will not repair on accessible time scales.
- **Missing atoms and residues.** Crystal structures lack hydrogens and often lack flexible loops and side chains. Build missing side chains (PDBFixer, MODELLER, Swiss-PdbViewer, CHARMM-GUI). For a missing loop either model it or cap the chain ends, and say which.
- **Alternate conformations.** Keep one (usually the A conformer).
- **Termini.** Decide between charged termini (NH$_3^+$, COO$^-$) and neutral caps (acetyl, N-methylamide). A fragment cut from a longer protein should be capped, otherwise you create charges that do not exist in the real molecule.
- **Disulfide bonds.** Make sure they are declared in the topology.
- **Protonation states.** The force field needs one fixed protonation state per residue. At pH 7, Asp and Glu are deprotonated, Lys and Arg protonated. **Histidine** (pK$_a$ near 6 to 6.5) is the difficult one: it can be neutral with the proton on N$\delta$ (HID) or N$\varepsilon$ (HIE), or doubly protonated and positive (HIP). Choose by inspecting hydrogen-bond partners or with a pK$_a$ predictor (PROPKA, H++). Buried Asp, Glu, Lys and Cys can also have shifted pK$_a$ values. If the science depends on pH, plan simulations in each relevant protonation state.
- **Ligands, cofactors, ions, structural waters.** Keep those that matter and get parameters for anything non-standard from a compatible general force field (Module 6). Metal sites need special care.

## Steps 2 to 4: topology, box, water, ions

<div data-videos="8oGZn1NdvbY Kbq6Gf9m2T8 GRH81ABCq54 nKYrzrwaRmc zCTGd5xYwoQ"></div>

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

**How many ions?** A concentration of 0.15 mol/L is $0.15\times0.6022 = 0.0903$ ion pairs per nm$^3$. A box of 500 nm$^3$ needs 45 Na$^+$ and 45 Cl$^-$, plus counter-ions for the net charge of the solute. Equivalently, one ion pair per $55.5/0.15 = 370$ water molecules. In small boxes the number of ions is small, so the realised concentration is coarse-grained: one ion pair more or less in a 100 nm$^3$ box changes it by 17 mM.

<div class="widget" data-widget="syscalc"></div>

## Step 5: energy minimisation

<div data-videos="OCcxxddYrDg WvkSCxLqkxY AyFXfAhwVBQ Y_IAolv3ZZg"></div>

The freshly built system has overlapping atoms: water placed too close to the protein, hydrogens added in idealised positions. The Lennard-Jones repulsion there is enormous, and the first MD step would give those atoms huge velocities. Minimisation moves the system downhill to the nearest local minimum of $U$.

- **Steepest descent.** Move every atom along its force: $\mathbf r\leftarrow\mathbf r + h\,\mathbf F/|\mathbf F|_{max}$, increasing the step $h$ after a successful step and decreasing it after a failed one. Robust far from a minimum, slow close to it. The right choice for removing clashes.
- **Conjugate gradient and L-BFGS.** Use information from previous steps to choose better directions. Faster near a minimum. Needed when you want a tightly converged minimum, for example before normal-mode analysis.

Convergence criterion: the maximum force on any atom below about 1,000 kJ mol$^{-1}$ nm$^{-1}$ is enough to start MD. Minimisation does not find the global minimum and does not "relax" the structure in any thermodynamic sense: it is a 0 K operation that only removes strain.

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

## Steps 6 and 7: equilibration

<div data-videos="WU_8wdSSZC8 3T5-m-FNR8Y"></div>

The minimised system is at 0 K with a density that is slightly wrong and water that is not adapted to the solute. Equilibration brings it to the target temperature and pressure without damaging the structure you prepared.

**Position restraints.** During equilibration the heavy atoms of the solute are tied to their starting positions with harmonic springs, $U_{restr} = \tfrac12k|\mathbf r-\mathbf r_{ref}|^2$ with $k$ = 1,000 kJ mol$^{-1}$ nm$^{-2}$ (fluctuations of about 0.05 nm). The solvent relaxes around the solute while the solute keeps its shape.

**NVT stage (about 100 ps).** Velocities are drawn from the Maxwell-Boltzmann distribution, the thermostat takes the system to 300 K at fixed volume. Check: the temperature reaches the target and fluctuates about it.

**NPT stage (100 ps to a few ns).** The barostat is switched on and the box volume adjusts. Check: the density rises to a plateau, close to 1,000 kg/m$^3$ for a dilute aqueous system (the exact value depends on the water model). For membranes, large complexes or anything built by hand, extend this stage and release the restraints gradually (for example 1,000, then 100, then 10 kJ mol$^{-1}$ nm$^{-2}$).

```bash
gmx grompp -f em.mdp  -c ions.gro -p topol.top -o em.tpr                     && gmx mdrun -deffnm em
gmx grompp -f nvt.mdp -c em.gro  -r em.gro  -p topol.top -o nvt.tpr          && gmx mdrun -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr && gmx mdrun -deffnm npt
gmx grompp -f md.mdp  -c npt.gro -t npt.cpt -p topol.top -o md.tpr           && gmx mdrun -deffnm md
```

## Step 8: production, an annotated input file

<div data-videos="P9pyJmbK3tM xS4r2bLATvo IArpsQsZ95U sSVME8caRCM"></div>

Every line below refers to a module of this course. Settings are for an AMBER-family force field; a CHARMM force field needs `rvdw = 1.2`, `rvdw-switch = 1.0`, `vdw-modifier = Force-switch`, `rcoulomb = 1.2` and, following the GROMACS recommendation for CHARMM36, `DispCorr = no`.

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

### The same workflow in OpenMM

<div data-videos="hbQ_dfgWPc8 AlWsbbdUNC0 yLnjbjtRgdg 71snkHHku1c"></div>

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

This short script skips the restrained equilibration stages. For real work add position restraints with a `CustomExternalForce` for the first stage and remove them before production.

## Planning: length, repeats, output, cost

<div data-videos="EsKsPEdYksE F-SsbOw2YrM"></div>

- **How long?** Long enough to see the slowest process relevant to your question many times, which you often do not know in advance. Start by listing the time scales (Module 1) and deciding what you can and cannot claim.
- **Repeats.** Three to five independent runs from different initial velocities are worth more than one run of the same total length: they give an honest error bar (Module 11). To find out whether the result depends on the starting structure, start some of the runs from different conformations.
- **Output frequency.** Saving every 10 to 100 ps is enough for most structural analysis. Saving more often than the correlation time of your observable only fills disks. If you do not need the water, save only the solute (`compressed-x-grps` in GROMACS).
- **Benchmark first.** Run 5 minutes and read the performance in ns/day from the log before submitting a long job. Size the job's time limit from the measured speed.
- **Checkpoints.** Long runs must be restartable: `gmx mdrun -cpi` continues exactly from the last checkpoint, and OpenMM's checkpoint reporter does the same. Chain short jobs if the cluster favours them.

## What goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Crash in the first steps, "LINCS warning", "particle moved more than the cutoff", NaN energies | Clashes left after minimisation, missing atoms, wrong topology, time step too large for the system state | Inspect the named atoms; minimise further; start with a smaller time step and restraints |
| "System has non-zero total charge" | Ions not added or miscounted | Neutralise with `genion -neutral` |
| Protein appears torn apart in the viewer | Molecules wrapped across the periodic box, a display artefact | `gmx trjconv -pbc mol -center` or the equivalent in MDAnalysis |
| Density far from 1,000 kg/m$^3$, box collapsing or exploding | Barostat too aggressive on an unequilibrated system, vacuum bubbles | Longer NVT, gentler barostat (stochastic cell rescaling), check solvation |
| Protein interacts with its own image | Box too small for the conformations sampled | Larger box; monitor with `gmx mindist -pi` |
| Ligand or ion flies away immediately | Wrong protonation or charges, missing restraints during equilibration | Recheck parameters and protonation |
| Structure drifts steadily, RMSD never levels off | Could be real (wrong starting model), a force-field problem, or wrong protonation | Compare repeats and force fields; check against experiment |

## What to report

A reader must be able to repeat your simulation. State: source and preparation of the structure, protonation states and how they were chosen; force field, water model and ion parameters with versions; box shape and size, number of atoms, salt concentration; minimisation and equilibration protocol; integrator and time step, constraints, mass repartitioning; cutoffs, long-range electrostatics and dispersion treatment; thermostat and barostat with coupling constants; length and number of repeats, what was discarded as equilibration; software and version; where the input files and trajectories can be obtained.

## Check yourself

<details markdown="1"><summary>1. Your solvated box is 7 × 7 × 7 nm and the protein has a net charge of −6. How many Na⁺ and Cl⁻ for 150 mM?</summary>
Volume 343 nm$^3$ gives $343\times0.0903 = 31$ ion pairs. Add 6 extra Na$^+$ to neutralise: 37 Na$^+$ and 31 Cl$^-$. (Strictly, the volume available to the solvent is slightly smaller than the box.)
</details>

<details markdown="1"><summary>2. Why equilibrate at constant volume before switching on the barostat?</summary>
Right after minimisation the kinetic energy is zero and the virial is unrepresentative, so the instantaneous pressure is far from equilibrium. A barostat acting on that would rescale the box violently. Bringing the system to temperature first makes the pressure meaningful.
</details>

<details markdown="1"><summary>3. What does the energy minimiser not do?</summary>
It does not cross barriers, does not find the global minimum, does not include entropy or temperature, and does not validate the structure. It only moves the system to the nearest local minimum.
</details>

<details markdown="1"><summary>4. A histidine sits next to an aspartate in your binding interface. Which protonation state would you consider?</summary>
The doubly protonated, positively charged form (HIP) is stabilised by the nearby negative charge, which raises the histidine pK$_a$. Run a pK$_a$ prediction, and if the result is near the experimental pH, simulate both states.
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
