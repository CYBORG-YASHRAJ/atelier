# Build

1. Resolve the selected plan with db/plan.py [ID]. Read its body and criteria. No plan means plan first; multiple active plans require selection.
2. Load loop-engine and the builder role. Work task-by-task against that contract. If architecture is invalid, return to the architect role and explain the necessary revision.
3. Load clean-code-law and structure-law for implementation; gateway and design-law for UI; auth-law/security-law when applicable. For UI research, use design-scout where available and permitted, otherwise do that research sequentially before final polish.
4. After each task run meaningful checks and the explicit size audit: python "<PLUGIN>/scripts/size_audit.py" "<PROJECT>". Have the parent record evidence only for verified criteria on this plan. Subagents return results instead of racing database updates.
5. Re-read remaining criteria for the selected plan. Continue within user scope and permissions; stop with a clear blocker when progress needs missing input or capabilities. Manual criteria need explicit user confirmation.
6. Return verified outcomes and remaining work. Do not claim completion while criteria remain unmet.
