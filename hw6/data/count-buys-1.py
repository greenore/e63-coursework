from __future__ import print_function
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
sc = SparkContext(appName="SparkStreamingCountBuys") 
ssc = StreamingContext(sc, 9)
filestream = ssc.textFileStream("hdfs:///user/cloudera/input")

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

from operator import add
numPerType = orders.map(lambda o: (o['buy'], 1L)).reduceByKey(add)

numPerType.repartition(1).saveAsTextFiles("hdfs:///user/cloudera/output/output", "txt")

ssc.start()
ssc.awaitTermination()
# ssc.stop(False)

