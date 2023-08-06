from kombu import Connection, Exchange, Queue, Producer

from tracardi_rabbitmq_publisher.model.queue_config import QueueConfig
from tracardi_rabbitmq_publisher.service.queue_publisher import QueuePublisher

# rabbit_url = "amqp://localhost:5672/"
#
# with Connection(rabbit_url) as conn:
#
#     channel = conn.channel()
#
#     exchange = Exchange("example-exchange", type="direct")
#
#     producer = Producer(exchange=exchange, channel=channel, routing_key="BOB")
#
#     queue = Queue(name="example-queue", exchange=exchange, routing_key="BOB")
#     queue.maybe_bind(conn)
#     queue.declare()
#
#     producer.publish({"a":"Hello there!"})


queue = QueueConfig(
    name='xxx',
    routing_key='xxxd'
)
payload = {"c": 1}
with Connection('amqp://localhost:5672/') as conn:
    channel = conn.channel()
    print(queue.queue_type)
    exchange = Exchange("xxxz", queue.queue_type)
    print(queue.name)
    print(queue.routing_key)
    queue = Queue(name=queue.name, exchange=exchange, routing_key=queue.routing_key)
    queue.maybe_bind(conn)
    queue.declare()
    producer = Producer(exchange=exchange, channel=conn.channel(), routing_key=queue.routing_key, serializer='json', auto_declare=True)
    producer.publish(payload)