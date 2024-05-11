import json
import boto3
import time
from te_client import get_all_tests, get_all_group_ids, get_all_tests_by_aid
import log_config
logger = log_config.logger



def send_message_to_queue(sqs, message_body):
    try:
        response = sqs.send_message(
            QueueUrl='optica-queue-out',
            MessageBody=message_body,
        )
        logger.info("Message sent. Message ID: %s", response['MessageId'])
    except Exception as e:
        logger.error("Failed to send message: %s", e)
def prepare_and_send_message(message):
    ac_groups_ids = get_all_group_ids()
    try:
        if 'key' in message and 'body' in message:
            if message['key'].lower() == 'tines' and message['body']=='ready':
                send_message_to_queue(sqs, json.dumps(ac_groups_ids))
            elif message['key'].lower() == 'tines' and message['body'].lower()=='primary':
                tests =  get_all_tests()
                send_message_to_queue(sqs,json.dumps(tests))
                logger.info(tests) # allow loki capture for grafana dashboard test visibility
            elif message['key'].lower() == 'tines' and int(message['body']) in ac_groups_ids:
                tests= get_all_tests_by_aid(list(filter(lambda item: item == int(message['body']), ac_groups_ids))[0])# allow loki capture for grafana dashboard test visibility
                send_message_to_queue(sqs,json.dumps(tests))
                logger.info(tests)
            else:
                logger.error("Invalid choice: %s", message)
    except Exception as e:
        logger.error("Failed to process the message: %s", message)

session = boto3.Session()
sqs = session.client('sqs')
queue_url = 'optica-queue'
if __name__ == '__main__':
    logger.info('Starting the application')
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
                    logger.info(f'Received and deleted message: {body}')
                except Exception as process_error:
                    logger.error("Failed to process the message: %s", process_error)
            else:
                pass
        except Exception as e:
            logger.error("Error in receiving messages: %s", e)

        time.sleep(3)

