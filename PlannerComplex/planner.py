from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import amqp_connection
import sys
from os import environ
import pika
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

@app.route('/publish')
def publish():
    itinerary = request.get_json()
    print(itinerary)
    try:
        email = requests.get(email_URL)
        if email.status_code not in range(200,300):
            print("email error")
            return "email error"
        emailResult = emailResult.json()
        print(emailResult)
        return(emailResult)
#         message={"body":"""
# <html>
# <head></head>
# <body>
#     <h1 style="color: green;">Your payment is Successful!&#x2714;</h1>
#     <p style="font-size: 16px;">Thank you for your payment. Your transaction has been completed, and a receipt for your purchase has been emailed to you2.</p>

# </body>
# </html>
# """,
#                  "email":email,
#                  "subject":"Payment Email Confirmation1"}
#         msg=json.dumps(message)
#         print('\n\n-----Publishing the message routing_key=payment.notification-----')
#         channel.basic_publish(exchange=exchangename, routing_key="payment.notification", 
#         body=msg, properties=pika.BasicProperties(delivery_mode = 2)) 
#         print("\nPayment published to RabbitMQ Exchange.\n")
#         return jsonify('success')
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