import lizard

from jamal.models import FileMetrics


class Extractor:
    """Extracts structural code metrics from source files using lizard."""

    def extract(self, filepath: str) -> FileMetrics:
        raise NotImplementedError
