import datetime
import logging
import os
import queue
import socket
from abc import ABC, abstractmethod
from typing import Optional

import confluent_kafka


DATETIME_FORMAT = '%Y%m%d_%H%M%S%f'
HOSTNAME = socket.gethostname()
PROCESS_ID = os.getpid()
UTF8 = 'utf-8'

# TODO make config value
MAX_BUFFER_SIZE = 10000


class AbstractKafkaProducer(ABC):

    def __init__(self,
                 brokers: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None):

        self.log = logging.getLogger(__name__)
        self.brokers = brokers
        self.username = username
        self.password = password
        self.producer = None

        # Create a buffer to hold messages that cannot be sent
        self.buffer = queue.Queue(MAX_BUFFER_SIZE)

    def get_common_config(self) -> dict:
        """
        Configuration values common to all Kafka producers.
        """

        kafka_config = {'bootstrap.servers': self.brokers,
                        'queue.buffering.max.ms': 200,
                        'message.send.max.retries': 5,
                        'retry.backoff.ms': 200,
                        'message.max.bytes': 104857600,
                        'delivery.timeout.ms': 20000,
                        'request.timeout.ms': 5000
                        }

        if self.username is not None and self.password is not None:
            if 'ssl' in self.brokers.lower():
                kafka_config['security.protocol'] = 'SASL_SSL'
            else:
                kafka_config['security.protocol'] = 'SASL_PLAINTEXT'

            kafka_config['sasl.mechanisms'] = 'PLAIN'
            kafka_config['sasl.username'] = self.username
            kafka_config['sasl.password'] = self.password
        else:
            kafka_config['security.protocol'] = 'PLAINTEXT'

        return kafka_config

    def flush(self):
        if self.producer is not None:
            self.producer.flush()

    @abstractmethod
    def _do_send(self, topic: str, msg: bytes, headers: dict) -> None:
        pass

    def send(self, topic: str, msg: str, message_id: Optional[str] = None) -> None:
        """
        Send a message to the kafka topic. The message is encoded to byte form before sending. The
        connection to kafka will be closed after the data is sent.

        :param topic: The name of the kafka topic to put the message on.
        :param msg: The data to put on the kafka topic. Assumes data is UTF-8
        :param message_id: Optional. Will be added to the header of the kafka message so a
                           message can be uniquely identified by a consumer or system the consumer
                           send the message to. If no value is supplied, then a message ID will
                           be generated for you.
        """

        self.send_bytes(topic, msg.encode(encoding=UTF8), message_id)

    def send_bytes(self, topic: str, msg: bytes, message_id: Optional[str] = None) -> None:
        """
        Send a message to the kafka topic. The connection to kafka will be closed after the data
        is sent.

        :param topic: The name of the kafka topic to put the message on.
        :param msg: The data to put on the kafka topic. Assumes data is bytes
        :param message_id: Optional. Will be added to the header of the kafka message so a
                           message can be uniquely identified by a consumer or system the consumer
                           send the message to. If no value is supplied, then a message ID will
                           be generated for you.
        """

        if message_id is None or len(message_id.strip()) == 0:
            message_id = self._generate_message_id()
        else:
            message_id = message_id.strip()

        headers = {'message_id': message_id}
        self._do_send(topic, msg, headers)

    @staticmethod
    def _generate_message_id() -> str:
        """
        Generate a unique message ID for Kafka. The ID will be unique all servers and processes
        running this code (assuming FQDNs are unique, since they should be).

        :return: A unique ID
        """

        now = datetime.datetime.today()
        dt = now.strftime(DATETIME_FORMAT)
        return f'{HOSTNAME}_{PROCESS_ID}_{dt}'

    def callback_handler(self, err: confluent_kafka.KafkaError, msg: confluent_kafka.Message):
        if err is not None:
            self.add_to_buffer(msg)

    def add_to_buffer(self, message: confluent_kafka.Message):
        try:
            self.buffer.put(item=message, block=False)
        except queue.Full as e:
            print(f'Failed to add message to the buffer, it is full')
            print(f'message = {message}')
            print(e)

    def send_buffered_messages(self):
        """
        Get all the buffered messages and then try to resend them. It is important to remove all
        the messages from the buffer first before resending as otherwise we could end up in an
        infinite loop where failed messages are added back to the buffer right after the fail.
        """

        # Get all the buffered messages into tmp_buf
        tmp_buf = []
        try:
            while self.buffer.qsize() > 0:
                message = self.buffer.get(block=False)
                tmp_buf.append(message)
        except queue.Empty:
            pass

        # Try resending
        for msg in tmp_buf:
            self.send_bytes(msg.topic(), msg.value())


class KafkaProducerAsync(AbstractKafkaProducer):
    """
    A utility for putting messages on kafka topics asynchronously.

    Be sure to manually call the flush() method when all messages have been sent to Kafka.
    """

    def __init__(self,
                 brokers: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Constructor. Initializes the Producer connection from details defined in the config file

        :param brokers: The brokers separated by commas
        """

        super().__init__(brokers, username, password)

        config = self.get_common_config()
        config['default.topic.config'] = {'request.required.acks': 0}
        self.producer = confluent_kafka.Producer(config)

    def _do_send(self, topic: str, msg: bytes, headers: dict):
        """
        Send a message to the kafka topic. The message is encoded to byte form before sending. The
        connection to kafka will be closed after the data is sent.

        :param topic: The name of the kafka topic to put the message on.
        :param msg: The data to put on the kafka topic. Assumes data is UTF-8
        :param headers: Kafka message headers
        """

        self.producer.produce(topic, msg, callback=self.callback_handler, headers=headers)


class KafkaProducerSync(AbstractKafkaProducer):
    """
    A utility for putting messages on kafka topics synchronously.
    """

    def __init__(self,
                 brokers: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """
        Constructor. Initializes the Producer connection from details defined in the config file

        :param brokers: The brokers separated by commas
        """

        super().__init__(brokers, username, password)

        config = self.get_common_config()
        config['default.topic.config'] = {'request.required.acks': 'all'}
        self.producer = confluent_kafka.Producer(config)

    def _do_send(self, topic: str, msg: bytes, headers: dict):
        """
        Send a message to the kafka topic. The message is encoded to byte form before sending. The
        connection to kafka will be closed after the data is sent.

        :param topic: The name of the kafka topic to put the message on.
        :param msg: The data to put on the kafka topic. Assumes data is UTF-8
        :param headers: Kafka message headers
        """

        self.producer.poll(0)
        self.producer.produce(topic, msg, callback=self.callback_handler, headers=headers)
        self.producer.flush()
