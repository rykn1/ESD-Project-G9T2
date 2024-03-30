FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY templates ./templates/
COPY tessdata ./tessdata/
COPY Arial_Unicode_MS.TTF ./
COPY ./orchestrator.py .
CMD [ "python", "./orchestrator.py" ]
