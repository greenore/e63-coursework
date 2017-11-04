from kafka import KafkaProducer
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_producer.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    broker_list, topic = sys.argv[1:]

    producer = KafkaProducer(bootstrap_servers=broker_list)

    for batch in range(3):
           print('Starting batch #' + str(batch))
           for i in range(4):
                   print('sending message #' + str(i))
                   message = 'test message #' + str(i)
                   producer.send(topic, value=message.encode())
           print('Finished batch #' + str(batch))
           print('Sleeping for 5 seconds ...')
           time.sleep(5)

    print('Done sending messages')