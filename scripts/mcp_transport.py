"""Bounded newline-JSON MCP smoke transport; never print server logs."""
import json
import os
import queue
import signal
import subprocess
import threading
import time


class Client:
    def __init__(self, command, cwd):
        options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
        self.process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        text=True, encoding="utf-8", **options)
        self.messages = queue.Queue()
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()

    def read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                pass
        self.messages.put(None)

    def send(self, value):
        self.process.stdin.write(json.dumps({"jsonrpc": "2.0", **value}) + "\n")
        self.process.stdin.flush()

    def request(self, identifier, method, params, timeout=60):
        self.send({"id": identifier, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while True:
            response = self.messages.get(timeout=max(0, deadline - time.monotonic()))
            if response is None:
                raise RuntimeError("server exited before responding")
            if response.get("id") == identifier:
                if "error" in response:
                    raise RuntimeError("MCP returned a protocol error")
                return response["result"]

    def close(self):
        if self.process.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(self.process.pid), "/T", "/F"],
                               capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                os.killpg(self.process.pid, signal.SIGTERM)
        self.process.wait(timeout=10)
        self.reader.join(timeout=2)
        self.process.stdin.close()
        self.process.stdout.close()
