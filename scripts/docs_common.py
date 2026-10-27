from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MANIFEST = ROOT / "migration" / "manifest.yaml"
OPENAPI = ROOT / "openapi"
PAGE_TYPES = {
    "quickstart",
    "task-guide",
    "concept",
    "sdk-reference",
    "protocol-reference",
    "troubleshooting",
}
APPROVAL_EVIDENCE_FIELDS = (
    "approved_by",
    "approved_at",
    "approval_method",
    "approved_content_sha256",
)

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
JSON_FENCE_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def classify_page_type(path: Path, metadata: dict[str, Any]) -> str:
    """Assign one of the six editorial templates from stable route/product metadata."""
    slug = str(metadata.get("slug", path.stem))
    product = str(metadata.get("product", ""))
    relative = path.relative_to(DOCS) if path.is_absolute() else path
    section = relative.parts[0] if len(relative.parts) > 1 else "home"
    if "troubleshoot" in slug:
        return "troubleshooting"
    if "quick-start" in slug or "quickstart" in slug or slug in {"getting-started-with-medkit"}:
        return "quickstart"
    if section == "reference" and product in {"Unity", "Gateway", "GameLink Native", "Unreal"}:
        return "sdk-reference"
    if section == "reference" or product in {"REST API", "GameLink WebSocket"}:
        return "protocol-reference"
    concept_slugs = {
        "index",
        "gamelink-release",
        "developing-with-medkit",
        "data-tracking",
        "state-information",
        "store-configuration-data",
        "data-aggregation-techniques",
        "viewer-engagement-tools",
        "accumulation",
        "ranking",
        "voting",
    }
    if slug in concept_slugs or section == "changelog":
        return "concept"
    return "task-guide"


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    return data, text[match.end() :]


def render_frontmatter(data: dict[str, Any], body: str) -> str:
    frontmatter = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{frontmatter}\n---\n\n{body.lstrip()}".rstrip() + "\n"


def approval_content_sha256(metadata: dict[str, Any], body: str) -> str:
    """Hash all substantive page metadata and the exact Markdown body.

    Approval evidence is excluded so approver identity and timestamps can be
    audited without creating a self-referential digest. Review state, version,
    ownership, and source provenance remain part of the approved content.
    """
    content_metadata = {
        key: value
        for key, value in metadata.items()
        if key not in APPROVAL_EVIDENCE_FIELDS
    }
    payload = json.dumps(
        content_metadata,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(f"{payload}\n---\n{body}".encode("utf-8")).hexdigest()


def json_fence_language(content: str) -> str:
    try:
        json.loads(content)
        return "json"
    except (json.JSONDecodeError, TypeError):
        return "jsonc" if content.lstrip().startswith(("{", "[")) else "text"


def normalize_json_fences(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        content = match.group(1)
        return f"```{json_fence_language(content)}\n{content}\n```"

    return JSON_FENCE_RE.sub(replace, text)


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def canonical_path(document: dict[str, Any], markdown: bool = False) -> str:
    suffix = ".md" if markdown else ""
    if document["section"] == "home":
        return "/"
    return f"/{document['section']}/{document['slug']}{suffix}"


def source_path(document: dict[str, Any]) -> Path:
    return ROOT / document["target_file"]
