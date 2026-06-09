"""Formats and outputs Jamal's analysis results."""

import csv
import json
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
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
        if summary.get("top_authors"):
            lines.append("\n[bold]Top contributors:[/bold]")
            for name, count in summary["top_authors"]:
                lines.append(f"  {name}: {count} commits")
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

    def print_coupled_files(self, pairs: list[tuple]) -> None:
        """Print frequently co-modified file pairs."""
        if not pairs:
            console.print("[yellow]No strongly coupled files found.[/yellow]")
            return
        table = Table(title="[bold blue]Coupled Files[/bold blue]", box=box.ROUNDED)
        table.add_column("File A", style="cyan")
        table.add_column("File B", style="cyan")
        table.add_column("Co-changes", justify="right", style="bold blue")
        for a, b, count in pairs:
            table.add_row(a, b, str(count))
        console.print(table)

    def print_growing_files(self, files: list[FileAnalysis]) -> None:
        """Print files with continuously growing churn."""
        if not files:
            console.print("[yellow]No growing files found.[/yellow]")
            return
        table = Table(title="[bold magenta]Continuously Growing Files[/bold magenta]", box=box.ROUNDED)
        table.add_column("File", style="cyan")
        table.add_column("Changes", justify="right")
        table.add_column("Total Churn", justify="right", style="bold magenta")
        for f in files:
            table.add_row(f.filename, str(f.change_count), str(f.total_churn))
        console.print(table)

    def export_json(self, data: dict, filepath: str) -> None:
        """Export analysis results to a JSON file."""
        Path(filepath).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def export_csv(self, hotspots: list[FileAnalysis], filepath: str) -> None:
        """Export hotspot data to a CSV file with UTF-8 encoding."""
        fieldnames = ["filename", "change_count", "total_churn", "avg_complexity", "bus_factor", "hotspot_score"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for h in hotspots:
                writer.writerow({
                    "filename": h.filename,
                    "change_count": h.change_count,
                    "total_churn": h.total_churn,
                    "avg_complexity": h.avg_complexity,
                    "bus_factor": h.bus_factor,
                    "hotspot_score": round(h.hotspot_score, 2),
                })
