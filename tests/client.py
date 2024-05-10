import pydantic_core
import requests, json

import config.settings
from config.settings import base_url, te_bearer_token, request_timeout
from .object.testObject import get_test_object, TestType
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, 'data')


headers = {"Authorization": f"Bearer {te_bearer_token}",
           "content-type": "application/json"}
te_session = requests.Session()

def send_get_request(path, method='GET'):
    try:
        if method == 'GET':
            return te_session.get(base_url + f'/{path}'
                                  , headers=headers
                                  , timeout=request_timeout)
    except Exception as e:
        return None

def test_te_api_reachability():
    response = send_get_request('tests.json')
    assert response.status_code == 200, f"Failed to reach ThousandEyes API. Status code: {response.status_code} with reasons {response.reason}"

def test_for_results_response():
    response = send_get_request('tests.json')

    assert 'test' in response.json(), f"Failed to get the test data from ThousandEyes API. Response: {response.text}"

def test_te_test_config_count():
    response = send_get_request('tests.json')
    assert len(response.json()['test']) == 4, f"expected 4 tests, but got {len(response.json()['test'])} tests"

def test_object_validation():
    # for te_test in te_test_response.json()['test']:
    with open(os.path.join(data_file_path,'te_sample_response.json'), 'r') as sample_data:
        sample_data = json.load(sample_data)
    for te_test in sample_data['test']:
        try:
            # ThousandEyesTestObject.model_validate(obj=te_test, strict=False)]
            get_test_object(te_test)
        except pydantic_core.ValidationError as e:
            assert False, f"Failed to validate the test object. Error: {e}"

def test_get_tests_by_type():
    test_type = [e.value for e in TestType]
    for test in test_type:
        te_test_response = send_get_request(f'tests/{test}.json')
        assert te_test_response.status_code == 200, f"Failed to get the test data from ThousandEyes API with test type {test}. Status code: {te_test_response.status_code} with reasons {te_test_response.reason}"
        assert 'test' in te_test_response.json(), f"Failed to get the test data from ThousandEyes API. Response: {te_test_response.text}"

# def test_get_test_by_id(test_id):
#     te_test_response = send_get_request(f'tests/{test_id}.json')
#     assert te_test_response.status_code == 200, f"Failed to get the test data from ThousandEyes API. Status code: {te_test_response.status_code} with reasons {te_test_response.reason}"


def test_get_account_groups():
    te_ag_response = send_get_request('account-groups.json')
    print(te_ag_response.json())
    assert te_ag_response.status_code == 200, f"Failed to get the account groups data from ThousandEyes API. Status code: {te_ag_response.status_code} with reasons {te_ag_response.reason}"
    assert 'accountGroups' in te_ag_response.json(), f"Failed to get the account groups data from ThousandEyes API. Response: {te_ag_response.text}"
    assert len(te_ag_response.json()['accountGroups']) >= 1, f"expected at least 1 account group, but got {len(te_ag_response.json()['accountGroup'])} account groups"
    account_group_ids = [ag['aid'] for ag in te_ag_response.json()['accountGroups']]
    assert set(account_group_ids) == set(config.settings.aids), f"expected account group ids: {set(config.settings.aids)}, but got {account_group_ids}"


