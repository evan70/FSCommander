# TODO - FSCommander

## Completed

**Initial Release - 2026-02-19**
- Project structure created
- CLI with typer + rich
- File operations: cp, mv, rm, rename
- Directory operations: mkdir, tree, ls, sync
- Search/find with filters
- Text search with regex
- Example workflows
- Git remote: https://github.com/evan70/FSCommander

## Next Tasks

### Priority 10 - Choose ONE:

**Option A: Add more file commands**
- touch - Create empty file or update timestamp
- chmod - Change file permissions
- chown - Change file owner
- ln - Create symbolic/hard links

**Option B: Add file content operations**
- cat - Display file content with syntax highlighting
- head/tail - Show first/last N lines
- wc - Word, line, character count

**Option C: Add batch operations**
- Batch rename with regex patterns
- Batch copy/move with transformations
- Parallel processing for large operations

### Priority 8:

**Enhance existing commands**
- tree - Add file size, icons, filtering
- ls - Add sorting, filtering, colors
- sync - Add conflict resolution, dry-run improvements

**Add unit tests**
- Test file_ops.py functions
- Test dir_ops.py functions
- Test search.py functions
- CLI command tests with typer.testing

### Priority 7:

**Documentation**
- Command reference with examples
- Tutorial for common workflows
- API documentation for modules

**Configuration**
- Config file for defaults
- Aliases for common commands
- Color theme customization

## Workflow Reminder

1. Pick task from list above
2. Implement feature
3. Create tests
4. Test manually
5. Mark complete
6. WAIT for user approval
7. If approved -> commit and push
8. Update this TODO
9. Exit cleanly

---
Last updated: 2026-02-19
Git commit: d6b436e
Next: Choose from Priority 10 tasks
