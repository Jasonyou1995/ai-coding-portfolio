"""Smart Mailbox CLI client."""

import argparse
import socket
import sys

from common.protocol import FETCH_INBOX, RELAY_MAIL, decode, encode, make_msg


def send_mail(host: str, port: int, from_: str, to: str, subject: str, body: str) -> None:
    msg = make_msg(RELAY_MAIL, {"from_": from_, "to": to, "subject": subject, "body": body})
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(encode(msg))
    resp = decode(sock.makefile("rb").readline())
    sock.close()
    payload = resp["payload"]
    print(f"Status: {payload['status']}")
    if payload.get("reason"):
        print(f"Reason: {payload['reason']}")
    sys.exit(0 if payload["status"] == "ok" else 1)


def fetch_inbox(host: str, port: int, user: str) -> None:
    msg = make_msg(FETCH_INBOX, {"user": user})
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port + 1000))
    sock.sendall(encode(msg))
    resp = decode(sock.makefile("rb").readline())
    sock.close()
    mails = resp["payload"]["mails"]
    if not mails:
        print("Inbox empty.")
        return
    print(f"{'From':<22} {'To':<22} {'Subject':<15} Body")
    print("-" * 80)
    for m in mails:
        print(f"{m['from_']:<22} {m['to']:<22} {m['subject']:<15} {m['body']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart Mailbox CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_send = sub.add_parser("send", help="Send an email")
    p_send.add_argument("--server-host", default="127.0.0.1")
    p_send.add_argument("--server-port", type=int, required=True)
    p_send.add_argument("--from", dest="from_", required=True)
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)

    p_inbox = sub.add_parser("inbox", help="Fetch inbox")
    p_inbox.add_argument("--server-host", default="127.0.0.1")
    p_inbox.add_argument("--server-port", type=int, required=True)
    p_inbox.add_argument("--user", required=True)

    args = parser.parse_args()
    if args.command == "send":
        send_mail(args.server_host, args.server_port, args.from_, args.to, args.subject, args.body)
    elif args.command == "inbox":
        fetch_inbox(args.server_host, args.server_port, args.user)


if __name__ == "__main__":
    main()
