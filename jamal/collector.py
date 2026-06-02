from pydriller import Repository

from jamal.models import CommitInfo, FileChange


class Collector:
    """Collects commit history from a git repository using pydriller."""

    def __init__(self, repo_path: str) -> None:
        self.repo_path = repo_path

    def collect(self) -> list[CommitInfo]:
        commits = []
        for commit in Repository(self.repo_path).traverse_commits():
            commits.append(
                CommitInfo(
                    hash=commit.hash,
                    author=commit.author.name,
                    author_email=commit.author.email,
                    date=commit.author_date,
                    message=commit.msg,
                    files_changed=[],
                )
            )
        return commits
