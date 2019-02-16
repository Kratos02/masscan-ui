import os
import tempfile
from urllib.error import URLError
from urllib.request import urlopen

import csv


def get_url_from_name(domain, country):
    return 'http://{}/countryip/{}.csv'.format(domain, country.lower())


def extract_ip_range(cells):
    return str(cells[1].text).split(' - ')


def generate_ip_range(start_ip, end_ip):
    # written by Tihomir Kit (https://github.com/pootzko)
    # https://gist.github.com/pootzko/ac34906e11d9715d9514c75507c24dc0

    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range


def get_ip_blocks_from_nirsoft(country_url):
    import requests

    blocks = []

    temp_file = tempfile.NamedTemporaryFile(mode='w+t')

    try:
        csv_file_content = requests.get(country_url).text
        temp_file.write(csv_file_content)
        temp_file.seek(0)
        reader = csv.reader(temp_file, delimiter=',')
        for row in reader:
            try:
                blocks.append(generate_ip_range(row[0], row[1]))
            except:
                pass

    except URLError as ex:
        raise Exception(ex.reason)
    except Exception as e:
        raise e
    finally:
        temp_file.close()

    return blocks


def count_ip_address(blocks):
    count = 0
    for block in blocks:
        count += len(block)
    return count


def generate_masscan_settings(blocks, rate, ports, destination, banners = True):
    if not os.path.exists(destination):
        os.makedirs(destination)

    settings = []
    output_format = "json"
    output_status = "all"

    count = 0
    for block in blocks:
        start =  block[0]
        end = block[len(block) - 1]
        range = "{}-{}".format(start, end)
        config = "rate = {}\n".format(int(rate))
        config += "output-format = {}\n".format(output_format)
        config += "output-status = {}\n".format(output_status)

        output_filename = "{}/{}.json".format(destination, str(count))
        config += "output-filename = {}\n".format(output_filename)

        config += "ports = {}\n".format(str(ports))
        config += "range = {}\n".format(range)

        if banners:
            config += "banners = true\n"

        settings.append(config)

        count += 1

    return settings

def write_massscan_config_files(settings, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    count = 0
    for config in settings:
        filename = "{}/{}.conf".format(destination, str(count))
        try:
            with open(filename,"w+") as f:
                f.write(config)
                f.close()
        except Exception as e:
            raise e
        count += 1

    path, dirs, files = next(os.walk(destination))

    return len(files) == len(settings)
