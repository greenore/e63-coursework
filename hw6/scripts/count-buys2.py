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

# Define schema
schema = StructType([StructField('time', TimestampType(), True),
                     StructField('orderId', IntegerType(), True),
                     StructField('clientId', IntegerType(), True),
                     StructField('symbol', StringType(), True),
                     StructField('amount', IntegerType(), True),
                     StructField('price', FloatType(), True),
                     StructField('buy', StringType(), True)])

# Read stream
df_stockmarket = spark.readStream.csv("/home/tim/e63-coursework/hw6/data/input/",
                                      schema=schema, sep=',')

# Group by (with watermark and window)
df_buys = df_stockmarket.withWatermark("time", "1 minutes") \
                        .groupBy("buy", window("time", "1 seconds")) \
                        .count()

# Write stream
df_buys.writeStream.queryName("aggregates") \
       .outputMode("complete") \
       .format("console") \
       .start() \
       .awaitTermination()
