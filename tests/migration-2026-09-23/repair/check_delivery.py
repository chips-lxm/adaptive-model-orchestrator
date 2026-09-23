"""Targeted A-02 checks against an isolated fixture directory."""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
path = Path(sys.argv[1]) / "pricing.py"
namespace = {}
exec(compile(path.read_text(), str(path), "exec"), namespace)
quote = namespace["quote"]
results = []


def check(name, fn):
    try:
        fn()
    except Exception as exc:
        results.append({"name": name, "status": "failed", "detail": f"{type(exc).__name__}: {exc}"})
    else:
        results.append({"name": name, "status": "passed"})


def equal(quantity, delivery, expected):
    actual = quote(quantity, delivery)
    assert type(actual) is int and actual == expected, (actual, expected)


def invalid(quantity, delivery):
    try:
        quote(quantity, delivery)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


class OrdinaryString(str):
    pass


class SpoofString(str):
    def __eq__(self, other):
        return other == "express"


class RaiserString(str):
    def __eq__(self, other):
        raise RuntimeError("unexpected subclass comparison")


class SpoofObject:
    def __eq__(self, other):
        return other == "express"


class RaiserObject:
    def __eq__(self, other):
        raise RuntimeError("unexpected object comparison")


for quantity in (0, 1, 3):
    for delivery, surcharge in (("standard", 0), ("express", 500)):
        check(f"plain {quantity} {delivery}", lambda q=quantity, d=delivery, s=surcharge: equal(q, d, q * 125 + s))
        check(f"subclass {quantity} {delivery}", lambda q=quantity, d=delivery, s=surcharge: equal(q, OrdinaryString(d), q * 125 + s))

for quantity in (0, 1):
    for delivery in ("overnight", "", None, 7, b"express", [], {}, SpoofObject(), RaiserObject(), OrdinaryString("overnight"), SpoofString("overnight"), RaiserString("overnight")):
        check(f"invalid {quantity} {type(delivery).__name__} {str.__str__(delivery) if isinstance(delivery, str) else repr(delivery)}", lambda q=quantity, d=delivery: invalid(q, d))

print(json.dumps({"passed": sum(item["status"] == "passed" for item in results), "total": len(results), "results": results}, indent=2))
sys.exit(any(item["status"] == "failed" for item in results))
