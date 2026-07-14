#!/usr/bin/env python3
"""Snapshot ReadMe, vendor assets, recover OpenAPI, and create the route manifest.

This is an explicit migration command. CI builds from its committed output and
never reaches back to ReadMe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

import yaml
from PIL import Image

from docs_common import (
    DOCS,
    OPENAPI,
    ROOT,
    classify_page_type,
    json_fence_language,
    normalize_json_fences,
    read_frontmatter,
    render_frontmatter,
)
from migrate_readme_export import BLOCK_RE, convert_block


HOST = "https://docs.muxy.io"
SNAPSHOT = ROOT / "migration" / "readme"
MANIFEST = ROOT / "migration" / "manifest.yaml"
ASSET_DIR = DOCS / "assets" / "readme"
LLMS_LINK_RE = re.compile(r"^- \[([^]]+)]\((https://docs\.muxy\.io/(docs|reference|changelog)/([^)]+)\.md)\)(?::\s*(.*))?$")
IMAGE_RE = re.compile(r"!\[([^]]*)]\((https://files\.readme\.io/[^)\s]+)(?:\s+\"([^\"]+)\")?\)")
ASSET_URL_RE = re.compile(r"https://files\.readme\.io/[^\"')\s]+")
OPENAPI_RE = re.compile(r"(?:^|\n)# OpenAPI definition\s*\n+```json\s*\n(.*?)\n```", re.DOTALL)
LINK_RE = re.compile(r"(\[[^]]+])\(([^)]+)\)")

ARCHIVED_SLUGS = {
    "basic-usage-examples",
    "create-a-muxy-login-flow",
    "game-codes",
    "implement-gamelink-polling",
    "initialization-api",
    "initialize-the-extension",
    "install-the-muxy-plugin-for-unreal-engine",
    "manage-polling",
    "pin-auth",
    "transactions",
    "trivia",
    "trivia-1",
    "user-info",
    "workflow-examples",
}

# These pages have been deliberately restructured after the ReadMe snapshot.
# Preserve the reviewed working copy when refreshing the upstream export.
CURATED_SLUGS = {
    "accumulation",
    "broadcast",
    "dev-auth",
    "event-handling",
    "extension-setup-api",
    "gamelink-library",
    "install-manually",
    "quick-start",
    "ranking",
    "sdk-class",
    "state-config-fns",
    "state-information",
    "store-configuration-data",
    "try-sandbox-auth",
    "unity-fps-demo-code-walkthrough",
    "unity-gamelink-tutorial",
    "unity-gateway-tutorial",
    "websocket-protocol",
    "ws-authentication",
    "ws-polling",
    "ws-pubsub",
    "ws-purchase-transactions",
    "ws-state-access",
}

PRODUCT_RULES = (
    (("unity-gateway",), "Gateway", "Gateway SDK owner", "muxy/gateway-unity", "v1.0.0-rc"),
    (("unity-",), "Unity", "Unity SDK owner", "muxy/gamelink-unity", "unverified"),
    (("websocket", "ws-"), "GameLink WebSocket", "GameLink owner", "muxy/gamelink-cpp", "unverified"),
    (("gamelink-library", "sdk-class", "extension-setup-api", "state-config-fns", "event-handling"), "GameLink Native", "Native SDK owner", "muxy/gamelink-cpp", "unverified"),
    (("unreal", "create-a-muxy-login-flow", "workflow-examples", "initialize-the-extension", "manage-polling", "basic-usage-examples", "implement-gamelink-polling"), "Unreal", "Unreal SDK owner", "muxy/github-pages:migration/readme", "unverified"),
)


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "muxy-docs-migration/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def text(url: str) -> str:
    return fetch(url).decode("utf-8").replace("\r\n", "\n")


def existing_documents() -> dict[str, tuple[Path, dict, str]]:
    found = {}
    for path in DOCS.rglob("*.md"):
        metadata, body = read_frontmatter(path)
        slug = metadata.get("slug")
        if slug:
            found[str(slug)] = (path, metadata, body)
    return found


def historical_documents() -> dict[str, tuple[Path, dict, str]]:
    """Read the untouched export from HEAD, even after a local refresh."""
    found = existing_documents()
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "docs"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for filename in result.stdout.splitlines():
        if not filename.endswith(".md"):
            continue
        payload = subprocess.run(
            ["git", "show", f"HEAD:{filename}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        temporary = ROOT / filename
        match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", payload, re.DOTALL)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1)) or {}
        slug = metadata.get("slug")
        if slug:
            found[str(slug)] = (temporary, metadata, payload[match.end() :])
    return found


def parse_llms(content: str) -> list[dict]:
    documents = []
    for line in content.splitlines():
        match = LLMS_LINK_RE.match(line)
        if not match:
            continue
        title, legacy_md, section, encoded_slug, description = match.groups()
        slug = unquote(encoded_slug)
        documents.append(
            {
                "title": title,
                "description": (description or f"Muxy {title} documentation.").strip(),
                "section": section,
                "slug": slug,
                "legacy_url": legacy_md[:-3],
                "legacy_markdown_url": legacy_md,
                "status": "current",
            }
        )
    return documents


def classify(slug: str, section: str) -> tuple[str, str, str, str]:
    for needles, product, owner, repo, version in PRODUCT_RULES:
        if any(needle in slug for needle in needles):
            return product, owner, repo, version
    if section == "reference":
        return "REST API", "API Platform", "muxy/github-pages:openapi/rest-v1.yaml", "v1"
    if section == "changelog":
        return "GameLink", "Developer Experience", "muxy/gamelink-cpp", "unverified"
    return "MEDKit", "Developer Experience", "muxy/extensions-js", "2.4.18"


def clean_body(body: str, title: str) -> str:
    replacements = {
        "ðŸ“˜": "Note",
        "ðŸ‘�": "Tip",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "Â": "",
        "ConvertTextureToImage": "ConvertTextureToBase64",
        "OnActionUsed": "OnGameActionUsed",
        "SetActions": "SetGameActions",
        "ActionCategory": "GameActionCategory",
        "ActionState": "GameActionState",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    lines = body.strip().splitlines()
    in_fence = False
    h1_seen = False
    fixed = []
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("# "):
            if not h1_seen:
                line = f"# {title}"
                h1_seen = True
            else:
                line = "#" + line
        fixed.append(line.rstrip())
    if not h1_seen:
        fixed.insert(0, f"# {title}")
        fixed.insert(1, "")
    return normalize_json_fences("\n".join(fixed).strip() + "\n")


def copy_asset(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    filename = Path(parsed.path).name
    destination = ASSET_DIR / filename
    payload = fetch(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    return f"/assets/readme/{filename}", hashlib.sha256(payload).hexdigest()


def extract_openapi(raw: str) -> dict | None:
    match = OPENAPI_RE.search(raw)
    if not match:
        return None
    return json.loads(match.group(1))


def merge_openapi(fragments: list[dict], title: str) -> dict:
    merged = {
        "openapi": "3.1.0",
        "info": {
            "title": title,
            "version": "1.0.0",
            "description": "Version-controlled source of truth recovered from the Muxy ReadMe API reference.",
        },
        "servers": [],
        "paths": {},
        "components": {},
    }
    seen_servers = set()
    for fragment in fragments:
        for server in fragment.get("servers", []):
            marker = json.dumps(server, sort_keys=True)
            if marker not in seen_servers:
                merged["servers"].append(server)
                seen_servers.add(marker)
        # ReadMe stores one method per page. Several pages share the same path,
        # so replacing the whole path item silently discarded sibling methods.
        for route, path_item in fragment.get("paths", {}).items():
            target = merged["paths"].setdefault(route, {})
            for method, operation in path_item.items():
                if method in target and target[method] != operation:
                    raise ValueError(f"conflicting OpenAPI operation: {method.upper()} {route}")
                target[method] = operation
        for key, value in fragment.get("components", {}).items():
            merged["components"].setdefault(key, {}).update(value)
        if fragment.get("security"):
            merged["security"] = fragment["security"]
    return normalize_openapi(merged)


def normalize_openapi(spec: dict) -> dict:
    """Repair known ReadMe export artifacts without changing API semantics."""
    secured = spec.get("info", {}).get("title") != "Muxy Sandbox API"
    spec.setdefault("components", {})["securitySchemes"] = {
        "MuxyAuthorization": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "`<Twitch Extension Client ID> <Muxy JWT>`",
        }
    }
    spec["security"] = [{"MuxyAuthorization": []}] if secured else []

    object_body_examples = {
        "/accumulate": {"next_game": "Day of the Tentacle"},
        "/config/channel": {"broadcaster_birthday": "2000-01-01"},
        "/channel_state": {"favorite_color": "blue"},
        "/config/extension": {"release_date": "2021-10-31"},
        "/extension_state": {"favorite_color": "blue"},
        "/extension_viewer_state": {"favorite_color": "blue"},
        "/viewer_state": {"favorite_color": "blue"},
    }
    response_examples = {
        ("get", "/accumulate", "200"): {
            "data": [{
                "observed": 1634401498121,
                "channel_id": "12345",
                "opaque_user_id": "U12345",
                "user_id": "",
                "data": {"next_game": "Day of the Tentacle"},
            }],
            "latest": 1634401498121,
        },
        ("get", "/config/channel", "200"): {"broadcaster_birthday": "2000-01-01"},
        ("get", "/channel_state", "200"): {"favorite_color": "blue"},
        ("get", "/config/extension", "200"): {"release_date": "2021-10-31"},
        ("get", "/config", "200"): {"channel": {}, "extension": {}},
        ("get", "/extension_state", "200"): {"favorite_color": "blue"},
        ("get", "/extension_viewer_state", "200"): {"favorite_color": "blue"},
        ("get", "/viewer_state", "200"): {"favorite_color": "blue"},
        ("get", "/all_state", "200"): {"extension": {}, "channel": {}, "viewer": {}, "extension_viewer": {}},
        ("post", "/rank", "200"): {"accepted": True, "original": "Serious Sam"},
    }
    write_routes = {
        "/accumulate",
        "/config/channel",
        "/channel_state",
        "/config/extension",
        "/extension_state",
        "/extension_viewer_state",
        "/viewer_state",
    }

    for route, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                continue
            if legacy_operation_id := operation.get("operationId"):
                operation["x-doc-slug"] = legacy_operation_id
                normalized_route = route.strip("/").replace("/", "-").replace("_", "-") or "root"
                operation["operationId"] = f"{method.lower()}-{normalized_route}"
            if operation.get("security") != [] and secured:
                operation["security"] = [{"MuxyAuthorization": []}]
            for media in operation.get("requestBody", {}).get("content", {}).values():
                schema = media.get("schema", {})
                if "RAW_BODY" in schema.get("properties", {}):
                    if method.lower() == "patch":
                        media["schema"] = {
                            "type": "array",
                            "description": "RFC 6902 JSON Patch operations.",
                            "items": {"$ref": "#/components/schemas/JsonPatchOperation"},
                        }
                        media["example"] = [{"op": "replace", "path": "/favorite_color", "value": "blue"}]
                    else:
                        media["schema"] = {
                            "type": "object",
                            "description": "Complete JSON value to store or submit.",
                            "additionalProperties": True,
                        }
                        media["example"] = object_body_examples.get(route, {})
            if operation.get("requestBody"):
                operation["requestBody"]["required"] = method.lower() != "post" or route != "/rank"
            for status, response in operation.get("responses", {}).items():
                key = (method.lower(), route, str(status))
                if key in response_examples:
                    media = response.get("content", {}).get("application/json")
                    if media is not None:
                        media.pop("examples", None)
                        media["example"] = response_examples[key]
                else:
                    for media in response.get("content", {}).values():
                        if isinstance(media.get("example"), str):
                            try:
                                media["example"] = json.loads(re.sub(r"\s*//.*", "", media["example"]))
                            except json.JSONDecodeError:
                                pass

            if route == "/all_state" and method.lower() == "get":
                media = operation["responses"]["200"]["content"]["application/json"]
                media["schema"] = {
                    "type": "object",
                    "required": ["extension", "channel", "viewer", "extension_viewer"],
                    "properties": {
                        name: {"type": "object", "additionalProperties": True}
                        for name in ("extension", "channel", "viewer", "extension_viewer")
                    },
                }

            if route in write_routes and method.lower() in {"post", "patch"}:
                operation["responses"]["200"] = {
                    "description": "Write accepted. The current service returns an empty JSON object.",
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "maxProperties": 0},
                            "example": {},
                        }
                    },
                }

            restricted_roles = {
                ("post", "/config/channel"): "Requires an admin or broadcaster JWT.",
                ("patch", "/config/channel"): "Requires an admin or broadcaster JWT.",
                ("post", "/channel_state"): "Requires an admin, backend, or broadcaster JWT.",
                ("patch", "/channel_state"): "Requires an admin, backend, or broadcaster JWT.",
                ("post", "/config/extension"): "Requires an admin JWT; backend JWTs are rejected.",
                ("patch", "/config/extension"): "Requires an admin JWT; backend JWTs are rejected.",
                ("post", "/extension_state"): "Requires a validated admin or backend JWT.",
                ("patch", "/extension_state"): "Requires a validated admin or backend JWT.",
                ("get", "/accumulate"): "Requires an admin, backend, or broadcaster JWT.",
            }
            role_note = restricted_roles.get((method.lower(), route))
            if role_note:
                operation["description"] = (operation.get("description") or operation.get("summary") or "") + f"\n\n{role_note}"
                operation.setdefault("responses", {})["403"] = {
                    "description": "The JWT role is not allowed to perform this operation.",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                            "example": {"reason": "role is not authorized"},
                        }
                    },
                }

            if route == "/config/extension" and method.lower() == "post":
                for sample in operation.get("x-readme", {}).get("code-samples", []):
                    sample["code"] = sample.get("code", "").replace("setChannelConfig", "setExtensionConfig")
            for sample in operation.get("x-readme", {}).get("code-samples", []):
                code = sample.get("code", "")
                if route == "/config/extension" and method.lower() in {"post", "patch"}:
                    code = code.replace("<admin or backend JWT>", "<admin JWT>")
                if route == "/config/channel" and method.lower() in {"post", "patch"}:
                    code = code.replace("<broadcaster JWT>", "<admin or broadcaster JWT>")
                if route == "/channel_state" and method.lower() in {"post", "patch"}:
                    code = code.replace("<broadcaster JWT>", "<admin, backend, or broadcaster JWT>")
                sample["code"] = code

    spec["components"].setdefault("schemas", {})["JsonPatchOperation"] = {
        "type": "object",
        "required": ["op", "path"],
        "properties": {
            "op": {"type": "string", "enum": ["add", "remove", "replace", "move", "copy", "test"]},
            "path": {"type": "string", "description": "JSON Pointer to the target value."},
            "from": {"type": "string", "description": "Source JSON Pointer for move or copy."},
            "value": {"description": "Value used by add, replace, or test."},
        },
    }
    spec["components"]["schemas"]["ErrorResponse"] = {
        "type": "object",
        "properties": {"reason": {"type": "string"}},
    }
    for route, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                continue
            for status, response in operation.get("responses", {}).items():
                if str(status).startswith(("4", "5")):
                    response["content"] = {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                            "example": {"reason": response.get("description", "Request failed")},
                        }
                    }
            if method.lower() == "patch":
                media = operation.get("requestBody", {}).get("content", {}).get("application/json")
                if media and media.get("schema", {}).get("type") == "array":
                    media["schema"] = {
                        "oneOf": [
                            {
                                "type": "array",
                                "description": "RFC 6902 JSON Patch operations.",
                                "items": {"$ref": "#/components/schemas/JsonPatchOperation"},
                            },
                            {
                                "type": "object",
                                "description": "JSON Merge Patch object.",
                                "additionalProperties": True,
                            },
                        ]
                    }
                    if route == "/extension_viewer_state":
                        operation["requestBody"]["description"] = (
                            "Admin JWTs may also send an object mapping up to 1,000 Twitch user IDs to patch values."
                        )
    if secured:
        spec["components"]["schemas"]["BroadcastMessage"] = {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "PubSub target; use broadcast for a channel-wide message."},
                "event": {"type": "string", "default": "default"},
                "user_id": {"type": "string", "description": "Target Twitch channel ID for channel broadcasts."},
                "data": {"type": "object", "additionalProperties": True},
            },
            "required": ["data"],
        }
        spec["components"]["schemas"].update(
            {
                "VoteResponse": {
                    "type": "object",
                    "required": ["stddev", "mean", "sum", "specific", "count", "decay"],
                    "properties": {
                        "stddev": {"type": "number", "description": "Sample standard deviation across effective stored votes."},
                        "mean": {"type": "number", "description": "Mean of all effective stored vote values."},
                        "sum": {"type": "number", "description": "Sum of all effective stored vote values."},
                        "specific": {
                            "type": "array",
                            "description": "Exactly 32 counters. Indexes 0 through 31 count votes whose value equals that index; values outside this range still contribute to the other statistics.",
                            "minItems": 32,
                            "maxItems": 32,
                            "items": {"type": "integer", "minimum": 0},
                        },
                        "count": {
                            "type": "integer",
                            "minimum": 0,
                            "description": "Number of effective stored vote entries after per-user replacement and modifiers; this is not the number of requests.",
                        },
                        "decay": {"type": "object", "additionalProperties": True},
                        "vote": {
                            "type": "integer",
                            "minimum": -128,
                            "maximum": 128,
                            "description": "The caller's known vote, omitted when no vote is known.",
                        },
                    },
                },
                "VoteConfiguration": {
                    "type": "object",
                    "properties": {
                        "userIDVoting": {"type": "boolean"},
                        "distinctOptionsPerUser": {"type": "integer", "minimum": 1, "maximum": 258, "default": 1},
                        "totalVotesPerUser": {"type": "integer", "minimum": 1, "maximum": 1024, "default": 1},
                        "votesPerOption": {"type": "integer", "minimum": 1, "maximum": 1024, "default": 1},
                        "global": {"type": "boolean"},
                        "disabled": {"type": "boolean"},
                        "prompt": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "string"}},
                        "userData": {},
                        "endsAt": {"type": "integer", "description": "Unix timestamp in seconds."},
                        "startsAt": {"type": "integer", "description": "Unix timestamp in seconds."},
                        "status": {"type": "string", "enum": ["pending", "active", "expired"], "readOnly": True},
                    },
                },
            }
        )

        id_parameter = {
            "name": "id",
            "in": "query",
            "required": False,
            "description": "Poll identifier. Defaults to `default`; global polls use an ID beginning with `global`.",
            "schema": {"type": "string", "default": "default", "maxLength": 64},
        }
        empty_success = {
            "description": "Operation accepted. The current service returns an empty JSON object.",
            "content": {"application/json": {"schema": {"type": "object", "maxProperties": 0}, "example": {}}},
        }
        role_error = {
            "description": "The JWT role is not allowed to perform this operation.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                    "example": {"reason": "role is not authorized"},
                }
            },
        }
        bad_request = {
            "description": "The request body or poll configuration is invalid.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                    "example": {"reason": "Invalid body"},
                }
            },
        }
        internal_error = {
            "description": "The service could not complete the operation because an internal or storage dependency failed.",
            "content": {
                "application/json": {
                    "schema": {"type": "object", "additionalProperties": True},
                    "example": {"reason": ""},
                }
            },
        }
        specific_example = [0, 2] + [0] * 30
        extension_viewer_get = spec["paths"].get("/extension_viewer_state", {}).get("get")
        if extension_viewer_get:
            extension_viewer_get.update(
                {
                    "summary": "Get extension viewer state",
                    "description": "Returns extension-wide state for the current viewer. A backend JWT may use `userID` to select one Twitch user. A validated admin JWT may instead pass up to 1,000 comma-separated Twitch IDs in `user_ids`; the response is then keyed by each ID whose state exists.",
                    "x-doc-description": "Read one viewer's extension-wide state or batch-read state for up to 1,000 Twitch user IDs.",
                    "parameters": [
                        {
                            "name": "userID",
                            "in": "query",
                            "required": False,
                            "description": "Twitch user ID to read when using a backend JWT. Ignored for other roles and superseded when `user_ids` is present.",
                            "schema": {"type": "string"},
                        },
                        {
                            "name": "user_ids",
                            "in": "query",
                            "required": False,
                            "description": "Comma-separated Twitch user IDs for an admin-only batch read. At most 1,000 IDs are accepted; missing state entries are omitted from the result.",
                            "schema": {"type": "string"},
                        },
                    ],
                }
            )
            extension_viewer_get["responses"]["200"] = {
                "description": "The selected viewer state, or an object keyed by Twitch user ID for a `user_ids` batch request.",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "additionalProperties": True,
                            "description": "Developer-defined state. Batch responses map each found Twitch user ID to its state object.",
                        },
                        "examples": {
                            "Current viewer": {"value": {"favorite_color": "blue"}},
                            "Admin batch": {"value": {"12345": {"favorite_color": "blue"}, "67890": {"favorite_color": "green"}}},
                        },
                    }
                },
            }
            extension_viewer_get["responses"]["400"] = {
                "description": "State lookup failed, or more than 1,000 IDs were supplied.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {"reason": "Too many ids specified"},
                    }
                },
            }
            extension_viewer_get["responses"]["403"] = role_error
        spec["paths"].update(
            {
                "/vote": {
                    "get": {
                        "summary": "Get vote totals",
                        "description": "Returns aggregate statistics and, when available, the current viewer's known vote.",
                        "operationId": "vote-get",
                        "parameters": [id_parameter],
                        "responses": {
                            "200": {
                                "description": "Current vote statistics.",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/VoteResponse"},
                                        "example": {"stddev": 0, "mean": 1, "sum": 2, "specific": specific_example, "count": 2, "decay": {}, "vote": 1},
                                    }
                                },
                            }
                        },
                    },
                    "post": {
                        "summary": "Submit votes",
                        "description": "Submits a value from -128 through 128. If `value` is omitted the handler submits `0`. Missing or explicit `count: 0` becomes `1`; positive counts are capped at 30 per request and must also fit the poll's configured per-user limit.",
                        "operationId": "vote-submit",
                        "parameters": [id_parameter],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "value": {"type": "integer", "minimum": -128, "maximum": 128, "default": 0},
                                            "count": {
                                                "type": "integer",
                                                "minimum": 0,
                                                "maximum": 30,
                                                "default": 1,
                                                "description": "Number of copies to submit. The service treats 0 as 1.",
                                            },
                                        },
                                    },
                                    "example": {"value": 1, "count": 1},
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Vote accepted and current statistics returned.",
                                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VoteResponse"}}},
                            },
                            "400": bad_request,
                        },
                    },
                    "delete": {
                        "summary": "Delete a poll",
                        "description": "Deletes a poll. Requires an admin, backend, or broadcaster JWT.",
                        "operationId": "vote-delete",
                        "parameters": [id_parameter],
                        "responses": {"200": empty_success, "403": role_error},
                    },
                },
                "/vote_logs": {
                    "get": {
                        "summary": "Get vote logs",
                        "description": "Returns individual vote records. Requires a valid admin JWT.",
                        "operationId": "vote-logs",
                        "parameters": [id_parameter],
                        "responses": {
                            "200": {
                                "description": "Vote log records.",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["result"],
                                            "properties": {
                                                "result": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "identifier": {"type": "string"},
                                                            "opaque": {"type": "string"},
                                                            "value": {"type": "integer"},
                                                            "timestamp": {"type": "integer"},
                                                        },
                                                    },
                                                }
                                            },
                                        },
                                        "example": {"result": []},
                                    }
                                },
                            },
                            "403": role_error,
                            "500": internal_error,
                        },
                    }
                },
                "/vote_modifier": {
                    "post": {
                        "summary": "Add a vote modifier",
                        "description": "Adds a signed adjustment for one user. Requires an admin, backend, or broadcaster JWT.",
                        "operationId": "vote-modifier",
                        "parameters": [id_parameter],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["user", "add"],
                                        "properties": {"user": {"type": "string"}, "add": {"type": "integer"}},
                                    },
                                    "example": {"user": "U12345", "add": 2},
                                }
                            },
                        },
                        "responses": {"200": empty_success, "400": bad_request, "403": role_error},
                    }
                },
                "/vote_config": {
                    "get": {
                        "summary": "Get poll configuration",
                        "description": "Returns the stored configuration and computed poll status.",
                        "operationId": "vote-config-get",
                        "parameters": [id_parameter],
                        "responses": {
                            "200": {
                                "description": "Poll configuration.",
                                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VoteConfiguration"}}},
                            },
                            "404": {
                                "description": "No configuration exists for this poll.",
                                "content": {"application/json": {"schema": {"type": "object"}, "example": {}}},
                            },
                        },
                    },
                    "post": {
                        "summary": "Create or update poll configuration",
                        "description": "Creates or replaces poll configuration. Requires an admin, backend, or broadcaster JWT.",
                        "operationId": "vote-config-post",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["id", "config"],
                                        "properties": {
                                            "id": {"type": "string", "maxLength": 64},
                                            "config": {"$ref": "#/components/schemas/VoteConfiguration"},
                                        },
                                    },
                                    "example": {
                                        "id": "next-game",
                                        "config": {"prompt": "Choose the next game", "options": ["A", "B"], "startsAt": 1760000000, "endsAt": 1760003600},
                                    },
                                }
                            },
                        },
                        "responses": {"200": empty_success, "400": bad_request, "403": role_error, "500": internal_error},
                    },
                },
                "/json_store": {
                    "get": {
                        "summary": "Get a JSON store",
                        "description": "Returns a named channel-scoped JSON document. The `default` store is used when `id` is omitted; IDs beginning with `global` use extension-wide storage. A cache miss can return `202` while a registered external data source is being refreshed.",
                        "operationId": "get-json-store",
                        "x-doc-title": "Get a JSON Store",
                        "x-doc-description": "Read a named channel-scoped or extension-wide JSON store.",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "query",
                                "required": False,
                                "description": "Store identifier. Defaults to `default`; IDs beginning with `global` use extension-wide storage.",
                                "schema": {"type": "string", "default": "default"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "The stored JSON document.",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object", "additionalProperties": True},
                                        "example": {"favorite_color": "blue"},
                                    }
                                },
                            },
                            "202": {
                                "description": "The document is not cached and a registered source is being refreshed, or another request already holds the refresh lock.",
                                "content": {"application/json": {"schema": {"type": "object", "maxProperties": 0}, "example": {}}},
                            },
                            "404": {
                                "description": "No cached document or registered source exists for this store identifier.",
                                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}, "example": {"reason": "Not Found"}}},
                            },
                            "500": internal_error,
                            "502": {
                                "description": "The registered external source returned a response that was not a JSON object.",
                                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}, "example": {"reason": "external server returned a bad response"}}},
                            },
                        },
                    }
                },
                "/user_ids": {
                    "get": {
                        "summary": "List shared Twitch user IDs",
                        "description": "Returns Twitch user IDs that users have shared with the extension. Requires a backend JWT or a validated admin JWT for the extension owner or a listed extension administrator. Continue scanning until `next` is `0`.",
                        "operationId": "get-user-ids",
                        "x-doc-title": "List Shared Twitch User IDs",
                        "x-doc-description": "Page through Twitch user IDs shared with an extension.",
                        "parameters": [
                            {
                                "name": "cursor",
                                "in": "query",
                                "required": False,
                                "description": "Redis scan cursor returned as `next` by the previous call. Start with `0` and stop when the response returns `0`.",
                                "schema": {"type": "string", "default": "0"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "One scan page of shared Twitch user IDs.",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["next", "results"],
                                            "properties": {
                                                "next": {"type": "string", "description": "Cursor for the next scan page; `0` means the scan is complete."},
                                                "results": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "required": ["twitch_id"],
                                                        "properties": {"twitch_id": {"type": "string"}},
                                                    },
                                                },
                                            },
                                        },
                                        "example": {"next": "0", "results": [{"twitch_id": "27419011"}]},
                                    }
                                },
                            },
                            "403": role_error,
                            "500": internal_error,
                        },
                    }
                },
                "/gamelink/token": {
                    "post": {
                        "summary": "Create a GameLink authorization code",
                        "description": "Creates a six-character authorization code for the current JWT. The code expires after five minutes and can be exchanged by a GameLink client during PIN authentication.",
                        "operationId": "post-gamelink-token",
                        "x-doc-title": "Create a GameLink Authorization Code",
                        "x-doc-description": "Create a short-lived GameLink PIN for the current extension authorization.",
                        "responses": {
                            "200": {
                                "description": "A short-lived GameLink authorization code.",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["token"],
                                            "properties": {
                                                "token": {
                                                    "type": "string",
                                                    "minLength": 6,
                                                    "maxLength": 6,
                                                    "pattern": "^[A-HJ-KM-NP-Z2-46-9]{6}$",
                                                    "description": "Six-character code using an ambiguity-reduced uppercase alphabet; expires after five minutes.",
                                                }
                                            },
                                        },
                                        "example": {"token": "ABC234"},
                                    }
                                },
                            },
                            "400": {
                                "description": "The serialized authorization header exceeds 1,024 characters.",
                                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}, "example": {"reason": "Bad request"}}},
                            },
                        },
                    }
                },
            }
        )
        broadcast_operations = {
            "/broadcast": ("broadcast-channel", "Send a channel broadcast", "Requires a broadcaster, admin, or backend JWT."),
            "/extension_broadcast": ("broadcast-extension", "Send an extension-wide broadcast", "Requires a privileged broadcaster, admin, or backend JWT."),
            "/whisper_self": ("whisper-self", "Send a message to the current viewer", "Uses the viewer represented by the JWT."),
        }
        for route, (operation_id, summary, description) in broadcast_operations.items():
            example = {"event": "score-updated", "data": {"score": 42}}
            if route == "/broadcast":
                example.update({"target": "broadcast", "user_id": "12345678"})
            spec["paths"].setdefault(route, {})["post"] = {
                "summary": summary,
                "description": description,
                "operationId": operation_id,
                "security": [{"MuxyAuthorization": []}],
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BroadcastMessage"}, "example": example}},
                },
                "responses": {
                    "200": {"description": "Message accepted for delivery.", "content": {"application/json": {"schema": {"type": "object"}, "example": {}}}},
                    "400": bad_request,
                    "403": role_error,
                },
            }
    if not secured and "/authtoken" in spec.get("paths", {}):
        operation = spec["paths"]["/authtoken"]["post"]
        operation["security"] = []
        operation["requestBody"]["required"] = True
        media = operation["requestBody"]["content"]["application/json"]
        media["schema"].pop("required", None)
        media["schema"].pop("oneOf", None)
        media["schema"]["anyOf"] = [{"required": ["extension_id"]}, {"required": ["app_id"]}]
        media["schema"]["properties"]["app_id"] = {
            "type": "string",
            "description": "Registered Muxy app ID. The server resolves its owning extension when available.",
        }
        media["schema"]["properties"]["role"]["description"] = (
            "Role string copied into the testing JWT. The endpoint does not validate an enum. "
            "Use `viewer`, `broadcaster`, `admin`, or `backend` only when the target handler supports it."
        )
        media["schema"]["properties"]["user_id"]["description"] = (
            "Optional Twitch user ID. For broadcaster tokens the server replaces this value with `channel_id`."
        )
        media["schema"]["properties"]["user_ids"]["description"] = (
            "Optional additional Twitch user IDs. May be supplied with `user_id`; one JWT is returned per ID."
        )
        media["examples"] = {
            "Viewer token": {
                "value": {
                    "extension_id": "your-extension-client-id",
                    "channel_id": "12345678",
                    "user_id": "87654321",
                    "role": "viewer",
                }
            },
            "Anonymous token": {
                "value": {
                    "extension_id": "your-extension-client-id",
                    "channel_id": "12345678",
                    "role": "viewer",
                }
            },
        }
        operation["description"] = (
            (operation.get("description") or operation.get("summary") or "Create sandbox JWTs.")
            + "\n\n`user_id` and `user_ids` are both optional and may be combined. With neither, the server creates one anonymous token. "
            "A token whose role string is `admin` is not guaranteed to satisfy handlers that require a validated admin JWT."
        )
        operation["responses"]["200"]["content"]["application/json"] = {
            "schema": {
                "oneOf": [
                    {"type": "object", "required": ["token"], "properties": {"token": {"type": "string"}}},
                    {"type": "object", "required": ["tokens"], "properties": {"tokens": {"type": "array", "items": {"type": "string"}}}},
                ]
            },
            "examples": {
                "Single user": {"value": {"token": "<sandbox JWT>"}},
                "Multiple users": {"value": {"tokens": ["<sandbox JWT>", "<sandbox JWT>"]}},
            },
        }
        operation["responses"]["400"]["content"] = {
            "application/json": {
                "schema": {"type": "object", "required": ["reason"], "properties": {"reason": {"type": "string"}}},
                "examples": {"Unknown extension": {"value": {"reason": "No such extension found"}}},
            }
        }
        operation["x-readme"] = {
            "code-samples": [
                {
                    "language": "curl",
                    "code": "curl --request POST \\\n  --url https://sandbox.api.muxy.io/v1/e/authtoken \\\n  --header 'content-type: application/json' \\\n  --data '{\"extension_id\":\"your-extension-client-id\",\"channel_id\":\"12345678\",\"user_id\":\"87654321\",\"role\":\"viewer\"}'",
                }
            ]
        }
    return spec


def snapshot_openapi() -> tuple[list[dict], list[dict]]:
    rest: list[dict] = []
    sandbox: list[dict] = []
    for path in sorted(SNAPSHOT.rglob("*.md")):
        fragment = extract_openapi(path.read_text(encoding="utf-8"))
        if not fragment:
            continue
        title = fragment.get("info", {}).get("title", "")
        (sandbox if "Sandbox" in title else rest).append(fragment)
    return rest, sandbox


def write_openapi_specs(rest_fragments: list[dict], sandbox_fragments: list[dict]) -> None:
    specs = {
        OPENAPI / "rest-v1.yaml": merge_openapi(rest_fragments, "Muxy REST API"),
        OPENAPI / "sandbox-v1.yaml": merge_openapi(sandbox_fragments, "Muxy Sandbox API"),
    }
    OPENAPI.mkdir(parents=True, exist_ok=True)
    for path, spec in specs.items():
        path.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), encoding="utf-8")


def fenced(value: object, language: str = "json") -> str:
    if isinstance(value, str):
        content = value
    else:
        content = json.dumps(value, indent=2, ensure_ascii=False)
    if language.lower() == "json":
        language = json_fence_language(content)
    return f"```{language}\n{content.rstrip()}\n```"


def resolve_schema(schema: object, fragment: dict, seen: frozenset[str] = frozenset()) -> object:
    """Resolve local schema references so generated pages are useful on their own."""
    if isinstance(schema, list):
        return [resolve_schema(value, fragment, seen) for value in schema]
    if not isinstance(schema, dict):
        return schema
    reference = schema.get("$ref")
    if isinstance(reference, str) and reference.startswith("#/") and reference not in seen:
        target: object = fragment
        for part in reference[2:].split("/"):
            if not isinstance(target, dict) or part not in target:
                break
            target = target[part]
        else:
            resolved = resolve_schema(target, fragment, seen | {reference})
            if isinstance(resolved, dict):
                return {**resolved, **{key: resolve_schema(value, fragment, seen) for key, value in schema.items() if key != "$ref"}}
            return resolved
    return {key: resolve_schema(value, fragment, seen) for key, value in schema.items()}


def render_schema(schema: dict, fragment: dict) -> str:
    if not schema:
        return "No schema is specified."
    return fenced(resolve_schema(schema, fragment))


def parameter_type(schema: dict) -> str:
    value = schema.get("type", "object")
    if value == "array":
        value = f"array<{schema.get('items', {}).get('type', 'object')}>"
    return str(value)


def parameter_constraints(schema: dict) -> str:
    constraints = []
    if "default" in schema:
        constraints.append(f"default `{json.dumps(schema['default'], ensure_ascii=False)}`")
    if "enum" in schema:
        constraints.append("one of " + ", ".join(f"`{value}`" for value in schema["enum"]))
    minimum = schema.get("minimum", schema.get("exclusiveMinimum"))
    maximum = schema.get("maximum", schema.get("exclusiveMaximum"))
    if minimum is not None and maximum is not None:
        constraints.append(f"{minimum} to {maximum}")
    elif minimum is not None:
        constraints.append(f"minimum {minimum}")
    elif maximum is not None:
        constraints.append(f"maximum {maximum}")
    min_length = schema.get("minLength")
    max_length = schema.get("maxLength")
    if min_length is not None and max_length is not None and min_length == max_length:
        constraints.append(f"exactly {min_length} characters")
    else:
        if min_length is not None:
            constraints.append(f"at least {min_length} characters")
        if max_length is not None:
            constraints.append(f"at most {max_length} characters")
    if "pattern" in schema:
        constraints.append(f"pattern `{schema['pattern']}`")
    return "; ".join(constraints) or "none"


def render_openapi_operation(fragment: dict, title: str) -> str:
    lines = [f"# {title}", ""]
    for route, path_item in fragment.get("paths", {}).items():
        common_parameters = path_item.get("parameters", [])
        for method, operation in path_item.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                continue
            security = operation.get("security", fragment.get("security"))
            authorization = (
                "No authorization header is required for this sandbox operation."
                if security == []
                else "Send `Authorization: <Twitch Extension Client ID> <Muxy JWT>`. The JWT role must satisfy the endpoint requirements shown in the examples."
            )
            lines.extend(
                [
                    f"## `{method.upper()} {route}`",
                    "",
                    operation.get("description") or operation.get("summary") or "Muxy REST API operation.",
                    "",
                    "### Authorization",
                    "",
                    authorization,
                    "",
                ]
            )
            parameters = common_parameters + operation.get("parameters", [])
            if parameters:
                lines.extend(
                    [
                        "### Parameters",
                        "",
                        "| Name | In | Required | Type | Constraints | Description |",
                        "| --- | --- | --- | --- | --- | --- |",
                    ]
                )
                for parameter in parameters:
                    schema = parameter.get("schema", {})
                    lines.append(
                        f"| `{parameter.get('name', '')}` | {parameter.get('in', '')} | "
                        f"{'yes' if parameter.get('required') else 'no'} | `{parameter_type(schema)}` | "
                        f"{parameter_constraints(schema).replace('|', '\\|')} | "
                        f"{str(parameter.get('description', '')).replace('|', '\\|')} |"
                    )
                lines.append("")
            request = operation.get("requestBody", {})
            if request:
                lines.extend(["### Request body", ""])
                if request.get("description"):
                    lines.extend([request["description"], ""])
                for content_type, media in request.get("content", {}).items():
                    lines.extend([f"Content type: `{content_type}`", "", "#### Schema", "", render_schema(media.get("schema", {}), fragment), ""])
                    examples = media.get("examples") or ({"Example": {"value": media["example"]}} if "example" in media else {})
                    for name, example in examples.items():
                        lines.extend([f"#### {name}", "", fenced(example.get("value", example)), ""])
            lines.extend(["### Responses", ""])
            for status, response in operation.get("responses", {}).items():
                label = "Error" if str(status).startswith(("4", "5")) else "Response"
                lines.extend([f"#### {status} {label}", "", response.get("description", "Response from the API."), ""])
                for content_type, media in response.get("content", {}).items():
                    lines.extend([f"Content type: `{content_type}`", ""])
                    if media.get("schema"):
                        lines.extend(["##### Schema", "", render_schema(media["schema"], fragment), ""])
                    examples = media.get("examples") or ({"Example": {"value": media["example"]}} if "example" in media else {})
                    for name, example in examples.items():
                        lines.extend([f"##### {name}", "", fenced(example.get("value", example)), ""])
            samples = operation.get("x-readme", {}).get("code-samples", [])
            if samples:
                lines.extend(["### Examples", ""])
                for sample in samples:
                    lines.extend([f"#### {sample.get('language', 'Example').title()}", "", fenced(sample.get("code", ""), sample.get("language", "text")), ""])
    return "\n".join(lines).strip() + "\n"


def dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def relative_target(current: dict, target: dict, anchor: str = "") -> str:
    source = PurePosixPath(current["target_file"]).parent
    destination = PurePosixPath(target["target_file"])
    up = [".."] * len(source.relative_to("docs").parts)
    rel = PurePosixPath(*(up + list(destination.relative_to("docs").parts))).as_posix()
    return rel + (f"#{anchor}" if anchor else "")


def rewrite_links(body: str, current: dict, documents: list[dict]) -> str:
    by_slug = {item["slug"]: item for item in documents}
    aliases = {
        "sarbitrary-state": "arbitrary-state",
        "troubleshooting": "troubleshooting-tips",
        "docs;state-information": "state-information",
        "ws-communication": "ws-pubsub",
    }

    def replace(match: re.Match[str]) -> str:
        label, raw = match.groups()
        if raw.startswith(("mailto:", "#")):
            return match.group(0)
        value, marker, anchor = raw.partition("#")
        parsed = urlparse(value)
        slug = ""
        if parsed.netloc == "docs.muxy.io":
            slug = Path(parsed.path).stem
        elif value.startswith(("doc:", "ref:")):
            slug = value.split(":", 1)[1]
        elif value.endswith(".md"):
            slug = Path(unquote(value)).stem
        elif value in aliases:
            slug = value
        slug = aliases.get(slug, slug)
        target = by_slug.get(slug)
        if target:
            return f"{label}({relative_target(current, target, anchor if marker else '')})"
        return match.group(0)

    return LINK_RE.sub(replace, body)


def frontmatter_for(document: dict) -> dict:
    review = "blocked-release" if document["product"] == "Unity" else "needs-sme-review"
    metadata = {
        "title": document["title"],
        "description": document["description"],
        "slug": document["slug"],
        "product": document["product"],
        "audience": "developers",
        "status": document["status"],
        "owner": document["owner"],
        "source_of_truth": document["source_of_truth"],
        "version": document["version"],
        "last_verified": str(date.today()),
        "review_state": review,
        "page_type": document["page_type"],
    }
    if document["status"] == "archived":
        metadata["robots"] = "noindex, nofollow"
        metadata["search"] = {"exclude": True}
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--refresh", action="store_true", help="Replace an existing snapshot")
    parser.add_argument(
        "--rebuild-openapi",
        action="store_true",
        help="Rebuild OpenAPI deterministically from the committed ReadMe snapshot",
    )
    args = parser.parse_args()

    if args.rebuild_openapi:
        rest_fragments, sandbox_fragments = snapshot_openapi()
        write_openapi_specs(rest_fragments, sandbox_fragments)
        print(f"Rebuilt OpenAPI from {len(rest_fragments) + len(sandbox_fragments)} fragments")
        return 0

    current = existing_documents()
    old = historical_documents()
    home_metadata, home_body = read_frontmatter(DOCS / "index.md")
    curated = {slug: current[slug] for slug in CURATED_SLUGS if slug in current}
    preserved_archives = {}
    if SNAPSHOT.exists():
        for slug in ARCHIVED_SLUGS:
            for section in ("docs", "reference"):
                candidate = SNAPSHOT / section / f"{slug}.md"
                if candidate.exists():
                    preserved_archives[slug] = candidate.read_text(encoding="utf-8")
                    break
    if SNAPSHOT.exists() and not args.refresh:
        print("Snapshot already exists; use --refresh to replace it", file=sys.stderr)
        return 2

    if SNAPSHOT.exists():
        shutil.rmtree(SNAPSHOT)
    SNAPSHOT.mkdir(parents=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    OPENAPI.mkdir(parents=True, exist_ok=True)

    llms = text(f"{args.host}/llms.txt")
    (SNAPSHOT / "llms.txt").write_text(llms, encoding="utf-8")
    documents = parse_llms(llms)
    public_slugs = {item["slug"] for item in documents}

    for slug in sorted(ARCHIVED_SLUGS):
        path, metadata, _ = old[slug]
        section = "reference" if "REST API" in path.as_posix() else "docs"
        documents.append(
            {
                "title": str(metadata["title"]),
                "description": f"Archived Muxy documentation for {metadata['title']}.",
                "section": section,
                "slug": slug,
                "legacy_url": f"{args.host}/{section}/{slug}",
                "legacy_markdown_url": f"{args.host}/{section}/{slug}.md",
                "status": "archived",
            }
        )

    for document in documents:
        product, owner, repo, version = classify(document["slug"], document["section"])
        target_file = f"docs/{document['section']}/{document['slug']}.md"
        existing_page_type = current.get(document["slug"], (None, {}, None))[1].get("page_type")
        document.update(
            {
                "canonical_slug": document["slug"],
                "target_file": target_file,
                "product": product,
                "owner": owner,
                "source_of_truth": repo,
                "version": version,
                "redirects": [],
                "review_state": "blocked-release" if product == "Unity" else "needs-sme-review",
                "page_type": existing_page_type or classify_page_type(ROOT / target_file, {**document, "product": product}),
            }
        )

    imported_slugs = {item["slug"] for item in documents}
    derived = {
        slug: (path, metadata, body)
        for slug, (path, metadata, body) in current.items()
        if slug not in imported_slugs and slug != "index"
    }

    raw_by_slug: dict[str, str] = {}
    asset_hashes: dict[str, str] = {}
    rest_fragments: list[dict] = []
    sandbox_fragments: list[dict] = []
    for document in documents:
        slug = document["slug"]
        snapshot_path = SNAPSHOT / document["section"] / f"{slug}.md"
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        if slug in public_slugs:
            raw = text(document["legacy_markdown_url"])
        elif slug in preserved_archives:
            raw = preserved_archives[slug]
        else:
            _, metadata, body = old[slug]
            raw = render_frontmatter(metadata, body)
        snapshot_path.write_text(raw, encoding="utf-8")
        raw_by_slug[slug] = raw
        fragment = extract_openapi(raw)
        if fragment and document["status"] == "current":
            title = fragment.get("info", {}).get("title", "")
            (sandbox_fragments if "Sandbox" in title else rest_fragments).append(fragment)

    for raw in raw_by_slug.values():
        for url in ASSET_URL_RE.findall(raw):
            if url not in asset_hashes:
                _, digest = copy_asset(url)
                asset_hashes[url] = digest

    logo_url = "https://files.readme.io/86e839b-muxy-character.svg"
    if logo_url not in asset_hashes:
        _, digest = copy_asset(logo_url)
        asset_hashes[logo_url] = digest

    write_openapi_specs(rest_fragments, sandbox_fragments)

    for child in list(DOCS.iterdir()):
        if child.name in {"assets", "index.md"}:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    by_slug = {item["slug"]: item for item in documents}
    for document in documents:
        slug = document["slug"]
        raw = raw_by_slug[slug]
        _, snapshot_body = read_frontmatter(SNAPSHOT / document["section"] / f"{slug}.md")
        body = BLOCK_RE.sub(convert_block, snapshot_body)
        fragment = extract_openapi(raw)
        if fragment:
            body = render_openapi_operation(fragment, document["title"])
            body += "\n!!! info \"Generated API reference\"\n    This endpoint is generated from the version-controlled OpenAPI specification.\n"
        body = clean_body(body, document["title"])

        def replace_image(match: re.Match[str]) -> str:
            alt, url, title = match.groups()
            filename = Path(urlparse(url).path).name
            alt = alt or title or filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ")
            size = dimensions(ASSET_DIR / filename)
            attrs = f'{{ width="{size[0]}" height="{size[1]}" loading="lazy" }}' if size else '{ loading="lazy" }'
            return f"![{alt}](../assets/readme/{filename}){attrs}"

        body = IMAGE_RE.sub(replace_image, body)
        body = rewrite_links(body, document, documents)
        if document["status"] == "archived":
            warning = (
                "!!! warning \"Archived documentation\"\n"
                "    This page is retained for URL compatibility. It is not maintained, indexed, or included in agent exports.\n\n"
            )
            first_break = body.find("\n", body.find("# ")) + 1
            body = body[:first_break] + "\n" + warning + body[first_break:]
        destination = ROOT / document["target_file"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_frontmatter(frontmatter_for(document), body), encoding="utf-8")

    for _, (path, metadata, body) in derived.items():
        metadata.setdefault("page_type", classify_page_type(path, metadata))
        destination = path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_frontmatter(metadata, body), encoding="utf-8")

    for slug, (_, metadata, body) in curated.items():
        document = by_slug[slug]
        destination = ROOT / document["target_file"]
        metadata.setdefault("page_type", classify_page_type(destination, metadata))
        for field in ("product", "status", "owner", "source_of_truth", "version", "review_state", "page_type"):
            document[field] = metadata[field]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_frontmatter(metadata, body), encoding="utf-8")

    home_metadata.setdefault("page_type", classify_page_type(DOCS / "index.md", home_metadata))
    (DOCS / "index.md").write_text(render_frontmatter(home_metadata, home_body), encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "generated_from": args.host,
        "generated_on": str(date.today()),
        "counts": {"homepage": 1, "current": len(public_slugs), "archived": len(ARCHIVED_SLUGS), "total": 1 + len(documents)},
        "homepage": {
            "title": home_metadata["title"],
            "description": home_metadata["description"],
            "section": "home",
            "slug": home_metadata["slug"],
            "legacy_url": f"{args.host}/",
            "legacy_markdown_url": f"{args.host}/index.md",
            "status": home_metadata["status"],
            "canonical_slug": home_metadata["slug"],
            "target_file": "docs/index.md",
            "product": home_metadata["product"],
            "owner": home_metadata["owner"],
            "source_of_truth": home_metadata["source_of_truth"],
            "version": home_metadata["version"],
            "redirects": [],
            "review_state": home_metadata["review_state"],
            "page_type": home_metadata["page_type"],
        },
        "documents": sorted(documents, key=lambda item: (item["section"], item["slug"])),
        "assets": [
            {"legacy_url": url, "target_file": f"docs/assets/readme/{Path(urlparse(url).path).name}", "sha256": digest}
            for url, digest in sorted(asset_hashes.items())
        ],
        "derived_documents": [
            {
                "title": metadata["title"],
                "description": metadata["description"],
                "section": path.relative_to(DOCS).parts[0],
                "slug": slug,
                "legacy_url": None,
                "legacy_markdown_url": None,
                "canonical_slug": slug,
                "target_file": path.relative_to(ROOT).as_posix(),
                "product": metadata["product"],
                "status": metadata["status"],
                "owner": metadata["owner"],
                "source_of_truth": metadata["source_of_truth"],
                "version": metadata["version"],
                "legacy_parent": (
                    f"{args.host}/docs/unity-gateway-tutorial"
                    if slug.startswith("unity-gateway-")
                    else None
                ),
                "redirects": [],
                "review_state": metadata["review_state"],
                "page_type": metadata["page_type"],
            }
            for slug, (path, metadata, _) in sorted(derived.items())
        ],
        "site_counts": {
            "current": sum(1 for path in DOCS.rglob("*.md") if read_frontmatter(path)[0].get("status") == "current"),
            "archived": sum(1 for path in DOCS.rglob("*.md") if read_frontmatter(path)[0].get("status") == "archived"),
            "total": sum(1 for _ in DOCS.rglob("*.md")),
        },
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Imported {len(documents)} documents and {len(asset_hashes)} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
