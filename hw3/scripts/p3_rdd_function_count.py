# Import findspark
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("p3_rdd_function")
sc = SparkContext(conf = conf)

# Define function
def has_word_in(line):
    return ("night" in line or "morning" in line or "afternoon" in line)

rdd_lines = sc.textFile("file:///home/tim/e63-coursework/hw3/data/ulysses10.txt")
rdd_linematch = rdd_lines.filter(has_word_in)

print "Number of lines with 'morning', 'afternoon', 'night':"
print rdd_linematch.count()
sc.stop()
