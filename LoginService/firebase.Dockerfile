FROM python:3-slim
WORKDIR /usr/src/app
COPY reqs.txt firebaseKey.json ./
RUN python -m pip install --no-cache-dir -r reqs.txt
COPY ./firebase.py .
CMD [ "python", "./firebase.py" ]