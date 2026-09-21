"""Read affected paths from host hook payloads without executing patch text."""
from pathlib import Path


def affected(data):
    tool = data.get("tool_input") or {}
    if not isinstance(tool, dict):
        return []
    names = []
    if isinstance(tool.get("file_path"), str):
        names.append(tool["file_path"])
    if data.get("tool_name") == "apply_patch":
        patch = tool.get("command", "")
        if not isinstance(patch, str):
            return names
        current = None
        for line in patch.splitlines():
            if line.startswith(("*** Add File: ", "*** Update File: ")):
                current = line.split(": ", 1)[1]
                names.append(current)
            elif line.startswith("*** Move to: "):
                if current in names:
                    names.remove(current)
                names.append(line.split(": ", 1)[1])
            elif line.startswith("*** Delete File: "):
                current = None
    root = Path(data.get("cwd") or Path.cwd()).resolve()
    return list(dict.fromkeys(str((root / name).resolve()) for name in names if name))
