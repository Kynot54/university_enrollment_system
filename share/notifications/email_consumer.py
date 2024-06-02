#!/usr/bin/env python
import pika
from email.message import EmailMessage
import smtplib
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notifications', exchange_type='direct')

result = channel.queue_declare(queue='email_queue', durable=True)

channel.queue_bind(exchange='notifications', queue='email_queue', routing_key='email')

#Processing Specific to Email
def sendEmail(address, msg):
    message = EmailMessage()
    message.set_content(msg)
    message['Subject'] = "Notification, You have been enrolled in a class!"
    message['From'] = "noreply@enrollment.com"
    message['To'] = address
    with smtplib.SMTP('localhost', 8025) as smtp:
        smtp.send_message(message)
    print(f" [x] Sent \"{message['Subject']}\" to {address}")

def callback(ch, method, properties, body):
    body = json.loads(body.decode())
    if method.routing_key == "email":
        print(" [x] Received Message: %r" % body["msg"])
        sendEmail(body["address"], body["msg"])


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
