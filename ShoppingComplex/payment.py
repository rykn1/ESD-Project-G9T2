#  pip install stripe

from flask import Flask, render_template, url_for, request, abort, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import logging
import stripe

app = Flask(__name__, static_url_path="",static_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51OrELHATlCeKbEIxdOhbVW5Vii3DbYkWUtdqLtf88Mg4ATq96PtsfQRqbwbJbNikvmwedig7BQtED7vDb9zvQlKQ00FD5yU6c0'
app.config['STRIPE_SECRET_KEY'] = 'rk_test_51OrELHATlCeKbEIxLxwiyGHRkrXW3Di18YfJdrzOxGvI9mjz8QfGMR07VLy3FXsMiuRDrfNTbps32m5HBpV0ComF006WAL1TfX'


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
        
        cart_items = Cart.query.all()
        line_items=[]
        line_item={}
        
        for item in cart_items:
            line_item ={
                'price': item.id,
                'quantity': item.quantity,
            }
            line_items.append(line_item)
        print(line_items)
        checkout_session=stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        )
        print ("test")
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return redirect(checkout_session.url, code=303)


@app.route('/thanks')
def thanks():
    print("testest")
    return render_template('thanks.html')


@app.route('/get_emails', methods=['GET'])
def get_emails():
    customer_emails=[]
    try:
    # Retrieve list of charges from Stripe
        charge_list = stripe.Charge.list(limit=10)  # Limit to 10 charges for example

        # Extract customer email from each charge
        for charge in charge_list.auto_paging_iter():
            if charge.billing_details and charge.billing_details.email:
                customer_emails.append(charge.billing_details.email)

    except stripe.error.StripeError as e:
        # Handle any errors
        print(f"Error retrieving customer emails: {e}")

    return customer_emails


if __name__ == '__main__':
    app.run(port=5007, debug=True)