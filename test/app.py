from flask import Flask, render_template, request, redirect, abort, send_file
import requests
from PIL import Image, ImageDraw, ImageFont
import os
import pytesseract


app = Flask(__name__)

# Set the path to Tesseract language data directory
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

# Function to perform text detection, translation, and text replacement
def process_image(image_path, target_language):
    # Read image
    img = Image.open(image_path)
    img_with_text = img.copy()  # Create a copy to overlay text with background
    draw = ImageDraw.Draw(img_with_text)

    # Define a threshold for confidence score
    threshold = 0.25

    # Perform text detection using Pytesseract
    # Specify languages to detect both English and Arabic text
    detections = pytesseract.image_to_data(img, lang='eng+ara+mal+jap', output_type=pytesseract.Output.DICT)

    # Check if detections dictionary is empty or does not contain necessary keys
    if not detections or 'text' not in detections or 'conf' not in detections:
        print("No text detected or unexpected format in detections dictionary.")
        return "", None

    # Initialize empty string for extracted text
    extracted_text = ""

    # Initialize empty list for bounding box coordinates
    box_coords = []

    # Iterate over the detected text regions
    for i in range(len(detections['text'])):
        text = detections['text'][i].strip()
        confidence = int(detections['conf'][i])

        # Filter out text regions below the confidence threshold and ensure text is not empty
        if confidence > threshold and text:
            x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]

            # Append the coordinates to the list
            box_coords.append((x, y, x + w, y + h))

            # Draw green box
            draw.rectangle([(x, y), (x + w, y + h)], outline="green")

            # Draw text in red inside the green box
            draw.text((x, y - 10), text, fill="red")

            extracted_text += text + "\n"  # Append extracted text

    # Save the processed image with bounding boxes
    processed_image_path = 'static/processed_image.jpg'
    img_with_text_rgb = img_with_text.convert('RGB')  # Convert to RGB mode
    img_with_text_rgb.save(processed_image_path)

    # Translate the extracted text using RapidAPI Deep Translate API
    translated_text = translate_text(extracted_text, target_language)

    # Perform text replacement using translated text and box coordinates
    replaced_image = replace_text(img, box_coords, translated_text)

    # Save the replaced image
    replaced_image_path = 'static/replaced_image.jpg'
    replaced_image_rgb = replaced_image.convert('RGB')  # Convert to RGB mode
    replaced_image_rgb.save(replaced_image_path)

    return translated_text, replaced_image_path

# Function to translate text using RapidAPI Deep Translate API
def translate_text(text, target_language):
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
        translated_text = response.json()['data']['translations']['translatedText']
        return translated_text
    else:
        print("Failed to translate. Please try again later.")
        return ""

# Function to replace text in the image with translated text
def replace_text(image, box_coords, translated_text, text_color=(0, 0, 0), background_color=(255, 255, 255), transparency=0.5):
    replaced_image = image.copy()
    draw = ImageDraw.Draw(replaced_image)

    # Define the font face and starting font size
    font_path = "Arial Unicode MS.ttf"  # Replace with the path to your font file
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)

    # Iterate over the bounding box coordinates and the translated text
    for box, text in zip(box_coords, translated_text.split("\n")):
        # Unpack the coordinates
        x1, y1, x2, y2 = box

        # Calculate the maximum font size to fit the text inside the bounding box
        while True:
            font = ImageFont.truetype(font_path, font_size)
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[:2]
            if text_width < (x2 - x1) * 0.9 and text_height < (y2 - y1) * 0.9:
                break
            font_size -= 1

        # Calculate the text position more centered within the bounding box
        text_x = x1 + ((x2 - x1) - text_width) // 4
        text_y = y1 + ((y2 - y1) - text_height) // 4

        # Draw a filled rectangle for semi-translucent background
        draw.rectangle([(x1, y1), (x2, y2)], fill=background_color)

        # Draw the translated text on the image
        draw.text((text_x, text_y), text, fill=text_color, font=font)

    return replaced_image

# to allow the translated image to be downloaded. (need to import send_file from flask)
@app.route('/download')
def download():
    # Path to the replaced image file
    replaced_image_path = 'static/replaced_image.jpg'

    # Send the file for download
    return send_file(replaced_image_path, as_attachment=True)

@app.route('/')
def index():
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2/languages"

    headers = {
        "X-RapidAPI-Key": "342731d95amsh83e40184d15719ep11f5ffjsna8e3ab0bffc3",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    language_data = response.json() if response.status_code == 200 else {'languages': []}

    return render_template('index.html', language_data=language_data)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        abort(400, "No file part")

    file = request.files['file']

    if file.filename == '':
        abort(400, "No selected file")

    if file:
        image_path = 'static/uploaded_image.jpg'
        file.save(image_path)

        # Get the selected language from the form
        target_language = request.form.get('target_language', 'en')

        # Process the uploaded image with the selected target language
        translated_text, replaced_image_path = process_image(image_path, target_language)

        return render_template('result.html', replaced_image=replaced_image_path, translated_text=translated_text)

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error=error), 400

if __name__ == '__main__':
    app.run(port=5003, debug=True)
