import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 299}

db = SQLAlchemy(app)
#test
CORS(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    body = db.Column(db.String(1000), nullable=True)

    def __init__(self,id,email):
        self.id = id
        self.email = email
        self.body = None

    def json(self):
        return {"id": self.id, "email": self.email, "body": self.body}

cred = credentials.Certificate("firebaseKey.json")
firebase_admin.initialize_app(cred)

# @app.route('/user', methods=['GET'])
# def get_user():
    

@app.route('/user', methods=['POST'])
def create_user():
    print('test')
    data = request.json
    id = data['id']
    email = data['email']
    if (db.session.scalars(
        db.select(User).filter_by(id=id).
        limit(1)
    ).first()
    ):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "id": id
                    },
                    "message": "User already exists."
                }
            ), 400
    



    user = User(id, email)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred creating the user."
            }
        ), 500




    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

@app.route('/updatebody', methods=['POST'])
def update_body():
    data = request.json
    id = data['id']
    user = db.session.scalars(
        db.select(User).filter_by(id=id).limit(1)).first()
    if user:
        try:
            user.body += data['body']
            db.session.commit()
        except:
            return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred updating the database."
            }
        ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "message": "User not found"
            }
        )
    return jsonify(
        {
            "code": 204,
            "message": "Updated successfully"
        }
    )


@app.route('/email', methods=['POST'])
def get_email():
    data = request.json
    id = data['id']
    user = auth.get_user(id)
    return user.email

@app.route('/body', methods=['POST'])
def get_body():
    data = request.json
    id = data['id']
    user = db.session.scalars(
        db.select(User).filter_by(id=id).limit(1)).first()
    
    if user:
        print(user.json())
        return jsonify(
            {
                "code": 200,
                "data": user.json()['body']
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5010)