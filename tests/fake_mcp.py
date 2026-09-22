"""Local protocol fixture: presence checks never expose credential values."""
import json
import os
import sys

for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    result = {"protocolVersion": "2024-11-05", "capabilities": {},
              "serverInfo": {"name": "fixture", "version": "1"}}
    if request["method"] == "tools/list":
        result = {"tools": [{"name": "fixture", "inputSchema": {"type": "object"}}],
                  "credentialInherited": bool(os.getenv("ATELIER_TEST_TOKEN"))}
    print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
