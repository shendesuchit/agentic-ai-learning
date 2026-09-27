"""Build or preview the learning website from the repository root."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "serve"], nargs="?", default="build")
    args = parser.parse_args()
    (ROOT / ".website-build" / "content").mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "mkdocs", args.command, "--config-file", str(ROOT / "mkdocs.yml")]
    if args.command == "build":
        command.append("--strict")
    raise SystemExit(subprocess.call(command, cwd=ROOT))

if __name__ == "__main__":
    main()
