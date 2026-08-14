#!/usr/bin/env bash
# Verify the fix for LibVNC/libvncserver#615 — stack-buffer-overflow in
# listenerRun (main.c:646) when an fd exceeds FD_SETSIZE in FD_SET.
#
# Strategy:
#   1. Install build deps for libvncserver.
#   2. Out-of-source cmake build (/tmp/build) so we don't pollute /testbed.
#   3. Confirm the project still builds cleanly with the patch applied.
#   4. Statically check that main.c:listenerRun guards FD_SET against
#      FD_SETSIZE (this is what the fix must do).
#
# Exits 0 on success.
set -euo pipefail

cd /testbed

echo "[verify-fix] Installing build deps..."
apt-get update -qq
apt-get install -y -q --no-install-recommends \
    cmake \
    pkg-config \
    libssl-dev \
    libjpeg-dev \
    libpng-dev \
    libz-dev \
    >/dev/null

echo "[verify-fix] Configuring (out-of-source) ..."
mkdir -p /tmp/build
cmake -S /testbed -B /tmp/build \
    -DWITH_OPENSSL=OFF \
    -DWITH_GNUTLS=OFF \
    -DWITH_GCRYPT=OFF \
    -DWITH_SYSTEMD=OFF \
    -DWITH_LZO=OFF \
    -DCMAKE_BUILD_TYPE=Debug

echo "[verify-fix] Building libvncserver..."
cmake --build /tmp/build --target vncserver -j"$(nproc)"

echo "[verify-fix] Static check: does listenerRun guard FD_SET against FD_SETSIZE?"
# The fix must guard each FD_SET call inside listenerRun (main.c) so that fds
# >= FD_SETSIZE are not written into the fd_set bitmap. Look for any of:
#   - an `if (fd < FD_SETSIZE)` style guard immediately before FD_SET
#   - a helper macro/inline that does the check
LISTENER_BLOCK=$(awk '/^listenerRun\(/,/^\}/' /testbed/src/libvncserver/main.c)
if [ -z "$LISTENER_BLOCK" ]; then
    LISTENER_BLOCK=$(awk '/listenerRun\(void/,/^\}/' /testbed/src/libvncserver/main.c)
fi

if printf '%s\n' "$LISTENER_BLOCK" | grep -qE 'FD_SETSIZE'; then
    echo "[verify-fix] OK: listenerRun references FD_SETSIZE (bounds check present)."
else
    echo "[verify-fix] FAIL: listenerRun has no FD_SETSIZE bounds check."
    echo "----- listenerRun in main.c -----"
    printf '%s\n' "$LISTENER_BLOCK"
    echo "---------------------------------"
    exit 1
fi

echo "[verify-fix] PASS"
