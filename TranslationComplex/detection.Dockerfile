FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY tessdata ./tessdata/
COPY Arial_Unicode_MS.TTF ./
COPY ./detection.py .
CMD [ "python", "./detection.py" ]
