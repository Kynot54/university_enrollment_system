#!/usr/bin/env python
import pika
import httpx
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notifications', exchange_type='direct')

result = channel.queue_declare(queue='webhook_queue', durable=True)

channel.queue_bind(exchange='notifications', queue="webhook_queue", routing_key='web_hook')

#Processing Specific to WebHook
def sendNotificationToWebHook(web_hook, msg):
    try:
        r = httpx.post(web_hook, data={"msg": msg})
        if r.status_code == 200:
            print(f" [x] Sent \"{msg}\" to {web_hook}")
    except httpx.HTTPStatusError as exc:
        print(f" [x] Failed with {exc.response.status_code} while requesting {exc.request.url!r}.")
    except httpx.RequestError as exc:
        print(f" [x] An error occurred while sending message to:{exc.request.url!r}.")

def callback(ch, method, properties, body):
    body = json.loads(body.decode())
    if method.routing_key == "web_hook":
        print(" [x] Received Message: %r" % body["msg"])
        sendNotificationToWebHook(body["address"], body["msg"])


channel.basic_consume(queue="webhook_queue", on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
