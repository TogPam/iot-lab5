import argparse
import json
import os
import signal
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

ROOT = Path(__file__).resolve().parents[1]


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def parser(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--host", default=os.getenv("MQTT_HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "1883")))
    p.add_argument("--anonymous", action="store_true")
    return p


def credentials(role):
    if os.getenv("MQTT_USERNAME"):
        return os.environ["MQTT_USERNAME"], os.getenv("MQTT_PASSWORD", "")
    path = ROOT / "config" / "credentials.json"
    if not path.exists():
        raise RuntimeError("Run scripts/setup.ps1 first, or set MQTT_USERNAME and MQTT_PASSWORD")
    account = json.loads(path.read_text(encoding="utf-8"))[role]
    return account["username"], account["password"]


class Session:
    """Wait for CONNACK/SUBACK before announcing readiness; resubscribe after reconnect."""

    def __init__(self, args, role="gateway", subscriptions=(), on_message=None):
        self.args = args
        self.subscriptions = list(subscriptions)
        self.ready = threading.Event()
        self.error = None
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                  client_id=f"lab5-{role}-{uuid.uuid4().hex[:8]}")
        if not args.anonymous:
            self.client.username_pw_set(*credentials(role))
        self.client.on_connect = self._connected
        self.client.on_subscribe = self._subscribed
        if on_message:
            self.client.on_message = on_message
        self.client.reconnect_delay_set(1, 10)

    def _connected(self, client, userdata, flags, reason, properties):
        self.ready.clear()
        if reason.is_failure:
            self.error = f"MQTT connection refused: {reason}"
            self.ready.set()
        elif self.subscriptions:
            client.subscribe([(topic, 1) for topic in self.subscriptions])
        else:
            self.ready.set()

    def _subscribed(self, client, userdata, mid, reasons, properties):
        if any(reason.is_failure for reason in reasons):
            self.error = f"MQTT subscription refused: {reasons}"
        self.ready.set()

    def __enter__(self):
        self.client.connect(self.args.host, self.args.port, keepalive=30)
        self.client.loop_start()
        if not self.ready.wait(10) or self.error:
            self.client.disconnect()
            self.client.loop_stop()
            raise RuntimeError(self.error or "Timed out waiting for MQTT broker")
        print(f"CONNECTED {self.args.host}:{self.args.port}", flush=True)
        if self.subscriptions:
            print("SUBSCRIBED " + ", ".join(self.subscriptions), flush=True)
        return self

    def publish(self, topic, payload, retain=False):
        data = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, allow_nan=False)
        result = self.client.publish(topic, data, qos=1, retain=retain)
        result.wait_for_publish(timeout=10)
        if not result.is_published():
            raise RuntimeError(f"MQTT publish timed out: {topic}")
        return data

    def __exit__(self, *exc):
        self.client.disconnect()
        self.client.loop_stop()


def stop_event():
    stop = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    return stop
