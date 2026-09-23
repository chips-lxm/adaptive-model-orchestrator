"""Read-only fixture probes and executed W01 adjudication."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-sol"
FIXTURE = ROOT / "fixture-before"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


failures = 0


def check(label: str, function, expected=None, error=None) -> None:
    global failures
    try:
        actual = function()
    except Exception as exc:
        if error is not None and type(exc) is error:
            print(f"PASS {label}: {type(exc).__name__}({exc})")
        else:
            print(f"FAIL {label}: unexpected {type(exc).__name__}({exc})")
            failures += 1
        return
    if error is not None:
        print(f"FAIL {label}: expected {error.__name__}, got {actual!r}")
        failures += 1
    elif type(actual) is type(expected) and actual == expected:
        print(f"PASS {label}: {actual!r}")
    else:
        print(f"FAIL {label}: expected {expected!r}, got {actual!r}")
        failures += 1


class IntChild(int):
    pass


class DeliverySpoof:
    def __eq__(self, other):
        return other == "express"


class DeliveryRaiser:
    def __eq__(self, other):
        raise RuntimeError("custom comparison failed")


def main() -> None:
    baseline = json.loads((ROOT / "evidence/baseline.json").read_text())
    for name in ("requirements.md", "pricing.py"):
        assert digest(FIXTURE / name) == baseline[name], f"baseline drift: {name}"
    print("Fixture baseline matches requirements.md and pricing.py hashes")

    # Import only the isolated copy, so bytecode and other test effects cannot
    # change the source fixture.
    shutil.copy2(FIXTURE / "pricing.py", OUT / "pricing_test_copy.py")
    namespace = {}
    exec((OUT / "pricing_test_copy.py").read_text(), namespace)
    quote = namespace["quote"]
    check("standard zero", lambda: quote(0), 0)
    check("standard one", lambda: quote(1), 125)
    check("standard three", lambda: quote(3), 375)
    check("express zero", lambda: quote(0, "express"), 500)
    check("express three", lambda: quote(3, "express"), 875)
    check("large integer", lambda: quote(10**30, "express"), 125 * 10**30 + 500)
    check("negative integer", lambda: quote(-1), error=ValueError)
    check("float", lambda: quote(1.0), error=ValueError)
    check("string quantity", lambda: quote("1"), error=ValueError)
    check("None quantity", lambda: quote(None), error=ValueError)
    check("True quantity", lambda: quote(True), error=ValueError)
    check("False quantity", lambda: quote(False), error=ValueError)
    check("int subclass", lambda: quote(IntChild(2)), error=ValueError)
    check("invalid delivery", lambda: quote(1, "priority"), error=ValueError)
    check("None delivery", lambda: quote(1, None), error=ValueError)
    check("delivery spoof", lambda: quote(1, DeliverySpoof()), error=ValueError)
    check("delivery comparison error", lambda: quote(1, DeliveryRaiser()), error=ValueError)

    cases = json.loads((ROOT / "legacy-cases.json").read_text())
    w01 = next(case for case in cases["workflow_cases"] if case["id"] == "W01")
    w01_ns = {}
    exec(w01["artifact"], w01_ns)
    total = w01_ns["total"]
    check("W01 zero", lambda: total(0), 0)
    check("W01 one", lambda: total(1), 10)
    check("W01 minus one", lambda: total(-1), error=ValueError)
    check("W01 True", lambda: total(True), error=ValueError)
    check("W01 False", lambda: total(False), error=ValueError)
    check("W01 float", lambda: total(1.0), error=ValueError)
    check("W01 int subclass", lambda: total(IntChild(2)), error=ValueError)

    for name in ("requirements.md", "pricing.py"):
        assert digest(FIXTURE / name) == baseline[name], f"fixture changed: {name}"
    print("Fixture source hashes unchanged after probes")
    print(f"Total failed assertions: {failures}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
