---
name: loop-engine
description: The Atelier operating loop — understand → clarify → plan → execute → review → compare-vs-done-state. Governs when to stop, when to ask, which model tier runs each phase, and when to think deep or compact. Load for ANY nontrivial task.
---

# Loop Engine

**Step 0 — before anything: adopt the principal-mind skill.** It sets how you
decide (no hedging), debug (root cause), secure (reflexes), and speak
(outcome-first). Every phase below runs inside that mindset, on every model tier.

Every task is recursion with a base case: `if (done) return;`. You may not claim
"done" while any done-criterion is unmet.

## The loop

```
Understand → Clarify → Plan → Execute → Review → Compare vs Done-State
     ▲                                                    │
     └────────────── criteria unmet? loop ────────────────┘
                     all criteria met? STOP
```

## 1. Understand (always first, never skipped)

Read BEFORE asking: the repo, applicable host instructions (AGENTS.md on Codex, CLAUDE.md on Claude), `workspace/project.md`, the store
(`python <plugin>/db/store.py rules <domain>`), code-review-graph if present, and
the web when facts are missing. **Don't hunt for framework files — query the
map:** `python <plugin>/db/store.py map <topic>` returns exactly which
skill/tool/agent to load for a topic (one query instead of directory reads). Then write down: assumptions (things you'll take
as true) and unknowns (things only the user can settle).

## 2. Clarify (once, batched, only unknowns)

Ask **only** questions that change what you build — stack choice, auth mode,
repo layout, product intent. Never re-ask what intake already answered
(`clarifications` table). One batch, not a drip. If a default is industrial
standard, state it and proceed unless overridden.

## 3. Plan (architect tier)

Complex/ambiguous/architectural work → the **architect** role produces:
the plan, the file map, risks, and a **done-state contract** — concrete,
checkable criteria written to `plans` + `done_criteria`. Planning respects the host's configured reasoning settings. The architect NEVER writes
production code.

## 4. Execute (builder tier)

The **builder** role implements plan tasks one at a time, obeying
design-law, clean-code-law, structure-law, auth-law, security-law. Independent
small tasks may fan out to parallel builders. Trivial mechanical edits and
digests go to the **summarizer** role.

## Host routing

Read [the runtime contract](../../references/runtime.md). Claude agent wrappers retain their model pins. Codex uses the selected model for architect, builder, summarizer, learner and design-scout responsibilities, delegating only where supported and permitted; otherwise run sequentially. The parent coordinates state writes. Never change the user's model configuration.

## 5. Review (gates, not opinions)

Atelier review: ponytail pass, code-review-graph impact, lint/typecheck,
file-size law, design-token compliance for UI, a11y/perf where relevant. Update
`done_criteria.passed` with evidence.

## 6. Compare & terminate

`SELECT criterion FROM done_criteria WHERE plan_id=? AND passed=0`. Rows remain →
loop (fix, don't restart). Zero rows → report done, with evidence. A `manual`
criterion passes only when the user says so — log their words as evidence.

## Session hygiene

- Use the host's configured model and reasoning effort.
- After a milestone or before a long build: use host compaction only when available and appropriate — persist state
  to the store first so nothing is lost (plans and criteria live in SQLite, not
  in chat history).
- Never poll anything, anywhere. Event-driven or one-shot timers only.
User instructions and host permissions take precedence. Unmet criteria prevent a completion claim, but do not authorize ignoring a stop or retrying an external blocker indefinitely.
