"""Formats and outputs Jamal's analysis results."""

from rich.console import Console

console = Console()


class Reporter:
    """Formats and outputs analysis results to terminal, JSON, or CSV."""

    def print_summary(self, summary: dict) -> None:
        raise NotImplementedError
