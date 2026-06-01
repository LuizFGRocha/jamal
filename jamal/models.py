"""Data models for Jamal's commit and code analysis pipeline."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileChange:
    """Represents a single file modified within a commit."""

    filename: str
    added_lines: int
    removed_lines: int

    @property
    def churn(self) -> int:
        """Total lines changed (added + removed)."""
        return self.added_lines + self.removed_lines


@dataclass
class CommitInfo:
    """Encapsulates metadata and file changes for one git commit."""

    hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    files_changed: list = field(default_factory=list)

    @property
    def total_churn(self) -> int:
        """Sum of churn across all modified files."""
        return sum(f.churn for f in self.files_changed)

    @property
    def is_big(self) -> bool:
        """True when the commit exceeds configured file or churn thresholds."""
        from jamal.config import BIG_COMMIT_FILES_THRESHOLD, BIG_COMMIT_CHURN_THRESHOLD
        return (
            len(self.files_changed) > BIG_COMMIT_FILES_THRESHOLD
            or self.total_churn > BIG_COMMIT_CHURN_THRESHOLD
        )


@dataclass
class FileMetrics:
    """Static code metrics extracted from a source file."""

    filename: str
    cyclomatic_complexity: float
    lines_of_code: int
    function_count: int
    token_count: int


@dataclass
class FileAnalysis:
    """Aggregated analysis result combining change history and code metrics."""

    filename: str
    change_count: int
    total_churn: int
    avg_complexity: float
    lines_of_code: int
    function_count: int
    authors: set = field(default_factory=set)

    @property
    def bus_factor(self) -> int:
        """Number of distinct authors who touched this file."""
        return len(self.authors)

    @property
    def hotspot_score(self) -> float:
        """Composite risk score: change frequency × cyclomatic complexity."""
        return self.change_count * max(self.avg_complexity, 1.0)
