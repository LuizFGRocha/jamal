"""CLI entry point for Jamal."""

from datetime import datetime

import click
from rich.console import Console

from jamal.analyzer import Analyzer
from jamal.collector import Collector
from jamal.reporter import Reporter

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Jamal — Repository maintenance issue analyzer."""


@cli.command()
@click.argument("repo")
@click.option("--top", default=10, show_default=True, help="Number of results per section.")
@click.option("--since", default=None, help="Start date filter (YYYY-MM-DD).")
@click.option("--until", default=None, help="End date filter (YYYY-MM-DD).")
@click.option("--branch", default=None, help="Analyze only this branch.")
@click.option("--output", type=click.Choice(["json", "csv"]), default=None, help="Export format.")
@click.option("--output-file", default=None, help="Path for the exported file.")
def analyze(
    repo: str,
    top: int,
    since: str,
    until: str,
    branch: str,
    output: str,
    output_file: str,
) -> None:
    """Analyze REPO for maintenance issues.

    REPO can be a local path or a remote GitHub URL.
    """
    since_dt = datetime.fromisoformat(since) if since else None
    until_dt = datetime.fromisoformat(until) if until else None

    console.print(f"[bold green]Analyzing:[/bold green] {repo}")
    with console.status("[bold]Collecting commits…[/bold]"):
        commits = Collector(repo, since=since_dt, until=until_dt, branch=branch).collect()

    if not commits:
        console.print("[red]No commits found. Check the path or filters.[/red]")
        return

    console.print(f"Found [bold]{len(commits)}[/bold] commits.\n")

    analyzer = Analyzer(commits)
    reporter = Reporter()

    summary = analyzer.get_summary()
    hotspots = analyzer.get_hotspots(top_n=top)
    big_commits = analyzer.get_big_commits(top_n=top)
    growing = analyzer.get_growing_files(top_n=top)
    coupled = analyzer.get_coupled_files(top_n=top)

    reporter.print_summary(summary)
    reporter.print_hotspots(hotspots)
    reporter.print_big_commits(big_commits)
    reporter.print_growing_files(growing)
    reporter.print_coupled_files(coupled)

    if output and output_file:
        if output == "json":
            data = {
                "summary": summary,
                "hotspots": [
                    {
                        "filename": h.filename,
                        "change_count": h.change_count,
                        "total_churn": h.total_churn,
                        "avg_complexity": h.avg_complexity,
                        "bus_factor": h.bus_factor,
                        "hotspot_score": h.hotspot_score,
                    }
                    for h in hotspots
                ],
                "big_commits": [
                    {
                        "hash": c.hash[:8],
                        "author": c.author,
                        "date": str(c.date.date()),
                        "files": len(c.files_changed),
                        "churn": c.total_churn,
                        "message": c.message.split("\n")[0],
                    }
                    for c in big_commits
                ],
            }
            reporter.export_json(data, output_file)
        elif output == "csv":
            reporter.export_csv(hotspots, output_file)
        console.print(f"\n[green]Results exported to:[/green] {output_file}")
