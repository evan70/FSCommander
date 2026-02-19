"""FSCommand CLI - Main entry point."""

import typer
from rich.console import Console
from rich.table import Table

from fscommand import __version__
from fscommand import file_ops, dir_ops, search

app = typer.Typer(
    name="fscommand",
    help="Filesystem Script Commander - CLI tool for file and directory operations",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold blue]fscommand[/bold blue] v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", callback=version_callback, help="Show version"
    ),
):
    pass


# ─────────────────────────────────────────────────────────────────────────────
# File Operations
# ─────────────────────────────────────────────────────────────────────────────

@app.command("cp")
def copy_file(
    source: str = typer.Argument(..., help="Source file path"),
    dest: str = typer.Argument(..., help="Destination file path"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite destination"),
):
    """Copy a file from source to destination."""
    success = file_ops.copy_file(source, dest, overwrite=force)
    if success:
        console.print(f"[green]✓[/green] Copied: {source} → {dest}")
    else:
        console.print(f"[red]✗[/red] Failed to copy: {source} → {dest}")
        raise typer.Exit(1)


@app.command("mv")
def move_file(
    source: str = typer.Argument(..., help="Source file path"),
    dest: str = typer.Argument(..., help="Destination file path"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite destination"),
):
    """Move or rename a file."""
    success = file_ops.move_file(source, dest, overwrite=force)
    if success:
        console.print(f"[green]✓[/green] Moved: {source} → {dest}")
    else:
        console.print(f"[red]✗[/red] Failed to move: {source} → {dest}")
        raise typer.Exit(1)


@app.command("rm")
def remove_file(
    path: str = typer.Argument(..., help="File or directory path"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Remove directories recursively"),
    force: bool = typer.Option(False, "--force", "-f", help="Ignore non-existent paths"),
):
    """Remove a file or directory."""
    success = file_ops.remove(path, recursive=recursive, force=force)
    if success:
        console.print(f"[green]✓[/green] Removed: {path}")
    else:
        console.print(f"[red]✗[/red] Failed to remove: {path}")
        raise typer.Exit(1)


@app.command("rename")
def rename_file(
    path: str = typer.Argument(..., help="File path"),
    new_name: str = typer.Argument(..., help="New file name"),
):
    """Rename a file."""
    success = file_ops.rename(path, new_name)
    if success:
        console.print(f"[green]✓[/green] Renamed: {path} → {new_name}")
    else:
        console.print(f"[red]✗[/red] Failed to rename: {path}")
        raise typer.Exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Directory Operations
# ─────────────────────────────────────────────────────────────────────────────

@app.command("mkdir")
def make_directory(
    path: str = typer.Argument(..., help="Directory path to create"),
    parents: bool = typer.Option(False, "--parents", "-p", help="Create parent directories"),
):
    """Create a new directory."""
    success = dir_ops.create_directory(path, parents=parents)
    if success:
        console.print(f"[green]✓[/green] Created directory: {path}")
    else:
        console.print(f"[red]✗[/red] Failed to create: {path}")
        raise typer.Exit(1)


@app.command("tree")
def tree_view(
    path: str = typer.Argument(".", help="Root directory path"),
    max_depth: int = typer.Option(3, "--depth", "-d", help="Maximum depth to display"),
):
    """Display directory tree structure."""
    tree = dir_ops.tree(path, max_depth=max_depth)
    console.print(tree)


@app.command("sync")
def sync_dirs(
    source: str = typer.Argument(..., help="Source directory"),
    dest: str = typer.Argument(..., help="Destination directory"),
    delete: bool = typer.Option(False, "--delete", help="Delete extra files in destination"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show what would be done"),
):
    """Synchronize two directories."""
    result = dir_ops.sync(source, dest, delete=delete, dry_run=dry_run)
    
    if dry_run:
        console.print("[yellow]Dry run - no changes made[/yellow]")
    
    console.print(f"\n[green]✓[/green] Synced: {source} → {dest}")
    console.print(f"  Files copied: {result['copied']}")
    console.print(f"  Files skipped: {result['skipped']}")
    if delete:
        console.print(f"  Files deleted: {result['deleted']}")


@app.command("ls")
def list_files(
    path: str = typer.Argument(".", help="Directory to list"),
    all_files: bool = typer.Option(False, "--all", "-a", help="Include hidden files"),
    long_format: bool = typer.Option(False, "--long", "-l", help="Detailed listing"),
):
    """List directory contents."""
    files = dir_ops.list_directory(path, show_hidden=all_files, detailed=long_format)
    
    if long_format:
        table = Table(title=f"Contents of {path}")
        table.add_column("Name", style="cyan")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Modified", style="magenta")
        
        for f in files:
            table.add_row(f["name"], f.get("size", "-"), f.get("modified", "-"))
        console.print(table)
    else:
        for f in files:
            name = f["name"] if isinstance(f, dict) else f
            console.print(name)


# ─────────────────────────────────────────────────────────────────────────────
# Search & Find
# ─────────────────────────────────────────────────────────────────────────────

@app.command("find")
def find_files(
    path: str = typer.Argument(".", help="Search root path"),
    name: str = typer.Option(None, "--name", "-n", help="Pattern for file name (e.g., *.py)"),
    size: str = typer.Option(None, "--size", "-s", help="Filter by size (e.g., >1MB, <100KB)"),
    file_type: str = typer.Option(None, "--type", "-t", help="Filter by type (file, dir, link)"),
):
    """Find files and directories matching criteria."""
    results = search.find(path, name=name, size=size, file_type=file_type)
    
    if not results:
        console.print("[yellow]No files found[/yellow]")
        return
    
    for item in results:
        console.print(item["path"])
    
    console.print(f"\n[bold]Found {len(results)} items[/bold]")


@app.command("search")
def search_content(
    pattern: str = typer.Argument(..., help="Search pattern (regex supported)"),
    path: str = typer.Argument(".", help="Search root path"),
    include: str = typer.Option("*.txt", "--include", help="Glob pattern for files to include"),
    exclude: str = typer.Option(None, "--exclude", help="Glob pattern for files to exclude"),
):
    """Search for text pattern in files."""
    results = search.search_text(pattern, path, include=include, exclude=exclude)
    
    if not results:
        console.print("[yellow]No matches found[/yellow]")
        return
    
    for match in results:
        console.print(f"[cyan]{match['file']}[/cyan]:{match['line']}")
        console.print(f"  {match['content'].strip()}")
    
    console.print(f"\n[bold]Found {len(results)} matches[/bold]")


def run():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    run()
