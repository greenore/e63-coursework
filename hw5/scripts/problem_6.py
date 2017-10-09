# Load libraries
from pyspark.sql.types import *
from pyspark.sql import SQLContext, HiveContext, Row
from pyspark import SparkConf, SparkContext, SQLContext
import re
from operator import add

# Spark configuration
conf = (
            SparkConf().setAppName("problem_6")
            .set("spark.executor.cores", 1)
            .set("spark.shuffle.compress", "true")
            .set("spark.executor.instances", 1)
            .set("spark.executor.memory", "4g")
            .set("spark.io.compression.codec", "snappy")
)

# Set context
sc = SparkContext().getOrCreate(conf = conf)
sc.setLogLevel("ERROR")
sqlContext = SQLContext(sc)
hivecontext = HiveContext(sc)

# Select statement
df_bible_freq = hivecontext.sql("SELECT freq, lower(word) word FROM kingjames WHERE lower(word) like 'w%' AND length(word) > 4 AND freq > 250 ORDER BY freq DESC")

# Print frequencies
print(df_bible_freq.show(20))
print(df_bible_freq.show.agg({"freq": "sum"}).show())
print("Number of words:")
print(df_bible_freq.count())
