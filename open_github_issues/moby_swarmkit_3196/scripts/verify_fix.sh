#!/usr/bin/env bash
# Verify the fix for moby/swarmkit#3196 (goroutine leak in peer.go:stop).
#
# Strategy:
#   1. Confirm the transport package still builds.
#   2. Run TestSendRemoved (transport_test.go:129) — the test the upstream
#      reporter cited as reproducing the leak with goleak.
#   3. Drop in a small goleak-instrumented variant of TestSendRemoved so the
#      verification actually fails when the leak is present.
#
# Exits 0 on success, non-zero otherwise.
set -euo pipefail

cd /testbed

echo "[verify-fix] Go version:"
go version

echo "[verify-fix] Ensuring go.uber.org/goleak is available..."
go get go.uber.org/goleak@v1.3.0
go mod tidy

PKG_DIR="manager/state/raft/transport"

echo "[verify-fix] Building $PKG_DIR..."
go build ./$PKG_DIR/...

cat > "$PKG_DIR/leakcheck_3196_test.go" <<'EOF'
package transport

import (
	"context"
	"testing"

	"github.com/moby/swarmkit/v2/manager/state/raft/membership"
	"github.com/stretchr/testify/require"
	"go.uber.org/goleak"
	raftpb "go.etcd.io/raft/v3/raftpb"
)

// TestSendRemovedNoLeak mirrors TestSendRemoved (transport_test.go:129) but
// asserts that no goroutines leak after the cluster stops. This is the check
// the upstream issue reporter described.
func TestSendRemovedNoLeak(t *testing.T) {
	defer goleak.VerifyNone(t,
		// Ignore long-lived goroutines unrelated to the peer/grpc stop path.
		goleak.IgnoreTopFunction("go.opencensus.io/stats/view.(*worker).start"),
		goleak.IgnoreTopFunction("go.opencensus.io/trace.(*defaultIDGenerator).NewSpanID"),
	)

	ctx, cancel := context.WithCancel(context.Background())
	c := newCluster()
	defer func() {
		cancel()
		c.Stop()
	}()
	require.NoError(t, c.Add(1))
	require.NoError(t, c.Add(2))
	require.NoError(t, c.Add(3))
	require.NoError(t, c.Get(1).RemovePeer(2))

	err := sendMessages(ctx, c, 1, []uint64{2, 3}, raftpb.MsgHup)
	require.Error(t, err)
	require.Contains(t, err.Error(), "to removed member")
	_ = membership.ErrMemberRemoved
}
EOF

echo "[verify-fix] Running TestSendRemoved + TestSendRemovedNoLeak..."
go test -count=1 -timeout 180s -run 'TestSendRemoved|TestSendRemovedNoLeak' ./$PKG_DIR/...

echo "[verify-fix] PASS"
