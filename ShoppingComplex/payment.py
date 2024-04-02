#  pip install stripe

from flask import Flask, render_template, url_for, request, abort, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import logging
import stripe
import os, sys
from os import environ

app = Flask(__name__, static_url_path="",static_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}
app.config['STRIPE_PUBLIC_KEY'] = ''
app.config['STRIPE_SECRET_KEY'] = ''


db = SQLAlchemy(app)

CORS(app)

    

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



stripe.api_key = app.config['STRIPE_SECRET_KEY']



@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    
    try:
        line_items=request.get_json()
        print ('pay', line_items)
        
        checkout_session=stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url="http://localhost/ESD-PROJECT-G9T2/ShoppingComplex/templates/thanks.html",
            cancel_url="http://localhost/ESD-PROJECT-G9T2/ShoppingComplex/templates/cancel.html",
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'url': checkout_session.url})

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')
    

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/get_emails', methods=['GET'])
def get_emails():
    customer_emails=[]
    try:
        charge_list = stripe.Charge.list(limit=10)  

        for charge in charge_list.auto_paging_iter():
            if charge.billing_details and charge.billing_details.email:
                customer_emails.append(charge.billing_details.email)
    
    except stripe.error.StripeError as e:
        print(f"Error retrieving customer emails: {e}")
    return customer_emails


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5007, debug=True)