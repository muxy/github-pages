#!/usr/bin/env python3
"""Assign and normalize the editorial template used by every documentation page."""

from __future__ import annotations

from docs_common import DOCS, classify_page_type, read_frontmatter, render_frontmatter


def main() -> None:
    changed = 0
    for path in sorted(DOCS.rglob("*.md")):
        metadata, body = read_frontmatter(path)
        page_type = classify_page_type(path, metadata)
        if metadata.get("page_type") == page_type:
            continue
        metadata["page_type"] = page_type
        path.write_text(render_frontmatter(metadata, body), encoding="utf-8")
        changed += 1
    print(f"Assigned editorial templates to {changed} pages")


if __name__ == "__main__":
    main()
