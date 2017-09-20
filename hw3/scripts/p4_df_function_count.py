# Import libraries
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark.sql import SparkSession

# Create Session
spark = SparkSession.builder.master("local").appName("p4_df_filter_count").getOrCreate()

# Read data
tbl_ulysses = spark.read.text("file:///home/tim/e63-coursework/hw3/data/ulysses10.txt")

tbl_lines = tbl_ulysses.filter(tbl_ulysses.value.contains('afternoon') |
                               tbl_ulysses.value.contains('night') |
                               tbl_ulysses.value.contains('morning'))

print "Number of lines with 'morning', 'afternoon', 'night':"
print tbl_lines.count()
