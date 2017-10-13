







spark.readStream

lines = spark.readStream.format("socket").option("host", "localhost") \
.option("port", 9999).load()



I would need to see your schema. Here the idea :
  
  1) define Schema for the input rows

2) spark = SparkSession.....with builder.appName.getOrCreate()

3) Create DataFrame representing the stream of input files, like spark.readStream...

4) Count the buys / sells in the window using the timestamp as a watermark.





from pyspark.sql.functions import explode
from pyspark.sql.functions import split


lines = spark.readStream.format("socket").option("host", "localhost") \
.option("port", 9999).load()

# Split the lines into words
words = lines.select( explode( split(lines.value, " ")).alias("word"))

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts.writeStream.outputMode("complete").format("console") \
.start()

query.awaitTermination()






# Start context
sc = SparkContext(appName="SparkStreamingCountBuys")
ssc = StreamingContext(sc, 3)
ssc.checkpoint("/home/tim/checkpoint")
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

















from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession.builder.appName("StructuredNetworkWordCount").getOrCreate()

lines = spark.readStream.format("socket").option("host", "localhost") \
.option("port", 9999).load()

# Split the lines into words
words = lines.select( explode( split(lines.value, " ")).alias("word"))

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts.writeStream.outputMode("complete").format("console") \
.start()

query.awaitTermination()













from __future__ import print_function

import sys
import findspark
findspark.init("/home/tim/spark")

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
  if len(sys.argv) != 3:
  print("Usage: network_wordcount.py <hostname> <port>", file=sys.stderr)
exit(-1)
sc = SparkContext(appName="PythonStreamingNetworkWordCount")
ssc = StreamingContext(sc,3 )

lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
counts = lines.flatMap(lambda line: line.split(" "))\
.map(lambda word: (word, 1))\
.reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
ssc.awaitTermination()





from __future__ import print_function
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# sc = SparkContext(appName="SparkStreamingCountBuys") 
# ssc = StreamingContext(sc, 9)
filestream = ssc.textFileStream("hdfs://quickstart.cloudera:8020/user/cloudera/input")

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

numPerType.repartition(1).saveAsTextFiles("hdfs://quickstart.cloudera:8020/user/cloudera/output/output", "txt")

ssc.start()
ssc.awaitTermination()
# ssc.stop(False)


