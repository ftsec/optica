import json
import requests
from object.object import validate_test_data
import boto3
from botocore.exceptions import ClientError
BASE_URL = "https://api.thousandeyes.com/v6"
import log_config
logger = log_config.logger
def get_te_secret():
    secret_name = 'thousandeyesbearertoken'# nosec
    region_name = "us-west-2" # nosec

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.info("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logger.info("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logger.info("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            logger.info("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            logger.info("An error occurred on service side:", e)
    else:
        if 'SecretString' in get_secret_value_response:
            return  get_secret_value_response['SecretString']
        return None

# Session setup
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {get_te_secret()}",
    "Content-Type": "application/json"
})
def send_request(path, params=None):
    url = f"{BASE_URL}/{path}"
    try:
        response = session.get(url, timeout=30, params=params)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Request failed for {url}. Error: {e}")
        return None

def get_all_tests():
    try:
        response = send_request('tests.json')
        if response:
            tests = [json.loads(validate_test_data(test)) for test in response.json()['test']]
            return json.dumps(tests)
    except Exception as e:
        logger.error(f"Failed to process test data. Error: {e}")
    return None

def get_all_tests_by_aid(aid):
    logger.info(f"Retrieving tests for account group: {aid}")
    try:
        response = send_request('tests.json', params={'aid': aid})
        if response:
            tests = [json.loads(validate_test_data(test)) for test in response.json()['test']]
            return json.dumps(tests)
    except Exception as e:
        logger.error(f"Failed to retrieve test data for account group {aid}. Error: {e}")
    return None

def get_account_groups():
    try:
        return send_request('account-groups.json').json()
    except Exception as e:
        logger.error(f"Failed to retrieve account group data. Error: {e}")
        return None

def get_all_group_ids():
    try:
        account_groups = get_account_groups()
        if account_groups:
            return [group['aid'] for group in account_groups['accountGroups']] + ['primary']
    except Exception as e:
        logger.error(f"Failed to retrieve account group IDs. Error: {e}")
    return []


