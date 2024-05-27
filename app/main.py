from fastapi import FastAPI, Form, Request
from typing import List, Dict, Any
from pydantic import BaseModel
from detoxify import Detoxify
from fastapi.responses import HTMLResponse, JSONResponse
import re

app = FastAPI()

# Load the model, on first run will download ~1Gb
model = Detoxify('multilingual')

class TextInput(BaseModel):
    tags: List[str]

@app.post("/detoxify/")
async def detoxify(request: Request, tags: str = Form(None)):
    if request.headers.get("Content-Type") == "application/json":
        json_body = await request.json()
        input_text = json_body['tags']
    else:
        input_text = re.split(r'\r\n|[\r\n]', tags) if tags else []

    concatenated_text = " ".join(input_text)
    all_texts = input_text + [concatenated_text]
    
    predictions = model.predict(all_texts)
    
    labeled_predictions = [{text: {k: v[i] for k, v in predictions.items()}} for i, text in enumerate(all_texts)]
    
    response_data = {
        "predictions": labeled_predictions
    }
    
    return JSONResponse(response_data)

@app.get("/", response_class=HTMLResponse)
async def form_post():
    return """
    <html>
        <body>
            <h2>Detoxify Model Test Form</h2>
            <form action="/detoxify/" method="post">
                <textarea name="tags" rows="10" cols="30"></textarea><br>
                <input type="submit">
            </form>
        </body>
    </html>
    """
