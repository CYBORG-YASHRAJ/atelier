# Promote

List unpromoted design_guide_versions overlays. Resolve the requested overlay or latest candidate, read its content, and present the exact promotion. Honor existing explicit promotion authorization; ask for confirmation if the choice/content has not been approved.

Validate that the source is inside PROJECT/workspace/overlays and the destination stays inside PROJECT/docs/design. Do not overwrite a conflicting destination. Copy needed reference assets into docs/design/assets and adjust relative links.

Write the promoted document and verify it, then transactionally update the pointer, promoted flag and matching overlay rule sources. Remove the old overlay only after the new file and database update succeed. If an operation fails, keep the recoverable source and report the state.

Never change the installed design-law. Report paths and diff; staging/committing requires its own user instruction.
