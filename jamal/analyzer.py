"""Analyzer module for identifying maintenance problem indicators."""

from collections import defaultdict
from typing import Optional

from jamal.models import CommitInfo, FileAnalysis, FileMetrics


class Analyzer:
    """Analyzes commit history to identify maintenance problem indicators."""

    def __init__(self, commits: list[CommitInfo], file_metrics: Optional[dict] = None) -> None:
        self.commits = commits
        self.file_metrics = file_metrics or {}

    def _build_file_stats(self) -> dict:
        stats: dict = defaultdict(lambda: {"changes": 0, "churn": 0, "authors": set()})
        for commit in self.commits:
            for f in commit.files_changed:
                stats[f.filename]["changes"] += 1
                stats[f.filename]["churn"] += f.churn
                stats[f.filename]["authors"].add(commit.author)
        return stats

    def _build_file_analysis(self, filename: str, stats: dict) -> FileAnalysis:
        metrics = self.file_metrics.get(filename)
        return FileAnalysis(
            filename=filename,
            change_count=stats["changes"],
            total_churn=stats["churn"],
            avg_complexity=metrics.cyclomatic_complexity if metrics else 0.0,
            lines_of_code=metrics.lines_of_code if metrics else 0,
            function_count=metrics.function_count if metrics else 0,
            authors=stats["authors"],
        )

    def get_hotspots(self, top_n: int = 10) -> list[FileAnalysis]:
        """Return files ranked by hotspot score (change frequency × complexity)."""
        stats = self._build_file_stats()
        analyses = [self._build_file_analysis(fn, s) for fn, s in stats.items()]
        return sorted(analyses, key=lambda x: x.hotspot_score, reverse=True)[:top_n]
