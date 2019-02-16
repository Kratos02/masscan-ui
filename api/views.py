import json
from os import path
from os.path import exists

from sanic.response import html as sanic_html, json as sanic_json

from api import app, template_env
from api.logic import get_ip_list, get_results_by_ip, get_results_path, get_results_files, analyze_results_files


@app.route('/', methods=['GET'])
async def home(request):
    results_path = get_results_path()
    files = get_results_files(results_path)
    results_analysis = analyze_results_files(files, results_path)

    template = template_env.get_template("dashboard.html")
    rendered_template = await template.render_async(summary=results_analysis[0], details=results_analysis[1])
    return sanic_html(rendered_template)

@app.route('/details/<file:string>', methods=['GET'])
async def file_details(request, file):
    file_path = path.join(get_results_path(), file)

    with open(file_path) as f:
        data = json.load(f)
    results = []
    targets = get_ip_list(data)
    for ip in targets:
        results.append({'ip': ip, 'details': get_results_by_ip(data, ip)})

    template = template_env.get_template("details.html")
    rendered_template = await template.render_async(results=results)

    return sanic_html(rendered_template)

@app.route('/summary', methods=['GET'], version=1)
async def summary(request):
    absolute_path = get_results_path()

    if not exists(absolute_path):
        return sanic_json({'summary': {}, 'details': {}})

    files = get_results_files(absolute_path)

    results_analysis = analyze_results_files(files, absolute_path)

    return sanic_json({'summary': results_analysis[0], 'details': results_analysis[1]})


@app.route('/details/<file:string>/<ip:string>', methods=['GET'], version=1)
async def ip_details_handler(request, file, ip):
    file_path = path.join(get_results_path(), file)

    if not exists(file_path):
        return sanic_json({})

    with open(file_path) as f:
        data = json.load(f)

    return sanic_json(get_results_by_ip(data, ip))


@app.route('/details/<file:string>', methods=['GET'], version=1)
async def file_details_handler(request, file):
    file_path = path.join(get_results_path(), file)

    if not exists(file_path):
        return sanic_json({})

    with open(file_path) as f:
        data = json.load(f)
    results = []
    targets = get_ip_list(data)
    for ip in targets:
        results.append({'ip': ip, 'results': get_results_by_ip(data, ip)})
    return sanic_json(results)
