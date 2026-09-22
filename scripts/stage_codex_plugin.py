"""Build a clean, local Codex marketplace from the working tree."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "codex-marketplace"

PLUGIN_DIRECTORIES = (
    ".codex-plugin",
    "db",
    "docs/assets",
    "hooks",
    "mcp",
    "references",
    "skills",
    "templates",
)
PLUGIN_FILES = (".mcp.json", "LICENSE", "README.md", "runtime.py")
EXCLUDED_NAMES = {"__pycache__", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def ignored(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in EXCLUDED_NAMES or Path(name).suffix in EXCLUDED_SUFFIXES
    }


def clean_output(output: Path) -> None:
    allowed_parent = (ROOT / "dist").resolve()
    resolved = output.resolve()
    if resolved.parent != allowed_parent:
        raise ValueError(f"output must be a direct child of {allowed_parent}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def stage(output: Path) -> Path:
    clean_output(output)
    plugin_root = output / "plugins" / "atelier"
    plugin_root.mkdir(parents=True)

    for relative in PLUGIN_DIRECTORIES:
        shutil.copytree(
            ROOT / relative, plugin_root / relative, ignore=ignored
        )
    for relative in PLUGIN_FILES:
        destination = plugin_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)

    catalog = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
    catalog["plugins"][0]["source"] = {
        "source": "local",
        "path": "./plugins/atelier",
    }
    catalog_path = output / ".agents" / "plugins" / "marketplace.json"
    catalog_path.parent.mkdir(parents=True)
    catalog_path.write_text(
        json.dumps(catalog, indent=2) + "\n", encoding="utf-8"
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage Atelier without checkout-only files."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(stage(args.output))


if __name__ == "__main__":
    main()
