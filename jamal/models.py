from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileChange:
    filename: str
    added_lines: int
    removed_lines: int

    @property
    def churn(self) -> int:
        return self.added_lines + self.removed_lines


@dataclass
class CommitInfo:
    hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    files_changed: list = field(default_factory=list)

    @property
    def total_churn(self) -> int:
        return sum(f.churn for f in self.files_changed)

    @property
    def is_big(self) -> bool:
        from jamal.config import BIG_COMMIT_FILES_THRESHOLD, BIG_COMMIT_CHURN_THRESHOLD
        return (
            len(self.files_changed) > BIG_COMMIT_FILES_THRESHOLD
            or self.total_churn > BIG_COMMIT_CHURN_THRESHOLD
        )


@dataclass
class FileMetrics:
    filename: str
    cyclomatic_complexity: float
    lines_of_code: int
    function_count: int
    token_count: int


@dataclass
class FileAnalysis:
    filename: str
    change_count: int
    total_churn: int
    avg_complexity: float
    lines_of_code: int
    function_count: int
    authors: set = field(default_factory=set)

    @property
    def bus_factor(self) -> int:
        return len(self.authors)

    @property
    def hotspot_score(self) -> float:
        return self.change_count * max(self.avg_complexity, 1.0)
