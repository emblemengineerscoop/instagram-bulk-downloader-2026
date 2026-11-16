"""CLI entry-point: ``python -m ig_downloader ...``."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .client import Client

console = Console()
load_dotenv()


@click.command()
@click.option("--user", "username", required=True, help="Target Instagram username.")
@click.option("--out",  "out_dir",  default="./downloads", type=click.Path())
@click.option("--kind", "kinds",    default="post,reel,story",
              help="Comma-separated: post,reel,story,highlight,igtv.")
@click.option("--since", help="Only items newer than this (e.g. 30d, 2026-01-01).")
@click.option("--metadata", type=click.Path(), help="Write JSON metadata to this file.")
def main(username: str, out_dir: str, kinds: str, since: str | None, metadata: str | None):
    """Bulk-download Instagram media in original quality."""
    sess = os.environ.get("IG_SESSION")
    if not sess:
        console.print("[red]ERROR[/]: set IG_SESSION in .env or environment.")
        sys.exit(2)

    cli = Client(session_cookie=sess, proxy=os.environ.get("IG_PROXY"))
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as pg:
        tid = pg.add_task(f"Fetching @{username}...", total=None)
        count = 0
        for it in cli.iter_profile(username, kinds=tuple(kinds.split(","))):
            cli.download(it, directory=out_dir)
            count += 1
            pg.update(tid, description=f"Downloaded {count} items")
    console.print(f"[green]Done.[/] {count} items saved to {Path(out_dir).resolve()}")


if __name__ == "__main__":
    main()
