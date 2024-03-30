from flask import Flask, request, jsonify
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract

app = Flask(__name__)

# Set the path to Tesseract language data directory
os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files\\Tesseract-OCR\\tessdata'

# Function to perform text detection
def process_image(image_path):
    try:
        # Read image
        img = Image.open(image_path)
        img_with_text = img.copy()  # Create a copy to overlay text with background
        draw = ImageDraw.Draw(img_with_text)

        # Define a threshold for confidence score
        threshold = 0.15

        # Perform text detection using Pytesseract
        detections = pytesseract.image_to_data(img, lang='eng+ara+mal+spa+fra+ita+tur+de', output_type=pytesseract.Output.DICT)

        # Check if detections dictionary is empty or does not contain necessary keys
        if not detections or 'text' not in detections or 'conf' not in detections:
            error_message = "No text detected or unexpected format in detections dictionary."
            print(error_message)
            return "", None, None, error_message

        # Initialize empty string for extracted text
        extracted_text = ""

        # Initialize empty list for bounding box coordinates
        box_coords = []

        # Load a font that supports Arabic characters
        arabic_font_path = "./Arial_Unicode_MS.ttf"  # Replace with the path to your Arabic font file
        arabic_font = ImageFont.truetype(arabic_font_path, size=14)  # Adjust the size as needed

        # Iterate over the detected text regions
        for i in range(len(detections['text'])):
            text = detections['text'][i].strip()
            confidence = int(detections['conf'][i])

            # Filter out text regions below the confidence threshold and ensure text is not empty
            if confidence > threshold and text:
                x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]

                # Append the coordinates to the list
                box_coords.append((x, y, x + w, y + h))

                # Print the coordinates to the console
                print("Bounding box coordinates:", (x, y, x + w, y + h))

                # Draw green box
                draw.rectangle([(x, y), (x + w, y + h)], outline="green")

                # Draw text in red inside the green box
                # Specify the font parameter with the Arabic font
                draw.text((x, y - 10), text, fill="red", font=arabic_font)

                extracted_text += text + "\n"  # Append extracted text

        return extracted_text, img_with_text, box_coords, None
    except Exception as e:
        error_message = f"An error occurred during text detection: {str(e)}"
        print(error_message)
        return "", None, None, error_message

@app.route('/detect_text', methods=['POST'])
def detect_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded image
        image_path = "uploaded_image.jpg"
        file.save(image_path)
        print('Image path works')

        # Process the uploaded image
        extracted_text, img_with_text, box_coords, error_message = process_image(image_path)

        if extracted_text:
            processed_image_path = 'processed_image.jpg'
            img_with_text.save(processed_image_path)  # Save the processed image with text overlay
            return jsonify({'extracted_text': extracted_text, 'processed_image_path': processed_image_path, 'box_coords': box_coords}), 200
        else:
            return jsonify({'error': 'Failed to detect text'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5011, debug=True)