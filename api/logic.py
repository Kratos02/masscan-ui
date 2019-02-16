import datetime
import json
import struct
from os import listdir, stat
from os import path
from os.path import isfile, join
from socket import inet_aton
from itertools import groupby


def analyze_results_files(files, absolute_path):
    open_ports = 0
    closed_ports = 0

    details = []
    for result in files:
        _open_ports = 0
        _closed_ports = 0

        file_path = path.join(absolute_path, result)
        info = stat(file_path)
        with open(file_path) as f:
            data = json.load(f)
            targets = get_ip_list(data)

            for ip in targets:
                for record in get_results_by_ip(data, ip):
                    if record.get("status") == "closed":
                        closed_ports += 1
                        _closed_ports += 1
                    else:
                        open_ports += 1
                        _open_ports += 1

            details.append(
                {
                    'filename': result,
                    'timestamp': datetime.datetime.fromtimestamp(info.st_birthtime),
                    'targets': len(targets),
                    '_link': '/details/{}'.format(result),
                    'open': _open_ports, 'closed': _closed_ports
                }
            )

    return {'results': len(files), "open": open_ports, "closed": closed_ports}, details


def get_results_files(absolute_path):
    return [f for f in listdir(path=absolute_path) if isfile(join(absolute_path, f))]


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


def summarize_details(details):
    ports = []
    open_ports = []
    closed_ports = []

    frequency = {}
    status_frequency = {}
    for result in details:
        for entry in result.get('details'):
            port = entry.get('port')
            if entry.get('status') == 'open':
                open_ports.append(port)
            else:
                closed_ports.append(port)
            ports.append(port)

    for port in ports:
        frequency[port] = ports.count(port)
        status_frequency[port] = {'open': open_ports.count(port), 'closed': closed_ports.count(port)}

    return {'frequency': frequency, 'open': len(open_ports), 'closed': len(closed_ports), 'status': status_frequency}
