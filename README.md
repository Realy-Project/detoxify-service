# Text scoring service


## Run in docker

    docker build -t detoxify_service .
    docker run -d -p 8000:80 detoxify_service

## Local run

    pip install -r requirements.txt
    cd app
    uvicorn main:app

## Test
    curl 'http://127.0.0.1:8000/detoxify/' -X POST -H 'Content-Type: application/json' --data-raw '{"tags": ["asd","bsd"]}'

