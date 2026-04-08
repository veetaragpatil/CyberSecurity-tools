import argparse
import socket
from datetime import datetime
import os

from scanner import scan_range, filtered_scan
from config import TOP_PORTS, FULL_PORTS

def smart_scan(ip, output_file):
    print("⚡ Phase 1: Top 1000 Ports Scan")
    open_ports = scan_range(ip, *TOP_PORTS, output_file)

    if open_ports:
        print(f"✅ Found open ports: {open_ports}")
        return open_ports

    print("⚠️ No open ports found → Checking filtered ports...")
    filtered = filtered_scan(ip, *TOP_PORTS)

    if filtered:
        print("🛡️ Target may be behind firewall (filtered ports detected)")
        return filtered

    print("🚨 Escalating to FULL scan (1-65535)...")
    return scan_range(ip, *FULL_PORTS, output_file)


def main():
    parser = argparse.ArgumentParser(description="🔥 ReconX Smart Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP/Domain")

    args = parser.parse_args()
    target = args.target

    try:
        ip = socket.gethostbyname(target)
    except:
        print("❌ Invalid target")
        return

    os.makedirs("reports", exist_ok=True)
    output_file = f"reports/scan_{ip}.txt"

    print("="*60)
    print("🔥 ReconX Scanner Started")
    print(f"Target: {target} ({ip})")
    print("="*60)

    start = datetime.now()

    smart_scan(ip, output_file)

    end = datetime.now()

    print("\n✅ Scan Complete")
    print(f"⏱ Time Taken: {end - start}")


if __name__ == "__main__":
    main()
