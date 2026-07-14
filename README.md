# Muxy Documentation Site

This repository is the static, agent-readable replacement for the ReadMe project at `docs.muxy.io`. MkDocs Material builds the site and GitHub Pages hosts it. ReadMe remains the production host until the approval and route-parity gates in `CUTOVER.md` pass.

## Local development

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_docs.py
.venv/bin/python scripts/generate_api_reference.py
.venv/bin/python scripts/serve_preview.py
```

`serve_preview.py` rebuilds and serves the exact GitHub Pages artifact, including raw `.md` routes, OpenAPI, `llms.txt`, `llms-full.txt`, robots, sitemap, route manifest, and legacy recipe aliases. Use `mkdocs serve` only for fast authoring when those generated contracts are not under test.

The committed ReadMe snapshot makes normal builds deterministic and offline. A deliberate upstream refresh is the only command that reads the legacy host:

```bash
.venv/bin/python scripts/import_readme.py --refresh
.venv/bin/python scripts/generate_api_reference.py --write
.venv/bin/python scripts/normalize_code_fences.py
```

Review the resulting manifest, source, assets, and OpenAPI diff before committing it.

After changing document ownership, version, status, or review metadata, synchronize the migration ledger and review its diff:

```bash
.venv/bin/python scripts/assign_page_types.py
.venv/bin/python scripts/sync_manifest.py
```

Approved pages carry the approver, UTC timestamp, method, and a SHA-256 digest of
their substantive metadata and Markdown. Any later edit invalidates the approval.
Record an explicitly authorized approval batch with an expected-count guard, then
synchronize the ledger:

```bash
.venv/bin/python scripts/approve_docs.py \
  --approved-by <github-login> \
  --approved-at <YYYY-MM-DDTHH:MM:SSZ> \
  --approval-method <review-method> \
  --expected-count <count>
.venv/bin/python scripts/sync_manifest.py
```

## Reproduce CI locally

```bash
.venv/bin/python scripts/validate_docs.py
.venv/bin/python scripts/generate_api_reference.py
.venv/bin/python scripts/verify_sdk_sources.py --online
.venv/bin/python scripts/verify_sdk_snippets.py --online
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/generate_site_contracts.py
.venv/bin/python scripts/validate_docs.py --site site
.venv/bin/python -m http.server 8000 --directory site
```

With the local server running, execute responsive browser checks with:

```bash
.venv/bin/python scripts/render_checks.py --base-url http://127.0.0.1:8000
.venv/bin/python scripts/accessibility_checks.py --base-url http://127.0.0.1:8000
.venv/bin/python scripts/no_js_checks.py --base-url http://127.0.0.1:8000
.venv/bin/python scripts/smoke_production.py --base-url http://127.0.0.1:8000 --indexing-mode preview
```

These checks cover every current page at 390px and 1280px in light and dark themes,
verify mobile accessibility structure, and prove that the documentation remains
readable when JavaScript is disabled. Representative full-page screenshots are saved
under `artifacts/visual/`.

## Repository contracts

- `migration/manifest.yaml` accounts for all legacy pages and records route, ownership, status, version, and review state.
- `migration/snippet-sources.yaml` pins released SDK artifacts, source files, hashes, and the documented API surface used by examples.
- `migration/readme/` is the immutable source snapshot for a migration run.
- `openapi/` is canonical for generated REST endpoint reference.
- `docs/` contains current and archived authored pages; archived pages are excluded from navigation and indexes.
- `site/*.md`, `site/llms*.txt`, route manifests, robots, sitemap, and raw OpenAPI are generated build artifacts.
- `.github/workflows/deploy.yml` validates and previews/publishes the site.
- `.github/workflows/smoke.yml` checks production route and agent-interface parity each day.

New or substantially rewritten pages should start from a template in `migration/templates/`. See `CUTOVER.md` for ownership, approval, DNS, rollback, and decommissioning procedures.
