# Brief: rewrite one lesson so that it teaches on its own

## The readers and the complaint

People who run molecular dynamics simulations and can read Python but are not physicists or mathematicians, for example a master's student in biology whose last calculus course was years ago. Some read English as a second language. Readers of the first published lessons reported three things:

1. The text is not informative enough without the videos. It cannot explain everything on its own.
2. More explanation of the physics and the mathematics is needed, for a non-expert, whenever something new appears.
3. Every letter in every formula should be defined, because a formula is of no use to a reader who is not sure what each symbol stands for.

The present lessons are correct but compressed. They read like a summary for someone who already knows the subject. Your job is to rewrite ONE lesson file so that this reader can learn the topic from the text alone, with the videos as an optional extra.

## The pattern to follow

Module 2 has already been rewritten. Before you write anything, read both versions side by side:

- new: `src/modules/02-classical-mechanics.md`
- original: `research/modules_before_expand/02-classical-mechanics.md`

Match its voice, its level and its devices. Then read `research/toolbox_anchors.md` (the background pages you can link to) and your own module.

## What to add

1. **A plain-words opening for every section.** Before any formula: what question does this section answer, why does a simulation need it, and the smallest picture or example that carries the idea. One analogy per idea at most, and short. If the analogy breaks down somewhere that matters, say where.

2. **Every new physical idea explained from zero** at the place where it first appears in your module. "New" means any term a biology master's student would not be sure of: ensemble, partition function, degree of freedom, dielectric constant, dipole, virial, reciprocal space, detailed balance, collective variable, and so on. Do not assume the reader remembers an earlier module: if a term was introduced earlier, give a one-sentence reminder and the module number. For background that needs more than a few sentences, use a box:

        <div class="box physics" markdown="1">
        **Physics you need here: the dielectric constant.** ...
        </div>

   and link to the physics primer where a section fits, e.g. `[primer](physics.html#electrostatics)`.

3. **Every new mathematical tool explained from zero** in a box, with a tiny worked example (numbers or two lines of algebra), and a link to the maths toolbox:

        <div class="box maths" markdown="1">
        **Maths you need here: the Taylor expansion.** ...
        More in the [toolbox](maths.html#taylor).
        </div>

   Tools that need this include, when they occur: partial derivative, gradient, divergence, chain rule in several variables, integral over many variables, Taylor expansion, order-of-error notation, dot and cross product, matrix and eigenvalue, complex exponential, Fourier series and transform, differential equation, operator and its exponential, probability density, mean and variance, Gaussian integral, delta function, error function, Lagrange multiplier, Legendre transform, factorial and Stirling's formula, logarithm rules, least squares, random numbers. Explain a tool where it is first needed, not all at the top.

4. **A symbol list after every displayed formula.** Directly after the `$$ ... $$` block:

        <div class="legend" markdown="1">
        - $m_i$: the mass of atom $i$, in atomic mass units (u).
        - $\ddot{\mathbf r}_i$: the acceleration of atom $i$, the rate at which its velocity changes.
        </div>

   The page prints the heading "What each symbol means" above the list by itself, so do not write a title. Rules:
   - List every letter and sign in the formula: variables, constants, indices (say what they run over), Greek letters, operators ($\nabla$, $\partial$, $\sum$, $\int$, $\langle\ \rangle$), bars, brackets with a special meaning, and subscripts or superscripts that carry meaning.
   - Say what the thing *is* physically, not only its name. Give the unit and a typical size where that helps ("about 2.5 kJ/mol at 300 K").
   - When a letter has more than one meaning in the module, say which one is meant here.
   - One or two lines per item.
   - In a derivation where one formula follows directly from the one before, a later list may contain only the symbols that are new, followed by the item "Other symbols: as in the list above." Never leave a section that has a displayed formula without any list.
   - Formulas inside a `box maths`, a `box physics`, a worked-example box or an "Optional" `<details>` block do not need a list if the sentences around them define the symbols.
   - Symbols in formulas inside a sentence must be defined in that sentence or within the few sentences before it.

5. **Derivations with no missing steps.** Say what is done at each step and name the rule used (chain rule, integration by parts, "divide both sides by", "the terms cancel because"). Where the original jumps or says something follows, fill the gap if it takes up to about ten lines. A longer derivation that the reader can skip goes in

        <details markdown="1"><summary>Optional: where this formula comes from</summary>
        ...
        </details>

6. **"Read it like this" after each important formula.** What the formula says in words. What happens to the result when one of the symbols gets larger or smaller. A small numerical example with units when one is natural.

7. **Signposts.** At the top, a short section "The plan of this module" (what the module is for, its layers, in the manner of Module 2), and a small table "How to read the formulas" only for notation that first appears in your module, with a link to `maths.html#notation`. If letters have two meanings in your module, add a `box warn` that lists them. For a heavy section, say what is essential and what can be skipped on a first reading.

8. **The lectures become optional.** Replace the heading `## Watch first` by `## Lectures for this module` followed by exactly this paragraph, then the placeholder:

        The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

        {{WATCH}}

   Never send the reader to a video for an explanation.

## What must not change

The present text was checked sentence by sentence against 124 of the cited papers and by three referees. That work must not be lost.

- **Every factual statement, number, name, date, attribution and citation link in the present file must survive with its meaning unchanged.** The safest way is to keep the original sentences word for word and add around them, as Module 2 does. You may split a long sentence or add a definition in brackets. You may not change what a sentence claims, soften or strengthen it, or drop it.
- **Every displayed equation of the original stays exactly as written.** You may add new displayed equations (intermediate steps, simple cases).
- Keep unchanged: the front matter, the goal box, every `<div data-videos="..."></div>` line (same ids, directly under the same heading), every widget line, every `{{PLACEHOLDER}}`, every `[text](cite:key)` link, and every existing `##` heading with the same wording (page links depend on them). You may add new `##` or `###` headings. Do not add video lines, widgets or citation keys.
- Keep the "Check yourself" questions and the exercises. You may add definitions of symbols to an answer, and add up to three new "Check yourself" questions that test the basics you introduced.
- **Do not add facts about the literature from memory.** No new statements about who introduced what or when, what a paper showed, what a program does by default, benchmark numbers, or force-field parameter values. What you add is explanation: concepts, textbook physics and mathematics, and arithmetic you have checked. If an example needs a number that is not in the module, use a round value and label it as an illustration ("say, $k = 100$ kJ mol$^{-1}$ nm$^{-2}$"). Physical constants may be used; take care with them: $k_B = 0.0083145$ kJ mol$^{-1}$ K$^{-1}$, $k_BT = 2.494$ kJ/mol $= 0.596$ kcal/mol at 300 K, 1 kcal $= 4.184$ kJ, $1/(4\pi\epsilon_0) = 138.935$ kJ mol$^{-1}$ nm $e^{-2}$, 1 kJ/mol $= 1$ u nm$^2$ ps$^{-2}$.
- If you think a statement in the original is wrong or unclear, do not change it. Report it in your notes file.

## Correctness

You are responsible for every formula, definition and number you add. Derive each added formula yourself and check that it agrees with the original equations around it. Check every piece of arithmetic by running it (Python is available through the shell, see below). Check units. A wrong explanation is worse than no explanation: if you are not sure how to explain something correctly, say less and record it in your notes.

## Style

- Plain English, short sentences, active voice, "you". British spelling, as in the file.
- Say the thing directly. No scene-setting openers, no closing summaries that repeat the paragraph, no rhetorical questions in series, no praise of the topic.
- Do not use: "simply", "just", "obviously", "clearly", "it is easy to see", "of course", "note that" as filler, "dive", "delve", "crucial", "key insight", "powerful", "elegant", "landscape" as a metaphor for a field (an energy landscape is fine).
- No em dashes. Use a full stop, a comma or brackets.
- Avoid the pattern "not X, but Y" when "Y" alone says it.
- Paragraphs of five sentences at most.
- Keep the level steady: do not explain one thing for a child and the next for an expert.
- Length: Module 2 grew to about four times its original length, most of it symbol lists and maths boxes. Expect between 2.5 and 4 times for your module. Do not pad to reach a length and do not cut explanation to stay under one.

## Syntax the build depends on

- Inline maths `$...$` on one line: no line break inside, no space directly after the opening `$` or before the closing `$`, and the closing `$` must not be followed directly by a digit. Displayed maths as `$$` on its own line, the formula, `$$` on its own line, with a blank line before and after.
- KaTeX renders the maths. Use only standard commands. `\dddot` does not exist. Use `\text{...}` for words inside maths. `aligned` works inside `$$`.
- Never put a `[..](cite:..)` link inside maths.
- A `|` inside maths in a table breaks the table: write `\vert` or `\mid`.
- Blocks `<div class="..." markdown="1">` and `<details markdown="1">` start at the beginning of a line, with a blank line before the opening tag and after the closing tag. The closing `</div>` is on its own line.
- A list needs a blank line before it (except directly after the opening tag of a legend or box).
- A literal dollar sign is written `\$`.
- Links to other lessons: `[Module 4](04-integrators.html)`. Links to the background pages only as listed in `research/toolbox_anchors.md`.
- Code blocks keep their ``` fences and language tag.

## How to work

1. Read this brief, the two versions of Module 2, `research/toolbox_anchors.md` and your module (the copy in `src/modules/`; an identical backup is in `research/modules_before_expand/`).
2. Write the new lesson to the same path in `src/modules/` with the Write tool (the file is long: you may write it in two or three passes, first Write, then Edit to append).
3. Run the checker and repeat until there is no `FAIL`. Read every `WARN` and fix those that point to a real problem:

        wsl -e bash -lc "cd '<course folder>' && python3 research/check_module.py YOUR-FILE.md"

   The same shell runs Python for arithmetic: `wsl -e bash -lc "python3 -c 'print(2.494/4.184)'"`.
4. Write `research/expand_notes/YOUR-STEM.md` with: the maths and physics boxes you added; the terms you defined; toolbox anchors you linked to and anchors you would have liked to exist; statements of the original you doubt (quote them); anything you chose not to explain because you were not sure; WARN lines you left and why.
5. Finish with a report of at most eight lines: word count before and after, number of symbol lists and boxes, what a reviewer should look at first.

## Limits

- Edit only your module file and your notes file. Other agents are rewriting the other modules at the same time.
- Do not run `src/build.py`, do not start a server or a browser, and do not use the web.
- Never put an e-mail address, a name or any other personal detail of the reader in any file or request.
