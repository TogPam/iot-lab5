import socket
import time

import psutil

from gateway.common import Session, parser, stop_event, timestamp


def main():
    p = parser("Bai 4: publish real CPU/RAM metrics every 5 seconds")
    p.add_argument("--interval", type=float, default=5)
    p.add_argument("--count", type=int, default=0, help="0 = run continuously")
    args = p.parse_args()
    if args.interval <= 0 or args.count < 0:
        p.error("interval must be positive; count must be nonnegative")
    stop = stop_event()
    psutil.cpu_percent(interval=None)
    with Session(args) as session:
        sent = 0
        deadline = time.monotonic() + args.interval
        while not stop.wait(max(0, deadline - time.monotonic())):
            ram = psutil.virtual_memory()
            payload = {"gateway_id": socket.gethostname(), "timestamp": timestamp(),
                       "cpu_percent": psutil.cpu_percent(interval=None),
                       "ram_percent": ram.percent, "ram_used_bytes": ram.used,
                       "ram_total_bytes": ram.total}
            print("METRICS " + session.publish("gateway/system/metrics", payload), flush=True)
            sent += 1
            if args.count and sent >= args.count:
                break
            deadline += args.interval


if __name__ == "__main__":
    main()
