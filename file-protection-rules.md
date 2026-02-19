# GitHub File Protection Rules

## Core Rules

### Rule 1: New Files → Direct Push
Creating new files that don't exist in the repo: push directly, no confirmation needed.
Log the creation to `logs/changelog.md`.

### Rule 2: Modify Existing Files → Must Confirm
Any modification to existing files requires:
1. Show diff (what changed) to user
2. Wait for user's explicit confirmation ("确认修改" / "confirm")
3. Backup old version to `backups/YYYY-MM-DD/` before pushing
4. Push the modification
5. Log to `logs/changelog.md`

### Rule 3: Delete Files → Explicit Request Only
Never delete files unless user explicitly says "delete [filename]".
Backup before deletion.

## Backup System
- Location: `backups/YYYY-MM-DD/HHMMSS_path_to_file`
- Every modified file gets a backup before changes
- Backups are never auto-deleted

## Changelog
- Location: `logs/changelog.md`
- Format: `| Time | File | Action | Message | Backup |`
- Actions: CREATE, MODIFY, DELETE

## For Claude (claude.ai / Telegram Agent)
- Before pushing to an existing file, ALWAYS call github_read first
- Show the diff to user and wait for confirmation
- Never silently modify — transparency is mandatory
- This applies to ALL environments: claude.ai, Claude Desktop, Telegram Agent

## Protected File Categories
These files require EXTRA caution (mention to user even for small changes):
- `CLAUDE.md` — project spec
- `notes/memory/claude-memory.md` — memory file
- `projects/oskris-agent/core/*.py` — agent core code
- `skills/*/SKILL.md` — skill definitions
- `.github/workflows/*.yml` — CI/CD pipelines

## Exempt from Protection (auto-push OK)
- `logs/changelog.md` — auto-updated by system
- `backups/*` — auto-created by system
- `index/timeline.json` — auto-updated index
