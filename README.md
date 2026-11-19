# Molecular dynamics: a course from Newton's law to free energies

A self-study course on how molecular dynamics simulations work: the equations of motion, the force fields, the statistical mechanics, and the mathematics behind each.

**Read it here: https://jpigles.github.io/md-course/**

## What is in it

- 18 modules in five parts: foundations (classical and statistical mechanics), the engine (integrators, force fields, periodic boundaries and Ewald summation, thermostats and barostats, constraints), practice (running a simulation, analysis and error bars), free energy and sampling (umbrella sampling, WHAM and MBAR, alchemical methods, enhanced sampling), and beyond all-atom (coarse-grained models, kinetics and Markov state models, machine-learned potentials, and the state of the art in machine-learning models trained on MD data).
- Each module has learning goals, lectures to watch, the lesson with derivations and worked numbers, questions with hidden answers, exercises, and a reading list.
- Seventeen simulations that run in the page, one per module, most with toy data you can download as CSV: a live 2D Lennard-Jones fluid, Liouville's theorem, thermostats, block averaging, umbrella sampling with WHAM, free-energy perturbation against BAR, metadynamics, a Markov state model, a small neural-network potential, and others.
- Specific lectures attached to specific sections of each lesson, playable in the page.
- A library of lecture videos, textbooks, free lecture notes, tutorials and key papers, a formula sheet, and eight capstone projects.

## Layout of this repository

| Path | Content |
|---|---|
| `*.html`, `style.css`, `course.js` | The built site, served by GitHub Pages from the repository root |
| `src/modules/*.md` | The source of every page: Markdown with LaTeX maths |
| `src/build.py` | Turns the sources and the research lists into the HTML pages |
| `src/style.css`, `src/course.js`, `src/demos2.js` | Stylesheet and the interactive demos |
| `research/` | The verified lists of videos, books, notes, tutorials and papers that the pages are generated from; the short annotation of every paper that was read (`paper_notes.json`); the referees' reports (`review_part1.md` to `review_part3.md`) |

The full reading notes (one per paper) and the evidence files behind Module 18 quote the papers at length, so they are kept offline with the course sources and are not published here.

## Rebuilding

```bash
pip install markdown pygments
python3 src/build.py        # writes the pages into site/
```

Maths is rendered in the browser with KaTeX.

## How it was checked

The lessons were written by an AI system (Claude) and then checked by independent referees and against the full text of every cited paper that could be obtained legally. What was verified, what was found wrong and corrected, and what is still unverified is recorded on the site under "How this course was checked". Linked videos, books and papers belong to their authors and publishers.
