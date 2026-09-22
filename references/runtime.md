# Atelier host contract

Read this once per workflow. User instructions, repository instructions and host permissions take precedence over Atelier defaults. Only perform the workflow the user requested.

## Paths and execution

PLUGIN is the installed plugin root, derived from the current skill file (two parent directories) or Claude's supplied plugin root. Resolve every plugin-relative path against PLUGIN, never against the project. Read scripts and references from the installed copy; never modify that copy.

PROJECT is the target project directory selected by the user, normally the host working directory. Run Python commands with PROJECT as their working directory, quoting absolute script paths for the actual shell. Require Python 3.10+ available as python. Use argument arrays where available; do not interpolate user text into shell commands or SQL.

The shared database resolver honors ATELIER_DB (relative to PROJECT or absolute), otherwise PROJECT/workspace/atelier.db. Overlays and references remain under PROJECT/workspace; promoted design lives under PROJECT/docs/design. A relocated database does not relocate project files.

Use python "<PLUGIN>/db/store.py" for rules, registry, map and read-only sql queries. Use python "<PLUGIN>/db/plan.py" [ID] for active-plan selection and criteria. Zero active plans means run plan; multiple active plans require an ID. All criterion queries/updates must include the selected plan_id. Use parameterized sqlite3 operations for user-provided text; never concatenate it into SQL. Parent agent owns durable plan/evidence writes.

## Host adapters

- Codex: invoke $atelier-<workflow>, use applicable AGENTS.md instructions, inherit the user's current model and effort settings. Do not edit global model configuration or assume Claude agent Markdown registers Codex agents.
- Claude Code: invoke /atelier:<workflow>, read applicable CLAUDE.md instructions. The agents/ wrappers retain their model pins.
- Shared role instructions live in references/roles/<role>.md. Read the role before using it. On Codex, delegate bounded independent work only when the host exposes and permits delegation; supply the role, project/plugin paths, selected plan ID and task. Otherwise perform the roles sequentially. Read-only scouts return findings before final polish; parent records accepted lessons.
- Do not force model changes, compaction, or continued execution against a user stop. Persist progress at task boundaries. When checks cannot run, report the unmet criterion and concrete blocker instead of looping indefinitely.
- In a host's read-only Plan mode, draft the plan in the conversation; defer database/project writes until execution is allowed.

## Capabilities and credentials

Discover actual tools before calling them. The four registry MCPs are optional enhancements. Missing ponytail means apply the local minimalism checklist; missing graph means inspect references and tests with repository search. Report these substitutions; never claim an unavailable external check ran.

Use the host's MCP installation mechanism only for requested integrations. Credentials come from the process environment or a user-configured credential-file path. Never request secret values in chat, print them, or store them in SQLite. A project .env file is not automatically loaded by Python or MCP servers: explain how to supply variables through the host/terminal. Keep any existing credential files gitignored.

Plugin startup hooks require Python on PATH. Codex requires review of installed hooks through /hooks. A successful script self-test does not prove hook trust or delivery; doctor reports these separately.
