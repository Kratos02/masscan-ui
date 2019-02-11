from socket import inet_aton
import struct

from os import path


def get_results_path():
    current_path = path.dirname(path.abspath(__file__))
    results_path = '../results'
    absolute_path = path.join(current_path, results_path)
    return absolute_path


def get_ip_list(data):
    list_of_ips = []

    for item in data:
        ip = item.get("ip")
        if ip not in list_of_ips:
            list_of_ips.append(ip)

    return sorted(list_of_ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])


def get_results_by_ip(data, ip):
    results = []

    ports = []
    for item in data:
        if item.get("ip") == ip:
            ports.append(item.get("ports"))
    for port in ports:
        item = port[0]
        record = {
            "port": item.get("port"),
            "protocol": item.get("proto", None),
            "status": item.get("status", None),
            "ttl": item.get("ttl", None),
            "service": [],
        }
        if not is_record_in_results(record, results):
            results.append(record)
        banner = item.get("service", None)
        if banner:
            for _result in results:
                if _result.get("port") == record.get("port"):
                    _result.get("service").append({"content": banner.get("banner"), "name": banner.get("name")})

    return results


def is_record_in_results(record, results):
    for item in results:
        if item.get("port") == record.get("port"):
            return True
    return False
