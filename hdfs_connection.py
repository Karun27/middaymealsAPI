from kafka import KafkaProducer
from hdfs import InsecureClient
import sys
class someclass:
    def __init__(self,input_json):
      self.hdfs_host= input_json.get('host')
      self.hdfs_port = input_json.get('port')
      self.hdfs_user = input_json.get('user')
      self.bootstrap_servers = input_json.get('kafka')
      self.kafka_port = input_json.get('kafka_Port')
    def HDFSConnection(self):
      try:
	client = InsecureClient('http://' + self.hdfs_host + ':'+ str(self.hdfs_port) , user=self.hdfs_user)
	return True
      except:
	return False          

    def KafkaConnection(self):
      try:
       	producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers + ':' + str(self.kafka_port))
	return True
      except:
	return False
          

  
  


