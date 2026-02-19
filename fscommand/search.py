"""Search and find module - pattern matching, filtering, text search."""

import re
import fnmatch
from pathlib import Path
from typing import List, Dict, Any, Optional


def find(
    path: str,
    name: Optional[str] = None,
    size: Optional[str] = None,
    file_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Find files and directories matching criteria.
    
    Args:
        path: Search root path
        name: Glob pattern for file name (e.g., *.py)
        size: Filter by size (e.g., >1MB, <100KB)
        file_type: Filter by type (file, dir, link)
        
    Returns:
        List of matching file info dictionaries
    """
    root = Path(path)
    
    if not root.exists():
        return []
    
    results = []
    size_filter = _parse_size_filter(size) if size else None
    
    for item in root.rglob("*"):
        # Filter by name pattern
        if name and not fnmatch.fnmatch(item.name, name):
            continue
        
        # Filter by type
        if file_type:
            if file_type == "file" and not item.is_file():
                continue
            elif file_type == "dir" and not item.is_dir():
                continue
            elif file_type == "link" and not item.is_symlink():
                continue
        
        # Filter by size
        if size_filter and item.is_file():
            try:
                file_size = item.stat().st_size
                if not _matches_size(file_size, size_filter):
                    continue
            except (OSError, IOError):
                continue
        
        results.append({
            "path": str(item),
            "name": item.name,
            "type": "dir" if item.is_dir() else "file",
        })
    
    return results


def search_text(
    pattern: str,
    path: str,
    include: str = "*.txt",
    exclude: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search for text pattern in files.
    
    Args:
        pattern: Search pattern (regex supported)
        path: Search root path
        include: Glob pattern for files to include
        exclude: Glob pattern for files to exclude
        
    Returns:
        List of match dictionaries with file, line number, and content
    """
    root = Path(path)
    
    if not root.exists():
        return []
    
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        # If regex is invalid, treat as literal
        regex = re.compile(re.escape(pattern), re.IGNORECASE)
    
    results = []
    
    for file_path in root.rglob(include):
        if not file_path.is_file():
            continue
        
        if exclude and fnmatch.fnmatch(file_path.name, exclude):
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    if regex.search(line):
                        results.append({
                            "file": str(file_path),
                            "line": line_num,
                            "content": line,
                        })
        except (OSError, IOError, PermissionError):
            continue
    
    return results


def _parse_size_filter(size_str: str) -> tuple:
    """Parse size filter string like '>1MB' or '<100KB'.
    
    Returns:
        Tuple of (operator, size_in_bytes)
    """
    size_str = size_str.strip().upper()
    
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 ** 2,
        "GB": 1024 ** 3,
        "TB": 1024 ** 4,
    }
    
    # Extract operator and value
    if size_str.startswith(">="):
        op = ">="
        val_str = size_str[2:]
    elif size_str.startswith("<="):
        op = "<="
        val_str = size_str[2:]
    elif size_str.startswith(">"):
        op = ">"
        val_str = size_str[1:]
    elif size_str.startswith("<"):
        op = "<"
        val_str = size_str[1:]
    else:
        op = ">"
        val_str = size_str
    
    # Extract number and unit
    for unit, multiplier in sorted(units.items(), key=lambda x: -len(x[0])):
        if val_str.endswith(unit):
            try:
                value = float(val_str[:-len(unit)])
                return (op, int(value * multiplier))
            except ValueError:
                break
    
    # No unit, assume bytes
    try:
        return (op, int(val_str))
    except ValueError:
        return (">", 0)


def _matches_size(file_size: int, filter_tuple: tuple) -> bool:
    """Check if file size matches the filter criteria."""
    op, threshold = filter_tuple
    
    if op == ">":
        return file_size > threshold
    elif op == ">=":
        return file_size >= threshold
    elif op == "<":
        return file_size < threshold
    elif op == "<=":
        return file_size <= threshold
    
    return False
