"""Analyzer module for identifying maintenance problem indicators."""

from jamal.models import CommitInfo, FileAnalysis, FileMetrics


class Analyzer:
    """Analyzes commit history to identify maintenance problem indicators."""

    def __init__(self, commits: list[CommitInfo], file_metrics: dict | None = None) -> None:
        self.commits = commits
        self.file_metrics = file_metrics or {}
