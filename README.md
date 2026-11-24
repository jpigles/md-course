# Molecular dynamics: a course from Newton's law to free energies

A self-study course on how molecular dynamics simulations work: the equations of motion, the force fields, the statistical mechanics, and the mathematics behind each.

**Read it here: https://jpigles.github.io/md-course/**

## What is in it

- 18 modules in five parts: foundations (classical and statistical mechanics), the engine (integrators, force fields, periodic boundaries and Ewald summation, thermostats and barostats, constraints), practice (running a simulation, analysis and error bars), free energy and sampling (umbrella sampling, WHAM and MBAR, alchemical methods, enhanced sampling), and beyond all-atom (coarse-grained models, kinetics and Markov state models, machine-learned potentials, and the state of the art in machine-learning models trained on MD data).
- Each module has learning goals, the lesson with derivations and worked numbers, optional lectures, questions with hidden answers, exercises, and a reading list.
- The lessons are written to be followed without the videos and without a physics degree: each section starts in plain words, every new idea from physics or mathematics is explained from the beginning in a box of its own, and under every displayed formula a list says what each letter means.
- Three background pages: a maths toolbox (28 sections, from "how to read a formula" to Fourier transforms), a physics primer (16 sections) and a searchable list of all symbols, built from the lessons.
- Seventeen simulations that run in the page, one per module, most with toy data you can download as CSV: a live 2D Lennard-Jones fluid, Liouville's theorem, thermostats, block averaging, umbrella sampling with WHAM, free-energy perturbation against BAR, metadynamics, a Markov state model, a small neural-network potential, and others.
- Specific lectures attached to specific sections of each lesson, playable in the page.
- A library of lecture videos, textbooks, free lecture notes, tutorials and key papers, a formula sheet, and eight capstone projects.

## Layout of this repository

| Path | Content |
|---|---|
| `*.html`, `style.css`, `course.js` | The built site, served by GitHub Pages from the repository root |
| `src/modules/*.md` | The source of every page: Markdown with LaTeX maths |
| `notebooks/md_lysozyme_gromacs.ipynb` | A notebook for Google Colab that runs the GROMACS commands and the five parameter files of Module 10 for real, on lysozyme with a GPU ([open in Colab](https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_gromacs.ipynb)). `build_notebook_gromacs.py` writes it and takes the parameter files from the lesson source |
| `notebooks/md_lysozyme_openmm.ipynb` | A notebook for Google Colab that runs the workflow of Module 10 for real: lysozyme in water with OpenMM on a GPU ([open in Colab](https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb)). `build_notebook.py` writes it, `run_local_test.py` runs it in a shortened form |
| `src/build.py` | Turns the sources and the research lists into the HTML pages |
| `src/style.css`, `src/course.js`, `src/demos2.js` | Stylesheet and the interactive demos |
| `research/` | The verified lists of videos, books, notes, tutorials and papers that the pages are generated from; the short annotation of every paper that was read (`paper_notes.json`); the referees' reports (`review_part1.md` to `review_part3.md`); the rules and programs of the rewrite that made the lessons self-contained (`expand_brief.md`, `toolbox_brief.md`, `expand_review_brief.md`, `check_module.py`, `apply_expand_fixes.py`) |

The full reading notes (one per paper), the evidence files behind Module 18 and the referee reports of the rewrite quote the papers at length, so they are kept offline with the course sources and are not published here. The originals of the lessons before the rewrite are in `research/modules_before_expand/`.

## Rebuilding

```bash
pip install markdown pygments
python3 src/build.py        # writes the pages into site/
```

Maths is rendered in the browser with KaTeX.

## How it was checked

The lessons were written by an AI system (Claude) and then checked by independent referees and against the full text of every cited paper that could be obtained legally. What was verified, what was found wrong and corrected, and what is still unverified is recorded on the site under "How this course was checked". Linked videos, books and papers belong to their authors and publishers.
