from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import traceback
import os

app = Flask(__name__)

# Function to replace text in the image with translated text
def replace_text(image, box_coords, translated_text, text_color=(0, 0, 0), background_color=(255, 255, 255), transparency=0.5):
    replaced_image = image.copy()
    draw = ImageDraw.Draw(replaced_image)

    # Define the font face and starting font size
    font_path = "./Arial_Unicode_MS.ttf"  # Replace with the path to your font file
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

@app.route('/replace_text', methods=['POST'])
def replace_text_endpoint():
    try:
        #current_directory = os.getcwd()
        #return current_directory
        # Extract data from the request
        data = request.json
        print("Received data:", data)
        
        image_path = data.get('image_path')
        translated_text = data.get('translated_text')
        bounding_boxes = data.get('bounding_boxes', [])
        print("Translated text:", translated_text)
        print("Bounding boxes:", bounding_boxes)

        try:
            # Load the image
            image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print("Error:", e)  # Print the actual exception message for debugging
            traceback.print_exc()
            return jsonify({'error': 'Cannot open the specified image file'}), 500

        # Replace text in the image with translated text
        replaced_image = replace_text(image, bounding_boxes, translated_text)

        # Save replaced image
        replaced_image_path = './static/replaced_image.png'  # Change extension based on your preference
        replaced_image.save(replaced_image_path)
        print("Replaced image saved at:", replaced_image_path)

        # Return path to replaced image
        return jsonify({'replaced_image_path': replaced_image_path}), 200

    except Exception as e:
        traceback.print_exc()  # Print traceback for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5013, debug=True)
