#!/usr/bin/env python3
"""Example workflow - Backup project files using fscommand modules."""

from pathlib import Path
from datetime import datetime

from fscommand import dir_ops, file_ops, search


def backup_project(source_dir: str, backup_dir: str, keep_days: int = 7):
    """Backup project directory with rotation.
    
    Args:
        source_dir: Source project directory
        backup_dir: Base backup directory
        keep_days: Number of days to keep backups
    """
    source = Path(source_dir)
    backup_base = Path(backup_dir)
    
    if not source.exists():
        print(f"Error: Source directory does not exist: {source}")
        return
    
    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dest = backup_base / f"backup_{timestamp}"
    
    print(f"📦 Creating backup: {backup_dest}")
    result = dir_ops.sync(str(source), str(backup_dest), dry_run=False)
    
    print(f"  ✓ Files copied: {result['copied']}")
    print(f"  ✓ Files skipped: {result['skipped']}")
    
    # Cleanup old backups
    print(f"\n🧹 Cleaning up backups older than {keep_days} days...")
    cleanup_old_backups(backup_base, keep_days)


def cleanup_old_backups(backup_base: Path, keep_days: int):
    """Remove backups older than specified days."""
    if not backup_base.exists():
        return
    
    now = datetime.now()
    
    for backup_dir in backup_base.glob("backup_*"):
        if not backup_dir.is_dir():
            continue
        
        # Extract timestamp from directory name
        try:
            timestamp_str = backup_dir.name.replace("backup_", "")
            backup_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            age_days = (now - backup_date).days
            
            if age_days > keep_days:
                print(f"  Removing old backup: {backup_dir.name} ({age_days} days old)")
                file_ops.remove(str(backup_dir), recursive=True)
        except ValueError:
            continue


def find_large_files(path: str, min_size: str = "10MB"):
    """Find large files in directory."""
    print(f"🔍 Finding files larger than {min_size} in {path}")
    
    results = search.find(path, size=f">{min_size}")
    
    if not results:
        print("  No large files found")
        return
    
    for item in results:
        print(f"  {item['path']}")
    
    print(f"\n  Found {len(results)} large files")


def organize_downloads(downloads_dir: str):
    """Organize downloads directory by file type."""
    downloads = Path(downloads_dir)
    
    if not downloads.exists():
        print(f"Downloads directory not found: {downloads}")
        return
    
    # Define category mappings
    categories = {
        "images": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.svg"],
        "documents": ["*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.ppt", "*.pptx"],
        "archives": ["*.zip", "*.tar", "*.gz", "*.rar", "*.7z"],
        "code": ["*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.h", "*.rs"],
    }
    
    for category, patterns in categories.items():
        category_dir = downloads / category
        category_dir.mkdir(exist_ok=True)
        
        for pattern in patterns:
            for file_path in downloads.glob(pattern):
                if file_path.is_file():
                    dest = category_dir / file_path.name
                    file_ops.move_file(str(file_path), str(dest), overwrite=True)
                    print(f"  Moved: {file_path.name} → {category}/")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_workflow.py <command> [args]")
        print("\nCommands:")
        print("  backup <source> <dest>     - Backup project directory")
        print("  large <path>               - Find large files")
        print("  organize <downloads_dir>   - Organize downloads")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "backup":
        if len(sys.argv) < 4:
            print("Usage: python example_workflow.py backup <source> <dest>")
            sys.exit(1)
        backup_project(sys.argv[2], sys.argv[3])
    
    elif command == "large":
        if len(sys.argv) < 3:
            print("Usage: python example_workflow.py large <path>")
            sys.exit(1)
        find_large_files(sys.argv[2])
    
    elif command == "organize":
        if len(sys.argv) < 3:
            print("Usage: python example_workflow.py organize <downloads_dir>")
            sys.exit(1)
        organize_downloads(sys.argv[2])
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
