# Evaluation and Comparison

Measure behavior, routing, and context separately. A smaller skill is not better if it routes incorrectly or loses a critical invariant.

## Scenario set

Create the smallest set that covers the actual contract:

1. **Core task**: the common request the skill exists to solve.
2. **Edge task**: a difficult but supported variation.
3. **Completion task**: verifies the workflow reaches the requested finished state.
4. **Safety task**: exercises an authorization or destructive-action gate when applicable.
5. **Positive routing prompt**: should invoke the skill.
6. **Near-miss routing prompt**: resembles the domain but should not invoke it.

Add scenarios only for distinct risks. Do not inflate the set with paraphrases.

## Assertions

Judge observable outcomes such as:

- required artifact or fields are present;
- exact format or schema is valid;
- prohibited side effect did not occur;
- the task completed without an unnecessary stop;
- the correct reference or tool was selected;
- the skill did or did not trigger for the intended prompt.

Avoid assertions about headings, preferred phrasing, or hidden reasoning unless wording itself is the deliverable.

## Comparison procedure

1. Freeze the same task-local inputs for original and candidate.
2. Run them in fresh, isolated sessions when the environment supports it.
3. Do not reveal the expected answer, suspected defect, or candidate changes to the evaluator.
4. Compare original, candidate, and—when useful—no-skill baseline.
5. Record pass/fail per assertion, significant qualitative differences, model/effort, and tool availability.
6. Restore or revise any change that causes a material regression.

Use independent agents only when delegation is available and authorized. Keep tests read-only or isolated unless the user approved live effects.

## Ablation

For a rule suspected to be dead weight:

1. Remove only that rule in an isolated candidate.
2. Run the scenarios most likely to depend on it.
3. Keep the deletion only if no relevant behavior regresses.
4. If the outcome is inconclusive, retain or rewrite the rule and record the uncertainty.

## Comparison output

| Scenario | Original | Candidate | No skill | Decision |
|---|---|---|---|---|
| Core task | pass/fail | pass/fail | optional | keep/revise |

Alongside the table, report before/after loading-tier estimates and any untested risks. Do not collapse behavior and token savings into one score.

