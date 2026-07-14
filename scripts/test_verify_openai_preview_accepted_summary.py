#!/usr/bin/env python3
"""Fail-closed fixtures for the independent accepted-summary consumer."""

from __future__ import annotations

import copy
import contextlib
import hashlib
import io
import json
import os
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import test_build_openai_preview_accepted_summary as producer_fixture
import verify_openai_preview_accepted_summary as consumer
from build_openai_preview_accepted_summary import build_summary


REPOSITORY = "owner/repository"
SOURCE = "a" * 40
RUN_ID = 123
RUN_ATTEMPT = 2
CONSUMER_RUN_ID = 456
CONSUMER_RUN_ATTEMPT = 1
REPOSITORY_ID = 9001
WORKFLOW_ID = 701
PREFLIGHT_JOB_ID = 801
PROTECTED_JOB_ID = 802
ENVIRONMENT_ID = 901
DEPLOYMENT_ID = 1001
STATUS_QUEUED_ID = 1101
STATUS_SUCCESS_ID = 1102
ARTIFACT_ID = 1201
JOB_URL = (
    f"https://github.com/{REPOSITORY}/actions/runs/{RUN_ID}/job/{PROTECTED_JOB_ID}"
)


class FakeJson:
    def __init__(self, values: dict[str, Any]) -> None:
        self.values = values
        self.calls: list[str] = []

    def __call__(self, url: str) -> Any:
        self.calls.append(url)
        if url not in self.values:
            raise AssertionError(f"unexpected JSON URL: {url}")
        value = self.values[url]
        if isinstance(value, JsonSequence):
            if not value.responses:
                raise AssertionError(f"exhausted JSON sequence: {url}")
            value = value.responses.pop(0)
        return copy.deepcopy(value)


class JsonSequence:
    def __init__(self, responses: list[Any]) -> None:
        self.responses = responses


class FakeBinary:
    def __init__(self, values: dict[str, bytes]) -> None:
        self.values = values
        self.calls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.calls.append(url)
        if url not in self.values:
            raise AssertionError(f"unexpected binary URL: {url}")
        return self.values[url]


def api(suffix: str = "") -> str:
    return f"https://api.github.com/repos/{REPOSITORY}{suffix}"


def zip_summary(summary: Any, *, name: str = consumer.SUMMARY_JSON_NAME) -> bytes:
    payload = json.dumps(
        summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(name, payload)
    return stream.getvalue()


def base_summary() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary:
        values = producer_fixture.fixture(Path(temporary))
        return build_summary(**values)


def stage_b_summary() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary:
        values = producer_fixture.fixture(Path(temporary))
        producer_fixture.promote_fixture_to_stage_b(values)
        return build_summary(**values)


def run_document() -> dict[str, Any]:
    repository = {"id": REPOSITORY_ID, "full_name": REPOSITORY}
    return {
        "id": RUN_ID,
        "run_attempt": RUN_ATTEMPT,
        "workflow_id": WORKFLOW_ID,
        "event": "workflow_dispatch",
        "path": consumer.SOURCE_WORKFLOW_PATH,
        "name": consumer.SOURCE_WORKFLOW_NAME,
        "head_branch": "main",
        "head_sha": SOURCE,
        "status": "completed",
        "conclusion": "success",
        "html_url": f"https://github.com/{REPOSITORY}/actions/runs/{RUN_ID}",
        "repository": repository,
        "head_repository": copy.deepcopy(repository),
        "created_at": "2026-07-14T00:01:00Z",
        "run_started_at": "2026-07-14T00:02:00Z",
        "updated_at": "2026-07-14T00:21:00Z",
    }


def job(job_id: int, name: str, *, html_url: str) -> dict[str, Any]:
    return {
        "id": job_id,
        "run_id": RUN_ID,
        "run_attempt": RUN_ATTEMPT,
        "head_sha": SOURCE,
        "head_branch": "main",
        "name": name,
        "status": "completed",
        "conclusion": "success",
        "html_url": html_url,
        "started_at": "2026-07-14T00:11:00Z",
        "completed_at": "2026-07-14T00:20:00Z",
    }


def fixture() -> dict[str, Any]:
    summary = base_summary()
    archive_url = api(f"/actions/artifacts/{ARTIFACT_ID}/zip")
    archive = zip_summary(summary)
    source_run = run_document()
    preflight = job(
        PREFLIGHT_JOB_ID,
        consumer.PREFLIGHT_JOB_NAME,
        html_url=(
            f"https://github.com/{REPOSITORY}/actions/runs/{RUN_ID}/job/{PREFLIGHT_JOB_ID}"
        ),
    )
    protected = job(PROTECTED_JOB_ID, consumer.PROTECTED_JOB_NAME, html_url=JOB_URL)
    environment_url = api(f"/environments/{consumer.ENVIRONMENT_NAME}")
    deployment_url = api(f"/deployments/{DEPLOYMENT_ID}")
    artifact = {
        "id": ARTIFACT_ID,
        "name": f"{consumer.SUMMARY_ARTIFACT_PREFIX}{RUN_ID}-{RUN_ATTEMPT}",
        "size_in_bytes": len(archive),
        "archive_download_url": archive_url,
        "digest": "sha256:" + hashlib.sha256(archive).hexdigest(),
        "expired": False,
        "created_at": "2026-07-14T00:18:00Z",
        "updated_at": "2026-07-14T00:18:00Z",
        "expires_at": "2026-10-12T00:18:00Z",
        "workflow_run": {
            "id": RUN_ID,
            "head_sha": SOURCE,
            "head_branch": "main",
        },
    }
    deployment = {
        "id": DEPLOYMENT_ID,
        "sha": SOURCE,
        "ref": "main",
        "task": "deploy",
        "environment": consumer.ENVIRONMENT_NAME,
        "created_at": "2026-07-14T00:10:00Z",
        "url": deployment_url,
        "statuses_url": deployment_url + "/statuses",
        "repository_url": api(),
    }
    queued_status = {
        "id": STATUS_QUEUED_ID,
        "state": "queued",
        "log_url": JOB_URL,
        "target_url": JOB_URL,
        "deployment_url": deployment_url,
        "repository_url": api(),
        "environment": consumer.ENVIRONMENT_NAME,
        "created_at": "2026-07-14T00:11:00Z",
        "updated_at": "2026-07-14T00:11:00Z",
    }
    success_status = {
        **queued_status,
        "id": STATUS_SUCCESS_ID,
        "state": "success",
        "created_at": "2026-07-14T00:19:00Z",
        "updated_at": "2026-07-14T00:19:00Z",
    }
    deployment_query = (
        api("/deployments")
        + f"?sha={SOURCE}&ref=main&environment={consumer.ENVIRONMENT_NAME}"
        + "&per_page=100&page=1"
    )
    listed_run = copy.deepcopy(source_run)
    exact_run = copy.deepcopy(source_run)
    listed_preflight = copy.deepcopy(preflight)
    listed_protected = copy.deepcopy(protected)
    direct_protected = copy.deepcopy(protected)
    listed_deployment = copy.deepcopy(deployment)
    direct_deployment = copy.deepcopy(deployment)
    listed_success = copy.deepcopy(success_status)
    listed_queued = copy.deepcopy(queued_status)
    listed_artifact = copy.deepcopy(artifact)
    direct_artifact = copy.deepcopy(artifact)
    jobs_url = api(
        f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=1"
    )
    branch_policies_url = (
        environment_url + "/deployment-branch-policies?per_page=100&page=1"
    )
    approvals_url = api(f"/actions/runs/{RUN_ID}/approvals")
    pending_url = api(f"/actions/runs/{RUN_ID}/pending_deployments")
    statuses_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    artifacts_url = api(f"/actions/runs/{RUN_ID}/artifacts?per_page=100&page=1")
    direct_artifact_url = api(f"/actions/artifacts/{ARTIFACT_ID}")
    json_values = {
        api(): {"id": REPOSITORY_ID, "full_name": REPOSITORY, "default_branch": "main"},
        api(f"/actions/runs/{RUN_ID}"): listed_run,
        api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}"): exact_run,
        api(f"/actions/workflows/{WORKFLOW_ID}"): {
            "id": WORKFLOW_ID,
            "name": consumer.SOURCE_WORKFLOW_NAME,
            "path": consumer.SOURCE_WORKFLOW_PATH,
            "state": "active",
        },
        jobs_url: {
            "total_count": 2,
            "jobs": [listed_preflight, listed_protected],
        },
        api(f"/actions/jobs/{PROTECTED_JOB_ID}"): direct_protected,
        environment_url: {
            "id": ENVIRONMENT_ID,
            "name": consumer.ENVIRONMENT_NAME,
            "url": environment_url,
            "created_at": "2026-07-13T00:00:00Z",
            "updated_at": "2026-07-13T00:00:00Z",
            "protection_rules": [
                {
                    "id": 910,
                    "type": "required_reviewers",
                    "prevent_self_review": False,
                    "reviewers": [
                        {
                            "type": "User",
                            "reviewer": {"id": 1, "login": "xuxu-wei"},
                        }
                    ],
                },
                {"id": 911, "type": "branch_policy"},
            ],
            "deployment_branch_policy": {
                "protected_branches": False,
                "custom_branch_policies": True,
            },
        },
        branch_policies_url: {
            "total_count": 1,
            "branch_policies": [{"id": 920, "name": "main", "type": "branch"}],
        },
        approvals_url: [
            {
                "state": "approved",
                "comment": "Preview evidence accepted",
                "environments": [
                    {"id": ENVIRONMENT_ID, "name": consumer.ENVIRONMENT_NAME}
                ],
                "user": {"id": 1, "login": "xuxu-wei"},
            }
        ],
        pending_url: [],
        deployment_query: [listed_deployment],
        statuses_url: [
            listed_success,
            listed_queued,
        ],
        deployment_url: direct_deployment,
        artifacts_url: {
            "total_count": 1,
            "artifacts": [listed_artifact],
        },
        direct_artifact_url: direct_artifact,
    }
    expected_json_calls = [
        api(),
        api(f"/actions/runs/{RUN_ID}"),
        api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}"),
        api(f"/actions/workflows/{WORKFLOW_ID}"),
        jobs_url,
        api(f"/actions/jobs/{PROTECTED_JOB_ID}"),
        environment_url,
        branch_policies_url,
        approvals_url,
        pending_url,
        deployment_query,
        statuses_url,
        deployment_url,
        artifacts_url,
        direct_artifact_url,
        environment_url,
        branch_policies_url,
        statuses_url,
        direct_artifact_url,
        api(f"/actions/runs/{RUN_ID}"),
    ]
    return {
        "summary": summary,
        "archive_url": archive_url,
        "artifact_objects": [listed_artifact, direct_artifact],
        "deployment_objects": [listed_deployment, direct_deployment],
        "success_status": listed_success,
        "protected_job": listed_protected,
        "json": json_values,
        "binary": {archive_url: archive},
        "expected_json_calls": expected_json_calls,
        "deployment_query": deployment_query,
        "environment_url": environment_url,
        "deployment_url": deployment_url,
    }


def refresh_archive(values: dict[str, Any], *, name: str = consumer.SUMMARY_JSON_NAME) -> None:
    archive = zip_summary(values["summary"], name=name)
    values["binary"][values["archive_url"]] = archive
    for artifact in values["artifact_objects"]:
        artifact["size_in_bytes"] = len(archive)
        artifact["digest"] = "sha256:" + hashlib.sha256(archive).hexdigest()


def run(values: dict[str, Any]) -> dict[str, Any]:
    json_fetcher = FakeJson(values["json"])
    binary_fetcher = FakeBinary(values["binary"])
    result = consumer.verify(
        repository=REPOSITORY,
        run_id=RUN_ID,
        run_attempt=RUN_ATTEMPT,
        source_commit=SOURCE,
        consumer_commit=SOURCE,
        consumer_run_id=CONSUMER_RUN_ID,
        consumer_run_attempt=CONSUMER_RUN_ATTEMPT,
        json_fetcher=json_fetcher,
        binary_fetcher=binary_fetcher,
        now=datetime(2026, 7, 14, 1, 0, tzinfo=timezone.utc),
    )
    assert json_fetcher.calls == values["expected_json_calls"]
    assert binary_fetcher.calls == [values["archive_url"]]
    return result


def rejected(
    mutation: Callable[[dict[str, Any]], None],
    base: dict[str, Any],
    expected_code: str,
) -> None:
    values = copy.deepcopy(base)
    mutation(values)
    try:
        run(values)
    except consumer.AcceptedSummaryConsumerError as exc:
        assert exc.code == expected_code, (
            f"mutation raised {exc.code}, expected {expected_code}: {mutation}"
        )
        return
    raise AssertionError(f"consumer accepted mutation: {mutation}")


def remove_job(values: dict[str, Any], name: str) -> None:
    url = api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=1")
    listing = values["json"][url]
    listing["jobs"] = [job_value for job_value in listing["jobs"] if job_value["name"] != name]
    listing["total_count"] = len(listing["jobs"])


def duplicate_protected_job(values: dict[str, Any]) -> None:
    url = api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=1")
    listing = values["json"][url]
    duplicate = copy.deepcopy(values["protected_job"])
    duplicate["id"] = 803
    duplicate["html_url"] = f"https://github.com/{REPOSITORY}/actions/runs/{RUN_ID}/job/803"
    listing["jobs"].append(duplicate)
    listing["total_count"] += 1


def two_page_jobs(values: dict[str, Any]) -> None:
    first_url = api(
        f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=1"
    )
    second_url = api(
        f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=2"
    )
    first = values["json"][first_url]
    first["jobs"].extend({"id": 2000 + offset} for offset in range(98))
    first["total_count"] = 101
    values["json"][second_url] = {"total_count": 101, "jobs": [{"id": 3000}]}
    call_index = values["expected_json_calls"].index(first_url)
    values["expected_json_calls"].insert(call_index + 1, second_url)


def duplicate_job_across_pages(values: dict[str, Any]) -> None:
    two_page_jobs(values)
    second_url = api(
        f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=2"
    )
    values["json"][second_url]["jobs"][0]["id"] = 2000


def drift_job_total_across_pages(values: dict[str, Any]) -> None:
    two_page_jobs(values)
    second_url = api(
        f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=2"
    )
    values["json"][second_url]["total_count"] = 102


def two_page_deployments(values: dict[str, Any]) -> None:
    first_url = values["deployment_query"]
    second_url = first_url.removesuffix("page=1") + "page=2"
    values["json"][first_url].extend(
        {"id": 5000 + offset} for offset in range(99)
    )
    values["json"][second_url] = []
    call_index = values["expected_json_calls"].index(first_url)
    values["expected_json_calls"].insert(call_index + 1, second_url)


def duplicate_deployment_across_pages(values: dict[str, Any]) -> None:
    two_page_deployments(values)
    second_url = values["deployment_query"].removesuffix("page=1") + "page=2"
    values["json"][second_url] = [{"id": 5000}]


def two_page_statuses(values: dict[str, Any]) -> None:
    first_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    second_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=2")
    values["json"][first_url].extend(
        {
            "id": 6000 + offset,
            "state": "inactive",
            "log_url": f"https://github.com/{REPOSITORY}/actions/runs/999/job/{6000 + offset}",
            "created_at": "2026-07-14T00:12:00Z",
        }
        for offset in range(98)
    )
    values["json"][second_url] = []
    for call_index in reversed(
        [
            index
            for index, url in enumerate(values["expected_json_calls"])
            if url == first_url
        ]
    ):
        values["expected_json_calls"].insert(call_index + 1, second_url)


def duplicate_status_across_pages(values: dict[str, Any]) -> None:
    two_page_statuses(values)
    second_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=2")
    values["json"][second_url] = [
        {
            "id": 6000,
            "state": "inactive",
            "log_url": "https://example.test/duplicate",
            "created_at": "2026-07-14T00:12:00Z",
        }
    ]


def add_branch_policy(values: dict[str, Any]) -> None:
    url = values["environment_url"] + "/deployment-branch-policies?per_page=100&page=1"
    listing = values["json"][url]
    listing["branch_policies"].append({"id": 921, "name": "dev", "type": "branch"})
    listing["total_count"] = 2


def remove_artifacts(values: dict[str, Any]) -> None:
    url = api(f"/actions/runs/{RUN_ID}/artifacts?per_page=100&page=1")
    values["json"][url] = {"total_count": 0, "artifacts": []}


def duplicate_artifact(values: dict[str, Any]) -> None:
    url = api(f"/actions/runs/{RUN_ID}/artifacts?per_page=100&page=1")
    listing = values["json"][url]
    duplicate = copy.deepcopy(values["artifact_objects"][0])
    duplicate["id"] = 1202
    duplicate["archive_download_url"] = api("/actions/artifacts/1202/zip")
    listing["artifacts"].append(duplicate)
    listing["total_count"] = 2


def duplicate_deployment(values: dict[str, Any]) -> None:
    duplicate = copy.deepcopy(values["deployment_objects"][0])
    duplicate["id"] = 1002
    duplicate_url = api("/deployments/1002")
    duplicate["url"] = duplicate_url
    duplicate["statuses_url"] = duplicate_url + "/statuses"
    values["json"][values["deployment_query"]].append(duplicate)
    values["json"][duplicate_url] = copy.deepcopy(duplicate)
    statuses = copy.deepcopy(
        values["json"][api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")]
    )
    for status in statuses:
        status["id"] += 100
        status["deployment_url"] = duplicate_url
    values["json"][api("/deployments/1002/statuses?per_page=100&page=1")] = statuses


def later_failure(values: dict[str, Any]) -> None:
    statuses_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    failure = copy.deepcopy(values["success_status"])
    failure.update(id=1103, state="failure", created_at="2026-07-14T00:19:30Z")
    values["json"][statuses_url].append(failure)


def later_failure_other_job(values: dict[str, Any]) -> None:
    later_failure(values)
    statuses_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    values["json"][statuses_url][-1]["log_url"] = (
        f"https://github.com/{REPOSITORY}/actions/runs/999/job/999"
    )


def same_second_ambiguous_failure(values: dict[str, Any]) -> None:
    statuses_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    failure = copy.deepcopy(values["success_status"])
    failure.update(
        id=1103,
        state="failure",
        log_url=f"https://github.com/{REPOSITORY}/actions/runs/999/job/999",
        created_at=values["success_status"]["created_at"],
    )
    values["json"][statuses_url].insert(0, failure)


def environment_drift(values: dict[str, Any]) -> None:
    url = values["environment_url"]
    initial = copy.deepcopy(values["json"][url])
    changed = copy.deepcopy(initial)
    changed["updated_at"] = "2026-07-14T00:30:00Z"
    changed["protection_rules"][0]["reviewers"][0]["reviewer"]["login"] = "other"
    values["json"][url] = JsonSequence([initial, changed])


def branch_policy_drift(values: dict[str, Any]) -> None:
    url = values["environment_url"] + "/deployment-branch-policies?per_page=100&page=1"
    initial = copy.deepcopy(values["json"][url])
    changed = copy.deepcopy(initial)
    changed["branch_policies"][0]["name"] = "release/*"
    values["json"][url] = JsonSequence([initial, changed])


def deployment_status_drift(values: dict[str, Any]) -> None:
    url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    initial = copy.deepcopy(values["json"][url])
    changed = copy.deepcopy(initial)
    failure = copy.deepcopy(values["success_status"])
    failure.update(
        id=1199,
        state="failure",
        log_url=f"https://github.com/{REPOSITORY}/actions/runs/999/job/999",
        created_at="2026-07-14T00:19:30Z",
    )
    changed.append(failure)
    values["json"][url] = JsonSequence([initial, changed])


def artifact_expiry_drift(values: dict[str, Any]) -> None:
    url = api(f"/actions/artifacts/{ARTIFACT_ID}")
    initial = copy.deepcopy(values["json"][url])
    changed = copy.deepcopy(initial)
    changed["expired"] = True
    values["json"][url] = JsonSequence([initial, changed])


def latest_attempt_drift(values: dict[str, Any]) -> None:
    url = api(f"/actions/runs/{RUN_ID}")
    initial = copy.deepcopy(values["json"][url])
    changed = copy.deepcopy(initial)
    changed["run_attempt"] = RUN_ATTEMPT + 1
    changed["conclusion"] = "failure"
    values["json"][url] = JsonSequence([initial, changed])


def direct_deployment_mismatch(values: dict[str, Any]) -> None:
    values["json"][values["deployment_url"]]["created_at"] = (
        "2026-07-14T00:10:01Z"
    )


def direct_artifact_mismatch(values: dict[str, Any]) -> None:
    url = api(f"/actions/artifacts/{ARTIFACT_ID}")
    values["json"][url]["digest"] = "sha256:" + "0" * 64


def invalid_summary_json(values: dict[str, Any]) -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(consumer.SUMMARY_JSON_NAME, b"{")
    payload = stream.getvalue()
    values["binary"][values["archive_url"]] = payload
    for artifact in values["artifact_objects"]:
        artifact["size_in_bytes"] = len(payload)
        artifact["digest"] = "sha256:" + hashlib.sha256(payload).hexdigest()


def multi_member_zip(values: dict[str, Any]) -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(consumer.SUMMARY_JSON_NAME, json.dumps(values["summary"]))
        archive.writestr("extra.json", "{}")
    payload = stream.getvalue()
    values["binary"][values["archive_url"]] = payload
    for artifact in values["artifact_objects"]:
        artifact["size_in_bytes"] = len(payload)
        artifact["digest"] = "sha256:" + hashlib.sha256(payload).hexdigest()


def mutate_summary(
    callback: Callable[[dict[str, Any]], None]
) -> Callable[[dict[str, Any]], None]:
    def mutation(values: dict[str, Any]) -> None:
        callback(values["summary"])
        refresh_archive(values)

    return mutation


def main() -> int:
    base = fixture()
    result = run(copy.deepcopy(base))
    assert result["schema_version"] == consumer.RESULT_SCHEMA
    assert result["target_run"]["run_attempt"] == RUN_ATTEMPT
    assert result["deployment"]["status_id"] == STATUS_SUCCESS_ID
    assert result["artifact"]["artifact_id"] == ARTIFACT_ID
    assert result["accepted_summary_binding"]["release_stage"] == "A"
    assert result["accepted_summary_binding"]["stage_a_verified_record_count"] == 0
    assert (
        result["accepted_summary_binding"][
            "stage_a_closure_consumer_result_sha256"
        ]
        is None
    )
    assert result["decision"] == {
        "verification_level": "preview_attested",
        "provider_verified": False,
        "counts_as_phase78_closure": True,
        "accepted": True,
    }
    paginated = copy.deepcopy(base)
    two_page_jobs(paginated)
    assert run(paginated)["decision"]["accepted"] is True
    paginated_deployments = copy.deepcopy(base)
    two_page_deployments(paginated_deployments)
    assert run(paginated_deployments)["decision"]["accepted"] is True
    paginated_statuses = copy.deepcopy(base)
    two_page_statuses(paginated_statuses)
    assert run(paginated_statuses)["decision"]["accepted"] is True

    run_url = api(f"/actions/runs/{RUN_ID}")
    attempt_url = api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}")
    jobs_url = api(f"/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100&page=1")
    environment_url = base["environment_url"]
    approvals_url = api(f"/actions/runs/{RUN_ID}/approvals")
    pending_url = api(f"/actions/runs/{RUN_ID}/pending_deployments")
    statuses_url = api(f"/deployments/{DEPLOYMENT_ID}/statuses?per_page=100&page=1")
    artifacts_url = api(f"/actions/runs/{RUN_ID}/artifacts?per_page=100&page=1")

    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda v: v["json"][api()].__setitem__("default_branch", "dev"),
        lambda v: v["json"][api()].__setitem__("id", 9999),
        lambda v: v["json"][run_url].__setitem__("run_attempt", 3),
        lambda v: v["json"][attempt_url].__setitem__("run_attempt", 1),
        lambda v: v["json"][attempt_url].__setitem__("event", "push"),
        lambda v: v["json"][attempt_url].__setitem__("path", ".github/workflows/other.yml"),
        lambda v: v["json"][attempt_url].__setitem__("name", "Other"),
        lambda v: v["json"][attempt_url].__setitem__("head_branch", "dev"),
        lambda v: v["json"][attempt_url].__setitem__("head_sha", "b" * 40),
        lambda v: v["json"][attempt_url].__setitem__("status", "in_progress"),
        lambda v: v["json"][attempt_url].__setitem__("conclusion", "failure"),
        lambda v: v["json"][attempt_url].__setitem__("html_url", "https://example.test/run"),
        lambda v: v["json"][attempt_url]["repository"].__setitem__("id", 99),
        lambda v: v["json"][api(f"/actions/workflows/{WORKFLOW_ID}")].__setitem__("state", "disabled_manually"),
        duplicate_protected_job,
        lambda v: remove_job(v, consumer.PROTECTED_JOB_NAME),
        lambda v: v["json"][jobs_url]["jobs"][1].__setitem__("conclusion", "failure"),
        lambda v: v["json"][jobs_url]["jobs"][1].__setitem__("run_attempt", 1),
        lambda v: v["json"][jobs_url]["jobs"][1].__setitem__("html_url", "https://example.test/job"),
        lambda v: v["json"][api(f"/actions/jobs/{PROTECTED_JOB_ID}")].__setitem__("head_sha", "b" * 40),
        lambda v: remove_job(v, consumer.PREFLIGHT_JOB_NAME),
        lambda v: v["json"][environment_url]["protection_rules"].pop(0),
        lambda v: v["json"][environment_url]["deployment_branch_policy"].__setitem__("custom_branch_policies", False),
        lambda v: v["json"][environment_url]["protection_rules"].pop(),
        add_branch_policy,
        lambda v: v["json"].__setitem__(approvals_url, []),
        lambda v: v["json"][approvals_url][0].__setitem__("state", "rejected"),
        lambda v: v["json"][approvals_url][0]["user"].__setitem__("login", "intruder"),
        lambda v: v["json"].__setitem__(pending_url, [{"environment": {"id": ENVIRONMENT_ID}}]),
        lambda v: v["json"][environment_url].__setitem__("updated_at", "2026-07-14T00:10:30Z"),
        lambda v: v["json"].__setitem__(v["deployment_query"], []),
        lambda v: [item.__setitem__("sha", "b" * 40) for item in v["deployment_objects"]],
        duplicate_deployment,
        lambda v: [item.__setitem__("state", "queued") for item in v["json"][statuses_url]],
        lambda v: v["success_status"].__setitem__("log_url", "https://example.test/job"),
        later_failure,
        later_failure_other_job,
        same_second_ambiguous_failure,
        lambda v: v["success_status"].__setitem__("environment", "other"),
        lambda v: [item.__setitem__("created_at", "2026-07-14T00:21:00Z") for item in v["deployment_objects"]],
        remove_artifacts,
        duplicate_artifact,
        lambda v: [item.__setitem__("expired", True) for item in v["artifact_objects"]],
        lambda v: [item["workflow_run"].__setitem__("id", 999) for item in v["artifact_objects"]],
        lambda v: [item.__setitem__("archive_download_url", "https://example.test/archive") for item in v["artifact_objects"]],
        lambda v: [item.__setitem__("digest", "sha256:" + "0" * 64) for item in v["artifact_objects"]],
        lambda v: [item.__setitem__("size_in_bytes", item["size_in_bytes"] + 1) for item in v["artifact_objects"]],
        lambda v: refresh_archive(v, name="../openai-preview-accepted-summary.json"),
        multi_member_zip,
        invalid_summary_json,
        mutate_summary(lambda s: s.__setitem__("schema_version", "openai-preview-accepted-run-summary/v1")),
        mutate_summary(lambda s: s.__setitem__("run_id", 999)),
        mutate_summary(lambda s: s.__setitem__("repository", "other/repository")),
        mutate_summary(lambda s: s.__setitem__("acceptance_scope", "external")),
        mutate_summary(lambda s: s.__setitem__("counts_as_phase78_closure", True)),
        mutate_summary(lambda s: s["phase7"].__setitem__("verified_runtime_count", 9)),
        mutate_summary(lambda s: s["phase7"]["live_slot_results"][1].__setitem__("evidence_id", s["phase7"]["live_slot_results"][0]["evidence_id"])),
        mutate_summary(lambda s: s["phase8"]["reviewer_items"][1].__setitem__("reviewer_instance_id", s["phase8"]["reviewer_items"][0]["reviewer_instance_id"])),
        mutate_summary(lambda s: s["phase8"]["retrieval_distribution"].__setitem__("search", 2)),
        mutate_summary(lambda s: s["evidence_inventory"].pop()),
        mutate_summary(lambda s: s["candidate_assets"].pop()),
        mutate_summary(lambda s: s["releases"]["evidence"].__setitem__("immutable", False)),
        mutate_summary(lambda s: s["release_evidence"].__setitem__("provider_verified", True)),
        mutate_summary(lambda s: s["final_status"].__setitem__("accepted", False)),
        lambda v: v["json"][jobs_url].__setitem__("total_count", 3),
        lambda v: v["json"][jobs_url]["jobs"][1].__setitem__("id", PREFLIGHT_JOB_ID),
        direct_deployment_mismatch,
        direct_artifact_mismatch,
        environment_drift,
        branch_policy_drift,
        deployment_status_drift,
        artifact_expiry_drift,
        latest_attempt_drift,
        mutate_summary(
            lambda s: s["releases"]["evidence"].__setitem__("final_commit", "b" * 40)
        ),
        mutate_summary(
            lambda s: s["releases"]["candidate"].__setitem__("final_commit", "b" * 40)
        ),
    ]
    expected_codes = [
        "repository_identity_invalid",
        *(["workflow_attempt_invalid"] * 12),
        "workflow_identity_invalid",
        *(["protected_job_invalid"] * 7),
        *(["environment_policy_invalid"] * 4),
        *(["environment_approval_invalid"] * 4),
        *(["deployment_binding_invalid"] * 11),
        *(["summary_artifact_invalid"] * 7),
        "summary_archive_invalid",
        "summary_archive_invalid",
        "summary_json_invalid",
        *(["summary_identity_invalid"] * 5),
        "summary_phase7_invalid",
        "summary_lineage_invalid",
        "summary_phase8_invalid",
        "summary_phase8_invalid",
        "summary_inventory_invalid",
        "summary_inventory_invalid",
        "summary_release_invalid",
        "summary_evidence_invalid",
        "summary_final_status_invalid",
        "pagination_invalid",
        "pagination_invalid",
        "deployment_binding_invalid",
        "summary_artifact_invalid",
        "environment_policy_changed",
        "environment_policy_changed",
        "deployment_binding_invalid",
        "summary_artifact_changed",
        "workflow_attempt_changed",
        "summary_release_invalid",
        "summary_release_invalid",
    ]
    assert len(expected_codes) == len(mutations)
    for expected_code, mutation in zip(expected_codes, mutations, strict=True):
        rejected(mutation, base, expected_code)
    rejected(
        mutate_summary(
            lambda summary: summary["release_evidence"].update(
                release_stage="B",
                stage_a_predecessor_scope="previous_releases[0]",
                stage_a_verified_record_count=8,
            )
        ),
        base,
        "summary_evidence_invalid",
    )

    stage_b_base = fixture()
    stage_b_base["summary"] = stage_b_summary()
    refresh_archive(stage_b_base)
    stage_b_result = run(copy.deepcopy(stage_b_base))
    assert stage_b_result["accepted_summary_binding"]["release_stage"] == "B"
    assert (
        stage_b_result["accepted_summary_binding"]["stage_a_verified_record_count"]
        == 9
    )
    assert (
        stage_b_result["accepted_summary_binding"][
            "stage_a_closure_consumer_result_sha256"
        ]
        == stage_b_base["summary"]["release_evidence"]["stage_a_closure"][
            "consumer_result_sha256"
        ]
    )
    rejected(
        mutate_summary(
            lambda summary: summary["release_evidence"].__setitem__(
                "stage_a_predecessor_scope", "previous_releases[1]"
            )
        ),
        stage_b_base,
        "summary_evidence_invalid",
    )
    rejected(
        mutate_summary(
            lambda summary: summary["release_evidence"]["history_items"].pop()
        ),
        stage_b_base,
        "summary_evidence_invalid",
    )
    rejected(
        mutate_summary(
            lambda summary: summary["release_evidence"]["stage_a_closure"].__setitem__(
                "phase7_verified_runtime_count", 9
            )
        ),
        stage_b_base,
        "summary_evidence_invalid",
    )
    rejected(
        mutate_summary(
            lambda summary: summary["release_evidence"]["stage_a_closure"].__setitem__(
                "consumer_result_sha256", "not-a-digest"
            )
        ),
        stage_b_base,
        "digest_invalid",
    )
    rejected(duplicate_job_across_pages, base, "pagination_invalid")
    rejected(drift_job_total_across_pages, base, "pagination_invalid")
    rejected(duplicate_deployment_across_pages, base, "pagination_invalid")
    rejected(duplicate_status_across_pages, base, "pagination_invalid")

    try:
        consumer.verify(
            repository=REPOSITORY,
            run_id=RUN_ID,
            run_attempt=RUN_ATTEMPT,
            source_commit=SOURCE,
            consumer_commit="b" * 40,
            consumer_run_id=CONSUMER_RUN_ID,
            consumer_run_attempt=CONSUMER_RUN_ATTEMPT,
            json_fetcher=FakeJson({}),
            binary_fetcher=FakeBinary({}),
        )
    except consumer.AcceptedSummaryConsumerError as exc:
        assert exc.code == "consumer_source_drift"
    else:
        raise AssertionError("consumer accepted default-branch source drift")

    old_token = os.environ.pop("GH_TOKEN", None)
    old_actions_token = os.environ.pop("GITHUB_TOKEN", None)
    try:
        try:
            consumer.github_json(api())
        except consumer.AcceptedSummaryConsumerError as exc:
            assert exc.code == "github_token_missing"
        else:
            raise AssertionError("GitHub transport accepted a missing token")
    finally:
        if old_token is not None:
            os.environ["GH_TOKEN"] = old_token
        if old_actions_token is not None:
            os.environ["GITHUB_TOKEN"] = old_actions_token

    for callback, expected_code in (
        (lambda: consumer.github_json("https://example.com/repos/x/y"), "github_url_invalid"),
        (
            lambda: consumer.github_artifact(
                api(f"/actions/artifacts/{ARTIFACT_ID}/zip?x=1")
            ),
            "artifact_url_invalid",
        ),
    ):
        try:
            callback()
        except consumer.AcceptedSummaryConsumerError as exc:
            assert exc.code == expected_code
        else:
            raise AssertionError(f"transport accepted invalid URL for {expected_code}")

    request = urllib.request.Request(base["archive_url"])
    request.add_unredirected_header("Authorization", "Bearer secret")
    redirect = consumer._ArtifactRedirect()
    redirected = redirect.redirect_request(
        request,
        None,
        302,
        "Found",
        {},
        "https://productionresults1.blob.core.windows.net/container/result.zip?sig=test",
    )
    assert redirected is not None
    assert redirected.get_header("Authorization") is None
    assert "Authorization" not in redirected.unredirected_hdrs
    for callback in (
        lambda: redirect.redirect_request(
            request,
            None,
            302,
            "Found",
            {},
            "https://productionresults2.blob.core.windows.net/container/result.zip?sig=test",
        ),
        lambda: consumer._ArtifactRedirect().redirect_request(
            request, None, 302, "Found", {}, "https://example.com/result.zip"
        ),
    ):
        try:
            callback()
        except consumer.AcceptedSummaryConsumerError as exc:
            assert exc.code == "artifact_redirect_rejected"
        else:
            raise AssertionError("artifact transport accepted an unsafe redirect")
    try:
        consumer._NoRedirect().redirect_request(
            urllib.request.Request(api()), None, 302, "Found", {}, api("/redirected")
        )
    except urllib.error.URLError:
        pass
    else:
        raise AssertionError("JSON transport accepted a redirect")

    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "result.json"
        consumer.write_result(output, result)
        try:
            consumer.write_result(output, result)
        except FileExistsError:
            pass
        else:
            raise AssertionError("consumer result writer overwrote an existing result")
        original_payload = output.read_bytes()
        original_verify = consumer.verify
        consumer.verify = lambda **_kwargs: result
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = consumer.main(
                    [
                        "--repository",
                        REPOSITORY,
                        "--run-id",
                        str(RUN_ID),
                        "--run-attempt",
                        str(RUN_ATTEMPT),
                        "--source-commit",
                        SOURCE,
                        "--consumer-commit",
                        SOURCE,
                        "--consumer-run-id",
                        str(CONSUMER_RUN_ID),
                        "--consumer-run-attempt",
                        str(CONSUMER_RUN_ATTEMPT),
                        "--output",
                        str(output),
                    ]
                )
        finally:
            consumer.verify = original_verify
        assert exit_code == 1 and output.read_bytes() == original_payload

    print(
        "OpenAI Preview accepted-summary consumer contracts passed: "
        f"{len(mutations) + 17} guards"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
