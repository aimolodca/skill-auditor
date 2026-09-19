---
name: skill-auditor
description: Audit, simplify, and optimize Agent Skills without losing intended behavior. Use when asked to review a SKILL.md, reduce token or context cost, find duplicates or contradictions, improve triggering and progressive disclosure, compare an original skill with a revised version, or regression-test a skill rewrite. Do not use for ordinary skill creation unless audit or optimization is part of the request.
---

# Skill Auditor

Audit skills by evidence, optimize only what is unnecessary, and preserve the behavior that makes the skill worth invoking.

## Choose a Mode

- **Audit**: inspect and report without editing. Read [references/audit-rubric.md](references/audit-rubric.md).
- **Optimize**: audit, establish protected behavior, then revise. Read [references/optimization-workflow.md](references/optimization-workflow.md).
- **Compare**: measure original versus candidate and test for regressions. Read [references/evaluation.md](references/evaluation.md).
- **Collection audit**: audit several skills, then identify shared duplication, routing collisions, and candidates to merge or retire. Read the audit rubric and optimization workflow.

If the request is ambiguous, default to **Audit**. Never edit a skill merely because it was supplied for review.

## Operating Contract

1. Resolve the skill directory and inspect `SKILL.md`, linked references, scripts, assets, and UI metadata. Do not read unrelated repositories or user files.
2. Run the deterministic inventory when scripts are available:

   ```bash
   python3 scripts/audit_skill.py <skill-directory>
   ```

   Treat token counts as estimates unless the output names a real tokenizer. Automated duplicate findings are candidates, not semantic conclusions.
3. Identify the skill's behavioral contract before recommending cuts: intended triggers, outputs, non-obvious knowledge, authorization boundaries, safety gates, tool dependencies, exact formats, completion state, and observed-failure protections.
4. Separate findings into **keep**, **merge**, **move**, **rewrite**, **cut**, and **retire**. Attach file evidence and a concrete consequence to every material finding.
5. Prefer the smallest change supported by evidence. Do not chase an arbitrary reduction percentage.
6. Preserve user-authored intent and portable protections. Never remove a gate merely because the current host also enforces it; first determine whether the skill targets other hosts.
7. For optimization, show or record a change ledger and validate the edited directory. For substantial changes, compare realistic scenarios before declaring success.
8. Report uncertainty plainly. Do not claim a rule is dead weight, a trigger works, or behavior is preserved without a relevant check.

## Loading and Cost Model

Distinguish three costs:

- **Discovery cost**: name and description exposed before invocation.
- **Triggered cost**: the `SKILL.md` body loaded when invoked.
- **On-demand cost**: references read only for the active mode; scripts and assets usually need not enter context.

Optimize the tier that causes the real cost. Moving text from `SKILL.md` to a reference helps only when the reference has a clear read condition and is not loaded every time.

## Required Output

Lead with the verdict, then provide:

1. **Measured footprint**: discovery, triggered, and on-demand estimates; before/after delta when applicable.
2. **Behavioral contract**: what must survive.
3. **Findings**: severity, evidence, consequence, and action.
4. **Change ledger**: keep/merge/move/rewrite/cut/retire.
5. **Validation**: structural checks and behavioral scenarios actually run.
6. **Risks and unknowns**: anything not tested or dependent on a specific host/model.

Do not hide important findings behind a single score. A compact table is preferred when several exact mappings or comparisons are present.

## Resources

- `scripts/audit_skill.py`: deterministic inventory, loading-tier estimates, exact duplicate detection, link checks, and before/after comparison.
- [references/audit-rubric.md](references/audit-rubric.md): eleven-dimension semantic audit.
- [references/optimization-workflow.md](references/optimization-workflow.md): safe reduction and rewrite procedure.
- [references/evaluation.md](references/evaluation.md): routing, regression, and ablation testing.

## Attribution

Version 0.5  
Author: Alexander Dobrokotov — https://t.me/strangedalle

