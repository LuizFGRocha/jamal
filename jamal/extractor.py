import lizard

from jamal.models import FileMetrics


class Extractor:
    """Extracts structural code metrics from source files using lizard."""

    def extract(self, filepath: str) -> FileMetrics:
        """Analyze a file and return its cyclomatic complexity."""
        analysis = lizard.analyze_file(filepath)
        functions = analysis.function_list if analysis else []
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
            token_count=0,
        )
