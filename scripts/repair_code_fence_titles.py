#!/usr/bin/env python3
"""Restore code lines consumed by the historical multiline caption bug.

The buggy normalizer preserved the consumed line losslessly in ``title=``. This
repair intentionally recognizes code-shaped titles only; legitimate filename and
human-readable captions stay attached to the fence.
"""

from __future__ import annotations

import json
import re

from docs_common import DOCS


FENCE_RE = re.compile(
    r'^(?P<indent>[ \t]*)```(?P<language>[^ \t\r\n`]+)'
    r'(?P<before>.*?)[ \t]+title="(?P<title>(?:\\.|[^"\\])*)"'
    r'(?P<after>[ \t].*)?$',
    re.MULTILINE,
)

CODE_PREFIX_RE = re.compile(
    r"^(?:"
    r"import\b|export\b|from\b|const\b|let\b|var\b|return\b|async\b|await\b|try\b|"
    r"using\b|namespace\b|class\b|public\b|private\b|protected\b|static\b|"
    r"#(?:include|define|if|pragma)\b|template\s*<|gamelink::|std::|auto\b|void\b|int\b|bool\b|"
    r"curl\b|cp\b|npm\b|npx\b|yarn\b|pnpm\b|git\b|pip\b|python\b|dotnet\b|"
    r"GET\b|POST\b|PUT\b|PATCH\b|DELETE\b|Authorization:|Content-Type:|"
    r"https?://|wss?://|VITE_|REACT_APP_|MUXY_|"
    r"Muxy\.|medkit\.|sdk\.|GameLink\.|Gateway\.|"
    r"[\[{<]|//|/\*|<!--|\$\s|>\s"
    r")"
)


def decode_title(value: str) -> str:
    return json.loads(f'"{value}"')


def looks_like_code(value: str) -> bool:
    stripped = value.strip()
    if CODE_PREFIX_RE.match(stripped):
        return True
    if any(token in stripped for token in (" => ", ";", " = ", "()", "::")):
        return True
    if re.match(r"^[A-Za-z_$][\w.$]*(?:\[[^]]+\])?\s*[=(]", stripped):
        return True
    if re.match(r"^[A-Za-z_$][\w.$]*\s*:\s*(?:true|false|null|[\d\"'{[])" , stripped):
        return True
    return False


def repair(text: str) -> tuple[str, int]:
    repaired = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal repaired
        title = decode_title(match.group("title"))
        if not looks_like_code(title):
            return match.group(0)
        repaired += 1
        opening = (
            f'{match.group("indent")}```{match.group("language")}'
            f'{match.group("before")}{match.group("after") or ""}'
        ).rstrip()
        return f"{opening}\n{match.group('indent')}{title}"

    return FENCE_RE.sub(replace, text), repaired


def main() -> None:
    files_changed = 0
    lines_restored = 0
    for path in sorted(DOCS.rglob("*.md")):
        before = path.read_text(encoding="utf-8")
        after, count = repair(before)
        if count:
            path.write_text(after, encoding="utf-8")
            files_changed += 1
            lines_restored += count
    print(f"Restored {lines_restored} code lines across {files_changed} documents")


if __name__ == "__main__":
    main()
