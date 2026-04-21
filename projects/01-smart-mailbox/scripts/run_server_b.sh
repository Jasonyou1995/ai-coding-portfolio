#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
export DOMAIN=b.mail PORT=9002 PEER_DOMAIN=a.mail PEER_PORT=9001
exec uv run python -m server.main
