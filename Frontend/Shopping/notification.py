from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import amqp_connection 
import json 
import pika

app = Flask(__name__)

# HTTP GET all the shopping items from shopping cart {listingID}

# 1. Items sent to Payment for confirmation 

# 2. AMQP message sent to Notifcation(consumer) ; direct message type

notification_queue_name = "Notification"

def receiveNotification(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=notification_queue_name, on_message_callback=callback, auto_ack=True)
        print('notification: Consuming from queue:', notification_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"notification: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("notification: Program interrupted by user.") 
        
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\notification: Received a payment log by " + __file__)
    processPaymentLog(json.loads(body))
    print()

def processPaymentLog(order):
    print("notification: Recording an order log:")
    print(order)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("notification: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("notification: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)
