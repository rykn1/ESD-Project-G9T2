from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import amqp_connection 
import json 
import pika
from flask_mail import Mail , Message
from flask import request

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587  # 
app.config['MAIL_USE_TLS'] = True  # Enable TLS encryption
app.config['MAIL_USERNAME'] = 'lim263654@gmail.com'  
app.config['MAIL_PASSWORD'] = 'Warriors@240100'  

mail = Mail(app)

# Creating send_email to send email (No use of API)

@app.route('/')
def index():
    return 'Hello, World!'

def send_email(subject, recipient, body):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.json
    if not all(key in data for key in ['subject', 'recipient', 'body']):
        return 'Missing required fields', 400

    subject = data['subject']
    recipient = data['recipient']
    body = data['body']

    if send_email(subject, recipient, body):
        return 'Email sent successfully!'
    else:
        return 'Failed to send email', 500

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
