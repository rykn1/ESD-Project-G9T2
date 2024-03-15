from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from invokes import invoke_http
import pika
import json
import amqp_connection
from os import environ

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

# maybe change to environ 
exchangename = "payment_handler"
exchangetype = "topic"


connection = amqp_connection.create_connection() 
channel = connection.channel()


#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  
    # Exit with a success status

# Put this in whenever u want to call Cart Database , include the one at Line21 too
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

# Inform the Payment Microservice to process the payment via http "POST"
# AMQP to send message to Notification Microservice upon successful payment 
# Notification Microservice to invoke and send email to user
# 2. AMQP message sent to Notifcation(consumer) ; direct message type



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5909, debug=True)