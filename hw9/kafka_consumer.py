
from __future__ import print_function
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import logging
import sys
from kafka.errors import OffsetOutOfRangeError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main(broker_str, topic):
    #topic = "test3"
    group = "my-group1"
    #bootstrap_servers = ['localhost:9092']
    bootstrap_servers = [broker_str]

    print('Topic is: ', topic)
    print('Group is: ', group)

    # To consume latest messages and auto-commit offsets
    try:
        consumer = KafkaConsumer(
            group_id=group, bootstrap_servers=bootstrap_servers,
            auto_offset_reset="latest")
        consumer.subscribe([topic])
        
        while True:
            # Process messages
            try:
                k_msg = consumer.poll(timeout_ms=200)
            except OffsetOutOfRangeError:
                log.info("Offset out of range. Seeking to begining")
                # consumer.seek_to_beginning(tp)
                # You can save `consumer.position(tp)` to redis after this,
                # but it will be saved after next message anyway
            else:
                if k_msg:
                    for msgs in list(k_msg.values()):
                        for msg in msgs:
                            print('got msg: ', str(msg))
                            # Process message and increment offset
                            print('partition: ', msg.partition, 'message offset: ', msg.offset)

    except KafkaError as e:
        log.info('Got kafka error %s: %s' % (str(e), type(e)))
    except Exception as e:
        log.info('Got exception %s: %s' % (str(e), type(e)))
    else:
        log.info('No exception raised!')
    finally:
        consumer.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: kafka_consumer2.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)
    main(sys.argv[1], sys.argv[2])
