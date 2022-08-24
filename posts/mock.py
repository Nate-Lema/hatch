from unittest import mock
from urllib.parse import urlparse, parse_qs

from requests import status_codes
from utils.json_file_control import load_json_file


def side_effect_parallel_requests(method_args, max_workers):
    body = ''
    for url in method_args:
        parsed_url = urlparse(url['url'])
        query = parse_qs(parsed_url.query)
        if query['tag'][0] == 'show_error':
            return [mock.Mock(status_codes=404)]
        elif query['tag'][0] == 'tech':
            body = load_json_file('mock/hatchways_api_tag_tech.json')
        elif query['tag'][0] == 'science':
            body = load_json_file('mock/hatchways_api_tag_science.json')

    MockResponse = mock.Mock(status_code=200)
    MockResponse.json.return_value = body
    return [MockResponse]
