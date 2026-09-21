# Codex installation and verification

Atelier supports Codex CLI/app 0.155.1 or newer, plus Claude Code, from the
same repository. Codex uses the current selected model for every Atelier role;
Claude keeps the model pins declared in `agents/`.

## Install from this repository

Requirements: Python 3.10+ available as `python`, Node.js/npm for the optional
registry MCPs, and Codex with plugin commands enabled.

```text
codex plugin marketplace add INERATE/atelier
codex plugin add atelier@atelier-codex
```

For a local checkout, stage a runtime-only marketplace first. This prevents
development dependencies and browser reports from entering Codex's cache:

```text
python scripts/stage_codex_plugin.py
codex plugin marketplace add ./dist/codex-marketplace
codex plugin add atelier@atelier-codex
```

After installation, restart Codex and open a new thread. Run `/hooks`, inspect
Atelier's two hook definitions, and trust their current hashes. Installation
does not grant hook trust automatically.

Start in the target project:

```text
$atelier-bootstrap
$atelier-plan Describe what you want to build
```

The full workflow is available as `$atelier-bootstrap`, `plan`, `clarify`,
`build`, `review`, `learn`, `promote`, `ship`, `status`, `doctor`, and `update`,
each prefixed with `atelier-`.

## Local author loop

After modifying the checkout, rebuild the clean marketplace and reinstall:

```text
python scripts/stage_codex_plugin.py
codex plugin marketplace upgrade atelier-codex
codex plugin add atelier@atelier-codex
```

Start a new thread so Codex loads the updated skills and tools. If a hook
changed, review its new hash through `/hooks`.

## Verification

Run the deterministic suite before installation:

```text
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/check_package.py
python scripts/validate_skills.py
python scripts/size_audit.py .
npm ci
npx playwright install chromium
npm run audit:site
```

The browser audit uses the included reference page by default. Set
`ATELIER_SITE_URL` to an absolute URL to inspect a running generated site.

`python scripts/mcp_smoke.py .` is an optional network test that downloads and
initializes all four registry servers. Its failure indicates an optional
integration gap; core Atelier workflows still work.

For host delivery, create a temporary project, invoke `$atelier-bootstrap`,
then verify `$atelier-status`. Apply an oversized Python edit and confirm the
post-edit hook returns corrective feedback. Start a new thread and confirm the
session hook restores the active plan. Script self-checks alone do not prove
that installed hooks are trusted or firing.

The compatibility matrix is exercised in CI on Windows, Ubuntu, and macOS with
Python 3.12. Live host delivery remains a release smoke test because it depends
on an installed interactive Codex session.
