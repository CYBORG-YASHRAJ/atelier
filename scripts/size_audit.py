"""Audit source files, including writes made outside the editor hook."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from file_size_gate import check

SOURCE = {".py", ".tsx", ".ts", ".jsx", ".js", ".mjs", ".cjs", ".css", ".scss",
          ".rs", ".go", ".java", ".c", ".cpp", ".h", ".cs", ".rb", ".php", ".sh", ".ps1"}
SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
        "workspace", "generated", "migrations"}


def audit(root):
    messages = []
    for directory, folders, files in os.walk(root):
        folders[:] = [name for name in folders if name not in SKIP]
        for name in files:
            path = Path(directory) / name
            if path.suffix in SOURCE:
                message = check(str(path))
                if message:
                    messages.append(message)
    return messages


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        sys.exit(f"Not a project directory: {root}")
    messages = audit(root)
    print("\n".join(messages) if messages else "Size audit passed")
    sys.exit(1 if any(msg.startswith("BLOCK") for msg in messages) else 0)
