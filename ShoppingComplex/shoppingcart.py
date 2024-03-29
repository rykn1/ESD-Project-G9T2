from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

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

@app.route("/cart")
def get_all ():
    itemList = db.session.scalars(db.select(Cart)).all()

    if len(itemList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "item": [item.json() for item in itemList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items."
        }
    ), 404
    
@app.route("/cart", methods=['POST'])
def add_items():
    data = request.json
    id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')  
      
    existing_item = Cart.query.filter_by(id=id).first()
    new_item = None
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = Cart(id=id, name=name, price=price, quantity=quantity)
        db.session.add(new_item)
        
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500
    
    if new_item:  # Check if new_item is defined
        print(json.dumps(new_item.json(), default=str)) # convert a JSON object to a string and print
        print()

    return jsonify(
        {
            "code": 201,
            "data": new_item.json() if new_item else None  # Return new_item.json() if new_item is defined, otherwise return None
        }
    ), 201

@app.route("/cart/<string:id>", methods=['DELETE'])
def delete_item(id):
    item = db.session.scalars(db.select(Cart).filter_by(id=id).limit(1)).first()
    print(item)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "id": id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "id": id
            },
            "message": "Item not found."
        }
    ), 404

@app.route("/totalprice", methods=['GET'])
def get_total_price():
    cart_items = Cart.query.all()
    
    if cart_items:
        return jsonify (
            {
                "code": 200,
                "data": {
                    "totalprice": sum(item.price * item.quantity for item in cart_items)
                }
            }
        )
    return jsonify(
        {
            "code": 200,
            "data": {
                    "totalprice": 0
                }
        }
    ), 404
    
@app.route("/clear-cart", methods=["POST"])
def clear_cart():
    
    try:
        cart_items = Cart.query.all()
        if cart_items:
            for item in cart_items:
                db.session.delete(item)
                db.session.commit()
        
        return jsonify({'message': 'Cart cleared successfully.'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
            

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5006, debug=True)