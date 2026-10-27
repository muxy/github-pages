# docs.muxy.io Cutover Runbook

This runbook is approval-gated. Preview deployments do not authorize a DNS change or removal of the ReadMe project.

## Fixed cutover values

| Item | Value |
| --- | --- |
| Production hostname | `docs.muxy.io` |
| Old ReadMe CNAME | `ssl.readmessl.com` |
| New GitHub Pages CNAME | `muxy.github.io` |
| Target DNS TTL | `300` seconds |
| Production URL | `https://docs.muxy.io` |

Do not substitute a Pages IP address or a repository-specific hostname for `muxy.github.io`.

## Ownership and review

The migration manifest is the release ledger. Each current row must have a confirmed version and `review_state: approved` before cutover. Approved rows must also carry `approved_by`, `approved_at`, `approval_method`, and `approved_content_sha256`; validation recomputes the digest and invalidates approval after any substantive page or metadata change.

The normal Pages workflow publishes a review build at the GitHub project URL while these gates are open. It does not authorize the `docs.muxy.io` DNS change. Run **Verify docs production cutover gate** from the exact commit intended for production immediately before configuring the custom domain.

| Domain | Required approver |
| --- | --- |
| Information architecture, accessibility, and editorial quality | Developer Experience |
| REST OpenAPI and generated endpoint reference | API Platform |
| MEDKit, Gateway, Unity, Unreal, WebSocket, and native-library content | Owning SDK or protocol team |

`blocked-release` means the source repository has no confirmed public release tag. Do not turn it into `approved` based on an untagged branch.

## Pre-cutover gates

1. Freeze ReadMe edits or refresh the snapshot and review the complete deterministic diff.
2. Confirm the manifest totals remain 87 legacy files: 72 current, 14 archived, and one homepage.
3. Obtain the owner approval recorded on every current manifest row and confirm every SDK example against a supported release tag.
4. Run **Verify docs production cutover gate** on the release SHA. The workflow, commit, and Pages deployment must all identify the same SHA.
5. Run the deploy workflow and inspect its route, OpenAPI drift, link, responsive, accessibility, and Lighthouse results.
6. Exercise the Pages preview at 390 px and 1280 px, including search, keyboard focus, theme switching, code copy, raw Markdown, and API specifications.
7. Build the preview artifact, serve it on loopback, and retain the smoke output:

   ```sh
   mkdocs build --strict
   python scripts/generate_site_contracts.py
   python -m http.server 8000 --directory site
   ```

   In another terminal:

   ```sh
   python scripts/smoke_production.py \
     --base-url http://127.0.0.1:8000 \
     --indexing-mode preview
   ```

8. Confirm the preview smoke proves that archived pages remain available by direct HTML and Markdown URL but are absent from search, sitemap, `llms.txt`, and `llms-full.txt`; it must also prove the preview is `noindex, nofollow`.
9. Verify GitHub Pages domain ownership for `docs.muxy.io` without changing production DNS.
10. Keep the repository variable `DOCS_PRODUCTION=false` while the project-URL preview is under review.
11. At least 48 hours before the window, change the `docs.muxy.io` DNS TTL to exactly `300` while leaving its CNAME as `ssl.readmessl.com`. Confirm the authoritative answer:

    ```sh
    dig +noall +answer docs.muxy.io CNAME
    ```

12. Create the cutover record in the release/change ticket using this exact template. Fill every field and attach or link the gate and preview-smoke logs before DNS changes:

    ```text
    docs.muxy.io cutover record
    deployed_sha: <40-character git SHA>
    cutover_gate_run: <GitHub Actions run URL>
    cutover_gate_result: success
    pages_deployment_run: <GitHub Actions run URL>
    preview_smoke: <artifact or log URL>
    old_cname: ssl.readmessl.com
    new_cname: muxy.github.io
    ttl: 300
    dns_change_utc: pending
    production_smoke: pending
    certificate: pending
    rollback_owner: <name>
    readme_retention_end_utc: <cutover time plus 30 days>
    ```

Record the release SHA with `git rev-parse HEAD`; do not use a shortened SHA.

## Cutover

1. Confirm the change window is open, the rollback owner is present, the ReadMe freeze is still in effect, and the pre-cutover record is complete.
2. Configure the Pages custom domain as `docs.muxy.io` and verify repository/domain ownership.
3. Set the repository variable `DOCS_PRODUCTION=true`, then deploy the recorded SHA. Do not continue if the deployed SHA differs from `deployed_sha` in the cutover record.
4. At the authoritative DNS provider, replace only this record and keep TTL `300`:

   ```text
   docs.muxy.io. 300 IN CNAME muxy.github.io.
   ```

5. Record `dns_change_utc` immediately. Verify the authoritative answer and two independent public resolvers:

   ```sh
   dig +noall +answer docs.muxy.io CNAME
   dig @1.1.1.1 +noall +answer docs.muxy.io CNAME
   dig @8.8.8.8 +noall +answer docs.muxy.io CNAME
   ```

6. Wait for GitHub Pages to issue the certificate, then enable enforced HTTPS. Verify the complete HTTP redirect/final response and certificate name and validity:

   ```sh
   curl --fail --show-error --silent --location \
     --dump-header - --output /dev/null http://docs.muxy.io/
   curl --fail --show-error --silent --location \
     --dump-header - --output /dev/null https://docs.muxy.io/
   openssl s_client -connect docs.muxy.io:443 -servername docs.muxy.io </dev/null 2>/dev/null \
     | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
   ```

   The HTTP request must finish at `https://docs.muxy.io/` with a successful response. The certificate must be currently valid, trusted by `curl`, and list `docs.muxy.io` in its subject alternative names.

7. Run and retain the full production smoke against the recorded deployment:

   ```sh
   python scripts/smoke_production.py \
     --base-url https://docs.muxy.io \
     --indexing-mode production
   ```

   The smoke must pass status/body and content-type checks, structured JSON/YAML/XML parsing, redirects and canonicals, missing-route behavior, archive exclusion, production indexing, every vendored asset, and HTTPS certificate validation.

8. Manually verify search, an API endpoint, a Gateway guide, an archived page, dark mode, code copy, and mobile navigation.
9. Update `production_smoke` and `certificate` in the cutover record with the retained logs. Record the final Pages deployment URL and verify it still identifies `deployed_sha`.

## Propagation acceptance criteria

Cutover is complete only when all of these criteria are true:

- The authoritative resolver, `1.1.1.1`, and `8.8.8.8` return only `muxy.github.io` with TTL no greater than `300`; none returns `ssl.readmessl.com`.
- The DNS criterion passes twice, at least 300 seconds apart, so one full target TTL has elapsed without an old answer.
- HTTP redirects to HTTPS, HTTPS is trusted and currently valid for `docs.muxy.io`, and the final response is successful.
- The production smoke passes in `production` indexing mode from a network outside the DNS provider's control plane.
- The deployed SHA, successful cutover-gate run, Pages deployment, DNS evidence, TLS output, and production-smoke log are attached to the cutover record.

Any failed criterion keeps the cutover open and starts the rollback decision timer.

## Rollback

Rollback immediately if any critical canonical or Markdown route, vendored asset, OpenAPI document, agent index, search flow, indexing policy, redirect, or TLS check fails, or if propagation remains split beyond the approved window.

1. At the authoritative DNS provider, restore exactly:

   ```text
   docs.muxy.io. 300 IN CNAME ssl.readmessl.com.
   ```

2. Record the rollback UTC time and reason in the cutover record.
3. Set `DOCS_PRODUCTION=false` so the Pages project preview returns to `noindex, nofollow`; keep the failed Pages deployment and logs available for investigation.
4. Check authoritative and public DNS until all three answers return `ssl.readmessl.com` twice at least 300 seconds apart:

   ```sh
   dig +noall +answer docs.muxy.io CNAME
   dig @1.1.1.1 +noall +answer docs.muxy.io CNAME
   dig @8.8.8.8 +noall +answer docs.muxy.io CNAME
   ```

5. Verify ReadMe HTTP and HTTPS behavior with `curl` and `openssl`, then re-run representative legacy HTML and `.md` requests.
6. Fix the issue through a new reviewed commit and a new successful cutover-gate record; never amend the failed deployment's evidence.

## 30-day retention and decommission evidence

Keep the ReadMe project unchanged, accessible to the rollback owner, and recoverable for at least 30 full days after `dns_change_utc`. Keep the CNAME TTL at `300` during this period and run the scheduled production smoke daily.

The decommission approval must include all of the following evidence in the cutover record:

- The exact 30-day start and end timestamps in UTC.
- A ReadMe owner/export identifier and a timestamped screenshot or export proving the legacy project remains recoverable.
- Links to 30 consecutive daily production-smoke runs, with every failure linked to its resolution and subsequent passing run.
- The original cutover-gate run, deployed 40-character SHA, Pages deployment, DNS propagation captures, and TLS capture.
- A day-30 route-parity smoke and manual review covering HTML, Markdown, search, sitemap, `llms.txt`, `llms-full.txt`, OpenAPI, archived pages, and vendored assets.
- Written approval from Developer Experience and the rollback owner to decommission ReadMe.

Do not delete, downgrade, or otherwise make the ReadMe project unrecoverable until the 30-day timestamp has elapsed and every evidence item is present.
