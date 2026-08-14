#!/usr/bin/env python3

"""check_checkstyle

Verify that a patch correctly sets up the Checkstyle Gradle plugin for the
app module with a versioned ruleset, proper generated-code exclusions, and
a GitHub Actions workflow.

Usage:
    ./check_checkstyle <repo_root>

Exits 0 if all acceptance criteria are satisfied, 1 otherwise.
"""

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# Helpers


def find_files(root: Path, *patterns: str) -> list[Path]:
    results = []
    for pattern in patterns:
        results.extend(root.glob(pattern))
    return results


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return ""


def pass_(msg: str) -> None:
    print(f"  PASS  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


# Check 1 – Versioned Checkstyle ruleset committed


def check_ruleset(root: Path) -> bool:
    print("\n==> Check 1: Versioned Checkstyle ruleset committed")

    candidates = find_files(
        root,
        "**/checkstyle*.xml",
        "config/checkstyle/*.xml",
        "app/config/checkstyle/*.xml",
    )
    if not candidates:
        fail("No Checkstyle XML ruleset file found in the repository")
        return False

    ruleset = candidates[0]
    print(f"  Found ruleset: {ruleset.relative_to(root)}")
    text = read_text(ruleset)

    required_modules = {
        "naming conventions": [
            "ConstantName",
            "LocalVariableName",
            "MemberName",
            "MethodName",
            "PackageName",
            "TypeName",
        ],
        "imports": ["AvoidStarImport", "UnusedImports", "IllegalImport"],
        "whitespace": [
            "WhitespaceAround",
            "WhitespaceAfter",
            "NoWhitespaceBefore",
            "GenericWhitespace",
        ],
        "braces": ["NeedBraces", "LeftCurly", "RightCurly"],
        "common bugs": [
            "EqualsHashCode",
            "MissingSwitchDefault",
            "DefaultComesLast",
            "FallThrough",
        ],
        "modifier order": ["ModifierOrder"],
        "line length 120": ["LineLength"],
    }

    ok = True
    for category, modules in required_modules.items():
        if not any(m in text for m in modules):
            fail(f"Ruleset missing {category} checks (expected one of: {modules})")
            ok = False
        else:
            pass_(f"Ruleset includes {category} checks")

    if "LineLength" in text and "120" not in text:
        fail("LineLength rule found but max is not set to 120")
        ok = False
    elif "LineLength" in text:
        pass_("LineLength max=120 configured")

    return ok


# Check 2 – Checkstyle wired into app Gradle build; ignoreFailures=false


def check_gradle_config(root: Path) -> bool:
    print("\n==> Check 2: Checkstyle Gradle plugin applied to app module")

    build_files = find_files(root, "app/build.gradle", "app/build.gradle.kts")
    if not build_files:
        fail("app/build.gradle (or .kts) not found")
        return False

    ok = True
    for bf in build_files:
        text = read_text(bf)
        name = bf.relative_to(root)

        if not re.search(r"['\"]checkstyle['\"]|apply\s+plugin.*checkstyle|id\(['\"]checkstyle", text, re.I):
            fail(f"{name}: 'checkstyle' plugin not applied")
            ok = False
        else:
            pass_(f"{name}: checkstyle plugin applied")

        exclusion_patterns = [
            r"R\.java",
            r"BuildConfig",
            r"generated",
            r"exclude.*R\b",
            r"exclude.*Build",
        ]
        if not any(re.search(p, text, re.I) for p in exclusion_patterns):
            fail(
                f"{name}: no generated-code exclusions found "
                "(expected exclusions for R.java / BuildConfig / generated paths)"
            )
            ok = False
        else:
            pass_(f"{name}: generated-code exclusions present")

        if re.search(r"ignoreFailures\s*=\s*true", text, re.I):
            fail(f"{name}: ignoreFailures=true – violations will NOT fail the build")
            ok = False
        else:
            pass_(f"{name}: ignoreFailures is not set to true")

    return ok


# Check 3 – ./gradlew checkstyleMain / checkstyleTest executes and reports


def check_gradle_run(root: Path) -> bool:
    print("\n==> Check 3: ./gradlew checkstyleMain / checkstyleTest executes")

    gradlew = root / "gradlew"
    if not gradlew.exists() or not (gradlew.stat().st_mode & 0o111):
        fail(f"gradlew not found or not executable at {gradlew}")
        return False

    result = subprocess.run(
        [str(gradlew), "-p", str(root), "checkstyleMain", "checkstyleTest", "--continue", "--quiet"],
        capture_output=True,
        text=True,
    )

    task_not_found = re.search(
        r"Task.*checkstyle.*not found|Could not determine.*checkstyle",
        (result.stderr or "") + (result.stdout or ""),
        re.I,
    )
    if task_not_found:
        fail("checkstyleMain / checkstyleTest tasks not found – plugin not configured")
        print((result.stdout or "")[-1500:])
        print((result.stderr or "")[-1500:])
        return False

    if result.returncode == 0:
        pass_("checkstyleMain/checkstyleTest ran and found no violations")
    else:
        pass_(f"checkstyleMain/checkstyleTest ran and correctly fails on violations (exit {result.returncode})")

    report_paths = list(root.glob("app/build/reports/checkstyle/*.xml"))
    if report_paths:
        pass_(f"Checkstyle report produced: {report_paths[0].relative_to(root)}")
    else:
        fail("Checkstyle XML report not found under app/build/reports/checkstyle/")
        return False

    return True


# Check 4 – GitHub Actions workflow: triggers, command, artifact upload


def check_workflow(root: Path) -> bool:
    print("\n==> Check 4: GitHub Actions workflow for Checkstyle")

    workflow_files = find_files(root, ".github/workflows/*.yml", ".github/workflows/*.yaml")
    if not workflow_files:
        fail("No GitHub Actions workflow files found under .github/workflows/")
        return False

    ok = False
    matched: list[str] = []

    for wf in workflow_files:
        text = read_text(wf)
        name = wf.relative_to(root)

        if not re.search(r"checkstyleMain.*checkstyleTest|checkstyleTest.*checkstyleMain|gradlew.*checkstyle", text):
            continue

        ok = True
        matched.append(str(name))
        print(f"  Found checkstyle workflow: {name}")

        push_main = bool(
            re.search(
                r"on:.*?push:.*?branches:.*?-\s*['\"]?main['\"]?",
                text,
                re.S,
            )
        )
        if push_main:
            pass_(f"{name}: triggers on push to main")
        else:
            fail(f"{name}: no push-to-main trigger found")
            ok = False

        if "pull_request" in text:
            pass_(f"{name}: triggers on pull_request")
        else:
            fail(f"{name}: no pull_request trigger found")
            ok = False

        if re.search(r"upload-artifact|actions/upload-artifact", text, re.I):
            pass_(f"{name}: Checkstyle report uploaded as workflow artifact")
        else:
            fail(f"{name}: no artifact upload step found (expected actions/upload-artifact)")
            ok = False

    if not matched:
        fail("No workflow found that runs checkstyleMain/checkstyleTest via gradlew")
        return False

    return ok


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <repo_root>", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = [
        check_ruleset(root),
        check_gradle_config(root),
        check_gradle_run(root),
        check_workflow(root),
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
