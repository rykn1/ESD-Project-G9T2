
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Make your openweather API key
OPENWEATHERMAP_API_KEY = ""

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    country = data.get('country')
    if not country:
        return jsonify({'error': 'Missing country'}), 400

    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={country}&appid={OPENWEATHERMAP_API_KEY}"

    try:
        response = requests.get(api_url) 
        weather_data = response.json()
        temperature_c = round(weather_data['main']['temp']-273.15,1)
        print(weather_data)
        return jsonify({
            'temperature': temperature_c,
            'description': weather_data['weather'][0]['description']
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error fetching weather data'}), 500 

if __name__ == '__main__':
    app.run(debug=True, port=5004)
