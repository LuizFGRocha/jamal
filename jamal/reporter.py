"""Formats and outputs Jamal's analysis results."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from jamal.models import CommitInfo, FileAnalysis

console = Console()


class Reporter:
    """Formats and outputs analysis results to terminal, JSON, or CSV."""

    def print_summary(self, summary: dict) -> None:
        """Print a summary statistics panel."""
        lines = [
            f"[bold]Total commits:[/bold]       {summary['total_commits']}",
            f"[bold]Unique files:[/bold]         {summary['total_files']}",
            f"[bold]Authors:[/bold]              {summary['total_authors']}",
            f"[bold]Avg churn/commit:[/bold]     {summary['avg_churn_per_commit']}",
        ]
        console.print(Panel("\n".join(lines), title="[bold cyan]Repository Summary[/bold cyan]", expand=False))

    def print_hotspots(self, hotspots: list[FileAnalysis]) -> None:
        """Print hotspots ranked by hotspot score."""
        if not hotspots:
            console.print("[yellow]No hotspots found.[/yellow]")
            return
        table = Table(title="[bold red]Top Hotspots[/bold red]", box=box.ROUNDED)
        table.add_column("File", style="cyan", no_wrap=False)
        table.add_column("Changes", justify="right")
        table.add_column("Churn", justify="right")
        table.add_column("Avg CC", justify="right")
        table.add_column("Score", justify="right", style="bold red")
        for h in hotspots:
            table.add_row(
                h.filename,
                str(h.change_count),
                str(h.total_churn),
                f"{h.avg_complexity:.1f}",
                f"{h.hotspot_score:.1f}",
            )
        console.print(table)
