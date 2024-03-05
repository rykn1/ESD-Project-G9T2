import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# GEMINI AI GENERATED RESPONSE LOL I HAVE NO IDEA HOW =(

# API Keys (Replace with your actual keys)
AI_SERVICE_URL = "http://127.0.0.1:5001/plan"
WEATHER_SERVICE_URL = "http://127.0.0.1:5003/weather"
CURRENCY_SERVICE_URL = "http://127.0.0.1:5002/exchange"

@app.route('/plan', methods=['POST'])
def plan_itinerary():
    data = request.get_json()
    country = data.get('country')
    days = data.get('days')

    if not country or not days:
        return jsonify({'error': 'Missing country or days'}), 400

    # Call AI service
    try:
        ai_response = requests.post(AI_SERVICE_URL, json=data)
        ai_response.raise_for_status()  # Check for errors
        itinerary = ai_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error calling AI service'}), 500

    # Call weather service
    try:
        weather_response = requests.post(WEATHER_SERVICE_URL, json={'country': country})
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except requests.exceptions.RequestException as e:
        weather_data = {'error': 'Error calling weather service'}  # Error handling

    # Call currency service
    try:
        currency_response = requests.get(
            CURRENCY_SERVICE_URL,
            params={
                'from': 'SGD', 
                'to': itinerary.get('CountryCurrency', {}).get('CurrencySymbol'),
                'amount': 1
            }
        )
        currency_response.raise_for_status()
        currency_data = currency_response.json()
    except requests.exceptions.RequestException as e:
        currency_data = {'error': 'Error calling currency service'}  # Error handling

    # Combine results
    combined_response = {
        'itinerary': itinerary,
        'weather': weather_data,
        'currencyRate': currency_data.get('result'),
        'currencyError': currency_data.get('error')
    }
    return jsonify(combined_response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)