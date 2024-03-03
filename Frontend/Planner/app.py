# pip install google-generativeai  - if you haven't lol.

from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyAZGQei2hEWa3YBQtHuO6TBuYK6Si6ZFC4")

# Set up the model
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

@app.route('/plan', methods=['POST'])
def plan_itinerary():
    data = request.get_json()
    country = data.get('country')
    days = data.get('days')

    if not country or not days:
        return jsonify({'error': 'Missing country or days'})

    prompt = f"""Generate a travel itinerary for {country} for {days} number of day(s) in JSON format without backticks, where "Days" would be the key and "Activities" would be the list of activities to do on that specific day. Also generate "CountryCurrency" as the key and "CurrencySymbol" would be the 3 letter currency symbol of the country selected."""

    try:
        response = model.generate_content(prompt)
        print(response)
        itinerary_json = response.text
        itinerary = json.loads(itinerary_json) 
        return jsonify(itinerary)
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return jsonify({'error': 'An error occurred while generating the itinerary.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 