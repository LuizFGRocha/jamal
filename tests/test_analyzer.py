from datetime import datetime, timedelta

import pytest

from jamal.analyzer import Analyzer
from jamal.models import CommitInfo, FileChange, FileMetrics


def _commit(hash_, author, files, days=0):
    date = datetime(2024, 1, 1) + timedelta(days=days)
    return CommitInfo(hash_, author, f"{author}@x.com", date, f"commit {hash_}", files)


def test_get_hotspots_ranks_by_score():
    commits = [
        _commit("a", "Alice", [FileChange("hot.py", 50, 50)], 0),
        _commit("b", "Alice", [FileChange("hot.py", 40, 40)], 1),
        _commit("c", "Bob",   [FileChange("cold.py", 5, 5)], 2),
    ]
    metrics = {"hot.py": FileMetrics("hot.py", 5.0, 100, 10, 500)}
    hotspots = Analyzer(commits, metrics).get_hotspots(top_n=5)
    assert hotspots[0].filename == "hot.py"
    assert hotspots[0].hotspot_score > hotspots[1].hotspot_score


def test_get_big_commits_filters_correctly():
    small = _commit("s", "Alice", [FileChange("a.py", 10, 5)])
    big   = _commit("b", "Bob",   [FileChange("a.py", 400, 200)])
    result = Analyzer([small, big]).get_big_commits()
    assert len(result) == 1
    assert result[0].hash == "b"


def test_get_big_commits_empty_when_none():
    commits = [_commit("x", "Alice", [FileChange("a.py", 5, 5)])]
    assert Analyzer(commits).get_big_commits() == []


def test_get_growing_files_detects_trend():
    commits = [
        _commit("a", "Alice", [FileChange("grow.py", 5, 5)], 0),
        _commit("b", "Alice", [FileChange("grow.py", 5, 5)], 1),
        _commit("c", "Bob",   [FileChange("grow.py", 50, 50)], 2),
        _commit("d", "Bob",   [FileChange("grow.py", 60, 60)], 3),
    ]
    growing = Analyzer(commits).get_growing_files()
    assert any(f.filename == "grow.py" for f in growing)


def test_get_coupled_files():
    commits = [
        _commit("a", "Alice", [FileChange("x.py", 1, 0), FileChange("y.py", 1, 0)], 0),
        _commit("b", "Bob",   [FileChange("x.py", 1, 0), FileChange("y.py", 1, 0)], 1),
        _commit("c", "Carol", [FileChange("x.py", 1, 0), FileChange("y.py", 1, 0)], 2),
    ]
    pairs = Analyzer(commits).get_coupled_files()
    assert len(pairs) > 0
    assert pairs[0][2] == 3


def test_get_summary():
    commits = [
        _commit("a", "Alice", [FileChange("a.py", 10, 5)]),
        _commit("b", "Alice", [FileChange("b.py", 20, 10)]),
        _commit("c", "Bob",   [FileChange("c.py", 5, 5)]),
    ]
    summary = Analyzer(commits).get_summary()
    assert summary["total_commits"] == 3
    assert summary["total_authors"] == 2
    assert summary["total_files"] == 3
    assert summary["top_authors"][0][0] == "Alice"


def test_get_summary_empty():
    summary = Analyzer([]).get_summary()
    assert summary["total_commits"] == 0
    assert summary["avg_churn_per_commit"] == 0


def test_get_big_commits_sorted_by_churn():
    commits = [
        _commit("a", "Alice", [FileChange("f.py", 400, 200)]),
        _commit("b", "Bob",   [FileChange("g.py", 300, 400)]),
    ]
    result = Analyzer(commits).get_big_commits()
    assert result[0].total_churn >= result[1].total_churn


def test_get_hotspots_bus_factor(fixture_repo):
    from jamal.collector import Collector
    commits = Collector(fixture_repo).collect()
    hotspots = Analyzer(commits).get_hotspots()
    for h in hotspots:
        assert h.bus_factor >= 1
