from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import amqp_connection 
import json 
import pika
from flask import request
from email.message import EmailMessage
import ssl
import smtplib


app = Flask(__name__)



# Creating send_email to send email (No use of API)

email_sender = 'lim263654@gmail.com'
email_password = 'mzktuipjgxecxhvw'
email_receiver = 'lim263654@gmail.com'

subject = "Try and Error"
body = """
Payment Successful 
"""


em = EmailMessage()
em['From'] = email_sender
em["To"] = email_receiver
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

# Create server and ?? 
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
    print("Email sent!")


if __name__ == '__main__':
    app.run(port=5892, debug=True)
    
    
    # notification_queue_name = "Notification"

# def receiveNotification(channel):
#     try:
#         # set up a consumer and start to wait for coming messages
#         channel.basic_consume(queue=notification_queue_name, on_message_callback=callback, auto_ack=True)
#         print('notification: Consuming from queue:', notification_queue_name)
#         channel.start_consuming()  # an implicit loop waiting to receive messages;
#              #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
#     except pika.exceptions.AMQPError as e:
#         print(f"notification: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

#     except KeyboardInterrupt:
#         print("notification: Program interrupted by user.") 
        
# def callback(channel, method, properties, body): # required signature for the callback; no return
#     print("\notification: Received a payment log by " + __file__)
#     processPaymentLog(json.loads(body))
#     print()

# def processPaymentLog(order):
#     print("notification: Recording an order log:")
#     print(order)

# if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
#     print("notification: Getting Connection")
#     connection = amqp_connection.create_connection() #get the connection to the broker
#     print("notification: Connection established successfully")
#     channel = connection.channel()
#     receiveNotification(channel)

# Function of sending email 
