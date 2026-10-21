import json
import threading
import time

from gateway.common import Session, parser, stop_event, timestamp


class Aggregator:
    """Keep the latest JSON object per node for each 10-second window."""

    def __init__(self):
        self.lock = threading.Lock()
        self.pending = {}
        self.messages = 0
        self.started = timestamp()

    def receive(self, client, userdata, msg):
        try:
            parts = msg.topic.split("/")
            if len(parts) != 3 or parts[0] != "sensor" or not parts[1] or parts[2] != "data":
                return
            data = json.loads(msg.payload.decode("utf-8"),
                              parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
            if not isinstance(data, dict):
                raise ValueError("sensor payload must be a JSON object")
        except (ValueError, UnicodeDecodeError) as exc:
            print(f"IGNORED {msg.topic}: {exc}", flush=True)
            return
        with self.lock:
            self.pending[parts[1]] = {"data": data, "received_at": timestamp()}
            self.messages += 1
        print(f"SENSOR {parts[1]} {json.dumps(data, ensure_ascii=False)}", flush=True)

    def snapshot(self):
        with self.lock:
            end = timestamp()
            report = {"window_start": self.started, "timestamp": end,
                      "node_count": len(self.pending), "message_count": self.messages,
                      "nodes": self.pending}
            self.pending = {}
            self.messages = 0
            self.started = end
        return report

    def restore(self, report):
        # Preserve newer arrivals when retrying an unsuccessful publication.
        with self.lock:
            self.pending = {**report["nodes"], **self.pending}
            self.messages += report["message_count"]
            self.started = report["window_start"]


def main():
    p = parser("Ve nha 1: aggregate sensor/+/data every 10 seconds")
    p.add_argument("--interval", type=float, default=10)
    p.add_argument("--count", type=int, default=0)
    args = p.parse_args()
    if args.interval <= 0 or args.count < 0:
        p.error("interval must be positive; count must be nonnegative")
    state, stop = Aggregator(), stop_event()
    with Session(args, subscriptions=["sensor/+/data"], on_message=state.receive) as session:
        sent = 0
        deadline = time.monotonic() + args.interval
        while not stop.wait(max(0, deadline - time.monotonic())):
            report = state.snapshot()
            try:
                print("REPORT " + session.publish("gateway/aggregated_report", report), flush=True)
            except (RuntimeError, ValueError) as exc:
                state.restore(report)
                print(f"RETRY {exc}", flush=True)
            else:
                sent += 1
            if args.count and sent >= args.count:
                break
            deadline = max(deadline + args.interval, time.monotonic())


if __name__ == "__main__":
    main()
