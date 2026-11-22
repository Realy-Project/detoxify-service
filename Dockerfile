FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Models live on a persistent volume and are downloaded once, not baked into the image.
ENV MODEL_DIR=/models \
    MALLOC_ARENA_MAX=2
VOLUME /models
EXPOSE 80

COPY app /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
