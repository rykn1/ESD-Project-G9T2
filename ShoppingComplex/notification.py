import amqp_connection 
import json 
import pika
from email.message import EmailMessage
import ssl
import smtplib





email_sender = 'lim263654@gmail.com'
email_password = 'mzktuipjgxecxhvw'

notification_queue_name = "Notification"


def receiveNotification(channel):
    try:
        channel.basic_consume(queue=notification_queue_name, on_message_callback=callback, auto_ack=True)
        print('Notification: Consuming from queue:', notification_queue_name)
        channel.start_consuming()  
    
    except pika.exceptions.AMQPError as e:
        print(f"notification: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("notification: Program interrupted by user.") 


def callback(channel, method, properties, body): 
    try:
        order = json.loads(body)
        processPaymentLog(order)  
        print(send_email(order['body'],order['email'],order['subject']))  
    except Exception as e:
        print(f"Error processing message and sending email: {e}")
    print()
    

def processPaymentLog(order):
    print("notification: Recording an order log:")
    print(order['email'])





def send_email(body,receipient,subject):
    try:
        print(receipient)        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = receipient
        em['Subject'] = subject

        em.set_content(body)  
        em.add_alternative(body, subtype='html')  


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, receipient, em.as_string())
        print("Email sent!")
        return ({'message': 'Email sent successfully'})
    except Exception as e:
        print("Error:", e)
        
    




if __name__ == '__main__':
    print("notification: Getting Connection")
    connection = amqp_connection.create_connection() 
    print("notification: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)
    
    
    




