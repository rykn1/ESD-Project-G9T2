from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection
from os import environ

app = Flask(__name__)
CORS(app)

exchange_name = "payment_handler"
exchange_type = "direct"

connection = amqp_connection.create_connection()
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchange_name, exchange_type):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status




# HTTP GET all the shopping items from shopping cart {listingID}

# 1. Items sent to Payment for confirmation 

# 2. AMQP message sent to Notifcation(consumer) ; direct message type

