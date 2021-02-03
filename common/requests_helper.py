import datetime
import json

import httpretty
import requests
from flask import current_app
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt.utils import dump

from common.constants import INTERNAL_SERVER_ERROR_MESSAGE, STATUS_FORCE_LIST

MOCK_URLS = {
    'https://cheap-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://cheap-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
    'https://expensive-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://expensive-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
    'https://premium-payment-gateway/api/v1/availability/': {'data': 'ok', 'status_code': 200},
    'https://premium-payment-gateway/api/v1/transaction/': {'data': 'ok', 'status_code': 200},
}


def date_time_json_serialize(date):
    """
    Serialize datetime object to string
    :param date: datetime object
    :return:
    """
    if isinstance(date, datetime.datetime):
        return "{}-{}-{}".format(date.year, date.month, date.day)


def logging_hook(response, *args, **kwargs):
    """
    Print the details of requests
    :param response:
    :param args:
    :param kwargs:
    :return:
    """
    data = dump.dump_all(response)
    print(data.decode('utf-8'))


@httpretty.activate
def make_request(method='get', api_url='', api_key='', data={}, retries=0):
    """
    Make call to external urls using python request
    :param method: get|post (str)
    :param api_url:
    :param api_key:
    :param data: data to send in the request (dict)
    :param retries:
    :return:
    """
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=STATUS_FORCE_LIST,
        allowed_methods=frozenset(['GET', 'POST'])
    )
    retry_adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    if current_app.debug:
        session.hooks["response"] = [logging_hook]
    session.mount('http://', retry_adapter)
    session.mount('https://', retry_adapter)
    headers = {'content-type': 'application/json'}
    if api_key and isinstance(data, dict):
        data['api_key'] = api_key
    try:
        method = method.upper()
        # mocking the requests
        httpretty.register_uri(
            method,
            api_url,
            body=json.dumps(MOCK_URLS[api_url]['data'], default=date_time_json_serialize),
            status=MOCK_URLS[api_url]['status_code']
        )
        if method == httpretty.GET:
            response = session.get(api_url, params=data, headers=headers)
        elif method == httpretty.POST:
            response = session.post(
                api_url,
                data=json.dumps(data, default=date_time_json_serialize),
                headers=headers
            )
        return {'status_code': response.status_code, 'data': response.json()}
    except Exception as exception_occurred:
        if current_app.debug:
            print(exception_occurred)
        return {'status_code': 500, 'data': INTERNAL_SERVER_ERROR_MESSAGE}
