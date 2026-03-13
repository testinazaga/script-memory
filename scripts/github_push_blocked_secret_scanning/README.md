# GitHub Push Blocked by Secret Scanning

## Problem

GitHub push protection rejects a push with:

```
remote: - GITHUB PUSH PROTECTION
remote:   Push cannot contain secrets
remote:   — GitHub Personal Access Token ——
remote:     locations:
remote:       - commit: <sha>  path: .env:1
```

This happens when a `.env` file (or any file containing a secret) was committed and
the `.gitignore` did not cover its path.

## Environment

- OS: Ubuntu (any Linux)
- Tool: git, GitHub

## Why This Works

GitHub scans every commit for known secret patterns (PATs, API keys, etc.) before
allowing the push. Amending the commit removes the secret from git history so the
push is no longer blocked. `--force-with-lease` is safer than `--force` because it
refuses to overwrite if someone else pushed in the meantime.

## Fix

```bash
# 1. Add the file to .gitignore so it is never staged again
echo ".env" >> .gitignore

# 2. Untrack the file without deleting it from disk
git rm --cached .env

# 3. Stage the updated .gitignore
git add .gitignore

# 4. Amend the last commit (removes the secret from that commit)
git commit --amend --no-edit

# 5. Push — use force-with-lease, not --force
git push --force-with-lease
```

## Prevention

Structure `.gitignore` to cover ALL locations where secrets can land:

```gitignore
# Covers root and any subdirectory
.env
.env.*
!.env.example
```

Avoid path-specific entries like `backend/.env` — they miss root-level `.env` files.

## Notes

- `--amend` only rewrites the most recent local commit. If the secret exists in older
  commits that are already on the remote, use `git filter-repo` to purge the full history.
- After a force push, team members must `git fetch && git reset --hard origin/main`.
- GitHub may still flag the token as compromised — rotate it immediately after the fix.
- The `.env.example` file (with placeholder values, no real secrets) should be committed
  as documentation of required environment variables.
