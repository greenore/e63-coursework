# Import findspark
import findspark
findspark.init()

# Or the following command
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")

from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf = conf)

lines = sc.textFile("file:///home/tim/ulysses10.txt")
tofday  = lines.filter(lambda line: "night" in line or "morning" in line or "afternoon" in line)
print "Number of lines with 'night', 'morning', 'afternoon' :"
print tofday.count()
sc.stop()
