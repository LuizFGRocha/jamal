from jamal.models import CommitInfo, FileChange


class Collector:
    """Collects commit history from a git repository."""

    def __init__(self, repo_path: str) -> None:
        self.repo_path = repo_path

    def collect(self) -> list[CommitInfo]:
        raise NotImplementedError
