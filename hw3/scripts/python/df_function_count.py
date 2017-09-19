# Load libraries
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import split
from pyspark.sql.functions import explode

# Create Session
spark = SparkSession.builder.master("local").appName("spark session example").getOrCreate()

# Read data
df = spark.read.text("file:///home/tim/ulysses10.txt")

# Next split each of the line into words using split function. This will create
# a new DataFrame with words column, each words column would have array of words
# for that line.
wordsDF = df.select(split(df.value, " ").alias("words"))

# Next use explode transformation to convert the words array into a dataframe
# with word column. This is equivalent of using flatMap() method on RDD 
wordDF = wordsDF.select(explode(wordsDF.words).alias("word"))

# Now you have data frame with each line containing single word in the file.
# So group the data frame based on word and count the occurrence of each word.
wordCountDF = wordDF.groupBy("word").count()

# This is the code you need if you want to figure out 20 top most words in the file:
wordCountDF.filter(wordCountDF.word.isin("night", "morning", "afternoon")) \
  .orderBy("count", ascending=0).show(truncate = False)


