import firebase_admin
from firebase_admin import credentials
from flask import Flask,request, jsonify
from flask_cors import CORS

cred = credentials.Certificate("./firebaseKey.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)
CORS(app)

@ap

