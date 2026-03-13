# KVM VM IP Detector

Detects IP addresses of running KVM/QEMU virtual machines by cross-referencing MAC addresses from `virsh` with DHCP lease files and ARP tables.

## Usage

```bash
sudo python3 script.py
```

## How it works

1. Lists running VMs via `virsh list`
2. Retrieves MAC addresses via `virsh domiflist <vm>`
3. Looks up IPs in `/var/lib/libvirt/dnsmasq/default.leases`
4. Falls back to `arp -n` if no lease found

## Requirements

- `libvirt-clients` (`virsh`)
- `net-tools` (`arp`)
- Python 3.10+

## Output

```
VM Name                        MAC                  IP
----------------------------------------------------------------------
ubuntu-server                  52:54:00:ab:cd:ef    192.168.122.10
```
