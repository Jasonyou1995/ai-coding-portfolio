#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
export DOMAIN=a.mail PORT=9001 PEER_DOMAIN=b.mail PEER_PORT=9002
exec uv run python -m server.main
