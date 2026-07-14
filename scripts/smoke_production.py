#!/usr/bin/env python3
"""End-to-end smoke checks for the deployed Muxy documentation artifact."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import ssl
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

import yaml


HTML_TYPES = {"text/html", "application/xhtml+xml"}
JSON_TYPES = {"application/json", "text/json"}
XML_TYPES = {"application/xml", "text/xml"}
TEXT_TYPES = {"text/plain"}
# GitHub Pages and Python's loopback server use different MIME databases for
# source files. Both values below are safe only after the body parses as YAML.
YAML_TYPES = {"application/yaml", "application/x-yaml", "text/yaml", "text/x-yaml", "text/plain", "application/octet-stream"}
MARKDOWN_TYPES = {"text/markdown", "text/x-markdown", "text/plain", "application/octet-stream"}
ASSET_TYPES = {
    ".css": {"text/css"},
    ".png": {"image/png"},
    ".svg": {"image/svg+xml"},
}
SOFT_404_RE = re.compile(r"(?:\b404\b|page\s+not\s+found|not\s+found)", re.IGNORECASE)
REFRESH_URL_RE = re.compile(r"(?:^|;)\s*url\s*=\s*['\"]?([^'\";]+)", re.IGNORECASE)


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes
    content_type: str
    final_url: str


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.robots: list[str] = []
        self.refreshes: list[str] = []
        self._capture: str | None = None
        self._text: dict[str, list[str]] = {"title": [], "h1": []}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        tag = tag.lower()
        if tag == "link" and "canonical" in values.get("rel", "").lower().split():
            if values.get("href"):
                self.canonicals.append(values["href"].strip())
        elif tag == "meta":
            if values.get("name", "").lower() == "robots" and values.get("content"):
                self.robots.append(values["content"].strip().lower())
            if values.get("http-equiv", "").lower() == "refresh" and values.get("content"):
                match = REFRESH_URL_RE.search(values["content"])
                if match:
                    self.refreshes.append(match.group(1).strip())
        if tag in self._text:
            self._capture = tag

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == self._capture:
            self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._text[self._capture].append(data)

    @property
    def identifying_text(self) -> str:
        return " ".join(" ".join(parts) for parts in self._text.values()).strip()


class Smoke:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.failures: list[str] = []
        self._responses: dict[str, Response] = {}

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}" if path != "/" else f"{self.base_url}/"

    def fetch(self, path: str) -> Response | None:
        if path in self._responses:
            return self._responses[path]
        request = Request(self.url(path), headers={"User-Agent": "muxy-docs-smoke/2.0"})
        try:
            with urlopen(request, timeout=20) as response:
                result = Response(
                    status=response.status,
                    body=response.read(),
                    content_type=response.headers.get_content_type().lower(),
                    final_url=response.geturl(),
                )
        except HTTPError as exc:
            result = Response(
                status=exc.code,
                body=exc.read(),
                content_type=exc.headers.get_content_type().lower(),
                final_url=exc.geturl(),
            )
        except Exception as exc:
            self.fail(f"{path}: request failed: {exc}")
            return None
        self._responses[path] = result
        return result

    def expect(
        self,
        path: str,
        content_types: set[str],
        *,
        status: int = 200,
        nonempty: bool = True,
    ) -> Response | None:
        response = self.fetch(path)
        if response is None:
            return None
        if response.status != status:
            self.fail(f"{path}: expected status {status}, got {response.status} (final URL {response.final_url})")
        if nonempty and not response.body.strip():
            self.fail(f"{path}: response body is empty")
        if response.content_type not in content_types:
            expected = ", ".join(sorted(content_types))
            self.fail(f"{path}: content type {response.content_type!r}, expected one of {expected}")
        return response

    @property
    def request_count(self) -> int:
        return len(self._responses)


def parse_html(smoke: Smoke, path: str, response: Response) -> MetadataParser | None:
    try:
        text = response.body.decode("utf-8")
    except UnicodeDecodeError as exc:
        smoke.fail(f"{path}: HTML is not UTF-8: {exc}")
        return None
    parser = MetadataParser()
    try:
        parser.feed(text)
    except Exception as exc:
        smoke.fail(f"{path}: malformed HTML metadata: {exc}")
        return None
    if SOFT_404_RE.search(parser.identifying_text):
        smoke.fail(f"{path}: successful response looks like a soft 404 ({parser.identifying_text!r})")
    return parser


def normalized_url(url: str) -> tuple[str, str, str]:
    parsed = urlsplit(url)
    return parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/"


def expected_html_path(path: str) -> str:
    return "/" if path == "/" else f"{path.rstrip('/')}/"


def canonical_url(origin: str, path: str) -> str:
    return f"{origin.rstrip('/')}{expected_html_path(path)}"


def check_final_url(smoke: Smoke, path: str, response: Response, expected_path: str) -> None:
    expected = smoke.url(expected_path)
    if normalized_url(response.final_url) != normalized_url(expected):
        smoke.fail(f"{path}: final URL {response.final_url!r}, expected {expected!r}")


def check_canonical(smoke: Smoke, path: str, parser: MetadataParser, expected: str, response: Response) -> None:
    resolved = [urljoin(response.final_url, value) for value in parser.canonicals]
    if resolved != [expected]:
        smoke.fail(f"{path}: canonical links {resolved!r}, expected [{expected!r}]")


def parse_json(smoke: Smoke, path: str, response: Response | None) -> object | None:
    if response is None:
        return None
    try:
        return json.loads(response.body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        smoke.fail(f"{path}: invalid JSON: {exc}")
        return None


def parse_yaml(smoke: Smoke, path: str, response: Response | None) -> object | None:
    if response is None:
        return None
    try:
        return yaml.safe_load(response.body)
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        smoke.fail(f"{path}: invalid YAML: {exc}")
        return None


def decode_text(smoke: Smoke, path: str, response: Response | None) -> str:
    if response is None:
        return ""
    try:
        return response.body.decode("utf-8")
    except UnicodeDecodeError as exc:
        smoke.fail(f"{path}: body is not UTF-8: {exc}")
        return ""


def load_migration_manifest(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
        raise ValueError(f"{path} must contain a documents list")
    return payload


def validate_route_manifest(smoke: Smoke, payload: object) -> list[dict]:
    if not isinstance(payload, list) or not payload:
        smoke.fail("/route-manifest.json: root must be a non-empty array")
        return []
    routes: list[dict] = []
    required = {"canonical", "markdown", "status"}
    for index, route in enumerate(payload):
        if not isinstance(route, dict):
            smoke.fail(f"/route-manifest.json: route {index} is not an object")
            continue
        missing = required - route.keys()
        if missing:
            smoke.fail(f"/route-manifest.json: route {index} is missing {sorted(missing)}")
            continue
        if not all(isinstance(route[key], str) and route[key].startswith("/") for key in ("canonical", "markdown")):
            smoke.fail(f"/route-manifest.json: route {index} has invalid paths")
            continue
        if "redirect" in route and not isinstance(route["redirect"], str):
            smoke.fail(f"/route-manifest.json: route {index} has a non-string redirect")
            continue
        routes.append(route)
    return routes


def validate_search(smoke: Smoke, payload: object) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get("docs"), list):
        smoke.fail("/search/search_index.json: root must contain a docs array")
        return []
    docs: list[dict] = []
    for index, entry in enumerate(payload["docs"]):
        if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) for key in ("location", "title", "text")):
            smoke.fail(f"/search/search_index.json: docs[{index}] is malformed")
            continue
        docs.append(entry)
    if not docs:
        smoke.fail("/search/search_index.json: docs array is empty")
    return docs


def validate_sitemap(smoke: Smoke, response: Response | None) -> set[str]:
    if response is None:
        return set()
    try:
        root = ET.fromstring(response.body)
    except ET.ParseError as exc:
        smoke.fail(f"/sitemap.xml: invalid XML: {exc}")
        return set()
    if root.tag != "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset":
        smoke.fail(f"/sitemap.xml: unexpected root element {root.tag!r}")
    locations = {
        node.text.strip()
        for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text and node.text.strip()
    }
    if not locations:
        smoke.fail("/sitemap.xml: contains no URL locations")
    if any(urlsplit(location).scheme not in {"http", "https"} for location in locations):
        smoke.fail("/sitemap.xml: contains a non-HTTP URL")
    return locations


def validate_openapi(smoke: Smoke, path: str, payload: object) -> None:
    if not isinstance(payload, dict):
        smoke.fail(f"{path}: OpenAPI root must be an object")
        return
    if not str(payload.get("openapi", "")).startswith("3."):
        smoke.fail(f"{path}: missing OpenAPI 3.x version")
    if not isinstance(payload.get("info"), dict) or not isinstance(payload.get("paths"), dict) or not payload["paths"]:
        smoke.fail(f"{path}: must contain info and non-empty paths objects")


def indexing_tokens(values: list[str]) -> set[str]:
    return {token.strip() for value in values for token in value.split(",") if token.strip()}


def check_indexing(smoke: Smoke, path: str, parser: MetadataParser, mode: str) -> None:
    tokens = indexing_tokens(parser.robots)
    expected = {"index", "follow"} if mode == "production" else {"noindex", "nofollow"}
    if not expected.issubset(tokens):
        smoke.fail(f"{path}: robots metadata {sorted(tokens)!r}, expected {sorted(expected)!r} for {mode}")


def check_routes(
    smoke: Smoke,
    routes: list[dict],
    canonical_origin: str,
    indexing_mode: str,
    sitemap_locations: set[str],
) -> None:
    for route in routes:
        path = route["canonical"]
        response = smoke.expect(path, HTML_TYPES)
        if response is None:
            continue
        parser = parse_html(smoke, path, response)
        if parser is None:
            continue
        redirect = route.get("redirect")
        if redirect:
            expected_target = canonical_url(canonical_origin, redirect)
            check_canonical(smoke, path, parser, expected_target, response)
            if parser.refreshes != [redirect]:
                smoke.fail(f"{path}: refresh targets {parser.refreshes!r}, expected [{redirect!r}]")
            target = smoke.expect(redirect, HTML_TYPES)
            if target is not None:
                check_final_url(smoke, redirect, target, expected_html_path(redirect))
                target_parser = parse_html(smoke, redirect, target)
                if target_parser is not None:
                    check_canonical(smoke, redirect, target_parser, expected_target, target)
                    check_indexing(smoke, redirect, target_parser, indexing_mode)
        else:
            expected_path = expected_html_path(path)
            expected_canonical = canonical_url(canonical_origin, path)
            check_final_url(smoke, path, response, expected_path)
            check_canonical(smoke, path, parser, expected_canonical, response)
            if route.get("status") == "current":
                check_indexing(smoke, path, parser, indexing_mode)
                if expected_canonical not in sitemap_locations:
                    smoke.fail(f"{path}: current canonical is missing from sitemap.xml")
        smoke.expect(route["markdown"], MARKDOWN_TYPES)


def check_archives(
    smoke: Smoke,
    documents: list[dict],
    canonical_origin: str,
    routes: list[dict],
    search_docs: list[dict],
    sitemap_locations: set[str],
    llms: str,
    llms_full: str,
) -> None:
    published = {route["canonical"] for route in routes}
    search_locations = {entry["location"].lstrip("/") for entry in search_docs}
    for document in documents:
        if document.get("status") != "archived":
            continue
        path = f"/{document['section']}/{document['slug']}"
        markdown = f"{path}.md"
        response = smoke.expect(path, HTML_TYPES)
        if response is not None:
            check_final_url(smoke, path, response, expected_html_path(path))
            parser = parse_html(smoke, path, response)
            if parser is not None:
                check_canonical(smoke, path, parser, canonical_url(canonical_origin, path), response)
                tokens = indexing_tokens(parser.robots)
                if not {"noindex", "nofollow"}.issubset(tokens):
                    smoke.fail(f"{path}: archived page is not noindex, nofollow")
        smoke.expect(markdown, MARKDOWN_TYPES)

        search_path = path.lstrip("/") + "/"
        canonical = canonical_url(canonical_origin, path)
        leaked = []
        if any(location == search_path or location.startswith(search_path + "#") for location in search_locations):
            leaked.append("search")
        if canonical in sitemap_locations:
            leaked.append("sitemap")
        if markdown in llms:
            leaked.append("llms.txt")
        if f"Source: {canonical_origin.rstrip('/')}{markdown}" in llms_full:
            leaked.append("llms-full.txt")
        if path in published:
            leaked.append("route manifest")
        if leaked:
            smoke.fail(f"{path}: archived page leaked into {', '.join(leaked)}")


def check_robots(smoke: Smoke, robots: str, documents: list[dict], indexing_mode: str) -> None:
    directives = {line.strip().lower() for line in robots.splitlines() if line.strip()}
    if indexing_mode == "production":
        if "allow: /" not in directives or "disallow: /" in directives:
            smoke.fail("/robots.txt: production mode must allow root indexing")
    elif "disallow: /" not in directives or "allow: /" in directives:
        smoke.fail("/robots.txt: preview mode must disallow root indexing")
    for document in documents:
        if document.get("status") != "archived":
            continue
        route = f"/{document['section']}/{document['slug']}"
        for expected in (f"disallow: {route}/", f"disallow: {route}.md"):
            if expected.lower() not in directives:
                smoke.fail(f"/robots.txt: missing archived route directive {expected!r}")


def check_assets(smoke: Smoke, assets_root: Path) -> None:
    if not assets_root.is_dir():
        smoke.fail(f"vendored assets directory does not exist: {assets_root}")
        return
    assets = sorted(path for path in assets_root.rglob("*") if path.is_file())
    if not assets:
        smoke.fail(f"vendored assets directory is empty: {assets_root}")
        return
    for asset in assets:
        suffix = asset.suffix.lower()
        content_types = ASSET_TYPES.get(suffix)
        if content_types is None:
            smoke.fail(f"{asset}: no expected content type configured for vendored asset")
            continue
        path = "/assets/" + asset.relative_to(assets_root).as_posix()
        response = smoke.expect(path, content_types)
        if response is not None:
            check_final_url(smoke, path, response, path)
            if response.body != asset.read_bytes():
                smoke.fail(f"{path}: deployed bytes differ from vendored source {asset}")


def is_loopback(hostname: str | None) -> bool:
    if not hostname:
        return False
    if hostname == "localhost" or hostname.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def check_certificate(smoke: Smoke, base_url: str) -> None:
    parsed = urlsplit(base_url)
    if parsed.scheme.lower() != "https":
        return
    if not parsed.hostname:
        smoke.fail("HTTPS base URL has no hostname")
        return
    port = parsed.port or 443
    try:
        context = ssl.create_default_context()
        with socket.create_connection((parsed.hostname, port), timeout=20) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=parsed.hostname) as tls_socket:
                certificate = tls_socket.getpeercert()
        not_before = certificate.get("notBefore")
        not_after = certificate.get("notAfter")
        if not not_before or not not_after:
            smoke.fail("HTTPS certificate is missing validity timestamps")
            return
        now = datetime.now(timezone.utc).timestamp()
        starts = ssl.cert_time_to_seconds(not_before)
        expires = ssl.cert_time_to_seconds(not_after)
        if now < starts:
            smoke.fail(f"HTTPS certificate is not valid until {not_before}")
        if now >= expires:
            smoke.fail(f"HTTPS certificate expired at {not_after}")
    except Exception as exc:
        smoke.fail(f"HTTPS certificate validation failed for {parsed.hostname}:{port}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://docs.muxy.io")
    parser.add_argument("--migration-manifest", type=Path, default=Path("migration/manifest.yaml"))
    parser.add_argument("--assets-root", type=Path, default=Path("docs/assets"))
    parser.add_argument("--canonical-origin", default="https://docs.muxy.io")
    parser.add_argument(
        "--indexing-mode",
        choices=("production", "preview"),
        help="expected robots/meta policy; required for a loopback base URL and defaults to production otherwise",
    )
    args = parser.parse_args()

    parsed_base = urlsplit(args.base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.hostname:
        parser.error("--base-url must be an absolute HTTP(S) URL")
    if is_loopback(parsed_base.hostname) and args.indexing_mode is None:
        parser.error("--indexing-mode is required when --base-url is loopback")
    indexing_mode = args.indexing_mode or "production"

    try:
        migration = load_migration_manifest(args.migration_manifest)
    except Exception as exc:
        print(f"Cannot load migration manifest: {exc}", file=sys.stderr)
        return 2

    smoke = Smoke(args.base_url)
    check_certificate(smoke, args.base_url)

    route_response = smoke.expect("/route-manifest.json", JSON_TYPES)
    search_response = smoke.expect("/search/search_index.json", JSON_TYPES)
    sitemap_response = smoke.expect("/sitemap.xml", XML_TYPES)
    llms_response = smoke.expect("/llms.txt", TEXT_TYPES)
    llms_full_response = smoke.expect("/llms-full.txt", TEXT_TYPES)
    robots_response = smoke.expect("/robots.txt", TEXT_TYPES)

    routes = validate_route_manifest(smoke, parse_json(smoke, "/route-manifest.json", route_response))
    search_docs = validate_search(smoke, parse_json(smoke, "/search/search_index.json", search_response))
    sitemap_locations = validate_sitemap(smoke, sitemap_response)
    llms = decode_text(smoke, "/llms.txt", llms_response)
    llms_full = decode_text(smoke, "/llms-full.txt", llms_full_response)
    robots = decode_text(smoke, "/robots.txt", robots_response)

    for path in ("/openapi/rest-v1.yaml", "/openapi/sandbox-v1.yaml"):
        response = smoke.expect(path, YAML_TYPES)
        validate_openapi(smoke, path, parse_yaml(smoke, path, response))

    check_robots(smoke, robots, migration["documents"], indexing_mode)
    check_routes(smoke, routes, args.canonical_origin, indexing_mode, sitemap_locations)
    check_archives(
        smoke,
        migration["documents"],
        args.canonical_origin,
        routes,
        search_docs,
        sitemap_locations,
        llms,
        llms_full,
    )
    check_assets(smoke, args.assets_root)

    missing_path = "/__muxy_smoke_missing_7e63f1d5__/"
    missing = smoke.expect(missing_path, HTML_TYPES, status=404)
    if missing is not None and missing.status == 200:
        smoke.fail(f"{missing_path}: missing route returned a soft-404 200 response")

    if smoke.failures:
        print("Production smoke failed:", file=sys.stderr)
        for failure in smoke.failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"Smoke passed in {indexing_mode} indexing mode: "
        f"{smoke.request_count} unique requests, {len(routes)} published routes, "
        f"{len([path for path in args.assets_root.rglob('*') if path.is_file()])} vendored assets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
