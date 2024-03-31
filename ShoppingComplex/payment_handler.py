from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os, sys
from flask_sqlalchemy import SQLAlchemy
import requests
from invokes import invoke_http
import pika
import json
import amqp_connection
from os import environ


app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}
db = SQLAlchemy(app)
CORS(app)

shopping_cart_url = environ.get('shopping_cart_url') or "http://localhost:5006/cart"
payment_url = environ.get('payment_url') or "http://localhost:5007/create-checkout-session"
notification_url = environ.get('notification_url') or "http://localhost:5008/notification"
recipient_url = environ.get('recipient_url') or "http://localhost:5007/get_emails"

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def json(self):
        return {"id": self.id, "name": self.name, "price": self.price, "quantity": self.quantity}


exchangename = "payment_handler"
exchangetype = "topic"
connection = amqp_connection.create_connection() 
channel = connection.channel()
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)
    
@app.route('/publish')
def publish():
    try:
        email = retrieve_recipient()
        message={"body":"""
<html>
<head></head>
<body>
    <h1 style="color: green;">Your payment is Successful!&#x2714;</h1>
    <p style="font-size: 16px;">Thank you for your payment. Your transaction has been completed, and a receipt for your purchase has been emailed to you2.</p>

</body>
</html>
""",
                 "email":email,
                 "subject":"Payment Email Confirmation1"}
        msg=json.dumps(message)
        print('\n\n-----Publishing the message routing_key=payment.notification-----')
        channel.basic_publish(exchange=exchangename, routing_key="payment.notification", 
        body=msg, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nPayment published to RabbitMQ Exchange.\n")
        return jsonify('success')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/paymentProcess", methods=["POST"])
def paymentProcess():
    
    cart_items= Cart.query.all()
    try:
        
        cart_items = Cart.query.all()
        line_items=[]
        line_item={}
        
        for item in cart_items:
            line_item ={
                'price': item.id,
                'quantity': item.quantity,
            }
            line_items.append(line_item)
        print('hand:', line_items)
        response = invoke_http(payment_url, method='POST', json=line_items)
        if 'url' in response:
            
            return redirect(response['url'])
        else:
            return jsonify({'error': 'Failed to create checkout session'}), 500
         
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
     
def retrieve_recipient():
    recipient = requests.get('http://payment:5007/get_emails')
    return recipient.json()[0]
    

        
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5909, debug=True)