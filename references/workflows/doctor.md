# Doctor

Probe dependencies and report version/availability. Open the store read-only and run PRAGMA integrity_check; expect meta.schema_version = 1. Do not initialize or overwrite a missing, corrupt or incompatible database.

Check exposed registry MCPs with a real request, and graph freshness if available. Record capabilities only when health-check maintenance is authorized; do not auto-install missing packages.

Run both hook scripts with --test. Separately inspect host hook discovery/trust and actual delivery. A script test alone is not proof that hooks fire. On Codex, instruct /hooks review if needed; never bypass trust.

Report each result with a concrete next step. The host integration smoke tests in docs/CODEX.md demonstrate patch feedback and session recovery. Repair only problems within existing authorization; database recovery requires an explicit recovery choice.
