from unittest import TestCase


class Test_Functions(TestCase):
    def test_get_url_from_name(self):
        from helpers.functions import get_url_from_name
        from main import XMyIP_DOMAIN

        country = 'Dominican Republic'
        url = get_url_from_name(XMyIP_DOMAIN, country)
        assert 'https://{}/ip-addresses/{}'.format(XMyIP_DOMAIN, 'dominican--republic') == url

    def test_generate_ip_range(self):
        from helpers.functions import generate_ip_range
        start = '66.98.48.1'
        end = '66.98.48.255'
        ip_range = generate_ip_range(start, end)
        assert ip_range[0] == start
        assert ip_range[len(ip_range)-1] == end


    def test_count_ip_address(self):
        from helpers.functions import count_ip_address

        count = 0
        blocks = [['66.98.48.0', '66.98.48.1', '66.98.48.2'], ['64.32.124.0', '64.32.124.1']]
        for block in blocks:
            count += len(block)

        assert count == count_ip_address(blocks)
