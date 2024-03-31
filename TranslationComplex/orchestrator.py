from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, send_from_directory
import requests
import traceback
from os import environ
from PIL import Image

app = Flask(__name__)

# Define Docker volume name
volume_name = 'my_volume'

# Docker volume directory where images will be saved
volume_directory = '/data'

text_detection_service_url = environ.get('detect_url') or "http://localhost:5011/detect_text" #or "http://localhost:8000/detect_text"
translation_service_url = environ.get('translate_url') or "http://localhost:5012/get_languages" #or "http://localhost:8000/get_languages"
translation_decipher_url = environ.get('decipher_url') or "http://localhost:5012/translate_text" #or "http://localhost:8000/translate_text"
text_replacement_service_url = environ.get('replacement_url') or "http://localhost:5013/replace_text" #or "http://localhost:8000/replace_text"
error_microservice_url = environ.get('error_url') or "http://localhost:5014/log_error" #or "http://localhost:8000/log_error"

def process_image(file, target_language):
    try:
        # Save the image file to Docker volume directory
        image_path = f'{volume_directory}/uploaded_image.jpg'
        file.save(image_path)

        # Step 1: Text Detection
        files = {'file': open(image_path, 'rb')}
        response = requests.post(text_detection_service_url, files=files)
        detection_result = response.json() if response.ok else None
        print(response.json())
        print('Detection Result:', detection_result)

        if detection_result:
            extracted_text = detection_result.get('extracted_text', '')
            bounding_boxes = detection_result.get('box_coords', [])  # Update to 'box_coords'
            print('Bounding Boxes:', bounding_boxes)  # Print bounding box coordinates

            # Step 2: Translation
            translation_payload = {'text': extracted_text, 'target_language': target_language}
            response = requests.post(translation_decipher_url, json=translation_payload)
            translated_text = response.json().get('translated_text', '') if response.ok else ''
            print('Translated Text:', translated_text)

            # Step 3: Text Replacement
            # new_image_path = os.path.join("../ocr_orchestrator", image_path)
            # im= Image.open(image_path)
            # im.save('static/uploaded_image.png')
            replacement_payload = {'image_path': image_path, 'translated_text': translated_text,
                                   'bounding_boxes': bounding_boxes}
            response = requests.post(text_replacement_service_url, json=replacement_payload)
            print('Replacement Response:', response.content)
            replaced_image_path = response.json().get('replaced_image_path', '') if response.ok else ''

            return replaced_image_path, translated_text

        else:
            log_error("Text detection failed.")
            return None, "Text detection failed."

    except Exception as e:
        error_message = str(e)
        traceback.print_exc()  # Print traceback for debugging
        log_error(error_message)
        return None, error_message

def log_error(error_message):
    try:
        response = requests.post(error_microservice_url, json={'error_message': error_message})
        if not response.ok:
            print("Failed to log error:", response.text)
    except Exception as e:
        print("Error while logging error:", str(e))

@app.route('/')
def index():
    try:
        # Fetch language data
        response = requests.get(translation_service_url)
        language_data = response.json() if response.ok else {'languages': []}

        return render_template('index.html', language_data=language_data)
    except Exception as e:
        return redirect(url_for('handle_error', error_msg=str(e)))

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        target_language = request.form['target_language']

        replaced_image_path, translated_text = process_image(file, target_language)

        if replaced_image_path:
            return render_template('result.html', replaced_image=replaced_image_path, translated_text=translated_text)
        else:
            return redirect(url_for('handle_error', error_msg="Failed to process the image"))

    except Exception as e:
        return redirect(url_for('handle_error', error_msg=str(e)))

@app.route('/download')
def download():
    # Path to the replaced image file
    replaced_image_path = f'{volume_directory}/replaced_image.png'

    # Send the file for download
    return send_file(replaced_image_path, as_attachment=True)

@app.route('/error')
def handle_error():
    error_message = request.args.get('error_msg', 'Unknown error occurred.')
    return render_template('error.html', error=error_message)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('/data', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5100, debug=True)
