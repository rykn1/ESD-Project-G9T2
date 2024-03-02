# pip install google-generativeai   if you haven't lol.

from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

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

prompt_parts = [
  "Itinerary Parameters country",
  "Itinerary Generated ",
  "Itinerary Parameters days",
  "Itinerary Generated ",
  "Itinerary Parameters Generate an Itinerary in JSON format for country using days as a key",
  "Itinerary Generated ",
]

response = model.generate_content(prompt_parts)
print(response.text)

@app.route('/plan', methods=['POST'])
def plan_itinerary():
    data = request.get_json()
    country = data.get('country')
    days = data.get('days')

    if not country or not days:
        return jsonify({'error': 'Missing country or days'})

    # Construct your prompt carefully 
    prompt = f"""Generate a travel itinerary for {country} for {days} number of days in JSON format, where "Days" would be the key and "Activities" would be the list of activities to do on that specific day"""

    try:
        response = model.generate_content(prompt)
        itinerary_json = response.text
        return jsonify(itinerary_json) 
    except Exception as e:  
        print(f"Error generating itinerary: {e}") 
        return jsonify({'error': 'An error occurred while generating the itinerary.'}), 500

if __name__ == '__main__':
    app.run(debug=True) 