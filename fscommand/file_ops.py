"""File operations module - copy, move, delete, rename."""

import shutil
from pathlib import Path


def copy_file(source: str, dest: str, overwrite: bool = False) -> bool:
    """Copy a file from source to destination.
    
    Args:
        source: Source file path
        dest: Destination file path
        overwrite: If True, overwrite existing destination
        
    Returns:
        True if successful, False otherwise
    """
    src = Path(source)
    dst = Path(dest)
    
    if not src.exists():
        return False
    
    if dst.exists() and not overwrite:
        return False
    
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except (OSError, IOError):
        return False


def move_file(source: str, dest: str, overwrite: bool = False) -> bool:
    """Move or rename a file.
    
    Args:
        source: Source file path
        dest: Destination file path
        overwrite: If True, overwrite existing destination
        
    Returns:
        True if successful, False otherwise
    """
    src = Path(source)
    dst = Path(dest)
    
    if not src.exists():
        return False
    
    if dst.exists() and not overwrite:
        return False
    
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src, dst)
        return True
    except (OSError, IOError):
        return False


def remove(path: str, recursive: bool = False, force: bool = False) -> bool:
    """Remove a file or directory.
    
    Args:
        path: Path to file or directory
        recursive: If True, remove directories recursively
        force: If True, ignore non-existent paths
        
    Returns:
        True if successful, False otherwise
    """
    p = Path(path)
    
    if not p.exists():
        return force
    
    try:
        if p.is_dir():
            if recursive:
                shutil.rmtree(p)
            else:
                p.rmdir()
        else:
            p.unlink()
        return True
    except (OSError, IOError):
        return False


def rename(path: str, new_name: str) -> bool:
    """Rename a file.
    
    Args:
        path: Current file path
        new_name: New file name
        
    Returns:
        True if successful, False otherwise
    """
    src = Path(path)
    
    if not src.exists():
        return False
    
    dst = src.parent / new_name
    
    try:
        src.rename(dst)
        return True
    except (OSError, IOError):
        return False
