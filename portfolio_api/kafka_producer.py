from confluent_kafka import Producer
from django.conf import settings
import os
import sys
import django

# absolute path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings")
django.setup()

config = {
    'bootstrap.servers': getattr(settings, 'KAFKA_BROKER_URL', 'localhost:9092'),
    'acks': 'all'
}

producer = Producer(config)


def send_to_kafka(topic, key, value):
    try:
        producer.produce(topic, key=key, value=value)
        producer.flush()  # all queued messages to be sent
        print(f"Message sent to {topic}: key={key}, value={value}")
    except Exception as e:
        print(f" Kafka Failed: {e}")


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


if __name__ == "__main__":
    send_to_kafka("ai-investment", "test_key", "Hello Kafka!")
