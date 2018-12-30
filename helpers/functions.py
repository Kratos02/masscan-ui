import urllib2

from bs4 import BeautifulSoup


def get_url_from_name(domain, country):
    return 'https://{}/ip-addresses/{}'.format(domain, country.replace(' ','--').lower())


def extract_ip_range(cells):
    return str(cells[1].text).split(' - ')


def generate_ip_range(start_ip, end_ip):
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


def get_ip_blocks_from_xmyip(country_url=None):
    # written by Tihomir Kit (https://github.com/pootzko)
    # https://gist.github.com/pootzko/ac34906e11d9715d9514c75507c24dc0
    blocks = []
    try:
        html = urllib2.urlopen(country_url)
        soup = BeautifulSoup(html, features="html.parser")
        table = soup.body.find('div', attrs={'class': 'divTableBody'})

        for row in table.findAll('div', attrs={'class': 'divTableRow'}):
            cells = row.findAll('div', attrs={'class': 'divTableCell'})
            block = extract_ip_range(cells)
            ip_range = generate_ip_range(block[0], block[1])
            blocks.append(ip_range)

    except ValueError, ex:
        raise Exception(ex.message)
    except urllib2.URLError, ex:
        raise Exception(ex.reason)

    return blocks


def count_ip_address(blocks):
    count = 0
    for block in blocks:
        count += len(block)
    return count
