"""Validate skill frontmatter and shared workflow metadata."""
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate():
    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    for path in skills:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), path
        metadata = yaml.safe_load(content.split("---", 2)[1])
        assert metadata["name"] == path.parent.name, path
        assert re.fullmatch(r"[a-z0-9-]{1,64}", metadata["name"]), path
        assert isinstance(metadata["description"], str) and metadata["description"].strip(), path
    for path in (ROOT / "commands").glob("*.md"):
        metadata = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        assert metadata["description"], path
    models = {"architect": "opus", "builder": "sonnet", "summarizer": "haiku",
              "learner": "sonnet", "design-scout": "sonnet"}
    for name, model in models.items():
        text = (ROOT / "agents" / f"{name}.md").read_text(encoding="utf-8")
        assert yaml.safe_load(text.split("---", 2)[1])["model"] == model
    print(f"Validated {len(skills)} skills, 11 commands and 5 Claude model pins")


if __name__ == "__main__":
    validate()
