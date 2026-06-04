"""Formats and outputs Jamal's analysis results."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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
        table.add_column("Bus Factor", justify="right")
        table.add_column("Score", justify="right", style="bold red")
        for h in hotspots:
            score = h.hotspot_score
            style = "red" if score > 50 else ("yellow" if score > 20 else "green")
            table.add_row(
                h.filename,
                str(h.change_count),
                str(h.total_churn),
                f"{h.avg_complexity:.1f}",
                str(h.bus_factor),
                Text(f"{score:.1f}", style=style),
            )
        console.print(table)

    def print_big_commits(self, commits: list[CommitInfo]) -> None:
        """Print large commits table."""
        if not commits:
            console.print("[yellow]No large commits found.[/yellow]")
            return
        table = Table(title="[bold orange1]Large Commits[/bold orange1]", box=box.ROUNDED)
        table.add_column("Hash", style="yellow")
        table.add_column("Author")
        table.add_column("Date")
        table.add_column("Files", justify="right")
        table.add_column("Churn", justify="right", style="bold red")
        table.add_column("Message")
        for c in commits:
            table.add_row(
                c.hash[:8],
                c.author,
                c.date.strftime("%Y-%m-%d"),
                str(len(c.files_changed)),
                str(c.total_churn),
                c.message.split("\n")[0][:60],
            )
        console.print(table)
