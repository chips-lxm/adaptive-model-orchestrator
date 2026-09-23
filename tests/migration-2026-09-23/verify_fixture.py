"""Contract tests for the isolated parcel quote fixture. Usage: python verify_fixture.py FIXTURE_DIR."""
import importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
p = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("fixture_pricing", p / "pricing.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = []
def check(name, fn):
    try:
        fn()
        results.append({"name": name, "status": "passed"})
    except Exception as e:
        results.append({"name": name, "status": "failed", "detail": str(e)})
def equal(q, d, expected):
    actual = m.quote(q, d)
    assert type(actual) is int and actual == expected, f"expected exact int {expected}, got {actual!r}"
def invalid(q, d="standard"):
    try:
        m.quote(q, d)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
for q,d,total in [(0,"standard",0),(1,"standard",125),(100,"standard",12500),(0,"express",500),(3,"express",875)]:
    check(f"valid {q} {d}",lambda q=q,d=d,total=total:equal(q,d,total))
class IntSubclass(int):
    pass
for q in [-1,True,False,1.0,"1",None,[],IntSubclass(1)]:
    check(f"invalid quantity {q!r} ({type(q).__name__})",lambda q=q:invalid(q))
class DeliverySpoof:
    def __eq__(self, other):
        return other == "express"
class DeliveryRaiser:
    def __eq__(self, other):
        raise RuntimeError("unexpected custom comparison")
for d in ["overnight","",None,7,DeliverySpoof(),DeliveryRaiser()]:
    check(f"invalid delivery {d!r}",lambda d=d:invalid(1,d))
data = json.loads((p / "metadata.json").read_text())
for key,value in {"currency":"AUD","unit":"cents","delivery_modes":["standard","express"]}.items():
    def match(key=key,value=value):
        assert data.get(key) == value, f"expected {key}={value!r}, got {data.get(key)!r}"
    check("metadata "+key,match)
print(json.dumps({"passed":sum(r["status"]=="passed" for r in results),"total":len(results),"results":results},indent=2))
sys.exit(any(r["status"]=="failed" for r in results))
