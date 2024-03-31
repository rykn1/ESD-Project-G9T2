from flask import Flask, request, jsonify
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract
app = Flask(__name__)

os.environ['TESSDATA_PREFIX'] = './tessdata'

def process_image(image_path):
    try:
        img = Image.open(image_path)
        img_with_text = img.copy() 
        draw = ImageDraw.Draw(img_with_text)
        threshold = 0.15

        detections = pytesseract.image_to_data(img, lang='eng+ara+mal+spa+fra+ita+tur+de', output_type=pytesseract.Output.DICT)
        print('test3')
        if not detections or 'text' not in detections or 'conf' not in detections:
            error_message = "No text detected or unexpected format in detections dictionary."
            print(error_message)
            return "", None, None, error_message
        print('test3.5')
        extracted_text = ""

        box_coords = []

        arabic_font_path = "Arial_Unicode_MS.TTF"  
        print('test3.6')
        arabic_font = ImageFont.truetype(arabic_font_path, size=14) 

        for i in range(len(detections['text'])):
            text = detections['text'][i].strip()
            confidence = int(detections['conf'][i])

          
            if confidence > threshold and text:
                x, y, w, h = detections['left'][i], detections['top'][i], detections['width'][i], detections['height'][i]

                
                box_coords.append((x, y, x + w, y + h))

                
                print("Bounding box coordinates:", (x, y, x + w, y + h))

               
                draw.rectangle([(x, y), (x + w, y + h)], outline="green")

   
                draw.text((x, y - 10), text, fill="red", font=arabic_font)

                extracted_text += text + "\n"

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
        
        image_path = "uploaded_image.jpg"
        file.save(image_path)
        print('Image path works')

        
        extracted_text, img_with_text, box_coords, error_message = process_image(image_path)

        if extracted_text:
            processed_image_path = 'processed_image.jpg'
            img_with_text.save(processed_image_path)  
            return jsonify({'extracted_text': extracted_text, 'processed_image_path': processed_image_path, 'box_coords': box_coords}), 200
        else:
            return jsonify({'error': 'Failed to detect text'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5011, debug=True)