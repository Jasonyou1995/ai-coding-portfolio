import json
import uuid

import pytest

from common.protocol import (
    ACK,
    HELLO,
    KNOWN_TYPES,
    ProtocolError,
    UnknownMessageType,
    decode,
    encode,
    make_msg,
    require_known_type,
)


def test_roundtrip_encode_decode():
    """encode -> decode must return the original dict."""
    original = make_msg(HELLO, {"domain": "example.com"})
    wire = encode(original)
    assert wire.endswith(b"\n")
    restored = decode(wire)
    assert restored == original


def test_missing_field_raises():
    """A line missing a required field must raise ProtocolError."""
    for drop in ("type", "msg_id", "ts", "payload"):
        msg = make_msg(HELLO, {"domain": "x.com"})
        del msg[drop]
        line = encode(msg)
        with pytest.raises(ProtocolError):
            decode(line)


def test_make_msg_has_uuid_and_ts():
    """make_msg must inject a valid UUID4 msg_id and a numeric ts."""
    msg = make_msg(ACK, {"ref_msg_id": "abc", "status": "ok", "reason": None})

    # msg_id looks like a uuid4
    parsed = uuid.UUID(msg["msg_id"])
    assert parsed.version == 4

    # ts is a sensible float
    assert isinstance(msg["ts"], float)
    assert msg["ts"] > 0

    # payload is untouched
    assert msg["payload"] == {"ref_msg_id": "abc", "status": "ok", "reason": None}


def test_unknown_type_still_decoded_but_handler_raises():
    """Decode must accept unknown types; semantic validation is separate."""
    msg = make_msg("BOGUS", {"extra": 42})
    wire = encode(msg)

    # structural decode succeeds
    decoded = decode(wire)
    assert decoded["type"] == "BOGUS"
    assert decoded["payload"] == {"extra": 42}

    # semantic check raises
    with pytest.raises(UnknownMessageType):
        require_known_type(decoded)
