from sanic import Sanic
from sanic_cors import CORS

from jinja2 import Environment, PackageLoader, select_autoescape

template_env = Environment(
    loader=PackageLoader(package_name='api', package_path='templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)


app = Sanic(__name__)
CORS(app, automatic_options=True)

import api.views # noqa