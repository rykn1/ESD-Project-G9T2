FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http_amqp.reqs.txt
COPY ./notification.py .
CMD [ "python", "./notification.py" ]