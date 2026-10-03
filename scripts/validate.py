"""Small, offline repository checks. Only FULL writes generated website output."""

import argparse
from collections import Counter
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tokenize
import tomllib


ROOT = Path(__file__).resolve().parents[1]
COUNTS = Counter()
# Add a learning script only after reviewing its entire execution path for
# provider calls, writes, and network access. No current experiment qualifies.
OFFLINE_EXPERIMENTS = ()
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk-proj-|gsk_|ghp_|github_pat_)[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"),
    re.compile(r'''(?i)(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*["'][A-Za-z0-9_+/=-]{24,}["']'''),
)


def report(level, message):
    COUNTS[level] += 1
    print(f"[{level}] {message}")


def command(args, timeout=60):
    # Never echo subprocess output: a tool or hook could include credentials.
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(args, cwd=ROOT, env=env, capture_output=True,
                          timeout=timeout, check=False)


def git(*args):
    result = command(["git", *args])
    if result.returncode:
        raise RuntimeError("Git command failed")
    return result.stdout


def paths(*args):
    return [p.decode("utf-8") for p in git("ls-files", "-z", *args).split(b"\0") if p]


def forbidden(name):
    p = Path(name)
    return (any(part in {".venv", "venv", "__pycache__"} for part in p.parts)
            or (p.name.startswith(".env") and p.name != ".env.example")
            or p.name in {"id_rsa", "id_ed25519", "credentials.json", "service-account.json"}
            or p.suffix.lower() in {".key", ".p12", ".pfx"})


def redirected(path):
    """Reject symlinks and Windows junction/reparse points, including ancestors."""
    for part in (path, *path.parents):
        if part.is_symlink():
            return True
        if part.exists() and getattr(part.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            return True
        if part == ROOT:
            break
    return False


def read(name):
    path = ROOT / name
    if forbidden(name) or redirected(path) or not path.resolve().is_relative_to(ROOT):
        raise ValueError("Unsafe input path")
    return path.read_text(encoding="utf-8-sig")


def snapshot():
    # Include non-ignored untracked work, but never open real .env/credential files.
    names = set(paths()) | set(paths("--others", "--exclude-standard"))
    hashes = {}
    for name in names:
        path = ROOT / name
        if forbidden(name) or name.startswith(".website-build/"):
            continue
        if path.is_file() and not redirected(path):
            hashes[name] = hashlib.sha256(path.read_bytes()).digest()
    return git("status", "--porcelain=v1", "-z"), hashes


def fast(tracked):
    state = git("status", "--short").decode("utf-8").strip()
    report("PASS", "Git working tree: " + ("changes present (allowed)" if state else "clean"))
    if state:
        print(state)
    report("FAIL" if git("ls-files", "-u") else "PASS", "Git merge-conflict check")
    expected = read(".python-version").strip()
    actual = f"{sys.version_info.major}.{sys.version_info.minor}"
    report("PASS" if actual == expected else "FAIL", f"Python version {actual}; expected {expected}")
    for name in sorted({p for p in tracked if p.endswith('.toml')} | {"pyproject.toml", "uv.lock"}):
        try:
            data = tomllib.loads(read(name))
            if name == "pyproject.toml":
                # Explicit checks remain active under -O / PYTHONOPTIMIZE.
                if (not data["project"]["name"]
                        or not data["project"]["requires-python"]
                        or not (ROOT / data["project"]["readme"]).is_file()
                        or data["tool"]["uv"]["package"] is not False):
                    raise ValueError("Invalid project metadata")
            report("PASS", name)
        except (ValueError, OSError, KeyError, TypeError):
            report("FAIL", f"{name}: invalid TOML, metadata, or missing file")
    # Include this validator before the user stages the new file.
    python_files = sorted({p for p in tracked if p.endswith('.py')} | {"scripts/validate.py"})
    failures = 0
    for name in python_files:
        try:
            if forbidden(name) or redirected(ROOT / name):
                raise ValueError("Unsafe Python path")
            with tokenize.open(ROOT / name) as source:
                compile(source.read(), name, "exec")
        except (SyntaxError, UnicodeError, OSError, ValueError):
            failures += 1
            report("FAIL", f"Python syntax: {name} (source omitted)")
    if not failures:
        report("PASS", f"Python syntax ({len(python_files)} files; no imports executed)")
    bad = [p for p in tracked if forbidden(p)]
    report("FAIL" if bad else "PASS", f"Tracked credential/environment paths ({len(bad)} forbidden)")
    generated = [p for p in tracked if p.startswith('.website-build/')]
    safe = not generated
    for name in (".website-build/content/index.md", ".website-build/site/index.html"):
        ignored = command(["git", "check-ignore", "--no-index", "--quiet", name])
        safe = safe and ignored.returncode == 0
    for name in (".website-build", ".website-build/content", ".website-build/site"):
        safe = safe and not redirected(ROOT / name)
    if safe and (ROOT / '.website-build').exists():
        for base, folders, files in os.walk(ROOT / '.website-build', followlinks=False):
            if any(redirected(Path(base) / name) for name in folders + files):
                safe = False
                break
    report("PASS" if safe else "FAIL", "Generated output: ignored, untracked, no redirected output roots")
    for name in tracked:
        if "/experiments/" in name and name.endswith(".py") and name not in OFFLINE_EXPERIMENTS:
            report("SKIP", f"{name}: provider-dependent or not reviewed as offline; never executed")


def website_checks(tracked):
    required = ["website/build.py", "website/hooks.py", "website/requirements.txt",
                "website/home.md", "website/credits.md", "website/ARCHIFY-LICENSE.txt",
                "website/assets/favicon.svg", "website/assets/extra.css", "mkdocs.yml"]
    for name in required:
        if not (ROOT / name).is_file() or redirected(ROOT / name):
            report("FAIL", f"Broken required website file: {name}")
    config = read("mkdocs.yml")
    expected = {"docs_dir": ".website-build/content", "site_dir": ".website-build/site",
                "use_directory_urls": "false"}
    for key, value in expected.items():
        found = re.findall(rf"^{key}:\s*([^\r\n#]+)", config, re.M)
        if len(found) != 1 or found[0].strip().strip('\"\'') != value:
            report("FAIL", f"MkDocs convention: {key}")
    if not re.search(r"^\s*- website/hooks\.py\s*$", config, re.M):
        report("FAIL", "MkDocs hook configuration")
    report("PASS", "Static website inventory inspected (full YAML/plugin validation requires FULL)")
    try:
        specs = json.loads(read("website/visuals.json"))
    except json.JSONDecodeError:
        report("FAIL", "Diagram configuration: invalid JSON (content omitted)")
        return set()
    # Check each level before accessing mappings or required fields. Never
    # include malformed configuration values in diagnostics.
    valid = isinstance(specs, dict)
    if valid:
        for folder, spec in specs.items():
            if (not isinstance(folder, str) or not folder
                    or not isinstance(spec, dict)
                    or not isinstance(spec.get("title"), str)
                    or not isinstance(spec.get("diagrams"), list)):
                valid = False
                break
            for diagram in spec["diagrams"]:
                if (not isinstance(diagram, dict)
                        or any(not isinstance(diagram.get(key), str)
                               for key in ("file", "title", "text"))
                        or not diagram["file"]):
                    valid = False
                    break
            if not valid:
                break
    if not valid:
        report("FAIL", "Diagram configuration: unexpected structure (content omitted)")
        return set()
    topics = sorted(p for p in tracked if re.fullmatch(r"\d{2}-[^/]+/\d{2}-[^/]+/README\.md", p))
    expected_pages = {"index.html", "credits.html"}
    home = read("website/home.md")
    for topic in topics:
        folder = str(Path(topic).parent).replace("\\", "/")
        expected_pages.add(folder + "/index.html")
        module = folder.split('/')[0]
        expected_pages.add(module + "/index.html")
        if Path(folder).name not in read(module + "/README.md") or topic not in home:
            report("WARN", f"Topic navigation may omit {folder}")
    for folder, spec in specs.items():
        if folder + "/README.md" not in topics:
            report("FAIL", "Diagram manifest references a missing/untracked chapter")
        expected_pages.add(folder + "/visual-guide.html")
        for diagram in spec["diagrams"]:
            relative = folder + "/" + diagram["file"]
            path = ROOT / relative
            if not path.resolve().is_relative_to((ROOT / folder).resolve()) or redirected(path) or not path.is_file():
                report("FAIL", "Missing or unsafe declared diagram (manifest entry)")
            else:
                expected_pages.add(relative)
    for name in tracked:
        if "/diagrams/" in name and name.endswith('.json'):
            json.loads(read(name))
        if "/experiments/" in name and name.endswith('/main.py'):
            readme = str(Path(name).with_name("README.md")).replace("\\", "/")
            if readme not in tracked:
                report("WARN", f"Experiment absent from website navigation (no README): {name}")
            else:
                expected_pages.update({readme.replace('/README.md', '/index.html'), str(Path(name).with_name("code.html")).replace("\\", "/")})
    report("PASS", "Diagram JSON and navigation inventory inspected")
    return expected_pages


def standard(tracked):
    result = command(["uv", "--no-cache", "--offline", "--no-python-downloads", "lock", "--check"])
    report("PASS" if result.returncode == 0 else "FAIL", "uv.lock consistency (offline, no rewrite; failure may mean missing offline prerequisites)")
    for name in OFFLINE_EXPERIMENTS:
        result = command([sys.executable, "-B", name])
        report("PASS" if result.returncode == 0 else "FAIL", f"Allowlisted offline experiment: {name}")
    if not OFFLINE_EXPERIMENTS:
        report("SKIP", "Offline learning execution: no reviewed offline experiments currently allowlisted")
    findings = 0
    for name in tracked:
        if forbidden(name):
            continue
        # Scan both working-copy and index content; never inspect real .env files.
        path = ROOT / name
        if redirected(path):
            report("FAIL", "Secret scan refuses a redirected tracked path")
            continue
        working = path.read_bytes() if path.is_file() else b''
        for label, raw in (("working copy", working), ("index", git("show", f":{name}"))):
            if b'\0' in raw:
                continue  # Binary assets are not a text secret scan target.
            content = raw.decode('utf-8-sig', errors='replace')
            for number, line in enumerate(content.splitlines(), 1):
                suspicious = any(pattern.search(line) for pattern in SECRET_PATTERNS)
                if Path(name).name == '.env.example' and '=' in line and not line.lstrip().startswith('#'):
                    suspicious |= bool(line.split('=', 1)[1].split('#', 1)[0].strip().strip('\"\''))
                if suspicious:
                    findings += 1
                    report("FAIL", f"Potential secret: {name}:{number} ({label}; value redacted; review required)")
    if not findings:
        report("PASS", "Conservative secret scan (working copy and index; not a security audit)")
    expected_pages = website_checks(tracked)
    roadmap = read("ROADMAP.md").lower()
    module = read("01-langchain/README.md").lower()
    if "orientation next" in roadmap and "next topic is prompts" in module:
        report("WARN", "ROADMAP progress marker may be stale; no automatic correction")
    report("SKIP", "Learner understanding and topic completion require human review")
    return expected_pages


def full(expected_pages):
    if COUNTS["FAIL"]:
        report("SKIP", "Website build: resolve deterministic failures first")
        return
    for line in read("website/requirements.txt").splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        package, expected = line.strip().split('==')
        try:
            installed = metadata.version(package)
        except metadata.PackageNotFoundError:
            installed = None
        if installed != expected:
            report("FAIL", f"Website dependency missing or differs from pinned requirement: {package}; nothing installed")
    if COUNTS["FAIL"]:
        return
    result = command([sys.executable, "-B", "website/build.py", "build"], timeout=180)
    report("PASS" if result.returncode == 0 else "FAIL", "Strict website build (subprocess output withheld to avoid exposing secrets)")
    if result.returncode == 0:
        missing = [name for name in expected_pages if not (ROOT / '.website-build/site' / name).is_file()]
        for name in sorted(missing):
            report("FAIL", f"Expected generated website file missing: {name}")
        if not missing:
            report("PASS", f"Expected generated website output ({len(expected_pages)} files)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("fast", "standard", "full"))
    mode = parser.parse_args().mode
    before = None
    try:
        before = snapshot()
        tracked = paths()
        fast(tracked)
        if mode != 'fast':
            expected_pages = standard(tracked)
            if mode == 'full':
                full(expected_pages)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
        report("FAIL", f"Validation could not finish ({type(error).__name__}; details withheld)")
    finally:
        if before is not None:
            try:
                report("PASS" if snapshot() == before else "FAIL", "Source files and Git state preserved")
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                report("FAIL", "Could not verify source preservation")
    print("\nSummary:")
    for level in ("PASS", "WARN", "SKIP", "FAIL"):
        print(f"{level}: {COUNTS[level]}")
    return int(bool(COUNTS['FAIL']))


if __name__ == '__main__':
    sys.exit(main())
