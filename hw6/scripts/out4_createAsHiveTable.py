from pyspark import SparkContext,SparkConf
from pyspark.sql import Row , HiveContext


#sc = SparkContext(appName="readHDFS") 
conf = SparkConf().setMaster("local").setAppName("fromHdfsToHive")
sc = SparkContext(conf=conf)
hvcontext = HiveContext(sc)



ofiles = sc.wholeTextFiles("hdfs:///user/cloudera/out/out4/result-*/part-00000")
	#returns (filename,content)


ofiles_format = ofiles.map(lambda x: x[1]
	).map(lambda x: [line for line in x.splitlines()]
	).map(lambda x: x[0]
	).map(lambda x: tuple(x[1:-1].split(','))
	).map(lambda r: Row(dttime=r[0],symbol=r[1],txtype=r[2],totalvol=int(r[3])))



ofiles_df = hvcontext.createDataFrame(ofiles_format)			
ofiles_df.saveAsTable("stocks_Ordered")
			#save dataframe as a persistent Hive table


