#!/usr/bin/env python3
"""Synchronize document metadata into the migration ledger."""

from __future__ import annotations

import hashlib

import yaml

from docs_common import APPROVAL_EVIDENCE_FIELDS, DOCS, MANIFEST, ROOT, read_frontmatter


FIELDS = (
    "title",
    "description",
    "product",
    "status",
    "owner",
    "source_of_truth",
    "version",
    "review_state",
    "page_type",
)


def sync_approval_evidence(row: dict, metadata: dict) -> None:
    for field in APPROVAL_EVIDENCE_FIELDS:
        row.pop(field, None)
        if field in metadata:
            row[field] = metadata[field]


def main() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    legacy_by_target = {item["target_file"]: item for item in manifest["documents"]}
    old_derived = {item["target_file"]: item for item in manifest.get("derived_documents", [])}
    derived = []

    home_metadata, _ = read_frontmatter(DOCS / "index.md")
    manifest["homepage"] = {
        "title": home_metadata["title"],
        "description": home_metadata["description"],
        "section": "home",
        "slug": home_metadata["slug"],
        "legacy_url": "https://docs.muxy.io/",
        "legacy_markdown_url": "https://docs.muxy.io/index.md",
        "status": home_metadata["status"],
        "canonical_slug": home_metadata["slug"],
        "target_file": "docs/index.md",
        "product": home_metadata["product"],
        "owner": home_metadata["owner"],
        "source_of_truth": home_metadata["source_of_truth"],
        "version": home_metadata["version"],
        "redirects": [],
        "review_state": home_metadata["review_state"],
        "page_type": home_metadata["page_type"],
    }
    sync_approval_evidence(manifest["homepage"], home_metadata)

    for path in sorted(DOCS.rglob("*.md")):
        target = path.relative_to(ROOT).as_posix()
        if target == "docs/index.md":
            continue
        metadata, _ = read_frontmatter(path)
        legacy = legacy_by_target.get(target)
        if legacy is not None:
            for field in FIELDS:
                legacy[field] = metadata[field]
            sync_approval_evidence(legacy, metadata)
            snapshot = ROOT / "migration" / "readme" / legacy["section"] / f"{legacy['slug']}.md"
            if snapshot.is_file():
                legacy["source_sha256"] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            continue

        previous = old_derived.get(target, {})
        slug = metadata["slug"]
        legacy_parent = previous.get("legacy_parent")
        if legacy_parent is None and slug.startswith("unity-gateway-"):
            legacy_parent = "https://docs.muxy.io/docs/unity-gateway-tutorial"
        derived_row = {
                "title": metadata["title"],
                "description": metadata["description"],
                "section": path.relative_to(DOCS).parts[0],
                "slug": slug,
                "legacy_url": None,
                "legacy_markdown_url": None,
                "canonical_slug": slug,
                "target_file": target,
                "product": metadata["product"],
                "status": metadata["status"],
                "owner": metadata["owner"],
                "source_of_truth": metadata["source_of_truth"],
                "version": metadata["version"],
                "redirects": previous.get("redirects", []),
                "legacy_parent": legacy_parent,
                "review_state": metadata["review_state"],
                "page_type": metadata["page_type"],
            }
        sync_approval_evidence(derived_row, metadata)
        derived.append(derived_row)

    manifest["derived_documents"] = derived
    manifest["site_counts"] = {
        "current": sum(1 for path in DOCS.rglob("*.md") if read_frontmatter(path)[0].get("status") == "current"),
        "archived": sum(1 for path in DOCS.rglob("*.md") if read_frontmatter(path)[0].get("status") == "archived"),
        "total": sum(1 for _ in DOCS.rglob("*.md")),
    }
    MANIFEST.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"Synchronized {len(manifest['documents'])} legacy and {len(derived)} derived documents")


if __name__ == "__main__":
    main()
