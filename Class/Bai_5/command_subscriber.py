from gateway.common import Session, parser, stop_event, timestamp


def main():
    args = parser("Bai 5: listen to gateway/command/#").parse_args()
    stop = stop_event()

    def receive(client, userdata, msg):
        print(f"COMMAND {timestamp()} {msg.topic} {msg.payload.decode('utf-8', errors='replace')}", flush=True)

    with Session(args, subscriptions=["gateway/command/#"], on_message=receive):
        stop.wait()


if __name__ == "__main__":
    main()
