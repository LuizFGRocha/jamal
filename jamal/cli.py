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
def analyze(repo: str) -> None:
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
    reporter.print_summary(analyzer.get_summary())
    reporter.print_hotspots(analyzer.get_hotspots())
    reporter.print_big_commits(analyzer.get_big_commits())
