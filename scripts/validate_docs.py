#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from openapi_spec_validator import validate

from docs_common import (
    APPROVAL_EVIDENCE_FIELDS,
    DOCS,
    JSON_FENCE_RE,
    MANIFEST,
    OPENAPI,
    PAGE_TYPES,
    ROOT,
    approval_content_sha256,
    read_frontmatter,
)


REQUIRED = {
    "title",
    "description",
    "slug",
    "product",
    "audience",
    "status",
    "owner",
    "source_of_truth",
    "version",
    "last_verified",
    "review_state",
    "page_type",
}
MOJIBAKE = ("ðŸ", "â€™", "â€œ", "â€", "Â")
FENCE_RE = re.compile(r"^\s*```")
NUMERIC_IMAGE_ALT_RE = re.compile(r"!\[\s*\d+\s*\]\(")
RELATIVE_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\((?!https?://|mailto:|#)([^)]+)\)")
REQUIRED_RECIPE_ROUTES = {
    "generate-a-production-jwt",
    "create-the-medkit-control-object",
    "simulate-users-while-testing",
    "gamelink-polling",
    "gamelink-transactions",
}
REQUIRED_LEGACY_ALIAS_ROUTES = REQUIRED_RECIPE_ROUTES | {"gamelink-authentication"}
REQUIRED_OPERATION_IDS = {
    "vote-get",
    "vote-submit",
    "vote-delete",
    "vote-logs",
    "vote-modifier",
    "vote-config-get",
    "vote-config-post",
    "get-json-store",
    "get-user-ids",
    "post-gamelink-token",
}
REQUIRED_TEMPLATES = {
    "quickstart.md",
    "task-guide.md",
    "concept.md",
    "sdk-reference.md",
    "protocol-reference.md",
    "troubleshooting.md",
}
MANIFEST_FIELDS = {
    "title",
    "description",
    "section",
    "slug",
    "legacy_url",
    "legacy_markdown_url",
    "status",
    "canonical_slug",
    "target_file",
    "product",
    "owner",
    "source_of_truth",
    "version",
    "redirects",
    "review_state",
    "page_type",
}
GENERIC_DESCRIPTION_RE = re.compile(r"^Muxy .+ documentation\.$")
REWRITE_SIMILARITY_LIMIT = 0.82
REVIEW_STATES = {"approved", "needs-sme-review", "blocked-release"}
APPROVED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def source_checks(require_approved: bool = False) -> list[str]:
    errors = []
    current_doc_paths: set[str] = set()
    archived_doc_paths: set[str] = set()
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    manifest_rows = [manifest["homepage"], *manifest["documents"], *manifest.get("derived_documents", [])]
    manifest_by_target = {item["target_file"]: item for item in manifest_rows}
    if len(manifest_by_target) != len(manifest_rows):
        errors.append("migration manifest contains duplicate target files")
    counts = manifest["counts"]
    if counts != {"homepage": 1, "current": 72, "archived": 14, "total": 87}:
        errors.append(f"unexpected migration counts: {counts}")
    if len(manifest["documents"]) != 86:
        errors.append("manifest must contain 86 legacy documents plus the homepage")
    expected_site_counts = {
        "current": counts["current"] + counts["homepage"] + sum(
            item.get("status") == "current" for item in manifest.get("derived_documents", [])
        ),
        "archived": counts["archived"] + sum(
            item.get("status") == "archived" for item in manifest.get("derived_documents", [])
        ),
    }
    expected_site_counts["total"] = expected_site_counts["current"] + expected_site_counts["archived"]
    if manifest.get("site_counts") != expected_site_counts:
        errors.append(f"unexpected authored site counts: {manifest.get('site_counts')}")
    for item in manifest_rows:
        missing = MANIFEST_FIELDS - item.keys()
        if missing:
            errors.append(
                f"{item.get('target_file', '<unknown manifest row>')}: migration row missing "
                f"{', '.join(sorted(missing))}"
            )
        if item.get("page_type") not in PAGE_TYPES:
            errors.append(f"{item.get('target_file')}: invalid page_type {item.get('page_type')!r}")
    for item in manifest["documents"]:
        snapshot = ROOT / "migration" / "readme" / item["section"] / f"{item['slug']}.md"
        if not snapshot.is_file():
            errors.append(f"missing ReadMe source snapshot: {snapshot.relative_to(ROOT)}")
            continue
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        if item.get("source_sha256") != digest:
            errors.append(f"ReadMe source hash drift: {snapshot.relative_to(ROOT)}")
    legacy_assets = [item for item in manifest["assets"] if "86e839b-muxy-character.svg" not in item["legacy_url"]]
    if len(legacy_assets) != 51:
        errors.append(f"expected 51 ReadMe page assets, found {len(legacy_assets)}")
    asset_targets = [item["target_file"] for item in manifest["assets"]]
    if len(set(asset_targets)) != len(asset_targets):
        errors.append("migration manifest contains duplicate asset targets")
    for item in manifest["assets"]:
        path = ROOT / item["target_file"]
        if not path.is_file():
            errors.append(f"missing vendored asset: {item['target_file']}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            errors.append(f"vendored asset hash drift: {item['target_file']}")

    template_dir = ROOT / "migration" / "templates"
    actual_templates = {path.name for path in template_dir.glob("*.md")}
    if actual_templates != REQUIRED_TEMPLATES:
        errors.append(
            "unexpected documentation templates: "
            f"missing={sorted(REQUIRED_TEMPLATES - actual_templates)}, "
            f"extra={sorted(actual_templates - REQUIRED_TEMPLATES)}"
        )
    for name in sorted(REQUIRED_TEMPLATES & actual_templates):
        metadata, body = read_frontmatter(template_dir / name)
        missing = REQUIRED - metadata.keys()
        if missing:
            errors.append(f"migration/templates/{name}: missing metadata {', '.join(sorted(missing))}")
        if sum(line.startswith("# ") for line in body.splitlines()) != 1:
            errors.append(f"migration/templates/{name}: expected exactly one H1")

    slugs = {}
    for path in sorted(DOCS.rglob("*.md")):
        metadata, body = read_frontmatter(path)
        relative = path.relative_to(ROOT)
        missing = REQUIRED - metadata.keys()
        if missing:
            errors.append(f"{relative}: missing metadata {', '.join(sorted(missing))}")
        manifest_row = manifest_by_target.get(relative.as_posix())
        if relative.as_posix() != "docs/index.md" and manifest_row is None:
            errors.append(f"{relative}: document is missing from the migration manifest")
        if manifest_row:
            for field in (
                "title",
                "description",
                "product",
                "status",
                "owner",
                "source_of_truth",
                "version",
                "review_state",
                "page_type",
                *APPROVAL_EVIDENCE_FIELDS,
            ):
                if manifest_row.get(field) != metadata.get(field):
                    errors.append(
                        f"{relative}: metadata {field} does not match migration manifest "
                        f"({metadata.get(field)!r} != {manifest_row.get(field)!r})"
                    )
        slug = metadata.get("slug")
        if metadata.get("page_type") not in PAGE_TYPES:
            errors.append(f"{relative}: invalid page_type {metadata.get('page_type')!r}")
        if GENERIC_DESCRIPTION_RE.match(str(metadata.get("description", ""))):
            errors.append(f"{relative}: description is generic rather than task-specific")
        if slug in slugs:
            errors.append(f"duplicate slug {slug}: {slugs[slug]} and {relative}")
        slugs[slug] = relative
        in_fence = False
        headings = []
        for number, line in enumerate(body.splitlines(), 1):
            if FENCE_RE.match(line):
                if not in_fence:
                    info = line.strip()[3:].strip()
                    parts = info.split(maxsplit=1)
                    if len(parts) == 2 and not parts[1].startswith(("title=", "linenums=", "hl_lines=", "{")):
                        errors.append(
                            f"{relative}:{number}: code-fence caption must use title= instead of literal text"
                        )
                in_fence = not in_fence
            if not in_fence:
                match = re.match(r"^(#{1,6})\s+", line)
                if match:
                    headings.append((number, len(match.group(1))))
        if sum(level == 1 for _, level in headings) != 1:
            errors.append(f"{relative}: expected exactly one H1")
        for (_, previous), (line, current) in zip(headings, headings[1:]):
            if current > previous + 1:
                errors.append(f"{relative}:{line}: heading level skips from H{previous} to H{current}")
        if any(token in body for token in MOJIBAKE):
            errors.append(f"{relative}: contains mojibake")
        if "files.readme.io" in body:
            errors.append(f"{relative}: depends on files.readme.io")
        if "[block:" in body:
            errors.append(f"{relative}: contains unconverted ReadMe block")
        for match in JSON_FENCE_RE.finditer(body):
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"{relative}: malformed JSON fence at line {body[:match.start()].count(chr(10)) + 1}: {exc.msg}")
        if metadata.get("status") == "archived":
            archived_doc_paths.add(path.relative_to(DOCS).as_posix())
            if metadata.get("robots") != "noindex, nofollow":
                errors.append(f"{relative}: archive is missing noindex")
            if not metadata.get("search", {}).get("exclude"):
                errors.append(f"{relative}: archive is not excluded from search")
        elif NUMERIC_IMAGE_ALT_RE.search(body):
            errors.append(f"{relative}: current-page image has a numeric-only alternative description")
        else:
            current_doc_paths.add(path.relative_to(DOCS).as_posix())
        review_state = metadata.get("review_state")
        if review_state not in REVIEW_STATES:
            errors.append(f"{relative}: invalid review_state {review_state!r}")
        if review_state == "approved":
            missing_evidence = [field for field in APPROVAL_EVIDENCE_FIELDS if not metadata.get(field)]
            if missing_evidence:
                errors.append(
                    f"{relative}: approved page is missing evidence "
                    f"{', '.join(missing_evidence)}"
                )
            else:
                approved_at = str(metadata["approved_at"])
                if not APPROVED_AT_RE.fullmatch(approved_at):
                    errors.append(f"{relative}: approved_at must be an RFC 3339 UTC timestamp")
                expected_digest = approval_content_sha256(metadata, body)
                if metadata["approved_content_sha256"] != expected_digest:
                    errors.append(
                        f"{relative}: approval invalidated by content or metadata change "
                        f"(expected {expected_digest})"
                    )
            if metadata.get("version") == "unverified":
                errors.append(f"{relative}: approved page references an unverified SDK")
        elif any(field in metadata for field in APPROVAL_EVIDENCE_FIELDS):
            errors.append(f"{relative}: non-approved page contains stale approval evidence")
        if require_approved and metadata.get("status") == "current" and metadata.get("review_state") != "approved":
            errors.append(f"{relative}: production publication requires review_state: approved")

        if manifest_row and manifest_row in manifest["documents"] and metadata.get("status") == "current":
            snapshot = ROOT / "migration" / "readme" / manifest_row["section"] / f"{manifest_row['slug']}.md"
            source_words = re.findall(r"[a-z0-9_]+", snapshot.read_text(encoding="utf-8").lower())
            current_words = re.findall(r"[a-z0-9_]+", body.lower())
            similarity = SequenceMatcher(None, source_words, current_words, autojunk=False).ratio()
            if similarity > REWRITE_SIMILARITY_LIMIT:
                errors.append(
                    f"{relative}: remains {similarity:.1%} similar to the legacy export; substantive rewrite required"
                )

        required_sections = {
            "quick-start": ("run and verify", "if verification fails"),
            "troubleshooting-tips": ("diagnosis", "resolution", "escalation"),
            "websocket-protocol": ("connection lifecycle", "limits and security"),
        }.get(slug, ())
        body_headings = {
            re.sub(r"[^a-z0-9 ]", "", line.lstrip("# ").lower()).strip()
            for line in body.splitlines()
            if line.startswith("##")
        }
        for section in required_sections:
            if section not in body_headings:
                errors.append(f"{relative}: {metadata.get('page_type')} template is missing section {section!r}")

    class MkDocsLoader(yaml.SafeLoader):
        pass

    MkDocsLoader.add_constructor("!ENV", lambda loader, node: loader.construct_sequence(node))
    mkdocs = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=MkDocsLoader)

    def nav_paths(value: object) -> list[str]:
        if isinstance(value, str):
            return [value] if value.endswith(".md") else []
        if isinstance(value, list):
            return [path for item in value for path in nav_paths(item)]
        if isinstance(value, dict):
            return [path for item in value.values() for path in nav_paths(item)]
        return []

    nav_documents = nav_paths(mkdocs.get("nav", []))
    duplicate_nav = sorted({path for path in nav_documents if nav_documents.count(path) > 1})
    if duplicate_nav:
        errors.append(f"navigation contains duplicate pages: {', '.join(duplicate_nav)}")
    missing_nav = sorted(current_doc_paths - set(nav_documents))
    if missing_nav:
        errors.append(f"current pages missing from navigation: {', '.join(missing_nav)}")
    leaked_archives = sorted(archived_doc_paths & set(nav_documents))
    if leaked_archives:
        errors.append(f"archived pages leaked into navigation: {', '.join(leaked_archives)}")

    for slug in REQUIRED_RECIPE_ROUTES:
        if not (DOCS / "recipes" / f"{slug}.md").exists():
            errors.append(f"missing developer-portal recipe route: /recipes/{slug}")

    operation_ids: set[str] = set()
    operation_counts: dict[str, int] = {}
    for path in sorted(OPENAPI.glob("*.yaml")):
        try:
            raw = path.read_text(encoding="utf-8")
            spec = yaml.safe_load(raw)
            validate(spec)
            count = 0
            for route, path_item in spec.get("paths", {}).items():
                for method, operation in path_item.items():
                    if method.lower() not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                        continue
                    count += 1
                    operation_id = operation.get("operationId")
                    if not operation_id:
                        errors.append(f"{path.relative_to(ROOT)}: {method.upper()} {route} is missing operationId")
                    elif operation_id in operation_ids:
                        errors.append(f"duplicate OpenAPI operationId: {operation_id}")
                    operation_ids.add(operation_id)
                    request_media = operation.get("requestBody", {}).get("content", {}).get("application/json", {})
                    request_schema = request_media.get("schema", {})
                    if method.lower() == "post" and request_schema.get("description") == "RFC 6902 JSON Patch operations.":
                        errors.append(f"{path.relative_to(ROOT)}: POST {route} incorrectly uses a JSON Patch request")
                    for status, response in operation.get("responses", {}).items():
                        media = response.get("content", {}).get("application/json", {})
                        values = ([media["example"]] if "example" in media else []) + [
                            example.get("value") for example in (media.get("examples") or {}).values()
                        ]
                        for value in values:
                            if isinstance(value, str):
                                try:
                                    json.loads(value)
                                except json.JSONDecodeError:
                                    errors.append(
                                        f"{path.relative_to(ROOT)}: {method.upper()} {route} response {status} "
                                        "contains a non-JSON application/json example"
                                    )
            operation_counts[path.name] = count
            if "example.com/oauth2" in raw or "RAW_BODY" in raw:
                errors.append(f"{path.relative_to(ROOT)}: contains a known ReadMe export placeholder")
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid OpenAPI: {exc}")
    if operation_counts.get("rest-v1.yaml") != 38 or operation_counts.get("sandbox-v1.yaml") != 1:
        errors.append(f"unexpected OpenAPI operation coverage: {operation_counts}")
    missing_operations = REQUIRED_OPERATION_IDS - operation_ids
    if missing_operations:
        errors.append(f"OpenAPI is missing required operations: {', '.join(sorted(missing_operations))}")
    return errors


def site_checks(site: Path, production: bool) -> list[str]:
    errors = []
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    llms = (site / "llms.txt").read_text(encoding="utf-8")
    llms_full = (site / "llms-full.txt").read_text(encoding="utf-8")
    search_payload = json.loads((site / "search" / "search_index.json").read_text(encoding="utf-8"))
    search_locations = {entry.get("location", "") for entry in search_payload.get("docs", [])}
    sitemap = (site / "sitemap.xml").read_text(encoding="utf-8")
    route_manifest = json.loads((site / "route-manifest.json").read_text(encoding="utf-8"))
    published_routes = {item["canonical"] for item in route_manifest}
    if len(llms_full) < 1000:
        errors.append("llms-full.txt is unexpectedly small")
    relative_links = RELATIVE_MARKDOWN_LINK_RE.findall(llms_full)
    if relative_links:
        errors.append(f"llms-full.txt contains {len(relative_links)} relative links")
    for metadata_field in ("Product:", "Version:", "Owner:", "Review state:", "Last verified:"):
        if metadata_field not in llms_full:
            errors.append(f"llms-full.txt is missing metadata field: {metadata_field}")
    if not (site / "robots.txt").exists():
        errors.append("robots.txt is missing")
    else:
        robots = (site / "robots.txt").read_text(encoding="utf-8")
        if production and ("Allow: /" not in robots or "Disallow: /\n" in robots):
            errors.append("production robots.txt does not allow indexing")
        if not production and ("Disallow: /\n" not in robots or "Allow: /" in robots):
            errors.append("preview robots.txt does not block indexing")
    for spec in ("rest-v1.yaml", "sandbox-v1.yaml"):
        if not (site / "openapi" / spec).exists():
            errors.append(f"published OpenAPI file is missing: {spec}")
    for item in manifest["documents"]:
        html = site / item["section"] / item["slug"] / "index.html"
        markdown = site / item["section"] / f"{item['slug']}.md"
        if not html.exists():
            errors.append(f"missing HTML compatibility route: /{item['section']}/{item['slug']}")
            continue
        if not markdown.exists():
            errors.append(f"missing Markdown compatibility route: /{item['section']}/{item['slug']}.md")
        page = html.read_text(encoding="utf-8")
        expected_canonical = f"https://docs.muxy.io/{item['section']}/{item['slug']}/"
        if expected_canonical not in page:
            errors.append(f"wrong canonical metadata: {html.relative_to(site)}")
        if item["status"] == "archived":
            route = f"{item['section']}/{item['slug']}/"
            markdown_route = f"/{item['section']}/{item['slug']}.md"
            canonical = f"https://docs.muxy.io/{route}"
            leaked = (
                markdown_route in llms
                or f"Source: https://docs.muxy.io{markdown_route}" in llms_full
                or any(location == route or location.startswith(route + "#") for location in search_locations)
                or canonical in sitemap
                or f"/{item['section']}/{item['slug']}" in published_routes
            )
            if leaked:
                errors.append(f"archived document leaked into an index: {item['slug']}")
            if 'content="noindex, nofollow"' not in page:
                errors.append(f"archived HTML is missing noindex: {item['slug']}")
            if markdown.exists() and '<meta name="robots" content="noindex, nofollow">' not in markdown.read_text(encoding="utf-8"):
                errors.append(f"archived Markdown is missing an embedded noindex directive: {item['slug']}")
        elif f"/{item['section']}/{item['slug']}.md" not in llms:
            errors.append(f"current document missing from llms.txt: {item['slug']}")
    try:
        root = ET.fromstring(sitemap)
        if len(list(root)) == 0:
            errors.append("sitemap.xml is empty")
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml is invalid: {exc}")
    for path in DOCS.rglob("*.md"):
        metadata, _ = read_frontmatter(path)
        if metadata.get("status") == "archived":
            continue
        if path == DOCS / "index.md":
            route = "/"
            html = site / "index.html"
            markdown = site / "index.md"
            expected_canonical = "https://docs.muxy.io/"
        else:
            route = "/" + path.relative_to(DOCS).with_suffix("").as_posix()
            html = site / path.relative_to(DOCS).with_suffix("") / "index.html"
            markdown = site / path.relative_to(DOCS).with_suffix(".md")
            expected_canonical = f"https://docs.muxy.io{route}/"
            if route not in published_routes:
                errors.append(f"published route manifest is missing: {route}")
        if not html.exists():
            errors.append(f"current page HTML is missing: {route}")
        else:
            rendered = html.read_text(encoding="utf-8")
            if expected_canonical not in rendered:
                errors.append(f"current page canonical metadata is wrong: {route}")
            expected_robots = "index, follow" if production else "noindex, nofollow"
            if f'content="{expected_robots}"' not in rendered:
                errors.append(f"current page indexing metadata is wrong: {route}")
        if not markdown.exists():
            errors.append(f"current page Markdown is missing: {route}.md")
    for html in site.rglob("*.html"):
        rendered = html.read_text(encoding="utf-8", errors="replace")
        if "files.readme.io" in rendered:
            errors.append(f"published HTML depends on files.readme.io: {html.relative_to(site)}")
        if re.search(r"<p>\s*```(?:csharp|javascript|json|bash|html)", rendered):
            errors.append(f"published HTML contains a literal code fence: {html.relative_to(site)}")
    for slug in REQUIRED_RECIPE_ROUTES:
        if not (site / "recipes" / slug / "index.html").exists():
            errors.append(f"missing rendered recipe route: /recipes/{slug}/")
    for slug in REQUIRED_LEGACY_ALIAS_ROUTES:
        if not (site / "v1.0" / "recipes" / slug / "index.html").exists():
            errors.append(f"missing legacy recipe alias: /v1.0/recipes/{slug}/")
        if not (site / "v1.0" / "recipes" / f"{slug}.md").exists():
            errors.append(f"missing legacy recipe Markdown alias: /v1.0/recipes/{slug}.md")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path)
    parser.add_argument("--require-approved", action="store_true")
    policy = parser.add_mutually_exclusive_group()
    policy.add_argument("--production", action="store_true")
    policy.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    production = args.production or (
        not args.preview and os.environ.get("DOCS_PRODUCTION", "false").lower() == "true"
    )
    errors = site_checks(args.site, production) if args.site else source_checks(args.require_approved)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    current_states = Counter()
    for path in DOCS.rglob("*.md"):
        metadata, _ = read_frontmatter(path)
        if metadata.get("status") == "current":
            current_states[metadata.get("review_state", "missing")] += 1
    print("Documentation validation passed")
    print(
        "Review gate: "
        f"{current_states['approved']} approved, "
        f"{current_states['needs-sme-review']} needs-sme-review, "
        f"{current_states['blocked-release']} blocked-release"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
