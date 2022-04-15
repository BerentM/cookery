FROM python:3.10.4-buster

WORKDIR /home/root/api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "cookery.api:api", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
