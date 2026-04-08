TOP_PORTS = (1, 1000)
FULL_PORTS = (1, 65535)
THREADS = 100
TIMEOUT = 1

SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3389: "RDP", 8080: "HTTP-Proxy"
}
