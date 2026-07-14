#!/usr/bin/env python3
"""Record content-bound documentation approvals."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docs_common import DOCS, approval_content_sha256, read_frontmatter, render_frontmatter


RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-by", required=True)
    parser.add_argument("--approved-at", required=True)
    parser.add_argument("--approval-method", required=True)
    parser.add_argument("--from-state", default="needs-sme-review")
    parser.add_argument("--expected-count", type=int, required=True)
    args = parser.parse_args()

    if not RFC3339_UTC_RE.fullmatch(args.approved_at):
        parser.error("--approved-at must use YYYY-MM-DDTHH:MM:SSZ")

    candidates: list[tuple[Path, dict, str]] = []
    for path in sorted(DOCS.rglob("*.md")):
        metadata, body = read_frontmatter(path)
        if metadata.get("status") != "current" or metadata.get("review_state") != args.from_state:
            continue
        if metadata.get("version") == "unverified":
            raise SystemExit(f"Refusing to approve unverified SDK content: {path}")
        candidates.append((path, metadata, body))

    if len(candidates) != args.expected_count:
        raise SystemExit(
            f"Refusing to approve {len(candidates)} pages; expected exactly {args.expected_count}"
        )

    for path, metadata, body in candidates:
        metadata["review_state"] = "approved"
        metadata["approved_by"] = args.approved_by
        metadata["approved_at"] = args.approved_at
        metadata["approval_method"] = args.approval_method
        metadata["approved_content_sha256"] = approval_content_sha256(metadata, body)
        path.write_text(render_frontmatter(metadata, body), encoding="utf-8")

    print(f"Recorded content-bound approval evidence for {len(candidates)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
