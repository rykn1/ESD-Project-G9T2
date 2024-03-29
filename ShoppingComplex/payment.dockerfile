FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt amqp.reqs.txt
COPY ./payment.py .
CMD [ "python", "./payment.py" ]