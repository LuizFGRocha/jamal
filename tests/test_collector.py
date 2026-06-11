import pytest

from jamal.collector import Collector
from jamal.models import CommitInfo


def test_collect_returns_commits(fixture_repo):
    commits = Collector(fixture_repo).collect()
    assert len(commits) >= 3


def test_collect_commit_structure(fixture_repo):
    commits = Collector(fixture_repo).collect()
    first = commits[0]
    assert isinstance(first, CommitInfo)
    assert first.hash
    assert first.author
    assert first.date is not None
    assert first.message


def test_collect_files_changed(fixture_repo):
    commits = Collector(fixture_repo).collect()
    assert any(len(c.files_changed) > 0 for c in commits)


def test_collect_empty_repo(tmp_path):
    import subprocess
    subprocess.run(["git", "init"], cwd=str(tmp_path), capture_output=True)
    commits = Collector(str(tmp_path)).collect()
    assert commits == []


def test_collect_invalid_repo():
    commits = Collector("/nonexistent/path/repo").collect()
    assert commits == []
