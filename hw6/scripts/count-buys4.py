# Libraries
from __future__ import print_function
import findspark
findspark.init("/home/tim/spark")
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# Build session
spark = SparkSession.builder.appName("StructuredCountBuys").getOrCreate()

# Defina schema
schema = StructType([StructField('time', TimestampType(), True),
                     StructField('orderId', IntegerType(), True),
                     StructField('clientId', IntegerType(), True),
                     StructField('symbol', StringType(), True),
                     StructField('amount', IntegerType(), True),
                     StructField('price', FloatType(), True),
                     StructField('buy', StringType(), True)])


lines = spark.readStream.csv("/home/tim/e63-coursework/hw6/data/input/", schema=schema, sep=',')
buys = lines.withWatermark("time", "1 minutes").groupBy("buy", window("time", "1 seconds")).count()
buys.writeStream.queryName("aggregates").outputMode("complete").format("console").start().awaitTermination()




#buys = lines.withWatermark("time", "1 minutes").groupBy(window(lines.time, "1 seconds"), lines.buyOrSell).count()


# Create schema
#df_stocks = spark.readStream.schema(myschema).csv("/home/tim/e63-coursework/hw6/data/input/")
#query = df_stocks.writeStream("/home/tim/e63-coursework/hw6/data/output/")
#query.awaitTermination()


# lines = spark.readStream.csv("/home/tim/e63-coursework/hw6/data/input/", schema=myschema, sep=',')

#fileStreamDf = spark.readStream.option("header", "False").schema(schema).csv("/home/tim/e63-coursework/hw6/data/input/")

#query = fileStreamDf.writeStream.format("console").outputMode(OutputMode.Append()).start()
      
      
#buys = lines.withWatermark("time", "1 minutes").groupBy(window(lines.time, "1 seconds"), lines.buyOrSell).count()
#lines.writeStream.format("console").start()
#lines.awaitTermination()
