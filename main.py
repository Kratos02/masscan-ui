#!/usr/bin/env python
import argparse
import sys

from helpers.functions import get_url_from_name, get_ip_blocks_from_xmyip, count_ip_address
from labels import *

XMyIP_DOMAIN = 'www.xmyip.com'


def should_continue(blocks, total):
    return total != 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyCaribbean')
    parser.add_argument('--country', help='Country')

    args = parser.parse_args()

    total = 0
    blocks = []

    if args.country:
        country_url = get_url_from_name(XMyIP_DOMAIN, args.country)
        blocks = get_ip_blocks_from_xmyip(country_url)

    total = count_ip_address(blocks)

    if not should_continue(blocks, total):
        print "No IP was found."
        sys.exit(-1)

    print TOTAL_IP_COUNTS.format(total)
