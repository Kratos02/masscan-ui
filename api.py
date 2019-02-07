import datetime
import json

from sanic import Sanic
from sanic.response import json as s_jon
import configparser
from os import listdir, path, stat
from os.path import isfile, join

app = Sanic()


@app.route('/')
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
                'targets': len(targets)
            }
        )

    return s_jon({'summary': {'files': len(files)}, 'details': details})


if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    app.run(host='0.0.0.0', port=settings.get('api', 'port'))
