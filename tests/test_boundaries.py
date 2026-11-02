import copy
import unittest
from unittest.mock import patch
from workbench.core import *
from workbench.runtime import *
from workbench.evaluation import evaluate
from workbench.labs import lab


class BoundaryTests(unittest.TestCase):
    def test_input_stops_before_inference(self):
        for raw in ({}, None, [], {**request(), "issue": 1}, {**request(), "issue": "x" * 4001},
                    {**request(), "issue": "\ud800"}):
            with self.subTest(raw=type(raw)):
                p = FixtureProvider()
                self.assertEqual(run(raw, p)["state"], "reject")
                self.assertEqual(p.calls, 0)

    def test_permission_stops_before_inference(self):
        for changes in ({"action": "merge"}, {"repo": "other/private"}):
            p = FixtureProvider()
            self.assertEqual(run({**request(), **changes}, p)["state"], "reject")
            self.assertEqual(p.calls, 0)
        self.assertEqual(run(request(), FixtureProvider(), principal="guest")["state"], "reject")

    def test_invalid_probability_rejected(self):
        for value in (float("nan"), float("inf"), -1, 1.1, True, "0.9", None):
            p = FixtureProvider()
            p.decision["answers"]["route"]["probabilities"]["pricing"] = value
            self.assertEqual(run(request(), p)["state"], "review")
            self.assertEqual(p.calls, 1)

    def test_unknown_label_or_missing_answer(self):
        for mutate in (lambda d: d["answers"]["route"].update(choice="shell"),
                       lambda d: d["answers"].pop("injection"),
                       lambda d: d.update(model="jev-latest"),
                       lambda d: d["answers"].update(route=[])):
            p = FixtureProvider(); mutate(p.decision)
            self.assertEqual(run(request(), p)["state"], "review")

    def test_semantic_review_cannot_generate(self):
        p = FixtureProvider(); p.decision["answers"]["injection"]["noul"] = .5
        self.assertEqual(run(request(), p)["state"], "review")
        self.assertEqual(p.calls, 1)

    def test_output_disallows_executable_python_features(self):
        sources = ["import os\n", "def discount_cents(price, percent):\n    return __import__('os')\n",
                   "def discount_cents(price, percent):\n    return price ** 999999\n",
                   "@evil\ndef discount_cents(price, percent):\n    return price\n",
                   "def discount_cents(price=evil(), percent=0):\n    return price\n",
                   "def discount_cents(price, percent):\n    return secret\n",
                   "def discount_cents(price, percent):\n    return True\n",
                   "def discount_cents(price, percent):\n    return 1.5\n",
                   "def discount_cents(price, percent):\n    return\n"]
        for source in sources:
            with self.subTest(source=source):
                self.assertEqual(output_check(candidate(source)).state, "reject")

    def test_path_and_provenance(self):
        c = candidate(); c["path"] = "../../secret"
        self.assertEqual(output_check(c).state, "reject")
        c = candidate(); c["evidence_id"] = "unknown"
        self.assertEqual(output_check(c).state, "review")

    def test_shape_does_not_imply_behavior(self):
        c = candidate("def discount_cents(price, percent):\n    return price - percent\n")
        self.assertEqual(output_check(c).state, "pass")
        self.assertEqual(behavior_check(c).state, "revise")

    def test_no_division_by_zero_accept(self):
        c = candidate("def discount_cents(price, percent):\n    return price // 0\n")
        self.assertEqual(behavior_check(c).state, "reject")

    def test_expected_rounding(self):
        self.assertEqual(behavior_check(candidate()).state, "pass")
        expr = ast.parse(candidate()["source"]).body[0].body[0].value
        for price in (0, 1, 99, 100, 1999, 999999):
            previous = price
            for percent in range(101):
                v = interpret(expr, {"price": price, "percent": percent})
                self.assertTrue(0 <= v <= previous)
                previous = v

    def test_quality_bound_to_candidate(self):
        p = FixtureProvider(); c = candidate(); ctx = assemble_context(request())
        verdict = p.judge(c, ctx)
        c["summary"] += " changed"
        self.assertEqual(quality_gate(verdict, digest(c)).state, "review")

    def test_high_average_does_not_override_low_dimension(self):
        p = FixtureProvider(quality={"explains_change": 1, "explains_rounding": .8, "avoids_claims": 1})
        self.assertEqual(run(request(), p)["state"], "review")

    def test_bounded_repair(self):
        wrong = candidate("def discount_cents(price, percent):\n    return price - percent\n")
        r = run(request(), FixtureProvider(candidates=[wrong, candidate()]))
        self.assertEqual((r["state"], r["attempts"], r["calls"]), ("accepted_draft", 2, 4))

    def test_persistent_failure_stops(self):
        p = FixtureProvider(quality={"explains_change": 0, "explains_rounding": 0, "avoids_claims": 0})
        r = run(request(), p)
        self.assertEqual((r["state"], r["attempts"], r["calls"]), ("review", 2, 5))

    def test_call_budget_and_deadline(self):
        self.assertEqual(run(request(), FixtureProvider(), max_calls=0)["state"], "review")
        times = iter([0, 0, 3])
        self.assertEqual(run(request(), FixtureProvider(), clock=lambda: next(times))["state"], "review")

    def test_provider_failure_is_review(self):
        p = FixtureProvider()
        with patch.object(p, "decide", side_effect=OSError("offline")):
            self.assertEqual(run(request(), p)["state"], "review")

    def test_accept_still_has_zero_effects(self):
        r = run(request(), FixtureProvider())
        self.assertEqual(r["state"], "accepted_draft")
        self.assertEqual(r["external_effects"], 0)
        self.assertIsNotNone(r["draft"])
        self.assertIsNone(run({}, FixtureProvider())["draft"])

    def test_release_separate_from_runtime(self):
        self.assertEqual(release_gate({}).state, "review")
        self.assertEqual(release_gate(dict.fromkeys(("held_out", "manifest_match", "rollback_ready", "human_signoff"), True)).state, "pass")

    def test_reproducible_manifest(self):
        a = run(request(), FixtureProvider()); b = run(request(), FixtureProvider())
        self.assertEqual(a["manifest_hash"], b["manifest_hash"])
        c = run(request(), FixtureProvider(), max_calls=6)
        self.assertNotEqual(a["manifest_hash"], c["manifest_hash"])

    def test_fixtures_do_not_claim_model_accuracy(self):
        e = evaluate()
        self.assertEqual(e["agreements"], e["cases"])
        self.assertIsNone(e["model_accuracy"])

    def test_all_lessons_run(self):
        for n in range(1, 16):
            with self.subTest(part=n):
                self.assertIsInstance(lab(n), dict)


if __name__ == "__main__":
    unittest.main()
