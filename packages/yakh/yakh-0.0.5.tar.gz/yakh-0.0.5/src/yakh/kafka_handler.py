import datetime
import json
import logging
import os
import socket
from typing import Optional

from yakh.kafka_producers import KafkaProducerAsync, KafkaProducerSync


def _get_host_name() -> str:
    hostname = socket.gethostname()
    if hostname.endswith('.local'):
        hostname = hostname.replace('.local', '')

    return hostname


def _get_ip_address(hostname: str) -> str:
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:  # TODO Thrown if connected to a VPN, need a better way to get IP
        ip_address = ''

    return ip_address


# TODO Make config values
DT_FORMAT = '%Y-%m-%d %H:%M:%S,%f'
ENVIRONMENT_VARIABLE = 'ENV'


HOSTNAME = _get_host_name()
FQDN = socket.getfqdn()
IP_ADDRESS = _get_ip_address(HOSTNAME)
ENVIRONMENT = os.environ.get(ENVIRONMENT_VARIABLE)


class KafkaHandler(logging.Handler):

    def __init__(self,
                 brokers: str,
                 topic: str,
                 enrich_data: Optional[bool] = True,
                 synchronous: Optional[bool] = False,
                 username: Optional[str] = None,
                 password: Optional[str] = None):

        # Initialize the parent class
        super().__init__()
        self.setFormatter(logging.Formatter())

        # Store the arguments
        self.brokers = brokers
        self.topic = topic
        self.enrich_data = enrich_data
        self.synchronous = synchronous
        self.username = username
        self.password = password

        # Initialize the kafka producer
        producer_type = KafkaProducerSync if synchronous is True else KafkaProducerAsync
        self.producer = producer_type(self.brokers)

    def emit(self, record: logging.LogRecord):
        self.producer.send_buffered_messages()

        message = self._create_json_record(record)
        self.producer.send(self.topic, json.dumps(message))

    def _create_json_record(self, record: logging.LogRecord) -> dict:
        dt = datetime.datetime.fromtimestamp(record.created).strftime(DT_FORMAT)
        message = {'log_message': record.msg,
                   'unix_epoch': record.created,
                   'datetime': dt,
                   'level': record.levelname,
                   'process_name': record.processName,
                   'name': record.name}

        # Handle if an exception was thrown
        if record.exc_info is not None:
            stack_trace = self.formatter.formatException(record.exc_info)
            message['log_message'] = f'{record.msg}\n{stack_trace}'

        if self.enrich_data:
            message = self._enrich_log_record(message)

        return message

    @staticmethod
    def _enrich_log_record(json_record: dict) -> dict:
        json_record['environment'] = ENVIRONMENT
        json_record['hostname'] = HOSTNAME
        json_record['fqdn'] = FQDN
        json_record['ip_address'] = IP_ADDRESS

        return json_record

    def flush(self):
        self.producer.send_buffered_messages()
        self.producer.flush()

    def close(self):
        self.flush()
        super().close()
