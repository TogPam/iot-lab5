"""Exercise real Mosquitto binaries and gateway processes, not mocked MQTT."""
import json
import os
import queue
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import paho.mqtt.client as mqtt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gateway.common import Session, credentials

BIN = ROOT / "tools" / "mosquitto"
RESULTS = []
PROCESSES = []


def check(name, condition, evidence):
    RESULTS.append({"name": name, "passed": bool(condition), "evidence": evidence})
    print(f"{'PASS' if condition else 'FAIL'} {name}: {evidence}", flush=True)
    if not condition:
        raise AssertionError(name)


def spawn(name, command):
    log = (ROOT / "logs" / f"test-{name}.log").open("w", encoding="utf-8")
    proc = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    log.close()
    PROCESSES.append(proc)
    return proc


def wait_port(port, proc):
    for _ in range(100):
        if proc.poll() is not None:
            raise RuntimeError(f"Broker exited {proc.returncode}; inspect test log")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=.1):
                return
        except OSError:
            time.sleep(.1)
    raise TimeoutError("broker did not start")


def cli(program, port, arguments, role=None):
    command = [str(BIN / f"{program}.exe"), "-h", "127.0.0.1", "-p", str(port)]
    if role:
        user, password = credentials(role)
        command += ["-u", user, "-P", password]
    return subprocess.run(command + arguments, cwd=ROOT, capture_output=True, text=True, timeout=15)


def wait_log(name, text, timeout=15):
    deadline = time.monotonic() + timeout
    file = ROOT / "logs" / f"test-{name}.log"
    while time.monotonic() < deadline:
        if file.exists() and text in file.read_text(encoding="utf-8", errors="replace"):
            return True
        time.sleep(.1)
    return False


def main():
    # Isolated ports leave the demonstration on 1883 untouched.
    anon, secure = 18884, 18885
    for port in (anon, secure):
        with socket.socket() as probe:
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                raise RuntimeError(f"Test port {port} occupied")
    cfg = ROOT / "config"
    local = (cfg / "mosquitto-local.conf").read_text().replace("listener 1883", f"listener {anon}")
    secured = (cfg / "mosquitto-secure.conf").read_text().replace("listener 1883", f"listener {secure}")
    (ROOT / "logs/test-anonymous.conf").write_text(local)
    (ROOT / "logs/test-secure.conf").write_text(secured)
    broker = spawn("anonymous", [str(BIN / "mosquitto.exe"), "-c", str(ROOT / "logs/test-anonymous.conf")])
    wait_port(anon, broker)
    received = queue.Queue()
    args = SimpleNamespace(host="127.0.0.1", port=anon, anonymous=True)
    with Session(args, subscriptions=["gateway/test"], on_message=lambda c,u,m: received.put(m.payload.decode())):
        sent = cli("mosquitto_pub", anon, ["-t", "gateway/test", "-m", "Hello Local MQTT"])
        message = received.get(timeout=5)
        check("Bai 1-2: local broker and CLI publish", sent.returncode == 0 and message == "Hello Local MQTT", message)
    # Native mosquitto_sub is also tested with a retained message and automatic timeout.
    cli("mosquitto_pub", anon, ["-t", "gateway/test", "-m", "Hello Local MQTT", "-r"])
    sub = cli("mosquitto_sub", anon, ["-t", "gateway/test", "-C", "1", "-W", "5"])
    check("Bai 2: native mosquitto_sub", sub.returncode == 0 and sub.stdout.strip() == "Hello Local MQTT", sub.stdout.strip())
    broker.terminate()
    broker.wait(5)
    broker = spawn("secure", [str(BIN / "mosquitto.exe"), "-c", str(ROOT / "logs/test-secure.conf")])
    wait_port(secure, broker)
    for label, extra in (("anonymous", []), ("wrong password", ["-u", "gateway", "-P", "definitely-wrong"])):
        denied = cli("mosquitto_pub", secure, ["-t", "gateway/test", "-m", "denied"] + extra)
        check(f"Ve nha 2: reject {label}", denied.returncode != 0, denied.stderr.strip())
    denied = cli("mosquitto_pub", secure, ["-V", "mqttv5", "-q", "1", "-t", "gateway/command/led", "-m", "denied"], "node1")
    check("Ve nha 2: ACL prevents sensor commands", denied.returncode != 0 or "Not authorized" in denied.stderr,
          denied.stderr.strip())
    connected = subprocess.run([sys.executable, "-m", "gateway.check_connection", "--port", str(secure)], cwd=ROOT, capture_output=True, text=True, timeout=15)
    check("Bai 3: Paho connection callback", connected.returncode == 0 and "thanh cong" in connected.stdout, connected.stdout.strip())
    events = queue.Queue()
    args = SimpleNamespace(host="127.0.0.1", port=secure, anonymous=False)
    with Session(args, role="operator", subscriptions=["gateway/system/metrics", "gateway/aggregated_report"],
                 on_message=lambda c,u,m: events.put((m.topic, time.monotonic(), json.loads(m.payload)))) as observer:
        spawn("metrics", [sys.executable, "-u", "-m", "gateway.metrics_publisher", "--port", str(secure), "--count", "3"])
        spawn("commands", [sys.executable, "-u", "-m", "gateway.command_subscriber", "--port", str(secure)])
        spawn("aggregator", [sys.executable, "-u", "-m", "gateway.aggregator", "--port", str(secure), "--count", "2"])
        assert wait_log("commands", "SUBSCRIBED") and wait_log("aggregator", "SUBSCRIBED")
        observer.publish("gateway/command/led", {"state": "ON"})
        check("Bai 5: wildcard command callback", wait_log("commands", '"state": "ON"'), "gateway/command/led -> ON")
        with Session(args, role="node1") as node1, Session(args, role="node2") as node2:
            node1.publish("sensor/node1/data", {"temperature_c": 28, "sequence": 1})
            node1.publish("sensor/node1/data", {"temperature_c": 29, "sequence": 2})
            node1.publish("sensor/node1/data", "invalid JSON")
            node2.publish("sensor/node2/data", {"humidity_percent": 70})
        metrics, reports = [], []
        deadline = time.monotonic() + 28
        while time.monotonic() < deadline and (len(metrics) < 3 or len(reports) < 2):
            topic, at, data = events.get(timeout=28)
            (metrics if topic.endswith("metrics") else reports).append((at, data))
        gaps = [round(metrics[i][0] - metrics[i-1][0], 2) for i in range(1, len(metrics))]
        check("Bai 4: real CPU/RAM every 5s", len(metrics) == 3 and all(4 <= n <= 6 for n in gaps)
              and all(0 <= x[1][key] <= 100 for x in metrics for key in ("cpu_percent", "ram_percent")),
              {"intervals_seconds": gaps, "sample": metrics[0][1]})
        report = reports[0][1]
        gap = round(reports[1][0] - reports[0][0], 2)
        check("Ve nha 1: aggregate nodes every 10s", report["node_count"] == 2 and report["message_count"] == 3
              and report["nodes"]["node1"]["data"]["sequence"] == 2 and 9 <= gap <= 11,
              {"interval_seconds": gap, "report": report})
        check("Ve nha 1: empty window and invalid JSON", reports[1][1]["node_count"] == 0 and wait_log("aggregator", "IGNORED"), reports[1][1])
        cli("mosquitto_pub", secure, ["-V", "mqttv5", "-q", "1", "-t", "gateway/system/metrics", "-m", "999"], "dashboard")
        try:
            forbidden = events.get(timeout=1)
        except queue.Empty:
            forbidden = None
        check("Ve nha 2: dashboard is read-only", forbidden is None, "Dashboard publish was not delivered")


if __name__ == "__main__":
    error = None
    try:
        main()
    except Exception as exc:
        error = str(exc)
        print(f"ERROR {type(exc).__name__}: {exc}", flush=True)
    finally:
        for proc in reversed(PROCESSES):
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        result = {"tested_at": datetime.now(timezone.utc).isoformat(), "results": RESULTS, "error": error}
        (ROOT / "reports/test-results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(1 if error or any(not r["passed"] for r in RESULTS) else 0)
