#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import pika

credentials = pika.PlainCredentials('admin','12345')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='dltask')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # 对message进行确认
    #ch.basic_ack(delivery_tag=method.delivery_tag)
print channel.basic_get(queue="dltask")[2]

channel.basic_consume(callback,
                      queue='dltask',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
#channel.start_consuming()
