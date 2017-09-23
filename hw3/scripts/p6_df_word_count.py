# Import libraries
import findspark
findspark.init("/opt/spark-2.2.0-bin-hadoop2.7")
from pyspark.sql import SparkSession
from pyspark.sql.functions import split          # Function to split data
from pyspark.sql.functions import explode        # Equivalent to flatMap

# Create Session
spark = SparkSession.builder.master("local").appName("p6_df_count").getOrCreate()

# Read data
df_ulysses = spark.read.text("/home/tim/e63-coursework/hw3/data/ulysses10.txt")

# Split data
df_words = df_ulysses.select(split(df_ulysses.value, " ").alias("words"))

# Create one row per word
df_word = df_words.select(explode(df_words.words).alias("words"))

# Remove empy lines
df_word = df_word.filter('words != Null or words != ""')

# Output
print("Number of words: ")
print(df_word.count())
