import json
from socket import inet_aton
import struct


def get_ip_list(file_path):
    list_of_ips = []
    with open(file_path) as f:
        data = json.load(f)
        for item in data:
            ip = item.get("ip")
            if ip not in list_of_ips:
                list_of_ips.append(ip)

    return sorted(list_of_ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

