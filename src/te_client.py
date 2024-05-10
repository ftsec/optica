import json
import logging
import time
from pprint import pprint

import requests

import config.settings
from config.settings import base_url, te_bearer_token, request_timeout
from object.object import TestType, validate_test_data
from src.tines import send_to_tines_webhook

te_session = requests.Session()
headers = {"Authorization": f"Bearer {te_bearer_token}",
           "content-type": "application/json"}
def send_get_request(path, method='GET', params=None):
    try:
        if method == 'GET':
            response = te_session.get(base_url + f'/{path}'
                                  , headers=headers
                                  , timeout=request_timeout, params=params)
            if response.status_code != 200:
                logging.error(f"Failed to get the data from ThousandEyes API. Status code: {response.status_code}")
                return None
            return response
    except Exception as e:
        logging.error(f"Failed to get the test data from ThousandEyes API. Error: {e}")
        return None

def get_all_tests():
    try:
        te_test_response = send_get_request('tests.json')
        tests = []
        if te_test_response is not None:
            for test in te_test_response.json()['test']:
                tests.append(json.loads(validate_test_data(test)))
        return json.dumps(tests)
    except Exception as e:
        logging.error(f"Failed to get the test data from ThousandEyes API. Error: {e}")
        return None
def get_all_tests_by_aid(aid):
    try:
        params = {'aid': aid}
        logging.info(f"Getting tests for account group: {aid}")
        print(f"Getting tests for account group: {aid}")
        te_test_response = send_get_request('tests.json', params=params)
        tests = []
        if te_test_response is not None:
            for test in te_test_response.json()['test']:
                tests.append(json.loads(validate_test_data(test)))
        return json.dumps(tests)
    except Exception as e:
        logging.error(f"Failed to get the test data from ThousandEyes API. Error: {e}")
        return None

def get_account_groups():
    try:
        te_test_response = send_get_request('account-groups.json')
        return te_test_response.json()
    except Exception as e:
        logging.error(f"Failed to get the test data from ThousandEyes API. Error: {e}")
        return None
def get_all_group_ids():
    try:
        ida_s=[]
        for account_group in get_account_groups()['accountGroups']:
            ida_s.append(account_group['aid'])
        ida_s.append('primary')
        return ida_s
    except Exception as e:
        logging.error(f"Failed to get the test data from ThousandEyes API. Error: {e}")
        return ''

print(get_all_tests())
# tests_by_accounts = {}
# for account_group in get_account_groups()['accountGroups']:
#     tests_by_accounts[account_group['aid']] = get_all_tests_by_aid(account_group['aid'])['test']
# tests_by_accounts['primary'] = get_all_tests()['test']
#
#
# # Webhook URL
# url = "https://winter-moon-1900.tines.com/webhook/optica/"
# print(send_to_tines_webhook(url, config.settings.tines_webhook_secret, tests_by_accounts))