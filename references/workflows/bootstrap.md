# Bootstrap

Set up Atelier in PROJECT using the runtime contract.

1. Probe python, node, git, docker, ffmpeg, pnpm and uv with version commands. Missing optional tools do not block the core workflow; missing Python blocks scripts.
2. Run python "<PLUGIN>/db/store.py" init. Add workspace/ to the project's .gitignore if absent, preserving existing entries. Record capability names, availability and versions through parameterized writes.
3. Check whether shadcn, magicui, aceternityui and reactbits tools are exposed and respond. Missing or failed servers remain capability gaps. Consult registry entries for alternatives; never report a configured server as healthy without a response.
4. Offer optional companion setup only if useful for the requested project. Use the host's supported installation tools and existing authorization; do not issue Claude commands on Codex.
5. Detect Google environment credentials without displaying values. If absent, explain the public API environment-variable or Vertex credential-file options and the no-credentials paste-prompt fallback. Skipping credentials is a supported outcome.
6. Report store location, tool/companion availability, credential mode, and hook status. On Codex direct the user to /hooks for any required trust review.
7. Recommend Atelier plan as the next workflow.
