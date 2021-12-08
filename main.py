import boto3
import logging
import os

from json import dumps
from botocore.exceptions import ClientError
from uuid import uuid4

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
boto3.set_stream_logger('botocore', level='INFO')
sqs = boto3.resource(
    'sqs', 
    # aws_access_key_id=None, 
    # aws_secret_access_key=None, 
    endpoint_url='http://localhost:9324', 
    # region_name="us-west-2"
)

class SQSApp():

    def __init__(self, queue_name='default') -> None:
        self.queue = self.get_queue_by_name(queue_name=queue_name)

    def get_queue_by_name(self, queue_name):
        try:
            queue = sqs.get_queue_by_name(QueueName=queue_name)
            logger.info("Got queue '%s' with URL=%s", queue_name, queue.url)
        except ClientError as error:
            logger.exception("Couldn't get queue named %s.", queue_name)
            raise error
        else:
            return queue
    
    def send_message(self, body):
        try:
            response = self.queue.send_message(
                MessageGroupId=str(uuid4()),
                MessageDeduplicationId=str(uuid4()),
                MessageBody=dumps(body),
            )
            # logger.info(response)
            return response
        except ClientError as error:
            logger.exception("Send message failed: %s", body)
        raise error

    def receive_message(self):
        return self.queue.receive_messages(
            MessageAttributeNames=['Messages'],
        )

    def delete_messages(self, messages):
        """
        Delete a batch of messages from a queue in a single request.

        :param queue: The queue from which to delete the messages.
        :param messages: The list of messages to delete.
        :return: The response from SQS that contains the list of successful and failed
                message deletions.
        """
        try:
            entries = [{
                'Id': str(ind),
                'ReceiptHandle': msg.receipt_handle
            } for ind, msg in enumerate(messages)]
            response = self.queue.delete_messages(Entries=entries)
            if 'Successful' in response:
                for msg_meta in response['Successful']:
                    logger.info("Deleted %s", messages[int(msg_meta['Id'])].receipt_handle)
            if 'Failed' in response:
                for msg_meta in response['Failed']:
                    logger.warning(
                        "Could not delete %s",
                        messages[int(msg_meta['Id'])].receipt_handle
                    )
        except ClientError:
            logger.exception("Couldn't delete messages from queue %s", self.queue)
        else:
            return response
        
    def delete_queue(self):
        return self.queue.delete()

# test the app here
def main():
    try:
        queue_name = "skill-assessments.fifo"
        app = SQSApp(queue_name=queue_name)
        app.send_message(body={"message":"Hello world"})
        
        try:
            more_messages = True
            while more_messages:
                messages = app.receive_message()
                # print(messages)
                for msg in messages:
                    logger.info("Received message: %s: %s", msg.message_id, msg.body)
                if not messages:
                    more_messages = False
        except ClientError as error:
            logger.exception("Couldn't receive messages from queue: %s", queue_name)
            raise error

    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()
