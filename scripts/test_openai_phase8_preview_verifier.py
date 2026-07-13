#!/usr/bin/env python3
"""Regression tests for the Phase 8 GitHub transport and witness boundary."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
VERIFIER = REPO / "tests" / "openai_phase8" / "verify_preview_evidence.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("phase8_preview_verifier", VERIFIER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Phase 8 Preview verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Response:
    def __init__(self, payload: bytes, url: str) -> None:
        self.payload = payload
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def geturl(self) -> str:
        return self.url

    def read(self) -> bytes:
        return self.payload


class FakeOpener:
    def __init__(self, payload: bytes, final_url: str | None = None) -> None:
        self.payload = payload
        self.final_url = final_url
        self.calls = []

    def open(self, request, timeout):
        self.calls.append((request, timeout))
        return Response(self.payload, self.final_url or request.full_url)


def expect_rejected(verifier, callback, label: str) -> None:
    try:
        callback()
    except verifier.VerificationError:
        return
    raise AssertionError(f"{label} was accepted")


def transport_tests(verifier) -> int:
    rejected_urls = (
        ("https://evil.example/?github", False),
        ("https://api.github.com.evil.example/repos/o/r/releases/1", False),
        ("https://github.com/repos/o/r/releases/1", False),
        (
            "https://github.com/owner/repository/releases/download/v1/evidence.json",
            True,
        ),
        ("https://user@api.github.com/repos/o/r/releases/1", False),
        ("https://api.github.com:443/repos/o/r/releases/1", False),
        ("http://api.github.com/repos/o/r/releases/1", False),
    )
    for url, binary in rejected_urls:
        expect_rejected(
            verifier,
            lambda url=url, binary=binary: verifier.github_request(url, binary=binary),
            url,
        )

    api_url = "https://api.github.com/repos/owner/repository/releases/1"
    json_opener = FakeOpener(json.dumps({"ok": True}).encode("utf-8"))
    with patch.dict(os.environ, {"GH_TOKEN": "secret-token", "GITHUB_TOKEN": ""}):
        verifier.github_request(api_url, binary=False, opener=json_opener)
    api_request = json_opener.calls[-1][0]
    if api_request.get_header("Authorization") != "Bearer secret-token":
        raise AssertionError("GitHub API request did not receive the configured token")

    page_url = (
        "https://api.github.com/repos/owner/repository/releases/1/assets"
        "?per_page=100&page=1"
    )
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            page_url,
            binary=False,
            opener=FakeOpener(b"[]"),
            json_array=True,
        ),
        "unscoped GitHub API query",
    )
    page_result = verifier.github_request(
        page_url,
        binary=False,
        opener=FakeOpener(b"[]"),
        allow_query=True,
        json_array=True,
    )
    if page_result != []:
        raise AssertionError("GitHub array response was not accepted for pagination")
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            page_url,
            binary=False,
            opener=FakeOpener(b"{}"),
            allow_query=True,
            json_array=True,
        ),
        "object-shaped GitHub asset page",
    )
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            api_url,
            binary=False,
            opener=FakeOpener(b"[]"),
        ),
        "array-shaped GitHub object response",
    )
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            page_url,
            binary=False,
            opener=FakeOpener(
                b"[]",
                page_url.replace("page=1", "page=2"),
            ),
            allow_query=True,
            json_array=True,
        ),
        "redirected GitHub asset page",
    )
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            api_url,
            binary=True,
            opener=FakeOpener(b"[]"),
            json_array=True,
        ),
        "binary JSON-array request",
    )

    handler = verifier.SafeGitHubRedirectHandler(allow_asset_redirects=True)
    initial = urllib.request.Request(
        "https://api.github.com/repos/owner/repository/releases/assets/9",
        headers={"Authorization": "Bearer secret-token", "Cookie": "private"},
    )
    redirected = handler.redirect_request(
        initial,
        None,
        302,
        "Found",
        {},
        "https://release-assets.githubusercontent.com/github-production-release-asset/file?sig=1",
    )
    if redirected.get_header("Authorization") is not None or redirected.get_header(
        "Cookie"
    ) is not None:
        raise AssertionError("credential leaked across the GitHub asset redirect")
    expect_rejected(
        verifier,
        lambda: handler.redirect_request(
            initial,
            None,
            302,
            "Found",
            {},
            "https://evil.example/stolen",
        ),
        "cross-domain asset redirect",
    )
    expect_rejected(
        verifier,
        lambda: handler.redirect_request(
            initial,
            None,
            302,
            "Found",
            {},
            "https://release-assets.githubusercontent.com.evil.example/stolen",
        ),
        "lookalike asset redirect",
    )
    expect_rejected(
        verifier,
        lambda: verifier.SafeGitHubRedirectHandler(
            allow_asset_redirects=False
        ).redirect_request(
            initial,
            None,
            302,
            "Found",
            {},
            "https://release-assets.githubusercontent.com/file?sig=1",
        ),
        "JSON API redirect",
    )

    binary_opener = FakeOpener(
        b"asset",
        "https://release-assets.githubusercontent.com/github-production-release-asset/file?sig=1",
    )
    verifier.github_request(
        "https://api.github.com/repos/owner/repository/releases/assets/9",
        binary=True,
        opener=binary_opener,
    )
    expect_rejected(
        verifier,
        lambda: verifier.github_request(
            "https://api.github.com/repos/owner/repository/releases/assets/9",
            binary=True,
            opener=FakeOpener(b"asset", "https://evil.example/final"),
        ),
        "untrusted final response URL",
    )
    return len(rejected_urls) + 13


def witness_before_download_tests(verifier) -> int:
    repository = "owner/repository"
    release_id = 17
    run_id = 23
    workflow_id = 29
    asset_id = 31
    index_asset_id = 37
    source_commit = "b" * 40
    release_tag = "v1"
    browser_url = (
        "https://github.com/owner/repository/releases/download/v1/evidence.json"
    )
    evidence_digest = "sha256:" + "a" * 64
    index_digest = "sha256:" + "d" * 64

    def git_target(object_type: str, object_sha: str) -> dict:
        collection = "commits" if object_type == "commit" else "tags"
        return {
            "type": object_type,
            "sha": object_sha,
            "url": (
                f"https://api.github.com/repos/{repository}/git/"
                f"{collection}/{object_sha}"
            ),
        }

    def release_asset(
        live_id: int,
        name: str,
        live_digest: str,
        size: int,
    ) -> dict:
        return {
            "id": live_id,
            "name": name,
            "url": (
                f"https://api.github.com/repos/{repository}/releases/assets/"
                f"{live_id}"
            ),
            "browser_download_url": (
                f"https://github.com/{repository}/releases/download/{release_tag}/"
                f"{name}"
            ),
            "digest": live_digest,
            "size": size,
            "state": "uploaded",
        }

    def filler_assets(count: int, *, start: int = 1_000) -> list[dict]:
        return [
            release_asset(
                filler_id,
                f"filler-{filler_id}.json",
                "sha256:" + f"{filler_id:064x}"[-64:],
                1,
            )
            for filler_id in range(start, start + count)
        ]

    live_evidence = release_asset(
        asset_id, "evidence.json", evidence_digest, 100
    )
    live_index = release_asset(index_asset_id, "index.json", index_digest, 200)
    index = {
        "github_release": {
            "repository": repository,
            "release_id": release_id,
            "release_tag": release_tag,
        },
        "github_witness": {
            "workflow_run_id": run_id,
            "workflow_id": workflow_id,
            "workflow_path": ".github/workflows/openai-plugin-preview.yml",
            "workflow_event": "push",
            "run_head_sha": source_commit,
            "source_commit": source_commit,
            "actor": "owner",
        },
        "assets": [
            {
                "asset_id": asset_id,
                "name": "evidence.json",
                "browser_download_url": browser_url,
                "sha256": evidence_digest,
                "size": 100,
            }
        ],
    }
    request = {
        "workflow_path": ".github/workflows/openai-plugin-preview.yml",
        "workflow_id": workflow_id,
        "workflow_event": "push",
        "workflow_run_id": run_id,
        "run_head_sha": source_commit,
        "release_asset_ids": [asset_id],
        "release_asset_digests": {str(asset_id): evidence_digest},
        "release_asset_index_name": "index.json",
        "release_asset_index_digest": index_digest,
        "release_asset_index_size": 200,
        "expected_source_identity": {"source_commit": source_commit},
    }

    ref_url = (
        f"https://api.github.com/repos/{repository}/git/ref/tags/{release_tag}"
    )
    release_url = f"https://api.github.com/repos/{repository}/releases/{release_id}"
    run_url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}"

    def base_state() -> dict:
        return {
            "release": {
                "id": release_id,
                "tag_name": release_tag,
                "draft": False,
                "prerelease": True,
                "immutable": True,
                # A verifier must ignore this incomplete embedded list.
                "assets": [],
            },
            "ref": {
                "ref": f"refs/tags/{release_tag}",
                "object": git_target("commit", source_commit),
            },
            "tags": {},
            "commits": {
                source_commit: {
                    "sha": source_commit,
                    "url": (
                        f"https://api.github.com/repos/{repository}/git/commits/"
                        f"{source_commit}"
                    ),
                }
            },
            "pages": {1: [live_evidence, live_index], 2: []},
            "run": {
                "id": run_id,
                "workflow_id": workflow_id,
                "path": ".github/workflows/openai-plugin-preview.yml",
                "event": "push",
                "head_sha": source_commit,
                "actor": {"login": "owner"},
                "status": "completed",
                "conclusion": "success",
            },
        }

    def invoke(
        state: dict,
        *,
        index_value: dict | None = None,
        request_value: dict | None = None,
    ):
        calls = []

        def fake_request(
            url: str,
            *,
            binary: bool,
            opener=None,
            allow_query: bool = False,
            json_array: bool = False,
        ):
            calls.append((url, binary, allow_query, json_array))
            if binary:
                raise AssertionError(
                    "asset bytes were downloaded before witness validation"
                )
            if url == release_url:
                return state["release"]
            if url == ref_url:
                return state["ref"]
            tag_prefix = f"https://api.github.com/repos/{repository}/git/tags/"
            if url.startswith(tag_prefix):
                tag_sha = url.removeprefix(tag_prefix)
                if tag_sha not in state["tags"]:
                    raise AssertionError(f"unexpected annotated tag request: {url}")
                return state["tags"][tag_sha]
            commit_prefix = (
                f"https://api.github.com/repos/{repository}/git/commits/"
            )
            if url.startswith(commit_prefix):
                commit_sha = url.removeprefix(commit_prefix)
                if commit_sha not in state["commits"]:
                    raise AssertionError(f"unexpected Git commit request: {url}")
                return state["commits"][commit_sha]
            assets_prefix = (
                f"https://api.github.com/repos/{repository}/releases/{release_id}/"
                "assets?per_page=100&page="
            )
            if url.startswith(assets_prefix):
                if not allow_query or not json_array:
                    raise AssertionError("asset pagination flags were not explicit")
                page_number = int(url.removeprefix(assets_prefix))
                return state["pages"].get(page_number, [])
            if url == run_url:
                return state["run"]
            raise AssertionError(f"unexpected GitHub request: {url}")

        with patch.object(verifier, "github_request", fake_request):
            result = verifier.validate_live_github_witness(
                index if index_value is None else index_value,
                request if request_value is None else request_value,
            )
        return result, calls

    state = base_state()
    (verified, verified_index), calls = invoke(state)
    if (
        set(verified) != {asset_id}
        or verified_index.get("id") != index_asset_id
        or calls != [
            (release_url, False, False, False),
            (ref_url, False, False, False),
            (
                f"https://api.github.com/repos/{repository}/git/commits/"
                f"{source_commit}",
                False,
                False,
                False,
            ),
            (
                f"https://api.github.com/repos/{repository}/releases/{release_id}/"
                "assets?per_page=100&page=1",
                False,
                True,
                True,
            ),
            (
                f"https://api.github.com/repos/{repository}/releases/{release_id}/"
                "assets?per_page=100&page=2",
                False,
                True,
                True,
            ),
            (run_url, False, False, False),
        ]
    ):
        raise AssertionError("live witness validation did not precede asset download")

    guards = 1

    annotated_state = base_state()
    tag_sha = "c" * 40
    annotated_state["ref"]["object"] = git_target("tag", tag_sha)
    annotated_state["tags"][tag_sha] = {
        "sha": tag_sha,
        "url": f"https://api.github.com/repos/{repository}/git/tags/{tag_sha}",
        "object": git_target("commit", source_commit),
    }
    invoke(annotated_state)
    guards += 1

    paginated_state = base_state()
    paginated_state["pages"] = {
        1: filler_assets(100),
        2: [live_evidence, live_index],
        3: [],
    }
    (paginated_result, paginated_calls) = invoke(paginated_state)
    if (
        paginated_result[1].get("id") != index_asset_id
        or not any("page=2" in call[0] for call in paginated_calls)
        or not any("page=3" in call[0] for call in paginated_calls)
    ):
        raise AssertionError("second-page Release assets were not read to exhaustion")
    guards += 1

    tampered = json.loads(json.dumps(index))
    tampered["assets"][0]["sha256"] = "sha256:" + "c" * 64
    expect_rejected(
        verifier,
        lambda: invoke(base_state(), index_value=tampered),
        "tampered indexed asset digest",
    )
    guards += 1
    tampered_request = dict(request)
    tampered_request["release_asset_index_digest"] = "sha256:" + "e" * 64
    expect_rejected(
        verifier,
        lambda: invoke(base_state(), request_value=tampered_request),
        "tampered Release asset-index digest",
    )
    guards += 1

    for immutable_value, label in (
        (False, "mutable GitHub Release"),
        (1, "non-boolean immutable flag"),
    ):
        mutable_state = base_state()
        mutable_state["release"]["immutable"] = immutable_value
        expect_rejected(
            verifier,
            lambda state=mutable_state: invoke(state),
            label,
        )
        guards += 1
    missing_immutable = base_state()
    del missing_immutable["release"]["immutable"]
    expect_rejected(
        verifier,
        lambda: invoke(missing_immutable),
        "missing immutable flag",
    )
    guards += 1

    wrong_commit = "d" * 40
    wrong_tag_state = base_state()
    wrong_tag_state["ref"]["object"] = git_target("commit", wrong_commit)
    wrong_tag_state["commits"][wrong_commit] = {
        "sha": wrong_commit,
        "url": (
            f"https://api.github.com/repos/{repository}/git/commits/{wrong_commit}"
        ),
    }
    expect_rejected(
        verifier,
        lambda: invoke(wrong_tag_state),
        "Release tag resolving to another commit",
    )
    guards += 1

    wrong_ref_state = base_state()
    wrong_ref_state["ref"]["ref"] = "refs/tags/other"
    expect_rejected(
        verifier,
        lambda: invoke(wrong_ref_state),
        "Release tag reference-name mismatch",
    )
    guards += 1

    cycle_state = base_state()
    first_tag = "c" * 40
    second_tag = "d" * 40
    cycle_state["ref"]["object"] = git_target("tag", first_tag)
    cycle_state["tags"] = {
        first_tag: {
            "sha": first_tag,
            "url": f"https://api.github.com/repos/{repository}/git/tags/{first_tag}",
            "object": git_target("tag", second_tag),
        },
        second_tag: {
            "sha": second_tag,
            "url": f"https://api.github.com/repos/{repository}/git/tags/{second_tag}",
            "object": git_target("tag", first_tag),
        },
    }
    expect_rejected(
        verifier,
        lambda: invoke(cycle_state),
        "annotated tag cycle",
    )
    guards += 1

    depth_state = base_state()
    depth_tags = [f"{value:040x}" for value in (10, 11, 12)]
    depth_state["ref"]["object"] = git_target("tag", depth_tags[0])
    depth_state["tags"] = {
        depth_tags[0]: {
            "sha": depth_tags[0],
            "url": (
                f"https://api.github.com/repos/{repository}/git/tags/{depth_tags[0]}"
            ),
            "object": git_target("tag", depth_tags[1]),
        },
        depth_tags[1]: {
            "sha": depth_tags[1],
            "url": (
                f"https://api.github.com/repos/{repository}/git/tags/{depth_tags[1]}"
            ),
            "object": git_target("tag", depth_tags[2]),
        },
    }
    with patch.object(verifier, "MAX_TAG_DEREFERENCE_DEPTH", 2):
        expect_rejected(
            verifier,
            lambda: invoke(depth_state),
            "annotated tag depth overflow",
        )
    guards += 1

    unsupported_target_state = base_state()
    unsupported_target_state["ref"]["object"] = {
        "type": "blob",
        "sha": "e" * 40,
        "url": f"https://api.github.com/repos/{repository}/git/blobs/{'e' * 40}",
    }
    expect_rejected(
        verifier,
        lambda: invoke(unsupported_target_state),
        "unsupported tag target",
    )
    guards += 1

    first_page = [live_evidence, *filler_assets(99)]
    duplicate_id_state = base_state()
    duplicate_id_state["pages"] = {
        1: first_page,
        2: [
            release_asset(
                asset_id,
                "duplicate-id.json",
                "sha256:" + "f" * 64,
                1,
            ),
            live_index,
        ],
        3: [],
    }
    expect_rejected(
        verifier,
        lambda: invoke(duplicate_id_state),
        "duplicate Release asset ID across pages",
    )
    guards += 1

    duplicate_name_state = base_state()
    duplicate_name_state["pages"] = {
        1: first_page,
        2: [
            release_asset(
                50_000,
                "evidence.json",
                "sha256:" + "f" * 64,
                1,
            ),
            live_index,
        ],
        3: [],
    }
    expect_rejected(
        verifier,
        lambda: invoke(duplicate_name_state),
        "duplicate Release asset name across pages",
    )
    guards += 1

    oversized_state = base_state()
    oversized_state["pages"] = {1: filler_assets(101), 2: []}
    expect_rejected(
        verifier,
        lambda: invoke(oversized_state),
        "oversized Release asset page",
    )
    guards += 1

    malformed_root_state = base_state()
    malformed_root_state["pages"] = {1: {"assets": []}}
    expect_rejected(
        verifier,
        lambda: invoke(malformed_root_state),
        "malformed Release asset page root",
    )
    guards += 1

    malformed_item_state = base_state()
    malformed_item_state["pages"] = {1: ["not-an-asset"]}
    expect_rejected(
        verifier,
        lambda: invoke(malformed_item_state),
        "malformed Release asset page item",
    )
    guards += 1

    inconsistent_state = base_state()
    inconsistent_state["pages"] = {
        1: [live_evidence, live_index],
        2: filler_assets(1),
        3: [],
    }
    expect_rejected(
        verifier,
        lambda: invoke(inconsistent_state),
        "nonempty page after a short Release asset page",
    )
    guards += 1

    truncated_state = base_state()
    truncated_state["pages"] = {
        1: filler_assets(100, start=10_000),
        2: filler_assets(100, start=20_000),
    }
    with patch.object(verifier, "MAX_RELEASE_ASSET_PAGES", 2):
        expect_rejected(
            verifier,
            lambda: invoke(truncated_state),
            "Release asset pagination without exhaustion",
        )
    guards += 1
    return guards


def bundle_request_tests(verifier) -> int:
    with tempfile.TemporaryDirectory(prefix="phase8-bundle-request-") as temp:
        root = Path(temp).resolve()
        raw_path = root / "raw.json"
        envelope_path = root / "envelope.json"
        index_path = root / "index.json"
        identity_path = root / "identity.json"
        raw_path.write_text(
            json.dumps({"captured_at": "2026-07-13T10:00:00Z"}),
            encoding="utf-8",
        )
        envelope_path.write_text(
            json.dumps(
                {
                    "capture": {
                        "captured_at": "2026-07-13T10:00:00Z",
                        "raw_export_asset_id": 101,
                    }
                }
            ),
            encoding="utf-8",
        )
        raw_digest = verifier.digest(raw_path)
        index_path.write_text(
            json.dumps(
                {
                    "github_release": {
                        "repository": "owner/repository",
                        "release_id": 17,
                        "release_tag": "v1",
                    },
                    "github_witness": {
                        "workflow_run_id": 23,
                        "workflow_id": 29,
                        "workflow_path": ".github/workflows/openai-plugin-preview.yml",
                        "workflow_event": "push",
                        "run_head_sha": "b" * 40,
                        "source_commit": "b" * 40,
                        "actor": "owner",
                    },
                    "assets": [
                        {
                            "asset_id": 101,
                            "name": "raw.json",
                            "sha256": raw_digest,
                            "browser_download_url": "https://github.com/owner/repository/releases/download/v1/raw.json",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        identity = {
            "plugin_version": "0.7.0-preview.1",
            "source_commit": "b" * 40,
            "manifest_sha256": "sha256:" + "1" * 64,
            "registry_sha256": "sha256:" + "2" * 64,
            "skill_tree_sha256": "sha256:" + "3" * 64,
        }
        identity_path.write_text(
            json.dumps({"source_identity": identity}), encoding="utf-8"
        )
        normalized_identity = {
            **identity,
            "manifest_sha256": "sha256:" + "1" * 64,
            "registry_sha256": "sha256:" + "2" * 64,
            "skill_tree_sha256": "sha256:" + "3" * 64,
        }
        request = verifier.build_request_from_bundle(
            evidence_root=root,
            asset_index_path=str(index_path),
            envelope_path=str(envelope_path),
            expected_source_identity_path=identity_path,
        )
        if (
            request["schema_version"] != verifier.REQUEST_SCHEMA_VERSION
            or request["adapter_id"] != verifier.PREVIEW_ADAPTER_ID
            or request["release_asset_ids"] != [101]
            or request["release_asset_digests"] != {"101": raw_digest}
            or request["release_asset_index_name"] != "index.json"
            or request["release_asset_index_size"] != index_path.stat().st_size
            or request["workflow_id"] != 29
            or request["workflow_event"] != "push"
            or request["run_head_sha"] != "b" * 40
            or request["expected_source_identity"] != normalized_identity
        ):
            raise AssertionError("bundle mode omitted a required gate binding")
        expect_rejected(
            verifier,
            lambda: verifier.build_request_from_bundle(
                evidence_root=root,
                asset_index_path=str(index_path),
                envelope_path=str(VERIFIER),
                expected_source_identity_path=identity_path,
            ),
            "bundle path escape",
        )
    return 2


def verify_call_order_test(verifier) -> int:
    with tempfile.TemporaryDirectory(prefix="phase8-call-order-") as temp:
        root = Path(temp).resolve()
        envelope_path = root / "envelope.json"
        index_path = root / "index.json"
        raw_path = root / "raw.json"
        envelope_path.write_text("{}", encoding="utf-8")
        index_path.write_text(
            json.dumps(
                {
                    "source_identity": {"source_commit": "b" * 40},
                    "assets": [],
                }
            ),
            encoding="utf-8",
        )
        raw_path.write_text("{}", encoding="utf-8")
        request = {
            "schema_version": verifier.REQUEST_SCHEMA_VERSION,
            "adapter_id": verifier.PREVIEW_ADAPTER_ID,
            "evidence_root": str(root),
            "envelope_path": "envelope.json",
            "envelope_digest": verifier.digest(envelope_path),
            "release_asset_index_path": "index.json",
            "release_asset_index_digest": verifier.digest(index_path),
            "raw_export_path": "raw.json",
            "raw_export_digest": verifier.digest(raw_path),
            "synthetic_test_only": False,
            "expected_source_identity": {
                "plugin_version": "0.7.0-preview.1",
                "source_commit": "b" * 40,
                "manifest_sha256": "1" * 64,
                "registry_sha256": "2" * 64,
                "skill_tree_sha256": "3" * 64,
            },
        }
        ordering = {"live": False}

        def live_first(_index, _request):
            ordering["live"] = True
            return {}, {"url": "https://api.github.com/index"}

        def integrity_second(*_args, **_kwargs):
            if not ordering["live"]:
                raise AssertionError("integrity layer ran before the live API witness")
            raise verifier.VerificationError("ordering sentinel")

        with patch.object(verifier, "validate_code_bindings", lambda *_a, **_k: {}), patch.object(
            verifier, "validate_live_github_witness", live_first
        ), patch.object(
            verifier, "github_request", lambda *_a, **_k: index_path.read_bytes()
        ), patch.object(verifier, "validate_evidence_bundle", integrity_second):
            expect_rejected(
                verifier,
                lambda: verifier.verify(request, synthetic_self_test=False),
                "live-before-integrity ordering sentinel",
            )
        if not ordering["live"]:
            raise AssertionError("live API witness was never checked")
    return 1


def structured_result_tests(verifier) -> int:
    identity = {
        "plugin_version": "0.7.0-preview.1",
        "source_commit": "b" * 40,
        "manifest_sha256": "1" * 64,
        "registry_sha256": "2" * 64,
        "skill_tree_sha256": "3" * 64,
    }

    for synthetic in (True, False):
        with tempfile.TemporaryDirectory(prefix="phase8-result-contract-") as temp:
            root = Path(temp).resolve()
            captured_at = "2026-07-13T10:00:00Z"
            raw = root / "raw.json"
            envelope = root / "envelope.json"
            report = root / "report.json"
            index_path = root / "index.json"
            raw.write_text(
                json.dumps(
                    {
                        "captured_at": captured_at,
                        "synthetic_test_only": synthetic,
                    }
                ),
                encoding="utf-8",
            )
            envelope.write_text(
                json.dumps({"capture": {"captured_at": captured_at}}),
                encoding="utf-8",
            )
            report.write_text(json.dumps({"verdict": "accepted"}), encoding="utf-8")
            records = []
            for asset_id, path, kind in (
                (101, raw, "raw_export"),
                (102, envelope, "evidence_envelope"),
                (103, report, "verifier_report"),
            ):
                records.append(
                    {
                        "asset_id": asset_id,
                        "name": path.name,
                        "sha256": verifier.digest(path),
                        "size": path.stat().st_size,
                        "evidence_kind": kind,
                        "fixture_path": path.name,
                        "browser_download_url": (
                            "https://github.com/owner/repository/releases/download/v1/"
                            + path.name
                        ),
                    }
                )
            index_path.write_text(
                json.dumps(
                    {
                        "source_identity": identity,
                        "github_release": {
                            "repository": "owner/repository",
                            "release_id": 17,
                            "release_tag": "v1",
                        },
                        "assets": records,
                    }
                ),
                encoding="utf-8",
            )
            request = {
                "schema_version": verifier.REQUEST_SCHEMA_VERSION,
                "adapter_id": verifier.PREVIEW_ADAPTER_ID,
                "evidence_root": str(root),
                "envelope_path": envelope.name,
                "envelope_digest": verifier.digest(envelope),
                "release_asset_index_path": index_path.name,
                "release_asset_index_digest": verifier.digest(index_path),
                "release_asset_index_name": index_path.name,
                "release_asset_index_size": index_path.stat().st_size,
                "raw_export_path": raw.name,
                "raw_export_digest": verifier.digest(raw),
                "raw_export_reference": records[0]["browser_download_url"],
                "capture_timestamp_digest": verifier.time_digest(captured_at),
                "verifier_digest": "sha256:" + "9" * 64,
                "synthetic_test_only": synthetic,
                "expected_source_identity": identity,
            }

            def fake_integrity(_envelope, _index, fetch, **_kwargs):
                for record in records:
                    fetch(record)
                return SimpleNamespace(
                    evidence_id="preview-result-contract",
                    integrity_valid=True,
                    gate_eligible=False,
                    verification_level=verifier.PREVIEW_ATTESTED,
                    claimed_provider_verified=False,
                    claimed_counts_as_preview_acceptance=True,
                    provider_verified=False,
                    counts_as_preview_acceptance=False,
                    source_identity_bound=True,
                    source_identity=identity,
                    raw_export_asset_id=101,
                    raw_export_sha256=verifier.digest(raw),
                    evidence_envelope_asset_id=102,
                    evidence_envelope_sha256=verifier.digest(envelope),
                    verifier_report_asset_id=103,
                    verifier_report_sha256=verifier.digest(report),
                    release_asset_index_sha256=verifier.digest(index_path),
                )

            live_assets = {
                record["asset_id"]: {
                    "id": record["asset_id"],
                    "name": record["name"],
                    "url": (
                        "https://api.github.com/repos/owner/repository/releases/assets/"
                        + str(record["asset_id"])
                    ),
                    "browser_download_url": record["browser_download_url"],
                    "digest": record["sha256"],
                    "size": record["size"],
                    "state": "uploaded",
                }
                for record in records
            }
            index_live = {
                "id": 104,
                "name": index_path.name,
                "url": "https://api.github.com/repos/owner/repository/releases/assets/104",
                "browser_download_url": "https://github.com/owner/repository/releases/download/v1/index.json",
                "digest": verifier.digest(index_path),
                "size": index_path.stat().st_size,
                "state": "uploaded",
            }
            payload_by_url = {
                live_assets[record["asset_id"]]["url"]: (root / record["name"]).read_bytes()
                for record in records
            }
            payload_by_url[index_live["url"]] = index_path.read_bytes()

            def fake_github(url, *, binary, opener=None):
                if not binary or url not in payload_by_url:
                    raise AssertionError("unexpected GitHub request in result-contract test")
                return payload_by_url[url]

            environment = {
                "GITHUB_ACTIONS": "true" if not synthetic else "false",
                "GITHUB_RUN_ID": "7001" if not synthetic else "",
                "GITHUB_REPOSITORY": "owner/repository" if not synthetic else "",
            }
            with patch.object(
                verifier, "validate_code_bindings", lambda *_a, **_k: {}
            ), patch.object(
                verifier,
                "validate_evidence_bundle",
                fake_integrity,
            ), patch.object(
                verifier,
                "validate_live_github_witness",
                lambda *_a, **_k: (live_assets, index_live),
            ), patch.object(
                verifier, "github_request", fake_github
            ), patch.dict(os.environ, environment, clear=False):
                result = verifier.verify(request, synthetic_self_test=synthetic)
                if not synthetic:
                    original_index_payload = payload_by_url[index_live["url"]]
                    payload_by_url[index_live["url"]] = b"tampered-index"
                    expect_rejected(
                        verifier,
                        lambda: verifier.verify(
                            request, synthetic_self_test=False
                        ),
                        "Release asset-index byte substitution",
                    )
                    payload_by_url[index_live["url"]] = original_index_payload

            if (
                result.get("schema_version") != 3
                or result.get("evidence_id") != "preview-result-contract"
                or result.get("adapter_id") != verifier.PREVIEW_ADAPTER_ID
                or result.get("verification_level") != verifier.PREVIEW_ATTESTED
                or result.get("source_identity") != identity
                or set(result.get("artifact_digests", {}))
                != {
                    "raw_export_sha256",
                    "evidence_envelope_sha256",
                    "verifier_report_sha256",
                    "release_asset_index_sha256",
                }
                or len(result.get("verified_assets", [])) != (3 if synthetic else 4)
                or result.get("live_verifier", {}).get("live_requery") is synthetic
                or result.get("live_verifier", {}).get("independent") is synthetic
                or result.get("gate_eligibility", {}).get("eligible") is synthetic
                or result.get("gate_eligible") is synthetic
                or result.get("counts_as_preview_attested") is synthetic
                or result.get("counts_as_provider_verified") is not False
            ):
                raise AssertionError("schema-v3 result contract is incomplete or unsafe")
            expected_asset_fields = {
                "asset_id",
                "name",
                "sha256",
                "size",
                "evidence_kind",
                "state",
                "api_url",
                "browser_download_url",
            }
            if any(
                set(asset) != expected_asset_fields
                or (not synthetic and any(value is None for value in asset.values()))
                for asset in result["verified_assets"]
            ):
                raise AssertionError("verified asset metadata is incomplete")
            verifier.parse_time(
                result.get("live_verifier", {}).get("verified_at", ""),
                "result verified_at",
            )
            if not synthetic:
                integrity = result["integrity_result"]
                if (
                    integrity.get("raw_export_sha256") != verifier.digest(raw)
                    or integrity.get("evidence_envelope_sha256")
                    != verifier.digest(envelope)
                    or integrity.get("verifier_report_sha256")
                    != verifier.digest(report)
                    or integrity.get("release_asset_index_sha256")
                    != verifier.digest(index_path)
                    or integrity.get("release_asset_index_asset_id") != 104
                    or result["verified_assets"][-1].get("evidence_kind")
                    != "release_asset_index"
                ):
                    raise AssertionError("live result omitted a raw/E/V/index binding")
    if getattr(verifier.verify, "adapter_id", None) != verifier.PREVIEW_ADAPTER_ID:
        raise AssertionError("verify callable has no canonical adapter id")
    return 3


def main() -> int:
    verifier = load_verifier()
    count = (
        transport_tests(verifier)
        + witness_before_download_tests(verifier)
        + bundle_request_tests(verifier)
        + verify_call_order_test(verifier)
        + structured_result_tests(verifier)
    )
    print(f"Phase 8 Preview verifier transport tests passed; guards={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
