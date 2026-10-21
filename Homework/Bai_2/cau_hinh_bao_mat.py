"""Generate local credentials and portable Mosquitto configuration."""
import json
import secrets
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    config = ROOT / "config"
    shutil.copyfile(ROOT / "Ve_nha/Bai_2/acl", config / "acl")
    accounts_file = config / "credentials.json"
    if accounts_file.exists():
        accounts = json.loads(accounts_file.read_text(encoding="utf-8"))
    else:
        accounts = {role: {"username": role, "password": secrets.token_urlsafe(24)}
                    for role in ("gateway", "dashboard", "operator", "node1", "node2")}
        accounts_file.write_text(json.dumps(accounts, indent=2), encoding="utf-8")
    passwd = ROOT / "tools" / "mosquitto" / "mosquitto_passwd.exe"
    if not passwd.exists():
        passwd = shutil.which("mosquitto_passwd")
    if not passwd:
        raise SystemExit("Install Mosquitto first")
    # Convert clear text to salted hashes with the official mosquitto_passwd utility.
    # Passwords are not placed in process command-line arguments.
    password_file = config / "passwords"
    password_file.write_text("".join(f"{a['username']}:{a['password']}\n" for a in accounts.values()), encoding="utf-8")
    result = subprocess.run([str(passwd), "-U", str(password_file)], capture_output=True, text=True)
    if result.returncode:
        password_file.unlink(missing_ok=True)
        raise RuntimeError(result.stderr)
    for filename, address in (("mosquitto-secure.conf", "127.0.0.1"),
                              ("mosquitto-lan.conf", "0.0.0.0")):
        (config / filename).write_text(
            f"listener 1883 {address}\nallow_anonymous false\n"
            f"password_file {password_file.as_posix()}\nacl_file {(config / 'acl').as_posix()}\n"
            "persistence false\nlog_dest stdout\nlog_type all\n", encoding="utf-8")
    # Credentials stay separate from the shareable flows.json.
    (ROOT / "node-red" / "flows_cred.json").write_text(json.dumps({
        "lab5-mqtt-local": {"user": accounts["dashboard"]["username"],
                       "password": accounts["dashboard"]["password"]}
    }), encoding="utf-8")
    print("Prepared password hashes, ACL configuration and Node-RED credentials (no secrets displayed).")


if __name__ == "__main__":
    main()
