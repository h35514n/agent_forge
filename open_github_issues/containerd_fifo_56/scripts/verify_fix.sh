#!/usr/bin/env bash
# Verify the fix for containerd/fifo#56 (goroutine leak in OpenFifo when called
# with O_RDONLY|O_CREAT|O_NONBLOCK and a non-cancellable context).
#
# Strategy:
#   1. Make sure go.uber.org/goleak is on go.mod.
#   2. Drop in TestFifoNocancel (verbatim from the issue body) as a *_test.go.
#   3. Run go test on that single test with goleak verification.
#
# Exits 0 on success.
set -euo pipefail

# golang:1.24 puts the toolchain at /usr/local/go/bin and only sets PATH for
# login shells, so non-login shell invocations need this added explicitly.
export PATH="$PATH:/usr/local/go/bin"

cd /testbed

echo "[verify-fix] Go version:"
go version

echo "[verify-fix] Ensuring go.uber.org/goleak is available..."
go get go.uber.org/goleak@v1.3.0
go mod tidy

echo "[verify-fix] Writing leak-detection test..."
cat > leakcheck_56_test.go <<'EOF'
package fifo

import (
	"context"
	"os"
	"path/filepath"
	"sync"
	"syscall"
	"testing"

	"github.com/stretchr/testify/assert"
	"go.uber.org/goleak"
)

// TestFifoNocancel mirrors the reproduction in containerd/fifo#56. Calling
// OpenFifo with O_RDONLY|O_CREAT|O_NONBLOCK and a non-cancellable context
// must not leak the internal goroutines after the call returns.
func TestFifoNocancel(t *testing.T) {
	defer goleak.VerifyNone(t)
	tmpdir, err := os.MkdirTemp("", "fifos")
	assert.NoError(t, err)
	defer os.RemoveAll(tmpdir)

	leakCheckWg = &sync.WaitGroup{}
	defer func() {
		leakCheckWg = nil
	}()

	_, _ = OpenFifo(
		context.Background(),
		filepath.Join(tmpdir, "f0"),
		syscall.O_RDONLY|syscall.O_CREAT|syscall.O_NONBLOCK,
		0600,
	)
	assert.NoError(t, checkWgDone(leakCheckWg))
}
EOF

echo "[verify-fix] Building..."
go build ./...

echo "[verify-fix] Running TestFifoNocancel..."
go test -count=1 -timeout 60s -run TestFifoNocancel -v .

echo "[verify-fix] PASS"
