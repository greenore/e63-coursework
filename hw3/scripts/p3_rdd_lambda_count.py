# Import libraries
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark import SparkContext, SparkConf

# Start session
conf = SparkConf().setMaster("local").setAppName("p3_rdd_lambda")
sc = SparkContext(conf = conf)

# Read data
rdd_ulysses = sc.textFile("/home/tim/e63-coursework/hw3/data/ulysses10.txt")

# Filter values
rdd_linematch = rdd_ulysses.filter(lambda line: "night" in line or "morning" in
                                  line or "afternoon" in line)

# Print data
print "Number of lines with 'morning', 'afternoon', 'night':"
print rdd_linematch.count()
sc.stop()
