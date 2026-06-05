import lizard

from jamal.models import FileMetrics


class Extractor:
    """Extracts structural code metrics from source files using lizard."""

    def extract(self, filepath: str) -> FileMetrics:
        """Analyze a file and return its structural metrics."""
        try:
            analysis = lizard.analyze_file(filepath)
            if not analysis:
                return self._empty_metrics(filepath)
            functions = analysis.function_list
            avg_complexity = (
                sum(f.cyclomatic_complexity for f in functions) / len(functions)
                if functions
                else 0.0
            )
            return FileMetrics(
                filename=filepath,
                cyclomatic_complexity=round(avg_complexity, 2),
                lines_of_code=analysis.nloc or 0,
                function_count=len(functions),
                token_count=analysis.token_count or 0,
            )
        except Exception:
            return self._empty_metrics(filepath)

    def _empty_metrics(self, filepath: str) -> FileMetrics:
        """Return zero-value metrics for files that cannot be parsed."""
        return FileMetrics(
            filename=filepath,
            cyclomatic_complexity=0.0,
            lines_of_code=0,
            function_count=0,
            token_count=0,
        )
