# Git Submodule Add (Public Repo)

## Problem

You need to embed an external repository (e.g. a shared knowledge base) inside your
own project repo as a submodule, so it stays independently versioned but is available
at a known path.

## Environment

- OS: Ubuntu (any Linux)
- Tool: git

## Why This Works

`git submodule add` clones the target repo and registers it in `.gitmodules`. The parent
repo tracks the submodule as a pointer (specific commit SHA), not a copy. Anyone who
clones the parent with `--recurse-submodules` gets the submodule automatically.

HTTPS works for public repos without credentials. For private repos you need a PAT
embedded in the URL or an SSH key — see `github_init_push_with_pat`.

## Commands

```bash
# Add submodule at a named subdirectory
git submodule add https://github.com/<owner>/<repo>.git <local-dir>

# Verify it was registered correctly
git submodule status
cat .gitmodules

# Commit the pointer + .gitmodules
git add .gitmodules <local-dir>
git commit -m "chore: add <repo> as submodule under <local-dir>"
git push
```

## Clone an Existing Repo With Its Submodules

```bash
# On first clone
git clone --recurse-submodules <repo-url>

# If already cloned without submodules
git submodule update --init --recursive
```

## Notes

- The submodule directory shows as a single commit pointer in the parent repo — not a folder of files in `git diff`
- To update a submodule to its latest remote commit: `cd <local-dir> && git pull origin main && cd .. && git add <local-dir> && git commit`
- Submodule URL is stored in `.gitmodules` — keep this file committed
- If the target repo is private, embed the PAT: `https://<token>@github.com/<owner>/<repo>.git`
