from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/plan', methods=['POST'])
def plan_itinerary():
    data = request.json
    response = requests.post('http://127.0.0.1:5002/plan', json=data)
    return jsonify(response.json()), response.status_code

@app.route('/api/weather', methods=['POST'])
def get_weather():
    data = request.json
    response = requests.post('http://127.0.0.1:5004/weather', json=data)
    return jsonify(response.json()), response.status_code

@app.route('/api/exchange', methods=['GET'])
def get_exchange_rate():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount')
    response = requests.get(f'http://127.0.0.1:5003/exchange?from={from_currency}&to={to_currency}&amount={amount}')
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5001)