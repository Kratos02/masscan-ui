from helpers.masscan.classes.banner import Banner
from helpers.masscan.classes.port import Port
from helpers.masscan.classes.result import Result


def parse(results):
    scans = {}
    for result in results:
        ip = result.get('ip')
        if not scans.has_key(ip):
            scans[ip] = {"timestamp" : result.get('timestamp'),
                         "ports": {}
                         }
        for port in result.get('ports'):
            if not scans[ip].get('ports').has_key(port.get('port')):
                scans[ip].get('ports')[port.get('port')] = []
            scans[ip].get('ports')[port.get('port')].append(port)

    return scans

def transform(scans):
    results = []
    for key in scans.keys():
        ports = []
        for port in scans[key].get('ports').keys():
            number = None
            status = None
            reason = None
            protocol = None
            ttl = None
            banners = []

            for entry in scans[key].get('ports')[port]:
                if not entry.has_key('service'):
                    number = entry.get('port')
                    status = entry.get('status')
                    reason = entry.get('reason')
                    protocol = entry.get('proto')
                    ttl = entry.get('ttl')
                else:
                    banners.append(Banner(entry.get('service')['name'], entry.get('service')['banner']))

            service = Port(number, status, reason, protocol, ttl, banners)
            ports.append(service)

        result = Result(ip=key, timestamp=scans[key].get('timestamp'), ports=ports)
        results.append(result)

    return results
