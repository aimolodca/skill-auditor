# Optimization Workflow

Optimize from a protected behavioral contract, not from line count alone.

## 1. Establish the baseline

Run the inventory and record:

- discovery, triggered, and on-demand token estimates;
- file graph and unreferenced resources;
- exact duplicate blocks and repeated absolute rules;
- the current description and invocation policy;
- available validators, scripts, and behavioral examples.

Keep an untouched original outside the edited directory or rely on version control. Do not overwrite the only copy.

## 2. Freeze protected behavior

Write a concise list of invariants that must survive:

- positive and negative trigger boundaries;
- required outputs and completion evidence;
- user-selected voice, process, tools, and formats;
- permissions, confirmation gates, and destructive-action protections;
- domain facts, schemas, assets, and observed-failure gotchas;
- fallback and recovery behavior.

If an invariant is unclear and materially changes the result, ask rather than silently deciding.

## 3. Classify content

Use one action per block:

| Action | Use when |
|---|---|
| Keep | It changes decisions or protects a real invariant. |
| Merge | Several passages express one rule. |
| Move | The content is needed only in a particular mode or edge case. |
| Rewrite | The intent matters but the current wording is vague, brittle, or over-prescriptive. |
| Cut | The content is obvious, duplicated, stale, or has no observable effect. |
| Retire | A file, mode, or entire skill adds no distinct capability and has no active consumer. |

Do not label content `cut` without saying why behavior should remain unchanged.

## 4. Apply reductions in a safe order

1. Remove placeholders, stale maintenance notes, and unused files.
2. Merge exact repetition and choose one authoritative location.
3. Move conditional procedures and substantial examples into directly linked references.
4. Replace repeated deterministic prose with a tested script when portability permits.
5. Tighten the description after defining positive and near-miss triggers.
6. Convert generic process coaching into outcome criteria or remove it.
7. Reconsider absolute rules; retain them for safety, permissions, exact contracts, and demonstrated failures.

Do not move every paragraph into references. A reference read on every invocation has only relocated the cost.

## 5. Validate the candidate

- Run the host's structural validator.
- Run every added or changed script.
- Re-run the inventory with `--compare`.
- Check all links and required files.
- Use [evaluation.md](evaluation.md) for behavioral comparison when changes are substantial.

## 6. Produce a change ledger

For each material change record:

```text
Action: merge | move | rewrite | cut | retire
Source: file and section
Reason: evidence-backed explanation
Protected invariant: what must remain true
Validation: scenario or check that supports the change
```

Report token reduction by loading tier. Never present estimated tokens as billing data or guaranteed runtime savings.

