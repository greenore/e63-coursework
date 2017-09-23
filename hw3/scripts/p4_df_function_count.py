# Import libraries
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark.sql import SparkSession

# Create Session
spark = SparkSession.builder.master("local") \
                    .appName("p4_df_filter_count").getOrCreate()

# Read data
df_ulysses = spark.read.text("/home/tim/e63-coursework/hw3/data/ulysses10.txt")

# Filter values
df_linematch = df_ulysses.filter(df_ulysses.value.contains('afternoon') |
                                 df_ulysses.value.contains('night') |
                                 df_ulysses.value.contains('morning'))

# Print data
print "Number of lines with 'morning', 'afternoon', 'night':"
print df_linematch.count()
