"""Explicit opt-in: real Jev decisions on a local, reviewed fixture draft."""
import argparse
import json
from .jev import JevProvider
from .runtime import candidate, request, run


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--allow-paid-api", action="store_true", required=True)
    args = p.parse_args()
    provider = JevProvider(candidate())
    result = run(request(), provider, max_revisions=0, seconds=30)
    result["provider_usage"] = provider.usage
    result["generation_mode"] = "reviewed_fixture_not_live_generation"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
