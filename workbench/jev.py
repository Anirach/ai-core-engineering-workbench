"""Optional real decision adapter. Generation remains an explicitly supplied draft."""
import json
import os
import urllib.request
from .core import MODEL, QUESTION, QUALITY_QUESTIONS, digest


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class JevProvider:
    def __init__(self, draft, api_key=None, model=MODEL, timeout=10):
        self.key = api_key or os.environ.get("TYPESAFE_API_KEY")
        if not self.key:
            raise ValueError("Set TYPESAFE_API_KEY only for an intentional live run")
        self.draft, self.model, self.timeout = draft, model, timeout
        self.usage = []

    def ask(self, state, questions):
        body = json.dumps({"model": self.model, "state": state, "questions": questions}, allow_nan=False).encode()
        req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body,
            {"Authorization": "Bearer " + self.key, "Content-Type": "application/json"})
        with urllib.request.build_opener(NoRedirect).open(req, timeout=self.timeout) as response:
            raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("response_size")
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ValueError("response_object")
        self.usage.append(result.get("usage"))
        return result

    def decide(self, request):
        return self.ask({"issue": request["issue"]}, QUESTION)

    def generate(self, context, attempt):
        return self.draft.copy()

    def judge(self, draft, context):
        result = self.ask({"summary": draft["summary"], "requirements": context["skill"]["requirements"]}, QUALITY_QUESTIONS)
        # Local envelope field binds this request/response pair. It is NOT a Jev API field or signature.
        result["candidate_hash"] = digest(draft)
        return result
