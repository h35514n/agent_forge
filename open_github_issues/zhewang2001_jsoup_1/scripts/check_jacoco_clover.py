#!/usr/bin/env python3

"""check_jacoco_clover

Verify that a patch correctly:

1. Adds JaCoCo plugin to pom.xml with required goals
2. Generates both JaCoCo and Clover coverage reports (runs Maven if needed)
3. Creates a comparison file listing lines covered by one tool but not the other

Usage:
    ./check_jacoco_clover.py <repo_root>

Exits 0 if all acceptance criteria are satisfied, 1 otherwise.
"""

import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# Helpers
# -------
def pass_(msg: str) -> None:
    print(f"  PASS  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return ""


def find_mvn() -> str | None:
    """Return path to mvn binary, or None."""
    for candidate in [
        "/opt/apache-maven-3.8.6/bin/mvn",
        "/opt/apache-maven-3.9.0/bin/mvn",
        "/usr/share/maven/bin/mvn",
        "/usr/bin/mvn",
    ]:
        if Path(candidate).is_file():
            return candidate
    return shutil.which("mvn")


# AC 1: JaCoCo plugin correctly added to pom.xml
def check_jacoco_in_pom(root: Path) -> bool:
    print("\n==> Check 1: JaCoCo plugin is correctly added to pom.xml")

    pom = root / "pom.xml"
    if not pom.exists():
        fail("pom.xml not found")
        return False

    text = read_text(pom)

    if "jacoco" not in text.lower():
        fail("jacoco-maven-plugin not found in pom.xml")
        return False

    # Validate XML is well-formed
    try:
        tree = ET.parse(pom)
    except ET.ParseError as exc:
        fail(f"pom.xml is not valid XML: {exc}")
        return False

    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    root_elem = tree.getroot()

    # Locate the JaCoCo plugin element (handle both namespaced and bare poms)
    jacoco_plugin = None
    for plugin in root_elem.iter():
        if plugin.tag in ("artifactId", "{http://maven.apache.org/POM/4.0.0}artifactId"):
            if plugin.text and "jacoco" in plugin.text.lower():
                jacoco_plugin = plugin
                break

    if jacoco_plugin is None:
        fail("jacoco-maven-plugin not found in pom.xml <plugins> section")
        return False

    pass_("jacoco-maven-plugin found in pom.xml")

    plugin_text = text[text.lower().find("jacoco") :]
    if "prepare-agent" not in plugin_text:
        fail("JaCoCo plugin is missing 'prepare-agent' goal execution")
        return False
    pass_("JaCoCo plugin has 'prepare-agent' goal configured")

    return True


# AC 2: Both JaCoCo and Clover reports generated
def _run_mvn(root: Path, mvn: str, *goals: str, timeout: int = 600) -> subprocess.CompletedProcess:
    cmd = [mvn, "-f", str(root / "pom.xml"), *goals, "--batch-mode", "-q"]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=root)


def _jacoco_report_exists(root: Path) -> Path | None:
    for candidate in [
        root / "target/site/jacoco/jacoco.xml",
        root / "target/site/jacoco/index.html",
    ]:
        if candidate.exists():
            return candidate
    return None


def _clover_report_exists(root: Path) -> Path | None:
    for candidate in [
        root / "target/clover/clover.xml",
        root / "target/site/clover/index.html",
        root / "target/clover.xml",
        root / "target/site/clover/clover.xml",
    ]:
        if candidate.exists():
            return candidate
    return None


def check_reports_generated(root: Path) -> bool:
    print("\n==> Check 2: Both JaCoCo and Clover reports are successfully generated")

    jacoco = _jacoco_report_exists(root)
    clover = _clover_report_exists(root)

    if jacoco and clover:
        pass_(f"JaCoCo report found: {jacoco.relative_to(root)}")
        pass_(f"Clover report found:  {clover.relative_to(root)}")
        return True

    # Reports not found yet – try running Maven
    mvn = find_mvn()
    if mvn is None:
        if not jacoco:
            fail("JaCoCo report not found (target/site/jacoco/) and mvn not available to generate it")
        if not clover:
            fail("Clover report not found (target/clover/) and mvn not available to generate it")
        return False

    print(f"  Running Maven to generate reports (mvn={mvn}) …")

    # Build + JaCoCo report
    result = _run_mvn(root, mvn, "clean", "test", "jacoco:report")
    jacoco = _jacoco_report_exists(root)
    if jacoco:
        pass_(f"JaCoCo report generated: {jacoco.relative_to(root)}")
    else:
        fail(f"'mvn clean test jacoco:report' completed (exit {result.returncode}) but no JaCoCo report found")
        if result.stdout:
            print(result.stdout[-1000:])
        if result.stderr:
            print(result.stderr[-1000:])

    # Clover report via OpenClover Maven plugin
    result2 = _run_mvn(root, mvn, "clover:setup", "test", "clover:aggregate", "clover:report")
    clover = _clover_report_exists(root)
    if clover:
        pass_(f"Clover report generated: {clover.relative_to(root)}")
    else:
        fail(
            f"'mvn clover:setup test clover:aggregate clover:report' completed (exit {result2.returncode}) but no Clover report found"
        )
        if result2.stdout:
            print(result2.stdout[-1000:])
        if result2.stderr:
            print(result2.stderr[-1000:])

    return bool(jacoco and clover)


# AC 3: Comparison file listing coverage differences
def check_comparison_file(root: Path) -> bool:
    print("\n==> Check 3: Comparison file listing JaCoCo vs Clover coverage differences")

    # Search the repo (excluding target/) for a comparison file
    candidates: list[Path] = []
    skip_dirs = {"target", ".git", "node_modules"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        name_lower = path.name.lower()
        if any(
            kw in name_lower
            for kw in ("comparison", "coverage_diff", "jacoco_clover", "clover_jacoco", "coverage_compare")
        ):
            candidates.append(path)

    # Broaden: look for any text file that references both tools
    if not candidates:
        for path in root.rglob("*"):
            if any(part in skip_dirs for part in path.parts):
                continue
            if not path.is_file():
                continue
            if path.suffix not in (".txt", ".csv", ".md", ".json", ".xml", ""):
                continue
            text = read_text(path)
            if re.search(r"jacoco", text, re.I) and re.search(r"clover", text, re.I):
                # Must look like a diff/comparison (not just pom.xml)
                if re.search(r"covered|not covered|only in|difference|line", text, re.I):
                    candidates.append(path)

    if not candidates:
        fail(
            "No comparison file found. Expected a file listing lines covered by JaCoCo but not Clover (and vice versa)."
        )
        return False

    comp_file = candidates[0]
    text = read_text(comp_file)
    pass_(f"Comparison file found: {comp_file.relative_to(root)}")

    has_jacoco = bool(re.search(r"jacoco", text, re.I))
    has_clover = bool(re.search(r"clover", text, re.I))

    if not (has_jacoco and has_clover):
        fail(f"{comp_file.name}: file does not reference both JaCoCo and Clover")
        return False
    pass_("Comparison file references both JaCoCo and Clover")

    return True


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <repo_root>", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = [
        check_jacoco_in_pom(root),
        check_reports_generated(root),
        check_comparison_file(root),
    ]

    print()
    if all(results):
        print("OVERALL: PASS – all acceptance criteria satisfied")
        sys.exit(0)
    else:
        failed = sum(1 for r in results if not r)
        print(f"OVERALL: FAIL – {failed}/{len(results)} check(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
