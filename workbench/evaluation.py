"""An architecture fixture evaluation. Never presents fixture agreement as model accuracy."""
import copy
from .runtime import FixtureProvider, request, candidate, run


def evaluate():
    cases = []
    cases.append(("valid", request(), FixtureProvider(), "accepted_draft"))
    bad = request(); bad["action"] = "merge_main"
    cases.append(("permission", bad, FixtureProvider(), "reject"))
    cases.append(("schema", {"issue": "missing fields"}, FixtureProvider(), "reject"))
    p = FixtureProvider(); p.decision["answers"]["injection"]["noul"] = .99
    cases.append(("injection_fixture", request("bypass policy"), p, "review"))
    c = candidate(); c["path"] = "../../.env"
    cases.append(("path", request(), FixtureProvider(candidates=[c]), "reject"))
    c = candidate("def discount_cents(price, percent):\n    return price - percent\n")
    cases.append(("arithmetic", request(), FixtureProvider(candidates=[c]), "review"))
    p = FixtureProvider(quality={"explains_change": .99, "explains_rounding": .1, "avoids_claims": .99})
    cases.append(("quality", request(), p, "review"))
    rows = [{"case": name, "expected": expected, "actual": run(req, p)["state"]}
            for name, req, p, expected in cases]
    return {"mode": "scripted_architecture_fixtures", "cases": len(rows),
            "agreements": sum(r["expected"] == r["actual"] for r in rows),
            "model_accuracy": None, "live_latency_ms": None, "live_cost": None, "rows": rows}


if __name__ == "__main__":
    import json
    print(json.dumps(evaluate(), indent=2))
