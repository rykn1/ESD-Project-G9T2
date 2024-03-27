from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os, sys
from flask_sqlalchemy import SQLAlchemy
import requests
from invokes import invoke_http
import pika
import json
import amqp_connection
# from os import environ

app = Flask(__name__)

# Connecting to 'Cart' Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}
db = SQLAlchemy(app)
CORS(app)

shopping_cart_url = "http://localhost:5006/cart"
payment_url = "http://localhost:5007/create-checkout-session"
notification_url = "http://localhost:5008/notification"

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


# AMQP connection
exchangename = "payment_handler"
exchangetype = "topic"
connection = amqp_connection.create_connection() 
channel = connection.channel()
#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  
    # Exit with a success status
    


@app.route("/paymentProcess", methods=["POST"])
def payementProcess():
    
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
            # Use the URL for client-side redirection or as needed
            return redirect(response['url'])
        else:
            # Handle error or unexpected response
            return jsonify({'error': 'Failed to create checkout session'}), 500
         
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/payment_handler")
def valid_items():
    # Simple check of input format and data of the request are JSON
    results = invoke_http(shopping_cart_url, method='GET')
    print( type(results) )
    print()
    print(results)
   
    try:
        if results:
            # do the actual work
            # 1. Invoke the Payment Microservice
            result = processPayment(results)         
            print("\nReceived cart items in JSON:", result)
            return jsonify(result), result["code"]
        

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "payment_handler.py internal error: " + ex_str
        }), 500


def processPayment(items):
    # 1. Send order info {cart items}
    # Invoking the paymemnt microservice
    print('\n-----Invoking payment microservice-----')
    result = invoke_http(payment_url, method='POST', json=items)
    print("payment_result:", result)
    
    # Checking if the payemnt is successful (In the case of successful)
    
    # Whatever is inside here, shift it into the payment microservice
    code = result["code"]
    message = json.dumps(result)
    
    if code in range(200, 300):
        print('\n\n-----Publishing the message routing_key=payment.notification-----')
        channel.basic_publish(exchange=exchangename, routing_key="payment.notification", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nPayment published to RabbitMQ Exchange.\n")
    
    else:
        return {
            "code": 500,
            "data": {"payment": result},
            "message": "Payment Failed to process. Please try again."
        }




        
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5909, debug=True)