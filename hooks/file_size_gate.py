#!/usr/bin/env python3
"""Atelier clean-code-law gate: source files stay <=250 words (350 hard cap).

PostToolUse hook on Write|Edit. Exit 2 feeds guidance back to the model.
ponytail: PostToolUse corrective (file already written); upgrade to PreToolUse
deny only if oversized files ever actually ship.
"""
import json, sys, os
from pathlib import Path
from patch_paths import affected

SOFT, HARD = 250, 350
EXEMPT_EXT = {".md", ".mdx", ".txt", ".json", ".yaml", ".yml", ".toml", ".lock",
              ".csv", ".svg", ".sql", ".html"}
EXEMPT_PARTS = ("node_modules", "migrations", "generated", ".min.", "dist", "build")


def check(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in EXEMPT_EXT or any(p in Path(path).parts for p in EXEMPT_PARTS) or ".min." in Path(path).name:
        return None
    try:
        words = len(Path(path).read_text(encoding="utf-8", errors="ignore").split())
    except OSError:
        return None
    if words > HARD:
        return (f"BLOCK: {path} is {words} words (hard cap {HARD}). Split it now: "
                "extract helpers to a sibling module / one component per file / "
                "split by responsibility. See clean-code-law.")
    if words > SOFT:
        return (f"warn: {path} is {words} words (budget {SOFT}, cap {HARD}). "
                "Split at the next natural seam.")
    return None


def main():
    try:
        data = json.load(sys.stdin)
        messages = [msg for path in affected(data) if (msg := check(path))]
    except (ValueError, TypeError, AttributeError, OSError):
        messages = ["Atelier: invalid hook payload; run the review size audit."]
    if messages:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": "\n".join(messages)}}))
    if any(msg.startswith("BLOCK") for msg in messages):
        print("\n".join(messages), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    if "--test" in sys.argv:
        import tempfile
        f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
        f.write("x " * 400); f.close()
        assert "BLOCK" in check(f.name)
        assert check(f.name.replace(".py", ".md")) is None
        os.unlink(f.name); print("self-check ok")
    else:
        main()
