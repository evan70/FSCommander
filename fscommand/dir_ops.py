"""Directory operations module - create, tree, sync, list."""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from rich.tree import Tree


def create_directory(path: str, parents: bool = False) -> bool:
    """Create a new directory.
    
    Args:
        path: Directory path to create
        parents: If True, create parent directories as needed
        
    Returns:
        True if successful, False otherwise
    """
    p = Path(path)
    
    try:
        p.mkdir(parents=parents, exist_ok=parents)
        return True
    except (OSError, IOError):
        return False


def tree(path: str, max_depth: int = 3) -> Tree:
    """Generate a directory tree visualization.
    
    Args:
        path: Root directory path
        max_depth: Maximum depth to traverse
        
    Returns:
        Rich Tree object
    """
    root_path = Path(path).resolve()
    tree = Tree(f"📁 {root_path}")
    
    def _add_to_tree(current_path: Path, current_tree: Tree, depth: int):
        if depth > max_depth:
            return
        
        try:
            entries = sorted(current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return
        
        for entry in entries:
            if entry.name.startswith("."):
                continue
            
            if entry.is_dir():
                branch = current_tree.add(f"📁 {entry.name}")
                _add_to_tree(entry, branch, depth + 1)
            else:
                current_tree.add(f"📄 {entry.name}")
    
    _add_to_tree(root_path, tree, 1)
    return tree


def list_directory(path: str, show_hidden: bool = False, detailed: bool = False) -> List[Dict[str, Any]]:
    """List directory contents.
    
    Args:
        path: Directory path
        show_hidden: If True, include hidden files (starting with .)
        detailed: If True, include size and modification time
        
    Returns:
        List of file info dictionaries
    """
    p = Path(path)
    
    if not p.exists() or not p.is_dir():
        return []
    
    results = []
    
    try:
        entries = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        return []
    
    for entry in entries:
        if not show_hidden and entry.name.startswith("."):
            continue
        
        info: Dict[str, Any] = {"name": entry.name}
        
        if detailed:
            try:
                stat = entry.stat()
                info["size"] = _format_size(stat.st_size)
                info["modified"] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                info["type"] = "dir" if entry.is_dir() else "file"
            except (OSError, IOError):
                info["size"] = "-"
                info["modified"] = "-"
        
        results.append(info)
    
    return results


def sync(source: str, dest: str, delete: bool = False, dry_run: bool = False) -> Dict[str, int]:
    """Synchronize two directories.
    
    Args:
        source: Source directory path
        dest: Destination directory path
        delete: If True, delete files in dest that don't exist in source
        dry_run: If True, don't make any changes
        
    Returns:
        Dictionary with counts of copied, skipped, and deleted files
    """
    src = Path(source).resolve()
    dst = Path(dest).resolve()
    
    result = {"copied": 0, "skipped": 0, "deleted": 0}
    
    if not src.exists() or not src.is_dir():
        return result
    
    dst.mkdir(parents=True, exist_ok=True)
    
    # Copy files from source to dest
    for src_file in src.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(src)
            dst_file = dst / rel_path
            
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            if dst_file.exists():
                result["skipped"] += 1
            else:
                if not dry_run:
                    shutil.copy2(src_file, dst_file)
                result["copied"] += 1
    
    # Delete extra files in dest
    if delete:
        for dst_file in dst.rglob("*"):
            if dst_file.is_file():
                rel_path = dst_file.relative_to(dst)
                src_file = src / rel_path
                
                if not src_file.exists():
                    if not dry_run:
                        dst_file.unlink()
                    result["deleted"] += 1
    
    return result


def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}PB"
