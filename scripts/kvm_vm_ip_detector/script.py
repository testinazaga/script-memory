#!/usr/bin/env python3
"""
KVM VM IP Detector
Detects IP addresses of running KVM/QEMU virtual machines via ARP/DHCP leases.
"""

import subprocess
import re
import sys


def get_running_vms() -> list[str]:
    result = subprocess.run(
        ["virsh", "list", "--name"],
        capture_output=True, text=True, check=True
    )
    return [name.strip() for name in result.stdout.splitlines() if name.strip()]


def get_vm_mac(vm_name: str) -> list[str]:
    result = subprocess.run(
        ["virsh", "domiflist", vm_name],
        capture_output=True, text=True, check=True
    )
    macs = re.findall(r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})", result.stdout)
    return macs


def get_ip_from_leases(mac: str, lease_file: str = "/var/lib/libvirt/dnsmasq/default.leases") -> str | None:
    try:
        with open(lease_file) as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3 and parts[1].lower() == mac.lower():
                    return parts[2]
    except FileNotFoundError:
        pass
    return None


def get_ip_from_arp(mac: str) -> str | None:
    result = subprocess.run(["arp", "-n"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if mac.lower() in line.lower():
            parts = line.split()
            if parts:
                return parts[0]
    return None


def main():
    vms = get_running_vms()
    if not vms:
        print("No running VMs found.")
        sys.exit(0)

    print(f"{'VM Name':<30} {'MAC':<20} {'IP':<20}")
    print("-" * 70)

    for vm in vms:
        macs = get_vm_mac(vm)
        for mac in macs:
            ip = get_ip_from_leases(mac) or get_ip_from_arp(mac) or "unknown"
            print(f"{vm:<30} {mac:<20} {ip:<20}")


if __name__ == "__main__":
    main()
