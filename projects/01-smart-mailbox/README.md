# Smart Mailbox

A security-first email system using raw TCP/TLS and logical server isolation.

## Quickstart

```bash
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
./scripts/run_server_a.sh
./scripts/run_server_b.sh
```

## Architecture

```text
  [Client A] ----> [Server A]
                      |
                      v
  [Client B] <---- [Server B]
```

## Structure

- `server/`: Server logic for TCP/TLS handling and storage.
- `client/`: CLI client for secure communication.
- `common/`: Shared protocols and cryptographic utilities.
- `scripts/`: Operational scripts for management.
- `tests/`: Pytest suite for validation.
