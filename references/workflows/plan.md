# Plan

Run project intake and create a checkable done-state contract.

1. Load the loop-engine skill. Read the project and prior clarifications before asking questions.
2. If workspace/project.md is absent, collect the project brief or missing decisions: audience, features, success criteria, stack, layout, auth, hosting and brand accent. Use existing answers. Save the brief and projects row when writes are allowed.
3. Use the architect role to propose architecture, milestones, risks and criteria tagged manual|test|lint|perf|a11y|design. Keep one criterion per independently verifiable outcome.
4. Persist the new plans row and its done_criteria in one transaction, using the inserted plan ID. Record the actual model only if known; otherwise leave it null. Do not deactivate another plan silently.
5. Persist answered clarifications linked to that plan. Return the plan ID, summary, contract, and next build task. In read-only Plan mode return the proposal and defer persistence.
