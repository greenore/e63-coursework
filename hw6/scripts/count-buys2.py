# Libraries
from __future__ import print_function
import findspark
findspark.init("/home/tim/spark")
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Start context
sc = SparkContext(appName="SparkStreamingCountBuys")
ssc = StreamingContext(sc, 3)
ssc.checkpoint("checkpoint")
filestream = ssc.textFileStream("/home/tim/e63-coursework/hw6/data/input/")

from datetime import datetime
def parseOrder(line):
  s = line.split(",")
  try:
      if s[6] != "B" and s[6] != "S":
        raise Exception('Wrong format')
      return [{"time": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"), "orderId": long(s[1]), "clientId": long(s[2]), "symbol": s[3],"amount": int(s[4]), "price": float(s[5]), "buy": s[6] == "B"}]
  except Exception as err:
      print("Wrong line format (%s): " % line)
      return []

orders = filestream.flatMap(parseOrder)

# Generate (symbol, volume) pairs for each micro-batch
from operator import add
numPerType = orders.map(lambda o: (o['buy'], 1L)).reduceByKey(add)

numPerType.repartition(1).saveAsTextFiles("/home/tim/e63-coursework/hw6/data/output/output")

ssc.start()
ssc.awaitTermination()
