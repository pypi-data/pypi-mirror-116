import logging

from kombu import Exchange, Queue

from tracardi_rabbitmq_publisher.model.queue_config import QueueConfig

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QueuePublisher:

    def __init__(self, conn, queue_config: QueueConfig):
        self.conn = conn
        self.queue_config = queue_config
        self.exchange = Exchange(queue_config.name, queue_config.queue_type, durable=queue_config.durable)
        self.queue = Queue(queue_config.name, exchange=self.exchange, routing_key=queue_config.routing_key)
        producer = self.conn.Producer(serializer='json', auto_declare=True)
        self.publisher = self.conn.ensure(producer, producer.publish, errback=self.error_reporter, max_retries=None)

    @staticmethod
    def error_reporter(exc, interval):
        print("error", exc)
        logger.info('Error: {}', str(exc))
        logger.info('Retry in %s seconds.', interval)

    def publish(self, payload):
        self.publisher(payload,
                       retry=True,
                       exchange=self.exchange, routing_key=self.queue_config.routing_key,
                       declare=[self.queue])  # , compression='bzip2'
