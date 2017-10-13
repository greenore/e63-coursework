# Libraries
from __future__ import print_function
import findspark
findspark.init("/home/tim/spark")
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

# Build session
spark = SparkSession.builder.appName("p4").getOrCreate()

# Defina schema
schemaString = "Date OrderId ClientId Stocksymbol NoStockTraded Price ByOrSell"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
myschema = StructType(fields)

# Create schema
df_stocks = spark.readStream.schema(myschema).csv("/home/tim/e63-coursework/hw6/data/input/")
query = df_stocks.writeStream("/home/tim/e63-coursework/hw6/data/output/")
query.awaitTermination()

