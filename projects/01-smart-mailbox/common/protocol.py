"""Wire protocol V0.1 – NDJSON server-to-server messages."""

import json
import time
import uuid
from typing import Any, Dict, TypedDict


class ProtocolError(Exception):
    """Malformed or invalid protocol message."""


class UnknownMessageType(ProtocolError):
    """Message type is not recognised."""


# ---------------------------------------------------------------------------
# Typed payload shapes
# ---------------------------------------------------------------------------

class HelloPayload(TypedDict):
    domain: str


class RelayMailPayload(TypedDict):
    from_: str
    to: str
    subject: str
    body: str


class AckPayload(TypedDict):
    ref_msg_id: str
    status: str          # "ok" | "error"
    reason: str | None


# ---------------------------------------------------------------------------
# Message type constants
# ---------------------------------------------------------------------------

HELLO = "HELLO"
RELAY_MAIL = "RELAY_MAIL"
ACK = "ACK"

KNOWN_TYPES = {HELLO, RELAY_MAIL, ACK}

REQUIRED_FIELDS = ("type", "msg_id", "ts", "payload")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_msg(msg_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return a fresh message dict with auto-generated *msg_id* and *ts*."""
    return {
        "type": msg_type,
        "msg_id": str(uuid.uuid4()),
        "ts": time.time(),
        "payload": payload,
    }


def encode(msg: Dict[str, Any]) -> bytes:
    """Serialize *msg* to a single NDJSON line (appends ``\\n``)."""
    line = json.dumps(msg, separators=(",", ":"), ensure_ascii=False) + "\n"
    return line.encode("utf-8")


def decode(line: bytes) -> Dict[str, Any]:
    """Parse and structurally validate one NDJSON line.

    Raises:
        ProtocolError: JSON is broken or a required field is missing / wrong type.
    """
    try:
        text = line.decode("utf-8")
        msg = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"Invalid JSON: {exc}") from exc

    if not isinstance(msg, dict):
        raise ProtocolError("Message must be a JSON object")

    for field in REQUIRED_FIELDS:
        if field not in msg:
            raise ProtocolError(f"Missing required field: {field}")

    if not isinstance(msg["type"], str):
        raise ProtocolError("Field 'type' must be a string")
    if not isinstance(msg["msg_id"], str):
        raise ProtocolError("Field 'msg_id' must be a string")
    if not isinstance(msg["ts"], (int, float)):
        raise ProtocolError("Field 'ts' must be a number")
    if not isinstance(msg["payload"], dict):
        raise ProtocolError("Field 'payload' must be a JSON object")

    return msg


def require_known_type(msg: Dict[str, Any]) -> None:
    """Raise :exc:`UnknownMessageType` if *msg*['type'] is not a known constant."""
    msg_type = msg.get("type")
    if msg_type not in KNOWN_TYPES:
        raise UnknownMessageType(msg_type)
