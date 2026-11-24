#!/usr/bin/env python3
"""Write notebooks/md_lysozyme_gromacs.ipynb from the cells below.

    python3 notebooks/build_notebook_gromacs.py

The notebook runs the GROMACS track of Module 10 for real, on Google Colab with a GPU.
The five parameter files are taken from the lesson source when this script runs, so the
notebook always uses the files that the lesson prints.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = "https://jpigles.github.io/md-course"
L10 = SITE + "/10-running-a-simulation.html"

lesson = (ROOT / "src" / "modules" / "10-running-a-simulation.md").read_text(encoding="utf-8")
MDP = {}
for block in re.findall(r"^```[a-z]*\n(.*?)^```[ \t]*$", lesson, flags=re.S | re.M):
    first = block.lstrip().splitlines()[0] if block.strip() else ""
    m = re.match(r";\s*(ions|em|nvt|npt|md)\.mdp", first)
    if m:
        MDP[m.group(1)] = block.rstrip("\n")
assert set(MDP) == {"ions", "em", "nvt", "npt", "md"}, sorted(MDP)

cells = []


def md(text):
    cells.append(("markdown", text.strip("\n").replace("{L10}", L10).replace("{SITE}", SITE)))


def code(text):
    cells.append(("code", text.strip("\n")))


# ----------------------------------------------------------------------------------------
md("""
# A real MD simulation with GROMACS: lysozyme in water

This notebook runs the GROMACS commands of [Module 10]({L10}) of the course *Molecular dynamics, from Newton's law to free energies*, exactly as the lesson prints them, on a real protein. The structure is downloaded from the Protein Data Bank, and everything else happens here: topology, box, water, ions, minimisation, two equilibration runs with the protein held in place, a production run, and the analysis.

| | |
|---|---|
| Protein | Hen egg-white lysozyme, PDB entry [1AKI](https://www.rcsb.org/structure/1AKI), 129 residues |
| Program | [GROMACS](https://www.gromacs.org) 2026, the GPU build from conda-forge |
| Model | The files of the lesson: Amber99SB-ILDN protein force field, TIP3P water, particle-mesh Ewald, bonds to hydrogen constrained, 2 fs time step |
| What runs | Minimisation, 100 ps at constant volume and 100 ps at constant pressure with position restraints, then a production run (1 ns by default) |

**Before you start, switch the GPU on:** menu *Runtime*, *Change runtime type*, choose *T4 GPU*, *Save*. Then run the cells from top to bottom (*Runtime > Run all*).

The cells that start with `%%bash` contain the commands as you would type them in a terminal. The cells that start with `%%writefile` create the parameter files, which are the five `.mdp` files of the lesson, unchanged. The other cells are Python and only draw plots.

There is a sister notebook that does the same with OpenMM: [md_lysozyme_openmm.ipynb](https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb).
""")

md("""
## 0. Installing GROMACS

Colab does not come with GROMACS. The cell below downloads a ready-made build from conda-forge, a public collection of scientific software: the GPU build if this session has an NVIDIA GPU, the processor-only build otherwise. This takes two or three minutes and is needed once per session. The last lines print the version that was installed.
""")

code(r'''
import os, re, sys, shutil, subprocess, time
import numpy as np
import matplotlib.pyplot as plt

IN_COLAB = "google.colab" in sys.modules
GMX_PREFIX = "/opt/gmx"


def has_nvidia_gpu():
    try:
        return subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


GPU = has_nvidia_gpu()
build = "nompi_cuda*" if GPU else "nompi_h*"
print("NVIDIA GPU found:", GPU, "-> installing the", "GPU" if GPU else "processor-only", "build of GROMACS")

start = time.time()
if not os.path.exists(f"{GMX_PREFIX}/bin/gmx"):
    !curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj -C /tmp bin/micromamba
    !/tmp/bin/micromamba create -y -q -p {GMX_PREFIX} -c conda-forge "gromacs=2026.*={build}" > /tmp/gromacs_install.log 2>&1 || tail -n 20 /tmp/gromacs_install.log

# take over the settings that "activating" the installation would make in a terminal
activated = subprocess.run(
    f'eval "$(/tmp/bin/micromamba shell hook -s bash)" && micromamba activate {GMX_PREFIX} && env',
    shell=True, capture_output=True, text=True, executable="/bin/bash").stdout
for line in activated.splitlines():
    name, _, value = line.partition("=")
    if name in ("PATH", "LD_LIBRARY_PATH", "CONDA_PREFIX") or name.startswith("GMX"):
        os.environ[name] = value
os.environ["GMX_MAXBACKUP"] = "-1"        # no numbered backup copies when a cell is run twice
print(f"installation took {time.time() - start:.0f} s")

!gmx --version | grep -E "GROMACS version|Precision|GPU support|SIMD instructions"
!pip install -q mdtraj py3Dmol
''')

md("""
## Settings

The lesson's production file asks for 100 ns, which would take most of a day here. This cell sets the length used in this notebook. Everything else is taken from the lesson's files as they are.
""")

code(r'''
PDB_ID  = "1AKI"     # which entry of the Protein Data Bank to simulate
PROD_NS = 1.0        # production run in nanoseconds (the lesson's md.mdp has 100)

if not GPU:
    print("No GPU in this session: every run below will be slow (hours). Switch the GPU on, or set PROD_NS = 0.02.")


def read_xvg(filename):
    """Read a GROMACS .xvg table: returns the numbers and the names of the data columns."""
    names, rows = [], []
    for line in open(filename):
        if line.startswith("@"):
            found = re.match(r'@\s+s\d+\s+legend\s+"(.*)"', line)
            if found:
                names.append(found.group(1))
        elif not line.startswith("#") and line.strip():
            rows.append([float(x) for x in line.split()])
    return np.array(rows), names
''')

md("""
## 1. The starting structure

Lesson: [Step 1: the starting structure]({L10}#step-1-the-starting-structure).

The file from the Protein Data Bank holds the protein atoms and 78 water molecules that were ordered enough to be seen in the crystal. It holds no hydrogen atoms. The crystal waters are removed here (the lines that contain `HOH`), because the box will be filled with water in step 3. The hydrogens are added by the next command.
""")

code(r'''
import urllib.request

if not os.path.exists(f"{PDB_ID}.pdb"):
    urllib.request.urlretrieve(f"https://files.rcsb.org/download/{PDB_ID}.pdb", f"{PDB_ID}.pdb")
lines = open(f"{PDB_ID}.pdb").read().splitlines()
kept = [l for l in lines if "HOH" not in l]
open("protein.pdb", "w").write("\n".join(kept) + "\n")

atoms = [l for l in kept if l.startswith("ATOM")]
print(" ".join(l[10:].strip() for l in lines if l.startswith("TITLE")))
print(f"{len(atoms)} protein atoms in {len({(l[21], l[22:27]) for l in atoms})} residues; "
      f"{sum(1 for l in lines if l.startswith('HETATM') and 'HOH' in l)} crystal waters removed; "
      f"hydrogen atoms in the file: {sum(1 for l in atoms if l[76:78].strip() == 'H')}")
''')

code(r'''
import py3Dmol

view = py3Dmol.view(width=640, height=400)
view.addModel(open("protein.pdb").read(), "pdb")
view.setStyle({"cartoon": {"color": "spectrum"}})
view.zoomTo()
view.show()
''')

md("""
## 2. The topology

Lesson: [Steps 2 to 4: topology, box, water, ions]({L10}#steps-2-to-4-topology-box-water-ions).

`gmx pdb2gmx` reads the structure, adds the hydrogens, and writes three files: the structure with hydrogens (`processed.gro`), the **topology** (`topol.top`: every atom with its type and charge, every bond, angle and torsion), and the list of atoms for the position restraints (`posre.itp`). The options choose the force field and the water model. `-ignh` tells it to ignore any hydrogens in the input and to build its own.

The program prints several screens of text. Here that text goes into a file, and only the line with the net charge is shown.
""")

code(r'''
%%bash
set -e
gmx pdb2gmx -f protein.pdb -o processed.gro -p topol.top -ff amber99sb-ildn -water tip3p -ignh > pdb2gmx.log 2>&1
grep "Total charge" pdb2gmx.log | tail -1
echo "atoms with hydrogens: $(sed -n 2p processed.gro)"
ls -l processed.gro topol.top posre.itp | awk '{print $5, "bytes", $9}'
''')

md("""
## 3. The box, the water and the ions

Three commands, as in the lesson.

1. `gmx editconf` puts the protein in the centre (`-c`) of a rhombic dodecahedron (`-bt dodecahedron`) whose faces are at least 1.2 nm away from it (`-d 1.2`).
2. `gmx solvate` fills the box with water. `spc216.gro` is a small equilibrated box of three-site water that is copied as often as needed.
3. `gmx genion` replaces water molecules by ions: enough to cancel the charge of the protein (`-neutral`), plus sodium chloride up to 0.15 mol/L (`-conc 0.15`).
""")

code(r'''
%%bash
set -e
gmx editconf -f processed.gro -o boxed.gro -c -d 1.2 -bt dodecahedron > editconf.log 2>&1
grep -E "new box volume" editconf.log
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top > solvate.log 2>&1
grep -E "Number of solvent molecules" solvate.log
echo "atoms in the box: $(sed -n 2p solvated.gro)"
''')

md("""
`gmx genion` needs a run input file (`.tpr`), and a `.tpr` file needs a parameter file. That is the only job of `ions.mdp`: no run is made from it. It is the minimisation file with one change, a plain cutoff in place of PME.
""")

code("%%writefile ions.mdp\n" + MDP["ions"])

md("""
**See for yourself why the change is needed.** The next cell tries the step with the minimisation file `em.mdp`, which uses PME. The box still has a net charge, GROMACS gives a warning, and a warning stops `gmx grompp`. (The file `em.mdp` is written here already and is used for the minimisation in step 4.)
""")

code("%%writefile em.mdp\n" + MDP["em"])

code(r'''
%%bash
gmx grompp -f em.mdp -c solvated.gro -p topol.top -o try.tpr > try.log 2>&1 \
  && echo "grompp accepted the file" \
  || { echo "grompp stopped. Its message:"; grep -A6 "^WARNING" try.log; grep -A1 "Fatal error" try.log; }
''')

md("""
Now the same step with `ions.mdp`, and then `gmx genion`. The tool asks which group of molecules it may replace. The answer, the water, is the group `SOL`, and `echo SOL |` types it for us.
""")

code(r'''
%%bash
set -e
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr > grompp_ions.log 2>&1
grep -c "^NOTE" grompp_ions.log | sed 's/^/notes from grompp (expected: non-zero charge, plain cutoff): /'
echo SOL | gmx genion -s ions.tpr -o ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15 > genion.log 2>&1
echo "the end of topol.top now lists what is in the box:"
tail -n 5 topol.top
''')

md("""
## 4. Energy minimisation

Lesson: [Step 5: energy minimisation]({L10}#step-5-energy-minimisation).

The water and the hydrogens were placed without looking at the forces, so some atoms are too close to each other. Minimisation moves the atoms downhill in energy until the largest force is below the limit `emtol` of `em.mdp` (1,000 kJ mol$^{-1}$ nm$^{-1}$).

Every run in GROMACS has the same two commands: `gmx grompp` packs the parameters, the structure and the topology into one run input file, and `gmx mdrun` runs it. `-deffnm em` gives all files of this run the name `em`.
""")

code(r'''
%%bash
set -e
gmx grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr > grompp_em.log 2>&1
gmx mdrun -deffnm em > mdrun_em.log 2>&1
grep -A4 "Steepest Descents converged\|did not converge" em.log | head -6
echo Potential | gmx energy -f em.edr -o em_potential.xvg > /dev/null 2>&1
''')

code(r'''
data, names = read_xvg("em_potential.xvg")
plt.figure(figsize=(6, 3.4))
plt.plot(data[:, 0], data[:, 1])
plt.xlabel("minimisation step")
plt.ylabel("potential energy (kJ/mol)")
plt.tight_layout()
plt.show()
print(f"potential energy: {data[0, 1]:,.0f} -> {data[-1, 1]:,.0f} kJ/mol in {int(data[-1, 0])} steps")
''')

md("""
## 5. Equilibration at constant volume (NVT)

Lesson: [Steps 6 and 7: equilibration]({L10}#steps-6-and-7-equilibration) and [The equilibration input files]({L10}#the-equilibration-input-files).

Velocities are drawn at random for 300 K, and the thermostat holds the temperature. The protein is held near its minimised structure by position restraints: `define = -DPOSRES` in the file below switches them on, and `-r em.gro` in the command gives the reference positions. The run is 100 ps.
""")

code("%%writefile nvt.mdp\n" + MDP["nvt"])

code(r'''
%%bash
set -e
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr > grompp_nvt.log 2>&1
gmx mdrun -deffnm nvt > mdrun_nvt.log 2>&1
grep -B1 "^Performance" nvt.log
echo Temperature | gmx energy -f nvt.edr -o nvt_temperature.xvg > /dev/null 2>&1
''')

code(r'''
data, names = read_xvg("nvt_temperature.xvg")
plt.figure(figsize=(6, 3.4))
plt.plot(data[:, 0], data[:, 1])
plt.axhline(300, color="tab:red", lw=0.8)
plt.xlabel("time (ps)")
plt.ylabel("temperature (K)")
plt.tight_layout()
plt.show()
half = data[len(data) // 2:, 1]
print(f"second half of the run: {half.mean():.1f} K, standard deviation {half.std():.1f} K")
''')

md("""
**Check.** The temperature should reach 300 K within a few picoseconds and then fluctuate around it by a few kelvin. The fluctuation is physics, not an error (Module 3).

## 6. Equilibration at constant pressure (NPT)

The barostat is switched on, and the box may now change its size until the density is right. The run continues from the NVT run: `-t nvt.cpt` passes on the velocities, and `continuation = yes` in the file says that the bonds already have their fixed lengths. The restraints stay on, and `refcoord-scaling = all` lets their reference positions follow the box.
""")

code("%%writefile npt.mdp\n" + MDP["npt"])

code(r'''
%%bash
set -e
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr > grompp_npt.log 2>&1
gmx mdrun -deffnm npt > mdrun_npt.log 2>&1
grep -B1 "^Performance" npt.log
printf "Density\nPressure\n" | gmx energy -f npt.edr -o npt_density.xvg > /dev/null 2>&1
''')

code(r'''
data, names = read_xvg("npt_density.xvg")
column = {name: i + 1 for i, name in enumerate(names)}
fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
axes[0].plot(data[:, 0], data[:, column["Density"]])
axes[0].set_xlabel("time (ps)"); axes[0].set_ylabel("density (kg/m$^3$)")
axes[1].plot(data[:, 0], data[:, column["Pressure"]], lw=0.8)
axes[1].axhline(1, color="tab:red", lw=0.8)
axes[1].set_xlabel("time (ps)"); axes[1].set_ylabel("pressure (bar)")
plt.tight_layout()
plt.show()
half = data[len(data) // 2:]
print(f"second half: density {half[:, column['Density']].mean():.0f} kg/m^3, "
      f"pressure {half[:, column['Pressure']].mean():.0f} bar with a standard deviation of {half[:, column['Pressure']].std():.0f} bar")
''')

md("""
**Check.** Use the density, not the pressure. The density should settle near 1,000 kg/m$^3$ (a little higher with a protein in the box). The pressure swings by hundreds of bar from one moment to the next, because water is nearly incompressible, and only its long average means anything (Module 8).

## 7. The production run

Lesson: [Step 8: production]({L10}#step-8-production-an-annotated-input-file).

The restraints are off: the production file has no `define = -DPOSRES`. First the file of the lesson is written as it is, under the name `md_lesson.mdp`. The cell after it makes `md.mdp` from it by changing one line, the number of steps, to the length set in "Settings".
""")

code("%%writefile md_lesson.mdp\n" + MDP["md"])

code(r'''
n_steps = int(round(PROD_NS * 1000 / 0.002))             # the time step of the file is 2 fs = 0.002 ps
text = open("md_lesson.mdp").read()
new_line = f"nsteps                  = {n_steps:<13d} ; {n_steps:,} x 2 fs = {PROD_NS:g} ns"
text, n_changed = re.subn(r"^nsteps .*$", new_line, text, flags=re.M)
assert n_changed == 1
open("md.mdp", "w").write(text)
print(new_line)
''')

code(r'''
%%bash
set -e
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr > grompp_md.log 2>&1
gmx mdrun -deffnm md > mdrun_md.log 2>&1
grep -B1 "^Performance" md.log
grep "^ *Time:" md.log
ls -l md.xtc md.edr md.cpt md.gro | awk '{print $5, "bytes", $9}'
''')

md("""
`Performance` is the speed in nanoseconds of simulation per day of computing, and the number next to it is hours per nanosecond. Multiply by the length you plan to run before you start a long simulation.

## 8. Putting the molecules back together

Lesson: [Periodic images in the output]({L10}#periodic-images-in-the-output).

During the run, a molecule that leaves the box through one face comes back in through the opposite one. In the saved frames the protein can therefore appear to jump across the box. `gmx trjconv` repairs the pictures: `-pbc mol` keeps every molecule in one piece and `-center` puts the protein in the middle. It asks two questions (which group to centre, which group to write out), and `printf` answers them: `Protein`, then `System`.
""")

code(r'''
%%bash
set -e
printf "Protein\nSystem\n" | gmx trjconv -s md.tpr -f md.xtc -o md_centred.xtc -pbc mol -center > trjconv.log 2>&1
ls -l md_centred.xtc | awk '{print $5, "bytes", $9}'
''')

md("""
## 9. Analysis

Lesson: Module 11 for the quantities and their error bars.

GROMACS has a tool for each standard quantity. Each asks which atoms to use, and the answers are again typed by `echo` or `printf`.

- `gmx energy` reads temperature, density and energies from the energy file.
- `gmx rms` computes the RMSD: how far the backbone is from the minimised structure, after laying each frame on top of it.
- `gmx gyrate` computes the radius of gyration, the overall size of the protein.
- `gmx rmsf` computes how much each residue moves around its average position.
""")

code(r'''
%%bash
set -e
printf "Temperature\nDensity\nPotential\n" | gmx energy -f md.edr -o md_energy.xvg > /dev/null 2>&1
printf "Backbone\nBackbone\n" | gmx rms -s em.tpr -f md_centred.xtc -o rmsd.xvg -tu ns > rms.log 2>&1
gmx gyrate -s md.tpr -f md_centred.xtc -o gyrate.xvg -sel Protein -tu ns > gyrate.log 2>&1
echo "C-alpha" | gmx rmsf -s md.tpr -f md_centred.xtc -o rmsf.xvg -res > rmsf.log 2>&1
ls -l md_energy.xvg rmsd.xvg gyrate.xvg rmsf.xvg | awk '{print $5, "bytes", $9}'
''')

code(r'''
energy, names = read_xvg("md_energy.xvg")
column = {name: i + 1 for i, name in enumerate(names)}
time_ns = energy[:, 0] / 1000

fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
for axis, name, label in zip(axes, ["Temperature", "Density", "Potential"],
                             ["temperature (K)", "density (kg/m$^3$)", "potential energy (kJ/mol)"]):
    axis.plot(time_ns, energy[:, column[name]], lw=1.0)
    axis.set_xlabel("time (ns)"); axis.set_ylabel(label)
plt.tight_layout()
plt.show()
print(f"temperature {energy[:, column['Temperature']].mean():.1f} K (standard deviation {energy[:, column['Temperature']].std():.1f} K), "
      f"density {energy[:, column['Density']].mean():.0f} kg/m^3")
''')

code(r'''
rmsd, _ = read_xvg("rmsd.xvg")            # time in ns, RMSD in nm
gyr, gyr_names = read_xvg("gyrate.xvg")   # time in ns, radius of gyration in nm (first data column)
rmsf, _ = read_xvg("rmsf.xvg")            # residue number, RMSF in nm

fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
axes[0].plot(rmsd[:, 0], rmsd[:, 1] * 10)
axes[0].set_xlabel("time (ns)"); axes[0].set_ylabel(r"backbone RMSD from the minimised structure ($\AA$)")
axes[1].plot(gyr[:, 0], gyr[:, 1])
axes[1].set_xlabel("time (ns)"); axes[1].set_ylabel("radius of gyration (nm)")
axes[2].plot(rmsf[:, 0], rmsf[:, 1] * 10)
axes[2].set_xlabel("residue number"); axes[2].set_ylabel(r"C$\alpha$ RMSF ($\AA$)")
plt.tight_layout()
plt.show()


def block_average(values, n_blocks=5):
    """Mean and standard error from the means of n_blocks consecutive blocks (Module 11)."""
    means = np.array([block.mean() for block in np.array_split(np.asarray(values), n_blocks)])
    return means.mean(), means.std(ddof=1) / np.sqrt(n_blocks)


second_half = gyr[len(gyr) // 2:, 1]
mean, error = block_average(second_half)
print(f"radius of gyration, second half of the run: {mean:.3f} +/- {error:.3f} nm (5 blocks)")
print(f"the plain formula would have claimed +/- {second_half.std(ddof=1) / np.sqrt(len(second_half)):.4f} nm")
''')

md("""
**How to read the result.** One nanosecond is very short for a protein. The RMSD shows that the fold stays close to the crystal structure, and the RMSF shows which loops are mobile. Motions slower than the run are not sampled at all, and no error bar computed from this run can know about them: treat the error above as a lower limit.

### Watch it

`gmx trjconv` writes the protein alone, with every frame laid on top of the first (`-fit rot+trans`), and the cell after it plays the frames.
""")

code(r'''
%%bash
set -e
printf "Backbone\nProtein\n" | gmx trjconv -s md.tpr -f md_centred.xtc -o movie.pdb -fit rot+trans -skip 2 > movie.log 2>&1
grep -c "^MODEL" movie.pdb | sed 's/$/ frames in movie.pdb/'
''')

code(r'''
view = py3Dmol.view(width=640, height=420)
view.addModelsAsFrames(open("movie.pdb").read(), "pdb")
view.setStyle({"cartoon": {"color": "spectrum"}})
view.zoomTo()
view.animate({"loop": "forward", "interval": 120})
view.show()
''')

md("""
## 10. Going on, and keeping your results

**After an interruption.** The command `gmx mdrun -deffnm md -cpi md.cpt` continues a run from its checkpoint. If there is no checkpoint yet it starts from the first step, so the same command serves for the first job and for every later one.

**A longer run.** To add time to a finished run, extend its run input file and continue (here by 1,000 ps):

```bash
gmx convert-tpr -s md.tpr -extend 1000 -o md.tpr
gmx mdrun -deffnm md -cpi md.cpt
```

**Repeats.** One trajectory is one sample. For an honest error bar, repeat steps 5 to 7 with other starting velocities: in `nvt.mdp`, give `gen-seed` a different whole number for each repeat (Exercise 2 of the lesson).

**Download.** Colab deletes its files when the session ends. The cell below packs the results into one file.
""")

code(r'''
import zipfile

keep = ["topol.top", "posre.itp", "ions.gro", "em.gro", "nvt.gro", "npt.gro", "md.gro", "md.tpr", "md.cpt",
        "md.xtc", "md_centred.xtc", "md.edr", "md.log", "ions.mdp", "em.mdp", "nvt.mdp", "npt.mdp", "md.mdp",
        "rmsd.xvg", "gyrate.xvg", "rmsf.xvg", "md_energy.xvg"]
with zipfile.ZipFile("gromacs_results.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for name in keep:
        if os.path.exists(name):
            archive.write(name)
print(f"gromacs_results.zip: {os.path.getsize('gromacs_results.zip') / 1e6:.1f} MB")

DOWNLOAD = False          # set to True on Colab to save the file to your computer
if DOWNLOAD and IN_COLAB:
    from google.colab import files
    files.download("gromacs_results.zip")
''')

md("""
## Things to try

1. **Read a log file.** Run `!tail -n 40 md.log` in a new cell. It shows where the computing time went and how the work was shared between the processor and the GPU.
2. **Skip the equilibration.** Start the production run directly from `em.gro` (you will need `gen-vel = yes` and `continuation = no` in a copy of `md.mdp`). Look at the density during the first picoseconds.
3. **Another seed.** Set `gen-seed = 2` in `nvt.mdp` and run steps 5 to 9 again. Compare the averages, not the curves.
4. **Forget `refcoord-scaling`.** Remove that line from `npt.mdp` and run `gmx grompp` for the NPT step. Read the message.
5. **Another protein.** Set `PDB_ID = "1UBQ"` (ubiquitin). Entries with ligands, several chains or missing atoms need more care at step 2: read what `pdb2gmx.log` says.

*Part of the course [Molecular dynamics, from Newton's law to free energies]({SITE}/). The lysozyme structure 1AKI belongs to the Protein Data Bank and its depositors.*
""")

# ----------------------------------------------------------------------------------------
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"provenance": [], "gpuType": "T4", "name": "md_lysozyme_gromacs.ipynb"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "cells": [],
}
for n, (kind, text) in enumerate(cells):
    cell = {"cell_type": kind, "metadata": {}, "source": text.splitlines(keepends=True), "id": f"g{n:02d}"}
    if kind == "code":
        cell.update({"execution_count": None, "outputs": []})
    nb["cells"].append(cell)

out = HERE / "md_lysozyme_gromacs.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(f"{out.name}: {len(cells)} cells ({sum(1 for k, _ in cells if k == 'code')} code)")
