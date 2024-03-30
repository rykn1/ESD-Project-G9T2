FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY Arial_Unicode_MS.TTF ./
COPY ./text_replacement.py .
CMD [ "python", "./text_replacement.py" ]
