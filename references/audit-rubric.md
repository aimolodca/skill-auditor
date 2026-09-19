# Audit Rubric

Use every applicable dimension. Mark each `pass`, `attention`, `fail`, or `not applicable`; cite the file or section that supports the judgment. Do not calculate a vanity total.

## 1. Scope and routing

- Does the description say what the skill does and when it should trigger?
- Does it avoid catch-all wording that attracts unrelated tasks?
- Are near-miss requests excluded when confusion with sibling skills is likely?
- Could the description survive truncation without losing its primary trigger?

## 2. Capability delta

- What does the skill add that a capable base model would not reliably do unaided?
- Are generic writing, reasoning, or planning reminders consuming context without changing decisions?
- Is each strong opinion tied to domain knowledge, an observed failure, or a real contract?

## 3. Behavioral contract

- Are intended outputs, completion evidence, and stopping conditions explicit?
- Are user choices, domain rules, exact formats, and non-obvious invariants identifiable?
- Does the skill finish the requested work instead of stopping at an unnecessary review checkpoint?

## 4. Instruction economy

- Is the same idea explained multiple times?
- Are examples longer than the distinction they teach?
- Can repeated deterministic logic become a script?
- Are historical explanations, setup notes, or maintenance commentary loaded during ordinary use?

## 5. Progressive disclosure

- Does `SKILL.md` contain only shared workflow, routing, and essential constraints?
- Does each reference have a clear read condition?
- Are references split by loading condition rather than arbitrary file size?
- Are assets kept out of instructional context?

## 6. Duplication and contradiction

- Do body sections, references, scripts, tool descriptions, or sibling skills restate the same rule?
- Do absolute words such as `always`, `never`, and `must` collide?
- Do examples contradict the formal workflow or output contract?
- Is a rule repeated because one copy is compensating for poor routing?

## 7. Degrees of freedom

- Are open-ended judgments expressed as outcomes and criteria?
- Are exact steps reserved for fragile, destructive, or contract-bound operations?
- Does over-prescription prevent the model from using current capabilities?
- Does under-specification leave a real failure mode unguarded?

## 8. Authorization and safety

- Are external writes, sending, spending, deletion, publication, and production changes correctly scoped?
- Are safe read-only or reversible loops permitted clearly enough to avoid needless pauses?
- Are destructive targets resolved before action?
- Would removing a duplicated safety rule make the skill unsafe on another host?

## 9. Resource architecture

- Are every referenced file and executable present?
- Are important files discoverable from `SKILL.md`?
- Are there orphaned references, placeholder files, stale assets, or untested scripts?
- Does an implementation or schema provide a better contract than prose?

## 10. Executability and validation

- Can another agent follow the workflow with the named tools and paths?
- Are scripts portable or are prerequisites stated?
- Do validators test only syntax, or is behavioral quality also checked?
- Are failure messages and recovery paths actionable?

## 11. Evidence and evaluation

- Are routing positives and near-misses tested separately?
- Are core, edge, safety, and completion scenarios represented?
- Are assertions observable rather than based on preferred wording?
- Has a suspected dead rule been ablated before removal when the risk is material?

## Severity

- **Critical**: unsafe action, lost authorization boundary, broken dependency, or behavior that prevents task completion.
- **High**: likely misrouting, contradiction, or loss of a core capability.
- **Medium**: recurring context waste, ambiguity, or brittle workflow.
- **Low**: localized clarity, naming, or maintenance issue with little behavioral impact.

For each finding record: `severity`, `dimension`, `evidence`, `consequence`, `recommended action`, and `confidence`.

