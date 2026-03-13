# Script Memory Index

Master table of all stored scripts and solutions.

| Script | Language | Tags | Purpose |
|--------|----------|------|---------|
| [kvm_vm_ip_detector](scripts/kvm_vm_ip_detector/) | Python | kvm, networking, virtualization | Detect IPs of running KVM VMs via ARP/DHCP leases |
| [esphome_sensor_boot_fix](scripts/esphome_sensor_boot_fix/) | YAML | esphome, esp32, home-assistant | Suppress invalid sensor readings on device boot |
| [grafana_dashboard_provision](scripts/grafana_dashboard_provision/) | JSON | grafana, prometheus, monitoring | Provisionable infrastructure dashboard (CPU + RAM) |
| [github_init_push_with_pat](scripts/github_init_push_with_pat/) | Bash | git, github, pat, authentication | Initialize a local git repo and push to GitHub using a PAT in .env |
| [git_submodule_add](scripts/git_submodule_add/) | Bash | git, submodule, github, monorepo | Add an external public GitHub repo as a git submodule at a named path |
| [github_push_blocked_secret_scanning](scripts/github_push_blocked_secret_scanning/) | Bash | git, github, security, secret-scanning | Fix a push blocked by GitHub secret scanning — remove secret, amend, force push |
| [fastapi_jwt_httponly_cookies](scripts/fastapi_jwt_httponly_cookies/) | Python/JS | fastapi, jwt, cookies, security, react | Full FastAPI + React JWT auth using httpOnly cookies instead of localStorage |
| [passlib_bcrypt_compatibility](scripts/passlib_bcrypt_compatibility/) | Python | passlib, bcrypt, fastapi, docker, dependency-pinning | Fix passlib 1.7.4 crash (ValueError) caused by bcrypt>=4.1 breaking wrap-bug detection |

## Structure

Each script directory contains:
- **`script.*`** — The solution file
- **`metadata.yaml`** — Structured context (name, purpose, language, dependencies, tags)
- **`README.md`** — Human and AI readable description with usage instructions
