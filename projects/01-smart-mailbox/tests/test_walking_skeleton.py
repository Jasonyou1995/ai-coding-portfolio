"""Walking-skeleton integration test: cross-domain mail delivery."""

import os
import socket
import subprocess
import sys
import time

import pytest

from common.protocol import FETCH_INBOX, RELAY_MAIL, decode, encode, make_msg

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_A = {"DOMAIN": "a.mail", "PORT": "9001", "PEER_DOMAIN": "b.mail", "PEER_PORT": "9002"}
ENV_B = {"DOMAIN": "b.mail", "PORT": "9002", "PEER_DOMAIN": "a.mail", "PEER_PORT": "9001"}


def _wait_for_tcp(host: str, port: int, timeout: float = 10.0) -> None:
    """Retry connecting until the port accepts or timeout expires."""
    deadline = time.monotonic() + timeout
    last_err = None
    while time.monotonic() < deadline:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((host, port))
            sock.close()
            return
        except (ConnectionRefusedError, OSError) as exc:
            last_err = exc
    raise TimeoutError(f"Could not connect to {host}:{port} after {timeout}s: {last_err}")


def _send_mail(host: str, port: int, from_: str, to: str, subject: str, body: str) -> dict:
    msg = make_msg(RELAY_MAIL, {"from_": from_, "to": to, "subject": subject, "body": body})
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(encode(msg))
    line = sock.makefile("rb").readline()
    sock.close()
    return decode(line)


def _fetch_inbox(host: str, port: int, user: str) -> dict:
    msg = make_msg(FETCH_INBOX, {"user": user})
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port + 1000))
    sock.sendall(encode(msg))
    line = sock.makefile("rb").readline()
    sock.close()
    return decode(line)


@pytest.fixture(scope="module")
def servers():
    proc_a = subprocess.Popen(
        [sys.executable, "-m", "server.main"],
        cwd=PROJECT_ROOT,
        env={**os.environ, **ENV_A},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc_b = subprocess.Popen(
        [sys.executable, "-m", "server.main"],
        cwd=PROJECT_ROOT,
        env={**os.environ, **ENV_B},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_tcp("127.0.0.1", 9001)
        _wait_for_tcp("127.0.0.1", 9002)
        _wait_for_tcp("127.0.0.1", 10001)
        _wait_for_tcp("127.0.0.1", 10002)
        yield {"a": proc_a, "b": proc_b}
    finally:
        proc_a.terminate()
        proc_b.terminate()
        proc_a.wait()
        proc_b.wait()


def test_a_to_b(servers):
    ack = _send_mail("127.0.0.1", 9001, "alice@a.mail", "bob@b.mail", "Hi Bob", "Hello from Alice")
    assert ack["payload"]["status"] == "ok", ack["payload"].get("reason")

    resp = _fetch_inbox("127.0.0.1", 9002, "bob@b.mail")
    mails = resp["payload"]["mails"]
    assert len(mails) == 1
    assert mails[0]["from_"] == "alice@a.mail"
    assert mails[0]["to"] == "bob@b.mail"
    assert mails[0]["subject"] == "Hi Bob"
    assert mails[0]["body"] == "Hello from Alice"


def test_b_to_a(servers):
    ack = _send_mail("127.0.0.1", 9002, "charlie@b.mail", "dave@a.mail", "Hey Dave", "Hello from Charlie")
    assert ack["payload"]["status"] == "ok", ack["payload"].get("reason")

    resp = _fetch_inbox("127.0.0.1", 9001, "dave@a.mail")
    mails = resp["payload"]["mails"]
    assert len(mails) == 1
    assert mails[0]["from_"] == "charlie@b.mail"
    assert mails[0]["to"] == "dave@a.mail"
    assert mails[0]["subject"] == "Hey Dave"
    assert mails[0]["body"] == "Hello from Charlie"
