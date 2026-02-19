# FSCommander

Filesystem Script Commander - Python CLI tool for file and directory operations.

## Features

- **File Operations**: copy, move, delete, rename, batch operations
- **Directory Operations**: create, tree view, sync, cleanup
- **Search & Find**: pattern matching, filtering by size/date/type
- **Automation**: scriptable workflows, batch processing

## Installation

```bash
cd FSCommander
python -m venv .venv
.venv/bin/pip install -e .
```

## Usage

```bash
# File operations
.venv/bin/fscommand cp source.txt dest.txt
.venv/bin/fscommand mv old.txt new.txt
.venv/bin/fscommand rm file.txt --recursive

# Directory operations
.venv/bin/fscommand mkdir path/to/dir
.venv/bin/fscommand tree ./src
.venv/bin/fscommand sync ./src ./backup

# Search
.venv/bin/fscommand find . --name "*.py" --size ">1MB"
.venv/bin/fscommand search "pattern" --include "*.txt"
```

## License

MIT
