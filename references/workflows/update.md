# Update

Use the current host's plugin update/install mechanism. On Codex refresh the configured atelier-codex marketplace and reinstall atelier from that source; see docs/CODEX.md. On Claude use its plugin update mechanism. Never git pull an installed cache or edit its core.

After the updated plugin is loaded in a new thread, inspect schema/version and run db/store.py init to refresh core defaults. Initialization refuses incompatible schemas; it is not a general migration engine.

Compare before/after core counts and run doctor. Preserve plans, criteria, clarifications, learned registry rows, overlays and references. Record any missing capabilities without calling them healthy. Do not touch user files to force compatibility.
