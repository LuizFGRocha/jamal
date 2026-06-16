"""Collector module — traverses a git repository and extracts commit history."""

from datetime import datetime
from typing import Optional

from pydriller import Repository

from jamal.models import CommitInfo, FileChange


class Collector:
    """Collects commit history from a git repository using pydriller."""

    def __init__(
        self,
        repo_path: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        branch: Optional[str] = None,
    ) -> None:
        self.repo_path = repo_path
        self.since = since
        self.until = until
        self.branch = branch

    def _build_kwargs(self) -> dict:
        """Build keyword arguments for pydriller's Repository based on active filters."""
        kwargs: dict = {}
        if self.since:
            kwargs["since"] = self.since
        if self.until:
            kwargs["to"] = self.until
        if self.branch:
            kwargs["only_in_branch"] = self.branch
        return kwargs

    def collect(self) -> list[CommitInfo]:
        """Traverse the repository and return a list of CommitInfo objects.

        Returns an empty list if the repository is empty, invalid, or inaccessible.
        """
        kwargs = self._build_kwargs()
        commits = []
        try:
            for commit in Repository(self.repo_path, **kwargs).traverse_commits():
                files = [
                    FileChange(
                        filename=mod.new_path or mod.old_path or "",
                        added_lines=mod.added_lines,
                        removed_lines=mod.deleted_lines,
                    )
                    for mod in commit.modified_files
                ]
                commits.append(
                    CommitInfo(
                        hash=commit.hash,
                        author=commit.author.name,
                        author_email=commit.author.email,
                        date=commit.author_date,
                        message=commit.msg,
                        files_changed=files,
                    )
                )
        except Exception:
            return []
        return commits
