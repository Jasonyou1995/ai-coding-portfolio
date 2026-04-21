"""Smart Mailbox TCP server (Phase 1)."""

import logging
import socket
import threading
import time
import uuid
from typing import Any, Dict, List

from common.protocol import ACK, FETCH_INBOX, HELLO, RELAY_MAIL, decode, encode, make_msg
from server.config import DOMAIN, PEER_DOMAIN, PEER_PORT, PORT

logging.basicConfig(level=logging.INFO, format="%(message)s")


class MailServer:
    def __init__(self) -> None:
        self.domain = DOMAIN
        self.port = PORT
        self.peer_domain = PEER_DOMAIN
        self.peer_port = PEER_PORT
        self.inbox: Dict[str, List[Dict[str, Any]]] = {}
        self.lock = threading.Lock()

    def _send(self, sock: socket.socket, msg: Dict[str, Any]) -> None:
        sock.sendall(encode(msg))

    def _log(self, arrow: str, msg_type: str, payload: Dict[str, Any]) -> None:
        if msg_type == RELAY_MAIL:
            logging.info(
                f"[SERVER {self.domain}] {arrow} {msg_type} from {payload['from_']} to {payload['to']}"
            )
        else:
            logging.info(f"[SERVER {self.domain}] {arrow} {msg_type}")

    def _ack(self, ref_msg_id: str, status: str = "ok", reason: str | None = None, **extra: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"ref_msg_id": ref_msg_id, "status": status, "reason": reason}
        payload.update(extra)
        return make_msg(ACK, payload)

    def _handle_relay(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        payload = msg["payload"]
        to_addr = payload["to"]
        if to_addr.endswith(f"@{self.domain}"):
            with self.lock:
                self.inbox.setdefault(to_addr, []).append(payload)
            return self._ack(msg["msg_id"])
        try:
            peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer.connect(("127.0.0.1", self.peer_port))
            self._send(peer, msg)
            line = peer.makefile("rb").readline()
            peer.close()
            return decode(line)
        except Exception as exc:
            return self._ack(msg["msg_id"], "error", str(exc))

    def _handle_fetch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        user = payload.get("user", "")
        with self.lock:
            mails = list(self.inbox.get(user, []))
        return {
            "type": FETCH_INBOX,
            "msg_id": str(uuid.uuid4()),
            "ts": time.time(),
            "payload": {"mails": mails},
        }

    def handle_client(self, sock: socket.socket, _addr: Any) -> None:
        try:
            for line in sock.makefile("rb"):
                try:
                    msg = decode(line)
                except Exception as exc:
                    logging.warning(f"[SERVER {self.domain}] decode error: {exc}")
                    continue
                msg_type = msg["type"]
                payload = msg["payload"]
                self._log("<-", msg_type, payload)
                if msg_type == HELLO:
                    reply = self._ack(msg["msg_id"])
                elif msg_type == RELAY_MAIL:
                    reply = self._handle_relay(msg)
                elif msg_type == FETCH_INBOX:
                    reply = self._handle_fetch(payload)
                elif msg_type == ACK:
                    continue
                else:
                    reply = self._ack(msg["msg_id"], "error", "unknown_type")
                self._send(sock, reply)
                self._log("->", reply["type"], reply.get("payload", {}))
        except (ConnectionError, ConnectionResetError, BrokenPipeError):
            pass
        finally:
            sock.close()

    def _listen(self, port: int, label: str) -> None:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", port))
        srv.listen()
        logging.info(f"[SERVER {self.domain}] {label} on 127.0.0.1:{port}")
        while True:
            sock, addr = srv.accept()
            threading.Thread(target=self.handle_client, args=(sock, addr), daemon=True).start()

    def run(self) -> None:
        t1 = threading.Thread(target=self._listen, args=(self.port, "S2S"), daemon=True)
        t2 = threading.Thread(target=self._listen, args=(self.port + 1000, "API"), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    MailServer().run()
