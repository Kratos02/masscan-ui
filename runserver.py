#!/usr/bin/env python3
from argparse import ArgumentParser
from multiprocessing import cpu_count
import configparser

from api import app

HOSTS = ('127.0.0.1', '0.0.0.0')

if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    parser = ArgumentParser(__doc__)
    parser.add_argument('--port', type=int, default=settings.get('api', 'port'))
    parser.add_argument('--host', choices=HOSTS, default=HOSTS[0])
    parser.add_argument('--workers', type=int, default=cpu_count())
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, workers=args.workers)
