#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from docs_common import DOCS, OPENAPI, classify_page_type, read_frontmatter, render_frontmatter
from import_readme import clean_body, render_openapi_operation


def operations() -> dict[str, tuple[dict, str]]:
    found = {}
    for spec_path in sorted(OPENAPI.glob("*.yaml")):
        spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        for route, path_item in spec.get("paths", {}).items():
            for method, operation in path_item.items():
                if not isinstance(operation, dict) or not operation.get("operationId"):
                    continue
                fragment = {
                    "openapi": spec["openapi"],
                    "info": spec["info"],
                    "security": spec.get("security"),
                    "components": spec.get("components", {}),
                    "paths": {route: {method: operation}},
                }
                slug = operation.get("x-doc-slug", operation["operationId"])
                found[slug] = (fragment, spec_path.name)
    return found


def operation_for(fragment: dict) -> dict:
    path_item = next(iter(fragment["paths"].values()))
    return next(operation for operation in path_item.values() if isinstance(operation, dict) and operation.get("operationId"))


TASK_DESCRIPTIONS = {
    "get-accumulate": "Retrieve entries from a named accumulation buffer.",
    "post-accumulate": "Add a JSON entry to a named accumulation buffer.",
    "get-config-channel": "Retrieve the current channel configuration document.",
    "post-config-channel": "Replace the current channel configuration document.",
    "patch-config-channel": "Patch selected fields in the current channel configuration document.",
    "get-channel-state": "Retrieve the current channel state document.",
    "post-channel-state": "Replace the current channel state document.",
    "patch-channel-state": "Patch selected fields in the current channel state document.",
    "get-config-extension": "Retrieve the extension-wide configuration document.",
    "post-config-extension": "Replace the extension-wide configuration document.",
    "patch-config-extension": "Patch selected fields in the extension-wide configuration document.",
    "get-config": "Retrieve the combined channel and extension configuration documents.",
    "get-extension-state": "Retrieve the extension-wide state document.",
    "post-extension-state": "Replace the extension-wide state document.",
    "patch-extension-state": "Patch selected fields in the extension-wide state document.",
    "post-extension-viewer-state": "Replace extension-wide state for the selected viewer.",
    "patch-extension-viewer-state": "Patch extension-wide state for the selected viewer.",
    "get-rank": "Retrieve ranked values from a named ranking buffer.",
    "post-rank": "Submit a value to a named ranking buffer.",
    "delete-rank": "Delete a named ranking buffer and its stored values.",
    "get-viewer-state": "Retrieve channel-scoped state for the current viewer.",
    "post-viewer-state": "Replace channel-scoped state for the current viewer.",
    "patch-viewer-state": "Patch channel-scoped state for the current viewer.",
    "get-all-state": "Retrieve extension, channel, viewer, and extension-viewer state in one response.",
    "post-authtoken": "Create one or more sandbox JWTs for simulated users.",
}


def generated_description(fragment: dict) -> str:
    route, path_item = next(iter(fragment["paths"].items()))
    method, operation = next(
        (method, operation)
        for method, operation in path_item.items()
        if isinstance(operation, dict) and operation.get("operationId")
    )
    if operation.get("x-doc-description"):
        return str(operation["x-doc-description"])
    if operation["operationId"] in TASK_DESCRIPTIONS:
        return TASK_DESCRIPTIONS[operation["operationId"]]
    verb = {
        "get": "Retrieve",
        "post": "Submit",
        "put": "Replace",
        "patch": "Patch",
        "delete": "Delete",
    }.get(method.lower(), "Call")
    value = re.sub(r"\s+", " ", str(operation.get("description") or operation.get("summary") or "Muxy REST API operation.")).strip()
    first_sentence = re.split(r"(?<=[.!?])\s+", value, maxsplit=1)[0]
    if len(first_sentence.split()) >= 4:
        return first_sentence if first_sentence.endswith((".", "!", "?")) else f"{first_sentence}."
    summary = str(operation.get("summary") or "API operation").strip().rstrip(".")
    return f"{verb} {summary.lower()} with {method.upper()} {route}."


def metadata_for(path: Path, slug: str, fragment: dict, existing: dict | None = None) -> dict:
    operation = operation_for(fragment)
    metadata = dict(existing or {})
    metadata.setdefault("title", operation.get("x-doc-title") or operation.get("summary") or operation["operationId"])
    current_description = str(metadata.get("description", ""))
    if operation.get("x-doc-description"):
        metadata["description"] = generated_description(fragment)
    elif not current_description or re.fullmatch(r"Muxy .+ documentation\.", current_description):
        metadata["description"] = generated_description(fragment)
    metadata.setdefault("slug", slug)
    metadata.setdefault("product", "REST API" if fragment["info"]["title"] != "Muxy Sandbox API" else "Sandbox API")
    metadata.setdefault("audience", "developers")
    metadata.setdefault("status", "current")
    metadata.setdefault("owner", "API Platform")
    metadata.setdefault("source_of_truth", f"muxy/github-pages:openapi/{'rest-v1.yaml' if fragment['info']['title'] != 'Muxy Sandbox API' else 'sandbox-v1.yaml'}")
    metadata.setdefault("version", "v1")
    metadata.setdefault("last_verified", str(date.today()))
    metadata.setdefault("review_state", "needs-sme-review")
    metadata.setdefault("page_type", classify_page_type(path, metadata))
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    failures = []
    for slug, (fragment, spec_name) in operations().items():
        path = DOCS / "reference" / f"{slug}.md"
        if path.exists():
            existing_metadata, body = read_frontmatter(path)
        else:
            existing_metadata, body = {}, ""
        metadata = metadata_for(path, slug, fragment, existing_metadata)
        generated = clean_body(render_openapi_operation(fragment, metadata["title"]), metadata["title"])
        generated += "\n!!! info \"Generated API reference\"\n"
        generated += f"    This endpoint is generated from [`{spec_name}`](https://docs.muxy.io/openapi/{spec_name}).\n"
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render_frontmatter(metadata, generated), encoding="utf-8")
        elif not path.exists():
            failures.append(f"missing generated page for operationId {slug}")
        elif existing_metadata != metadata or body.strip() != generated.strip():
            failures.append(f"generated reference drift: {path.relative_to(DOCS.parent)}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Verified {len(operations())} generated API operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
