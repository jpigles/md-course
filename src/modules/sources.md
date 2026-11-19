---
title: How this course was checked
short: How it was checked
summary: An honest account of what was verified, how, what was found wrong and corrected, and what still rests on unverified knowledge.
---

This course was written by an AI system (Claude) for one student, and then checked in several independent ways. You should know exactly how far the checking went.

## The lesson text

Modules 1 to 17 were first written from general knowledge, without consulting the papers. They were then checked twice.

**1. Three independent technical referees.** Each read six modules, re-derived the main equations, recomputed every worked number and "check yourself" answer, ran the code, and checked software statements against the GROMACS and OpenMM documentation. They found **39 problems: 5 wrong, 6 misleading, 28 imprecise**. All were corrected. The most serious:

| Where | What was wrong | Now |
|---|---|---|
| Module 1 | "$10^{11}$ steps per day at best" | About $5\times10^8$ (the old figure was 200 times too high) |
| Module 1 | SHAKE listed under the 1980s | 1977 |
| Module 13 | Sign of the restraint term in the absolute binding free energy | Enters with a minus sign (the error was worth about 14 kcal/mol) |
| Module 3 | Mean force and binding-constant formulas mixed two definitions of the radial PMF | The two definitions are now stated and kept apart |
| Module 10 | OpenMM `padding=1.2 nm` presented as equal to GROMACS `-d 1.2` | `padding=2.4 nm`, since OpenMM's padding is the distance between periodic copies |
| Projects | Check for Project 4 said $\ln k$ against $h$ has slope $-1$ | $\ln(k/h)$ has slope $-1$ |

**2. The cited papers, read in full.** Of the 144 papers in the main reference list, 58 could be obtained legally and were read: 55 from first line to last and 3 in part. Fifty of them are open-access articles, PubMed Central full text or arXiv preprints that a program can fetch. Eight more are free on PubMed Central but only in a browser, and they were read there, two of them (Gilson et al. 1997 and Huber and Kim 1996) from scanned page images. In four of the browser-read papers the displayed equations are pictures and were read only through the surrounding text, which is why Woo and Roux (2005) is labelled read in part. Against the 58 papers, **572 statements of the course were checked: 2 were wrong and 116 imprecise**, and the substantive ones were corrected. The two wrong ones:

| Where | What the course said | What the paper says |
|---|---|---|
| Module 6 | ff19SB was fitted with OPC water | It was fitted to quantum-mechanical energy surfaces in implicit solvent; OPC is only recommended with it (Tian et al. 2020) |
| Module 6 | CHARMM36m re-fitted selected Lennard-Jones pairs and the water model | It changed the backbone CMAP term and one pair-specific term, and kept CHARMM-modified TIP3P (Huang et al. 2017) |

In the reference lists, a paper that was read carries the label <span class="tag read">read in full</span> or <span class="tag read">read in part</span>, with a line on what it is for and what to read in it.

**What this does not cover.** The other 86 papers could not be read: most are behind a paywall, and two open-access ones (the GROMACS and LAMMPS reference papers) sit on a publisher site that turns automated readers away. For those, only the bibliographic details were verified. Statements in the lessons about what those papers did (for example the original Verlet, SHAKE, Nosé, Hoover and Ewald papers) rest on textbook knowledge and on the referees' checks, not on a reading of the paper. Where a text was read as a preprint, the published article may differ.

**Module 18** was written the other way round: from evidence files built by reading the literature first, with a page reference for every number.

## The references

- **Papers.** Every DOI was looked up in Crossref twice, by two separate programs, and title, year and first author compared: 144 of 144 match. PubMed Central links were checked to point at the same DOI. The 60 references of Module 18 were checked against Crossref or the arXiv record.
- **Books.** Publisher or author pages were confirmed to load, and ISBN check digits are valid. An automatic catalogue lookup by ISBN was not available at the time, so editions and years rely on the publisher pages.
- **Lecture notes and tutorials.** Each link was requested and returned a page; five publisher or university pages answer programs with a challenge page and were confirmed by hand.

## The videos

- Each of the {{N_VIDEOS}} catalogue entries was confirmed against YouTube twice. Title and channel are YouTube's own.
- Durations, and the list of lectures inside each playlist, were read from the YouTube pages: {{N_LECTURES}} individual lectures are known this way.
- Lectures were attached to sections of the lessons according to their **title and the uploader's description**. Nobody watched them from start to end for this course. If a lecture turns out not to match its section, that is where the error came from.
- Three entries were removed after reading their descriptions (two student presentations and one with no description).

## The simulations in the pages

The {{N_WIDGETS}} in-page simulations were each started and checked for errors in a browser, on a wide and a narrow screen. The umbrella-sampling demo recovers the exact potential to about 0.2 $k_BT$, the Liouville demo conserves area to about a percent, and the free-energy demo reproduces the exact answer with the acceptance-ratio estimator. They are teaching toys in reduced units, not research code.

## Where the records are

In the repository: the referees' reports (`research/review_part1.md` to `review_part3.md`), the lists the pages are built from, and the short annotation of each paper that was read (`research/paper_notes.json`).

Kept offline with the course sources, not published: the full reading note for each paper (`research/paper_notes/`) and the evidence files behind Module 18 (`research/sota_partA.md`, `sota_partB.md`). They quote the papers at length, and those passages belong to the publishers.

If you find an error, it is most likely in a statement about a paper that could not be read. Check the paper.
