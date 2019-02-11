import configparser
import datetime
import json
from os import listdir, path, stat
from os.path import isfile, join

from sanic import Sanic
from sanic.response import json as s_json

app = Sanic()


@app.route('/', methods=['GET'])
async def home(request):
    current_path = path.dirname(path.abspath(__file__))
    results_path = 'results'
    absolute_path = path.join(current_path, results_path)
    files = [f for f in listdir(path=absolute_path) if isfile(join(results_path, f))]

    details = []
    for result in files:
        file_path = path.join(absolute_path, result)
        info = stat(file_path)
        with open(file_path) as f:
            data = json.load(f)
        targets = []
        for line in data:
            ip = line.get('ip', None)
            if ip not in targets:
                targets.append(ip)

        details.append(
            {
                'filename': result,
                'timestamp': datetime.datetime.fromtimestamp(info.st_birthtime),
                'targets': len(targets),
                '_link': '/details/{}'.format(result)
            }
        )

    return s_json({'summary': {'files': len(files)}, 'details': details})


@app.route('/details/<file:string>', methods=['GET'])
async def integer_handler(request, file):
    current_path = path.dirname(path.abspath(__file__))
    results_path = 'results'
    absolute_path = path.join(current_path, results_path)
    file_path = path.join(absolute_path, file)
    with open(file_path) as f:
        data = json.load(f)

    return s_json({'file': data[0]})


if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    app.run(host='0.0.0.0', port=settings.get('api', 'port'))
