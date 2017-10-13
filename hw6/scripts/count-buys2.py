from __future__ import print_function
import findspark
findspark.init("/home/tim/spark")
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

from pyspark.streaming import StreamingContext

# Create Session
spark = SparkSession.builder.master("local") \
                    .appName("SparkStreamingCountBuys").getOrCreate()


# Create schema
schemaString = "date OrderId Client Id Stocksymbol NoStockTraded Price ByOrSell"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
filestream = spark.readStream.format("csv").option("sep", ",").schema(schema).load("file:////home/tim/e63-coursework/hw6/data/input/")

filestream.show(5)
df_chunk = spark.read.csv("/home/tim/e63-coursework/hw6/data/input/chunkaa")
df_chunk.show(5)

val df = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").option("inferSchema", "true").option("delimiter", '|').load("/path/to/file.csv")






filestream = scc.textFileStream("/home/tim/e63-coursework/hw6/data/input/")




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

