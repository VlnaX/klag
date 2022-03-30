#!/usr/bin/python3
# 2022 (c) ~VlNa~
# See: https://localcoder.org/aug-2019-kafka-consumer-lag-programmatically
#      https://buildmedia.readthedocs.org/media/pdf/kafka-python/master/kafka-python.pdf
#      https://towardsdatascience.com/3-libraries-you-should-know-to-master-apache-kafka-in-python-c95fdf8700f2
# required: python3, kafka-python module
# Use:
#     python3 klags.py host[:port] [consumerGroupID]
#     - with no consumerGroupID program will display consumer groups available on host (broker) and user can choose
#

from kafka import KafkaAdminClient, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import sys, traceback

if len(sys.argv) < 2:
  print (f"{sys.argv[0]} - display consumer groups and lags")
  print (f" Use: {sys.argv[0]} host[:port] [consumerGroup]")
  sys.exit(1)

slist = []       # sorted list of groups
ugrp  = ""       # group name from command line
onRow = 1        # display N groups on row ()
# ZL 
#server="contstor01:9192" 
 
server = sys.argv[1]
if len(sys.argv) > 2:
  ugrp = sys.argv[2] 

try:
  client = KafkaAdminClient(bootstrap_servers=server)

  groups = client.list_consumer_groups()
  for g in groups:
    if g[1] == 'consumer':
      slist.append(g[0])
    
  if len(slist):
    slist = sorted(slist)

    if len(ugrp):
      if not ugrp in slist:
        client.close()   
        print(f" Error: Not such consumer group ID ({ugrp}) found.")
        sys.exit(1)        
    else:
      print (" Consumer groups:")
      for i in slist:
        print (f"  [{slist.index(i):3d}]: {i:74s}", end = '')
        if not (slist.index(i)+1)%onRow: print ("\n", end = '')                 

      while True:    
        choose = input("\nChoose group number (q-quit): ")
        if choose.isnumeric()  and  int(choose) >= 0  and  int(choose) < len(slist):
          break
        if choose == 'q':
          client.close()   
          sys.exit(0)      
  else: 
    client.close()   
    print(" Info: No consumer groups found.")
    sys.exit(0)
  
  if len(ugrp):
    group = ugrp
  else:
    group = slist[int(choose)]
     
  offsets = client.list_consumer_group_offsets(group)
  client.close()
except NoBrokersAvailable:
  print ("Error: Wrong servername or port. No brokers available.")
  sys.exit(1)
except Exception as e:
  try:
    client
    client.close()
  except:
    pass
  traceback.print_exc()
  sys.exit(1)

try:
  if offsets.keys():
    tps = offsets.keys()
    consumer = KafkaConsumer(bootstrap_servers=server, enable_auto_commit=False, group_id=group)

    print (f" Consumer group: {group}")
    for tp in tps:
      consumer.assign([tp])
      committed = consumer.committed(tp) 
      consumer.seek_to_end(tp)  
      last_offset = consumer.position(tp)
      if last_offset != None and committed != None:
        lag = last_offset - committed
        print (f"  topic: {tp[0]:46s} partition: {tp[1]:2d}\t end: {last_offset:<8,d}\t offset: {committed:<8,d}\t lag: {lag:<8,d}")

    consumer.close(autocommit=False)
except Exception as e:
  try:
    consumer
    consumer.close(autocommit=False)
  except:
    pass
  traceback.print_exc()
  sys.exit(1)
