from sanic import Sanic
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app, automatic_options=True)

import api.views # noqa