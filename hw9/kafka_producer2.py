from kafka import KafkaProducer
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_producer2.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    broker_list, topic = sys.argv[1:]

    producer = KafkaProducer(bootstrap_servers=broker_list)

    for i in sys.stdin:
        message = 'typed message #' + str(i)
        producer.send(topic, value=message.encode())