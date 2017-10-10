from kafka import KafkaProducer
import sys, time
from datetime import datetime
from itertools import islice



producer = KafkaProducer(bootstrap_servers='localhost:9092')  
topic = 'lenaTopic1'

file_path = '/home/cloudera/hw5_data/orders.txt'
N = 1000
with open(file_path, 'rb') as infile:
    try:
        while True:
            lines_gen = islice(infile, N) 
            #To get N lines at a time instead of loading all file to memory
            blines = ""
            for line in lines_gen:
                blines += line      #Kafka only accept in bytes so 
                                    #need to concatenate line strings
            if len(blines.strip())>0:           #EOF check
             producer.send(topic,blines)
             print 'Sending to topic:' + str(datetime.now())
            else:
             break
            time.sleep(1)
    except Exception as e:
        print("Error:" + str(e))

print 'Done sending messages'