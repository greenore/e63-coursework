# Import findspark
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark import SparkConf, SparkContext

# Configuration
conf = SparkConf().setMaster("local") \
                  .setAppName("p5_rdd_count")

# Load Spark
sc = SparkContext(conf = conf)

# Load data
rdd_lines = sc.textFile("file:///home/tim/e63-coursework/hw3/data/ulysses10.txt")

# Map and reduce data
rdd_counts = rdd_lines.flatMap(lambda x: x.split(" ")) \
                      .map(lambda x: (x, 1)) \
                      .reduceByKey(lambda x, y : x + y) \
                      .map(lambda x : x[1]).sum()

# Print
print "Total word count:"
print rdd_counts
sc.stop()
