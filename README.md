# Molecular dynamics: a course from Newton's law to free energies

A self-study course on how molecular dynamics simulations work: the equations of motion, the force fields, the statistical mechanics, and the mathematics behind each.

**Read it here: https://jpigles.github.io/md-course/**

## What is in it

- 17 modules in five parts: foundations (classical and statistical mechanics), the engine (integrators, force fields, periodic boundaries and Ewald summation, thermostats and barostats, constraints), practice (running a simulation, analysis and error bars), free energy and sampling (umbrella sampling, WHAM and MBAR, alchemical methods, enhanced sampling), and beyond all-atom (coarse-grained models, kinetics and Markov state models, machine-learned potentials).
- Each module has learning goals, lectures to watch, the lesson with derivations and worked numbers, questions with hidden answers, exercises, and a reading list.
- Four simulations that run in the page: a pair-potential plotter, three integrators on a spring, a live 2D Lennard-Jones fluid, and umbrella sampling with WHAM on a double well.
- A library of lecture videos, textbooks, free lecture notes, tutorials and key papers, a formula sheet, and eight capstone projects.

## Layout of this repository

| Path | Content |
|---|---|
| `*.html`, `style.css`, `course.js` | The built site, served by GitHub Pages from the repository root |
| `src/modules/*.md` | The source of every page: Markdown with LaTeX maths |
| `src/build.py` | Turns the sources and the research lists into the HTML pages |
| `src/style.css`, `src/course.js` | Stylesheet and the interactive demos |
| `research/` | The verified lists of videos, books, notes, tutorials and papers that the pages are generated from |

## Rebuilding

```bash
pip install markdown pygments
python3 src/build.py        # writes the pages into site/
```

Maths is rendered in the browser with KaTeX.

## Sources

Video links were checked against YouTube, and paper details were taken from the Crossref record of each DOI, in November 2026. Linked videos, books and papers belong to their authors and publishers. The lesson text is original.
