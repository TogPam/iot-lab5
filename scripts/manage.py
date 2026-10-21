"""Start/stop this lab's own background processes, with PID identity checks."""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "logs" / "processes.json"


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def owned(record):
    try:
        proc = psutil.Process(record["pid"])
        if abs(proc.create_time() - record["created"]) < 0.01:
            return proc
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return None


def wait_port(port, proc):
    for _ in range(150):
        if proc.poll() is not None:
            raise RuntimeError(f"Process exited: inspect logs (port {port})")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError(f"Port {port} not ready")


def start():
    state = load()
    if any(owned(record) for record in state.values()):
        raise RuntimeError("Lab already running; use status or stop first")
    for port in (1880, 1883):
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                raise RuntimeError(f"Port {port} already in use")
    commands = [
        ("broker", [str(ROOT / "tools/mosquitto/mosquitto.exe"), "-c", str(ROOT / "config/mosquitto-secure.conf")], 1883),
        ("node-red", [shutil.which("node"), str(ROOT / "node-red/node_modules/node-red/red.js"),
                      "--userDir", str(ROOT / "node-red"), "--settings", str(ROOT / "node-red/settings.js")], 1880),
        ("metrics", [sys.executable, "-u", "-m", "gateway.metrics_publisher"], None),
        ("commands", [sys.executable, "-u", "-m", "gateway.command_subscriber"], None),
        ("aggregator", [sys.executable, "-u", "-m", "gateway.aggregator"], None),
        ("sensor-node1", [sys.executable, "-u", "-m", "gateway.sensor_simulator", "--node", "node1"], None),
        ("sensor-node2", [sys.executable, "-u", "-m", "gateway.sensor_simulator", "--node", "node2"], None),
    ]
    state = {}
    try:
        for name, command, port in commands:
            with (ROOT / "logs" / f"{name}.log").open("a", encoding="utf-8") as log:
                flags = (subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0
                proc = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                        stdin=subprocess.DEVNULL, creationflags=flags)
            state[name] = {"pid": proc.pid, "created": psutil.Process(proc.pid).create_time()}
            STATE.write_text(json.dumps(state, indent=2))
            if port:
                wait_port(port, proc)
        time.sleep(2)
        if not all(owned(record) and owned(record).is_running() for record in state.values()):
            raise RuntimeError("A process stopped during startup; inspect logs")
    except Exception:
        stop()
        raise
    print("Lab started. Dashboard: http://127.0.0.1:1880/dashboard/gateway")


def stop():
    for name, record in reversed(list(load().items())):
        proc = owned(record)
        if proc:
            proc.terminate()
            try:
                proc.wait(5)
            except psutil.TimeoutExpired:
                proc.kill()
            print(f"Stopped {name}")
    STATE.unlink(missing_ok=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["start", "stop", "status"])
    args = p.parse_args()
    if args.action == "start":
        start()
    elif args.action == "stop":
        stop()
    else:
        for name, record in load().items():
            print(f"{name}: {'running' if owned(record) else 'stopped'} (PID {record['pid']})")
