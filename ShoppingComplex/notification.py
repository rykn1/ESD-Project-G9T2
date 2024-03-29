import amqp_connection 
import json 
import pika
from email.message import EmailMessage
import ssl
import smtplib

# from payment_handler import retrieve_receipient


#calling of this url has to be done in the composite microservice aka payment_handler
# customer_email_url='http://127.0.0.1:5007/get_emails'
# customer_email_url='http://payment/get_emails'


email_sender = 'lim263654@gmail.com'
email_password = 'mzktuipjgxecxhvw'

notification_queue_name = "Notification"

email_receiver = retrieve_receipient()

def receiveNotification(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=notification_queue_name, on_message_callback=callback, auto_ack=True)
        print('Notification: Consuming from queue:', notification_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"notification: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("notification: Program interrupted by user.") 


# Is this necessary?   
def callback(channel, method, properties, body): # required signature for the callback; no return
    try:
        # print(body[0])
        order = json.loads(body)
        processPaymentLog(order)  # Process log if needed
        print(send_email(order['body'],order['email'],order['subject']))  # Now calling send_email directly here
    except Exception as e:
        print(f"Error processing message and sending email: {e}")
    print()
    # print("\n notification: Received a payment log by " + __file__)
    

def processPaymentLog(order):
    print("notification: Recording an order log:")
    print(order['email'])

# We need to export receiver, subject and body from payment handler
# subject = "Payment Email Confirmation"

# This part will be retrieved from the shoppingcart.py



def send_email(body,receipient,subject):
    try:
        # response = requests.get(customer_email_url)
        # if response.status_code == 200:
        #     customer_emails = response.json()
        #     if customer_emails:
                # email_receiver = customer_emails[0]     
        print(receipient)        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = receipient
        em['Subject'] = subject
        # em.set_content(msg)

        em.set_content(body)  # Set the plain text content
        em.add_alternative(body, subtype='html')  # Add the HTML content

        # Connect to SMTP server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, receipient, em.as_string())
        print("Email sent!")
        return ({'message': 'Email sent successfully'})
            # else:
            #     print("No customer emails found.")
        # else:
        #     print("Failed to retrieve customer emails:", response.status_code)
    except Exception as e:
        print("Error:", e)
        
    




if __name__ == '__main__':
    print("notification: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("notification: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)
    
    
    




