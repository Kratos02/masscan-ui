import configparser
import datetime
import json
from os import listdir, path, stat
from os.path import isfile, join, exists

from sanic import Sanic
from sanic.response import json as s_json

from helpers.masscan import get_ip_list, get_results_by_ip

app = Sanic()


def get_results_path():
    current_path = path.dirname(path.abspath(__file__))
    results_path = 'results'
    absolute_path = path.join(current_path, results_path)
    return absolute_path

@app.route('/', methods=['GET'])
async def home(request):
    absolute_path = get_results_path()

    if not exists(absolute_path):
         return s_json({'summary': {}, 'details': {}})

    files = [f for f in listdir(path=absolute_path) if isfile(join(absolute_path, f))]

    details = []
    for result in files:
        file_path = path.join(absolute_path, result)
        info = stat(file_path)
        with open(file_path) as f:
            data = json.load(f)
            targets = get_ip_list(data)

            details.append(
                {
                    'filename': result,
                    'timestamp': datetime.datetime.fromtimestamp(info.st_birthtime),
                    'targets': len(targets),
                    '_link': '/details/{}'.format(result)
                }
            )

    return s_json({'summary': {'files': len(files)}, 'details': details})

@app.route('/details/<file:string>/<ip:string>', methods=['GET'])
async def ip_details_handler(request, file, ip):
    file_path = path.join(get_results_path(), file)

    with open(file_path) as f:
        data = json.load(f)

    return s_json(get_results_by_ip(data, ip))

@app.route('/details/<file:string>', methods=['GET'])
async def file_details_handler(request, file):
    file_path = path.join(get_results_path(), file)

    with open(file_path) as f:
        data = json.load(f)
    results = {}
    targets = get_ip_list(data)
    for ip in targets:
        results[ip] = get_results_by_ip(data, ip)
    return s_json(results)



if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    app.run(host='0.0.0.0', port=settings.get('api', 'port'))
