import socket

from getmac import get_mac_address
import httpx

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("google.com", 80))
        local_ip = s.getsockname()[0]
    return local_ip

def get_mac():
    return get_mac_address(ip=get_local_ip())

def get_public_ip():
    request = httpx.get('http://ip-api.com/json')
    return request.json()['query']

def get_summary():
    return {
        'local': get_local_ip(),
        'public': get_public_ip(),
        'mac': get_mac()
    }

