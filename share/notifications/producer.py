#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='notifications', exchange_type='direct')

def sendWebHook(web_hook, message):
    message = {
        "address":web_hook, 
        "msg":message
    }
    message_json = json.dumps(message).encode()
    channel.basic_publish(
                        exchange='notifications',
                        routing_key='web_hook',
                        body=message_json,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent Message {message.msg} to {message.address}")
    
def sendEmail(email, message):

    message = {
        "address":email, 
        "msg":message
    }
    message_json = json.dumps(message).encode()
    channel.basic_publish(
                        exchange='notifications',
                        routing_key='email',
                        body=message_json,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.DeliveryMode.Persistent
                        ))
    print(f" [x] Sent Message {message.msg} to {message.address}")
