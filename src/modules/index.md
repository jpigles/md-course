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
2. **Watch first**: lectures on YouTube for that topic, from full university courses down to short explainers. Inside the lesson, most sections also carry a strip called **Watch for this part**: the specific lectures that teach that section. Click one and it plays in the page.
3. **The lesson**: the ideas and the mathematics, step by step, with worked numbers.
4. **Try it**: in every module from 1 to 17, a simulation that runs in the page. Most of them let you download the data they generate, and the [toy data page](toy-data.html) shows what to do with it.
5. **Check yourself**: short questions with answers hidden until you click.
6. **Exercises**: things to derive, code and run.
7. **Read** and **Key papers**: where to go deeper, with free sources marked.

Tick "I have finished this module" at the bottom of each page and the sidebar keeps track of your progress (stored in your browser only).

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

The lessons were written by an AI system and then checked. Three independent referees re-derived the equations and recomputed the numbers, and every cited paper whose full text could be obtained legally (58 of the 144 in the main list) was read and compared with what the course says about it. Together they found 7 statements that were wrong and about 150 that were imprecise, and these were corrected. Papers that could not be read are not labelled as read. The full account, including what is still unverified, is on the page [How this course was checked](sources.html).

Module 18 was written differently: from the papers first, with a source for every number.

The video, book and paper lists were compiled in November 2026. Linked videos, books and papers belong to their authors and publishers.
