# Import findspark
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark import SparkConf, SparkContext

# Load Spark
conf = SparkConf().setMaster("local") \
                  .setAppName("p5_rdd_count")
sc = SparkContext(conf = conf)

# Load data
rdd_ulysses = sc.textFile("/home/tim/e63-coursework/hw3/data/ulysses10.txt")

# Map and reduce data
rdd_word_count = rdd_ulysses.flatMap(lambda x: x.split()) \
                            .map(lambda x: (x, 1)) \
                            .reduceByKey(lambda x, y : x + y) \
                            .map(lambda x : x[1])

# Print data
print "Total word count:"
print rdd_word_count.sum()
sc.stop()
