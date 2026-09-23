"""Independent behavioral checks for the copied parcel quote fixture.

Usage: python3 -B independent_checks.py TEST_COPY_DIR
"""

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
fixture = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("independent_fixture_pricing", fixture / "pricing.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
results = []


def check(name, operation):
    try:
        operation()
        results.append({"name": name, "status": "passed"})
    except Exception as exc:
        results.append({
            "name": name,
            "status": "failed",
            "exception": type(exc).__name__,
            "detail": str(exc),
        })


def expect_total(quantity, delivery, expected, use_default=False):
    actual = module.quote(quantity) if use_default else module.quote(quantity, delivery)
    if type(actual) is not int or actual != expected:
        raise AssertionError(f"expected exact int {expected}, got {actual!r} ({type(actual).__name__})")


def expect_value_error(quantity, delivery, use_default=False):
    try:
        if use_default:
            module.quote(quantity)
        else:
            module.quote(quantity, delivery)
    except ValueError:
        return
    except Exception as exc:
        raise AssertionError(f"expected ValueError, got {type(exc).__name__}: {exc}") from exc
    raise AssertionError("expected ValueError, returned normally")


class OrdinaryText(str):
    pass


class IntChild(int):
    pass


class SpoofObject:
    def __eq__(self, other):
        return other == "express"


class RaisingObject:
    def __eq__(self, other):
        raise RuntimeError("comparison must not run")


class SpoofText(str):
    def __eq__(self, other):
        return other == "express"


class RaisingText(str):
    def __eq__(self, other):
        raise RuntimeError("comparison must not run")


for quantity in (0, 1, 3, 10**30):
    for delivery, surcharge in (("standard", 0), ("express", 500)):
        expected = quantity * 125 + surcharge
        check(f"plain {quantity} {delivery}", lambda q=quantity, d=delivery, e=expected: expect_total(q, d, e))
        check(f"ordinary subclass {quantity} {delivery}", lambda q=quantity, d=delivery, e=expected: expect_total(q, OrdinaryText(d), e))
    check(f"default {quantity}", lambda q=quantity: expect_total(q, "standard", q * 125, True))

for quantity in (-1, -(10**30), True, False, 1.0, "1", None, [], {}, object(), IntChild(0), IntChild(2)):
    label = f"invalid quantity {type(quantity).__name__} {repr(quantity)}"
    check(label, lambda q=quantity: expect_value_error(q, "standard"))

for quantity in (0, 1):
    for delivery in ("overnight", "", None, 7, b"express", [], {}, SpoofObject(), RaisingObject(), OrdinaryText("overnight"), SpoofText("overnight"), RaisingText("overnight")):
        label = f"invalid delivery q={quantity} {type(delivery).__name__} {repr(delivery)}"
        check(label, lambda q=quantity, d=delivery: expect_value_error(q, d))

metadata = json.loads((fixture / "metadata.json").read_text())
for key, expected in (("currency", "AUD"), ("unit", "cents"), ("delivery_modes", ["standard", "express"])):
    def validate(field=key, value=expected):
        if metadata.get(field) != value:
            raise AssertionError(f"expected {field}={value!r}, got {metadata.get(field)!r}")
    check(f"metadata {key}", validate)

summary = {"passed": sum(item["status"] == "passed" for item in results), "total": len(results), "results": results}
print(json.dumps(summary, indent=2))
sys.exit(0 if summary["passed"] == summary["total"] else 1)
