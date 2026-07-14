#!/usr/bin/env python3
"""Prove that every current documentation page remains useful without JavaScript."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--routes", default="site/current-pages.txt")
    args = parser.parse_args()
    urls = [url for url in Path(args.routes).read_text(encoding="utf-8").splitlines() if url]
    routes = [urlparse(url).path or "/" for url in urls]
    failures: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(
            java_script_enabled=False,
            viewport={"width": 390, "height": 844},
        )
        page = context.new_page()
        for route in routes:
            response = page.goto(args.base_url.rstrip("/") + route, wait_until="domcontentloaded")
            if response is None or not response.ok:
                failures.append(f"{route}: failed to load without JavaScript")
                continue
            result = page.evaluate(
                r"""() => {
                  const main = document.querySelector('main');
                  const article = main?.querySelector('article');
                  const text = (article?.innerText || '').replace(/\s+/g, ' ').trim();
                  const style = article ? getComputedStyle(article) : null;
                  return {
                    main: Boolean(main),
                    article: Boolean(article),
                    h1: article?.querySelectorAll('h1').length || 0,
                    textLength: text.length,
                    visible: Boolean(style && style.display !== 'none' && style.visibility !== 'hidden'),
                    links: article?.querySelectorAll('a[href]').length || 0
                  };
                }"""
            )
            if not result["main"]:
                failures.append(f"{route}: main landmark is missing without JavaScript")
            if not result["article"] or not result["visible"]:
                failures.append(f"{route}: documentation article is not visible without JavaScript")
            if result["h1"] != 1:
                failures.append(f"{route}: expected one article H1 without JavaScript, found {result['h1']}")
            if result["textLength"] < 80:
                failures.append(f"{route}: documentation content is too short without JavaScript")
        context.close()
        browser.close()

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"No-JavaScript readability passed for {len(routes)} current pages at 390px")


if __name__ == "__main__":
    main()
