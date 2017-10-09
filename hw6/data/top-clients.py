from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="FindTopClients")
ssc = StreamingContext(sc, 5)
filestream = ssc.textFileStream("hdfs:///user/cloudera/input")

from datetime import datetime
def parseOrder(line):
  s = line.split(",")
  try:
      if s[6] != "B" and s[6] != "S":
        raise Exception('Wrong format')
      return [{"time": datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S"), "orderId": long(s[1]), "clientId": long(s[2]), "symbol": s[3],
      "amount": int(s[4]), "price": float(s[5]), "buy": s[6] == "B"}]
  except Exception as err:
      print("Wrong line format (%s): " % line)
      return []

orders = filestream.flatMap(parseOrder)
from operator import add
numPerType = orders.map(lambda o: (o['buy'], 1L)).reduceByKey(add)

amountPerClient = orders.map(lambda o: (o['clientId'], o['amount']*o['price']))

amountState = amountPerClient.updateStateByKey(lambda vals, totalOpt: sum(vals)+totalOpt if totalOpt != None else sum(vals))
top5clients = amountState.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False).map(lambda x: x[0]).zipWithIndex().filter(lambda x: x[1] < 5))

buySellList = numPerType.map(lambda t: ("BUYS", [str(t[1])]) if t[0] else ("SELLS", [str(t[1])]) )
top5clList = top5clients.repartition(1).map(lambda x: str(x[0])).glom().map(lambda arr: ("TOP5CLIENTS", arr))

finalStream = buySellList.union(top5clList)

finalStream.repartition(1).saveAsTextFiles("hdfs:///user/cloudera/output/output", "txt")

sc.setCheckpointDir("hdfs:///user/cloudera/checkpoint/")

ssc.start()
ssc.awaitTermination()
