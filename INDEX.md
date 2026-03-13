# Script Memory Index

Master table of all stored scripts and solutions.

| Script | Language | Tags | Purpose |
|--------|----------|------|---------|
| [kvm_vm_ip_detector](scripts/kvm_vm_ip_detector/) | Python | kvm, networking, virtualization | Detect IPs of running KVM VMs via ARP/DHCP leases |
| [esphome_sensor_boot_fix](scripts/esphome_sensor_boot_fix/) | YAML | esphome, esp32, home-assistant | Suppress invalid sensor readings on device boot |
| [grafana_dashboard_provision](scripts/grafana_dashboard_provision/) | JSON | grafana, prometheus, monitoring | Provisionable infrastructure dashboard (CPU + RAM) |

## Structure

Each script directory contains:
- **`script.*`** — The solution file
- **`metadata.yaml`** — Structured context (name, purpose, language, dependencies, tags)
- **`README.md`** — Human and AI readable description with usage instructions
