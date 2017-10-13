# Load libraries
from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Exit condition
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: stateful_network_wordcount.py <hostname> <port>", file=sys.stderr)
        exit(-1)
    
    # Load Sparkcontext
    sc = SparkContext(appName="PythonStreamingStatefulNetworkWordCount")
    ssc = StreamingContext(sc, 3)
    ssc.checkpoint("checkpoint")

    # Define update function
    def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

    # Load data
    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    
    # Map and filter data
    running_counts = lines.flatMap(lambda line: line.split(" "))\
                          .filter(lambda x: x.startswith("a") or x.startswith("b"))\
                          .map(lambda word: (word, 1))\
                          .updateStateByKey(updateFunc)
    
    # Print data
    running_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
