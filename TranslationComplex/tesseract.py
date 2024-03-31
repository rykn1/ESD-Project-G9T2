from flask import Flask, request, jsonify
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract
app = Flask(__name__)

# Set the path to Tesseract language data directory
os.environ['TESSDATA_PREFIX'] = './tessdata'

print ('dog')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5016, debug=True)