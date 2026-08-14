# zhewang2001/Project#1

Upstream Issue: https://github.com/zhewang2001/Project/issues/1\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/25

Target Issue: https://github.com/zhewang2001/Project/issues/1
Number of iterations: 7
Attempted mitigations: Tool implementation, custom config
Result: Unresolved 

## Motivation

The agent thrashed around a lot in early iterations trying to dig itself out of two holes: (1) irreparably mangling configuration files with `sed -i` edits, and (2) repeatedly getting confused about what kind of project it's working on then about the missing Java runtime, then when trying to install Java.


## Mitigation Details

1. Introduce a `str_replace` tool (a439621150af94b4ec77272f9474c161507c4b0a)

   Safer than using `sed -i`. Eliminated that class of failures -- the agent no longer mangled the gradle config and then churned trying to restore its previous state.

   The system prompt also had to be customized to explicitly steer the agent toward actually using tools. I ported this to the default github issue agent config on `main`, in less issue-specific terms, because the language used there explicitly biases the agent away from tool use.

2. Add custom config with Java image and installation (24d46b48dddb65ba76db10470efce1065be3ca06)

   The image used for the agent's Docker container is configurable, so changing it to an Android image (`ghcr.io/cirruslabs/android-sdk:34`) eliminated a lot of early thrashing.


## Results

Both mitigations were effective against the specific issues they targeted, but ultimately the agent couldn't get to a patch within the step / cost budget. 

This first issue was partly intended as recon and skirmishing to determine what infra tooling updates would be necessary, so I let it go long, but moving forward I'll work with a predefined time-box for these.


# zhewang2001/Project#2

Upstream Issue: https://github.com/zhewang2001/Project/issues/2\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/44

Target Issue: https://github.com/zhewang2001/Project/issues/2
Number of iterations:  1
Attempted mitigations: custom config, custom validation script
Result: Resolved

## Motivation

Running with the default config, the agent immediately ran into issues with an unset JAVA_HOME, so I ported the Java config used for other issues on this project. 


## Mitigations

The target issue helpfully articulates explicit acceptance criteria so I added a verification script that checks for each of them. This enabled to agent to iteratively satisfy the ACs.

## Results

A resolution was found in 80 steps. The patch initially did not apply cleanly, but that was due to a one-character bug (EOF newline) fixed in e799157, so I just fixed it manually and the patch applied cleanly and passed the verification script.

# zhewang2001/Project#3

Upstream Issue: https://github.com/zhewang2001/Project/issues/3\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/42

Target Issue: https://github.com/zhewang2001/Project/issues/3
Number of iterations: 1
Attempted mitigations: Tool implementation, custom config
Result: Resolved

## Motivation

Adopted learnings from #25. Validated by the use of `str_replace` in step 8, and a quick resolution in ten steps.

That said, the issue task was a bit trivial, since no source files needed annotation by the criteria specified in the issue.


## Mitigation Details

Same as in #25.

## Results

A patch was produced in 10 steps, consisting of a single-line addition of the `androidx.annotation` dependency and a backup copy of the edited gradle config.

# zhewang2001/Project#4

Upstream Issue: https://github.com/zhewang2001/Project/issues/4\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/43

Target Issue: https://github.com/zhewang2001/Project/issues/4
Number of iterations: 4
Attempted mitigations: custom config, tool, verification script
Result: Resolved

## Motivation

With the baseline modifications to the default config, a patch was generated successfully on the first attempt. Manual visual inspection gave the appearance of a valid resolution, but we had not yet implemented evaluation logic to validate the agent's decision to consider the issue resolved.

After implementing that logic (in f6875ef, 8c4e835, and 80593c4), other issues arose:

1. The original fix introduced a syntax error due to the lack of a `str_replace` tool
2. Backup files being retained and confusing the verifier script (for this issue, a linter check for hard-coded strings)
3. Build and gradle directories being retained and creating a corrupted patch.

## Mitigations

For (1): Porting the `str_replace` tool introduced for another issue

Also for (1): Adding a `verify_fix.sh` script, which delegates to a script checking the linter result for hard-coded strings.

For (2) and (3): Adding exclusions to the `git add` command used to generate the patch

## Results

Resolved in 4 iterations, in 44 steps on the successful iteration.

# zhewang2001/jsoup#1

Upstream Issue: https://github.com/zhewang2001/jsoup/issues/1\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/46

Target Issue: https://github.com/zhewang2001/jsoup/issues/1
Number of iterations: 3   
Attempted mitigations: All 3 options
Result: AC passed but a cleanly applied patch could not be produced in 3 iterations

## Motivation

Iteration 1: Max steps reached
Iteration 2: Success, but a bad patch (from build artifacts in the output)
Iteration 3: Success, but a bad patch (from whitespace changes in the output)

## Mitigations

Mitigation for 1: Add a custom config and a verification script encoding issue ACs
Mitigation for 2: Exclude binary output directories (one source of patch conflicts)
Mitigation for 3: None. Time boxed.

## Results

Unresolved

## Notes

- Substantively resolved, but a clean patch was not generated

# zhewang2001/cs427-mp2#1

Upstream Issue: https://github.com/zhewang2001/cs427-mp2/issues/1\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/47

Target Issue: https://github.com/zhewang2001/cs427-mp2/issues/1
Number of iterations: 2 
Attempted mitigations: Custom config, AC verification script   
Result: No Patch / Timeboxed 

## Motivation

Initial iteration churned writing and re-writing lines to config files without first orienting itself in the project. Second iteration actually made it to successfully running the autoformatter (Steps 14-17) but churned attempting to fix a subsequent build failure from missing dependencies and then getting into manual fixes of individual linter violations.

## Mitigations

Custom config with a maven image and explicit hints in the instance prompt to try using an autoformatter instead of manually correcting linter violations

## Results

- No patch, ran into environment issues (container not found)
- Had to timebox it because I was saturating my API rate limits

# zhewang2001/cs427-mp2#2

Upstream Issue: https://github.com/zhewang2001/cs427-mp2/issues/2\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/48

Target Issue: https://github.com/zhewang2001/cs427-mp2/issues/2
Number of iterations: 1  
Attempted mitigations: Custom config, verify script    
Result: Resolved    

## Motivation

For this instance, with API limits in mind, I just eagerly adopted all of the available improvements from previous runs on the zhewang2001 GitHub issues. Despite some stumbling on tricky JSON-encoded input (which informed an improvement to writer tools in 1668494), the agent recovered and produced a patch that applied cleanly and resolved the issue ACs.

## Mitigations

- Custom config: Includes a maven image and an explicit tip on how to upgrade a Maven project to JDK 17
- Verification script: Explicitly encodes the ACs as comments for reference and uses `mvn help:evaluate` and `mvn -B -ntp clean install` to validate the ACs.

## Results

- Issue Resolved
- Improvements to writer tools based on agent feedback

# zhewang2001/cs427-mp4#1

Upstream Issue: https://github.com/zhewang2001/cs427-mp4/issues/1\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/49

Target Issue: https://github.com/zhewang2001/cs427-mp4/issues/1
Number of iterations: 1    
Attempted mitigations: All of them, None of them   
Result: Resolved   

## Motivation

Any potential obstacles were headed off by improvements made for preceding work.

## Mitigations

None (specific to this run) were needed

## Results

As in #48, with API limits in mind, I took all improvements made thus far (current tool implementations for `verified-40` runs and learnings from past GitHub issue runs) as the starting point, and this allowed the agent to reach a resolution in 16 steps.

- Explicitly encoded ACs served as a TODO list, which are known to help keep agents on track
- Agent correctly figured out that specific test failures were expected becuase the implementation was still in an unfinished state.

<details>
<summary>Key steps</summary>

```
mini-swe-agent (step 12, $0.03):
THOUGHT: My apologies. I made an incorrect assumption. The original tests *also* fail with the same `expected:<...> but
was:<0.0>` error. This means the `SBFL.java` provided is indeed a stub, and the task is to refactor the tests *even
though* the underlying implementation is not complete. The problem statement says "Refactor SBFLTest to use JUnit
parameterized tests to eliminate duplicated test logic." It doesn't say "make the tests pass".

So, my previous refactoring was correct in terms of structure. The failures are due to the `SBFL` implementation, which
is outside the scope of this task.

I will re-apply the parameterized test refactoring.
```

```
mini-swe-agent (step 13, $0.03):
THOUGHT: I've reapplied the refactoring. I noticed a small error in the `getFileFromResource` method:
`getClass().getClass().getClassLoader()` should be `getClass().getClassLoader()`. I've corrected that in the
`write_file` command.

Now, I'll run `mvn -B -ntp test` again to verify that the parameterized tests compile and run, even if they fail due to
the `SBFL` implementation. The acceptance criteria are:
- [x] All 5 original test cases are covered as parameterized inputs
- [x] Test logic is consolidated into a single `@Test` method
- [ ] Parameterized tests compile and run via `mvn test` (this is what I'm checking now)

The key is that they *run*, meaning Surefire executes them and reports 5 test cases.

   mvn -B -ntp test

The key is that they *run*, meaning Surefire executes them and reports 5 test cases.

   mvn -B -ntp test
```

```
mini-swe-agent (step 16, $0.04):
THOUGHT: Great! The tests now run without `NullPointerException`s, and the output clearly shows "Tests run: 5, Failures:
5, Errors: 0, Skipped: 0". This confirms that:
- All 5 original test cases are covered as parameterized inputs.
- Test logic is consolidated into a single `@Test` method.
- Parameterized tests compile and run via `mvn test`.

The failures are expected because the `SBFL` implementation is a stub, as discussed. The task was to refactor the tests,
not to implement the `SBFL` logic.

I have met all the acceptance criteria.
I will now submit the task.
```
</details>

# moby/swarmkit#3196

Upstream Issue: https://github.com/moby/swarmkit/issues/3196\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/60

Target Issue: https://github.com/moby/swarmkit/issues/3196
Number of iterations: 2
Attempted mitigations: golang:1.24 image, issue-specific guidance, goleak verify_fix.sh
Result: Unresolved (verification flake, not fix defect)

## Motivation

`peer.cc` (a `*grpc.ClientConn`) was never `Close()`'d in `peer.stop()` — its background goroutines lingered after the run loop exited. Reporter cited a goleak repro in `TestSendRemoved` (`transport_test.go:129`).

## Mitigations

- **Iter 1**: default config baseline. ~5 steps wasted on `apt-get install golang` since `python:3.11` lacks Go.
- **Iter 2**: `golang:1.24` image, guidance pointing at `peer.go:stop()`, `verify_fix.sh` that drops in a goleak mirror of `TestSendRemoved`.

## Results

Iter 2 fix: `p.cc.Close()` under `p.mu` *after* `<-p.done`, with nil-check — safer than iter 1's *before*-`done` placement (which could race with `defer p.drain()` in `run()`).

Verification reports Unresolved because `TestSendRemoved` itself is intermittently flaky in the verify env (transient gRPC `TRANSIENT_FAILURE` during teardown), not because the fix is wrong. Agent reached the same conclusion (step 24).

## Observations

- `golang:1.24` image still hits `go: not found` because `bash -lc` (`DockerEnvironment.execute`) sources `/etc/profile`, which clobbers the Dockerfile-set PATH. Agent has to `export PATH=$PATH:/usr/local/go/bin`.
- Asserting goleak on top of an already-flaky base test is brittle — a standalone leak test would be more reliable.

<details>
<summary>Key steps</summary>

```
iter1 (step 5): THOUGHT: ... no explicit call to p.cc.Close() when the peer is stopped.
The peer.stop() method is the appropriate place to close p.cc. ... acquire p.mu before
accessing p.cc to ensure thread safety.
```

```
iter2 (step 24): THOUGHT: The test is still failing, but the output does not explicitly
indicate a goleak failure. ... If the goleak check passes, it means the leak is fixed,
even if other parts of the test suite might be failing for unrelated reasons.
```

</details>

# containerd/fifo#56

Upstream Issue: https://github.com/containerd/fifo/issues/56\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/61

Target Issue: https://github.com/containerd/fifo/issues/56
Number of iterations: 2
Attempted mitigations: golang:1.24 image, PATH guidance, heredoc-only edit guidance, goleak verify_fix.sh seeded with the reporter's TestFifoNocancel
Result: Resolved

## Motivation

`OpenFifo(context.Background(), ..., O_RDONLY|O_CREAT|O_NONBLOCK, 0600)` leaks goroutines: the first goroutine in `openFifo` blocks on `<-ctx.Done()` (never fires for `Background()`), the open never completes (NONBLOCK + RDONLY with no writer), and `f.opened`/`f.closed` never signal.

## Mitigations

- **Iter 1**: aborted at step 91. Agent spent 50+ steps fighting JSON-escaping in `str_replace`/`replace_lines`/`insert_lines`, broke the build, recovered one line at a time. No `traj.json.gz` since the run was killed before post-run archive.
- **Iter 2**: `golang:1.24`, instance template forces `export PATH=$PATH:/usr/local/go/bin` and heredoc-only edits. `eval.command` runs a script that drops in `TestFifoNocancel` verbatim from the issue body.

## Results

Resolved at step 19, $0.32. `TestFifoNocancel` FAIL → PASS. Fix adds `case <-f.closing:` to the first goroutine's select, plus a `defer f.Close()` on the `openFifo` error path so `closing` propagates and wakes the goroutines.

**Caveat:** the agent's whole-file rewrite dropped the upstream copyright header, the `//go:build !windows` constraint, and the `OpenFifoDup2` function. Those are regressions unrelated to the leak fix and would need to be restored before this could go upstream.

## Observations

- Setting `environment.env.PATH` in YAML is futile — `bash -lc` + Debian's `/etc/profile` resets PATH unconditionally. Must `export` in-command.
- Heredoc-only guidance up front turned a 91-step thrash into a 20-step success.
- A self-contained verification test (vs. asserting on the upstream test suite) gave a clean Resolved signal — compare PR #60.

<details>
<summary>Key steps</summary>

```
iter2 (step ~5):
[verify-fix] Running TestFifoNocancel...
--- FAIL: TestFifoNocancel (3.48s)   # leak reproduces pre-fix
```

```
iter2 (step ~19):
[verify-fix] Running TestFifoNocancel...
--- PASS: TestFifoNocancel (0.00s)
[verify-fix] PASS
```

</details>

# LibVNC/libvncserver#615

Upstream Issue: https://github.com/LibVNC/libvncserver/issues/615\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/62

Target Issue: https://github.com/LibVNC/libvncserver/issues/615
Number of iterations: 2
Attempted mitigations: gcc:13 image, out-of-source build guidance, heredoc-only edit guidance, verify_fix.sh that builds + statically checks for FD_SETSIZE bound in listenerRun
Result: Unresolved (patch malformed + lost FD_ZERO; agent intent was correct)

## Motivation

ASAN flagged a stack-buffer-overflow in `listenerRun` at `src/libvncserver/main.c:646`. `fd_set listen_fds` is a 1024-bit stack bitmap, but `FD_SET(fd, ...)` is called with `fd >= FD_SETSIZE` (the offset-336 access ASAN reported). Three sites: `listenSock`, `listen6Sock`, `pipe_notify_listener_thread[0]`.

## Mitigations

- **Iter 1**: agent identified the bug but ended in `Empty_Patch` — ran `cmake .` from `/testbed`, which polluted the tree and broke `git add -A` patch collection. Also fought `replace_lines` JSON-escaping and broke an `#endif`.
- **Iter 2**: `gcc:13`, instance template forces out-of-source builds (`/tmp/build`) and steers toward `git apply <<'EOF'`. `verify_fix.sh` builds vncserver out-of-source and greps `listenerRun` for `FD_SETSIZE`.

## Results

In-container `verify_fix.sh` PASSed at step 11 (build clean, FD_SETSIZE present). Eval still reports Unresolved for two distinct reasons:

1. **Malformed patch**: `git apply` rejects with "corrupt patch at line 42" — trailing context-line newline didn't survive cleanly.
2. **Regression in patch**: `replace_lines` ate the `FD_ZERO(&listen_fds);` line immediately before the first `FD_SET` block. Without `FD_ZERO`, stale bits persist across loop iterations.

The conceptual fix in the patch is correct (bounds-check + `<sys/select.h>` include + log on overflow). With `FD_ZERO` restored and the trailing-newline fixed, it would apply.

## Observations

- The default patch-collection pipeline is incompatible with any in-tree build. Out-of-source guidance is mandatory for C/CMake projects.
- Even with "use heredoc" guidance, the agent reached for `replace_lines` on what it judged a targeted edit — and again ate an adjacent line. For C, `git apply` with enough hunk context is the only reliable path.
- Static grep verification is cheap but trades coverage. It missed the `FD_ZERO` regression. A runtime reproducer (open 1100+ fds, drive listenerRun under ASAN) would have caught it but is well beyond the iteration budget.

<details>
<summary>Key steps</summary>

```
iter1 final ($0.10):
RuntimeError: Could not collect submission patch:
The following paths are ignored by one of your .gitignore files:
build
```

```
iter2 (step 11, $0.02):
[verify-fix] OK: listenerRun references FD_SETSIZE (bounds check present).
[verify-fix] PASS
```

```
iter2 eval:
[verify-patch] Applying patch...
error: corrupt patch at line 42
[github-issue] Verification: Unresolved
```

</details>

# alrevuelta/cONNXr#102

Upstream Issue: https://github.com/alrevuelta/cONNXr/issues/102\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/45

Target Issue: https://github.com/alrevuelta/cONNXr/issues/102
Number of iterations: 2  
Attempted mitigations: None needed
Result: Resolved

## Motivation

- First run was interrupted due to API limits and execution loop
- Reran the agent and manually extracted the final patch after confirming the fix

## Mitigations

None needed — only environmental issues (API rate limits) encountered on the first run.

## Results

Resolved. Agent added missing null checks for searchAttributeNyName in both Constant-12 and MaxPool-12.

# fortra/impacket#1902

Upstream Issue: https://github.com/fortra/impacket/issues/1902\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/52

Target Issue: https://github.com/fortra/impacket/issues/1902
Number of iterations: 7   
Attempted mitigations: custom config, verification script   
Result: Resolved   

## Motivation

In early iterations, the patch the agent would produce would not apply cleanly.
Additionally, errors from both the environment (missing pytest) and application (missing dependencies) were encountered when attempting to verify work naively by running pytest.

## Mitigations

- A custom config with tailored instructions
- A verify_fix.sh with project-specific testing commands

## Results

Resolved.


# swftools/swftools#109

Upstream Issue: https://github.com/swftools/swftools/issues/109\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/54

Target Issue: https://github.com/swftools/swftools/issues/109
Number of iterations:    1
Attempted mitigations: N/A  
Result: Resolved

## Motivation

N/A

## Mitigations

None needed -- reported as resolved without any mitigations.

## Results

Resolved. The patch applies cleanly and was verified manually.

# Lekensteyn/dmg2img#10

Upstream Issue: https://github.com/Lekensteyn/dmg2img/issues/10\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/55

Target Issue: https://github.com/Lekensteyn/dmg2img/issues/10
Number of iterations: 1
Attempted mitigations: Added a simple verification script for rebuilding dmg2img and rerunning the issue input.
Result: Unresolved

## Motivation

- Command and artifact to reproduce the issue provided in the issue description
- Custom build requirements described in the project README

## Mitigations

Added verify_fix.sh to verify a fix by building the project and attempt a reproduction 
Used a clang container image (in the eval — not made available to agent however)

## Results

In the trajectory, the agent downloaded the provided heap-overflow-adc-66.zip file, extracted it, and reran the issue command "./dmg2img -i ./heap-overflow-adc-66 -o /dev/null". After the patch, the program no longer segfaulted, so the agent concluded, considering the issue resolved.

However, when evaluating the patch, although we were able to build the project, it still segfaulted when attempting a reproduction as reported in the issue. Time constraints precluded investigating more deeply.

# jameswalmsley/bitthunder#57

Upstream Issue: https://github.com/jameswalmsley/bitthunder/issues/57\
Team PR: https://github.com/team408uiuc/cs427-agent-team408/pull/53

Target Issue: https://github.com/jameswalmsley/bitthunder/issues/57
Number of iterations: 3    
Attempted mitigations: None needed   
Result: N/A (Already resolved)    

## Motivation

Function `bt_system_init` does not return a value of type `BT_ERROR`.

## Mitigations

None needed — the issue is already resolved upstream.

## Results

Empty_Patch — the issue was already fixed in the current HEAD of the repository. The function `bt_system_init` in `os/src/bt_main.c` now correctly returns `Error` of type `BT_ERROR`. The agent correctly identified no changes were needed.

<!-- hrefs -->

[issue:zhewang2001/Project#1]: https://github.com/zhewang2001/Project/issues/1
[issue:zhewang2001/Project#2]: https://github.com/zhewang2001/Project/issues/2
[issue:zhewang2001/Project#3]: https://github.com/zhewang2001/Project/issues/3
[issue:zhewang2001/Project#4]: https://github.com/zhewang2001/Project/issues/4
[issue:zhewang2001/jsoup#1]: https://github.com/zhewang2001/jsoup/issues/1
[issue:zhewang2001/cs427-mp2#1]: https://github.com/zhewang2001/cs427-mp2/issues/1
[issue:zhewang2001/cs427-mp2#2]: https://github.com/zhewang2001/cs427-mp2/issues/2
[issue:zhewang2001/cs427-mp4#1]: https://github.com/zhewang2001/cs427-mp4/issues/1
[issue:moby/swarmkit#3196]: https://github.com/moby/swarmkit/issues/3196
[issue:containerd/fifo#56]: https://github.com/containerd/fifo/issues/56
[issue:LibVNC/libvncserver#615]: https://github.com/LibVNC/libvncserver/issues/615
[issue:alrevuelta/cONNXr#102]: https://github.com/alrevuelta/cONNXr/issues/102
[issue:fortra/impacket#1902]: https://github.com/fortra/impacket/issues/1902
[issue:swftools/swftools#109]: https://github.com/swftools/swftools/issues/109
[issue:Lekensteyn/dmg2img#10]: https://github.com/Lekensteyn/dmg2img/issues/10
[issue:jameswalmsley/bitthunder#57]: https://github.com/jameswalmsley/bitthunder/issues/57

[pr:zhewang2001/Project#1]: https://github.com/team408uiuc/cs427-agent-team408/pull/25
[pr:zhewang2001/Project#2]: https://github.com/team408uiuc/cs427-agent-team408/pull/44
[pr:zhewang2001/Project#3]: https://github.com/team408uiuc/cs427-agent-team408/pull/42
[pr:zhewang2001/Project#4]: https://github.com/team408uiuc/cs427-agent-team408/pull/43
[pr:zhewang2001/jsoup#1]: https://github.com/team408uiuc/cs427-agent-team408/pull/46
[pr:zhewang2001/cs427-mp2#1]: https://github.com/team408uiuc/cs427-agent-team408/pull/47
[pr:zhewang2001/cs427-mp2#2]: https://github.com/team408uiuc/cs427-agent-team408/pull/48
[pr:zhewang2001/cs427-mp4#1]: https://github.com/team408uiuc/cs427-agent-team408/pull/49
[pr:moby/swarmkit#3196]: https://github.com/team408uiuc/cs427-agent-team408/pull/60
[pr:containerd/fifo#56]: https://github.com/team408uiuc/cs427-agent-team408/pull/61
[pr:LibVNC/libvncserver#615]: https://github.com/team408uiuc/cs427-agent-team408/pull/62
[pr:alrevuelta/cONNXr#102]: https://github.com/team408uiuc/cs427-agent-team408/pull/45
[pr:fortra/impacket#1902]: https://github.com/team408uiuc/cs427-agent-team408/pull/52
[pr:swftools/swftools#109]: https://github.com/team408uiuc/cs427-agent-team408/pull/54
[pr:Lekensteyn/dmg2img#10]: https://github.com/team408uiuc/cs427-agent-team408/pull/55
[pr:jameswalmsley/bitthunder#57]: https://github.com/team408uiuc/cs427-agent-team408/pull/53
