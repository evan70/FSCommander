# FSCommander - Process Flow

## Development Workflow

### For AI Agents

```
1. Get task from TODO.md or Task Manager
2. Implement feature
3. Create tests
4. Test manually with CLI
5. Mark task completed
6. WAIT for user approval
7. If approved -> commit & push
8. Update TODO.md for next agent
9. Exit cleanly
```

### Important Rules

- **NEVER** commit without user approval
- **NEVER** push without user approval  
- Always test before marking complete
- Always update TODO.md for continuity
- Clean exit with /quit or /exit

## Testing Commands

```bash
cd /home/evan/Desktop/ai/opencode/FSCommander

# Test CLI
.venv/bin/fscommand --version
.venv/bin/fscommand --help

# Test file operations
.venv/bin/fscommand cp src.txt dest.txt
.venv/bin/fscommand mv old.txt new.txt
.venv/bin/fscommand rm file.txt

# Test directory operations
.venv/bin/fscommand mkdir test_dir
.venv/bin/fscommand tree .
.venv/bin/fscommand ls -l

# Test search
.venv/bin/fscommand find . --name "*.py"
.venv/bin/fscommand search "pattern" --include "*.txt"
```

## Git Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "feat: description"

# Push
git push
```

## Task Manager Integration

```bash
# List tasks
tm list FSCommander

# Start task
tm start <id>

# Complete task
tm done <id>

# Add new task
tm task add FSCommander "Task title" -d "Description" -p 8 -t feature
```

---
Last updated: 2026-02-19
