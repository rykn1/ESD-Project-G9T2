from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import traceback
import os

app = Flask(__name__)

def replace_text(image, box_coords, translated_text, text_color=(0, 0, 0), background_color=(255, 255, 255), transparency=0.5):
    replaced_image = image.copy()
    draw = ImageDraw.Draw(replaced_image)

    font_path = "./Arial_Unicode_MS.TTF"  
    font_size = 16
    font = ImageFont.truetype(font_path, font_size)

    for box, text in zip(box_coords, translated_text.split("\n")):
        x1, y1, x2, y2 = box

        while True:
            font = ImageFont.truetype(font_path, font_size)
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[:2]
            if text_width < (x2 - x1) * 0.9 and text_height < (y2 - y1) * 0.9:
                break
            font_size -= 1

        text_x = x1 + ((x2 - x1) - text_width) // 4
        text_y = y1 + ((y2 - y1) - text_height) // 4

        draw.rectangle([(x1, y1), (x2, y2)], fill=background_color)

        draw.text((text_x, text_y), text, fill=text_color, font=font)

    return replaced_image

@app.route('/replace_text', methods=['POST'])
def replace_text_endpoint():
    try:
        data = request.json
        print("Received data:", data)
        
        image_path = data.get('image_path')
        translated_text = data.get('translated_text')
        bounding_boxes = data.get('bounding_boxes', [])
        print("Translated text:", translated_text)
        print("Bounding boxes:", bounding_boxes)

        try:
            image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print("Error:", e)  
            traceback.print_exc()
            return jsonify({'error': 'Cannot open the specified image file'}), 500

        replaced_image = replace_text(image, bounding_boxes, translated_text)
        
        replaced_image_path = '/data/replaced_image.png'  
        replaced_image.save(replaced_image_path)
        print("Replaced image saved at:", replaced_image_path)

        return jsonify({'replaced_image_path': replaced_image_path}), 200

    except Exception as e:
        traceback.print_exc() 
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5013, debug=True)
