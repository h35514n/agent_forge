#!/usr/bin/env bash

set -euo pipefail

# Task
# ----
# Refactor SBFLTest to use parameterized unit tests to eliminate duplicated
# test logic.
#
# Acceptance Criteria
# -------------------
# - All 5 original test cases are covered as parameterized inputs
# - Test logic is consolidated into a single @Test method
# - Parameterized tests compile and run via mvn test

cd /testbed

# Locate the (refactored) test source. Fail fast if it's missing or no
# parameterized infrastructure is wired in -- otherwise a single @Test that
# just contains 5 sequential asserts could pass the surefire-count check
# below for the wrong reason.
src=$(find . -path '*/src/test/java/*SBFLTest.java' -type f | head -n 1)
[[ -n "$src" ]] || {
	echo "FAIL: SBFLTest.java not found under src/test/java"
	exit 1
}
grep -qE '@ParameterizedTest|@RunWith\(Parameterized\.class\)' "$src" ||
	{
		echo "FAIL: SBFLTest does not use JUnit's parameterized test machinery"
		exit 1
	}

# AC 3: parameterized tests compile and run under mvn test.
mvn -B -ntp test

# Surefire emits one <testcase> per parameterized invocation. The report
# name encodes the fully-qualified class, so any TEST-*SBFLTest*.xml is ours.
report=$(find . -path '*/target/surefire-reports/TEST-*SBFLTest*.xml' -type f | head -n 1)
[[ -n "$report" ]] || {
	echo "FAIL: no SBFLTest surefire report found"
	exit 1
}

# AC 1: exactly 5 testcase invocations recorded.
tests=$(grep -oE 'tests="[0-9]+"' "$report" | head -n 1 | grep -oE '[0-9]+' || true)
[[ "$tests" == "5" ]] ||
	{
		echo "FAIL: expected 5 testcases in SBFLTest, got ${tests:-0}"
		exit 1
	}

# AC 2: all 5 invocations share a single base method name (one parameterized
# method, not five separate methods). Surefire encodes the case as
# "methodName[..]" or "methodName(...)"; strip from the first '[' or '('.
distinct=$(grep -oE 'name="[^"]+"' "$report" |
	sed -E 's/name="([^[(]+).*"/\1/' |
	sort -u | wc -l | tr -d ' ')
[[ "$distinct" == "1" ]] ||
	{
		echo "FAIL: expected 1 distinct test method, got $distinct"
		exit 1
	}

echo "PASS: 5 parameterized cases over 1 method, mvn test green"
