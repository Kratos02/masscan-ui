import datetime
import json
from os import listdir, path, stat
from os.path import isfile, join, exists

from sanic.response import file as sanic_file, json as sanic_json

from api import app
from api.logic import get_ip_list, get_results_by_ip, get_results_path


@app.route('/', methods=['GET'])
async def home(request):
    return await sanic_file('./assets/dashboard.html')

@app.route('/summary', methods=['GET'], version=1)
async def summary(request):
    summary = {}

    absolute_path = get_results_path()

    if not exists(absolute_path):
        return sanic_json({'summary': summary, 'details': {}})

    files = [f for f in listdir(path=absolute_path) if isfile(join(absolute_path, f))]

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
                    '_link': '/v1/details/{}'.format(result),
                    'open': _open_ports, 'closed': _closed_ports
                }
            )

    return sanic_json({'summary': {'scans': len(files), "open": open_ports, "closed": closed_ports}, 'details': details})


@app.route('/details/<file:string>/<ip:string>', methods=['GET'],  version=1)
async def ip_details_handler(request, file, ip):
    file_path = path.join(get_results_path(), file)

    if not exists(file_path):
        return sanic_json({})

    with open(file_path) as f:
        data = json.load(f)

    return sanic_json(get_results_by_ip(data, ip))


@app.route('/details/<file:string>', methods=['GET'],  version=1)
async def file_details_handler(request, file):
    file_path = path.join(get_results_path(), file)

    if not exists(file_path):
        return sanic_json({})

    with open(file_path) as f:
        data = json.load(f)
    results = {}
    targets = get_ip_list(data)
    for ip in targets:
        results[ip] = get_results_by_ip(data, ip)
    return sanic_json(results)
