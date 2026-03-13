# Script Memory

A personal knowledge base of verified scripts and solutions — built to avoid solving the same problem twice.

Each entry is a self-contained directory with a solution file, structured metadata, and a human-readable explanation. When starting a new project, pull this repo in as a git submodule to reuse solutions without copying files or duplicating work.

---

## What's Inside

```
scripts/
├── kvm_vm_ip_detector/          # Detect IPs of running KVM VMs
├── esphome_sensor_boot_fix/     # Suppress invalid sensor readings on boot
├── grafana_dashboard_provision/ # Provisionable Grafana dashboard (CPU + RAM)
└── github_init_push_with_pat/   # Init a git repo and push to GitHub via PAT
```

Each script directory contains:

| File | Purpose |
|------|---------|
| `script.*` | The working solution (`.py`, `.sh`, `.yaml`, `.json`, etc.) |
| `metadata.yaml` | Structured context: name, purpose, language, tags, dependencies |
| `README.md` | Human-readable explanation with usage instructions |

See [`INDEX.md`](INDEX.md) for a full table of all available solutions.

---

## Using This Repo in a New Project

Add this repo as a git submodule — not a copy. This keeps the knowledge base independent, version-controlled separately, and updatable without touching your project's own git history.

```bash
# Inside your new project's root directory
git submodule add https://github.com/testinazaga/script-memory.git knowledge

# On first clone of a project that already uses this submodule
git clone --recurse-submodules https://github.com/you/your-project.git

# Or if you forgot --recurse-submodules
git submodule update --init --recursive
```

Your project structure will look like:

```
your-project/
├── .env                  ← your project's own secrets (never shared)
├── knowledge/            ← this repo, mounted as a submodule
│   ├── .env              ← this repo's own secrets (separate, never shared)
│   ├── INDEX.md
│   └── scripts/
└── src/
```

### Updating the knowledge base from within your project

```bash
cd knowledge
git pull origin main
cd ..
git add knowledge
git commit -m "Update script-memory submodule"
```

---

## Keeping Secrets Separate

Both this repo and any project that uses it as a submodule maintain their own independent `.env` files. They are never shared, merged, or committed.

| Location | Contains | Committed? |
|----------|----------|------------|
| `knowledge/.env` | Secrets needed by this repo (e.g. `GITHUB_TOKEN`) | No — excluded by this repo's `.gitignore` |
| `your-project/.env` | Secrets for your project | No — excluded by your project's `.gitignore` |

The submodule boundary enforces this naturally: each repo has its own `.gitignore` and its own git history. Changes to one `.env` are invisible to the other.

---

## Why a Submodule and Not a Copy?

| Approach | Problem |
|----------|---------|
| Copy-paste scripts | Fixes and improvements never flow back; duplicates diverge |
| Git submodule | Single source of truth; pull updates any time; projects stay decoupled |

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version: only commit verified solutions.
