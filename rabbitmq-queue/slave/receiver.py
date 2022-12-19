import pika
import os
import socket
from subprocess import call
import json
import ast
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect() for UDP doesn't send packets
s.connect(('10.0.0.0', 0)) 
IPAddr = s.getsockname()[0]
print(IPAddr)
s.close()
url = "amqps://afwhnghs:uB2Nad64yb4U4oL5HRwlIEl8FDLCMmyd@puffin.rmq2.cloudamqp.com/afwhnghs"
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
queue_name="192.168.43.72"
channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    body1 = body.decode()
    print(body1)
    request = eval(body1)
    print(type(request))
    if request["IP"] == '192.168.43.72':
        type1 = request["type"]
        vm_name1 = request["vm_name"]
        os.environ['vm_name'] = vm_name1
        match type1:
            case "create_vm":
                rc = call("./vm_creation.sh")    
            case "run_task":
                rc = call("./task_driver.sh")
            case "getInfo":
                rc = call("./vmInfo.sh")
            case "checkResults":
                rc=call(['python3', 'taskResult.py'])
    print(" [x] Received " + str(body))


channel.basic_consume(queue_name,
                      callback,
                      auto_ack=True)
channel.start_consuming()
