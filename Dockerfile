FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from detoxify import Detoxify; model = Detoxify('multilingual')"
EXPOSE 80

COPY app /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
