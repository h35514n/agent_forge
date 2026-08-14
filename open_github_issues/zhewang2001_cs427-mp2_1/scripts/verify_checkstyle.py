#!/usr/bin/env python3

"""verify_checkstyle

Verify that a patch wires the Maven Checkstyle plugin into a project's
pom.xml using the default Sun/Oracle ruleset, binds
`mvn checkstyle:check` to the standard Maven build lifecycle, and that
the codebase passes Checkstyle with zero violations.

Usage:
    ./verify_checkstyle.py <repo_root>

Exits 0 if all acceptance criteria are satisfied, 1 otherwise.

Acceptance Criteria covered:

  1. Checkstyle plugin added to pom.xml with default Sun/Oracle configuration
  2. `mvn checkstyle:check` is bound to the Maven build lifecycle
  3. Codebase passes this Checkstyle configuration with 0 violations
"""

import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# Helpers


POM_NS = "http://maven.apache.org/POM/4.0.0"


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def find_child(elem, name: str):
    for child in elem:
        if strip_ns(child.tag) == name:
            return child
    return None


def find_children(elem, name: str):
    return [child for child in elem if strip_ns(child.tag) == name]


def text_of(elem) -> str:
    return (elem.text or "").strip() if elem is not None else ""


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return ""


def pass_(msg: str) -> None:
    print(f"  PASS  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def find_pom_files(root: Path) -> list[Path]:
    poms = sorted(root.rglob("pom.xml"))
    # Skip anything buried in a build/output directory.
    skip = {"target", "build", "out", ".git", "node_modules"}
    return [p for p in poms if not any(part in skip for part in p.relative_to(root).parts)]


def iter_checkstyle_plugins(pom_path: Path):
    """Yield (pom_path, plugin_element) for every maven-checkstyle-plugin
    declaration found in the given pom (under <build><plugins>,
    <build><pluginManagement><plugins>, and inside <profiles>)."""
    try:
        tree = ET.parse(str(pom_path))
    except ET.ParseError as exc:
        fail(f"{pom_path}: failed to parse XML ({exc})")
        return
    root = tree.getroot()

    locations = []

    build = find_child(root, "build")
    if build is not None:
        plugins = find_child(build, "plugins")
        if plugins is not None:
            locations.extend(find_children(plugins, "plugin"))
        pm = find_child(build, "pluginManagement")
        if pm is not None:
            pm_plugins = find_child(pm, "plugins")
            if pm_plugins is not None:
                locations.extend(find_children(pm_plugins, "plugin"))

    profiles = find_child(root, "profiles")
    if profiles is not None:
        for profile in find_children(profiles, "profile"):
            pbuild = find_child(profile, "build")
            if pbuild is None:
                continue
            pplugins = find_child(pbuild, "plugins")
            if pplugins is not None:
                locations.extend(find_children(pplugins, "plugin"))
            ppm = find_child(pbuild, "pluginManagement")
            if ppm is not None:
                ppm_plugins = find_child(ppm, "plugins")
                if ppm_plugins is not None:
                    locations.extend(find_children(ppm_plugins, "plugin"))

    for plugin in locations:
        artifact = text_of(find_child(plugin, "artifactId"))
        if artifact == "maven-checkstyle-plugin":
            yield plugin


# AC1: Checkstyle plugin declared with default Sun/Oracle ruleset

# Phases that bind into the standard Maven build lifecycle. Per the Maven
# Checkstyle plugin docs, `checkstyle:check` is conventionally bound to
# `verify`, but `validate` is also commonly used and is part of the
# default lifecycle.
LIFECYCLE_PHASES = {
    "validate",
    "initialize",
    "generate-sources",
    "process-sources",
    "generate-resources",
    "process-resources",
    "compile",
    "process-classes",
    "generate-test-sources",
    "process-test-sources",
    "generate-test-resources",
    "process-test-resources",
    "test-compile",
    "process-test-classes",
    "test",
    "prepare-package",
    "package",
    "pre-integration-test",
    "integration-test",
    "post-integration-test",
    "verify",
    "install",
    "deploy",
}


def check_plugin_declared(pom_files: list[Path]) -> tuple[bool, list[tuple[Path, ET.Element]]]:
    print("\n==> Check 1: maven-checkstyle-plugin declared with default Sun/Oracle ruleset")

    if not pom_files:
        fail("No pom.xml found in repository")
        return False, []

    found: list[tuple[Path, ET.Element]] = []
    for pom in pom_files:
        for plugin in iter_checkstyle_plugins(pom):
            found.append((pom, plugin))

    if not found:
        fail("maven-checkstyle-plugin not declared in any pom.xml")
        return False, []

    ok = True
    for pom, plugin in found:
        rel = pom
        try:
            rel = pom.relative_to(pom.parents[len(pom.parents) - 1])
        except Exception:
            pass
        pass_(f"maven-checkstyle-plugin declared in {pom}")

        # Sun/Oracle ruleset is the plugin's default. It is acceptable to
        # either (a) omit <configLocation> entirely, or (b) explicitly set
        # it to the bundled "sun_checks.xml". Anything else (e.g. a
        # google_checks.xml or a custom file) violates the AC.
        config_locations: list[str] = []

        def collect_config_locations(elem):
            cl = find_child(elem, "configLocation")
            if cl is not None:
                config_locations.append(text_of(cl))

        collect_config_locations(find_child(plugin, "configuration") or ET.Element("x"))
        executions = find_child(plugin, "executions")
        if executions is not None:
            for execution in find_children(executions, "execution"):
                config = find_child(execution, "configuration")
                if config is not None:
                    collect_config_locations(config)

        if not config_locations:
            pass_(f"{pom}: no <configLocation> set -- defaults to Sun/Oracle ruleset")
        else:
            for loc in config_locations:
                if re.search(r"sun[_\-]?checks(\.xml)?$", loc, re.I) or loc.lower() in {
                    "sun_checks.xml",
                    "config/sun_checks.xml",
                }:
                    pass_(f"{pom}: configLocation set to Sun/Oracle ruleset ({loc!r})")
                else:
                    fail(
                        f"{pom}: configLocation={loc!r} is not the default Sun/Oracle "
                        "ruleset (expected sun_checks.xml or no configLocation)"
                    )
                    ok = False

    return ok, found


# AC2: `checkstyle:check` bound to the Maven build lifecycle

def check_lifecycle_binding(found: list[tuple[Path, ET.Element]]) -> bool:
    print("\n==> Check 2: mvn checkstyle:check bound to the Maven build lifecycle")

    if not found:
        fail("Cannot verify lifecycle binding -- plugin not declared")
        return False

    ok = False
    for pom, plugin in found:
        executions = find_child(plugin, "executions")
        if executions is None:
            continue

        for execution in find_children(executions, "execution"):
            goals = find_child(execution, "goals")
            goal_names = []
            if goals is not None:
                goal_names = [text_of(g) for g in find_children(goals, "goal")]
            if "check" not in goal_names:
                continue

            phase_elem = find_child(execution, "phase")
            phase = text_of(phase_elem)
            # If <phase> is omitted, the plugin's default phase for the
            # `check` goal applies (`verify`), which IS in the standard
            # lifecycle, so this still satisfies the AC.
            if not phase:
                pass_(
                    f"{pom}: execution binds goal 'check' with no explicit phase "
                    "(defaults to 'verify' -- part of the standard lifecycle)"
                )
                ok = True
            elif phase in LIFECYCLE_PHASES:
                pass_(f"{pom}: execution binds goal 'check' to lifecycle phase '{phase}'")
                ok = True
            else:
                fail(
                    f"{pom}: execution binds goal 'check' to phase '{phase}', which "
                    "is not a standard Maven lifecycle phase"
                )

    if not ok:
        fail(
            "No <execution> binds the 'check' goal to a standard lifecycle phase. "
            "Add an <execution> with <goals><goal>check</goal></goals> under the "
            "maven-checkstyle-plugin."
        )

    return ok


# AC3: `mvn checkstyle:check` reports zero violations

def check_zero_violations(root: Path) -> bool:
    print("\n==> Check 3: mvn checkstyle:check reports 0 violations")

    mvn = shutil.which("mvn")
    if not mvn:
        fail("`mvn` not found on PATH -- cannot run Checkstyle")
        return False

    cmd = [mvn, "-B", "-q", "-f", str(root / "pom.xml"), "checkstyle:check"]
    print(f"  Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root))
    except OSError as exc:
        fail(f"Failed to invoke Maven: {exc}")
        return False

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    combined = stdout + stderr

    if result.returncode == 0:
        pass_("mvn checkstyle:check exited 0 -- no violations reported")
        return True

    fail(f"mvn checkstyle:check exited {result.returncode}")

    violations = re.findall(
        r"There (?:is|are) (\d+) error[s]? reported by Checkstyle",
        combined,
    )
    if violations:
        total = sum(int(v) for v in violations)
        fail(f"Checkstyle reported {total} violation(s)")

    tail = combined.strip().splitlines()[-40:]
    if tail:
        print("  --- last lines of Maven output ---")
        for line in tail:
            print(f"  {line}")
        print("  --- end Maven output ---")

    return False


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <repo_root>", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    pom_files = find_pom_files(root)

    plugin_ok, found = check_plugin_declared(pom_files)
    binding_ok = check_lifecycle_binding(found)
    violations_ok = check_zero_violations(root)

    results = [plugin_ok, binding_ok, violations_ok]

    print()
    if all(results):
        print("OVERALL: PASS -- all acceptance criteria satisfied")
        sys.exit(0)
    else:
        failed = sum(1 for r in results if not r)
        print(f"OVERALL: FAIL -- {failed}/{len(results)} check(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
