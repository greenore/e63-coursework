# Libraries
from __future__ import print_function
import sys
import time
import itertools

import findspark
findspark.init("/home/tim/spark")

from kafka import KafkaProducer

# __name__
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    broker_list, topic = sys.argv[1:]
    producer = KafkaProducer(bootstrap_servers=broker_list)

    # Open file
    file = open('/home/tim/e63/orders.txt')
    rdd_file = file.read()
    rdd_split = rdd_file.split('\n')

    # Loop trough file (the orders file has 500'000 rows)
    for batch in range(500):
        print('Start batch #' + str(batch))
        for i in range(1000):
            place = i + (batch * 1000)
            print(rdd_split[place])
            producer.send(topic, rdd_split[place].encode())
        print('Finish batch #' + str(batch))
        print('Sleep 1 second')
        time.sleep(1)

    # End
    print('Finished!')
    