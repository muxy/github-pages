#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


SCREENSHOT_PAGES = ("/", "/docs/unity-gateway-tutorial/", "/reference/extension-config-1/")
VIEWPORTS = (("mobile", 390, 844), ("desktop", 1280, 900))
SCHEMES = ("light", "dark")
CODE_PAGE = "/reference/extension-config-1/"
MOBILE_NAV_TARGET = "/docs/quick-start/"
SEARCH_TERM = "Gateway"


def load_page(page, base_url: str, route: str) -> None:
    response = page.goto(base_url.rstrip("/") + route, wait_until="networkidle")
    if response is None or not response.ok:
        raise AssertionError(f"failed to load {route}")


def check_keyboard_skip(browser, base_url: str) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    try:
        page = context.new_page()
        load_page(page, base_url, CODE_PAGE)
        skip = page.locator("a.md-skip")
        if skip.count() != 1:
            raise AssertionError(f"expected one keyboard skip link, found {skip.count()}")

        page.evaluate("document.activeElement?.blur()")
        page.keyboard.press("Tab")
        state = skip.evaluate(
            """element => {
              const style = getComputedStyle(element);
              const rect = element.getBoundingClientRect();
              return {
                focused: document.activeElement === element,
                inViewport: rect.width > 0 && rect.height > 0 && rect.bottom > 0 && rect.right > 0 &&
                  rect.top < innerHeight && rect.left < innerWidth,
                focusRing: (style.outlineStyle !== "none" && parseFloat(style.outlineWidth) > 0) ||
                  style.boxShadow !== "none"
              };
            }"""
        )
        if not state["focused"]:
            raise AssertionError("first Tab did not focus the skip link")
        if not state["inViewport"]:
            raise AssertionError("focused skip link is outside the viewport")
        if not state["focusRing"]:
            raise AssertionError("focused skip link has no visible focus indicator")

        target = urlparse(skip.get_attribute("href") or "").fragment
        page.keyboard.press("Enter")
        if not target or urlparse(page.url).fragment != target:
            raise AssertionError("activating the skip link did not navigate to its content target")
    finally:
        context.close()


def check_search(browser, base_url: str) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    try:
        page = context.new_page()
        load_page(page, base_url, "/")
        query = page.locator('[data-md-component="search-query"]')
        query.click()
        # Material's search observes keyboard events, so drive it as a user would instead of assigning the value.
        query.press_sequentially(SEARCH_TERM, delay=20)
        results = page.locator(".md-search-result__item")
        results.first.wait_for(state="visible")
        result_text = "\n".join(results.all_inner_texts())
        if SEARCH_TERM.casefold() not in result_text.casefold():
            raise AssertionError(f"search returned no result containing {SEARCH_TERM!r}")
        if not all(results.nth(index).locator("a[href]").count() for index in range(results.count())):
            raise AssertionError("search returned a result without a destination link")
    finally:
        context.close()


def check_theme_switch(browser, base_url: str) -> None:
    context = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    try:
        page = context.new_page()
        load_page(page, base_url, "/")
        initial_scheme = page.locator("body").get_attribute("data-md-color-scheme")
        toggle = page.locator('[data-md-component="palette"] label:visible')
        if toggle.count() != 1:
            raise AssertionError(f"expected one visible theme toggle, found {toggle.count()}")
        target_id = toggle.get_attribute("for")
        target = page.locator(f"#{target_id}") if target_id else None
        expected_scheme = target.get_attribute("data-md-color-scheme") if target else None
        if not expected_scheme or expected_scheme == initial_scheme:
            raise AssertionError("theme toggle does not target a different color scheme")

        toggle.click()
        page.wait_for_function(
            "expected => document.body.dataset.mdColorScheme === expected", arg=expected_scheme
        )
        page.reload(wait_until="networkidle")
        if page.locator("body").get_attribute("data-md-color-scheme") != expected_scheme:
            raise AssertionError("selected theme did not persist after reload")
    finally:
        context.close()


def check_code_copy(browser, base_url: str) -> None:
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        color_scheme="light",
        permissions=["clipboard-read", "clipboard-write"],
    )
    try:
        page = context.new_page()
        load_page(page, base_url, CODE_PAGE)
        button = page.locator("main button.md-clipboard").first
        code = button.locator("xpath=ancestor::pre[1]/code")
        if button.count() != 1 or code.count() != 1:
            raise AssertionError("representative code block or its copy control is missing")
        expected = (code.text_content() or "").rstrip()
        if not expected:
            raise AssertionError("representative code block is empty")

        sentinel = "clipboard-not-yet-copied"
        page.evaluate("value => navigator.clipboard.writeText(value)", sentinel)
        button.click()
        page.wait_for_function(
            "value => navigator.clipboard.readText().then(text => text !== value)", arg=sentinel
        )
        actual = page.evaluate("navigator.clipboard.readText()")
        if actual != expected:
            raise AssertionError("copy control did not write the displayed code to the clipboard")
    finally:
        context.close()


def check_mobile_navigation(browser, base_url: str) -> None:
    context = browser.new_context(viewport={"width": 390, "height": 844}, color_scheme="light")
    try:
        page = context.new_page()
        load_page(page, base_url, "/")
        drawer = page.locator('[data-md-toggle="drawer"]')
        menu = page.locator('label.md-header__button[for="__drawer"]')
        if drawer.count() != 1 or menu.count() != 1 or not menu.is_visible():
            raise AssertionError("mobile navigation toggle is missing or hidden")

        menu.click()
        page.wait_for_function(
            """() => {
              const drawer = document.querySelector('[data-md-toggle="drawer"]');
              const nav = document.querySelector('.md-sidebar--primary');
              return drawer?.checked && nav?.getBoundingClientRect().left >= -1;
            }"""
        )
        target = page.get_by_role("link", name="Quick Start", exact=True)
        if target.count() != 1 or not target.is_visible():
            raise AssertionError("mobile drawer did not expose the Quick Start link")
        target.click()
        page.wait_for_url(f"**{MOBILE_NAV_TARGET}")
        if urlparse(page.url).path != MOBILE_NAV_TARGET:
            raise AssertionError(f"mobile navigation did not reach {MOBILE_NAV_TARGET}")
        if drawer.is_checked():
            raise AssertionError("mobile drawer remained open after navigation")
    finally:
        context.close()


def run_interaction_checks(browser, base_url: str, failures: list[str]) -> None:
    checks = (
        ("keyboard skip/focus", check_keyboard_skip),
        ("search results", check_search),
        ("theme switching", check_theme_switch),
        ("mobile navigation", check_mobile_navigation),
        ("code copy", check_code_copy),
    )
    for label, check in checks:
        try:
            check(browser, base_url)
        except Exception as error:  # Keep the full page matrix running and report every failed interaction together.
            failures.append(f"interaction {label}: {error}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--routes", default="site/current-pages.txt")
    args = parser.parse_args()
    urls = [url for url in Path(args.routes).read_text(encoding="utf-8").splitlines() if url]
    routes = [urlparse(url).path or "/" for url in urls]
    artifacts = Path("artifacts/visual")
    artifacts.mkdir(parents=True, exist_ok=True)
    failures = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for scheme in SCHEMES:
            for label, width, height in VIEWPORTS:
                context = browser.new_context(viewport={"width": width, "height": height}, color_scheme=scheme)
                page = context.new_page()
                for route in routes:
                    response = page.goto(args.base_url.rstrip("/") + route, wait_until="domcontentloaded")
                    prefix = f"{scheme} {label} {route}"
                    if response is None or not response.ok:
                        failures.append(f"{prefix}: failed to load")
                        continue
                    overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
                    if overflow:
                        failures.append(f"{prefix}: horizontal overflow")
                    bad_images = page.locator("main img").evaluate_all(
                        "els => els.filter(img => !img.alt || !img.naturalWidth || !img.naturalHeight).length"
                    )
                    if bad_images:
                        failures.append(f"{prefix}: {bad_images} inaccessible or broken images")
                    headings = page.locator("main h1").count()
                    if headings != 1:
                        failures.append(f"{prefix}: expected one rendered H1, found {headings}")
                    if page.locator('[data-md-component="palette"]').count() != 1:
                        failures.append(f"{prefix}: theme switcher is missing")
                    if page.locator("a.md-skip").count() != 1:
                        failures.append(f"{prefix}: keyboard skip link is missing")
                    code_blocks = page.locator("main pre > code").count()
                    copy_controls = page.locator("main button.md-clipboard").count()
                    if code_blocks and copy_controls < code_blocks:
                        failures.append(
                            f"{prefix}: found {code_blocks} code blocks but only {copy_controls} code-copy controls"
                        )
                    if route in SCREENSHOT_PAGES:
                        name = "home" if route == "/" else route.strip("/").replace("/", "-")
                        page.screenshot(path=artifacts / f"{name}-{scheme}-{label}.png", full_page=True)
                context.close()
        run_interaction_checks(browser, args.base_url, failures)
        browser.close()
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"Responsive rendering passed for {len(routes)} current pages in light/dark themes at "
        f"{', '.join(str(width) + 'px' for _, width, _ in VIEWPORTS)}; "
        f"captured {len(SCREENSHOT_PAGES) * len(VIEWPORTS) * len(SCHEMES)} representative screenshots; "
        "keyboard skip/focus, search, theme switching, mobile navigation, and code copy passed"
    )


if __name__ == "__main__":
    main()
