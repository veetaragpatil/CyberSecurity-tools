import socket
from config import SERVICES

def grab_banner(sock):
    try:
        return sock.recv(1024).decode().strip()
    except:
        return "No banner"

def get_service(port):
    return SERVICES.get(port, "Unknown")
