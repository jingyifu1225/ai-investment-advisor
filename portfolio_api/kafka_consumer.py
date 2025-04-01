from confluent_kafka import Consumer, KafkaException, KafkaError
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "ai-investment")

consumer_config = {
    'bootstrap.servers': KAFKA_BROKER_URL,
    'group.id': 'investment-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])


def consume_from_kafka():
    print(f" Kafka Consumer received from:  {KAFKA_TOPIC}...")

    try:
        while True:
            msg = consumer.poll(5.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError.PARTITION_EOF:
                    print(f"Reached end of partition {msg.partition()}")
                else:
                    print(f"Kafka Error: {msg.error()}")
                    continue

            print(f" Received message: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("Consumer stopped")
    finally:
        consumer.close()


if __name__ == "__main__":
    consume_from_kafka()
