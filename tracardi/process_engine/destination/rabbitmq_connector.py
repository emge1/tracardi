from .connector import Connector
from kombu import Connection

from ...service.rabbitmq.queue_config import QueueConfig
from ...service.rabbitmq.queue_publisher import QueuePublisher
from ...service.rabbitmq.rabbit_configuration import RabbitConfiguration


class RabbitMqConnector(Connector):

    async def run(self, data, delta):

        credentials = self.resource.credentials.test if self.debug is True else self.resource.credentials.production
        configuration = RabbitConfiguration(**credentials)

        if 'queue' not in self.destination.destination.init:
            raise ValueError("Missing queue config.")

        settings = QueueConfig(**self.destination.destination.init['queue'])

        with Connection(configuration.uri, connect_timeout=configuration.timeout) as conn:
            queue_publisher = QueuePublisher(conn, queue_config=settings)
            queue_publisher.publish(data)
