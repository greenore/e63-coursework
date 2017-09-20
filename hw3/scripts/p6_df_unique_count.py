# Import libraries
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark.sql import SparkSession
from pyspark.sql.functions import split   # Function to split data
from pyspark.sql.functions import explode # Equivalent to flatMap

# Create Session
spark = SparkSession.builder.master("local").appName("p6_df_count").getOrCreate()

# Read data
df = spark.read.text("file:///home/tim/e63-coursework/hw3/data/ulysses10.txt")

# First we're spliting each of the lines into words using the split function.
# This will create a new dataframe with the words column, each words column
# has an array of words for that line.
words_df = df.select(split(df.value, " ").alias("words"))

# Next we're using the explode function to convert the words array into
# a dataframe with word column. This is equivalent of using flatMap() method on RDD 
word_df = words_df.select(explode(words_df.words).alias("word"))

# Get unique words
word_count_df = word_df.groupBy("word").count()

print("Number of unique words: ")
print(word_count_df.count())
