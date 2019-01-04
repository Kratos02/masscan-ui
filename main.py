#!/usr/bin/env python
import argparse
import os.path
import sys

import configparser

from helpers.functions import get_url_from_name, get_ip_blocks_from_nirsoft, count_ip_address
from labels import *

CONFIG_FILE = 'settings.ini'
NirSoft_DOMAIN = 'www.nirsoft.net'


def should_continue(blocks, total):
    return total != 0


def validate_settings(config):
    return os.path.exists(config['DEFAULT']['masscan']) and config['DEFAULT']['masscan'] > 0


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    if not validate_settings(config):
        print "Settings are not valid."
        sys.exit(-1)

    masscan = config['DEFAULT']['masscan']

    parser = argparse.ArgumentParser(description='Mass scanning a whole country.')
    parser.add_argument('--country', help='Country')

    args = parser.parse_args()

    total = 0
    blocks = []

    if args.country:
        country_url = get_url_from_name(NirSoft_DOMAIN, args.country)
        blocks = get_ip_blocks_from_nirsoft(country_url)

    total = count_ip_address(blocks)

    if not should_continue(blocks, total):
        print "No IP was found."
        sys.exit(-1)

    print TOTAL_IP_COUNTS.format(total)
