from kafka import KafkaProducer
import socket    
import time    
import json 
import os
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()
config = dotenv_values(".env")
print(config)
s = socket.socket() 
HOST=os.getenv("HOST")
PORT= int(os.getenv("PORT"))         
s.connect((HOST, PORT))
bootstrap_servers= os.getenv("bootstrap_servers")
# topic_name= os.getenv("topicname")
topic_name="Device_data"
# bootstrap_servers=["scm-kafka-1:9092"]
producer=KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda m: json.dumps(m).encode("utf-8"),
         retries=5)
while True:
	try:
		data=s.recv(70240).decode()
		json_acceptable_string = data.replace("'", "\"")
		rec = json.loads(json_acceptable_string)
		for i in rec:
			producer.send(topic_name,i)
			print(i)
	except Exception as e:
		print(e)
s.close() 
        








