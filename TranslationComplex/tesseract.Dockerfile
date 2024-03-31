FROM python:3-slim
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY tessdata ./tessdata/
COPY Arial_Unicode_MS.TTF ./
COPY ./tesseract.py .
CMD [ "python", "./tesseract.py" ]