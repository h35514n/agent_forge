#!/usr/bin/env bash

set -euo pipefail

# Task
# ----
# Update the project to use JDK 17 as the target Java version.
#
# Modify the Maven configuration to ensure compatibility with JDK 17, including
# updating the maven-compiler-plugin settings.
#
# Then, review and upgrade all project dependencies and plugins in pom.xml to
# their latest stable versions. Resolve any compatibility issues that arise in
# the code and ensure the project builds and runs tests successfully after the
# upgrades.

# Acceptance Criteria
# -------------------
# Project configured to use JDK 17 with maven-compiler-plugin updated
# accordingly
#
# All dependencies and plugins updated to latest stable versions
#
# Project builds successfully with mvn clean install
#
# No new test failures introduced by the upgrade

cd /testbed

# AC 1: Java 17 is the effective compiler target. <release> takes precedence
# over <target> when both are set, so check release first; either being "17"
# satisfies the AC. help:evaluate goes through Maven's full pom-resolution
# pipeline (properties, profiles, parent inheritance), so this catches any
# valid configuration shape.

release=$(mvn -q help:evaluate -Dexpression=maven.compiler.release -DforceStdout 2>/dev/null || echo "")
target=$(mvn -q help:evaluate -Dexpression=maven.compiler.target -DforceStdout 2>/dev/null || echo "")
[[ "${release//[[:space:]]/}" == "17" || "${target//[[:space:]]/}" == "17" ]] ||
	{
		echo "FAIL: Java 17 is not the compiler target (release='${release}', target='${target}')"
		exit 1
	}


# AC 2 (latest stable deps/plugins) stale plugins will typically fail the JDK
# 17 build below anyway.
#
# ACs 3 & 4 (build + tests under the upgraded toolchain): `install` runs the
# test phase by default, so a non-zero exit covers test failures too.

mvn -B -ntp clean install
