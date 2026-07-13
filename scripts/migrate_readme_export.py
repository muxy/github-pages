from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
BLOCK_RE = re.compile(r"\[block:([^\]]+)\]\s*(\{.*?\})\s*\[/block\]", re.DOTALL)
README_LINK_RE = re.compile(r"\]\((doc|ref):([^)]+)\)")


def extract_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values, text[match.end() :]


def build_slug_map() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = extract_frontmatter(text)
        slug = frontmatter.get("slug")
        if slug and slug not in mapping:
            mapping[slug] = path
    return mapping


def escape_cell(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\n", "<br>")
    value = value.replace("|", "\\|")
    return value.strip()


def convert_parameters(payload: dict) -> str:
    data = payload.get("data", {})
    cols = int(payload.get("cols", 0))
    rows = int(payload.get("rows", 0))
    if not data or cols <= 0:
        return ""

    headers = [escape_cell(str(data.get(f"h-{col}", ""))) for col in range(cols)]
    if not any(headers):
        headers = [f"Column {col + 1}" for col in range(cols)]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * cols) + " |",
    ]

    for row in range(rows):
        cells = [escape_cell(str(data.get(f"{row}-{col}", ""))) for col in range(cols)]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def convert_image(payload: dict) -> str:
    images = payload.get("images", [])
    lines: list[str] = []
    for item in images:
        image = item.get("image") if isinstance(item, dict) else None
        if not image or not image[0]:
            continue
        url = image[0]
        alt = image[2] if len(image) > 2 and image[2] else Path(url).stem
        lines.append(f"![{alt}]({url})")
    return "\n\n".join(lines)


def convert_api_header(payload: dict) -> str:
    title = str(payload.get("title", "")).strip()
    return f"## {title}" if title else ""


def convert_tutorial_tile(payload: dict) -> str:
    title = str(payload.get("title", "")).strip()
    link = str(payload.get("link", "")).strip()
    if title and link:
        return f"> Tutorial: [{title}]({link})"
    if title:
        return f"> Tutorial: {title}"
    return ""


def convert_block(match: re.Match[str]) -> str:
    block_type = match.group(1)
    raw_json = match.group(2)
    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError:
        return match.group(0)

    converters = {
        "image": convert_image,
        "api-header": convert_api_header,
        "parameters": convert_parameters,
        "tutorial-tile": convert_tutorial_tile,
    }
    converter = converters.get(block_type)
    if not converter:
        return match.group(0)

    converted = converter(payload).strip()
    return f"\n\n{converted}\n\n" if converted else "\n\n"


def relative_link(from_path: Path, to_path: Path, anchor: str | None = None) -> str:
    rel = to_path.relative_to(DOCS)
    source_dir = from_path.parent.relative_to(DOCS)
    target = Path(*([".."] * len(source_dir.parts))) / rel
    link = target.as_posix()
    if anchor:
        link += "#" + quote(anchor, safe="-_")
    return link


def convert_readme_links(text: str, path: Path, slug_map: dict[str, Path]) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(2)
        slug, _, anchor = target.partition("#")
        target_path = slug_map.get(slug)
        if not target_path:
            return f"]({target})"
        return f"]({relative_link(path, target_path, anchor or None)})"

    return README_LINK_RE.sub(replace, text)


def ensure_homepage() -> None:
    index = DOCS / "index.md"
    if index.exists():
        return

    index.write_text(
        """---
title: Muxy Documentation
---

# Muxy Documentation

Welcome to the Muxy developer documentation.

## Start Here

- [Quick Start for Developers](v1.0/Documentation/quick-start.md)
- [Unity Gateway Tutorial](v1.0/Integrate%20with%20Unity/unity-gateway-tutorial.md)
- [MEDKit REST API](v1.0/REST%20API/medkit-rest-api.md)
- [GameLink WebSocket API](v1.0/GameLink%20WebSocket%20API/websocket-protocol.md)
- [Changelog](Changelog%20Posts/gamelink-release.md)
""",
        encoding="utf-8",
    )


def migrate() -> None:
    slug_map = build_slug_map()
    for path in DOCS.rglob("*.md"):
        original = path.read_text(encoding="utf-8")
        migrated = BLOCK_RE.sub(convert_block, original)
        migrated = convert_readme_links(migrated, path, slug_map)
        if migrated != original:
            path.write_text(migrated, encoding="utf-8", newline="\n")
    ensure_homepage()


if __name__ == "__main__":
    migrate()

