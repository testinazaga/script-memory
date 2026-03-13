#!/usr/bin/env bash
# github_init_push_with_pat
# Initializes a local git repo and pushes to GitHub using a PAT stored in .env

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
ENV_FILE=".env"
REMOTE_URL="https://github.com/testinazaga/script-memory.git"
BRANCH="main"
COMMIT_MSG="Initial commit"

# ── Load PAT from .env ────────────────────────────────────────────────────────
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: $ENV_FILE not found. Create it with: GITHUB_TOKEN=ghp_..." >&2
  exit 1
fi

# shellcheck source=.env
source "$ENV_FILE"

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "ERROR: GITHUB_TOKEN is not set in $ENV_FILE" >&2
  exit 1
fi

# ── Init git ──────────────────────────────────────────────────────────────────
git init
git branch -m "$BRANCH"

# ── Stage and commit ──────────────────────────────────────────────────────────
git add .
git commit -m "$COMMIT_MSG"

# ── Set authenticated remote and push ────────────────────────────────────────
AUTHED_URL="https://${GITHUB_TOKEN}@${REMOTE_URL#https://}"
git remote add origin "$AUTHED_URL"
git push -u origin "$BRANCH"

echo "Done — pushed to $REMOTE_URL on branch $BRANCH"
