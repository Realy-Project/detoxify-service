# Text scoring service

Recieves some list of tags or comments and returns its classification.

Based on `multilingual` model [https://github.com/unitaryai/detoxify](https://github.com/unitaryai/detoxify)
and works with `English`, `French`, `Spanish`, `Italian`, `Portuguese`, `Turkish` or `Russian` languages

## Run in docker

    docker build -t detoxify-service .
    docker run -d -p 8000:80 -e API_TOKEN=secret_token detoxify-service

or

    docker run -d -p 8000:80 -e API_TOKEN=secret_token serg123e/detoxify-service:latest

## Local run

    pip install -r requirements.txt
    cd app
    API_TOKEN=secret_token uvicorn app:app

## Test
    curl 'http://127.0.0.1:8000/detoxify/' -X POST -H 'Content-Type: application/json' -H "Authorization: secret_token" --data-raw '{"tags": ["тест"]}'


## Authentication

If the environment variable API_TOKEN is not set, you can make requests without authentication:

    curl 'http://127.0.0.1:8000/detoxify/' -X POST -H 'Content-Type: application/json' --data-raw '{"tags": ["traje","negro"]}'

###  Example response

```json
{
    "predictions":
    [
        {
            "traje":
            {
                "toxicity": 0.0013423995114862919,
                "severe_toxicity": 0.00011458800145192072,
                "obscene": 0.0012843833537772298,
                "identity_attack": 0.00020291536930017173,
                "insult": 0.0017864112742245197,
                "threat": 0.00015220811474137008,
                "sexual_explicit": 0.00008424278348684311
            }
        },
        {
            "negro":
            {
                "toxicity": 0.4326218068599701,
                "severe_toxicity": 0.0018967259675264359,
                "obscene": 0.006122534163296223,
                "identity_attack": 0.12131743878126144,
                "insult": 0.042863570153713226,
                "threat": 0.0013023156207054853,
                "sexual_explicit": 0.002164836972951889
            }
        },
        {
            "traje negro":
            {
                "toxicity": 0.03802017867565155,
                "severe_toxicity": 0.0001297694689128548,
                "obscene": 0.0007853837450966239,
                "identity_attack": 0.010957055725157261,
                "insult": 0.007239991798996925,
                "threat": 0.00027434166986495256,
                "sexual_explicit": 0.00016771270020399243
            }
        }
    ]
}
```
