# Releasing & Updating

Both host manifests must announce the same version. Claude reads
`.claude-plugin/plugin.json`; Codex reads `.codex-plugin/plugin.json` and caches
the installed package. Commits without a synchronized bump may not reach users.

Before release, run `python scripts/stage_codex_plugin.py` and inspect the
staged plugin. It must not contain `.git`, `node_modules`, browser reports,
tests, or project workspace state.

## Owner / contributor — every release

1. Make the change. Code files stay ≤ 250 words (CI hard-caps at 350).
2. Seed discipline: `db/seed/seed.sql` builds defaults in a temporary database.
   `db/initialize.py` replaces core rules, adds missing registry/map rows, and
   refreshes only defaults whose previous snapshot remains unchanged.
3. New skill/tool/agent? Add its `framework_map` row in the seed, or agents
   can never find it (`store.py map <topic>` is how they discover pieces).
4. **Bump `version`** in both host manifests:
   patch = fix · minor = new skill/tool/command · major = breaking schema.
5. Commit `release: vX.Y.Z — what changed`, push to `main`, confirm CI green.
   That IS the release — no registry, no upload, no build.

Pre-push checks are documented in [CODEX.md](CODEX.md). CI runs regression,
package, skill, hook, word-budget, and Playwright checks.

## Users — getting updates

- Manual: `/plugin update atelier` (or `claude plugin update atelier`), then restart.
- Automatic: `/plugin` → Marketplaces → `atelier-marketplace` → **Enable
  auto-update** — third-party marketplaces are OFF by default; official
  Anthropic ones are ON.
- Then `/atelier:update` inside a project migrates its store.

Codex users upgrade the `atelier-codex` marketplace, reinstall
`atelier@atelier-codex`, restart in a new thread, then invoke
`$atelier-update`. Changed hooks require a new `/hooks` trust review.

## Agents — what /atelier:update guarantees

`store.py init` refreshes compatible schema-v1 defaults. It refuses unknown
schema versions and never touches `workspace/overlays/`, plans, criteria,
clarifications, or user-learned registry rows. Report version and core row
counts before and after.
