import json

import boto3
import time
import logging

import config.settings
from src.main import get_account_groups, get_all_tests, get_all_group_ids, get_all_tests_by_aid

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message_to_queue(sqs, message_body):
    try:
        response = sqs.send_message(
            QueueUrl='optica-queue-out',
            MessageBody=message_body,
        )
        logging.info('Message sent. Message ID:', response['MessageId'])
    except Exception as e:
        logging.error("Failed to send message: %s", e)


def prepare_and_send_message(message):
    print("Received message: ", message)
    ac_groups_ids = get_all_group_ids()
    try:
        if 'key' in message and 'body' in message:
            if message['key'].lower() == 'tines' and message['body']=='ready':
                send_message_to_queue(sqs, json.dumps(ac_groups_ids))
            elif message['key'].lower() == 'tines' and message['body'].lower()=='primary':
                send_message_to_queue(sqs, json.dumps(get_all_tests()))
            elif message['key'].lower() == 'tines' and int(message['body']) in ac_groups_ids:
                send_message_to_queue(sqs, json.dumps(get_all_tests_by_aid(list(filter(lambda item: item == int(message['body']), ac_groups_ids))[0])))
            else:
                logging.error("Invalid choice: %s", message)
    except Exception as e:
        logging.error("Failed to process the message: %s", message)

session = boto3.Session(profile_name='eks-admin')
sqs = session.client('sqs')
queue_url = 'optica-queue'

while True:
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=0,
            WaitTimeSeconds=20
        )
        if 'Messages' in response:
            message = response['Messages'][0]
            body = json.loads(response['Messages'][0]['Body'])
            receipt_handle = message['ReceiptHandle']
            try:
                prepare_and_send_message(body)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle,
                )
                logging.info(f'Received and deleted message: {body}')
            except Exception as process_error:
                logging.error("Failed to process the message: %s", process_error)
        else:
            pass
    except Exception as e:
        logging.error("Error in receiving messages: %s", e)

    time.sleep(3)

