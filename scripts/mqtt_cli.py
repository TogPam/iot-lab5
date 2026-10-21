"""Run Mosquitto CLI using a local account without copying passwords into examples."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--role", default="operator", choices=["operator", "gateway", "dashboard", "node1", "node2"])
p.add_argument("command", choices=["pub", "sub"])
args, rest = p.parse_known_args()
account = json.loads((ROOT / "config/credentials.json").read_text())[args.role]
program = f"mosquitto_{args.command}"
binary = ROOT / "tools/mosquitto" / f"{program}.exe"
if not binary.exists():
    binary = shutil.which(program)
raise SystemExit(subprocess.call([str(binary), "-h", "127.0.0.1", "-p", "1883",
                                 "-u", account["username"], "-P", account["password"], *rest]))
