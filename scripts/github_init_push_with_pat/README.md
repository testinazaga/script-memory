# GitHub Init & Push with PAT

Initializes a local directory as a git repo and pushes it to a GitHub remote, authenticating via a Personal Access Token (PAT) stored in a `.env` file.

## Usage

```bash
# 1. Create .env with your token
echo "GITHUB_TOKEN=ghp_yourTokenHere" > .env

# 2. Run the script from inside your project directory
bash script.sh
```

## How it works

1. Reads `GITHUB_TOKEN` from `.env` via `source`
2. Runs `git init` and renames the default branch to `main`
3. Stages all files with `git add .` and creates the initial commit
4. Constructs an authenticated remote URL: `https://<token>@github.com/...`
5. Adds the remote as `origin` and pushes with `-u` to track the branch

## Requirements

- `git`
- A GitHub PAT with `repo` scope
- `.env` file in the project root formatted as:
  ```
  GITHUB_TOKEN=ghp_...
  ```

## Notes

- Ensure `.env` is listed in `.gitignore` — the token must never be committed
- The `.env` format must be `KEY=value`, not a raw token on its own line
- The script will error if `GITHUB_TOKEN` is unset or `.env` is missing
