import socket
from concurrent.futures import ThreadPoolExecutor
from utils import grab_banner, get_service
from config import THREADS, TIMEOUT

def scan_range(ip, start, end, output_file):
    open_ports = []

    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)

        try:
            s.connect((ip, port))
            service = get_service(port)
            banner = grab_banner(s)

            result = f"[OPEN] {port} ({service}) | {banner}"
            print(result)

            open_ports.append(port)

            with open(output_file, "a") as f:
                f.write(result + "\n")

        except:
            pass
        finally:
            s.close()

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(scan, range(start, end + 1))

    return open_ports


def filtered_scan(ip, start, end):
    filtered_ports = []

    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        try:
            result = s.connect_ex((ip, port))
            if result != 0:
                filtered_ports.append(port)
        except:
            filtered_ports.append(port)
        finally:
            s.close()

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(scan, range(start, end + 1))

    return filtered_ports
