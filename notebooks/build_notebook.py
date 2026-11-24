#!/usr/bin/env python3
"""Write notebooks/md_lysozyme_openmm.ipynb from the cells below.

    python3 notebooks/build_notebook.py

The notebook runs the workflow of Module 10 for real: lysozyme in water with OpenMM,
meant for Google Colab with a GPU. Keeping the cells here as plain text makes them easy to edit.
"""
import json
from pathlib import Path

SITE = "https://jpigles.github.io/md-course"
L10 = SITE + "/10-running-a-simulation.html"
cells = []


def md(text):
    cells.append(("markdown", text.strip("\n")))


def code(text):
    cells.append(("code", text.strip("\n")))


# ----------------------------------------------------------------------------------------
md(f"""
# A real MD simulation: lysozyme in water

This notebook runs the workflow of [Module 10]({L10}) of the course *Molecular dynamics, from Newton's law to free energies* on a real protein, from a file of the Protein Data Bank to an analysed trajectory. Nothing is prepared in advance: the structure is downloaded, cleaned, put in a box of water with ions, minimised, equilibrated and simulated here, in front of you.

| | |
|---|---|
| Protein | Hen egg-white lysozyme, PDB entry [1AKI](https://www.rcsb.org/structure/1AKI), 129 residues |
| Program | [OpenMM](https://openmm.org), the second of the two programs of Module 10 |
| Model | The settings of the OpenMM script in the lesson: Amber14 protein force field, TIP3P-FB water, particle-mesh Ewald, bonds to hydrogen constrained, 4 fs time step |
| What runs | Minimisation, 100 ps at constant volume and 200 ps at constant pressure with the protein held in place, then 1 ns of production |
| Time needed | Under 10 minutes on the free T4 GPU of Google Colab (when this notebook was tested there, the 1 ns production run took 4.5 minutes). Without a GPU it works too, but then shorten the run (see "Settings") |

**Before you start, switch the GPU on:** menu *Runtime*, *Change runtime type*, choose *T4 GPU*, *Save*. Then run the cells from top to bottom (Shift+Enter runs one cell, *Runtime > Run all* runs everything).

Every step below names the section of the lesson that explains it. The lesson has the reasons. This notebook has the practice.
""")

md("""
## 0. Set-up

The first cell installs the programs: OpenMM (the simulation engine), PDBFixer (repairs structure files), MDTraj (reads and analyses trajectories) and py3Dmol (shows molecules in the page). On Colab this takes about a minute. It then looks for the fastest way to run on this machine: an NVIDIA GPU through CUDA, any GPU through OpenCL, or the processor.
""")

code(r'''
import sys, os, time
IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    !nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || echo "No GPU found: choose Runtime > Change runtime type > T4 GPU"
    !pip install -q "openmm[cuda12]" pdbfixer mdtraj py3Dmol

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openmm as mm
from openmm import app, unit

print("OpenMM", mm.version.version)


def pick_platform():
    """Return the fastest platform that works here: CUDA, then OpenCL, then CPU."""
    for name in ("CUDA", "OpenCL", "CPU"):
        try:
            platform = mm.Platform.getPlatformByName(name)
            test = mm.System()
            test.addParticle(1.0)
            mm.Context(test, mm.VerletIntegrator(0.001), platform)
            return platform
        except Exception:
            print(f"  {name}: not available on this machine")
    return mm.Platform.getPlatformByName("Reference")


platform = pick_platform()
properties = {"Precision": "mixed"} if platform.getName() in ("CUDA", "OpenCL") else {}
print("The simulation will run on:", platform.getName())
if platform.getName() == "CPU":
    print("No GPU is in use. The run below will be slow: set PROD_NS = 0.05 in the settings.")
''')

md("""
## Settings

All the numbers you may want to change are in this one cell. The defaults reproduce the lesson. Change one thing at a time and run the notebook again from this cell.
""")

code(r'''
PDB_ID      = "1AKI"    # which entry of the Protein Data Bank to simulate
TEMPERATURE = 300       # kelvin
NVT_PS      = 100       # equilibration at constant volume, in picoseconds (protein restrained)
NPT_PS      = 200       # equilibration at constant pressure, in picoseconds (protein restrained)
PROD_NS     = 1.0       # production run, in nanoseconds
SEED        = 1         # seed of the random starting velocities: another number gives another run

DT_FS       = 4.0       # time step in femtoseconds (allowed by constraints plus heavier hydrogens, Module 9)
REPORT_PS   = 1.0       # how often the equilibration writes temperature, density and so on
TRAJ_PS     = 10.0      # how often the production run saves a frame
MIN_ITER    = 0         # minimisation steps; 0 means "until converged"

# A fast dry run, used to test this notebook on a computer without a GPU. Leave it alone.
QUICK = os.environ.get("MDC_QUICK") == "1"
if QUICK:
    NVT_PS, NPT_PS, PROD_NS, REPORT_PS, TRAJ_PS, MIN_ITER = 2, 2, 0.02, 0.2, 1.0, 100


def steps(picoseconds):
    """Number of time steps in a given number of picoseconds."""
    return int(round(picoseconds * 1000 / DT_FS))


print(f"time step {DT_FS:g} fs: NVT {steps(NVT_PS):,} steps, NPT {steps(NPT_PS):,} steps, "
      f"production {steps(PROD_NS * 1000):,} steps")
''')

md(f"""
## 1. The starting structure

Lesson: [Step 1: the starting structure]({L10}#step-1-the-starting-structure).

The structure comes from the Protein Data Bank, as determined by X-ray crystallography. A crystal structure is not ready to simulate. Look at what the file contains: the protein atoms, some water molecules that were ordered enough to be seen in the crystal, and no hydrogen atoms at all, because X-rays hardly see them.
""")

code(r'''
import urllib.request
from collections import Counter

pdb_file = f"{PDB_ID}.pdb"
if not os.path.exists(pdb_file):
    urllib.request.urlretrieve(f"https://files.rcsb.org/download/{PDB_ID}.pdb", pdb_file)

lines = open(pdb_file).read().splitlines()
title = " ".join(l[10:].strip() for l in lines if l.startswith("TITLE"))
atom_lines = [l for l in lines if l.startswith("ATOM")]
het_lines = [l for l in lines if l.startswith("HETATM")]
residues = {(l[21], l[22:27]) for l in atom_lines}

print(title)
print(f"{len(atom_lines)} protein atoms in {len(residues)} residues")
print("other molecules in the file:", dict(Counter(l[17:20].strip() for l in het_lines)))
print("hydrogen atoms in the file:", sum(1 for l in atom_lines if l[76:78].strip() == "H"))
''')

code(r'''
import py3Dmol

view = py3Dmol.view(width=640, height=420)
view.addModel(open(pdb_file).read(), "pdb")
view.setStyle({"cartoon": {"color": "spectrum"}})
view.addStyle({"resn": "HOH"}, {"sphere": {"radius": 0.35, "color": "red"}})
view.zoomTo()
view.show()   # drag to turn, scroll to zoom. The red dots are the water molecules seen in the crystal.
''')

md("""
### Cleaning the file and adding hydrogens

Three repairs, in the order of the lesson:

1. **Remove what is not the protein.** The crystal waters go. The box will be filled with water in the next step.
2. **Add atoms that are missing.** Side chains at the surface are sometimes too mobile to be seen. PDBFixer rebuilds them. For this entry nothing is missing, and the cell says so.
3. **Add the hydrogens**, which fixes the protonation state: which acidic and basic groups carry a charge. The cell asks for the states that are usual at pH 7. The net charge that results decides how many counter-ions are needed.
""")

code(r'''
from pdbfixer import PDBFixer

fixer = PDBFixer(filename=pdb_file)
fixer.findMissingResidues()
print("residues missing inside or at the ends of the chain:", sum(len(v) for v in fixer.missingResidues.values()))
fixer.missingResidues = {}             # do not invent residues that the experiment did not see
fixer.findNonstandardResidues()
print("non-standard residues:", len(fixer.nonstandardResidues))
fixer.replaceNonstandardResidues()
fixer.removeHeterogens(keepWater=False)
fixer.findMissingAtoms()
print("residues with missing heavy atoms:", len(fixer.missingAtoms), "| chain ends to complete:", len(fixer.missingTerminals))
fixer.addMissingAtoms()

forcefield = app.ForceField("amber14-all.xml", "amber14/tip3pfb.xml")
model = app.Modeller(fixer.topology, fixer.positions)
before = model.topology.getNumAtoms()
model.addHydrogens(forcefield, pH=7.0)
print(f"atoms: {before} without hydrogens, {model.topology.getNumAtoms()} with hydrogens")

# the net charge: add up the partial charges that the force field gives to the atoms
vacuum = forcefield.createSystem(model.topology)
nonbonded = [f for f in vacuum.getForces() if isinstance(f, mm.NonbondedForce)][0]
net_charge = sum(nonbonded.getParticleParameters(i)[0].value_in_unit(unit.elementary_charge)
                 for i in range(vacuum.getNumParticles()))
n_protein_atoms = model.topology.getNumAtoms()
print(f"net charge of the protein: {net_charge:+.0f} e")
''')

md(f"""
## 2. The box, the water and the ions

Lesson: [Steps 2 to 4: topology, box, water, ions]({L10}#steps-2-to-4-topology-box-water-ions).

One call builds the box, fills it with water and adds the ions.

- `boxShape="dodecahedron"`: a rhombic dodecahedron, the nearly spherical box that needs the least water for a globular protein.
- `padding=2.4 nm`: in OpenMM this is the guaranteed distance between the protein and its nearest periodic copy. It builds the same box as `gmx editconf -d 1.2` in GROMACS, where the 1.2 nm is the distance to the box face.
- `ionicStrength=0.15 molar`: first enough counter-ions to cancel the net charge of the protein, then sodium chloride up to 0.15 mol/L.

The force field was already chosen in the cell above: `amber14-all.xml` for the protein and `amber14/tip3pfb.xml` for the water and the ions.
""")

code(r'''
model.addSolvent(forcefield, padding=2.4 * unit.nanometer,
                 ionicStrength=0.15 * unit.molar, boxShape="dodecahedron")

counts = Counter(residue.name for residue in model.topology.residues())
n_water, n_na, n_cl = counts["HOH"], counts["NA"], counts["CL"]
a, b, c = model.topology.getPeriodicBoxVectors()
volume = (a[0] * b[1] * c[2]).value_in_unit(unit.nanometer**3)

print(f"atoms in the box: {model.topology.getNumAtoms():,} ({n_protein_atoms:,} of them protein)")
print(f"water molecules: {n_water:,}    sodium ions: {n_na}    chloride ions: {n_cl}")
print(f"box volume: {volume:.1f} nm^3, edge of the dodecahedron cell {a[0].value_in_unit(unit.nanometer):.2f} nm")
print(f"chloride minus sodium = {n_cl - n_na}, which cancels the protein charge of {net_charge:+.0f} e")
print(f"pure water would put {33.4 * volume:,.0f} molecules in this volume; the {33.4 * volume - n_water:,.0f} "
      f"that are not here give the room taken by the protein and the ions")
print(f"salt: {min(n_na, n_cl)} ion pairs for {n_water:,} waters = one pair per {n_water / min(n_na, n_cl):.0f} waters "
      f"(0.15 mol/L is one pair per 370)")

app.PDBFile.writeFile(model.topology, model.positions, open("solvated.pdb", "w"), keepIds=True)
''')

md(f"""
### The system: how the forces are computed

Lesson: [The same workflow in OpenMM]({L10}#the-same-workflow-in-openmm), and for the meaning of each choice Modules 7, 8 and 9.

`createSystem` turns the list of atoms into the full energy function. The four settings are those of the lesson:

- `nonbondedMethod=app.PME`: particle-mesh Ewald for the electrostatics (Module 7);
- `nonbondedCutoff=1.0 nm`: the distance up to which pairs are computed one by one;
- `constraints=app.HBonds`: bonds to hydrogen keep a fixed length (Module 9);
- `hydrogenMass=4 amu`: each hydrogen is made heavier at the cost of the atom it is bonded to, which slows the fastest motions and allows a time step of 4 fs.

One more term is added by hand: a **position restraint**, a spring between every heavy atom of the protein and a reference position. Its strength `k_restraint` is a number we can change during the run. It starts at zero.
""")

code(r'''
NOT_SOLUTE = ("HOH", "NA", "CL")


def make_simulation(seed):
    """Build the system, the integrator and the simulation object. Returns them with the restraint."""
    system = forcefield.createSystem(model.topology,
                                     nonbondedMethod=app.PME,
                                     nonbondedCutoff=1.0 * unit.nanometer,
                                     constraints=app.HBonds,
                                     hydrogenMass=4 * unit.amu)

    # position restraints on the heavy atoms of the protein; periodicdistance() is the
    # distance to the nearest periodic copy of the reference point, as the OpenMM manual advises
    restraint = mm.CustomExternalForce("0.5*k_restraint*periodicdistance(x, y, z, x0, y0, z0)^2")
    restraint.addGlobalParameter("k_restraint", 0.0)            # kJ/mol/nm^2, switched on later
    for name in ("x0", "y0", "z0"):
        restraint.addPerParticleParameter(name)
    heavy = [atom.index for atom in model.topology.atoms()
             if atom.residue.name not in NOT_SOLUTE and atom.element.symbol != "H"]
    for index in heavy:
        restraint.addParticle(index, model.positions[index].value_in_unit(unit.nanometer))
    system.addForce(restraint)

    # the thermostat is part of the integrator: Langevin dynamics at 300 K, friction 1/ps (Module 8)
    integrator = mm.LangevinMiddleIntegrator(TEMPERATURE * unit.kelvin,
                                             1 / unit.picosecond,
                                             DT_FS * unit.femtoseconds)
    integrator.setRandomNumberSeed(seed)
    simulation = app.Simulation(model.topology, system, integrator, platform, properties)
    simulation.context.setPositions(model.positions)
    return simulation, system, restraint, heavy


sim, system, restraint, heavy = make_simulation(SEED)
print(f"{system.getNumParticles():,} particles, {system.getNumConstraints():,} constraints, "
      f"{len(heavy):,} restrained atoms")
print("energy terms:", ", ".join(type(f).__name__ for f in system.getForces()))
''')

md(f"""
## 3. Energy minimisation

Lesson: [Step 5: energy minimisation]({L10}#step-5-energy-minimisation).

The water was placed around the protein without looking at the forces, and the hydrogens were added by geometry. Some atoms sit too close to each other, and there the forces are enormous. A simulation started from here would blow up in its first steps. Minimisation moves the atoms downhill in energy until the largest forces are gone. It does not look for the best structure. It only removes the worst contacts.

The cell prints the potential energy and the largest force on any atom, before and after.
""")

code(r'''
def energy_and_max_force(simulation):
    state = simulation.context.getState(getEnergy=True, getForces=True)
    energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
    forces = state.getForces(asNumpy=True).value_in_unit(unit.kilojoule_per_mole / unit.nanometer)
    return energy, float(np.linalg.norm(forces, axis=1).max())


e_before, f_before = energy_and_max_force(sim)
start = time.time()
sim.minimizeEnergy(maxIterations=MIN_ITER)
e_after, f_after = energy_and_max_force(sim)

print(f"potential energy: {e_before:14,.0f} -> {e_after:12,.0f} kJ/mol")
print(f"largest force:    {f_before:14,.0f} -> {f_after:12,.0f} kJ/mol/nm")
print(f"minimisation took {time.time() - start:.0f} s")
''')

md(f"""
## 4. Equilibration

Lesson: [Steps 6 and 7: equilibration]({L10}#steps-6-and-7-equilibration).

The minimised system is at zero temperature and its water has never moved. Equilibration brings it to the temperature and the density of the experiment, in two stages, while the protein is held near its starting structure so that the unsettled water cannot distort it.

1. **Constant volume (NVT).** Velocities are drawn at random for 300 K, and the thermostat holds the temperature. Check: the temperature reaches 300 K and fluctuates around it.
2. **Constant pressure (NPT).** A barostat is added and lets the box change its size. Check: the density settles near 1 g/cm$^3$.

The restraints use the minimised structure as their reference (the same choice as `-r em.gro` in the GROMACS commands of the lesson) and a spring constant of 1,000 kJ mol$^{{-1}}$ nm$^{{-2}}$.
""")

code(r'''
# reference positions of the restraints = the minimised structure; then switch the springs on
minimised = sim.context.getState(getPositions=True).getPositions(asNumpy=True).value_in_unit(unit.nanometer)
for n, index in enumerate(heavy):
    restraint.setParticleParameters(n, index, minimised[index].tolist())
restraint.updateParametersInContext(sim.context)
sim.context.setParameter("k_restraint", 1000.0)

# stage 1: constant volume
sim.context.setVelocitiesToTemperature(TEMPERATURE * unit.kelvin, SEED)
sim.reporters = [app.StateDataReporter("equilibration.csv", steps(REPORT_PS), time=True,
                                       potentialEnergy=True, temperature=True, volume=True, density=True)]
start = time.time()
sim.step(steps(NVT_PS))
print(f"NVT: {NVT_PS} ps in {time.time() - start:.0f} s")

# stage 2: constant pressure. Adding a force to the system needs a fresh context; the state is kept.
barostat = mm.MonteCarloBarostat(1 * unit.bar, TEMPERATURE * unit.kelvin)
system.addForce(barostat)
sim.context.reinitialize(preserveState=True)
start = time.time()
sim.step(steps(NPT_PS))
print(f"NPT: {NPT_PS} ps in {time.time() - start:.0f} s")
''')

code(r'''
def read_log(filename):
    table = pd.read_csv(filename)
    table.columns = [name.strip('#"') for name in table.columns]
    return table


eq = read_log("equilibration.csv")
eq_time = (np.arange(len(eq)) + 1) * REPORT_PS            # ps since the start of the equilibration

fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
for axis, column, label in zip(axes, ["Temperature (K)", "Density (g/mL)", "Potential Energy (kJ/mole)"],
                               ["temperature (K)", "density (g/cm$^3$)", "potential energy (kJ/mol)"]):
    axis.plot(eq_time, eq[column], lw=1.2)
    axis.axvline(NVT_PS, color="gray", ls="--", lw=1)
    axis.set_xlabel("time (ps)")
    axis.set_ylabel(label)
axes[0].axhline(TEMPERATURE, color="tab:red", lw=0.8)
axes[0].set_title("left of the dashed line: constant volume; right: constant pressure", fontsize=10, loc="left")
plt.tight_layout()
plt.show()

half = eq[eq_time > NVT_PS + NPT_PS / 2]
print(f"second half of the NPT stage: temperature {half['Temperature (K)'].mean():.1f} K, "
      f"density {half['Density (g/mL)'].mean():.3f} g/cm^3")
''')

md("""
**How to read the plots.** The temperature should reach the target within a few picoseconds and then fluctuate by a few kelvin. That fluctuation is physics: the smaller the system, the larger it is (Module 3). The density is constant in the first stage, because the box cannot change, and moves to its own value once the barostat is on. If the density were still drifting at the right edge, the equilibration would be too short.
""")

md(f"""
## 5. The production run

Lesson: [Step 8: production]({L10}#step-8-production-an-annotated-input-file).

The springs are switched off and the protein is free. From here on, frames are saved for analysis:

- `trajectory.dcd`: the positions of all atoms, every 10 ps;
- `production.csv`: energies, temperature, density at the same times;
- `state.chk`: a checkpoint, from which an interrupted run can be continued.

The table that the cell prints shows the progress and the speed in nanoseconds of simulation per day of computing.
""")

code(r'''
sim.context.setParameter("k_restraint", 0.0)        # release the protein

n_production = steps(PROD_NS * 1000)
progress_every = max(n_production // 10, 1)
sim.reporters = [
    app.DCDReporter("trajectory.dcd", steps(TRAJ_PS)),
    app.StateDataReporter("production.csv", steps(TRAJ_PS), time=True, potentialEnergy=True,
                          kineticEnergy=True, temperature=True, volume=True, density=True),
    app.StateDataReporter(sys.stdout, progress_every, step=True, temperature=True, speed=True,
                          remainingTime=True, totalSteps=sim.currentStep + n_production, separator="\t"),
    app.CheckpointReporter("state.chk", progress_every),
]
start = time.time()
sim.step(n_production)
elapsed = time.time() - start

speed = PROD_NS / elapsed * 86400
print(f"\n{PROD_NS:g} ns in {elapsed / 60:.1f} minutes: {speed:.0f} ns per day on {platform.getName()}")
print(f"at this speed 100 ns would take {100 / speed * 24:.1f} hours")

sim.saveState("final_state.xml")
final = sim.context.getState(getPositions=True, enforcePeriodicBox=True)
app.PDBFile.writeFile(sim.topology, final.getPositions(), open("final.pdb", "w"), keepIds=True)
''')

md(f"""
## 6. Is the run healthy?

Lesson: [What goes wrong]({L10}#what-goes-wrong), and Module 11 for the statistics.

Before looking at the protein, look at the thermodynamic record. In a healthy run the temperature and the density fluctuate around steady values, with no drift.
""")

code(r'''
prod = read_log("production.csv")
prod_time = (np.arange(len(prod)) + 1) * TRAJ_PS / 1000          # ns

fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
for axis, column, label in zip(axes, ["Temperature (K)", "Density (g/mL)", "Potential Energy (kJ/mole)"],
                               ["temperature (K)", "density (g/cm$^3$)", "potential energy (kJ/mol)"]):
    axis.plot(prod_time, prod[column], lw=1.2)
    axis.set_xlabel("time (ns)")
    axis.set_ylabel(label)
plt.tight_layout()
plt.show()

print(f"temperature: {prod['Temperature (K)'].mean():.1f} K, standard deviation {prod['Temperature (K)'].std():.1f} K")
print(f"density:     {prod['Density (g/mL)'].mean():.4f} g/cm^3, standard deviation {prod['Density (g/mL)'].std():.4f}")
n_df = 3 * system.getNumParticles() - system.getNumConstraints() - 3
print(f"expected size of the temperature fluctuation, T*sqrt(2/N_df): {TEMPERATURE * np.sqrt(2 / n_df):.1f} K (Module 3)")
''')

md(f"""
## 7. What did the protein do?

Lesson: [Periodic images in the output]({L10}#periodic-images-in-the-output), and Module 11 for the quantities.

First a repair. During the run a molecule that leaves the box through one face comes back in through the opposite one, so in the saved frames the protein can appear to jump or to be cut in pieces. Nothing is wrong with the simulation: the pictures have to be put back together (`image_molecules`). Then each frame is laid on top of the starting structure (`superpose`), which removes the tumbling of the whole molecule.

Three standard quantities follow:

- **RMSD**: how far the C$\\alpha$ atoms are, on average, from where they were in the starting structure. It says how much the fold has changed.
- **Radius of gyration** $R_g$: the overall size of the protein.
- **RMSF**: how much each residue moves around its own average position. It shows which parts are rigid and which are floppy.
""")

code(r'''
import mdtraj as md

traj = md.load("trajectory.dcd", top="solvated.pdb")
print(traj)
traj.image_molecules(inplace=True)                         # put the molecules back together

protein_atoms = traj.topology.select("protein")
ptraj = traj.atom_slice(protein_atoms)                     # the protein alone
reference = md.load("solvated.pdb").atom_slice(protein_atoms)
ca = ptraj.topology.select("name CA")
ptraj.superpose(reference, 0, atom_indices=ca)             # remove the overall motion

time_ns = (np.arange(ptraj.n_frames) + 1) * TRAJ_PS / 1000
rmsd = md.rmsd(ptraj, reference, 0, atom_indices=ca) * 10          # nm -> angstrom
rg = md.compute_rg(ptraj)                                           # nm
positions = ptraj.xyz[:, ca, :]
rmsf = np.sqrt(((positions - positions.mean(axis=0)) ** 2).sum(axis=2).mean(axis=0)) * 10   # angstrom
residue_numbers = [ptraj.topology.atom(i).residue.resSeq for i in ca]

fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
axes[0].plot(time_ns, rmsd)
axes[0].set_xlabel("time (ns)"); axes[0].set_ylabel(r"C$\alpha$ RMSD from the start ($\AA$)")
axes[1].plot(time_ns, rg)
axes[1].set_xlabel("time (ns)"); axes[1].set_ylabel("radius of gyration (nm)")
axes[2].plot(residue_numbers, rmsf)
axes[2].set_xlabel("residue number"); axes[2].set_ylabel(r"C$\alpha$ RMSF ($\AA$)")
plt.tight_layout()
plt.show()
''')

md("""
### A number with an error bar

A result without an error bar is not a result. Successive frames of one trajectory resemble each other, so the plain formula "standard deviation divided by the square root of the number of frames" gives an error that is too small. **Block averaging** (Module 11) cuts the trajectory into a few long pieces, averages each piece, and takes the scatter of the piece averages.

One warning that the method cannot remove: one nanosecond is very short for a protein. Motions slower than the run are not sampled at all, and no error bar computed from the run can know about them. Treat the number below as a lower limit of the uncertainty.
""")

code(r'''
def block_average(values, n_blocks=5):
    """Mean and standard error from the means of n_blocks consecutive blocks."""
    means = np.array([block.mean() for block in np.array_split(np.asarray(values), n_blocks)])
    return means.mean(), means.std(ddof=1) / np.sqrt(n_blocks)


second_half = slice(ptraj.n_frames // 2, None)
rg_mean, rg_error = block_average(rg[second_half])
naive = rg[second_half].std(ddof=1) / np.sqrt(len(rg[second_half]))
print(f"radius of gyration, second half of the run: {rg_mean:.3f} +/- {rg_error:.3f} nm (5 blocks)")
print(f"the plain formula would have claimed +/- {naive:.4f} nm")

# secondary structure in every frame, with the DSSP method built into MDTraj
dssp = md.compute_dssp(ptraj, simplified=True)             # H = helix, E = strand, C = coil
helix, strand = (dssp == "H").mean(axis=1), (dssp == "E").mean(axis=1)
print(f"residues in a helix: {100 * helix.mean():.0f} %   in a strand: {100 * strand.mean():.0f} %"
      f"   (first frame: {100 * helix[0]:.0f} % and {100 * strand[0]:.0f} %)")
''')

md("""
### Watch it

The cell below plays the protein alone, from up to 50 frames spread over the run. Each frame was laid on the starting structure, so what you see is the internal motion.
""")

code(r'''
stride = max(1, ptraj.n_frames // 50)
ptraj[::stride].save_pdb("movie.pdb")

view = py3Dmol.view(width=640, height=420)
view.addModelsAsFrames(open("movie.pdb").read(), "pdb")
view.setStyle({"cartoon": {"color": "spectrum"}})
view.zoomTo()
view.animate({"loop": "forward", "interval": 120})
view.show()
''')

md(f"""
## 8. Repeats

Lesson: [Planning: length, repeats, output, cost]({L10}#planning-length-repeats-output-cost) and Exercise 2.

One trajectory is one sample of a random process. The honest way to say how sure you are is to run the whole protocol several times with different starting velocities and to compare the results. The cell below does that for three seeds. It is switched off by default because it triples the computing time: set `RUN_REPEATS = True` to try it. With the default lengths each repeat is short, so read the outcome as a demonstration of the method and not as a measurement of lysozyme.
""")

code(r'''
RUN_REPEATS = False
REPEAT_NS = 0.5                     # production length of each repeat, in ns
if QUICK:
    RUN_REPEATS, REPEAT_NS = True, 0.004


def run_repeat(seed, production_ns):
    """The whole protocol for one seed. Returns the radius of gyration of the saved frames (nm)."""
    simulation, system_r, restraint_r, heavy_r = make_simulation(seed)
    simulation.minimizeEnergy(maxIterations=MIN_ITER)
    start_xyz = simulation.context.getState(getPositions=True).getPositions(asNumpy=True).value_in_unit(unit.nanometer)
    for n, index in enumerate(heavy_r):
        restraint_r.setParticleParameters(n, index, start_xyz[index].tolist())
    restraint_r.updateParametersInContext(simulation.context)
    simulation.context.setParameter("k_restraint", 1000.0)
    simulation.context.setVelocitiesToTemperature(TEMPERATURE * unit.kelvin, seed)
    simulation.step(steps(NVT_PS))
    system_r.addForce(mm.MonteCarloBarostat(1 * unit.bar, TEMPERATURE * unit.kelvin))
    simulation.context.reinitialize(preserveState=True)
    simulation.step(steps(NPT_PS))
    simulation.context.setParameter("k_restraint", 0.0)
    name = f"repeat_{seed}.dcd"
    simulation.reporters = [app.DCDReporter(name, steps(TRAJ_PS))]
    simulation.step(steps(production_ns * 1000))
    del simulation.reporters[:]                      # closes the trajectory file
    t = md.load(name, top="solvated.pdb")
    t.image_molecules(inplace=True)
    return md.compute_rg(t.atom_slice(protein_atoms))


if RUN_REPEATS:
    means = []
    for seed in (11, 12, 13):
        start = time.time()
        rg_repeat = run_repeat(seed, REPEAT_NS)
        means.append(rg_repeat[len(rg_repeat) // 2:].mean())
        print(f"seed {seed}: mean radius of gyration {means[-1]:.3f} nm ({time.time() - start:.0f} s)")
    means = np.array(means)
    error = means.std(ddof=1) / np.sqrt(len(means))
    print(f"\nthree repeats: {means.mean():.3f} +/- {error:.3f} nm (standard error of the mean, n = 3)")
    print(f"95 % interval with the t factor for n = 3 (4.30): +/- {4.30 * error:.3f} nm")
else:
    print("Repeats are switched off. Set RUN_REPEATS = True and run this cell again to try them.")
''')

md("""
## 9. Going on, and keeping your results

**A longer run.** To add simulated time to the run above, keep the notebook open and run a cell like this one. `append=True` adds the new frames to the existing files.

```python
more_ns = 1.0
sim.reporters = [app.DCDReporter("trajectory.dcd", steps(TRAJ_PS), append=True),
                 app.StateDataReporter("production.csv", steps(TRAJ_PS), time=True, potentialEnergy=True,
                                       kineticEnergy=True, temperature=True, volume=True, density=True, append=True),
                 app.CheckpointReporter("state.chk", steps(100))]
sim.step(steps(more_ns * 1000))
```

**After an interruption.** Colab disconnects after a while, and its files are deleted when the session ends. A checkpoint (`state.chk`) lets a run continue: build the simulation again with the cells above, then call `sim.loadCheckpoint("state.chk")` before `sim.step(...)`. A checkpoint can only be read on the same kind of hardware and with the same OpenMM version that wrote it, so on Colab, download your results before you leave.

**Download.** The cell below packs the results into one file. On Colab it also offers the file for download.
""")

code(r'''
import zipfile

keep = ["solvated.pdb", "final.pdb", "final_state.xml", "trajectory.dcd",
        "equilibration.csv", "production.csv", "state.chk"]
with zipfile.ZipFile("md_results.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for name in keep:
        if os.path.exists(name):
            archive.write(name)
print(f"md_results.zip: {os.path.getsize('md_results.zip') / 1e6:.1f} MB")

DOWNLOAD = False          # set to True on Colab to save the file to your computer
if DOWNLOAD and IN_COLAB:
    from google.colab import files
    files.download("md_results.zip")
''')

md(f"""
## Things to try

Each of these changes one line in the "Settings" cell or in one step, and each connects to a lesson.

1. **Another seed.** Set `SEED = 2` and run again. The curves differ in detail and agree in their averages. That is what "statistically the same" means ([Module 2]({SITE}/02-classical-mechanics.html), chaos).
2. **No equilibration.** Set `NVT_PS = 0` and `NPT_PS = 1`, and look at the density at the start of the production run.
3. **Hotter.** Set `TEMPERATURE = 350`. What happens to the RMSD and to the size of the temperature fluctuation?
4. **A smaller time step.** Set `DT_FS = 2.0`. The run takes twice as long. Do the averages change?
5. **Another protein.** Set `PDB_ID = "1UBQ"` (ubiquitin, 76 residues). Entries with several chains, ligands or missing loops need more care at step 1: read what the cleaning cell reports.
6. **Longer.** Set `PROD_NS = 10`. Does the RMSD level off, or does it keep creeping up? How does the block error of the radius of gyration change?

What this notebook does not do: it does not tell you whether one nanosecond, or ten, is enough for your question. For that, read [Module 11]({SITE}/11-analysis-statistics.html).

*Part of the course [Molecular dynamics, from Newton's law to free energies]({SITE}/). The lysozyme structure 1AKI belongs to the Protein Data Bank and its depositors.*
""")

# ----------------------------------------------------------------------------------------
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"provenance": [], "gpuType": "T4", "name": "md_lysozyme_openmm.ipynb"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "cells": [],
}
for n, (kind, text) in enumerate(cells):
    src = text.splitlines(keepends=True)
    cell = {"cell_type": kind, "metadata": {}, "source": src, "id": f"c{n:02d}"}
    if kind == "code":
        cell.update({"execution_count": None, "outputs": []})
    nb["cells"].append(cell)

out = Path(__file__).resolve().parent / "md_lysozyme_openmm.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(f"{out.name}: {len(cells)} cells ({sum(1 for k, _ in cells if k == 'code')} code)")
