FROM python:3.11.4

WORKDIR /usr/src/app

COPY . .
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]