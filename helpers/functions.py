import tempfile
import urllib2

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
    blocks = []

    temp_file = tempfile.NamedTemporaryFile(mode='w+t')

    try:
        csv_file_content = urllib2.urlopen(country_url).read()
        temp_file.write(csv_file_content)
        temp_file.seek(0)
        reader = csv.reader(temp_file, delimiter=',')
        for row in reader:
            try:
                blocks.append(generate_ip_range(row[0], row[1]))
            except:
                pass

    except urllib2.URLError, ex:
        raise Exception(ex.reason)
    except Exception, e:
        raise e
    finally:
        temp_file.close()

    return blocks


def count_ip_address(blocks):
    count = 0
    for block in blocks:
        count += len(block)
    return count
