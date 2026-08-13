"""
test_release_gate.py — Legal Release Gate regression tests (v0.4.12).

Guards the release-gate scripts so a future edit cannot silently
disable stale-manifest detection (the exact class of failure the gate
exists to prevent).
"""
import json

import pytest


def test_check_manifests_fresh_on_current_repo():
    """The committed manifests must be fresh right now — the gate must
    agree, otherwise the repo itself is in a stale state."""
    import scripts.generate_manifests as gm
    issues = gm.check_manifests()
    assert issues == [], f"Repo manifests are stale: {issues}"


def test_check_manifests_detects_stale(monkeypatch, tmp_path):
    """A manifest whose sha256 does not match its source must be flagged."""
    import scripts.generate_manifests as gm

    sources_dir = tmp_path / "sources"
    manifests_dir = sources_dir / "manifests"
    sources_dir.mkdir(parents=True)
    manifests_dir.mkdir()

    (sources_dir / "fake.md").write_text("محتوى فعلي", encoding="utf-8")
    (manifests_dir / "fake.json").write_text(
        json.dumps({
            "id": "fake",
            "path": "sources/fake.md",
            "sha256": "0" * 64,  # deliberately wrong
            "metadata_status": "needs_review",
            "verification_status": "field_tested",
        }),
        encoding="utf-8",
    )

    monkeypatch.setattr(gm, "SOURCES_DIR", sources_dir)
    monkeypatch.setattr(gm, "MANIFESTS_DIR", manifests_dir)
    monkeypatch.setattr(gm, "_load_valid_regulations", lambda: {"fake"})

    issues = gm.check_manifests()
    assert any("fake" in issue for issue in issues), f"stale manifest not detected: {issues}"


def test_check_manifests_passes_when_fresh(monkeypatch, tmp_path):
    """A correctly generated manifest must pass the gate (no false positives)."""
    import scripts.generate_manifests as gm

    sources_dir = tmp_path / "sources"
    manifests_dir = sources_dir / "manifests"
    sources_dir.mkdir(parents=True)
    manifests_dir.mkdir()

    source_path = sources_dir / "fake.md"
    source_path.write_text("محتوى فعلي", encoding="utf-8")

    fresh = gm.build_manifest(source_path, existing={})
    (manifests_dir / "fake.json").write_text(
        json.dumps(fresh, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(gm, "SOURCES_DIR", sources_dir)
    monkeypatch.setattr(gm, "MANIFESTS_DIR", manifests_dir)
    monkeypatch.setattr(gm, "_load_valid_regulations", lambda: {"fake"})

    issues = gm.check_manifests()
    assert issues == []


def test_generated_at_excluded_from_staleness():
    """generated_at is a wall-clock timestamp — it must be excluded from
    the comparison, otherwise every check would fail spuriously."""
    import scripts.generate_manifests as gm
    assert "generated_at" in gm._NON_STALE_FIELDS


def test_generate_manifest_preserves_generated_at_when_unchanged(monkeypatch, tmp_path):
    """v0.4.13: regenerating an unchanged source must NOT rewrite the
    manifest — otherwise one source edit dirties all 20 manifests with
    fresh timestamps (spurious git churn observed in lifecycle test)."""
    import json
    import scripts.generate_manifests as gm

    sources_dir = tmp_path / "sources"
    manifests_dir = sources_dir / "manifests"
    sources_dir.mkdir(parents=True)
    manifests_dir.mkdir()

    source_path = sources_dir / "fake.md"
    source_path.write_text("محتوى ثابت", encoding="utf-8")

    first = gm.build_manifest(source_path, existing={})
    first["generated_at"] = "2026-01-01T00:00:00+00:00"  # simulate committed file
    (manifests_dir / "fake.json").write_text(
        json.dumps(first, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(gm, "SOURCES_DIR", sources_dir)
    monkeypatch.setattr(gm, "MANIFESTS_DIR", manifests_dir)

    gm.generate_manifest(source_path, overwrite=False)

    on_disk = json.loads((manifests_dir / "fake.json").read_text(encoding="utf-8"))
    assert on_disk["generated_at"] == "2026-01-01T00:00:00+00:00", (
        "generated_at was rewritten for an unchanged manifest — spurious churn"
    )


def test_generate_manifest_updates_when_substantive_change(monkeypatch, tmp_path):
    """A real content change MUST still update sha256 + generated_at."""
    import json
    import scripts.generate_manifests as gm

    sources_dir = tmp_path / "sources"
    manifests_dir = sources_dir / "manifests"
    sources_dir.mkdir(parents=True)
    manifests_dir.mkdir()

    source_path = sources_dir / "fake.md"
    source_path.write_text("المحتوى الأصلي", encoding="utf-8")

    first = gm.build_manifest(source_path, existing={})
    first["generated_at"] = "2026-01-01T00:00:00+00:00"
    (manifests_dir / "fake.json").write_text(
        json.dumps(first, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(gm, "SOURCES_DIR", sources_dir)
    monkeypatch.setattr(gm, "MANIFESTS_DIR", manifests_dir)

    source_path.write_text("محتوى معدل", encoding="utf-8")
    gm.generate_manifest(source_path, overwrite=False)

    on_disk = json.loads((manifests_dir / "fake.json").read_text(encoding="utf-8"))
    assert on_disk["sha256"] != first["sha256"]
    assert on_disk["generated_at"] != "2026-01-01T00:00:00+00:00"
