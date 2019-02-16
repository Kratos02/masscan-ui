#!/usr/bin/env python
import argparse
import os.path
import sys

import configparser

from helpers.functions import get_url_from_name, get_ip_blocks_from_nirsoft, count_ip_address, \
    generate_masscan_settings, write_massscan_config_files

CONFIG_FILE = 'settings.ini'
MASSCAN_SETTINGS_PATH = 'scans'
MASSCAN_SETTINGS_RESULTS = 'results'

NirSoft_DOMAIN = 'www.nirsoft.net'

NO_IP_WAS_FOUND = 'No IP was found'
TOTAL_IP_COUNTS = 'TOTAL OF IP FOUND: {:,}'


def should_continue(blocks, total):
    return total != 0


def validate_settings(config):
    return os.path.exists(config.get('scanner', 'masscan')) and \
           int(config.get('scanner', 'rate')) > 0 and \
           len(config.get('scanner', 'ports').split(',')) > 0


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    if not validate_settings(config):
        print("Settings are not valid.")
        sys.exit(-1)

    masscan = config.get('scanner', 'masscan')

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
        print(NO_IP_WAS_FOUND)
        sys.exit(-1)

    print(TOTAL_IP_COUNTS.format(total))

    current_path = os.path.dirname(os.path.realpath(__file__))

    masscan_settings = generate_masscan_settings(blocks,
                                                 config.getfloat('scanner', 'rate'),
                                                 config.get('scanner', 'ports'),
                                                 "{}/{}".format(current_path, MASSCAN_SETTINGS_RESULTS),
                                                 config.getboolean('scanner', 'banners'))

    scan_created = write_massscan_config_files(masscan_settings, "{}/{}".format(current_path, MASSCAN_SETTINGS_PATH))
