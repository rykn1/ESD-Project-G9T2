from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/item'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)

CORS(app)

class Item(db.Model):
    __tablename__ = 'item'

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



@app.route("/item")
def get_all():
    itemList = db.session.scalars(db.select(Item)).all()

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


@app.route("/item/<int:id>")
def find_by_id(id):
    item = db.session.scalars(
    	db.select(Item).filter_by(id=id).limit(1)).first()

    if item:
        return jsonify(
            {
                "code": 200,
                "data": item.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item not found."
        }
    ), 404


@app.route("/item/<int:id>", methods=['POST'])
def create_book(id):
    if (db.session.scalars(
      db.select(Item).filter_by(id=id).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Item already exists."
            }
        ), 400


    data = request.get_json()
    item = Item(id, **data)


    try:
        db.session.add(item)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred creating the item."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": item.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5003, debug=True)