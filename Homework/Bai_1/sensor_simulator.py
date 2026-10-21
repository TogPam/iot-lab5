import random

from gateway.common import Session, parser, stop_event, timestamp


def main():
    p = parser("Simulated sensor nodes; these values are not physical measurements")
    p.add_argument("--node", choices=["node1", "node2"], default="node1")
    p.add_argument("--interval", type=float, default=3)
    p.add_argument("--count", type=int, default=0)
    args = p.parse_args()
    if args.interval <= 0 or args.count < 0:
        p.error("interval must be positive; count must be nonnegative")
    stop, sent = stop_event(), 0
    with Session(args, role=args.node) as session:
        while not stop.is_set():
            data = {"simulated": True, "timestamp": timestamp(),
                    "temperature_c": round(random.uniform(25, 32), 2),
                    "humidity_percent": round(random.uniform(55, 80), 2)}
            print("SENSOR " + session.publish(f"sensor/{args.node}/data", data), flush=True)
            sent += 1
            if args.count and sent >= args.count:
                break
            stop.wait(args.interval)


if __name__ == "__main__":
    main()
