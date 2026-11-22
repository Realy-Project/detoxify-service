#!/bin/sh
set -e
# Download and quantize the model into the persistent volume if it is not there yet.
# Runs in its own process so the memory used while building is released before the server starts.
python -m model_store
exec uvicorn app:app --host 0.0.0.0 --port 80
