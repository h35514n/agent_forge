#!/bin/bash

set -e

echo "[verify_fix] Verifying Lekensteyn/dmg2img issue #10 fix"

cd /testbed

echo "[verify_fix] Installing build dependencies"
apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    zlib1g-dev \
    libbz2-dev \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*

echo "[verify_fix] Building dmg2img with AddressSanitizer..."
make clean || true
make dmg2img CC=clang LDFLAGS=-fsanitize=address

echo "[verify_fix] Attempting to reproduce segfault..."
if ./dmg2img -i /scripts/heap-overflow-adc-66 -o /dev/null; then
  echo "Success!"
  exit 0
else
  echo "No good."
  exit 1
fi
