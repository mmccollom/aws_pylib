import boto3
from botocore.exceptions import ClientError


class Sqs(object):
    def __init__(self, name: str):
        self.client = boto3.resource('sqs')
        self.queue = self.client.get_queue_by_name(QueueName=name)

    def write_to_queue(self, message_body):
        """
        Writes a message to an SQS queue.

        Parameters
        ----------
        message_body : str
            The message to write to the queue.

        Returns
        -------
        str
            The message ID of the message that was written to the queue.
        """
        try:
            response = self.queue.send_message(
                MessageBody=message_body,
                MessageAttributes={}
            )
            return response.get('MessageId')
        except ClientError as error:
            print(f"Send message failed: {message_body}")
            raise error
