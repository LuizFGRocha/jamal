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
