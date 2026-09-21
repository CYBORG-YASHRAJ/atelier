"""Opt-in network check: initialize bundled servers and discover tools."""
import json
import shutil
import sys
from pathlib import Path
from mcp_transport import Client

ROOT = Path(__file__).resolve().parents[1]


def smoke(name, config, project):
    executable = shutil.which(config["command"])
    if not executable:
        raise RuntimeError(f"{config['command']} is missing")
    client = Client([executable, *config.get("args", [])], project)
    try:
        result = client.request(1, "initialize", {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "atelier-smoke", "version": "0.5.0"}})
        assert result.get("protocolVersion"), "missing negotiated protocol"
        client.send({"method": "notifications/initialized"})
        result = client.request(2, "tools/list", {})
        assert result.get("tools"), "server exposed no tools"
        print(f"{name}: discovered {len(result['tools'])} tools", flush=True)
    finally:
        client.close()


if __name__ == "__main__":
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    servers = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]
    failed = []
    for name, config in servers.items():
        print(f"{name}: starting", flush=True)
        try:
            smoke(name, config, project)
        except Exception as error:
            failed.append(name)
            print(f"{name}: unavailable ({type(error).__name__})", flush=True)
    sys.exit(1 if failed else 0)
