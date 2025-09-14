import socket
import sys

target = input("Enter the IP address or hostname to scan: ")
ports_to_scan = [21, 22, 23, 25, 80, 443, 8080, 3389]

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        s.connect((ip, port))
        print(f"Port {port} is open! ✅")
        
    except socket.error:
        print(f"Port {port} is closed. ❌")
        
    finally:
        s.close()

def main():
    print(f"Starting scan on target: {target}")
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid hostname or IP address. Exiting.")
        sys.exit()
    for port in ports_to_scan:
        scan_port(target_ip, port)

    print("Scan complete. 👍")

if __name__ == "__main__":
    main()
