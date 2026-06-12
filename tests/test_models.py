from datetime import datetime

import pytest

from jamal.models import CommitInfo, FileAnalysis, FileChange, FileMetrics


def test_file_change_churn():
    fc = FileChange(filename="foo.py", added_lines=10, removed_lines=5)
    assert fc.churn == 15


def test_file_change_zero_churn():
    fc = FileChange(filename="foo.py", added_lines=0, removed_lines=0)
    assert fc.churn == 0


def test_commit_total_churn():
    files = [FileChange("a.py", 10, 5), FileChange("b.py", 20, 3)]
    commit = CommitInfo("abc", "Author", "a@b.com", datetime.now(), "msg", files)
    assert commit.total_churn == 38


def test_commit_is_big_by_churn():
    files = [FileChange("a.py", 400, 200)]
    commit = CommitInfo("abc", "Author", "a@b.com", datetime.now(), "msg", files)
    assert commit.is_big is True


def test_commit_is_not_big():
    files = [FileChange("a.py", 10, 5)]
    commit = CommitInfo("abc", "Author", "a@b.com", datetime.now(), "msg", files)
    assert commit.is_big is False


def test_commit_is_big_by_file_count():
    files = [FileChange(f"f{i}.py", 1, 1) for i in range(15)]
    commit = CommitInfo("abc", "Author", "a@b.com", datetime.now(), "msg", files)
    assert commit.is_big is True


def test_file_analysis_hotspot_score():
    fa = FileAnalysis("a.py", change_count=5, total_churn=100, avg_complexity=3.0,
                      lines_of_code=50, function_count=5, authors={"Alice"})
    assert fa.hotspot_score == pytest.approx(15.0)


def test_file_analysis_hotspot_score_no_complexity():
    fa = FileAnalysis("a.py", change_count=4, total_churn=40, avg_complexity=0.0,
                      lines_of_code=20, function_count=2, authors={"Bob"})
    assert fa.hotspot_score == pytest.approx(4.0)


def test_file_analysis_bus_factor():
    fa = FileAnalysis("a.py", 3, 30, 2.0, 20, 2, authors={"Alice", "Bob", "Carol"})
    assert fa.bus_factor == 3


def test_file_metrics_fields():
    fm = FileMetrics("x.py", cyclomatic_complexity=2.5, lines_of_code=100,
                     function_count=5, token_count=300)
    assert fm.cyclomatic_complexity == 2.5
    assert fm.token_count == 300
