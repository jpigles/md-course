---
title: Molecular dynamics, from Newton's law to free energies
short: Course home
summary: A self-study course on how molecular dynamics simulations work: the equations of motion, the force fields, the statistical mechanics, and the mathematics behind each, with lectures to watch, texts to read, live demos and exercises.
---

<div class="cards">
<div class="card"><b>{{N_MODULES}}</b><span>modules, about {{N_HOURS}} hours of study</span></div>
<div class="card"><b>{{N_VIDEOS}}</b><span>videos and playlists holding {{N_LECTURES}} lectures, nearly 300 of them attached to the section they teach</span></div>
<div class="card"><b>{{N_BOOKS}} + {{N_NOTES}}</b><span>textbooks, free lecture notes and tutorials</span></div>
<div class="card"><b>{{N_PAPERS}}</b><span>papers with verified identifiers, {{N_READ_FULL}} read in full</span></div>
<div class="card"><b>{{N_WIDGETS}}</b><span>simulations that run in the page, with toy data to download</span></div>
</div>

## What this course is

Molecular dynamics is easy to run and hard to understand. A tutorial will get you a trajectory in an afternoon. Knowing why the time step is 2 fs, what the thermostat does to your ensemble, why a cutoff on electrostatics is wrong, what a force field's parameters mean, and how many independent samples are in your trajectory takes longer, and it is what decides whether the result can be trusted.

This course goes through all of it in order, with the derivations written out. It assumes you can differentiate and integrate, have seen vectors and matrices, and can read Python. Everything else is built up from Newton's second law.

Each module has the same layout:

1. **Goals**: what you will be able to do at the end.
2. **Lectures for this module**: lectures on YouTube for that topic, from full university courses down to short explainers. They are optional. The lesson is written to be complete without them, and they are there for when you want a second explanation. Inside the lesson, most sections also carry a strip called **Lectures on this part**: the specific lectures that teach that section. Click one and it plays in the page.
3. **The lesson**: the ideas and the mathematics, step by step, with worked numbers. Each section starts in plain words. Every new idea from physics or mathematics is explained from the beginning where it first appears, in a box of its own. Under every displayed formula a list says what each letter in it means.
4. **Try it**: in every module from 1 to 17, a simulation that runs in the page. Most of them let you download the data they generate, and the [toy data page](toy-data.html) shows what to do with it. Module 10 also has a [notebook for Google Colab](https://colab.research.google.com/github/jpigles/md-course/blob/main/notebooks/md_lysozyme_openmm.ipynb) that runs a real simulation of a protein on a free GPU, from the structure file to the analysed trajectory.
5. **Check yourself**: short questions with answers hidden until you click.
6. **Exercises**: things to derive, code and run.
7. **Read** and **Key papers**: where to go deeper, with free sources marked.

Tick "I have finished this module" at the bottom of each page and the sidebar keeps track of your progress (stored in your browser only).

## If the mathematics or the physics is new to you

You do not need to be a physicist to follow the course. Three pages are there for the background, and the lessons link to them at the places where they are needed:

- the [maths toolbox](maths.html) explains every piece of mathematics the course uses, from "how to read a formula" and the derivative up to Fourier transforms and eigenvalues, each with a small worked example;
- the [physics primer](physics.html) does the same for the physics: units, force and energy, temperature, entropy and free energy, charges, and why atoms can be treated as classical balls;
- the [list of symbols](symbols.html) says what each letter stands for and in which module it is introduced.

You can read the first two once before Module 1, or open them only when a lesson sends you there.

## Syllabus

{{MODULE_TABLE}}

## A twelve-week plan

About eight to ten hours a week. Do the exercises: the derivations only stick when you have reproduced them.

| Week | Modules | Milestone |
|---|---|---|
| 1 | 1, 2 | You have run and read a 35-line MD program and can write Hamilton's equations |
| 2 | 3 | You can derive the Boltzmann distribution and compute an average from a partition function |
| 3 | 4 | You have derived velocity Verlet twice and measured energy conservation against time step |
| 4 | 5, 6 | You can read a topology file and say where each parameter came from |
| 5 | 7 | You have derived the Ewald sum and know every non-bonded setting in an input file |
| 6 | 8, 9 | You have added a Langevin thermostat and SHAKE to your own code |
| 7 | 10 | You have taken a protein from a PDB file to a production run, three repeats |
| 8 | 11 | Your results have error bars from block averaging and from repeats |
| 9 | 12 | You have written WHAM and converted a free-energy profile to a dissociation constant |
| 10 | 13, 14 | You have computed a hydration free energy and run a replica-exchange or metadynamics simulation |
| 11 | 15, 16 | You have run a coarse-grained model and built a small Markov state model |
| 12 | 17, 18, projects | You know what current machine-learning models were trained on, and you have completed one of the capstone projects |

## Whole courses on video

If you prefer to follow one lecturer from start to finish, pick one of these and use the modules here as the written companion.

{{COURSE_PLAYLISTS}}

## The backbone texts

Four books cover almost everything here at greater depth, and they complement each other: Frenkel and Smit, *Understanding Molecular Simulation* (algorithms and why they work); Tuckerman, *Statistical Mechanics: Theory and Molecular Simulation* (the rigorous derivations); Allen and Tildesley, *Computer Simulation of Liquids* (practical detail and code); and Leach, *Molecular Modelling* (force fields and applications). Free alternatives that go a long way: M. Scott Shell's lecture notes for his UCSB simulation course, David Tong's Cambridge notes on classical dynamics and statistical physics, the GROMACS reference manual, and the best-practice articles of the Living Journal of Computational Molecular Science. All are listed with links in the [library](library.html).

## How far you can trust this

The lessons were written by an AI system and then checked. Three independent referees re-derived the equations and recomputed the numbers, and every cited paper whose full text could be obtained legally (124 of the 144 in the main list) was read and compared with what the course says about it, equations included. Together they found 7 statements that were wrong and about 260 that were imprecise, and these were corrected. Papers that could not be read are not labelled as read. The full account, including what is still unverified, is on the page [How this course was checked](sources.html).

Module 18 was written differently: from the papers first, with a source for every number.

In November 2026 the lessons were rewritten so that they can be followed without the videos, with the background explained and every symbol defined. A program checked that no equation, number or citation of the checked text was lost. Each rewritten lesson then went to an independent referee, which re-derived the added formulas, recomputed the numbers and read every symbol list. The referees found about 540 problems, 44 of them statements that were wrong, and these were corrected. The new explanations have not been read by a human expert.

The video, book and paper lists were compiled in November 2026. Linked videos, books and papers belong to their authors and publishers.
