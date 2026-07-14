#!/usr/bin/env python3
"""Correct legacy code-fence labels without changing example payloads."""

from __future__ import annotations

import re

from docs_common import DOCS, normalize_json_fences


# Keep this expression strictly line-local. ``\s`` also matches newlines and can
# accidentally consume the first line of a code block as its caption.
FENCE_WITH_CAPTION_RE = re.compile(
    r"^([ \t]*)```([^ \t\r\n`]+)[ \t]+(.+?)[ \t]*$", re.MULTILINE
)
LANGUAGE_ALIASES = {"C#": "csharp", "JSON": "json"}


def normalize_fence_captions(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        indent, language, caption = match.groups()
        language = LANGUAGE_ALIASES.get(language, language.lower())
        if language in {"json", "jsonc"} and caption.startswith(("{", "[")):
            return f"{indent}```{language}\n{indent}{caption}"
        if caption.startswith(("title=", "linenums=", "hl_lines=", "{")):
            return f"{indent}```{language} {caption}"
        escaped = caption.replace("\\", "\\\\").replace('"', '\\"')
        return f'{indent}```{language} title="{escaped}"'

    return FENCE_WITH_CAPTION_RE.sub(replace, text)


def main() -> None:
    changed = 0
    for path in sorted(DOCS.rglob("*.md")):
        before = path.read_text(encoding="utf-8")
        after = normalize_fence_captions(normalize_json_fences(before))
        if before != after:
            path.write_text(after, encoding="utf-8")
            changed += 1
    print(f"Normalized code-fence labels in {changed} documents")


if __name__ == "__main__":
    main()
