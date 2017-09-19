# Import findspark
import findspark
findspark.init()

# Or the following command
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")

def hastod(line):
    return ("night" in line or "morning" in line or "afternoon" in line)

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MyApp")
sc = SparkContext(conf = conf)

lines = sc.textFile("file:///home/tim/ulysses10.txt")
linematch = lines.filter(hastod)

print "Number of lines with 'night', 'morning', 'afternoon' :"
print linematch.count()
sc.stop()
