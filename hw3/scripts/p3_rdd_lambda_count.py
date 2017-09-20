import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")

from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local").setAppName("p3_rdd_lambda")
sc = SparkContext(conf = conf)

rdd_lines = sc.textFile("file:///home/tim/e63-coursework/hw3/data/ulysses10.txt")

rdd_filt_words = rdd_lines.filter(lambda line: "night" in line or "morning" in line or "afternoon" in line)

print "Number of lines with 'morning', 'afternoon', 'night':"
print rdd_filt_words.count()
sc.stop()
