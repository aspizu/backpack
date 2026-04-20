#!/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

docker run --rm -i -v "$(pwd)":/opt/backpack -v /opt/backpack/.venv/ ghcr.io/astral-sh/uv:debian bash <<EOF
cd /opt/backpack
uv sync
source .venv/bin/activate
bkpk doctor --fix
EOF
