#!/usr/bin/env bash

set -euo pipefail

# Issue Description:
#
# Miss constraint checking for packet fields while doing decoding
#
# - IPv6: During decoding, miss check for the version field being equal to 6
#
# - DHCP: Miss validation checking for OP(op == 1 || op == 2 ),htype(htype > 0), hlen field
#
# - TCPL Miss validation checking for DataOffset( DataOffset >= 5 && DataOffset <= 15 && len >= 4 * DataOffset), Reserved field(Reserved == 0), and check for truncated packet.
#

# Tests:
cd /testbed

python3 -m pip install tox six pycryptodomex pyasn1
python3 -m pip install -r requirements-test.txt
python3 -m pip install -r requirements.txt

python3 -m pytest -k "IP6 or TCP or DHCP" -m "not remote"
