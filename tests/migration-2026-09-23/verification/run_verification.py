"""Copy fixture, run both test suites there, and preserve command/version evidence."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parents[1]
verification = Path(__file__).resolve().parent
source = base / "fixture"
before = base / "fixture-before"
copy = verification / "test-copy"
copy.mkdir(exist_ok=True)
names = ("requirements.md", "pricing.py", "metadata.json")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = json.loads((base / "evidence" / "baseline.json").read_text())
source_before = {name: digest(source / name) for name in names}
snapshot = {name: digest(before / name) for name in names}
for name in names:
    (copy / name).write_bytes((source / name).read_bytes())
copied = {name: digest(copy / name) for name in names}

commands = (
    ("root_contract", [sys.executable, "-B", str(base / "verify_fixture.py"), str(copy)]),
    ("independent", [sys.executable, "-B", str(verification / "independent_checks.py"), str(copy)]),
    ("pricing_diff", ["diff", "-u", str(before / "pricing.py"), str(source / "pricing.py")]),
    ("metadata_diff", ["diff", "-u", str(before / "metadata.json"), str(source / "metadata.json")]),
    ("requirements_diff", ["diff", "-u", str(before / "requirements.md"), str(source / "requirements.md")]),
)
executions = []
for label, command in commands:
    result = subprocess.run(command, capture_output=True, text=True, cwd=verification, check=False)
    (verification / f"{label}.stdout.txt").write_text(result.stdout)
    (verification / f"{label}.stderr.txt").write_text(result.stderr)
    executions.append({"name": label, "command": command, "cwd": str(verification), "exit_code": result.returncode,
                       "stdout": f"{label}.stdout.txt", "stderr": f"{label}.stderr.txt"})

source_after = {name: digest(source / name) for name in names}
copy_after = {name: digest(copy / name) for name in names}
hashes = {"baseline": baseline, "before_snapshot": snapshot, "source_before": source_before,
          "source_after": source_after, "copy_before": copied, "copy_after": copy_after,
          "source_unchanged_by_verification": source_before == source_after,
          "copy_matches_source": source_before == copied == copy_after,
          "requirements_matches_original": source_before["requirements.md"] == baseline["requirements.md"] == snapshot["requirements.md"]}
(verification / "source-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
(verification / "executions.json").write_text(json.dumps({"python": sys.version, "executions": executions}, indent=2) + "\n")
print(json.dumps({"hashes": hashes, "executions": executions}, indent=2))
if not hashes["source_unchanged_by_verification"] or not hashes["copy_matches_source"] or not hashes["requirements_matches_original"]:
    sys.exit(1)
if [item["exit_code"] for item in executions] != [0, 0, 1, 1, 0]:
    sys.exit(1)
