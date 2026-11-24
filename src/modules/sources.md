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

**2. The cited papers, read in full.** Of the 144 papers in the main reference list, 124 were obtained legally and read: 119 from first line to last and 5 in part (long reviews, a long software paper, and papers of which a section or the equations could not be read). They came from three sources. Fifty are open-access articles, PubMed Central full text or arXiv preprints that a program can fetch. Eight are free on PubMed Central but only in a browser, two of them (Gilson et al. 1997 and Huber and Kim 1996) as scanned page images. Sixty-six are publisher PDFs obtained through a university library subscription. For those, the equations, tables and numbers the course depends on were checked on images of the printed pages, because the text layer of a PDF garbles them. Against the 124 papers, **1,202 statements of the course were checked: 2 were wrong and 227 imprecise**, and the substantive ones were corrected. The two wrong ones:

| Where | What the course said | What the paper says |
|---|---|---|
| Module 6 | ff19SB was fitted with OPC water | It was fitted to quantum-mechanical energy surfaces in implicit solvent; OPC is only recommended with it (Tian et al. 2020) |
| Module 6 | CHARMM36m re-fitted selected Lennard-Jones pairs and the water model | It changed the backbone CMAP term and one pair-specific term, and kept CHARMM-modified TIP3P (Huang et al. 2017) |

The 66 library papers are mostly the original papers of the methods the course derives: Verlet, velocity Verlet, RESPA, SHAKE, RATTLE, LINCS, the Andersen, Berendsen, Nosé, Hoover and Parrinello-Rahman schemes, Nosé-Hoover chains, particle-mesh Ewald, thermodynamic integration, free-energy perturbation, the Bennett acceptance ratio, umbrella sampling, the Boresch restraints, replica exchange, generalised Born, and Kramers theory in the review of Hänggi, Talkner and Borkovec. Every equation of the course that comes from one of them was compared with the printed equation term by term, and none had to be changed. What changed were statements about the papers: who introduced what, what a paper actually showed, and numbers quoted from memory. Some examples:

| Where | What the course said | What the paper says |
|---|---|---|
| Module 12 | Umbrella sampling with a spring along a coordinate, attributed to Torrie and Valleau (1977) | They introduced non-Boltzmann sampling with exact reweighting for Monte Carlo free-energy differences; the spring along a coordinate came later |
| Module 7 | The PME of Darden et al. (1993) described with B-splines | The 1993 paper interpolated with Lagrange polynomials; B-splines are from Essmann et al. (1995) |
| Module 8 | Andersen's piston presented as a constant-temperature and pressure method | On its own it gives constant enthalpy; NPT needs his stochastic collisions as well |
| Module 14 | Replica-exchange acceptance of "about 30 %" | The original simulation had about 15 %; 20 to 30 % is later practice |
| Module 16 | Levelling-off of implied time scales presented as validation of a Markov model | It guides the choice of lag time; the Chapman-Kolmogorov test validates (Prinz et al. 2011) |
| Module 1 | The first protein simulation (1977) was "in vacuum" | Four buried water molecules were included |

In the reference lists, a paper that was read carries the label <span class="tag read">read in full</span> or <span class="tag read">read in part</span>, with a line on what it is for and what to read in it.

**What this does not cover.** Twenty papers could not be read. Eleven are in American Chemical Society journals, whose site stopped serving files after the first dozen (it limits how many articles one reader may fetch in a short time): the Martini papers, force matching (Izvekov and Voth 2005), GROMACS 4, g_wham, Lennard-Jones PME, hydrogen mass repartitioning, TIP4P-D, FEP+ and the Markov-model review of Husic and Pande. Three are in Science, which the library proxy does not cover (the Anton simulations and the published BioEmu paper, whose preprint was read for Module 18). For six the library has no online copy or the publisher page offered no file: Ewald (1921), Kramers (1940), Kumar et al. (1992, WHAM), Miyamoto and Kollman (1992, SETTLE), Izrailev et al. (1999) and Dror et al. (2012). For these 20 only the bibliographic details were verified, and what the lessons say about them rests on textbook knowledge and on the referees' checks. Where a text was read as a preprint, the published article may differ.

**Module 18** was written the other way round: from evidence files built by reading the literature first, with a page reference for every number.

## The rewrite that made the lessons self-contained

The first published version was correct but compressed. A reader reported three things: the lessons could not be followed without the videos, new physics and mathematics were not explained for someone who is not a physicist, and the letters in the formulas were not defined. In November 2026 all 18 lessons were rewritten to answer this, and three pages were added (the maths toolbox, the physics primer and the list of symbols).

**What was added.** Each section now opens in plain words. Every new idea from physics or mathematics is explained from the beginning where it is first needed, in a box of its own with a small worked example. Derivations give every step. Under every displayed formula a list says what each letter and sign means: {{N_SYMBOLS}} definitions in the 18 lessons. The lessons grew to between five and eight times their first length.

**How the checked text was protected.** The writers were told to keep every checked statement and to add around it. A program then compared each rewritten lesson with its checked original: every original equation, number, citation link, heading and lecture link had to be present, and the original sentences that were no longer present word for word were listed for the referee. No writer was allowed to add a statement about a paper, a program or a model from memory.

**How the new text was checked.** Each rewritten lesson went to an independent referee that had not written it, and the two background pages and the formula sheet went to four more: 22 referees in all. Each referee re-derived every added formula, recomputed every added number (often with a short program or a small simulation), read every symbol list against its formula, and compared every added statement about a named method with the reading notes or the full text of the cited paper. The referee of Module 10 compared each explanation of a GROMACS or OpenMM option with the official documentation.

| | Wrong | Misleading | Missing | Unclear |
|---|---|---|---|---|
| 18 lessons | 32 | 141 | 123 | 115 |
| Maths toolbox and physics primer | 10 | 21 | 42 | 24 |
| Formula sheet | 2 | 5 | 17 | 12 |

"Missing" is mostly a symbol without a definition or a step without a reason. About 470 corrections were applied. The added derivations and numbers held up almost everywhere. The errors were in explanatory sentences and in incomplete symbol lists. Some examples of what was wrong in the new text:

| Where | What the new text said | Corrected to |
|---|---|---|
| Module 2 | The demo "compares forward Euler with a symplectic method" | That demo shows phase-space area with and without friction; the comparison is in Module 4 |
| Module 6 | "Each type of amino acid has its own correction map" (ff19SB) | The map depends on the type of amino acid; the paper has 16 maps for 20 amino acids |
| Module 8 | The coupling time of a Langevin thermostat is $1/\gamma$ | The kinetic energy relaxes with $1/(2\gamma)$, twice as fast |
| Module 11 | A bootstrap range from six values called a 95 % confidence interval | It holds the true mean about 87 % of the time; use the $t$ interval for few values |
| Module 12 | The error rule $k_BT/\sqrt n$ "holds for the joined profile" | It gives only the scatter from bin to bin; the errors of the window constants add up along the profile |
| Module 17 | The volume factor of a change of variables, inverted | The factor of the inverse map |

**Statements of the first version that this round corrected.** The referees also read the original text again, and in Module 18 against its evidence files:

| Where | What the published page said | Now |
|---|---|---|
| Module 18 | GPCRmd: 191 systems, 0.41 ms | 0.41 ms is the total of the 615 simulations on the platform |
| Module 18 | Removing the language model "costs about thirty times more", beside a gain of 0.07 in correlation | Thirty times in mean squared error, not in correlation |
| Module 18 | BioEmu finds 49 % of the open "apo" forms | "Open" is not in the source and was removed |
| Module 18 | "The headroom for learning is a few hundredths" | About a tenth (0.09 to 0.12) |
| Module 1 | The total energy wanders "because the force still has a small jump at the cutoff" | Mostly because of the time step: halving it made the wander nearly four times smaller in a test run |
| Module 16 | $k_BT/h = 6.2\times10^{12}$ s$^{-1}$ at 300 K | $6.25\times10^{12}$ s$^{-1}$ |

**What this does not cover.**

- The new explanations were written by an AI system and checked by other instances of an AI system. No human expert has read them.
- They are textbook material and were checked by derivation and computation, not against a textbook page by page.
- A few one-line definitions of named methods rest on general knowledge and not on a source read for this course: the ECC charge scaling, the linear interaction energy method, OPES, Gaussian accelerated MD, what DSSP does, the shadow contact map, and the columns that MDAnalysis returns.
- In Module 10 the input files `ions.mdp`, `nvt.mdp` and `npt.mdp` are new. Every setting was compared with the GROMACS documentation, but the files have not been run. The page says so next to them.
- The referees worked on the source text. That every formula displays correctly was tested separately, in a browser, for all pages.
- The length is deliberate. The cuts that the referees proposed were not made, because the reader asked for completeness.

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

In the repository: the referees' reports of the first version (`research/review_part1.md` to `review_part3.md`), the lists the pages are built from, the short annotation of each paper that was read (`research/paper_notes.json`), the lessons as they were before the rewrite (`research/modules_before_expand/`), and the rules and programs of the rewrite (`research/expand_brief.md`, `expand_review_brief.md`, `check_module.py`).

Kept offline with the course sources, not published: the full reading note for each paper (`research/paper_notes/`), the evidence files behind Module 18 (`research/sota_partA.md`, `sota_partB.md`), the referee reports of the rewrite (`research/expand_review/`), and the papers themselves. The notes and reports quote the papers, and those passages and files belong to the publishers.

If you find an error, it is most likely in a statement about a paper that could not be read. Check the paper.
