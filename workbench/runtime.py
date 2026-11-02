"""Imperative shell. Drafts stay in memory; this does not open a GitHub PR."""
from dataclasses import asdict
from time import monotonic
import math
from .core import (MODEL, POLICY, SKILL, QUESTION, QUALITY_QUESTIONS, digest,
                   input_check, decision_check, semantic_input, authorize,
                   assemble_context, output_check, behavior_check, quality_gate)


class FixtureProvider:
    """Scripted answers, not Jev predictions or a benchmark of any model."""
    def __init__(self, decision=None, candidates=None, quality=None):
        self.decision = decision or {"model": MODEL, "answers": {
            "route": {"type": "choice", "choice": "pricing", "confidence": 1.0,
                      "probabilities": {"pricing": 1.0, "docs": 0.0, "unknown": 0.0}},
            "injection": {"type": "noul", "noul": .01}}}
        self.candidates = candidates or [candidate()]
        self.quality = quality or {k: .99 for k in QUALITY_QUESTIONS}
        self.calls = 0

    def decide(self, request):
        self.calls += 1
        return self.decision

    def generate(self, context, attempt):
        self.calls += 1
        return self.candidates[min(attempt, len(self.candidates) - 1)].copy()

    def judge(self, draft, context):
        self.calls += 1
        return {"model": MODEL, "candidate_hash": digest(draft), "answers": {
            k: {"type": "noul", "noul": v} for k, v in self.quality.items()}}


def candidate(source=None, summary=None):
    return {"path": "src/pricing.py", "source": source or
            "def discount_cents(price, percent):\n    return price * (100 - percent) // 100\n",
            "summary": summary or "Subtract the discount using integer cents; floor the result to whole cents. This is a draft for review.",
            "evidence_id": "pricing-spec-v1"}


def request(issue="Fix integer-cent discount rounding"):
    return {"id": "ISSUE-42", "issue": issue, "repo": "demo/shop", "action": "draft_patch"}


def run(raw, provider, principal="maintainer", max_calls=5, max_revisions=1,
        seconds=2, clock=monotonic):
    if type(max_calls) is not int or max_calls < 0 or type(max_revisions) is not int or max_revisions < 0:
        raise ValueError("nonnegative integer budgets required")
    if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("positive time budget required")
    trace, attempts, calls, started = [], 0, 0, clock()
    manifest = {"policy": POLICY, "skill_hash": digest(SKILL), "questions_hash": digest(QUESTION),
                "quality_questions_hash": digest(QUALITY_QUESTIONS), "decision_model": MODEL,
                "provider": type(provider).__name__, "max_revisions": max_revisions,
                "max_calls": max_calls, "seconds": seconds, "candidate_language": "integer-expression-v1"}

    def finish(state, reason, draft=None):
        return {"state": state, "reason": reason, "attempts": attempts, "calls": calls,
                "trace": trace, "manifest_hash": digest(manifest), "manifest": manifest,
                "candidate_hash": digest(draft) if draft else None,
                "draft": draft if state == "accepted_draft" else None,
                "mode": "fixture" if isinstance(provider, FixtureProvider) else "live-decisions",
                "usage": None, "external_effects": 0}

    def check(stage, gate):
        trace.append({"stage": stage, **asdict(gate)})
        return gate.state == "pass"

    def invoke(fn, *args):
        nonlocal calls
        if calls >= max_calls or clock() - started >= seconds:
            raise TimeoutError("budget_exhausted")
        calls += 1
        value = fn(*args)
        if clock() - started >= seconds:
            raise TimeoutError("deadline_exceeded")
        return value

    gate = input_check(raw)
    if not check("input", gate):
        return finish(gate.state, gate.reason)
    gate = authorize(raw, principal)
    if not check("policy", gate):
        return finish(gate.state, gate.reason)
    try:
        response = invoke(provider.decide, raw)
        for stage, gate in [("decision", decision_check(response))]:
            if not check(stage, gate):
                return finish(gate.state, gate.reason)
        gate = semantic_input(response)
        if not check("semantic_input", gate):
            return finish(gate.state, gate.reason)
        context = assemble_context(raw)
        manifest["context_hash"] = digest(context)
        while attempts <= max_revisions:
            draft = invoke(provider.generate, context, attempts)
            attempts += 1
            gate = output_check(draft)
            if not check("output", gate):
                return finish(gate.state, gate.reason)
            gate = behavior_check(draft)
            if not check("behavior", gate):
                if gate.state == "revise" and attempts <= max_revisions:
                    continue
                return finish("review" if gate.state == "revise" else gate.state, gate.reason)
            verdict = invoke(provider.judge, draft, context)
            gate = quality_gate(verdict, digest(draft))
            if check("quality", gate):
                return finish("accepted_draft", "ready_for_human_review", draft)
            if gate.state != "revise" or attempts > max_revisions:
                return finish("review", gate.reason)
    except (TimeoutError, OSError, ValueError, KeyError, TypeError) as exc:
        trace.append({"stage": "provider", "state": "review", "reason": type(exc).__name__})
        return finish("review", "provider_or_budget_failure")
    return finish("review", "revision_budget")
