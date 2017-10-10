from __future__ import print_function
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from datetime import datetime
from operator import add
from kafka import *
from pyspark.streaming.kafka import KafkaUtils
import sys, time






def parseOrder(line):   
  s = line.split(",")
  try:
      if s[6] != "B" and s[6] != "S":
          raise Exception('Wrong format')
      return [{"time": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"), "orderId": long(s[1]), "clientId": long(s[2]),
               "symbol": s[3],
               "amount": int(s[4]), "price": float(s[5]), "type": s[6]}]
  except Exception as err:
      print("Wrong line format (%s): " % line)
      return [] 



def volhigh(time, rdd):
	top1 = rdd.takeOrdered(1, lambda (x, y): -1 * y)  
	srdd = rdd.filter(lambda x: x in top1).map(lambda x: (time.strftime('%x %X'),x[0][0],x[0][1],x[1]))

	return srdd



def savefunc(time, rdd):
   if (not rdd.isEmpty()):  
       timesuffix = int(time.strftime('%s'))
       filepath = "hdfs:///user/cloudera/out/out5/result" + "-" + str(timesuffix)
       rdd.repartition(1).saveAsTextFile(filepath)
       print(str(time.strftime('%x %X')) + '...saving hdfs' )
       #saves to hdfs
 


def saveOfunc(time, rdd):
   if (not rdd.isEmpty()): 
       timesuffix = time.strftime('%x %X')
       print(str(timesuffix) + '...' + str(rdd.count()))
  

 

if __name__ == "__main__":
 if len(sys.argv) != 3:
    print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
    exit(-1)


 conf = SparkConf().setAppName("Kafka_streaming")
 conf = conf.setMaster("local[5]")
 sc = SparkContext(appName="Kafka_streaming")
 ssc = StreamingContext(sc, 1)
 brokers, topic = sys.argv[1:]
 	#pass broker host name and topic name as arguments 



 filestream = KafkaUtils.createDirectStream(
 			ssc, [topic], {"metadata.broker.list": brokers})
 		#createDirectStream() to fetch data from topic 
 print('starting streaming:'+str(datetime.now())) 




 stockvol = filestream.map(lambda x: x[1]
			).flatMap(lambda x: [line for line in x.splitlines()]
			).flatMap(parseOrder
			).map(lambda o: ((o['symbol'], o['type']), o['amount'])) 
			#process dstream , pick value as kafka sends (key,value); 
			#split data into lines/rows; format row , select columns 
			#required & create tuple ((Symbol , type),amount) 
			#to further reduce aggregating by key   		      



 noofrecords = filestream.map(lambda x: x[1]
 			).flatMap(lambda x: [line for line in x.splitlines()]
			).flatMap(parseOrder
			).map(lambda o: ((o['symbol'], o['type']), o['amount'])) 
 noofrecords.foreachRDD(saveOfunc)
	#to keep track of records' num received from Kakfa, for logging purpose



 stockvol_window = stockvol.window(10,10)
 stockvol_aggr = stockvol_window.reduceByKey(add)
  	#Create   dtream window duration/sliding to collects RDDs in it



 stockvol_highest = stockvol_aggr.window.transform(volhigh)
 stockvol_highest.foreachRDD(savefunc)
	 #Transform window dstream to find highest trade volume stock 
	 #in each rdd of window batch and save to hdfs



 sc.setCheckpointDir("hdfs:///user/cloudera/checkpoint/")
 ssc.start()

ssc.awaitTermination()
