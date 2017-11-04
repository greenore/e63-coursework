# Libraries
from __future__ import print_function
from operator import add, sub
import sys

import findspark
findspark.init("/home/tim/spark")

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime

# Parse function
def parse_data(line):
    s = line.rstrip().split(",")
    try:
        if s[6] != "B" and s[6] != "S":
            raise Exception('Wrong format')
        return [
            {"time": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"),
             "orderId": int(s[1]), "clientId": int(s[2]),
             "symbol": s[3], "amount": int(s[4]), "price": float(s[5]),
             "buy": s[6] == "B"}]
    except Exception as err:
        print("Wrong line format (%s): " % line)
        return []

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_consumer3.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)
    
    # Get brokers and topic
    broker_list, topic = sys.argv[1:]

    # Open spark context
    conf = SparkConf().setAppName("PythonStreamingDirectKafkaWordCount")
    conf = conf.setMaster("local[2]")
    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    ssc = StreamingContext(sc, 2)

    # Open kafka stream
    kvs = KafkaUtils.createDirectStream(ssc, [topic],
                                        {"metadata.broker.list": broker_list})
    filestream = kvs.transform(lambda rdd: rdd.values())
    
    # Parse file
    rdd_orders = filestream.flatMap(parse_data)

    # Sum buys (1) and sells (0)
    result = rdd_orders.map(lambda x: (x['symbol'], x['buy'])).reduceByKey(add)
    
    # Print result
    result.pprint()

    ssc.start()

ssc.awaitTermination()