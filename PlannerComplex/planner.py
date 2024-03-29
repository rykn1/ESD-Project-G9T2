from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
print('asd')
@app.route('/api/plan', methods=['POST'])
def plan_itinerary():
    data = request.json
    result = processPlanRequest(data)
    return result

def processPlanRequest(data):

    geminiResult = requests.post('http://127.0.0.1:5002/plan', json=data)
    if geminiResult.status_code not in range(200,300):
        print("gemini error")
        return "gemini error"
    geminiResult = geminiResult.json()
    weatherResult = requests.post('http://127.0.0.1:5004/weather', json=data)
    if weatherResult.status_code not in range(200,300):
        print("weather error")
        return "weather error"
    weatherResult = weatherResult.json()
    print('wok')
    destCurr = geminiResult["CountryCurrency"]["CurrencySymbol"]
    currencyResult = requests.get(f'http://127.0.0.1:5003/exchange?from=SGD&to={destCurr}&amount=1')
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