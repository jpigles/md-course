# Brief: referee one rewritten lesson

A self-study course on molecular dynamics was rewritten so that each lesson teaches on its own: plain-words explanations, every new piece of physics and mathematics explained from zero, a symbol list under every displayed formula, derivations with all steps. The original lessons had been checked sentence by sentence against the cited papers. The rewrite was done by another writer. You are the independent referee of ONE lesson. You did not write it. Assume nothing in the added text is right until you have checked it.

Working folder: the course folder

- rewritten lesson: `src/modules/<file>`
- checked original: `research/modules_before_expand/<file>`
- the rules the writer had: `research/expand_brief.md` (read it)
- original sentences that are no longer present word for word: `research/expand_notes/<stem>_changed_sentences.txt`
- the writer's own notes and doubts: `research/expand_notes/<stem>.md`

## What to check

**A. Nothing checked was lost or altered.** For every sentence in the changed-sentences file, find where its content went in the rewritten lesson and decide: kept with the same meaning, or meaning changed, weakened, strengthened or dropped. Then skim the two files side by side for facts, numbers, names, dates and attributions and confirm each survives. Any new statement about the literature, a program, a force field or a model that is not in the original is a problem (the writer was told to add none): list it.

**B. The added physics and mathematics are correct.** This is the main job. For every added explanation, formula, derivation step, worked example and analogy:
- re-derive each added formula yourself and check it against the original equations around it;
- recompute every number (Python is available: `wsl -e bash -lc "python3 -c '...'"`), check units and orders of magnitude;
- check that each definition is the standard one and is not subtly wrong (for example confusing a probability with a probability density, an angular frequency with a frequency, a force with an energy, kJ/mol with kcal/mol, sigma with r_min, Helmholtz with Gibbs);
- check that an analogy does not teach something false.

**C. The symbol lists.** For every displayed formula: is there a list (or does the brief exempt it), does it cover every letter and sign in the formula, and is each definition correct and the one that applies at that place? Report every symbol that is undefined, wrongly defined, or defined with the wrong unit. Also report symbols in in-sentence formulas that are never defined.

**D. Can the reader follow it?** The readers are not physicists (for example a master's student in biology), and some read English as a second language. Report places where a term is used before it is explained, a step is skipped, or the text falls back into expert shorthand. Report padding too: paragraphs that say nothing. Do not report matters of taste.

## What to deliver

1. `research/expand_review/<stem>.md`: your report, as a table with the columns: number, severity (`wrong`, `misleading`, `missing`, `unclear`), where (quote a few words so the place can be found), what is wrong, what it should say. Put `wrong` items first. End with one paragraph: your overall judgement of the lesson and what you could not check.

2. `research/expand_review/<stem>_fixes.txt`: corrections that can be applied mechanically, in this exact format, one block per correction:

        <file name, e.g. 03-statistical-mechanics.md>
        @@OLD
        <text exactly as it stands in the rewritten lesson, long enough to occur only once>
        @@NEW
        <the corrected text>
        @@END

   Rules for fixes: only for `wrong`, `misleading` and `missing` items (a missing symbol definition, a wrong number, a wrong statement, an altered fact restored to the original wording). Keep each one small. Never touch a sentence or equation that comes from the original except to restore it. Follow the syntax rules of `research/expand_brief.md`. Every new formula or number in a fix must be checked as strictly as the text you are reviewing. Do NOT edit the lesson file yourself.

3. A final message of at most eight lines: counts by severity, the three most serious findings, and whether the lesson is fit to publish once the fixes are applied.

## Limits

- Write only the two files above. Do not edit any lesson. Do not run `src/build.py`, do not start a server or browser, do not use the web.
- Never put an e-mail address, a name or any other personal detail in any file or request.
