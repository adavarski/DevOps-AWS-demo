FROM python:3.7.2-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py .

EXPOSE 8888

CMD python app.py
