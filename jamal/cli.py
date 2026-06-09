"""CLI entry point for Jamal."""

import click


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Jamal — Repository maintenance issue analyzer."""
