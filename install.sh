#!/usr/bin/env bash
#
# Sindlish Installer for macOS and Linux.
#
# Installs the Sindlish interpreter from source:
#   - prefers `uv tool install` (fastest)
#   - falls back to `pipx install`
#   - last resort: plain `pip install --user`
#
# Press a packaged binary instead? Download it from the latest GitHub
# release: https://github.com/Sindlish/Sindlish/releases/latest

set -euo pipefail

REPO="Sindlish/Sindlish"
SOURCE_URL="git+https://github.com/${REPO}.git"

if command -v uv >/dev/null 2>&1; then
    echo "Installing Sindlish with uv..."
    uv tool install --from "${SOURCE_URL}" sindlish
    INSTALLED=1
elif command -v pipx >/dev/null 2>&1; then
    echo "Installing Sindlish with pipx..."
    pipx install "${SOURCE_URL}"
    INSTALLED=1
elif command -v python3 >/dev/null 2>&1; then
    echo "Installing Sindlish with pip --user..."
    python3 -m pip install --user "sindlish @ ${SOURCE_URL}"
    INSTALLED=1
else
    echo "Error: no supported installer found. Install uv (https://docs.astral.sh/uv) and re-run this script." >&2
    exit 1
fi

if [ "${INSTALLED:-0}" = "1" ]; then
    echo
    echo "Sindlish installed successfully! Try running 'sindlish' in your terminal."
fi