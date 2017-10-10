#Streaming frequency =1 sec; splitAndSend.sh freq=  3 secs. 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from datetime import datetime
from operator import add
import time


sc = SparkContext(appName="SparkStreaming__topSellingStocks_TimeModification") 
ssc = StreamingContext(sc, 1)
filestream = ssc.textFileStream("hdfs:///user/cloudera/splits")


def parseOrder(line):
  s = line.split(",") 
  try:
      if s[6] != "B" and s[6] != "S":
        raise Exception('Wrong format')
      return [{"time": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"), "orderId": long(s[1]), "clientId": long(s[2]),  
                     "symbol": s[3],  "amount": int(s[4]), "price": float(s[5]), "type": s[6] }]
  except Exception as err:
      print("Wrong line format (%s): " % line)
      return []



def volhigh(time,rdd):
  top1 = rdd.takeOrdered(1,lambda (x,y): -1*y)  
         #sort descending by num of sells/buys and pick 1; - return only keys 
         #=~ to zipWithindex 
  srdd = rdd.filter(lambda x: x in top1
              ).map(lambda x: (time.strftime('%x %X'),x[0][0],x[0][1],x[1])) 
         #lookup for the entire record to get (key,value)
         #add time   
  return srdd   



def savefunc(time,rdd):
   if(not rdd.isEmpty()):
    timesuffix = int(time.strftime('%s')) 
    filepath = "hdfs:///user/cloudera/out/out4/result"+"-"+str(timesuffix)
    rdd.repartition(1).saveAsTextFile(filepath)




stockvol = filestream.flatMap(parseOrder
                    ).map(lambda o: ((o['symbol'],o['type']), o['amount'])
                    ).reduceByKey(add) 
stockvol_highest = stockvol.transform(volhigh)
stockvol_highest.foreachRDD(savefunc)
    #saves all rdds in the dsream to HDFS 

ssc.start()
ssc.awaitTermination()



#>>each chunk returns ('10/08/17 08:20:54', u'BP', u'B', 42930)
