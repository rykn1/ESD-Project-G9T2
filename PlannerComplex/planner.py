from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from os import environ
app = Flask(__name__)
CORS(app)

gemini_URL = environ.get('gemini_URL') or 'http://localhost:5002/plan'
weather_URL = environ.get('weather_URL') or 'http://localhost:5004/weather'
currency_URL = environ.get('currency_URL') or 'http://localhost:5003/exchange'



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