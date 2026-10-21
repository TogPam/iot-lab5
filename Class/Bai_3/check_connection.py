from gateway.common import Session, parser


def main():
    args = parser("Bai 3: verify Paho MQTT connection").parse_args()
    with Session(args):
        print("Ket noi MQTT thanh cong", flush=True)


if __name__ == "__main__":
    main()
