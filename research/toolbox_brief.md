# Brief: write one background page of the course

## The readers

People who run molecular dynamics simulations and can read Python but are not physicists or mathematicians, for example a master's student in biology whose last calculus course was years ago. Some read English as a second language. They asked for more explanation of the physics and mathematics for a non-expert, and for every letter in every formula to be defined.

The course has 18 lessons. Each lesson explains a new tool briefly where it needs it and links to a background page for the longer explanation. You write one of the two background pages:

- `src/modules/maths.md`: the maths toolbox
- `src/modules/physics.md`: the physics primer

`research/toolbox_anchors.md` lists the sections of both pages. The lessons link to exactly these anchors, so your page must contain every section listed for it, in that order, each with its anchor.

Read first: this brief, `research/toolbox_anchors.md`, `research/expand_brief.md` (the rules for the lessons: the style, syntax and symbol-list rules there apply to you too) and `src/modules/02-classical-mechanics.md` (the voice and level to match). To see where a tool is used, you may search the lessons in `research/modules_before_expand/` (do not read `src/modules/`: those files are being rewritten at this moment).

## The page

Front matter (no `num`):

    ---
    title: Maths toolbox            (or: Physics primer)
    short: Maths toolbox            (or: Physics primer)
    summary: one sentence saying what the page is and how to use it
    ---

Then a short introduction (how to use the page: read it once, or arrive from a lesson link and go back), a list of links to the sections, and the sections.

Each section is a level-2 heading with the anchor from the list, in this exact form:

    ## The gradient {#gradient}

Each section has, in this order:

1. **The idea in plain words**, with a picture from everyday life or from a molecule.
2. **The notation**: how it is written, how to read it aloud, each symbol defined. Every displayed formula is followed by a symbol list (`<div class="legend" markdown="1">`, see the lesson brief).
3. **One or two worked examples with numbers**, small enough to check by hand. Check every number by running it.
4. **Where the course uses it**: the lessons by number and name, one line each. The lessons are: 1 What MD is; 2 Classical mechanics; 3 Statistical mechanics; 4 Integrators; 5 The form of a force field; 6 Force-field parameters; 7 Boundaries and electrostatics; 8 Thermostats and barostats; 9 Constraints; 10 Running a simulation; 11 Analysis and statistics; 12 Free energy and the potential of mean force; 13 Alchemical free energy; 14 Enhanced sampling; 15 Coarse-grained models; 16 Kinetics and Markov state models; 17 Machine-learned potentials; 18 Machine-learning models trained on MD. Link as `[Module 4](04-integrators.html)`; the file names are those in `research/modules_before_expand/`.
5. **A common mistake**, where there is one worth naming.

Aim at 300 to 500 words per section, more only where the topic needs it (the derivative, probability, Fourier transforms; units, thermodynamics, electrostatics). Build each section on the ones before it and link back to them (`[the derivative](#derivative)`).

Rules:

- Only standard, textbook material. No history, no citations, no statements about papers or programs. Physical constants must be right: $k_B = 0.0083145$ kJ mol$^{-1}$ K$^{-1}$ $= 1.380649\times10^{-23}$ J/K, $N_A = 6.02214\times10^{23}$ mol$^{-1}$, $k_BT = 2.494$ kJ/mol $= 0.596$ kcal/mol at 300 K, 1 kcal $= 4.184$ kJ, 1 u $= 1.66054\times10^{-27}$ kg, $e = 1.602177\times10^{-19}$ C, $1/(4\pi\epsilon_0) = 138.935$ kJ mol$^{-1}$ nm $e^{-2}$, 1 kJ/mol $= 1$ u nm$^2$ ps$^{-2}$, 1 bar $= 10^5$ Pa.
- You are responsible for the correctness of everything. Derive, compute, check units. If you are unsure of a statement, leave it out.
- Tables are welcome for rules (derivative rules, unit conversions, the Greek alphabet).
- No images. Describe a picture in words when you need one.
- Follow the style and syntax sections of `research/expand_brief.md`.

## How to work

1. Write the page with the Write tool. It is long: write it in several passes (Write the first part, then Edit to append).
2. Check it and repeat until there is no `FAIL`; read every `WARN`:

        wsl -e bash -lc "cd '<course folder>' && python3 research/check_module.py maths.md"

   Python for arithmetic: `wsl -e bash -lc "python3 -c 'print(8.3145e-3*300)'"`.
3. Write `research/expand_notes/maths.md` (or `physics.md`): anything you were unsure of and left out, and anything a reviewer should check first.
4. Finish with a report of at most six lines.

## Limits

- Edit only your page and your notes file. Do not run `src/build.py`, do not start a server or a browser, do not use the web.
- Never put an e-mail address, a name or any other personal detail of the reader in any file or request.
