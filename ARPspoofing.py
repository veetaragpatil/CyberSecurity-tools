#this the code of  ARPSpoofing tool where this used for attack like "man in the middle".
#the command is for capturing packet *arpspoof -i [interface] -t [clientIP] [getwayIP]*
#the command is for forwarding packet *arpspoof -i [interface] -t [getwayIP] [clientIP]*


"""Poll interval — how often to read the ARP table (seconds).

Interface selection — which network interface to monitor (where supported).

Alert outputs — console, log file (text/JSON/CSV), or run a custom shell command on alert.

Whitelist / ignore lists — IPs or MACs that should be ignored (static entries).

Detection sensitivity — whether to alert on any MAC change for an IP, or require N differing MACs / repeated occurrences.

History retention — how long (or how many entries) to remember before pruning.

Formatting — plain text vs JSON output for logs.

Email / webhook alerting — hooks provided (placeholders) if you want to integrate with external systems (requires credentials).

Daemonize / background mode — run as a service (instructions included in comments).

Verbose / debug logging — more internal info for troubleshooting.

Run-once mode — check ARP table once, print results, exit (useful for cron).

Safe-only — this tool remains passive; no feature will send network traffic.
///the code is for this where we can customize it.
#!/usr/bin/env python3

arp_watch.py

Simple ARP cache monitor. Periodically polls the local ARP table and
alerts if an IP maps to more than one MAC (possible ARP spoofing).
Safe: does not send any packets or modify the network.
"""

import subprocess
import sys
import time
import re
from collections import defaultdict

POLL_INTERVAL = 5  # seconds

def parse_arp_output(output):
    """
    Parse `arp -a` output for common platforms.
    Returns dict: { ip: mac }
    """
    ip_mac = {}
    # Common MAC regex (xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx)
    mac_re = re.compile(r'([0-9a-fA-F]{2}[:\-](?:[0-9a-fA-F]{2}[:\-]){4}[0-9a-fA-F]{2})')
    ip_re = re.compile(r'(\d+\.\d+\.\d+\.\d+)')

    for line in output.splitlines():
        # Skip empty lines
        if not line.strip():
            continue
        # Try to find an IP and MAC on the line
        ip_match = ip_re.search(line)
        mac_match = mac_re.search(line)
        if ip_match and mac_match:
            ip = ip_match.group(1)
            mac = mac_match.group(1).lower().replace('-', ':')
            ip_mac[ip] = mac
    return ip_mac

def get_arp_table():
    try:
        if sys.platform.startswith('win'):
            proc = subprocess.run(['arp', '-a'], capture_output=True, text=True, check=True)
            out = proc.stdout
        else:
            proc = subprocess.run(['arp', '-a'], capture_output=True, text=True, check=True)
            out = proc.stdout
    except Exception as e:
        print(f"Error running arp: {e}")
        return {}
    return parse_arp_output(out)

def pretty_mac(mac):
    return mac.upper()

def main():
    print("Starting ARP watcher (safe, read-only). Press Ctrl-C to stop.")
    history = defaultdict(set)  # ip -> set(mac)
    try:
        while True:
            table = get_arp_table()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if not table:
                print(f"[{timestamp}] ARP table empty or couldn't read it.")
            # update history and check for conflicts
            for ip, mac in table.items():
                if mac not in history[ip]:
                    if history[ip]:
                        # we've seen a different MAC for this IP before -> alert
                        seen = ', '.join(pretty_mac(m) for m in history[ip])
                        print(f"[{timestamp}] WARNING: IP {ip} now maps to {pretty_mac(mac)}; previously seen: {seen}")
                    history[ip].add(mac)
            # Optionally prune history for entries no longer in table (keeps memory bounded)
            # If an IP disappears, we keep it in history for a short while; for simplicity, prune entries not seen for long runs could be added.
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == '__main__':
    main()

