import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from workbench.jev import JevProvider, NoRedirect
from workbench.runtime import candidate, request, run, FixtureProvider
from workbench.core import MODEL, QUESTION


class Response:
    def __init__(self, body): self.body = body
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, limit): return self.body[:limit]


class JevAdapterTests(unittest.TestCase):
    def test_exact_request_and_response_contract(self):
        received = []
        body = FixtureProvider().decision
        class Opener:
            def open(self, req, timeout):
                received.append((req, timeout))
                return Response(json.dumps(body).encode())
        with patch('urllib.request.build_opener', return_value=Opener()):
            result = JevProvider(candidate(), api_key='synthetic-test-key').decide(request())
        req, timeout = received[0]
        payload = json.loads(req.data)
        self.assertEqual(req.full_url, 'https://api.typesafe.ai/v1/systemone')
        self.assertEqual(set(payload), {'model', 'state', 'questions'})
        self.assertEqual(payload['model'], MODEL)
        self.assertEqual(payload['questions'], QUESTION)
        self.assertEqual(payload['state'], {'issue': request()['issue']})
        self.assertEqual(result, body)

    def test_http_failure_returns_review(self):
        class Opener:
            def open(self, req, timeout):
                raise HTTPError(req.full_url, 429, 'rate limited', {}, None)
        with patch('urllib.request.build_opener', return_value=Opener()):
            result = run(request(), JevProvider(candidate(), api_key='synthetic-test-key'))
        self.assertEqual(result['state'], 'review')
        self.assertEqual(result['external_effects'], 0)

    def test_key_required(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError): JevProvider(candidate())

    def test_redirects_disabled(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, None, None, None, None))

    def test_bad_json_returns_review(self):
        class Opener:
            def open(self, req, timeout): return Response(b'not-json')
        with patch('urllib.request.build_opener', return_value=Opener()):
            self.assertEqual(run(request(), JevProvider(candidate(), api_key='synthetic-test-key'))['state'], 'review')


if __name__ == '__main__': unittest.main()
