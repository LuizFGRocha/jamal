"""Analyzer module for identifying maintenance problem indicators."""

from collections import defaultdict
from itertools import combinations
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

    def get_big_commits(self, top_n: int = 10) -> list[CommitInfo]:
        """Return commits that are suspiciously large."""
        big = [c for c in self.commits if c.is_big]
        return sorted(big, key=lambda x: x.total_churn, reverse=True)[:top_n]

    def get_growing_files(self, top_n: int = 10) -> list[FileAnalysis]:
        """Return files whose churn is trending upward over time."""
        from jamal.config import GROWTH_THRESHOLD, MIN_CHANGES_FOR_GROWTH
        churn_over_time: dict = defaultdict(list)
        for commit in sorted(self.commits, key=lambda c: c.date):
            for f in commit.files_changed:
                churn_over_time[f.filename].append(f.churn)

        growing = []
        stats = self._build_file_stats()
        for filename, churns in churn_over_time.items():
            if len(churns) < MIN_CHANGES_FOR_GROWTH:
                continue
            mid = len(churns) // 2
            first_avg = sum(churns[:mid]) / mid if mid else 0
            second_avg = sum(churns[mid:]) / len(churns[mid:])
            if first_avg == 0 or second_avg > first_avg * GROWTH_THRESHOLD:
                if filename in stats:
                    growing.append(self._build_file_analysis(filename, stats[filename]))

        return sorted(growing, key=lambda x: x.total_churn, reverse=True)[:top_n]

    def get_coupled_files(self, top_n: int = 10) -> list[tuple[str, str, int]]:
        """Return pairs of files that are frequently changed together."""
        from jamal.config import COUPLING_MIN_COMMITS
        co_changes: dict = defaultdict(int)
        for commit in self.commits:
            filenames = [f.filename for f in commit.files_changed]
            for a, b in combinations(sorted(filenames), 2):
                co_changes[(a, b)] += 1
        pairs = [
            (a, b, count)
            for (a, b), count in co_changes.items()
            if count >= COUPLING_MIN_COMMITS
        ]
        return sorted(pairs, key=lambda x: x[2], reverse=True)[:top_n]

    def get_churn_ratio(self) -> list[tuple[str, float]]:
        """Return files sorted by churn-to-change-count ratio (avg churn per touch)."""
        stats = self._build_file_stats()
        ratios = [
            (fn, s["churn"] / s["changes"])
            for fn, s in stats.items()
            if s["changes"] > 0
        ]
        return sorted(ratios, key=lambda x: x[1], reverse=True)

    def get_summary(self) -> dict:
        """Return a high-level summary of the repository."""
        author_counts: dict = defaultdict(int)
        total_churn = 0
        all_files: set = set()
        for commit in self.commits:
            author_counts[commit.author] += 1
            total_churn += commit.total_churn
            for f in commit.files_changed:
                all_files.add(f.filename)
        n = len(self.commits)
        return {
            "total_commits": n,
            "total_files": len(all_files),
            "total_authors": len(author_counts),
            "avg_churn_per_commit": round(total_churn / n, 1) if n else 0,
            "top_authors": sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5],
        }
