"""Validate portable package wiring without installing either host."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check():
    claude = read(".claude-plugin/plugin.json")
    codex = read(".codex-plugin/plugin.json")
    assert claude["name"] == codex["name"] == "atelier"
    assert claude["version"] == codex["version"]
    catalog = read(".agents/plugins/marketplace.json")
    entry = catalog["plugins"][0]
    assert (ROOT / entry["source"]["path"]).resolve() == ROOT
    assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    for field in ("skills", "mcpServers"):
        assert (ROOT / codex[field]).exists()
    for field in ("logo", "composerIcon"):
        assert (ROOT / codex["interface"][field]).is_file()
    for command in (ROOT / "commands").glob("*.md"):
        skill = ROOT / "skills" / f"atelier-{command.stem}" / "SKILL.md"
        assert skill.is_file(), command
        assert (ROOT / "references/workflows" / command.name).is_file()
    for path in list((ROOT / "skills").glob("*/SKILL.md")) + list((ROOT / "references").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                assert (path.parent / target.split("#")[0]).exists(), (path, target)
    assert set(read(".mcp.json")["mcpServers"]) == {"shadcn", "magicui", "aceternityui", "reactbits"}
    assert (ROOT / "skills/web-quality/SKILL.md").is_file()
    assert (ROOT / "playwright.config.ts").is_file()
    assert (ROOT / "package-lock.json").is_file()
    hooks = read("hooks/hooks.json")["hooks"]
    assert {"SessionStart", "PostToolUse"} <= hooks.keys()
    print("Package wiring passed")


if __name__ == "__main__":
    check()
