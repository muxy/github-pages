#!/usr/bin/env python3
from __future__ import annotations

import gzip
import json
import os
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

from docs_common import DOCS, OPENAPI, ROOT, canonical_path, load_manifest, read_frontmatter, render_frontmatter


SITE = ROOT / "site"
BASE_URL = "https://docs.muxy.io"
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)([^)]*\))")
HTML_TAG_RE = re.compile(r"</?(?:div|span|section|article|aside)[^>]*>")
LEGACY_RECIPE_ALIASES = {
    "generate-a-production-jwt": "/recipes/generate-a-production-jwt/",
    "create-the-medkit-control-object": "/recipes/create-the-medkit-control-object/",
    "simulate-users-while-testing": "/recipes/simulate-users-while-testing/",
    "gamelink-polling": "/recipes/gamelink-polling/",
    "gamelink-transactions": "/recipes/gamelink-transactions/",
    "gamelink-authentication": "/reference/ws-authentication/",
}


def all_pages() -> list[tuple[Path, dict, str]]:
    pages = []
    for path in DOCS.rglob("*.md"):
        metadata, body = read_frontmatter(path)
        pages.append((path, metadata, body))
    return sorted(pages, key=lambda item: (item[1].get("product", ""), item[1].get("title", "")))


def all_current_pages() -> list[tuple[Path, dict, str]]:
    return [page for page in all_pages() if page[1].get("status") == "current"]


def raw_route(path: Path) -> Path:
    if path == DOCS / "index.md":
        return SITE / "index.md"
    return SITE / path.relative_to(DOCS)


def absolute_links(body: str, source_url: str) -> str:
    """Make concatenated Markdown links independent of their source location."""
    def replace(match: re.Match[str]) -> str:
        target = match.group(2)
        parsed = urlparse(target)
        if parsed.scheme or target.startswith(("#", "mailto:", "data:")):
            return match.group(0)
        return f"{match.group(1)}{urljoin(source_url, target)}{match.group(3)}"

    return MARKDOWN_LINK_RE.sub(replace, body)


def semantic_markdown(body: str, source_url: str) -> str:
    # Material homepage layout wrappers add no meaning to the aggregate export.
    return absolute_links(HTML_TAG_RE.sub("", body), source_url).strip()


def write_agent_exports() -> None:
    for path, metadata, body in all_pages():
        destination = raw_route(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if metadata.get("status") == "archived":
            body = '<meta name="robots" content="noindex, nofollow">\n\n' + body
            destination.write_text(render_frontmatter(metadata, body), encoding="utf-8")
        else:
            destination.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    pages = all_current_pages()
    index_lines = [
        "# Muxy Documentation",
        "",
        "> Build interactive game and Twitch experiences with Muxy SDKs, APIs, and protocols.",
        "",
        "## Machine-readable API specifications",
        "",
        f"- [Muxy REST API OpenAPI]({BASE_URL}/openapi/rest-v1.yaml)",
        f"- [Muxy Sandbox API OpenAPI]({BASE_URL}/openapi/sandbox-v1.yaml)",
        "",
        "## Documentation",
        "",
    ]
    full_lines = index_lines.copy()
    for path, metadata, body in pages:
        destination = raw_route(path)
        route = "/" + destination.relative_to(SITE).as_posix()
        review_prefix = "" if metadata["review_state"] == "approved" else f"[{metadata['review_state']}] "
        index_lines.append(f"- [{metadata['title']}]({BASE_URL}{route}): {review_prefix}{metadata['description']}")
        source_url = f"{BASE_URL}{route}"
        metadata_lines = [
            f"- Product: {metadata['product']}",
            f"- Audience: {metadata['audience']}",
            f"- Version: {metadata['version']}",
            f"- Owner: {metadata['owner']}",
            f"- Review state: {metadata['review_state']}",
            f"- Last verified: {metadata['last_verified']}",
        ]
        if metadata["review_state"] == "approved":
            metadata_lines.extend(
                [
                    f"- Approved by: {metadata['approved_by']}",
                    f"- Approved at: {metadata['approved_at']}",
                    f"- Approval method: {metadata['approval_method']}",
                    f"- Approved content SHA-256: {metadata['approved_content_sha256']}",
                ]
            )
        full_lines.extend(
            [f"## {metadata['title']}", "", f"Source: {source_url}", "", *metadata_lines, "", semantic_markdown(body, source_url), ""]
        )
    (SITE / "llms.txt").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    (SITE / "llms-full.txt").write_text("\n".join(full_lines).rstrip() + "\n", encoding="utf-8")


def write_link_inputs() -> None:
    routes = []
    html_files = []
    link_inputs = []
    for path, _, _ in all_current_pages():
        if path == DOCS / "index.md":
            route = "/"
            html = SITE / "index.html"
        else:
            route = "/" + path.relative_to(DOCS).with_suffix("").as_posix() + "/"
            html = SITE / path.relative_to(DOCS).with_suffix("") / "index.html"
        routes.append(f"http://127.0.0.1:8000{route}")
        html_files.append(html.relative_to(ROOT).as_posix())
        link_inputs.extend(
            [html.relative_to(ROOT).as_posix(), raw_route(path).relative_to(ROOT).as_posix()]
        )
    (SITE / "current-pages.txt").write_text("\n".join(routes) + "\n", encoding="utf-8")
    (SITE / "current-html.txt").write_text("\n".join(html_files) + "\n", encoding="utf-8")
    link_inputs.extend(["site/llms.txt", "site/llms-full.txt"])
    (SITE / "current-link-inputs.txt").write_text("\n".join(link_inputs) + "\n", encoding="utf-8")


def write_openapi() -> None:
    destination = SITE / "openapi"
    destination.mkdir(exist_ok=True)
    for path in OPENAPI.glob("*.yaml"):
        shutil.copy2(path, destination / path.name)


def write_route_manifest() -> None:
    manifest = load_manifest()
    routes = [
        {
            "legacy_url": "https://docs.muxy.io/",
            "canonical": "/",
            "markdown": "/index.md",
            "status": "current",
        }
    ]
    canonical_routes = set()
    for document in manifest["documents"]:
        if document["status"] == "archived":
            continue
        html = canonical_path(document)
        markdown = canonical_path(document, markdown=True)
        canonical_routes.add(html)
        routes.append(
            {
                "legacy_url": document["legacy_url"],
                "canonical": html,
                "markdown": markdown,
                "status": document["status"],
            }
        )
    for path, metadata, _ in all_pages():
        if path == DOCS / "index.md":
            continue
        if metadata.get("status") == "archived":
            continue
        html = "/" + path.relative_to(DOCS).with_suffix("").as_posix()
        if html in canonical_routes:
            continue
        routes.append(
            {
                "legacy_url": None,
                "canonical": html,
                "markdown": html + ".md",
                "status": metadata["status"],
            }
        )
    for slug, target in LEGACY_RECIPE_ALIASES.items():
        routes.append(
            {
                "legacy_url": f"https://docs.muxy.io/v1.0/recipes/{slug}",
                "canonical": f"/v1.0/recipes/{slug}",
                "markdown": f"/v1.0/recipes/{slug}.md",
                "redirect": target,
                "status": "compatibility",
            }
        )
    (SITE / "route-manifest.json").write_text(json.dumps(routes, indent=2) + "\n", encoding="utf-8")


def write_legacy_recipe_aliases() -> None:
    for slug, target in LEGACY_RECIPE_ALIASES.items():
        destination = SITE / "v1.0" / "recipes" / slug / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<link rel=\"canonical\" href=\"{BASE_URL}{target}\">"
            f"<meta http-equiv=\"refresh\" content=\"0; url={target}\">"
            f"<title>Moved</title></head><body><p>This page moved to <a href=\"{target}\">{target}</a>.</p></body></html>",
            encoding="utf-8",
        )
        markdown = SITE / "v1.0" / "recipes" / f"{slug}.md"
        markdown.write_text(
            f"# Moved\n\nThis compatibility route moved to [{target}]({BASE_URL}{target}).\n",
            encoding="utf-8",
        )


def filter_sitemap() -> None:
    sitemap = SITE / "sitemap.xml"
    tree = ET.parse(sitemap)
    root = tree.getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    archived = {
        f"{BASE_URL}/{item['section']}/{item['slug']}/"
        for item in load_manifest()["documents"]
        if item["status"] == "archived"
    }
    for node in list(root):
        location = node.find("sm:loc", namespace)
        if location is not None and location.text in archived:
            root.remove(node)
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)
    with gzip.open(SITE / "sitemap.xml.gz", "wb") as compressed:
        compressed.write(sitemap.read_bytes())


def main() -> None:
    if not SITE.exists():
        raise SystemExit("site/ does not exist; run mkdocs build first")
    write_agent_exports()
    write_link_inputs()
    write_openapi()
    write_route_manifest()
    write_legacy_recipe_aliases()
    filter_sitemap()
    archived = [page for page in all_pages() if page[1].get("status") == "archived"]
    production = os.environ.get("DOCS_PRODUCTION", "false").lower() == "true"
    robots = ["User-agent: *", "Allow: /"] if production else ["User-agent: *", "Disallow: /"]
    for path, _, _ in archived:
        route = "/" + path.relative_to(DOCS).with_suffix("").as_posix()
        robots.extend([f"Disallow: {route}/", f"Disallow: {route}.md"])
    robots.extend(["", "Sitemap: https://docs.muxy.io/sitemap.xml", ""])
    (SITE / "robots.txt").write_text("\n".join(robots), encoding="utf-8")
    print(f"Generated site contracts for {len(all_current_pages())} current pages")


if __name__ == "__main__":
    main()
