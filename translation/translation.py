from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/get_languages')
def get_languages():
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2/languages"
    headers = {
        "X-RapidAPI-Key": "342731d95amsh83e40184d15719ep11f5ffjsna8e3ab0bffc3",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    language_data = response.json() if response.status_code == 200 else {'languages': []}
    return jsonify(language_data), response.status_code

@app.route('/translate_text', methods=['POST'])
def translate_text():
    data = request.json
    #return data
    text = data.get('text')
    target_language = data.get('target_language')
    #return target_language

    if not text or not target_language:
        return jsonify({'error': 'Missing text or target language'}), 400

    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {
        "q": text,
        "target": target_language
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "342731d95amsh83e40184d15719ep11f5ffjsna8e3ab0bffc3",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        #return response.json()
        translations = response.json().get('data', {}).get('translations', [])
        #return translations
        if translations:
            translated_text = translations.get('translatedText')
            if translated_text:
                return jsonify({'translated_text': translated_text}), 200
    return jsonify({'error': 'Failed to translate or no translation available'}), response.status_code

if __name__ == '__main__':
    app.run(port=5002, debug=True)
