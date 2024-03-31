FROM python:3-slim
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6