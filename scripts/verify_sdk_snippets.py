#!/usr/bin/env python3
"""Verify SDK example usage against byte-pinned public source artifacts.

This is a provenance and declaration check. It does not compile the JavaScript
or C# examples.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

from docs_common import DOCS, ROOT, read_frontmatter


DEFAULT_MANIFEST = ROOT / "migration" / "snippet-sources.yaml"
DEFAULT_SOURCES = ROOT / "migration" / "sdk-sources.yaml"
FENCE_RE = re.compile(r"^```[^\n]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)
MEDKIT_METHOD_RE = re.compile(r"\bmedkit\.([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
MUXY_MEMBER_RE = re.compile(r"\bMuxy\.([A-Za-z_$][A-Za-z0-9_$]*)")
GATEWAY_PATTERNS = (
    re.compile(r"\b(?:gateway(?:\.Client)?|Client)\??\.([A-Za-z_]\w*)\s*\("),
    re.compile(r"\bSDK\.([A-Za-z_]\w*)\s*\("),
    re.compile(
        r"\bnew\s+(SDK|GameAction|GameMetadata|GameText|"
        r"MuxyGatewayGameActionUsedEvent|PollConfiguration)\b"
    ),
)
GATEWAY_DELEGATE_RE = re.compile(r"\bSDK\.(On[A-Za-z_]\w*Delegate)\b")
GATEWAY_DOTTED_PATTERNS = (
    re.compile(r"\b(GameActionCategory|GameActionState|PollMode)\.([A-Za-z_]\w*)"),
    re.compile(r"\b(GameAction)\.(InfiniteCount)\b"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, accept: str = "application/octet-stream") -> bytes:
    request = Request(
        url,
        headers={"Accept": accept, "User-Agent": "muxy-docs-snippet-check/1.0"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def code_fences(body: str) -> list[str]:
    return [match.group(1) for match in FENCE_RE.finditer(body)]


def documentation_files(config: dict) -> list[tuple[Path, str]]:
    selected: dict[Path, str] = {}
    for glob in config["globs"]:
        for path in ROOT.glob(glob):
            if not path.is_file():
                continue
            metadata, body = read_frontmatter(path)
            if (
                metadata.get("product") == config["product"]
                and metadata.get("status") == config["status"]
            ):
                selected[path] = body
    return sorted(selected.items())


def verify_required_literals(config: dict, errors: list[str]) -> None:
    for name, literal in config.get("required_literals", {}).items():
        path = ROOT / name
        if not path.is_file():
            errors.append(f"{name}: required provenance document is missing")
        elif literal not in path.read_text(encoding="utf-8"):
            errors.append(f"{name}: required pinned artifact reference is missing: {literal}")


def compare_symbols(
    label: str, actual: set[str], expected_values: list[str], errors: list[str]
) -> None:
    expected = set(expected_values)
    for symbol in sorted(expected - actual):
        errors.append(f"{label}: documented SDK usage disappeared: {symbol}")
    for symbol in sorted(actual - expected):
        errors.append(f"{label}: unpinned documented SDK usage appeared: {symbol}")


def verify_medkit_docs(config: dict, errors: list[str]) -> None:
    methods: set[str] = set()
    members: set[str] = set()
    documents = documentation_files(config)
    if not documents:
        errors.append("MEDKit: no current documentation matched the configured globs")
        return
    for _, body in documents:
        for snippet in code_fences(body):
            methods.update(MEDKIT_METHOD_RE.findall(snippet))
            members.update(MUXY_MEMBER_RE.findall(snippet))
    compare_symbols("MEDKit methods", methods, config["expected_sdk_methods"], errors)
    compare_symbols("MEDKit Muxy members", members, config["expected_muxy_members"], errors)
    verify_required_literals(config, errors)


def verify_gateway_docs(config: dict, errors: list[str]) -> None:
    symbols: set[str] = set()
    documents = documentation_files(config)
    if not documents:
        errors.append("Gateway: no current documentation matched the configured globs")
        return
    for _, body in documents:
        for snippet in code_fences(body):
            for pattern in GATEWAY_PATTERNS:
                symbols.update(pattern.findall(snippet))
            symbols.update(f"SDK.{name}" for name in GATEWAY_DELEGATE_RE.findall(snippet))
            for pattern in GATEWAY_DOTTED_PATTERNS:
                symbols.update(".".join(match) for match in pattern.findall(snippet))
    compare_symbols("Gateway symbols", symbols, config["expected_symbols"], errors)
    verify_required_literals(config, errors)


def verify_blocked_sources(
    manifest: dict, sdk_sources: dict, errors: list[str]
) -> list[str]:
    blocked = []
    for source_id, policy in manifest["blocked_sources"].items():
        source = sdk_sources.get(source_id)
        if source is None:
            errors.append(f"{source_id}: blocked source is missing from sdk-sources.yaml")
            continue
        expected_state = policy["expected_release_state"]
        if source.get("release_state") != expected_state:
            errors.append(
                f"{source_id}: expected release_state {expected_state}, "
                f"found {source.get('release_state')}"
            )
        products = set(source.get("products", []))
        matched = 0
        for path in sorted(DOCS.rglob("*.md")):
            metadata, _ = read_frontmatter(path)
            if metadata.get("status") != "current" or metadata.get("product") not in products:
                continue
            matched += 1
            required = policy["required_review_state"]
            if metadata.get("review_state") != required:
                errors.append(
                    f"{relative(path)}: unpublished {source_id} example must use "
                    f"review_state: {required}"
                )
        if products and not matched:
            errors.append(f"{source_id}: no current documents exercise blocked products")
        blocked.append(f"{source_id} ({', '.join(sorted(products))})")
    return blocked


def checked_tar_files(blob: bytes, expected: dict[str, str], errors: list[str]) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
            members = {member.name: member for member in archive.getmembers() if member.isfile()}
            for path, digest in expected.items():
                member = members.get(path)
                if member is None:
                    errors.append(f"npm tarball: pinned path is missing: {path}")
                    continue
                handle = archive.extractfile(member)
                if handle is None:
                    errors.append(f"npm tarball: could not read pinned path: {path}")
                    continue
                data = handle.read()
                files[path] = data
                actual = sha256(data)
                if actual != digest:
                    errors.append(f"npm tarball: {path} SHA-256 drifted: {actual}")
    except tarfile.TarError as exc:
        errors.append(f"npm tarball: invalid archive: {exc}")
    return files


def verify_source_symbols(
    label: str, symbols: list[str], source_text: str, errors: list[str]
) -> None:
    for symbol in symbols:
        parts = symbol.split(".")
        if any(re.search(rf"\b{re.escape(part)}\b", source_text) is None for part in parts):
            errors.append(f"{label}: pinned source does not contain declaration token {symbol}")


def verify_npm_artifact(config: dict, errors: list[str]) -> None:
    metadata = json.loads(fetch(config["registry_metadata_url"], "application/json"))
    if metadata.get("name") != config["package"]:
        errors.append(f"MEDKit registry metadata returned package {metadata.get('name')}")
    if str(metadata.get("version")) != str(config["version"]):
        errors.append(f"MEDKit registry metadata returned version {metadata.get('version')}")
    dist = metadata.get("dist", {})
    for key, manifest_key in (
        ("tarball", "tarball_url"),
        ("integrity", "npm_integrity"),
        ("shasum", "npm_shasum"),
    ):
        if dist.get(key) != config[manifest_key]:
            errors.append(f"MEDKit npm dist.{key} drifted: {dist.get(key)}")

    blob = fetch(config["tarball_url"])
    actual_sha256 = sha256(blob)
    if actual_sha256 != config["sha256"]:
        errors.append(f"MEDKit npm tarball SHA-256 drifted: {actual_sha256}")
    if hashlib.sha1(blob).hexdigest() != config["npm_shasum"]:
        errors.append("MEDKit npm tarball SHA-1 does not match the pinned npm shasum")
    algorithm, encoded = config["npm_integrity"].split("-", 1)
    if algorithm != "sha512":
        errors.append(f"MEDKit npm integrity algorithm is unsupported: {algorithm}")
    elif base64.b64encode(hashlib.sha512(blob).digest()).decode("ascii") != encoded:
        errors.append("MEDKit npm tarball SHA-512 does not match the pinned npm integrity")

    files = checked_tar_files(blob, config["files"], errors)
    package_data = files.get("package/package.json")
    if package_data:
        package = json.loads(package_data)
        if package.get("name") != config["package"] or str(package.get("version")) != str(
            config["version"]
        ):
            errors.append("MEDKit tarball package.json name/version does not match the pin")
    docs = config["documentation"]
    sdk_path = docs["sdk_declarations"]
    if sdk_path in files:
        verify_source_symbols(
            "MEDKit methods",
            docs["expected_sdk_methods"],
            files[sdk_path].decode("utf-8"),
            errors,
        )
    muxy_text = "\n".join(
        files[path].decode("utf-8") for path in docs["muxy_declarations"] if path in files
    )
    if muxy_text:
        verify_source_symbols(
            "MEDKit Muxy members", docs["expected_muxy_members"], muxy_text, errors
        )


def resolve_git_ref(repository: str, ref: str) -> str:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        ["git", "ls-remote", "--refs", repository, ref],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or f"git exited {result.returncode}"
        raise RuntimeError(detail)
    matches = [line.split() for line in result.stdout.splitlines() if line.strip()]
    if len(matches) != 1 or matches[0][1] != ref:
        raise RuntimeError(f"expected exactly one match for {ref}, found {len(matches)}")
    return matches[0][0]


def verify_gateway_artifact(config: dict, errors: list[str]) -> None:
    try:
        resolved = resolve_git_ref(config["repository"], config["ref"])
        if resolved != config["resolved_commit"]:
            errors.append(
                f"Gateway {config['ref']} drifted: expected {config['resolved_commit']}, found {resolved}"
            )
    except Exception as exc:
        errors.append(f"Gateway ref resolution failed: {exc}")

    files: dict[str, bytes] = {}
    for path, digest in config["files"].items():
        data = fetch(config["raw_base_url"] + path)
        files[path] = data
        actual = sha256(data)
        if actual != digest:
            errors.append(f"Gateway {path} SHA-256 drifted: {actual}")
    package_data = files.get("package.json")
    if package_data:
        package = json.loads(package_data)
        if str(package.get("version")) != str(config["package_version"]):
            errors.append(f"Gateway package.json version drifted: {package.get('version')}")
    docs = config["documentation"]
    source_text = "\n".join(
        files[path].decode("utf-8-sig") for path in docs["symbol_sources"] if path in files
    )
    if source_text:
        verify_source_symbols("Gateway symbols", docs["expected_symbols"], source_text, errors)


def validate_manifest(manifest: dict, sdk_sources: dict, errors: list[str]) -> None:
    if manifest.get("schema_version") != 1:
        errors.append(f"snippet manifest: unsupported schema_version {manifest.get('schema_version')}")
    scope = manifest.get("verification_scope", {})
    if scope.get("compiles_examples") is not False:
        errors.append("snippet manifest must explicitly set compiles_examples: false")
    artifacts = manifest.get("artifacts", {})
    expected_ids = {"medkit-2.4.18", "gateway-unity-v1.0.0-rc"}
    if set(artifacts) != expected_ids:
        errors.append(
            f"snippet manifest artifacts must be exactly {sorted(expected_ids)}, "
            f"found {sorted(artifacts)}"
        )
    for artifact_id, config in artifacts.items():
        if config.get("kind") not in {"npm-tarball", "github-tag"}:
            errors.append(f"{artifact_id}: unsupported artifact kind {config.get('kind')}")
        for path, digest in config.get("files", {}).items():
            if not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
                errors.append(f"{artifact_id}: {path} must have a lowercase SHA-256 hash")
        source = sdk_sources.get(config.get("source_id"))
        if source is None:
            errors.append(f"{artifact_id}: source_id is missing from sdk-sources.yaml")
            continue
        if artifact_id == "medkit-2.4.18" and str(source.get("documented_version")) != str(
            config.get("version")
        ):
            errors.append(f"{artifact_id}: version disagrees with sdk-sources.yaml")
        if artifact_id == "medkit-2.4.18" and not re.fullmatch(
            r"[0-9a-f]{64}", str(config.get("sha256"))
        ):
            errors.append(f"{artifact_id}: tarball must have a lowercase SHA-256 hash")
        if artifact_id == "gateway-unity-v1.0.0-rc":
            if source.get("ref") != config.get("ref", "").removeprefix("refs/tags/"):
                errors.append(f"{artifact_id}: ref disagrees with sdk-sources.yaml")
            commit = config.get("resolved_commit", "")
            if not re.fullmatch(r"[0-9a-f]{40}", str(commit)):
                errors.append(f"{artifact_id}: resolved_commit must be a lowercase Git SHA-1")
            if commit not in config.get("raw_base_url", ""):
                errors.append(f"{artifact_id}: raw_base_url must use resolved_commit")
            if config.get("provenance_state") != "tagged-source-not-confirmed-package-release":
                errors.append(f"{artifact_id}: tagged source must not claim a package release")

        docs = config.get("documentation", {})
        symbol_lists = [
            values
            for key, values in docs.items()
            if key.startswith("expected_") and isinstance(values, list)
        ]
        for values in symbol_lists:
            if len(values) != len(set(values)):
                errors.append(f"{artifact_id}: expected SDK symbols must not contain duplicates")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true", help="download and hash pinned sources")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    args = parser.parse_args()

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    sdk_sources = yaml.safe_load(args.sources.read_text(encoding="utf-8"))["sources"]
    errors: list[str] = []
    validate_manifest(manifest, sdk_sources, errors)

    artifacts = manifest.get("artifacts", {})
    medkit = artifacts.get("medkit-2.4.18")
    gateway = artifacts.get("gateway-unity-v1.0.0-rc")
    if medkit:
        verify_medkit_docs(medkit["documentation"], errors)
    if gateway:
        verify_gateway_docs(gateway["documentation"], errors)
    blocked = verify_blocked_sources(manifest, sdk_sources, errors)

    if args.online and medkit and gateway:
        try:
            verify_npm_artifact(medkit, errors)
        except Exception as exc:
            errors.append(f"MEDKit public artifact check failed: {exc}")
        try:
            verify_gateway_artifact(gateway, errors)
        except Exception as exc:
            errors.append(f"Gateway public artifact check failed: {exc}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    mode = "online source artifacts" if args.online else "local provenance manifest"
    print(f"Verified MEDKit and Gateway SDK example provenance against {mode}.")
    print("Verification is source/declaration-based; examples were not compiled.")
    print(f"Blocked unpublished sources remain enforced: {', '.join(blocked)}")
    if not args.online:
        print("Run with --online in CI to download and hash the pinned public artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
