from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import amqp_connection
import sys
from os import environ
import pika
import json
app = Flask(__name__)
CORS(app)
gemini_URL = environ.get('gemini_URL') or 'http://localhost:5002/plan'
weather_URL = environ.get('weather_URL') or 'http://localhost:5004/weather'
currency_URL = environ.get('currency_URL') or 'http://localhost:5003/exchange'
email_URL = environ.get('email_URL') or 'http://localhost:5010/email'

exchangename = "planner"
exchangetype = "topic"
connection = amqp_connection.create_connection()
channel = connection.channel()
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)
    # Exit with a success status

@app.route('/publish', methods=['POST'])
def publish():
    print('testtesttest')
    itinerary = request.json
    print(itinerary)
    #itinerary['Days'] -- list of days with key "Activities" : [activity1,2,3]
    #itinerary["country"] -- country
    id = itinerary['id']
    print(id)
    try:
        email = requests.post(email_URL,json=itinerary)
        print(email)
        if email.status_code not in range(200,300):
            print("email error")
            return "email error"
        print('testasda')
        emailResult = email.text
        print(emailResult)
        itinerary_details = json.loads(itinerary['body'])
        print(itinerary_details)
        
        message_body = f"""
        <html>
        <head></head>
        <body>
            <h1 style="color: green;">Here is your {len(itinerary_details['Days'])} Day itinerary to {itinerary_details['country']}!&#x2714;</h1>
            <div style="font-size: 16px;">
        """
        
        for day_number, day in enumerate(itinerary_details['Days'], start=1):
            message_body += f"<h2>Day {day_number}</h2><ul>"
            for activity in day['Activities']:
                message_body += f"<li>{activity}</li>"
            message_body += "</ul>"
        
        message_body += """
            </div>
        </body>
        </html>
        """

        message = {
            "body": message_body,
            "email": emailResult,  
            "subject": "Your itinerary by TravelBuddy!"
        }
        print(message)
        
        msg=json.dumps(message)
        print('\n\n-----Publishing the message routing_key=itinerary.notification-----')
        channel.basic_publish(exchange=exchangename, routing_key="itinerary.notification", 
        body=msg, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nPayment published to RabbitMQ Exchange.\n")
        return jsonify('success')
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/plan', methods=['POST'])
def plan_itinerary():
    print('testgh')
    data = request.json
    result = processPlanRequest(data)
    return result

def processPlanRequest(data):

    geminiResult = requests.post(gemini_URL, json=data)
    if geminiResult.status_code not in range(200,300):
        print("gemini error")
        return "gemini error"
    geminiResult = geminiResult.json()
    weatherResult = requests.post(weather_URL, json=data)
    if weatherResult.status_code not in range(200,300):
        print("weather error")
        return "weather error"
    weatherResult = weatherResult.json()
    print('wok')
    destCurr = geminiResult["CountryCurrency"]["CurrencySymbol"]
    currency_URLtemp = currency_URL + f"?from=SGD&to={destCurr}&amount=1"
    currencyResult = requests.get(currency_URLtemp)
    if currencyResult.status_code not in range(200,300):
        print("currency error")
        return "currency error"
    currencyResult = currencyResult.json()
    print('cok')
    return {
        "code":201,
        "data": {
            "itinerary":geminiResult,
            "weather":weatherResult,
            "exchange":currencyResult
        }
    }

    

    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)