from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Mapping


def canonical_json_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_portable_path(path: str) -> str:
    if not path or "\\" in path or ":" in path:
        raise ValueError("portable path must be non-empty POSIX relative path")
    parsed = PurePosixPath(path)
    if parsed.is_absolute():
        raise ValueError("portable path must be relative")
    parts = parsed.parts
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("portable path may not traverse or contain dot segments")
    normalized = str(parsed)
    if normalized.startswith("../") or "/../" in normalized:
        raise ValueError("portable path may not traverse")
    return normalized


def build_manifest(
    *,
    archive_id: str,
    files: Mapping[str, bytes],
    created_at: str,
) -> dict:
    if not archive_id:
        raise ValueError("archive_id is required")
    objects = []
    for path in sorted(files):
        safe_path = validate_portable_path(path)
        payload = files[path]
        objects.append(
            {
                "path": safe_path,
                "media_type": _guess_media_type(safe_path),
                "size_bytes": len(payload),
                "algorithm": "SHA-256",
                "digest": sha256_bytes(payload),
            }
        )
    return {
        "schema_version": "INTEGRITY_MANIFEST_V0",
        "archive_id": archive_id,
        "created_at": created_at,
        "objects": objects,
    }


def verify_manifest(manifest: Mapping, files: Mapping[str, bytes]) -> list[str]:
    problems: list[str] = []
    manifest_objects = manifest.get("objects")
    if not isinstance(manifest_objects, list):
        return ["manifest objects must be an array"]

    expected_paths: set[str] = set()
    for item in manifest_objects:
        if not isinstance(item, Mapping):
            problems.append("manifest object must be a mapping")
            continue
        try:
            path = validate_portable_path(str(item["path"]))
        except (KeyError, ValueError) as exc:
            problems.append(f"invalid manifest path: {exc}")
            continue
        expected_paths.add(path)
        payload = files.get(path)
        if payload is None:
            problems.append(f"missing object: {path}")
            continue
        expected_size = item.get("size_bytes")
        if expected_size != len(payload):
            problems.append(f"size mismatch: {path}")
        if item.get("algorithm") != "SHA-256":
            problems.append(f"unsupported digest algorithm: {path}")
        expected_digest = item.get("digest")
        actual_digest = sha256_bytes(payload)
        if expected_digest != actual_digest:
            problems.append(f"digest mismatch: {path}")

    actual_paths: set[str] = set()
    for path in files:
        try:
            actual_paths.add(validate_portable_path(path))
        except ValueError as exc:
            problems.append(f"invalid supplied path {path!r}: {exc}")
    for extra in sorted(actual_paths - expected_paths):
        problems.append(f"unmanifested object: {extra}")

    return problems


def _guess_media_type(path: str) -> str:
    lowered = path.lower()
    if lowered.endswith(".json"):
        return "application/json"
    if lowered.endswith(".txt") or lowered.endswith(".md"):
        return "text/plain"
    return "application/octet-stream"
