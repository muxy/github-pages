#!/usr/bin/env python3
"""Run structural accessibility and mobile-overflow checks on every current page."""

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
    # current-pages.txt contains absolute loopback URLs. Preserve only each URL path so callers can use another host.
    routes = [urlparse(url).path or "/" for url in urls]
    failures = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        for route in routes:
            url = args.base_url.rstrip("/") + route
            response = page.goto(url, wait_until="domcontentloaded")
            prefix = route
            if response is None or not response.ok:
                failures.append(f"{prefix}: failed to load")
                continue
            result = page.evaluate(
                """() => {
                  const main = document.querySelector('main');
                  const ids = [...document.querySelectorAll('[id]')].map(el => el.id);
                  const duplicates = ids.filter((id, index) => id && ids.indexOf(id) !== index);
                  const badImages = [...(main?.querySelectorAll('img') || [])].filter(img =>
                    !img.hasAttribute('alt') || !img.naturalWidth || !img.naturalHeight ||
                    !img.hasAttribute('width') || !img.hasAttribute('height'));
                  const unnamedLinks = [...document.querySelectorAll('a[href]')].filter(el =>
                    !(el.textContent || '').trim() && !el.getAttribute('aria-label') &&
                    !el.getAttribute('title') && !el.querySelector('img[alt]:not([alt=""])'));
                  const unnamedButtons = [...document.querySelectorAll('button')].filter(el =>
                    !(el.textContent || '').trim() && !el.getAttribute('aria-label') && !el.getAttribute('title'));
                  return {
                    h1: main?.querySelectorAll('h1').length || 0,
                    duplicateIds: [...new Set(duplicates)],
                    badImages: badImages.length,
                    unnamedLinks: unnamedLinks.length,
                    unnamedButtons: unnamedButtons.length,
                    lang: document.documentElement.lang,
                    main: Boolean(main),
                    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
                  };
                }"""
            )
            if result["h1"] != 1:
                failures.append(f"{prefix}: expected one main H1, found {result['h1']}")
            if result["duplicateIds"]:
                failures.append(f"{prefix}: duplicate IDs {', '.join(result['duplicateIds'])}")
            for key, label in (("badImages", "broken, unlabelled, or unsized images"), ("unnamedLinks", "unnamed links"), ("unnamedButtons", "unnamed buttons")):
                if result[key]:
                    failures.append(f"{prefix}: {result[key]} {label}")
            if not result["lang"]:
                failures.append(f"{prefix}: document language is missing")
            if not result["main"]:
                failures.append(f"{prefix}: main landmark is missing")
            if result["overflow"]:
                failures.append(f"{prefix}: horizontal overflow at 390px")
        context.close()
        browser.close()

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Accessibility structure and 390px layout passed for {len(routes)} current pages")


if __name__ == "__main__":
    main()
