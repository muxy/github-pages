#!/usr/bin/env python3
"""Verify documentation versions against pinned public SDK sources."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

import yaml

from docs_common import DOCS, ROOT, read_frontmatter


SOURCE_FILE = ROOT / "migration" / "sdk-sources.yaml"


def get_json(url: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json" if "api.github.com" in url else "application/json",
        "User-Agent": "muxy-docs-source-check/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def local_errors(sources: dict) -> list[str]:
    by_product = {
        product: source
        for source in sources.values()
        for product in source.get("products", [])
    }
    errors = []
    for path in sorted(DOCS.rglob("*.md")):
        metadata, _ = read_frontmatter(path)
        if metadata.get("status") != "current" or metadata.get("product") not in by_product:
            continue
        source = by_product[metadata["product"]]
        expected_version = source["documented_version"]
        if str(metadata.get("version")) != str(expected_version):
            errors.append(
                f"{path.relative_to(ROOT)}: expected {metadata['product']} version {expected_version}, "
                f"found {metadata.get('version')}"
            )
        if source["release_state"] != "released" and metadata.get("review_state") != "blocked-release":
            errors.append(f"{path.relative_to(ROOT)}: unconfirmed SDK artifact must use review_state: blocked-release")
        if source["release_state"] == "released" and metadata.get("review_state") == "blocked-release":
            errors.append(f"{path.relative_to(ROOT)}: confirmed public release is incorrectly marked blocked-release")
    return errors


def online_errors(sources: dict) -> list[str]:
    errors = []
    for name, source in sources.items():
        try:
            if package := source.get("npm_package"):
                version = source["documented_version"]
                payload = get_json(f"https://registry.npmjs.org/{quote(package, safe='')}/{version}")
                if str(payload.get("version")) != str(version):
                    errors.append(f"{name}: npm returned the wrong version for {package}@{version}")
            if ref := source.get("ref"):
                repository = source["repository"]
                get_json(f"https://api.github.com/repos/{repository}/commits/{ref}")
                if source["release_state"] == "released":
                    get_json(f"https://api.github.com/repos/{repository}/releases/tags/{ref}")
        except HTTPError as exc:
            errors.append(f"{name}: public source check returned HTTP {exc.code}")
        except Exception as exc:
            errors.append(f"{name}: public source check failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    sources = yaml.safe_load(SOURCE_FILE.read_text(encoding="utf-8"))["sources"]
    errors = local_errors(sources)
    if args.online:
        errors.extend(online_errors(sources))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Verified {len(sources)} pinned SDK source records" + (" online" if args.online else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
