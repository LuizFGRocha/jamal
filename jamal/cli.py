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
@click.option("--output", type=click.Choice(["json", "csv"]), default=None, help="Export format.")
@click.option("--output-file", default=None, help="Path for the exported file.")
def analyze(repo: str, output: str, output_file: str) -> None:
    """Analyze REPO for maintenance issues.

    REPO can be a local path or a remote GitHub URL.
    """
    console.print(f"[bold green]Analyzing:[/bold green] {repo}")
    with console.status("[bold]Collecting commits…[/bold]"):
        commits = Collector(repo).collect()
    if not commits:
        console.print("[red]No commits found.[/red]")
        return
    console.print(f"Found [bold]{len(commits)}[/bold] commits.\n")
    analyzer = Analyzer(commits)
    reporter = Reporter()
    summary = analyzer.get_summary()
    hotspots = analyzer.get_hotspots()
    big_commits = analyzer.get_big_commits()
    reporter.print_summary(summary)
    reporter.print_hotspots(hotspots)
    reporter.print_big_commits(big_commits)
    if output and output_file:
        if output == "json":
            reporter.export_json({"summary": summary}, output_file)
        elif output == "csv":
            reporter.export_csv(hotspots, output_file)
        console.print(f"\n[green]Exported to:[/green] {output_file}")
