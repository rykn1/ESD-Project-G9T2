FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
RUN pip install google-generativeai
COPY ./generative_ai.py .
CMD [ "python", "./generative_ai.py" ]